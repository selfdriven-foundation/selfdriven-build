"""FIELD DECK R3 — single source of truth for the two-piece back case.

Coords unchanged from C1: x+ -> ports / user's LEFT, y+ -> top, z=0 = display back
(the light-grey panel face the owner measures from), z+ -> case back.

Every number here is either MEASURED, read off the PRINTED FaceFrame/RetainerRing
(build_c1_frame.py, already on his desk), or a decision logged in-line.
"""
import math

# ---------------- outline, fixed by the PRINTED face frame ----------------
X_OUT  = 104.0           # half width  -> 208 outline
Y_BOT  = -92.0           # bottom of the outline at the front plane
Y_TOPF = 71.5            # frame top edge; the shell starts here
R_OUT  = 8.0             # outline corner radius
FRONT  = -11.6           # frame front plane (the shell no longer reaches it)
STAND_DEG = 12.0         # DERIVED in C1: max lean clearing the X1201 corner (46,-76.1)
STAND_TAN = math.tan(math.radians(STAND_DEG))

# ---------------- what the printed frame puts in our way ----------------
# build_c1_frame.py lines 27-35: registration ridge, z 0..2, x 99.2..101.2 (and the
# matching y bands); NO ridge on the bottom edge.
FRAME_RIDGE = dict(z=(0.0, 2.0), x=(99.2, 101.2))
# lines 64-67: four M3 bosses, SOLID, z 0..18 -> they punch straight through any
# skirt roof at z=6. The shell needs a hollow tower over each one.
FRAME_BOSS  = dict(x=(96.1, 101.2), z=(0.0, 18.0), y_half=5.0, ys=(-71.5, 55.0),
                   pilot_axis_x=100.0, pilot_z=12.5)
# ring(): rails/ears/feet all z 0..3, reaching x +-101.2, y -66..67.
RING = dict(z=(0.0, 3.0), x_out=101.2, y=(-66.0, 67.0))

# ---------------- the sandwich ----------------
STACK = dict(x=(-30.7, 67.7), y=(-76.1, 30.1), z=(0.0, 46.0))
PORTS_B_X   = (-16.15, 41.85)    # union of the 4 TOP port faces
PORT_FACE_Y = 30.1
ETH_FACE_X  = 67.7
ETH_USB_Z   = (15.0, 32.0)       # MEASURED 2026-09-17 off the assembled deck
POWER_BTN   = dict(x=23.7, z=38.0)
RIBBON_KEEPOUT = dict(x=(45, 70), y=(5, 30), z=(0, 20))

# ---------------- the shell ----------------
WALL    = 2.5
SKIRT_Z = 7.0            # skirt outer z 0..7; roof is the top 2.5 -> cavity z 0..4.5,
                         # which clears the 3.0 retainer ring by 1.5 and the 2.0 ridge by 2.5
ROOF_T  = 2.5
CAV_Z   = SKIRT_Z - ROOF_T          # 4.5
# internal corner radii are SMALL on purpose. The printed frame's registration ridge
# and the documented PCIe ribbon keep-out both run into square corners; a generous
# internal fillet puts solid material exactly where they sit.
SKIRT_CAV_R = 0.8
BODY_CAV_R  = 2.0
BACK    = 56.5           # was 54.0. Reviewer R3-1: from the panel counterbore floor the
                         # M3 budget was only 5.79 mm, so an M3x8 punched through the boss
                         # floor. +2.5 gives 8 mm of boss and a 7 mm pilot -> M3x8 fits.
CL      = 4.0            # body wall offset from the stack: 2.5 wall + 1.5 slack
# +x is pushed out 0.8 beyond CL: the documented PCIe ribbon keep-out runs to x=70,
# and CL alone put the wall's inner face at 69.2 - it would have pinched the ribbon.
BX = (STACK["x"][0] - CL, STACK["x"][1] + CL + 1.3)      # -34.7 .. 73.0
BY = (STACK["y"][0] - CL, STACK["y"][1] + CL)      # -80.1 .. 34.1

# ---------------- HUD pod ----------------
# 48 deg facet, not 36.3: printed mouth-down the facet is an underside, and 36.3 deg
# from the plate needs support on the one face you actually look at. 48 deg prints clean.
POD_X   = (-66.0, -30.0)
FACET_DEG   = 48.0                       # from the display plane
FACET_LEN   = 30.0                       # slope length; OLED board is 25.56 along it
POD_BACK_T  = 17.0                       # was 14.5 -> cavity bottomed at 12.005 and the
                                         # module's deepest point is 4.2 + 7.72 = 11.92.
                                         # 0.085 mm is not clearance. 17.0 -> 14.5 of cavity,
                                         # i.e. 2.58 mm of real air behind the header.
FACET_A = (Y_TOPF, 0.0)                  # facet lower edge, on the frame's back plane
FACET_B = (Y_TOPF + FACET_LEN*math.cos(math.radians(FACET_DEG)),
           0.0    + FACET_LEN*math.sin(math.radians(FACET_DEG)))   # ~ (91.6, 22.3)
FACET_MID = FACET_LEN / 2.0

# MEASURED 2026-09-15 off the owner's SSD1306
OLED = dict(board=(25.66, 25.56), holes=21.0, hole_d=1.74, glass=(24.66, 17.0),
            pcb_t=1.66, header_t=7.72, apert=(23.6, 15.8), pocket=(25.4, 17.8),
            lip=1.0, seat=4.2, pilot_d=1.3, x=-48.0)

# ---------------- openings ----------------
SIDE_WIN = dict(y=(-26.0, 34.1), z=(11.0, 36.0))    # Eth/USB; ports measured z 15..32
TOP_WIN  = dict(x=(-20.0, 46.0), z_top=44.0)        # top ports exit straight up. The notch
                                                    # STOPS at z=44 (above the stack) so the
                                                    # panel rebate survives across the top edge;
                                                    # its upper edge is chamfered 45 deg so the
                                                    # 66 mm re-closure is self-supporting.
PWR_SLOT = dict(x=(16.7, 30.7), z=(30.0, 46.0))

# ---------------- fastening ----------------
PILOT_D     = 2.5        # self-tap pilot for M3 (C1 lesson: 2.9 was loose)
CLEAR_D     = 3.4
HEAD_D      = 6.1
HEAD_DEEP   = 1.70
PANEL_T     = 2.5
PANEL_Z     = (BACK - PANEL_T, BACK)                # 51.5 .. 54
PANEL_INSET = 2.0                                   # rebate ledge width. Was 1.0 -> a 1.00 mm
                                                    # rim was the only thing retaining the lid.
PANEL_GAP   = 0.15                                  # per side
# bosses must OVERLAP their wall (tangent does not fuse - two of them printed as
# free-floating bodies on the first build) and must start ABOVE the stack (z=46),
# or they punch into the electronics.
# the two lower screws were at y=-75.1. Raising the rebate lip 1.0->2.0 shrank the
# panel, and the O6.1 counterbore then broke out through the panel's bevelled bottom
# edge (reviewer round 2). Moved to y=-71.5: 3.8 mm of material outside the counterbore.
# Round 3: the O6.1 counterbore still overshot the panel's x edge by 0.2 mm, and at the
# top corners the 5 mm corner fillet left only 1.96 mm - it was taking the lid's corners
# off. Screw circle moved 1.5 mm inboard in x and clear of both corner fillets in y.
# BOSS_D 7->10 so the boss still overlaps the shell wall by 1.0 mm and fuses to it.
PANEL_SCREWS = [(-28.2, -65.0), (-28.2, -23.0), (-28.2, 27.5),
                ( 66.5, -65.0), ( 66.5, -23.0), ( 66.5, 27.5)]
BOSS_D      = 10.0
BOSS_Z      = (46.0, PANEL_Z[0])        # 5.5 mm of M3 self-tap thread
BOSS_PILOT_DEEP = 8.2        # THROUGH the 8 mm boss, so an M3x8 can never bottom out.
                             # Head-recess floor 54.8 - 8.0 screw = tip at z 46.8, still
                             # 1.0 mm inside the boss, so nothing pokes into the foam.

# the 6 panel bosses occupy z 46..51.5 at the cavity's edges, i.e. inside the foam
# zone. Cut the pad to clear them rather than trying to squash it round them.
# Reviewer round 4: the six O10 bosses bottom at z=46.002 and overlap the stack
# footprint by 7.5 mm on -x and 6.2 mm on +x. Cut the pad to clear them.
FOAM = dict(nominal=5.0, gap=PANEL_Z[0] - STACK["z"][1],       # 8.0 mm gap -> use two 4 mm
            pad_x=(-23.2, 61.5), pad_y=(-67.0, 22.0))          # pads or one 8 mm, cut to pad_x
