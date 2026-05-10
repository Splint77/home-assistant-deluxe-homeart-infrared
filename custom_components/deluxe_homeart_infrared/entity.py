"""Base entity for the Deluxe Homeart Infrared integration."""

from __future__ import annotations

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

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        unique_id_suffix: str,
    ) -> None:
        """Initialize the entity."""
        self._infrared_entity_id = infrared_entity_id
        self._attr_unique_id = f"{entry.entry_id}_{unique_id_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="Deluxe Homeart",
            model="FB-0001",
        )

    async def async_added_to_hass(self) -> None:
        """Subscribe to infrared emitter state changes."""
        await super().async_added_to_hass()

        @callback
        def _ir_state_changed(event: Event[EventStateChangedData]) -> None:
            new_state = event.data["new_state"]
            available = (
                new_state is not None and new_state.state != STATE_UNAVAILABLE
            )
            if available != self.available:
                _LOGGER.debug(
                    "Infrared entity %s is now %s",
                    self._infrared_entity_id,
                    "available" if available else "unavailable",
                )
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
        """Send an IR command via the infrared component."""
        await async_send_command(
            self.hass,
            self._infrared_entity_id,
            code.to_command(),
            context=self._context,
        )
