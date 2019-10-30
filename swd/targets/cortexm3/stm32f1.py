"""STM32F1xx"""

import swd.targets.stm32 as _stm32


class Stm32f1(_stm32.Stm32):
    """STM32F0xx"""

    _CORE = "Cortex-M3"
    _FAMILY = "STM32F1"
    _IDCODE_REG = 0xE0042000
    _FLAS_SIZE_REG = 0x1ffff7e0
    _FREQ = 24000000
    _DEVICES = [
    ]

    def __init__(self, cortexm, expected_devices=None):
        super().__init__(cortexm, expected_devices)
