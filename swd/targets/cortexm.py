"""Cortex-Mx definitions
"""

import time
import swd.io.cortexm as _io_cm
import swd.targets.stm32 as _stm32
import swd.targets.cortexm0 as _cortexm0
import swd.targets.cortexm0p as _cortexm0p
import swd.targets.cortexm3 as _cortexm3
import swd.targets.cortexm4 as _cortexm4
import swd.targets.cortexm7 as _cortexm7
import swd.targets.cortexm23 as _cortexm23
import swd.targets.cortexm33 as _cortexm33


class CortexMException(Exception):
    """CortexM general exception"""


class CortexMNotDetected(Exception):
    """Exception"""


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

    def create_io(self):
        """Create IO registers"""
        cpuid = _io_cm.Cpuid(self._swd)
        implementer = cpuid.cached.named_value('IMPLEMENTER')
        partno = cpuid.cached.named_value('PARTNO')
        if implementer != 'ARM' or partno is None:
            raise CortexMNotDetected(
                f"Unknown MCU with CPUID: 0x{cpuid.cached.raw:08x}")
        self._swd.append_io({
            cpuid,
            _io_cm.Aircr(self._swd),
            _io_cm.DhcsrWrite(self._swd),
            _io_cm.DhcsrRead(self._swd),
            _io_cm.Demcr(self._swd),
        })

    def __init__(self, swd, expected_parts):
        self._swd = swd
        self.create_io()
        cpuid = self._swd.reg('CPUID')
        self._implementer = cpuid.cached.named_value('IMPLEMENTER')
        self._core = cpuid.cached.named_value('PARTNO')

        if self._core not in self._TARGETS:
            raise CortexMNotDetected(
                f"Unsupported MCU with core: {self._core}")

        devices = self._TARGETS[self._core].DEVICES

        self._device = None
        for device in devices:
            family = device.get_family()
            try:
                parts = []
                if expected_parts:
                    for part in expected_parts:
                        if part.startswith(family):
                            parts.append(part)
                    if not parts:
                        continue
                self._device = device(self, parts)
            except _stm32.UnknownDevice:
                continue
            break

    @property
    def swd(self):
        """Return instance of SWD"""
        return self._swd

    @property
    def device(self):
        """Return instance of device"""
        return self._device

    @property
    def implementer(self):
        """Return implementer name"""
        return self._implementer

    @property
    def core(self):
        """Return core name"""
        return self._core

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

    def reset(self):
        """Reset"""
        self._swd.reg('DEMCR').set_bits({
            'VC_CORERESET': False})
        self._swd.reg('AIRCR').set_bits({
            'VECTKEY': 'KEY',
            'SYSRESETREQ': True})
        time.sleep(.01)

    def reset_halt(self):
        """Reset and halt"""
        self.halt()
        self._swd.reg('DEMCR').set_bits({
            'VC_CORERESET': True})
        self._swd.reg('AIRCR').set_bits({
            'VECTKEY': 'KEY',
            'SYSRESETREQ': True})
        time.sleep(.01)

    def halt(self):
        """Halt"""
        self._swd.reg('DHCSR_W').set_bits({
            'DBGKEY': 'KEY',
            'C_DEBUGEN': True,
            'C_HALT': True})

    def step(self):
        """Step"""
        self._swd.reg('DHCSR_W').set_bits({
            'DBGKEY': 'KEY',
            'C_DEBUGEN': True,
            'C_STEP': True})

    def run(self):
        """Enable debug"""
        self._swd.reg('DHCSR_W').set_bits({
            'DBGKEY': 'KEY',
            'C_DEBUGEN': True})

    def nodebug(self):
        """Disable debug"""
        self._swd.reg('DHCSR_W').set_bits({
            'DBGKEY': 'KEY',
            'C_DEBUGEN': False})

    def is_halted(self):
        """check if core is halted"""
        return self._swd.reg('DHCSR_R').value('S_HALT')
