# HUD BENCH DRY-RUN — everything on the table, no case required

Goal: prove OLED + encoder + battery gauge + RTL-SDR end-to-end while the shell is
still unprinted. Order matters — each step assumes the previous one passed.

## 0. Wire it (deck powered OFF; wiring diagram: `2 - Docs/FieldDeck-HUD-Wiring.png`)

| Wire | From | To Pi header |
|---|---|---|
| OLED VCC | OLED | pin 1 (3V3) |
| OLED SDA | OLED | pin 3 (GPIO2) |
| OLED SCL | OLED | pin 5 (GPIO3) |
| OLED GND | OLED | pin 9 |
| EC11 A / CLK | encoder | pin 11 (GPIO17) |
| EC11 B / DT | encoder | pin 13 (GPIO27) |
| EC11 SW | encoder | pin 15 (GPIO22) |
| EC11 GND (common + switch GND) | encoder | pin 14 |
| KY-040 module only: VCC | module | pin 17 (3V3) |

Bare SR1230 note: its 5 solder lugs need wires attached — solder them, or use the
KY-040 module to skip soldering. Keep bare lugs from touching each other or the stack.
RTL-SDR: plug into a USB-A port (right-angle adapter fine on the bench); screw the
kit's dipole antenna cable straight onto the dongle's SMA.

Power the deck the normal way (battery or 27W PSU — PSU preferred while the SDR is in:
it adds ~300 mA).

## 1. Install the software (once)

```bash
cd "~/path/to/6 - HUD Software"     # wherever this folder lands on the Pi
sudo bash install.sh
sudo reboot
```

## 2. Prove the I2C bus sees both chips

```bash
i2cdetect -y 1
```
Expect TWO hits: **0x36** (X1201 fuel gauge — there even with nothing wired) and
**0x3c** (the OLED). Missing 0x3c → recheck pins 1/3/5/9. Missing 0x36 → X1201 seating.

## 3. Battery gauge (answers "battery % on screen" too)

```bash
fielddeck-bat            # one-shot:  battery  87.4%   4.087 V/cell   on battery
fielddeck-bat --watch    # live; plug/unplug the charger and watch 'charging' flip
```
The desktop pill appears top-right of the touch display after the next login/reboot
(green >40%, amber >15%, red below; ↑ while charging; drag it anywhere; right-click quits).

## 4. OLED + encoder together (bench mode = every event printed)

```bash
sudo systemctl stop fielddeck-hud
PYTHONPATH=/opt/fielddeck python3 -m fielddeck.hud --bench
```
- The OLED lights up on the BATTERY page (big %, bar, V/cell).
- Rotate the encoder: pages change (BATTERY → SYSTEM → NETWORK → SDR) and each
  step prints `encoder -> page ...` in the terminal. Backwards rotation = swap the
  A and B wires (pins 11/13) — that's the fix, not a fault.
- Short press: next page. Long press (1.2 s): display off; again: on.
- Ctrl-C to exit, then `sudo systemctl start fielddeck-hud` for the always-on service.

## 5. RTL-SDR + antenna

```bash
rtl_test -t            # must find 'RTL2838' and report Rafael Micro R820T/R828D tuner
rtl_test -s 2400000    # streams samples ~10 s; Ctrl-C. No 'lost samples' = healthy USB
```
Real reception check (FM broadcast, strongest thing on air — antenna at ~75 cm legs):
```bash
rtl_fm -f 104.1M -M wbfm -s 200k -r 48k - | aplay -r 48k -f S16_LE
```
(Pick any strong local station; audio out the touch display's speakers/HDMI. Ctrl-C.)
The HUD's SDR page should now say `RTL-SDR: OK`.

## 6. What "pass" looks like

Both I2C addresses seen · % and voltage plausible and 'charging' flips with the
charger · all four OLED pages render · encoder steps cleanly both directions ·
button short/long both work · rtl_test clean · FM audio audible. When all seven are
true, the HUD hardware is DONE — final assembly later is purely mechanical.

Troubleshooting quickies: OLED garbled → shorten jumpers/reseat; encoder double-steps
→ it's fine at HUD speeds (gpiozero debounces); `rtl_test` says device busy → reboot
(the DVB blacklist takes effect after reboot); widget missing → log out/in once.
