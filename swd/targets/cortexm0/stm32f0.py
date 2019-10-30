"""STM32F0xx"""

import swd.targets.stm32 as _stm32


class Stm32f0(_stm32.Stm32):
    """STM32F0xx"""

    _CORE = "Cortex-M0"
    _FAMILY = "STM32F0"
    _IDCODE_REG = 0x40015800
    _FLAS_SIZE_REG = 0x1ffff7cc
    _FREQ = 48000000
    _DEVICES = [
        {
            'part_no': 'STM32F030x4',
            'dev_id': 0x444,
            'flash_size': 16 * _stm32.KILO,
            'sram_size': 4 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F030x6',
            'dev_id': 0x444,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 4 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F030x8',
            'dev_id': 0x440,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 8 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F030xC',
            'dev_id': 0x442,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F031x4',
            'dev_id': 0x444,
            'flash_size': 16 * _stm32.KILO,
            'sram_size': 4 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F031x6',
            'dev_id': 0x444,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 4 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F038x6',
            'dev_id': 0x444,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 4 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F042x4',
            'dev_id': 0x445,
            'flash_size': 16 * _stm32.KILO,
            'sram_size': 6 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F042x6',
            'dev_id': 0x445,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 6 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F048x6',
            'dev_id': 0x445,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 6 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F051x4',
            'dev_id': 0x440,
            'flash_size': 16 * _stm32.KILO,
            'sram_size': 8 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F051x6',
            'dev_id': 0x440,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 8 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F051x8',
            'dev_id': 0x440,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 8 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F058x8',
            'dev_id': 0x440,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 8 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F070x6',
            'dev_id': 0x445,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 6 * _stm32.KILO,
            'erase_sizes': 1024,
        }, {
            'part_no': 'STM32F070xB',
            'dev_id': 0x448,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F071x8',
            'dev_id': 0x448,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F071xB',
            'dev_id': 0x448,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F072x8',
            'dev_id': 0x448,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F072xB',
            'dev_id': 0x448,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F078xB',
            'dev_id': 0x448,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F091xB',
            'dev_id': 0x442,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F091xC',
            'dev_id': 0x442,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'erase_sizes': 2048,
        }, {
            'part_no': 'STM32F098xC',
            'dev_id': 0x442,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'erase_sizes': 2048,
        }, ]

    def __init__(self, cortexm, expected_devices=None):
        super().__init__(cortexm, expected_devices)
