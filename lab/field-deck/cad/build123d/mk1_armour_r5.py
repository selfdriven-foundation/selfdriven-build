"""MK-I r5 — the armour, for a body with a separate back plate (mk1_body_r5.py).

r4's pattern, made the same way (nothing added: a 0.75 mm pocket, plates left standing, every edge
a 45 deg bevel, hex sockets 0.6 deep), with these differences:
  * the back's plates are on the BACK PLATE now (face "PK"). The pocket runs out over the plate's
    edge, so the joint to the body's rim sits in the bottom of the channel round the plate group.
    The four ears stay at full height and continue the plates next to them: lower ears the long
    bottom plate, upper ears the two top L plates. Each ear carries a REAL screw.
  * the side facets (LF, RF) are interrupted by the lugs: two strips between them ("keep" depth).
    At the "slim" depth the facets are 9.2 wide - too narrow for plates - and get a row of hex
    sockets instead.
  * the left and right walls' pockets stop at z 41.5 (r4: 44.5 / 43): under a lug the screw pilot
    comes down to z 42.3, and a lug's proud part starts at z 45.
Faces are built per variant: faces(g) for the body, plate_face(g) for the plate.
"""
from build123d import *
import math
import r3_params as R
import mk1_body_r3 as B3
import mk1_body_r5 as B5
from mk1_body_r5 import offset_poly, area2, Z_FAC, LUG_W, LUG_OUT, GAP, PLATE_M

DEPTH = 0.75
HEX_AF, HEX_D = 4.0, 0.6
EPS = 0.4
A = 1.0 / math.sqrt(2.0)
PX, PY = B3.PX, B3.PY
Z_SK = R.SKIRT_Z


def rect(a0, a1, b0, b1):
    return [(a0, b0), (a1, b0), (a1, b1), (a0, b1)]


def _face(origin, U, N, to_uv, region, plates, hexes, title):
    return dict(origin=origin, U=U, N=N, to_uv=to_uv, region=region, plates=plates, hexes=hexes, title=title)


def faces(g):
    """the decorated faces of the BODY, for one variant"""
    F = {}
    S = g.C_BACK * math.sqrt(2.0)                       # a facet's width up the slope
    wide = S > 12.0
    SV, PV = (2.0, S - 2.0), (3.6, S - 3.6)
    strips = lambda spans: [rect(a0, a1, *PV) for a0, a1 in spans]
    strip_hex = lambda spans, af=3.2: [(a, S / 2, af, 0.0) for a0, a1 in spans for a in (a0 + 4.0, a1 - 4.0)]
    keep_out = LUG_W / 2 + GAP + 2.0                    # a lug block's half width + 2 mm of plain facet
    lo, hi = g.LUG_Y[0] + keep_out, g.LUG_Y[1] - keep_out

    # ---- the three facets round the back ----
    if wide:
        TF_SP = [(-24.0, -2.0), (1.0, 36.0), (39.0, 61.5)]
        tf = (rect(-26.0, 63.5, *SV), strips(TF_SP), strip_hex(TF_SP))
        mid = (lo + hi) / 2
        LR_SP = [(lo + 2.0, mid - 1.5), (mid + 1.5, hi - 2.0)]
        lr = (rect(lo, hi, *SV), strips(LR_SP), strip_hex(LR_SP))
    else:
        tf = (None, [], [(-22.0 + 11.6 * k, S / 2, 3.2, 0.0) for k in range(8)])
        n = 6
        lr = (None, [], [(lo + 3.0 + (hi - lo - 6.0) * k / (n - 1), S / 2, 3.2, 0.0) for k in range(n)])
    F["TF"] = _face((0, PY[1], Z_FAC), (-1, 0, 0), (0, A, A), lambda a, b: (-a, b), *tf, "top facet")
    F["LF"] = _face((PX[1], 0, Z_FAC), (0, 1, 0), (A, 0, A), lambda a, b: (a, b), *lr, "left facet (handle side), between the lugs")
    F["RF"] = _face((PX[0], 0, Z_FAC), (0, -1, 0), (-A, 0, A), lambda a, b: (-a, b), *lr, "right facet, between the lugs")

    # ---- walls ----
    # LW and RW stop at z WALL_TOP. A screw pilot in a lug column runs down to z SEAT - 8.2 and its outer edge lies
    # 0.45 mm inside the wall; a pocket reaching up there would leave 1.31 mm between pocket and pilot (found by the
    # rays, first r5 build). The pocket's bevel must end below the pilot's foot.
    WALL_TOP = g.SEAT - B5.PILOT_DEEP - DEPTH - 0.05          # 41.5 at the slim depth (r4: 43 / 44.5)
    F["LW"] = _face((PX[1], 0, 0), (0, 1, 0), (1, 0, 0), lambda a, b: (a, b),
                    rect(-74.5, -31.0, 9.0, WALL_TOP),
                    [rect(-72.5, -54.25, 11.0, WALL_TOP - 2.0), rect(-51.25, -33.0, 11.0, WALL_TOP - 2.0)],
                    [(y, z, HEX_AF, 30.0) for y in (-68.0, -58.75, -46.75, -37.5) for z in (15.5, WALL_TOP - 6.5)], "left wall, below the sockets")
    F["RW"] = _face((PX[0], 0, 0), (0, -1, 0), (-1, 0, 0), lambda a, b: (-a, b),
                    rect(-74.5, 27.1, 9.0, WALL_TOP),
                    [rect(-72.0, 24.6, 10.4, WALL_TOP - 2.0)],
                    [(y, z, HEX_AF, 30.0) for y in (-67.8, 20.4) for z in (14.9, WALL_TOP - 6.5)], "right wall: the grille plate")
    F["TW"] = _face((0, PY[1], 0), (-1, 0, 0), (0, 1, 0), lambda a, b: (-a, b),
                    rect(-28.6, -5.5, 9.0, 44.5),
                    [rect(-26.6, -7.5, 11.0, 42.5)],
                    [(x, z, HEX_AF, 30.0) for x in (-22.1, -12.0) for z in (15.5, 38.0)], "top wall, beside the top opening")

    # ---- the skirt (r4's, unchanged) ----
    CK_REGION = [(-101.0, -58.5), (-41.2, -58.5), (-41.2, 68.5), (-90.0, 68.5), (-90.0, 42.0), (-101.0, 42.0)]
    CK_PLATES = [rect(-88.0, -43.2, 44.0, 66.5),
                 rect(-99.0, -43.2, 12.0, 40.0),
                 rect(-99.0, -72.6, -22.0, 9.0), rect(-69.6, -43.2, -22.0, 9.0),
                 [(-99.0, -50.5), (-93.0, -56.5), (-43.2, -56.5), (-43.2, -25.0), (-99.0, -25.0)]]
    CK_HEX = [(-83.5, 62.0), (-47.7, 62.0), (-83.5, 48.5), (-47.7, 48.5),
              (-94.5, 35.5), (-47.7, 35.5), (-94.5, 16.5), (-47.7, 16.5),
              (-94.5, 4.5), (-77.1, -17.5), (-65.1, 4.5), (-47.7, -17.5),
              (-94.5, -29.5), (-47.7, -29.5), (-90.5, -50.5), (-47.7, -52.0)]
    sk = ((0, 0, Z_SK), (1, 0, 0), (0, 0, 1), lambda a, b: (a, b))
    F["CK"] = _face(*sk, CK_REGION, CK_PLATES, [(a, b, HEX_AF, 0.0) for a, b in CK_HEX], "skirt: right cheek")
    LS_Y = [(4.0, 31.6), (-26.0, 1.0), (-56.5, -29.0)]
    F["LS"] = _face(*sk, rect(78.7, 101.0, -58.5, 33.6), [rect(80.7, 99.0, y0, y1) for y0, y1 in LS_Y],
                    [(89.85, y, HEX_AF, 0.0) for y0, y1 in LS_Y for y in (y0 + 4.5, y1 - 4.5)], "skirt: handle side")
    F["TS"] = _face(*sk, rect(-35.2, 57.0, 44.0, 68.5), [rect(-33.2, -4.2, 46.0, 66.5), rect(-1.2, 55.0, 46.0, 66.5)],
                    [(x, y, HEX_AF, 0.0) for x in (-28.7, -8.7, 3.3, 50.5) for y in (50.5, 62.0)], "skirt: above the body")
    return F


def plate_layout(g):
    """r4's seven plates on the back, tied to the plate's edges (identical to r4 at the "keep" depth)"""
    xa, xf, yb, yt = g.xa, g.xf, g.yb, g.yt
    xb, xc, xd, xe = -6.2, -3.2, 40.7, 43.7
    yl = yb + 13.0                                      # the L plates start 3 mm above the long bottom plate
    plates = {
        "centre (icon later)": [(xc, -44.0), (34.7, -44.0), (xd, -38.0), (xd, 1.0), (2.8, 1.0), (xc, -5.0)],
        "long bottom (spec line later)": rect(xa, xf, yb, yb + 10.0),
        "top-left L":     [(xa, -20.0), (xb, -20.0), (xb, -3.76), (1.56, 4.0), (12.0, 4.0), (12.0, yt), (xa, yt)],
        "top centre":     rect(15.0, 37.7, 4.0, yt),
        "top-right L":    [(40.7, 4.0), (xe, 4.0), (xe, -17.0), (xf, -17.0), (xf, yt), (40.7, yt)],
        "bottom-left L":  [(xa, yl), (17.25, yl), (17.25, -47.0), (xb, -47.0), (xb, -23.0), (xa, -23.0)],
        "bottom-right L": [(20.25, yl), (xf, yl), (xf, -20.0), (xe, -20.0), (xe, -39.24), (35.94, -47.0), (20.25, -47.0)],
    }
    hexes = [(1.3, -39.5), (36.2, -3.5), (3.3, -5.5), (34.2, -37.5),                                    # centre
             (xa + 16.0, yb + 5.0), (xf - 16.0, yb + 5.0),                                              # long bottom (clear of the ears' real screws)
             (xa + 4.5, yt - 4.5), (7.5, yt - 4.5), ((xa + xb) / 2, -15.5),                             # top-left L
             (19.5, yt - 4.5), (33.2, yt - 4.5), (19.5, 8.5), (33.2, 8.5),                              # top centre
             (45.2, yt - 4.5), (xf - 4.5, yt - 4.5), ((xe + xf) / 2, -12.5),                            # top-right L
             (xa + 4.5, -27.5), (xa + 4.5, yl + 4.5), (12.75, yl + 5.5),                                # bottom-left L
             (24.75, yl + 5.5), (xf - 4.5, yl + 4.5), ((xe + xf) / 2, -24.5)]                           # bottom-right L
    return plates, hexes


def ear_islands(g):
    """each ear stays at full height, from beyond its end to 2 mm into the plate beside it. 2 mm, not
    less: every island's top is 0.75 smaller than its outline, so two islands only read as ONE raised
    surface if they overlap by more than 1.5 (with 0.45 a V groove 0.5 deep ran between ear and plate)."""
    out = []
    for side, y in g.lugs:
        xw, s = g.wall(side)
        x_out = xw - s * (LUG_OUT + 1.0)
        x_in = (g.xa + 2.0) if side == "D" else (g.xf - 2.0)
        out.append(rect(min(x_out, x_in), max(x_out, x_in), y - LUG_W / 2, y + LUG_W / 2))
    return out


def plate_face(g):
    plates, hexes = plate_layout(g)
    return _face((0, 0, g.BACK), (1, 0, 0), (0, 0, 1), lambda a, b: (a, b),
                 offset_poly(g.plate, 0.3), list(plates.values()) + ear_islands(g),
                 [(a, b, HEX_AF, 0.0) for a, b in hexes], "BACK PLATE")


# ------------------------------------------------------------------ geometry (r4's, unchanged)
def bevel_solid(poly, z0, z1, grow):
    lo = Pos(0, 0, z0) * make_face(Polyline(*poly, close=True))
    hi = Pos(0, 0, z1) * make_face(Polyline(*offset_poly(poly, grow), close=True))
    return loft([lo, hi], ruled=True)


def hex_cut(u, v, af, rot):
    r = af / math.sqrt(3.0)
    return Pos(u, v, -HEX_D) * Rot(Z=rot) * extrude(RegularPolygon(r, 6), amount=HEX_D + EPS, dir=(0, 0, 1))


def plane_of(f):
    return Plane(origin=f["origin"], x_dir=f["U"], z_dir=f["N"])


def face_cutters(f):
    """(pocket or None, hexes or None) for one face, already in place"""
    uv = lambda poly: [f["to_uv"](a, b) for a, b in poly]
    h = DEPTH + EPS
    slab = None
    if f["region"] is not None:
        slab = bevel_solid(uv(f["region"]), -DEPTH, EPS, +h)
        for pl in f["plates"]:
            slab -= bevel_solid(uv(pl), -DEPTH - 0.01, EPS + 0.01, -(h + 0.02))
    hexes = None
    for (a, b, af, rot) in f["hexes"]:
        u, v = f["to_uv"](a, b)
        c = hex_cut(u, v, af, rot)
        hexes = c if hexes is None else hexes + c
    loc = plane_of(f).location
    return (None if slab is None else loc * slab), (None if hexes is None else loc * hexes)


def world(f, a, b, w=0.0):
    u, v = f["to_uv"](a, b)
    pl = plane_of(f)
    p = pl.origin + pl.x_dir * u + pl.y_dir * v + pl.z_dir * w
    return (p.X, p.Y, p.Z)


def armoured_body(g, verbose=False):
    import time
    p = B5.body(g)
    for name, f in faces(g).items():
        t = time.time()
        pocket, hexes = face_cutters(f)
        if pocket is not None:
            p -= pocket
        if hexes is not None:
            p -= hexes
        if verbose:
            print("   %-3s cut in %.1f s  (valid %s, solids %d)" % (name, time.time() - t, p.is_valid, len(p.solids())), flush=True)
    return p


def armoured_plate(g):
    q = B5.plate(g)
    pocket, hexes = face_cutters(plate_face(g))
    q -= pocket
    q -= hexes
    return q


if __name__ == "__main__":
    import sys
    for nm in (sys.argv[1:] or list(B5.VARIANTS)):
        g = B5.Geo(B5.VARIANTS[nm])
        F = faces(g)
        n_pl = sum(len(f["plates"]) for f in F.values()); n_hx = sum(len(f["hexes"]) for f in F.values())
        pf = plate_face(g)
        print("%s: body faces %d, plates %d, hex sockets %d | back plate: %d plates + 4 ears, %d hex sockets, 4 real screws" % (
            nm, len(F), n_pl, n_hx, len(pf["plates"]) - 4, len(pf["hexes"])))
