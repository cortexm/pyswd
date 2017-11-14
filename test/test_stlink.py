"""Unit tests for stlink.py"""
import unittest
import swd


class StlinkComMock():
    """StlinkCom Mock class for testing Stlink class"""
    def __init__(self):
        """MOCK CONSTRUCTOR"""
        self._mock_return_data = []
        self._mock_call_log = []

    def mock_set_return_data(self, return_data):
        """MOCK METHOD set expected return data"""
        self._mock_return_data = return_data

    def mock_get_call_log(self):
        """MOCK METHOD get expected call log"""
        call_log = self._mock_call_log
        self._mock_call_log = []
        return call_log

    @property
    def version(self):
        """Mock version"""
        return 'V2'

    def xfer(self, command, data=None, rx_length=0, tout=200):
        """Mock xfer"""
        self._mock_call_log.append({
            'command': command,
            'data': data,
            'rx_length': rx_length,
            'tout': tout})
        if self._mock_return_data:
            ret = self._mock_return_data[0]
            del self._mock_return_data[0]
            return ret
        return None

class TestStlinkCotor(unittest.TestCase):
    """Tests for Stlink class"""

    def setUp(self):
        self._com = StlinkComMock()
        self._com.mock_set_return_data([
            [0x26, 0xc6, 0x83, 0x04, 0x48, 0x37],
            [0x02, 0x00],
            None,
            [0x80, 0x00],
            [0x80, 0x00],
        ])
        self._swd = swd.Stlink(stlinkcom=self._com)
        self._ctor_call_log = self._com.mock_get_call_log()

    def test_stlinkcom_xfer_call(self):
        """test for creating Stlink object"""
        self.assertEqual(self._ctor_call_log, [
            {'command': [241, 128], 'data': None, 'rx_length': 6, 'tout': 200},
            {'command': [245], 'data': None, 'rx_length': 2, 'tout': 200},
            {'command': [242, 33], 'data': None, 'rx_length': 0, 'tout': 200},
            {'command': [242, 67, 1], 'data': None, 'rx_length': 2, 'tout': 200},
            {'command': [242, 48, 163], 'data': None, 'rx_length': 2, 'tout': 200},
        ])

    def test_version_str(self):
        """test version string"""
        self.assertEqual(self._swd.version.str, 'ST-Link/V2 V2J27S6')

    def test_version_stlink(self):
        """test version string"""
        self.assertEqual(self._swd.version.stlink, 2)

    def test_version_jtag(self):
        """test version string"""
        self.assertEqual(self._swd.version.jtag, 27)

    def test_version_swim(self):
        """test version string"""
        self.assertEqual(self._swd.version.swim, 6)

    def test_version_mass(self):
        """test version string"""
        self.assertEqual(self._swd.version.mass, None)

    def test_version_api(self):
        """test version string"""
        self.assertEqual(self._swd.version.api, 2)

    def test_get_target_voltage(self):
        """test getting target voltage"""
        self._com.mock_set_return_data([
            [0xfa, 0x05, 0x00, 0x00, 0xfb, 0x07, 0x00, 0x00],
        ])
        target_voltage = self._swd.get_target_voltage()
        self.assertEqual(self._com.mock_get_call_log(), [
            {'command': [247], 'data': None, 'rx_length': 8, 'tout': 200},
        ])
        self.assertEqual(target_voltage, 3.2)

    def test_get_coreid(self):
        """test getting target voltage"""
        self._com.mock_set_return_data([
            [0x77, 0x14, 0xb1, 0x0b],
        ])
        coreid = self._swd.get_coreid()
        self.assertEqual(self._com.mock_get_call_log(), [
            {'command': [242, 34], 'data': None, 'rx_length': 4, 'tout': 200},
        ])
        self.assertEqual(coreid, 0xbb11477)
