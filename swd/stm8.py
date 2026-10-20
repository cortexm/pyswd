"""STM8 definitions
"""
import time as _time


class Stm8Error(Exception):
    """Stm8 general error"""


class Stm8Exception(Stm8Error):
    """Stm8 general exception"""


class Stm8():
    """Definitions for STM8 MCUs"""
    REGISTERS = [
        'A', 'PCE', 'PCH', 'PCL', 'XH', 'XL', 'YH', 'YL', 'SPH', 'SPL', 'CC']
    REGISTERS_BASE = 0x7f00

    # assembled registers: name -> (first byte register, number of bytes)
    ASSEMBLED_REGISTERS = {
        'PC': ('PCE', 3),
        'X': ('XH', 2),
        'Y': ('YH', 2),
        'SP': ('SPH', 2),
    }

    SWIM_CSR = 0x7f80
    SWIM_CSR_SAFE_MASK = 0x80
    SWIM_CSR_NO_ACCESS = 0x40
    SWIM_CSR_SWIM_DM = 0x20
    SWIM_CSR_HS = 0x10
    SWIM_CSR_OSCOFF = 0x08
    SWIM_CSR_RST = 0x04
    SWIM_CSR_HSIT = 0x02
    SWIM_CSR_PRI = 0x01

    SWIM_DM_CSR2 = 0x7f99
    SWIM_DM_CSR2_SWBRK = 0x20
    SWIM_DM_CSR2_SWBKF = 0x10
    SWIM_DM_CSR2_STALL = 0x08
    SWIM_DM_CSR2_FLUSH = 0x01

    # debug module registers
    DM_BKR1 = 0x7f90
    DM_BKR2 = 0x7f93
    DM_CR1 = 0x7f96
    DM_CR1_WDGOFF = 0x80
    DM_CR1_BC = 0x38
    DM_CR1_BIR = 0x04
    DM_CR1_BIW = 0x02
    DM_CSR1 = 0x7f98
    DM_CSR1_STE = 0x40
    DM_CSR1_STF = 0x20
    DM_CSR1_RST = 0x10
    DM_CSR1_BRW = 0x08
    DM_CSR1_BK2F = 0x04
    DM_CSR1_BK1F = 0x02

    # breakpoint modes: name -> DM_CR1 control value
    # (BC2:BC0 << 3) | (BIR << 2) | (BIW << 1), per UM0470 Table 4.
    # Encodings verified on STM8L050J3.
    BREAKPOINT_MODES = {
        'disabled': 0x00,
        # data write/read on @=BK1 and data=BK2L
        'write': 0x02,
        'read': 0x04,
        'read_write': 0x06,
        # instruction fetch / data access within BK1..BK2 range
        'instruction_range': 0x08,
        'write_range': 0x0a,
        'read_range': 0x0c,
        'read_write_range': 0x0e,
        # instruction fetch / data access on @<=BK1 or BK2<=@
        'instruction_outside_range': 0x10,
        'write_outside_range': 0x12,
        'read_outside_range': 0x14,
        'read_write_outside_range': 0x16,
        # instruction fetch on @=BK1 then on @=BK2 (sequential)
        'instruction_then': 0x20,
        # data access on @=BK1 or @=BK2
        'write_two': 0x22,
        'read_two': 0x24,
        'read_write_two': 0x26,
        # instruction fetch on @=BK1 or @=BK2 (plain instruction breakpoint)
        'instruction': 0x28,
        # instruction fetch on @=BK1 / data access on @=BK2
        'instruction_data_write': 0x2a,
        'instruction_data_read': 0x2c,
        'instruction_data_read_write': 0x2e,
        # data write in stack on @<=BK1 combined with @=BK2 access
        'stack_write_instruction': 0x38,
        'stack_write': 0x3a,
        'stack_write_data_read': 0x3c,
        'stack_write_read_write': 0x3e,
    }

    # flash programming register layouts
    STM8S = {
        'CLK_CKDIVR': 0x50c6,
        'FLASH_PUKR': 0x5062,
        'FLASH_DUKR': 0x5064,
        'FLASH_IAPSR': 0x505f,
        'FLASH_CR2': 0x505b,
        'FLASH_NCR2': 0x505c,
        'BLOCK_SIZE': 64,
    }
    STM8L = {
        'CLK_CKDIVR': 0x50c0,
        'FLASH_PUKR': 0x5052,
        'FLASH_DUKR': 0x5053,
        'FLASH_IAPSR': 0x5054,
        'FLASH_CR2': 0x5051,
        'FLASH_NCR2': None,
        'BLOCK_SIZE': 128,
    }

    # FLASH_IAPSR bits
    IAPSR_WR_PG_DIS = 0x01
    IAPSR_PUL = 0x02
    IAPSR_EOP = 0x04
    IAPSR_DUL = 0x08

    # FLASH_CR2 bits
    CR2_STANDARD = 0x01
    CR2_FAST = 0x10
    CR2_OPTION = 0x80

    FLASH_PUKR_KEY1 = 0x56
    FLASH_PUKR_KEY2 = 0xae
    FLASH_DUKR_KEY1 = 0xae
    FLASH_DUKR_KEY2 = 0x56

    def __init__(self, swim, part='STM8S'):
        """Stm8 constructor

        Arguments:
            swim: instance of Swim
            part: part family ('STM8S' or 'STM8L') or dict with registers:
                CLK_CKDIVR, FLASH_PUKR, FLASH_DUKR, FLASH_IAPSR,
                FLASH_CR2, FLASH_NCR2 (optional), BLOCK_SIZE (optional)
        """
        self._swim = swim
        if isinstance(part, str):
            try:
                part = getattr(self, part.upper())
            except AttributeError:
                raise Stm8Exception("Unknown part: %s" % part)
        self._part = dict(part)

    @classmethod
    def _get_reg_index(cls, reg):
        if isinstance(reg, int):
            return reg  # allow user to override register name lookup

        reg = reg.upper()
        if reg in cls.ASSEMBLED_REGISTERS:
            reg = cls.ASSEMBLED_REGISTERS[reg][0]
        if reg not in cls.REGISTERS:
            raise Stm8Exception("Not a register")

        return cls.REGISTERS.index(reg)

    def _read8(self, address):
        """Read one byte from memory and return it as int"""
        return self._swim.read_mem8(address, 1)[0]

    def _write8(self, address, value):
        """Write one byte (int) into memory"""
        self._swim.write_mem8(address, bytes([value & 0xff]))

    def get_reg(self, reg):
        """Read register

        Arguments:
            reg: register name ('A', 'PCE', ..., or assembled: 'PC', 'X',
                'Y', 'SP') or register index

        Return:
            8, 16 or 24 bit number
        """
        name = reg.upper() if isinstance(reg, str) else None
        if name in self.ASSEMBLED_REGISTERS:
            first, size = self.ASSEMBLED_REGISTERS[name]
            address = self.REGISTERS_BASE + self.REGISTERS.index(first)
            data = self._swim.read_mem(address, size)
            return int.from_bytes(data, 'big')
        reg = self._get_reg_index(reg)
        return self._read8(self.REGISTERS_BASE + reg)

    def set_reg(self, reg, data):
        """Write register

        Arguments:
            reg: register name ('A', 'PCE', ..., or assembled: 'PC', 'X',
                'Y', 'SP') or register index
            data: 8, 16 or 24 bit number
        """
        name = reg.upper() if isinstance(reg, str) else None
        if name in self.ASSEMBLED_REGISTERS:
            first, size = self.ASSEMBLED_REGISTERS[name]
            address = self.REGISTERS_BASE + self.REGISTERS.index(first)
            self._swim.write_mem(address, data.to_bytes(size, 'big'))
            return
        reg = self._get_reg_index(reg)
        self._write8(self.REGISTERS_BASE + reg, data)

    def get_reg_all(self):
        """Read all registers

        Return:
            dictionary with register name as key and as value
            8, 16 or 24 bit number for each register
        """
        values = self._swim.read_mem(self.REGISTERS_BASE, len(self.REGISTERS))
        regs = dict(zip(self.REGISTERS, values))
        for name, (first, size) in self.ASSEMBLED_REGISTERS.items():
            index = self.REGISTERS.index(first)
            regs[name] = int.from_bytes(values[index:index + size], 'big')
        return regs

    def halt(self):
        """Halt CPU"""
        csr = self._read8(self.SWIM_DM_CSR2)
        self._write8(self.SWIM_DM_CSR2, csr | self.SWIM_DM_CSR2_STALL)

    def run(self):
        """Run CPU"""
        csr = self._read8(self.SWIM_DM_CSR2)
        self._write8(self.SWIM_DM_CSR2, csr & ~self.SWIM_DM_CSR2_STALL)

    def is_halted(self):
        """Check if CPU is halted

        Return:
            True if CPU is halted, or False if is running
        """
        csr = self._read8(self.SWIM_DM_CSR2)
        return bool(csr & self.SWIM_DM_CSR2_STALL)

    def _wait_dm_bits(self, address, mask, state, timeout=1.0):
        """Wait until mask bits of debug module register reach state

        Arguments:
            address: debug module register address
            mask: bits to test
            state: expected state of masked bits
            timeout: maximum waiting time in seconds

        Raise:
            Stm8Exception: on timeout
        """
        deadline = _time.monotonic() + timeout
        while _time.monotonic() < deadline:
            if bool(self._read8(address) & mask) == state:
                return
            _time.sleep(0.001)
        raise Stm8Exception(
            "Timeout waiting for debug module register 0x%04X" % address)

    def step(self, count=1):
        """Execute single instruction(s) in step mode

        CPU must be halted. Each step executes one instruction and stalls
        the CPU again (DM step mode, UM0470 section 4.10).

        Arguments:
            count: number of instructions to execute

        Raise:
            Stm8Exception: on timeout
        """
        for _ in range(count):
            csr1 = self._read8(self.DM_CSR1)
            csr2 = self._read8(self.SWIM_DM_CSR2)
            # enable step mode
            self._write8(self.DM_CSR1, csr1 | self.DM_CSR1_STE)
            # flush instruction pipeline and resume in one write (the
            # flush bit is only cleared by hardware once the CPU runs)
            self._write8(
                self.SWIM_DM_CSR2,
                (csr2 | self.SWIM_DM_CSR2_FLUSH)
                & ~self.SWIM_DM_CSR2_STALL)
            # DM stalls the CPU again after one instruction
            self._wait_dm_bits(
                self.SWIM_DM_CSR2, self.SWIM_DM_CSR2_STALL, True)
        # leave step mode disabled, so run() resumes normally
        self._write8(
            self.DM_CSR1, self._read8(self.DM_CSR1) & ~self.DM_CSR1_STE)

    def nodebug(self):
        """Run CPU without debug module

        Note:
            not available on STM8: the SWIM_DM bit in SWIM_CSR is write-1
            only (verified on STM8L050: writing 0 has no effect) and is
            cleared only by a hardware reset. The closest equivalent is
            reset(), after which the CPU runs without debug module.
        """
        raise Stm8Exception(
            "nodebug is not supported on STM8 "
            "(SWIM_DM can only be cleared by a reset)")

    def set_breakpoint(self, mode, address, data=None):
        """Set hardware break condition (UM0470 Table 4)

        The debug module has one break condition built from two breakpoint
        registers: BK1 holds the address, BK2 an optional second address or
        data compare value depending on the mode.

        Arguments:
            mode: one of BREAKPOINT_MODES keys. Common ones:
                'instruction': break on instruction fetch at address = BK1
                'write'/'read'/'read_write': break on data access at
                    address = BK1 (optionally matched with data = BK2L)
                'instruction_then': break on fetch at BK1, then at BK2
                _range modes: BK1..BK2 range ('*_outside_range' for the
                    complementary range)
            address: break address (BK1, 24 bits)
            data: second address (BK2) for range/two-address modes, or the
                data compare value (BK2, low 16 bits used) for
                'read'/'write'

        Raise:
            Stm8Exception: on invalid mode
        """
        if mode not in self.BREAKPOINT_MODES:
            raise Stm8Exception(
                "Unknown breakpoint mode: %s (available: %s)"
                % (mode, ', '.join(sorted(self.BREAKPOINT_MODES))))
        self._swim.write_mem(
            self.DM_BKR1, (address & 0xffffff).to_bytes(3, 'big'))
        if data is None:
            data = 0
        self._swim.write_mem(
            self.DM_BKR2, (data & 0xffffff).to_bytes(3, 'big'))
        # shared break condition (BC, BIR, BIW)
        cr1 = self._read8(self.DM_CR1)
        cr1 &= ~(self.DM_CR1_BC | self.DM_CR1_BIR | self.DM_CR1_BIW)
        cr1 |= self.BREAKPOINT_MODES[mode]
        self._write8(self.DM_CR1, cr1)
        self.clear_breakpoint_flags()

    def clear_breakpoint(self):
        """Disable break condition and reset breakpoint registers"""
        self._write8(
            self.DM_CR1,
            self._read8(self.DM_CR1)
            & ~(self.DM_CR1_BC | self.DM_CR1_BIR | self.DM_CR1_BIW))
        self._swim.write_mem(self.DM_BKR1, b'\xff\xff\xff')
        self._swim.write_mem(self.DM_BKR2, b'\xff\xff\xff')
        self.clear_breakpoint_flags()

    def clear_breakpoint_flags(self):
        """Clear BK1F, BK2F and BRW break flags in DM_CSR1"""
        csr1 = self._read8(self.DM_CSR1)
        self._write8(
            self.DM_CSR1,
            csr1 & ~(self.DM_CSR1_BK1F | self.DM_CSR1_BK2F
                     | self.DM_CSR1_BRW))

    def is_breakpoint_hit(self):
        """Check if a breakpoint condition was hit

        Return:
            True if BK1F or BK2F break flag is set in DM_CSR1
        """
        csr1 = self._read8(self.DM_CSR1)
        return bool(csr1 & (self.DM_CSR1_BK1F | self.DM_CSR1_BK2F))

    def _check_debug_mode(self):
        csr = self._read8(self.SWIM_CSR)
        if not csr & self.SWIM_CSR_SWIM_DM:
            raise Stm8Exception("SWIM not in debug mode")
        return csr

    def reset(self):
        """Reset MCU (SWIM disable after reset)"""
        csr = self._check_debug_mode()
        # disable SWIM after reset
        self._write8(self.SWIM_CSR, csr | self.SWIM_CSR_RST)
        # clear the stall bit
        self._write8(self.SWIM_DM_CSR2, 0)
        self._swim.srst()
        _time.sleep(0.001)

    def reset_halt(self):
        """Reset MCU and halt after reset"""
        csr = self._check_debug_mode()
        # disable SWIM after reset
        self._write8(self.SWIM_CSR, csr | self.SWIM_CSR_RST)
        # keep the stall bit set
        self._write8(self.SWIM_DM_CSR2, self.SWIM_DM_CSR2_STALL)
        self._swim.srst()
        _time.sleep(0.001)

    def unlock_flash(self):
        """Unlock FLASH for writing (PUKR)"""
        self._write8(self._part['FLASH_PUKR'], self.FLASH_PUKR_KEY1)
        self._write8(self._part['FLASH_PUKR'], self.FLASH_PUKR_KEY2)

    def unlock_data(self):
        """Unlock DATA EEPROM / option bytes for writing (DUKR)"""
        self._write8(self._part['FLASH_DUKR'], self.FLASH_DUKR_KEY1)
        self._write8(self._part['FLASH_DUKR'], self.FLASH_DUKR_KEY2)

    def wait_eop(self, retries=5):
        """Wait for end of programming (EOP in FLASH_IAPSR)

        Arguments:
            retries: number of retries

        Raise:
            Stm8Exception: on timeout or write protection
        """
        # t_prog per datasheets is 6ms typ, 6.6ms max, fast mode is 2x faster
        _time.sleep(0.006)
        while retries > 0:
            iapsr = self._read8(self._part['FLASH_IAPSR'])
            if iapsr & self.IAPSR_EOP:
                return
            if iapsr & self.IAPSR_WR_PG_DIS:
                raise Stm8Exception(
                    "Target page is write protected (UBC) or "
                    "read-out protection is enabled")
            retries -= 1
            _time.sleep(0.001)
        raise Stm8Exception("Timeout waiting for EOP")

    def _set_prg_mode(self, mode):
        self._write8(self._part['FLASH_CR2'], mode)
        if self._part['FLASH_NCR2'] is not None:
            self._write8(self._part['FLASH_NCR2'], ~mode)

    def _stall_cpu(self):
        csr = self._read8(self.SWIM_DM_CSR2)
        self._write8(self.SWIM_DM_CSR2, csr | self.SWIM_DM_CSR2_STALL)

    def _lock_flash(self):
        # reset DUL and PUL in IAPSR to disable flash and data writes
        iapsr = self._read8(self._part['FLASH_IAPSR'])
        self._write8(
            self._part['FLASH_IAPSR'],
            iapsr & ~(self.IAPSR_DUL | self.IAPSR_PUL))

    def write_flash_block(self, address, data, fast=True):
        """Write one FLASH block

        Arguments:
            address: block aligned address in FLASH memory
            data: list or bytes of block_size bytes to write
            fast: use fast programming mode

        Raise:
            Stm8Exception: on error
        """
        block_size = self._part['BLOCK_SIZE']
        data = bytes(data)
        if address % block_size:
            raise Stm8Exception(
                "Address is not aligned to block size %d" % block_size)
        if len(data) != block_size:
            raise Stm8Exception(
                "Block size mismatch (expected %d, got %d)"
                % (block_size, len(data)))
        # fastest clock
        self._write8(self._part['CLK_CKDIVR'], 0x00)
        # stall the CPU before block programming
        self._stall_cpu()
        # set programming mode
        self._set_prg_mode(self.CR2_FAST if fast else self.CR2_STANDARD)
        # unlock FLASH
        self.unlock_flash()
        # program the block
        self._swim.write_mem(address, data)
        self.wait_eop()
        # lock FLASH and DATA
        self._lock_flash()

    def write_option_block(self, address, data):
        """Write option bytes block

        Arguments:
            address: address of option bytes
            data: list or bytes of option bytes to write

        Raise:
            Stm8Exception: on error
        """
        data = bytes(data)
        # fastest clock
        self._write8(self._part['CLK_CKDIVR'], 0x00)
        # stall the CPU
        self._stall_cpu()
        # set option programming mode
        self._set_prg_mode(self.CR2_OPTION)
        # unlock option bytes / DATA EEPROM
        self.unlock_data()
        # option bytes are written one byte at a time
        for index, byte in enumerate(data):
            self._write8(address + index, byte)
            self.wait_eop()
        # lock FLASH and DATA
        self._lock_flash()
