"""Button platform for the Schou Infrared integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_INFRARED_ENTITY_ID, SchouCode
from .entity import SchouEntity

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class SchouButtonDescription(ButtonEntityDescription):
    """Describes a Schou Infrared button."""

    command_code: SchouCode


BUTTON_DESCRIPTIONS: tuple[SchouButtonDescription, ...] = (
    SchouButtonDescription(
        key="play_pause",
        translation_key="play_pause",
        icon="mdi:play-pause",
        command_code=SchouCode.PLAY_PAUSE,
    ),
    SchouButtonDescription(
        key="color",
        translation_key="color",
        icon="mdi:palette",
        command_code=SchouCode.COLOR,
    ),
    SchouButtonDescription(
        key="brightness",
        translation_key="brightness",
        icon="mdi:brightness-6",
        command_code=SchouCode.BRIGHTNESS,
    ),
    SchouButtonDescription(
        key="candle",
        translation_key="candle",
        icon="mdi:candle",
        command_code=SchouCode.CANDLE,
    ),
    SchouButtonDescription(
        key="speed",
        translation_key="speed",
        icon="mdi:speedometer",
        command_code=SchouCode.SPEED,
    ),
    SchouButtonDescription(
        key="white",
        translation_key="white",
        icon="mdi:lightbulb-outline",
        command_code=SchouCode.WHITE,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Schou Infrared buttons from a config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    async_add_entities(
        SchouButton(entry, infrared_entity_id, description)
        for description in BUTTON_DESCRIPTIONS
    )


class SchouButton(SchouEntity, ButtonEntity):
    """Schou Infrared timer button entity."""

    entity_description: SchouButtonDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        description: SchouButtonDescription,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(entry, infrared_entity_id, unique_id_suffix=description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Send the timer IR command."""
        await self._send_command(self.entity_description.command_code)
