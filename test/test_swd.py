"""Unit tests for stlink.py"""
import unittest
import swd


class FncMock():
    """Function mock"""
    def __init__(self):
        self._return_data = []
        self._call_log = []
        self._return_data_default = None

    def set_return_data(self, return_data, default=None):
        """set expected return data"""
        self._return_data = return_data
        self._return_data_default = default

    def get_call_log(self):
        """get expected call log"""
        call_log = self._call_log
        self._call_log = []
        return call_log

    def fnc(self, **kwargs):
        """mock function"""
        self._call_log.append(kwargs)
        if self._return_data:
            ret = self._return_data[0]
            del self._return_data[0]
            return ret
        return self._return_data_default


class DrvMock():
    """Com Mock class for testing Stlink class"""

    MAXIMUM_8BIT_DATA = 64
    MAXIMUM_32BIT_DATA = 1024

    def __init__(self):
        """MOCK CONSTRUCTOR"""
        self.read_mem8_mock = FncMock()
        self.write_mem8_mock = FncMock()
        self.read_mem32_mock = FncMock()
        self.write_mem32_mock = FncMock()

    def read_mem8(self, address, size):
        """Mock read_mem8"""
        return self.read_mem8_mock.fnc(
            address=address,
            size=size)

    def write_mem8(self, address, data):
        """Mock write_mem8"""
        return self.write_mem8_mock.fnc(
            address=address,
            data=data)

    def read_mem32(self, address, size):
        """Mock read_mem32"""
        return self.read_mem32_mock.fnc(
            address=address,
            size=size)

    def write_mem32(self, address, data):
        """Mock write_mem32"""
        return self.write_mem32_mock.fnc(
            address=address,
            data=data)


class _TestSwd(unittest.TestCase):
    """Base class for testing Stlink class"""

    def setUp(self):
        self._drv = DrvMock()
        self._swd = swd.Swd(driver=self._drv)


class TestReadMem(_TestSwd):
    """Tests for Swd.read_mem class"""

    def test_4bytes(self):
        """Test reading memory"""
        data = list(range(4))
        self._drv.read_mem32_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 4))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_64bytes(self):
        """Test reading memory"""
        data = list(range(64))
        self._drv.read_mem32_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 64))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 64},
        ])
        self.assertEqual(ret_data, data)

    def test_1024bytes(self):
        """Test reading memory"""
        data = list(range(1024))
        self._drv.read_mem32_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 1024))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 1024},
        ])
        self.assertEqual(ret_data, data)

    def test_1028bytes(self):
        """Test reading memory"""
        data = list(range(1028))
        self._drv.read_mem32_mock.set_return_data([
            data[:1024],
            data[1024:],
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 1028))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 1024},
            {'address': 0x08000400, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_2048bytes(self):
        """Test reading memory"""
        data = list(range(2048))
        self._drv.read_mem32_mock.set_return_data([
            data[:1024],
            data[1024:],
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 2048))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 1024},
            {'address': 0x08000400, 'size': 1024},
        ])
        self.assertEqual(ret_data, data)

class TestReadMemUnalignedSize(_TestSwd):
    """Tests for Swd.read_mem class with unaligned size"""

    def test_1byte(self):
        """Test reading memory"""
        data = list(range(1))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 1))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 1},
        ])
        self.assertEqual(ret_data, data)

    def test_63bytes(self):
        """Test reading memory"""
        data = list(range(63))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 63))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 63},
        ])
        self.assertEqual(ret_data, data)

    def test_65bytes(self):
        """Test reading memory"""
        data = list(range(65))
        self._drv.read_mem8_mock.set_return_data([
            data[64:],
        ])
        self._drv.read_mem32_mock.set_return_data([
            data[:64],
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 65))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000040, 'size': 1},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 64},
        ])
        self.assertEqual(ret_data, data)

    def test_1023bytes(self):
        """Test reading memory"""
        data = list(range(1023))
        self._drv.read_mem8_mock.set_return_data([
            data[1020:],
        ])
        self._drv.read_mem32_mock.set_return_data([
            data[:1020],
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 1023))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x080003fc, 'size': 3},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 1020},
        ])
        self.assertEqual(ret_data, data)

    def test_1025bytes(self):
        """Test reading memory"""
        data = list(range(1025))
        self._drv.read_mem8_mock.set_return_data([
            data[1024:],
        ])
        self._drv.read_mem32_mock.set_return_data([
            data[:1024],
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 1025))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000400, 'size': 1},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 1024},
        ])
        self.assertEqual(ret_data, data)

    def test_1087bytes(self):
        """Test reading memory"""
        data = list(range(1087))
        self._drv.read_mem8_mock.set_return_data([
            data[1024:],
        ])
        self._drv.read_mem32_mock.set_return_data([
            data[:1024],
        ])
        ret_data = list(self._swd.read_mem(0x08000000, 1087))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000400, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000000, 'size': 1024},
        ])
        self.assertEqual(ret_data, data)

class TestReadMemUnalignedAddress(_TestSwd):
    """Tests for Swd.read_mem class with unaligned address"""

    def test_4bytes(self):
        """Test reading memory"""
        data = list(range(4))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x08000001, 4))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000001, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_64bytes(self):
        """Test reading memory"""
        data = list(range(64))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ], [])
        ret_data = list(self._swd.read_mem(0x08000001, 64))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000001, 'size': 64},
        ])
        self.assertEqual(ret_data, data)

    def test_67bytes(self):
        """Test reading memory"""
        data = list(range(67))
        self._drv.read_mem8_mock.set_return_data([
            data[:63],
        ])
        self._drv.read_mem32_mock.set_return_data([
            data[63:],
        ])
        ret_data = list(self._swd.read_mem(0x08000001, 67))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000001, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000040, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_126bytes(self):
        """Test reading memory"""
        data = list(range(126))
        self._drv.read_mem8_mock.set_return_data([
            data[:63],
            data[63:],
        ])
        ret_data = list(self._swd.read_mem(0x08000001, 126))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000001, 'size': 63},
            {'address': 0x08000040, 'size': 63},
        ])
        self.assertEqual(ret_data, data)

    def test_1024bytes(self):
        """Test reading memory"""
        data = list(range(1023))
        self._drv.read_mem8_mock.set_return_data([
            data[:63],
        ])
        self._drv.read_mem32_mock.set_return_data([
            data[63:],
        ])
        ret_data = list(self._swd.read_mem(0x08000001, 1023))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000001, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000040, 'size': 960},
        ])
        self.assertEqual(ret_data, data)

    def test_1087bytes(self):
        """Test reading memory"""
        data = list(range(1087))
        self._drv.read_mem8_mock.set_return_data([
            data[:63],
        ])
        self._drv.read_mem32_mock.set_return_data([
            data[63:],
        ])
        ret_data = list(self._swd.read_mem(0x08000001, 1087))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000001, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000040, 'size': 1024},
        ])
        self.assertEqual(ret_data, data)

    def test_1150bytes(self):
        """Test reading memory"""
        data = list(range(1150))
        self._drv.read_mem8_mock.set_return_data([
            data[:63],
            data[1087:],
        ])
        self._drv.read_mem32_mock.set_return_data([
            data[63:1087],
        ])
        ret_data = list(self._swd.read_mem(0x08000001, 1150))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x08000001, 'size': 63},
            {'address': 0x08000440, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000040, 'size': 1024},
        ])
        self.assertEqual(ret_data, data)


class TestWriteMem(_TestSwd):
    """Tests for Swd.write_mem class"""

    def test_4bytes(self):
        """Test writing memory"""
        data = list(range(4))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_64bytes(self):
        """Test writing memory"""
        data = list(range(64))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_1024bytes(self):
        """Test writing memory"""
        data = list(range(1024))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_1028bytes(self):
        """Test writing memory"""
        data = list(range(1028))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1024]},
            {'address': 0x20000400, 'data': data[1024:]},
        ])

    def test_2048bytes(self):
        """Test writing memory"""
        data = list(range(2048))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1024]},
            {'address': 0x20000400, 'data': data[1024:]},
        ])

class TestWriteMemUnalignedSize(_TestSwd):
    """Tests for Swd.write_mem class with unaligned size"""

    def test_1byte(self):
        """Test writing memory"""
        data = list(range(1))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_63bytes(self):
        """Test writing memory"""
        data = list(range(63))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_65bytes(self):
        """Test writing memory"""
        data = list(range(65))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[64:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:64]},
        ])

    def test_1023bytes(self):
        """Test writing memory"""
        data = list(range(1023))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x200003fc, 'data': data[1020:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1020]},
        ])

    def test_1025bytes(self):
        """Test writing memory"""
        data = list(range(1025))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000400, 'data': data[1024:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1024]},
        ])

    def test_1087bytes(self):
        """Test writing memory"""
        data = list(range(1087))
        self._swd.write_mem(0x20000000, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000400, 'data': data[1024:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1024]},
        ])

class TestWriteMemUnalignedAddress(_TestSwd):
    """Tests for Swd.write_mem class with unaligned address"""

    def test_4bytes(self):
        """Test writing memory"""
        data = list(range(4))
        self._swd.write_mem(0x20000001, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data},
        ])

    def test_64bytes(self):
        """Test writing memory"""
        data = list(range(64))
        self._swd.write_mem(0x20000001, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_67bytes(self):
        """Test writing memory"""
        data = list(range(67))
        self._swd.write_mem(0x20000001, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_126bytes(self):
        """Test writing memory"""
        data = list(range(126))
        self._swd.write_mem(0x20000001, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_1024bytes(self):
        """Test writing memory"""
        data = list(range(1023))
        self._swd.write_mem(0x20000001, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_1087bytes(self):
        """Test writing memory"""
        data = list(range(1087))
        self._swd.write_mem(0x20000001, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_1150bytes(self):
        """Test writing memory"""
        data = list(range(1150))
        self._swd.write_mem(0x20000001, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
            {'address': 0x20000440, 'data': data[1087:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[63:1087]},
        ])


class TestFillMem(_TestSwd):
    """Tests for Swd.fill_mem class"""
    _PATTERN = [0x42, ]

    def test_4bytes(self):
        """Test filling memory"""
        size = 4
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_64bytes(self):
        """Test filling memory"""
        size = 64
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_1024bytes(self):
        """Test filling memory"""
        size = 1024
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_1028bytes(self):
        """Test filling memory"""
        size = 1028
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1024]},
            {'address': 0x20000400, 'data': data[1024:]},
        ])

    def test_2048bytes(self):
        """Test filling memory"""
        size = 2048
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1024]},
            {'address': 0x20000400, 'data': data[1024:]},
        ])

class TestFillMemUnalignedSize(_TestSwd):
    """Tests for Swd.fill_mem class with unaligned size"""
    _PATTERN = [0x42, ]

    def test_1byte(self):
        """Test filling memory"""
        size = 1
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_63bytes(self):
        """Test filling memory"""
        size = 63
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data},
        ])

    def test_65bytes(self):
        """Test filling memory"""
        size = 65
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[64:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:64]},
        ])

    def test_1023bytes(self):
        """Test filling memory"""
        size = 1023
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x200003fc, 'data': data[1020:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1020]},
        ])

    def test_1025bytes(self):
        """Test filling memory"""
        size = 1025
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000400, 'data': data[1024:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1024]},
        ])

    def test_1087bytes(self):
        """Test filling memory"""
        size = 1087
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000400, 'data': data[1024:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000000, 'data': data[:1024]},
        ])

class TestFillMemUnalignedAddress(_TestSwd):
    """Tests for Swd.fill_mem class with unaligned address"""
    _PATTERN = [0x42, ]

    def test_4bytes(self):
        """Test filling memory"""
        size = 4
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000001, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data},
        ])

    def test_64bytes(self):
        """Test filling memory"""
        size = 64
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000001, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_67bytes(self):
        """Test filling memory"""
        size = 67
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000001, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_126bytes(self):
        """Test filling memory"""
        size = 126
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000001, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_1024bytes(self):
        """Test filling memory"""
        size = 1023
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000001, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_1087bytes(self):
        """Test filling memory"""
        size = 1087
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000001, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[63:]},
        ])

    def test_1150bytes(self):
        """Test filling memory"""
        size = 1150
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x20000001, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x20000001, 'data': data[:63]},
            {'address': 0x20000440, 'data': data[1087:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x20000040, 'data': data[63:1087]},
        ])


class TestFillMem2(TestFillMem):
    """Tests for Swd.fill_mem class"""
    _PATTERN = [0x42, 0xab, ]

class TestFillMem2UnalignedSize(TestFillMemUnalignedSize):
    """Tests for Swd.fill_mem class with unaligned size"""
    _PATTERN = [0x42, 0xab, ]

class TestFillMem2UnalignedAddress(TestFillMemUnalignedAddress):
    """Tests for Swd.fill_mem class with unaligned address"""
    _PATTERN = [0x42, 0xab, ]


class TestFillMem3(TestFillMem):
    """Tests for Swd.fill_mem class"""
    _PATTERN = [0x42, 0xab, 0xf0, ]

class TestFillMem3UnalignedSize(TestFillMemUnalignedSize):
    """Tests for Swd.fill_mem class with unaligned size"""
    _PATTERN = [0x42, 0xab, 0xf0, ]

class TestFillMem3UnalignedAddress(TestFillMemUnalignedAddress):
    """Tests for Swd.fill_mem class with unaligned address"""
    _PATTERN = [0x42, 0xab, 0xf0, ]


class TestFillMem10(TestFillMem):
    """Tests for Swd.fill_mem class"""
    _PATTERN = list(range(10))

class TestFillMem10UnalignedSize(TestFillMemUnalignedSize):
    """Tests for Swd.fill_mem class with unaligned size"""
    _PATTERN = list(range(10))

class TestFillMem10UnalignedAddress(TestFillMemUnalignedAddress):
    """Tests for Swd.fill_mem class with unaligned address"""
    _PATTERN = list(range(10))
