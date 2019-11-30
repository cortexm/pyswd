"""STM32F0xx"""

import swd.devices.memory as _mem
import swd.devices.stm32 as _stm32


class Stm32l0(_stm32.Stm32):
    """STM32L0xx"""

    _NAME = "STM32L0"
    _IDCODE_REG = 0x40015800
    _FLASH_SIZE_REG = 0x1ff8007c
    _MCUS = [
        {
            'mcu_name': 'STM32L011x3',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 8 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 2 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 512,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L011x4',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 16 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 2 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 512,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L021x4',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 16 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 2 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 512,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L031x4',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 16 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 1 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L031x6',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 1 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L041x6',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 1 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L051x6',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 2 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L051x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 2 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L052x6',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 2 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x2.svd',
        }, {
            'mcu_name': 'STM32L052x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 2 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x2.svd',
        }, {
            'mcu_name': 'STM32L053x6',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 32 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 2 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, {
            'mcu_name': 'STM32L053x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 2 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, {
            'mcu_name': 'STM32L062x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 2 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x2.svd',
        }, {
            'mcu_name': 'STM32L063x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 8 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 2 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, {
            'mcu_name': 'STM32L071x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 3 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L071xB',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L071xZ',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 192 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L072x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 3 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x2.svd',
        }, {
            'mcu_name': 'STM32L072xB',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x2.svd',
        }, {
            'mcu_name': 'STM32L072xZ',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 192 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x2.svd',
        }, {
            'mcu_name': 'STM32L073x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 3 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, {
            'mcu_name': 'STM32L073xB',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, {
            'mcu_name': 'STM32L073xZ',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 192 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, {
            'mcu_name': 'STM32L081xB',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L081xZ',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 192 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x1.svd',
        }, {
            'mcu_name': 'STM32L082xB',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x2.svd',
        }, {
            'mcu_name': 'STM32L082xZ',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 192 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x2.svd',
        }, {
            'mcu_name': 'STM32L083x8',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 3 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, {
            'mcu_name': 'STM32L083xB',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, {
            'mcu_name': 'STM32L083xZ',
            'dev_id': 0x457,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 192 * _mem.KILO,
                    'page_size': 128,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 20 * _mem.KILO,
                }, {
                    'kind': 'EEPROM',
                    'address': 0x08080000,
                    'size': 6 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1ff00000,
                    'size': 8 * _mem.KILO,
                }],
            'freq': 32,
            'svd_file': 'svd/STM32L0_svd_V1.2/STM32L0x3.svd',
        }, ]
