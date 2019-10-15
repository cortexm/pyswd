"""STM32F3xx"""

# import swd.io.stm32 as _io_stm32
import swd.targets.stm32 as _stm32


class Stm32f4(_stm32.Stm32):
    """STM32F4xx"""

    _CORE = "Cortex-M4"
    _FAMILY = "STM32F4"
    _IDCODE_REG = 0xe0042000
    _FLAS_SIZE_REG = 0x1fff7a22
    _DEVICES = [
        {
            'part_no': 'STM32F401xB',
            'dev_id': 0x423,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 84,
        }, {
            'part_no': 'STM32F401xC',
            'dev_id': 0x423,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 64 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 84,
        }, {
            'part_no': 'STM32F401xD',
            'dev_id': 0x433,
            'flash_size': 384 * _stm32.KILO,
            'sram_size': 96 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 84,
        }, {
            'part_no': 'STM32F401xE',
            'dev_id': 0x433,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 96 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 84,
        }, {
            'part_no': 'STM32F405xE',
            'dev_id': 0x413,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 192 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 168,
        }, {
            'part_no': 'STM32F405xG',
            'dev_id': 0x413,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 192 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 168,
        }, {
            'part_no': 'STM32F407xE',
            'dev_id': 0x413,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 192 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 168,
        }, {
            'part_no': 'STM32F407xG',
            'dev_id': 0x411,  # some devices has wrong DEV_ID
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 192 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 168,
        }, {
            'part_no': 'STM32F407xG',
            'dev_id': 0x413,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 192 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 168,
        }, {
            'part_no': 'STM32F410x8',
            'dev_id': 0x458,
            'flash_size': 64 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F410xB',
            'dev_id': 0x458,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 32 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F411xC',
            'dev_id': 0x431,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F411xE',
            'dev_id': 0x431,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F412xE',
            'dev_id': 0x441,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F412xG',
            'dev_id': 0x441,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F413xG',
            'dev_id': 0x463,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 320 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F413xH',
            'dev_id': 0x463,
            'flash_size': 1536 * _stm32.KILO,
            'sram_size': 320 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F415xG',
            'dev_id': 0x413,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 192 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 168,
        }, {
            'part_no': 'STM32F417xE',
            'dev_id': 0x413,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 192 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 168,
        }, {
            'part_no': 'STM32F417xG',
            'dev_id': 0x413,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 192 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 168,
        }, {
            'part_no': 'STM32F423xH',
            'dev_id': 0x463,
            'flash_size': 1536 * _stm32.KILO,
            'sram_size': 320 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 100,
        }, {
            'part_no': 'STM32F427xG',
            'dev_id': 0x419,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F427xI',
            'dev_id': 0x419,
            'flash_size': 2048 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F429xE',
            'dev_id': 0x419,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F429xG',
            'dev_id': 0x419,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F429xI',
            'dev_id': 0x419,
            'flash_size': 2048 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F437xG',
            'dev_id': 0x419,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F437xI',
            'dev_id': 0x419,
            'flash_size': 2048 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F439xG',
            'dev_id': 0x419,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F439xI',
            'dev_id': 0x419,
            'flash_size': 2048 * _stm32.KILO,
            'sram_size': 256 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F446xC',
            'dev_id': 0x421,
            'flash_size': 256 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F446xE',
            'dev_id': 0x421,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 128 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F469xE',
            'dev_id': 0x434,
            'flash_size': 512 * _stm32.KILO,
            'sram_size': 384 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F469xG',
            'dev_id': 0x434,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 384 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F469xI',
            'dev_id': 0x434,
            'flash_size': 2048 * _stm32.KILO,
            'sram_size': 384 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F479xG',
            'dev_id': 0x434,
            'flash_size': 1024 * _stm32.KILO,
            'sram_size': 384 * _stm32.KILO,
            'eeprom_size': 0 * _stm32.KILO,
            'freq': 180,
        }, {
            'part_no': 'STM32F479xI',
            'dev_id': 0x434,
            'flash_size': 2048 * _stm32.KILO,
            'sram_size': 384 * _stm32.KILO,
            'eeprom_size': 0,
            'freq': 180,
        }, ]

    def __init__(self, cortexm, expected_devices=None):
        super().__init__(cortexm, expected_devices)
