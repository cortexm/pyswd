"""Unit tests for stlink.py
"""

import unittest
import swd


class FncMock():
    """Function mock"""
    def __init__(self, default_return=None):
        self._return_data = []
        self._call_log = []
        self._return_data_default = default_return

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
        self.read_mem8_mock = FncMock(list())
        self.write_mem8_mock = FncMock()
        self.read_mem32_mock = FncMock(list())
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
        ret_data = list(self._swd.read_mem(0x00000000, 4))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x00000000, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_64bytes(self):
        """Test reading memory"""
        data = list(range(64))
        self._drv.read_mem32_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0xf1000004, 64))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0xf1000004, 'size': 64},
        ])
        self.assertEqual(ret_data, data)

    def test_1024bytes(self):
        """Test reading memory"""
        data = list(range(1024))
        self._drv.read_mem32_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x02000008, 1024))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x02000008, 'size': 1024},
        ])
        self.assertEqual(ret_data, data)

    def test_1028bytes(self):
        """Test reading memory"""
        data = list(range(1028))
        self._drv.read_mem32_mock.set_return_data([
            data[:1024],
            data[1024:],
        ])
        ret_data = list(self._swd.read_mem(0xf300000c, 1028))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0xf300000c, 'size': 1024},
            {'address': 0xf300040c, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_2048bytes(self):
        """Test reading memory"""
        data = list(range(2048))
        self._drv.read_mem32_mock.set_return_data([
            data[:1024],
            data[1024:],
        ])
        ret_data = list(self._swd.read_mem(0x04000010, 2048))
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x04000010, 'size': 1024},
            {'address': 0x04000410, 'size': 1024},
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
        ret_data = list(self._swd.read_mem(0xf5000014, 1))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0xf5000014, 'size': 1},
        ])
        self.assertEqual(ret_data, data)

    def test_63bytes(self):
        """Test reading memory"""
        data = list(range(63))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x06000018, 63))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x06000018, 'size': 63},
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
        ret_data = list(self._swd.read_mem(0xf700001c, 65))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0xf700005c, 'size': 1},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0xf700001c, 'size': 64},
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
        ret_data = list(self._swd.read_mem(0x08000020, 1023))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x0800041c, 'size': 3},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x08000020, 'size': 1020},
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
        ret_data = list(self._swd.read_mem(0xf9000024, 1025))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0xf9000424, 'size': 1},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0xf9000024, 'size': 1024},
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
        ret_data = list(self._swd.read_mem(0x0a000028, 1087))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x0a000428, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x0a000028, 'size': 1024},
        ])
        self.assertEqual(ret_data, data)


class TestReadMemUnalignedAddress(_TestSwd):
    """Tests for Swd.read_mem class with unaligned address"""

    def test_1bytes1(self):
        """Test reading memory"""
        data = list(range(1))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000001, 1))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000001, 'size': 1},
        ])
        self.assertEqual(ret_data, data)

    def test_1bytes2(self):
        """Test reading memory"""
        data = list(range(1))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000002, 1))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000002, 'size': 1},
        ])
        self.assertEqual(ret_data, data)

    def test_1bytes3(self):
        """Test reading memory"""
        data = list(range(1))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000003, 1))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000003, 'size': 1},
        ])
        self.assertEqual(ret_data, data)

    def test_2bytes1(self):
        """Test reading memory"""
        data = list(range(2))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000001, 2))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000001, 'size': 2},
        ])
        self.assertEqual(ret_data, data)

    def test_2bytes2(self):
        """Test reading memory"""
        data = list(range(2))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000002, 2))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000002, 'size': 2},
        ])
        self.assertEqual(ret_data, data)

    def test_2bytes3(self):
        """Test reading memory"""
        data = list(range(2))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000003, 2))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000003, 'size': 2},
        ])
        self.assertEqual(ret_data, data)

    def test_3bytes1(self):
        """Test reading memory"""
        data = list(range(3))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000001, 3))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000001, 'size': 3},
        ])
        self.assertEqual(ret_data, data)

    def test_3bytes2(self):
        """Test reading memory"""
        data = list(range(3))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000002, 3))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000002, 'size': 3},
        ])
        self.assertEqual(ret_data, data)

    def test_3bytes3(self):
        """Test reading memory"""
        data = list(range(3))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000003, 3))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000003, 'size': 3},
        ])
        self.assertEqual(ret_data, data)

    def test_4bytes1(self):
        """Test reading memory"""
        data = list(range(4))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000001, 4))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000001, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_4bytes2(self):
        """Test reading memory"""
        data = list(range(4))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000002, 4))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000002, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_4bytes3(self):
        """Test reading memory"""
        data = list(range(4))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ])
        ret_data = list(self._swd.read_mem(0x10000003, 4))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x10000003, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_64bytes(self):
        """Test reading memory"""
        data = list(range(64))
        self._drv.read_mem8_mock.set_return_data([
            data,
        ], [])
        ret_data = list(self._swd.read_mem(0xe1000005, 64))
        self.assertEqual([
            {'address': 0xe1000005, 'size': 64},
        ], self._drv.read_mem8_mock.get_call_log())
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
        ret_data = list(self._swd.read_mem(0x12000009, 67))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x12000009, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x12000048, 'size': 4},
        ])
        self.assertEqual(ret_data, data)

    def test_126bytes(self):
        """Test reading memory"""
        data = list(range(126))
        self._drv.read_mem8_mock.set_return_data([
            data[:63],
            data[63:],
        ])
        ret_data = list(self._swd.read_mem(0xe300000d, 126))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0xe300000d, 'size': 63},
            {'address': 0xe300004c, 'size': 63},
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
        ret_data = list(self._swd.read_mem(0x14000011, 1023))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x14000011, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x14000050, 'size': 960},
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
        ret_data = list(self._swd.read_mem(0xe5000015, 1087))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0xe5000015, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0xe5000054, 'size': 1024},
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
        ret_data = list(self._swd.read_mem(0x16000019, 1150))
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x16000019, 'size': 63},
            {'address': 0x16000458, 'size': 63},
        ])
        self.assertEqual(self._drv.read_mem32_mock.get_call_log(), [
            {'address': 0x16000058, 'size': 1024},
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
        self._swd.write_mem(0xd1000004, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0xd1000004, 'data': data},
        ])

    def test_1024bytes(self):
        """Test writing memory"""
        data = list(range(1024))
        self._swd.write_mem(0x22000008, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x22000008, 'data': data},
        ])

    def test_1028bytes(self):
        """Test writing memory"""
        data = list(range(1028))
        self._swd.write_mem(0xd300000c, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0xd300000c, 'data': data[:1024]},
            {'address': 0xd300040c, 'data': data[1024:]},
        ])

    def test_2048bytes(self):
        """Test writing memory"""
        data = list(range(2048))
        self._swd.write_mem(0x24000010, data)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x24000010, 'data': data[:1024]},
            {'address': 0x24000410, 'data': data[1024:]},
        ])

class TestWriteMemUnalignedSize(_TestSwd):
    """Tests for Swd.write_mem class with unaligned size"""

    def test_1byte(self):
        """Test writing memory"""
        data = list(range(1))
        self._swd.write_mem(0x30000000, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x30000000, 'data': data},
        ])

    def test_63bytes(self):
        """Test writing memory"""
        data = list(range(63))
        self._swd.write_mem(0xc1000004, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0xc1000004, 'data': data},
        ])

    def test_65bytes(self):
        """Test writing memory"""
        data = list(range(65))
        self._swd.write_mem(0x32000008, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x32000048, 'data': data[64:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x32000008, 'data': data[:64]},
        ])

    def test_1023bytes(self):
        """Test writing memory"""
        data = list(range(1023))
        self._swd.write_mem(0xc300000c, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0xc3000408, 'data': data[1020:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0xc300000c, 'data': data[:1020]},
        ])

    def test_1025bytes(self):
        """Test writing memory"""
        data = list(range(1025))
        self._swd.write_mem(0x34000010, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x34000410, 'data': data[1024:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x34000010, 'data': data[:1024]},
        ])

    def test_1087bytes(self):
        """Test writing memory"""
        data = list(range(1087))
        self._swd.write_mem(0xc5000014, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0xc5000414, 'data': data[1024:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0xc5000014, 'data': data[:1024]},
        ])


class TestWriteMemUnalignedAddress(_TestSwd):
    """Tests for Swd.write_mem class with unaligned address"""

    def test_4bytes(self):
        """Test writing memory"""
        data = list(range(4))
        self._swd.write_mem(0x40000001, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x40000001, 'data': data},
        ])

    def test_64bytes(self):
        """Test writing memory"""
        data = list(range(64))
        self._swd.write_mem(0xb1000005, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0xb1000005, 'data': data[:63]},
            {'address': 0xb1000044, 'data': data[63:]},
        ])

    def test_67bytes(self):
        """Test writing memory"""
        data = list(range(67))
        self._swd.write_mem(0x42000009, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x42000009, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x42000048, 'data': data[63:]},
        ])

    def test_126bytes(self):
        """Test writing memory"""
        data = list(range(126))
        self._swd.write_mem(0xb300000d, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0xb300000d, 'data': data[:63]},
            {'address': 0xb300004c, 'data': data[63:]},
        ])

    def test_1024bytes(self):
        """Test writing memory"""
        data = list(range(1023))
        self._swd.write_mem(0x44000011, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x44000011, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x44000050, 'data': data[63:]},
        ])

    def test_1087bytes(self):
        """Test writing memory"""
        data = list(range(1087))
        self._swd.write_mem(0xb5000015, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0xb5000015, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0xb5000054, 'data': data[63:]},
        ])

    def test_1150bytes(self):
        """Test writing memory"""
        data = list(range(1150))
        self._swd.write_mem(0x46000019, data)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x46000019, 'data': data[:63]},
            {'address': 0x46000458, 'data': data[1087:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x46000058, 'data': data[63:1087]},
        ])


class TestFillMem(_TestSwd):
    """Tests for Swd.fill_mem class"""
    _PATTERN = [0x42, ]

    def test_4bytes(self):
        """Test filling memory"""
        size = 4
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x50000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x50000000, 'data': data},
        ])

    def test_64bytes(self):
        """Test filling memory"""
        size = 64
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0xa1000004, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0xa1000004, 'data': data},
        ])

    def test_1024bytes(self):
        """Test filling memory"""
        size = 1024
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x52000008, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x52000008, 'data': data},
        ])

    def test_1028bytes(self):
        """Test filling memory"""
        size = 1028
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0xa300000c, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0xa300000c, 'data': data[:1024]},
            {'address': 0xa300040c, 'data': data[1024:]},
        ])

    def test_2048bytes(self):
        """Test filling memory"""
        size = 2048
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x54000010, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x54000010, 'data': data[:1024]},
            {'address': 0x54000410, 'data': data[1024:]},
        ])


class TestFillMemUnalignedSize(_TestSwd):
    """Tests for Swd.fill_mem class with unaligned size"""
    _PATTERN = [0x42, 0xc8, 0x1f]

    def test_1byte(self):
        """Test filling memory"""
        size = 1
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x60000000, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x60000000, 'data': data},
        ])

    def test_63bytes(self):
        """Test filling memory"""
        size = 63
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x91000004, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x91000004, 'data': data},
        ])

    def test_65bytes(self):
        """Test filling memory"""
        size = 65
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x62000008, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x62000048, 'data': data[64:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x62000008, 'data': data[:64]},
        ])

    def test_1023bytes(self):
        """Test filling memory"""
        size = 1023
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x9300000c, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x93000408, 'data': data[1020:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x9300000c, 'data': data[:1020]},
        ])

    def test_1025bytes(self):
        """Test filling memory"""
        size = 1025
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x64000010, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x64000410, 'data': data[1024:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x64000010, 'data': data[:1024]},
        ])

    def test_1087bytes(self):
        """Test filling memory"""
        size = 1087
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x95000014, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x95000414, 'data': data[1024:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x95000014, 'data': data[:1024]},
        ])


class TestFillMemUnalignedAddress(_TestSwd):
    """Tests for Swd.fill_mem class with unaligned address"""
    _PATTERN = [0x12, 0xbe, 0xef]

    def test_4bytes(self):
        """Test filling memory"""
        size = 4
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x70000001, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x70000001, 'data': data},
        ])

    def test_64bytes(self):
        """Test filling memory"""
        size = 64
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x81000005, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x81000005, 'data': data},
        ])

    def test_67bytes(self):
        """Test filling memory"""
        size = 67
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x72000009, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x72000009, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x72000048, 'data': data[63:]},
        ])

    def test_126bytes(self):
        """Test filling memory"""
        size = 126
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x8300000d, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x8300000d, 'data': data[:63]},
            {'address': 0x8300004c, 'data': data[63:]},
        ])

    def test_1024bytes(self):
        """Test filling memory"""
        size = 1023
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x74000011, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x74000011, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x74000050, 'data': data[63:]},
        ])

    def test_1087bytes(self):
        """Test filling memory"""
        size = 1087
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x85000015, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x85000015, 'data': data[:63]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x85000054, 'data': data[63:]},
        ])

    def test_1150bytes(self):
        """Test filling memory"""
        size = 1150
        data = (self._PATTERN * (size // len(self._PATTERN) + 1))[:size]
        self._swd.fill_mem(0x76000019, self._PATTERN, size)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x76000019, 'data': data[:63]},
            {'address': 0x76000458, 'data': data[1087:]},
        ])
        self.assertEqual(self._drv.write_mem32_mock.get_call_log(), [
            {'address': 0x76000058, 'data': data[63:1087]},
        ])
