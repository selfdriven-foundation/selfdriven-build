"""MK-I r9 - DOES A REAL M3x8 FIT EVERY BLIND PILOT? (2026-10-13)
Found while answering "the screws look too small": the screws in the Fusion file are drawn SHORTER than a real ISO 7380 M3x8
(8.0 under the head): the handle's 6.975, the lever's 7.35; the back plate's and the HUD cap's are heads only; the speaker
cover's are 8.0. The design checks measured their bites with those models - so here every screw is checked with the REAL
length: from its head's seat, 8.0 along its axis; the hole in the part it threads into must go deeper than the tip.
(The 4 body-to-front screws go through a through-pilot in the front's boss - they cannot bottom out; not here.)
Each part is cropped to a 40 mm cube round the screw first (the probes on the whole body are slow).
  python3 mk1_screw_real_length_r9.py"""
import sys, hashlib
import numpy as np
from build123d import import_step, Vector, GeomType, Box, Pos

READBACK = "readback/item_r9_hud.step"
REAL_UNDER = 8.0
VOL = dict(body=115715.2078, front=129177.2313, plate=23686.9156, handle=96836.0778, cap=3782.2976, cover=11190.0952, lever=789.5319)
SCREWS = [(40.8281, "back plate / HUD cap"), (91.4074, "handle"), (94.0581, "power lever"), (110.7349, "speaker cover")]
INTO = {"back plate / HUD cap": "body", "handle": "front", "power lever": "body", "speaker cover": "body"}
FAILS = []


def expect(name, value, lo, hi, unit="mm "):
    ok = lo <= value <= hi
    print("  %-100s %8.3f %s %s" % (name, value, unit, "ok" if ok else "*** FAIL ***"), flush=True)
    if not ok:
        FAILS.append(name)


def runs(solid, p0, u, length, step=0.05):
    """stretches (t0, t1) of the line p0 + t u, t in 0..length, inside `solid` (sampled, edges bisected to ~1e-5)"""
    at = lambda t: solid.is_inside(Vector(*(np.asarray(p0) + t * np.asarray(u))))

    def edge(a, b, ina):
        for _ in range(12):
            m = (a + b) / 2
            a, b = (m, b) if at(m) == ina else (a, m)
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
                out.append((t_in, e)); t_in = None
    if t_in is not None:
        out.append((t_in, length))
    return out


sols = list(import_step(READBACK).solids())
print("REAL M3x8 (8.0 under the head) AGAINST EVERY BLIND PILOT, from %s (md5 %s)" % (READBACK, hashlib.md5(open(READBACK, "rb").read()).hexdigest()))
part = {k: [s for s in sols if abs(s.volume - v) < 0.01][0] for k, v in VOL.items()}
seen, rows = [], []
for vol, kind in SCREWS:
    for s in [x for x in sols if abs(x.volume - vol) < 0.01]:
        c = np.array(tuple(s.center()))
        if any(np.linalg.norm(c - q) < 0.05 for q in seen):
            continue                                           # the same screw twice in the file (the cover's screw 1)
        if kind == "speaker cover" and abs(c[0] + 6.6) < 0.05:
            print("  (left out: the speaker cover's OLD screw 2 at x -6.6 - hidden in Fusion, no hole there; mk1_final_r9_check)")
            continue
        seen.append(c)
        flats = [f for f in s.faces() if f.geom_type == GeomType.PLANE]
        und = max(flats, key=lambda f: f.area)
        u = np.array(tuple(und.normal_at(und.center()))); u /= np.linalg.norm(u)
        a0 = np.array(tuple(und.center()))
        a0 = a0 + np.dot(c - a0, u) * u                        # a point on the axis level with the centre
        side = np.cross(u, [1, 0, 0] if abs(u[0]) < 0.9 else [0, 1, 0]); side /= np.linalg.norm(side)
        V = np.array([tuple(v) for v in s.vertices()])
        tt = (V - a0) @ u
        L0, L1 = tt.min() - 0.3, tt.max() + 0.3
        head = runs(s, a0 + L0 * u + 2.2 * side, u, L1 - L0)   # beside the shank: the head only
        shank = runs(s, a0 + L0 * u, u, L1 - L0)              # on the axis: head + shank
        h0, h1 = L0 + head[0][0], L0 + head[-1][1]
        s0, s1 = L0 + shank[0][0], L0 + shank[-1][1]
        box = Pos(*c) * Box(40.0, 40.0, 40.0)
        into = part[INTO[kind]] & box
        if s1 > h1 + 0.5:                                      # the shank goes +u
            seat, d = h1, u
        elif s0 < h0 - 0.5:
            seat, d = h0, -u
        else:                                                  # a head only: the side where the threaded part is
            hit = []
            for sg, sx in ((+1, h1), (-1, h0)):
                r_ = runs(into, a0 + sx * u + 2.3 * side, sg * u, 15.0)
                hit.append((r_[0][0] if r_ else 99.0, sg, sx))
            _, sg, sx = min(hit)
            seat, d = sx, sg * u
        o = a0 + seat * u                                      # the seat point on the axis
        r_out = runs(into, o + 2.3 * side, d, 20.0)
        r_ax = runs(into, o + 0.02 * d, d, 25.0)
        if not r_out:
            print("  %s at (%.2f, %.2f, %.2f): the %s not found beside the screw" % (kind, *o, INTO[kind])); FAILS.append(kind); continue
        entry = r_out[0][0]
        bottom = [a for a, b in r_ax if a > entry + 0.5]
        model_under = (s1 - h1) if d is u else (h0 - s0)
        print("\n  %s screw, seat at (%.2f, %.2f, %.2f), into (%.3f, %.3f, %.3f); the model: %.3f under its head" % (kind, *o, *d, max(model_under, 0.0)))
        thread = REAL_UNDER - entry
        print("    under the head to the %s's face (the clamped part): %.3f -> a real M3x8 has %.3f of thread in the %s" % (INTO[kind], entry, thread, INTO[kind]))
        if not bottom:
            far = r_out[0][1]                                  # where the boss round the pilot ends
            print("    the pilot runs through; the plastic round it ends %.3f from the seat" % far)
            expect("    %s at (%.1f, %.1f, %.1f): a real M3x8's tip stays inside the boss by" % (kind, *o), far - REAL_UNDER, 0.0, 99)
            rows.append((kind, o, entry, thread, None)); continue
        depth = bottom[0] - entry
        print("    the pilot: %.3f deep from the %s's face" % (depth, INTO[kind]))
        rows.append((kind, o, entry, thread, depth))
        expect("    %s at (%.1f, %.1f, %.1f): hole left below a real M3x8's tip" % (kind, *o), depth - thread, 0.5, 99)
        expect("    %s at (%.1f, %.1f, %.1f): real thread in the %s" % (kind, *o, INTO[kind]), thread, 3.0, 99)
print("\n  %-22s %-26s %8s %8s %8s %8s" % ("screw", "seat", "clamped", "thread", "pilot", "spare"))
for kind, o, entry, thread, depth in rows:
    print("  %-22s (%7.2f, %7.2f, %6.2f) %8.3f %8.3f %8s %8s" % (kind, *o, entry, thread, "through" if depth is None else "%.3f" % depth,
                                                              "-" if depth is None else "%.3f" % (depth - thread)))
print("\n%s" % ("ALL CHECKS PASS" if not FAILS else "FAILED: %d -> %s" % (len(FAILS), FAILS)))
sys.exit(1 if FAILS else 0)
