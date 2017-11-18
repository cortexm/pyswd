"""SWD protocol"""

import logging as _logging
import itertools as _itertools
from swd.stlink import Stlink as _Stlink


class Swd():
    """Swd class"""
    _LOGGER_LEVEL1 = _logging.DEBUG - 1

    def __init__(self, swd_frequency=1800000, driver=None, logger=None):
        if logger is None:
            logger = _logging.Logger('stlink')
        self._logger = logger
        if driver is None:
            # default SWD driver is Stlink
            driver = _Stlink(swd_frequency=swd_frequency, logger=self._logger)
        self._drv = driver

    def get_version(self):
        """Get SWD driver version

        Return:
            driver version string
        """
        return str(self._drv.get_version())

    def get_target_voltage(self):
        """Get target voltage from debugger

        Return:
            measured voltage
        """
        return self._drv.get_target_voltage()

    def get_coreid(self):
        """Get core ID from MCU

        Return:
            32 bit number
        """
        return self._drv.get_coreid()

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

    def get_mem32(self, address):
        """Get 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory

        Return:
            return 32 bit number
        """
        return self._drv.get_mem32(address)

    def set_mem32(self, address, data):
        """Set 32 bit memory register with 32 bit memory access.

        Address must be aligned to 4 Bytes.

        Arguments:
            address: address in memory
            data: 32 bit number
        """
        self._drv.set_mem32(address, data)

    def read_mem(self, address, size):
        """Read bytes memory

        Automatically use 8 and 32 bit access read which depends on alignment

        Arguments:
            address: address in memory
            size: number of bytes to read

        Return:
            iterable of read data
        """
        self._logger.log(
            self._LOGGER_LEVEL1,
            "address:0x%08x, size:%d",
            address,
            size)
        while size:
            chunk_size = size
            if address % 4 or (chunk_size < self._drv.MAXIMUM_8BIT_DATA and chunk_size % 4):
                if chunk_size > 64:
                    chunk_size = min(chunk_size, self._drv.MAXIMUM_8BIT_DATA - (address % 4))
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
        self._logger.log(
            self._LOGGER_LEVEL1,
            "address:0x%08x, data:[..]",
            address)
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
            chunk = list(_itertools.islice(data, 0, self._drv.MAXIMUM_32BIT_DATA))
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
        self._logger.log(
            self._LOGGER_LEVEL1,
            "address:0x%08x, pattern:%s, size:%d",
            address,
            ', '.join(['0x%02x' % i for i in pattern]),
            size)
        index = 0
        data = pattern * ((min(size, self._drv.MAXIMUM_32BIT_DATA)) // len(pattern) + 1)
        while size:
            chunk_size = size
            if address % 4 or (chunk_size < self._drv.MAXIMUM_8BIT_DATA and chunk_size % 4):
                chunk_size = min(chunk_size, self._drv.MAXIMUM_8BIT_DATA - (address % 4))
                self._drv.write_mem8(address, data[index:index + chunk_size])
            else:
                chunk_size = min(chunk_size, self._drv.MAXIMUM_32BIT_DATA)
                chunk_size -= chunk_size % 4
                self._drv.write_mem32(address, data[index:index + chunk_size])
            index = (index + chunk_size) % len(pattern)
            address += chunk_size
            size -= chunk_size
