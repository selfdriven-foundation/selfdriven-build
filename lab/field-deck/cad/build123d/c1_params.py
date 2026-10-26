"""FIELD DECK C1 'Bridge' — single source of truth for all dimensions.
Case coords: x+ -> C (user's LEFT), y+ -> top, z=0 = display back, z+ -> case back.
Every number here traces to R1 (caliper map, bezel extraction, or a decision logged in-line)."""
import math

# ---------------- global envelope ----------------
FRONT = -11.6            # front face plane (kept from validated bezel thickness)
BACK  = 54.0             # outer back plane (stack 46 + foam 4 + shell 2.5 + margin)
X_OUT = 104.0            # half-width (208 total, unchanged)
Y_BOT = -92.0            # bottom of outline at the front plane
Y_TOPF= 71.5             # frame top edge / band start (was bezel top)
Y_TOP = 96.0             # top of band
R_OUT = 8.0              # outline corner radius
WALL  = 2.5

STAND_DEG = 12.0   # DERIVED: max angle clearing the X1201 A-overhang corner (46,-76.1) with 2.5 wall +1.0 clearance is 12.15deg
STAND_TAN = math.tan(math.radians(STAND_DEG))   # bottom cut: y = Y_BOT + tan*(z-FRONT)

# ---------------- display pocket (measured off the printed bezel) ----------------
POCKET_X, POCKET_Y = 95.1, 60.5     # cavity half-sizes (display 94.7/60.1 + 0.4 fit)
POCKET_FLOOR = -8.6                  # display front plane (display back flush at z=0)
APERT_X, APERT_Y = 92.0, 60.0       # screen aperture through the armor
ARMOR_BACK = POCKET_FLOOR            # armor spans FRONT..POCKET_FLOOR (3.0 thick)

# ---------------- caliper ground truths ----------------
STACK = dict(x=(-30.7, 67.7), y=(-76.1, 30.1), z=(0.0, 46.0))
PORTS_B_X = (-16.15, 41.85)          # union of the 4 top-port faces (from v7b audit)
PORT_FACE_Y = 30.1
ETH_FACE_X = 67.7
ETH_Y = 28.1
ETH_USB_Z = (15.0, 32.0)             # MEASURED 2026-09-17 off the assembled deck,
                                     # datum = light-grey back face of the display panel.
                                     # Was (15.0, 31.0) ESTIMATED. Caliper rows 7 & 8, blank
                                     # since day one, are now filled. Consequence: the whole
                                     # port band sits ABOVE the frame ridge (z 0..2) and clear
                                     # of the 4 screw bosses (y -71.5/+55, outside the bay),
                                     # so the +x wall may neck in to ~x 72 above z~5.
POWER_BTN = dict(x=23.7, z=38.0)
RIBBON_KEEPOUT = dict(x=(45, 70), y=(5, 30), z=(0, 20))

# ---------------- band / facet ----------------
FACET_Z_TOP = FRONT + 18.0           # facet: (Y_TOPF, FRONT) -> (Y_TOP, FRONT+18)
BAND_Z_BACK = 48.0                   # band inner back before joining shell back
FACET_ANG = math.degrees(math.atan2(FACET_Z_TOP - FRONT, Y_TOP - Y_TOPF))  # ~36.3 from vertical

# rev3-S4 2026-09-15: MEASURED off the owner's actual SSD1306 module (the old values were
# generic-datasheet, same failure class as the encoder): board 25.66 x 25.56, mounting holes
# 21.0 x 21.0 c-t-c dia 1.74 (=> M1.6 screws, NOT M2 - 2.0 will not pass), glass 24.66 x 17
# centred, board+back components 1.66 (nothing protrudes behind except the header), pin
# header protrudes 7.72. Glass THICKNESS not measured -> design made tolerant: 3.2 deep
# glass pocket seats the PCB on hard bosses regardless (any glass up to 3.2 fits).
OLED = dict(x=-48.0, board=(25.66, 25.56), holes=21.0, hole_d=1.74,
            glass=(24.66, 17.0), pcb_t=1.66, header_t=7.72,
            apert=(23.6, 15.8), pocket=(25.4, 17.8), lip=1.0, seat=4.2, pilot_d=1.3)
# pocket 25.0->25.4 / 17.4->17.8 (reviewer N-13): 0.16/side on fragile glass in a printed
# pocket was too tight; now 0.37/side, and it widens the lip land over two extrusion lines.
# rev3-S3 2026-09-15: MEASURED off the owner's actual SR1230 (the old numbers came from a
# generic EC11 datasheet inherited from v7 — never re-derived; caught by the bench gate).
# bushing thread O4.68, thread LENGTH 4.88, nut + washer supplied, shaft O3.9 with a flat.
# Panel must fit inside the thread: 2.5 panel + ~0.5 washer + ~1.6 nut = 4.6 < 4.88.
# -> boss DELETED (bare facet wall = 2.5), bore 4.9, key notch removed (no confirmed
#    anti-rotation flat on the bushing; nut+washer does the clamping).
ENC  = dict(x=-84.0, bush_d=4.9, panel_t=2.5, shaft_d=3.9)
# knob D-bore across-flat = MEASURED shaft across-flat + 0.15. PROVISIONAL until the owner
# MEASURED 2026-09-15: shaft across-flat 2.40.
KNOB_AF = 2.55   # MEASURED shaft across-flat 2.40 + 0.15 (flat cut is 1.5 deep on a 3.9 shaft)
# rev3-S2 2026-09-14: 6.5 bulkhead-style hole was WRONG for the documented plan (the V3
# kit's dipole coax SMA MALE ~O8 passes THROUGH onto the dongle; no bulkhead adapter in
# the BOM; v7b precedent O8.6). Now a plain O8.6 pass-through, no spot-face.
SMA  = dict(x=82.0, z=28.0, d=8.6)

# ---------------- openings ----------------
TRENCH_X = (-19.0, 45.0)             # port bay through the band (ports +2.85/+3.15 margin)
TRENCH_Z = (13.0, 48.0)
TRENCH_BACK_OPEN_Y = 62.0            # back wall removed above this y in trench zone
SIDEBAY = dict(y=(-22.0, 38.0), z=(13.0, 44.0))   # Eth/USB, matches v7b audited clears
PWR_SLOT = dict(x=(16.7, 30.7), z=(30.0, 46.0))   # validated in v7b audit

VENT_ZONES = [dict(x=(-90, -45), y=(-74, -58)),   # low (moved off the bevel corner)
              dict(x=(-90, -45), y=(42, 56))]     # high
VENT_SLOT = dict(w=2.6, gap=6.0)

# ---------------- retention / fastening ----------------
RING_T = 3.0                         # retainer ring thickness (z 0..3)
RING_RAIL_XI = 95.5                  # ring rails: x 95.5..101.5 sides
RING_RAIL_XO = 101.5
RING_TOP_Y = (61.0, 67.5)
RING_PADS_BOT = [(-95, -45), (75, 95)]  # x-ranges of bottom pads (clear of stack + ribbon)
RING_SCREWS = [(99, 64), (-99, 64), (99, -64), (-99, -64), (99, 0), (-99, 0)]
PILOT_D = 2.5                        # self-tap pilot (lesson from v7b: 2.9 was loose)
RING_CLEAR_D = 3.4

FOAM = dict(x=STACK["x"], y=STACK["y"], inner_z=50.0)   # 5mm pad -> 4mm crush over stack

# slide bolts (tool-free latch, one per side wall)
BOLT = dict(y_c=-10.0, ch_w=18.0, ch_l=34.0, plate=(15.0, 24.0, 3.0),
            tongue=(12.0, 3.2, 6.0), travel=8.0)
HOOKS_X = (-60.0, 60.0)              # chin hooks on shell bottom
