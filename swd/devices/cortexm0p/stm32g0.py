"""STM32F0xx"""

import swd.devices.memory as _mem
import swd.devices.stm32 as _stm32


class Stm32g0(_stm32.Stm32):
    """STM32G0xx"""

    _NAME = "STM32G0"
    _IDCODE_REG = 0x40015800
    _FLASH_SIZE_REG = 0x1fff75e0
    _MCUS = [
        {
            'mcu_name': 'STM32G070x8',
            'dev_id': 0x460,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fff0000,
                    'size': 28 * _mem.KILO,
                }, {
                    'kind': 'OTP',
                    'address': 0x1fff7000,
                    'size': 1 * _mem.KILO,
                }],
            'freq': 64,
            'svd_file': 'svd/STM32G0_svd/STM32G070',
        }, {
            'mcu_name': 'STM32G070xB',
            'dev_id': 0x460,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 2 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fff0000,
                    'size': 28 * _mem.KILO,
                }, {
                    'kind': 'OTP',
                    'address': 0x1fff7000,
                    'size': 1 * _mem.KILO,
                }],
            'freq': 64,
            'svd_file': 'svd/STM32G0_svd/STM32G070',
        }, {
            'mcu_name': 'STM32G071x8',
            'dev_id': 0x460,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 64 * _mem.KILO,
                    'page_size': 2 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fff0000,
                    'size': 28 * _mem.KILO,
                }, {
                    'kind': 'OTP',
                    'address': 0x1fff7000,
                    'size': 1 * _mem.KILO,
                }],
            'freq': 64,
            'svd_file': 'svd/STM32G0_svd/STM32G071',
        }, {
            'mcu_name': 'STM32G071xB',
            'dev_id': 0x460,
            'memory': [
                {
                    'kind': 'FLASH',
                    'address': 0x08000000,
                    'size': 128 * _mem.KILO,
                    'page_size': 2 * _mem.KILO,
                }, {
                    'kind': 'SRAM',
                    'address': 0x20000000,
                    'size': 32 * _mem.KILO,
                }, {
                    'name': 'SYSTEM_MEMORY',
                    'kind': 'OTP',
                    'address': 0x1fff0000,
                    'size': 28 * _mem.KILO,
                }, {
                    'kind': 'OTP',
                    'address': 0x1fff7000,
                    'size': 1 * _mem.KILO,
                }],
            'freq': 64,
            'svd_file': 'svd/STM32G0_svd/STM32G071',
        }, ]
