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
`swd.Swd(swd_frequency=None, driver=None, serial_no='', debug=0)`

#### Arguments:
- swd_frequency: SWD communication frequency (optional)
- driver: SWD driver instance (optional, default driver is `swd.stlink.Stlink`)
- serial_no: serial number of connected USB ST-Link debugger (optional). Serial number can be also part from begin or end, if more devices are detected then it stops with error
- debug: debug output level (optional)

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
`set_reg(register, data)`
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

## Microcontrollers with multiple APs

Some MCUs (with STM32H5 series as an example) could have multiple independent APs (debug access ports). In such cases,
you will need to specify which AP debugger should use:

```python
swd.open_ap(1)
swd.default_ap = 1

# continue using as usual:
cm = CortexM(swd)
print(cm.get_reg_all())
```

Note that you should use only `CortexM` high-level functions, as these functions will dynamically select between ST-Link
native implementation (which is faster, but supports only AP0) and software emulation via memory accesses. `SWD` class
exposes ST-Link native implementation directly, regardless of default AP selected.

To dynamically detect which MCU is attached, you could use IDCODE and DBGMCU registers. Both methods are AP-independent, 
as DBGMCU register block is available on AP0 as well. 

## Python SWIM module documentation

SWIM (Single Wire Interface Module) is debug interface of STM8 microcontrollers, accessed through ST-Link/V2 (/V2-1) or V3 debugger.

### swd.Swim:
`swd.Swim(driver=None, serial_no='', debug=0, high_speed=True)`

#### Arguments:
- driver: instance of SWIM driver (optional, default driver is swd.stlink.swim.StlinkSwim)
- serial_no: serial number of connected USB ST-Link debugger (optional)
- debug: debug output level (optional)
- high_speed: switch SWIM to high speed mode after connect (optional, default True)

```Python
>>> import swd
>>> swim = swd.Swim()
>>> swim.get_version().str
'ST-Link/V2 V2J35S7'
>>> swim.get_target_voltage()
3.21
```

### Read/write/fill memory
Same API as `swd.Swd`: `read_mem`, `read_mem8`, `read_mem16`, `read_mem32`, `write_mem`, `write_mem8`, `write_mem16`, `write_mem32`, `fill_mem`, `fill_mem8`, `fill_mem16`, `fill_mem32`, `get_mem32`, `set_mem32`.

Transfers are automatically chunked by the debugger's SWIM buffer size (`maximum_8bit_data`).

```Python
>>> swim.write_mem(0x8000, [1, 2, 3, 4])
>>> data = swim.read_mem(0x8000, 4)
>>> ' '.join(['%02x' % d for d in data])
'01 02 03 04'
```

### swd.Stm8:
`swd.Stm8(swim, part='STM8S')`

#### Arguments:
- swim: instance of Swim
- part: part family - 'STM8S' or 'STM8L', or dictionary with flash register layout

```Python
>>> import swd
>>> swim = swd.Swim()
>>> stm8 = swd.Stm8(swim, 'STM8S')
```

### Read core register
`get_reg(register)`

#### Arguments:
- register: register name ('A', 'PCE', 'PCH', 'PCL', 'XH', 'XL', 'YH', 'YL', 'SPH', 'SPL', 'CC', or assembled: 'PC', 'X', 'Y', 'SP')

#### Return:
  8, 16 or 24 bit number

```Python
>>> hex(stm8.get_reg('PC'))
'0x8000'
>>> hex(stm8.get_reg('A'))
'0x5a'
```

### Write core register
`set_reg(register, data)`

```Python
>>> stm8.set_reg('X', 0x1234)
```

### Read all core registers
`get_reg_all()`

#### Return:
  dictionary with register name as key and as value 8, 16 or 24 bit number for each register

```Python
>>> stm8.get_reg_all()
{'A': 90, 'CC': 8, 'PCE': 1, 'PC': 65792, ...}
```

### Halt core
`halt()`

### Run in debug mode
`run()`

### Check if MCU is halted
`is_halted()`

#### Return:
  True if MCU is halted, or False if is running

### Reset
`reset()` - reset MCU (SWIM disable after reset)

### Reset and halt
`reset_halt()` - reset MCU and halt after reset

### Step
`step(count=1)` - execute `count` instructions in step mode (UM0470 4.10)

CPU must be halted. Each instruction is executed and the CPU is stalled again.

### Disable debug mode and run
`nodebug()`

Not supported on STM8: `SWIM_DM` in `SWIM_CSR` is write-1 only and can only be
cleared by a hardware reset, so this function raises `Stm8Exception`. The closest
equivalent is `reset()`, after which the CPU runs without the debug module.

### Hardware breakpoints
`set_breakpoint(mode, address, data=None)` - program the debug module break
condition. `mode` is one of the `Stm8.BREAKPOINT_MODES` keys (UM0470 Table 4):

- `'instruction'` - break on instruction fetch at `address`
- `'write'`, `'read'`, `'read_write'` - break on data access at `address`
  (optionally matched against `data`)
- `'instruction_then'` - break on fetch at `address`, then at `data`
- `'*_range'` / `'*_outside_range'` modes - break over the `address`..`data` range
  (or its complement)

```Python
>>> stm8.set_breakpoint('instruction', 0x8000)
>>> stm8.run()
>>> stm8.is_breakpoint_hit()
True
```

`clear_breakpoint()` - disable the break condition and reset the breakpoint
registers.

`clear_breakpoint_flags()` - clear the BK1F/BK2F/BRW flags in `DM_CSR1`.

`is_breakpoint_hit()` - return True if a breakpoint flag is set.

Note: instruction breakpoints only trigger on instruction boundaries (not at the
initial PC), and data-read breakpoints are not usable on all parts (they depend
on `DM_CR2.FV_ROM`).

### Unlock FLASH / DATA for writing
`unlock_flash()` - unlock FLASH (PUKR)

`unlock_data()` - unlock DATA EEPROM / option bytes (DUKR)

### Write FLASH block
`write_flash_block(address, data, fast=True)`

Stalls CPU, sets programming mode (fast or standard), unlocks FLASH, writes one block (64 bytes on STM8S, 128 on STM8L) and waits for end of programming (EOP).

#### Arguments:
- address: block aligned address in FLASH memory
- data: list or bytes of block_size bytes to write
- fast: use fast programming mode (default True)

```Python
>>> stm8.halt()
>>> stm8.write_flash_block(0x8000, bytes(range(64)))
```

### Write option bytes block
`write_option_block(address, data)`

```Python
>>> stm8.write_option_block(0x4800, bytes([0x00, 0x00]))
```

## Python application
Simple tool for access MCU debugging features from command line. Is installed together with python module.

```
$ pyswd --help
```
### Usage:
```
pyswd [-h] [-V] [-q] [-i] [-v] [-d] [-f FREQ] [-w] [-s SERIAL] [action ...]
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
-v, --verbose         increase verbose output
-d, --debug           increase debug output
-f FREQ, --freq FREQ  set SWD frequency
-w, --swim            use SWIM interface (STM8 targets)
-s SERIAL, --serial SERIAL
                      select ST-Link by serial number
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

  sleep:{seconds}           sleep (float) - insert delay between commands

  reset[:halt]              reset core or halt after reset
  run[:nodebug]             run core
  step[:{n}]                step core (n-times)
  halt                      halt core

  (number formats: 42, 0x2a, 0o52, 0b101010, 32K, 1M, ..)
  (reg: R0, R1, ..., R12, SP, LR, PC, PSR, MSP, PSP)
```

With `--swim` option memory actions work over SWIM (STM8). `reg`, `reset`, `halt` and `step` are supported, `run:nodebug` is not available on STM8 (`nodebug()` raises an error, since SWIM debug mode can only be left by a reset).

## License
Whole project is under MIT license

