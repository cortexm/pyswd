"""ST-Link/V2 USB communication
"""

import sys as _sys
import usb as _usb


class StlinkComError(Exception):
    """StlinkCom general errors"""


class StlinkComException(Exception):
    """StlinkCom general exception"""


class NoDeviceFoundException(StlinkComException):
    """Exception raised when no STLink device is connected"""


class MoreDevicesException(StlinkComException):
    """Exception raised when more devices was detected"""

    def __init__(self, devices):
        super().__init__("More than one device found.")
        self._serial_numbers = [dev.serial_no for dev in devices]

    @property
    def serial_numbers(self):
        """return list of serial numbers"""
        return self._serial_numbers


class StlinkComBase:
    """ST link comm base class"""
    ID_VENDOR = None
    ID_PRODUCT = None
    PIPE_OUT = None
    PIPE_IN = None
    DEV_NAME = None

    def __init__(self, dev):
        self._dev = dev

    @classmethod
    def find_all(cls):
        """return all devices with this idVendor and idProduct"""
        devices = []
        try:
            usb_devices = _usb.core.find(
                idVendor=cls.ID_VENDOR,
                idProduct=cls.ID_PRODUCT,
                find_all=True)
            for device in usb_devices:
                devices.append(cls(device))
        except _usb.NoBackendError as err:
            raise StlinkComException("USB Error: %s" % err)
        return devices

    @property
    def serial_no(self):
        """Return device serial number"""
        serial_no = self._dev.serial_number
        try:
            if serial_no.isalnum():
                return serial_no
            return ''.join(['%02X' % ord(c) for c in serial_no])
        except NotImplementedError as err:
            return "unknown"

    def compare_serial_no(self, serial_no):
        """Compare device serial no with selected serial number"""
        if self.serial_no.startswith(serial_no):
            return True
        if self.serial_no.endswith(serial_no):
            return True
        return False

    def write(self, data, timeout=200):
        """Write data to USB pipe"""
        try:
            count = self._dev.write(self.PIPE_OUT, data, timeout)
        except _usb.USBError as err:
            self._dev = None
            raise StlinkComException("USB Error: %s" % err)
        if count != len(data):
            raise StlinkComException("Error Sending data")

    def read(self, size, timeout=200):
        """Read data from USB pipe"""
        try:
            data = self._dev.read(self.PIPE_IN, size, timeout).tobytes()
        except _usb.USBError as err:
            self._dev = None
            raise StlinkComException("USB Error: %s" % err)
        return data

    def __del__(self):
        if self._dev is not None:
            self._dev.finalize()


class StlinkComV2Usb(StlinkComBase):
    """ST-Link/V2 USB communication class"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x3748
    PIPE_OUT = 0x02
    PIPE_IN = 0x81
    DEV_NAME = "V2"


class StlinkComV21MUsb(StlinkComBase):
    """ST-Link/V2-1 USB communication"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x374b
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V2-1"


class StlinkComV21Usb(StlinkComBase):
    """ST-Link/V2-1 USB communication"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x3752
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V2-1"


class StlinkComV3EUsb(StlinkComBase):
    """ST-Link/V3 USB communication"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x374e
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V3E"


class StlinkComV3Usb(StlinkComBase):
    """ST-Link/V3 USB communication"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x374f
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V3"


class StlinkCom:
    """ST-Link communication class"""
    STLINK_MAXIMUM_TRANSFER_SIZE = 6144
    _STLINK_CMD_SIZE = 16
    _COM_CLASSES = [
        StlinkComV2Usb,
        StlinkComV21MUsb,
        StlinkComV21Usb,
        StlinkComV3EUsb,
        StlinkComV3Usb
    ]

    @classmethod
    def _find_all_devices(cls):
        devices = []
        for com_cls in cls._COM_CLASSES:
            devices.extend(com_cls.find_all())
        return devices

    @staticmethod
    def _filter_devices(devices, serial_no):
        filtered_devices = []
        for dev in devices:
            serial = dev.serial_no
            if serial.startswith(serial_no) or serial.endswith(serial_no):
                filtered_devices.append(dev)
        return filtered_devices

    def print_debug(self, msg, level=0):
        """Print info string"""
        if self._debug >= level:
            _sys.stderr.write(f"D: {msg}\n")

    def print_debug_data(self, msg, data, level=0):
        """Print info string with hexadecimal representation of data"""
        if self._debug >= level:
            if data is None:
                _sys.stderr.write(f"{msg}\n")
            else:
                _sys.stderr.write(
                    f"{msg}: {' '.join([f'{i:02x}' for i in data])}\n")

    def __init__(self, serial_no='', debug=0):
        self._dev = None
        self._debug = debug
        devices = StlinkCom._find_all_devices()
        if serial_no:
            devices = StlinkCom._filter_devices(devices, serial_no)
        if not devices:
            raise NoDeviceFoundException()
        if len(devices) > 1:
            raise MoreDevicesException(devices)
        self._dev = devices[0]

    @property
    def version(self):
        """property with device version"""
        return self._dev.DEV_NAME

    def xfer(self, command, data=None, rx_length=0, timeout=200):
        """Transfer command between ST-Link

        Arguments:
            command: is an list of bytes with command (max 16 bytes)
            data: data will be sent after command
            rx_length: number of expected data to receive after command
                and data transfer
            timeout: maximum waiting time for received data in ms

        Return:
            received data

        Raises:
            StlinkComException
        """
        if not isinstance(command, bytes):
            raise StlinkComError("command is not type of bytes")
        self.print_debug_data("command", command, level=3)
        if len(command) > self._STLINK_CMD_SIZE:
            raise StlinkComError(
                "Error too many Bytes in command (maximum is %d Bytes)"
                % self._STLINK_CMD_SIZE)
        # pad to _STLINK_CMD_SIZE
        command += b'\x00' * (self._STLINK_CMD_SIZE - len(command))
        self.print_debug_data("USB:WR", command, level=4)
        self._dev.write(command, timeout)
        if data:
            if not isinstance(data, bytes):
                raise StlinkComError("command is not type of bytes")
            self.print_debug_data("USB:WR", data, level=4)
            self._dev.write(data, timeout)
        if rx_length:
            # minimum read length is 2 bytes
            data = self._dev.read(max(2, rx_length))
            self.print_debug_data("USB:RD", data, level=4)
            if len(data) != rx_length:
                data = data[:rx_length]
            return data
        return None
