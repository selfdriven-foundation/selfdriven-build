"""MK-I, M1 - where the X1201's power switch is, in case coordinates, and how design r5 stands to it.
2026-10-03.  ESTIMATES. The only caliper readings in here are marked CALIPER; everything else was
read off the owner's photos (mk1_m1_photos.py) and must be confirmed before anything is cut.

What the photos show (IMG_1908, IMG_1890, IMG_1895, IMG_1882, IMG_1856; read twice, the second
time by a reader who was not told the first result - same answers):
  - the switch is a right-angle 6 x 6 tact switch on the X1201's COMPONENT face (the face toward the
    Pi and the display), at the corner of the A end (bottom, the white sockets) and the D edge (the
    side WITHOUT the handle - the side of the Pi's own power button, its LED and the PCIe ribbon);
  - its plunger (dia 3.5) points SIDEWAYS, toward -x, parallel to the board, and ends 3..4 mm
    outside the board's D edge. It is pressed toward +x. It does not face down;
  - the five white sockets are 2-pin JST-XH, TOP-ENTRY, standing on the component face along the A
    end: their mouths face the DISPLAY (-z). The one right beside the switch has the silk "P", very
    probably "S", the rest hidden: PSW, the socket for an external button;
  - the two 18650 cells sit on the component face too, beside the Pi - NOT at the back. The back of
    the stack is the X1201's bare solder side: four black screw heads (Pi pattern) and, at the A
    end, two brass hex posts - the deck stands on them when it lies on its back.
"""
import math
import r3_params as R
import mk1_body_r3 as B3, mk1_body_r5 as B5, mk1_armour_r5 as A5, mk1_parts_r5 as P5

G = P5.G
PX, PY, WALL = B3.PX, B3.PY, R.WALL
mid = lambda t: sum(t) / 2

BOARD = dict(L=106.6, W=85.0, T=1.6)                 # Geekworm; in IMG_1882 it measures 106.2 x 84.7

# ---- across (x) ----
# CALIPER: the Eth/USB faces are 27 mm inside the display's C edge -> x 67.7. The USB shells stand 2.5..3.0 proud
# of the Pi's board; the X1201 is as wide as the Pi is long (85) and its Pi screws sit 3.5 from its D edge, as
# the Pi's own holes do (IMG_1882: 3.49) - so the two boards' D edges line up.
X_D = (67.7 - 3.0 - 85.0, 67.7 - 2.5 - 85.0)         # the X1201's D edge: -20.3 .. -19.8
TIP_OUT = (3.0, 3.9)                                 # the plunger's tip outside that edge (IMG_1882: 3.9; by eye 3)
X_TIP = (X_D[0] - TIP_OUT[1], X_D[1] - TIP_OUT[0])   # -24.2 .. -22.8
X_TIP_MID = mid(X_TIP)                               # -23.5
X_D_MID, TIP_OUT_MID = mid(X_D), mid(X_D) - mid(X_TIP)   # for the drawings: -20.05, 3.45
# An old note says "power button 71 mm from display-left". Taken from the display's D edge (-94.7) that is
# -23.7 and agrees. But the note is from the same early batch as "charge 33 mm from display-left", which was
# wrong, and it does not say how it was taken: it is NOT counted as a measurement. The records made +23.7
# of it ("on the A face") - mirrored, and the wrong face.

# ---- along (y) ----
Y_A = (-77.5, -76.1)       # the board's A end: CALIPER B end 29.1, minus 106.6 -> -77.5;
                           # CALIPER "16.0 OUT" past the display's bottom edge -> -76.1. They disagree by 1.4.
Y_A_MID = mid(Y_A)
SW_U = (10.4, 11.8)        # the switch's axis from the A end: 10.8 by its four solder joints (IMG_1882); second reader 11..12
SW_Y = (Y_A[0] + SW_U[0], Y_A[1] + SW_U[1])          # -67.1 .. -64.3
SW_Y_MID = mid(Y_A) + mid(SW_U)                      # -65.7

# ---- height (z) : not measured directly, but pinned (2026-10-04) ----
# "46" - the stack height in every record since September - is the caliper sheet's PHOTO ESTIMATE (row 6: both
# reading cells are empty), and it is wrong by about 2.5 mm. No photo shows the height being measured.
# What IS measured: Settle Sheet N6 / N7, the owner's depth rod on 2026-09-17: the Eth/USB port bodies run from
# 15.0 to 32.0 mm above the display's back. 15.0 + 15.6 (USB stack) + 1.4 (board) = 32.0: the Pi's back face.
#   + 5.0  the spacer between Pi and X1201 (Geekworm's packing list: "M2.5x5 F/F Spacers", "M2.5x5+3mm F/M Spacer")
#   + 1.6  the X1201's board                                                   -> 38.6
#   IMG_1888 (square-on from the handle side; scale from the Ethernet jack)   -> 38.7 .. 39.0
#   IMG_1856 (camera from the frame's pilot holes)                            -> 37.3 +- 1.5 (+-3 honestly)
#   IMG_1895 (reads a known 16 mm standoff as 18..20)                         -> 42.9 uncorrected, 36..38 corrected
Z_BACKFACE = (38.3, 39.3)
Z_BACK_MID = 38.7
AXIS_OVER_BOARD = (3.55, 3.85)   # the plunger's axis above the component face: 3.55 read in IMG_1908; 3.85 is the usual
                                 # figure for a right-angle 6 x 6 tact switch
Z_AXIS = (Z_BACKFACE[0] - BOARD["T"] - AXIS_OVER_BOARD[1], Z_BACKFACE[1] - BOARD["T"] - AXIS_OVER_BOARD[0])   # 32.85 .. 34.15
Z_AXIS_MID = Z_BACK_MID - BOARD["T"] - mid(AXIS_OVER_BOARD)                                               # 33.4
PLUNGER_D = 3.5
POST = dict(u=3.5, v=(3.6, 61.6), h=(4.7, 6.0), nominal=5.0, af=4.5)   # brass posts on the back face: Geekworm's M2.5x5 spacers (photos: 4.7..6)
SCREW_HEAD = 2.2                                          # the four Pi-pattern screws' heads above the back face
XH = dict(tall=7.0, deep=5.75, plug_out=4.0, wire=6.0)    # JST B2B-XH-A header; a plug stands ~4 out of it, the wires need ~6 to turn
HEX_MARK = (-67.8, G.SEAT - B5.PILOT_DEEP - A5.DEPTH - 0.05 - 6.5)   # r5's armour: the hex mark at the grille plate's lower rear corner (y, z)


def report():
    xin = PX[0] + WALL
    print("the board:   D edge x %.1f .. %.1f, A end y %.1f .. %.1f, back face z %.1f .. %.1f (best %.1f; '46' was never measured)" % (*X_D, *Y_A, *Z_BACKFACE, Z_BACK_MID))
    print("PLUNGER:     tip x %.1f .. %.1f (mid %.1f)   axis y %.1f .. %.1f (mid %.1f)   axis z %.2f .. %.2f (best guess %.2f)" % (
        *X_TIP, X_TIP_MID, *SW_Y, SW_Y_MID, *Z_AXIS, Z_AXIS_MID))
    print("the wall on that side: outer face x %.1f, inner face x %.1f -> %.1f .. %.1f mm (mid %.1f) from the wall's inner face to the plunger's tip" % (
        PX[0], xin, X_TIP[0] - xin, X_TIP[1] - xin, X_TIP_MID - xin))
    yl = G.LUG_Y[0]
    print("\nr5 round that spot:")
    print("  lower screw lug: y %.2f, its column y %.2f .. %.2f, corbel leaves the wall at z %.1f, pilot z %.1f .. %.1f" % (
        yl, yl - B5.COL_HALF, yl + B5.COL_HALF, G.ZK, G.SEAT - B5.PILOT_DEEP, G.SEAT))
    for dia in (4.0, 4.5, 5.0):
        top = [z + dia / 2 for z in Z_AXIS]
        print("     a %.1f mm bore on the plunger's axis has its top at z %.2f .. %.2f (best guess %.2f): %.2f .. %.2f under the corbel's foot (best guess %.2f)" % (
            dia, *top, Z_AXIS_MID + dia / 2, G.ZK - top[1], G.ZK - top[0], G.ZK - Z_AXIS_MID - dia / 2))
    ys, w, (z0, z1) = B3.VENT["ys"], B3.VENT["w"], B3.VENT["z"]
    near = min(ys, key=lambda v: abs(v - SW_Y_MID))
    e0, e1 = (near - w / 2) - SW_Y[1], (near - w / 2) - SW_Y[0]
    print("  air slots: nine, %.0f wide, z %.0f .. %.0f. The lowest (y %.1f .. %.1f) has its edge %.1f .. %.1f mm from the plunger's axis;" % (w, z0, z1, near - w / 2, near + w / 2, e0, e1))
    print("     a 4.5 bore has a radius of 2.25: between that bore and the slot there is %.1f .. %.1f mm (negative = they run into each other)" % (e0 - 2.25, e1 - 2.25))
    hx, hz = HEX_MARK
    print("  armour: the grille plate's corner hex mark at (y %.1f, z %.1f) is %.1f mm from the plunger's axis (y %.1f, z %.1f)" % (
        hx, hz, math.hypot(hx - SW_Y_MID, hz - Z_AXIS_MID), SW_Y_MID, Z_AXIS_MID))
    print("\nthe back of the stack against the slim back plate (inner face z %.1f):" % G.SEAT)
    for zb, tag in ((Z_BACK_MID, "best value"), (Z_BACKFACE[1], "upper end of the range")):
        print("  back face z %.1f (%s): screw heads to %.1f, brass posts to %.1f .. %.1f  ->  %.1f .. %.1f mm of air over the posts" % (
            zb, tag, zb + SCREW_HEAD, zb + POST["h"][0], zb + POST["h"][1], G.SEAT - zb - POST["h"][1], G.SEAT - zb - POST["h"][0]))
    print("  only IF the board's back face were at 46 (what 'stack 46' was taken to mean) would the posts reach the plate: %.1f .. %.1f" % (
        G.SEAT - 46 - POST["h"][1], G.SEAT - 46 - POST["h"][0]))
    print("  posts at x %.1f and %.1f, y %.1f .. %.1f" % (mid(X_D) + POST["v"][0], mid(X_D) + POST["v"][1], Y_A[0] + POST["u"], Y_A[1] + POST["u"]))
    print("  with the plate off: the plunger lies %.1f mm under the board's back face, in the %.1f mm gap between the board's D edge and the wall;" % (
        BOARD["T"] + mid(AXIS_OVER_BOARD), mid(X_D) - xin))
    print("     r5's opening starts at x %.1f, so %.1f mm of that gap is open from behind - not a place for a finger" % (G.opening[0][0], X_TIP_MID - G.opening[0][0]))
    zc = Z_BACK_MID - BOARD["T"]; zmouth = zc - XH["tall"]
    print("\nthe 2-pin socket for an outside button (PSW): top-entry, mouth toward the display at z %.1f; a plug and its wires reach down to z %.1f;" % (
        zmouth, zmouth - XH["plug_out"] - XH["wire"]))
    print("   free under it: down to the retainer ring (z 3). Sideways it sits %.1f .. %.1f mm from the stand wall's inner face (y %.2f at that height)" % (
        Y_A[0] - B5.stand_y(zmouth - 5.0, WALL), Y_A[1] + XH["deep"] - B5.stand_y(zmouth - 5.0, WALL), B5.stand_y(zmouth - 5.0, WALL)))


if __name__ == "__main__":
    report()
