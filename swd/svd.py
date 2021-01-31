"""SVD (System View Description) file parser"""

import sys as _sys
import string as _string
import xml.etree.ElementTree as _et


class SvdException(Exception):
    """SVD Exception"""


class _Element:
    def __init__(self):
        self._name = None
        self._description = None

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def copy(self, source):
        self._name = source.name
        self._description = source.description

    def parse(self, element):
        for sub_element in element:
            if sub_element.tag == 'name':
                name = sub_element.text.upper()
                name = name.replace('[', '').replace(']', '')
                if not set(name).issubset(
                        _string.ascii_uppercase + _string.digits + '_'):
                    raise SvdException(f'wrong name: "{name}"')
                self._name = name
            elif sub_element.tag == 'description':
                description = sub_element.text
                self._description = " ".join(description.split())
            else:
                self._parse(sub_element)

    def _parse(self, element):
        """Virtual"""

    def validate(self):
        if self._name is None:
            raise SvdException("name is not set")
        if self._description is None:
            raise SvdException("description is not set")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"


class EnumeratedValue(_Element):
    def __init__(self, field):
        super().__init__()
        self._field = field
        self._value = None

    @property
    def value(self):
        if self._field.mask == 1:
            return bool(self._value)
        return self._value

    def copy(self, source):
        super().copy(source)
        self._value = source.value

    def _parse(self, element):
        if element.tag == 'value':
            self._value = int(element.text, 0)

    def validate(self):
        # name and description are optional
        if self._value is None:
            raise SvdException("EnumeratedValue/value is not set")

    def __str__(self):
        common = super().__str__()
        if self._field.mask <= 7:
            return f"{common}: {self.value}"
        digits = (self._field.width + 3) // 4
        return f"{common}: 0x{self.value:0{digits}x}"


class Field(_Element):
    def __init__(self, register):
        super().__init__()
        self._register = register
        self._offset = None
        self._width = None
        self._mask = None
        self._mask_off = None
        self._mask_inv = None
        self._enumerated_values = []
        self._allow_read = None
        self._allow_write = None

    @property
    def register(self):
        return self._register

    @property
    def offset(self):
        return self._offset

    @property
    def width(self):
        return self._width

    @property
    def mask(self):
        if self._mask is None:
            self._mask = 2 ** self._width - 1
        return self._mask

    @property
    def mask_offset(self):
        if self._mask_off is None:
            self._mask_off = self._mask << self._offset
        return self._mask_off

    @property
    def mask_inverted(self):
        if self._mask_inv is None:
            self._mask_inv = self._mask_off ^ self._register.mask
        return self._mask_inv

    @property
    def allow_read(self):
        return self._allow_read

    @property
    def allow_write(self):
        return self._allow_write

    @property
    def numeric_value(self):
        """read value from register"""
        return (self._register.value >> self._offset) & self.mask

    @property
    def value(self):
        value = self.numeric_value
        if self.mask == 1:
            value = bool(value)
        return value

    @property
    def named_value(self):
        value = self.numeric_value
        for enumerated_value in self._enumerated_values:
            if value == enumerated_value.value:
                if enumerated_value.name:
                    return enumerated_value.name
        if self.mask == 1:
            value = bool(value)
        return value

    @property
    def str_value(self):
        value = self.numeric_value
        for enumerated_value in self._enumerated_values:
            if value == enumerated_value.value:
                if enumerated_value.name:
                    return enumerated_value.name
        if self.mask == 1:
            value = f"{bool(value)}"
        elif self.mask < 10:
            value = f"{value}"
        else:
            value = f"0x{value:0{(self.width + 3) // 4}x}"
        return value

    def _convert_value(self, value):
        if isinstance(value, int):
            pass
        elif isinstance(value, bool):
            value = int(value)
        elif isinstance(value, bytes):
            value = int.from_bytes(value, byteorder='little')
        elif isinstance(value, str) and len(value) == 1:
            value = ord(value)
        elif isinstance(value, str):
            value = self._enumerated_value(value).value
        else:
            raise SvdException("Value can be int, bool, char, bytes")
        if value > self.mask:
            raise SvdException("Value can't fit into field")
        return value

    @value.setter
    def value(self, value):
        """write value into register

        Uses read-modify-write method to update bits

        Arguments:
            value: value to store into register
        """
        value = self._convert_value(value)
        if self.mask_offset == self._register.mask:
            # direct write
            self._register.value = value
        else:
            # read-modify-write
            reg_value = self._register.value & self.mask_inverted
            self._register.value = reg_value | (value << self._offset)

    @property
    def enumerated_values(self):
        return self._enumerated_values

    def _enumerated_value(self, name):
        name = name.upper()
        for enumerated_value in self._enumerated_values:
            if name == enumerated_value.name.upper():
                return enumerated_value
        raise SvdException(f"EnumeratedValue name '{name}' not found.")

    def copy(self, source):
        super().copy(source)
        self._offset = source.offset
        self._width = source.width

    def _parse(self, element):
        if element.tag == 'bitOffset':
            self._offset = int(element.text, 0)
        elif element.tag == 'bitWidth':
            self._width = int(element.text, 0)
        elif element.tag == 'bitRange':
            bit_range = element.text
            if bit_range[0] == '[' and bit_range[-1] == ']':
                last, first = bit_range[1:-1].split(':')
                first = int(first, 0)
                last = int(last, 0)
                self._offset = first
                self._width = (last - first) + 1
        elif element.tag == 'access':
            if element.text == 'write-only':
                self._allow_read = False
                self._allow_write = True
            elif element.text == 'read-write':
                self._allow_read = True
                self._allow_write = True
            elif element.text == 'read-only':
                self._allow_read = True
                self._allow_write = False
            else:
                raise SvdException(f"Unknown access: '{element.text}'")
        elif element.tag == 'enumeratedValues':
            for sub_element in element:
                if sub_element.tag == 'enumeratedValue':
                    enumerated_value = EnumeratedValue(self)
                    enumerated_value.parse(sub_element)
                    self._enumerated_values.append(enumerated_value)

    def validate(self):
        super().validate()
        if self._offset is None:
            raise SvdException("field/offset is not set")
        if self._width is None:
            raise SvdException("field/bit_widht is not set")

    def __str__(self):
        common = super().__str__()
        offset = self._offset
        width = self._width
        return f"{common}: {offset:d}:{width:d}"


class Register(_Element):
    def __init__(self, peripheral):
        super().__init__()
        self._peripheral = peripheral
        self._offset = None
        self._size = peripheral.size
        self._mask = None
        self._value = None
        self._fields = []

    @property
    def peripheral(self):
        return self._peripheral

    @property
    def offset(self):
        return self._offset

    @property
    def address(self):
        return self._peripheral.base_address + self._offset

    @property
    def size(self):
        return self._size

    @property
    def size_bytes(self):
        return self._size // 8

    @property
    def mask(self):
        if self._mask is None:
            self._mask = 2 ** self._size - 1
        return self._mask

    @property
    def fields(self):
        return self._fields

    def field(self, name):
        name = name.upper()
        for field in self._fields:
            if field.name == name:
                return field
        return None

    @property
    def value(self):
        """Property to read value value"""
        return self._value

    @value.setter
    def value(self, value):
        """Property to set value value"""
        self._value = value

    def copy(self, source):
        super().copy(source)
        self._offset = source.offset
        self._size = source.size
        for field in source.fields:
            new_field = Field(self)
            new_field.copy(field)
            self._fields.append(new_field)
            setattr(self, field.name, field)

    def _parse(self, element):
        if element.tag == 'addressOffset':
            self._offset = int(element.text, 0)
        if element.tag == 'size':
            self._size = int(element.text, 0)
        elif element.tag == 'fields':
            fields = []
            for sub_element in element:
                if sub_element.tag == 'field':
                    field = Field(self)
                    field.parse(sub_element)
                    fields.append(field)
                    setattr(self, field.name, field)
            self._fields = sorted(fields, key=lambda field: field.offset)

    def validate(self):
        super().validate()
        if self._offset is None:
            raise SvdException("register/offset is not set")
        if self.size is None:
            raise SvdException("register/size is not set")
        for field in self._fields:
            field.validate()

    def __str__(self):
        common = super().__str__()
        offset = self._offset
        return f"{common}: +0x{offset:04x}"


class MemRegister(Register):
    def __init__(self, peripheral):
        super().__init__(peripheral)
        self._mem_drv = peripheral.device.mem_drv
        self._cache = Register(peripheral)

    @property
    def value(self):  # override
        if self.address % 4 == 0 and self.size == 32:
            return self._mem_drv.get_mem32(self.address)
        # if self.address % 2 == 0 and self.size == 16:
        #     return self._mem_drv.get_mem16(self.address)
        data = self._mem_drv.read_mem(self.address, self.size_bytes)
        return int.from_bytes(data, byteorder='little')

    @value.setter
    def value(self, value):  # override
        """Write value value to memory"""
        if self.address % 4 == 0 and self.size == 32:
            self._mem_drv.set_mem32(self.address, value)
        else:
            data = value.to_bytes(self.size_bytes, byteorder='little')
            self._mem_drv.write_mem(self.address, data)

    @property
    def cached(self):
        """Access cached memory register and load current value on invalid"""
        if self._cache.value is None:
            self._cache.value = self.value
        return self._cache

    @property
    def cache(self):
        """Access cached memory register"""
        return self._cache

    def discard_cache(self):
        """Discard content of cache"""
        self._cache.value = None

    def write_cache(self):
        """Write cache to memory register"""
        if self._cache.value is None:
            raise SvdException('Cache is not valid')
        self.value = self._cache.value

    def copy(self, source):
        super().copy(source)
        self._cache.copy(source.cache)

    def parse(self, element):
        super().parse(element)
        self._cache.parse(element)


class Interrupt(_Element):
    def __init__(self, peripheral):
        super().__init__()
        self._peripherals = [peripheral]
        self._vector = None

    def add_peripheral(self, peripheral):
        for per in self._peripherals:
            if per.name == peripheral.name:
                return
        self._peripherals.append(peripheral)

    @property
    def peripherals(self):
        return self._peripherals

    @property
    def vector(self):
        return self._vector

    def copy(self, source):
        raise SvdException("can't copy INTERRUPT")

    def _parse(self, element):
        if element.tag == 'value':
            self._vector = int(element.text, 0)

    def validate(self):
        super().validate()
        if self._vector is None:
            raise SvdException("vector is not set")

    def __str__(self):
        common = super().__str__()
        return f"{common}: {self._vector}"


class Peripheral(_Element):
    def __init__(self, device):
        super().__init__()
        self._device = device
        self._base_address = None
        self._size = device.size
        self._registers = []

    @property
    def device(self):
        return self._device

    @property
    def base_address(self):
        return self._base_address

    @property
    def size(self):
        return self._size

    @property
    def registers(self):
        return self._registers

    def register(self, name):
        name = name.upper()
        for register in self._registers:
            if register.name == name:
                return register
        return None

    def copy(self, source):
        super().copy(source)
        self._base_address = source.base_address
        self._size = source.size
        for source_register in source.registers:
            if self.device.mem_drv is None:
                register = Register(self)
            else:
                register = MemRegister(self)
            register.copy(source_register)
            self._registers.append(register)
            setattr(self, register.name, register)

    def _parse(self, element):
        if element.tag == 'baseAddress':
            self._base_address = int(element.text, 0)
        if element.tag == 'size':
            self._size = int(element.text, 0)
        if element.tag == 'interrupt':
            interrupt = Interrupt(self)
            interrupt.parse(element)
            self.device.add_interrupt(self, interrupt)
        elif element.tag == 'registers':
            registers = []
            for sub_element in element:
                if sub_element.tag == 'register':
                    if self.device.mem_drv is None:
                        register = Register(self)
                    else:
                        register = MemRegister(self)
                    register.parse(sub_element)
                    registers.append(register)
                    setattr(self, register.name, register)
            self._registers = sorted(registers, key=lambda register: register.offset)

    def validate(self):
        super().validate()
        if self._base_address is None:
            raise SvdException("peripheral/base_address is not set")
        if self.size is None:
            raise SvdException("peripheral/size is not set")
        for register in self._registers:
            register.validate()

    def __str__(self):
        common = super().__str__()
        base_address = self._base_address
        return f"{common}: 0x{base_address:08x}"


class Cpu(_Element):
    def __init__(self):
        super().__init__()
        self._revision = None
        self._endian = None
        self._mpu_present = None
        self._fpu_present = None
        self._nvic_prio_bits = None
        self._vendor_systick_config = None

    @property
    def revision(self):
        return self._revision

    @property
    def endian(self):
        return self._endian

    @property
    def mpu_present(self):
        return self._mpu_present

    @property
    def fpu_present(self):
        return self._fpu_present

    @property
    def nvic_prio_bits(self):
        return self._nvic_prio_bits

    @property
    def vendor_systick_config(self):
        return self._vendor_systick_config

    def copy(self, source):
        raise SvdException("can't copy CPU")

    def _parse(self, element):
        if element.tag == 'revision':
            self._revision = element.text
        if element.tag == 'endian':
            self._endian = element.text
        if element.tag == 'mpuPresent':
            self._mpu_present = element.text.lower() in ('true', '1')
        if element.tag == 'fpuPresent':
            self._fpu_present = element.text.lower() in ('true', '1')
        if element.tag == 'nvicPrioBits':
            self._nvic_prio_bits = int(element.text, 0)
        if element.tag == 'vendorSystickConfig':
            self._vendor_systick_config = element.text.lower() in ('true', '1')

    def validate(self):
        # no super called, cpu has no description
        if self._name is None:
            raise SvdException("cpu is not set")


class Svd(_Element):
    def __init__(self, mem_drv=None):
        super().__init__()
        self._mem_drv = mem_drv
        self._size = None
        self._width = None
        self._peripherals = []
        self._cpu = None
        self._interrupts = []

    def parse_svd(self, svd_file):
        device_element = _et.parse(svd_file).getroot()
        self.parse(device_element)

    @property
    def mem_drv(self):
        return self._mem_drv

    @property
    def cpu(self):
        return self._cpu

    @property
    def size(self):
        return self._size

    @property
    def peripherals(self):
        return sorted(self._peripherals, key=lambda peripheral: peripheral.base_address)

    def peripheral(self, name):
        name = name.upper()
        for peripheral in self._peripherals:
            if peripheral.name == name:
                return peripheral
        return None

    @property
    def interrupts(self):
        return sorted(self._interrupts, key=lambda interrupt: interrupt.vector)

    def interrupt(self, name):
        name = name.upper()
        for interrupt in self._interrupts:
            if interrupt.name == name:
                return interrupt
        return None

    def interrupt_by_vector(self, vector):
        for interrupt in self._interrupts:
            if interrupt.vector == vector:
                return interrupt
        return None

    def add_interrupt(self, peripheral, interrupt):
        existing_interrupt = self.interrupt_by_vector(interrupt.vector)
        if existing_interrupt:
            if existing_interrupt.name != interrupt.name:
                raise SvdException("vector already exists but with different name")
            existing_interrupt.add_peripheral(peripheral)
        else:
            self._interrupts.append(interrupt)

    def _parse(self, element):
        if element.tag == 'size':
            self._size = int(element.text, 0)
        if element.tag == 'width':
            self._width = int(element.text, 0)
        if element.tag == 'cpu':
            cpu = Cpu()
            cpu.parse(element)
            self._cpu = cpu
        if element.tag == 'peripherals':
            for sub_element in element:
                if sub_element.tag == 'peripheral':
                    peripheral = Peripheral(self)
                    if 'derivedFrom' in sub_element.attrib:
                        derived_element = sub_element.attrib['derivedFrom']
                        derived_element = derived_element.upper()
                        peripheral.copy(self.peripheral(derived_element))
                    peripheral.parse(sub_element)
                    self._peripherals.append(peripheral)
                    setattr(self, peripheral.name, peripheral)

    def validate(self):
        super().validate()
        if self.size is None:
            raise SvdException("device/size is not set")
        if self.cpu:
            self.cpu.validate()
        for peripheral in self._peripherals:
            peripheral.validate()


def main(svd_file):
    """test"""
    svd = Svd()
    svd.parse_svd(svd_file)
    print("parsing done.")
    svd.validate()
    print("Validation done.")
    print(svd)
    print(f": {svd.cpu}")
    for peripheral in svd.peripherals:
        print(f": {peripheral}")
        for register in peripheral.registers:
            print(f"  : {register}")
            for field in register.fields:
                print(f"    : {field} ({field.description})")
                for enumerated_value in field.enumerated_values:
                    print(f"      : {enumerated_value}")
    last_vector = -1
    for interrupt in svd.interrupts:
        while last_vector + 1 < interrupt.vector:
            last_vector += 1
            print(f"interrupt: {last_vector}")
        last_vector = interrupt.vector
        print(f"interrupt: {interrupt.vector} : {interrupt.name} : [{', '.join([peripheral.name for peripheral in interrupt.peripherals])}]")


if __name__ == "__main__":
    if len(_sys.argv) == 2:
        main(_sys.argv[1])
    else:
        print(f'Usage: {_sys.argv[0]} path/to/file.svd')
