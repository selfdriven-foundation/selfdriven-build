"""MK-I BODY r5 + BACK PLATE — the owner, looking at r4 in Fusion (2026-10-02):
  "this design also looks as if it does not have the back panel screwed. I thought we were printing
   it separate and screwing to avoid support."
  "in the last printed design, the gap between the sandwich back and the screwed back panel was 10
   [mm]. it is better to keep it less?"

So the back is a SEPARATE PLATE again (as R3's panel was), and the body prints open, mouth-down,
with no ceiling: the ~105 g of support under r2-r4's closed back is gone.

WHY R3's GAP WAS 8 mm: its panel screws (M3x8) went into bosses that hung ABOVE the stack, because
beside the stack the walls are only 5 mm away. Those bosses also start in mid-air when the shell is
printed mouth-down. r5 moves the screws to the SIDES:
  - the plate has four EARS that reach out over the back bevel to the side walls;
  - under each ear the body has a LUG (a block rising from the bevel) and, inside, a short COLUMN
    on the wall, beside the stack, that carries the M3 pilot. Its underside is a 45 deg corbel.
  Nothing hangs: every new surface is vertical, top-facing or 45 deg.
That frees the gap: BACK (the plate's outer face) is a parameter. Two variants were built and shown
side by side (out/mk1/MK1_back_depth_options_r5.png):
  keep  BACK 56.5 (r4's depth): 8.0 mm between the stack and the plate, back bevel 10 mm
  slim  BACK 53.0             : 4.5 mm between the stack and the plate, back bevel 6.5 mm
THE OWNER PICKED "A - Slim" (2026-10-03). `CHOSEN` below; "keep" stays buildable as the record.
The bevel starts at z 46.5 in both (above every opening's chamfered top edge), so only its width
changes. Lower limit for BACK: the HUD cap's highest point is z 51.9, and the deck should lie on
its back, not on the pod.

THE BACK BEVEL IS NOW A THICK RING. It carries the plate: flat rim (RIM) at the top of the bevel,
a rebate for the plate, a LEDGE under the plate's edge, and below that a 45 deg inner slope down to
the wall. The ledge is as wide as the stack allows on each side (the slope must pass the stack's
top edge with >= 1.2 mm): 2.0 at the sides and bottom, 1.2 at the top.

Everything else is r3's, verbatim: frame interface, HUD pod and cap, openings, vents, stand.
"""
from build123d import *
import math
import r3_params as R
from r3_params import (X_OUT, Y_BOT, Y_TOPF, R_OUT, FRONT, STAND_DEG, FRAME_BOSS, STACK, PORT_FACE_Y, ETH_FACE_X,
                       WALL, SKIRT_Z, CAV_Z, SKIRT_CAV_R, FACET_DEG, FACET_A, FACET_MID, OLED, SIDE_WIN, TOP_WIN,
                       PILOT_D, CLEAR_D, HEAD_D, HEAD_DEEP)
from build_r3 import rrect, stand_cutter, facet_pt, edge_wedge_yz, FDIR, FIN
import mk1_body_r3 as B3
from mk1_body_r3 import (PX, PY, C_PLAN, K_IN, TOP_NOTCH_X, SIDE_Y, VENT, HUD_X, POD_X, L_REAR, CAP_PILOT_DEEP,
                         POD_BACK_Y, TROUGH_Y1, OLED_ALONG, fbox, axis_cyl, on_facet, wedge_x, pod_outer, pod_cavity,
                         cap_screws, cap_bosses, export_clean_stl, cap_for_print)

Z_FAC = 46.5                      # where the back bevel starts (r3: above every opening's chamfered top edge)
PANEL_T = 2.5                     # the plate (R3's panel thickness; 0.8 left under a screw head)
RIM = 1.2                         # flat rim between the bevel's top edge and the plate
GAP = 0.25                        # plate to rebate, per side (R3 drew 0.15 and never printed it; the frame fit uses 0.3)
NOSE = 0.4                        # vertical lip at the opening's edge, under the ledge (no knife edge)
LEDGE_NOM = dict(D=2.0, C=2.0, top=1.2, bot=2.0)
STACK_CLEAR = 1.2                 # the ring's inner slope passes the stack's top edge by at least this
LUG_W = 10.0                      # ear width
LUG_OUT = 1.5                     # the lug stands this proud of the side wall (room for the ear's end past the counterbore)
LUG_AX = 3.3                      # screw axis, in from the wall's outer face
COL_IN = 5.8                      # the column's inner face, in from the wall's outer face (stack: 7.5 / 8.0)
COL_HALF = 4.5                    # the column's half width
PILOT_DEEP = 8.2                  # R3: through the thread zone, so an M3x8 can never bottom out
PLATE_M = 2.55                    # armour: plates start this far inside the plate's edge (r4's layout exactly, for "keep")
PRY = dict(d_in=0.2, half=3.0, deep=1.0)   # a notch under each ear's end: a fingernail or the T9's tip lifts the plate out
PLATE_CH = 0.4                    # chamfer on the plate's lower edge (first layers bulge; the rebate's corner is never sharp)
VARIANTS = {"keep": 56.5, "slim": 53.0}
CHOSEN = "slim"


def crect(x0, x1, y0, y1, c):
    """rectangle with 45 deg corners, counter-clockwise"""
    return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]


def area2(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))


def offset_poly(p, d):
    """mitre offset of a simple polygon; d > 0 grows it (mk1_armour_r4's, unchanged)"""
    ccw = area2(p) > 0
    n, out = len(p), []
    for i in range(n):
        p0, p1, p2 = p[i - 1], p[i], p[(i + 1) % n]
        def nrm(a, b):
            ex, ey = b[0] - a[0], b[1] - a[1]
            L = math.hypot(ex, ey)
            return ((ey / L, -ex / L) if ccw else (-ey / L, ex / L))
        n1, n2 = nrm(p0, p1), nrm(p1, p2)
        den = 1.0 + n1[0] * n2[0] + n1[1] * n2[1]
        out.append((p1[0] + d * (n1[0] + n2[0]) / den, p1[1] + d * (n1[1] + n2[1]) / den))
    return out


def prism(poly, z0, z1):
    return Pos(0, 0, z0) * extrude(make_face(Polyline(*poly, close=True)), z1 - z0, dir=(0, 0, 1))


def stand_y(z, offset=0.0):
    """y of the stand plane (or of its inner face, offset perpendicular) at height z"""
    return Y_BOT + offset / math.cos(math.radians(STAND_DEG)) + R.STAND_TAN * (z - FRONT)


class Geo:
    """every derived number of one variant"""
    def __init__(self, BACK):
        self.BACK = BACK
        self.C_BACK = BACK - Z_FAC
        self.SEAT = BACK - PANEL_T                 # plate underside = ledge = lug seats
        self.ZN = self.SEAT - NOSE                 # where the inner slopes end
        t = self.C_BACK + RIM
        self.T = t
        # rebate: the plan outline moved in by bevel + rim; its bottom edge keeps off the stand wall's inner face
        self.c_reb = max(C_PLAN - (2.0 - math.sqrt(2.0)) * t, 1.0)
        self.y0r = max(PY[0] + t, stand_y(BACK, WALL) + 0.3)
        self.x0r, self.x1r, self.y1r = PX[0] + t, PX[1] - t, PY[1] - t
        self.rebate = crect(self.x0r, self.x1r, self.y0r, self.y1r, self.c_reb)
        self.plate = offset_poly(self.rebate, -GAP)
        self.x0p, self.x1p, self.y0p, self.y1p = self.x0r + GAP, self.x1r - GAP, self.y0r + GAP, self.y1r - GAP
        # ledges: as wide as the stack lets the 45 deg slope under them be
        sx, sy = STACK["x"], STACK["y"]
        room = self.ZN - STACK["z"][1] - STACK_CLEAR * math.sqrt(2.0)       # how far the slope may run past the stack edge
        self.ledge = dict(D=min(LEDGE_NOM["D"], (sx[0] - self.x0r) + room), C=min(LEDGE_NOM["C"], (self.x1r - sx[1]) + room),
                          top=min(LEDGE_NOM["top"], (self.y1r - sy[1]) + room), bot=min(LEDGE_NOM["bot"], (sy[0] - self.y0r) + room))
        self.ledge = {k: math.floor(v * 10.0) / 10.0 for k, v in self.ledge.items()}
        # the opening is a plain rectangle ON PURPOSE. A cut corner would give the ring a fifth, diagonal slope,
        # and that one runs straight into the stack's top corners (first build: 11 mm3 of overlap, found by the
        # measured gap). With square corners the two side slopes meet in a hip that clears them.
        xo0, xo1 = self.x0r + self.ledge["D"], self.x1r - self.ledge["C"]
        yo0, yo1 = self.y0r + self.ledge["bot"], self.y1r - self.ledge["top"]
        self.opening = [(xo0, yo0), (xo1, yo0), (xo1, yo1), (xo0, yo1)]
        # armour layout on the plate (r4's, tied to the plate's edges) -> where the ears go
        self.xa, self.xf = self.x0p + PLATE_M, self.x1p - PLATE_M
        self.yb, self.yt = self.y0p + PLATE_M, self.y1p - PLATE_M
        self.LUG_Y = (self.yb + 5.0, self.yt - 7.0)       # lower ears continue the long bottom plate, upper ears the top L plates
        self.ZK = self.SEAT - PILOT_DEEP - 4.0           # where a column's corbel leaves the wall
        self.lugs = [(side, y) for side in ("D", "C") for y in self.LUG_Y]

    def wall(self, side):
        """(x of the wall's outer face, +1 if 'in' is +x)"""
        return (PX[0], 1) if side == "D" else (PX[1], -1)

    def screw_xy(self, side, y):
        xw, s = self.wall(side)
        return (xw + s * LUG_AX, y)


def dbox(g, side, d0, d1, y0, y1, z0, z1):
    """box given by its distance IN from a side wall's outer face"""
    xw, s = g.wall(side)
    xa, xb = sorted((xw + s * d0, xw + s * d1))
    return Pos((xa + xb) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(xb - xa, y1 - y0, z1 - z0)


def dprofile(g, side, pts, y0, y1):
    """a (d, z) profile extruded along y from y0 to y1 (explicit direction: see r3's extrude trap)"""
    xw, s = g.wall(side)
    face = make_face(Plane.XZ * Polyline(*[(xw + s * d, z) for d, z in pts], close=True))
    return Pos(0, y0, 0) * extrude(face, y1 - y0, dir=(0, 1, 0))


def plan_prism(x0, x1, y0, y1, z0, z1, c):
    b = Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)
    return chamfer(b.edges().filter_by(Axis.Z), c)


def hump_outer(g):
    return B3.faceted(*PX, *PY, SKIRT_Z - 0.5, g.BACK, C_PLAN, g.C_BACK)


def hump_cavity(g):
    """the electronics cavity, open through the back: straight walls (2.5), then the ring's 45 deg
    inner slopes up to the opening, the nose, the rebate."""
    DROP = 30.0
    walls = plan_prism(PX[0] + WALL, PX[1] - WALL, PY[0] + WALL, PY[1] - WALL, CAV_Z, g.ZN + 5.0, C_PLAN - K_IN)
    lo = Pos(0, 0, g.ZN) * make_face(Polyline(*g.opening, close=True))
    hi = Pos(0, 0, g.ZN - DROP) * make_face(Polyline(*offset_poly(g.opening, DROP), close=True))
    under = loft([hi, lo], ruled=True)                                        # inside the slopes
    under += Pos(40, -20, (g.ZN - DROP + 0.5) / 2 - 5.0) * Box(400, 400, g.ZN - DROP + 0.5 + 10.0)   # and everything below them
    cav = walls & under
    cav += prism(g.opening, g.ZN - 0.5, g.SEAT + 0.3)                         # the nose
    cav += prism(g.rebate, g.SEAT, g.BACK + 1.0)                              # the rebate
    return cav


def lug_outer(g, side, y):
    """what a lug adds to the OUTSIDE: the block on the bevel under the ear, and the part standing
    proud of the wall, with a 45 deg underside. (Whatever of it falls inside the cavity is removed
    with the cavity.)"""
    h = LUG_W / 2 + GAP
    top = dbox(g, side, 0.0, g.T + 0.5, y - h, y + h, Z_FAC, g.SEAT)
    pts = [(1.0, g.SEAT), (-LUG_OUT, g.SEAT), (-LUG_OUT, Z_FAC), (0.0, Z_FAC - LUG_OUT), (1.0, Z_FAC - LUG_OUT)]
    return top + dprofile(g, side, pts, y - h, y + h)


def lug_column(g, side, y):
    """the column on the wall's inside, beside the stack: it carries the pilot. 45 deg corbel under
    it; it starts 1 mm inside the wall so the two are one piece (R3: a boss that only touches does
    not fuse)."""
    pts = [(WALL - 1.0, g.ZK), (WALL, g.ZK), (COL_IN, g.ZK + (COL_IN - WALL)), (COL_IN, g.SEAT), (WALL - 1.0, g.SEAT)]
    return dprofile(g, side, pts, y - COL_HALF, y + COL_HALF)


def body(g):
    # ---- outer solid ----
    p = extrude(rrect(-X_OUT, X_OUT, Y_BOT, Y_TOPF, R_OUT), SKIRT_Z)                 # skirt (R3)
    p += hump_outer(g)
    p += pod_outer()
    for sgn in (1, -1):                                                              # boss towers (R3)
        for yc in FRAME_BOSS["ys"]:
            p += Pos(sgn*(93.0+X_OUT)/2, yc, (SKIRT_Z+21.0)/2) * Box(X_OUT-93.0, 20.0, 21.0-SKIRT_Z)
    for side, y in g.lugs:
        p += lug_outer(g, side, y)

    # ---- interior ----
    inner = extrude(rrect(-X_OUT+WALL, X_OUT-WALL, Y_BOT+WALL, Y_TOPF-WALL, SKIRT_CAV_R), CAV_Z+2)
    inner = Pos(0, 0, -2) * inner
    inner += hump_cavity(g)                                                          # OPEN at the back
    inner += pod_cavity()
    for sgn in (1, -1):                                                              # tower pockets (R3)
        for yc in FRAME_BOSS["ys"]:
            inner += Pos(sgn*(95.5+101.5)/2, yc, 22.0/2) * Box(101.5-95.5, 13.0, 22.0)
    RELIEF, RZ = 0.6, 0.8                                                            # lead-in relief (R3)
    inner += Pos(0, 0, -2) * extrude(rrect(-X_OUT+WALL-RELIEF, X_OUT-WALL+RELIEF,
                                           Y_BOT+WALL-RELIEF, Y_TOPF-WALL+RELIEF,
                                           SKIRT_CAV_R), 2 + RZ)
    for sgn in (1, -1):
        for yc in FRAME_BOSS["ys"]:
            inner += Pos(sgn*(95.5+101.5)/2, yc, (-2+RZ)/2) * \
                     Box(101.5-95.5+2*RELIEF, 13.0+2*RELIEF, 2+RZ)
    inner -= stand_cutter(WALL / math.cos(math.radians(STAND_DEG)))
    p -= inner

    # ---- the wire way: skirt roof cut away under the pod's cavity (r3) ----
    wx0, wx1 = POD_X[0] + WALL, POD_X[1] - WALL
    ty0 = POD_BACK_Y + WALL
    p -= Pos((wx0+wx1)/2, (ty0 + TROUGH_Y1)/2, (CAV_Z - 1.5 + SKIRT_Z + 0.5)/2) * \
         Box(wx1-wx0, TROUGH_Y1 - ty0, SKIRT_Z + 0.5 - (CAV_Z - 1.5))

    # ---- HUD cap bosses + pilots (r3) ----
    p += cap_bosses()
    for (sx, a) in cap_screws():
        p -= axis_cyl(sx, a, L_REAR - CAP_PILOT_DEEP, L_REAR + 0.5, PILOT_D/2)

    # ---- the plate's four lugs: column, ear slot, pilot ----
    h = LUG_W / 2 + GAP
    for side, y in g.lugs:
        p += lug_column(g, side, y)
    for side, y in g.lugs:
        p -= dbox(g, side, -LUG_OUT - 1.0, g.T + 0.5, y - h, y + h, g.SEAT, g.BACK + 1.0)       # where the ear lies
        p -= dbox(g, side, -LUG_OUT - 1.0, PRY["d_in"], y - PRY["half"], y + PRY["half"], g.SEAT - PRY["deep"], g.SEAT + 0.5)   # pry notch
        sx, sy = g.screw_xy(side, y)
        p -= Pos(sx, sy, g.SEAT + 0.5 - (PILOT_DEEP + 0.5) / 2) * Cylinder(PILOT_D / 2, PILOT_DEEP + 0.5)

    # ---- openings (r3) ----
    p -= Pos((ETH_FACE_X + PX[1] + 5.0)/2, (SIDE_Y[0]+SIDE_Y[1])/2, (SIDE_WIN["z"][0]+SIDE_WIN["z"][1])/2) * \
         Box(PX[1] + 5.0 - ETH_FACE_X, SIDE_Y[1]-SIDE_Y[0], SIDE_WIN["z"][1]-SIDE_WIN["z"][0])
    p -= wedge_x(PX[1]-WALL, PX[1], SIDE_WIN["z"][1], True, SIDE_Y[0], SIDE_Y[1], 3.0)     # upper edge
    p -= wedge_x(PX[1]-WALL, PX[1], SIDE_WIN["z"][0], False, SIDE_Y[0], SIDE_Y[1], 0.5)    # lower edge
    p -= Pos((TOP_NOTCH_X[0]+TOP_NOTCH_X[1])/2, PY[1], (CAV_Z+TOP_WIN["z_top"])/2) * \
         Box(TOP_NOTCH_X[1]-TOP_NOTCH_X[0], 10, TOP_WIN["z_top"]-CAV_Z)
    p -= edge_wedge_yz(PY[1]-WALL, PY[1], TOP_WIN["z_top"], True, TOP_NOTCH_X[0], TOP_NOTCH_X[1])
    for y in VENT["ys"]:
        p -= Pos(PX[0] + WALL/2, y, (VENT["z"][0]+VENT["z"][1])/2) * Box(WALL + 3.0, VENT["w"], VENT["z"][1]-VENT["z"][0])
    for sgn in (1, -1):
        for yc in FRAME_BOSS["ys"]:
            p -= Pos(sgn*100.0, yc, FRAME_BOSS["pilot_z"]) * Rot(Y=90) * Cylinder(CLEAR_D/2, 14)
            p -= Pos(sgn*(X_OUT-HEAD_DEEP/2), yc, FRAME_BOSS["pilot_z"]) * Rot(Y=90) * \
                 Cylinder(HEAD_D/2, HEAD_DEEP+0.02)

    # ---- OLED seat on the facet (R3's, at HUD_X) ----
    lip, seat = OLED["lip"], OLED["seat"]
    for sx in (1, -1):
        for sy in (1, -1):
            p += on_facet(OLED_ALONG, Pos(sx*OLED["holes"]/2, sy*OLED["holes"]/2, (2.0+seat)/2) *
                          Cylinder(3.0, seat-2.0))
    ap = Pos(0, 0, (seat - 1.0)/2) * Box(OLED["apert"][0], OLED["apert"][1], seat + 1.0)
    pocket = Pos(0, 0, (lip+seat)/2) * Box(OLED["pocket"][0], OLED["pocket"][1], seat-lip)
    p -= on_facet(OLED_ALONG, ap + pocket)
    for sx in (1, -1):
        for sy in (1, -1):
            p -= on_facet(OLED_ALONG, Pos(sx*OLED["holes"]/2, sy*OLED["holes"]/2, (lip+seat+0.1)/2) *
                          Cylinder(OLED["pilot_d"]/2, seat+0.1-lip))

    p -= stand_cutter()
    return p


def plate(g):
    """the back plate, in place: flat, PANEL_T thick, four ears, four M3 clearance holes with
    counterbores. Prints flat, inside face down."""
    q = prism(g.plate, g.SEAT, g.BACK)
    for side, y in g.lugs:
        q += dbox(g, side, -LUG_OUT + 0.3, g.T + GAP + 1.0, y - LUG_W / 2, y + LUG_W / 2, g.SEAT, g.BACK)
    low = [e for e in q.edges() if abs(e.center().Z - g.SEAT) < 1e-6 and abs(e.bounding_box().max.Z - e.bounding_box().min.Z) < 1e-6]
    q = chamfer(low, PLATE_CH)                               # the whole lower outline, ears included
    for side, y in g.lugs:
        sx, sy = g.screw_xy(side, y)
        q -= Pos(sx, sy, g.SEAT + PANEL_T / 2) * Cylinder(CLEAR_D / 2, PANEL_T + 2.0)
        q -= Pos(sx, sy, g.BACK - HEAD_DEEP / 2 + 0.25) * Cylinder(HEAD_D / 2, HEAD_DEEP + 0.5)
    return q


def plate_for_print(q, g):
    """inside face on the bed, centred"""
    bb = q.bounding_box()
    return Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -g.SEAT) * q


def plate_screw_heads(g):
    out = None
    for side, y in g.lugs:                                   # M3x8 button heads, sunk 1.7 into the ears
        sx, sy = g.screw_xy(side, y)
        s = Pos(sx, sy, g.BACK - HEAD_DEEP + 0.8) * Cylinder(2.85, 1.6)
        out = s if out is None else out + s
    return out


def report(name, s):
    bb = s.bounding_box()
    print("%-22s valid %s  solids %d  vol %6.1f cm3  x %7.2f..%7.2f  y %7.2f..%7.2f  z %6.2f..%6.2f" % (
        name, s.is_valid, len(s.solids()), s.volume/1000, bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z), flush=True)


if __name__ == "__main__":
    import sys, time
    for nm in (sys.argv[1:] or list(VARIANTS)):
        g = Geo(VARIANTS[nm])
        print("== %s: BACK %.1f, bevel %.1f, plate z %.1f..%.1f, gap to the stack %.1f" % (nm, g.BACK, g.C_BACK, g.SEAT, g.BACK, g.SEAT - STACK["z"][1]))
        print("   rebate x %.2f..%.2f  y %.2f..%.2f (corner %.2f); ledges %s" % (g.x0r, g.x1r, g.y0r, g.y1r, g.c_reb, g.ledge))
        print("   plate %.1f x %.1f; lugs at y %.2f and %.2f; column from z %.1f" % (g.x1p - g.x0p, g.y1p - g.y0p, g.LUG_Y[0], g.LUG_Y[1], g.ZK))
        t = time.time(); b = body(g); report("body (plain)", b); print("   built in %.0f s" % (time.time() - t))
        q = plate(g); report("plate (plain)", q)
