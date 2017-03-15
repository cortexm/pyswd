# PYSWD

Debugging MCUs over SWD with ST-Link/V2 debugger

## Python library

Allow direct access to SWD

`import swd`

constructor for connected swd device:

`dev = swd.stlink.Stlink()`

all public methods from `swd.stlink.Stlink` class:

`com(self)`
instance to Communication class

`version(self)`
ST-Link version

`get_target_voltage(self)`
Get target voltage from programmer

`get_coreid(self)`
Get core ID from MCU

`get_reg(self, reg)`
Get core register (R0, R1, ... )

`set_reg(self, reg, data)`
Set core register

`set_mem32(self, addr, data)`
Set memory register (32 bits)

`get_mem32(self, addr)`
Get memory register (32 bits)

`read_mem32(self, addr, size)`
Read memory (32 bits access)

`write_mem32(self, addr, data)`
Write memory (32 bits access)

`read_mem8(self, addr, size)`
Read memory (8 bits access)

`write_mem8(self, addr, data)`
Write memory (8 bits access)

### Example:

```Python
>>> import swd
>>> dev = swd.stlink.Stlink()
>>> dev.version.str
'ST-Link/V2 V2J27S6'
>>> dev.get_target_voltage()
3.201045068582626
>>> hex(dev.get_coreid())
'0xbb11477'
>>> hex(dev.get_mem32(0x08000000))
'0x20001000'
>>> dev.set_mem32(0x20000200, 0x12345678)
>>> hex(dev.get_mem32(0x20000200))
'0x12345678
>>> data = dev.read_mem32(0x08000000, 256)
>>> ' '.join(['%02x' % d for d in data])
'00 10 00 20 65 03 00 08 5d 03 00 08 c1 00 00 08 5d 03 00 08 5d 03 00 08 5d 03 00 08 5d 03 00 08'
>>> dev.write_mem8(0x20000100, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
data = dev.read_mem8(0x20000100, 15)
>>> ' '.join(['%02x' % d for d in data])
'01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f'
>>> hex(dev.get_reg(1))
'0x0800012e'
```

## Python application

TODO
