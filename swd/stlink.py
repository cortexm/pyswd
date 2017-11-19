"""ST-Link/V2 driver"""

# import itertools as _itertools
from swd.stlinkcom import StlinkCom as _StlinkCom
import swd._log as _log


class StlinkException(Exception):
    """Exception"""

class Stlink():
    """ST-Link class"""
    _STLINK_GET_VERSION = 0xf1
    _STLINK_DEBUG_COMMAND = 0xf2
    _STLINK_DFU_COMMAND = 0xf3
    _STLINK_SWIM_COMMAND = 0xf4
    _STLINK_GET_CURRENT_MODE = 0xf5
    _STLINK_GET_TARGET_VOLTAGE = 0xf7

    _STLINK_MODE_DFU = 0x00
    _STLINK_MODE_MASS = 0x01
    _STLINK_MODE_DEBUG = 0x02
    _STLINK_MODE_SWIM = 0x03
    _STLINK_MODE_BOOTLOADER = 0x04

    _STLINK_DFU_EXIT = 0x07

    _STLINK_SWIM_ENTER = 0x00
    _STLINK_SWIM_EXIT = 0x01

    _STLINK_DEBUG_ENTER_JTAG = 0x00
    _STLINK_DEBUG_STATUS = 0x01
    _STLINK_DEBUG_FORCEDEBUG = 0x02
    _STLINK_DEBUG_A1_RESETSYS = 0x03
    _STLINK_DEBUG_A1_READALLREGS = 0x04
    _STLINK_DEBUG_A1_READREG = 0x05
    _STLINK_DEBUG_A1_WRITEREG = 0x06
    _STLINK_DEBUG_READMEM_32BIT = 0x07
    _STLINK_DEBUG_WRITEMEM_32BIT = 0x08
    _STLINK_DEBUG_RUNCORE = 0x09
    _STLINK_DEBUG_STEPCORE = 0x0a
    _STLINK_DEBUG_A1_SETFP = 0x0b
    _STLINK_DEBUG_READMEM_8BIT = 0x0c
    _STLINK_DEBUG_WRITEMEM_8BIT = 0x0d
    _STLINK_DEBUG_A1_CLEARFP = 0x0e
    _STLINK_DEBUG_A1_WRITEDEBUGREG = 0x0f
    _STLINK_DEBUG_A1_SETWATCHPOINT = 0x10
    _STLINK_DEBUG_A1_ENTER = 0x20
    _STLINK_DEBUG_EXIT = 0x21
    _STLINK_DEBUG_READCOREID = 0x22
    _STLINK_DEBUG_A2_ENTER = 0x30
    _STLINK_DEBUG_A2_READ_IDCODES = 0x31
    _STLINK_DEBUG_A2_RESETSYS = 0x32
    _STLINK_DEBUG_A2_READREG = 0x33
    _STLINK_DEBUG_A2_WRITEREG = 0x34
    _STLINK_DEBUG_A2_WRITEDEBUGREG = 0x35
    _STLINK_DEBUG_A2_READDEBUGREG = 0x36
    _STLINK_DEBUG_A2_READALLREGS = 0x3a
    _STLINK_DEBUG_A2_GETLASTRWSTAT = 0x3b
    _STLINK_DEBUG_A2_DRIVE_NRST = 0x3c
    _STLINK_DEBUG_SYNC = 0x3e
    _STLINK_DEBUG_A2_START_TRACE_RX = 0x40
    _STLINK_DEBUG_A2_STOP_TRACE_RX = 0x41
    _STLINK_DEBUG_A2_GET_TRACE_NB = 0x42
    _STLINK_DEBUG_A2_SWD_SET_FREQ = 0x43
    _STLINK_DEBUG_ENTER_SWD = 0xa3

    _STLINK_DEBUG_A2_NRST_LOW = 0x00
    _STLINK_DEBUG_A2_NRST_HIGH = 0x01
    _STLINK_DEBUG_A2_NRST_PULSE = 0x02

    _STLINK_DEBUG_A2_SWD_FREQ = (
        (4000000, 0, ),
        (1800000, 1, ),   # default
        (1200000, 2, ),
        (950000, 3, ),
        (480000, 7, ),
        (240000, 15, ),
        (125000, 31, ),
        (100000, 40, ),
        (50000, 79, ),
        (25000, 158, ),
        # 16-bit number is not currently supported
        # (15000, 265, ),
        # (5000, 798, ),
    )

    _STLINK_MAXIMUM_TRANSFER_SIZE = 1024
    _STLINK_MAXIMUM_8BIT_DATA = 64

    MAXIMUM_8BIT_DATA = _STLINK_MAXIMUM_8BIT_DATA
    MAXIMUM_32BIT_DATA = _STLINK_MAXIMUM_TRANSFER_SIZE


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

        def __str__(self):
            """String representation"""
            return self._str

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

    @_log.log(_log.DEBUG2)
    def __init__(self, swd_frequency=1800000, com=None):
        if com is None:
            # default com driver is StlinkCom
            com = _StlinkCom()
        self._com = com
        self._version = self._get_version()
        self._leave_state()
        if self._version.jtag >= 22:
            self._set_swd_freq(swd_frequency)
        self._enter_debug_swd()

    @_log.log(_log.DEBUG3)
    def _get_version(self):
        res = self._com.xfer([Stlink._STLINK_GET_VERSION, 0x80], rx_length=6)
        ver = int.from_bytes(res[:2], byteorder='big')
        return Stlink.StlinkVersion(self._com.version, ver)

    @_log.log(_log.DEBUG3)
    def _leave_state(self):
        res = self._com.xfer([Stlink._STLINK_GET_CURRENT_MODE], rx_length=2)
        if res[0] == Stlink._STLINK_MODE_DFU:
            cmd = [Stlink._STLINK_DFU_COMMAND, Stlink._STLINK_DFU_EXIT]
        elif res[0] == Stlink._STLINK_MODE_DEBUG:
            cmd = [Stlink._STLINK_DEBUG_COMMAND, Stlink._STLINK_DEBUG_EXIT]
        elif res[0] == Stlink._STLINK_MODE_SWIM:
            cmd = [Stlink._STLINK_SWIM_COMMAND, Stlink._STLINK_SWIM_EXIT]
        else:
            return
        self._com.xfer(cmd)

    @_log.log(_log.DEBUG3)
    def _set_swd_freq(self, frequency=1800000):
        for freq, data in Stlink._STLINK_DEBUG_A2_SWD_FREQ:
            if frequency >= freq:
                cmd = [
                    Stlink._STLINK_DEBUG_COMMAND,
                    Stlink._STLINK_DEBUG_A2_SWD_SET_FREQ,
                    data]
                res = self._com.xfer(cmd, rx_length=2)
                if res[0] != 0x80:
                    raise StlinkException("Error switching SWD frequency")
                return
        raise StlinkException("Selected SWD frequency is too low")

    @_log.log(_log.DEBUG3)
    def _enter_debug_swd(self):
        cmd = [
            Stlink._STLINK_DEBUG_COMMAND,
            Stlink._STLINK_DEBUG_A2_ENTER,
            Stlink._STLINK_DEBUG_ENTER_SWD]
        self._com.xfer(cmd, rx_length=2)

    def get_version(self):
        """Get ST-Link debugger version

        Return:
            instance of StlinkVersion
        """
        return self._version

    @_log.log(_log.DEBUG2)
    def get_target_voltage(self):
        """Get target voltage from debugger

        Return:
            measured voltage
        """
        res = self._com.xfer([Stlink._STLINK_GET_TARGET_VOLTAGE], rx_length=8)
        an0 = int.from_bytes(res[:4], byteorder='little')
        an1 = int.from_bytes(res[4:8], byteorder='little')
        return round(2 * an1 * 1.2 / an0, 2) if an0 != 0 else None

    @_log.log(_log.DEBUG2)
    def get_coreid(self):
        """Get core ID from MCU

        Return:
            32 bit number
        """
        cmd = [
            Stlink._STLINK_DEBUG_COMMAND,
            Stlink._STLINK_DEBUG_READCOREID]
        res = self._com.xfer(cmd, rx_length=4)
        return int.from_bytes(res[:4], byteorder='little')

    @_log.log(_log.DEBUG2)
    def get_reg(self, register):
        """Get core register

        Read 32 bit CPU core register (e.g. R0, R1, ...)
        Register ID depends on architecture.
        (MCU must be halted to access core register)

        Arguments:
            register: register ID

        Return:
            32 bit number
        """
        cmd = [
            Stlink._STLINK_DEBUG_COMMAND,
            Stlink._STLINK_DEBUG_A2_READREG,
            register]
        res = self._com.xfer(cmd, rx_length=8)
        return int.from_bytes(res[4:8], byteorder='little')

    @_log.log(_log.DEBUG2)
    def set_reg(self, register, data):
        """Set core register

        Write 32 bit CPU core register (e.g. R0, R1, ...)       R
        Register ID depends on architecture.
        (MCU must be halted to access core register)

        Arguments:
            register: register ID
            data: 32 bit number
        """
        cmd = [
            Stlink._STLINK_DEBUG_COMMAND,
            Stlink._STLINK_DEBUG_A2_WRITEREG,
            register]
        cmd.extend(list(data.to_bytes(4, byteorder='little')))
        self._com.xfer(cmd, rx_length=2)

    @_log.log(_log.DEBUG2)
    def get_mem32(self, address):
        """Get 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory

        Return:
            return 32 bit number
        """
        if address % 4:
            raise StlinkException('Address is not aligned to 4 Bytes')
        cmd = [
            Stlink._STLINK_DEBUG_COMMAND,
            Stlink._STLINK_DEBUG_A2_READDEBUGREG]
        cmd.extend(list(address.to_bytes(4, byteorder='little')))
        res = self._com.xfer(cmd, rx_length=8)
        return int.from_bytes(res[4:8], byteorder='little')

    @_log.log(_log.DEBUG2)
    def set_mem32(self, address, data):
        """Set 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            data: 32 bit number
        """
        if address % 4:
            raise StlinkException('Address is not aligned to 4 Bytes')
        cmd = [
            Stlink._STLINK_DEBUG_COMMAND,
            Stlink._STLINK_DEBUG_A2_WRITEDEBUGREG]
        cmd.extend(list(address.to_bytes(4, byteorder='little')))
        cmd.extend(list(data.to_bytes(4, byteorder='little')))
        self._com.xfer(cmd, rx_length=2)

    @_log.log(_log.DEBUG2)
    def read_mem8(self, address, size):
        """Read data from memory with 8 bit memory access.

        Maximum number of bytes for read can be 64.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            list of read data
        """
        if size > Stlink.MAXIMUM_8BIT_DATA:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % Stlink.MAXIMUM_8BIT_DATA)
        cmd = [Stlink._STLINK_DEBUG_COMMAND, Stlink._STLINK_DEBUG_READMEM_8BIT]
        cmd.extend(list(address.to_bytes(4, byteorder='little')))
        cmd.extend(list(size.to_bytes(4, byteorder='little')))
        return self._com.xfer(cmd, rx_length=size)

    @_log.log(_log.DEBUG2)
    def write_mem8(self, address, data):
        """Write data into memory with 8 bit memory access.

        Maximum number of bytes for one write can be 64.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        if len(data) > Stlink.MAXIMUM_8BIT_DATA:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % Stlink.MAXIMUM_8BIT_DATA)
        cmd = [Stlink._STLINK_DEBUG_COMMAND, Stlink._STLINK_DEBUG_WRITEMEM_8BIT]
        cmd.extend(list(address.to_bytes(4, byteorder='little')))
        cmd.extend(list(len(data).to_bytes(4, byteorder='little')))
        self._com.xfer(cmd, data=data)

    @_log.log(_log.DEBUG2)
    def read_mem32(self, address, size):
        """Read data from memory with 32 bit memory access.

        Maximum number of bytes for one read can be 1024.
        Address and size must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            list of read data
        """
        if address % 4:
            raise StlinkException('Address is not aligned to 4 Bytes')
        if size % 4:
            raise StlinkException('Size is not aligned to 4 Bytes')
        if size > Stlink.MAXIMUM_32BIT_DATA:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % Stlink.MAXIMUM_32BIT_DATA)
        cmd = [
            Stlink._STLINK_DEBUG_COMMAND,
            Stlink._STLINK_DEBUG_READMEM_32BIT]
        cmd.extend(list(address.to_bytes(4, byteorder='little')))
        cmd.extend(list(size.to_bytes(4, byteorder='little')))
        return self._com.xfer(cmd, rx_length=size)

    @_log.log(_log.DEBUG2)
    def write_mem32(self, address, data):
        """Write data into memory with 32 bit memory access.

        Maximum number of bytes for one write can be 1024.
        Address and number of bytes must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        if address % 4:
            raise StlinkException('Address is not aligned to 4 Bytes')
        if len(data) % 4:
            raise StlinkException('Size is not aligned to 4 Bytes')
        if len(data) > Stlink.MAXIMUM_32BIT_DATA:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % Stlink.MAXIMUM_32BIT_DATA)
        cmd = [
            Stlink._STLINK_DEBUG_COMMAND,
            Stlink._STLINK_DEBUG_WRITEMEM_32BIT]
        cmd.extend(list(address.to_bytes(4, byteorder='little')))
        cmd.extend(list(len(data).to_bytes(4, byteorder='little')))
        self._com.xfer(cmd, data=data)
