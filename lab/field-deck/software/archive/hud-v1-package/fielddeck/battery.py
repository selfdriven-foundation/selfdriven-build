"""X1201 UPS fuel gauge reader (MAX17048-compatible, I2C addr 0x36).

The SupTronics/Geekworm X1201 exposes a fuel gauge on the Pi's I2C-1 bus:
  reg 0x02 VCELL — cell voltage,  LSB 78.125 uV per cell (word, big-endian)
  reg 0x04 SOC   — state of charge, 1/256 % per LSB       (word, big-endian)
Charging detection: primary = voltage trend (rising while >4.0 V/cell is a
charger present); optional = a power-loss-detect GPIO if wired (config).
"""
import time

I2C_BUS = 1
ADDR = 0x36
_VCELL = 0x02
_SOC = 0x04


class Gauge:
    def __init__(self, bus_num: int = I2C_BUS, addr: int = ADDR):
        from smbus2 import SMBus          # import here so --help works without deps
        self._bus = SMBus(bus_num)
        self._addr = addr
        self._hist = []                    # (t, volts) for trend detection

    def _word(self, reg: int) -> int:
        raw = self._bus.read_word_data(self._addr, reg)
        return ((raw & 0xFF) << 8) | (raw >> 8)      # swap to big-endian

    def voltage(self) -> float:
        """Pack-side per-cell voltage in volts (2S pack shares one gauge node)."""
        return self._word(_VCELL) * 78.125e-6

    def soc(self) -> float:
        return min(100.0, self._word(_SOC) / 256.0)

    def charging(self) -> bool | None:
        """True/False from voltage trend; None until enough history (~30 s)."""
        v = self.voltage()
        now = time.monotonic()
        self._hist.append((now, v))
        self._hist = [(t, x) for (t, x) in self._hist if now - t < 90]
        if len(self._hist) < 4 or self._hist[-1][0] - self._hist[0][0] < 25:
            return None
        dv = self._hist[-1][1] - self._hist[0][1]
        if dv > 0.004:
            return True
        if dv < -0.004:
            return False
        return v > 4.05                    # holding high and flat = on charger, full-ish

    def read(self) -> dict:
        v = self.voltage()
        return {"volts": round(v, 3), "percent": round(self.soc(), 1),
                "charging": self.charging()}


def main():
    import argparse, json, sys
    ap = argparse.ArgumentParser(description="Field Deck battery status (X1201 fuel gauge)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--watch", action="store_true", help="refresh every 5 s")
    args = ap.parse_args()
    try:
        g = Gauge()
    except FileNotFoundError:
        sys.exit("I2C bus not found — enable I2C (sudo raspi-config nonint do_i2c 0) and reboot.")
    while True:
        try:
            d = g.read()
        except OSError:
            sys.exit("No response at 0x36 — is the X1201 seated? Check: i2cdetect -y 1")
        if args.json:
            print(json.dumps(d), flush=True)
        else:
            chg = {True: "charging", False: "on battery", None: "…"}[d["charging"]]
            print(f"battery {d['percent']:5.1f}%   {d['volts']:.3f} V/cell   {chg}", flush=True)
        if not args.watch:
            break
        time.sleep(5)


if __name__ == "__main__":
    main()
