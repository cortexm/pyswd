"""Application"""

import argparse
import logging
import swd
import swd.stlink
import swd.stlinkcom


PROGNAME_STR = "pyswd"
VERSION_STR = "%s v1.0.0 (ST-LinkV2)" % PROGNAME_STR
ACTIONS_HELP_STR = """
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


class PyswdException(Exception):
    """Exception"""


def chunks(data, chunk_size):
    """Yield successive n-sized chunks from l."""
    data = iter(data)
    while True:
        chunk = []
        try:
            for _ in range(chunk_size):
                chunk.append(next(data))
        except StopIteration:
            if not chunk:
                return
        yield chunk

def print_buffer32(addr, data, verbose=0):
    """print buffer in 8bit size"""
    prev_chunk = []
    same_chunk = False
    for chunk in chunks(data, 16):
        if verbose > 0 or prev_chunk != chunk:
            chunk32 = [int.from_bytes(part, byteorder='little') for part in chunks(chunk, 4)]
            print('%08x  %s%s  %s' % (
                addr,
                ' '.join(['%08x' % d for d in chunk32]),
                '         ' * (4 - len(chunk32)),
                ''.join([chr(d) if d >= 32 and d < 127 else '.' for d in chunk]),
            ))
            prev_chunk = chunk
            same_chunk = False
        elif not same_chunk:
            print('*')
            same_chunk = True
        addr += len(chunk)
    if same_chunk or verbose > 1:
        print('%08x' % addr)

def print_buffer16(addr, data, verbose=0):
    """print buffer in 8bit size"""
    prev_chunk = []
    same_chunk = False
    for chunk in chunks(data, 16):
        if verbose > 0 or  prev_chunk != chunk:
            chunk16 = [int.from_bytes(part, byteorder='little') for part in chunks(chunk, 2)]
            print('%08x  %s%s  %s' % (
                addr,
                ' '.join(['%04x' % d for d in chunk16]),
                '     ' * (8 - len(chunk16)),
                ''.join([chr(d) if d >= 32 and d < 127 else '.' for d in chunk]),
            ))
            prev_chunk = chunk
            same_chunk = False
        elif not same_chunk:
            print('*')
            same_chunk = True
        addr += len(chunk)
    if same_chunk or verbose > 1:
        print('%08x' % addr)

def print_buffer8(addr, data, verbose=0):
    """print buffer in 8bit size"""
    prev_chunk = []
    same_chunk = False
    for chunk in chunks(data, 16):
        if verbose > 0 or prev_chunk != chunk:
            print('%08x  %s%s  %s' % (
                addr,
                ' '.join(['%02x' % d for d in chunk]),
                '   ' * (16 - len(chunk)),
                ''.join([chr(d) if d >= 32 and d < 127 else '.' for d in chunk]),
            ))
            prev_chunk = chunk
            same_chunk = False
        elif not same_chunk:
            print('*')
            same_chunk = True
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

class _PyswdFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno <= logging.DEBUG:
            return logging.Formatter.format(self, record)
        if record.levelno <= logging.INFO:
            return record.getMessage()
        if record.levelno <= logging.WARNING:
            return "WARNING: %s" % record.getMessage()
        return "ERROR: %s" % record.getMessage()

class Application():
    """Application"""
    _FORMATER = '%(levelname)s:%(module)s.%(funcName)s:%(lineno)d: %(message)s'

    def __init__(self):
        """Application startup"""
        logging.addLevelName(9, 'DEBUG1')
        logging.addLevelName(8, 'DEBUG2')
        logging.addLevelName(7, 'DEBUG3')
        logging.addLevelName(6, 'DEBUG4')
        logging.addLevelName(5, 'DEBUG5')
        fmt = _PyswdFormatter(Application._FORMATER)
        hdlr = logging.StreamHandler()
        hdlr.setLevel(1)
        hdlr.setFormatter(fmt)
        self._logger = logging.Logger('pyswd')
        self._logger.addHandler(hdlr)
        self._logger.setLevel(logging.WARNING)
        self._dev = None
        self._verbose = 0

    def print_device_info(self):
        """Show device informations"""
        self._logger.info(self._dev.version)
        self._logger.info("Target voltage: %0.2fV", self._dev.get_target_voltage())
        self._logger.info("COREID: 0x%08x", self._dev.get_coreid())

    def action_dump32(self, params):
        """Dump memory 32 bit"""
        if not params:
            raise PyswdException("dump32: no parameters")
        addr = convert_numeric(params[0])
        if len(params) == 1:
            if addr % 4:
                data = self._dev.read_mem(addr, 4)
                val = int.from_bytes(data, byteorder='little')
            else:
                val = self._dev.get_mem32(addr)
            print("%08x: %08x" % (addr, val))
        elif len(params) == 2:
            size = convert_numeric(params[1])
            test_alignment(size, "Size", 4)
            data = self._dev.read_mem(addr, size)
            print_buffer32(addr, data, verbose=self._verbose)
        else:
            raise PyswdException("dump32: too many parameters")

    def action_dump16(self, params):
        """Dump memory 16 bit"""
        if not params:
            raise PyswdException("dump16: no parameters")
        addr = convert_numeric(params[0])
        if len(params) == 1:
            data = self._dev.read_mem(addr, 2)
            val = int.from_bytes(data, byteorder='little')
            print("%08x: %04x" % (addr, val))
        elif len(params) == 2:
            size = convert_numeric(params[1])
            test_alignment(size, "Size", 2)
            data = self._dev.read_mem(addr, size)
            print_buffer16(addr, data, verbose=self._verbose)
        else:
            raise PyswdException("dump32: too many parameters")

    def action_dump8(self, params):
        """Dump memory 8 bit"""
        if not params:
            raise PyswdException("dump: no parameters")
        addr = convert_numeric(params[0])
        if len(params) == 1:
            data = self._dev.read_mem(addr, 1)
            print("%08x: %02x" % (addr, next(data)))
        elif len(params) == 2:
            size = convert_numeric(params[1])
            data = self._dev.read_mem(addr, size)
            print_buffer8(addr, data, verbose=self._verbose)
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
        self._dev.write_mem(addr, data)

    def action_fill8(self, params):
        """Fill memory with pattern"""
        if len(params) < 3:
            raise PyswdException("fill: require at least 3 parameters")
        addr = convert_numeric(params[0])
        size = convert_numeric(params[1])
        pattern = [int(i, 0) for i in params[2:]]
        self._dev.fill_mem(addr, size, pattern)

    def process_actions(self, actions):
        """Process all actions"""
        for action in actions:
            self._logger.debug(action)
            action_parts = action.split(":")
            action_name = "action_" + action_parts[0]
            if not hasattr(self, action_name):
                raise PyswdException("Action '%s' is not implemented" % action)
            getattr(self, action_name)(action_parts[1:])

    def start(self):
        """Application start point"""
        parser = argparse.ArgumentParser(
            prog=PROGNAME_STR, formatter_class=argparse.RawTextHelpFormatter,
            epilog=ACTIONS_HELP_STR)
        parser.add_argument('-V', '--version', action='version', version=VERSION_STR)
        parser.add_argument("-q", "--quite", action="store_true", help="quite output")
        parser.add_argument("-d", "--debug", action="count", help="increase debug output")
        parser.add_argument("-i", "--info", action="count", help="increase info output")
        parser.add_argument("-v", "--verbose", action="count", help="increase verbose output")
        parser.add_argument("-f", "--freq", type=int, default=1800000, help="set SWD frequency")
        parser.add_argument('action', nargs='*', help='actions will be processed sequentially')
        args = parser.parse_args()
        # print(args)
        if args.verbose is not None:
            self._verbose = args.verbose
        if args.quite:
            self._logger.setLevel(logging.ERROR)
        elif args.debug is not None:
            self._logger.setLevel(logging.DEBUG - (args.debug - 1))
        elif args.info is not None:
            self._logger.setLevel(logging.INFO - (args.info - 1))
        try:
            self._dev = swd.Stlink(swd_frequency=args.freq, logger=self._logger)
        except swd.stlinkcom.StlinkComNotFound:
            self._logger.error("No debugging device was found.")
            return 1
        except swd.stlinkcom.StlinkComException as err:
            self._logger.error("StlinkCom error: %s.", err)
            return 1
        self.print_device_info()
        try:
            self.process_actions(args.action)
        except swd.stlinkcom.StlinkComNotFound:
            self._logger.error("No debugging device was found.")
            return 1
        except swd.stlink.StlinkException as err:
            self._logger.error("Stlink error: %s.", err)
            return 1
        except swd.stlinkcom.StlinkComException as err:
            self._logger.error("StlinkCom error: %s.", err)
            return 1
        except PyswdException as err:
            self._logger.error("pyswd error: %s.", err)
            return 1
        return 0

def main():
    """application startup"""
    app = Application()
    exit(app.start())
