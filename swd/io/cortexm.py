"""IO registers for Cortex-M
"""

# pylint: disable=too-few-public-methods

from swd.bitfield import BitfieldMem as _BitfieldMem


class Cpuid(_BitfieldMem):
    """CPUID register definition"""
    NAME = 'CPUID'
    _REGISTERS = (
        ('REVISION', 4),
        ('PARTNO', 12, (
            (0xc20, "Cortex-M0"),
            (0xc60, "Cortex-M0+"),
            (0xc23, "Cortex-M3"),
            (0xc24, "Cortex-M4"),
            (0xc27, "Cortex-M7"),
            (0xd20, "Cortex-M23"),
            (0xd21, "Cortex-M33"),
        ), ),
        ('ARCHITECTURE', 4),
        ('VARIANT', 4),
        ('IMPLEMENTER', 8, (
            (0x41, "ARM"),
        ), ),
    )
    _ADDRESS = 0xe000ed00


class Aircr(_BitfieldMem):
    """AIRCR register definition"""
    _NAME = 'AIRCR'
    _REGISTERS = (
        ('VECTRESET', 1),
        ('VECTCLRACTIVE', 1),
        ('SYSRESETREQ', 1),
        (None, 5),
        ('PRIGROUP', 3),
        (None, 4),
        ('ENDIANESS', 1),
        ('VECTKEY', 16, (
            (0x05fa, 'KEY'),
        ), ),
    )
    _ADDRESS = 0xe000ed0c


class Dhcsr(_BitfieldMem):
    """DHCSR register definition"""
    _NAME = 'DHCSR'
    _REGISTERS_COMMON = (
        ('C_DEBUGEN', 1),
        ('C_HALT', 1),
        ('C_STEP', 1),
        ('C_MASKINTS', 1),
        (None, 1),
        ('C_SNAPSTALL', 1),
        (None, 10),
    )
    _ADDRESS = 0xe000edf0


class DhcsrWrite(Dhcsr):
    """DHCSR register definition write access"""
    _REGISTERS = Dhcsr._REGISTERS_COMMON + (
        ('DBGKEY', 16, (
            (0xa05f, 'KEY'),
        ), ),
    )


class DhcsrRead(Dhcsr):
    """DHCSR register definition read access"""
    _REGISTERS = Dhcsr._REGISTERS_COMMON + (
        ('S_REGRDY', 1),
        ('S_HALT', 1),
        ('S_SLEEP', 1),
        ('S_LOCKUP', 1),
        (None, 4),
        ('S_RETIRE_ST', 1),
        ('S_RESET_ST', 1),
        (None, 6),
    )


class Demcr(_BitfieldMem):
    """DEMCR register definition"""
    _NAME = 'DEMCR'
    _REGISTERS = (
        ('VC_CORERESET', 1),
        (None, 3),
        ('VC_MMERR', 1),
        ('VC_NOCPERR', 1),
        ('VC_CHKERR', 1),
        ('VC_STATERR', 1),
        ('VC_BUSERR', 1),
        ('VC_INTERR', 1),
        ('VC_HARDERR', 1),
        (None, 5),
        ('MON_EN', 1),
        ('MON_PEND', 1),
        ('MON_STEP', 1),
        ('MON_REQ', 1),
        (None, 4),
        ('TRCENA', 1),
        (None, 7),
    )
    _ADDRESS = 0xe000edfc
