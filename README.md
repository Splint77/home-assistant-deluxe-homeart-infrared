# DeluxeHomeart Infrared — Home Assistant Integration

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]

Control your DeluxeHomeart LED candles from Home Assistant via infrared.

## Disclaimer

DeluxeHomeart ApS is not involved in any way with this integration.

The IR codes were reverse-engineered from the physical FB-0001 remote using a BroadLink RM4 Pro. Use at your own risk.

## Compatibility

This integration controls DeluxeHomeart (and compatible RealFlame) LED candles that use the **FB-0001 infrared remote** (EAN 745114424044).

All candles that respond to this remote are controlled together — IR is broadcast and there is no way to address individual candles.

> **Note:** Black and dark-coloured candles have significantly reduced IR reception range, as confirmed by the manufacturer.

> **Note:** Brightness adjustment is not supported by all candle models. The brightness buttons are still exposed but may have no effect on some candles.

### Required hardware

An IR transmitter registered with the Home Assistant **infrared** integration is required. Supported transmitters include:

| Hardware | HA Integration |
| :-- | :-- |
| BroadLink RM4 Pro (and similar) | [BroadLink][broadlink_integration] |
| ESPHome device with `remote_transmitter` | [ESPHome][esphome_integration] |
| Any other transmitter that registers an `infrared.*` entity | — |

## What it does

This integration sends NEC infrared commands to your candles via the HA `infrared` component. Since the candles have no feedback channel, all state is assumed and tracked locally.

The following entities are created per configured device:

| Platform | Entity | Description |
| :-- | :-- | :-- |
| `light` | Candle | Turn on/off and adjust brightness (step up/down) |
| `button` | Timer 2H | Start 2-hour auto-off timer |
| `button` | Timer 4H | Start 4-hour auto-off timer |
| `button` | Timer 6H | Start 6-hour auto-off timer |
| `button` | Timer 8H | Start 8-hour auto-off timer |

> **Brightness** is stepwise only — the remote has no absolute brightness control. Each press of the brightness button in HA sends one IR command, equivalent to one press on the physical remote.

> **Timers** are one-shot commands. HA has no way to track the remaining time or whether the timer is still active.

## Installation

Installation is done using [HACS][hacs] as a custom repository:

1. Go to your Home Assistant instance
1. Go to **HACS** → **Integrations** → click the three-dot menu → **Custom repositories**
1. Add `https://github.com/Splint77/home-assistant-deluxe-homeart-infrared` as an **Integration**
1. Click **+ Explore & Download Repositories** and search for **DeluxeHomeart Infrared**
1. Download the integration

## Configuration

Configuration is done via the Home Assistant interface.

1. Make sure your IR transmitter is set up and working (e.g. BroadLink or ESPHome)
1. Go to **Settings** → **Devices & Services** → click **+ Add Integration**
1. Search for **DeluxeHomeart Infrared** and select it
1. Select the infrared emitter entity to use from the dropdown

A new device named **DeluxeHomeart Infrared via \<emitter name\>** will be created with the light and timer button entities.

## Credits

IR codes sourced from:
- [stephanschuurman/com.stephanschuurman.candlelight](https://github.com/stephanschuurman/com.stephanschuurman.candlelight/blob/main/docs/ir-codes.md) — ON/OFF and timer codes
- Physical capture with BroadLink RM4 Pro — brightness codes

<!-- Links -->
[hacs]: https://hacs.xyz/
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2026.svg
[releases-shield]: https://img.shields.io/github/release/Splint77/home-assistant-deluxe-homeart-infrared.svg
[releases]: https://github.com/Splint77/home-assistant-deluxe-homeart-infrared/releases
[broadlink_integration]: https://www.home-assistant.io/integrations/broadlink/
[esphome_integration]: https://www.home-assistant.io/integrations/esphome/
