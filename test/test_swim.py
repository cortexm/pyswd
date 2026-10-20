"""Unit tests for SWIM and STM8
"""

import unittest
import swd
import swd.stlink.swim


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


class UsbMock():
    """USB Mock class for testing StlinkSwim class"""
    DEV_NAME = 'V2'

    def __init__(self):
        self.xfer_mock = FncMock()

    @property
    def dev_name(self):
        """Mock device name"""
        return 'V2'

    def xfer(self, command, data=None, rx_length=0, timeout=200, pad=True):
        """Mock xfer"""
        return self.xfer_mock.fnc(
            command=command,
            data=data,
            rx_length=rx_length,
            timeout=timeout,
            pad=pad)


# SWIM command shortcut builders
def _swim(sub, data=None):
    """Build unpadded SWIM command bytes"""
    cmd = bytes([0xf4, sub])
    if data:
        cmd += data
    return cmd


_STATUS_OK = bytes([0x00, 0x00, 0x00, 0x00])
_STATUS_BUSY = bytes([0x01, 0x00, 0x00, 0x00])
_XFER_T = 200


def _xfer_log(command, data=None, rx_length=0, pad=False):
    """Build expected xfer call log entry (pad=False for SWIM commands)"""
    return {
        'command': command,
        'data': data,
        'rx_length': rx_length,
        'timeout': _XFER_T,
        'pad': pad}


def _connect_return_data(mode=0x02, buf_size=64, high_speed_csr=None):
    """Return data for full StlinkSwim connect sequence

    One entry per xfer call; None for calls without response.
    """
    data = [
        bytes([0x28, 0xc7, 0x83, 0x04, 0x48, 0x37]),  # version V2J35S7
        bytes([mode, 0x00]),  # current mode
        None,  # exit debug
        None,  # swim enter
        buf_size.to_bytes(2, 'little'),  # read buffer size
        bytes(8),  # capabilities
        None,  # assert reset
        _STATUS_OK,  # assert reset status
        None,  # enter seq
        _STATUS_OK,  # enter seq status
        None,  # write SWIM_CSR
        _STATUS_OK,  # write SWIM_CSR status
        None,  # write SWIM_DM_CSR2
        _STATUS_OK,  # write SWIM_DM_CSR2 status
        None,  # gen reset
        None,  # deassert reset
        _STATUS_OK,  # deassert reset status
    ]
    if high_speed_csr is not None:
        data.extend([
            None,  # read SWIM_CSR (READMEM)
            _STATUS_OK,  # read SWIM_CSR status
            bytes([high_speed_csr]),  # SWIM_CSR value
        ])
        if high_speed_csr & 0x02:  # HSIT set
            data.extend([
                None,  # write SWIM_CSR|HS
                _STATUS_OK,  # write status
                None,  # speed command
            ])
    return data


def _connect_call_log(buf_size=64, high_speed=False, high_speed_csr=None):
    """Expected xfer call log for StlinkSwim connect sequence"""
    log = [
        _xfer_log(bytes([0xf1, 0x80]), rx_length=6, pad=True),  # get version
        _xfer_log(bytes([0xf5]), rx_length=2, pad=True),  # get current mode
        _xfer_log(bytes([0xf2, 0x21]), pad=True),  # exit debug
        _xfer_log(_swim(0x00)),  # swim enter
        _xfer_log(_swim(0x0d), rx_length=2),  # read buffer size
        _xfer_log(_swim(0x02, bytes([0x01])), rx_length=8),  # read cap
        _xfer_log(_swim(0x07)),  # assert reset
        _xfer_log(_swim(0x09), rx_length=4),  # status
        _xfer_log(_swim(0x04)),  # enter seq
        _xfer_log(_swim(0x09), rx_length=4),  # status
        _xfer_log(
            _swim(0x0a, bytes([0x00, 0x01, 0x00, 0x00, 0x7f, 0x80])),
            data=bytes([0xa1])),  # write SWIM_CSR
        _xfer_log(_swim(0x09), rx_length=4),  # status
        _xfer_log(
            _swim(0x0a, bytes([0x00, 0x01, 0x00, 0x00, 0x7f, 0x99])),
            data=bytes([0x08])),  # write SWIM_DM_CSR2 (STALL)
        _xfer_log(_swim(0x09), rx_length=4),  # status
        _xfer_log(_swim(0x05)),  # gen reset
        _xfer_log(_swim(0x08)),  # deassert reset
        _xfer_log(_swim(0x09), rx_length=4),  # status
    ]
    if high_speed:
        log.extend([
            _xfer_log(
                _swim(0x0b, bytes([0x00, 0x01, 0x00, 0x00, 0x7f, 0x80]))),
            _xfer_log(_swim(0x09), rx_length=4),  # status
            _xfer_log(_swim(0x0c), rx_length=1),  # read SWIM_CSR
        ])
        if high_speed_csr & 0x02:  # HSIT set
            log.extend([
                _xfer_log(
                    _swim(0x0a, bytes([0x00, 0x01, 0x00, 0x00, 0x7f, 0x80])),
                    data=bytes([high_speed_csr | 0x10])),
                _xfer_log(_swim(0x09), rx_length=4),  # status
                _xfer_log(_swim(0x03, bytes([0x01]))),  # speed high
            ])
    return log


class _TestStlinkSwim(unittest.TestCase):
    """Base class for testing StlinkSwim class"""

    def setUp(self):
        self._usb = UsbMock()

    def _create(self, high_speed=False, **kwargs):
        """Create StlinkSwim with mocked USB"""
        self._usb.xfer_mock.set_return_data(
            _connect_return_data(
                high_speed_csr=0x02 if high_speed else None))
        driver = swd.stlink.swim.StlinkSwim(
            usb=self._usb, high_speed=high_speed, **kwargs)
        self._usb.xfer_mock.get_call_log()  # clear connect log
        return driver


class TestStlinkSwimConnect(_TestStlinkSwim):
    """Tests for StlinkSwim connect sequence"""

    def test_connect_call(self):
        """test exact commands of connect sequence"""
        self._usb.xfer_mock.set_return_data(_connect_return_data())
        swd.stlink.swim.StlinkSwim(usb=self._usb, high_speed=False)
        self.assertEqual(
            self._usb.xfer_mock.get_call_log(),
            _connect_call_log())

    def test_connect_high_speed(self):
        """test connect sequence with high speed switch"""
        self._usb.xfer_mock.set_return_data(
            _connect_return_data(high_speed_csr=0x02))
        swd.stlink.swim.StlinkSwim(usb=self._usb, high_speed=True)
        self.assertEqual(
            self._usb.xfer_mock.get_call_log(),
            _connect_call_log(high_speed=True, high_speed_csr=0x02))

    def test_buffer_size(self):
        """test read_buf_size from READ_BUFFERSIZE"""
        self._usb.xfer_mock.set_return_data(_connect_return_data())
        driver = swd.stlink.swim.StlinkSwim(
            usb=self._usb, high_speed=False)
        self.assertEqual(driver.maximum_8bit_data, 64)

    def test_version(self):
        """test ST-Link version after connect"""
        self._usb.xfer_mock.set_return_data(_connect_return_data())
        driver = swd.stlink.swim.StlinkSwim(
            usb=self._usb, high_speed=False)
        self.assertEqual(driver.get_version().str, 'ST-Link/V2 V2J35S7')


class TestStlinkSwimReadWrite(_TestStlinkSwim):
    """Tests for StlinkSwim read/write memory"""

    def test_read_mem8(self):
        """test read single chunk"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([
            None,  # READMEM command
            _STATUS_OK,
            bytes([0x11, 0x22]),
        ])
        data = driver.read_mem8(0x123456, 2)
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(
                _swim(0x0b, bytes([0x00, 0x02, 0x00, 0x12, 0x34, 0x56]))),
            _xfer_log(_swim(0x09), rx_length=4),
            _xfer_log(_swim(0x0c), rx_length=2),
        ])
        self.assertEqual(data, bytes([0x11, 0x22]))

    def test_read_mem8_too_many(self):
        """test read size guard"""
        driver = self._create()
        with self.assertRaises(swd.SwimException):
            driver.read_mem8(0, 65)
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [])

    def test_write_mem8(self):
        """test write single chunk"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([
            None,  # WRITEMEM command
            _STATUS_OK,
        ])
        driver.write_mem8(0x8000, bytes([0xaa, 0xbb]))
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(
                _swim(0x0a, bytes([0x00, 0x02, 0x00, 0x00, 0x80, 0x00])),
                data=bytes([0xaa, 0xbb])),
            _xfer_log(_swim(0x09), rx_length=4),
        ])

    def test_write_mem8_too_many(self):
        """test write size guard"""
        driver = self._create()
        with self.assertRaises(swd.SwimException):
            driver.write_mem8(0, bytes(65))
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [])

    def test_read_mem_chunking(self):
        """test read with chunking by buffer size"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([
            None,  # READMEM
            _STATUS_OK,
            bytes([0xaa] * 64),
            None,  # READMEM
            _STATUS_OK,
            bytes([0xbb] * 36),
        ])
        data = driver.read_mem(0x1000, 100)
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(
                _swim(0x0b, bytes([0x00, 0x40, 0x00, 0x00, 0x10, 0x00]))),
            _xfer_log(_swim(0x09), rx_length=4),
            _xfer_log(_swim(0x0c), rx_length=64),
            _xfer_log(
                _swim(0x0b, bytes([0x00, 0x24, 0x00, 0x00, 0x10, 0x40]))),
            _xfer_log(_swim(0x09), rx_length=4),
            _xfer_log(_swim(0x0c), rx_length=36),
        ])
        self.assertEqual(data, bytes([0xaa] * 64 + [0xbb] * 36))

    def test_write_mem_chunking(self):
        """test write with chunking by buffer size"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([
            None,  # WRITEMEM
            _STATUS_OK,
            None,  # WRITEMEM
            _STATUS_OK,
        ])
        driver.write_mem(0x1000, bytes([1] * 100))
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(
                _swim(0x0a, bytes([0x00, 0x40, 0x00, 0x00, 0x10, 0x00])),
                data=bytes([1] * 64)),
            _xfer_log(_swim(0x09), rx_length=4),
            _xfer_log(
                _swim(0x0a, bytes([0x00, 0x24, 0x00, 0x00, 0x10, 0x40])),
                data=bytes([1] * 36)),
            _xfer_log(_swim(0x09), rx_length=4),
        ])

    def test_status_busy_poll(self):
        """test status polling on BUSY"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([
            None,  # WRITEMEM command
            _STATUS_BUSY,
            _STATUS_BUSY,
            _STATUS_OK,
        ])
        driver.write_mem8(0x8000, bytes([0x01]))
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(
                _swim(0x0a, bytes([0x00, 0x01, 0x00, 0x00, 0x80, 0x00])),
                data=bytes([0x01])),
            _xfer_log(_swim(0x09), rx_length=4),
            _xfer_log(_swim(0x09), rx_length=4),
            _xfer_log(_swim(0x09), rx_length=4),
        ])

    def test_status_error(self):
        """test error status raises exception"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([
            None,  # WRITEMEM command
            bytes([0x04, 0x00, 0x00, 0x00]),  # NO_RESPONSE
        ])
        with self.assertRaises(swd.SwimException):
            driver.write_mem8(0x8000, bytes([0x01]))

    def test_get_set_mem32(self):
        """test get_mem32/set_mem32 byte emulation"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([
            None,  # READMEM
            _STATUS_OK,
            bytes([0x78, 0x56, 0x34, 0x12]),
        ])
        value = driver.get_mem32(0x100)
        self.assertEqual(value, 0x12345678)
        self._usb.xfer_mock.set_return_data([
            None,  # WRITEMEM
            _STATUS_OK,
        ])
        driver.set_mem32(0x100, 0xaabbccdd)
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(
                _swim(0x0b, bytes([0x00, 0x04, 0x00, 0x00, 0x01, 0x00]))),
            _xfer_log(_swim(0x09), rx_length=4),
            _xfer_log(_swim(0x0c), rx_length=4),
            _xfer_log(
                _swim(0x0a, bytes([0x00, 0x04, 0x00, 0x00, 0x01, 0x00])),
                data=bytes([0xdd, 0xcc, 0xbb, 0xaa])),
            _xfer_log(_swim(0x09), rx_length=4),
        ])


class TestStlinkSwimReset(_TestStlinkSwim):
    """Tests for StlinkSwim reset API"""

    def test_assert_reset(self):
        """test assert reset"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([None, _STATUS_OK])
        driver.assert_reset()
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(_swim(0x07)),
            _xfer_log(_swim(0x09), rx_length=4),
        ])

    def test_deassert_reset(self):
        """test deassert reset"""
        driver = self._create()
        self._usb.xfer_mock.set_return_data([None, _STATUS_OK])
        driver.deassert_reset()
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(_swim(0x08)),
            _xfer_log(_swim(0x09), rx_length=4),
        ])

    def test_generate_reset(self):
        """test generate reset"""
        driver = self._create()
        driver.generate_reset()
        self.assertEqual(self._usb.xfer_mock.get_call_log(), [
            _xfer_log(_swim(0x05)),
        ])


class DrvMock():
    """Driver Mock class for testing Swim class"""

    def __init__(self, maximum_8bit_data=64):
        self._maximum_8bit_data = maximum_8bit_data
        self.read_mem8_mock = FncMock(bytes())
        self.write_mem8_mock = FncMock()
        self.get_mem32_mock = FncMock(0)
        self.set_mem32_mock = FncMock()
        self.get_version_mock = FncMock()
        self.get_target_voltage_mock = FncMock(0.0)

    @property
    def maximum_8bit_data(self):
        return self._maximum_8bit_data

    @property
    def com(self):
        return None

    def read_mem8(self, address, size):
        """Mock read_mem8"""
        return self.read_mem8_mock.fnc(address=address, size=size)

    def write_mem8(self, address, data):
        """Mock write_mem8"""
        return self.write_mem8_mock.fnc(address=address, data=data)

    def get_mem32(self, address):
        """Mock get_mem32"""
        return self.get_mem32_mock.fnc(address=address)

    def set_mem32(self, address, value):
        """Mock set_mem32"""
        return self.set_mem32_mock.fnc(address=address, value=value)

    def get_version(self):
        """Mock get_version"""
        return self.get_version_mock.fnc()

    def get_target_voltage(self):
        """Mock get_target_voltage"""
        return self.get_target_voltage_mock.fnc()


class TestSwimReadWrite(unittest.TestCase):
    """Tests for Swim high level read/write"""

    def setUp(self):
        self._drv = DrvMock()
        self._swim = swd.Swim(driver=self._drv)

    def test_read_mem(self):
        """Test reading memory with chunking"""
        self._drv.read_mem8_mock.set_return_data([
            bytes(range(64)),
            bytes(range(64, 100)),
        ])
        data = self._swim.read_mem(0x1000, 100)
        self.assertEqual(self._drv.read_mem8_mock.get_call_log(), [
            {'address': 0x1000, 'size': 64},
            {'address': 0x1040, 'size': 36},
        ])
        self.assertEqual(data, bytes(range(100)))

    def test_write_mem(self):
        """Test writing memory with chunking"""
        self._swim.write_mem(0x1000, list(range(100)))
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x1000, 'data': bytes(range(64))},
            {'address': 0x1040, 'data': bytes(range(64, 100))},
        ])

    def test_fill_mem(self):
        """Test filling memory with pattern"""
        self._swim.fill_mem(0x1000, bytes([5, 6]), 5)
        self.assertEqual(self._drv.write_mem8_mock.get_call_log(), [
            {'address': 0x1000, 'data': bytes([5, 6, 5, 6, 5])},
        ])

    def test_maximum_data(self):
        """Test maximum transfer properties"""
        self.assertEqual(self._swim.maximum_8bit_data, 64)
        self.assertEqual(self._swim.maximum_16bit_data, 64)
        self.assertEqual(self._swim.maximum_32bit_data, 64)

    def test_get_set_mem32(self):
        """Test get_mem32/set_mem32 pass-through"""
        self._drv.get_mem32_mock.set_return_data([0x12345678])
        self.assertEqual(self._swim.get_mem32(0x100), 0x12345678)
        self._swim.set_mem32(0x100, 0x12345678)
        self.assertEqual(self._drv.set_mem32_mock.get_call_log(), [
            {'address': 0x100, 'value': 0x12345678},
        ])


class SwimCoreMock():
    """Swim Mock class for testing Stm8 class"""

    def __init__(self):
        self.read_mem8_mock = FncMock(bytes([0x00]))
        self.write_mem8_mock = FncMock()
        self.read_mem_mock = FncMock(bytes([0x00]))
        self.write_mem_mock = FncMock()
        self.srst_mock = FncMock()

    def read_mem8(self, address, size):
        """Mock read_mem8"""
        return self.read_mem8_mock.fnc(address=address, size=size)

    def write_mem8(self, address, data):
        """Mock write_mem8"""
        return self.write_mem8_mock.fnc(address=address, data=data)

    def read_mem(self, address, size):
        """Mock read_mem"""
        return self.read_mem_mock.fnc(address=address, size=size)

    def write_mem(self, address, data):
        """Mock write_mem"""
        return self.write_mem_mock.fnc(address=address, data=data)

    def srst(self):
        """Mock srst"""
        return self.srst_mock.fnc()


class _TestStm8(unittest.TestCase):
    """Base class for testing Stm8 class"""

    def setUp(self):
        self._swim = SwimCoreMock()
        self._stm8 = swd.Stm8(self._swim)


class TestStm8HaltRun(_TestStm8):
    """Tests for Stm8 halt/run/is_halted"""

    def test_halt(self):
        """test halt"""
        self._swim.read_mem8_mock.set_return_data([bytes([0x00])])
        self._stm8.halt()
        self.assertEqual(self._swim.read_mem8_mock.get_call_log(), [
            {'address': 0x7f99, 'size': 1},
        ])
        self.assertEqual(self._swim.write_mem8_mock.get_call_log(), [
            {'address': 0x7f99, 'data': bytes([0x08])},
        ])

    def test_run(self):
        """test run"""
        self._swim.read_mem8_mock.set_return_data([bytes([0x08])])
        self._stm8.run()
        self.assertEqual(self._swim.write_mem8_mock.get_call_log(), [
            {'address': 0x7f99, 'data': bytes([0x00])},
        ])

    def test_is_halted(self):
        """test is_halted"""
        self._swim.read_mem8_mock.set_return_data([bytes([0x08])])
        self.assertEqual(self._stm8.is_halted(), True)
        self._swim.read_mem8_mock.set_return_data([bytes([0x00])])
        self.assertEqual(self._stm8.is_halted(), False)


class TestStm8Reset(_TestStm8):
    """Tests for Stm8 reset/reset_halt"""

    def test_reset(self):
        """test reset"""
        self._swim.read_mem8_mock.set_return_data([
            bytes([0xa1]),  # SWIM_CSR with SWIM_DM
        ])
        self._stm8.reset()
        self.assertEqual(self._swim.write_mem8_mock.get_call_log(), [
            {'address': 0x7f80, 'data': bytes([0xa5])},  # | RST
            {'address': 0x7f99, 'data': bytes([0x00])},  # clear stall
        ])
        self.assertEqual(self._swim.srst_mock.get_call_log(), [{}])

    def test_reset_halt(self):
        """test reset_halt"""
        self._swim.read_mem8_mock.set_return_data([
            bytes([0xa1]),  # SWIM_CSR with SWIM_DM
        ])
        self._stm8.reset_halt()
        self.assertEqual(self._swim.write_mem8_mock.get_call_log(), [
            {'address': 0x7f80, 'data': bytes([0xa5])},  # | RST
            {'address': 0x7f99, 'data': bytes([0x08])},  # keep stall
        ])
        self.assertEqual(self._swim.srst_mock.get_call_log(), [{}])

    def test_reset_not_debug_mode(self):
        """test reset without SWIM_DM raises exception"""
        self._swim.read_mem8_mock.set_return_data([bytes([0x00])])
        with self.assertRaises(swd.Stm8Exception):
            self._stm8.reset()


class TestStm8Registers(_TestStm8):
    """Tests for Stm8 registers"""

    def test_get_reg_byte(self):
        """test get 8 bit register"""
        self._swim.read_mem8_mock.set_return_data([bytes([0x5a])])
        value = self._stm8.get_reg('A')
        self.assertEqual(self._swim.read_mem8_mock.get_call_log(), [
            {'address': 0x7f00, 'size': 1},
        ])
        self.assertEqual(value, 0x5a)

    def test_get_reg_pc(self):
        """test get assembled PC register"""
        self._swim.read_mem_mock.set_return_data([bytes([0x01, 0x82, 0x00])])
        value = self._stm8.get_reg('PC')
        self.assertEqual(self._swim.read_mem_mock.get_call_log(), [
            {'address': 0x7f01, 'size': 3},
        ])
        self.assertEqual(value, 0x018200)

    def test_set_reg_x(self):
        """test set assembled X register"""
        self._stm8.set_reg('X', 0x1234)
        self.assertEqual(self._swim.write_mem_mock.get_call_log(), [
            {'address': 0x7f04, 'data': bytes([0x12, 0x34])},
        ])

    def test_set_reg_byte(self):
        """test set 8 bit register"""
        self._stm8.set_reg('CC', 0x08)
        self.assertEqual(self._swim.write_mem8_mock.get_call_log(), [
            {'address': 0x7f0a, 'data': bytes([0x08])},
        ])

    def test_get_reg_all(self):
        """test get all registers"""
        regs = bytes([
            0xaa,  # A
            0x01, 0x82, 0x00,  # PCE PCH PCL
            0x12, 0x34,  # XH XL
            0x56, 0x78,  # YH YL
            0x01, 0x00,  # SPH SPL
            0x08,  # CC
        ])
        self._swim.read_mem_mock.set_return_data([regs])
        values = self._stm8.get_reg_all()
        self.assertEqual(self._swim.read_mem_mock.get_call_log(), [
            {'address': 0x7f00, 'size': 11},
        ])
        self.assertEqual(values['A'], 0xaa)
        self.assertEqual(values['PC'], 0x018200)
        self.assertEqual(values['X'], 0x1234)
        self.assertEqual(values['Y'], 0x5678)
        self.assertEqual(values['SP'], 0x0100)
        self.assertEqual(values['CC'], 0x08)

    def test_wrong_register(self):
        """test wrong register name"""
        with self.assertRaises(swd.Stm8Exception):
            self._stm8.get_reg('R0')


class TestStm8Flash(_TestStm8):
    """Tests for Stm8 flash programming"""

    def test_unlock_flash(self):
        """test FLASH unlock key order"""
        self._stm8.unlock_flash()
        self.assertEqual(self._swim.write_mem8_mock.get_call_log(), [
            {'address': 0x5062, 'data': bytes([0x56])},
            {'address': 0x5062, 'data': bytes([0xae])},
        ])

    def test_unlock_data(self):
        """test DATA unlock key order"""
        self._stm8.unlock_data()
        self.assertEqual(self._swim.write_mem8_mock.get_call_log(), [
            {'address': 0x5064, 'data': bytes([0xae])},
            {'address': 0x5064, 'data': bytes([0x56])},
        ])

    def test_unlock_flash_stm8l(self):
        """test FLASH unlock on STM8L (different PUKR address)"""
        stm8 = swd.Stm8(self._swim, part='STM8L')
        stm8.unlock_flash()
        self.assertEqual(self._swim.write_mem8_mock.get_call_log(), [
            {'address': 0x5052, 'data': bytes([0x56])},
            {'address': 0x5052, 'data': bytes([0xae])},
        ])

    def test_write_flash_block(self):
        """test FLASH block programming sequence"""
        # read DM_CSR2 (stall), IAPSR (EOP), IAPSR (lock)
        self._swim.read_mem8_mock.set_return_data([
            bytes([0x00]),  # DM_CSR2
            bytes([0x04]),  # IAPSR EOP set
            bytes([0x06]),  # IAPSR for lock
        ])
        self._stm8.write_flash_block(0x8000, bytes([1] * 64), fast=True)
        write_log = self._swim.write_mem8_mock.get_call_log()
        self.assertEqual(write_log, [
            {'address': 0x50c6, 'data': bytes([0x00])},  # CKDIVR
            {'address': 0x7f99, 'data': bytes([0x08])},  # stall CPU
            {'address': 0x505b, 'data': bytes([0x10])},  # CR2 fast
            {'address': 0x505c, 'data': bytes([0xef])},  # NCR2
            {'address': 0x5062, 'data': bytes([0x56])},  # PUKR key1
            {'address': 0x5062, 'data': bytes([0xae])},  # PUKR key2
            # _lock_flash: IAPSR (0x06) & ~(DUL|PUL)
            {'address': 0x505f, 'data': bytes([0x06 & ~0x0a & 0xff])},
        ])
        self.assertEqual(self._swim.write_mem_mock.get_call_log(), [
            {'address': 0x8000, 'data': bytes([1] * 64)},
        ])
        self.assertEqual(self._swim.read_mem8_mock.get_call_log(), [
            {'address': 0x7f99, 'size': 1},
            {'address': 0x505f, 'size': 1},
            {'address': 0x505f, 'size': 1},
        ])

    def test_write_flash_block_misaligned(self):
        """test FLASH block address alignment check"""
        with self.assertRaises(swd.Stm8Exception):
            self._stm8.write_flash_block(0x8001, bytes([1] * 64))

    def test_write_flash_block_wrong_size(self):
        """test FLASH block size check"""
        with self.assertRaises(swd.Stm8Exception):
            self._stm8.write_flash_block(0x8000, bytes([1] * 63))

    def test_wait_eop_write_protected(self):
        """test wait_eop raises on write protection"""
        self._swim.read_mem8_mock.set_return_data([bytes([0x01])])
        with self.assertRaises(swd.Stm8Exception):
            self._stm8.wait_eop()

    def test_wait_eop_timeout(self):
        """test wait_eop raises on timeout"""
        self._swim.read_mem8_mock.set_return_data(
            [bytes([0x00])] * 5)
        with self.assertRaises(swd.Stm8Exception):
            self._stm8.wait_eop()
