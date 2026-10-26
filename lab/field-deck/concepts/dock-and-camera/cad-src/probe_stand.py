import numpy as np, math
from build123d import import_step
import os
FD_STEP = os.environ.get("FD_STEP", "readback/item_r9_hud.step")   # the printed r9 read-back (Fusion v12); in the public
# repo use cad/MK1-r9_design_public_NOT-FOR-PRINT.step, whose body (the two names filled in) is 115741.7297 mm3
def vmatch(a, v):
    return abs(a - v) < 0.01 or (abs(v - 115715.2078) < 1e-6 and abs(a - 115741.7297) < 0.05)
sols = list(import_step(FD_STEP).solids())
def pick(v):
    m = [s for s in sols if vmatch(s.volume, v)]; assert len(m) == 1, (v, len(m)); return m[0]
body, front, grip = pick(115715.2078), pick(129177.2313), pick(96836.0778)
c, s = math.cos(math.radians(12)), math.sin(math.radians(12))
nstand = np.array([0, -c, s])
for name, sh in (("body", body), ("front", front), ("grip", grip)):
    print(name)
    for f in sh.faces():
        try:
            n = f.normal_at(f.center())
        except Exception:
            continue
        n = np.array([n.X, n.Y, n.Z])
        ang = math.degrees(math.acos(max(-1, min(1, n @ nstand))))
        if ang < 3 and f.area > 50:
            bb = f.bounding_box()
            p = f.center(); d = n @ np.array([p.X, p.Y, p.Z])
            print("  area %8.1f  ang %.2f  n %s  offset %.3f  x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f" % (f.area, ang, n.round(4), d, bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z))
# lowest points along nstand (support) for each solid
for name, sh in (("body", body), ("front", front), ("grip", grip)):
    v, t = sh.tessellate(0.3, 0.3)
    V = np.array([[p.X, p.Y, p.Z] for p in v])
    d = V @ nstand
    print(name, "max along stand normal %.3f" % d.max(), "verts within 0.2: ", (d > d.max() - 0.2).sum())
