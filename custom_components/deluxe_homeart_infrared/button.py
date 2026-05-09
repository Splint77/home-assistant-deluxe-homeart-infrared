"""Button platform for the DeluxeHomeart Infrared integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_INFRARED_ENTITY_ID, DeluxeHomeartCode
from .entity import DeluxeHomeartEntity

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class DeluxeHomeartButtonDescription(ButtonEntityDescription):
    """Describes a DeluxeHomeart Infrared button."""

    command_code: DeluxeHomeartCode


BUTTON_DESCRIPTIONS: tuple[DeluxeHomeartButtonDescription, ...] = (
    DeluxeHomeartButtonDescription(
        key="brightness_up",
        translation_key="brightness_up",
        icon="mdi:brightness-7",
        command_code=DeluxeHomeartCode.BRIGHTNESS_UP,
    ),
    DeluxeHomeartButtonDescription(
        key="brightness_down",
        translation_key="brightness_down",
        icon="mdi:brightness-5",
        command_code=DeluxeHomeartCode.BRIGHTNESS_DOWN,
    ),
    DeluxeHomeartButtonDescription(
        key="timer_2h",
        translation_key="timer_2h",
        icon="mdi:timer-outline",
        command_code=DeluxeHomeartCode.TIMER_2H,
    ),
    DeluxeHomeartButtonDescription(
        key="timer_4h",
        translation_key="timer_4h",
        icon="mdi:timer-outline",
        command_code=DeluxeHomeartCode.TIMER_4H,
    ),
    DeluxeHomeartButtonDescription(
        key="timer_6h",
        translation_key="timer_6h",
        icon="mdi:timer-outline",
        command_code=DeluxeHomeartCode.TIMER_6H,
    ),
    DeluxeHomeartButtonDescription(
        key="timer_8h",
        translation_key="timer_8h",
        icon="mdi:timer-outline",
        command_code=DeluxeHomeartCode.TIMER_8H,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DeluxeHomeart Infrared buttons from a config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    async_add_entities(
        DeluxeHomeartButton(entry, infrared_entity_id, description)
        for description in BUTTON_DESCRIPTIONS
    )


class DeluxeHomeartButton(DeluxeHomeartEntity, ButtonEntity):
    """DeluxeHomeart Infrared timer button entity."""

    entity_description: DeluxeHomeartButtonDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        description: DeluxeHomeartButtonDescription,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(entry, infrared_entity_id, unique_id_suffix=description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Send the timer IR command."""
        await self._send_command(self.entity_description.command_code)
