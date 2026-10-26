"""NEXT CASE — six style mock-ups (owner, 2026-10-02: "mock a version for each").

Each one is OUR OWN design in the spirit of a kind of sci-fi equipment. No film prop is copied
and no film name, lettering or logo goes on a part. MASSING ONLY: nothing here is printable.

Common to all six, so the comparison is about style and not about the hardware:
  the C1 front frame's proven pocket and outline, the back body hugging the sandwich, the HUD
  window on the 48 deg facet at the top right, the top and left port openings, the 12 deg stand,
  and a way to hold or carry it with the LEFT hand free of the plugs.

  S1 Machine skeleton   bare-metal armour front, piston handle, one red HUD lens
  S2 Field tracker      army-green, hooded screen, chunky keys, ribbed grip with sling loops
  S3 Test machine       black + brass, CRT-style bezel, the HUD as an "eye" on bellows
  S4 Recorder box       smooth black box, bright trim, shoulder strap, lid over the HUD
  S5 Steel rack         raw-steel rack ears with forward guard handles
  S6 Worn field gear    off-white + orange, coloured light bars, a knob, kit-part blocks

Case coords: x+ = user's LEFT, y+ = top, z = 0 display back, z+ = case back, front face z = -11.6.
"""
from build123d import *
import math, os
import c1_params as C
import r3_params as R
from build_concepts import box, hexbolt, to_fusion, stand_cutter, skirt, port_cuts, armoured_front
from build_v2 import facet_plane
from build_grips import island, hud_pod, try_fillet
import build_g2l_r3 as H

D = "/home/claude/fielddeck_redo/"
OUT = D + "out/styles"
os.makedirs(OUT, exist_ok=True)
FRONT = C.FRONT
HUD_X, HUD_S = -49.0, 14.0                               # OLED centre: x, and mm up the facet

COL = dict(chrome=(0.80, 0.82, 0.86), gunmetal=(0.40, 0.42, 0.46), black=(0.155, 0.155, 0.165),
           glass=(0.06, 0.07, 0.09), red=(0.88, 0.10, 0.08), olive=(0.38, 0.42, 0.27),
           orange=(0.93, 0.47, 0.10), key=(0.80, 0.80, 0.76), brass=(0.76, 0.61, 0.30),
           silver=(0.78, 0.79, 0.80), leather=(0.40, 0.26, 0.15), steel=(0.33, 0.36, 0.40),
           rawsteel=(0.56, 0.59, 0.62), bright=(0.84, 0.85, 0.87), offwhite=(0.88, 0.88, 0.84),
           dark=(0.21, 0.22, 0.24), yellow=(0.94, 0.78, 0.14), blue=(0.14, 0.38, 0.82))
SHINY = {"chrome": 0.55, "bright": 0.5, "brass": 0.4, "silver": 0.35, "glass": 0.45, "red": 0.5,
         "gunmetal": 0.3, "rawsteel": 0.3, "steel": 0.25}

# ------------------------------------------------------------------ shared pieces
def frame_plain():
    return import_step("/mnt/user-data/outputs/C1/C1-FaceFrame.step")

def glass():
    return box(-94.7, 94.7, -60.1, 60.1, -8.6, 0.0)

def round_edges(s):
    return [e for e in s.edges() if e.geom_type in (GeomType.CIRCLE, GeomType.ELLIPSE)]

def island_faceted():
    isl = box(R.BX[0], R.BX[1], R.BY[0], R.BY[1], 0, R.BACK)
    isl = H.try_chamfer(isl, isl.edges().filter_by(Axis.Z), (8, 6))
    isl = H.try_chamfer(isl, isl.edges().group_by(Axis.Z)[-1], (6, 4))
    return isl

def back(pod=True, faceted=False, vents=False):
    b = skirt() + (island_faceted() if faceted else island())
    if pod:
        b = b + hud_pod()
    b -= port_cuts(R.BACK)
    if vents:                                            # louvre slots over the Pi's fan side
        for k in range(6):
            b -= box(-8.0, 44.0, -62.0 + 8.0 * k, -59.0 + 8.0 * k, R.BACK - 2.0, R.BACK + 1.0)
    b -= stand_cutter()
    return b

def hud_plate():
    """the OLED's glass, sitting in the pod window."""
    return facet_plane(HUD_X, HUD_S).location * Pos(0, 0, -1.5) * Box(R.OLED["apert"][0] - 0.6, R.OLED["apert"][1] - 0.6, 1.0)

def back_bolts(z=R.BACK):
    out = None
    for (x, y) in ((-24.0, -70.0), (62.0, -70.0), (-24.0, 24.0), (62.0, 24.0)):
        b = hexbolt(x, y, z - 0.3, af=5.5, h=1.5)
        out = b if out is None else out + b
    return out

def arms(x1):
    """the two flat bracket arms off the frame's left edge, flush with its face, two bolts each."""
    out = None
    for (y0, y1) in H.ARMS:
        a = box(H.ARM_X0, x1, y0, y1, H.ARM_Z[0], H.ARM_Z[1])
        a = H.try_chamfer(a, a.edges().filter_by(Axis.X), (2.0, 1.5))
        for x in (110.0, 121.0):
            a = a + hexbolt(x, (y0 + y1) / 2, H.ARM_Z[0], af=5.0, h=1.0, up=-1)
        out = a if out is None else out + a
    return out

# ------------------------------------------------------------------ S1 machine skeleton
def piston_handle():
    gx, gz = H.GRIP_X, H.GRIP_Z
    (ty0, ty1), (by0, by1) = H.ARMS
    br = arms(gx - 8.0)
    for (y0, y1) in H.ARMS:
        cap = Pos(gx, y0, gz) * H.oval(17.0, 17.0, y1 - y0)
        cap = H.try_chamfer(cap, round_edges(cap), (2.0, 1.5))
        br = br + cap
    br = br + Pos(gx, ty1 - 0.5, gz) * H.hex_y(9.0, 2.0, +1) + Pos(gx, by0 + 0.5, gz) * H.hex_y(9.0, 2.0, -1)
    barrel = Pos(gx, by1 - 2.0, gz) * H.oval(15.0, 15.0, 84.0)                  # y -70..14
    for yy in (-62.0, 6.0):                                                     # retaining rings
        barrel = barrel + Pos(gx, yy, gz) * H.oval(16.2, 16.2, 3.0)
    nut = Pos(gx, 13.0, gz) * Rot(X=-90) * extrude(RegularPolygon(18.0, 6), amount=9.0)   # y 13..22
    rod = Pos(gx, 20.0, gz) * H.oval(7.0, 7.0, 22.0)                            # y 20..42
    return br, barrel, nut, rod

def s1():
    br, barrel, nut, rod = piston_handle()
    return [("Front (armour)", armoured_front(), "chrome"),
            ("Back", back(faceted=True), "gunmetal"),
            ("Back bolts", back_bolts(), "chrome"),
            ("Screen", glass(), "glass"),
            ("HUD lens (red)", hud_plate(), "red"),
            ("Handle brackets", br, "chrome"),
            ("Handle barrel", barrel, "black"),
            ("Handle nut", nut, "chrome"),
            ("Handle rod", rod, "bright")]

# ------------------------------------------------------------------ S2 field tracker
def hood(depth=16.0, wall=6.0):
    o = box(-92 - wall, 92 + wall, -60 - wall, 60 + wall, FRONT - depth, FRONT + 1.0)
    o = try_fillet(o, o.edges().filter_by(Axis.Z), (6, 4))
    o = H.try_chamfer(o, o.edges().group_by(Axis.Z)[0], (2.0, 1.5))            # front rim
    return o - box(-92, 92, -60, 60, FRONT - depth - 1.0, FRONT + 2.0)

def keys(xs, y=-79.0, size=14.0, h=3.5):
    out = []
    for x in xs:
        k = box(x - size / 2, x + size / 2, y - size / 2, y + size / 2, FRONT - h, FRONT + 0.5)
        out.append(H.try_chamfer(k, k.edges().group_by(Axis.Z)[0], (1.2, 0.8)))
    return out

def sling_loops():
    a = box(H.GRIP_X - 11, H.GRIP_X + 11, 55.0, 67.0, H.GRIP_Z - 5, H.GRIP_Z + 5)       # on the top collar
    a = try_fillet(a, a.edges().filter_by(Axis.Z), (3, 2))
    a -= box(H.GRIP_X - 7, H.GRIP_X + 7, 59.0, 63.5, H.GRIP_Z - 6, H.GRIP_Z + 6)
    b = box(-116.0, -102.0, 42.0, 58.0, -9.6, 5.0)                                       # right edge
    b = try_fillet(b, b.edges().filter_by(Axis.Z), (3, 2))
    b -= box(-113.0, -107.5, 45.5, 54.5, -10.6, 6.0)
    return a + b

def s2():
    ks = keys((-88.0, -70.0, -52.0, -34.0))
    grip, _ = H.grip()
    return [("Front", frame_plain(), "olive"),
            ("Screen hood", hood(), "olive"),
            ("Back", back(vents=True), "olive"),
            ("Screen", glass(), "glass"),
            ("HUD glass", hud_plate(), "glass"),
            ("Key 1", ks[0], "orange"), ("Key 2", ks[1], "key"), ("Key 3", ks[2], "key"), ("Key 4", ks[3], "key"),
            ("Handle brackets", H.brackets(), "olive"),
            ("Handle grip", grip, "black"),
            ("Sling loops", sling_loops(), "black")]

# ------------------------------------------------------------------ S3 test machine
def crt_bezel(t=8.0):
    o = box(-100, 100, -68, 68, FRONT - t, FRONT + 1.0)
    o = try_fillet(o, o.edges().filter_by(Axis.Z), (10, 8))
    o = try_fillet(o, o.edges().group_by(Axis.Z)[0], (2.5, 2.0))
    cut = loft([Pos(0, 0, FRONT + 1.5) * RectangleRounded(164, 98, 14),
                Pos(0, 0, FRONT - t - 0.5) * RectangleRounded(182, 116, 22)])
    return o - cut

def bezel_screws(t=8.0):
    out = None
    for (x, y) in ((93, 60), (-93, 60), (93, -60), (-93, -60)):
        s = Pos(x, y, FRONT - t - 0.3) * Cylinder(3.0, 1.8)
        out = s if out is None else out + s
    return out

def bellows_hud():
    loc = facet_plane(HUD_X, HUD_S).location
    head = loc * Pos(0, 0, -2.5) * Box(46, 30, 5.0)
    head -= loc * Box(R.OLED["apert"][0], R.OLED["apert"][1], 12.0)
    secs = []
    for i in range(11):                                                # 5 pleats
        w, h = (44, 28) if i % 2 == 0 else (36, 20)
        secs.append(Pos(0, 0, -5.0 - 2.2 * i) * Rectangle(w, h))
    bel = loc * loft(secs, ruled=True)
    base = box(-72, -26, 46, 71, 0, 42)
    base = H.try_chamfer(base, base.edges().filter_by(Axis.X), (4.0, 3.0))
    plate = loc * Pos(0, 0, -3.5) * Box(R.OLED["apert"][0] - 0.6, R.OLED["apert"][1] - 0.6, 1.0)
    return head, bel, base, plate

def s3():
    head, bel, base, plate = bellows_hud()
    grip, _ = H.grip()
    return [("Front", frame_plain(), "black"),
            ("Screen bezel", crt_bezel(), "dark"),
            ("Bezel screws", bezel_screws(), "brass"),
            ("Back", back(pod=False), "black"),
            ("Back bolts", back_bolts(), "brass"),
            ("Screen", glass(), "glass"),
            ("HUD head", head, "brass"),
            ("HUD bellows", bel, "dark"),
            ("HUD base", base, "black"),
            ("HUD glass", plate, "glass"),
            ("Handle brackets", H.brackets(), "brass"),
            ("Handle grip", grip, "black")]

# ------------------------------------------------------------------ S4 recorder box
def chin_band():
    p = box(-96, 96, -88, -68, FRONT - 1.2, FRONT + 0.5)
    return try_fillet(p, p.edges().filter_by(Axis.Z), (4, 3))

def strap_lugs():
    out = None
    for sx in (1, -1):
        x0, x1 = (102.0, 114.0) if sx > 0 else (-114.0, -102.0)
        l = box(x0, x1, 42, 60, -13, 13)
        l = try_fillet(l, l.edges().filter_by(Axis.Y), (2.5, 2))
        l -= box(min(sx * 105.0, sx * 111.0), max(sx * 105.0, sx * 111.0), 41, 61, -11, 11)
        out = l if out is None else out + l
    return out

def strap():
    with BuildSketch() as s:
        Ellipse(109, 91)
        Ellipse(107, 89, mode=Mode.SUBTRACT)
    band = Pos(0, 51, -10) * extrude(s.sketch, amount=20)
    return band & box(-150, 150, 51, 200, -12, 12)

def hud_lid():
    lid = Pos(HUD_X, 94.0, 25.0) * Rot(X=25) * box(-23, 23, 0, 34, -1.2, 1.3)
    hinge = Pos(HUD_X, 94.0, 25.0) * Rot(Y=90) * Cylinder(2.6, 46)
    return lid + hinge

def s4():
    return [("Front", frame_plain(), "black"),
            ("Chin trim", chin_band(), "silver"),
            ("Back", back(), "black"),
            ("Screen", glass(), "glass"),
            ("HUD glass", hud_plate(), "glass"),
            ("HUD lid", hud_lid(), "silver"),
            ("Strap lugs", strap_lugs(), "silver"),
            ("Strap", strap(), "leather")]

# ------------------------------------------------------------------ S5 steel rack
EAR_X, HANDLE_STAND, HANDLE_R = 116.0, 36.0, 6.0
HANDLE_Y = (-62.0, 50.0)

def rack_ear(sx):
    x0, x1 = (103.0, 128.0) if sx > 0 else (-128.0, -103.0)
    e = box(x0, x1, -84, 64, FRONT, FRONT + 4.0)
    e = try_fillet(e, e.edges().filter_by(Axis.Z), (3, 2))
    for y in (-78.0, -6.0, 60.0):
        e -= box(sx * EAR_X - 4, sx * EAR_X + 4, y - 2.5, y + 2.5, FRONT - 1, FRONT + 5)
    return e

def rack_handle(sx):
    xc, zb, r = sx * EAR_X, FRONT - HANDLE_STAND, HANDLE_R
    h = Pos(xc, sum(HANDLE_Y) / 2, zb) * Rot(X=90) * Cylinder(r, HANDLE_Y[1] - HANDLE_Y[0])
    for y in HANDLE_Y:
        h = h + Pos(xc, y, (FRONT + 1.0 + zb) / 2) * Cylinder(r, FRONT + 1.0 - zb)
        h = h + Pos(xc, y, zb) * Sphere(r + 0.5)
    return h

def rack_hand():
    r = HANDLE_R
    ring = Cylinder(r + H.FINGER, HANDLE_Y[1] - HANDLE_Y[0] - 2 * r) - Cylinder(r, HANDLE_Y[1] - HANDLE_Y[0])
    return Pos(EAR_X, sum(HANDLE_Y) / 2, FRONT - HANDLE_STAND) * Rot(X=90) * ring

def s5():
    return [("Front", frame_plain(), "steel"),
            ("Back", back(faceted=True), "steel"),
            ("Back bolts", back_bolts(), "rawsteel"),
            ("Screen", glass(), "glass"),
            ("HUD glass", hud_plate(), "glass"),
            ("Rack ear left", rack_ear(+1), "rawsteel"),
            ("Rack ear right", rack_ear(-1), "rawsteel"),
            ("Guard handle left", rack_handle(+1), "bright"),
            ("Guard handle right", rack_handle(-1), "bright")]

# ------------------------------------------------------------------ S6 worn field gear
def chin_panel():
    p = box(-98, -8, -88, -66, FRONT - 0.8, FRONT + 0.5)
    return try_fillet(p, p.edges().filter_by(Axis.Z), (3, 2))

def knob():
    k = Pos(-86, -77, FRONT - 0.8 - 4.5) * Cylinder(8.0, 9.0)
    k = H.try_chamfer(k, k.edges().group_by(Axis.Z)[0], (1.5, 1.0))
    return k + Pos(-86, -71.5, FRONT - 0.8 - 9.3) * Box(1.6, 5.0, 1.0)             # index mark

def light_bar(x):
    b = box(x - 7, x + 7, -80.5, -73.5, FRONT - 0.8 - 2.0, FRONT - 0.5)
    return H.try_chamfer(b, b.edges().group_by(Axis.Z)[0], (0.8, 0.5))

def stripe():
    return box(93.5, 102.5, -56, 56, FRONT - 0.8, FRONT + 0.5)

def kit_blocks():
    z = R.BACK
    fins = box(-22, 18, -58, -28, z - 0.5, z + 3.0)
    for k in range(7):
        fins = fins + box(-22, 18, -57.0 + 4.2 * k, -55.0 + 4.2 * k, z + 2.5, z + 9.0)
    cans = None
    for x in (34.0, 50.0):
        c = Pos(x, -43, z + 5.5) * Rot(X=90) * Cylinder(6.0, 28.0)
        cans = c if cans is None else cans + c
    cans = cans + box(26, 58, -31, -25, z - 0.5, z + 8.0) + box(26, 58, -61, -55, z - 0.5, z + 8.0)
    return fins, cans

def s6():
    fins, cans = kit_blocks()
    grip, _ = H.grip()
    return [("Front", frame_plain(), "offwhite"),
            ("Back", back(), "offwhite"),
            ("Screen", glass(), "glass"),
            ("HUD glass", hud_plate(), "glass"),
            ("Chin panel", chin_panel(), "dark"),
            ("Knob", knob(), "black"),
            ("Light bar red", light_bar(-62.0), "red"),
            ("Light bar yellow", light_bar(-44.0), "yellow"),
            ("Light bar blue", light_bar(-26.0), "blue"),
            ("Side stripe", stripe(), "orange"),
            ("Kit block fins", fins, "dark"),
            ("Kit block cans", cans, "dark"),
            ("Handle brackets", H.brackets(), "orange"),
            ("Handle grip", grip, "dark")]

STYLES = [("S1", "Machine skeleton", s1), ("S2", "Field tracker", s2), ("S3", "Test machine", s3),
          ("S4", "Recorder box", s4), ("S5", "Steel rack", s5), ("S6", "Worn field gear", s6)]

# ------------------------------------------------------------------ checks
SIDE_ZONE = box(R.ETH_FACE_X, 200.0, -26.0, 34.1, 11.0, 36.0)          # plugs + cables, left side
TOP_ZONE = box(R.TOP_WIN["x"][0], R.TOP_WIN["x"][1], R.BY[1], 130.0, R.SKIRT_Z, R.TOP_WIN["z_top"])
BASE_LABELS = ("Front", "Front (armour)", "Back", "Screen")

def hud_sight():
    """two views of the OLED window that must stay open: square-on, and from the front 10 deg low."""
    loc = facet_plane(HUD_X, HUD_S).location
    win = loc * Pos(0, 0, 3.0) * Rectangle(R.OLED["apert"][0], R.OLED["apert"][1])
    a = extrude(win, amount=200)
    t = math.radians(10)
    b = extrude(win, amount=200, dir=(0, -math.sin(t), -math.cos(t)))
    return a, b

def vol(a, b):
    try:
        i = a & b                                        # None when they do not touch
    except Exception:
        return float("nan")
    return 0.0 if i is None else i.volume

def check(code, parts):
    ok = True
    sa, sb = hud_sight()
    cutter = stand_cutter()
    for label, s, _ in parts:
        valid = s.is_valid
        row = [label, "valid" if valid else "INVALID", "solids %d" % len(s.solids())]
        ok &= valid
        if label in BASE_LABELS:
            if label.startswith("Front"):
                v = vol(s, sb)
                row.append("HUD view from front: %.1f" % v); ok &= v < 0.5
            print("   %-22s %s" % (row[0], "  ".join(row[1:])))
            continue
        hud_part = label.startswith("HUD")
        vals = dict(side=vol(s, SIDE_ZONE), top=vol(s, TOP_ZONE), stand=vol(s, cutter),
                    hudA=0.0 if hud_part else vol(s, sa), hudB=0.0 if hud_part else vol(s, sb))
        bad = [k for k, v in vals.items() if not (v < 0.5)]
        ok &= not bad
        print("   %-22s %s  %s" % (label, "  ".join(row[1:]), "OK" if not bad else "CLASH " + str({k: round(vals[k], 1) for k in bad})))
    return ok

if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or [c for c, _, _ in STYLES]
    case = back()
    front = frame_plain()
    for code, name, fn in STYLES:
        if code not in only:
            continue
        print(code, name)
        parts = fn()
        ok = check(code, parts)
        if code == "S5":                                 # the left guard handle is the grip
            hd = rack_hand()
            v = vol(hd, front) + vol(hd, case) + vol(hd, SIDE_ZONE) + sum(vol(hd, s) for l, s, _ in parts if l.startswith("Rack ear"))
            print("   hand round the left guard handle vs case / ear / plugs: %.1f (must be 0)" % v); ok &= v < 0.5
        bb = Compound(children=[s for _, s, _ in parts]).bounding_box()
        print("   size x %.0f..%.0f  y %.0f..%.0f  z %.0f..%.0f   %s" % (bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z, "ALL OK" if ok else "*** PROBLEMS ***"))
        kids = []
        for label, s, col in parts:
            k = to_fusion(s); k.label = label; k.color = Color(*COL[col])
            kids.append(k)
        export_step(Compound(label=f"{code} - {name}", children=kids), f"{OUT}/{code}_{name.replace(' ', '_')}_r1.step")
    print("done")
