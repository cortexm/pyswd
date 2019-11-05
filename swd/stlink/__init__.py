"""Stlink package
"""

import swd.stlink.com as _com
import swd.stlink.usb as _usb


class StlinkError(Exception):
    """StlinkCom general error"""


class StlinkException(StlinkError):
    """StlinkCom general error"""


class StlinkOutdatedFirmware(StlinkException):
    """StlinkCom general exception"""
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
        StlinkComException: on error
        StlinkComError: on unknown status

    """
    if status == _com.StlinkCom.STATUS.JTAG_OK:
        return
    if status in _com.StlinkCom.STATUS.MESSAGES:
        raise StlinkException(_com.StlinkCom.STATUS.MESSAGES[status])
    raise StlinkError(f"Unknown status: 0x{status:x}")


class Stlink:
    """Stlink driver"""
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

    def __init__(
            self,
            swd_frequency=None,
            serial_no='',
            debug=0,
            usb=None,
            com=None):
        self._debug = debug
        if not usb:
            usb = _usb.StlinkUsb(serial_no, debug=debug)
        if not com:
            com = _com.StlinkCom(usb, debug=debug)
        self._com = com
        self._version = self._read_version()
        self._leave_state()
        if swd_frequency:
            self.set_swd_freq(swd_frequency)
        status = self._com.enter_debug_swd()
        _check_status(status)

    @property
    def maximum_8bit_data(self):
        """Maximum transfer size for 8 bit data"""
        return self._com.STLINK_MAXIMUM_8BIT_DATA

    @property
    def maximum_16bit_data(self):
        """Maximum transfer size for 16 bit data"""
        return self._com.usb.STLINK_MAXIMUM_TRANSFER_SIZE

    @property
    def maximum_32bit_data(self):
        """Maximum transfer size for 32 bit data"""
        return self._com.usb.STLINK_MAXIMUM_TRANSFER_SIZE

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
            major, swim, jtag, bridge, msc, _, _ = self._com.get_version_ex()
            version = {
                'V': major,
                'S': swim,
                'J': jtag,
                'M': msc,
                'B': bridge}
        version['HW'] = self._com.usb.dev_name
        return self.StlinkVersion(version)

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

    def _leave_state(self):
        mode = self._com.get_current_mode()
        if mode in (self._com.CMD.MODE.DFU, self._com.CMD.MODE.MASS):
            self._com.exit_dfu()
        elif mode == self._com.CMD.MODE.DEBUG:
            self._com.exit_debug()
        elif mode == self._com.CMD.MODE.SWIM:
            self._com.exit_swim()

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
                self._com.CMD.DEBUG.APIV3.COM.SWD)

    def _set_swd_freq_v2(self, swd_frequency):
        if self._version.jtag < 20:
            raise StlinkOutdatedFirmware(self._version.str, "J20")
        for freq, freq_id in self._com.SWD_FREQ:
            if swd_frequency >= freq:
                status = self._com.set_swd_freq(freq_id)
                _check_status(status)
                break
        else:
            raise StlinkException("Selected SWD frequency is too low")

    def _set_com_freq_v3(self, req_frequency, com):
        if self._version.major < 3:
            raise StlinkError("This command require ST-Link/V3")
        req_freq_khz = req_frequency // 1000
        status, current_freq_khz, frequencies_khz = self._com.get_com_freq(com)
        _check_status(status)
        if current_freq_khz == req_freq_khz:
            return
        for freq_khz in frequencies_khz:
            if req_freq_khz >= freq_khz:
                status, set_freq_khz = self._com.set_com_freq(freq_khz, com)
                _check_status(status)
                if freq_khz != set_freq_khz:
                    raise StlinkError("Error setting frequency.")
                break
        else:
            raise StlinkException("Requested SWD frequency is too low")

    def get_idcode(self):
        """Get core ID from MCU

        Return:
            32 bit number
        """
        status, idcode = self._com.get_idcode()
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
        status, value = self._com.get_reg(register)
        _check_status(status)
        return value

    def get_reg_all(self):
        """Get all core registers

        Read all 32 bit CPU core registers (R0, R1, ...)
        Order of registers depends on architecture.
        (MCU must be halted to access core registers)

        Return:
            status: command status
            list of 32 bit numbers
        """
        status, values = self._com.get_reg_all()
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

        Return:
            status: command status
        """
        status = self._com.set_reg(register, value)
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
        status, value = self._com.get_mem32(address)
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
        status = self._com.set_mem32(address, value)
        _check_status(status)

    def _check_last_rw_state(self):
        status, fault_address = self._com.get_last_rw_state_ex()
        if status == self._com.STATUS.JTAG_OK:
            return
        if status in self._com.STATUS.MESSAGES:
            msg = self._com.STATUS.MESSAGES[status]
            msg = f"{msg} at address: 0x{fault_address:08x}"
            raise StlinkException(msg)
        raise StlinkError("Unknown status")

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
        data = self._com.read_mem8(address, size)
        if check_last_error_status:
            self._check_last_rw_state()
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
        self._com.write_mem8(address, data)
        if check_last_error_status:
            self._check_last_rw_state()

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
        if self._version.major <= 2 and self._version.jtag < 26:
            raise StlinkException(self._version.str, "J26")
        _check_alignment(2, address=address, size=size)
        if size > self.maximum_32bit_data:
            raise StlinkException(
                'Too many Bytes to read (maximum is %d Bytes)'
                % self.maximum_32bit_data)
        data = self._com.read_mem16(address, size)
        if check_last_error_status:
            self._check_last_rw_state()
        return data

    def write_mem16(self, address, data, check_last_error_status=True):
        """Write data into memory with 16 bit memory access.

        Maximum number of bytes for one write can be 1024.
        Address and number of bytes must be aligned to 2 Bytes.

        Arguments:
            address: address in memory
            data: list of bytes to write into memory
        """
        if self._version.major <= 2 and self._version.jtag < 26:
            raise StlinkException(self._version.str, "J26")
        _check_alignment(2, address=address, size=len(data))
        if len(data) > self.maximum_32bit_data:
            raise StlinkException(
                'Too many Bytes to write (maximum is %d Bytes)'
                % self.maximum_32bit_data)
        self._com.write_mem16(address, data)
        if check_last_error_status:
            self._check_last_rw_state()

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
        data = self._com.read_mem32(address, size)
        if check_last_error_status:
            self._check_last_rw_state()
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
        self._com.write_mem32(address, data)
        if check_last_error_status:
            self._check_last_rw_state()
