"""STM32F3xx"""

# import swd.io.stm32 as _io_stm32
import swd.devices.memory as _mem
import swd.devices.stm32 as _stm32


class Stm32f3(_stm32.Stm32):
    """STM32F3xx"""

    _NAME = "STM32F3"
    _IDCODE_REG = 0xe0042000
    _FLASH_SIZE_REG = 0x1ffff7cc
    _MCUS = [
        {
            'mcu_name': 'STM32F301x6',
            'dev_id': 0x439,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F301.svd',
        }, {
            'mcu_name': 'STM32F301x8',
            'dev_id': 0x439,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F301.svd',
        }, {
            'mcu_name': 'STM32F302x6',
            'dev_id': 0x439,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F302.svd',
        }, {
            'mcu_name': 'STM32F302x8',
            'dev_id': 0x439,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F302.svd',
        }, {
            'mcu_name': 'STM32F302xB',
            'dev_id': 0x422,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F302.svd',
        }, {
            'mcu_name': 'STM32F302xC',
            'dev_id': 0x422,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 40 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F302.svd',
        }, {
            'mcu_name': 'STM32F302xD',
            'dev_id': 0x446,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 384 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F302.svd',
        }, {
            'mcu_name': 'STM32F302xE',
            'dev_id': 0x446,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F302.svd',
        }, {
            'mcu_name': 'STM32F303x6',
            'dev_id': 0x438,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 12 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F303.svd',
        }, {
            'mcu_name': 'STM32F303x8',
            'dev_id': 0x438,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 12 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F303.svd',
        }, {
            'mcu_name': 'STM32F303xB',
            'dev_id': 0x422,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 40 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F303.svd',
        }, {
            'mcu_name': 'STM32F303xC',
            'dev_id': 0x422,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 40 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F303.svd',
        }, {
            'mcu_name': 'STM32F303xD',
            'dev_id': 0x446,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 384 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F303.svd',
        }, {
            'mcu_name': 'STM32F303xE',
            'dev_id': 0x446,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F303.svd',
        }, {
            'mcu_name': 'STM32F318x8',
            'dev_id': 0x439,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F3x8.svd',
        }, {
            'mcu_name': 'STM32F328x8',
            'dev_id': 0x438,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 12 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F3x8.svd',
        }, {
            'mcu_name': 'STM32F334x4',
            'dev_id': 0x438,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 16 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F3x4.svd',
        }, {
            'mcu_name': 'STM32F334x6',
            'dev_id': 0x438,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F3x4.svd',
        }, {
            'mcu_name': 'STM32F334x8',
            'dev_id': 0x438,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 4 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F3x4.svd',
        }, {
            'mcu_name': 'STM32F358xC',
            'dev_id': 0x422,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 40 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F3x8.svd',
        }, {
            'mcu_name': 'STM32F373x8',
            'dev_id': 0x432,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F373.svd',
        }, {
            'mcu_name': 'STM32F373xB',
            'dev_id': 0x432,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 24 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F373.svd',
        }, {
            'mcu_name': 'STM32F373xC',
            'dev_id': 0x432,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F373.svd',
        }, {
            'mcu_name': 'STM32F378xC',
            'dev_id': 0x432,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F3x8.svd',
        }, {
            'mcu_name': 'STM32F398xE',
            'dev_id': 0x446,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                    'page_size': 2048,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fffd800,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 72,
            'svd_file': 'svd/STM32F3_svd_V1.2/STM32F3x8.svd',
        }, ]
