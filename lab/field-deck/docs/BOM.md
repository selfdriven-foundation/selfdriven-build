# Field Deck — bill of materials

*Guide v3, 20 October 2026. Prices in AUD including GST, as paid in 2026. The source spreadsheet is
`Field-Deck-AUS-Sourcing.xlsx` (BOM, Summary and Build Log sheets).*

## Core parts

| # | Item | Exact part | Qty | A$ | Supplier | Notes |
|---|---|---|---|---|---|---|
| 1 | Computer | Raspberry Pi 5, 8 GB | 1 | 285.65 | Core Electronics | |
| 2 | Cooling | Official Active Cooler | 1 | 8.80 | Core Electronics | |
| 3 | Storage | Official Raspberry Pi 512 GB SSD Kit: 2230 SSD + M.2 HAT+ (CE09981) | 1 | 209.58 | Core Electronics | Billed 215.83 with ~A$6 shipping. Includes a 16 mm stacking header |
| 4 | Backup card | SanDisk Extreme microSD 32 GB, A1 | 1 | 38.99 | Amazon AU | |
| 5 | Screen | Raspberry Pi Touch Display 2, 7" DSI (CE09978) | 1 | 106.36 | Core Electronics | |
| 6 | Keyboard | Royal Kludge RK61, 60 %, brown switches, RGB | 1 | 75.99 | CozyDev (AU) | Wired USB-C recommended |
| 7 | UPS | Geekworm X1201 (2 × 18650, pogo pins) | 1 | 90.63 | Amazon AU | Cells not included |
| 8 | Cells | Samsung 35E 3500 mAh 18650, flat-top 65 mm, unprotected | 2 | 49.90 (24.95 each) | Jaycar | |
| 9 | Enclosure | Bambu PETG-HF filament, 1 kg (CE10443) | 1 | 36.00 | Core Electronics | |
| 10 | Fixings | M2.5 nylon standoff and screw set, 380 pc (ADA3299) | 1 | 35.30 | Core Electronics | |
| 11 | Cable | Right-angle USB-C cable, short | 1 | 11.99 | Amazon AU | |
| 12 | Fixings | Heat-set insert kit, 220 pc, M2–M6 | 1 | 22.99 | Amazon AU | Not used by the MK-I case |
| 13 | Hub *(optional)* | USB 3.0 hub, 4-port (XC5941) | 1 | 29.95 | Jaycar | |
| 14 | SDR *(optional)* | RTL-SDR Blog V3 + dipole antenna kit | 1 | 184.95 | Core Electronics | Never tested |
| 15 | HUD | 0.96" I2C OLED, SSD1306, yellow/blue 128 × 64 | 2 received | 15.90 for the order | eBay AU | |
| 16 | Knob *(optional)* | EC11 encoder with switch (SR1230) | 1 | 9.95 | Jaycar | Not fitted |
| 17 | Power supply | Official Raspberry Pi 27 W USB-C, 5.1 V / 5 A | 1 | 21.07 (estimate) | Core Electronics | Actual price not recorded |
| 18 | Leads *(optional)* | F–F DuPont jumpers, 150 mm, 40-pack (WC6026) | 1 | ~5.95 | Jaycar | Outside every total |

| Totals (Summary sheet) | A$ |
|---|---|
| Essentials (rows 1–12 + 17, PSU at its estimate) | 993.25 |
| Optional (rows 13–16) | 240.75 |
| Shipping and fees (actual) | 26.59 |
| **Everything** | **1,260.59** |
| Actually billed to 27 June (parts 1,212.93 + shipping 26.59) | 1,239.52 |

Billed by order: Core six-item order 665.76 · Amazon X1201 90.63 · Amazon microSD, USB-C cable and inserts 73.97 ·
eBay OLED 15.90 · Jaycar 101.44 (with delivery and a fuel surcharge) · CozyDev keyboard 75.99 · Core SSD kit 215.83.

## Added since September (not in the spreadsheet)

| Item | Part | Qty | Cost | Source | Notes |
|---|---|---|---|---|---|
| Microphone | INMP441 I2S MEMS module (pins loose) | 6 bought | A$26.87 for the order | AliExpress | One of two tried works |
| Mic leads | 150 mm F–F jumpers (row 18's pack) | 6 | in row 18 | Jaycar | Long enough for the MK-I chin |
| OLED extension leads | M–F jumpers, 150–200 mm | 4 | not recorded | — | For the MK-I's HUD position |
| Case screws | M3 × 8 button head, hex socket (uxcell B01B1OD62C, 100 pc) | 26 | not recorded | — | 18 case + 8 retainer ring. Measured 9.0 mm overall, 1.65 mm head |
| Foam tape | Double-sided foam tape | a little | not recorded | — | OLED corners; the mic's ring |
| Screen foam | Moroday garage weatherseal, 12.7 × 25 mm × 3 m, closed-cell (I/N 4114639) | 20 mm used | 16.42 | Bunnings | |
| Filament | PETG HF for the MK-I | ~490 g | — | — | Within the 1 kg spool + restock |
| Speaker | Bluetooth speaker | 1 | not recorded | — | Any |

Considered and not bought: a DFRobot DFR0954 amplifier and a small speaker for inside the case (the speaker posts are
there, under the speaker cover); a Seeed ReSpeaker Lite USB board.

## Tools

| Tool | Notes |
|---|---|
| T9 Torx bit | Grips the M3 button heads better than a 2 mm hex key (which rounded one socket) |
| Slim driver, ~65 mm shaft | For the lower grip-side body screw |
| Soldering iron with temperature control | For the INMP441's pins. A fixed-heat iron gave cold joints and melted the header plastic |
| Multimeter with diode test | This build: Protech QM-1500 |
| Breadboard | Holds the header pins straight for soldering |
| Calipers | Read at the zero line |
| Flush cutters, pliers, 120-grit paper, a needle | Mic pin ends, support removal, the mic pinhole |
