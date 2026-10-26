"""NEXT CASE v2 (2026-10-01) — owner feedback on concepts v1:
  * the back already fits the sandwich: keep that envelope;
  * the big 'grip box' is too much: a small curve you can grip, merging into the back body;
  * the HUD slot looks small and faces straight up: angle it so it reads from the front;
  * the stuck-on decoration looks superficial: v2 is form only, artwork comes later;
  * the power switch got buried: its position must be MEASURED before any opening is drawn
    (the recorded x = 23.7 is suspect — see CLAUDE.md / plan M1). No switch opening in v2.

Case coords: x+ -> ports / user's LEFT, y+ -> top, z=0 display back, z+ -> case back.
Grip side = user's RIGHT = x < 0.  Export rotated for Fusion: (X, Y, Z) = (-x, z, y).
"""
from build123d import *
import math, os
import c1_params as C
import r3_params as R
from build_concepts import box, stand_cutter, safe_fillet, skirt, port_cuts, armoured_front, to_fusion

OUT = "/home/claude/fielddeck_redo/out/v2"
os.makedirs(OUT, exist_ok=True)

BACK = R.BACK                    # 56.5: stack 46 + foam + panel, as R3
X_ISL = R.BX[0]                  # -34.7: island's grip-side wall
GRIP_EDGE = -C.X_OUT             # plan runs to the outline; the shoulder dives into the skirt at x~-100
AX = 66.0                        # elliptic shoulder: half-width in x ...
AZ = BACK                        # ... and height, so it lands tangent on the island's back
FACET_DEG = R.FACET_DEG          # 48 deg from the display plane (prints clean mouth-down)
TOP_GRIP = 92.0                  # the grip side rises past the frame top to carry the HUD facet
STEP_X = -22.0                   # grip side / island-top boundary (top ports start at x -20).
                                 # At -26 the R9 plan corner ended 0.3 mm from the shoulder's tangent
                                 # line and the sliver edge blocked every fillet on the back face.

def shoulder_region():
    """everything under the back surface: elliptic shoulder on the grip side, flat island back."""
    with BuildSketch(Plane.XZ) as s:          # sketch x = world x, sketch y = world z
        Ellipse(AX, AZ)
    # one-sided extrusion: 'both=True' leaves a seam edge across the shoulder at y=0 that
    # no fillet can take
    ell = Pos(X_ISL, 250, 0) * extrude(s.sketch, amount=500)
    flat = box(X_ISL, 200, -250, 250, -20, BACK)
    return ell + flat

def plan():
    pts = [(GRIP_EDGE, -86), (R.BX[1], -86), (R.BX[1], R.BY[1]), (STEP_X, R.BY[1]),
           (STEP_X, TOP_GRIP), (GRIP_EDGE, TOP_GRIP)]
    with BuildSketch() as sk:
        Polygon(*pts, align=None)
        fillet(sk.vertices(), radius=8)
    return extrude(sk.sketch, amount=90)

def facet_cutter():
    # keep z >= (y - 71.5) * tan(48): the facet starts at the frame's top-back edge and leans back
    t = math.radians(FACET_DEG)
    return Pos(0, C.Y_TOPF, 0) * Rot(X=FACET_DEG) * Pos(0, 150, -150) * Box(600, 300, 300)

def facet_plane(x_c, s_along):
    """plane on the facet: origin s_along mm up the slope from the frame edge, at x_c."""
    t = math.radians(FACET_DEG)
    y = C.Y_TOPF + s_along * math.cos(t)
    z = s_along * math.sin(t)
    n = Vector(0, math.sin(t), -math.cos(t))          # outward: up and toward the viewer
    return Plane(origin=(x_c, y, z), x_dir=(1, 0, 0), z_dir=n)

def back_v2():
    body = plan() & shoulder_region()
    body -= facet_cutter()
    def vertical_line(e):
        return e.geom_type == GeomType.LINE and abs(e.tangent_at(0.5).Z) > 0.99
    def tangent_seam(e):          # where the shoulder lands tangent on the flat back
        c = e.center()
        return e.geom_type == GeomType.LINE and abs(c.X - X_ISL) < 0.2 and abs(c.Z - BACK) < 0.2
    rim = [e for e in body.edges() if e.center().Z > 9 and not vertical_line(e) and not tangent_seam(e)]
    for r in (8, 6, 5, 4, 3):
        try:
            body = fillet(rim, r); print("  v2 rim fillet r =", r); break
        except Exception:
            print("  v2 rim fillet failed at r =", r)
    body = skirt() + body
    body -= port_cuts(BACK)
    # HUD: the 0.96" OLED behind a window on the 48 deg facet, inside a raised bezel
    hx = -49.0                                  # OLED centre in x (R3 kept it at -48)
    fp = facet_plane(hx, 14.0)
    bezel = fp * Pos(0, 0, 0.75) * Box(40, 24, 3.0)   # s 2..26: clear of z=0 and of the rim fillet
    body = body + bezel
    body -= fp * Pos(0, 0, 0.5) * Box(R.OLED["apert"][0], R.OLED["apert"][1], 8.0)   # 23.6 x 15.8 window
    body -= stand_cutter()
    return body

if __name__ == "__main__":
    b = back_v2()
    bb = b.bounding_box()
    print("v2 back valid", b.is_valid, "vol", round(b.volume / 1000, 1), "cm3",
          "bbox", [round(v, 1) for v in (bb.min.X, bb.min.Y, bb.min.Z, bb.max.X, bb.max.Y, bb.max.Z)])
    # checks against the sandwich and the grip side
    stack = box(R.STACK["x"][0], R.STACK["x"][1], R.STACK["y"][0], R.STACK["y"][1], 0, R.STACK["z"][1])
    print("stack inside the envelope:", round((stack - b).volume, 1), "mm3 of stack NOT covered (expect >0: the stack sits in the solid massing)")
    gr = (b & box(-110, -40, -95, 100, 0, 80)).volume
    pr = (b & box(40, 110, -95, 100, 0, 80)).volume
    print("grip side x<-40:", round(gr / 1000, 1), "cm3   port side x>40:", round(pr / 1000, 1), "cm3")
    export_step(to_fusion(b), f"{OUT}/v2_back.step")
    print("exported", os.listdir(OUT))
