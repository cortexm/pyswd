# PYSWD

Is a python module for debugging microcontrollers with SWD using ST-Link/V2 (/V2-1) debugger.

This package also contain small command line tool.

## Goal

Is to create python module for access debugging interface on MCU with SWD interface.

Main purpose of python module is to create automated functional and hardware tests from simple python scripts and without special firmware for microcontroller.

## Compatibility

### OS
PYSWD will work on Linux, Mac and Windows.
### Python
Python 3.4+ (Development is under python 3.6)
### Dependencies
- [pyusb](https://github.com/walac/pyusb) - is installed automatically as dependency with pip
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
### uninstall:
```
pip3 uninstall pyswd
```

## Python SWD module

### Constructor:
`swd.Swd(swd_frequency=1800000, logger=None)`
#### Arguments:
- swd_frequency: SWD communication frequency
- logger: logging interface (optional)
```Python
>>> import swd
>>> dev = swd.Swd()
```
### ST-Link version
property with ST-Link version
#### Return:
  instance of StlinkVersion
```Python
>>> dev.version.str
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
'0x12345678
```
### Read memory
`read_mem(address, size)`
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
`write_mem(address, data)`
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
`write_mem(address, pattern, size)`
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
### Write core register
`get_reg(register)`
On CortexM platform this will work only if program is halted
#### Arguments:
- register: is numeric coded register (e.g. 0: R0, 1: R1, ...)
- data: 32bit unsigned data
```Python
>>> hex(dev.get_reg(1))
'0x0800012e'
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
````
### List of available actions:
```
dump8:{addr}[:{size}]     print content of memory 8 bit register or dump
dump16:{addr}[:{size}]    print content of memory 16 bit register or dump
dump32:{addr}[:{size}]    print content of memory 32 bit register or dump
dump:{addr}[:{size}]      print content of memory 32 bit register or 8 bit dump

set8:{addr}:{data}[:{data}..]     set 8 bit memory

fill8:{addr}:{size}:{pattern}     fill memory with 8 bit pattern
```
(numerical values can be in different formats, like: 42, 0x2a, 0o52, 0b101010, 32K, 1M, ..)

## License
Whole project is under MIT license

