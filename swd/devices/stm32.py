"""STM32"""

import swd.devices.memory as _memory
import swd.devices.mcu as _mcu

import pkg_resources as _pkg


class UnknownMcuDetected(_mcu.UnknownMcuDetected):
    """Raised when MCU is not detected"""
    def __init__(self, dev_id, flash_size=None):
        msg = f"Unknown MCU with DEV_ID: {dev_id:03x}"
        if flash_size:
            msg += f" with FLASH: {flash_size // _memory.KILO} KB"
        super().__init__(msg)


class McuNotMatch(_mcu.McuNotMatch):
    """Raised when expected MCU(s) was not detected"""
    def __init__(self, detected_mcu_names, expected_mcu_names):
        detected = "/".join(name for name in detected_mcu_names)
        expected = "/".join(name for name in expected_mcu_names)
        msg = f"Detected MCU: {detected}, but expected: {expected}."
        super().__init__(msg)


class Stm32(_mcu.Mcu):
    """STM32xxxx"""

    _NAME = "STM32"
    _IDCODE_REG = None
    _FLAS_SIZE_REG = None
    _FREQ = None
    _FLASH_START_ADDRESS = 0x08000000
    _SRAM_START_ADDRESS = 0x20000000
    _MCUS = []

    def __init__(self, cortexm, expected_mcus=None):
        super().__init__(cortexm, expected_mcus)
        # browse MCUs by DEV_ID
        dev_id = self._load_devid_from_idcode(self._IDCODE_REG)
        mcus = self._select_mcus(self._MCUS, dev_id=dev_id)
        if not mcus:
            raise UnknownMcuDetected(dev_id)
        # browse MCUs by FLASH_SIZE
        flash_size_reg_addr = self._FLAS_SIZE_REG
        if not flash_size_reg_addr:
            flash_size_reg_addr = self._mcu_value(mcus, 'flash_size_reg')
        flash_size = self._load_flash_size(flash_size_reg_addr) * _memory.KILO
        mcus = self._select_mcus(mcus, flash_size=flash_size)
        if not mcus:
            raise UnknownMcuDetected(dev_id, flash_size)
        if expected_mcus:
            selected_mcus = self._select_mcus_by_expected(mcus, expected_mcus)
            if not selected_mcus:
                raise McuNotMatch(
                    self._get_mcu_names(mcus), expected_mcus)
            mcus = selected_mcus
        self._mcus = mcus
        self._flash_size = flash_size
        self._sram_sizes = {mcu['sram_size'] for mcu in mcus}
        # self._memory_regions = [
        #     {
        #         'type': 'FLASH',
        #         'name': 'FLASH',
        #         'start': self._FLASH_START_ADDRESS,
        #         'size': self.get_flash_size(),
        #     }, {
        #         'type': 'SRAM',
        #         'name': 'SRAM',
        #         'start': self._SRAM_START_ADDRESS,
        #         'size': self.get_sram_size(),
        #     }
        # ]
        # for memory_region in self.get_memory_regions():
        #     print(memory_region)
        # print("STM32: FLASH_SIZE: %d KB" % (self.get_flash_size() // KILO))
        # print("STM32: SRAM_SIZE: %d KB" % (self.get_sram_size() // KILO))

    def _load_devid_from_idcode(self, address):
        idcode = self.swd.get_mem32(address)
        return idcode & 0x00000fff

    def _load_flash_size(self, address):
        return self.swd.get_mem16(address)

    @staticmethod
    def _select_mcus(mcus, **arguments):
        """Select mcus by arguments (key=value)

        Arguments:
            mcus: input list of mcus structures
            arguments: dev_id
        """
        selected_mcus = []
        for mcu in mcus:
            for key, value in arguments.items():
                if mcu[key] == value:
                    selected_mcus.append(mcu)
        return selected_mcus

    @staticmethod
    def _mcu_values(mcus, key):
        """Return values from all mcus

        Arguments:
            mcus: input list of MCU structures
            key: key from values
        """
        return {mcu[key] for mcu in mcus if key in mcu}

    @classmethod
    def _mcu_value(cls, mcus, key):
        """Return values from all mcus

        Arguments:
            mcus: input list of MCU structures
            key: key from values

        Returns:
            only one common value
            if more values found then Exception is raised
        """
        values = cls._mcu_values(mcus, key)
        if len(values) > 1:
            raise _mcu.McuError("Error, more values in MCUs under key")
        return values.pop()

    @classmethod
    def _is_expected_mcu(cls, mcu, expected_mcus):
        """Test if mcu contain expected MCU name"""
        if not expected_mcus:
            return True
        for mcu_name in expected_mcus:
            if mcu['mcu_name'].startswith(mcu_name):
                return True
        return False

    @classmethod
    def _select_mcus_by_expected(cls, mcus, expected_mcus):
        """Return selected MCUs

        select from detected expected MCUs
        """
        expected_mcus_fixed = cls._fix_mcu_names(expected_mcus)
        selected_mcus = []
        if expected_mcus_fixed:
            for mcu in mcus:
                if cls._is_expected_mcu(mcu, expected_mcus_fixed):
                    selected_mcus.append(mcu)
        return selected_mcus

    @staticmethod
    def _fix_mcu_name(mcu_name):
        """Return fixed MCU name

        Change character on 10 position to 'x'
        where is package size code"""
        if len(mcu_name) > 9:
            mcu_name = list(mcu_name)
            mcu_name[9] = 'x'
            mcu_name = ''.join(mcu_name)
        return mcu_name

    @classmethod
    def _fix_mcu_names(cls, mcu_names):
        """Return fixed MCU names

        Select only MCU names from this family.

        Change character on 10 position to 'x'
        where is package size code.


        Arguments:
            mcu_names: list of MCU names

        Returns:
            list of fixed MCU names
        """
        if not mcu_names:
            return None
        fixed_names = set()
        for mcu_name in mcu_names:
            fixed_name = mcu_name.upper()
            if fixed_name.startswith(cls._NAME[:len(fixed_name)]):
                fixed_name = cls._fix_mcu_name(mcu_name)
                fixed_names.add(fixed_name)
        return fixed_names


    @property
    def cortexm(self):
        """Instance of CortexM"""
        return self._cortexm

    @property
    def swd(self):
        """Instance of Swd"""
        return self._cortexm.swd

    @classmethod
    def get_family_name(cls):
        """Return MCUs family"""
        return cls._NAME

    @staticmethod
    def _get_mcu_names(mcus):
        return [mcu['mcu_name'] for mcu in mcus]

    def get_mcu_name(self):
        """Return list of supposed MCU names"""
        return " / ".join(self._get_mcu_names(self._mcus))

    def load_svd(self):
        svd_files = self._mcu_values(self._mcus, 'svd_file')
        if len(svd_files) == 1:
            svd_file = _pkg.resource_filename('swd', svd_files.pop())
            self.swd.load_svd(svd_file)
        elif len(svd_files) > 1:
            raise _mcu.McuException("Specify MCU to load SVD file")

