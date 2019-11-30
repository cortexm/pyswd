"""MCU"""


class McuError(Exception):
    """General STM32 error"""


class McuException(McuError):
    """General STM32 exception"""


class UnknownMcuDetected(McuException):
    """Raised when MCU is not detected"""


class McuNotMatch(McuException):
    """Raised when expected device(s) was not detected"""


class Mcu:
    """General MCU class"""

    def __init__(self, cortexm):
        self._cortexm = cortexm

    @property
    def cortexm(self):
        """Instance of CortexM"""
        return self._cortexm

    @property
    def swd(self):
        """Instance of Swd"""
        return self._cortexm.swd

    def get_name(self):
        """Return detected MCU name"""
        raise NotImplementedError()

    def load_svd(self):
        """Load SVD associated with this MCU"""
        raise NotImplementedError()

    def get_flash_size(self):
        """Return minimal size of all memory regions"""
        raise NotImplementedError()
