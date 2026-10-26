"""What a slicer would hold up from the BED: faces of a part (as it lies on the bed) that face down flatter than THRESH degrees
from level and have nothing of the part itself straight under them. Normal support "on build plate only" at that threshold
puts a tower under exactly these. Listed by height; the skirt's roof (4.5 mm up) is meant to be held up - anything higher is
a tower.   python3 support_survey.py FILE.stl [THRESH=30]"""
import sys, math
import numpy as np, trimesh
import mk1_gates as G

def survey(path, thresh=30.0, verbose=True):
    m = G.place(path)
    n = m.face_normals; a = m.area_faces; c = m.triangles_center
    down = n[:, 2] < -math.cos(math.radians(thresh))             # flatter than THRESH from level, facing down
    idx = np.where(down & (c[:, 2] > 0.05) & (a > 1e-9))[0]
    org = c[idx] - np.array([0, 0, 1e-4])
    hit = m.ray.intersects_any(org, np.tile([0.0, 0.0, -1.0], (len(idx), 1)))
    free = idx[~hit]                                             # only the bed under them
    rows = {}
    for k in free:
        z = round(float(c[k, 2]) * 5) / 5.0
        r = rows.setdefault(z, [0.0, [], []]); r[0] += a[k]; r[1].append(c[k, 0]); r[2].append(c[k, 1])
    out = []
    for z in sorted(rows):
        ar, xs, ys = rows[z]
        if ar > 0.05:
            out.append((z, ar, min(xs), max(xs), min(ys), max(ys)))
    if verbose:
        print("%s: faces flatter than %.0f deg, facing down, only the bed under them" % (path, thresh))
        for z, ar, x0, x1, y0, y1 in out:
            print("   z %5.1f   %8.1f mm2   x %7.1f .. %7.1f   y %7.1f .. %7.1f" % (z, ar, x0, x1, y0, y1))
        print("   total %.1f mm2; above z 5: %.1f mm2" % (sum(o[1] for o in out), sum(o[1] for o in out if o[0] > 5.0)))
    return out

if __name__ == "__main__":
    survey(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 30.0)
