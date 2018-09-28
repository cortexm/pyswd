"""Cortex-Mx definitions
"""


class CortexMException(Exception):
    """Exception"""


class CortexM():
    """Definitions for Cortex-M MCUs"""
    REGISTERS = [
        'R0', 'R1', 'R2', 'R3', 'R4', 'R5',
        'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12',
        'SP', 'LR', 'PC', 'PSR', 'MSP', 'PSP']

    AIRCR_REG = 0xe000ed0c
    DHCSR_REG = 0xe000edf0
    DEMCR_REG = 0xe000edfc
    DWTCTRL_REG = 0xe0001000
    BPCTRL_REG = 0xe0002000
    BPCOMP0_REG = 0xe0002008
    BPCOMP1_REG = 0xe000200c
    BPCOMP2_REG = 0xe0002010
    BPCOMP3_REG = 0xe0002014

    BPCTRL_KEY = 0x00000002
    BPCTRL_ENABLE = BPCTRL_KEY | 0x00000001
    BPCTRL_DISABLE = BPCTRL_KEY | 0x00000000

    BPCTRL_ENABLE = BPCTRL_KEY | 0x00000001
    BPCTRL_DISABLE = BPCTRL_KEY | 0x00000000

    AIRCR_KEY = 0x05fa0000
    AIRCR_SYSRESETREQ_BIT = 0x00000004
    AIRCR_SYSRESETREQ = AIRCR_KEY | AIRCR_SYSRESETREQ_BIT

    DHCSR_KEY = 0xa05f0000
    DHCSR_DEBUGEN_BIT = 0x00000001
    DHCSR_HALT_BIT = 0x00000002
    DHCSR_STEP_BIT = 0x00000004
    DHCSR_STATUS_HALT_BIT = 0x00020000
    DHCSR_DEBUGDIS = DHCSR_KEY
    DHCSR_DEBUGEN = DHCSR_KEY | DHCSR_DEBUGEN_BIT
    DHCSR_HALT = DHCSR_KEY | DHCSR_DEBUGEN_BIT | DHCSR_HALT_BIT
    DHCSR_STEP = DHCSR_KEY | DHCSR_DEBUGEN_BIT | DHCSR_STEP_BIT

    DEMCR_RUN_AFTER_RESET = 0x00000000
    DEMCR_HALT_AFTER_RESET = 0x00000001

    def __init__(self, swd):
        self._swd = swd

    @classmethod
    def _get_reg_index(cls, reg):
        if reg.upper() not in cls.REGISTERS:
            raise CortexMException("Not a register")
        return cls.REGISTERS.index(reg)

    def get_reg(self, reg):
        """Read register"""
        return self._swd.get_reg(CortexM._get_reg_index(reg))

    def set_reg(self, reg, data):
        """Read register"""
        return self._swd.set_reg(CortexM._get_reg_index(reg), data)

    def get_reg_all(self):
        """Read all registers"""
        return dict(zip(CortexM.REGISTERS, self._swd.get_reg_all()))

    def reset(self):
        """Reset"""
        self._swd.set_mem32(CortexM.DEMCR_REG, CortexM.DEMCR_RUN_AFTER_RESET)
        self._swd.set_mem32(CortexM.AIRCR_REG, CortexM.AIRCR_SYSRESETREQ)
        # self._swd.get_mem32(CortexM.AIRCR_REG)

    def reset_halt(self):
        """Reset and halt"""
        self._swd.set_mem32(CortexM.DHCSR_REG, CortexM.DHCSR_HALT)
        self._swd.set_mem32(CortexM.DEMCR_REG, CortexM.DEMCR_HALT_AFTER_RESET)
        self._swd.set_mem32(CortexM.AIRCR_REG, CortexM.AIRCR_SYSRESETREQ)
        # self._swd.get_mem32(CortexM.AIRCR_REG)

    def halt(self):
        """Halt"""
        self._swd.set_mem32(CortexM.DHCSR_REG, CortexM.DHCSR_HALT)

    def step(self):
        """Step"""
        self._swd.set_mem32(CortexM.DHCSR_REG, CortexM.DHCSR_STEP)

    def run(self):
        """Enable debug"""
        self._swd.set_mem32(CortexM.DHCSR_REG, CortexM.DHCSR_DEBUGEN)

    def nodebug(self):
        """Disable debug"""
        self._swd.set_mem32(CortexM.DHCSR_REG, CortexM.DHCSR_DEBUGDIS)

    def is_halted(self):
        """check if core is halted"""
        return self._swd.get_mem32(
            CortexM.DHCSR_REG) & CortexM.DHCSR_STATUS_HALT_BIT > 0

    # def get_num_breakpoints(self):
    #     """Return number of HW break points"""
    #     return (self._swd.get_mem32(CortexM.BPCTRL_REG) >> 4) & 0x0f

    # def break_point(self, id, address=None, enable=True):
    #     pass
