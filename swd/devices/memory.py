"""Memory"""

KILO = 1024
MEGA = 1024 * KILO
GIGO = 1024 * MEGA


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

    def __init__(self, kind, size, address=0, name=None, **attributes):
        """Constructor

        Arguments:
            kind: string memory kind ('FLASH', 'SRAM', 'EEPROM', ...)
            size: memory size in Bytes
            address: start address
            name: name of memory region
        """
        if not name:
            name = kind
        self._kind = kind
        self._name = name
        self._address = address
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
    def address(self):
        """Start address"""
        return self._address

    @property
    def size(self):
        """Memory size in Bytes"""
        return self._size

    def attribute(self, attribute):
        """Return memory attribute"""
        return self._attributes.get(attribute)

    def __str__(self):
        return (
            f"{self._kind}.{self.name}:"
            f" 0x{self._address:08x}:{self._size // KILO} KB")


class MemoryRegions:
    """Memory regions manager class"""

    def __init__(self, memory_specs):
        self._memory_regions = []
        for memory_spec in memory_specs:
            self._memory_regions.append(Memory(**memory_spec))

    def get_memory_regions(self, name=None):
        """return list of memory regions

        Arguments:
            kind: string memory kind ('FLASH', 'SRAM', ..)
        """
        memory_regions = []
        if name is None:
            return self._memory_regions
        for memory in self._memory_regions:
            if name in (memory.kind, memory.name):
                memory_regions.append(memory)
        return memory_regions

    def get_size(self, name):
        """Return total size of memory regions"""
        return sum([mem.size for mem in self.get_memory_regions(name)])

    def get_memory(self, name):
        """return memory region with name
        """
        for memory in self._memory_regions:
            if memory.name == name:
                return memory
        raise NotFoundMemory(f"{name} memory not found.")


def main():
    mem_regions = MemoryRegions([{
        'name': "ITCM",
        'kind': "SRAM",
        'address': 0x00000000,
        'size': 64 * KILO,
    }, {
        'name': "FLASH1",
        'kind': "FLASH",
        'address': 0x08000000,
        'size': 1024 * KILO,
        'sector_size': 128 * KILO,
    }, {
        'name': "FLASH2",
        'kind': "FLASH",
        'address': 0x08100000,
        'size': 1024 * KILO,
        'sector_size': 128 * KILO,
    }, {
        'name': "DTCM",
        'kind': "SRAM",
        'address': 0x20000000,
        'size': 128 * KILO,
    }, {
        'name': "AXI",
        'kind': "SRAM",
        'address': 0x24000000,
        'size': 512 * KILO,
    }, {
        'name': "SRAM1",
        'kind': "SRAM",
        'address': 0x30000000,
        'size': 128 * KILO,
    }, {
        'name': "SRAM2",
        'kind': "SRAM",
        'address': 0x30020000,
        'size': 128 * KILO,
    }, {
        'name': "SRAM3",
        'kind': "SRAM",
        'address': 0x30040000,
        'size': 32 * KILO,
    }, {
        'name': "SRAM4",
        'kind': "SRAM",
        'address': 0x38000000,
        'size': 64 * KILO,
    }, {
        'name': "BACKUP",
        'kind': "SRAM",
        'address': 0x38000000,
        'size': 4 * KILO,
    }])
    for mem_reg in mem_regions.get_memory_regions():
        print(mem_reg)
    print("SRAM", mem_regions.get_size("SRAM") // KILO, 'KB')
    print("FLASH", mem_regions.get_size("FLASH") // KILO, 'KB')
    print("BACKUP", mem_regions.get_size("BACKUP") // KILO, 'KB')


if __name__ == "__main__":
    main()
