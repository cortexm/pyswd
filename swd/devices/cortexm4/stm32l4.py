"""STM32L4xx"""

import swd.devices.memory as _mem
import swd.devices.stm32 as _stm32


class Stm32l4(_stm32.Stm32):
    """STM32L4xx"""

    _NAME = "STM32L4"
    _IDCODE_REG = 0xe0042000
    _FLASH_SIZE_REG = 0x1fff75e0
    _MCUS = [
        {
            'mcu_name': 'STM32L431xB',
            'dev_id': 0x435,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 48 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x1.svd',
        }, {
            'mcu_name': 'STM32L431xC',
            'dev_id': 0x435,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 48 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x1.svd',
        }, {
            'mcu_name': 'STM32L432xB',
            'dev_id': 0x435,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 48 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x2.svd',
        }, {
            'mcu_name': 'STM32L432xC',
            'dev_id': 0x435,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 48 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x2.svd',
        }, {
            'mcu_name': 'STM32L433xB',
            'dev_id': 0x435,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 48 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x3.svd',
        }, {
            'mcu_name': 'STM32L433xC',
            'dev_id': 0x435,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 48 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x3.svd',
        }, {
            'mcu_name': 'STM32L442xC',
            'dev_id': 0x435,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 48 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x2.svd',
        }, {
            'mcu_name': 'STM32L443xC',
            'dev_id': 0x435,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 48 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x3.svd',
        }, {
            'mcu_name': 'STM32L451xC',
            'dev_id': 0x462,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x1.svd',
        }, {
            'mcu_name': 'STM32L451xE',
            'dev_id': 0x462,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x1.svd',
        }, {
            'mcu_name': 'STM32L452xC',
            'dev_id': 0x462,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x2.svd',
        }, {
            'mcu_name': 'STM32L452xE',
            'dev_id': 0x462,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x2.svd',
        }, {
            'mcu_name': 'STM32L462xE',
            'dev_id': 0x462,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x2.svd',
        }, {
            'mcu_name': 'STM32L471xE',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x1.svd',
        }, {
            'mcu_name': 'STM32L471xG',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x1.svd',
        }, {
            'mcu_name': 'STM32L475xC',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x5.svd',
        }, {
            'mcu_name': 'STM32L475xE',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x5.svd',
        }, {
            'mcu_name': 'STM32L475xG',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x5.svd',
        }, {
            'mcu_name': 'STM32L476xC',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x6.svd',
        }, {
            'mcu_name': 'STM32L476xE',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x6.svd',
        }, {
            'mcu_name': 'STM32L476xG',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x6.svd',
        }, {
            'mcu_name': 'STM32L486xG',
            'dev_id': 0x415,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x6.svd',
        }, {
            'mcu_name': 'STM32L496xE',
            'dev_id': 0x461,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x6.svd',
        }, {
            'mcu_name': 'STM32L496xG',
            'dev_id': 0x461,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x6.svd',
        }, {
            'mcu_name': 'STM32L4A6xG',
            'dev_id': 0x461,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 80,
            'flash_page_size': None,
            'svd_file': 'svd/STM32L4_svd_V1.2/STM32L4x6.svd',
        }, ]
