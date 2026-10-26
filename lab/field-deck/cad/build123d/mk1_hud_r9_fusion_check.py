"""MK-I r9 - checks of THE HUD FOR THE REAL OLED AS FUSION BUILT IT (h1 body, h2 cap + references), read back (h3):
readback/item_r9_hud.step = mk1/MK1_r9_hud_fusion_readback_item_NOT-FOR-PRINT.step (the whole r8 item).
  1. the item: every solid but the body is the one read back before (readback/item_r8_vents.step), each by its own measures
     (volume, area, box, every face's area and centre: a boolean of two identical solids is degenerate in OCC); new: the
     cap r9 and the five pieces of the real OLED (reference);
  2. Fusion's body is the cloud's trial (mk1_hud_r9.py) CELL BY CELL (20 mm cells; each solid cut by each cell - not a boolean
     of the two near-identical solids), and nothing else of the old body changed; the cap the same way (5 mm cells); the OLED
     pieces by volume and box;
  3. every check of the trial again, on FUSION's body and cap (mk1_hud_r9.main(fusion=...)): the board in the tube, the pod,
     the other parts, the route in, the driver, the views, the print gates.
  python3 mk1_hud_r9_fusion_check.py [STEP | --selftest-bad]"""
import sys, os
import numpy as np
from build123d import import_step, Pos, Box
import mk1_hud_r9 as H

PATH = sys.argv[1] if len(sys.argv) > 1 else "readback/item_r9_hud.step"
OLD = H.READBACK
expect, info, vol, FAILS = H.expect, H.info, H.vol, H.FAILS
old = list(import_step(OLD).solids())
b0 = [s for s in old if abs(s.volume - H.VOLS["body"]) < 0.01][0]
TL = H.tools()
trial, _ = H.new_body(b0, TL)
tcap = H.new_cap()
tboard = H.board()
if PATH == "--selftest-bad":                 # must FAIL: the trial with a 0.2 mm3 nick in the pod's side wall, and the cap 0.1 thinner nowhere
    nick = H.fbox(91.5, 92.0, 14.0, 14.8, 10.0, 10.5)                    # 0.5 x 0.8 x 0.5 = 0.2 mm3 in the handle-side wall
    new = [s for s in old if s is not b0] + [trial - nick, tcap] + [s for _, s in tboard]
else:
    new = list(import_step(PATH).solids())
print("1. THE ITEM (%s, %d solids) AGAINST THE ONE READ BACK BEFORE (%s, %d solids)" % (PATH, len(new), OLD, len(old)))
expect("solids: 6 more than before (the cap r9 + 5 pieces of the real OLED)", len(new) - len(old), 6, 6, "   ")
cand = sorted([s for s in new if abs(s.volume - trial.volume) < 50.0], key=lambda s: abs(s.volume - trial.volume))
expect("one solid near the new body's volume (%.4f; within 50 mm3)" % trial.volume, len(cand), 1, 1, "   ")
if not cand:
    print("FAILED: no body in the readback"); sys.exit(1)
fus = cand[0]
capc = sorted([s for s in new if abs(s.volume - tcap.volume) < 1.0], key=lambda s: abs(s.volume - tcap.volume))
expect("one solid near the new cap's volume (%.4f; within 1 mm3)" % tcap.volume, len(capc), 1, 1, "   ")
fcap = capc[0]
sig = lambda x: sorted((round(f.area, 4), tuple(round(c, 4) for c in f.center())) for f in x.faces())
bx = lambda x: [round(v, 4) for v in (x.bounding_box().min.X, x.bounding_box().min.Y, x.bounding_box().min.Z, x.bounding_box().max.X, x.bounding_box().max.Y, x.bounding_box().max.Z)]
rest_new = [s for s in new if s is not fus and s is not fcap]
rest_old = [s for s in old if s is not b0]
unmatched, used = [], set()
for s in rest_new:
    hit = None
    for k, o in enumerate(rest_old):
        if k in used or abs(s.volume - o.volume) > 1e-3 or abs(s.area - o.area) > 1e-3 or bx(s) != bx(o) or len(s.faces()) != len(o.faces()):
            continue
        if sig(s) == sig(o):
            hit = k; break
    if hit is None:
        unmatched.append(s)
    else:
        used.add(hit)
expect("every old solid but the body found again, identical (volume, area, box, every face's area and centre): missing", len(rest_old) - len(used), 0, 0, "   ")
expect("new solids that are not an old one: the 5 OLED pieces", len(unmatched), 5, 5, "   ")
for (nm, ts) in tboard:
    m = [s for s in unmatched if abs(s.volume - ts.volume) < 0.01 and max(abs(a - b) for a, b in zip(bx(s), bx(ts))) < 0.002]
    expect("  the real OLED's %s: one solid with the trial's volume (%.4f) and box" % (nm, ts.volume), len(m), 1, 1, "   ")

print("\n2. FUSION'S BODY AND CAP ARE THE TRIAL'S (cell by cell)")
expect("body: one valid solid", (1.0 if fus.is_valid else 0.0) * len(fus.solids()), 1, 1, "   ")
expect("body: volume, Fusion's minus the trial's", fus.volume - trial.volume, -0.01, 0.01, "mm3")
expect("body: bounding boxes, largest difference of any corner", max(abs(a - b) for a, b in zip(bx(fus), bx(trial))), 0, 0.001)
cuts = [s for _, _, s in TL]


def cells_compare(a, t, o, x0, x1, y0, y1, z0, z1, step, label, tools):
    worst_t, worst_o, n_cut, n_rest = 0.0, 0.0, 0, 0
    for x in np.arange(x0, x1, step):
        for y in np.arange(y0, y1, step):
            for z in np.arange(z0, z1, step):
                c = Pos(x + step / 2, y + step / 2, z + step / 2) * Box(step, step, step)
                cb = c.bounding_box()
                va = vol(a, c)
                vt = vol(t, c)
                if va == 0.0 and vt == 0.0 and (o is None or vol(o, c) == 0.0):
                    continue
                worst_t = max(worst_t, abs(va - vt))
                crosses = any(not (k.bounding_box().max.X <= cb.min.X or cb.max.X <= k.bounding_box().min.X or k.bounding_box().max.Y <= cb.min.Y or
                                   cb.max.Y <= k.bounding_box().min.Y or k.bounding_box().max.Z <= cb.min.Z or cb.max.Z <= k.bounding_box().min.Z) for k in tools)
                if crosses:
                    n_cut += 1
                elif o is not None:
                    n_rest += 1
                    worst_o = max(worst_o, abs(va - vol(o, c)))
    expect("%s cell by cell (%d cells crossing a tool, %d not): largest difference, Fusion's against the trial" % (label, n_cut, n_rest), worst_t, 0, 0.01, "mm3")
    if o is not None:
        expect("  %s cells away from the tools: largest difference, Fusion's against the old one" % label, worst_o, 0, 0.01, "mm3")


cells_compare(fus, trial, b0, -110.0, 110.0, -100.0, 100.0, -10.0, 60.0, 20.0, "body", cuts)
expect("the old body minus Fusion's = what the eight steps change in all (%.4f)" % (b0.volume - trial.volume), b0.volume - fus.volume, b0.volume - trial.volume - 0.02, b0.volume - trial.volume + 0.02, "mm3")
info("faces: Fusion's body %d, the trial %d, the old body %d" % (len(fus.faces()), len(trial.faces()), len(b0.faces())), 0.0, "   ")
expect("cap: one valid solid", (1.0 if fcap.is_valid else 0.0) * len(fcap.solids()), 1, 1, "   ")
expect("cap: volume, Fusion's minus the trial's", fcap.volume - tcap.volume, -0.01, 0.01, "mm3")
expect("cap: bounding boxes, largest difference", max(abs(a - b) for a, b in zip(bx(fcap), bx(tcap))), 0, 0.001)
cb_ = tcap.bounding_box()
cells_compare(fcap, tcap, None, 55.0, 100.0, 35.0, 75.0, 10.0, 55.0, 5.0, "cap", [tcap])

if os.environ.get("STOP_AFTER_2"):
    print("\n(stopped after section 2) %s" % ("ALL CHECKS PASS" if not FAILS else "FAILED: %d -> %s" % (len(FAILS), FAILS)))
    sys.exit(1 if FAILS else 0)
print("\n3. EVERY CHECK OF THE TRIAL AGAIN, ON FUSION'S BODY AND CAP")
H.main(fusion=PATH)
print("\n%s" % ("ALL CHECKS PASS" if not FAILS else "FAILED: %d -> %s" % (len(FAILS), FAILS)))
sys.exit(1 if FAILS else 0)
