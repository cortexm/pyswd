"""Main module"""

import swd.stlink
import swd.stlinkcom


def main():
    """Entry point for the application script"""
    try:
        dev = swd.stlink.Stlink()
        print("Detected: %s" % dev.version.str)
        print("Target voltage: %0.2f" % dev.target_voltage)
        print("COREID: 0x%08x" % dev.coreid)
    except swd.stlinkcom.StlinkNotFound:
        print("*** No debugging device was found ***")
