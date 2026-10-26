# Field Deck — errata

*All corrections to the original public guide — first at `selfdriven.you/cyberdeck-build-guide`, now
[selfdriven.build/cyberdeck-build-guide](https://selfdriven.build/cyberdeck-build-guide), source
[`docs/pages/cyberdeck-build-guide.html`](../../../docs/pages/cyberdeck-build-guide.html) in this repository — as of guide v3,
20 October 2026.*

E1–E14 came from the June desk audit and the August field findings (`Field-Deck-Guide-Errata.docx`), E15–E24 from
August–September (the v2 change list, 28 September 2026). E25–E37 are new in v3, found while building the MK-I case and
adding the microphone (October 2026). Every v3 fix is already worked into [BUILD_GUIDE.md](../BUILD_GUIDE.md); this file
is the trail.

Severity: **HIGH** = can damage something or stop the build · **MED** = costs real time · **LOW** = annoyance.

## E1–E24: status in v3

| ID | Sev | Topic | Status in v3 | Where in v3 |
|---|---|---|---|---|
| E1 | HIGH | `BOOT_ORDER` comment wrong | **Confirmed.** The real default is `0xf461`; use `0xf416` (NVMe → SD → USB). Read back on the deck 10 Oct | Step 4, Step 5 |
| E2 | HIGH | A 2280 NVMe won't fit the HAT+ | Untested — the kit's 2230 was used | Parts |
| E3 | HIGH | Cooler + HAT + UPS stacking | **Confirmed** | Step 2 |
| E4 | MED | Flat-top cells | **Fix held** (flat-top fits). Protected cells never tried — *untested*, not "confirmed" or "refuted" | Parts |
| E5 | MED | A2 32 GB microSD scarce | Untested — an A1 card was used | Parts |
| E6 | MED | Cost ballpark | **Superseded** — about A$1,260 for the sourced parts | Parts |
| E7 | LOW | Display is portrait-native | **Confirmed**; the method is E23 | Step 3 |
| E8 | LOW | A 3B model needs 8 GB | **Confirmed** — llama3.2:3b answers offline on battery and is the voice assistant's model | Step 7 |
| E9 | HIGH | No 5 V / 5 A PSU in the BOM | **Confirmed**; the official 27 W supply is a BOM line | Parts |
| E10 | HIGH | X1201 fixed silver posts | **Confirmed**, with `PSU_MAX_CURRENT=5000`. Note: when the stack was opened on 10 Oct the X1201's silver standoffs came away with the board, unscrewed from the spacers below — re-check this wording against your own X1201 | Step 2, Step 5 |
| E11 | HIGH | SSH off by default | **Confirmed** (Imager's *Services* tab) | Step 1 |
| E12 | MED | Assembly order | **Confirmed**; refined by E18 | Step 2 |
| E13 | MED | The display needs the J1 power lead | **Confirmed.** J1 is a 3-way plug on pins 2-4-6 (pin 4 covered) and doubles as the pin-1 landmark (E17) | Step 2 |
| E14 | MED | NVMe migration missing | **Confirmed** — `rpi-clone` | Step 4 |
| E15 | LOW | GPIO16 charge control | Unchanged: `gpio=16=op,dl` is a precaution; the test that would settle it hasn't been run. New: never load an overlay that drives GPIO16 (E31) | Step 5, Rules |
| E16 | HIGH | Lifting the Pi; live header | **Confirmed.** The stack was opened and closed again on 10–11 Oct with no PCIe fault — the ribbon was unlatched first (E27). "Power off" only really means off with E26 | Rules, Step 2 |
| E17 | HIGH | Finding pin 1 | **Field-proven again**: the J1 landmark placed all six microphone pins correctly | Rules, Step 2, Step 6 |
| E18 | MED | Header unreachable once the HAT is on | Partly answered: the leads sit on the 16 mm stacking header's long pins between the Pi and the HAT; the HAT's own header holes are empty. A HAT seated on the stacking header is still untested | Step 2 |
| E19 | MED | No audio path | **Solved, by another route:** an INMP441 I2S microphone on the header plus a Bluetooth speaker through PipeWire (E31, E32) | Step 7 |
| E20 | MED | No runtime figures | Unchanged — about 4.7 h idle is still an estimate; a timed run is owed | Step 5, Step 10 |
| E21 | MED | Jumper length | 150 mm reached the microphone in the MK-I chin; the MK-I HUD needs four 150–200 mm extension leads. Keep "measure your route" | Parts |
| E22 | LOW | SSH and networking | Kept; extended by E34 and E35 | Step 1, Everyday use |
| E23 | LOW | Rotation method | **Confirmed** — Control Centre → Screens → Orientation | Step 3 |
| E24 | MED | No HUD software | **Resolved** for the deck: `software/hud/` (one page, run by `hud.service`). The earlier four-page package is archived, never installed | Step 6 |

## E25–E37: new in v3

| ID | Sev | Where | Issue | Fix | Evidence · confidence |
|---|---|---|---|---|---|
| E25 | LOW | Step 1, Step 3 | The reference deck runs Raspberry Pi OS on Debian 13 "trixie" (13.6). Its desktop settings are in *Control Centre* (Screens, Display), so older paths in the guide no longer match. | Name trixie; use the Control Centre paths. | `/etc/os-release` on the deck · verified |
| E26 | HIGH | Step 5, Rules | With the Pi 5's default `POWER_OFF_ON_HALT=0`, `sudo poweroff` only halts the Pi and the X1201 keeps powering it: a red LED on, 3.3 V still live, the OLED frozen. The X1201 also starts the deck when power returns. | Add `POWER_OFF_ON_HALT=1` to the bootloader config next to `PSU_MAX_CURRENT=5000`; read it back. Before any header work: charger out, then power off, then check every light is off. | Field-proven 10 Oct ("all dark, OLED off"). The ~1.5 W halted draw is from published measurements, not measured here |
| E27 | MED | Step 2 | No way back to a header buried under the HAT, e.g. to add a microphone. | The opening sequence: power off; X1201 off (4 screws); **unlatch the PCIe ribbon at the Pi first**; lift the Pi with the display ribbon left in, in a loose arc; fit the leads (pin 1 from J1); back in reverse, cells on the header side. | Field-proven once (10–11 Oct) |
| E28 | LOW | Step 5 | On the charger the battery reading stops in the mid-to-high 90s, never 100 %. | Normal: the X1201 stops charging near 4.23 V and restarts at 4.1 V. Read the voltage, not the %. | Build Log #66 + one reading (98 % at 4.16 V) · vendor spec |
| E29 | MED | Step 10 | The power check never tests the closed case under load while charging. | A 30-minute soak: full load, charger in, case closed. Pass: `throttled=0x0`, CPU under 80 °C, cells at or under 45 °C. About 48–50 °C idle is normal. | The heat rise (~25 K at 10 W) is a calculation; no soak result recorded yet |
| E30 | MED | Step 6, case design | The OLED module, measured from a flat photo: board 27.3 × 27.6 mm, holes 23.36 × 23.80 mm apart and 2.0 mm across, glass 26.7 × 19.48 mm. The caliper figures used before were 2–3 mm short. | Measure your own module against a reference in the same plane; hold it with foam tape where screws can't be reached; fit it header-up (or `rotate=2`). | Photo measurement · medium-high |
| E31 | MED | Step 7 | No microphone recipe, and the overlay most INMP441 guides use (`googlevoicehat-soundcard`) drives GPIO16, the X1201's charge control. | `dtoverlay=adau7002-simple` under `[all]`; wire SCK 12, WS 35, SD 38, L/R 34, VDD 17, GND 39; record `-D hw:CARD=adau7002,DEV=0 -f S32_LE -r 48000 -c 2`, left channel; judge by the measured level (dBFS); plug the leads by the solder-side labels; diode-test the joints. | Field-proven on 1 of 2 modules (peak −14.4 dBFS) |
| E32 | MED | Step 7 | `aplay` fails with "audio open error: Unknown error 524": ALSA's default device was the HDMI output. Also the old HUD package's `DRYRUN.md` step 5 promises "the touch display's speakers" — it has none. | `sudo apt install -y pipewire-alsa`; pair a Bluetooth speaker and pick it as the output; `wpctl status` if silent. | Fix field-proven; the cause from a forum post |
| E33 | LOW | Step 3 | The display never blanked when idle (Build Log #65). | Control Centre → Display → Screen Blanking on, then restart: it blanks after 10 minutes. | Field-proven 14 Oct. Whether "off" is the OS default isn't recorded |
| E34 | LOW | Everyday use | On Wi-Fi with a sign-in page, no page opened and Chromium never showed the sign-in page (plain http returned a 404 page, https failed). | Open `http://neverssl.com` to bring the sign-in page up. | Field-proven 14 Oct |
| E35 | LOW | Everyday use | With auto-login the login keyring stays locked, so Chromium and saved Wi-Fi keep asking for its password. | Say so; to reset, move `~/.local/share/keyrings/*` aside, reboot and set a new password. | Field-observed 14 Oct |
| E36 | MED | Case design | The cases were first drawn to a caliper sheet that was 2.6–4.4 mm short sideways (the vernier was read at the sliding plate's edge). The display is 6.42 mm to its metal back — "8.6 mm" was the bezel pocket's depth. The encoder's thread is M7, not "4.68". | Design from the maker's drawing (Raspberry Pi's Touch Display 2 drawing places the Pi's posts relative to the glass); read a vernier at its zero line or photograph the scale. | The drawing and a photo measurement agree · high |
| E37 | LOW | Step 9, case design | Screw length vs hole depth was judged from CAD screws that were heads only. | Check with the real screw: M3 × 8 cuts its own thread in 2.5 mm PETG pilots (no inserts); M3 × 10 bottoms out. A T9 Torx bit grips these shallow hex sockets better than a 2 mm hex key, which rounded one. | Field use; the pull-out strength comes from a published test |

## Still unverified

The SDR; E2 and E5 (the risky parts were never bought); protected cells (E4); whether GPIO16 matters (E15); a timed
runtime (E20); a HAT seated on the stacking header (E18); the closed-case soak test (E29); a recorded end-to-end run of
the wake phrase.
