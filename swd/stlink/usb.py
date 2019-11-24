"""ST-Link USB communication
"""

import usb as _usb
import logging as _logging


class StlinkUsbError(Exception):
    """StlinkUsb general errors"""


class StlinkUsbException(Exception):
    """StlinkUsb general exception"""


class NoDeviceFoundException(StlinkUsbException):
    """Exception raised when no STLink device is connected"""


class MoreDevicesException(StlinkUsbException):
    """Exception raised when more devices was detected"""

    def __init__(self, devices):
        super().__init__("More than one device found.")
        self._devices = devices

    @property
    def serial_numbers(self):
        """return list of serial numbers"""
        return [f"{dev.serial_no} : {dev.DEV_NAME}" for dev in self._devices]


class StlinkUsbBase:
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
        except _usb.core.NoBackendError as err:
            raise StlinkUsbException("USB Error: %s" % err)
        return devices

    @property
    def serial_no(self):
        """Return device serial number"""
        try:
            serial_no = self._dev.serial_number
        except ValueError:
            return None
        try:
            if serial_no.isalnum():
                return serial_no
            return ''.join(['%02X' % ord(c) for c in serial_no])
        except NotImplementedError:
            return None

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
            raise StlinkUsbException("USB Error: %s" % err)
        if count != len(data):
            raise StlinkUsbException("Error Sending data")

    def read(self, size, timeout=200):
        """Read data from USB pipe"""
        try:
            data = self._dev.read(self.PIPE_IN, size, timeout).tobytes()
        except _usb.USBError as err:
            self._dev = None
            raise StlinkUsbException("USB Error: %s" % err)
        return data

    def __del__(self):
        if self._dev is not None:
            self._dev.finalize()


class StlinkUsbV2(StlinkUsbBase):
    """ST-Link/V2 USB communication class"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x3748
    PIPE_OUT = 0x02
    PIPE_IN = 0x81
    DEV_NAME = "V2"


class StlinkUsbV21M(StlinkUsbBase):
    """ST-Link/V2-1 USB communication"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x374b
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V2-1"


class StlinkUsbV21(StlinkUsbBase):
    """ST-Link/V2-1 USB communication without mass storage"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x3752
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V2-1"


class StlinkUsbV3E(StlinkUsbBase):
    """ST-Link/V3 USB communication"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x374e
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V3E"


class StlinkUsbV3(StlinkUsbBase):
    """ST-Link/V3 USB communication"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x374f
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V3"


class StlinkUsbV3(StlinkUsbBase):
    """ST-Link/V3 USB communication without mass storage"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x3753
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V3"


class StlinkUsb:
    """ST-Link communication class"""
    STLINK_MAXIMUM_TRANSFER_SIZE = 6144
    _STLINK_CMD_SIZE = 16
    _COM_CLASSES = [
        StlinkUsbV2,
        StlinkUsbV21M,
        StlinkUsbV21,
        StlinkUsbV3E,
        StlinkUsbV3
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
            if serial and (serial.startswith(serial_no) or serial.endswith(serial_no)):
                filtered_devices.append(dev)
            else:
                del dev
        return filtered_devices

    def print_debug_data(self, msg, data):
        """Print info string with hexadecimal representation of data"""
        if self._logger.isEnabledFor(_logging.DEBUG):
            self._logger.debug(
                msg=f"{msg}: {' '.join([f'{i:02x}' for i in data])}")

    def __init__(self, serial_no=''):
        self._logger = _logging.getLogger('swd:stlink:usb')
        self._dev = None
        devices = StlinkUsb._find_all_devices()
        if serial_no:
            devices = StlinkUsb._filter_devices(devices, serial_no)
        if not devices:
            raise NoDeviceFoundException()
        if len(devices) > 1:
            raise MoreDevicesException(devices)
        self._dev = devices[0]

    @property
    def dev_name(self):
        """property with device name"""
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
            StlinkUsbException
        """
        if not isinstance(command, bytes):
            raise StlinkUsbError("command is not type of bytes")
        self.print_debug_data("command", command)
        if len(command) > self._STLINK_CMD_SIZE:
            raise StlinkUsbError(
                "Error too many Bytes in command (maximum is %d Bytes)"
                % self._STLINK_CMD_SIZE)
        # pad to _STLINK_CMD_SIZE
        command += b'\x00' * (self._STLINK_CMD_SIZE - len(command))
        self.print_debug_data("USB:WR", command)
        self._dev.write(command, timeout)
        if data:
            if not isinstance(data, bytes):
                raise StlinkUsbError("data are not type of bytes")
            self.print_debug_data("USB:WR", data)
            self._dev.write(data, timeout)
        if rx_length:
            # minimum read length is 2 bytes
            data = self._dev.read(max(2, rx_length))
            self.print_debug_data("USB:RD", data)
            if len(data) != rx_length:
                data = data[:rx_length]
            return data
        return None
