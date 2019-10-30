"""STM32L4xx"""

# import swd.io.stm32 as _io_stm32
import swd.targets.stm32 as _stm32


class Stm32l4(_stm32.Stm32):
    """STM32L4xx"""

    _CORE = "Cortex-M4"
    _FAMILY = "STM32L4"
    _IDCODE_REG = 0xe0042000
    _FLAS_SIZE_REG = 0x1fff75e0
    _DEVICES = [
        {
            'part_no': 'STM32L431xB',
            'dev_id': 0x435,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L431xC',
            'dev_id': 0x435,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L432xB',
            'dev_id': 0x435,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L432xC',
            'dev_id': 0x435,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L433xB',
            'dev_id': 0x435,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L433xC',
            'dev_id': 0x435,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L442xC',
            'dev_id': 0x435,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L443xC',
            'dev_id': 0x435,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L451xC',
            'dev_id': 0x462,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 160 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L451xE',
            'dev_id': 0x462,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 160 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L452xC',
            'dev_id': 0x462,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 160 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L452xE',
            'dev_id': 0x462,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 160 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L462xE',
            'dev_id': 0x462,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 160 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L471xE',
            'dev_id': 0x415,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L471xG',
            'dev_id': 0x415,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L475xC',
            'dev_id': 0x415,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L475xE',
            'dev_id': 0x415,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L475xG',
            'dev_id': 0x415,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L476xC',
            'dev_id': 0x415,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L476xE',
            'dev_id': 0x415,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L476xG',
            'dev_id': 0x415,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L486xG',
            'dev_id': 0x415,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L496xE',
            'dev_id': 0x461,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 320 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L496xG',
            'dev_id': 0x461,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 320 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, {
            'part_no': 'STM32L4A6xG',
            'dev_id': 0x461,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 320 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 80,
            'flash_page_size': None,
        }, ]

    def __init__(self, cortexm, expected_devices=None):
        super().__init__(cortexm, expected_devices)
