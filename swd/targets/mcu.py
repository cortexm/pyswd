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

    def __init__(self, cortexm, expected_mcus):
        self._cortexm = cortexm
        self._expected_mcus = expected_mcus
        self._memory_regions = []

    @property
    def cortexm(self):
        """Instance of CortexM"""
        return self._cortexm

    @property
    def swd(self):
        """Instance of Swd"""
        return self._cortexm.swd

    def get_mcu_name(self):
        """Return detected_ MCU name"""
        raise NotImplementedError()

    def get_mcu_revision(self):
        """Return MCU revision string"""
        raise NotImplementedError()
