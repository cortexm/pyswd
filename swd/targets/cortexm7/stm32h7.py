"""STM32H7xx"""

# import swd.io.stm32 as _io_stm32
import swd.targets.stm32 as _stm32


class Stm32h7(_stm32.Stm32):
    """STM32H7xx"""

    _CORE = "Cortex-M7"
    _FAMILY = "STM32H7"
    _IDCODE_REG = 0x5c001000
    _FLAS_SIZE_REG = 0x1ff1e880
    _FLASH_2M = [
        {
            'name': "BANK1",
            'start_address': 0x08000000,
            'size': 1024 * _stm32.KILO,
            'sector_size': 128 * _stm32.KILO,
        }, {
            'name': "BANK2",
            'start_address': 0x08100000,
            'size': 1024 * _stm32.KILO,
            'sector_size': 128 * _stm32.KILO,
        }
    ]
    _FLASH_128K = [
        {
            'name': "BANK1",
            'start_address': 0x08000000,
            'size': 128 * _stm32.KILO,
            'sector_size': 128 * _stm32.KILO,
        }
    ]
    _DEVICES = [
        {
            'part_no': 'STM32H743xI',
            'dev_id': 0x450,
            'flash_size': 2048 * _stm32.KILO,
            'sram_size': 1024 * _stm32.KILO,
            'flash': _FLASH_2M,
            'freq': 480,
        }, {
            'part_no': 'STM32H753xI',
            'dev_id': 0x450,
            'flash_size': 2048 * _stm32.KILO,
            'sram_size': 1024 * _stm32.KILO,
            'flash': _FLASH_2M,
            'freq': 480,
        }, {
            'part_no': 'STM32H750xB',
            'dev_id': 0x450,
            'flash_size': 128 * _stm32.KILO,
            'sram_size': 1024 * _stm32.KILO,
            'flash': _FLASH_128K,
            'freq': 480,
        }, ]

    def __init__(self, cortexm, expected_devices=None):
        super().__init__(cortexm, expected_devices)
