"""Unit tests for bitfield.py
"""

import unittest
import swd.bitfield


class Bitfield32(unittest.TestCase):
    """Testing 32 bit register"""

    def setUp(self):
        self._reg = swd.bitfield.Bitfield((
            ('A', 1),
            ('B', 2),
            (None, 1),
            ('C', 4),
            (None, 8),
            ('D', 12),
            ('E', 4),
        ), raw=0x12345675)

    def test_read_raw(self):
        """Test read raw"""
        self.assertEqual(self._reg.raw, 0x12345675)

    def test_read_a(self):
        """Test read A"""
        self.assertEqual(self._reg.get('A'), 0x1)

    def test_read_b(self):
        """Test read B"""
        self.assertEqual(self._reg.get('B'), 0x2)

    def test_read_c(self):
        """Test read C"""
        self.assertEqual(self._reg.get('C'), 0x7)

    def test_read_d(self):
        """Test read D"""
        self.assertEqual(self._reg.get('D'), 0x234)

    def test_read_e(self):
        """Test read E"""
        self.assertEqual(self._reg.get('E'), 0x1)

    def test_write_raw(self):
        """Test write raw"""
        self._reg.raw = 0x87654321
        self.assertEqual(self._reg.raw, 0x87654321)

    def test_write_a_0(self):
        """Test write A 0"""
        self._reg.set('A', 0)
        self.assertEqual(self._reg.raw, 0x12345674)

    def test_write_a_1(self):
        """Test write A 1"""
        self._reg.set('A', 1)
        self.assertEqual(self._reg.raw, 0x12345675)

    def test_write_b(self):
        """Test write B"""
        self._reg.set('B', 1)
        self.assertEqual(self._reg.raw, 0x12345673)

    def test_write_c(self):
        """Test write C"""
        self._reg.set('C', 0xa)
        self.assertEqual(self._reg.raw, 0x123456a5)

    def test_write_d(self):
        """Test write D"""
        self._reg.set('D', 0xabc)
        self.assertEqual(self._reg.raw, 0x1abc5675)

    def test_write_e(self):
        """Test write E"""
        self._reg.set('E', 0xf)
        self.assertEqual(self._reg.raw, 0xf2345675)

    def test_get_bits_1(self):
        """Test get_bits method"""
        val = self._reg.get_bits({
            'A': 1,
            'B': 2,
        })
        self.assertEqual(val, 0x00000005)

    def test_get_bits_2(self):
        """Test get_bits method"""
        val = self._reg.get_bits({
            'C': 0xa,
            'D': 0xabc,
        })
        self.assertEqual(val, 0x0abc00a0)


class Bitfield8(unittest.TestCase):
    """Testing 8 bit register"""

    def setUp(self):
        self._reg = swd.bitfield.Bitfield((
            ('A', 1),
            ('B', 2),
            (None, 1),
            ('C', 4),
        ), raw=0x75, bits=8)

    def test_read_raw(self):
        """Test read raw"""
        self.assertEqual(self._reg.raw, 0x75)

    def test_read_a(self):
        """Test read A"""
        self.assertEqual(self._reg.get('A'), 0x1)

    def test_read_b(self):
        """Test read B"""
        self.assertEqual(self._reg.get('B'), 0x2)

    def test_read_c(self):
        """Test read C"""
        self.assertEqual(self._reg.get('C'), 0x7)

    def test_write_raw(self):
        """Test write raw"""
        self._reg.raw = 0x21
        self.assertEqual(self._reg.raw, 0x21)

    def test_write_a_0(self):
        """Test write A 0"""
        self._reg.set('A', 0)
        self.assertEqual(self._reg.raw, 0x74)

    def test_write_a_1(self):
        """Test write A 1"""
        self._reg.set('A', 1)
        self.assertEqual(self._reg.raw, 0x75)

    def test_write_b(self):
        """Test write B"""
        self._reg.set('B', 1)
        self.assertEqual(self._reg.raw, 0x73)

    def test_write_c(self):
        """Test write C"""
        self._reg.set('C', 0xa)
        self.assertEqual(self._reg.raw, 0xa5)
