"""ST-Link/V2 driver
"""

import struct as _struct


class StlinkCom:
    """ST-Link class"""

    class CMD:  # pylint: disable=too-few-public-methods
        """StlinkCom commands"""

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

    SWD_FREQ = (
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

    JTAG_FREQ = (
        (18000000, 2),
        (9000000, 4),
        (4500000, 8),
        (2250000, 16),
        (1120000, 32),
        (560000, 64),
        (280000, 128),
        (140000, 256),
    )

    STLINK_MAXIMUM_8BIT_DATA = 64

    def __init__(self, usb):
        """Stlink constructor

        Attributes:
            serial_no: serial number or part (begin or end
            debug: debug level
        """
        self._usb = usb

    @property
    def usb(self):
        """Read USB device name"""
        return self._usb

    def get_version(self):
        """Get ST-Link version

        Returns: tuple with:
            ver: encoded version
            vid: USB Vendor ID
            pid: USB Product ID
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.GET_VERSION,
            0x80)
        res = self._usb.xfer(cmd, rx_length=6)
        ver, = _struct.unpack('>H4x', res)  # big endian
        vid, pid = _struct.unpack('<xxHH', res)  # little endian
        return ver, vid, pid

    def get_version_ex(self):
        """Get ST-Link version

        Returns: tuple with:
            major: major version number
            swim: SWIM version number
            jtag: JTAG version number
            msc: MSC version number
            bridge: bridge version number
            vid: USB Vendor ID
            pid: USB Product ID
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.GET_VERSION_EX,
            0x80)
        res = self._usb.xfer(cmd, rx_length=12)
        major, swim, jtag, msc, bridge, vid, pid = _struct.unpack(
            '<5B3xHH', res)
        return major, swim, jtag, msc, bridge, vid, pid

    def exit_dfu(self):
        """Exit DFU mode
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.DFU.COMMAND,
            self.CMD.DFU.EXIT)
        self._usb.xfer(cmd)

    def exit_debug(self):
        """Exit debug mode
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.EXIT)
        self._usb.xfer(cmd)

    def exit_swim(self):
        """Exit SWIM mode
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.SWIM.COMMAND,
            self.CMD.SWIM.EXIT)
        self._usb.xfer(cmd)

    def get_current_mode(self):
        """Get current mode
        """
        cmd = _struct.pack(
            '<B',
            self.CMD.GET_CURRENT_MODE)
        res = self._usb.xfer(cmd, rx_length=2)
        mode, = _struct.unpack('<Bx', res)
        return mode

    def enter_debug_swd(self):
        """Enter debug mode

        Returns:
            status: command status
        """
        cmd = _struct.pack(
            '<BBB',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.ENTER,
            self.CMD.DEBUG.ENTERDEBUG.SWD)
        res = self._usb.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        return status

    def set_swd_freq(self, freq_id):
        """Set SWD frequency

        Arguments:
            freq_id: ID from SWD_FREQ

        Returns:
            status: command status
        """
        cmd = _struct.pack(
            '<BBH',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.SET_SWD_FREQ,
            freq_id)
        res = self._usb.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        return status

    def get_com_freq(self, com):
        """Get communication frequency

        Arguments:
            com: COM.SWD or COM.JTAG

        Returns: tuple with:
            status: command status
            current_freq: current communication frequency in kHz
            frequencies: possible frequencies in kHz
        """
        cmd = _struct.pack(
            '<BBB',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV3.GET_COM_FREQ,
            com)
        res = self._usb.xfer(cmd, rx_length=52)
        status, current_freq, count, *frequencies = _struct.unpack(
            '<HxxLL10L', res)
        return status, current_freq, frequencies[:count]

    def set_com_freq(self, freq_khz, com):
        """Set communication frequency

        Arguments:
            freq_khz: frequency to set in kHz
            com: COM.SWD or COM.JTAG

        Returns: tuple with:
            status: command status
            set_freq_khz: set frequency in kHz
        """
        cmd = _struct.pack(
            '<BBHL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV3.SET_COM_FREQ,
            com,
            freq_khz)
        res = self._usb.xfer(cmd, rx_length=8)
        status, set_freq_khz = _struct.unpack('<HxxL', res)
        return status, set_freq_khz

    def get_target_voltage(self):
        """Get target voltage from debugger

        Return:
            measured voltage
        """
        cmd = _struct.pack(
            '<B',
            self.CMD.GET_TARGET_VOLTAGE)
        res = self._usb.xfer(cmd, rx_length=8)
        an0, an1 = _struct.unpack('<LL', res)
        return round(2 * an1 * 1.2 / an0, 2) if an0 != 0 else None

    def get_idcode(self):
        """Get core ID from MCU

        Returns: tuple with:
            status: command status
            32 bit number
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.READ_IDCODES)
        res = self._usb.xfer(cmd, rx_length=12)
        status, idcode = _struct.unpack('<HxxL4x', res)
        return status, idcode

    def get_reg(self, register):
        """Get core register

        Read 32 bit CPU core register (e.g. R0, R1, ...)
        Register ID depends on architecture.
        (MCU must be halted to access core register)

        Arguments:
            register: register ID

        Returns: tuple with:
            status: command status
            32 bit number
        """
        cmd = _struct.pack(
            '<BBB',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.READ_REG,
            register)
        res = self._usb.xfer(cmd, rx_length=8)
        status, value = _struct.unpack('<HxxL', res)
        return status, value

    def get_reg_all(self):
        """Get all core registers

        Read all 32 bit CPU core registers (R0, R1, ...)
        Order of registers depends on architecture.
        (MCU must be halted to access core registers)

        Returns: tuple with:
            status: command status
            list of 32 bit numbers
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.READ_ALL_REGS)
        res = self._usb.xfer(cmd, rx_length=88)
        status, *values = _struct.unpack('<Hxx21L', res)
        return status, values

    def set_reg(self, register, value):
        """Set core register

        Write 32 bit CPU core register (e.g. R0, R1, ...)       R
        Register ID depends on architecture.
        (MCU must be halted to access core register)

        Arguments:
            register: register ID
            value: 32 bit number

        Return:
            status: command status
        """
        cmd = _struct.pack(
            '<BBBL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.WRITE_REG,
            register,
            value)
        res = self._usb.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        return status

    def get_ap_reg(self, ap_sel, register):
        """Get AP register

        Arguments:
            ap_sel: AP address space selection
            register: register ID

        Returns: tuple with:
            status: command status
            32 bit number
        """
        cmd = _struct.pack(
            '<BBHH',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.READ_AP_REG,
            ap_sel,
            register)
        res = self._usb.xfer(cmd, rx_length=8)
        status, value = _struct.unpack('<HxxL', res)
        return status, value

    def set_ap_reg(self, ap_sel, register, value):
        """Set AP register

        Arguments:
            ap_sel: AP address space selection
            register: register ID
            value: 32 bit number

        Return:
            status: command status
        """
        cmd = _struct.pack(
            '<BBHHL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.WRITE_REG,
            ap_sel,
            register,
            value)
        res = self._usb.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        return status

    def get_mem32(self, address):
        """Get 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory

        Returns: tuple with:
            status: command status
            return 32 bit number
        """
        cmd = _struct.pack(
            '<BBL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.READ_DEBUG_REG,
            address)
        res = self._usb.xfer(cmd, rx_length=8)
        status, value = _struct.unpack('<HxxL', res)
        return status, value

    def set_mem32(self, address, value):
        """Set 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            value: 32 bit number

        Return:
            status: command status
        """
        cmd = _struct.pack(
            '<BBLL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.WRITE_DEBUG_REG,
            address,
            value)
        res = self._usb.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        return status

    def get_last_rw_state(self):
        """Get last RW state after bulk R/W operation

        Returns:
            RW status from STATUS
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.GET_LAST_RW_STATE)
        res = self._usb.xfer(cmd, rx_length=2)
        status, = _struct.unpack('<H', res)
        return status

    def get_last_rw_state_ex(self):
        """Get last RW state after bulk R/W operation

        Returns: tuple with:
            status: last RW from STATUS
            fault_address: fault address
        """
        cmd = _struct.pack(
            '<BB',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.GET_LAST_RW_STATE_EX)
        res = self._usb.xfer(cmd, rx_length=12)
        status, fault_address = _struct.unpack('<HxxI4x', res)
        return status, fault_address

    def read_mem8(self, address, size):
        """Read data from memory with 8 bit memory access.

        Maximum number of bytes for read can be 64.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            bytes of data
        """
        cmd = _struct.pack(
            '<BBLL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.READ_MEM_8BIT,
            address,
            size)
        return self._usb.xfer(cmd, rx_length=size)

    def write_mem8(self, address, data):
        """Write data into memory with 8 bit memory access.

        Maximum number of bytes for one write can be 64.

        Arguments:
            address: address in memory
            data: bytes of data to write into memory
        """
        cmd = _struct.pack(
            '<BBLL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.WRITE_MEM_8BIT,
            address,
            len(data))
        self._usb.xfer(cmd, data=data)

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
        cmd = _struct.pack(
            '<BBLL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.READ_MEM_16BIT,
            address,
            size)
        return self._usb.xfer(cmd, rx_length=size)

    def write_mem16(self, address, data):
        """Write data into memory with 16 bit memory access.

        Maximum number of bytes for one write can be 1024.
        Address and number of bytes must be aligned to 2 Bytes.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        cmd = _struct.pack(
            '<BBLL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.APIV2.WRITE_MEM_16BIT,
            address,
            len(data))
        self._usb.xfer(cmd, data=data)

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
        cmd = _struct.pack(
            '<BBLL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.READ_MEM_32BIT,
            address,
            size)
        return self._usb.xfer(cmd, rx_length=size)

    def write_mem32(self, address, data):
        """Write data into memory with 32 bit memory access.

        Maximum number of bytes for one write can be 1024.
        Address and number of bytes must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        cmd = _struct.pack(
            '<BBLL',
            self.CMD.DEBUG.COMMAND,
            self.CMD.DEBUG.WRITE_MEM_32BIT,
            address,
            len(data))
        self._usb.xfer(cmd, data=data)
