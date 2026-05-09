# DeluxeHomeart Infrared

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]

Home Assistant integration for DeluxeHomeart LED candles controlled via infrared. Since the candles have no feedback channel, state is assumed and tracked locally.

> This is not an official DeluxeHomeart integration. IR codes were reverse-engineered from the FB-0001 remote using a BroadLink RM4 Pro.

## Prerequisites

An IR transmitter registered with the Home Assistant [infrared][infrared_integration] integration is required, such as a [BroadLink][broadlink_integration] device or an [ESPHome][esphome_integration] device with `remote_transmitter`.

## Supported functionality

The integration creates the following entities:

| Platform | Entity | Description |
| :-- | :-- | :-- |
| `light` | Candle | Turn on/off and adjust brightness |
| `button` | Brightness up | Increase brightness one step |
| `button` | Brightness down | Decrease brightness one step |
| `button` | Timer 2H | Start 2-hour auto-off timer |
| `button` | Timer 4H | Start 4-hour auto-off timer |
| `button` | Timer 6H | Start 6-hour auto-off timer |
| `button` | Timer 8H | Start 8-hour auto-off timer |

Brightness is stepwise — each press sends one IR command, equivalent to one press on the physical remote. There is no absolute brightness control.

Timers are one-shot commands. HA has no way to track remaining time.

All candles in IR range are controlled simultaneously — there is no way to address individual candles.

> Black and dark-coloured candles have significantly reduced IR reception range, as confirmed by the manufacturer.

## Installation

1. In Home Assistant, go to **HACS** → **Integrations** → three-dot menu → **Custom repositories**
2. Add `https://github.com/Splint77/DeluxeHomeart-Infrared-HA` as an **Integration**
3. Search for **DeluxeHomeart Infrared** and download it
4. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services** → **+ Add Integration**
2. Search for **DeluxeHomeart Infrared**
3. Select the infrared emitter entity from the dropdown

<!-- Links -->
[hacs]: https://hacs.xyz/
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2026.svg
[releases-shield]: https://img.shields.io/github/release/Splint77/DeluxeHomeart-Infrared-HA.svg
[releases]: https://github.com/Splint77/DeluxeHomeart-Infrared-HA/releases
[infrared_integration]: https://www.home-assistant.io/integrations/infrared/
[broadlink_integration]: https://www.home-assistant.io/integrations/broadlink/
[esphome_integration]: https://www.home-assistant.io/integrations/esphome/
