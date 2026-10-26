# Config

What the reference deck changes from a fresh Raspberry Pi OS. The reasons are in Steps 4, 5 and 7 of the
[build guide](../BUILD_GUIDE.md).

## `boot-firmware-config.txt`

The lines added at the end of `/boot/firmware/config.txt`. Add them with `sudo nano /boot/firmware/config.txt`, then
reboot. Check:

```bash
tail -n 12 /boot/firmware/config.txt
pinctrl get 16          # expect: op dl pd | lo
arecord -l              # expect an adau7002 card (only with the microphone fitted)
```

The `dtoverlay=adau7002-simple` line is only for the INMP441 microphone. **Never** use
`dtoverlay=googlevoicehat-soundcard` instead: it drives GPIO16, the X1201's charge control.

## `eeprom.conf`

The bootloader config, exactly as read back on the deck with `sudo rpi-eeprom-config` (10 October 2026). The three lines
that matter:

| Line | Why |
|---|---|
| `BOOT_ORDER=0xf416` | NVMe first, then SD, then USB, then restart |
| `PSU_MAX_CURRENT=5000` | Tells the Pi it has 5 A — the X1201 feeds it through pogo pins, so the Pi can't ask the supply |
| `POWER_OFF_ON_HALT=1` | `sudo poweroff` really cuts the power (otherwise the X1201 keeps powering the halted Pi) |

`BOOT_UART=1` and `NET_INSTALL_AT_POWER_ON=1` were already there.

Edit yours with `sudo rpi-eeprom-config --edit`, or write the lines to a file and run
`sudo rpi-eeprom-config --apply <file>`; then reboot and read it back with `sudo rpi-eeprom-config`.
