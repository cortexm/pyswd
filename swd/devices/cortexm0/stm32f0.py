"""STM32F0xx"""

import swd.devices.memory as _mem
import swd.devices.stm32 as _stm32


class Stm32f0(_stm32.Stm32):
    """STM32F0xx"""

    _NAME = "STM32F0"
    _IDCODE_REG = 0x40015800
    _FLASH_SIZE_REG = 0x1ffff7cc
    _MCUS = [
        {
            'mcu_name': 'STM32F030x4',
            'dev_id': 0x444,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 16 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F030x6',
            'dev_id': 0x444,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F030x8',
            'dev_id': 0x440,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F030xC',
            'dev_id': 0x442,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F031x4',
            'dev_id': 0x444,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 16 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F031x6',
            'dev_id': 0x444,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F038x6',
            'dev_id': 0x444,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, {
            'mcu_name': 'STM32F042x4',
            'dev_id': 0x445,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 16 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc400,
                    'size': 13 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x2.svd',
        }, {
            'mcu_name': 'STM32F042x6',
            'dev_id': 0x445,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc400,
                    'size': 13 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x2.svd',
        }, {
            'mcu_name': 'STM32F048x6',
            'dev_id': 0x445,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc400,
                    'size': 13 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, {
            'mcu_name': 'STM32F051x4',
            'dev_id': 0x440,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 16 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F051x6',
            'dev_id': 0x440,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F051x8',
            'dev_id': 0x440,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F058x8',
            'dev_id': 0x440,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffec00,
                    'size': 3 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, {
            'mcu_name': 'STM32F070x6',
            'dev_id': 0x445,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_sizes': 1024,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc400,
                    'size': 13 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F070xB',
            'dev_id': 0x448,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc800,
                    'size': 12 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x0.svd',
        }, {
            'mcu_name': 'STM32F071x8',
            'dev_id': 0x448,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc800,
                    'size': 12 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F071xB',
            'dev_id': 0x448,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc800,
                    'size': 12 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F072x8',
            'dev_id': 0x448,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc800,
                    'size': 12 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x2.svd',
        }, {
            'mcu_name': 'STM32F072xB',
            'dev_id': 0x448,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc800,
                    'size': 12 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x2.svd',
        }, {
            'mcu_name': 'STM32F078xB',
            'dev_id': 0x448,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffc800,
                    'size': 12 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, {
            'mcu_name': 'STM32F091xB',
            'dev_id': 0x442,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F091xC',
            'dev_id': 0x442,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x1.svd',
        }, {
            'mcu_name': 'STM32F098xC',
            'dev_id': 0x442,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                    'page_sizes': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 48 * 1000 * 1000,
            'svd_file': 'svd/STM32F0_svd_V1.3/STM32F0x8.svd',
        }, ]
