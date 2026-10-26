# HUD

The small OLED on top of the deck. One page, refreshed every 2 seconds:

```
FIELD DECK        [battery icon]
BAT 98% 4.16V
IP 192.168.1.50
CPU 48.0C 6h48m
```

| File | What it is |
|---|---|
| `hud.py` | The HUD. SSD1306 128 × 64 at `0x3C` on I2C bus 1; the battery from the X1201's MAX17040G+ gauge at `0x36` (VCELL register 0x02 at 1.25 mV/LSB, SOC register 0x04 in 1/256 %) |
| `hud.service` | The systemd unit that starts it at boot and restarts it if it stops. It runs as `YOURUSER` from `/home/YOURUSER/hud`; the install line below puts your own user name in |

The two 18650 cells are in parallel and the MAX17040 is a one-cell gauge, so the voltage reads 3.0–4.2 V, never 7.4 V.

## Install

Wiring and the I2C check (`i2cdetect -y 1` shows `36` and `3c`) are in Step 6 of the [build guide](../../BUILD_GUIDE.md).

```bash
python3 -m venv --system-site-packages ~/hud
~/hud/bin/pip install luma.oled smbus2
cp hud.py ~/hud/hud.py
sed "s/YOURUSER/$USER/g" hud.service | sudo tee /etc/systemd/system/hud.service > /dev/null   # your user instead of YOURUSER
sudo systemctl daemon-reload
sudo systemctl enable --now hud
```

- Restart after a change: `sudo systemctl restart hud`
- See what it's doing: `systemctl status hud` and `journalctl -u hud -e`

## Which way up

Fit the OLED with its header pins at the **top** — in the MK-I case they must be, as there is no room for the plugs
below — and on this build the picture is upright. If yours is upside down, add `rotate=2` to the display line:

```bash
sed -i 's/height=64)/height=64, rotate=2)/' ~/hud/hud.py && sudo systemctl restart hud
```

(On the reference deck the picture is upright; it isn't recorded whether the board was turned or `rotate=2` was added.
This copy has no `rotate`.)

## The older package

`../archive/hud-v1-package/` is a larger HUD (four pages, an encoder, a desktop battery widget) written in September and
never installed on this deck. Don't run both: they would fight over the same screen.
