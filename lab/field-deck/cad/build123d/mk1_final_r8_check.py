"""MK-I r8 - THE FINAL CANDIDATE, CHECKED AS ONE (2026-10-12).
Read back from Fusion (version 10, the whole r8 item): readback/item_r8_final_candidate.step
= mk1/MK1_r8_final_candidate_item_readback_NOT-FOR-PRINT.step. Every solid is named by its volume (Fusion's list of the item).
  1. inventory: every solid accounted for; the ones that are hidden in Fusion (old or replaced) are named and left out;
  2. what changed since the last full checks: each part to print against the readback of 2026-10-11 (names 3.5 mm,
     readback/item_r8names35.step) - only the front may differ (the mic pocket, checked on its own today);
  3. assembly: every pair of solids that are in the deck - overlaps (only screws biting into their pilots are allowed) and
     the smallest gaps between the printed parts and the electronics;
  4. each part to print, lying as it is printed: one closed mesh, the Bambu A1's bed (256 x 256 x 256), erosion, attachment,
     support survey, weight (PETG 1.27 g/cm3).
  python3 mk1_final_r8_check.py"""
import sys, os, math, tempfile, itertools
import numpy as np, trimesh
from build123d import import_step, Pos, Rot
import mk1_gates as G
import support_survey as SS
from attach_scan import scan_attach, validate_instrument
from mk1_body_r3 import export_clean_stl, cap_for_print
import mk1_sound_r8 as S8
import mk1_body_r7 as B7

NEW = "readback/item_r8_final_candidate.step"
OLD = "readback/item_r8names35.step"
TMP = tempfile.mkdtemp(prefix="mk1_final_")
FAILS = []


def expect(name, value, lo, hi, unit="   "):
    ok = (value == value) and lo <= value <= hi
    print("  %-112s %12.4f %s  %s" % (name, value, unit, "ok" if ok else "*** FAIL ***"), flush=True)
    if not ok:
        FAILS.append(name)


def info(name, value=0.0, unit="   ", note=""):
    print("  %-112s %12.4f %s  %s" % (name, value, unit, note), flush=True)


# ---------------------------------------------------------------- names by volume (Fusion's list of the item, version 10)
TABLE = [  # (volume, name, role)   role: print / ring / ref / screw / hidden
    (117633.4739, "Body", "print"), (129177.2313, "Front r8 (mic pocket)", "print"), (23686.9156, "Back plate r8", "print"),
    (96836.0778, "Handle (grooved)", "print"), (3701.0170, "HUD cap", "print"), (11190.0952, "Speaker cover", "print"),
    (789.5319, "Power lever r8", "print"), (14024.4414, "Retainer ring (printed, reused)", "ring"),
    (130545.8641, "Front (armoured), shared - HIDDEN, replaced", "hidden"), (1059.4635, "Power lever r7 - HIDDEN, replaced", "hidden"),
    (383818.4055, "Electronics block (old estimate) - HIDDEN", "hidden"),
    (195786.5680, "Screen", "ref"), (33600.0, "Speaker (deferred; maker's size)", "ref"), (142.9120, "HUD red filter (film)", "ref"),
    (1088.7435, "OLED board", "ref"), (14497.6, "X1201 battery board", "ref"), (6664.0, "Pi 5 board", "ref"),
    (4536.0, "Network socket", "ref"), (3603.6, "USB pair", "ref"), (208.8384, "Pi USB-C (stays shut)", "ref"),
    (146.25, "HDMI socket", "ref"), (209.9827, "Charge socket USB-C", "ref"), (127.4230, "Brass post (6 tall)", "ref"),
    (37.5224, "Power switch plunger", "ref"), (33.2891, "Old switch plunger estimate - HIDDEN", "hidden"),
    (87.6851, "Old brass post estimate - HIDDEN", "hidden"), (255.6, "Old top socket - HIDDEN", "hidden"),
    (161.525, "Old top socket - HIDDEN", "hidden"), (204.48, "Old top socket - HIDDEN", "hidden"),
    (40.8281, "M3x8 (plate / HUD cap)", "screw"), (91.4074, "M3x8 (handle)", "screw"), (94.0581, "M3x8 (lever)", "screw"),
    (110.7349, "M3x8 (speaker cover)", "screw")]


def name_of(s):
    v = s.volume
    for tv, nm, role in TABLE:
        if abs(v - tv) < 0.01:
            return nm, role
    if abs(v - 362.88) < 0.01:                     # two switch bodies: the stack's (true place) and the old estimate (hidden)
        bb = s.bounding_box()
        return ("Power switch (true place)", "ref") if bb.min.X < -23.0 else ("Old switch estimate - HIDDEN", "hidden")
    return "UNKNOWN %.4f" % v, "unknown"


def vol(a, b):
    try:
        c = a & b
        return 0.0 if c is None else sum(x.volume for x in c.solids())
    except Exception:
        return float("nan")


def gap(a, b):
    try:
        return a.distance_to(b)
    except Exception:
        return float("nan")


new = import_step(NEW).solids()
old = import_step(OLD).solids()
print("1. INVENTORY (%s): %d solids" % (NEW, len(new)))
named = [(s, *name_of(s)) for s in new]
for role in ("print", "ring", "ref", "screw", "hidden", "unknown"):
    rows = [(n, s) for s, n, r in named if r == role]
    if rows:
        print("   %-7s %2d: %s" % (role, len(rows), ", ".join(sorted(set(n for n, _ in rows)))))
expect("solids that no name fits", sum(1 for _, _, r in named if r == "unknown"), 0, 0)
expect("every solid valid", sum(1 for s, _, _ in named if not s.is_valid), 0, 0)
# the old cover screw 2 (hidden) and the new one sit 4.4 apart; the two screw 1s coincide: keep the shown ones (the reference set)
info("speaker-cover screws in the file: %d (screw 1 twice, the old screw 2 hidden in Fusion) - section 3 keeps screw 1 once and screw 2 at the new post" % sum(1 for s, n, r in named if n.startswith("M3x8 (speaker cover)")))

print("\n2. WHAT CHANGED SINCE THE LAST FULL CHECKS (against %s)" % OLD)
oldmap = {}
for s in old:
    n, r = name_of(s)
    if r == "print":
        oldmap.setdefault(n, s)
for s, n, r in named:
    if r != "print":
        continue
    o = oldmap.get(n)
    if n.startswith("Front r8"):
        o = [x for x in old if abs(x.volume - 130545.8641) < 0.01][0]
        d1, d2 = s.volume - vol(s, o), o.volume - vol(o, s)
        info("%s against the shared front of 2026-10-11: only the mic pocket and the chin's marks (checked today, mk1_mic_pocket_fusion_check)" % n, d1 + d2, "mm3")
        continue
    if o is None:
        expect("%s: found in the old readback" % n, 0, 1, 1); continue
    # a boolean of two identical solids is degenerate in OCC (every face coincides) and comes back empty: compare the solids'
    # own measures instead - volume, area, box, and every face's area and centre
    sig = lambda x: sorted((round(f.area, 4), tuple(round(c, 4) for c in f.center())) for f in x.faces())
    bx = lambda x: [round(v, 4) for v in (x.bounding_box().min.X, x.bounding_box().min.Y, x.bounding_box().min.Z, x.bounding_box().max.X, x.bounding_box().max.Y, x.bounding_box().max.Z)]
    same = abs(s.volume - o.volume) < 1e-3 and abs(s.area - o.area) < 1e-3 and bx(s) == bx(o) and len(s.faces()) == len(o.faces()) and sig(s) == sig(o)
    expect("%s: identical to the one checked last (volume, area, box, %d faces each with its area and centre)" % (n, len(s.faces())), 1.0 if same else 0.0, 1, 1)

print("\n3. ASSEMBLY: the deck as it goes together (hidden and replaced solids left out)")
deck = [(s, n, r) for s, n, r in named if r in ("print", "ring", "ref", "screw")]
cover_screws = [(s, n, r) for s, n, r in deck if n.startswith("M3x8 (speaker cover)")]
dup = []
for i, (s, n, r) in enumerate(cover_screws):
    for t, m, q in cover_screws[i + 1:]:
        if abs(s.bounding_box().min.X - t.bounding_box().min.X) < 0.01 and abs(s.bounding_box().min.Y - t.bounding_box().min.Y) < 0.01:
            dup.append(t)
old_screw2 = [s for s, n, r in cover_screws if abs(s.bounding_box().min.X + 13.8) < 0.01]
deck = [(s, n, r) for s, n, r in deck if not any(s is d for d in dup + old_screw2)]
info("solids in the deck: %d (one duplicate cover screw 1 and the old cover screw 2 left out)" % len(deck))
bbs = [s.bounding_box() for s, _, _ in deck]
over = []
for i, j in itertools.combinations(range(len(deck)), 2):
    a, b = bbs[i], bbs[j]
    if a.max.X < b.min.X or b.max.X < a.min.X or a.max.Y < b.min.Y or b.max.Y < a.min.Y or a.max.Z < b.min.Z or b.max.Z < a.min.Z:
        continue
    v = vol(deck[i][0], deck[j][0])
    if v > 0.001 or v != v:
        over.append((v, deck[i][1], deck[j][1], deck[i][2], deck[j][2]))
for v, n1, n2, r1, r2 in sorted(over, reverse=True):
    screwish = "screw" in (r1, r2)
    print("     overlap %9.3f mm3  %-40s x %-40s %s" % (v, n1, n2, "(a screw biting into its pilot)" if screwish else "<--- LOOK"))
KNOWN = {frozenset(("Screen", "Retainer ring (printed, reused)")): "the screen is drawn as a full box up to z 0; the real screen's metal back is at -2.18 and the glass border under the ring at about -7.4 (2026-10-07: 'the ring's pads touch nothing')"}
for v, n1, n2, r1, r2 in over:
    k = KNOWN.get(frozenset((n1, n2)))
    if k:
        info("  known, not a clash: %s x %s - %s" % (n1, n2, k), v, "mm3")
expect("overlaps between solids where neither is a screw (and not a known reference over-estimate)", sum(1 for v, n1, n2, r1, r2 in over if "screw" not in (r1, r2) and frozenset((n1, n2)) not in KNOWN), 0, 0)
for v, n1, n2, r1, r2 in over:
    if "screw" in (r1, r2):
        expect("  screw overlap %s x %s: a thread's bite (a pilot 2.5 in an M3: up to about 60 mm3 for 8 mm)" % (n1, n2), v, 0, 60.0, "mm3")
printed = [(s, n) for s, n, r in deck if r in ("print", "ring")]
elec = [(s, n) for s, n, r in deck if r == "ref" and n not in ("Speaker (deferred; maker's size)", "HUD red filter (film)", "Screen")]
print("   smallest gaps, printed part <-> electronics:")
for s, n in printed:
    best = min(((gap(s, e), m) for e, m in elec), key=lambda q: q[0])
    info("    %-34s nearest electronics: %-34s" % (n, best[1]), best[0], "mm ")

print("\n4. EACH PART TO PRINT, LYING AS IT IS PRINTED (Bambu A1: 256 x 256 x 256)")
ORIENT = {"Body": lambda s: s, "Front r8 (mic pocket)": lambda s: s, "Back plate r8": lambda s: s, "Handle (grooved)": lambda s: s,
          "HUD cap": cap_for_print, "Speaker cover": S8.cover_for_print, "Power lever r8": B7.lever_for_print}
bad = trimesh.boolean.union([trimesh.creation.box(bounds=[[0, 0, 0], [20, 20, 4]]), trimesh.creation.box(bounds=[[9.85, 0, 3.9], [10.15, 20, 6.1]]),
                             trimesh.creation.box(bounds=[[0, 0, 6], [20, 20, 10]])], engine="manifold")
assert any(3.5 < lo < 5.0 for lo, hi in G.erosion(bad, "coupon (0.3 mm band)")), "erosion instrument missed the coupon"
validate_instrument()
summary = []
for s, n, r in named:
    if r != "print":
        continue
    p = os.path.join(TMP, n.split(" ")[0] + ".stl")
    export_clean_stl(ORIENT[n](s), p)
    m = G.place(p)
    ex = m.bounds[1] - m.bounds[0]
    print("\n   %s: watertight %s, %d faces, %.1f x %.1f x %.1f on the plate, %.1f g PETG" % (n, m.is_watertight, len(m.faces), *ex, m.volume / 1000 * 1.27), flush=True)
    expect("   %s: one closed mesh" % n, 1.0 if (m.is_watertight and len(m.split(only_watertight=False)) == 1) else 0.0, 1, 1)
    fits = min(max(ex[0], ex[1]) <= 256 and min(ex[0], ex[1]) <= 256, ex[2] <= 256)
    expect("   %s: fits the A1's bed (largest side %.1f, height %.1f)" % (n, max(ex[0], ex[1]), ex[2]), 1.0 if fits else 0.0, 1, 1)
    e = G.erosion(m, "   " + n)
    expect("   %s: layers that leave no printable line" % n, len(e), 0, 0)
    f = scan_attach(m, "   " + n + " attachment")
    sv = SS.survey(p, 30.0, False)
    tall = sum(o[1] for o in sv if o[0] > 5.0)
    info("   %s: attachment lines %d (islands %d); faces needing a tower %.1f mm2, above z 5 %.1f mm2" % (n, len(f), sum(1 for q in f if q[0] == "ISLAND"), sum(o[1] for o in sv), tall))
    summary.append((n, ex, m.volume / 1000 * 1.27, len(f), sum(1 for q in f if q[0] == "ISLAND"), sum(o[1] for o in sv), tall))
print("\n   part                          size on the plate           PETG    attach. lines  islands  tower faces  of them above z 5")
for n, ex, g, nf, ni, sv, tall in summary:
    print("   %-28s %6.1f x %6.1f x %5.1f  %6.1f g  %8d %9d %10.1f mm2 %10.1f mm2" % (n, *ex, g, nf, ni, sv, tall))
print("\n%s" % ("ALL CHECKS PASS" if not FAILS else "FAILED: %d -> %s" % (len(FAILS), FAILS)))
sys.exit(1 if FAILS else 0)
