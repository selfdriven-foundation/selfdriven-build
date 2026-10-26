"""MK-I - SOUND, the body's share. A DRAFT on top of design r7 (2026-10-06) - NOT FOR PRINT.

The owner's decision of 2026-10-06: the speaker's bar is a SEPARATE screw-on cover, not walls on the body, so that
nothing on the big parts has to fit a bought part. The body gets only
  - two screw posts on the top band of its back, on the side WITHOUT the handle (x < 0), and
  - one slot through the top wall of the raised middle, for the speaker's lead and its white plug.
Everything of r7 stays as it is: this module only ADDS to r7's finished body (mk1_parts_r7.body()).

The cover drawn here is PROVISIONAL: it is built round the maker's figures for the speaker (DFRobot FIT0502:
70 x 30 x 16 mm, 24 g, lead 42 cm, white 2-pin plug; read 2026-10-06 on core-electronics.com.au) and is fixed only
after the owner has measured the real speaker. It is here to prove that the two posts leave room for it.

Where things are (case coordinates, mm; the band's surface is z 7.0, 6.25 in the armour's recesses):
  top band            y 36.6 (the top wall's outer face, x > -30.4) .. 71.5 (the body's top edge), flat, no edge bevel
  screw tower         x -104 .. -93, y 45 .. 65, up to z 21, open at the top (the front's boss stands in it)
  top notch           x > -1.2, y 31.6 .. 41.6; HDMI 0's plug zone starts at x 1.2
"""
import math
from build123d import Pos, Rot, Box, Cylinder

WALL = 2.5
Z_BAND, Z_ROOF_UNDER = 7.0, 4.5
Y_WALL, Y_TOP = 36.6, 71.5                     # the top wall's outer face; the body's top edge
X_TOWER, Y_TOWER = -93.0, 45.0                 # the screw tower's face toward the bar; its lower (south) face
X_NOTCH = -1.2

# ---------------------------------------------------------------- the body's share
POST_D, POST_Z1 = 7.0, 14.0                    # the posts: dia 7, from the band up to z 14 (7 mm tall)
POST_Z0 = 6.0                                  # drawn from just under the band's surface, so they fuse in the recesses too
PILOT_D, PILOT_Z0 = 2.5, 6.3                   # self-tap pilot for M3 (2.5: the C1 lesson). It ends at z 6.3: r7's check keeps the skirt at
                                               # x < -90 IDENTICAL to the printed R3 shell below z 6.2 (the frame interface) - the first draft's
                                               # pilot went to 6.0 and that check caught its last 0.2 mm (0.98 mm3). 1.8 of roof stays under it
P1 = (-98.0, 40.3)                             # beside the cover's end, just below the screw tower - fused to the tower
                                               # (40.3, not 40.8: the screw's head then clears the foot's upper cheek by 0.4)
P2 = (-6.6, 66.1)                              # inside the cover's far corner, at the top edge
SLOT_X, SLOT_Z, SLOT_PEAK = (-28.0, -21.0), (9.0, 14.0), 17.5   # the lead's slot: 7 wide, 5 high + a 45 deg peak (prints without a bridge)
SLOT_Y = (Y_WALL - WALL - 0.5, Y_WALL + 0.5)

# ---------------------------------------------------------------- the provisional cover
GAP = 0.3                                      # between the cover and the body's faces
T_LONG, T_END, T_ROOF, T_TUBE, T_LUG = 1.2, 1.2, 2.0, 1.2, 2.0
POST_PLAY = 0.4                                # round each post
SPK = (70.0, 30.0, 16.0)                       # maker's figures - NOT measured
PAD = 2.0                                      # foam pads under the speaker (the lead passes between them)
HEADROOM = 0.5
CX0, CX1 = X_TOWER + GAP, X_NOTCH - GAP        # -92.7 .. -1.5
CY0, CY1 = Y_WALL + GAP, Y_TOP - GAP           # 36.9 .. 71.2
Z_LUG0 = POST_Z1                               # the cover's lugs lie on the posts
Z_LUG1 = Z_LUG0 + T_LUG
Z_IN = Z_BAND + PAD + SPK[2] + HEADROOM        # the roof's underside: 25.5
Z_TOP = Z_IN + T_ROOF                          # 27.5
SCREW_L, HEAD_D, HEAD_H, CLEAR_D = 8.0, 5.6, 2.2, 3.4
TUBE = 2 * POST_PLAY + POST_D                  # the square room round a post: 7.8


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def cyl(x, y, z0, z1, d):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


# ================================================================ the body
def posts():
    p1 = cyl(P1[0], P1[1], POST_Z0, POST_Z1, POST_D) + box(P1[0] - POST_D / 2, P1[0] + POST_D / 2, P1[1], Y_TOWER + 0.5, POST_Z0, POST_Z1)
    return p1 + cyl(P2[0], P2[1], POST_Z0, POST_Z1, POST_D)


def pilots():
    return cyl(P1[0], P1[1], PILOT_Z0, POST_Z1 + 1.0, PILOT_D) + cyl(P2[0], P2[1], PILOT_Z0, POST_Z1 + 1.0, PILOT_D)


def slot():
    xm = sum(SLOT_X) / 2; w = SLOT_X[1] - SLOT_X[0]; ly = SLOT_Y[1] - SLOT_Y[0]; ym = sum(SLOT_Y) / 2
    peak = Pos(xm, ym, SLOT_Z[1]) * Rot(Y=45) * Box(w / math.sqrt(2.0), ly, w / math.sqrt(2.0))
    return box(SLOT_X[0], SLOT_X[1], SLOT_Y[0], SLOT_Y[1], SLOT_Z[0], SLOT_Z[1]) + peak


def apply(body):
    """r7's finished body + the two posts, with their pilots and the lead's slot cut"""
    return body + posts() - pilots() - slot()


# ================================================================ the provisional cover (in place)
def bay():
    """the cover's inside: (x0, x1, y0, y1)"""
    return CX0 + T_END, CX1 - T_END, CY0 + T_LONG, CY1 - T_LONG


def tube2():
    """the square room round post 2, in the cover's far corner at the top edge: (x0, x1, y0, y1) of its inside"""
    bx0, bx1, by0, by1 = bay()
    return bx1 - TUBE, bx1, by1 - TUBE, by1


def ear1():
    """the foot round post 1, outside the cover's end wall: inside (x0, x1, y0, y1)"""
    return P1[0] - POST_D / 2 - POST_PLAY, CX0, P1[1] - POST_D / 2 - POST_PLAY, Y_TOWER - GAP


def speaker_at():
    """the speaker (maker's size) centred in what the bay leaves it: (x0, x1, y0, y1, z0, z1)"""
    bx0, bx1, by0, by1 = bay(); tx0 = tube2()[0] - T_TUBE
    xm, ym = (bx0 + tx0) / 2, (by0 + by1) / 2
    return xm - SPK[0] / 2, xm + SPK[0] / 2, ym - SPK[1] / 2, ym + SPK[1] / 2, Z_BAND + PAD, Z_BAND + PAD + SPK[2]


def cover(grille=True):
    bx0, bx1, by0, by1 = bay()
    c = box(CX0, CX1, CY0, CY1, Z_BAND, Z_TOP) - box(bx0, bx1, by0, by1, Z_BAND - 1, Z_IN)
    # ---- post 2: a square well in the far corner; its floor (the lug) lies on the post
    tx0, tx1, ty0, ty1 = tube2()
    c += box(tx0 - T_TUBE, tx1, ty0 - T_TUBE, ty1, Z_BAND, Z_IN)                       # the tube, solid first
    c -= box(tx0, tx1, ty0, ty1, Z_BAND - 1, Z_LUG0)                                    # room round the post
    c -= box(tx0, tx1, ty0, ty1, Z_LUG1, Z_TOP + 1)                                     # the well for the screw's head, open to the back
    c -= cyl(P2[0], P2[1], Z_LUG0 - 1, Z_LUG1 + 1, CLEAR_D)
    # ---- post 1: a foot outside the end wall, just below the tower; two 45 deg cheeks carry its lug
    ex0, ex1, ey0, ey1 = ear1()
    lug = box(ex0 - T_TUBE, ex1, ey0 - T_TUBE, ey1, Z_LUG0, Z_LUG1)
    reach = ex1 - (ex0 - T_TUBE)                                                        # how far the foot stands out from the end wall
    for (y0, y1) in ((ey0 - T_TUBE, ey0), (ey1 - T_TUBE, ey1)):                          # a cheek on each side of the screw
        blk = box(ex0 - T_TUBE, ex1, y0, y1, Z_LUG1, Z_LUG1 + reach)
        cutter = Pos(ex0 - T_TUBE, (y0 + y1) / 2, Z_LUG1 + reach) * Rot(Y=45) * Box(reach * math.sqrt(2.0), (y1 - y0) + 1, reach * math.sqrt(2.0))
        c += blk - cutter
    c += lug + box(ex0 - T_TUBE, ex0, ey0 - T_TUBE, ey1, Z_BAND, Z_LUG0) + box(ex0 - T_TUBE, ex1, ey0 - T_TUBE, ey0, Z_BAND, Z_LUG0)   # lug, and a skirt on two sides
    # 2026-10-07 (review of the saved Fusion file): the lower cheek stands OUTSIDE the cover's outline - y 35.2 .. 36.4, the end
    # wall began at y 36.9 - so it touched nothing but the lug under it, and printed roof down it began in mid-air. Two
    # independent reviewers found it; the attachment gate had a hole exactly there (attach_scan.py, repaired the same day).
    # The end wall now runs on to the foot's outer edge and carries the cheek, like the upper one.
    c += box(CX0, CX0 + T_END, ey0 - T_TUBE, CY0, Z_BAND, Z_TOP)
    c -= cyl(P1[0], P1[1], Z_LUG0 - 1, Z_LUG1 + 1, CLEAR_D)
    # ---- the lead's way out, over the slot
    c -= box(SLOT_X[0] - 0.5, SLOT_X[1] + 0.5, CY0 - 1, by0 + 1, Z_BAND - 1, SLOT_PEAK + 0.5)
    if grille:
        sx0, sx1, sy0, sy1, _, _ = speaker_at()
        n = 11; pitch = 5.0; xm = (sx0 + sx1) / 2
        for k in range(n):
            x = xm + (k - (n - 1) / 2) * pitch
            c -= box(x - 0.9, x + 0.9, sy0 + 5.0, sy1 - 5.0, Z_IN - 1, Z_TOP + 1)
    return c


def screws():
    """the two M3 x 8, heads on the lugs"""
    out = None
    for (x, y) in (P1, P2):
        s = cyl(x, y, Z_LUG1, Z_LUG1 + HEAD_H, HEAD_D) + cyl(x, y, Z_LUG1 - SCREW_L, Z_LUG1, 3.0)
        out = s if out is None else out + s
    return out


def cover_for_print(c):
    """roof down on the bed"""
    return Pos(0, 0, Z_TOP) * Rot(X=180) * c


if __name__ == "__main__":
    c = cover(); bb = c.bounding_box()
    print("cover valid %s, solids %d, %.1f cm3 (%.0f g PETG), x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f" % (
        c.is_valid, len(c.solids()), c.volume / 1000, c.volume / 1000 * 1.27, bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z))
    print("bay inside", bay(), " tube2", tube2(), " ear1", ear1(), " speaker", speaker_at())
    p = posts(); print("posts valid", p.is_valid, "solids", len(p.solids()), "vol %.1f mm3" % p.volume)
    s = slot(); bb = s.bounding_box(); print("slot z %.2f..%.2f x %.2f..%.2f vol %.1f" % (bb.min.Z, bb.max.Z, bb.min.X, bb.max.X, s.volume))
