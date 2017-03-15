# PYSWD

Debugging MCUs over SWD with ST-Link/V2 debugger

## Python library

### Example:

```Python
>>> import swd
>>> dev = swd.stlink.Stlink()
>>> dev.version.str
'ST-Link/V2 V2J27S6'
>>> hex(dev.get_mem32(0x08000000))
'0x20001000'
>>> dev.set_mem32(0x20000200, 0x12345678)
>>> hex(dev.get_mem32(0x20000200))
'0x12345678

## Python application
