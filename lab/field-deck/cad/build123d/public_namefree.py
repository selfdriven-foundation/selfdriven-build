"""PUBLIC COPY OF THE r9 CAD WITHOUT THE TWO PERSONAL NAMES (2026-10-26).
The body (read-back solid 115715.2078 mm3) has two first names cut 0.4 mm into its flat back (z 7.0 -> 6.6) at the bottom
corners: one at x -100.4 .. -87.0, the other at x 70.8 .. 100.4, both y -86.4 .. -83.2 (a 0.2 mm survey; nothing else but
the flat face within 0.6 mm round them). Each is filled with a box from z 6.5 up to the face (z 7.0), 0.4 mm past the
letters - so the public body is the printed body with a plain face there. Nothing else changes.
Writes (OUT, default out/public):
  MK1-r9_design_public_NOT-FOR-PRINT.step   the whole design, the body swapped, Fusion's part names kept
  MK1-r9-Body_PRINT-THIS.stl                the body as the 12 Oct print files laid it (skirt down, centred, z 0)
  public_namefree_checks.txt                (printed to stdout; tee it)
  python3 public_namefree.py [OUT]"""
import sys, os, hashlib
import numpy as np, trimesh
from build123d import import_step, export_step, Box, Pos, Align, Compound
from mk1_body_r3 import export_clean_stl

READBACK = "readback/item_r9_hud.step"
ORIG_STL = "/mnt/user-data/uploads/Field Deck/8 - Repo/field-deck/print/MK1-r9/MK1-r9-Body_PRINT-THIS.stl"
OUT = sys.argv[1] if len(sys.argv) > 1 else "out/public"
BODY_V = 115715.2078
FACE, FLOOR = 7.0, 6.6
FILLS = [(-100.8, -86.6, -86.8, -82.8), (70.4, 100.8, -86.8, -82.8)]     # x0, x1, y0, y1 (letters + 0.4)
FAILS = []


def expect(name, ok, val=""):
    print("  %-92s %-26s %s" % (name, val, "ok" if ok else "*** FAIL ***"), flush=True)
    if not ok:
        FAILS.append(name)


def mesh_of(shape, tol=0.02, ang=0.05):
    v, t = shape.tessellate(tol, ang)
    return trimesh.Trimesh(np.array([[p.X, p.Y, p.Z] for p in v]), np.array(t), process=False)


def heights(m, x0, x1, y0, y1, step=0.2):
    xs, ys = np.arange(x0, x1 + 1e-9, step), np.arange(y0, y1 + 1e-9, step)
    O = np.array([[x, y, 200.0] for x in xs for y in ys])
    loc, ri, _ = m.ray.intersects_location(O, np.tile([0, 0, -1.0], (len(O), 1)), multiple_hits=False)
    Z = np.full(len(O), np.nan); Z[ri] = loc[:, 2]
    return Z


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("PUBLIC r9 CAD WITHOUT THE NAMES, from %s (md5 %s)" % (READBACK, hashlib.md5(open(READBACK, "rb").read()).hexdigest()))
    top = import_step(READBACK)
    sols = list(top.solids())
    body = [s for s in sols if abs(s.volume - BODY_V) < 0.01]
    expect("one body solid of %.4f mm3 in the read-back" % BODY_V, len(body) == 1, "%d found" % len(body))
    body = body[0]
    m0 = mesh_of(body)
    for i, (x0, x1, y0, y1) in enumerate(FILLS):
        Z = heights(m0, x0, x1, y0, y1)
        u = np.unique(np.round(Z[~np.isnan(Z)], 3))
        expect("name %d: before, only the face and the letter floor under the fill (z %.1f / %.1f)" % (i + 1, FACE, FLOOR),
               set(u.tolist()) <= {FACE, FLOOR}, str(u.tolist()))
    filled = body
    for x0, x1, y0, y1 in FILLS:
        filled = filled + Pos((x0 + x1) / 2, (y0 + y1) / 2, 6.5) * Box(x1 - x0, y1 - y0, FACE - 6.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    filled = filled.solids()[0] if len(filled.solids()) == 1 else filled
    expect("filled body: one valid solid", filled.is_valid and len(filled.solids()) == 1, "%d solid(s)" % len(filled.solids()))
    dv = filled.volume - body.volume
    expect("volume added = the letters only (between 10 and 120 mm3)", 10 < dv < 120, "+%.2f mm3" % dv)
    bb0, bb1 = body.bounding_box(), filled.bounding_box()
    same_bb = all(abs(a - b) < 1e-6 for a, b in zip((bb0.min.X, bb0.min.Y, bb0.min.Z, bb0.max.X, bb0.max.Y, bb0.max.Z),
                                                     (bb1.min.X, bb1.min.Y, bb1.min.Z, bb1.max.X, bb1.max.Y, bb1.max.Z)))
    expect("same outside size as the printed body", same_bb)
    m1 = mesh_of(filled)
    for i, (x0, x1, y0, y1) in enumerate(FILLS):
        Z = heights(m1, x0, x1, y0 - 0.2, y1 + 0.2)          # inside the surveyed flat frame (letters + 0.6)
        u = np.unique(np.round(Z[~np.isnan(Z)], 3))
        expect("name %d: after, the face is plain (one height, z %.1f)" % (i + 1, FACE), u.tolist() == [FACE], str(u.tolist()))
    # everything else unchanged: same points on the rest of the body's outside (sampled)
    rng = np.random.default_rng(0)
    pts = m0.sample(4000, seed=0) if hasattr(m0, "sample") else m0.vertices[rng.choice(len(m0.vertices), 4000)]
    far = [p for p in pts if not any(x0 - 1 <= p[0] <= x1 + 1 and y0 - 1 <= p[1] <= y1 + 1 for x0, x1, y0, y1 in FILLS)]
    _, d, _ = trimesh.proximity.closest_point(m1, np.array(far))
    expect("the rest of the body unchanged (4000 surface points, away from the fills)", d.max() < 0.03, "max %.4f mm" % d.max())
    # ---- the whole design, the body swapped, labels kept
    kids = list(top.children)
    swapped, newkids = 0, []
    for k in kids:
        if hasattr(k, "volume") and len(k.solids()) == 1 and abs(k.solids()[0].volume - BODY_V) < 0.01:
            f = filled.solids()[0]
            f.label = k.label
            newkids.append(f); swapped += 1
        else:
            newkids.append(k)
    expect("the body swapped once in the design (its part name kept)", swapped == 1, "%d" % swapped)
    design = Compound(label=top.label, children=newkids)
    step = os.path.join(OUT, "MK1-r9_design_public_NOT-FOR-PRINT.step")
    export_step(design, step)
    back = import_step(step)
    vs0 = sorted(s.volume for s in sols)
    vs1 = sorted(s.volume for s in back.solids())
    want = sorted([v for v in vs0 if abs(v - BODY_V) > 0.01] + [filled.volume])
    worst = max(abs(a - b) / (1e-5 * a + 0.02) for a, b in zip(want, vs1)) if len(want) == len(vs1) else 1e9
    expect("public STEP read back: same %d solids, only the body changed (each within 1e-5 + 0.02 mm3)" % len(vs0),
           len(vs1) == len(vs0) and worst < 1.0, "%d solids, worst %.2f of the allowance" % (len(vs1), worst))
    txt = open(step, "rb").read().decode("latin-1").lower()
    words = [w.strip().lower() for w in os.environ.get("FD_PRIVATE_WORDS", "").split(",") if w.strip()]
    expect("none of the private words (FD_PRIVATE_WORDS, %d given) anywhere in the STEP text" % len(words),
           len(words) > 0 and not any(w in txt for w in words), "set FD_PRIVATE_WORDS to check" if not words else "")
    labels = [getattr(k, "label", "") for k in back.children]
    expect("part names kept in the STEP", sum(1 for l in labels if l) >= len(kids) - 1, "%d named parts" % sum(1 for l in labels if l))
    # ---- the body print file, laid as on 12 Oct (identity orientation, centred, lowest face z 0)
    s = filled.solids()[0]
    bb = s.bounding_box()
    s = Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * s
    stl = os.path.join(OUT, "MK1-r9-Body_PRINT-THIS.stl")
    export_clean_stl(s, stl)
    mm = trimesh.load(stl, force="mesh", process=False); mm.merge_vertices()
    expect("body STL: one closed mesh", mm.is_watertight and mm.is_winding_consistent and len(mm.split(only_watertight=False)) == 1)
    expect("body STL: volume against the solid's", abs(mm.volume - s.volume) / s.volume < 2e-3, "%.1f mm3" % mm.volume)
    if os.path.exists(ORIG_STL):
        mo = trimesh.load(ORIG_STL, force="mesh", process=False)
        expect("body STL lies exactly like the printed one (same bounds)", np.allclose(mo.bounds, mm.bounds, atol=0.01),
               "%s" % np.round(mm.bounds - mo.bounds, 3).tolist())
        _, d, _ = trimesh.proximity.closest_point(mm, mo.sample(4000, seed=1))
        expect("body STL against the printed one: same shape except the names (95th pct gap)", np.percentile(d, 95) < 0.02,
               "p95 %.4f, max %.3f mm" % (np.percentile(d, 95), d.max()))
    print("\n  files:")
    for p in (step, stl):
        print("    %-60s %9d bytes  md5 %s" % (os.path.basename(p), os.path.getsize(p), hashlib.md5(open(p, "rb").read()).hexdigest()))
    print("\n%s" % ("ALL CHECKS PASS" if not FAILS else "FAILED: %s" % FAILS))
    sys.exit(1 if FAILS else 0)
