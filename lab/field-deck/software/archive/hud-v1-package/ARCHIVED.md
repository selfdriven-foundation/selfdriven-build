# Archived: fielddeck-hud v1.0 (15 September 2026)

**Never installed on the reference deck.** The deck runs the one-page HUD in [`software/hud/`](../../hud/README.md).
Kept here so the work isn't lost.

What it has that the running HUD doesn't: four pages (battery, system, network, SDR), the EC11 encoder (turn to change
page, long press to sleep the screen), a charging indicator from the voltage trend, the throttle state, the Wi-Fi name,
an RTL-SDR check, a `fielddeck-bat` command and a battery pill on the desktop. `sudo bash install.sh` installs it to
`/opt/fielddeck` and enables `fielddeck-hud.service`.

Before using it:

- **Don't install it next to `software/hud/`** — both drive the same OLED.
- `fielddeck/battery.py`'s comment says "MAX17048" and "2S pack": the X1201 has a MAX17040G+ and its cells are in
  **parallel**. The maths is the same for both chips; only the comment is wrong.
- `DRYRUN.md` step 5 plays sound through "the touch display's speakers" — the Touch Display 2 has none (errata E32).
- The encoder needs GPIO17, 27 and 22 (pins 11, 13, 15) on the buried header, so fitting it means opening the stack.
