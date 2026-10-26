"""Field Deck HUD service: SSD1306 OLED pages + EC11 encoder.

Wiring (locked in 2 - Docs/FieldDeck-HUD-Wiring.png):
  OLED  VCC->pin1 (3V3)  SDA->pin3 (GPIO2)  SCL->pin5 (GPIO3)  GND->pin9   addr 0x3C
  EC11  A/CLK->pin11 (GPIO17)  B/DT->pin13 (GPIO27)  SW->pin15 (GPIO22)  GND->pin14
        (KY-040 module only: VCC->pin17 3V3)
Pages: BATTERY / SYSTEM / NETWORK / SDR.  Rotate = change page, short press =
next page, long press (>1.2 s) = display sleep/wake.
Run modes:  python3 -m fielddeck.hud            (service)
            python3 -m fielddeck.hud --bench    (verbose bench test, Ctrl-C to stop)
"""
import os, re, socket, subprocess, sys, time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
from gpiozero import RotaryEncoder, Button

from .battery import Gauge

PAGES = ["BATTERY", "SYSTEM", "NETWORK", "SDR"]
LONG_PRESS = 1.2


def _run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=4).stdout.strip()
    except Exception:
        return ""


def cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000.0
    except OSError:
        return None


def throttled_flag():
    out = _run(["vcgencmd", "get_throttled"])
    m = re.search(r"0x([0-9a-fA-F]+)", out)
    return int(m.group(1), 16) if m else None


def cpu_load():
    try:
        with open("/proc/loadavg") as f:
            return float(f.read().split()[0])
    except OSError:
        return None


def mem_used_frac():
    try:
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                k, v = line.split(":", 1)
                info[k] = int(v.strip().split()[0])
        return 1.0 - (info["MemAvailable"] / info["MemTotal"])
    except Exception:
        return None


def ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 80))       # no traffic actually sent
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def ssid():
    out = _run(["iwgetid", "-r"])
    return out or None


def sdr_present():
    out = _run(["lsusb"])
    for line in out.splitlines():
        if "RTL2838" in line or "Realtek" in line and "2838" in line:
            return line.split(":", 1)[-1].strip()[:20]
    return None


class Hud:
    def __init__(self, bench=False):
        self.bench = bench
        self.device = ssd1306(i2c(port=1, address=0x3C))
        self.font = ImageFont.load_default()
        try:
            self.big = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
            self.mid = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        except OSError:
            self.big = self.mid = self.font
        try:
            self.gauge = Gauge()
        except Exception as e:
            self.gauge = None
            self.log(f"battery gauge unavailable: {e}")
        self.page = 0
        self.awake = True
        self._press_t = None

        self.enc = RotaryEncoder(17, 27, max_steps=0, wrap=False)
        self.enc.when_rotated_clockwise = lambda: self.step(+1)
        self.enc.when_rotated_counter_clockwise = lambda: self.step(-1)
        self.btn = Button(22, pull_up=True, bounce_time=0.03)
        self.btn.when_pressed = self._pressed
        self.btn.when_released = self._released

    def log(self, msg):
        if self.bench:
            print(msg, flush=True)

    def step(self, d):
        self.page = (self.page + d) % len(PAGES)
        self.log(f"encoder -> page {PAGES[self.page]}")
        self.draw()

    def _pressed(self):
        self._press_t = time.monotonic()

    def _released(self):
        if self._press_t is None:
            return
        held = time.monotonic() - self._press_t
        self._press_t = None
        if held >= LONG_PRESS:
            self.awake = not self.awake
            self.log(f"button long press -> display {'on' if self.awake else 'off'}")
            (self.device.show if self.awake else self.device.hide)()
        else:
            self.log("button press -> next page")
            self.step(+1)

    # ---- pages ----
    def draw(self):
        if not self.awake:
            return
        with canvas(self.device) as d:
            name = PAGES[self.page]
            d.text((0, 0), name, font=self.font, fill=255)
            d.line((0, 10, 127, 10), fill=60)
            getattr(self, "page_" + name.lower())(d)

    def page_battery(self, d):
        if not self.gauge:
            d.text((0, 24), "gauge offline (0x36)", font=self.mid, fill=255)
            return
        try:
            s = self.gauge.read()
        except OSError:
            d.text((0, 24), "read error @0x36", font=self.mid, fill=255)
            return
        d.text((0, 16), f"{s['percent']:.0f}%", font=self.big, fill=255)
        d.text((0, 48), f"{s['volts']:.2f} V/cell", font=self.mid, fill=255)
        chg = s["charging"]
        tag = "CHG" if chg else ("BAT" if chg is False else "...")
        d.text((100, 16), tag, font=self.font, fill=255)
        # battery outline
        d.rectangle((96, 34, 124, 46), outline=255)
        d.rectangle((124, 38, 127, 42), fill=255)
        w = int(27 * max(0.0, min(1.0, s["percent"] / 100)))
        if w:
            d.rectangle((97, 35, 97 + w, 45), fill=255)

    def page_system(self, d):
        t = cpu_temp(); ld = cpu_load(); mf = mem_used_frac(); th = throttled_flag()
        d.text((0, 14), f"temp {t:.1f} C" if t is not None else "temp ?", font=self.mid, fill=255)
        d.text((0, 27), f"load {ld:.2f}" if ld is not None else "load ?", font=self.mid, fill=255)
        d.text((0, 40), f"mem  {mf*100:.0f}%" if mf is not None else "mem ?", font=self.mid, fill=255)
        if th:
            d.text((0, 53), f"THROTTLED 0x{th:x}", font=self.font, fill=255)

    def page_network(self, d):
        ip = ip_addr(); ss = ssid()
        d.text((0, 16), ip or "no network", font=self.mid, fill=255)
        d.text((0, 32), (ss and f"ssid {ss}") or "", font=self.mid, fill=255)
        d.text((0, 48), socket.gethostname(), font=self.mid, fill=255)

    def page_sdr(self, d):
        s = sdr_present()
        d.text((0, 18), "RTL-SDR: " + ("OK" if s else "not found"), font=self.mid, fill=255)
        if s:
            d.text((0, 34), s, font=self.font, fill=255)
            d.text((0, 48), "rtl_test -t to verify", font=self.font, fill=255)

    def run(self):
        self.log("HUD up: rotate = pages, press = next, long-press = sleep")
        while True:
            self.draw()
            time.sleep(2 if PAGES[self.page] == "BATTERY" else 3)


def main():
    bench = "--bench" in sys.argv
    hud = Hud(bench=bench)
    try:
        hud.run()
    except KeyboardInterrupt:
        hud.device.clear()


if __name__ == "__main__":
    main()
