"""ST-Link SWIM driver
"""

import struct as _struct
import time as _time
import itertools as _itertools
import swd.stlink.com as _com
import swd.stlink.usb as _usb
from swd.stlink import Stlink as _Stlink


class SwimError(Exception):
    """Swim general error"""


class SwimException(SwimError):
    """Swim general exception"""


class SwimTimeoutException(SwimException):
    """Timeout while waiting for SWIM status"""


class StlinkSwim:
    """ST-Link SWIM driver"""

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

    def __init__(
            self,
            serial_no='',
            debug=0,
            high_speed=True,
            usb=None,
            com=None):
        """StlinkSwim constructor

        Arguments:
            serial_no: serial number or part (begin or end)
            debug: debug level
            high_speed: switch to high speed SWIM after connect
            usb: USB driver instance (for testing)
            com: communication instance (for testing)
        """
        self._debug = debug
        if not usb:
            usb = _usb.StlinkUsb(serial_no, debug=debug)
        if not com:
            com = _com.StlinkCom(usb, debug=debug)
        self._com = com
        self._read_buf_size = 64
        self.high_speed = False
        self._version = self._read_version()
        self._leave_state()
        self._swim_cmd(self._com.CMD.SWIM.ENTER)
        self._read_buffer_size()
        self._read_cap()
        self.assert_reset()
        self._enter_seq()
        # mask internal interrupt sources, enable access to whole of memory,
        # prioritize SWIM; RST will be 0 so a SWIM SRST will not exit SWIM mode
        self.write_mem8(
            self.SWIM_CSR,
            bytes([self.SWIM_CSR_SAFE_MASK
                   | self.SWIM_CSR_SWIM_DM
                   | self.SWIM_CSR_PRI]))
        # halt CPU via debug module
        self.write_mem8(
            self.SWIM_DM_CSR2,
            bytes([self.SWIM_DM_CSR2_STALL]))
        self.force_debug()
        # generate a reset to cause option bytes to load and start the
        # internal clock (HSIT will be set, allowing high speed mode)
        self.generate_reset()
        _time.sleep(0.01)
        self.deassert_reset()
        _time.sleep(0.001)
        if high_speed:
            self.set_high_speed()

    @property
    def maximum_8bit_data(self):
        """Maximum transfer size for 8 bit data"""
        return self._read_buf_size

    @property
    def com(self):
        """Communication class"""
        return self._com

    def _read_version(self):
        ver, _, _ = self._com.get_version()
        version = {
            'V': (ver >> 12) & 0x000f,
            'J': (ver >> 6) & 0x003f}
        if self._com.usb.dev_name == 'V2':
            version['S'] = ver & 0x003f
        elif self._com.usb.dev_name == 'V2-1':
            version['M'] = ver & 0x003f
        if version['V'] == 3:
            major, swim, jtag, msc, bridge, _, _ = self._com.get_version_ex()
            version = {
                'V': major,
                'S': swim,
                'J': jtag,
                'M': msc,
                'B': bridge}
        version['HW'] = self._com.usb.dev_name
        return _Stlink.StlinkVersion(version)

    def _leave_state(self):
        mode = self._com.get_current_mode()
        if mode in (self._com.CMD.MODE.DFU, self._com.CMD.MODE.MASS):
            self._com.exit_dfu()
        elif mode == self._com.CMD.MODE.DEBUG:
            self._com.exit_debug()
        elif mode == self._com.CMD.MODE.SWIM:
            self._com.exit_swim()

    def _swim_cmd(self, subcommand, data=None, rx_length=0, pad=False):
        """Send SWIM command

        Arguments:
            subcommand: SWIM subcommand code
            data: optional data appended to the command
            rx_length: number of expected data to receive
            pad: pad command to 16 Bytes (must be False for SWIM)

        Return:
            received data
        """
        cmd = _struct.pack(
            '<BB',
            self._com.CMD.SWIM.COMMAND,
            subcommand)
        if data:
            cmd += data
        return self._com.usb.xfer(cmd, rx_length=rx_length, pad=pad)

    def _get_status(self):
        """Get SWIM status

        Return:
            status code from SWIM_STATUS
        """
        res = self._swim_cmd(
            self._com.CMD.SWIM.READSTATUS,
            rx_length=4)
        return res[0]

    def _wait_for_status(self, timeout=5.0):
        """Wait until SWIM status is OK

        Arguments:
            timeout: maximum time to wait in seconds

        Raise:
            SwimException: on error status
            SwimTimeoutException: on timeout
        """
        status = _com.StlinkCom.SWIM_STATUS
        start = _time.monotonic()
        while True:
            sw_status = self._get_status()
            if sw_status == status.OK:
                return
            if sw_status == status.BUSY:
                if _time.monotonic() - start > timeout:
                    raise SwimTimeoutException(
                        f"Timeout waiting for SWIM status: 0x{sw_status:x}")
                _time.sleep(0.001)
                continue
            if sw_status in status.MESSAGES:
                raise SwimException(status.MESSAGES[sw_status])
            raise SwimError(f"Unknown SWIM status: 0x{sw_status:x}")

    def _read_buffer_size(self):
        """Read SWIM buffer size (maximum transfer size)"""
        res = self._swim_cmd(
            self._com.CMD.SWIM.READ_BUFFERSIZE,
            rx_length=2)
        self._read_buf_size = int.from_bytes(res, 'little')

    def _read_cap(self):
        """Read SWIM capabilities"""
        self._swim_cmd(
            self._com.CMD.SWIM.READ_CAP,
            data=bytes([0x01]),
            rx_length=8)

    def _enter_seq(self):
        """Enter sequence to get access to SWIM module"""
        self._swim_cmd(self._com.CMD.SWIM.ENTER_SEQ)
        self._wait_for_status()

    def read_mem8(self, address, size):
        """Read data from memory with 8 bit memory access

        Maximum number of bytes is maximum_8bit_data.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            bytes of data
        """
        if size > self.maximum_8bit_data:
            raise SwimException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % self.maximum_8bit_data)
        cmd = _struct.pack(
            '>BBHI',
            self._com.CMD.SWIM.COMMAND,
            self._com.CMD.SWIM.READMEM,
            size,
            address)
        self._com.usb.xfer(cmd, pad=False)
        self._wait_for_status()
        cmd = _struct.pack(
            '<BB',
            self._com.CMD.SWIM.COMMAND,
            self._com.CMD.SWIM.READBUF)
        return self._com.usb.xfer(cmd, rx_length=size, pad=False)

    def write_mem8(self, address, data):
        """Write data into memory with 8 bit memory access

        Maximum number of bytes is maximum_8bit_data.

        Arguments:
            address: address in memory
            data: bytes of data to write into memory
        """
        if len(data) > self.maximum_8bit_data:
            raise SwimException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % self.maximum_8bit_data)
        cmd = _struct.pack(
            '>BBHI',
            self._com.CMD.SWIM.COMMAND,
            self._com.CMD.SWIM.WRITEMEM,
            len(data),
            address)
        self._com.usb.xfer(cmd, data=data, pad=False)
        self._wait_for_status()

    def read_mem(self, address, size):
        """Read data from memory

        Data are read in chunks of maximum_8bit_data bytes.

        Arguments:
            address: address in memory
            size: number of bytes to read from memory

        Return:
            bytes of data
        """
        data = bytearray()
        while size:
            chunk_size = min(size, self.maximum_8bit_data)
            data += self.read_mem8(address, chunk_size)
            address += chunk_size
            size -= chunk_size
        return bytes(data)

    def write_mem(self, address, data):
        """Write data into memory

        Data are written in chunks of maximum_8bit_data bytes.

        Arguments:
            address: address in memory
            data: bytes of data to write into memory
        """
        data = iter(data)
        while True:
            chunk = bytes(
                _itertools.islice(data, 0, self.maximum_8bit_data))
            if not chunk:
                return
            self.write_mem8(address, chunk)
            address += len(chunk)

    def get_mem32(self, address):
        """Get 32 bit memory register

        Address does not need to be aligned.

        Arguments:
            address: address in memory

        Return:
            32 bit number
        """
        return int.from_bytes(self.read_mem(address, 4), 'little')

    def set_mem32(self, address, value):
        """Set 32 bit memory register

        Address does not need to be aligned.

        Arguments:
            address: address in memory
            value: 32 bit number
        """
        self.write_mem(address, value.to_bytes(4, 'little'))

    def assert_reset(self):
        """Assert reset line"""
        self._swim_cmd(self._com.CMD.SWIM.ASSERT_RESET)
        self._wait_for_status()

    def deassert_reset(self):
        """Deassert reset line"""
        self._swim_cmd(self._com.CMD.SWIM.DEASSERT_RESET)
        self._wait_for_status()

    def generate_reset(self):
        """Generate SWIM system reset"""
        self._swim_cmd(self._com.CMD.SWIM.GEN_RST)

    def srst(self):
        """SWIM system reset, requires SWIM debug mode (SWIM_DM)"""
        csr = self.read_mem8(self.SWIM_CSR, 1)
        if not csr[0] & self.SWIM_CSR_SWIM_DM:
            raise SwimException("SWIM not in debug mode")
        self.generate_reset()

    def set_high_speed(self):
        """Switch to high speed SWIM format (UM0470: 3.3)"""
        csr = self.read_mem8(self.SWIM_CSR, 1)[0]
        if csr & self.SWIM_CSR_HSIT:
            self.write_mem8(self.SWIM_CSR, bytes([csr | self.SWIM_CSR_HS]))
            # tell ST-Link to use high speed format
            self._swim_cmd(
                self._com.CMD.SWIM.SPEED,
                data=bytes([0x01]))
            self.high_speed = True

    def force_debug(self, wait=True):
        if wait:
            return self._com.debug_force()
        return self._com.debug_force(no_wait=True)

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
        return self._com.get_target_voltage()

    def exit_swim(self):
        """Exit SWIM mode"""
        self._com.exit_swim()


def _iter_slice(data, size):
    """Yield next size bytes from data iterator"""
    import itertools as _itertools
    return _itertools.islice(data, 0, size)
