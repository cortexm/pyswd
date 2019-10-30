"""STM32F3xx"""

# import swd.io.stm32 as _io_stm32
import swd.targets.stm32 as _stm32


class Stm32f3(_stm32.Stm32):
    """STM32F3xx"""

    _CORE = "Cortex-M3"
    _FAMILY = "STM32F3"
    _IDCODE_REG = 0xe0042000
    _FLAS_SIZE_REG = 0x1ffff7cc
    _DEVICES = [
        {
            'part_no': 'STM32F301x6',
            'dev_id': 0x439,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F301x8',
            'dev_id': 0x439,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F302x6',
            'dev_id': 0x439,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F302x8',
            'dev_id': 0x439,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F302xB',
            'dev_id': 0x422,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F302xC',
            'dev_id': 0x422,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 40 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F302xD',
            'dev_id': 0x446,
            'flash_size': 384 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F302xE',
            'dev_id': 0x446,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F303x6',
            'dev_id': 0x438,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F303x8',
            'dev_id': 0x438,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F303xB',
            'dev_id': 0x422,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 40 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F303xC',
            'dev_id': 0x422,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 48 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F303xD',
            'dev_id': 0x446,
            'flash_size': 384 * _stm32.KILO,
            'sram_size': 80 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F303xE',
            'dev_id': 0x446,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 80 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F318x8',
            'dev_id': 0x439,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F328x8',
            'dev_id': 0x438,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F334x4',
            'dev_id': 0x438,
            'flash_size': 16 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F334x6',
            'dev_id': 0x438,
            'flash_size': 32 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F334x8',
            'dev_id': 0x438,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F358xC',
            'dev_id': 0x422,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 48 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F373x8',
            'dev_id': 0x432,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 16 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F373xB',
            'dev_id': 0x432,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 24 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F373xC',
            'dev_id': 0x432,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F378xC',
            'dev_id': 0x432,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, {
            'part_no': 'STM32F398xE',
            'dev_id': 0x446,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 80 * _stm32.KILO,
            'freq': 72,
            'flash_page_size': 2048,
        }, ]

    def __init__(self, cortexm, expected_devices=None):
        super().__init__(cortexm, expected_devices)
