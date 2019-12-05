"""STM32H7xx"""

import swd.devices.memory as _mem
import swd.devices.stm32 as _stm32


class Stm32h7(_stm32.Stm32):
    """STM32H7xx"""

    _NAME = "STM32H7"
    _IDCODE_REG = 0x5c001000
    _FLASH_SIZE_REG = 0x1ff1e880

    _OTP_128KB = {
        'name': "SYSTEM_MEMORY",
        'kind': "OTP",
        'address': 0x1FF00000,
        'size': 128 * _mem.KILO,
    }

    _FLASH1_128K = {
        'name': "FLASH1",
        'kind': "FLASH",
        'address': 0x08000000,
        'size': 128 * _mem.KILO,
        'sector_size': 128 * _mem.KILO,
    }
    _FLASH1_1M = {
        'name': "FLASH1",
        'kind': "FLASH",
        'address': 0x08000000,
        'size': 1024 * _mem.KILO,
        'sector_size': 128 * _mem.KILO,
    }
    _FLASH2_1M = {
        'name': "FLASH2",
        'kind': "FLASH",
        'address': 0x08100000,
        'size': 1024 * _mem.KILO,
        'sector_size': 128 * _mem.KILO,
    }

    _ITCM_64K = {
        'name': "ITCM",
        'kind': "SRAM",
        'address': 0x00000000,
        'size': 64 * _mem.KILO,
    }
    _DTCM_128K = {
        'name': "DTCM",
        'kind': "SRAM",
        'address': 0x20000000,
        'size': 128 * _mem.KILO,
    }
    _AXI_512K = {
        'name': "AXI",
        'kind': "SRAM",
        'address': 0x24000000,
        'size': 512 * _mem.KILO,
    }
    _SRAM1_128K = {
        'name': "SRAM1",
        'kind': "SRAM",
        'address': 0x30000000,
        'size': 128 * _mem.KILO,
    }
    _SRAM2_128K = {
        'name': "SRAM2",
        'kind': "SRAM",
        'address': 0x30020000,
        'size': 128 * _mem.KILO,
    }
    _SRAM3_32K = {
        'name': "SRAM3",
        'kind': "SRAM",
        'address': 0x30040000,
        'size': 32 * _mem.KILO,
    }
    _SRAM4_64K = {
        'name': "SRAM4",
        'kind': "SRAM",
        'address': 0x38000000,
        'size': 64 * _mem.KILO,
    }
    _BACKUP_4K = {
        'name': "BACKUP",
        'kind': "SRAM",
        'address': 0x38800000,
        'size': 4 * _mem.KILO,
    }

    _FLASH_128K_SRAM_1M = [
        _ITCM_64K,
        _FLASH1_128K,
        _OTP_128KB,
        _DTCM_128K,
        _AXI_512K,
        _SRAM1_128K,
        _SRAM2_128K,
        _SRAM3_32K,
        _SRAM4_64K,
        _BACKUP_4K,
    ]

    _FLASH_2M_SRAM_1M = [
        _ITCM_64K,
        _FLASH1_1M,
        _FLASH2_1M,
        _OTP_128KB,
        _DTCM_128K,
        _AXI_512K,
        _SRAM1_128K,
        _SRAM2_128K,
        _SRAM3_32K,
        _SRAM4_64K,
        _BACKUP_4K,
    ]

    _MCUS = [
        {
            'mcu_name': 'STM32H743xI',
            'dev_id': 0x450,
            'memory': _FLASH_2M_SRAM_1M,
            'freq': 480,
            'svd_file': 'svd/STM32H7_svd_V1.5/STM32H743x.svd',
        }, {
            'mcu_name': 'STM32H753xI',
            'dev_id': 0x450,
            'memory': _FLASH_2M_SRAM_1M,
            'freq': 480,
            'svd_file': 'svd/STM32H7_svd_V1.5/STM32H753x.svd',
        }, {
            'mcu_name': 'STM32H750xB',
            'dev_id': 0x450,
            'memory': _FLASH_128K_SRAM_1M,
            'freq': 480,
            'svd_file': 'svd/STM32H7_svd_V1.5/STM32H750x.svd',
        }, ]
