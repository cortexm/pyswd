"""STM32F0xx"""

import swd.devices.memory as _mem
import swd.devices.stm32 as _stm32


class Stm32g0(_stm32.Stm32):
    """STM32G0xx"""

    _NAME = "STM32G0"
    _IDCODE_REG = 0x40015800
    _FLAS_SIZE_REG = 0x1fff75e0
    _FREQ = 64000000
    _MCUS = [
        {
            'mcu_name': 'STM32G070x8',
            'dev_id': 0x460,
            'flash_size': 64 * _mem.KILO,
            'sram_size': 32 * _mem.KILO,
            'freq': 64,
            'flash_page_sizes': 2 * _mem.KILO,
        }, {
            'mcu_name': 'STM32G070xB',
            'dev_id': 0x460,
            'flash_size': 128 * _mem.KILO,
            'sram_size': 32 * _mem.KILO,
            'freq': 64,
            'flash_page_sizes': 2 * _mem.KILO,
        }, {
            'mcu_name': 'STM32G071x8',
            'dev_id': 0x460,
            'flash_size': 64 * _mem.KILO,
            'sram_size': 32 * _mem.KILO,
            'freq': 64,
            'flash_page_sizes': 2 * _mem.KILO,
        }, {
            'mcu_name': 'STM32G071xB',
            'dev_id': 0x460,
            'flash_size': 128 * _mem.KILO,
            'sram_size': 32 * _mem.KILO,
            'freq': 64,
            'flash_page_sizes': 2 * _mem.KILO,
        }, ]
