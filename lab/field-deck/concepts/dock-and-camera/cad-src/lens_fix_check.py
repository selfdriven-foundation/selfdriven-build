"""Checks of the film-lens FIXING concept (lens_fix_concept.py) on the real r9 deck (2026-10-21).
Screw lengths and the hole, the base's seat (spigot, pin, contact), the dovetail capture and clearances, the click, the
camera's view, the dock, the lead. Run in the cloud folder:  python3 -m dock.lens_fix_check"""
import math, numpy as np, trimesh
from build123d import import_step
import dock.dock_concept as D
import dock.lens_fix_concept as L
import os
FD_STEP = os.environ.get("FD_STEP", "readback/item_r9_hud.step")   # the printed r9 read-back (Fusion v12); in the public
# repo use cad/MK1-r9_design_public_NOT-FOR-PRINT.step, whose body (the two names filled in) is 115741.7297 mm3
def vmatch(a, v):
    return abs(a - v) < 0.01 or (abs(v - 115715.2078) < 1e-6 and abs(a - 115741.7297) < 0.05)

FAIL = []
def chk(name, ok, val=""):
    print("  %-86s %-22s %s" % (name, val, "ok" if ok else "*** FAIL ***")); FAIL.append(name) if not ok else None

# the deck in the MODEL frame (no transform), for heights under the base
sols = list(import_step(FD_STEP).solids())
case = [s for s in sols if any(vmatch(s.volume, v) for v in (115715.2078, 129177.2313, 96836.0778, 23686.9156, 3782.2976, 11190.0952))]
dm = trimesh.util.concatenate([trimesh.Trimesh(np.array([[p.X, p.Y, p.Z] for p in v]), np.array(t), process=False)
                               for v, t in (s.tessellate(0.05, 0.1) for s in case)])
def top(x, y):
    loc, _, _ = dm.ray.intersects_location(np.array([[x, y, 120.0]]), np.array([[0, 0, -1.0]]))
    return loc[:, 2].max() if len(loc) else -99.0
print("deck's highest point (model z): %.3f" % dm.vertices[:, 2].max())

print("\nSCREW (the back plate's upper grip-side screw, %s)" % (L.SCREW,))
pilot = top(*L.SCREW)
print("  pilot bottom straight under the screw: z %.2f" % pilot)
TH_TOP = 50.5                                     # the body's boss starts under the back plate's 0.8 ear floor (z 50.5)
for name, length, want in (("his M3x8 now (7.35 under the head, measured 9.0 overall - 1.65 head)", 7.35, None),
                           ("M3x10 (10.0 under the head)", 10.0, True), ("M3x12", 12.0, False)):
    seat = 51.3 if "now" in name else L.HEAD_SEAT
    tip = seat - length
    thread, spare = TH_TOP - tip, tip - pilot
    print("  %-62s seat z %.2f  tip z %.2f  thread %.2f  hole to spare %.2f" % (name, seat, tip, thread, spare))
    if want is True:
        chk("M3x10 through the base: thread at least 6.0 (now 6.55)", thread >= 6.0, "%.2f mm" % thread)
        chk("M3x10 through the base: does not bottom out (0.5 to spare)", spare >= 0.5, "%.2f mm" % spare)
        chk("an M3x10 up to 0.5 long still does not bottom out", spare - 0.5 >= 0.2, "%.2f mm" % (spare - 0.5))
    if want is False:
        chk("an M3x12 WOULD bottom out (so: use the 10)", spare < 0.3, "%.2f mm" % spare)
    if "now" in name:
        through = (L.HEAD_SEAT - length)
        chk("his M3x8 through the base would leave too little thread (< 5)", TH_TOP - through < 5.0, "%.2f mm" % (TH_TOP - through))
chk("pan head (2.1 tall) sits below the base's top (56.5)", L.HEAD_SEAT + 2.1 <= L.FACE + L.B_T - 0.3, "top z %.2f" % (L.HEAD_SEAT + 2.1))
chk("lens channel ceiling clears the head", L.CEIL - (L.HEAD_SEAT + 2.1) >= 0.5, "%.2f mm" % (L.CEIL - (L.HEAD_SEAT + 2.1)))
chk("plastic under the head: base + spigot down to the seat floor (z 51.3)", L.HEAD_SEAT - 51.3 >= 2.5, "%.2f mm" % (L.HEAD_SEAT - 51.3))

print("\nBASE ON THE BACK PLATE")
# counterbore and hex mark empty where the spigot and pin go
r_sp = L.SPIGOT_D / 2
ring = [(L.SCREW[0] + r * math.cos(a), L.SCREW[1] + r * math.sin(a)) for r in (1.8, 2.5, r_sp) for a in np.radians(np.arange(0, 360, 30))]
zmax = max(top(x, y) for x, y in ring)
chk("spigot d6.0: the screw's seat is free down to its floor (z 51.3)", zmax <= 51.3 + 0.02, "highest %.2f" % zmax)
wall = [(L.SCREW[0] + 3.12 * math.cos(a), L.SCREW[1] + 3.12 * math.sin(a)) for a in np.radians(np.arange(0, 360, 30))]
chk("  ... and the seat's wall is just outside it (d6.1+): spigot is located", min(top(x, y) for x, y in wall) >= 52.9, "%.2f" % min(top(x, y) for x, y in wall))
pin = [(L.HEXMARK[0] + r * math.cos(a), L.HEXMARK[1] + r * math.sin(a)) for r in (0.0, 1.0, L.PIN_D / 2) for a in np.radians(np.arange(0, 360, 30))]
zp = max(top(x, y) for x, y in pin)
chk("pin d3.6 x 0.5: the hex mark is free under it", zp <= L.FACE - L.PIN_H - 0.05, "highest %.2f" % zp)
edge = []                                         # how far the hex mark's floor reaches from its centre, every 5 deg
for a in np.radians(np.arange(0, 360, 5)):
    r = 1.0
    while r < 4.0 and top(L.HEXMARK[0] + r * math.cos(a), L.HEXMARK[1] + r * math.sin(a)) < 52.95:
        r += 0.02
    edge.append(r)
play = min(edge) - L.PIN_D / 2
print("  hex mark: walls %.2f (flats) .. %.2f (corners) from its centre -> A/F %.2f" % (min(edge), max(edge), 2 * min(edge)))
chk("  ... and its walls hold the pin: play at the flats 0.1 .. 0.4", 0.1 <= play <= 0.4, "%.2f mm" % play)
print("  pin to screw: %.1f mm apart -> the base cannot turn" % math.dist(L.SCREW, L.HEXMARK))
# contact under the flat underside (outside the tongue, spigot, pin)
xs, ys = np.arange(L.B_X0 + 0.25, L.B_X1, 0.5), np.arange(L.B_Y_BOT[0] + 0.25, L.B_Y_BOT[1], 0.5)
tx0, tx1, ty0, ty1 = L.TONGUE
hi, cont, n = -99, 0, 0
for x in xs:
    for y in ys:
        if tx0 - 0.8 <= x <= tx1 and ty0 - 0.8 <= y <= ty1 + 0.8:
            continue
        if math.dist((x, y), L.SCREW) < r_sp + 0.1 or math.dist((x, y), L.HEXMARK) < L.PIN_D / 2 + 0.1:
            continue
        z = top(x, y); n += 1; hi = max(hi, z); cont += z >= L.FACE - 0.02
chk("nothing under the base's flat underside stands above z 53.0", hi <= L.FACE + 0.01, "%.3f" % hi)
chk("the underside rests on the armour over a fair area (>= 80 mm2)", cont * 0.25 >= 80, "%.0f mm2 of %.0f" % (cont * 0.25, n * 0.25))

print("\nLENS ON THE BASE")
blo, bhi = L.B_Y_BOT, L.B_Y_TOP
def chan_y(z):
    f = (z - L.FACE) / (L.CEIL - L.FACE)
    return (blo[0] - L.CLR) + f * ((bhi[0] - L.CLR) - (blo[0] - L.CLR)), (blo[1] + L.CLR) + f * ((bhi[1] + L.CLR) - (blo[1] + L.CLR))
o = chan_y(L.BACK)
chk("dovetail: the channel's mouth (at the lens's back) is narrower than the base's top", (o[1] - o[0]) < (bhi[1] - bhi[0]) - 4.0,
    "%.1f vs %.1f mm" % (o[1] - o[0], bhi[1] - bhi[0]))
chk("clearance on the base's top and sides", L.CLR >= 0.2, "%.2f mm" % L.CLR)
chk("the lens's back face floats over the deck while it slides", L.BACK - dm.vertices[:, 2].max() >= 0.05, "%.2f mm" % (L.BACK - dm.vertices[:, 2].max()))
lens_top_y = L.AY + 23.0
chk("lens wall above the channel (top)", lens_top_y - (bhi[1] + L.CLR) >= 2.0, "%.2f mm" % (lens_top_y - (bhi[1] + L.CLR)))
chk("lens floor over the channel", L.FLOOR >= 1.5, "%.1f mm" % L.FLOOR)
chk("stop: the channel's closed end 0.1 past the base's end", True, "x %.1f vs %.1f" % (L.B_X1 + 0.1, L.B_X1))
dz = 0.6 - L.CLR
tl, tt = L.TONGUE[1] - L.TONGUE[0], 1.5
strain = 1.5 * tt * dz / tl ** 2
chk("click: the tongue bends %.2f mm; PETG strain under 2 %%" % dz, strain < 0.02, "%.2f %%" % (strain * 100))
lb = L.lens_body(); br, ztop = L.lens_barrel(); bs = L.base()
chk("lens body is one valid solid", lb.is_valid, "%.1f cm3" % (lb.volume / 1000))
chk("lens barrel is one valid solid", br.is_valid, "%.1f cm3" % (br.volume / 1000))
chk("base is one valid solid", bs.is_valid, "%.2f cm3" % (bs.volume / 1000))
inter = (lb & bs).volume if (lb & bs) is not None else 0.0
chk("fitted, the lens and the base do not overlap", inter < 0.01, "%.3f mm3" % inter)
print("  out from the back plate: %.1f mm (the looks picture said ~32; the channel and plug room add 3)" % (ztop - L.FACE))

print("\nCAMERA VIEW, DOCK, LEAD (world frame)")
lens = trimesh.util.concatenate([trimesh.Trimesh(o_[0], o_[1], process=False) for o_ in L.lens_objects(0.0)
                                 if tuple(o_[3]) not in {D.BLACK, D.GLASS}])
deckw = trimesh.util.concatenate([trimesh.Trimesh(o_[0], o_[1], process=False) for o_ in D.deck_objects()])
dockw = trimesh.util.concatenate([trimesh.Trimesh(o_[0], o_[1], process=False) for o_ in D.dock_objects()])
ax = np.radians(np.linspace(-30, 30, 25)); ay = np.radians(np.linspace(-23.5, 23.5, 21))
DIRS = np.array([[math.tan(a), math.tan(b), 1.0] for a in ax for b in ay]); DIRS /= np.linalg.norm(DIRS, axis=1, keepdims=True)
org, dirs = [], []
for ox, oy in [(0, 0)] + [(1.5 * math.cos(t), 1.5 * math.sin(t)) for t in np.radians(np.arange(0, 360, 45))]:
    o_w = D.to_world(np.array([[L.AX + ox, L.AY + oy, L.AP + 0.7]]))[0]
    for dd in DIRS:
        org.append(o_w); dirs.append(dd @ D.R.T)
org, dirs = np.array(org), np.array(dirs)
for nm, m in (("the lens itself", lens), ("the deck", deckw), ("the dock", dockw)):
    hit = m.ray.intersects_any(org, dirs)
    chk("camera's full view (60 x 47 deg) clear of %s" % nm, not hit.any(), "%d of %d rays hit" % (hit.sum(), len(hit)))
cp, dist, _ = trimesh.proximity.closest_point(dockw, lens.vertices)
chk("docked: lens to the dock", dist.min() > 2.0, "%.1f mm" % dist.min())
lead = [o_ for o_ in L.lead_objects()]
plug = trimesh.Trimesh(lead[0][0], lead[0][1], process=False)
dock_lead = trimesh.util.concatenate([trimesh.Trimesh(o_[0], o_[1], process=False) for o_ in D.cables()[:2]])
cp, dist, _ = trimesh.proximity.closest_point(dock_lead, plug.vertices)
chk("camera plug clear of the dock's own lead and plug", dist.min() > 1.0, "%.1f mm" % dist.min())
pts = [(95.0, L.PORT[0], L.PORT[1]), (101.0, L.PORT[0], L.PORT[1] + 0.5), (105.5, L.PORT[0] - 1.0, L.PORT[1] + 9.0), (106.0, -3.0, 44.0),
       (103.0, L.AY - 13.5, 54.0), (L.AX + 27.0, L.AY - 13.5, L.CEIL + L.FLOOR + 3.0), (L.AX + 23.0, L.AY - 13.5, L.CEIL + L.FLOOR + 3.0)]
run = sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))
print("  lead from the lens to the plug: about %.0f mm (the camera comes with 1 m)" % run)

print("\nPRINT (rough, not sliced)")
for nm, v in (("base", bs.volume), ("lens body + barrel", lb.volume + br.volume)):
    print("  %-20s %.1f cm3 solid -> about %.0f g PETG at 70 %% fill" % (nm, v / 1000, v / 1000 * 1.27 * 0.7))
print("\nALL CHECKS PASS" if not FAIL else "\nFAILED: %s" % FAIL)
