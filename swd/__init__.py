"""Main module"""

import swd.stlink
import swd.stlinkcom


def main():
    """Entry point for the application script"""
    try:
        dev = swd.stlink.Stlink()
        print(dev.version.str)
        print("Target voltage: %0.2fV" % dev.get_target_voltage())
        print("COREID: 0x%08x" % dev.get_coreid())
    except swd.stlinkcom.StlinkNotFound:
        print("*** No debugging device was found ***")
