"""IO registers for STM32
"""

# pylint: disable=too-few-public-methods

from swd.bitfield import BitfieldMem as _BitfieldMem


class Idcode(_BitfieldMem):
    """CPUID register definition"""
    NAME = 'DBGMCU_IDCODE'
    _REGISTERS = (
        ('DEV_ID', 12, (
            (0xc20, "Cortex-M0"),
            (0xc60, "Cortex-M0+"),
            (0xc23, "Cortex-M3"),
            (0xc24, "Cortex-M4"),
            (0xc27, "Cortex-M7"),
            (0xd20, "Cortex-M23"),
            (0xd21, "Cortex-M33"),
        ), ),
        (None, 4),
        ('REV_ID_MINOR', 12),
        ('REV_ID_MAJOR', 4),
    )


class FlashSize(_BitfieldMem):
    """CPUID register definition"""
    NAME = 'FLASH_SIZE'
    _REGISTERS = (
        ('FLASH_SIZE', 16),
    )
    _BITS = 16
