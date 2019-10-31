"""STM32"""

import swd.io.stm32 as _io_stm32


KILO = 1024
MEGA = 1024 * KILO


class Stm32Exception(Exception):
    """General STM32 exception"""


class UnknownFamily(Stm32Exception):
    """Raised when expected device family is wrong"""


class UnknownDevice(Stm32Exception):
    """Raised when expected device family is wrong"""
    def __init__(self, dev_id=None, flash_size=None):
        error_string = "Unknown device"
        if dev_id:
            error_string += " with DEV_ID: 0x%03x" % dev_id
            if flash_size:
                flash_size //= KILO
                error_string += " and FLASH size: %d KB" % flash_size
        super().__init__(error_string)


class NoDeviceFound(Stm32Exception):
    """Raised when expected device(s) was not detected"""

    def __init__(self, detected_parts, expected_parts):
        error_string = "Device not found, detected: %s, expected: %s" % (
            ",".join(detected_parts),
            ",".join(expected_parts))
        super().__init__(error_string)


class Stm32:
    """STM32xxxx"""

    _CORE = None
    _FAMILY = None
    _IDCODE_REG = None
    _FLAS_SIZE_REG = None
    _FREQ = 48000000
    _FLASH_START_ADDRESS = 0x08000000
    _SRAM_START_ADDRESS = 0x20000000
    _DEVICES = []

    @staticmethod
    def _fix_part_name(part_name):
        """Return fixed part name

        Change character on 10 position to 'x'
        where is package size code"""
        if len(part_name) > 9:
            part_name = list(part_name)
            part_name[9] = 'x'
            part_name = ''.join(part_name)
        return part_name

    @classmethod
    def _fix_part_names(cls, part_names, family):
        """Return fixed part names

        Select only part names from this family.

        Change character on 10 position to 'x'
        where is package size code.

        Raise exception "UnknownFamily",
        when there are some part names
        but none is from this family."""
        if not part_names:
            return None
        fixed_names = set()
        for part_name in part_names:
            fixed_name = part_name.upper()
            if fixed_name.startswith(family):
                fixed_name = cls._fix_part_name(part_name)
                fixed_names.add(fixed_name)
        if not fixed_names:
            raise UnknownFamily()
        return fixed_names

    @staticmethod
    def _is_supposed_device(device, dev_id, flash_size):
        is_detected = device['dev_id'] == dev_id
        is_detected &= device['flash_size'] == flash_size
        return is_detected

    @staticmethod
    def _filter_devices_by_dev_id(devices, dev_id):
        """Select devices with specific DEV_ID"""
        supposed_devices = []
        for device in devices:
            if device['dev_id'] == dev_id:
                supposed_devices.append(device)
        return supposed_devices

    @staticmethod
    def _filter_devices_by_flash_size(devices, flash_size):
        """Select devices with specific FLASH size"""
        supposed_devices = []
        for device in devices:
            if device['flash_size'] == flash_size:
                supposed_devices.append(device)
        return supposed_devices

    @classmethod
    def _is_expected_part(cls, device, expected_parts):
        """Test if device contain expected part name"""
        if not expected_parts:
            return True
        for part_name in expected_parts:
            if device['part_no'].startswith(part_name):
                return True
        return False

    @staticmethod
    def _get_part_names(devices):
        """Return part names from devices"""
        part_names = set()
        for device in devices:
            part_names.add(device['part_no'])
        return part_names

    @classmethod
    def _filter_by_expected_parts(cls, supposed_devices, expected_parts):
        """Return selected devices

        select from supposed devices expected parts
        """
        selected_devices = []
        for device in supposed_devices:
            if cls._is_expected_part(device, expected_parts):
                selected_devices.append(device)
        if not selected_devices:
            raise NoDeviceFound(
                cls._get_part_names(supposed_devices), expected_parts)
        return selected_devices

    @classmethod
    def _find_devices(cls, dev_id, flash_size, expected_parts):
        expected_parts = cls._fix_part_names(expected_parts, cls._FAMILY)
        supposed_devices = cls._filter_devices_by_dev_id(
            cls._DEVICES, dev_id)
        if not supposed_devices:
            raise UnknownDevice(dev_id)
        supposed_devices = cls._filter_devices_by_flash_size(
            supposed_devices, flash_size)
        if not supposed_devices:
            raise UnknownDevice(dev_id, flash_size)
        if expected_parts:
            supposed_devices = cls._filter_by_expected_parts(
                supposed_devices, expected_parts)
        return supposed_devices

    def _create_idcode_reg(self):
        return _io_stm32.Idcode(self.swd, self._IDCODE_REG)

    def _create_flash_size_reg(self):
        return _io_stm32.FlashSize(self.swd, self._FLAS_SIZE_REG)

    def __init__(self, cortexm, expected_parts=None):
        self._cortexm = cortexm
        idcode_reg = self._create_idcode_reg()
        self._dev_id = idcode_reg.cached.value('DEV_ID')
        flash_size_reg = self._create_flash_size_reg()
        self._flash_size = flash_size_reg.cached.value('FLASH_SIZE') * KILO
        self._supposed_devices = self._find_devices(
            self._dev_id,
            self._flash_size,
            expected_parts)
        self._sram_sizes = {dev['sram_size'] for dev in self._supposed_devices}
        self.swd.append_io({
            idcode_reg,
            flash_size_reg,
        })
        self._memory_regions = [
            {
                'type': 'FLASH',
                'name': 'FLASH',
                'start': self._FLASH_START_ADDRESS,
                'size': self.get_flash_size(),
            }, {
                'type': 'SRAM',
                'name': 'SRAM',
                'start': self._SRAM_START_ADDRESS,
                'size': self.get_sram_size(),
            }
        ]

        # for memory_region in self.get_memory_regions():
        #     print(memory_region)
        # print("STM32: FLASH_SIZE: %d KB" % (self.get_flash_size() // KILO))
        # print("STM32: SRAM_SIZE: %d KB" % (self.get_sram_size() // KILO))

    @property
    def cortexm(self):
        """Instance of CortexM"""
        return self._cortexm

    @property
    def swd(self):
        """Instance of Swd"""
        return self._cortexm.swd

    @classmethod
    def get_family(cls):
        """Return devices family"""
        return cls._FAMILY

    def get_part_names(self):
        """Return list of supposed part names"""
        return [dev['part_no'] for dev in self._supposed_devices]

    def get_revision(self):
        """Return revision string"""
        revision = "%d.%d" % (
            self.swd.reg('IDCODE').cached.get('REV_ID_MAJOR'),
            self.swd.reg('IDCODE').cached.get('REV_ID_MINOR'))
        return revision

    def get_flash_size(self):
        """Return FLASH size"""
        return self._flash_size

    def get_sram_size(self):
        """Return minimal SRAM size"""
        return min(self._sram_sizes)

    @staticmethod
    def _compare_memory_region(memory_region, filter_):
        for filter_key, filter_value in filter_.items():
            if memory_region[filter_key] != filter_value.upper():
                return False
        return True

    def get_memory_regions(self, filter_=None):
        """Return all regions"""
        if filter_ is None:
            return self._memory_regions
        memory_regions = []
        for memory_region in self._memory_regions:
            if self._compare_memory_region(memory_region, filter_):
                memory_regions.append(memory_region)
        return memory_regions

    def erase_flash(self, bank=None, sector=None):
        """Erase Flash"""
        # raise Stm32Exception("Erasing is not implemented")
