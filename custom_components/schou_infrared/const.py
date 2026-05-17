"""Constants for the Schou Infrared integration."""

from enum import IntEnum

from infrared_protocols.commands import NECCommand

DOMAIN = "schou_infrared"
CONF_INFRARED_ENTITY_ID = "infrared_entity_id"

_NEC_ADDRESS = 0xFF02  # Extended NEC — no address parity


class SchouCode(IntEnum):
    """IR command codes for the Schou remote."""

    ON = 0x00
    OFF = 0x01
    PLAY_PAUSE = 0x02
    COLOR = 0x03
    BRIGHTNESS = 0x04
    CANDLE = 0x05
    SPEED = 0x06
    WHITE = 0x07
    
    def to_command(self) -> NECCommand:
        """Return a NECCommand for this button press."""
        return NECCommand(address=_NEC_ADDRESS, command=self.value)
