"""Light platform for the Schou Infrared integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.light import (
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import CONF_INFRARED_ENTITY_ID, SchouCode
from .entity import SchouEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Schou Infrared light from a config entry."""
    async_add_entities(
        [SchouLight(entry, entry.data[CONF_INFRARED_ENTITY_ID])]
    )


class SchouLight(SchouEntity, LightEntity, RestoreEntity):
    """Schou Infrared lamp — light entity."""

    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = {ColorMode.ONOFF}
    _attr_assumed_state = True
    _attr_icon = "mdi:floor-lamp"
    # Main entity for the device — name comes from the device name alone
    _attr_name = None

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialize the light entity."""
        super().__init__(entry, infrared_entity_id, unique_id_suffix="light")
        self._attr_is_on = False

    async def async_added_to_hass(self) -> None:
        """Restore last known state on startup."""
        await super().async_added_to_hass()
        if (state := await self.async_get_last_state()) is not None:
            self._attr_is_on = state.state == STATE_ON

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the lamp."""
        await self._send_command(SchouCode.ON)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the lamp."""
        await self._send_command(SchouCode.OFF)
        self._attr_is_on = False
        self.async_write_ha_state()
