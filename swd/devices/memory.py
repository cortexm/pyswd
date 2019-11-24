"""Memory"""

KILO = 1024
MEGA = 1024 * KILO


class MemError(Exception):
    """General memory error"""


class MemoryException(MemError):
    """General memory exception"""


class NotFoundMemory(MemoryException):
    """Raised when memory region was not found"""


class NotFoundAttribute(MemoryException):
    """Raised when memory region was not found"""


class Memory:
    """General memory class"""

    def __init__(self, kind, size, start_address=0, name=None, **attributes):
        """Constructor

        Arguments:
            kind: string memory kind ('FLASH', 'SRAM', 'EEPROM', ...)
            size: memory size in Bytes
            start_address: start address
            name: name of memory region
        """
        if not name:
            name = kind
        self._kind = kind
        self._name = name
        self._start_address = start_address
        self._size = size
        self._attributes = attributes

    @property
    def kind(self):
        """Memory kind ('FLASH', 'SRAM', 'EEPROM', ...)"""
        return self._kind

    @property
    def name(self):
        """Name of memory region"""
        return self._name

    @property
    def start_address(self):
        """Start address"""
        return self._start_address

    @property
    def size(self):
        """Memory size in Bytes"""
        return self._size

    def get_attribute(self, attribute):
        """Return memory attribute"""
        if attribute not in self._attributes:
            raise
        return self._attributes[attribute]


class MemoryRegions:
    """Memory regions manager class"""

    def __init__(self, specs):
        pass

    def get_memory_regions(self, kind=None):
        """return list of memory regions

        Arguments:
            kind: string memory kind ('FLASH', 'SRAM', ..)
        """
        memory_regions = []
        for memory in self._memory_regions:
            if memory.kind == kind:
                memory_regions.append(memory)
        return memory_regions

    def get_memory(self, name):
        """return memory region with name
        """
        for memory in self._memory_regions:
            if memory.name == name:
                return memory
        raise NotFoundMemory(f"{name} memory not found.")
