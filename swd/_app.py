"""Application"""

import sys
import argparse
import logging
import itertools
import swd
import swd.stlink
import swd.stlinkcom
import swd.__about__
import swd._log as _log


class PyswdException(Exception):
    """Exception"""

_VERSION_STR = "%s %s (%s <%s>)" % (
    swd.__about__.PROGNAME,
    swd.__about__.VERSION,
    swd.__about__.AUTHOR,
    swd.__about__.AUTHOR_EMAIL)
_ACTIONS_HELP_STR = """
list of available actions:
  dump8:{addr}[:{size}]     print content of memory 8 bit register or dump
  dump16:{addr}[:{size}]    print content of memory 16 bit register or dump
  dump32:{addr}[:{size}]    print content of memory 32 bit register or dump
  dump:{addr}[:{size}]      print content of memory 32 bit register or 8 bit dump

  set8:{addr}:{data}[:{data}..]     set 8 bit memory

  fill8:{addr}:{size}:{pattern}     fill memory with 8 bit pattern

  (numerical values can be in different formats, like: 42, 0x2a, 0o52, 0b101010, 32K, 1M, ..)
"""
# TODO unimplemented actions:
#   dump:core                 print content of core registers (R1, R2, ..)
#   dump:{reg_name}           print content of core register (R1, R2, ..)
#   set:{reg}:{data}                  set core register (halt core)
#   set:{addr}:{data}[:{data}..]      set 32 bit memory
#   set16:{addr}:{data}[:{data}..]    set 16 bit memory
#   set32:{addr}:{data}[:{data}..]    set 32 bit memory
#   fill:{addr}:{size}:{pattern}      fill memory with 8 bit pattern
#   fill16:{addr}:{size}:{pattern}    fill memory with 16 bit pattern
#   fill32:{addr}:{size}:{pattern}    fill memory with 32 bit pattern
#   read:{addr}:{size}:{file}      read memory with size into file
#   read:sram[:{size}]:{file}      read SRAM into file
#   read:flash[:{size}]:{file}     read FLASH into file
#   write:{file.srec}     write SREC file into memory
#   write:{addr}:{file}   write binary file into memory
#   write:sram:{file}     write binary file into SRAM memory
#   sleep:{seconds}        sleep (float) - insert delay between commands

def _configure_argparse():
    """configure and process command line arguments"""
    parser = argparse.ArgumentParser(
        prog=swd.__about__.PROGNAME, formatter_class=argparse.RawTextHelpFormatter,
        epilog=_ACTIONS_HELP_STR)
    parser.add_argument('-V', '--version', action='version', version=_VERSION_STR)
    parser.add_argument("-q", "--quite", action="store_true", help="quite output")
    parser.add_argument("-d", "--debug", action="count", help="increase debug output")
    parser.add_argument("-i", "--info", action="count", help="increase info output")
    parser.add_argument("-v", "--verbose", action="count", help="increase verbose output")
    parser.add_argument("-f", "--freq", type=int, default=1800000, help="set SWD frequency")
    parser.add_argument('action', nargs='*', help='actions will be processed sequentially')
    return parser.parse_args()

def chunks(data, chunk_size):
    """Yield chunks"""
    data = iter(data)
    while True:
        chunk = list(itertools.islice(data, 0, chunk_size))
        if not chunk:
            return
        yield chunk

def hex_line8(chunk):
    """Create 8 bit hex string from bytes in chunk"""
    result = ' '.join([
        '%02x' % part
        for part in chunk])
    return result.ljust(16 * 3 - 1)

def hex_line16(chunk):
    """Create 16 bit hex string from bytes in chunk"""
    result = ' '.join([
        '%04x' % int.from_bytes(part, byteorder='little')
        for part in chunks(chunk, 2)])
    return result.ljust((16 // 2) * 5 - 1)

def hex_line32(chunk):
    """Create 32 bit hex string from bytes in chunk"""
    result = ' '.join([
        '%08x' % int.from_bytes(part, byteorder='little')
        for part in chunks(chunk, 4)])
    return result.ljust((16 // 4) * 9 - 1)

def ascii_line(chunk):
    """Create ASCII string from bytes in chunk"""
    return ''.join([
        chr(d) if d >= 32 and d < 127 else '.'
        for d in chunk])

def print_buffer(addr, data, hex_line=hex_line8, verbose=0):
    """Print buffer in hex and ASCII"""
    prev_chunk = []
    same_chunk = False
    for chunk in chunks(data, 16):
        if verbose > 0 or prev_chunk != chunk:
            print('%08x  %s  %s' % (
                addr,
                hex_line(chunk),
                ascii_line(chunk),
            ))
            prev_chunk = chunk
            same_chunk = False
        elif not same_chunk:
            print('*')
            same_chunk = True
        elif sys.stdout.isatty() and addr % 0x1000 == 0:
            print('%08x\r' % addr, end='', flush=True)
        addr += len(chunk)
    if same_chunk or verbose > 1:
        print('%08x' % addr)

def test_alignment(num, param_name, align):
    """Test if number is aligned"""
    if num % align:
        raise PyswdException('%s must be aligned to %d Bytes' % (param_name, align))

def convert_numeric(num):
    """Convert string number into integer"""
    if num[-1] in ('K', 'k'):
        return int(num[:-1]) * 1024
    if num[-1] in ('M', 'm'):
        return int(num[:-1]) * 1024 ** 2
    if num[-1] in ('G', 'g'):
        return int(num[:-1]) * 1024 ** 3
    return int(num, 0)

class Application():
    """Application"""

    def __init__(self, args):
        """Application startup"""
        self._swd = None
        self._verbose = 0
        self._actions = args.action
        self._swd_frequency = args.freq
        if args.verbose is not None:
            self._verbose = args.verbose
        if args.quite:
            logging.basicConfig(level=logging.ERROR)
        elif args.debug is not None:
            logging.basicConfig(level=logging.DEBUG - (args.debug - 1))
        elif args.info is not None:
            logging.basicConfig(level=logging.INFO - (args.info - 1))
        else:
            logging.basicConfig(level=logging.WARNING)

    def print_device_info(self):
        """Show device informations"""
        logging.info(self._swd.get_version())
        logging.info("Target voltage: %0.2fV", self._swd.get_target_voltage())
        if self._swd.get_idcode() == 0:
            logging.warning("No IDCODE, probably MCU is not connected.")

    def action_dump32(self, params):
        """Dump memory 32 bit"""
        if not params:
            raise PyswdException("dump32: no parameters")
        addr = convert_numeric(params[0])
        if len(params) == 1:
            if addr % 4:
                data = self._swd.read_mem(addr, 4)
                val = int.from_bytes(data, byteorder='little')
            else:
                val = self._swd.get_mem32(addr)
            print("%08x: %08x" % (addr, val))
        elif len(params) == 2:
            size = convert_numeric(params[1])
            test_alignment(size, "Size", 4)
            data = self._swd.read_mem(addr, size)
            print_buffer(addr, data, hex_line32, verbose=self._verbose)
        else:
            raise PyswdException("dump32: too many parameters")

    def action_dump16(self, params):
        """Dump memory 16 bit"""
        if not params:
            raise PyswdException("dump16: no parameters")
        addr = convert_numeric(params[0])
        if len(params) == 1:
            data = self._swd.read_mem(addr, 2)
            val = int.from_bytes(data, byteorder='little')
            print("%08x: %04x" % (addr, val))
        elif len(params) == 2:
            size = convert_numeric(params[1])
            test_alignment(size, "Size", 2)
            data = self._swd.read_mem(addr, size)
            print_buffer(addr, data, hex_line16, verbose=self._verbose)
        else:
            raise PyswdException("dump16: too many parameters")

    def action_dump8(self, params):
        """Dump memory 8 bit"""
        if not params:
            raise PyswdException("dump: no parameters")
        addr = convert_numeric(params[0])
        if len(params) == 1:
            data = self._swd.read_mem(addr, 1)
            print("%08x: %02x" % (addr, next(data)))
        elif len(params) == 2:
            size = convert_numeric(params[1])
            data = self._swd.read_mem(addr, size)
            print_buffer(addr, data, hex_line8, verbose=self._verbose)
        else:
            raise PyswdException("dump: too many parameters")

    def action_dump(self, params):
        """Dump memory"""
        if not params:
            raise PyswdException("dump: no parameters")
        if len(params) == 1:
            self.action_dump32(params)
        elif len(params) == 2:
            self.action_dump8(params)
        else:
            raise PyswdException("dump: too many parameters")

    def action_set8(self, params):
        """Fill memory with data"""
        if len(params) < 2:
            raise PyswdException("set: require at least 3 parameters")
        addr = convert_numeric(params[0])
        data = [int(i, 0) for i in params[1:]]
        self._swd.write_mem(addr, data)

    def action_fill8(self, params):
        """Fill memory with pattern"""
        if len(params) < 3:
            raise PyswdException("fill: require at least 3 parameters")
        addr = convert_numeric(params[0])
        size = convert_numeric(params[1])
        pattern = [int(i, 0) for i in params[2:]]
        self._swd.fill_mem(addr, pattern, size)

    def process_actions(self):
        """Process all actions"""
        for action in self._actions:
            logging.debug(action)
            action_parts = action.split(":")
            action_name = "action_" + action_parts[0]
            if not hasattr(self, action_name):
                raise PyswdException("Action '%s' is not implemented" % action)
            getattr(self, action_name)(action_parts[1:])

    def start(self):
        """Application start point"""
        try:
            self._swd = swd.Swd(swd_frequency=self._swd_frequency)
            self.print_device_info()
            self.process_actions()
        except swd.stlinkcom.StlinkComNotFound:
            logging.error("ST-Link not connected.")
        except PyswdException as err:
            logging.error("pyswd error: %s.", err)
        except swd.stlink.StlinkException as err:
            logging.critical("Stlink error: %s.", err)
        except swd.stlinkcom.StlinkComException as err:
            logging.critical("StlinkCom error: %s.", err)
        else:
            return 0
        return 1

def main():
    """application startup"""
    _log.configure()
    args = _configure_argparse()
    app = Application(args)
    ret = app.start()
    exit(ret)
