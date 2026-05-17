# CLAUDE.md — Deluxe Homeart Infrared HA Integration

## Project overview

Home Assistant custom integration for Deluxe Homeart LED candles (remote model FB-0001, EAN 745114424044). Sends NEC infrared commands via the HA `infrared` component. IR codes were reverse-engineered from the physical remote using a BroadLink RM4 Pro.

Repository: `https://github.com/Splint77/Deluxe-Homeart-Infrared-HA`

## File structure

```
custom_components/schou_infrared/
├── __init__.py          # Entry setup / teardown
├── manifest.json        # Integration metadata
├── config_flow.py       # UI config flow — selects infrared emitter entity
├── const.py             # Deluxe HomeartCode enum with to_command()
├── entity.py            # Base entity — availability tracking, _send_command()
├── light.py             # LightEntity + RestoreEntity — on/off/brightness step
├── button.py            # 6 button entities — brightness up/down + 4 timers
├── strings.json         # UI strings (source of truth)
├── translations/
│   └── en.json          # English translations (kept in sync with strings.json)
└── brand/               # Brand assets — served by HA brands proxy API
    ├── icon.png          # 256×256
    ├── icon@2x.png       # 512×512
    ├── logo.png          # 678×148 — white text recoloured dark for light backgrounds
    └── logo@2x.png       # 1356×296
```

## Key constraints

### infrared-protocols version
The HA `infrared` component (introduced in **HA 2026.4.0**) pins `infrared-protocols==2.0.0`. In this version `NECCommand` lives in a flat module:

```python
from infrared_protocols.commands import NECCommand  # correct for 2.0.0
```

Do NOT use `from infrared_protocols.commands.nec import NECCommand` — that path only exists in 3.x and causes an `ImportError` at config flow load time.

### IR protocol
- **Standard NEC** (address `0x00`): ON, OFF, Timer 2H/4H/6H/8H
- **Extended NEC** (address `0x08B7`): Brightness up/down — 16-bit address, no address parity

### Assumed state
The candles have no feedback channel. `_attr_assumed_state = True` on the light entity. State is tracked locally and persisted via `RestoreEntity`.

### Brightness
Stepwise only — no absolute brightness control. Each call to `turn_on(brightness_step_pct=...)` or pressing a brightness button sends one IR command. Local brightness estimate is adjusted by `_BRIGHTNESS_STEP = 25` (~10% of 255) per press.

### Broadcast IR
All candles in IR range respond to every command simultaneously. There is no way to address individual candles.

## HACS requirements

- `hacs.json` is present at the repo root with `homeassistant: "2026.4.0"`
- The GitHub repository **must have topics set** (Settings → About → Topics). HACS validation fails without at least one topic. Recommended: `hacs`, `homeassistant`, `home-assistant`, `infrared`

## Brand assets

Brand images are sourced from the Deluxe Homeart website logo (`https://www.deluxehomeart.com/media/site/1/unknown.png`). The original logo has white text on a transparent background (designed for dark backgrounds). The `logo.png` and `logo@2x.png` files have had their text pixels recoloured to dark grey (`#282828`) to be readable on HA's light-coloured card backgrounds.

Placed in `brand/` per the HA brands proxy API introduced in the [2026-02-24 developer blog post](https://developers.home-assistant.io/blog/2026/02/24/brands-proxy-api/). No extra configuration needed — HA serves these automatically.

## manifest.json key order

HA validation requires: `domain`, `name`, then remaining keys in alphabetical order.
