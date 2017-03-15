# PYSWD

Debugging MCUs over SWD with ST-Link/V2 debugger

## Python library

Allow direct access to SWD

`import swd`

constructor for connected swd device:

`dev = swd.stlink.Stlink()`

all public methods

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
