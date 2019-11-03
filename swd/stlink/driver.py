"""ST-Link/V2 driver
"""

import struct as _struct
from swd.stlink.usb import StlinkCom as _StlinkCom


class StlinkError(Exception):
    """Stlink general error"""


class StlinkException(Exception):
    """Stlink general exception"""


class OutdatedStlinkFirmware(StlinkException):
    """Stlink general exception"""
    def __init__(self, current_version, minimal_version):
        super().__init__(
            f"Outdated FW: {current_version}, require: {minimal_version}.")


def _check_alignment(alignment, **values):
    """Check alignment of values

    Arguments:
        alignment: number of bytes to align
        **values: values for align checking

    Raise:
        StlinkException: if value is not aligned

    Example:
        _check_alignment(4, address=offset, size=len(data))
    """
    for key, value in values.items():
        if value % alignment:
            raise StlinkException(
                f'{key.capitalize()} is not aligned to {alignment} Bytes')


def _check_status(status):
    """check status and raise on error

    Arguments:
        status: status code returned from ST-Link

    Raise:
        StlinkException: on error
        StlinkError: on unknown status

    """
    if status == Stlink.STATUS.JTAG_OK:
        return
    if status in Stlink.STATUS.MESSAGES:
        raise StlinkException(Stlink.STATUS.MESSAGES[status])
    raise StlinkError("Unknown status")


class Stlink:
    """ST-Link class"""

    class CMD:  # pylint: disable=too-few-public-methods
        """Stlink commands"""

        GET_VERSION = 0xf1  # _get_version()
        GET_CURRENT_MODE = 0xf5  # _get_current_mode()
        GET_TARGET_VOLTAGE = 0xf7  # get_target_voltage()
        GET_VERSION_EX = 0xfb  # for V3  # _get_version_ex()

        class MODE:
            """Mode"""
            DFU = 0x00
            MASS = 0x01
            DEBUG = 0x02
            SWIM = 0x03
            BOOTLOADER = 0x04

        class DFU:
            """Dfu commands"""
            EXIT = 0x07  # _exit_dfu()
            COMMAND = 0xf3

        class SWIM:
            """Swim commands"""
            ENTER = 0x00
            EXIT = 0x01  # _exit_swim()
            COMMAND = 0xf4

        class DEBUG:
            """Debug commands"""
            STATUS = 0x01
            FORCE_DEBUG = 0x02
            RESET_SYS = 0x03
            READ_ALL_REGS = 0x04
            READ_REG = 0x05
            WRITE_REG = 0x06
            READ_MEM_32BIT = 0x07  # read_mem32()
            WRITE_MEM_32BIT = 0x08  # write_mem32()
            RUN_CORE = 0x09
            STEP_CORE = 0x0a
            SETFP = 0x0b
            READ_MEM_8BIT = 0x0c  # read_mem8()
            WRITE_MEM_8BIT = 0x0d  # write_mem8()
            CLEAR_FP = 0x0e
            WRITE_DEBUG_REG = 0x0f
            SET_WATCH_POINT = 0x10
            ENTER = 0x20
            EXIT = 0x21  # _exit_debug
            READ_COREID = 0x22
            COMMAND = 0xf2

            class APIV2:
                """Commands for V2"""
                ENTER = 0x30  # _enter_debug_swd()
                READ_IDCODES = 0x31  # get_idcode()
                RESET_SYS = 0x32
                READ_REG = 0x33  # get_reg()
                WRITE_REG = 0x34  # set_reg()
                WRITE_DEBUG_REG = 0x35  # set_mem32()
                READ_DEBUG_REG = 0x36  # get_mem32()
                READ_ALL_REGS = 0x3a  # get_reg_all()
                GET_LAST_RW_STATE = 0x3b  # _get_last_rw_state()
                GET_LAST_RW_STATE_EX = 0x3e  # V2J15  # _get_last_rw_state_ex()
                DRIVE_NRST = 0x3c
                START_TRACE_RX = 0x40
                STOP_TRACE_RX = 0x41
                GET_TRACE_NB = 0x42
                SET_SWD_FREQ = 0x43  # V2J20  # _set_swd_freq()
                SET_JTAG_FREQ = 0x44  # V2J24
                READ_AP_REG = 0x45  # V2J24
                WRITE_AP_REG = 0x46  # V2J24
                READ_MEM_16BIT = 0x47  # V2J26  # read_mem16()
                WRITE_MEM_16BIT = 0x48  # V2J26  # write_mem16()
                JTAG_INIT_AP = 0x4b  # V2J28
                JTAG_CLOSE_AP = 0x4c  # V2J28

                class NRST:
                    """for DRIVE_NRST"""
                    LOW = 0x00
                    HIGH = 0x01
                    PULSE = 0x02

            class APIV3:
                """Commands for V3"""
                SET_COM_FREQ = 0x61  # V3  # _get_com_freq()
                GET_COM_FREQ = 0x62  # V3  # _set_com_freq()

                class COM:
                    """Parameters for SET_COM_FREQ and GET_COM_FREQ"""
                    SWD = 0x00
                    JTAG = 0x01

            class ENTERDEBUG:
                """Parameters for APIV2.ENTER"""
                SWD = 0xa3
                JTAG = 0xa4

    class STATUS:
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
            JTAG_UNKNOWN_ERROR: "Unknown error",
            JTAG_SPI_ERROR: "SPI error",
            JTAG_DMA_ERROR: "DMA error",
            JTAG_UNKNOWN_JTAG_CHAIN: "Unknown JTAG chain",
            JTAG_NO_DEVICE_CONNECTED: "No device connected",
            JTAG_INTERNAL_ERROR: "Internal error",
            JTAG_CMD_WAIT: "Command wait",
            JTAG_CMD_ERROR: "Command error",
            JTAG_GET_IDCODE_ERROR: "Get IDCODE error",
            JTAG_ALIGNMENT_ERROR: "Alignment error",
            JTAG_DBG_POWER_ERROR: "Debug power error",
            JTAG_WRITE_ERROR: "Write error",
            JTAG_WRITE_VERIF_ERROR: "Write verification error",
            JTAG_ALREADY_OPENED_IN_OTHER_MODE: "Already opened in another mode",
            SWD_AP_WAIT: "AP wait",
            SWD_AP_FAULT: "AP fault",
            SWD_AP_ERROR: "AP error",
            SWD_AP_PARITY_ERROR: "AP parity error",
            SWD_DP_WAIT: "DP wait",
            SWD_DP_FAULT: "DP fault",
            SWD_DP_ERROR: "DP error",
            SWD_DP_PARITY_ERROR: "DP parity error",
            SWD_AP_WDATA_ERROR: "AP WDATA error",
            SWD_AP_STICKY_ERROR: "AP sticky error",
            SWD_AP_STICKY_OVERRUN_ERROR: "AP sticky overrun error",
            SWV_NOT_AVAILABLE: "SWV not available",
            JTAG_FREQ_NOT_SUPPORTED: "Frequency not supported",
            JTAG_UNKNOWN_CMD: "Unknown command",
        }

    _SWD_FREQ = (
        (4000000, 0),
        (1800000, 1),
        (1200000, 2),
        (950000, 3),
        (480000, 7),
        (240000, 15),
        (125000, 31),
        (100000, 40),
        (50000, 79),
        (25000, 158),
        (15000, 265),
        (5000, 798),
    )

    _JTAG_FREQ = (
        (18000000, 2),
        (9000000, 4),
        (4500000, 8),
        (2250000, 16),
        (1120000, 32),
        (560000, 64),
        (280000, 128),
        (140000, 256),
    )

    _STLINK_MAXIMUM_8BIT_DATA = 64

    class StlinkVersion:
        """ST-Link version holder class"""
        def __init__(self, version):
            self._version = version
            self._str = f"ST-Link/{version.get('HW')} "
            for name in 'VJSMB':
                if name in version:
                    self._str += f"{name}{version[name]}"

        def __str__(self):
            """String representation"""
            return self._str

        @property
        def major(self):
            """Major version"""
            return self._version.get('V')

        @property
        def jtag(self):
            """Jtag version"""
            return self._version.get('J')

        @property
        def swim(self):
            """SWIM version"""
            return self._version.get('S')

        @property
        def mass(self):
            """Mass storage version"""
            return self._version.get('M')

        @property
        def bridge(self):
            """Bridge version"""
            return self._version.get('B')

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
            self.set_swd_freq(swd_frequency)
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

    def _get_version(self):
        """Get ST-Link version

        Returns:
            dictionary with version:
                'V': major version
                'J': JTAG/SWD version
                'S': SWIM version
                'M': mass storage version
        """
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.GET_VERSION,
            0x80)
        res = self._com.xfer(cmd, rx_length=6)
        ver, _vid, _pid = _struct.unpack('>HHH', res)
        version = {
            'V': (ver >> 12) & 0x000f,
            'J': (ver >> 6) & 0x003f}
        if self._com.version == 'V2':
            version['S'] = ver & 0x003f
        elif self._com.version == 'V2-1':
            version['M'] = ver & 0x003f
        return version

    def _get_version_ex(self):
        """Get ST-Link version

        Returns:
            dictionary with version:
                'V': major version
                'S': SWIM version
                'J': JTAG/SWD version
                'M': mass storage version
                'B': bridge version
        """
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.GET_VERSION_EX,
            0x80)
        res = self._com.xfer(cmd, rx_length=12)
        major, swim, jtag, msc, bridge, _vid, _pid = _struct.unpack(
            '<5B3xHH', res)
        return {
            'V': major,
            'S': swim,
            'J': jtag,
            'M': msc,
            'B': bridge}

    def _read_version(self):
        version = self._get_version()
        if version['V'] == 3:
            version = self._get_version_ex()
        version['HW'] = self._com.version
        return Stlink.StlinkVersion(version)

    def _exit_dfu(self):
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.DFU.COMMAND,
            Stlink.CMD.DFU.EXIT)
        self._com.xfer(cmd)

    def _exit_debug(self):
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.EXIT)
        self._com.xfer(cmd)

    def _exit_swim(self):
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.SWIM.COMMAND,
            Stlink.CMD.SWIM.EXIT)
        self._com.xfer(cmd)

    def _get_current_mode(self):
        cmd = _struct.pack(
            '<B',
            Stlink.CMD.GET_CURRENT_MODE)
        res = self._com.xfer(cmd, rx_length=2)
        mode, = _struct.unpack('<H', res)
        return mode

    def _leave_state(self):
        mode = self._get_current_mode()
        if mode == Stlink.CMD.MODE.DFU:
            self._exit_dfu()
        elif mode == Stlink.CMD.MODE.DEBUG:
            self._exit_debug()
        elif mode == Stlink.CMD.MODE.SWIM:
            self._exit_swim()

    def _enter_debug_swd(self):
        cmd = _struct.pack(
            '<BBB',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.ENTER,
            Stlink.CMD.DEBUG.ENTERDEBUG.SWD)
        self._com.xfer(cmd, rx_length=2)

    def _set_swd_freq(self, freq_id):
        cmd = _struct.pack(
            '<BBH',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.SET_SWD_FREQ,
            freq_id)
        res = self._com.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        _check_status(status)

    def _get_com_freq(self, com):
        if self._version.major < 3:
            raise OutdatedStlinkFirmware(self._version.str, "V3")
        cmd = _struct.pack(
            '<BBB',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV3.GET_COM_FREQ,
            com)
        res = self._com.xfer(cmd, rx_length=52)
        status, current_freq, count, *frequencies = _struct.unpack(
            '<HxxLL10L', res)
        _check_status(status)
        return current_freq, frequencies[:count]

    def _set_com_freq(self, freq_khz, com):
        if self._version.major < 3:
            raise OutdatedStlinkFirmware(self._version.str, "V3")
        cmd = _struct.pack(
            '<BBHL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV3.SET_COM_FREQ,
            com,
            freq_khz)
        res = self._com.xfer(cmd, rx_length=8)
        status, set_freq_khz = _struct.unpack('<HxxL', res)
        _check_status(status)
        if freq_khz != set_freq_khz:
            raise StlinkException("Error setting frequency.")

    def _set_swd_freq_v2(self, swd_frequency):
        if self._version.jtag < 22:
            raise OutdatedStlinkFirmware(self._version.str, "J22")
        for freq, freq_id in Stlink._SWD_FREQ:
            if swd_frequency >= freq:
                self._set_swd_freq(freq_id)
                return
        raise StlinkException("Selected SWD frequency is too low")

    def _set_com_freq_v3(self, req_frequency, com):
        req_freq_khz = req_frequency // 1000
        current_freq_khz, frequencies_khz = self._get_com_freq(com)
        if current_freq_khz == req_freq_khz:
            return
        for freq_khz in frequencies_khz:
            if req_freq_khz >= freq_khz:
                self._set_com_freq(freq_khz, com)
                break
        else:
            raise StlinkException("Requested SWD frequency is too low")

    def set_swd_freq(self, swd_frequency):
        """Set frequency for SWD

        Arguments:
            swd_frequency: frequency in Hz
        """
        if self._version.major == 2:
            self._set_swd_freq_v2(swd_frequency)
        elif self._version.major == 3:
            self._set_com_freq_v3(
                swd_frequency,
                Stlink.CMD.DEBUG.APIV3.COM.SWD)

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
        cmd = _struct.pack(
            '<B',
            Stlink.CMD.GET_TARGET_VOLTAGE)
        res = self._com.xfer(cmd, rx_length=8)
        an0 = int.from_bytes(res[:4], byteorder='little')
        an1 = int.from_bytes(res[4:8], byteorder='little')
        return round(2 * an1 * 1.2 / an0, 2) if an0 != 0 else None

    def get_idcode(self):
        """Get core ID from MCU

        Return:
            32 bit number
        """
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_IDCODES)
        res = self._com.xfer(cmd, rx_length=12)
        status, idcode = _struct.unpack('<HxxL4x', res)
        _check_status(status)
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
        cmd = _struct.pack(
            '<BBB',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_REG,
            register)
        res = self._com.xfer(cmd, rx_length=8)
        status, value = _struct.unpack('<HxxL', res)
        _check_status(status)
        return value

    def get_reg_all(self):
        """Get all core registers

        Read all 32 bit CPU core registers (R0, R1, ...)
        Order of registers depends on architecture.
        (MCU must be halted to access core registers)

        Return:
            list of 32 bit numbers
        """
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_ALL_REGS)
        res = self._com.xfer(cmd, rx_length=88)
        status, *values = _struct.unpack('<Hxx21L', res)
        _check_status(status)
        return values

    def set_reg(self, register, value):
        """Set core register

        Write 32 bit CPU core register (e.g. R0, R1, ...)       R
        Register ID depends on architecture.
        (MCU must be halted to access core register)

        Arguments:
            register: register ID
            value: 32 bit number
        """
        cmd = _struct.pack(
            '<BBBL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.WRITE_REG,
            register,
            value)
        res = self._com.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        _check_status(status)

    def get_mem32(self, address):
        """Get 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory

        Return:
            return 32 bit number
        """
        _check_alignment(4, address=address)
        cmd = _struct.pack(
            '<BBL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_DEBUG_REG,
            address)
        res = self._com.xfer(cmd, rx_length=8)
        status, value = _struct.unpack('<HxxL', res)
        _check_status(status)
        return value

    def set_mem32(self, address, value):
        """Set 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            value: 32 bit number
        """
        _check_alignment(4, address=address)
        cmd = _struct.pack(
            '<BBLL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.WRITE_DEBUG_REG,
            address,
            value)
        res = self._com.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        _check_status(status)

    def _get_last_rw_state(self):
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.GET_LAST_RW_STATE)
        res = self._com.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        _check_status(status)

    def _get_last_rw_state_ex(self):
        cmd = _struct.pack(
            '<BB',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.GET_LAST_RW_STATE_EX)
        res = self._com.xfer(cmd, rx_length=12)
        status, fault_address = _struct.unpack('<HxxI4x', res)
        if status == Stlink.STATUS.JTAG_OK:
            return
        if status in Stlink.STATUS.MESSAGES:
            msg = Stlink.STATUS.MESSAGES[status]
            msg = f"{msg} at address: 0x{fault_address:08x}"
            raise StlinkException(msg)
        raise StlinkException("Unknown status")

    def read_mem8(self, address, size, check_last_error_status=True):
        """Read data from memory with 8 bit memory access.

        Maximum number of bytes for read can be 64.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            bytes of data
        """
        if size > self.maximum_8bit_data:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % self.maximum_8bit_data)
        cmd = _struct.pack(
            '<BBLL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.READ_MEM_8BIT,
            address,
            size)
        data = self._com.xfer(cmd, rx_length=size)
        if check_last_error_status:
            self._get_last_rw_state_ex()
        return data

    def write_mem8(self, address, data, check_last_error_status=True):
        """Write data into memory with 8 bit memory access.

        Maximum number of bytes for one write can be 64.

        Arguments:
            address: address in memory
            data: bytes of data to write into memory
        """
        if len(data) > self.maximum_8bit_data:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % self.maximum_8bit_data)
        cmd = _struct.pack(
            '<BBLL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.WRITE_MEM_8BIT,
            address,
            len(data))
        self._com.xfer(cmd, data=data)
        if check_last_error_status:
            self._get_last_rw_state_ex()

    def read_mem16(self, address, size, check_last_error_status=True):
        """Read data from memory with 16 bit memory access.

        Maximum number of bytes for one read can be 1024.
        Address and size must be aligned to 2 Bytes.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            list of read data
        """
        if self._version.major <= 2 and self._version.jtag < 29:
            raise StlinkException(self._version.str, "J29")
        _check_alignment(2, address=address, size=size)
        if size > self.maximum_32bit_data:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % self.maximum_32bit_data)
        cmd = _struct.pack(
            '<BBLL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.READ_MEM_16BIT,
            address,
            size)
        data = self._com.xfer(cmd, rx_length=size)
        if check_last_error_status:
            self._get_last_rw_state_ex()
        return data

    def write_mem16(self, address, data, check_last_error_status=True):
        """Write data into memory with 16 bit memory access.

        Maximum number of bytes for one write can be 1024.
        Address and number of bytes must be aligned to 2 Bytes.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        if self._version.major <= 2 and self._version.jtag < 29:
            raise StlinkException(self._version.str, "J29")
        _check_alignment(2, address=address, size=len(data))
        if len(data) > self.maximum_16bit_data:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % self.maximum_16bit_data)
        cmd = _struct.pack(
            '<BBLL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.APIV2.WRITE_MEM_16BIT,
            address,
            len(data))
        self._com.xfer(cmd, data=data)
        if check_last_error_status:
            self._get_last_rw_state_ex()

    def read_mem32(self, address, size, check_last_error_status=True):
        """Read data from memory with 32 bit memory access.

        Maximum number of bytes for one read can be 1024.
        Address and size must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            list of read data
        """
        _check_alignment(4, address=address, size=size)
        if size > self.maximum_32bit_data:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % self.maximum_32bit_data)
        cmd = _struct.pack(
            '<BBLL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.READ_MEM_32BIT,
            address,
            size)
        data = self._com.xfer(cmd, rx_length=size)
        if check_last_error_status:
            self._get_last_rw_state_ex()
        return data

    def write_mem32(self, address, data, check_last_error_status=True):
        """Write data into memory with 32 bit memory access.

        Maximum number of bytes for one write can be 1024.
        Address and number of bytes must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        _check_alignment(4, address=address, size=len(data))
        if len(data) > self.maximum_32bit_data:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % self.maximum_32bit_data)
        cmd = _struct.pack(
            '<BBLL',
            Stlink.CMD.DEBUG.COMMAND,
            Stlink.CMD.DEBUG.WRITE_MEM_32BIT,
            address,
            len(data))
        self._com.xfer(cmd, data=data)
        if check_last_error_status:
            self._get_last_rw_state_ex()
