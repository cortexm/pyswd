"""Unit tests package

Installs a minimal stub for the pyusb module when the real one is not
available, so the test suite (which mocks all USB transfers) can run
without pyusb/libusb installed.
"""

import sys
import types

try:
    import usb.core  # noqa: F401
except ImportError:
    _usb = types.ModuleType('usb')
    _usb_core = types.ModuleType('usb.core')

    class _USBError(Exception):
        """Stub for usb.USBError"""

    class _NoBackendError(_USBError):
        """Stub for usb.core.NoBackendError"""

    def _find(*args, **kwargs):
        """Stub for usb.core.find - returns no devices"""
        return iter([])

    _usb_core.NoBackendError = _NoBackendError
    _usb_core.find = _find
    _usb.USBError = _USBError
    _usb.core = _usb_core
    sys.modules['usb'] = _usb
    sys.modules['usb.core'] = _usb_core
