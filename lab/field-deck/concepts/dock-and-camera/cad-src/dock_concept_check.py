"""Checks of the dock CONCEPT (dock_concept.py) against the real r9 deck: bed fit, deck on the base, clearances."""
import math, numpy as np, trimesh
from build123d import import_step
import dock.dock_concept as D
import os
FD_STEP = os.environ.get("FD_STEP", "readback/item_r9_hud.step")   # the printed r9 read-back (Fusion v12); in the public
# repo use cad/MK1-r9_design_public_NOT-FOR-PRINT.step, whose body (the two names filled in) is 115741.7297 mm3
def vmatch(a, v):
    return abs(a - v) < 0.01 or (abs(v - 115715.2078) < 1e-6 and abs(a - 115741.7297) < 0.05)

sols = list(import_step(FD_STEP).solids())
pick = lambda v: [s for s in sols if vmatch(s.volume, v)][0]
def world_mesh(sh, tol=0.2):
    v, t = sh.tessellate(tol, 0.2)
    V = D.to_world(np.array([[p.X, p.Y, p.Z] for p in v])); return trimesh.Trimesh(V, np.array(t), process=False)
parts = {n: world_mesh(pick(v)) for n, v in (("body", 115715.2078), ("front", 129177.2313), ("grip", 96836.0778),
                                             ("backplate", 23686.9156), ("hudcap", 3782.2976), ("spkcover", 11190.0952))}
deck = trimesh.util.concatenate(list(parts.values()))
lo, hi = deck.bounds
print("deck in the dock (world): X %.1f..%.1f  Y %.1f..%.1f  Z %.1f..%.1f" % (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
FAIL = []
def chk(name, ok, val=""):
    print("  %-78s %-22s %s" % (name, val, "ok" if ok else "*** FAIL ***")); FAIL.append(name) if not ok else None
# 1 bed fit (A1 256 x 256 x 256)
for nm, (x0, x1) in (("left half", (D.X0, 0.0)), ("right half", (0.0, D.X1))):
    w, d_, h = x1 - x0, D.YB - 0, D.TOP
    chk("base %s fits the A1 bed: %.0f x %.0f x %.0f" % (nm, w, d_, h), max(w, d_, h) <= 250, "")
# 2 lowest point of the deck = the dock top
chk("deck's lowest point sits on the dock top (Z = %.1f)" % D.TOP, abs(lo[2] - D.TOP) < 0.05, "%.3f" % lo[2])
# 3 every vertex within 0.2 of the top lies over the base top (Y 109..226, X -152..152)
V = deck.vertices; on = V[V[:, 2] < D.TOP + 0.2]
chk("stand-face points over the base (X -152..152, Y 109..226)", on[:, 0].min() >= D.X0 and on[:, 0].max() <= D.X1 and on[:, 1].min() >= D.YS and on[:, 1].max() <= D.YB,
    "X %.1f..%.1f Y %.1f..%.1f" % (on[:, 0].min(), on[:, 0].max(), on[:, 1].min(), on[:, 1].max()))
# 4 grip clearance above the base top where it is over the base
g = parts["grip"].vertices; over = g[(g[:, 0] >= D.X0)]
chk("grip clears the base top where it is over it", over[:, 2].min() - D.TOP > 1.0, "%.2f mm" % (over[:, 2].min() - D.TOP))
# 5 lips and posts do not touch the deck: distance from the deck mesh to boxes
def box_pts(x0, x1, y0, y1, z0, z1, n=9):
    xs, ys, zs = np.linspace(x0, x1, n), np.linspace(y0, y1, n), np.linspace(z0, z1, n)
    return np.array([(x, y, z) for x in xs for y in ys for z in zs])
pq = trimesh.proximity.ProximityQuery(deck)
for nm, b in (("front lip", (-100, 100, 127.5, 130.5, D.TOP, D.TOP + 3)), ("right lip", (105, 108, 131, 152, D.TOP, D.TOP + 3)),
              ("post 1", (-60, -48, 205.0, 215, D.TOP, 76)), ("post 2", (4, 16, 205.0, 215, D.TOP, 76))):
    P = box_pts(*b); dmin = pq.signed_distance(P).max()  # >0 means inside the deck
    _, dist, _ = trimesh.proximity.closest_point(deck, P)
    chk("%s: no point inside the deck, nearest gap" % nm, dmin < 0 and dist.min() > 0.3, "%.2f mm" % dist.min())
# 6 the power lever stays reachable: nothing of the dock in front of its face
lev = D.to_world(np.array([[-38.7, -69.7, 17.1], [-38.7, -44.8, 35.7]]))
print("  power lever face (world): X %.1f  Y %.1f..%.1f  Z %.1f..%.1f" % (lev[0, 0], *sorted(lev[:, 1]), *sorted(lev[:, 2])))
chk("lever's bottom is above the dock top", min(lev[:, 2]) - D.TOP > 8, "%.1f mm above" % (min(lev[:, 2]) - D.TOP))
chk("knob is clear of the lever's finger space (X > lever + 60)", D.KNOB[0] - 12 > lev[0, 0] + 60, "%.1f mm" % (D.KNOB[0] - 12 - lev[0, 0]))
chk("posts are left of the lever face", 16 < lev[0, 0], "")
# 7 the deck lead: path length from the hub (inside, left end) to the port vs the hub's 200 mm lead
pts = np.array([(-120, 195, 20), (-128, 189, 30), (-128, 189, D.TOP), (-128, 189, 62), (-126, 188, 84), (-121, 186, 101),
                (-112, 184.5, 109.5), (-90, 184.5, 109.5)])
L = np.linalg.norm(np.diff(pts, axis=0), axis=1).sum()
chk("deck lead path (hub to the plug's end) under the hub's 200 mm lead", L < 185, "%.0f mm" % L)
# 8 screen height
scr = D.to_world(np.array([[0, -60.1, -8.6], [0, 60.1, -8.6]]))
print("  screen bottom/top above the desk: %.0f / %.0f mm" % (scr[0, 2], scr[1, 2]))
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
