"""SWIM protocol
"""

import itertools as _itertools
from swd.stlink.swim import StlinkSwim as _StlinkSwim


class Swim():
    """Swim class"""

    def __init__(self, driver=None, serial_no='', debug=0, high_speed=True):
        self._debug = debug
        if driver is None:
            # default SWIM driver is StlinkSwim
            driver = _StlinkSwim(
                serial_no=serial_no,
                debug=debug,
                high_speed=high_speed)
        self._drv = driver

    def get_version(self):
        """Get SWIM driver version

        Return:
            device version instance
        """
        return self._drv.get_version()

    def get_target_voltage(self):
        """Get target voltage from debugger

        Return:
            measured voltage
        """
        return self._drv.get_target_voltage()

    def srst(self):
        """Generate target system reset (SRST)"""
        self._drv.srst()

    def force_debug(self, wait=True):
        return self._drv.force_debug(wait=wait)

    def close(self):
        if hasattr(self._drv, 'exit_swim'):
            self._drv.exit_swim()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    @property
    def high_speed(self):
        return getattr(self._drv, 'high_speed', False)

    @high_speed.setter
    def high_speed(self, value):
        if hasattr(self._drv, 'high_speed'):
            self._drv.high_speed = value

    @property
    def maximum_8bit_data(self):
        """Maximum transfer size for 8 bit data"""
        return self._drv.maximum_8bit_data

    @property
    def maximum_16bit_data(self):
        """Maximum transfer size for 16 bit data (emulated with 8 bit access)"""
        return self._drv.maximum_8bit_data

    @property
    def maximum_32bit_data(self):
        """Maximum transfer size for 32 bit data (emulated with 8 bit access)"""
        return self._drv.maximum_8bit_data

    @property
    def com(self):
        """Communication class"""
        return self._drv.com

    def get_mem32(self, address):
        """Get 32 bit memory register

        Address does not need to be aligned.

        Arguments:
            address: address in memory

        Return:
            return 32 bit number
        """
        return self._drv.get_mem32(address)

    def set_mem32(self, address, value):
        """Set 32 bit memory register

        Address does not need to be aligned.

        Arguments:
            address: address in memory
            value: 32 bit number
        """
        self._drv.set_mem32(address, value)

    def read_mem(self, address, size):
        """Read bytes memory

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            bytes of read data
        """
        data = bytearray()
        while size:
            chunk_size = min(size, self.maximum_8bit_data)
            data += self._drv.read_mem8(address, chunk_size)
            address += chunk_size
            size -= chunk_size
        return bytes(data)

    def write_mem(self, address, data):
        """Write memory

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        data = iter(data)
        while True:
            chunk = bytes(
                _itertools.islice(data, 0, self.maximum_8bit_data))
            if not chunk:
                return
            self._drv.write_mem8(address, chunk)
            address += len(chunk)

    def fill_mem(self, address, pattern, size):
        """Fill memory with pattern

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        pattern = bytes(pattern)
        index = 0
        data = pattern * (
            (min(size, self.maximum_8bit_data) // len(pattern)) + 1)
        while size:
            chunk_size = min(size, self.maximum_8bit_data)
            self._drv.write_mem8(address, data[index:index + chunk_size])
            index = (index + chunk_size) % len(pattern)
            address += chunk_size
            size -= chunk_size

    def read_mem8(self, address, size):
        """Read memory with 8 bit access

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            bytes of read data
        """
        return self.read_mem(address, size)

    def write_mem8(self, address, data):
        """Write memory with 8 bit access

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        self.write_mem(address, data)

    def fill_mem8(self, address, pattern, size):
        """Fill memory with pattern using 8 bit access

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        self.fill_mem(address, pattern, size)

    def read_mem16(self, address, size):
        """Read memory with 16 bit access (emulated with 8 bit access)

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            bytes of read data
        """
        return self.read_mem(address, size)

    def write_mem16(self, address, data):
        """Write memory with 16 bit access (emulated with 8 bit access)

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        self.write_mem(address, data)

    def fill_mem16(self, address, pattern, size):
        """Fill memory with pattern using 16 bit access (emulated)

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        self.fill_mem(address, pattern, size)

    def read_mem32(self, address, size):
        """Read memory with 32 bit access (emulated with 8 bit access)

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            bytes of read data
        """
        return self.read_mem(address, size)

    def write_mem32(self, address, data):
        """Write memory with 32 bit access (emulated with 8 bit access)

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        self.write_mem(address, data)

    def fill_mem32(self, address, pattern, size):
        """Fill memory with pattern using 32 bit access (emulated)

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        self.fill_mem(address, pattern, size)
