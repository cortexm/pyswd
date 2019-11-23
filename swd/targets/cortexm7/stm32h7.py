"""STM32H7xx"""

import swd.targets.memory as _mem
import swd.targets.stm32 as _stm32


class Stm32h7(_stm32.Stm32):
    """STM32H7xx"""

    _NAME = "STM32H7"
    _IDCODE_REG = 0x5c001000
    _FLAS_SIZE_REG = 0x1ff1e880
    _FLASH_2M = [
        {
            'name': "BANK1",
            'start_address': 0x08000000,
            'size': 1024 * _mem.KILO,
            'sector_size': 128 * _mem.KILO,
        }, {
            'name': "BANK2",
            'start_address': 0x08100000,
            'size': 1024 * _mem.KILO,
            'sector_size': 128 * _mem.KILO,
        }
    ]
    _FLASH_128K = [
        {
            'name': "BANK1",
            'start_address': 0x08000000,
            'size': 128 * _mem.KILO,
            'sector_size': 128 * _mem.KILO,
        }
    ]
    _MCUS = [
        {
            'mcu_name': 'STM32H743xI',
            'dev_id': 0x450,
            'flash_size': 2048 * _mem.KILO,
            'sram_size': 1024 * _mem.KILO,
            'flash': _FLASH_2M,
            'freq': 480,
            'svd_file': 'svd/STM32H7_svd_V1.5/STM32H743x.svd',
        }, {
            'mcu_name': 'STM32H753xI',
            'dev_id': 0x450,
            'flash_size': 2048 * _mem.KILO,
            'sram_size': 1024 * _mem.KILO,
            'flash': _FLASH_2M,
            'freq': 480,
            'svd_file': 'svd/STM32H7_svd_V1.5/STM32H745x.svd',
        }, {
            'mcu_name': 'STM32H750xB',
            'dev_id': 0x450,
            'flash_size': 128 * _mem.KILO,
            'sram_size': 1024 * _mem.KILO,
            'flash': _FLASH_128K,
            'freq': 480,
            'svd_file': 'svd/STM32H7_svd_V1.5/STM32H750x.svd',
        }, ]
