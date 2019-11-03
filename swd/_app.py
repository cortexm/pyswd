"""Application
"""

import sys
import time
import argparse
import itertools
import swd
import swd.stlink
import swd.stlink.usb
import swd.__about__


class PyswdException(Exception):
    """Exception"""


_VERSION_STR = "%s %s (%s <%s>)" % (
    swd.__about__.APP_NAME,
    swd.__about__.VERSION,
    swd.__about__.AUTHOR,
    swd.__about__.AUTHOR_EMAIL)
_ACTIONS_HELP_STR = """
list of available actions:
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
"""
# TODO unimplemented actions:
#   fill:{addr}:{size}:{pattern}      fill memory with 8 bit pattern
#   fill16:{addr}:{size}:{pattern}    fill memory with 16 bit pattern
#   fill32:{addr}:{size}:{pattern}    fill memory with 32 bit pattern
#   read:{addr}:{size}:{file}      read memory with size into file
#   read:sram[:{size}]:{file}      read SRAM into file
#   read:flash[:{size}]:{file}     read FLASH into file
#   write:{file.srec}     write SREC file into memory
#   write:{addr}:{file}   write binary file into memory
#   write:sram:{file}     write binary file into SRAM memory


def _configure_argparse():
    """configure and process command line arguments"""
    parser = argparse.ArgumentParser(
        prog=swd.__about__.APP_NAME,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=_ACTIONS_HELP_STR)
    parser.add_argument(
        "-V", "--version", action='version', version=_VERSION_STR)
    parser.add_argument(
        "-q", "--quite", action="store_true",
        help="quite output")
    parser.add_argument(
        "-i", "--info", action="count", default=1,
        help="increase info output")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="increase verbose output")
    parser.add_argument(
        "-d", "--debug", action="count", default=0,
        help="increase debug output")
    parser.add_argument(
        "-f", "--freq", type=int,
        help="set SWD frequency")
    parser.add_argument(
        "-s", "--serial", type=str, default='',
        help="select ST-Link by serial number")
    parser.add_argument(
        'action', nargs='*',
        help='actions will be processed sequentially')
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
        chr(d) if 32 <= d < 127 else '.'
        for d in chunk])


def test_alignment(num, param_name, align):
    """Test if number is aligned"""
    if num % align:
        raise PyswdException(
            '%s must be aligned to %d Bytes' % (param_name, align))


UNITS = {
    'K': 1024,
    'M': 1024 ** 2,
    'G': 1024 ** 3,
}


def convert_numeric(num, max_bits=32):
    """Convert string number into integer"""
    ret = 0
    if not num:
        return 0
    multi = UNITS.get(num[-1].upper())
    try:
        if multi:
            ret = int(num[:-1], 0) * multi
        else:
            ret = int(num, 0)
    except ValueError:
        raise PyswdException('number "%s" has wrong format' % num)
    if ret >= pow(2, max_bits):
        raise PyswdException(
            '%s is too big, number must fit into %d bits' % (num, max_bits))
    return ret


class Application:
    """Application"""

    def __init__(self, args):
        """Application startup"""
        self._swd = None
        self._cortexm = None
        self._info = args.info
        self._verbose = args.verbose
        self._debug = args.debug
        if args.quite:
            self._info = -1
            self._verbose = -1
            self._debug = -1
        self._actions = args.action
        self._swd_frequency = args.freq
        self._serial_no = args.serial

    def print_info(self, msg, level=1, prefix="I: "):
        """Print info string"""
        if self._info >= level:
            sys.stderr.write(f"{prefix}{msg}\n")

    def print_verbose(self, msg, level=1, prefix="V: "):
        """Print info string"""
        if self._verbose >= level:
            sys.stderr.write(f"{prefix}{msg}\n")

    def print_debug(self, msg, level=1, prefix="D: "):
        """Print info string"""
        if self._debug >= level:
            sys.stderr.write(f"{prefix}{msg}\n")

    def print_warning(self, msg, prefix="W: "):
        """Print info string"""
        if self._info >= 0:
            sys.stderr.write(f"{prefix}{msg}\n")

    def print_error(self, msg, prefix="E: "):
        """Print info string"""
        sys.stderr.write(f"{prefix}{msg}\n")

    def print_io(self, reg_name):
        """Print IO register content"""
        bitf_reg = self._swd.reg(reg_name)
        bitf_reg.tmp_load()
        print("%s:" % reg_name)
        for reg in bitf_reg.tmp.get_registers():
            print("%16s: %8x" % (reg, bitf_reg.tmp.get(reg)))

    def print_buffer(self, addr, data, hex_line=hex_line8):
        """Print buffer in hex and ASCII"""
        prev_chunk = []
        same_chunk = False
        for chunk in chunks(data, 16):
            if self._verbose > 0 or prev_chunk != chunk:
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
                sys.stderr.write('%08x\r' % addr)
                sys.stderr.flush()
            addr += len(chunk)
        if same_chunk or self._verbose > 1:
            print('%08x' % addr)


    def action_dump32(self, params):
        """Dump memory 32 bit"""
        if not params:
            raise PyswdException("no parameters")
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
            self.print_buffer(addr, data, hex_line32)
        else:
            raise PyswdException("too many parameters")

    def action_dump16(self, params):
        """Dump memory 16 bit"""
        if not params:
            raise PyswdException("no parameters")
        addr = convert_numeric(params[0])
        if len(params) == 1:
            data = self._swd.read_mem(addr, 2)
            val = int.from_bytes(data, byteorder='little')
            print("%08x: %04x" % (addr, val))
        elif len(params) == 2:
            size = convert_numeric(params[1])
            test_alignment(size, "Size", 2)
            data = self._swd.read_mem(addr, size)
            self.print_buffer(addr, data, hex_line16)
        else:
            raise PyswdException("too many parameters")

    def action_dump8(self, params):
        """Dump memory 8 bit"""
        if not params:
            raise PyswdException("no parameters")
        addr = convert_numeric(params[0])
        if len(params) == 1:
            data = self._swd.read_mem(addr, 1)
            print("%08x: %02x" % (addr, next(data)))
        elif len(params) == 2:
            size = convert_numeric(params[1])
            data = self._swd.read_mem(addr, size)
            self.print_buffer(addr, data, hex_line8)
        else:
            raise PyswdException("too many parameters")

    def action_dump(self, params):
        """Dump memory"""
        if not params:
            raise PyswdException("no parameters")
        if len(params) == 1:
            self.action_dump32(params)
        elif len(params) == 2:
            self.action_dump8(params)
        else:
            raise PyswdException("too many parameters")

    def action_set32(self, params):
        """Fill memory with data"""
        if len(params) < 2:
            raise PyswdException("require at least 2 parameters")
        addr = convert_numeric(params[0])
        if addr % 4 == 0 and len(params) == 2:
            self._swd.set_mem32(addr, convert_numeric(params[1], 32))
        else:
            data = []
            for i in params[1:]:
                data.extend(
                    convert_numeric(i, 32).to_bytes(4, byteorder='little'))
            self._swd.write_mem(addr, data)

    def action_set16(self, params):
        """Fill memory with data"""
        if len(params) < 2:
            raise PyswdException("require at least 2 parameters")
        addr = convert_numeric(params[0])
        data = []
        for i in params[1:]:
            data.extend(convert_numeric(i, 16).to_bytes(2, byteorder='little'))
        self._swd.write_mem(addr, data)

    def action_set8(self, params):
        """Fill memory with data"""
        if len(params) < 2:
            raise PyswdException("require at least 2 parameters")
        addr = convert_numeric(params[0])
        data = [convert_numeric(i, 8) for i in params[1:]]
        self._swd.write_mem(addr, data)

    def action_set(self, params):
        """Dump memory"""
        if not params:
            raise PyswdException("no parameters")
        if len(params) == 2:
            self.action_set32(params)
        elif len(params) > 2:
            self.action_set8(params)
        else:
            raise PyswdException("too many parameters")

    def action_fill8(self, params):
        """Fill memory with pattern"""
        if len(params) < 3:
            raise PyswdException("require at least 3 parameters")
        addr = convert_numeric(params[0])
        size = convert_numeric(params[1])
        pattern = bytes([convert_numeric(i, 8) for i in params[2:]])
        self._swd.fill_mem(addr, pattern, size)

    def action_reg(self, params):
        """Read/Write core register"""
        if not params:
            raise PyswdException("no parameters")
        halted = self._cortexm.is_halted()
        if not halted:
            self._cortexm.halt()
        if len(params) == 1:
            if params[0] == 'all':
                for reg, val in self._cortexm.get_reg_all().items():
                    print("%s: %08x" % (reg, val))
            else:
                val = self._cortexm.get_reg(params[0])
                print("%s: %08x" % (params[0], val))
        elif len(params) == 2:
            val = convert_numeric(params[1])
            self._cortexm.set_reg(params[0], val)
        else:
            raise PyswdException("too many parameters")
        if not halted:
            self._cortexm.run()

    def action_reset(self, params):
        """Reset MCU"""
        if not params:
            self._cortexm.reset()
        elif params[0] == 'halt':
            self._cortexm.reset_halt()
        else:
            raise PyswdException("Wrong parameter")
        time.sleep(.05)

    def action_run(self, params):
        """Run core"""
        if not params:
            self._cortexm.run()
        elif params[0] == 'nodebug':
            self._cortexm.nodebug()
        else:
            raise PyswdException("Wrong parameter")

    def action_step(self, params):
        """Run core"""
        if not params:
            self._cortexm.step()
        else:
            for _ in range(convert_numeric(params[0])):
                self._cortexm.step()

    def action_halt(self, unused_params):
        """Run core"""
        self._cortexm.halt()

    @staticmethod
    def action_sleep(params):
        """Wait selected time and then continue"""
        if not params:
            time.sleep(1)
        elif len(params) > 1:
            raise PyswdException("too many parameters")
        else:
            try:
                time.sleep(float(params[0]))
            except ValueError:
                raise PyswdException("wrong float value: %s" % params[0])

    def process_actions(self):
        """Process all actions"""
        for action in self._actions:
            self.print_debug("ACTION: %s" % action)
            action_parts = action.split(":")
            action_name = "action_" + action_parts[0]
            if not hasattr(self, action_name):
                raise PyswdException("action '%s' is not implemented" % action)
            try:
                getattr(self, action_name)(action_parts[1:])
            except PyswdException as err:
                raise PyswdException("%s: %s" % (action_parts[0], err))

    def start(self):
        """Application start point"""
        try:
            self._swd = swd.Swd(
                swd_frequency=self._swd_frequency,
                serial_no=self._serial_no,
                debug=self._debug)
            self.print_info(self._swd.get_version(), level=2)
            idcode = self._swd.get_idcode()
            if idcode == 0:
                raise PyswdException(
                    "No IDCODE, probably MCU is not connected")
            self._cortexm = swd.CortexM(self._swd)
            was_halted = self._cortexm.is_halted()
            if was_halted:
                self.print_info("Core is halted.")
            if self._actions:
                self.process_actions()
                is_halted = self._cortexm.is_halted()
                if was_halted != is_halted:
                    if is_halted:
                        self.print_info("Core stay halted.")
                    else:
                        self.print_info("Core is running.")
        except swd.stlink.usb.NoDeviceFoundException:
            self.print_error("ST-Link not connected.")
        except swd.stlink.usb.MoreDevicesException as err:
            self.print_error(
                f"ST-Link Found more devices with these serial numbers:")
            for serial_number in err.serial_numbers:
                self.print_error(serial_number, prefix="  ")
            self.print_error("Use parameter: -s serial_no", prefix="")
        except PyswdException as err:
            self.print_error(f"pyswd error: {err}.")
        except swd.stlink.driver.StlinkException as err:
            self.print_error(f"Stlink error: {err}.")
        except swd.stlink.usb.StlinkComException as err:
            self.print_error(f"StlinkCom error: {err}.")
        else:
            return 0
        return 1


def main():
    """application startup"""
    args = _configure_argparse()
    app = Application(args)
    ret = app.start()
    exit(ret)
