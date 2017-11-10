# PYSWD

Debugging MCUs over SWD with ST-Link/V2 debugger

Allow to access to any SWD enabled MCU

## Instalation:

`pip3 install .`

or reinstall (upgrade):

`pip3 install --upgrade .`

uninstall:

`pip3 uninstall pyswd`

## Python SWD module

`import swd`

Constructor for connected swd device:

`dev = swd.Stlink()`

All public methods from `swd.Stlink` class:

`version`
Instance of ST-Link version (property)

`get_target_voltage(self)`
Get target voltage from programmer

`get_coreid(self)`
Get core ID from MCU

`get_reg(self, reg)`
Get core register (R0, R1, ... )
(CPU must be halted to access core registers)

`set_reg(self, reg, data)`
Set core register
(CPU must be halted to access core registers)

`get_mem32(self, addr)`
Get memory register (32 bits)

`set_mem32(self, addr, data)`
Set memory register (32 bits)

`read_mem(self, addr, size)`
Read memory (output is iterable)

`write_mem(self, addr, data)`
Write memory, data can be iterable

`fill_mem(self, addr, pattern)`
Fill memory with pattern

### Example:

```Python
>>> import swd

>>> dev = swd.Stlink()

>>> dev.version.str
'ST-Link/V2 V2J27S6'

>>> dev.get_target_voltage()
3.21

>>> hex(dev.get_coreid())
'0xbb11477'

>>> hex(dev.get_mem32(0x08000000))
'0x20001000'

>>> dev.set_mem32(0x20000200, 0x12345678)

>>> hex(dev.get_mem32(0x20000200))
'0x12345678

>>> data = dev.read_mem(0x08000000, 16)
>>> ' '.join(['%02x' % d for d in data])
'00 10 00 20 45 00 00 08 41 00 00 08 41 00 00 08'

>>> dev.write_mem(0x20000100, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

>>> data = dev.read_mem(0x20000100, 15)
>>> ' '.join(['%02x' % d for d in data])
'01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f'

>>> dev.fill_mem(0x20000300, 20, [5, 6, 7])
>>> data = dev.read_mem(0x20000300, 20)
>>> ' '.join(['%02x' % d for d in data])
'05 06 07 05 06 07 05 06 07 05 06 07 05 06 07 05 06 07 05 06'

>>> hex(dev.get_reg(1))
'0x0800012e'
```

## Python application

    $ pyswd --help
    usage: pyswd [-h] [-V] [-q] [-d] [-i] [-v] [-f FREQ] [action [action ...]]

    positional arguments:
      action                actions will be processed sequentially

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -q, --quite           quite output
      -d, --debug           increase debug output
      -i, --info            increase info output
      -v, --verbose         increase verbose output
      -f FREQ, --freq FREQ  set SWD frequency

    list of available actions:
      dump8:{addr}[:{size}]     print content of memory 8 bit register or dump
      dump16:{addr}[:{size}]    print content of memory 16 bit register or dump
      dump32:{addr}[:{size}]    print content of memory 32 bit register or dump
      dump:{addr}[:{size}]      print content of memory 32 bit register or 8 bit dump

      set8:{addr}:{data}[:{data}..]     set 8 bit memory

      fill8:{addr}:{size}:{pattern}     fill memory with 8 bit pattern

      (numerical values can be in different formats, like: 42, 0x2a, 0o52, 0b101010, 32K, 1M, ..)
