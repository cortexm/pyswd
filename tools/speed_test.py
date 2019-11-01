import time
import swd
import sys


def speed_test(dev, name, addr, size, max_time):
    times = []
    count = 0
    tm_total_start = time.perf_counter_ns()
    tm_total_current = 0
    while tm_total_current < max_time:
        sys.stderr.write(f" {name:<6s} | 0x{addr:08x} | {size // 1024:4d} KB | {int(100 * tm_total_current / max_time):5d} %\r")
        sys.stderr.flush()
        tm = time.perf_counter_ns()
        min(dev.read_mem(addr, size))
        tm = time.perf_counter_ns() - tm
        times.append(tm)
        count += 1
        tm_total_current = (time.perf_counter_ns() - tm_total_start) / 1000000000
    min_s = min(times) / 1000000000
    max_s = max(times) / 1000000000
    avg_s = (sum(times) / len(times)) / 1000000000
    med_s = sorted(times)[len(times) // 2] / 1000000000
    size_kb = size // 1024
    min_kbps = (size_kb) / max_s
    max_kbps = (size_kb) / min_s
    avg_kbps = (size_kb) / avg_s
    med_kbps = (size_kb) / med_s
    print(f" {name:<6s} | 0x{addr:08x} | {size_kb:4d} KB | {min_kbps:7.1f} | {max_kbps:7.1f} | {avg_kbps:7.1f} | {med_kbps:7.1f}")
    sys.stdout.flush()

def main():
    max_time = 10
    swd_frequency_mhz = 24
    dev = swd.Swd(swd_frequency=swd_frequency_mhz * 1000000, serial_no="00")
    print(f"{dev.get_version()} @ {swd_frequency_mhz} MHz")
    print("   KB/s |    address |    size | minimum | maximum | average | median")
    print("--------|-----------:|--------:|--------:|--------:|--------:|-------:")
    sys.stdout.flush()
    speed_test(dev, "ITCM",   0x00000000,   64 * 1024, max_time)
    speed_test(dev, "FLASH1", 0x08000000, 1024 * 1024, max_time)
    speed_test(dev, "FLASH2", 0x08100000, 1024 * 1024, max_time)
    speed_test(dev, "DTCM",   0x20000000,  128 * 1024, max_time)
    speed_test(dev, "AXI",    0x24000000,  512 * 1024, max_time)
    speed_test(dev, "SRAM1",  0x30000000,  128 * 1024, max_time)
    speed_test(dev, "SRAM2",  0x30020000,  128 * 1024, max_time)
    speed_test(dev, "SRAM3",  0x30040000,  32 * 1024, max_time)
    speed_test(dev, "SRAM4",  0x38000000,   64 * 1024, max_time)
    speed_test(dev, "BACKUP", 0x38000000,    4 * 1024, max_time)

if __name__ == "__main__":
    main()
