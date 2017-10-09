"""ST-Link/V2 protocol"""

import swd.stlinkcom as stlinkcom
import collections

class StlinkException(Exception):
    """Exception"""


class Stlink():
    """ST-Link protocol"""
    STLINK_GET_VERSION = 0xf1
    STLINK_DEBUG_COMMAND = 0xf2
    STLINK_DFU_COMMAND = 0xf3
    STLINK_SWIM_COMMAND = 0xf4
    STLINK_GET_CURRENT_MODE = 0xf5
    STLINK_GET_TARGET_VOLTAGE = 0xf7

    STLINK_MODE_DFU = 0x00
    STLINK_MODE_MASS = 0x01
    STLINK_MODE_DEBUG = 0x02
    STLINK_MODE_SWIM = 0x03
    STLINK_MODE_BOOTLOADER = 0x04

    STLINK_DFU_EXIT = 0x07

    STLINK_SWIM_ENTER = 0x00
    STLINK_SWIM_EXIT = 0x01

    STLINK_DEBUG_ENTER_JTAG = 0x00
    STLINK_DEBUG_STATUS = 0x01
    STLINK_DEBUG_FORCEDEBUG = 0x02
    STLINK_DEBUG_A1_RESETSYS = 0x03
    STLINK_DEBUG_A1_READALLREGS = 0x04
    STLINK_DEBUG_A1_READREG = 0x05
    STLINK_DEBUG_A1_WRITEREG = 0x06
    STLINK_DEBUG_READMEM_32BIT = 0x07
    STLINK_DEBUG_WRITEMEM_32BIT = 0x08
    STLINK_DEBUG_RUNCORE = 0x09
    STLINK_DEBUG_STEPCORE = 0x0a
    STLINK_DEBUG_A1_SETFP = 0x0b
    STLINK_DEBUG_READMEM_8BIT = 0x0c
    STLINK_DEBUG_WRITEMEM_8BIT = 0x0d
    STLINK_DEBUG_A1_CLEARFP = 0x0e
    STLINK_DEBUG_A1_WRITEDEBUGREG = 0x0f
    STLINK_DEBUG_A1_SETWATCHPOINT = 0x10
    STLINK_DEBUG_A1_ENTER = 0x20
    STLINK_DEBUG_EXIT = 0x21
    STLINK_DEBUG_READCOREID = 0x22
    STLINK_DEBUG_A2_ENTER = 0x30
    STLINK_DEBUG_A2_READ_IDCODES = 0x31
    STLINK_DEBUG_A2_RESETSYS = 0x32
    STLINK_DEBUG_A2_READREG = 0x33
    STLINK_DEBUG_A2_WRITEREG = 0x34
    STLINK_DEBUG_A2_WRITEDEBUGREG = 0x35
    STLINK_DEBUG_A2_READDEBUGREG = 0x36
    STLINK_DEBUG_A2_READALLREGS = 0x3a
    STLINK_DEBUG_A2_GETLASTRWSTATUS = 0x3b
    STLINK_DEBUG_A2_DRIVE_NRST = 0x3c
    STLINK_DEBUG_SYNC = 0x3e
    STLINK_DEBUG_A2_START_TRACE_RX = 0x40
    STLINK_DEBUG_A2_STOP_TRACE_RX = 0x41
    STLINK_DEBUG_A2_GET_TRACE_NB = 0x42
    STLINK_DEBUG_A2_SWD_SET_FREQ = 0x43
    STLINK_DEBUG_ENTER_SWD = 0xa3

    STLINK_DEBUG_A2_NRST_LOW = 0x00
    STLINK_DEBUG_A2_NRST_HIGH = 0x01
    STLINK_DEBUG_A2_NRST_PULSE = 0x02

    STLINK_DEBUG_A2_SWD_FREQ_MAP = collections.OrderedDict()
    STLINK_DEBUG_A2_SWD_FREQ_MAP[4000000] = 0
    STLINK_DEBUG_A2_SWD_FREQ_MAP[1800000] = 1
    STLINK_DEBUG_A2_SWD_FREQ_MAP[1200000] = 2
    STLINK_DEBUG_A2_SWD_FREQ_MAP[950000] = 3
    STLINK_DEBUG_A2_SWD_FREQ_MAP[480000] = 7
    STLINK_DEBUG_A2_SWD_FREQ_MAP[240000] = 15
    STLINK_DEBUG_A2_SWD_FREQ_MAP[125000] = 31
    STLINK_DEBUG_A2_SWD_FREQ_MAP[100000] = 40
    STLINK_DEBUG_A2_SWD_FREQ_MAP[50000] = 79
    STLINK_DEBUG_A2_SWD_FREQ_MAP[25000] = 158
    STLINK_DEBUG_A2_SWD_FREQ_MAP[15000] = 265
    STLINK_DEBUG_A2_SWD_FREQ_MAP[5000] = 798

    STLINK_MAXIMUM_TRANSFER_SIZE = 1024
    STLINK_MAXIMUM_8BIT_DATA = 64

    class StlinkVersion():
        """ST-Link version holder class"""
        def __init__(self, dev_ver, ver):
            self._stlink = (ver >> 12) & 0xf
            self._jtag = (ver >> 6) & 0x3f
            self._swim = ver & 0x3f if dev_ver == 'V2' else None
            self._mass = ver & 0x3f if dev_ver == 'V2-1' else None
            self._api = 2 if self._jtag > 11 else 1
            self._str = "ST-Link/%s V%dJ%d" % (dev_ver, self._stlink, self._jtag)
            if dev_ver == 'V2':
                self._str += "S%d" % self._swim
            if dev_ver == 'V2-1':
                self._str += "M%d" % self._mass

        @property
        def stlink(self):
            """Major version"""
            return self._stlink

        @property
        def jtag(self):
            """Jtag version"""
            return self._jtag

        @property
        def swim(self):
            """SWIM version"""
            return self._swim

        @property
        def mass(self):
            """Mass storage version"""
            return self._mass

        @property
        def api(self):
            """API version"""
            return self._api

        @property
        def str(self):
            """String representation"""
            return self._str


    def __init__(self, swd_frequency=1800000):
        self._com = stlinkcom.StlinkCom()
        self._version = self.get_version()
        self.leave_state()
        # self._target_volgtage = self.read_target_voltage()
        if self._version.jtag >= 22:
            self._set_swd_freq(swd_frequency)
        self.enter_debug_swd()
        # self._coreid = self.get_coreid()

    @property
    def com(self):
        """Communication class"""
        return self._com

    @property
    def version(self):
        """ST-Link version"""
        return self._version

    def get_version(self):
        """Read and decode version from ST-Link"""
        res = self._com.xfer([Stlink.STLINK_GET_VERSION, 0x80], rx_len=6)
        dev_ver = self._com.get_version()
        ver = int.from_bytes(res[:2], byteorder='big')
        return Stlink.StlinkVersion(dev_ver, ver)

    def leave_state(self):
        """Leave current state of ST-Link"""
        res = self._com.xfer([Stlink.STLINK_GET_CURRENT_MODE], rx_len=2)
        if res[0] == Stlink.STLINK_MODE_DFU:
            cmd = [Stlink.STLINK_DFU_COMMAND, Stlink.STLINK_DFU_EXIT]
        elif res[0] == Stlink.STLINK_MODE_DEBUG:
            cmd = [Stlink.STLINK_DEBUG_COMMAND, Stlink.STLINK_DEBUG_EXIT]
        elif res[0] == Stlink.STLINK_MODE_SWIM:
            cmd = [Stlink.STLINK_SWIM_COMMAND, Stlink.STLINK_SWIM_EXIT]
        else:
            return
        self._com.xfer(cmd)

    def _set_swd_freq(self, frequency=1800000):
        """Set SWD frequency"""
        for freq, data in Stlink.STLINK_DEBUG_A2_SWD_FREQ_MAP.items():
            if frequency >= freq:
                cmd = [
                    Stlink.STLINK_DEBUG_COMMAND,
                    Stlink.STLINK_DEBUG_A2_SWD_SET_FREQ,
                    data]
                res = self._com.xfer(cmd, rx_len=2)
                if res[0] != 0x80:
                    raise StlinkException("Error switching SWD frequency")
                return
        raise StlinkException("Selected SWD frequency is too low")

    def get_target_voltage(self):
        """Get target voltage from programmer"""
        res = self._com.xfer([Stlink.STLINK_GET_TARGET_VOLTAGE], rx_len=8)
        an0 = int.from_bytes(res[:4], byteorder='little')
        an1 = int.from_bytes(res[4:8], byteorder='little')
        return 2 * an1 * 1.2 / an0 if an0 != 0 else None

    def enter_debug_swd(self):
        """Enter SWD debug mode"""
        cmd = [
            Stlink.STLINK_DEBUG_COMMAND,
            Stlink.STLINK_DEBUG_A2_ENTER,
            Stlink.STLINK_DEBUG_ENTER_SWD]
        self._com.xfer(cmd, rx_len=2)

    def get_coreid(self):
        """Get core ID from MCU"""
        cmd = [
            Stlink.STLINK_DEBUG_COMMAND,
            Stlink.STLINK_DEBUG_READCOREID]
        res = self._com.xfer(cmd, rx_len=4)
        return int.from_bytes(res[:4], byteorder='little')

    def get_reg(self, reg):
        """Get core register"""
        cmd = [
            Stlink.STLINK_DEBUG_COMMAND,
            Stlink.STLINK_DEBUG_A2_READREG,
            reg]
        res = self._com.xfer(cmd, rx_len=8)
        return int.from_bytes(res[4:8], byteorder='little')

    def set_reg(self, reg, data):
        """Set core register"""
        cmd = [
            Stlink.STLINK_DEBUG_COMMAND,
            Stlink.STLINK_DEBUG_A2_WRITEREG,
            reg]
        cmd.extend(list(data.to_bytes(4, byteorder='little')))
        self._com.xfer(cmd, rx_len=2)

    def set_mem32(self, addr, data):
        """Set memory register (32 bits)"""
        if addr % 4:
            raise StlinkException('address is not in multiples of 4')
        cmd = [
            Stlink.STLINK_DEBUG_COMMAND,
            Stlink.STLINK_DEBUG_A2_WRITEDEBUGREG]
        cmd.extend(list(addr.to_bytes(4, byteorder='little')))
        cmd.extend(list(data.to_bytes(4, byteorder='little')))
        self._com.xfer(cmd, rx_len=2)

    def get_mem32(self, addr):
        """Get memory register (32 bits)"""
        if addr % 4:
            raise StlinkException('address is not in multiples of 4')
        cmd = [
            Stlink.STLINK_DEBUG_COMMAND,
            Stlink.STLINK_DEBUG_A2_READDEBUGREG]
        cmd.extend(list(addr.to_bytes(4, byteorder='little')))
        res = self._com.xfer(cmd, rx_len=8)
        return int.from_bytes(res[4:8], byteorder='little')

    def read_mem32(self, addr, size):
        """Read memory (32 bits access)"""
        if addr % 4:
            raise StlinkException('Address must be in multiples of 4')
        if size % 4:
            raise StlinkException('Size must be in multiples of 4')
        if size > Stlink.STLINK_MAXIMUM_TRANSFER_SIZE:
            raise StlinkException('Too much bytes to read')
        cmd = [
            Stlink.STLINK_DEBUG_COMMAND,
            Stlink.STLINK_DEBUG_READMEM_32BIT]
        cmd.extend(list(addr.to_bytes(4, byteorder='little')))
        cmd.extend(list(size.to_bytes(4, byteorder='little')))
        return self._com.xfer(cmd, rx_len=size)

    def write_mem32(self, addr, data):
        """Write memory (32 bits access)"""
        if addr % 4:
            raise StlinkException('Address must be in multiples of 4')
        if len(data) % 4:
            raise StlinkException('Size must be in multiples of 4')
        if len(data) > Stlink.STLINK_MAXIMUM_TRANSFER_SIZE:
            raise StlinkException('Too much bytes to write')
        cmd = [
            Stlink.STLINK_DEBUG_COMMAND,
            Stlink.STLINK_DEBUG_WRITEMEM_32BIT]
        cmd.extend(list(addr.to_bytes(4, byteorder='little')))
        cmd.extend(list(len(data).to_bytes(4, byteorder='little')))
        self._com.xfer(cmd, data=data)

    def read_mem8(self, addr, size):
        """Read memory (8 bits access)"""
        if size > Stlink.STLINK_MAXIMUM_8BIT_DATA:
            raise StlinkException('Too much bytes to read')
        cmd = [Stlink.STLINK_DEBUG_COMMAND, Stlink.STLINK_DEBUG_READMEM_8BIT]
        cmd.extend(list(addr.to_bytes(4, byteorder='little')))
        cmd.extend(list(size.to_bytes(4, byteorder='little')))
        return self._com.xfer(cmd, rx_len=size)

    def write_mem8(self, addr, data):
        """Write memory (8 bits access)"""
        if len(data) > Stlink.STLINK_MAXIMUM_8BIT_DATA:
            raise StlinkException('Too much bytes to write')
        cmd = [Stlink.STLINK_DEBUG_COMMAND, Stlink.STLINK_DEBUG_WRITEMEM_8BIT]
        cmd.extend(list(addr.to_bytes(4, byteorder='little')))
        cmd.extend(list(len(data).to_bytes(4, byteorder='little')))
        self._com.xfer(cmd, data=data)
