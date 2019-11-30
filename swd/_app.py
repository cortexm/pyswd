"""Application
"""

import sys
import time
import argparse
import itertools
import logging
import swd
import swd.stlink
import swd.stlink.usb
import swd.__about__
import swd.devices


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
        help="increase verbose output (standard printing)")
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
        "-c", "--cpu", type=str, action='append',
        help='set expected CPU type [eg: STM32F031G6, STM32H75]')
    parser.add_argument(
        "-S", "--svd", type=str,
        help='path to System View Description file (.svd)')
    parser.add_argument(
        "--no-load-svd", action="store_true",
        help='disable auto loading MCU .svd file')
    parser.add_argument(
        "--no-status-checking", action="store_true",
        help='disable checking status')
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
    if max_bits == 1:
        if num == 'True':
            return True
        if num == 'False':
            return False
    multi = UNITS.get(num[-1].upper())
    try:
        if multi:
            ret = int(num[:-1], 0) * multi
        else:
            ret = int(num, 0)
    except ValueError:
        raise PyswdException(f'number {num} has wrong format')
    if ret >= (2 ** max_bits):
        raise PyswdException(
            f'{num} is too big, number must fit into {max_bits:d} bits')
    return ret


class Application:
    """Application"""

    def __init__(self, args):
        """Application startup"""
        self._swd = None
        self._cortexm = None
        self._svd_file = args.svd
        self._verbose = args.verbose
        self._actions = args.action
        self._swd_frequency = args.freq
        self._serial_no = args.serial
        self._expected_parts = args.cpu
        self._load_svd = not args.no_load_svd
        self._status_checking = not args.no_status_checking
        self._logger = self._configure_loggers(args)

    @staticmethod
    def _configure_loggers(args):
        logging.basicConfig(format='%(levelname)s: %(message)s')
        # make names for all info levels
        for level in range(10):
            logging.addLevelName(logging.DEBUG - level, 'D')
            logging.addLevelName(logging.INFO - level, 'I')
            logging.addLevelName(logging.WARNING - level, 'W')
            logging.addLevelName(logging.ERROR - level, 'E')
        logger = logging.getLogger('swd:stlink:usb')
        logger.setLevel(logging.INFO + 1 - args.info)
        if args.debug:
            logger_usb = logging.getLogger('swd:stlink:usb')
            logger_usb.setLevel(logging.DEBUG + 1 - args.debug)
        if args.quite:
            logger.setLevel(logging.ERROR)
        return logger

    @property
    def cortexm(self):
        """return instance of CortexM or raise Error."""
        if not self._cortexm:
            raise PyswdException("This is not CortexM")
        return self._cortexm

    def _print_peripherals(self):
        """Print list of peripherals"""
        for peripheral in self._swd.io.peripherals:
            print(
                f"0x{peripheral.base_address:08x}:"
                f" {peripheral.name:12s}"
                f" ({peripheral.description:s})")

    @staticmethod
    def _print_registers(peripheral):
        """Print list of peripherals"""
        print(f"{peripheral.name:s}  ({peripheral.description:s})")
        for register in peripheral.registers:
            print(
                f"0x{register.address:08x}:"
                f" 0x{register.value:08x}"
                f" : {register.name:12s}"
                f" ({register.description})")

    @staticmethod
    def _print_fields(register):
        """Print list of peripherals"""
        register.discard_cache()
        register = register.cached
        print(
            f"0x{register.address:08x}:"
            f" 0x{register.value:08x}"
            f" : {register.peripheral.name:s}.{register.name:s}"
            f" ({register.description})")
        for field in register.fields:
            print(
                f"[{field.offset:02d}:{field.offset + field.width - 1:02d}]:"
                f" {field.str_value:10s}"
                f" : {field.name:12s}"
                f" ({field.description})")

    @staticmethod
    def _print_field(field):
        """Print list of peripherals"""
        register = field.register
        peripheral = register.peripheral
        print(
            f"[{field.width:d} bit{'s' if field.width > 1 else ''}]:"
            f" {field.str_value:s}"
            f" : {peripheral.name:s}.{register.name:s}.{field.name:s}"
            f" ({field.description})")

    def action_io(self, params):
        """Dump memory 32 bit

        [peripheral[:register[:field]]]
        """
        if not params:
            self._print_peripherals()
            return
        # register name
        reg = params.pop(0)
        reg_parts = reg.split('.')
        if len(reg_parts) > 3:
            raise PyswdException(
                f"Wrong register name `{reg}`")
        # list of registers:
        peripheral_name = reg_parts.pop(0)
        peripheral = self._swd.io.peripheral(peripheral_name)
        if not peripheral:
            raise PyswdException(
                f"Peripheral `{peripheral_name.upper()}` was not found")
        if not reg_parts:
            self._print_registers(peripheral)
            return
        # selected register
        register_name = reg_parts.pop(0)
        register = peripheral.register(register_name)
        if not register:
            raise PyswdException(
                f"Register `{register_name}` was not found")
        if not reg_parts:
            if params:
                # set register
                register.value = convert_numeric(params.pop(0))
                return
            # list of fields
            self._print_fields(register)
            return
        field_name = reg_parts.pop(0)
        field = register.field(field_name)
        if not field:
            raise PyswdException(
                f"field `{field_name.upper()}` was not found")
        if params:
            # set field
            field.value = convert_numeric(params.pop(0), field.width)
            return
        # print field value
        self._print_field(field)

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
        halted = self.cortexm.is_halted()
        if not halted:
            self.cortexm.halt()
        if len(params) == 1:
            if params[0] == 'all':
                for reg, val in self.cortexm.get_reg_all().items():
                    print("%s: %08x" % (reg, val))
            else:
                val = self.cortexm.get_reg(params[0])
                print("%s: %08x" % (params[0], val))
        elif len(params) == 2:
            val = convert_numeric(params[1])
            self.cortexm.set_reg(params[0], val)
        else:
            raise PyswdException("too many parameters")
        if not halted:
            self.cortexm.run()

    def action_reset(self, params):
        """Reset MCU"""
        if not params:
            self.cortexm.reset()
        elif params[0] == 'halt':
            self.cortexm.reset_halt()
        else:
            raise PyswdException("Wrong parameter")
        time.sleep(.05)

    def action_run(self, params):
        """Run core"""
        if not params:
            self.cortexm.run()
        elif params[0] == 'nodebug':
            self.cortexm.nodebug()
        else:
            raise PyswdException("Wrong parameter")

    def action_step(self, params):
        """Run core"""
        if not params:
            self.cortexm.step()
        else:
            for _ in range(convert_numeric(params[0])):
                self.cortexm.step()

    def action_halt(self, unused_params):
        """Run core"""
        self.cortexm.halt()

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
            self._logger.log(logging.INFO - 2, "ACTION: %s", action)
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
            driver = swd.stlink.Stlink(serial_no=self._serial_no)
            self._logger.log(logging.INFO - 1, driver.get_version())
            self._swd = swd.Swd(
                swd_frequency=self._swd_frequency,
                driver=driver)
            was_halted = None
            try:
                self._cortexm = swd.CortexM(self._swd, self._expected_parts)
            except swd.devices.cortexm.CortexMNotDetected as err:
                self._logger.warning(err)
            else:
                self._logger.info("CORE: %s", self.cortexm.name())
                if self.cortexm.part:
                    part = self.cortexm.part
                    self._logger.info("PART: %s", part.get_name())
                    self._logger.info(
                        "FLASH: %s KB",
                        part.get_flash_size() // swd.devices.memory.KILO)
                    if self._load_svd:
                        try:
                            part.load_svd()
                        except swd.devices.mcu.McuException as err:
                            self._logger.warning(err)
                was_halted = self.cortexm.is_halted()
                if was_halted:
                    self._logger.info("Core was halted.")
            if self._svd_file:
                self._swd.load_svd(self._svd_file)
            self._swd.status_checking = self._status_checking
            if self._actions:
                self.process_actions()
                is_halted = self.cortexm.is_halted()
                if was_halted != is_halted:
                    if is_halted:
                        self._logger.info("Core stay halted.")
                    else:
                        self._logger.info("Core is running.")
        except swd.stlink.usb.NoDeviceFoundException:
            self._logger.error("ST-Link not connected.")
        except swd.stlink.usb.MoreDevicesException as err:
            self._logger.error(
                "ST-Link Found more devices with these serial numbers:")
            for serial_number in err.serial_numbers:
                sys.stderr.write(f"  {serial_number}\n")
            sys.stderr.write("Use parameter: -s serial_no\n")
        except PyswdException as err:
            self._logger.error("Pyswd error: %s.", err)
        except swd.swd.SwdException as err:
            self._logger.error("Swd error: %s.", err)
        except swd.stlink.StlinkException as err:
            self._logger.error("Stlink error: %s.", err)
        except swd.stlink.usb.StlinkUsbException as err:
            self._logger.error("StlinkCom error: %s.", err)
        except swd.devices.mcu.McuException as err:
            self._logger.error("MCU error: %s.", err)
        else:
            return 0
        return 1


def main():
    """application startup"""
    args = _configure_argparse()
    app = Application(args)
    ret = app.start()
    sys.exit(ret)
