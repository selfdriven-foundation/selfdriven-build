"""MK-I r9 - THE GRIP'S SCREWS, MEASURED ON THE PRINTED DESIGN (2026-10-13; owner: "the screws look too small for that").
From Fusion's r9 read-back (readback/item_r9_hud.step = version 12, the design he printed): the handle, the front and the four
"M3x8 (handle)" screws. For each screw, probes along its axis (point-in-solid, 0.01 mm steps):
  the head's underside and the tip; the grip's plate under the head; the front's face, its pilot (diameter, bottom);
  so: how much of the 8 mm is in the plate, how much bites the front, how much hole is left below the tip,
  and the plastic round the pilot (to the front's outer side wall and to its inner side).
Then a picture: the cut through the middle of one screw (screen side up).
  python3 mk1_handle_screw_cut_r9.py [OUT_PNG]"""
import sys, os, hashlib, tempfile
import numpy as np
from build123d import import_step, Vector, Box, Pos, export_stl

READBACK = "readback/item_r9_hud.step"
OUT = sys.argv[1] if len(sys.argv) > 1 else "out/mk1/shots/MK1_r9_grip_screw_cut.png"
V_HANDLE, V_FRONT, V_SCREW = 96836.0778, 129177.2313, 91.4074
REAL_UNDER, HEAD_D, HEAD_H = 8.0, 5.7, 1.65       # ISO 7380 M3x8 button head: length under the head, head diameter, height
FAILS = []


def expect(name, value, lo, hi, unit="mm "):
    ok = lo <= value <= hi
    print("  %-96s %9.3f %s %s" % (name, value, unit, "ok" if ok else "*** FAIL ***"), flush=True)
    if not ok:
        FAILS.append(name)


def runs(solid, p0, d, length, step=0.05):
    """the stretches of a line p0 + t d (t 0..length) that lie inside `solid`: list of (t0, t1); sampled every `step`,
    each change of inside / outside then found by bisection to 0.0001"""
    at = lambda t: solid.is_inside(Vector(p0[0] + t * d[0], p0[1] + t * d[1], p0[2] + t * d[2]))

    def edge(a, b, ina):
        for _ in range(10):
            m = (a + b) / 2
            if at(m) == ina:
                a = m
            else:
                b = m
        return (a + b) / 2
    ts = list(np.arange(0.0, length, step)) + [length]
    vals = [at(t) for t in ts]
    out, t_in = [], (0.0 if vals[0] else None)
    for k in range(1, len(ts)):
        if vals[k] != vals[k - 1]:
            e = edge(ts[k - 1], ts[k], vals[k - 1])
            if vals[k]:
                t_in = e
            else:
                out.append((round(t_in, 4), round(e, 4))); t_in = None
    if t_in is not None:
        out.append((round(t_in, 4), round(length, 4)))
    return out


sols = list(import_step(READBACK).solids())
print("THE GRIP'S SCREWS from %s (md5 %s, %d solids)" % (READBACK, hashlib.md5(open(READBACK, "rb").read()).hexdigest(), len(sols)))
handle = [s for s in sols if abs(s.volume - V_HANDLE) < 0.01]
front = [s for s in sols if abs(s.volume - V_FRONT) < 0.01]
screws = [s for s in sols if abs(s.volume - V_SCREW) < 0.01]
expect("one handle, one front, four handle screws (count of each, as 1 / 1 / 4 -> product 4)", len(handle) * len(front) * len(screws), 4, 4, "   ")
handle, front = handle[0], front[0]
rows = []
for s in sorted(screws, key=lambda s: s.bounding_box().center().Y, reverse=True):
    bb = s.bounding_box()
    ext = (bb.max.X - bb.min.X, bb.max.Y - bb.min.Y, bb.max.Z - bb.min.Z)
    ax = int(np.argmax(ext))
    expect("screw at y %.1f: its long side is z (the axis along z) - the model, head to tip" % bb.center().Y, ext[2] if ax == 2 else -1, 8.0, 10.5)
    cx, cy = bb.center().X, bb.center().Y
    box = Pos(cx, cy, bb.center().Z) * Box(26.0, 26.0, 60.0)
    handle_c, front_c = handle & box, front & box
    z0, z1 = bb.min.Z - 0.5, bb.max.Z + 0.5
    L = z1 - z0
    # the screw itself: on the axis = shank + head; at r 2.0 = the head only
    sh = runs(s, (cx, cy, z0), (0, 0, 1), L)
    hd = runs(s, (cx + 2.0, cy, z0), (0, 0, 1), L)
    head_lo, head_hi = z0 + hd[0][0], z0 + hd[-1][1]
    tip_lo, tip_hi = z0 + sh[0][0], z0 + sh[-1][1]
    # which end is the head
    if abs(head_lo - tip_lo) < abs(head_hi - tip_hi):
        print("  (head at the low-z end)")
        head_under, tip, sgn = head_hi, tip_hi, +1
    else:
        print("  (head at the high-z end)")
        head_under, tip, sgn = head_lo, tip_lo, -1
    # the handle's plate under the head: r 2.3 (outside the 3.4 clearance hole, under the 5.7 head)
    zz0 = z0 - 15.0
    hp = runs(handle_c, (cx + 2.3, cy, zz0), (0, 0, 1), L + 30.0)
    hc = runs(handle_c, (cx, cy, zz0), (0, 0, 1), L + 30.0)       # on the axis: should be empty (the clearance hole)
    # the front: r 2.0 (outside the pilot) and on the axis (in the pilot)
    fo = runs(front_c, (cx + 2.0, cy, zz0), (0, 0, 1), L + 40.0)
    fa = runs(front_c, (cx, cy, zz0), (0, 0, 1), L + 40.0)
    plate = [(zz0 + a, zz0 + b) for a, b in hp]
    fr_out = [(zz0 + a, zz0 + b) for a, b in fo]
    fr_ax = [(zz0 + a, zz0 + b) for a, b in fa]
    print("  screw at (%.2f, %.2f): head underside z %.3f, tip z %.3f; handle at r 2.3: %s; handle on the axis: %s" % (cx, cy, head_under, tip, plate, hc))
    print("     front at r 2.0: %s ; front on the axis: %s" % (fr_out, fr_ax))
    # the plate the head sits on: the handle run that touches the head's underside
    pl = [r for r in plate if min(abs(r[0] - head_under), abs(r[1] - head_under)) < 0.05]
    expect("  the head sits on the grip's plate (a handle run starts at the head's underside)", len(pl), 1, 1, "   ")
    pl = pl[0]
    plate_t = pl[1] - pl[0]
    face = pl[1] if sgn > 0 else pl[0]          # the plate's far side = where it lies on the front
    fo_run = [r for r in fr_out if min(abs(r[0] - face), abs(r[1] - face)) < 0.05]
    expect("  the plate lies on the front's face (a front run starts where the plate ends)", len(fo_run), 1, 1, "   ")
    # the pilot: on the axis, the front starts again at the pilot's bottom
    if sgn > 0:
        bottom = min([a for a, b in fr_ax if a > face + 0.5] or [99.0])
    else:
        bottom = max([b for a, b in fr_ax if b < face - 0.5] or [-99.0])
    model_under = (tip - head_under) * sgn              # the model's length under the head (drawn short)
    bite = REAL_UNDER - plate_t                         # THE REAL SCREW: 8.0 under the head (ISO 7380 M3x8)
    spare = (bottom - face) * sgn - bite
    deep = (bottom - face) * sgn
    # the pilot's diameter at half the bite: from the axis out to the front, +x and -x
    zm = face + sgn * bite / 2
    px = runs(front_c, (cx, cy, zm), (1, 0, 0), 12.0)
    nx = runs(front_c, (cx, cy, zm), (-1, 0, 0), 12.0)
    r_pos, r_neg = px[0][0], nx[0][0]
    wall_out = px[0][1] - px[0][0]              # plastic from the pilot to the front's outer side (+x = the grip's side)
    wall_in = nx[0][1] - nx[0][0]
    rows.append(dict(y=cy, x=cx, plate=plate_t, bite=bite, spare=spare, deep=deep, d=r_pos + r_neg, wall_out=wall_out, wall_in=wall_in,
                     head_under=head_under, tip=tip, face=face, bottom=bottom, sgn=sgn))
    expect("  the grip's plate under the head (thickness)", plate_t, 2.9, 3.1)
    print("  %-96s %9.3f mm  (info: the screw in the Fusion file is drawn shorter than a real M3x8 - only the real one counts)" % ("  the model's length under the head", model_under))
    expect("  REAL M3x8 (8.0 under the head): thread in the front = 8.0 - the plate", bite, 4.8, 5.2)
    expect("  REAL M3x8: hole left below its tip (the pilot's depth - the thread)", spare, 1.0, 99)
    expect("  the pilot's depth from the front's face", deep, 6.8, 7.2)
    expect("  the pilot's diameter (half way down the bite)", r_pos + r_neg, 2.45, 2.55)
    expect("  plastic from the pilot to the front's outer side (toward the grip)", wall_out, 2.5, 99)
    expect("  plastic from the pilot to the inside", wall_in, 2.5, 99)

print("\n  %-10s %-10s %8s %8s %8s %8s %8s %10s %9s" % ("x", "y", "plate", "bite", "spare", "pilot", "pilot d", "wall out", "wall in"))
for r in rows:
    print("  %-10.2f %-10.2f %8.3f %8.3f %8.3f %8.3f %8.3f %10.3f %9.3f" % (r["x"], r["y"], r["plate"], r["bite"], r["spare"], r["deep"], r["d"], r["wall_out"], r["wall_in"]))
print("  a longer screw: M3x10 would need %.2f mm of hole below the plate; the pilot is %.2f deep -> %s" % (
    10.0 - rows[0]["plate"], rows[0]["deep"], "fits" if 10.0 - rows[0]["plate"] < rows[0]["deep"] - 0.5 else "DOES NOT FIT (would bottom out)"))

# ---------------------------------------------------------------- the picture: the cut through the screw at the top (y largest)
try:
    import trimesh
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path as MPath
    from shapely.geometry.polygon import orient
    r = rows[0]
    s0 = sorted(screws, key=lambda s: s.bounding_box().center().Y, reverse=True)[0]
    y0 = r["y"]
    crop = Pos(r["x"] + 2.0, y0, r["face"] + r["sgn"] * 2.0) * Box(34.0, 12.0, 30.0)
    M = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, y0], [0, 0, 0, 1]], float)   # (x, y, z) -> (x, z) in the plane y = y0
    tmp = tempfile.mkdtemp()
    polys = {}
    for nm, sol in (("front", front & crop), ("grip", handle & crop)):
        p = os.path.join(tmp, nm + ".stl")
        export_stl(sol, p, tolerance=0.01, angular_tolerance=0.05)
        m = trimesh.load(p, force="mesh")
        sec = m.section(plane_origin=[0, y0, 0], plane_normal=[0, 1, 0])
        pl2, _ = sec.to_2D(to_2D=M, check=False)
        polys[nm] = pl2.polygons_full
    fig, axp = plt.subplots(figsize=(9.6, 7.2), dpi=130)
    colours = {"front": "#b9b9b4", "grip": "#ee7a22", "screw": "#3d4650"}

    def draw(poly, c):
        if poly.geom_type == "MultiPolygon":
            for g in poly.geoms:
                draw(g, c)
            return
        poly = orient(poly, 1.0)
        verts, codes = [], []
        for ring in [poly.exterior] + list(poly.interiors):
            xy = np.asarray(ring.coords)
            xy = np.c_[xy[:, 0], -xy[:, 1]] if r["sgn"] > 0 else xy      # the screen side (the head) up
            verts += xy.tolist(); codes += [MPath.MOVETO] + [MPath.LINETO] * (len(xy) - 2) + [MPath.CLOSEPOLY]
        axp.add_patch(PathPatch(MPath(verts, codes), facecolor=c, edgecolor="#222222", lw=0.6))
    for nm in ("front", "grip"):
        for p in polys[nm]:
            draw(p, colours[nm])
    from shapely.geometry import Polygon as SPoly, box as sbox
    from shapely.ops import unary_union
    hu, sg = r["head_under"], r["sgn"]                  # the real screw in the cut plane, in (x, z)
    zt_real = hu + sg * REAL_UNDER
    shank = SPoly([(r["x"] - 1.5, hu), (r["x"] + 1.5, hu), (r["x"] + 1.5, zt_real - sg * 0.4), (r["x"] + 1.1, zt_real),
                   (r["x"] - 1.1, zt_real), (r["x"] - 1.5, zt_real - sg * 0.4)])
    th = np.linspace(0, np.pi, 40)
    head = SPoly([(r["x"] + HEAD_D / 2 * np.cos(t), hu - sg * HEAD_H * np.sin(t) ** 0.6) for t in th])
    draw(unary_union([shank, head]), colours["screw"])
    r["tip"] = zt_real
    up = (lambda z: -z) if r["sgn"] > 0 else (lambda z: z)
    xa = r["x"]
    zf, zt, zb, zh = up(r["face"]), up(r["tip"]), up(r["bottom"]), up(r["head_under"])
    axp.set_xlim(xa - 13.0, xa + 15.5); axp.set_ylim(min(zb, zt) - 6.0, zh + 5.0)
    axp.set_aspect("equal"); axp.axis("off")
    big = dict(fontsize=15, fontweight="bold")
    axp.text(xa + 9.5, (zf + zb) / 2, "grip", va="center", ha="center", color="white", **big)
    axp.text(xa - 12.5, zf - 3.2, "front", va="center", color="#555555", **big)
    axp.text(xa - 5.3, zh + 2.3, "screw M3x8", ha="center", va="center", color="#3d4650", **big)

    def dim(x, za, zb_, label):
        axp.annotate("", xy=(x, za), xytext=(x, zb_), arrowprops=dict(arrowstyle="<->", lw=1.4, color="black"))
        if label:
            axp.text(x + 0.5, (za + zb_) / 2, label, va="center", fontsize=12.5,
                     bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85))
    dim(xa + 3.4, zh, zf, "3 mm")
    dim(xa - 3.0, zf, zt, "")
    axp.text(xa - 3.6, (zf + zt) / 2, "5 mm of\nthread", va="center", ha="right", fontsize=12.5,
             bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85))
    dim(xa + 2.2, zt, zb, "2 mm to spare")
    axp.set_title("One grip screw, cut through the middle (screen side up)\n"
                  "3 mm through the grip, 5 mm into the front, 2 mm of hole left", fontsize=13)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight", facecolor="white")
    print("\n  picture: %s (md5 %s)" % (OUT, hashlib.md5(open(OUT, "rb").read()).hexdigest()))
except Exception as ex_:
    import traceback; traceback.print_exc()
    print("  (picture not made: %s)" % ex_)
print("\n%s" % ("ALL CHECKS PASS" if not FAILS else "FAILED: %d -> %s" % (len(FAILS), FAILS)))
sys.exit(1 if FAILS else 0)
