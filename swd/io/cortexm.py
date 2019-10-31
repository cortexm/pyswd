"""IO registers for Cortex-M
"""

# pylint: disable=too-few-public-methods

from swd.bitfield import MemRegister as _MemRegister


class Cpuid(_MemRegister):
    """CPUID register definition"""
    _NAME = 'CPUID'
    _ADDRESS = 0xe000ed00
    _FIELDS = (
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


class Aircr(_MemRegister):
    """AIRCR register definition"""
    _NAME = 'AIRCR'
    _ADDRESS = 0xe000ed0c
    _FIELDS = (
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


class Dhcsr(_MemRegister):
    """DHCSR register definition"""
    _NAME = 'DHCSR'
    _ADDRESS = 0xe000edf0
    _FIELDS = (
        ('C_DEBUGEN', 1),
        ('C_HALT', 1),
        ('C_STEP', 1),
        ('C_MASKINTS', 1),
        (None, 1),
        ('C_SNAPSTALL', 1),
        (None, 10),
    )


class DhcsrWrite(Dhcsr):
    """DHCSR register definition write access"""
    _NAME = 'DHCSR_W'
    _FIELDS = Dhcsr._FIELDS + (
        ('DBGKEY', 16, (
            (0xa05f, 'KEY'),
        ), ),
    )


class DhcsrRead(Dhcsr):
    """DHCSR register definition read access"""
    _NAME = 'DHCSR_R'
    _FIELDS = Dhcsr._FIELDS + (
        ('S_REGRDY', 1),
        ('S_HALT', 1),
        ('S_SLEEP', 1),
        ('S_LOCKUP', 1),
        (None, 4),
        ('S_RETIRE_ST', 1),
        ('S_RESET_ST', 1),
        (None, 6),
    )


class Demcr(_MemRegister):
    """DEMCR register definition"""
    _NAME = 'DEMCR'
    _ADDRESS = 0xe000edfc
    _FIELDS = (
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
