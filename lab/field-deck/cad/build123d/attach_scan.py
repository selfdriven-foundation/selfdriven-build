"""Attachment gate (companion to slice_scan.py's erosion gate).

Two orthogonal printability questions, each taught by a slicer warning:
  - erosion gate: is every layer's section printable (>= 1 extrusion line)?
  - THIS gate: is every layer's material attached to the layer below?
    ISLAND = region with no contact (floats); JUT = overhang beyond `allow`
    per layer (cantilever candidate; whitelist known bridges/zones).
Instrument rules: polygons are mapped back to WORLD coordinates through each
section's own to_3D transform (per-section to_2D frames are NOT comparable —
that trap has bitten this project twice), and the checker must be validated on
constructed coupons (clean box + known-bad tab) before any verdict counts.
"""
import numpy as np, trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

def world_layer(mesh, z):
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None: return None
    planar, T = sec.to_2D()
    polys = []
    for p in planar.polygons_full:
        def tw(coords):
            pts = np.array([[c[0], c[1], 0, 1] for c in coords]) @ np.asarray(T).T
            return [(q[0], q[1]) for q in pts]
        polys.append(Polygon(tw(p.exterior.coords), [tw(i.coords) for i in p.interiors]))
    return unary_union(polys) if polys else None

def _polys(u):
    return list(u.geoms) if u.geom_type in ("MultiPolygon", "GeometryCollection") else [u]


def scan_attach(mesh, label, step=0.2, allow=0.25, min_area=1.0, whitelist=None, zone_ok=None):
    """2026-10-07, after the speaker cover's floating cheek slipped through: a piece of a layer counts as attached only
    if it touches material below that is ITSELF attached. Before, a piece was 'attached' as soon as it touched anything
    below - so a 45 deg gusset that starts in mid-air as a hair-thin line (first slice 0.24 mm2, under the 0.3 mm2
    speck limit) was never reported: every later slice rested on the floating slice before it. Now a floating piece
    and everything that grows from it stays 'floating', and it is reported the first time it is larger than a speck."""
    zmax = mesh.bounds[1][2]; prev = None; findings = []
    float_prev = []           # the floating pieces of the layer below
    told_prev = []            # those of them that were already reported (or grew from a reported one)
    for z in np.arange(step/2, zmax, step):
        u = world_layer(mesh, z)
        if u is None or u.is_empty: prev = None; float_prev = []; told_prev = []; continue
        floating, told = [], []
        if prev is not None:
            ground_prev = prev
            if float_prev:
                ground_prev = unary_union([q for q in _polys(prev) if not any(q.equals(f) for f in float_prev)]) if len(_polys(prev)) > len(float_prev) else None
            for g in _polys(u):
                if g.is_empty or g.area <= 0:
                    continue
                if ground_prev is None or not g.intersects(ground_prev):
                    floating.append(g)
                    if any(g.intersects(t) for t in told_prev):
                        told.append(g)
                    elif g.area > 0.3:
                        c = tuple(round(v, 1) for v in g.representative_point().coords[0])
                        if not (zone_ok and zone_ok(c, z)):
                            findings.append(("ISLAND", round(z, 2), round(g.area, 1), c))
                        told.append(g)
                    continue
                juts = g.difference(prev.buffer(allow))
                if juts.area > min_area:
                    for j in (juts.geoms if juts.geom_type == "MultiPolygon" else [juts]):
                        if j.area <= min_area: continue
                        c = tuple(round(v, 1) for v in j.representative_point().coords[0])
                        if whitelist and any(abs(c[0]-wx) < 4 and abs(c[1]-wy) < 4 for wx, wy in whitelist): continue
                        if zone_ok and zone_ok(c, z): continue
                        findings.append(("JUT", round(z, 2), round(j.area, 1), c))
        prev = u; float_prev = floating; told_prev = told
    print(f"{label}: " + ("ATTACHED-CLEAN" if not findings else f"{len(findings)} findings: {findings[:10]}"))
    return findings


def _gusset(y0, y1):
    """a 45 deg gusset: nothing at z 3, 6 mm long at z 9 - with a 2 mm plate on top of it"""
    import trimesh.creation as tc
    from shapely.geometry import Polygon as P
    tri = tc.extrude_polygon(P([(0, 3), (0, 9), (6, 9)]), y1 - y0)          # drawn in (x, z), extruded along +z -> turn it up
    T = np.array([[1, 0, 0, 0], [0, 0, 1, y0], [0, 1, 0, 0], [0, 0, 0, 1.0]])   # (x, z, t) -> (x, y0 + t, z)
    tri.apply_transform(T)
    tri.fix_normals()
    return tri


def validate_instrument():
    good = trimesh.creation.box(bounds=[[0, 0, 0], [20, 20, 10]])
    bad = trimesh.boolean.union([trimesh.creation.box(bounds=[[0, 0, 0], [20, 20, 10]]),
                                 trimesh.creation.box(bounds=[[19.9, 8, 5], [22.5, 12, 6]])], engine="manifold")
    assert not scan_attach(good, "coupon clean box"), "instrument: false positive"
    f = scan_attach(bad, "coupon 2.5mm tab (must flag)")
    assert any(k == "JUT" and 4.4 < z < 5.7 for k, z, a, c in f), "instrument: missed the tab"
    # 2026-10-07: a 45 deg gusset on a wall. Attached to the wall it is clean; standing 0.5 mm beside the wall's end
    # it starts in mid-air as a hair line - that one must be reported (it is the speaker cover's lower cheek).
    wall = trimesh.creation.box(bounds=[[-2, 0, 0], [0, 10, 12]])
    on = trimesh.boolean.union([wall, _gusset(4.0, 5.2)], engine="manifold")
    assert not scan_attach(on, "coupon gusset on a wall (must be clean)"), "instrument: false positive on an attached 45 deg gusset"
    off = trimesh.boolean.union([wall, _gusset(10.5, 11.7), trimesh.creation.box(bounds=[[-1, 9, 9], [6, 11.7, 11]])], engine="manifold")
    f = scan_attach(off, "coupon gusset 0.5 mm beside the wall's end (must flag)")
    assert any(k == "ISLAND" and 3.0 < z < 4.0 for k, z, a, c in f), "instrument: missed the floating gusset"
    print("attachment instrument validated")
