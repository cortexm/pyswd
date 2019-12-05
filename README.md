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
`swd.Swd(swd_frequency=None, driver=None, serial_no='')`

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
'ST-Link/V3 V3J5S1M3B2 (005400283137510339383538)'
```

### Target voltage
Get target voltage measured by ST-Link

#### Return:
  float target voltage in volts

```Python
>>> dev.get_target_voltage()
3.25
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
`get_mem32(address)` - get 32 bit memory register
`get_mem16(address)` - get 16 bit memory register
`get_mem8(address)` - get 8 bit memory register

#### Arguments:
- address: address in memory

#### Return:
  unsigned data from memory

```Python
>>> hex(dev.get_mem32(0x08000000))
'0x20001000'
```

### Set memory register
`set_mem32(address, data)` - set 32 bit memory register
`set_mem16(address, data)` - set 16 bit memory register
`set_mem8(address, data)` - set 8 bit memory register

#### Arguments:
- address: address in memory
- data: unsigned data

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
[0, 0, 16942, 10, 100, 0, 0, 0, 0, 0, 0, 0, 10, 604502776, 134288075, 134284002, 1627389952, 604502776, 0, 0, 67125248]
```

### Write core register
`set_reg(register, data)`

On CortexM platform this will work only if program is halted

#### Arguments:
- register: is numeric coded register (e.g. 0: R0, 1: R1, ...)
- data: 32bit unsigned data

```Python
>>> dev.set_reg(1, 0x12345678)
```

### Load SVD file
`load_svd(svd_file)`

Will load SVD file. Registers are accessible under property `io`

detailed API in `swd/svd.py`

#### Arguments:
- svd_file: path to SVD file

```Python
>>> dev.load_svd('STM32H753')
>>> dev.io.RCC.CR.value
252166181
>>> dev.io.RCC.CR.HSEON.value
True
```

## swd.CortexM module documentation

detailed API in `swd/devices/cortexm.py`

### swd.CortexM:
`swd.CortexM(swd)`

#### Arguments:
- swd: instance of Swd

```Python
>>> import swd
>>> dev = swd.Swd()
>>> cm = swd.CortexM(dev)
```

```Python
>>> cm.name
'ARM/CORTEXM7'
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

### Detect connected MCU
`detect_mcu(expected_mcus=None)`

detailed API in: `swd/devices/mcu.py`

Arguments:
- expected_mcus: list of strings with expected MCUs

```Python
>>> cm.detect_mcu(['STM32H753'])
```

### Load attached MCU SVD
`Mcu.load_svd()`

will load attached SVD and all io registers will be accessible in dev.io

```Python
>>> cm.mcu.load_svd()
>>> dev.io.USART1.CR2.CPOL.value
False
```

### Memory regions:
`Mcu.memory_regions`

Instance of MemoryRegions class

detailed API in: `swd/devices/memory.py`

```Python
mr = cm.mcu.memory_regions
```

### Find memory
`MemoryRegions.find(name=None)`

find memory region by name or kind

Arguments:
- name: memory region name or kind

Returns:
  list of memory instances

```Python
>>> for sram in mr.find('SRAM'):
>>>     print(f"{sram.name} {sram.kind}: {sram.address:08x} {sram.size // 1024} KB")

ITCM SRAM: 00000000 64 KB
DTCM SRAM: 20000000 128 KB
AXI SRAM: 24000000 512 KB
SRAM1 SRAM: 30000000 128 KB
SRAM2 SRAM: 30020000 128 KB
SRAM3 SRAM: 30040000 32 KB
SRAM4 SRAM: 38000000 64 KB
BACKUP SRAM: 38800000 4 KB
```

### Get memory
`MemoryRegions.get(name)`

return memory with name

Arguments:
  name: memory region name

Returns:
  instance of memory

```Python
>>> axi = mr.find('AXI')
>>> axi.size // 1024
512
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
  -i, --info            increase info output
  -v, --verbose         increase verbose output (standard printing)
  -d, --debug           increase debug output
  -f FREQ, --freq FREQ  set SWD frequency
  -s SERIAL, --serial SERIAL
                        select ST-Link by serial number
  -c CPU, --cpu CPU     set expected CPU type [eg: STM32F031G6, STM32H75]
  -S SVD, --svd SVD     path to System View Description file (.svd)
  --no-load-svd         disable auto loading MCU .svd file
  --no-status-checking  disable checking status
```
### List of available actions:
```
  dump8:{addr}[:{size}]     print content of memory 8 bit register or dump
  dump16:{addr}[:{size}]    print content of memory 16 bit register or dump
  dump32:{addr}[:{size}]    print content of memory 32 bit register or dump
  dump:{addr}[:{size}]      print content 32 bit register or 8 bit dump

  set8:{addr}:{data}[:{data}..]     set 8 bit memory
  set16:{addr}:{data}[:{data}..]    set 16 bit memory
  set32:{addr}:{data}[:{data}..]    set 32 bit memory
  set:{addr}:{data}[:{data}..]      set 32 bit register or 8 bit memory area

  fill8:{addr}:{size}:{pattern}     fill memory with 8 bit pattern

  reg:all                   print all core register
  reg:{reg}                 print content of core register
  reg:{reg}:{data}          set core register

  io                        list all IO peripherals
  io:{peri}                 list all IO registers from peripheral
  io:{peri}.{reg}           print IO register value and its fields
  io:{peri}.{reg}.{field}   print IO register field value
  io:{peri}.{reg}:{data}    set IO register
  io:{peri}.{reg}.{field}:{data}  set IO field

  mem                       list all memory regions
  mem[:{region}[:{size}]]   dump memory regions

  sleep:{seconds}           sleep (float) - insert delay between commands

  reset[:halt]              reset core or halt after reset
  run[:nodebug]             run core
  step[:{n}]                step core (n-times)
  halt                      halt core

  (number formats: 42, 0x2a, 0o52, 0b101010, 32K, 1M, ..)
  (reg: R0, R1, ..., R12, SP, LR, PC, PSR, MSP, PSP)

## License
Whole project is under MIT license

