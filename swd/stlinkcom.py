"""ST-Link/V2 USB communication
"""

import logging as _logging
import usb.core as _usb


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


def _hex_data(data):
    """Return hexadecimal representation of array of bytes"""
    if data is None:
        return None
    return "[%s]" % ', '.join(['0x%02x' % i for i in data])


class StlinkComBase:
    """ST link comm base class"""
    ID_VENDOR = None
    ID_PRODUCT = None
    PIPE_OUT = None
    PIPE_IN = None

    def __init__(self, dev):
        self._dev = dev

    @classmethod
    def find_all(cls):
        """return all devices with this idVendor and idProduct"""
        devices = []
        try:
            usb_devices = _usb.find(
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
        try:
            return ''.join(['%02X' % ord(c) for c in self._dev.serial_number])
        except NotImplementedError as err:
            _logging.warning("Getting version is not implemented: %s", err)
            return ""

    def compare_serial_no(self, serial_no):
        """Compare device serial no with selected serial number"""
        if self.serial_no.startswith(serial_no):
            return True
        if self.serial_no.endswith(serial_no):
            return True
        return False

    def write(self, data, tout=200):
        """Write data to USB pipe"""
        _logging.debug("data: %s", _hex_data(data))
        try:
            count = self._dev.write(self.PIPE_OUT, data, tout)
        except _usb.USBError as err:
            self._dev = None
            raise StlinkComException("USB Error: %s" % err)
        if count != len(data):
            raise StlinkComException("Error Sending data")

    def read(self, size, tout=200):
        """Read data from USB pipe"""
        read_size = max(size, 16)
        try:
            data = self._dev.read(self.PIPE_IN, read_size, tout).tolist()
        except _usb.USBError as err:
            self._dev = None
            raise StlinkComException("USB Error: %s" % err)
        _logging.debug("data: %s", _hex_data(data))
        data = data[:size]
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


class StlinkComV21Usb(StlinkComBase):
    """ST-Link/V2-1 USB communication"""
    ID_VENDOR = 0x0483
    ID_PRODUCT = 0x374b
    PIPE_OUT = 0x01
    PIPE_IN = 0x81
    DEV_NAME = "V2-1"


class StlinkCom:
    """ST-Link communication class"""
    _STLINK_CMD_SIZE = 16
    _COM_CLASSES = [StlinkComV2Usb, StlinkComV21Usb]

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

    def __init__(self, serial_no=''):
        self._dev = None
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

    def xfer(self, command, data=None, rx_length=0, tout=200):
        """Transfer command between ST-Link

        Arguments:
            command: is an list of bytes with command (max 16 bytes)
            data: data will be sent after command
            rx_length: number of expected data to receive after command
                and data transfer
            tout: maximum waiting time for received data in ms

        Return:
            received data

        Raises:
            StlinkComException
        """
        _logging.info("command: %s", _hex_data(command))
        if len(command) > self._STLINK_CMD_SIZE:
            raise StlinkComException(
                "Error too many Bytes in command (maximum is %d Bytes)"
                % self._STLINK_CMD_SIZE)
        # pad to _STLINK_CMD_SIZE
        command += [0] * (self._STLINK_CMD_SIZE - len(command))
        self._dev.write(command, tout)
        if data:
            _logging.info("write: %s", _hex_data(data))
            self._dev.write(data, tout)
        if rx_length:
            data = self._dev.read(rx_length)
            _logging.info("read: %s", _hex_data(data))
            return data
        return None
