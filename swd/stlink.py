"""ST-Link/V2 driver
"""

import logging as _logging
from swd.stlinkcom import StlinkCom as _StlinkCom


class StlinkException(Exception):
    """Stlink general exception"""


class OutdatedStlinkFirmware(StlinkException):
    """Stlink general exception"""
    def __init__(self, current_version, minimal_version):
        super().__init__(
            f"Outdated FW: {current_version}, require: {minimal_version}.")


def check_alignment(alignment, **values):
    """Check alignment of values

    Arguments:
        alignment: number of bytes to align
        **values: values for align checking

    Raise:
        StlinkException: if value is not aligned

    Example:
        check_alignment(4, address=offset, size=len(data))
    """
    for key, value in values.items():
        if value % alignment:
            raise StlinkException(
                f'{key.capitalize()} is not aligned to {alignment} Bytes')


class Stlink:
    """ST-Link class"""

    class CMD:  # pylint: disable=too-few-public-methods
        """Stlink commands"""

        GET_VERSION = 0xf1
        GET_CURRENT_MODE = 0xf5
        GET_TARGET_VOLTAGE = 0xf7
        GET_VERSION_EX = 0xfb  # for V3

        class MODE:
            """Mode"""
            DFU = 0x00
            MASS = 0x01
            DEBUG = 0x02
            SWIM = 0x03
            BOOTLOADER = 0x04

        class DFU:
            """Dfu commands"""
            EXIT = 0x07
            COMMAND = 0xf3

        class SWIM:
            """Swim commands"""
            ENTER = 0x00
            EXIT = 0x01
            COMMAND = 0xf4

        class DEBUG:
            """Debug commands"""
            STATUS = 0x01
            FORCE_DEBUG = 0x02
            RESET_SYS = 0x03
            READ_ALL_REGS = 0x04
            READ_REG = 0x05
            WRITE_REG = 0x06
            READMEM_32BIT = 0x07
            WRITEMEM_32BIT = 0x08
            RUN_CORE = 0x09
            STEP_CORE = 0x0a
            SETFP = 0x0b
            READMEM_8BIT = 0x0c
            WRITEMEM_8BIT = 0x0d
            CLEAR_FP = 0x0e
            WRITE_DEBUG_REG = 0x0f
            SET_WATCH_POINT = 0x10
            ENTER = 0x20
            EXIT = 0x21
            READ_COREID = 0x22
            ENTER_SWD = 0xa3
            ENTER_JTAG = 0xa4
            COMMAND = 0xf2

            class APIV2:
                """Commands for V2"""
                ENTER = 0x30
                READ_IDCODES = 0x31
                RESET_SYS = 0x32
                READ_REG = 0x33
                WRITE_REG = 0x34
                WRITE_DEBUG_REG = 0x35
                READ_DEBUG_REG = 0x36
                READ_ALL_REGS = 0x3a
                GET_LAST_RW_STATE = 0x3b
                GET_LAST_RW_STATE_EX = 0x3e  # V2J15
                DRIVE_NRST = 0x3c
                START_TRACE_RX = 0x40
                STOP_TRACE_RX = 0x41
                GET_TRACE_NB = 0x42
                SWD_SET_FREQ = 0x43  # V2J20
                JTAG_SET_FREQ = 0x44  # V2J24
                READ_AP_REG = 0x45  # V2J24
                WRITE_AP_REG = 0x46  # V2J24
                READ_MEM_16BIT = 0x47  # V2J26
                WRITE_MEM_16BIT = 0x48  # V2J26
                JTAG_INIT_AP = 0x4b  # V2J28
                JTAG_CLOSE_AP = 0x4c  # V2J28

                class NRST:
                    """for DRIVE_NRST"""
                    LOW = 0x00
                    HIGH = 0x01
                    PULSE = 0x02

            class APIV3:
                """Commands for V3"""
                SET_COM_FREQ = 0x61  # V3
                GET_COM_FREQ = 0x62  # V3

                class COM_FREQ:
                    """Parameters for SET_COM_FREQ and GET_COM_FREQ"""
                    SWD_COM = 0x00
                    JTAG_COM = 0x01

    class STATUS(object):
        """STLink status codes"""
        JTAG_OK = 0x80
        JTAG_UNKNOWN_ERROR = 0x01
        JTAG_SPI_ERROR = 0x02
        JTAG_DMA_ERROR = 0x03
        JTAG_UNKNOWN_JTAG_CHAIN = 0x04
        JTAG_NO_DEVICE_CONNECTED = 0x05
        JTAG_INTERNAL_ERROR = 0x06
        JTAG_CMD_WAIT = 0x07
        JTAG_CMD_ERROR = 0x08
        JTAG_GET_IDCODE_ERROR = 0x09
        JTAG_ALIGNMENT_ERROR = 0x0a
        JTAG_DBG_POWER_ERROR = 0x0b
        JTAG_WRITE_ERROR = 0x0c
        JTAG_WRITE_VERIF_ERROR = 0x0d
        JTAG_ALREADY_OPENED_IN_OTHER_MODE = 0x0e
        SWD_AP_WAIT = 0x10
        SWD_AP_FAULT = 0x11
        SWD_AP_ERROR = 0x12
        SWD_AP_PARITY_ERROR = 0x13
        SWD_DP_WAIT = 0x14
        SWD_DP_FAULT = 0x15
        SWD_DP_ERROR = 0x16
        SWD_DP_PARITY_ERROR = 0x17
        SWD_AP_WDATA_ERROR = 0x18
        SWD_AP_STICKY_ERROR = 0x19
        SWD_AP_STICKY_OVERRUN_ERROR = 0x1a
        SWV_NOT_AVAILABLE = 0x20
        JTAG_FREQ_NOT_SUPPORTED = 0x41
        JTAG_UNKNOWN_CMD = 0x42

        MESSAGES = {
            JTAG_UNKNOWN_ERROR : "Unknown error",
            JTAG_SPI_ERROR : "SPI error",
            JTAG_DMA_ERROR : "DMA error",
            JTAG_UNKNOWN_JTAG_CHAIN : "Unknown JTAG chain",
            JTAG_NO_DEVICE_CONNECTED : "No device connected",
            JTAG_INTERNAL_ERROR : "Internal error",
            JTAG_CMD_WAIT : "Command wait",
            JTAG_CMD_ERROR : "Command error",
            JTAG_GET_IDCODE_ERROR : "Get IDCODE error",
            JTAG_ALIGNMENT_ERROR : "Alignment error",
            JTAG_DBG_POWER_ERROR : "Debug power error",
            JTAG_WRITE_ERROR : "Write error",
            JTAG_WRITE_VERIF_ERROR : "Write verification error",
            JTAG_ALREADY_OPENED_IN_OTHER_MODE : "Already opened in another mode",
            SWD_AP_WAIT : "AP wait",
            SWD_AP_FAULT : "AP fault",
            SWD_AP_ERROR : "AP error",
            SWD_AP_PARITY_ERROR : "AP parity error",
            SWD_DP_WAIT : "DP wait",
            SWD_DP_FAULT : "DP fault",
            SWD_DP_ERROR : "DP error",
            SWD_DP_PARITY_ERROR : "DP parity error",
            SWD_AP_WDATA_ERROR : "AP WDATA error",
            SWD_AP_STICKY_ERROR : "AP sticky error",
            SWD_AP_STICKY_OVERRUN_ERROR : "AP sticky overrun error",
            SWV_NOT_AVAILABLE : "SWV not available",
            JTAG_FREQ_NOT_SUPPORTED : "Frequency not supported",
            JTAG_UNKNOWN_CMD : "Unknown command",
        }

    class CmdBuilder:
        """CMD builder"""
        def __init__(self, cmd):
            if isinstance(cmd, int):
                self._cmd = [cmd]
            elif isinstance(cmd, list):
                self._cmd = cmd

        def add_u8(self, number):
            """add 8 bit unsigned number"""
            self._cmd.append(number)

        def add_u16(self, number):
            """add 16 bit unsigned number"""
            self._cmd.extend(list(number.to_bytes(2, byteorder='little')))

        def add_u32(self, number):
            """add 32 bit unsigned number"""
            self._cmd.extend(list(number.to_bytes(4, byteorder='little')))

        @property
        def cmd(self):
            """return command"""
            return self._cmd

    _SWD_FREQ = (
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
        (15000, 265, ),
        (5000, 798, ),
    )

    _STLINK_MAXIMUM_8BIT_DATA = 64

    class StlinkVersion:
        """ST-Link version holder class"""
        def __init__(self, version):
            self._stlink = version.get('stlink')
            self._jtag = version.get('jtag')
            self._swim = version.get('swim')
            self._mass = version.get('mass')
            self._api = version.get('api')
            self._bridge = version.get('bridge')
            self._str = f"ST-Link/{version.get('dev')}"
            self._str += f" V{self._stlink}"
            if self._jtag:
                self._str += f"J{self._jtag}"
            if self._swim:
                self._str += f"S{self._swim}"
            if self._mass:
                self._str += f"M{self._mass}"
            if self._bridge:
                self._str += f"B{self._bridge}"

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
        def bridge(self):
            """Bridge version"""
            return self._bridge

        @property
        def api(self):
            """API version"""
            return self._api

        @property
        def str(self):
            """String representation"""
            return self._str

    def __init__(self, swd_frequency=None, com=None, serial_no='', debug=0):
        self._debug = debug
        if com is None:
            # default com driver is StlinkCom
            com = _StlinkCom(serial_no, debug=debug)
        self._com = com
        self._version = self._read_version()
        self._leave_state()
        if swd_frequency:
            self._set_swd_freq(swd_frequency)
        self._enter_debug_swd()

    @property
    def maximum_8bit_data(self):
        """Maximum transfer size for 8 bit data"""
        return self._STLINK_MAXIMUM_8BIT_DATA

    @property
    def maximum_16bit_data(self):
        """Maximum transfer size for 16 bit data"""
        return self._com.STLINK_MAXIMUM_TRANSFER_SIZE

    @property
    def maximum_32bit_data(self):
        """Maximum transfer size for 32 bit data"""
        return self._com.STLINK_MAXIMUM_TRANSFER_SIZE

    def _read_version(self):
        res = self._com.xfer([Stlink.CMD.GET_VERSION, 0x80], rx_length=6)
        ver = int.from_bytes(res[:2], byteorder='big')
        ver_stlink = (ver >> 12) & 0xf
        version = {
            'stlink': ver_stlink,
            'dev': self._com.version,
        }
        if ver_stlink == 2:
            version['jtag'] = (ver >> 6) & 0x3f
            version['api'] = 1 if version['jtag'] <= 11 else 2
            if self._com.version == 'V2':
                version['swim'] = ver & 0x3f
            elif self._com.version == 'V2-1':
                version['mass'] = ver & 0x3f
        elif ver_stlink == 3:
            ver_ex = self._com.xfer(
                [Stlink.CMD.GET_VERSION_EX, 0x80],
                rx_length=16)
            version.update({
                'api': 3,
                'swim': int(ver_ex[1]),
                'jtag': int(ver_ex[2]),
                'mass': int(ver_ex[3]),
                'bridge': int(ver_ex[4]),
            })
        return Stlink.StlinkVersion(version)

    def _leave_state(self):
        res = self._com.xfer([Stlink.CMD.GET_CURRENT_MODE], rx_length=2)
        if res[0] == Stlink.CMD.MODE.DFU:
            self._com.xfer([Stlink.CMD.DFU.COMMAND, Stlink.CMD.DFU.EXIT])
        elif res[0] == Stlink.CMD.MODE.DEBUG:
            self._com.xfer([Stlink.CMD.DEBUG.COMMAND, Stlink.CMD.DEBUG.EXIT])
        elif res[0] == Stlink.CMD.MODE.SWIM:
            self._com.xfer([Stlink.CMD.SWIM.COMMAND, Stlink.CMD.SWIM.EXIT])

    def _set_swd_freq(self, swd_frequency):
        if self._version.stlink == 2:
            self._set_swd_freq_v2(swd_frequency)
        elif self._version.stlink == 3:
            self._set_swd_freq_v3(swd_frequency)

    def _set_swd_freq_v2(self, swd_frequency):
        if self._version.jtag < 22:
            raise OutdatedStlinkFirmware(self._version.str, "J22")
        for freq, val in Stlink._SWD_FREQ:
            if swd_frequency >= freq:
                cmd = Stlink.CmdBuilder([
                    Stlink.CMD.DEBUG.COMMAND,
                    Stlink.CMD.DEBUG.APIV2.SWD_SET_FREQ])
                cmd.add_u16(val)
                res = self._com.xfer(cmd.cmd, rx_length=2)
                if res[0] != 0x80:
                    raise StlinkException("Error switching SWD frequency")
                return
        raise StlinkException("Selected SWD frequency is too low")

    def _set_swd_freq_v3(self, swd_frequency):
        if self._version.api < 3:
            raise OutdatedStlinkFirmware(self._version.str, "V3")
        res = self._com.xfer([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV3.GET_COM_FREQ,
            0], rx_length=52)
        i = 0
        freq_khz = 0
        while i < res[8]:
            freq_khz = int.from_bytes(
                res[12 + 4 * i: 15 + 4 * i],
                byteorder='little')
            if swd_frequency // 1000 >= freq_khz:
                break
            i = i + 1
        _logging.info(
            f"Using {freq_khz} khz for {swd_frequency // 1000} kHz requested")
        if i == res[8]:
            raise StlinkException("Requested SWD frequency is too low")
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV3.SET_COM_FREQ,
            0x00, 0x00])
        cmd.add_u32(freq_khz)
        res = self._com.xfer(cmd.cmd, rx_length=2)
        if res[0] != 0x80:
            raise StlinkException("Error switching SWD frequency")

    def _enter_debug_swd(self):
        cmd = [
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.ENTER,
            Stlink.CMD.DEBUG.ENTER_SWD]
        self._com.xfer(cmd, rx_length=2)

    def get_version(self):
        """Get ST-Link debugger version

        Return:
            instance of StlinkVersion
        """
        return self._version

    def get_target_voltage(self):
        """Get target voltage from debugger

        Return:
            measured voltage
        """
        res = self._com.xfer([Stlink.CMD.GET_TARGET_VOLTAGE], rx_length=8)
        an0 = int.from_bytes(res[:4], byteorder='little')
        an1 = int.from_bytes(res[4:8], byteorder='little')
        return round(2 * an1 * 1.2 / an0, 2) if an0 != 0 else None

    def get_idcode(self):
        """Get core ID from MCU

        Return:
            32 bit number
        """
        cmd = [
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_IDCODES]
        res = self._com.xfer(cmd, rx_length=12)
        idcode = int.from_bytes(res[4:8], byteorder='little')
        if idcode == 0:
            raise StlinkException("No IDCODE, probably MCU is not connected")
        return idcode

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
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_REG])
        cmd.add_u8(register)
        res = self._com.xfer(cmd.cmd, rx_length=8)
        return int.from_bytes(res[4:8], byteorder='little')

    def get_reg_all(self):
        """Get all core registers

        Read all 32 bit CPU core registers (R0, R1, ...)
        Order of registers depends on architecture.
        (MCU must be halted to access core registers)

        Return:
            list of 32 bit numbers
        """
        cmd = [
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_ALL_REGS]
        res = self._com.xfer(cmd, rx_length=88)
        data = []
        for index in range(4, len(res), 4):
            data.append(
                int.from_bytes(res[index:index + 4], byteorder='little'))
        return data

    def set_reg(self, register, data):
        """Set core register

        Write 32 bit CPU core register (e.g. R0, R1, ...)       R
        Register ID depends on architecture.
        (MCU must be halted to access core register)

        Arguments:
            register: register ID
            data: 32 bit number
        """
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.WRITE_REG])
        cmd.add_u8(register)
        cmd.add_u32(data)
        self._com.xfer(cmd.cmd, rx_length=2)

    def get_mem32(self, address):
        """Get 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory

        Return:
            return 32 bit number
        """
        check_alignment(4, address=address)
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_DEBUG_REG])
        cmd.add_u32(address)
        res = self._com.xfer(cmd.cmd, rx_length=8)
        return int.from_bytes(res[4:8], byteorder='little')

    def set_mem32(self, address, data):
        """Set 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            data: 32 bit number
        """
        check_alignment(4, address=address)
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.WRITE_DEBUG_REG])
        cmd.add_u32(address)
        cmd.add_u32(data)
        self._com.xfer(cmd.cmd, rx_length=2)

    def read_mem8(self, address, size):
        """Read data from memory with 8 bit memory access.

        Maximum number of bytes for read can be 64.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            list of read data
        """
        if size > self.maximum_8bit_data:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % self.maximum_8bit_data)
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.READMEM_8BIT])
        cmd.add_u32(address)
        cmd.add_u32(size)
        return self._com.xfer(cmd.cmd, rx_length=size)

    def write_mem8(self, address, data):
        """Write data into memory with 8 bit memory access.

        Maximum number of bytes for one write can be 64.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        if len(data) > self.maximum_8bit_data:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % self.maximum_8bit_data)
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.WRITEMEM_8BIT])
        cmd.add_u32(address)
        cmd.add_u32(len(data))
        self._com.xfer(cmd.cmd, data=data)

    def read_mem16(self, address, size):
        """Read data from memory with 16 bit memory access.

        Maximum number of bytes for one read can be 1024.
        Address and size must be aligned to 2 Bytes.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            list of read data
        """
        if self._version.api <= 2 and self._version.jtag < 29:
            raise StlinkException(self._version.str, "J29")
        check_alignment(2, address=address, size=size)
        if size > self.maximum_16bit_data:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % self.maximum_16bit_data)
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_MEM_16BIT])
        cmd.add_u32(address)
        cmd.add_u32(size)
        return self._com.xfer(cmd.cmd, rx_length=size)

    def write_mem16(self, address, data):
        """Write data into memory with 16 bit memory access.

        Maximum number of bytes for one write can be 1024.
        Address and number of bytes must be aligned to 2 Bytes.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        if self._version.api <= 2 and self._version.jtag < 29:
            raise StlinkException(self._version.str, "J29")
        check_alignment(2, address=address, size=len(data))
        if len(data) > self.maximum_16bit_data:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % self.maximum_16bit_data)
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.WRITE_MEM_16BIT])
        cmd.add_u32(address)
        cmd.add_u32(len(data))
        self._com.xfer(cmd.cmd, data=data)

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
        if size > self.maximum_32bit_data:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % self.maximum_32bit_data)
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.READMEM_32BIT])
        cmd.add_u32(address)
        cmd.add_u32(size)
        return self._com.xfer(cmd.cmd, rx_length=size)

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
        if len(data) > self.maximum_32bit_data:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % self.maximum_32bit_data)
        cmd = Stlink.CmdBuilder([
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.WRITEMEM_32BIT])
        cmd.add_u32(address)
        cmd.add_u32(len(data))
        self._com.xfer(cmd.cmd, data=data)
