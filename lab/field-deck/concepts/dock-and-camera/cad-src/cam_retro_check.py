"""Checks of the camera-pod looks (cam_retro_concept.py) on the real r9 deck, standing alone and in the dock concept:
the camera's whole view passes each pod's own opening, nothing of the deck or the dock is in view, the pods clear the
deck and the dock, and the print facts (size, overhangs)."""
import math, numpy as np, trimesh
import dock.dock_concept as D
import dock.cam_retro_concept as C

FAIL = []
def chk(name, ok, val=""):
    print("  %-84s %-20s %s" % (name, val, "ok" if ok else "*** FAIL ***")); FAIL.append(name) if not ok else None

def tm(objs):
    return trimesh.util.concatenate([trimesh.Trimesh(o[0], o[1], process=False) for o in objs])

to_model = lambda Pw: (np.atleast_2d(Pw) - D.T) @ D.R          # R is orthonormal: model = R^T (world - T)

deck = tm(D.deck_objects())
dock_parts = {"dock base, lips, posts, mast socket": tm(D.dock_objects()), "cables (deck lead, camera lead, charger)": tm(D.cables())}
camera_cols = {D.BLACK, D.GLASS, (0.02, 0.02, 0.03)}
dV = to_model(deck.vertices)
print("deck, model frame: highest z %.2f (back plate face 53.0)" % dV[:, 2].max())

# the camera's view: a rectangular cone 60 x 47 deg from a 1.5 mm aperture, along model +z
ax = np.radians(np.linspace(-30, 30, 25)); ay = np.radians(np.linspace(-23.5, 23.5, 21))
DIRS = np.array([[math.tan(a), math.tan(b), 1.0] for a in ax for b in ay]); DIRS /= np.linalg.norm(DIRS, axis=1, keepdims=True)
ORIG = [(0.0, 0.0)] + [(C.AP_R * math.cos(t), C.AP_R * math.sin(t)) for t in np.radians(np.arange(0, 360, 45))]
APERTURE = {"Now": 82.4, "A  Film lens": C.A_AP, "B  Bellows": C.B_AP, "C  Lens turret": C.C_AP}

for title, sub, fn in C.DESIGNS:
    print("\n%s (%s)" % (title, sub))
    objs, ztop, _ = fn()
    shell = [o for o in objs if tuple(o[3]) not in camera_cols]
    pod = tm(shell)
    pV = to_model(pod.vertices)
    print("  size: x %.1f..%.1f  y %.1f..%.1f  z %.1f..%.1f  -> %.1f mm out from the back plate" % (
        pV[:, 0].min(), pV[:, 0].max(), pV[:, 1].min(), pV[:, 1].max(), pV[:, 2].min(), pV[:, 2].max(), pV[:, 2].max() - 53.0))
    chk("pod sits on top of the back plate (lowest point above z 53.0)", pV[:, 2].min() >= 53.0, "%.2f" % pV[:, 2].min())
    inside = (dV[:, 0] >= pV[:, 0].min()) & (dV[:, 0] <= pV[:, 0].max()) & (dV[:, 1] >= pV[:, 1].min()) & (dV[:, 1] <= pV[:, 1].max())
    chk("no deck part under it rises above z 53.0", dV[inside, 2].max() <= 53.0 + 1e-6, "%.2f" % dV[inside, 2].max())
    chk("stays inside the deck's width (model x <= 104)", pV[:, 0].max() <= 104.0, "%.1f" % pV[:, 0].max())
    chk("bed fit (A1 256 mm)", max(np.ptp(pV, axis=0)) <= 250, "%.0f mm" % max(np.ptp(pV, axis=0)))
    # rays from the aperture, in the world frame
    z_ap = APERTURE[title] + 0.9
    origins, dirs = [], []
    for ox, oy in ORIG:
        o = D.to_world(np.array([[C.CX + ox, C.CY + oy, z_ap]]))[0]
        for d in DIRS:
            origins.append(o); dirs.append(d @ D.R.T)
    origins, dirs = np.array(origins), np.array(dirs)
    for nm, m in [("the pod itself", pod), ("the deck", deck)] + list(dock_parts.items()):
        hit = m.ray.intersects_any(origins, dirs)
        chk("camera's full view (60 x 47 deg) clear of %s" % nm, not hit.any(), "%d of %d rays hit" % (hit.sum(), len(hit)))
    for nm, m in dock_parts.items():
        cp, dist, _ = trimesh.proximity.closest_point(m, pod.vertices)
        chk("docked: gap to the %s" % nm, dist.min() > 2.0, "%.1f mm" % dist.min())

print("\nPRINT NOTES (lens up, back on the bed)")
print("  A: the front barrel (r 17.6) steps out 1.1 mm over the scale ring (r 16.5), the lip 0.6 more: short ledges, no support")
print("  B: pleats 1.4 mm in per side over 1.4 mm = 45 deg; the front panel overhangs the last pleat by 1.5 mm")
print("  C: the turret is its own flat print (barrels up) on an M3 pivot; the body prints like A's")
print("\nALL CHECKS PASS" if not FAIL else "\nFAILED: %s" % FAIL)
