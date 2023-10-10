"""SWD protocol
"""

import itertools as _itertools
from swd.stlink import Stlink as _Stlink


class Swd():
    """Swd class"""

    def __init__(self, swd_frequency=None, driver=None, serial_no='', debug=0):
        self._debug = debug
        if driver is None:
            # default SWD driver is Stlink
            driver = _Stlink(
                swd_frequency=swd_frequency,
                serial_no=serial_no,
                debug=debug)
        self._drv = driver

    def get_version(self):
        """Get SWD driver version

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

    def get_idcode(self):
        """Get core ID from MCU

        Return:
            32 bit number
        """
        return self._drv.get_idcode()

    @property
    def default_ap(self):
        """ Get default AP number for accesses """
        return self._drv.com.default_ap

    @default_ap.setter
    def default_ap(self, value):
        """ Set default AP number for accesses """
        self._drv.com.default_ap = value

    def open_ap(self, ap_sel):
        """Open AP (debug access point) for accesses

        Arguments:
            ap_sel: AP number to open"""
        self._drv.open_ap(ap_sel)

    def close_ap(self, ap_sel):
        """Close AP (debug access point) for accesses

        Arguments:
            ap_sel: AP number to open"""
        self._drv.close_ap(ap_sel)

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
        return self._drv.get_reg(register)

    def get_reg_all(self):
        """Get all core registers

        Read all 32 bit CPU core registers (R0, R1, ...)
        Order of registers depends on architecture.
        (MCU must be halted to access core registers)

        Return:
            list of 32 bit numbers
        """
        return self._drv.get_reg_all()

    def set_reg(self, register, data):
        """Set core register

        Write 32 bit CPU core register (e.g. R0, R1, ...)
        Register ID depends on architecture.
        (MCU must be halted to access core register)

        Arguments:
            register: register ID
            data: 32 bit number
        """
        self._drv.set_reg(register, data)

    def get_mem32(self, address, **kwargs):
        """Get 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory

        Return:
            return 32 bit number
        """
        return self._drv.get_mem32(address, **kwargs)

    def set_mem32(self, address, data, **kwargs):
        """Set 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            data: 32 bit number
        """
        self._drv.set_mem32(address, data, **kwargs)

    def _get_chunk_size_to_align_size(self, address, size):
        if size > self._drv.maximum_8bit_data:
            return min(size, self._drv.maximum_8bit_data - (address % 4))
        return size

    def _get_chunk_size_to_align_address(self, address, size):
        if address % 4:
            if size == self._drv.maximum_8bit_data:
                return size
            return min(size, self._drv.maximum_8bit_data - (address % 4))
        return 0

    def read_mem(self, address, size, **kwargs):
        """Read bytes memory

        Automatically use 8 and 32 bit access read which depends on alignment

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            iterable of read data
        """
        chunk_size = self._get_chunk_size_to_align_address(address, size)
        if chunk_size:
            yield from self._drv.read_mem8(address, chunk_size, **kwargs)
            address += chunk_size
            size -= chunk_size
        while size:
            chunk_size = size
            if chunk_size < self._drv.maximum_8bit_data and chunk_size % 4:
                yield from self._drv.read_mem8(address, chunk_size, **kwargs)
            else:
                chunk_size = min(chunk_size, self._drv.maximum_32bit_data)
                chunk_size -= chunk_size % 4
                yield from self._drv.read_mem32(address, chunk_size, **kwargs)
            address += chunk_size
            size -= chunk_size

    def write_mem(self, address, data, **kwargs):
        """Write memory

        Automatically use 8 and 32 bit access write which depends on alignment

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        data = iter(data)
        # first chunk to align address
        if address % 4:
            chunk_size_max = self._drv.maximum_8bit_data - (address % 4)
            chunk = bytes(_itertools.islice(data, 0, chunk_size_max))
            if not chunk:
                return
            self._drv.write_mem8(address, chunk, **kwargs)
            address += len(chunk)
        # write remained data, here is address always aligned
        while True:
            chunk = bytes(_itertools.islice(data, 0, self._drv.maximum_32bit_data))
            if not chunk:
                return
            if len(chunk) % 4 == 0:
                self._drv.write_mem32(address, chunk, **kwargs)
                address += len(chunk)
                continue
            if len(chunk) > self._drv.maximum_8bit_data:
                chunk_size32 = len(chunk) & 0xfffffffc
                self._drv.write_mem32(address, chunk[:chunk_size32], **kwargs)
                chunk = chunk[chunk_size32:]
                address += chunk_size32
            self._drv.write_mem8(address, chunk, **kwargs)
            return

    def fill_mem(self, address, pattern, size):
        """Fill memory with pattern

        Automatically use 8 and 32 bit access write which depends on alignment

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        index = 0
        data = pattern * (
            (min(size, self._drv.maximum_32bit_data) // len(pattern)) + 1)
        while size:
            chunk_size = size
            if address % 4 or (chunk_size < self._drv.maximum_8bit_data and chunk_size % 4):
                if chunk_size > self._drv.maximum_8bit_data:
                    chunk_size = min(chunk_size, self._drv.maximum_8bit_data - (address % 4))
                self._drv.write_mem8(address, data[index:index + chunk_size])
            else:
                chunk_size = min(chunk_size, self._drv.maximum_32bit_data)
                chunk_size -= chunk_size % 4
                self._drv.write_mem32(address, data[index:index + chunk_size])
            index = (index + chunk_size) % len(pattern)
            address += chunk_size
            size -= chunk_size

    def read_mem8(self, address, size):
        """Read memory with 8 bit access

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            iterable of read data
        """
        while size:
            chunk_size = min(size, self._drv.maximum_8bit_data)
            yield from self._drv.read_mem8(address, chunk_size)
            address += chunk_size
            size -= chunk_size

    def write_mem8(self, address, data):
        """Write memory with 8 bit access

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        data = iter(data)
        while True:
            chunk = bytes(
                _itertools.islice(data, 0, self._drv.maximum_8bit_data))
            if not chunk:
                return
            self._drv.write_mem8(address, chunk)
            address += len(chunk)

    def fill_mem8(self, address, pattern, size):
        """Fill memory with pattern using 8 bit access

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        index = 0
        data = pattern * ((min(size, self._drv.maximum_8bit_data) // len(pattern)) + 1)
        while size:
            chunk_size = min(size, self._drv.maximum_8bit_data)
            self._drv.write_mem8(address, data[index:index + chunk_size])
            index = (index + chunk_size) % len(pattern)
            address += chunk_size
            size -= chunk_size

    def read_mem16(self, address, size):
        """Read memory with 16 bit access

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            iterable of read data
        """
        while size:
            chunk_size = min(size, self._drv.maximum_16bit_data)
            yield from self._drv.read_mem16(address, chunk_size)
            address += chunk_size
            size -= chunk_size

    def write_mem16(self, address, data):
        """Write memory with 16 bit access

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        data = iter(data)
        while True:
            chunk = bytes(
                _itertools.islice(data, 0, self._drv.maximum_16bit_data))
            if not chunk:
                return
            self._drv.write_mem16(address, chunk)
            address += len(chunk)

    def fill_mem16(self, address, pattern, size):
        """Fill memory with pattern using 16 bit access

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        index = 0
        data = pattern * ((min(size, self._drv.maximum_16bit_data) // len(pattern)) + 1)
        while size:
            chunk_size = min(size, self._drv.maximum_16bit_data)
            self._drv.write_mem16(address, data[index:index + chunk_size])
            index = (index + chunk_size) % len(pattern)
            address += chunk_size
            size -= chunk_size

    def read_mem32(self, address, size):
        """Read memory with 32 bit access

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            iterable of read data
        """
        while size:
            chunk_size = min(size, self._drv.maximum_32bit_data)
            yield from self._drv.read_mem32(address, chunk_size)
            address += chunk_size
            size -= chunk_size

    def write_mem32(self, address, data):
        """Write memory with 32 bit access

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        data = iter(data)
        while True:
            chunk = bytes(
                _itertools.islice(data, 0, self._drv.maximum_32bit_data))
            if not chunk:
                return
            self._drv.write_mem32(address, chunk)
            address += len(chunk)

    def fill_mem32(self, address, pattern, size):
        """Fill memory with pattern using 32 bit access

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        index = 0
        data = pattern * ((min(size, self._drv.maximum_32bit_data) // len(pattern)) + 1)
        while size:
            chunk_size = min(size, self._drv.maximum_32bit_data)
            self._drv.write_mem32(address, data[index:index + chunk_size])
            index = (index + chunk_size) % len(pattern)
            address += chunk_size
            size -= chunk_size
