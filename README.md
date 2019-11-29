# PYSWD

Is a python module for debugging microcontrollers with SWD using ST-Link/V2 (/V2-1) or V3 debugger.

This package also contain small command line tool.

## Goal

Is to create python module for access debugging interface on MCU with SWD interface.

Main purpose of python module is to create automated functional and hardware tests from simple python scripts and without special firmware for microcontroller.

## Compatibility

### OS
PYSWD will work on Linux, Mac and Windows.
### Python
Python 3.7+
### Dependencies
- [pyusb](https://github.com/walac/pyusb) - prefer latest version from github, especially on Windows platgorm
- [libusb](https://github.com/libusb/libusb)

## Installation:
### from downloaded sources
```
pip3 install .
```
### reinstall (upgrade):
```
pip3 install --upgrade .
```
### install for editing
```
pip3 install --editable .
```
### uninstall:
```
pip3 uninstall pyswd
```
### using make
```bash
make test
make install
make editable
make uninstall
```

## Python SWD module documentation

### swd.Swd:
`swd.Swd(swd_frequency=4000000, logger=None, serial_no='')`

#### Arguments:
- swd_frequency: SWD communication frequency
- logger: logging interface (optional)
- serial_no: serial number of connected USB ST-Link debugger (optional). Serial number can be also part from begin or end, if more devices are detected then it stops with error

```Python
>>> import swd
>>> dev = swd.Swd()
```

### ST-Link version
property with ST-Link version

#### Return:
  instance of StlinkVersion

```Python
>>> dev.get_version().str
'ST-Link/V2 V2J27S6'
```

### Target voltage
Get target voltage measured by ST-Link

#### Return:
  float target voltage in volts

```Python
>>> dev.get_target_voltage()
3.21
```

### ID code
Get MCU ID code

#### Return:
  32bit unsigned with ID code

```Python
>>> hex(dev.get_idcode())
'0xbb11477'
```

### Get memory register
`get_mem32(address)`

#### Arguments:
- address: address in memory, must be aligned to 32bits

#### Return:
  32bit unsigned data from memory

```Python
>>> hex(dev.get_mem32(0x08000000))
'0x20001000'
```

### Set memory register
`set_mem32(address, data)`

#### Arguments:
- address: address in memory, must be aligned to 32bits
- data: 32bit unsigned data

```Python
>>> dev.set_mem32(0x20000200, 0x12345678)
>>> hex(dev.get_mem32(0x20000200))
'0x12345678'
```

### Read memory
- `read_mem(address, size)` - automatically select read access
- `read_mem8(address, size)` - read using 8 bit access
- `read_mem16(address, size)` - read using 16 bit access
- `read_mem32(address, size)` - read using 32 bit access

#### Arguments:
- address: address in memory
- size: number of bytes to read from memory

#### Return:
  iterable of read data

```Python
>>> data = dev.read_mem(0x08000000, 16)
>>> ' '.join(['%02x' % d for d in data])
'00 10 00 20 45 00 00 08 41 00 00 08 41 00 00 08'
```

### Write memory
- `write_mem(address, data)` - automatically select write access
- `write_mem8(address, data)` - write using 8 bit access
- `write_mem16(address, data)` - write using 16 bit access
- `write_mem32(address, data)` - write using 32 bit access

#### Arguments:
- address: address in memory
- data: list or iterable of bytes whic will be stored into memory

```Python
>>> dev.write_mem(0x20000100, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
>>> data = dev.read_mem(0x20000100, 15)
>>> ' '.join(['%02x' % d for d in data])
'01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f'
```

### Fill memory
- `fill_mem(address, pattern, size)` - automatically select fill access
- `fill_mem8(address, pattern, size)` - fill using 8 bit access
- `fill_mem16(address, pattern, size)` - fill using 16 bit access
- `fill_mem32(address, pattern, size)` - fill using 32 bit access

#### Arguments:
- address: address in memory
- pattern: list or iterable of bytes whic will be stored into memory
- size: number of bytes to fill memory

```Python
>>> dev.fill_mem(0x20000300, [5, 6, 7], 20)
>>> data = dev.read_mem(0x20000300, 20)
>>> ' '.join(['%02x' % d for d in data])
'05 06 07 05 06 07 05 06 07 05 06 07 05 06 07 05 06 07 05 06'
```

### Read core register
`get_reg(register)`
On CortexM platform this will work only if program is halted

#### Arguments:
- register: is numeric coded register (e.g. 0: R0, 1: R1, ...)

#### Return:
  32bit unsigned data

```Python
>>> hex(dev.get_reg(1))
'0x0800012e'
```

### Read all core registers
`get_reg_all()`
On CortexM platform this will work only if program is halted

#### Return:
  list of 32bit unsigned data for all registers

```Python
>>> dev.get_reg_all()
[0,  0,  16942,  10,  100,  0,  0,  0,  0,  0,  0,  0,  10,  604502776,  134288075,  134284002,  1627389952,  604502776,  0,  0,  67125248]
```

### Write core register
`get_reg(register)`
On CortexM platform this will work only if program is halted

#### Arguments:
- register: is numeric coded register (e.g. 0: R0, 1: R1, ...)
- data: 32bit unsigned data

```Python
>>> dev.set_reg(1, 0x12345678)
```

### swd.CortexM:
`swd.CortexM(swd)`

#### Arguments:
- swd: instance of Swd

```Python
>>> import swd
>>> dev = swd.Swd()
>>> cm = swd.CortexM(dev)
```

### Read core register
`get_reg(register)`
On CortexM platform this will work only if program is halted

#### Arguments:
- register: name of register (e.g.: 'R0', 'R1', 'SP', 'PC', ...)

#### Return:
  32bit unsigned data

```Python
>>> hex(cm.get_reg('PC'))
'0x0800012e'
```

### Write core register
`set_reg(register)`
On CortexM platform this will work only if program is halted

#### Arguments:
- register: name of register (e.g.: 'R0', 'R1', 'SP', 'PC', ...)
- data: 32bit unsigned data

```Python
>>> cm.set_reg('R2', 0x12345678)
```

### Read all core registers
`get_reg_all()`
On CortexM platform this will work only if program is halted

#### Return:
  dictionary with register name as key and as value 32bit unsigned data for each register

```Python
>>> cm.get_reg_all()
{'LR': 134288075,
 'MSP': 604502776,
 'PC': 134284002,
 'PSP': 0,
 'PSR': 1627389952,
 'R0': 0,
 'R1': 0,
 'R10': 0,
 'R11': 0,
 'R12': 10,
 'R2': 16942,
 'R3': 10,
 'R4': 100,
 'R5': 0,
 'R6': 0,
 'R7': 0,
 'R8': 0,
 'R9': 0,
 'SP': 604502776}
```

### Reset
`reset()`

```Python
>>> cm.reset()
```

### Reset and halt
`reset_halt()`

```Python
>>> cm.reset_halt()
```

### Halt core
`halt()`

```Python
>>> cm.halt()
```

### step program
`step()`

```Python
>>> cm.step()
```

### Run in debug mode
`run()`

```Python
>>> cm.run()
```

### Disable debug mode and run
`nodebug()`

```Python
>>> cm.nodebug()
```

### Check if MCU is halted
`is_halted()`

#### Return:
  True if MCU is halted, or False if is running

```Python
>>> cm.is_halted()
True
```

## Python application
Simple tool for access MCU debugging features from command line. Is installed together with python module.

```
$ pyswd --help
```
### Usage:
```
pyswd [-h] [-V] [-q] [-d] [-i] [-v] [-f FREQ] [action [action ...]]
```
### positional arguments:
```
action                actions will be processed sequentially
```
### Optional arguments:
```
-h, --help            show this help message and exit
-V, --version         show program's version number and exit
-q, --quite           quite output
-d, --debug           increase debug output
-i, --info            increase info output
-v, --verbose         increase verbose output
-f FREQ, --freq FREQ  set SWD frequency
-s SERIAL, --serial SERIAL
                        select ST-Link by serial number (enough is part of serial number: begin or end
```
### List of available actions:
```
  dump8:{addr}[:{size}]     print content of memory 8 bit register or dump
  dump16:{addr}[:{size}]    print content of memory 16 bit register or dump
  dump32:{addr}[:{size}]    print content of memory 32 bit register or dump
  dump:{addr}[:{size}]      print content of memory 32 bit register or 8 bit dump

  set8:{addr}:{data}[:{data}..]     set 8 bit memory
  set16:{addr}:{data}[:{data}..]    set 16 bit memory
  set32:{addr}:{data}[:{data}..]    set 32 bit memory
  set:{addr}:{data}[:{data}..]      set 32 bit memory register or 8 bit memory area

  fill8:{addr}:{size}:{pattern}     fill memory with 8 bit pattern

  reg:all                   print all core register
  reg:{reg}                 print content of core register
  reg:{reg}:{data}          set core register

  reset[:halt]              reset core or halt after reset
  run[:nodebug]             run core
  step[:{n}]                step core (n-times)
  halt                      halt core

  sleep:{seconds}           sleep (float) - insert delay between commands
```
(numerical values can be in different formats, like: 42, 0x2a, 0o52, 0b101010, 32K, 1M, ..)

## License
Whole project is under MIT license

