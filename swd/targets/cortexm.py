"""Cortex-Mx definitions
"""

import time
import pkg_resources
import swd.targets.mcu as _mcu
import swd.targets.cortexm0 as _cortexm0
import swd.targets.cortexm0p as _cortexm0p
import swd.targets.cortexm3 as _cortexm3
import swd.targets.cortexm4 as _cortexm4
import swd.targets.cortexm7 as _cortexm7
import swd.targets.cortexm23 as _cortexm23
import swd.targets.cortexm33 as _cortexm33

CORTEXM_SVD = "svd/cortex-m.svd"


class CortexMError(Exception):
    """CortexM general error"""


class CortexMException(CortexMError):
    """CortexM general exception"""


class CortexMNotDetected(Exception):
    """CortexM not detected exception"""


class CortexM:
    """Definitions for Cortex-M MCUs"""

    REGISTERS = [
        'R0', 'R1', 'R2', 'R3', 'R4', 'R5',
        'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12',
        'SP', 'LR', 'PC', 'PSR', 'MSP', 'PSP']

    _TARGETS = {
        'Cortex-M0': _cortexm0,
        'Cortex-M0+': _cortexm0p,
        'Cortex-M3': _cortexm3,
        'Cortex-M4': _cortexm4,
        'Cortex-M7': _cortexm7,
        'Cortex-M23': _cortexm23,
        'Cortex-M33': _cortexm33,
    }

    def __init__(self, swd, expcted_parts=None):
        self._swd = swd
        svd_file = pkg_resources.resource_filename('swd', CORTEXM_SVD)
        self._swd.load_svd(svd_file)
        cpuid = self.swd.io.SCB.CPUID
        if cpuid.cached.value in (0x00000000, 0xffffffff):
            raise CortexMNotDetected(
                f"CortexM not detected with CPUID: 0x{cpuid.cached.raw:08x}")
        self._implementer = cpuid.cached.IMPLEMENTER.named_value
        if self._implementer != 'ARM':
            raise CortexMNotDetected(
                f"Unsupported implementer: {self._implementer}")
        self._core = cpuid.cached.PARTNO.named_value
        if self._core not in self._TARGETS:
            raise CortexMNotDetected(
                f"Unsupported MCU with core: {self._core}")
        families = self._TARGETS[self._core].FAMILIES
        self._part = None
        unknow_part_error = None
        for family in families:
            try:
                self._part = family(self, expcted_parts)
                break
            except _mcu.UnknownMcuDetected as err:
                unknow_part_error = err
        if expcted_parts and not self._part:
            raise unknow_part_error

    @property
    def swd(self):
        """Return instance of SWD"""
        return self._swd

    @property
    def implementer(self):
        """Return implementer name"""
        return self._implementer

    @property
    def core(self):
        """Return core name"""
        return self._core

    @property
    def part(self):
        """Return instance part"""
        return self._part

    def name(self):
        """Return controller info string"""
        return f"{self._implementer}/{self._core}"

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

    def _reset(self):
        """Reset"""
        self.swd.io.SCB.AIRCR.cache.value = 0
        self.swd.io.SCB.AIRCR.cache.VECTKEY.value = "Vector Key"
        self.swd.io.SCB.AIRCR.cache.SYSRESETREQ.value = True
        self.swd.io.SCB.AIRCR.write_cache()
        time.sleep(.01)

    def reset(self):
        """Reset"""
        self.swd.io.DCB.DEMCR.VC_CORERESET.value = False
        self._reset()
        time.sleep(.01)

    def reset_halt(self):
        """Reset and halt"""
        self.halt()
        self.swd.io.DCB.DEMCR.VC_CORERESET.value = True
        self._reset()
        time.sleep(.01)

    def halt(self):
        """Halt"""
        self.swd.io.DCB.DHCSR.cache.value = 0
        self.swd.io.DCB.DHCSR.cache.DBGKEY.value = "Vector Key"
        self.swd.io.DCB.DHCSR.cache.C_DEBUGEN.value = True
        self.swd.io.DCB.DHCSR.cache.C_HALT.value = True
        self.swd.io.DCB.DHCSR.write_cache()

    def step(self):
        """Step"""
        self.swd.io.DCB.DHCSR.cache.value = 0
        self.swd.io.DCB.DHCSR.cache.DBGKEY.value = "Vector Key"
        self.swd.io.DCB.DHCSR.cache.C_DEBUGEN.value = True
        self.swd.io.DCB.DHCSR.cache.C_STEP.value = True
        self.swd.io.DCB.DHCSR.write_cache()

    def run(self):
        """Enable debug"""
        self.swd.io.DCB.DHCSR.cache.value = 0
        self.swd.io.DCB.DHCSR.cache.DBGKEY.value = "Vector Key"
        self.swd.io.DCB.DHCSR.cache.C_DEBUGEN.value = True
        self.swd.io.DCB.DHCSR.write_cache()

    def nodebug(self):
        """Disable debug"""
        self.swd.io.DCB.DHCSR.cache.value = 0
        self.swd.io.DCB.DHCSR.cache.DBGKEY.value = "Vector Key"
        self.swd.io.DCB.DHCSR.write_cache()

    def is_halted(self):
        """check if core is halted"""
        return self.swd.io.DCB.DHCSR.S_HALT.value
