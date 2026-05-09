"""Constants for the DeluxeHomeart Infrared integration."""

from enum import IntEnum

from infrared_protocols.commands.nec import NECCommand

DOMAIN = "deluxe_homeart_infrared"
CONF_INFRARED_ENTITY_ID = "infrared_entity_id"

_BRIGHTNESS_NEC_ADDRESS = 0x08B7  # Extended NEC — no address parity


class DeluxeHomeartCode(IntEnum):
    """IR command codes for the DeluxeHomeart FB-0001 remote."""

    ON = 0x5E
    OFF = 0x0C
    BRIGHTNESS_UP = 0x12
    BRIGHTNESS_DOWN = 0x10
    TIMER_2H = 0x46
    TIMER_4H = 0x40
    TIMER_6H = 0x15
    TIMER_8H = 0x19

    def to_command(self) -> NECCommand:
        """Return a NECCommand for this button press."""
        if self in (DeluxeHomeartCode.BRIGHTNESS_UP, DeluxeHomeartCode.BRIGHTNESS_DOWN):
            # Brightness buttons use Extended NEC (16-bit address, no inverse check)
            return NECCommand(address=_BRIGHTNESS_NEC_ADDRESS, command=self.value)
        return NECCommand(address=0x00, command=self.value)
