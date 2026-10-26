"""MK-I design r1 — the two printability gates, each part in ITS print orientation.
  erosion    : does every layer leave at least one extrusion line? (slice_scan.py's method)
  attachment : is every layer attached to the one below? islands and juts (attach_scan.py)
Both instruments are validated on constructed coupons before their verdicts count.
"""
import numpy as np, trimesh, sys, os
from shapely.ops import unary_union
from attach_scan import scan_attach, validate_instrument

LAYER, HALF_LINE, FULL_LINE = 0.2, 0.21, 0.43
REV = os.environ.get("MK1_REV", "r1")              # r1 stays the default: MK1_REV=r2 python mk1_gates.py Body HUD-Lid

def erosion(mesh, label, step=LAYER):
    empty, thin, cur_e, cur_t = [], [], None, None
    zmax = mesh.bounds[1][2]
    for z in np.arange(step/2, zmax, step):
        sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        area = a_half = a_full = 0
        if sec is not None:
            planar, _ = sec.to_2D()
            if planar.polygons_full:
                u = unary_union(planar.polygons_full)
                area, a_half, a_full = u.area, u.buffer(-HALF_LINE).area, u.buffer(-FULL_LINE).area
        if area > 0.5 and a_half <= 1e-6:
            cur_e = z if cur_e is None else cur_e
        elif cur_e is not None:
            empty.append((round(cur_e - step/2, 2), round(z - step/2, 2))); cur_e = None
        if area > 0.5 and a_full <= 1e-6 and a_half > 1e-6:
            cur_t = z if cur_t is None else cur_t
        elif cur_t is not None:
            thin.append((round(cur_t - step/2, 2), round(z - step/2, 2))); cur_t = None
    print("%-22s erosion: %s%s" % (label, "CLEAN" if not empty else "EMPTY LAYERS %s" % empty, "  thin %s" % thin if thin else ""))
    return empty

def thin_features(mesh, label, step=1.0):
    """parts of a layer that vanish under a one-line erosion and do not come back when grown:
    slivers thinner than one line (the slicer drops them)."""
    worst = []
    zmax = mesh.bounds[1][2]
    for z in np.arange(0.1, zmax, step):
        sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if sec is None: continue
        planar, _ = sec.to_2D()
        if not planar.polygons_full: continue
        u = unary_union(planar.polygons_full)
        lost = u.difference(u.buffer(-HALF_LINE).buffer(HALF_LINE * 1.05))
        if lost.area > 2.0:
            worst.append((round(z, 1), round(lost.area, 1)))
    print("%-22s slivers under one line: %s" % (label, "none" if not worst else worst[:12]))
    return worst

def place(path):
    m = trimesh.load(path, force="mesh", process=False); m.merge_vertices()
    m.apply_translation([0, 0, -m.bounds[0][2]])           # min-z face on the plate (every MK-I part prints as exported)
    return m

if __name__ == "__main__":
    bad = trimesh.boolean.union([trimesh.creation.box(bounds=[[0,0,0],[20,20,4]]),
                                 trimesh.creation.box(bounds=[[9.85,0,3.9],[10.15,20,6.1]]),
                                 trimesh.creation.box(bounds=[[0,0,6],[20,20,10]])], engine="manifold")
    assert any(3.5 < a < 5.0 for a, b in erosion(bad, "coupon (0.3 mm band)")), "erosion instrument missed the coupon"
    validate_instrument()
    print()
    res = {}
    for nm in sys.argv[1:] or ["Front", "Handle", "Body", "Hatch", "HUD-Lid"]:
        m = place("out/mk1/MK1-%s_%s.stl" % (nm, REV))
        print("%s: watertight %s, %d faces, %.1f x %.1f x %.1f on the plate" % (nm, m.is_watertight, len(m.faces), *(m.bounds[1] - m.bounds[0])))
        e = erosion(m, nm)
        thin_features(m, nm)
        f = scan_attach(m, "%-22s attachment" % nm)
        res[nm] = (e, f)
        print()
