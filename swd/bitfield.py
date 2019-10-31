"""Bitfield manipulation class"""


class BitfieldException(Exception):
    """Custom exception for bitfield"""


class BitfieldRegisterValueNotExist(BitfieldException):
    """Raised if invalidated cache has been accessed"""


class BitfieldCacheIsNotValid(BitfieldException):
    """Raised if invalidated cache has been accessed"""


class _Field:
    """Bits in register

    Arguments:
        offset: offset of field
        size: size of field
        parent_mask: mask of parent register
        named_values: named values (like enum)
    """

    def __init__(self, offset, size, parent_mask, named_values=None):
        self._offset = offset
        self._size = size
        self._mask = 2 ** size - 1
        self._mask_off = self._mask << self._offset
        self._mask_off_inv = parent_mask ^ self._mask_off
        self._value_name = {}
        self._name_value = {}
        if named_values:
            for val, name in named_values:
                self._value_name[val] = name
                self._name_value[name] = val

    def _to_name(self, val):
        return self._value_name.get(val)

    @staticmethod
    def _to_bool(val):
        return str(bool(val))

    def _to_hex(self, val):
        return f"0x{val:0{(self._size + 3) // 4}x}"

    def _to_str(self, val):
        value = self._to_name(val)
        if value is None:
            if self._size == 1:
                value = self._to_bool(val)
            else:
                value = self._to_hex(val)
        return value

    def _to_value(self, val):
        if isinstance(val, int):
            return val
        if isinstance(val, bool):
            return int(val)
        if isinstance(val, str):
            if val in self._name_value:
                return self._name_value[val]
        raise BitfieldRegisterValueNotExist()

    def raw_value(self, val):
        """Get register bits value"""
        return (self._to_value(val) & self._mask) << self._offset

    def value(self, raw):
        """Get numeric value from field"""
        return (raw >> self._offset) & self._mask

    def update_raw(self, raw, val):
        """Update value into field

        Attributes:
            raw: raw register value
            val: new value
        """
        return (raw & self._mask_off_inv) | self.raw_value(val)

    def named_value(self, raw):
        """Get named from field"""
        return self._to_name((raw >> self._offset) & self._mask)

    def string_value(self, raw):
        """Return string representation of value"""
        return self._to_str(self.value(raw))

    def is_name(self, val):
        """Test if named value exists"""
        return val in self._name_value


class Bitfield:
    """Bitfield storage"""

    def __init__(self, description, size=32, raw=None):
        offset = 0
        self._fields = {}
        mask = 2 ** size - 1
        for field_descr in description:
            field_name = field_descr[0]
            field_size = field_descr[1]
            names = None
            if field_name is not None:
                if len(field_descr) > 2:
                    names = field_descr[2]
                self._fields[field_name] = _Field(offset, field_size, mask, names)
            offset += field_size
        if offset != size:
            raise BitfieldException(
                "Invalid number of bits in Bitfield (%d expected is %s)" % (
                    offset, size))
        self._raw = raw

    @property
    def raw(self):
        """Property to read raw value"""
        return self._raw

    @raw.setter
    def raw(self, raw):
        """Property to set raw value"""
        self._raw = raw

    def value(self, field_name):
        """Get register value"""
        return self._fields[field_name].value(self.raw)

    def update_fields(self, **values):
        """Set field value
        Uses read-modify-write

        Arguments:
            field_name: field name
            val: new value
        """
        for field_name, val in values.items():
            self.raw = self._fields[field_name].update_raw(self.raw, val)

    def set_fields(self, **values):
        """Get bits value for one register
        Uses only write with set values,
        not set values will be zero

        Arguments:
            field_name: field name
            val: new value
        """
        raw = 0
        for field_name, val in values.items():
            raw |= self._fields[field_name].raw_value(val)
        self.raw = raw

    def named_value(self, field_name):
        """Named value of string
        if value is not named, then return None

        Arguments:
            field_name: field name

        Returns:
            named value
        """
        return self._fields[field_name].named_value(self.raw)

    def string_value(self, field_name):
        """String representation of field value
        Representation of value can be:
        - named value
        - boolean (True/False)
        - hexadecimal representation

        Arguments:
            field_name: field name

        Returns:
            string representation of value
        """
        return self._fields[field_name].string_value(self.raw)

    @property
    def field_names(self):
        """List if fields names"""
        return self._fields.keys()


class MemRegister(Bitfield):
    """Memory mapped register"""

    _NAME = None
    _ADDRESS = None
    _FIELDS = None
    _SIZE = 32

    def __init__(self, mem_drv, address=None):
        if self._FIELDS is None:
            raise BitfieldException("_FIELDS is not defined")
        self._address = self._ADDRESS
        if address is not None:
            self._address = address
        if self._address is None:
            raise BitfieldException("address is not set")
        super().__init__(self._FIELDS, self._SIZE)
        self._mem_drv = mem_drv
        self._cached = Bitfield(self._FIELDS, self._SIZE, None)

    @property
    def raw(self):  # override
        """Read raw value from memory"""
        if self._address % 4 or self._SIZE != 32:
            data = self._mem_drv.read_mem(self._address, self._SIZE // 8)
            return int.from_bytes(data, byteorder='little')
        return self._mem_drv.get_mem32(self._address)

    @raw.setter
    def raw(self, raw):  # override
        """Write raw value to memory"""
        if self._address % 4:
            data = raw.to_bytes(self._SIZE // 8, byteorder='little')
            self._mem_drv.write_mem(self._address, data)
        else:
            self._mem_drv.set_mem32(self._address, raw)

    @property
    def cached(self):
        """Access cached memory register or load current value"""
        if self._cached.raw is None:
            self._cached.raw = self.raw
        return self._cached

    def discard_cache(self):
        """Discard content of cache"""
        self._cached.raw = None

    def write_cache(self):
        """Write cache to memory register"""
        if self._cached.raw is None:
            raise BitfieldCacheIsNotValid()
        self.raw = self._cached.raw

    @property
    def name(self):
        """Register name"""
        return self._NAME

    @property
    def address(self):
        """Register address"""
        return self._address

    @property
    def size(self):
        """return total number of bits in register"""
        return self._SIZE
