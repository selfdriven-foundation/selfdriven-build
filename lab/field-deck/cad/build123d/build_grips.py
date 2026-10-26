"""NEXT CASE — grip options round 3 (2026-10-01). Owner: neither v2 grip looks good; more options.

Every option shares one base: the armoured front, the back body hugging the sandwich (the part
the owner liked), and a small HUD pod at the top right with its window on a 48 deg facet.
Only the grip changes:
  G0  no grip — carry it by the edges
  G1  hand strap across the back of the right side (webbing through two printed lugs)
  G2  side handle, outboard of the right edge (a separate part, screwed on)
  G3  top carry handle (a separate part, screwed on)
  G4  slim rounded lip along the right edge
Case coords: x+ = ports = user's LEFT; grip side = user's RIGHT = x < 0.
"""
from build123d import *
import math, os
import c1_params as C
import r3_params as R
from build_concepts import box, stand_cutter, skirt, port_cuts, hexbolt, to_fusion
from build_v2 import facet_cutter, facet_plane

OUT = "/home/claude/fielddeck_redo/out/grips"
os.makedirs(OUT, exist_ok=True)
BACK = R.BACK

def try_fillet(shape, edges, radii):
    for r in radii:
        try:
            return fillet(edges, r)
        except Exception:
            pass
    return shape

def island():
    isl = box(R.BX[0], R.BX[1], R.BY[0], R.BY[1], 0, BACK)
    isl = try_fillet(isl, isl.edges().filter_by(Axis.Z), (8, 6))
    isl = try_fillet(isl, isl.edges().group_by(Axis.Z)[-1], (10, 8, 6))
    return isl

def hud_pod():
    pod = box(-70, -28, 56, 94, 0, 36)
    pod = try_fillet(pod, pod.edges().filter_by(Axis.Z), (6, 4))
    pod = try_fillet(pod, pod.edges().group_by(Axis.Z)[-1], (6, 4))
    pod -= facet_cutter()
    fp = facet_plane(-49.0, 14.0)
    pod = pod + fp * Pos(0, 0, 0.75) * Box(38, 24, 3.0)
    pod -= fp * Pos(0, 0, 0.5) * Box(R.OLED["apert"][0], R.OLED["apert"][1], 8.0)
    return pod

def base():
    b = skirt() + island() + hud_pod()
    b -= port_cuts(BACK)
    return b

def g1_strap():
    """webbing strap: two lugs on the skirt, a 30 mm band bowed 18 mm off the lugs."""
    parts = []
    for (y0, y1) in ((-80, -66), (44, 58)):
        lug = box(-90, -48, y0, y1, 0, 14)
        lug = try_fillet(lug, lug.edges().group_by(Axis.Z)[-1], (3, 2))
        lug -= box(-85, -53, (y0 + y1) / 2 - 1.8, (y0 + y1) / 2 + 1.8, 3, 11)     # webbing slot
        parts.append(lug)
    yc, zc, Rr = -11.0, -84.4, 112.4
    band = Pos(-69, yc, zc) * Rot(Y=90) * (Cylinder(Rr + 1.5, 30) - Cylinder(Rr - 1.5, 32))
    band = band & box(-90, -48, -73, 51, 9, 60)
    return parts, band

def g2_side_handle():
    arms = []
    for yc in (-50.0, 50.0):
        a = box(-128, -100, yc - 8, yc + 8, 0, 14)
        a = try_fillet(a, a.edges().filter_by(Axis.Y), (5, 3))
        arms.append(a)
    bar = Pos(-122, 0, 7) * Rot(X=90) * Cylinder(10.0, 116)
    bar = try_fillet(bar, bar.edges(), (4, 2))
    h = arms[0] + arms[1] + bar
    for yc in (-50.0, 50.0):
        for x in (-113.0, -106.0):
            h = h + hexbolt(x, yc, 14.0, af=5.0, h=1.2)
    return h

def g3_top_handle():
    posts = []
    for (x0, x1) in ((-100, -84), (84, 100)):
        p = box(x0, x1, 62, 102, 0, 20)
        p = try_fillet(p, p.edges().filter_by(Axis.Y), (5, 3))
        posts.append(p)
    bar = Pos(0, 104, 10) * Rot(Y=90) * Cylinder(9.0, 200)
    h = posts[0] + posts[1] + bar
    for (x0, x1) in ((-100, -84), (84, 100)):
        h = h + hexbolt((x0 + x1) / 2, 70, 20.0, af=5.0, h=1.2)
    return h

def g4_lip():
    # rail sits 1 mm above the bed and sinks 6 mm into the skirt: no tangent cut at z=0
    zc = 11.0
    lip = Pos(-93, -9, zc) * Rot(X=90) * Cylinder(10.0, 134)
    caps = [Pos(-93, y, zc) * Sphere(10.0) for y in (-76.0, 58.0)]
    return lip + caps[0] + caps[1]

def build(name, extra):
    b = base()
    for e in extra:
        b = b + e
    b -= stand_cutter()
    print(name, "valid", b.is_valid, "vol", round(b.volume / 1000, 1), "cm3")
    return b

if __name__ == "__main__":
    out = {}
    out["G0_none"] = build("G0", [])
    lugs, band = g1_strap()
    out["G1_strap"] = build("G1", lugs)
    out["G1_strapband"] = band                          # the webbing, kept as its own body
    print("G1 band vol", round(band.volume / 1000, 1))
    out["G2_sidehandle"] = build("G2", [])
    out["G2_handle"] = g2_side_handle()
    out["G3_tophandle"] = build("G3", [])
    out["G3_handle"] = g3_top_handle()
    out["G4_lip"] = build("G4", [g4_lip()])
    for k, s in out.items():
        export_step(to_fusion(s), f"{OUT}/{k}_r1.step")
    print(sorted(os.listdir(OUT)))
