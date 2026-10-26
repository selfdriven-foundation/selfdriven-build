"""MK-I r4 — the ARMOUR on the body (owner, 2026-10-02: "can the back and the whole body have the
terminator style pattern?").

Reference = the August armour set (`4 - Archive/FieldDeck-Armor-Map.png`): raised plates with hex
bolts, an L-shaped plate here and there, a centre plate for the icon, a long plate for the spec
line. It is our own artwork: no film imagery, no logos.

HOW IT IS MADE (and why): nothing is ADDED to the body — the outside stays where r3 put it, so no
clearance changes. On each decorated face a shallow POCKET (0.75 mm) is cut, and the PLATES are the
islands left standing in it. Every pocket edge and every plate edge is a 45 deg bevel, so on the
vertical walls (printed mouth-down) nothing hangs over. The "bolts" are hex sockets 0.6 deep in the
plates, the same idea as the front's fastener points. Wall left under a pocket: 1.75 mm; under a
hex socket: 1.9 mm.

Engravings are NOT part of this (plan item D8 is still the owner's to decide). The centre plate on
the back, the long plate under it and the top plate on the right cheek are left clear for the icon,
the spec line and the name.

Faces. Each has a frame (origin, U along the face, N outward; V = N x U) and its plates are written
in that face's NATURAL coordinates, mapped to (u, v) by `to_uv`:
  BK back flat (x, y) · SK skirt (x, y) · LW / RW left / right wall (y, z) · TW top wall (x, z)
  TF / LF / RF the 45 deg facets round the back (x or y, s = mm up the slope)
The stand bevel (it stands on the desk), the corner facets, the towers and the pod are left plain.
"""
from build123d import *
import math
import r3_params as R
import mk1_body_r3 as B3

DEPTH = 0.75                      # plates stand this proud of the pocket floor
HEX_AF, HEX_D = 4.0, 0.6          # hex socket: across flats, depth
EPS = 0.4                         # cutters run this far past the surface (no coplanar faces)
A = 1.0 / math.sqrt(2.0)
PX, PY, BACK = B3.PX, B3.PY, R.BACK
Z_FAC = BACK - B3.C_BACK          # 46.5: where the back-edge facets start
S_FAC = B3.C_BACK * math.sqrt(2.0)  # 14.14: a facet's width up the slope
Z_SK = R.SKIRT_Z                  # 7.0


def rect(a0, a1, b0, b1):
    return [(a0, b0), (a1, b0), (a1, b1), (a0, b1)]


FACES = {}

def face(name, origin, U, N, to_uv, region, plates, hexes, title):
    # every pocket outline stays >= 2.0 mm from its face's edges: 1.25 mm of flat rim is left after the bevel
    FACES[name] = dict(origin=origin, U=U, N=N, to_uv=to_uv, region=region, plates=plates, hexes=hexes, title=title)


# ------------------------------------------------------------------ BK: the back flat (x, y)
xa, xb, xc, xd, xe, xf = -24.2, -6.2, -3.2, 40.7, 43.7, 61.7
BK_PLATES = {
    "name (icon later)":  [(xc, -44.0), (34.7, -44.0), (xd, -38.0), (xd, 1.0), (2.8, 1.0), (xc, -5.0)],
    "data (spec line later)": rect(xa, xf, -70.0, -61.0),
    "top-left L":   [(xa, -20.0), (xb, -20.0), (xb, -3.76), (1.56, 4.0), (12.0, 4.0), (12.0, 22.6), (xa, 22.6)],
    "top centre":   rect(15.0, 37.7, 4.0, 22.6),
    "top-right L":  [(40.7, 4.0), (xe, 4.0), (xe, -17.0), (xf, -17.0), (xf, 22.6), (40.7, 22.6)],
    "bottom-left L": [(xa, -58.0), (17.25, -58.0), (17.25, -47.0), (xb, -47.0), (xb, -23.0), (xa, -23.0)],
    "bottom-right L": [(20.25, -58.0), (xf, -58.0), (xf, -20.0), (xe, -20.0), (xe, -39.24), (35.94, -47.0), (20.25, -47.0)],
}
BK_HEX = [(1.3, -39.5), (36.2, -3.5), (3.3, -5.5), (34.2, -37.5),               # name plate
          (-19.7, -65.5), (57.2, -65.5),                                          # data plate
          (-19.7, 18.1), (7.5, 18.1), (-15.2, -15.5),                             # top-left L
          (19.5, 18.1), (33.2, 18.1), (19.5, 8.5), (33.2, 8.5),                   # top centre
          (45.2, 18.1), (57.2, 18.1), (52.7, -12.5),                              # top-right L
          (-19.7, -27.5), (-19.7, -53.5), (12.75, -52.5),                         # bottom-left L
          (24.75, -52.5), (57.2, -53.5), (52.7, -24.5)]                           # bottom-right L
face("BK", (0, 0, BACK), (1, 0, 0), (0, 0, 1), lambda a, b: (a, b),
     rect(-26.2, 63.7, -72.0, 24.6), list(BK_PLATES.values()), [(a, b, HEX_AF, 0.0) for a, b in BK_HEX], "BACK")

# ------------------------------------------------------------------ the three facets round the back
SV = (2.0, S_FAC - 2.0)           # pocket across the slope: leaves a 1.25 mm flat rim at both edges of the facet
PV = (3.6, S_FAC - 3.6)           # plates across the slope: 6.94 wide
def strips(spans):
    return [rect(a0, a1, *PV) for a0, a1 in spans]
def strip_hex(spans, af=3.2):
    return [(a, S_FAC / 2, af, 0.0) for a0, a1 in spans for a in (a0 + 4.0, a1 - 4.0)]
TF_SP = [(-24.0, -2.0), (1.0, 36.0), (39.0, 61.5)]
face("TF", (0, PY[1], Z_FAC), (-1, 0, 0), (0, A, A), lambda a, b: (-a, b),
     rect(-26.0, 63.5, *SV), strips(TF_SP), strip_hex(TF_SP), "top facet")
LR_SP = [(-69.5, -40.0), (-37.0, -6.0), (-3.0, 22.0)]
face("LF", (PX[1], 0, Z_FAC), (0, 1, 0), (A, 0, A), lambda a, b: (a, b),
     rect(-71.5, 24.0, *SV), strips(LR_SP), strip_hex(LR_SP), "left facet (handle side)")
face("RF", (PX[0], 0, Z_FAC), (0, -1, 0), (-A, 0, A), lambda a, b: (-a, b),
     rect(-71.5, 24.0, *SV), strips(LR_SP), strip_hex(LR_SP), "right facet")

# ------------------------------------------------------------------ walls (y or x, z)
# left wall: only below the Eth/USB window (its lower chamfer runs to y -28)
face("LW", (PX[1], 0, 0), (0, 1, 0), (1, 0, 0), lambda a, b: (a, b),
     rect(-74.5, -31.0, 9.0, 44.5),
     [rect(-72.5, -54.25, 11.0, 42.5), rect(-51.25, -33.0, 11.0, 42.5)],
     [(y, z, HEX_AF, 30.0) for y in (-68.0, -58.75, -46.75, -37.5) for z in (15.5, 38.0)], "left wall, below the sockets")
# right wall: ONE plate carrying the nine air slots — a bolted grille
face("RW", (PX[0], 0, 0), (0, -1, 0), (-1, 0, 0), lambda a, b: (-a, b),
     rect(-74.5, 27.1, 9.0, 43.0),
     [rect(-72.0, 24.6, 10.4, 41.0)],
     [(y, z, HEX_AF, 30.0) for y in (-67.8, 20.4) for z in (14.9, 36.5)], "right wall: the grille plate")
# top wall: the blank part to the right of the top opening (seen from the back: its left)
face("TW", (0, PY[1], 0), (-1, 0, 0), (0, 1, 0), lambda a, b: (-a, b),
     rect(-28.6, -5.5, 9.0, 44.5),
     [rect(-26.6, -7.5, 11.0, 42.5)],
     [(x, z, HEX_AF, 30.0) for x in (-22.1, -12.0) for z in (15.5, 38.0)], "top wall, beside the top opening")

# ------------------------------------------------------------------ SK: the skirt (x, y)
# right cheek: clear of the two screw towers (x < -93 at y 45..65 and -81.5..-61.5)
CK_REGION = [(-101.0, -58.5), (-41.2, -58.5), (-41.2, 68.5), (-90.0, 68.5), (-90.0, 42.0), (-101.0, 42.0)]
CK_PLATES = [rect(-88.0, -43.2, 44.0, 66.5),                         # name plate (a name later, if wanted)
             rect(-99.0, -43.2, 12.0, 40.0),
             rect(-99.0, -72.6, -22.0, 9.0), rect(-69.6, -43.2, -22.0, 9.0),
             [(-99.0, -50.5), (-93.0, -56.5), (-43.2, -56.5), (-43.2, -25.0), (-99.0, -25.0)]]
CK_HEX = [(-83.5, 62.0), (-47.7, 62.0), (-83.5, 48.5), (-47.7, 48.5),
          (-94.5, 35.5), (-47.7, 35.5), (-94.5, 16.5), (-47.7, 16.5),
          (-94.5, 4.5), (-77.1, -17.5), (-65.1, 4.5), (-47.7, -17.5),
          (-94.5, -29.5), (-47.7, -29.5), (-90.5, -50.5), (-47.7, -52.0)]
face("CK", (0, 0, Z_SK), (1, 0, 0), (0, 0, 1), lambda a, b: (a, b),
     CK_REGION, CK_PLATES, [(a, b, HEX_AF, 0.0) for a, b in CK_HEX], "skirt: right cheek")
# strip on the handle side, between the two towers and below the HUD pod
LS_Y = [(4.0, 31.6), (-26.0, 1.0), (-56.5, -29.0)]
face("LS", (0, 0, Z_SK), (1, 0, 0), (0, 0, 1), lambda a, b: (a, b),
     rect(78.7, 101.0, -58.5, 33.6), [rect(80.7, 99.0, y0, y1) for y0, y1 in LS_Y],
     [(89.85, y, HEX_AF, 0.0) for y0, y1 in LS_Y for y in (y0 + 4.5, y1 - 4.5)], "skirt: handle side")
# strip above the body, up to the HUD pod. It starts at y 44: R3's top opening is cut 5 mm out into the
# skirt roof (to y 41.6), and a pocket must not run into that slot.
face("TS", (0, 0, Z_SK), (1, 0, 0), (0, 0, 1), lambda a, b: (a, b),
     rect(-35.2, 57.0, 44.0, 68.5), [rect(-33.2, -4.2, 46.0, 66.5), rect(-1.2, 55.0, 46.0, 66.5)],
     [(x, y, HEX_AF, 0.0) for x in (-28.7, -8.7, 3.3, 50.5) for y in (50.5, 62.0)], "skirt: above the body")


# ------------------------------------------------------------------ geometry
def area2(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))

def offset_poly(p, d):
    """mitre offset of a simple polygon; d > 0 grows it, d < 0 shrinks it; same number of corners"""
    ccw = area2(p) > 0
    n, out = len(p), []
    for i in range(n):
        p0, p1, p2 = p[i - 1], p[i], p[(i + 1) % n]
        def nrm(a, b):
            ex, ey = b[0] - a[0], b[1] - a[1]
            L = math.hypot(ex, ey)
            return ((ey / L, -ex / L) if ccw else (-ey / L, ex / L))          # outward normal of edge a->b
        n1, n2 = nrm(p0, p1), nrm(p1, p2)
        den = 1.0 + n1[0] * n2[0] + n1[1] * n2[1]
        out.append((p1[0] + d * (n1[0] + n2[0]) / den, p1[1] + d * (n1[1] + n2[1]) / den))
    return out

def bevel_solid(poly, z0, z1, grow):
    """solid between poly at z0 and poly offset by `grow` at z1 (a 45 deg flank when |grow| = z1 - z0)"""
    lo = Pos(0, 0, z0) * make_face(Polyline(*poly, close=True))
    hi = Pos(0, 0, z1) * make_face(Polyline(*offset_poly(poly, grow), close=True))
    return loft([lo, hi], ruled=True)

def hex_cut(u, v, af, rot):
    r = af / math.sqrt(3.0)
    return Pos(u, v, -HEX_D) * Rot(Z=rot) * extrude(RegularPolygon(r, 6), amount=HEX_D + EPS, dir=(0, 0, 1))

def plane_of(f):
    return Plane(origin=f["origin"], x_dir=f["U"], z_dir=f["N"])

def face_cutters(name):
    """(pocket, hexes) for one face, already in place"""
    f = FACES[name]
    uv = lambda poly: [f["to_uv"](a, b) for a, b in poly]
    h = DEPTH + EPS
    slab = bevel_solid(uv(f["region"]), -DEPTH, EPS, +h)                    # pocket, its rim bevelled outward
    for pl in f["plates"]:
        slab -= bevel_solid(uv(pl), -DEPTH - 0.01, EPS + 0.01, -(h + 0.02))  # plate, bevelled inward
    hexes = None
    for (a, b, af, rot) in f["hexes"]:
        u, v = f["to_uv"](a, b)
        c = hex_cut(u, v, af, rot)
        hexes = c if hexes is None else hexes + c
    loc = plane_of(f).location
    return loc * slab, (None if hexes is None else loc * hexes)

def world(name, a, b, w=0.0):
    """world point of a face's natural (a, b), w mm outside the surface"""
    f = FACES[name]
    u, v = f["to_uv"](a, b)
    pl = plane_of(f)
    p = pl.origin + pl.x_dir * u + pl.y_dir * v + pl.z_dir * w
    return (p.X, p.Y, p.Z)


if __name__ == "__main__":
    n_pl = sum(len(f["plates"]) for f in FACES.values()); n_hx = sum(len(f["hexes"]) for f in FACES.values())
    print("faces %d, plates %d, hex sockets %d" % (len(FACES), n_pl, n_hx))
    for nm, f in FACES.items():
        ar = abs(area2(f["region"])) / 2
        ap = sum(abs(area2(p)) / 2 for p in f["plates"])
        print("  %-3s %-34s pocket %7.0f mm2, plates %7.0f mm2 (%2d), hex %2d" % (nm, f["title"], ar, ap, len(f["plates"]), len(f["hexes"])))
