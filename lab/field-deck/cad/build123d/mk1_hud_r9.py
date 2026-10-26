"""MK-I r9 - THE HUD POD AND CAP FOR THE REAL OLED BOARD, tried here before Fusion builds them (2026-10-12).

Why. The pod (body) and the cap were drawn in R3 to the owner's caliper figures of 2026-09-15: board 25.66 x 25.56, holes
21.0 apart, glass 24.66 x 17. His photo IMG_2095 (board flat, glass up, straight down; measured with in-plane references)
gives the real board: PCB 27.3 x 27.6, holes 23.36 (along the header edge) x 23.80 centre to centre, glass 26.7 x 19.48
from 3.93 below the header edge, the lit area 21.74 x 10.86 (128 x 64 at 0.1698) from 6.43 below the header edge, the
display's flex folding round the far edge (0.7 beyond it), and FOUR SOLDER JOINTS ON THE FRONT at the header (the pins
come through from the back). The caliper figures were 2 .. 3 short (as found on 2026-10-07). The real board would not go
into R3's tube (cavity 27.6 along), and its screws would miss the posts by 1.2 mm a side.

Kept: R3's facet (48 deg), the lower end of the tube (A_LO 1.2), the tube's depth (rear plane 34.5: the plugs and the
wires' bend need it), header UP (the plugs need the 80 mm free above the tube while the board goes in - R3; the deck's
software shows the picture upright with the header at the top, as both photos show), the OLED screws M1.6x4 into d1.3
pilots (the holes are 2.0: M1.6 passes), the cap's three M3 screws in their places (the body's cap pilots do not move).
Changed (body):
  the tube along A_LO .. 31.2 (was 28.8), its top wall 2.5 above that (facet top 33.7, was 31.3); across x 62.1 .. 90.9
  (was 62.5 .. 90.5): at least 0.4 round the board at its largest, wherever it sits;
  the old window, glass pocket, posts and pilots filled; NEW four posts at the real holes (centre x 76.5, along 16.52,
  23.36 x 23.80), the two lower ones carried down to the tube's floor (R3's left a 0.3 slit there);
  glass pocket 27.9 x 20.68 round the glass (0.6 a side), 3.2 deep as before, with a RELIEF over the four solder joints (11.4 wide,
  up to the tube's top: 3.2 of room in front of the PCB there; R3 had 1.7 - the joints stand about 1.5 .. 2);
  window 23.6 x 12.93 over the lit area (at least 0.73 round it, with the 0.2 shift);
  the window's top edge FLAT at z 19.2 (review P "the chin": the lip above the window began as a 0.08 mm thread);
  the brow up to 38.2 (was 37.2).
Changed (cap): 1.0 longer at its upper edge (to the brow's 38.2), so the upper counterbores keep 1.25 to its edge (review P:
  0.25), 0.45 at the very top where the cap's 0.8 chamfer is; its highest point stays 0.39 below the back plate (z 53).

  python3 mk1_hud_r9.py      -> the checks (and out/mk1/MK1_r9_body_hud_trial / MK1_r9_hudcap_trial _NOT-FOR-PRINT.step)
  python3 mk1_hud_r9.py --fusion readback/item_r9_hud.step   -> the same checks on FUSION's body and cap (read back)
"""
import math, os, sys, tempfile
import numpy as np
from build123d import *
import mk1_body_r3 as R3
import mk1_body_r4 as B4
from r3_params import WALL, SKIRT_Z, Y_TOPF, FACET_DEG, PILOT_D, CLEAR_D, HEAD_D, HEAD_DEEP
from build_r3 import facet_pt, FDIR, FIN

READBACK = "readback/item_r8_vents.step"
VOLS = dict(body=116520.7858, cap=3701.0170, front=129177.2313, ring=14024.4414, oled=1088.7435, handle=96836.0778,
            plate=23686.9156, film=142.9120, screen=195786.5680)
GRID = 0.2
BACK_Z = 53.0                    # the back plate's outer face (r5 "slim")
C48, S48 = math.cos(math.radians(FACET_DEG)), math.sin(math.radians(FACET_DEG))
# ---------------- the board as measured (IMG_2095): u across (= x), v down from the HEADER edge
PCB = (27.3, 27.6)               # u, v
PCB_TOL = 0.15                   # each size, measured to about this
HOLES = (23.36, 23.80)           # centre to centre, u x v
HOLE_D = 2.0
GLASS = (26.7, 19.48)
GLASS_V0 = 3.93                  # the glass's top edge below the header edge
LIT = (21.74, 10.86)             # 128 x 64 at 0.1698 mm
LIT_V0 = 6.43                    # the lit area's top edge below the header edge
FLEX = (12.0, 0.7, 0.8)          # the display's flex round the far edge: width (u; 10.2 measured, 12 allowed), how far beyond
                                 # the edge (v), how far in front of the PCB (it leaves the panel's substrate ledge, behind the
                                 # cover glass's face: at most 1.45 - if it ever stood that far forward it would be 0.25 off
                                 # the wall, and it is a flexible film)
PCB_T, GLASS_T = 1.66, 1.45
JOINTS = dict(u=(-5.1, 5.1), v=(0.3, 2.7), h=2.0)      # the four solder joints on the FRONT (pins at v 1.47, 2.54 apart)
PLUGS = dict(u=(-5.1, 5.1), v=(0.3, 3.0), deep=20.0)   # the four plug-on housings at the back, from the PCB's front face
SHIFT_TOL = 0.2                  # the hole pattern against the PCB's outline (measured to about this)
# ---------------- placement in the pod (facet frame: x, along, deep)
HUD_X = 76.5
CEN_A = 16.52                    # the hole pattern's (and the board's) centre along the facet
HEADER_A = CEN_A + PCB[1] / 2    # 30.32: the header edge, at the top
SEAT = 4.2                       # the PCB's front face rests on the posts here (R3)
GLASS_A = (HEADER_A - GLASS_V0 - GLASS[1], HEADER_A - GLASS_V0)       # 6.91 .. 26.39
LIT_A = (HEADER_A - LIT_V0 - LIT[1], HEADER_A - LIT_V0)                # 13.03 .. 23.89
# ---------------- the new pod
A_LO = 1.2                       # unchanged
A_HI = 31.2
FLEN = A_HI + WALL               # 33.7
BROW_A = 38.2
CAV_X = (62.1, 90.9)
POCKET = dict(x=(HUD_X - 13.95, HUD_X + 13.95), a=(GLASS_A[0] - 0.6, GLASS_A[1] + 0.6), d=(1.0, SEAT))   # 0.6 round the glass
RELIEF = dict(x=(HUD_X - 5.7, HUD_X + 5.7), a=(GLASS_A[1], A_HI), d=(1.0, WALL + 0.5))
WIN = dict(x=(64.7, 88.3), a=(12.0, 24.93), d=(-1.0, 1.5))
CHIN_Z = 19.2                    # the window's top edge, flat (on the 0.2 grid)
POST_R, POST_D0 = 3.0, 2.0
PILOT_D0 = 1.0
OLED_PILOT = 1.3                 # M1.6x4 thread-forming (R3; drill 1.3 .. 1.4 after printing - review P)
POSTS = [(HUD_X + su * HOLES[0] / 2, CEN_A + sv * HOLES[1] / 2) for sv in (-1, 1) for su in (-1, 1)]
FILL = dict(x=(63.0, 90.0), a=(3.5, 26.5), d=(0.0, WALL))      # covers R3's window, pocket and pilots
CAP_A = (-10.5, BROW_A)
CAP_CH = 0.8
CAP_SCREWS = R3.cap_screws()     # (66.0, 33.9), (87.0, 33.9), (87.0, -5.0): unchanged
L = R3.L_REAR
FAILS = []


def expect(name, value, lo, hi, unit="mm "):
    ok = (value == value) and lo <= value <= hi
    print("  %-112s %10.4f %s  %s" % (name, value, unit, "ok" if ok else "*** FAIL ***"), flush=True)
    if not ok:
        FAILS.append(name)


def info(name, value, unit="mm ", note=""):
    print("  %-112s %10.4f %s  %s" % (name, value, unit, note), flush=True)


def vol(a, b):
    try:
        c = a & b
        return 0.0 if c is None else sum(x.volume for x in c.solids())
    except Exception:
        return float("nan")


def W(x, a, d):
    y, z = facet_pt(a, d)
    return Vector(x, y, z)


fbox, axis_cyl = R3.fbox, R3.axis_cyl


def pod_outer(flen, brow_a):
    """R3's pod outline with its top moved: the facet up to flen, the brow up to brow_a (R3.pod_outer, parametrised)"""
    A = facet_pt(0.0); B = facet_pt(flen)
    B1 = facet_pt(flen, L - R3.BROW_D); R1 = facet_pt(brow_a, L - R3.BROW_D); R2 = facet_pt(brow_a, L)
    _, zf = R3.rear_at_y(R3.POD_BACK_Y)
    pts = [A, B, B1, R1, R2, (R3.POD_BACK_Y, zf), (R3.POD_BACK_Y, SKIRT_Z - 0.5), (Y_TOPF, SKIRT_Z - 0.5)]
    prof = make_face(Plane.YZ * Polyline(*pts, pts[0]))
    pod = Pos(R3.POD_X[0], 0, 0) * extrude(prof, R3.POD_X[1] - R3.POD_X[0], dir=(1, 0, 0))
    hw, xc, pick = (R3.POD_X[1] - R3.POD_X[0]) / 2, (R3.POD_X[0] + R3.POD_X[1]) / 2, []
    for e in pod.edges():
        c = e.center(); a, d = R3.facet_ad(c.Y, c.Z)
        side = abs(abs(c.X - xc) - hw) < 0.01
        if side and abs(d) < 0.01 and 0.01 < a < flen - 0.01:
            pick.append(e)
        elif side and abs(a - flen) < 0.01 and 0.01 < d < L - R3.BROW_D - 0.01:
            pick.append(e)
        elif abs(c.X - xc) < 0.01 and abs(a - flen) < 0.01 and abs(d) < 0.01:
            pick.append(e)
    assert len(pick) == 5, "pod: expected 5 edges to chamfer, found %d" % len(pick)
    return chamfer(pick, R3.POD_C)


def chin_cut():
    """the lip over the window, below z CHIN_Z, across the window's width: its underside becomes flat (a bridge between
    the window's sides). Deep -0.6 .. 1.5: past the facet, and into the pocket (empty there), so no face is shared."""
    reg = fbox(*WIN["x"], WIN["a"][1] - 0.01, WIN["a"][1] + 4.0, -0.6, 1.5)
    below = Pos(sum(WIN["x"]) / 2, 85.0, CHIN_Z - 25.0) * Box(WIN["x"][1] - WIN["x"][0], 60.0, 50.0)
    return reg & below


def posts():
    """the four posts (r 3, deep 2.0 .. the seat); the two lower ones carried down to the tube's floor"""
    out = []
    for x, a in POSTS:
        p = axis_cyl(x, a, POST_D0, SEAT, POST_R)
        if a < CEN_A:
            p = p + fbox(x - POST_R, x + POST_R, A_LO - 0.05, a, POST_D0, SEAT)
        out.append(p)
    return out


def tools():
    """every tool solid, in the order Fusion will use them: (name, 'join' | 'cut', solid)"""
    t = [("outer", "join", pod_outer(FLEN, BROW_A) - R3.pod_outer()),
         ("tube", "cut", fbox(*CAV_X, A_LO, A_HI, WALL, L + 3.0)),
         ("fill", "join", fbox(*FILL["x"], *FILL["a"], *FILL["d"]))]
    ps = posts()
    t.append(("posts", "join", ps[0] + ps[1] + ps[2] + ps[3]))
    t.append(("pocket", "cut", fbox(*POCKET["x"], *POCKET["a"], *POCKET["d"]) + fbox(*RELIEF["x"], *RELIEF["a"], *RELIEF["d"])))
    t.append(("window", "cut", fbox(*WIN["x"], *WIN["a"], *WIN["d"])))
    t.append(("chin", "cut", chin_cut()))
    pl = [axis_cyl(x, a, PILOT_D0, SEAT + 0.1, OLED_PILOT / 2) for x, a in POSTS]
    t.append(("pilots", "cut", pl[0] + pl[1] + pl[2] + pl[3]))
    return t


def new_body(b0, tl=None):
    steps, b = {}, b0
    for nm, op, s in (tl or tools()):
        b = (b + s) if op == "join" else (b - s)
        steps[nm] = b.volume
    return b, steps


def new_cap():
    q = fbox(R3.POD_X[0], R3.POD_X[1], CAP_A[0], CAP_A[1], L, L + R3.CAP_T)
    outer = [e for e in q.edges() if abs(R3.facet_ad(e.center().Y, e.center().Z)[1] - (L + R3.CAP_T)) < 0.01]
    assert len(outer) == 4
    q = chamfer(outer, CAP_CH)
    for (sx, a) in CAP_SCREWS:
        q -= axis_cyl(sx, a, L - 1.0, L + R3.CAP_T + 1.0, CLEAR_D / 2)
        q -= axis_cyl(sx, a, L + R3.CAP_T - HEAD_DEEP, L + R3.CAP_T + 0.5, HEAD_D / 2)
    # r4's dummy fourth "bolt" at the corner with no real screw (mk1_body_r4.hud_cap, verbatim)
    D = B4.DUMMY
    sx, a = R3.HUD_X - R3.CAP_SCREW_DX, R3.CAP_SCREW_A[0]
    top = L + R3.CAP_T
    q -= axis_cyl(sx, a, top - D["ring_deep"], top + 0.5, D["ring_out"] / 2) - axis_cyl(sx, a, top - D["ring_deep"] - 0.5, top + 1.0, D["ring_in"] / 2)
    y, z = facet_pt(a, top - D["hex_deep"])
    q -= Pos(sx, y, z) * Rot(X=FACET_DEG) * extrude(RegularPolygon(D["hex_af"] / math.sqrt(3), 6), amount=D["hex_deep"] + 0.5, dir=(0, 0, 1))
    return q


def board(du=0.0, dv=0.0, grow=0.0):
    """the real module in place (header up): the PCB grown by `grow` a side; the whole board shifted du (x) / dv (along)
    against the hole pattern (the posts). Pieces as a list of (name, solid)."""
    xc, hdr = HUD_X + du, HEADER_A + dv
    far = hdr - PCB[1]
    parts = [("pcb", fbox(xc - PCB[0] / 2 - grow, xc + PCB[0] / 2 + grow, far - grow, hdr + grow, SEAT, SEAT + PCB_T)),
             ("glass", fbox(xc - GLASS[0] / 2, xc + GLASS[0] / 2, hdr - GLASS_V0 - GLASS[1], hdr - GLASS_V0, SEAT - GLASS_T, SEAT)),
             ("flex", fbox(xc - FLEX[0] / 2, xc + FLEX[0] / 2, far - grow - FLEX[1], far + 0.3, SEAT - FLEX[2], SEAT + PCB_T + 0.3)),
             ("joints", fbox(xc + JOINTS["u"][0], xc + JOINTS["u"][1], hdr - JOINTS["v"][1], hdr - JOINTS["v"][0], SEAT - JOINTS["h"], SEAT)),
             ("plugs", fbox(xc + PLUGS["u"][0], xc + PLUGS["u"][1], hdr - PLUGS["v"][1], hdr - PLUGS["v"][0], SEAT + PCB_T, SEAT + PLUGS["deep"]))]
    return parts


def load():
    sols = list(import_step(READBACK).solids())
    got = {}
    for k, v in VOLS.items():
        m = [s for s in sols if abs(s.volume - v) < 0.01]
        if len(m) != 1:
            raise RuntimeError("%s: %d solids of %.4f in %s" % (k, len(m), v, READBACK))
        got[k] = m[0]
    return got


def main(fusion=None):
    """the checks; with `fusion` (a read-back STEP of the r8 item) they run on FUSION's body and cap instead of the trial's"""
    import trimesh
    import mk1_gates as G
    import support_survey as SS
    from attach_scan import scan_attach, validate_instrument
    from mk1_body_r3 import export_clean_stl
    os.makedirs("out/mk1", exist_ok=True)
    print("MK-I r9 - the HUD pod and cap for the real OLED board: TRIAL (cloud), on %s" % READBACK)
    P = load()
    b0, cap0 = P["body"], P["cap"]

    print("\n1. THE POD AND CAP THEY START FROM ARE R3's (so R3's code is reused with new numbers)")
    probe_solid = [("facet wall below R3's window", W(76.5, 3.0, 1.2)), ("tube top wall", W(76.5, 30.0, 10.0)),
                   ("brow", W(76.5, 36.0, 30.0)), ("lower inner post, beside its pilot", W(64.5, 4.5, 3.6)),
                   ("upper handle-side post, beside its pilot", W(88.5, 25.5, 3.6)), ("below the tube's floor", W(64.82, 0.7, 3.0))]
    probe_air = [("R3's window", W(76.5, 15.0, 0.5)), ("R3's pocket", W(76.5, 15.0, 1.5)), ("the tube", W(76.5, 15.0, 10.0)),
                 ("a pilot", W(66.0, 4.5, 2.6)), ("the ridge chamfer", W(76.5, 30.5, 0.3)), ("above R3's brow", W(76.5, 37.6, 30.0))]
    bad = [n for n, p in probe_solid if not b0.is_inside(p)] + [n for n, p in probe_air if b0.is_inside(p)]
    expect("probes in the old pod (%d solid, %d air) as R3 drew it: wrong" % (len(probe_solid), len(probe_air)), len(bad), 0, 0, "   ")
    if bad:
        print("     wrong: %s" % bad)
    c0 = B4.hud_cap()
    expect("the cap in the file is r4's hud_cap() (R3's + the dummy fourth bolt): volume difference", cap0.volume - c0.volume, -0.01, 0.01, "mm3")
    bb, bc = cap0.bounding_box(), c0.bounding_box()
    expect("  ... and its box", max(abs(p - q) for p, q in zip((bb.min.X, bb.min.Y, bb.min.Z, bb.max.X, bb.max.Y, bb.max.Z), (bc.min.X, bc.min.Y, bc.min.Z, bc.max.X, bc.max.Y, bc.max.Z))), 0, 0.001)
    podbox = Pos((59.5 + 92.9) / 2, (36.7 + 100.0) / 2, (7.0 + 57.0) / 2) * Box(92.9 - 59.5, 100.0 - 36.7, 57.0 - 7.0)
    expect("R3's pod outline: the body has no material outside it (box x 59.5 .. 92.9, y 36.7 .. 100, z 7 .. 57)",
           vol(b0, podbox - R3.pod_outer()), 0, 0.01, "mm3")

    print("\n2. THE NEW BODY AND CAP")
    TL = tools()
    b1, steps = new_body(b0, TL)
    expect("body: one valid solid", (1.0 if b1.is_valid else 0.0) * len(b1.solids()), 1, 1, "   ")
    keys = list(steps)
    print("  step volumes for Fusion (mm3): start %.4f, %s" % (b0.volume, ", ".join("%s %.4f" % (k, steps[k]) for k in keys)))
    print("  step changes (mm3): %s" % ", ".join("%s %+.4f" % (k, steps[k] - (steps[keys[i - 1]] if i else b0.volume)) for i, k in enumerate(keys)))
    NSOL = dict(outer=2, posts=4, pilots=4)       # the outer: the strip on top of the tube + the brow's extra 1.0
    for nm, op, s in TL:
        expect("tool '%s' (%s): valid, %d solid(s)" % (nm, op, NSOL.get(nm, 1)), (1.0 if s.is_valid else 0.0) * len(s.solids()), NSOL.get(nm, 1), NSOL.get(nm, 1), "   ")
    region = Pos(76.5, 70.0, 26.0) * Box(40.0, 80.0, 60.0)          # x 56.5 .. 96.5, y 30 .. 110, z -4 .. 56: the pod and round it
    expect("outside the pod's region the body is unchanged (volume)", abs((b1 - region).volume - (b0 - region).volume), 0, 0.01, "mm3")
    # where a tool may add or take material: inside the new pod's outline, or inside R3's cavity (its tube runs below the
    # outline's foot, z 6.5, at its lower end); the tube's cut also widens that lower end by 0.4 a side (STRIPS)
    env = pod_outer(FLEN, BROW_A) + R3.pod_cavity()
    strips = Pos(62.3, 67.5, 4.5) * Box(0.4, 15.0, 11.0) + Pos(90.7, 67.5, 4.5) * Box(0.4, 15.0, 11.0)
    for nm, op, s in TL:
        expect("  tool '%s' lies inside that region" % nm, vol(s, region) - s.volume, -0.001, 0.001, "mm3")
        if op == "join":
            expect("    ... what it adds (the tool minus the old body) lies inside the new pod's outline or R3's cavity", vol(s - b0, region - env), 0, 0.001, "mm3")
        else:
            expect("    ... what it takes (the tool and the old body) lies inside the new pod's outline or R3's cavity%s" % (" (or the 0.4 strips)" if nm == "tube" else ""),
                   vol(s & b0, region - env - strips), 0, 0.001, "mm3")
            if nm == "tube":
                info("      the tube's lower end 0.4 wider a side, where R3's tube already passes the skirt's top wall (x 62.1 .. 62.5, 90.5 .. 90.9)", vol(s & b0, strips - env), "mm3")
    c1 = new_cap()
    if fusion:
        fs = list(import_step(fusion).solids())
        fb = sorted([s for s in fs if abs(s.volume - b1.volume) < 50.0], key=lambda s: abs(s.volume - b1.volume))
        fc = sorted([s for s in fs if abs(s.volume - c1.volume) < 1.0], key=lambda s: abs(s.volume - c1.volume))
        expect("FUSION: one body near the trial's volume in %s (within 50 mm3)" % fusion, len(fb), 1, 1, "   ")
        expect("FUSION: one cap near the trial's volume (within 1 mm3)", len(fc), 1, 1, "   ")
        print("  FROM HERE ON THE CHECKS RUN ON FUSION'S BODY (%.4f mm3; the trial's %.4f) AND CAP (%.4f; the trial's %.4f)" % (fb[0].volume, b1.volume, fc[0].volume, c1.volume))
        b1, c1 = fb[0], fc[0]
        expect("body: one valid solid (Fusion's)", (1.0 if b1.is_valid else 0.0) * len(b1.solids()), 1, 1, "   ")
        expect("outside the pod's region the body is unchanged (Fusion's)", abs((b1 - region).volume - (b0 - region).volume), 0, 0.01, "mm3")
    expect("cap: one valid solid", (1.0 if c1.is_valid else 0.0) * len(c1.solids()), 1, 1, "   ")
    info("cap volume: %.4f (was %.4f)" % (c1.volume, cap0.volume), c1.volume, "mm3")
    pod_part = b1 & (Pos(76.5, 96.0, 32.25) * Box(60.0, 48.0, 49.5))      # x 46.5 .. 106.5, y 72 .. 120, z 7.5 .. 57
    expect("body: the pod is %.0f wide as before (x 60 .. 93): largest difference" % (R3.POD_X[1] - R3.POD_X[0]),
           max(abs(pod_part.bounding_box().min.X - 60.0), abs(pod_part.bounding_box().max.X - 93.0)), 0, 0.001)

    print("\n3. THE BOARD IN THE TUBE (header up; the PCB at its largest; the board up to 0.2 off the hole pattern either way)")
    ps = posts()
    b1np = b1 - (ps[0] + ps[1] + ps[2] + ps[3])            # the PCB rests on the posts: its clearance is to everything else
    worst = {}
    for du in (-SHIFT_TOL, 0.0, SHIFT_TOL):
        for dv in (-SHIFT_TOL, 0.0, SHIFT_TOL):
            for nm, s in board(du, dv, PCB_TOL):
                d = (b1np if nm == "pcb" else b1).distance_to(s) if vol(b1, s) < 1e-6 else -1.0
                worst[nm] = min(worst.get(nm, 99.0), round(d, 4))
    for nm in ("pcb", "glass", "flex", "joints", "plugs"):
        expect("  %s: nearest body wall at the worst of 9 positions (0 would be touching%s)" % (nm, "; the posts left out" if nm == "pcb" else ""), worst[nm], 0.3, 99)
    for (x, a), p in zip(POSTS, ps):
        ring_ = axis_cyl(x, a, SEAT - 0.05, SEAT, 1.4) - axis_cyl(x, a, SEAT - 0.06, SEAT + 0.01, 0.66)
        expect("  post (%.2f, along %.2f): solid under the PCB round the hole (r 0.65 .. 1.4; the M1.6 head is r 1.6)" % (x, a),
               vol(b1, ring_) / ring_.volume, 0.999, 1.001, "   ")
    slab = fbox(HUD_X - PCB[0] / 2 - PCB_TOL - SHIFT_TOL, HUD_X + PCB[0] / 2 + PCB_TOL + SHIFT_TOL,
                HEADER_A - PCB[1] - PCB_TOL - SHIFT_TOL, HEADER_A + PCB_TOL + SHIFT_TOL, SEAT - 0.05, SEAT)
    expect("  nothing but the posts within 0.05 in front of the PCB", vol(b1, slab - (ps[0] + ps[1] + ps[2] + ps[3])), 0, 0.001, "mm3")
    for x, a in POSTS:
        side = 1.0 if x < HUD_X else -1.0
        okp = (not b1.is_inside(W(x, a, 2.5))) and (not b1.is_inside(W(x, a, 1.2))) and b1.is_inside(W(x + side * 1.0, a, 2.5)) and b1.is_inside(W(x, a, 0.6))
        expect("  pilot at (%.2f, along %.2f): open on its axis at deep 1.2 and 2.5, solid 1.0 beside it and 0.4 before the face" % (x, a), 1.0 if okp else 0.0, 1, 1, "   ")
    expect("the window covers the lit area (with the 0.2 shift): margin below", (LIT_A[0] - SHIFT_TOL) - WIN["a"][0], 0.6, 99)
    expect("  ... above (the window's inner top edge, at the lip's back face)", WIN["a"][1] - (LIT_A[1] + SHIFT_TOL), 0.6, 99)
    expect("  ... across", min(HUD_X - LIT[0] / 2 - SHIFT_TOL - WIN["x"][0], WIN["x"][1] - HUD_X - LIT[0] / 2 - SHIFT_TOL), 0.6, 99)
    expect("the window's outer top edge (z %.1f on the facet) stays inside the glass's top edge (with the 0.2 shift)" % CHIN_Z,
           (GLASS_A[1] - SHIFT_TOL) - CHIN_Z / S48, 0.3, 99)
    expect("  ... and the window's lower edge inside the glass's lower edge", WIN["a"][0] - (GLASS_A[0] + SHIFT_TOL), 0.3, 99)
    expect("the glass inside its pocket, every side (glass 26.7 x 19.48, pocket 27.9 x 20.68, 0.2 shift)",
           round(min(POCKET["x"][1] - HUD_X - GLASS[0] / 2, POCKET["a"][1] - GLASS_A[1], GLASS_A[0] - POCKET["a"][0]) - SHIFT_TOL, 4), 0.4, 99)
    info("  room in front of the glass (glass face to the pocket's floor)", (SEAT - GLASS_T) - POCKET["d"][0])
    info("  room in front of the PCB at the solder joints (R3: 1.7 - the joints stand about 1.5 .. 2)", SEAT - RELIEF["d"][0])
    expect("the board's lowest point (the flex) against R3's board's lowest point (along 2.22): no lower than", (HEADER_A - PCB[1] - FLEX[1]) - 2.22, -0.35, 99)
    info("  the flex's lowest point along the facet (R3's board: 2.22)", HEADER_A - PCB[1] - FLEX[1])
    info("room behind the plugs to the rear plane (where the cap sits) for the wires' bend (R3: the same)", L - (SEAT + PLUGS["deep"]))

    print("\n4. THE POD AS BUILT (probes on the solid) AND THE CAP")
    hx = HUD_X
    expect("window open (probe through the lip, 0.2 inside its edges)", vol(b1, fbox(WIN["x"][0] + 0.2, WIN["x"][1] - 0.2, WIN["a"][0] + 0.2, WIN["a"][1] - 0.2, -1.0, 1.0)), 0, 0.001, "mm3")
    expect("lip round the window (probe 0.1 .. 0.6 beside it, deep 0.1 .. 0.9)", vol(b1, fbox(WIN["x"][0] - 0.6, WIN["x"][0] - 0.1, 14.0, 22.0, 0.1, 0.9)), 0.5 * 8 * 0.8 * 0.999, 0.5 * 8 * 0.8 * 1.001, "mm3")
    expect("glass pocket open (deep 1.05 .. 4.15)", vol(b1, fbox(POCKET["x"][0] + 0.05, POCKET["x"][1] - 0.05, POCKET["a"][0] + 0.05, POCKET["a"][1] - 0.05, 1.05, 4.15)), 0, 0.001, "mm3")
    expect("joint relief open (deep 1.05 .. 2.95)", vol(b1, fbox(RELIEF["x"][0] + 0.05, RELIEF["x"][1] - 0.05, RELIEF["a"][0] + 0.05, RELIEF["a"][1] - 0.05, 1.05, 2.95)), 0, 0.001, "mm3")
    expect("board space open (the PCB at its largest + 0.2 shift, deep 4.25 .. 5.9)",
           vol(b1, fbox(hx - 13.65 - 0.35, hx + 13.65 + 0.35, HEADER_A - 27.6 - 0.35, HEADER_A + 0.35, 4.25, 5.9)), 0, 0.001, "mm3")
    for nm, a in (("plugs on the board's upper edge", HEADER_A - 1.65), ("behind the board's lower edge", HEADER_A - PCB[1] + 1.7), ("behind the board's centre", CEN_A)):
        expect("30 mm free behind the OLED's front: " + nm, vol(b1, fbox(hx - 6, hx + 6, a - 1.5, a + 1.5, 6.0, 31.0)) + vol(c1, fbox(hx - 6, hx + 6, a - 1.5, a + 1.5, 6.0, 31.0)), 0, 0.001, "mm3")
    expect("pod side wall (probe, x 91.0 .. 92.9)", vol(b1, fbox(CAV_X[1] + 0.1, R3.POD_X[1] - 0.1, 12, 18, 10, 30)), 1.9 * 6 * 20 * 0.999, 1.9 * 6 * 20 * 1.001, "mm3")
    expect("facet skin beside the window (probe)", vol(b1, fbox(WIN["x"][0] - 1.0, WIN["x"][0] - 0.3, 14, 16, 0.2, 0.9)), 0.7 * 2 * 0.7 * 0.999, 0.7 * 2 * 0.7 * 1.001, "mm3")
    expect("tube top wall (probe)", vol(b1, fbox(hx - 5, hx + 5, A_HI + 0.2, FLEN - 0.2, 8, 20)), 10 * 2.1 * 12 * 0.999, 10 * 2.1 * 12 * 1.001, "mm3")
    expect("tube side walls (pod x 60 .. 93, cavity %.1f .. %.1f)" % CAV_X, min(CAV_X[0] - R3.POD_X[0], R3.POD_X[1] - CAV_X[1]), 2.0, 99)
    expect("  ... where the pod's 2.5 chamfer runs along their outer edge: wall (R3: 1.77)", (min(CAV_X[0] - R3.POD_X[0], R3.POD_X[1] - CAV_X[1])) / math.sqrt(2), 1.2, 99)
    expect("cap <-> body: no overlap", vol(c1, b1), 0, 0.001, "mm3")
    expect("cap covers the tube's rear opening: overlap at the sides / below / above (at least 2)",
           min(CAV_X[0] - R3.POD_X[0], R3.POD_X[1] - CAV_X[1], R3.A_CH - CAP_A[0], CAP_A[1] - A_HI), 2.0, 99)
    expect("cap's highest point below the back plate (z %.1f): the deck lies on the plate, not on the cap" % BACK_Z, BACK_Z - c1.bounding_box().max.Z, 0.3, 99)
    info("  the cap's highest point z (R3's: %.2f)" % cap0.bounding_box().max.Z, c1.bounding_box().max.Z)
    expect("cap keeps off the body's top wall (0.3 band beside it)", vol(c1, Pos((R3.POD_X[0] + 67.7) / 2, R3.PY[1] + 0.15, 17.5) * Box(67.7 - R3.POD_X[0], 0.3, 15.0)), 0, 0.001, "mm3")
    up = [(x, a) for x, a in CAP_SCREWS if a > 0]
    expect("cap: wall from an upper counterbore to the cap's upper edge, below the chamfer (review P: 0.25)", min(BROW_A - a - HEAD_D / 2 for x, a in up), 0.9, 99)
    expect("  ... at the cap's outer face, where the %.1f chamfer is (the last %.1f mm printed)" % (CAP_CH, CAP_CH), min(BROW_A - CAP_CH - a - HEAD_D / 2 for x, a in up), 0.4, 99)
    expect("brow: wall from an upper cap pilot (d %.1f) down to the tube (R3: 3.85)" % PILOT_D, min(a - PILOT_D / 2 - A_HI for x, a in up), 1.25, 99)
    expect("  ... and up to the brow's top", min(BROW_A - a - PILOT_D / 2 for x, a in up), 1.25, 99)
    for x, a in CAP_SCREWS:
        pil = axis_cyl(x, a, L - R3.CAP_PILOT_DEEP + 0.1, L - 0.1, PILOT_D / 2 - 0.05)
        expect("  cap pilot at (%.1f, along %.1f) still open (%.0f deep)" % (x, a, R3.CAP_PILOT_DEEP), vol(b1, pil), 0, 0.001, "mm3")
        wall = axis_cyl(x, a, L - R3.CAP_PILOT_DEEP + 0.5, L - 0.5, PILOT_D / 2 + 1.2) - axis_cyl(x, a, L - R3.CAP_PILOT_DEEP, L, PILOT_D / 2 + 0.05)
        expect("    ... with solid 1.15 round it", vol(b1, wall) / wall.volume, 0.999, 1.001, "   ")

    print("\n5. THE OTHER PARTS (the board at its largest, every position)")
    allb = [s for du in (-SHIFT_TOL, SHIFT_TOL) for dv in (-SHIFT_TOL, SHIFT_TOL) for _, s in board(du, dv, PCB_TOL)]
    for nm in ("front", "ring", "handle", "screen", "plate"):
        dmin = min(P[nm].distance_to(s) for s in allb)
        expect("%s <-> the real board (R3's board: %.2f)" % (nm, P[nm].distance_to(P["oled"])), dmin, 0.8, 999)
    for nm in ("front", "ring", "handle", "screen", "plate"):
        expect("%s <-> the new cap: no overlap" % nm, vol(P[nm], c1), 0, 0.001, "mm3")
        expect("%s <-> the new body's pod: no overlap" % nm, vol(P[nm], b1 & region) - vol(P[nm], b0 & region), -0.001, 0.001, "mm3")
    expect("the new cap <-> the board and its plugs: no overlap", sum(vol(c1, s) for s in allb), 0, 0.001, "mm3")
    info("the red film (reference, in R3's window at along 7.3 .. 22.7) inside the new body: hide it in Fusion (this OLED is yellow/blue)", vol(P["film"], b1), "mm3")

    print("\n6. ROUTE IN: the OLED goes straight in from the back (R3's standing check)")
    g = PCB_TOL + 0.17
    sweep = lambda d1: fbox(HUD_X - PCB[0] / 2 - g, HUD_X + PCB[0] / 2 + g, HEADER_A - PCB[1] - g - FLEX[1], HEADER_A + g, SEAT + 0.1, d1)
    expect("the board's path (PCB at its largest + 0.17 a side, and the flex) from its seat to the rear plane: body", vol(b1, sweep(L)), 0, 0.001, "mm3")
    expect("  ... and the cap off: nothing else in the tube's mouth (front, handle)", vol(P["front"], sweep(L)) + vol(P["handle"], sweep(L)), 0, 0.001, "mm3")
    gl = fbox(HUD_X - GLASS[0] / 2 - SHIFT_TOL, HUD_X + GLASS[0] / 2 + SHIFT_TOL, GLASS_A[0] - SHIFT_TOL, GLASS_A[1] + SHIFT_TOL, SEAT - GLASS_T - 0.05, L)
    expect("the glass's path (with the 0.2 shift) into its pocket", vol(b1, gl), 0, 0.001, "mm3")
    jt = fbox(HUD_X + JOINTS["u"][0] - SHIFT_TOL, HUD_X + JOINTS["u"][1] + SHIFT_TOL, HEADER_A - JOINTS["v"][1] - SHIFT_TOL, HEADER_A - JOINTS["v"][0] + SHIFT_TOL, SEAT - JOINTS["h"], L)
    expect("the solder joints' path into the relief", vol(b1, jt), 0, 0.001, "mm3")
    fx = fbox(HUD_X - FLEX[0] / 2 - SHIFT_TOL, HUD_X + FLEX[0] / 2 + SHIFT_TOL, HEADER_A - PCB[1] - FLEX[1] - PCB_TOL - SHIFT_TOL, HEADER_A - PCB[1] + 0.3 + SHIFT_TOL, SEAT - GLASS_T, L)
    expect("the flex's path (round the lower edge, in front of the PCB)", vol(b1, fx), 0, 0.001, "mm3")
    expect("and 12 mm beyond the rear plane (the bare module is 9.4 thick)", vol(b1, sweep(L + 12.0)), 0, 0.001, "mm3")
    reach = 12
    for extra in range(14, 61, 2):
        if vol(b1, sweep(L + extra)) > 0.001:
            break
        reach = extra
    info("straight approach room behind the rear plane, whole board (R3: 14)", reach, "mm ")
    for nm, a in (("header on the UPPER edge (this design)", HEADER_A - 1.65), ("header on the LOWER edge", HEADER_A - PCB[1] + 1.65)):
        r_ = 0
        for extra in range(2, 81, 2):
            if vol(b1, fbox(HUD_X - 5.3, HUD_X + 5.3, a - 1.4, a + 1.4, 6.0, L + extra)) > 0.001:
                break
            r_ = extra
        if "UPPER" in nm:
            expect("room for the plugs on the pins, %s: at least 23 (R3: 80)" % nm, r_, 23, 999, "mm ")
        else:
            info("room for the plugs on the pins, %s (R3: 20)" % nm, r_, "mm ")

    print("\n7. DRIVER: a straight 3 mm shaft + 10 mm handle on each OLED screw (cap off), a T9 driver on each cap screw")
    ok_screws = {}
    for x, a in POSTS:
        shaft = axis_cyl(x, a, 6.0, 66.0, 1.5)                      # 60 mm from the screw head
        grip = axis_cyl(x, a, 51.0, 110.0, 5.0)                     # 10 mm handle from 45 mm out
        v = sum(vol(P[k], shaft) + vol(P[k], grip) for k in ("handle", "front")) + vol(b1, shaft) + vol(b1, grip)
        nm = "%s %s screw" % ("upper" if a > CEN_A else "lower", "handle-side" if x > HUD_X else "inner")
        ok_screws[nm] = v < 0.001
        info("%s (x %.2f, along %.2f): driver path %s" % (nm, x, a, "REACHABLE" if v < 0.001 else "blocked"), v, "mm3")
    expect("both UPPER screws reachable", 1.0 if ok_screws["upper handle-side screw"] and ok_screws["upper inner screw"] else 0.0, 1, 1, "   ")
    expect("at least 3 of the 4 reachable (R3: 3 - the lower inner one is behind the body's corner)", sum(ok_screws.values()), 3, 4, "   ")
    for (sx, a) in CAP_SCREWS:
        drv = axis_cyl(sx, a, L + R3.CAP_T, L + R3.CAP_T + 120.0, 2.25)
        expect("T9 driver reaches the cap screw at (x %.1f, along %.1f)" % (sx, a), vol(drv, b1) + sum(vol(drv, P[k]) for k in ("handle", "front")), 0, 0.001, "mm3")

    print("\n8. THE HUD CAN BE SEEN (R3's views, through the new window)")
    loc = Pos(HUD_X, *facet_pt(sum(WIN["a"]) / 2)) * Rot(X=FACET_DEG)
    win = loc * Pos(0, 0, -3.0) * Rectangle(WIN["x"][1] - WIN["x"][0], WIN["a"][1] - WIN["a"][0])
    t, t2 = math.radians(10), math.radians(25)
    views = [("square-on", extrude(win, amount=-200)), ("from the front, 10 deg low", extrude(win, amount=200, dir=(0, -math.sin(t), -math.cos(t)))),
             ("from 25 deg to the right (reader in front of the screen's middle)", extrude(win, amount=250, dir=(-math.sin(t2), 0, -math.cos(t2))))]
    for nm, v in views:
        expect("view " + nm + ": nothing in the way", vol(b1, v) + vol(c1, v) + sum(vol(P[k], v) for k in ("front", "handle")), 0, 0.5, "mm3")

    print("\n9. PRINTING: the new flats on the 0.2 grid, and the gates (the body z up as it prints; the cap flat)")
    expect("the window's flat top at z %.1f on the 0.2 grid" % CHIN_Z, abs(CHIN_Z / GRID - round(CHIN_Z / GRID)), 0, 1e-9, "   ")
    bad = trimesh.boolean.union([trimesh.creation.box(bounds=[[0, 0, 0], [20, 20, 4]]), trimesh.creation.box(bounds=[[9.85, 0, 3.9], [10.15, 20, 6.1]]),
                                 trimesh.creation.box(bounds=[[0, 0, 6], [20, 20, 10]])], engine="manifold")
    assert any(3.5 < lo < 5.0 for lo, hi in G.erosion(bad, "coupon (0.3 mm band)")), "erosion instrument missed the coupon"
    validate_instrument()
    TMP = tempfile.mkdtemp(prefix="mk1_hud9_")
    res = {}
    for nm, s in (("new", b1), ("old", b0)):
        p = os.path.join(TMP, nm + ".stl"); export_clean_stl(s, p); mm = G.place(p)
        print("  %s body: watertight %s, %.1f g PETG" % (nm, mm.is_watertight, mm.volume * 1.27e-3), flush=True)
        res[nm] = (G.erosion(mm, "  %s body" % nm), scan_attach(mm, "  %s body attachment" % nm), SS.survey(p, 30.0, False))
    (e1, f1, s1), (e0, f0, s0) = res["new"], res["old"]
    expect("erosion (new body): layers that leave no printable line", len(e1), 0, 0, "   ")
    inpod = lambda k: 56 < k[3][0] < 97 and 36.7 < k[3][1] < 110
    same = lambda a, b: a[0] == b[0] and abs(a[1] - b[1]) < 0.01 and abs(a[2] - b[2]) <= max(0.2, 0.02 * a[2]) and math.hypot(a[3][0] - b[3][0], a[3][1] - b[3][1]) < 2.0
    gone = [a for a in f0 if not any(same(a, b) for b in f1)]
    new = [b for b in f1 if not any(same(a, b) for a in f0)]
    for k, tag in [(g_, "GONE") for g_ in gone] + [(n, "NEW ") for n in new]:
        print("     %s  %-6s z %6.2f  area %8.1f  at (%7.1f, %7.1f)  %s" % (tag, k[0], k[1], k[2], k[3][0], k[3][1], "pod" if inpod(k) else "ELSEWHERE"))
    expect("attachment: changes outside the pod", len([1 for k in gone + new if not inpod(k)]), 0, 0, "   ")
    expect("attachment: islands in the new body", len([1 for k in f1 if k[0] == "ISLAND"]), 0, 0, "   ")
    chin_new = [k for k in new if inpod(k) and abs(k[1] - (CHIN_Z + 0.1)) < 0.01]
    expect("  the lip over the window now starts at z %.1f as one strip (23.6 x 1.35 = 32)" % (CHIN_Z + 0.1), max([k[2] for k in chin_new] + [0]), 25, 40, "mm2")
    expect("  no line in the pod starts as a thread at R3's chin (z 16.9 .. 17.5)", len([1 for k in f1 if inpod(k) and 16.9 < k[1] < 17.5]), 0, 0, "   ")
    a0 = {round(z, 1): r for z, *r in s0}; a1 = {round(z, 1): r for z, *r in s1}
    fmt = lambda d: ", ".join("z %.1f %.1f mm2" % (z, d[z][0]) for z in sorted(d) if z > 5)
    print("  support survey above z 5 (only the bed under them): old %s\n                                                    new %s" % (fmt(a0), fmt(a1)))
    pc = os.path.join(TMP, "cap.stl"); export_clean_stl(R3.cap_for_print(c1), pc); mc = G.place(pc)
    expect("cap (flat): erosion", len(G.erosion(mc, "  cap")), 0, 0, "   ")
    expect("cap (flat): attachment lines", len(scan_attach(mc, "  cap attachment")), 0, 0, "   ")
    print("  cap: %.1f g PETG (R3's: %.1f)" % (c1.volume * 1.27e-3, cap0.volume * 1.27e-3))
    if not fusion:
        export_step(b1, "out/mk1/MK1_r9_body_hud_trial_NOT-FOR-PRINT.step")
        export_step(c1, "out/mk1/MK1_r9_hudcap_trial_NOT-FOR-PRINT.step")
        os.makedirs("out/mk1/r9_tools", exist_ok=True)
        for i, (nm, op, s) in enumerate(TL):
            export_step(s, "out/mk1/r9_tools/%d_%s_%s.step" % (i + 1, nm, op))
    return FAILS


if __name__ == "__main__":
    fails = main(sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--fusion" else None)
    print("\n%s" % ("ALL CHECKS PASS" if not fails else "FAILED: %d -> %s" % (len(fails), fails)))
    sys.exit(1 if fails else 0)
