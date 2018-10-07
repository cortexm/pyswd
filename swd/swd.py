"""SWD protocol
"""

import logging as _logging
import itertools as _itertools
from swd.stlink import Stlink as _Stlink


class Swd():
    """Swd class"""

    def __init__(self, swd_frequency=1800000, driver=None, serial_no=''):
        if driver is None:
            # default SWD driver is Stlink
            driver = _Stlink(swd_frequency=swd_frequency, serial_no=serial_no)
        self._drv = driver

    def get_version(self):
        """Get SWD driver version

        Return:
            driver version string
        """
        _logging.info("")
        return str(self._drv.get_version())

    def get_target_voltage(self):
        """Get target voltage from debugger

        Return:
            measured voltage
        """
        _logging.info("")
        return self._drv.get_target_voltage()

    def get_idcode(self):
        """Get core ID from MCU

        Return:
            32 bit number
        """
        _logging.info("")
        return self._drv.get_idcode()

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
        _logging.info("")
        return self._drv.get_reg(register)

    def get_reg_all(self):
        """Get all core registers

        Read all 32 bit CPU core registers (R0, R1, ...)
        Order of registers depends on architecture.
        (MCU must be halted to access core registers)

        Return:
            list of 32 bit numbers
        """
        _logging.info("")
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
        _logging.info("")
        self._drv.set_reg(register, data)

    def get_mem32(self, address):
        """Get 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory

        Return:
            return 32 bit number
        """
        _logging.info("")
        return self._drv.get_mem32(address)

    def set_mem32(self, address, data):
        """Set 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            data: 32 bit number
        """
        _logging.info("")
        self._drv.set_mem32(address, data)

    def _get_chunk_size_to_align_size(self, address, size):
        if size > self._drv.MAXIMUM_8BIT_DATA:
            return min(size, self._drv.MAXIMUM_8BIT_DATA - (address % 4))
        return size

    def _get_chunk_size_to_align_address(self, address, size):
        if address % 4:
            if size == self._drv.MAXIMUM_8BIT_DATA:
                return size
            return min(size, self._drv.MAXIMUM_8BIT_DATA - (address % 4))
        return 0

    def read_mem(self, address, size):
        """Read bytes memory

        Automatically use 8 and 32 bit access read which depends on alignment

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            iterable of read data
        """
        _logging.info("")
        chunk_size = self._get_chunk_size_to_align_address(address, size)
        if chunk_size:
            yield from self._drv.read_mem8(address, chunk_size)
            address += chunk_size
            size -= chunk_size
        while size:
            chunk_size = size
            if chunk_size < self._drv.MAXIMUM_8BIT_DATA and chunk_size % 4:
                yield from self._drv.read_mem8(address, chunk_size)
            else:
                chunk_size = min(chunk_size, self._drv.MAXIMUM_32BIT_DATA)
                chunk_size -= chunk_size % 4
                yield from self._drv.read_mem32(address, chunk_size)
            address += chunk_size
            size -= chunk_size

    def write_mem(self, address, data):
        """Write memory

        Automatically use 8 and 32 bit access write which depends on alignment

        Arguments:
            address: address in memory
            data: list or iterable of bytes to write into memory
        """
        _logging.info("")
        data = iter(data)
        # first chunk to align address
        if address % 4:
            chunk_size_max = self._drv.MAXIMUM_8BIT_DATA - (address % 4)
            chunk = list(_itertools.islice(data, 0, chunk_size_max))
            if not chunk:
                return
            self._drv.write_mem8(address, chunk)
            address += len(chunk)
        # write remained data, here is address always aligned
        while True:
            chunk = list(
                _itertools.islice(data, 0, self._drv.MAXIMUM_32BIT_DATA))
            if not chunk:
                return
            if len(chunk) % 4 == 0:
                self._drv.write_mem32(address, chunk)
                address += len(chunk)
                continue
            if len(chunk) > self._drv.MAXIMUM_8BIT_DATA:
                chunk_size32 = len(chunk) & 0xfffffffc
                self._drv.write_mem32(address, chunk[:chunk_size32])
                del chunk[:chunk_size32]
                address += chunk_size32
            self._drv.write_mem8(address, chunk)
            return

    def fill_mem(self, address, pattern, size):
        """Fill memory with pattern

        Automatically use 8 and 32 bit access write which depends on alignment

        Arguments:
            address: address in memory
            pattern: list of bytes to fill
            size: number of bytes to fill
        """
        _logging.info("")
        index = 0
        data = pattern * (
            (min(size, self._drv.MAXIMUM_32BIT_DATA)) // len(pattern) + 1)
        while size:
            chunk_size = size
            if address % 4 or (chunk_size < self._drv.MAXIMUM_8BIT_DATA and chunk_size % 4):
                if chunk_size > self._drv.MAXIMUM_8BIT_DATA:
                    chunk_size = min(chunk_size, self._drv.MAXIMUM_8BIT_DATA - (address % 4))
                self._drv.write_mem8(address, data[index:index + chunk_size])
            else:
                chunk_size = min(chunk_size, self._drv.MAXIMUM_32BIT_DATA)
                chunk_size -= chunk_size % 4
                self._drv.write_mem32(address, data[index:index + chunk_size])
            index = (index + chunk_size) % len(pattern)
            address += chunk_size
            size -= chunk_size
