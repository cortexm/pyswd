"""STM32F0xx"""

import swd.targets.memory as _mem
import swd.targets.stm32 as _stm32


class Stm32f0(_stm32.Stm32):
    """STM32F0xx"""

    _NAME = "STM32F0"
    _IDCODE_REG = 0x40015800
    _FLAS_SIZE_REG = 0x1ffff7cc
    _FREQ = 48000000
    _MCUS = [
        {
            'mcu_name': 'STM32F030x4',
            'dev_id': 0x444,
            'flash_size': 16 * _mem.KILO,
            'sram_size': 4 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F030x6',
            'dev_id': 0x444,
            'flash_size': 32 * _mem.KILO,
            'sram_size': 4 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F030x8',
            'dev_id': 0x440,
            'flash_size': 64 * _mem.KILO,
            'sram_size': 8 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F030xC',
            'dev_id': 0x442,
            'flash_size': 256 * _mem.KILO,
            'sram_size': 32 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F031x4',
            'dev_id': 0x444,
            'flash_size': 16 * _mem.KILO,
            'sram_size': 4 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F031x6',
            'dev_id': 0x444,
            'flash_size': 32 * _mem.KILO,
            'sram_size': 4 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F038x6',
            'dev_id': 0x444,
            'flash_size': 32 * _mem.KILO,
            'sram_size': 4 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, {
            'mcu_name': 'STM32F042x4',
            'dev_id': 0x445,
            'flash_size': 16 * _mem.KILO,
            'sram_size': 6 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x2.svd',
        }, {
            'mcu_name': 'STM32F042x6',
            'dev_id': 0x445,
            'flash_size': 32 * _mem.KILO,
            'sram_size': 6 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x2.svd',
        }, {
            'mcu_name': 'STM32F048x6',
            'dev_id': 0x445,
            'flash_size': 32 * _mem.KILO,
            'sram_size': 6 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, {
            'mcu_name': 'STM32F051x4',
            'dev_id': 0x440,
            'flash_size': 16 * _mem.KILO,
            'sram_size': 8 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F051x6',
            'dev_id': 0x440,
            'flash_size': 32 * _mem.KILO,
            'sram_size': 8 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F051x8',
            'dev_id': 0x440,
            'flash_size': 64 * _mem.KILO,
            'sram_size': 8 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F058x8',
            'dev_id': 0x440,
            'flash_size': 64 * _mem.KILO,
            'sram_size': 8 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, {
            'mcu_name': 'STM32F070x6',
            'dev_id': 0x445,
            'flash_size': 32 * _mem.KILO,
            'sram_size': 6 * _mem.KILO,
            'flash_page_sizes': 1024,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F070xB',
            'dev_id': 0x448,
            'flash_size': 128 * _mem.KILO,
            'sram_size': 16 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F071x8',
            'dev_id': 0x448,
            'flash_size': 64 * _mem.KILO,
            'sram_size': 16 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F071xB',
            'dev_id': 0x448,
            'flash_size': 128 * _mem.KILO,
            'sram_size': 16 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F072x8',
            'dev_id': 0x448,
            'flash_size': 64 * _mem.KILO,
            'sram_size': 16 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x2.svd',
        }, {
            'mcu_name': 'STM32F072xB',
            'dev_id': 0x448,
            'flash_size': 128 * _mem.KILO,
            'sram_size': 16 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x2.svd',
        }, {
            'mcu_name': 'STM32F078xB',
            'dev_id': 0x448,
            'flash_size': 128 * _mem.KILO,
            'sram_size': 16 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, {
            'mcu_name': 'STM32F091xB',
            'dev_id': 0x442,
            'flash_size': 128 * _mem.KILO,
            'sram_size': 32 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F091xC',
            'dev_id': 0x442,
            'flash_size': 256 * _mem.KILO,
            'sram_size': 32 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F098xC',
            'dev_id': 0x442,
            'flash_size': 256 * _mem.KILO,
            'sram_size': 32 * _mem.KILO,
            'flash_page_sizes': 2048,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, ]
