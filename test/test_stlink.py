"""Unit tests for stlink.py
"""

import unittest
import swd.stlink


class FncMock():
    """Function mock"""
    def __init__(self):
        self._return_data = []
        self._call_log = []

    def set_return_data(self, return_data):
        """set expected return data"""
        self._return_data = return_data

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
        return None


class ComMock():
    """Com Mock class for testing Stlink class"""
    STLINK_MAXIMUM_TRANSFER_SIZE = 1024

    def __init__(self):
        self.xfer_mock = FncMock()

    @property
    def version(self):
        """Mock version"""
        return 'V2'

    def xfer(self, command, data=None, rx_length=0, tout=200):
        """Mock xfer"""
        return self.xfer_mock.fnc(
            command=command,
            data=data,
            rx_length=rx_length,
            tout=tout)


class _TestStlink(unittest.TestCase):
    """Base class for testing Stlink class"""

    def setUp(self):
        self._com = ComMock()
        self._com.xfer_mock.set_return_data([
            [0x26, 0xc6, 0x83, 0x04, 0x48, 0x37],
            [0x02, 0x00],
            None,
            [0x80, 0x00],
            [0x80, 0x00],
        ])
        self._stlink = swd.stlink.Stlink(com=self._com)
        self._ctor_call_log = self._com.xfer_mock.get_call_log()


class TestStlinkCotor(_TestStlink):
    """Tests for Stlink class"""

    def test_com_xfer_call(self):
        """test for creating Stlink object"""
        self.assertEqual(self._ctor_call_log, [
            {
                'command': [0xf1, 0x80],
                'data': None,
                'rx_length': 6,
                'tout': 200},
            {
                'command': [0xf5],
                'data': None,
                'rx_length': 2,
                'tout': 200},
            {
                'command': [0xf2, 0x21],
                'data': None,
                'rx_length': 0,
                'tout': 200},
            {
                'command': [0xf2, 0x43, 0x01],
                'data': None,
                'rx_length': 2,
                'tout': 200},
            {
                'command': [0xf2, 0x30, 0xa3],
                'data': None,
                'rx_length': 2,
                'tout': 200},
        ])


class TestStlinkVersion(_TestStlink):
    """Tests for Stlink.get_version()"""

    def test_str(self):
        """test version string"""
        self.assertEqual(self._stlink.get_version().str, 'ST-Link/V2 V2J27S6')

    def test_stlink(self):
        """test version string"""
        self.assertEqual(self._stlink.get_version().stlink, 2)

    def test_jtag(self):
        """test version string"""
        self.assertEqual(self._stlink.get_version().jtag, 27)

    def test_swim(self):
        """test version string"""
        self.assertEqual(self._stlink.get_version().swim, 6)

    def test_mass(self):
        """test version string"""
        self.assertEqual(self._stlink.get_version().mass, None)

    def test_api(self):
        """test version string"""
        self.assertEqual(self._stlink.get_version().api, 2)


class TestStlinkGetTargetVoltage(_TestStlink):
    """Tests for Stlink.get_target_voltage()"""

    def test(self):
        """test getting arget voltage"""
        self._com.xfer_mock.set_return_data([
            [0xfa, 0x05, 0x00, 0x00, 0xfb, 0x07, 0x00, 0x00],
        ])
        target_voltage = self._stlink.get_target_voltage()
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [0xf7], 'data': None, 'rx_length': 8, 'tout': 200},
        ])
        self.assertEqual(target_voltage, 3.2)


class TestStlinkGetCoreid(_TestStlink):
    """Tests for Stlink.get_coreid()"""

    def test(self):
        """test getting ore id"""
        self._com.xfer_mock.set_return_data([[
            0x80, 0x00, 0x55, 0x55, 0x77, 0x14,
            0xb1, 0x0b, 0x00, 0x00, 0x00, 0x00]])
        idcode = self._stlink.get_idcode()
        self.assertEqual(
            self._com.xfer_mock.get_call_log(),
            [{
                'command': [0xf2, 0x31],
                'data': None,
                'rx_length': 12,
                'tout': 200}])
        self.assertEqual(idcode, 0xbb11477)


class TestStlinkGetReg(_TestStlink):
    """Tests for Stlink.get_reg()"""

    def test(self):
        """test getting memory register"""
        self._com.xfer_mock.set_return_data([
            [0x80, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x20],
        ])
        coreid = self._stlink.get_reg(1)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x33, 0x01,
            ], 'data': None, 'rx_length': 8, 'tout': 200},
        ])
        self.assertEqual(coreid, 0x20001000)


class TestStlinkSetReg(_TestStlink):
    """Tests for Stlink.set_reg()"""

    def test(self):
        """test setting memory register"""
        self._com.xfer_mock.set_return_data([
            [0x80, 0x00],
        ])
        self._stlink.set_reg(1, 0x12345678)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x34, 0x01, 0x78, 0x56, 0x34, 0x12,
            ], 'data': None, 'rx_length': 2, 'tout': 200},
        ])


class TestStlinkGetMem32(_TestStlink):
    """Tests for Stlink.get_mem32()"""

    def test(self):
        """test getting memory register"""
        self._com.xfer_mock.set_return_data([
            [0x80, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x20],
        ])
        coreid = self._stlink.get_mem32(0x08000000)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x36, 0x00, 0x00, 0x00, 0x08,
            ], 'data': None, 'rx_length': 8, 'tout': 200},
        ])
        self.assertEqual(coreid, 0x20001000)

    def test_unaligned_address(self):
        """test getting memory register with unaligned address"""
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.get_mem32(0x08000001)
        self.assertEqual(
            str(context.exception), 'Address is not aligned to 4 Bytes')


class TestStlinkSetMem32(_TestStlink):
    """Tests for Stlink.set_mem32()"""

    def test(self):
        """test setting memory register"""
        self._com.xfer_mock.set_return_data([
            [0x80, 0x00],
        ])
        self._stlink.set_mem32(0x20000000, 0x12345678)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x35, 0x00, 0x00, 0x00, 0x20, 0x78, 0x56, 0x34, 0x12,
            ], 'data': None, 'rx_length': 2, 'tout': 200},
        ])

    def test_unaligned_address(self):
        """test setting memory register with unaligned address"""
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.set_mem32(0x20000001, 0x12345678)
        self.assertEqual(
            str(context.exception), 'Address is not aligned to 4 Bytes')


class TestStlinkReadMem8(_TestStlink):
    """Tests for Stlink.read_mem8()"""

    def test_1byte(self):
        """test reading emory with 8 bit access"""
        data = list(range(1))
        self._com.xfer_mock.set_return_data([
            data,
        ])
        ret_data = self._stlink.read_mem8(0x08000000, 1)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x0c, 0x00, 0x00, 0x00, 0x08, 0x01, 0x00, 0x00, 0x00,
            ], 'data': None, 'rx_length': 1, 'tout': 200},
        ])
        self.assertEqual(ret_data, data)

    def test_64bytes(self):
        """test reading memory with 8 bit access"""
        data = list(range(64))
        self._com.xfer_mock.set_return_data([
            data,
        ])
        ret_data = self._stlink.read_mem8(0x08000000, 64)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x0c, 0x00, 0x00, 0x00, 0x08, 0x40, 0x00, 0x00, 0x00,
            ], 'data': None, 'rx_length': 64, 'tout': 200},
        ])
        self.assertEqual(ret_data, data)

    def test_over_size(self):
        """test setting memory register with unaligned address"""
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.read_mem8(0x20000000, 65)
        self.assertEqual(
            str(context.exception),
            'Too many Bytes to read (maximum is 64 Bytes)')


class TestStlinkWriteMem8(_TestStlink):
    """Tests for Stlink.write_mem8()"""

    def test_1byte(self):
        """test writing memory with 8 bit access"""
        data = list(range(1))
        self._com.xfer_mock.set_return_data([
            None,
            None,
        ])
        self._stlink.write_mem8(0x20001000, data)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x0d, 0x00, 0x10, 0x00, 0x20, 0x01, 0x00, 0x00, 0x00
            ], 'data': data, 'rx_length': 0, 'tout': 200},
        ])

    def test_64bytes(self):
        """test writing memory with 8 bit access"""
        data = list(range(64))
        self._com.xfer_mock.set_return_data([
            None,
            None,
        ])
        self._stlink.write_mem8(0x20001000, data)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x0d, 0x00, 0x10, 0x00, 0x20, 0x40, 0x00, 0x00, 0x00
            ], 'data': data, 'rx_length': 0, 'tout': 200},
        ])

    def test_over_size(self):
        """test setting memory register with unaligned address"""
        data = list(range(65))
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.write_mem8(0x20000000, data)
        self.assertEqual(
            str(context.exception),
            'Too many Bytes to write (maximum is 64 Bytes)')


class TestStlinkReadMem32(_TestStlink):
    """Tests for Stlink.read_mem32()"""

    def test_4bytes(self):
        """test reading emory with 32 bit access"""
        data = list(range(4))
        self._com.xfer_mock.set_return_data([
            data,
        ])
        ret_data = self._stlink.read_mem32(0x08000000, 4)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x07, 0x00, 0x00, 0x00, 0x08, 0x04, 0x00, 0x00, 0x00
            ], 'data': None, 'rx_length': 4, 'tout': 200},
        ])
        self.assertEqual(ret_data, data)

    def test_1024bytes(self):
        """test reading memory with 32 bit access"""
        data = list(range(4))
        self._com.xfer_mock.set_return_data([
            data,
        ])
        ret_data = self._stlink.read_mem32(0x08000000, 1024)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x07, 0x00, 0x00, 0x00, 0x08, 0x00, 0x04, 0x00, 0x00
            ], 'data': None, 'rx_length': 1024, 'tout': 200},
        ])
        self.assertEqual(ret_data, data)

    def test_oversize(self):
        """test setting memory register with unaligned address"""
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.read_mem32(0x20000000, 1028)
        self.assertEqual(
            str(context.exception),
            'Too many Bytes to read (maximum is 1024 Bytes)')

    def test_unaligned_address(self):
        """test setting memory register with unaligned address"""
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.read_mem32(0x20000001, 12)
        self.assertEqual(
            str(context.exception),
            'Address is not aligned to 4 Bytes')

    def test_unaligned_size(self):
        """test setting memory register with unaligned address"""
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.read_mem32(0x20000000, 13)
        self.assertEqual(
            str(context.exception),
            'Size is not aligned to 4 Bytes')


class TestStlinkWriteMem32(_TestStlink):
    """Tests for Stlink.write_mem32()"""

    def test_4bytes(self):
        """test writing memory with 32 bit access"""
        data = list(range(4))
        self._stlink.write_mem32(0x20001000, data)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x08, 0x00, 0x10, 0x00, 0x20, 0x04, 0x00, 0x00, 0x00
            ], 'data': data, 'rx_length': 0, 'tout': 200},
        ])

    def test_1024bytes(self):
        """test writing memory with 32 bit access"""
        data = list(range(1024))
        self._stlink.write_mem32(0x20001000, data)
        self.assertEqual(self._com.xfer_mock.get_call_log(), [
            {'command': [
                0xf2, 0x08, 0x00, 0x10, 0x00, 0x20, 0x00, 0x04, 0x00, 0x00
            ], 'data': data, 'rx_length': 0, 'tout': 200},
        ])

    def test_over_size(self):
        """test setting memory register with unaligned address"""
        data = list(range(1028))
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.write_mem32(0x20000000, data)
        self.assertEqual(
            str(context.exception),
            'Too many Bytes to write (maximum is 1024 Bytes)')

    def test_unaligned_address(self):
        """test setting memory register with unaligned address"""
        data = list(range(12))
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.write_mem32(0x20000001, data)
        self.assertEqual(
            str(context.exception),
            'Address is not aligned to 4 Bytes')

    def test_unaligned_size(self):
        """test setting memory register with unaligned address"""
        data = list(range(13))
        with self.assertRaises(swd.stlink.StlinkException) as context:
            self._stlink.write_mem32(0x20000000, data)
        self.assertEqual(
            str(context.exception),
            'Size is not aligned to 4 Bytes')
