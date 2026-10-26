"""Where things are on the deck's back (r9 read-back), model frame: bounding boxes, the back plate's screw holes."""
import numpy as np
from build123d import import_step, GeomType
import os
FD_STEP = os.environ.get("FD_STEP", "readback/item_r9_hud.step")   # the printed r9 read-back (Fusion v12); in the public
# repo use cad/MK1-r9_design_public_NOT-FOR-PRINT.step, whose body (the two names filled in) is 115741.7297 mm3
def vmatch(a, v):
    return abs(a - v) < 0.01 or (abs(v - 115715.2078) < 1e-6 and abs(a - 115741.7297) < 0.05)
sols = list(import_step(FD_STEP).solids())
names = {115715.2078: "body", 129177.2313: "front", 96836.0778: "grip", 23686.9156: "backplate", 3782.2976: "hudcap", 11190.0952: "spkcover"}
for s in sols:
    nm = next((n for v, n in names.items() if vmatch(s.volume, v)), None)
    bb = s.bounding_box()
    print("%-10s vol %10.1f  x %7.1f..%7.1f  y %7.1f..%7.1f  z %7.1f..%7.1f" % (nm or "-", s.volume, bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z))
bp = [s for s in sols if abs(s.volume - 23686.9156) < 0.01][0]
print("\nback plate cylindrical faces (holes), axis along z:")
seen = set()
for f in bp.faces():
    if f.geom_type == GeomType.CYLINDER:
        try:
            r = f.radius
        except Exception:
            continue
        c = f.center()
        ax = f.normal_at(c)
        key = (round(c.X, 1), round(c.Y, 1), round(r, 2))
        if r < 4 and key not in seen:
            seen.add(key)
            bb = f.bounding_box()
            print("  r %.2f  centre x %.1f y %.1f  z %.1f..%.1f" % (r, (bb.min.X + bb.max.X) / 2, (bb.min.Y + bb.max.Y) / 2, bb.min.Z, bb.max.Z))
