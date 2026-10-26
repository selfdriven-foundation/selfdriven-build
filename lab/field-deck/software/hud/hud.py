#!/usr/bin/env python3
"""Field Deck HUD — selfdriven.you

128x64 SSD1306 at 0x3C on i2c-1.
Battery from the X1201's MAX17040G+ fuel gauge at 0x36:
  VCELL 0x02 — 12 bits left-justified, 1.25 mV/LSB  -> volts = (raw >> 4) * 0.00125
  SOC   0x04 — high byte = whole percent            -> pct   = raw / 256
Both registers are big-endian; SMBus read_word_data returns little-endian, so swap.
(Confirmed against the MAX17040/MAX17041 datasheet, not from memory.)

The two 18650s are in PARALLEL — MAX17040 is a one-cell gauge, so cell voltage
reads 3.0-4.2 V, not 7.4 V. Geekworm's own thresholds: full 3.87-4.2, low 3.4-3.55.
"""
import socket
import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from smbus2 import SMBus

GAUGE = 0x36
PANEL = 0x3C
BUS = 1


def _swap(word):
    return ((word & 0xFF) << 8) | (word >> 8)


def battery(bus):
    """(percent, volts) or (None, None) if the gauge doesn't answer."""
    try:
        volts = (_swap(bus.read_word_data(GAUGE, 0x02)) >> 4) * 0.00125
        pct = _swap(bus.read_word_data(GAUGE, 0x04)) / 256.0
        return min(pct, 100.0), volts
    except Exception:
        return None, None


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(0.2)
        s.connect(("8.8.8.8", 80))          # no packet is sent, just routes
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()


def cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000.0
    except Exception:
        return None


def uptime():
    try:
        with open("/proc/uptime") as f:
            secs = int(float(f.read().split()[0]))
        d, rem = divmod(secs, 86400)
        h, rem = divmod(rem, 3600)
        m = rem // 60
        return f"{d}d{h:02d}h" if d else f"{h}h{m:02d}m"
    except Exception:
        return "--"


def draw(dev, bus):
    pct, volts = battery(bus)
    ip = ip_address()
    temp = cpu_temp()

    with canvas(dev) as d:
        d.text((2, 0), "FIELD DECK", fill="white")

        # battery gauge, top right
        x0, x1, y0, y1 = 92, 125, 0, 8
        d.rectangle((x0, y0, x1, y1), outline="white")
        d.rectangle((x1 + 1, y0 + 2, x1 + 2, y1 - 2), outline="white", fill="white")
        if pct is not None:
            w = int((x1 - x0 - 3) * pct / 100.0)
            if w > 0:
                d.rectangle((x0 + 2, y0 + 2, x0 + 2 + w, y1 - 2), fill="white")

        d.line((0, 12, 127, 12), fill="white")

        if pct is None:
            d.text((2, 18), "BAT  gauge silent", fill="white")
        else:
            d.text((2, 18), f"BAT  {pct:4.0f}%   {volts:.2f}V", fill="white")

        d.text((2, 32), f"IP   {ip}" if ip else "IP   offline", fill="white")

        t = f"{temp:.1f}C" if temp is not None else "--"
        d.text((2, 46), f"CPU  {t}    {uptime()}", fill="white")


def main():
    dev = ssd1306(i2c(port=BUS, address=PANEL), width=128, height=64)
    with SMBus(BUS) as bus:
        while True:
            try:
                draw(dev, bus)
            except Exception:
                pass          # a transient I2C hiccup must not kill the service
            time.sleep(2)


if __name__ == "__main__":
    main()
