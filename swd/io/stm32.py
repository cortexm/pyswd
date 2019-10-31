"""IO registers for STM32
"""

# pylint: disable=too-few-public-methods

from swd.bitfield import MemRegister as _MemRegister


class Idcode(_MemRegister):
    """CPUID register definition"""
    _NAME = 'DBGMCU_IDCODE'
    _FIELDS = (
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


class FlashSize(_MemRegister):
    """CPUID register definition"""
    _NAME = 'FLASH_SIZE'
    _FIELDS = (
        ('FLASH_SIZE', 16),
    )
    _SIZE = 16
