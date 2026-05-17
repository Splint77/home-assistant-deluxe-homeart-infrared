# Schou Infrared

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]

Home Assistant integration for Schou LED lamps controlled via infrared. Since the lamps have no feedback channel, state is assumed and tracked locally.

> This is not an official Schou integration. IR codes were reverse-engineered from the remote using a BroadLink RM4 Pro.

## Prerequisites

An IR transmitter registered with the Home Assistant [infrared][infrared_integration] integration is required, such as a [BroadLink][broadlink_integration] device or an [ESPHome][esphome_integration] device with `remote_transmitter`.

## Supported functionality

The integration creates the following entities:

| Platform | Entity | Description |
| :-- | :-- | :-- |
| `light` | Lamp | Turn on/off |
| `button` | Play/Pause | Toggle playback of light effects |
| `button` | Color | Cycle through colors |
| `button` | Brightness | Cycle brightness level |
| `button` | Candle | Toggle candle flicker effect |
| `button` | Speed | Cycle effect speed |
| `button` | White | Switch to white light |

All lamps in IR range are controlled simultaneously — there is no way to address individual lamps.

## Installation

1. In Home Assistant, go to **HACS** → **Integrations** → three-dot menu → **Custom repositories**
2. Add `https://github.com/Splint77/Schou-Infrared-HA` as an **Integration**
3. Search for **Schou Infrared** and download it
4. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services** → **+ Add Integration**
2. Search for **Schou Infrared**
3. Select the infrared emitter entity from the dropdown

<!-- Links -->
[hacs]: https://hacs.xyz/
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2026.svg
[releases-shield]: https://img.shields.io/github/release/Splint77/Schou-Infrared-HA.svg
[releases]: https://github.com/Splint77/Schou-Infrared-HA/releases
[infrared_integration]: https://www.home-assistant.io/integrations/infrared/
[broadlink_integration]: https://www.home-assistant.io/integrations/broadlink/
[esphome_integration]: https://www.home-assistant.io/integrations/esphome/
