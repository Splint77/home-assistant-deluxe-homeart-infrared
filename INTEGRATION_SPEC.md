# Home Assistant Integration Spec: Deluxe Homeart Infrared

## Project Overview

**Integration name:** `deluxe_homeart_infrared`  
**Repository:** `Splint77/home-assistant-deluxe-homeart-infrared`  
**Description:** Home Assistant integration for Deluxe Homeart FB-0001 IR remote LED candles. Sends NEC infrared commands via the HA `infrared` component to control on/off, brightness, and 2/4/6/8-hour timers. Codes reverse-engineered from physical capture.

---

## The Physical Device

- **Remote model:** FB-0001 (Deluxe Homeart)
- **EAN:** 745114424044
- **Battery:** CR2025 3V (included)
- **Dimensions:** 9.9 cm × 4.3 cm, black
- **Controls on remote:**
  - ON button (center)
  - OFF button (center)
  - 2H, 4H, 6H, 8H timer buttons (ring around center)
  - Brightness + (up arrow)
  - Brightness − (down arrow)
- **Compatible with:** All Deluxe Homeart / RealFlame LED candles (indoor and outdoor). Note: black/dark coloured candles have reduced IR reception range.

---

## IR Protocol Documentation

All codes were verified by physical capture using a **BroadLink RM4 Pro**, then decoded in Python.

### Standard buttons — NEC protocol, Address 0x00

| Button     | CMD  | CMD_INV | Full 32-bit NEC  |
|------------|------|---------|------------------|
| ON         | 0x5E | 0xA1    | `0x00FF5EA1`     |
| OFF        | 0x0C | 0xF3    | `0x00FF0CF3`     |
| Timer 2H   | 0x46 | 0xB9    | `0x00FF46B9`     |
| Timer 4H   | 0x40 | 0xBF    | `0x00FF40BF`     |
| Timer 6H   | 0x15 | 0xEA    | `0x00FF15EA`     |
| Timer 8H   | 0x19 | 0xE6    | `0x00FF19E6`     |

### Brightness buttons — Extended NEC protocol, Address 0x08B7

The brightness buttons use **Extended NEC** (16-bit address). The address field `0x08B7` does NOT satisfy the standard NEC inverse checksum (intentional — this is valid Extended NEC).

| Button        | Address | CMD  | CMD_INV | Full 32-bit NEC  |
|---------------|---------|------|---------|------------------|
| Brightness +  | 0x08B7  | 0x12 | 0xED    | `0x08B712ED`     |
| Brightness −  | 0x08B7  | 0x10 | 0xEF    | `0x08B710EF`     |

### Protocol parameters

- **Carrier frequency:** 38 kHz
- **Header:** ~9.4 ms burst / ~4.7 ms space
- **Bit timing:** 562.5 µs burst + 562.5 µs space (0) or 1687.5 µs space (1)
- **Repeat:** Standard NEC repeat frame (9 ms burst / 2.25 ms space / 562.5 µs burst)

---

## Home Assistant Integration Design

### Integration type

This is a **config-entry based** integration that depends on the HA `infrared` component. It adds a `light` entity and a set of `button` entities representing the IR candle remote. Since the candle is one-way IR (no feedback), state is assumed/tracked locally.

### IR backend

The integration delegates all IR transmission to the HA `infrared` component. Any IR transmitter that registers as an `infrared.*` entity (e.g. BroadLink, ESPHome with remote_transmitter) is automatically available as a backend — no per-device code paths in this integration.

The user selects which `infrared` entity to use during config flow.

### Entity model

Implement as a **`light` entity** with:

| HA capability        | Maps to                        |
|----------------------|--------------------------------|
| `turn_on()`          | Send ON code                   |
| `turn_off()`         | Send OFF code                  |
| `brightness_step` +  | Send Brightness + code         |
| `brightness_step` −  | Send Brightness − code         |
| No color/color temp  | Not supported                  |

Additionally expose **`button` entities** for the timers:

| Button entity        | IR command  |
|----------------------|-------------|
| Timer 2H             | Timer 2H    |
| Timer 4H             | Timer 4H    |
| Timer 6H             | Timer 6H    |
| Timer 8H             | Timer 8H    |

Since the candle has no state feedback, the integration must track `is_on` locally (assume state).

### Config flow

```
User opens Add Integration → searches "Deluxe Homeart Infrared"
  Step 1: Select infrared emitter entity
    - Shows all available infrared.* entities via async_get_emitters()
    - Aborts with "no_emitters" if none are registered
  → Creates config entry with auto-generated title "Deluxe Homeart Infrared via {emitter_name}"
```

### File structure

```
custom_components/deluxe_homeart_infrared/
├── __init__.py            # Setup entry point
├── manifest.json          # Integration metadata
├── config_flow.py         # UI config flow
├── const.py               # Constants (IR codes enum, domain name)
├── entity.py              # Base entity (availability tracking, _send_command)
├── light.py               # Light entity (on/off/brightness_step)
├── button.py              # Timer button entities
├── strings.json           # UI strings
└── translations/
    └── en.json
```

### manifest.json

```json
{
  "domain": "deluxe_homeart_infrared",
  "name": "Deluxe Homeart Infrared",
  "version": "1.0.0",
  "documentation": "https://github.com/Splint77/home-assistant-deluxe-homeart-infrared",
  "dependencies": ["infrared"],
  "codeowners": ["@Splint77"],
  "integration_type": "device",
  "iot_class": "assumed_state",
  "config_flow": true
}
```

### const.py — IR code enum

```python
from enum import IntEnum
from infrared_protocols.commands.nec import NECCommand

DOMAIN = "deluxe_homeart_infrared"
CONF_INFRARED_ENTITY_ID = "infrared_entity_id"

_BRIGHTNESS_NEC_ADDRESS = 0x08B7  # Extended NEC — no address parity


class DeluxeHomeartCode(IntEnum):
    ON            = 0x5E
    OFF           = 0x0C
    BRIGHTNESS_UP = 0x12
    BRIGHTNESS_DOWN = 0x10
    TIMER_2H      = 0x46
    TIMER_4H      = 0x40
    TIMER_6H      = 0x15
    TIMER_8H      = 0x19

    def to_command(self) -> NECCommand:
        """Return a NECCommand for this button."""
        if self in (DeluxeHomeartCode.BRIGHTNESS_UP, DeluxeHomeartCode.BRIGHTNESS_DOWN):
            return NECCommand(address=_BRIGHTNESS_NEC_ADDRESS, command=self.value)
        return NECCommand(address=0x00, command=self.value)
```

### entity.py — base entity

```python
import logging
from homeassistant.components.infrared import async_send_command
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import Event, EventStateChangedData, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change_event
from .const import DOMAIN, DeluxeHomeartCode

_LOGGER = logging.getLogger(__name__)


class DeluxeHomeartEntity(Entity):
    """Deluxe Homeart Infrared base entity."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str, unique_id_suffix: str) -> None:
        self._infrared_entity_id = infrared_entity_id
        self._attr_unique_id = f"{entry.entry_id}_{unique_id_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="Deluxe Homeart",
            model="FB-0001",
        )

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        @callback
        def _ir_state_changed(event: Event[EventStateChangedData]) -> None:
            new_state = event.data["new_state"]
            available = new_state is not None and new_state.state != STATE_UNAVAILABLE
            if available != self.available:
                self._attr_available = available
                self.async_write_ha_state()

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._infrared_entity_id], _ir_state_changed
            )
        )
        ir_state = self.hass.states.get(self._infrared_entity_id)
        self._attr_available = (
            ir_state is not None and ir_state.state != STATE_UNAVAILABLE
        )

    async def _send_command(self, code: DeluxeHomeartCode) -> None:
        await async_send_command(
            self.hass,
            self._infrared_entity_id,
            code.to_command(),
            context=self._context,
        )
```

### light.py — key design points

All IR transmission goes through `_send_command(code)` inherited from `DeluxeHomeartEntity`. No direct calls to `broadlink` or `esphome` services anywhere in this integration.

```python
PARALLEL_UPDATES = 1
_BRIGHTNESS_STEP = 25  # ~10% of 255, applied per IR press to local brightness estimate

class DeluxeHomeartLight(DeluxeHomeartEntity, LightEntity, RestoreEntity):
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_assumed_state = True
    _attr_name = None  # main entity — displayed under device name only

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if (state := await self.async_get_last_state()) is not None:
            self._attr_is_on = state.state == STATE_ON
            if (brightness := state.attributes.get(ATTR_BRIGHTNESS)) is not None:
                self._attr_brightness = int(brightness)

    async def async_turn_on(self, **kwargs):
        if ATTR_BRIGHTNESS_STEP_PCT in kwargs:
            step_pct = kwargs[ATTR_BRIGHTNESS_STEP_PCT]
            if step_pct > 0:
                await self._send_command(DeluxeHomeartCode.BRIGHTNESS_UP)
                self._attr_brightness = min(255, (self._attr_brightness or 128) + _BRIGHTNESS_STEP)
            else:
                await self._send_command(DeluxeHomeartCode.BRIGHTNESS_DOWN)
                self._attr_brightness = max(1, (self._attr_brightness or 128) - _BRIGHTNESS_STEP)
        else:
            await self._send_command(DeluxeHomeartCode.ON)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._send_command(DeluxeHomeartCode.OFF)
        self._attr_is_on = False
        self.async_write_ha_state()
```

`button.py` also sets `PARALLEL_UPDATES = 1` and uses `DeluxeHomeartButtonDescription(ButtonEntityDescription)` with a `command_code: DeluxeHomeartCode` field.

---

## Key Implementation Notes

1. **One-way IR — assumed state.** The candle has no feedback channel. Track `_attr_is_on` as a boolean in the light entity and persist via `RestoreEntity`.

2. **Brightness is stepwise, not absolute.** The remote only has + and − buttons — there is no way to set an absolute brightness level. The HA light entity supports `brightness_step_pct` in `turn_on()`. Each call sends one IR command.

3. **Extended NEC for brightness.** The brightness codes use address `0x08B7` which is Extended NEC (16-bit address, no address parity). `NECCommand` handles this correctly — just pass `address=0x08B7`.

4. **Timer is not tracked.** The timer buttons send a one-shot IR command that starts an auto-off countdown in the candle. HA has no way to know the timer state. Timer buttons are modelled as `button` entities (momentary press).

5. **Multiple candles.** All Deluxe Homeart candles share the same IR address — one button press controls all candles in range simultaneously. This is by design (broadcast IR).

6. **Not all candles support brightness.** According to product documentation, brightness adjustment is not supported by all candle models. The integration still exposes the buttons.

7. **Black/dark candles** have significantly reduced IR reception range (confirmed by manufacturer).

---

## Sources

| Source | URL |
|--------|-----|
| IR codes (ON/OFF/timers) | https://github.com/stephanschuurman/com.stephanschuurman.candlelight/blob/main/docs/ir-codes.md |
| Brightness codes | Physical capture with BroadLink RM4 Pro (this session) |
| Homey app (loyasoft) | https://homey.app/da-dk/app/nl.loyasoft.deluxe_homeart/Deluxe-Homeart/ |
| Product info | https://www.koopeencadeautje.nl/en/deluxe-homeart-afstandsbediening.html |
| HA infrared integration | https://www.home-assistant.io/integrations/infrared/ |
| LG Infrared (reference impl) | https://www.home-assistant.io/integrations/lg_infrared/ |
| infrared-protocols library | https://github.com/home-assistant-libs/infrared-protocols |
| ESPHome transmit_nec | https://esphome.io/components/remote_transmitter.html |
