"""FIELD DECK R3 — two-piece back case.

  R3-Shell      skirt + hugging body + HUD pod, OPEN at the back (z=54).
                Prints MOUTH-DOWN (z=0 on the plate): every wall rises, the only
                ceiling is the 2.5 skirt roof over a 4.5 mm cavity that is open to
                the plate -> ~17 g of short support instead of 134 g.
  R3-BackPanel  flat lid, z 51.5..54, 6x M3 into printed bosses. Prints flat, no support.
"""
from build123d import *
import math
from r3_params import *


def rrect(x0, x1, y0, y1, r):
    s = Rectangle(x1 - x0, y1 - y0)
    s = fillet(s.vertices(), max(r, 0.2))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, 0) * s


def stand_cutter(offset=0.0):
    """removes everything below y = Y_BOT + offset + tan(STAND)*(z-FRONT)"""
    return Pos(0, Y_BOT + offset, FRONT) * Rot(X=-STAND_DEG) * Pos(0, -250, 0) * Box(600, 500, 900)


# ---------------------------------------------------------------- pod geometry
_c, _s = math.cos(math.radians(FACET_DEG)), math.sin(math.radians(FACET_DEG))
FDIR = (_c, _s)                       # along the facet, lower -> upper  (y, z)
FIN  = (-_s, _c)                      # perpendicular, INTO the pod       (y, z)


def facet_pt(along, deep=0.0):
    """point on/behind the facet: `along` mm up the slope, `deep` mm perpendicular in"""
    y = FACET_A[0] + FDIR[0] * along + FIN[0] * deep
    z = FACET_A[1] + FDIR[1] * along + FIN[1] * deep
    return (y, z)


def pod_outer():
    """closed (y,z) polygon of the pod: facet in front, parallel back face, sitting
    on the skirt roof.  Deliberately NOT an offset of the cavity - offsetting this
    polygon self-intersects near the facet's lower edge."""
    A  = facet_pt(0.0, 0.0)
    B  = facet_pt(FACET_LEN, 0.0)
    Bb = facet_pt(FACET_LEN, POD_BACK_T)
    Ab = facet_pt(0.0, POD_BACK_T)
    pts = [A, B, Bb, Ab, (Ab[0], SKIRT_Z), (Y_TOPF, SKIRT_Z)]
    prof = make_face(Plane.YZ * Polyline(*pts, pts[0]))
    return Pos(POD_X[0], 0, 0) * extrude(prof, POD_X[1] - POD_X[0])


def pod_cavity():
    """a rectangle in FACET coordinates, so the walls are a true perpendicular 2.5"""
    # the OLED board is 25.56 along the slope, centred at FACET_MID -> it spans
    # 2.22..27.78. A cavity of WALL..FACET_LEN-WALL (2.5..27.5) clipped BOTH ends of
    # the board by 0.28 mm. Open the cavity past the board and let the outer skin
    # carry the ends instead.
    lo, hi = 1.2, FACET_LEN - 1.2
    fc = [(lo, WALL), (hi, WALL), (hi, POD_BACK_T - WALL), (lo, POD_BACK_T - WALL)]
    pts = [facet_pt(a, d) for (a, d) in fc]
    prof = make_face(Plane.YZ * Polyline(*pts, pts[0]))
    return Pos(POD_X[0] + WALL, 0, 0) * extrude(prof, POD_X[1] - POD_X[0] - 2*WALL)


def edge_wedge_xz(x_in, x_out, z_edge, up, y0, y1):
    """A TRUE 45 deg chamfer on a window edge in a +x wall: one sloped face, nothing
    else. A rotated Box has four 45 deg faces - its far corner cuts back into the wall
    and leaves a sub-extrusion feather (reviewer round 2 found 26 mm2 of it)."""
    ov, eps = 3.0, 0.02      # eps keeps the wedge's faces off the window cut's faces
    zt = z_edge + (1 if up else -1) * (abs(x_out - x_in) + ov)
    z0 = z_edge - (1 if up else -1) * eps
    prof = make_face(Plane.XZ * Polyline((x_in - eps, z0), (x_out + ov, z0), (x_out + ov, zt),
                                         (x_in - eps, z0)))
    return Pos(0, y1 + 2.0, 0) * extrude(prof, (y1 - y0) + 4.0)


def edge_wedge_yz(y_in, y_out, z_edge, up, x0, x1):
    """same, for a window edge in a +y wall"""
    ov, eps = 3.0, 0.02
    zt = z_edge + (1 if up else -1) * (abs(y_out - y_in) + ov)
    z0 = z_edge - (1 if up else -1) * eps
    prof = make_face(Plane.YZ * Polyline((y_in - eps, z0), (y_out + ov, z0), (y_out + ov, zt),
                                         (y_in - eps, z0)))
    return Pos(x0 - 2.0, 0, 0) * extrude(prof, (x1 - x0) + 4.0)


def on_facet(along, obj):
    """place obj on the facet at OLED["x"]; local +z points INTO the pod"""
    y, z = facet_pt(along)
    return Pos(OLED["x"], y, z) * Rot(X=FACET_DEG) * obj


# ---------------------------------------------------------------- the shell
def shell():
    # ---- outer solid ----
    p = extrude(rrect(-X_OUT, X_OUT, Y_BOT, Y_TOPF, R_OUT), SKIRT_Z)                 # skirt
    p += Pos(0, 0, SKIRT_Z) * extrude(rrect(*BX, *BY, 6.0), BACK - SKIRT_Z)          # body
    p += pod_outer()                                                                 # HUD pod
    # towers over the frame's four M3 bosses (which are SOLID to z=18)
    for sgn in (1, -1):
        for yc in FRAME_BOSS["ys"]:
            p += Pos(sgn*(93.0+X_OUT)/2, yc, (SKIRT_Z+21.0)/2) * Box(X_OUT-93.0, 20.0, 21.0-SKIRT_Z)

    # ---- interior ----
    inner = extrude(rrect(-X_OUT+WALL, X_OUT-WALL, Y_BOT+WALL, Y_TOPF-WALL, SKIRT_CAV_R), CAV_Z+2)
    inner = Pos(0, 0, -2) * inner                                                    # open at z=0
    inner += Pos(0, 0, CAV_Z) * extrude(rrect(BX[0]+WALL, BX[1]-WALL, BY[0]+WALL, BY[1]-WALL, BODY_CAV_R),
                                        BACK - CAV_Z + 1)                            # body bore, open at z=54
    inner += pod_cavity()                                                            # pod cavity
    inner += Pos((POD_X[0]+POD_X[1])/2, (60.0+70.5)/2, (3.0+11.0)/2) * \
             Box(POD_X[1]-POD_X[0]-2*WALL, 10.5, 8.0)                                # wire channel:
                                                                                     # links pod cavity
                                                                                     # to skirt cavity
    # tower pockets, cut THROUGH the tower roof (z 0..22, tower tops at 21).
    # As a blind pocket 6 x 13 x 19 it has a flat ceiling, so the slicer packs it solid
    # and you get four 19 mm plugs to dig out - the fit coupon proved exactly that.
    # Open at the top there is no ceiling, so no support is generated at all, and
    # anything that does end up in there pushes straight out. Structurally free: the
    # screw bears on the OUTER wall (x 101.5..104), which is untouched.
    for sgn in (1, -1):
        for yc in FRAME_BOSS["ys"]:
            inner += Pos(sgn*(95.5+101.5)/2, yc, 22.0/2) * Box(101.5-95.5, 13.0, 22.0)
    # LEAD-IN RELIEF. On C1 the shell met the frame's ridge in the LAST layers printed.
    # R3 prints mouth-down, so the whole registration interface (ridge 0.31, tower pocket
    # 0.30) is now in the FIRST layers, where elephant's foot bulges walls inward by
    # 0.1-0.3 and would bind. Open everything below z=0.8 by 0.6 mm all round: a clean
    # step, not a chamfer, so it prints without feathering, and the real fit starts at
    # z=0.8 - clear of the squashed layers.
    RELIEF, RZ = 0.6, 0.8
    inner += Pos(0, 0, -2) * extrude(rrect(-X_OUT+WALL-RELIEF, X_OUT-WALL+RELIEF,
                                           Y_BOT+WALL-RELIEF, Y_TOPF-WALL+RELIEF,
                                           SKIRT_CAV_R), 2 + RZ)
    for sgn in (1, -1):
        for yc in FRAME_BOSS["ys"]:
            inner += Pos(sgn*(95.5+101.5)/2, yc, (-2+RZ)/2) * \
                     Box(101.5-95.5+2*RELIEF, 13.0+2*RELIEF, 2+RZ)
    # the 12 deg stand bevel eats the body's bottom-back wall: a flat inner face at
    # BY[0]+WALL left 0.01 mm of wall at z=51.5. Make the INNER bottom follow the
    # bevel instead, so the wall is a constant 2.5 perpendicular all the way up.
    inner -= stand_cutter(WALL / math.cos(math.radians(STAND_DEG)))
    p -= inner

    # ---- back-panel rebate + bosses ----
    rebate = Pos(0, 0, PANEL_Z[0]) * extrude(
        rrect(BX[0]+PANEL_INSET, BX[1]-PANEL_INSET, BY[0]+PANEL_INSET, BY[1]-PANEL_INSET, 5.0),
        PANEL_T + 1)
    rebate -= stand_cutter(PANEL_INSET / math.cos(math.radians(STAND_DEG)))   # keep a 1 mm
    p -= rebate                                                               # lip on the bevel
    for (sx, sy) in PANEL_SCREWS:
        p += Pos(sx, sy, (BOSS_Z[0]+BOSS_Z[1])/2) * Cylinder(BOSS_D/2, BOSS_Z[1]-BOSS_Z[0])
    for (sx, sy) in PANEL_SCREWS:
        p -= Pos(sx, sy, BOSS_Z[1]-BOSS_PILOT_DEEP/2+0.01) * Cylinder(PILOT_D/2, BOSS_PILOT_DEEP)

    # ---- openings ----
    # Eth / USB through the +x body wall (ports MEASURED at z 15..32)
    p -= Pos(BX[1], (SIDE_WIN["y"][0]+SIDE_WIN["y"][1])/2, (SIDE_WIN["z"][0]+SIDE_WIN["z"][1])/2) * \
         Box(10, SIDE_WIN["y"][1]-SIDE_WIN["y"][0], SIDE_WIN["z"][1]-SIDE_WIN["z"][0])
    # 45 deg chamfer on the window's upper z edge: printed mouth-down that edge is a
    # 60 mm bridge (attachment gate flagged 148 mm2 at z=36). Chamfering makes it
    # self-supporting, and it also opens the view into the ports.
    for ze, up in ((SIDE_WIN["z"][1], True), (SIDE_WIN["z"][0], False)):
        p -= edge_wedge_xz(BX[1]-WALL, BX[1], ze, up, SIDE_WIN["y"][0], SIDE_WIN["y"][1])
    # top ports: notch the top wall, stopping at z=44 so the panel rebate survives
    p -= Pos((TOP_WIN["x"][0]+TOP_WIN["x"][1])/2, BY[1], (CAV_Z+TOP_WIN["z_top"])/2) * \
         Box(TOP_WIN["x"][1]-TOP_WIN["x"][0], 10, TOP_WIN["z_top"]-CAV_Z)
    p -= edge_wedge_yz(BY[1]-WALL, BY[1], TOP_WIN["z_top"], True, TOP_WIN["x"][0], TOP_WIN["x"][1])
    # power button through the bottom wall
    p -= Pos((PWR_SLOT["x"][0]+PWR_SLOT["x"][1])/2, BY[0], (PWR_SLOT["z"][0]+PWR_SLOT["z"][1])/2) * \
         Box(PWR_SLOT["x"][1]-PWR_SLOT["x"][0], 12, PWR_SLOT["z"][1]-PWR_SLOT["z"][0])
    # the four M3 screws, through the towers into the frame's bosses
    for sgn in (1, -1):
        for yc in FRAME_BOSS["ys"]:
            p -= Pos(sgn*100.0, yc, FRAME_BOSS["pilot_z"]) * Rot(Y=90) * Cylinder(CLEAR_D/2, 14)
            p -= Pos(sgn*(X_OUT-HEAD_DEEP/2), yc, FRAME_BOSS["pilot_z"]) * Rot(Y=90) * \
                 Cylinder(HEAD_D/2, HEAD_DEEP+0.02)

    # ---- OLED on the facet ----
    lip, seat = OLED["lip"], OLED["seat"]
    for sx in (1, -1):
        for sy in (1, -1):
            p += on_facet(FACET_MID, Pos(sx*OLED["holes"]/2, sy*OLED["holes"]/2, (2.0+seat)/2) *
                          Cylinder(3.0, seat-2.0))
    # the aperture must cut the 1.0 lip ONLY, not tunnel out of the pod's back.
    # C1 used a 40 mm-deep box and got away with it because its band was 36 mm deep;
    # this pod is 17, so 40 punched a 23.6x15.8 hole clean through the back face.
    ap = Pos(0, 0, (seat - 1.0)/2) * Box(OLED["apert"][0], OLED["apert"][1], seat + 1.0)
    pocket = Pos(0, 0, (lip+seat)/2) * Box(OLED["pocket"][0], OLED["pocket"][1], seat-lip)
    p -= on_facet(FACET_MID, ap + pocket)
    for sx in (1, -1):
        for sy in (1, -1):
            p -= on_facet(FACET_MID, Pos(sx*OLED["holes"]/2, sy*OLED["holes"]/2, (lip+seat+0.1)/2) *
                          Cylinder(OLED["pilot_d"]/2, seat+0.1-lip))

    p -= stand_cutter()
    return p


# ---------------------------------------------------------------- the back panel
def panel():
    g = PANEL_GAP
    q = Pos(0, 0, PANEL_Z[0]) * extrude(
        rrect(BX[0]+PANEL_INSET+g, BX[1]-PANEL_INSET-g, BY[0]+PANEL_INSET+g, BY[1]-PANEL_INSET-g, 5.0),
        PANEL_T)
    q -= stand_cutter((PANEL_INSET + g) / math.cos(math.radians(STAND_DEG)))
    for (sx, sy) in PANEL_SCREWS:
        q -= Pos(sx, sy, PANEL_Z[0]+PANEL_T/2) * Cylinder(CLEAR_D/2, PANEL_T+2)
        q -= Pos(sx, sy, BACK-HEAD_DEEP/2+0.01) * Cylinder(HEAD_D/2, HEAD_DEEP+0.02)
    # vents over the electronics, clear of the screw bosses
    for i in range(7):
        cx = -14.0 + i*10.0
        q -= Pos(cx, -24.0, PANEL_Z[0]+PANEL_T/2) * Box(3.0, 54.0, PANEL_T+2)
    return q


if __name__ == "__main__":
    import os
    os.makedirs("out", exist_ok=True)
    s = shell()
    bb = s.bounding_box()
    print(f"SHELL  x[{bb.min.X:7.2f},{bb.max.X:7.2f}] y[{bb.min.Y:7.2f},{bb.max.Y:7.2f}] "
          f"z[{bb.min.Z:7.2f},{bb.max.Z:7.2f}]   {s.volume/1000:6.1f} cm3")
    export_stl(s, "out/R3-Shell.stl"); export_step(s, "out/R3-Shell.step")
    q = panel()
    bb = q.bounding_box()
    print(f"PANEL  x[{bb.min.X:7.2f},{bb.max.X:7.2f}] y[{bb.min.Y:7.2f},{bb.max.Y:7.2f}] "
          f"z[{bb.min.Z:7.2f},{bb.max.Z:7.2f}]   {q.volume/1000:6.1f} cm3")
    export_stl(q, "out/R3-BackPanel.stl"); export_step(q, "out/R3-BackPanel.step")
    print(f"total plastic {(s.volume+q.volume)/1000:.1f} cm3  ~ {(s.volume+q.volume)/1000*1.27:.0f} g PETG")
