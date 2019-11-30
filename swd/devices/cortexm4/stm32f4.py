"""STM32F4xx"""

import swd.devices.memory as _mem
import swd.devices.stm32 as _stm32


class Stm32f4(_stm32.Stm32):
    """STM32F4xx"""

    _NAME = "STM32F4"
    _IDCODE_REG = 0xe0042000
    _FLASH_SIZE_REG = 0x1fff7a22
    _MCUS = [
        {
            'mcu_name': 'STM32F401xB',
            'dev_id': 0x423,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 84,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F401.svd',
        }, {
            'mcu_name': 'STM32F401xC',
            'dev_id': 0x423,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 84,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F401.svd',
        }, {
            'mcu_name': 'STM32F401xD',
            'dev_id': 0x433,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 384 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }],
            'freq': 84,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F401.svd',
        }, {
            'mcu_name': 'STM32F401xE',
            'dev_id': 0x433,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 96 * _mem.KILO,
                }],
            'freq': 84,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F401.svd',
        }, {
            'mcu_name': 'STM32F405xE',
            'dev_id': 0x413,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 168,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F405.svd',
        }, {
            'mcu_name': 'STM32F405xG',
            'dev_id': 0x413,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 168,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F405.svd',
        }, {
            'mcu_name': 'STM32F407xE',
            'dev_id': 0x413,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 168,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F407.svd',
        }, {
            'mcu_name': 'STM32F407xG',
            'dev_id': 0x411,  # some devices has wrong DEV_ID
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 168,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F407.svd',
        }, {
            'mcu_name': 'STM32F407xG',
            'dev_id': 0x413,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 168,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F407.svd',
        }, {
            'mcu_name': 'STM32F410x8',
            'dev_id': 0x458,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F410.svd',
        }, {
            'mcu_name': 'STM32F410xB',
            'dev_id': 0x458,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F410.svd',
        }, {
            'mcu_name': 'STM32F411xC',
            'dev_id': 0x431,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 128 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F411.svd',
        }, {
            'mcu_name': 'STM32F411xE',
            'dev_id': 0x431,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 128 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F411.svd',
        }, {
            'mcu_name': 'STM32F412xE',
            'dev_id': 0x441,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 256 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F412.svd',
        }, {
            'mcu_name': 'STM32F412xG',
            'dev_id': 0x441,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 256 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F412.svd',
        }, {
            'mcu_name': 'STM32F413xG',
            'dev_id': 0x463,
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
                    'address': 0x20040000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F413.svd',
        }, {
            'mcu_name': 'STM32F413xH',
            'dev_id': 0x463,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1536 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x20040000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F413.svd',
        }, {
            'mcu_name': 'STM32F415xG',
            'dev_id': 0x413,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 168,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F405.svd',
        }, {
            'mcu_name': 'STM32F417xE',
            'dev_id': 0x413,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 168,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F407.svd',
        }, {
            'mcu_name': 'STM32F417xG',
            'dev_id': 0x413,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 168,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F407.svd',
        }, {
            'mcu_name': 'STM32F423xH',
            'dev_id': 0x463,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1536 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x20040000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 100,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F413.svd',
        }, {
            'mcu_name': 'STM32F427xG',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F427.svd',
        }, {
            'mcu_name': 'STM32F427xI',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 2048 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F427.svd',
        }, {
            'mcu_name': 'STM32F429xE',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F429.svd',
        }, {
            'mcu_name': 'STM32F429xG',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F429.svd',
        }, {
            'mcu_name': 'STM32F429xI',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 2048 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F429.svd',
        }, {
            'mcu_name': 'STM32F437xG',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F427.svd',
        }, {
            'mcu_name': 'STM32F437xI',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 2048 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F427.svd',
        }, {
            'mcu_name': 'STM32F439xG',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F429.svd',
        }, {
            'mcu_name': 'STM32F439xI',
            'dev_id': 0x419,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 2048 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20020000,
                    'size': 64 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F429.svd',
        }, {
            'mcu_name': 'STM32F446xC',
            'dev_id': 0x421,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 256 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F446.svd',
        }, {
            'mcu_name': 'STM32F446xE',
            'dev_id': 0x421,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 112 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x2001c000,
                    'size': 16 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F446.svd',
        }, {
            'mcu_name': 'STM32F469xE',
            'dev_id': 0x434,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 512 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 160 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x20028000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20030000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F469.svd',
        }, {
            'mcu_name': 'STM32F469xG',
            'dev_id': 0x434,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 160 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x20028000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20030000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F469.svd',
        }, {
            'mcu_name': 'STM32F469xI',
            'dev_id': 0x434,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 2048 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 160 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x20028000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20030000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F469.svd',
        }, {
            'mcu_name': 'STM32F479xG',
            'dev_id': 0x434,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 1024 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 160 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x20028000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20030000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F469.svd',
        }, {
            'mcu_name': 'STM32F479xI',
            'dev_id': 0x434,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 2048 * _mem.KILO,
                }, {
                    'name': 'SRAM1',
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 160 * _mem.KILO,
                }, {
                    'name': 'SRAM2',
                    'kind': 'SRAM',
                    'address': 0x20028000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SRAM3',
                    'kind': 'SRAM',
                    'address': 0x20030000,
                    'size': 128 * _mem.KILO,
                }, {
                    'name': 'CCM',
                    'kind': 'SRAM',
                    'address': 0x10000000,
                    'size': 64 * _mem.KILO,
                }],
            'freq': 180,
            'svd_file': 'svd/STM32F4_svd_V1.2/STM32F469.svd',
        }, ]
