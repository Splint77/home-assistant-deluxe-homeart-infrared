"""Light platform for the DeluxeHomeart Infrared integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_BRIGHTNESS_STEP_PCT,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import CONF_INFRARED_ENTITY_ID, DeluxeHomeartCode
from .entity import DeluxeHomeartEntity

PARALLEL_UPDATES = 1

# Each brightness IR press moves the local estimate by this amount (best-effort assumed state)
_BRIGHTNESS_STEP = 25  # ~10% of 255


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DeluxeHomeart Infrared light from a config entry."""
    async_add_entities(
        [DeluxeHomeartLight(entry, entry.data[CONF_INFRARED_ENTITY_ID])]
    )


class DeluxeHomeartLight(DeluxeHomeartEntity, LightEntity, RestoreEntity):
    """DeluxeHomeart Infrared candle — light entity."""

    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_assumed_state = True
    _attr_icon = "mdi:candle"
    # Main entity for the device — name comes from the device name alone
    _attr_name = None

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialize the light entity."""
        super().__init__(entry, infrared_entity_id, unique_id_suffix="light")
        self._attr_is_on = False
        self._attr_brightness: int = 255

    async def async_added_to_hass(self) -> None:
        """Restore last known state on startup."""
        await super().async_added_to_hass()
        if (state := await self.async_get_last_state()) is not None:
            self._attr_is_on = state.state == STATE_ON
            if (brightness := state.attributes.get(ATTR_BRIGHTNESS)) is not None:
                self._attr_brightness = int(brightness)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on or adjust brightness."""
        if ATTR_BRIGHTNESS_STEP_PCT in kwargs:
            step_pct: float = kwargs[ATTR_BRIGHTNESS_STEP_PCT]
            if step_pct > 0:
                await self._send_command(DeluxeHomeartCode.BRIGHTNESS_UP)
                self._attr_brightness = min(
                    255, (self._attr_brightness or 128) + _BRIGHTNESS_STEP
                )
            else:
                await self._send_command(DeluxeHomeartCode.BRIGHTNESS_DOWN)
                self._attr_brightness = max(
                    1, (self._attr_brightness or 128) - _BRIGHTNESS_STEP
                )
        else:
            await self._send_command(DeluxeHomeartCode.ON)

        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the candle."""
        await self._send_command(DeluxeHomeartCode.OFF)
        self._attr_is_on = False
        self.async_write_ha_state()
