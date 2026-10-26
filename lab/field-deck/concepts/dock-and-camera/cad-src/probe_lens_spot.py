"""Height map of the deck's back round the upper grip-side back-plate screw (model frame, rays straight down -z)."""
import numpy as np, trimesh
from build123d import import_step
import os
FD_STEP = os.environ.get("FD_STEP", "readback/item_r9_hud.step")   # the printed r9 read-back (Fusion v12); in the public
# repo use cad/MK1-r9_design_public_NOT-FOR-PRINT.step, whose body (the two names filled in) is 115741.7297 mm3
def vmatch(a, v):
    return abs(a - v) < 0.01 or (abs(v - 115715.2078) < 1e-6 and abs(a - 115741.7297) < 0.05)
sols = list(import_step(FD_STEP).solids())
names = {115715.2078: "body", 129177.2313: "front", 96836.0778: "grip", 23686.9156: "backplate", 3782.2976: "hudcap", 11190.0952: "spkcover"}
meshes = {}
for s in sols:
    nm = next((n for v, n in names.items() if vmatch(s.volume, v)), None)
    if nm is None:
        continue
    v, t = s.tessellate(0.05, 0.1)
    meshes[nm] = trimesh.Trimesh(np.array([[p.X, p.Y, p.Z] for p in v]), np.array(t), process=False)
allm = trimesh.util.concatenate(list(meshes.values()))
part_of = np.concatenate([[k] * len(m.faces) for k, m in enumerate(meshes.values())])
pnames = list(meshes.keys())
def top(x, y):
    loc, ri, tri = allm.ray.intersects_location(np.array([[x, y, 120.0]]), np.array([[0, 0, -1.0]]))
    if len(loc) == 0:
        return None, None
    k = np.argmax(loc[:, 2]); return loc[k, 2], pnames[part_of[tri[k]]]
print("top surface z (part) - rows y, columns x")
xs = [40, 50, 60, 66, 70, 72.4, 75, 76, 76.9, 77.5, 78, 79, 80, 82, 85, 88, 92, 96, 100]
print("   y\\x " + " ".join("%6.1f" % x for x in xs))
for y in [40, 37, 34, 31, 29.5, 28.7, 28, 26, 24, 22, 19.1, 16, 12, 8, 4, 0, -6, -12, -18, -24, -30]:
    row = []
    for x in xs:
        z, nm = top(x, y)
        row.append("   -  " if z is None else "%5.1f%s" % (z, nm[0]))
    print("%6.1f " % y + " ".join(row))
# fine scan across the back plate's grip-side edge at y 0 and y 19.1, and across its top edge at x 60 and 72.4
for y in (0.0, 19.1):
    print("\nacross the grip-side edge at y %.1f:" % y, " ".join("%.1f:%.2f%s" % (x, *(lambda r: (r[0] if r[0] is not None else -1, r[1][0] if r[1] else '-'))(top(x, y))) for x in np.arange(74.0, 84.01, 0.5)))
for x in (60.0, 72.4):
    print("\nacross the top edge at x %.1f:" % x, " ".join("%.1f:%.2f%s" % (y, *(lambda r: (r[0] if r[0] is not None else -1, r[1][0] if r[1] else '-'))(top(x, y))) for y in np.arange(26.0, 40.01, 0.5)))
