"""MK-I BODY r3 + HUD CAP — the owner's verdict on r2 (2026-10-02):
  * "the pebble makes it less aligned to the theme"      -> the back is ANGULAR again, faceted like
    the S1 mock-up he picked, and still ONE closed part ("I do not see much value in a detachable
    back panel");
  * HDMI: "Yes, keep them open"                           -> the HUD cannot sit over the top sockets;
  * HUD place: he picked "B - handle side" from the picture (so his left/right are FRONT-view);
  * "the back panel of the HUD is supposed to allow me to put in the OLED? ... how does it stay put
    at the front?"                                        -> the HUD is a STRAIGHT TUBE along the
    OLED's own axis: the module slides in from the back, stops on the front lip, and is screwed to
    its posts with a straight driver. A cap closes the tube.

THE BACK. Faceted box: four plan corners chamfered 8, the back edge chamfered 10, flat back at
z 56.5 (unchanged). Inside, every chamfer is matched (c - 1.464) so the wall is 2.5 everywhere.
Footprint x -38.2..75.7, y -84..36.6 (r2's, already checked for plugs and stack room): an 8 mm
corner needs 4..5.5 mm between wall and stack; R3's 1.5 allowed only 3.5 mm chamfers (r1).
The 10 mm back edge is the largest that starts above every opening's chamfered top (z 46.5);
its 45 deg inside is self-supporting, so only the flat 92 x 98 ceiling needs support.

THE HUD, handle side, x 60..93 (33 wide, between the charging cable and the top-left screw tower).
  facet (48 deg, R3's seat verbatim) -> tube cavity a 1.2..28.8 (module 2.22..27.78), 34.5 deep
  -> rear plane parallel to the facet, open from a -8.5 to 28.8. Under the tube the pod is hollow
  down to the skirt (side walls go straight down: nothing starts in mid-air), which gives
    - the place for the cap's lower screw boss, BELOW the module's path;
    - the wire way: the skirt roof is cut away under it (see r2's trough), so the leads lie on the
      back of the screen and the body is lowered over them.
  The cap's two upper screws go into a "brow" on top of the tube's rear end, ABOVE the module's path.
  Known limit (checked in mk1_check_r3.py): the body's top-left corner stands behind the tube's
  lower inner corner. So a straight driver reaches 3 of the 4 OLED screws (both upper ones and the
  lower one on the handle side) and the cap has 3 screws, not 4. Three hold a board or a plate;
  the OLED's 4th post is a rest.

Top opening: 2 x HDMI + charge, x -1.2..46 (r1's). The Pi's own USB-C stays behind solid wall.
Everything about the frame interface is R3's, verbatim. No power-switch opening yet (M1).
"""
from build123d import *
import math
from r3_params import *
from build_r3 import rrect, stand_cutter, facet_pt, edge_wedge_yz, FDIR, FIN

# ---------------- the body ----------------
PX = (-38.2, 75.7)
PY = (-84.0, 36.6)
C_PLAN, C_BACK = 7.5, 10.0                # 45 deg chamfers: plan corners, back edge. 8.0 left only 0.85 mm
                                          # between the stack's top-right-back corner and the corner facet's
                                          # own back chamfer; 7.5 gives 1.10 (measured in mk1_check_r3.py)
K_IN = WALL * (2.0 - math.sqrt(2.0))      # 1.464: the matching inside chamfer is this much smaller
TOP_NOTCH_X = (-1.2, TOP_WIN["x"][1])     # HDMI 6.7 and 19.7, charge 30.7 (plug zones 1.2 .. 39.4)
SIDE_Y = (SIDE_WIN["y"][0], 32.0)         # Eth/USB window
VENT = dict(ys=[-62.0 + 9.5 * k for k in range(9)], w=3.0, z=(12.0, 38.0))

# ---------------- the HUD pod ----------------
HUD_X = 76.5
POD_X = (60.0, 93.0)
A_LO, A_HI = 1.2, 28.8                    # tube cavity along the facet; the module is 2.22..27.78
FLEN = A_HI + WALL                        # 31.3: outside of the tube's top wall
L_REAR = 34.5                             # rear plane = cap seat, measured in from the facet
A_CH = -8.5                               # lower edge of the rear opening
BROW_A, BROW_D = 37.2, 9.0                # the brow: up to here, this far forward of the rear plane
POD_C = 2.5                               # chamfer on the pod's long outer edges (1.77 mm corner wall)
POD_BACK_Y = PY[1]                        # the pod's rear foot continues the body's top wall line
TROUGH_Y1 = 68.6                          # skirt roof cut under the pod, up to the pod cavity's end
OLED_ALONG = FACET_MID
# cap
CAP_T = 2.5
CAP_A = (-10.5, BROW_A)                   # its lower edge stops 0.4 short of the body's top wall
CAP_SCREW_A = (-5.0, 33.9)                # lower (in a boss under the tube), upper pair (in the brow)
CAP_SCREW_DX = 10.5
CAP_PILOT_DEEP = 8.0
BOSS_W, BOSS_A_TOP, BOSS_D = 7.0, -1.5, 10.0   # lower boss: 7 wide off the side wall, top 3.3 below the module, 10 long


def facet_ad(y, z):
    """(y, z) -> (along the facet, deep behind it)"""
    return ((y - Y_TOPF) * FDIR[0] + z * FDIR[1], (y - Y_TOPF) * FIN[0] + z * FIN[1])


def fbox(x0, x1, a0, a1, d0, d1):
    """box in FACET coordinates: world x, along the slope, deep behind the facet"""
    return Pos(0, FACET_A[0], FACET_A[1]) * Rot(X=FACET_DEG) * \
           Pos((x0+x1)/2, (a0+a1)/2, (d0+d1)/2) * Box(x1-x0, a1-a0, d1-d0)


def axis_cyl(x, a, d0, d1, r):
    """cylinder on an axis PERPENDICULAR to the facet, from deep d0 to deep d1"""
    y, z = facet_pt(a, (d0 + d1) / 2)
    return Pos(x, y, z) * Rot(X=FACET_DEG) * Cylinder(r, d1 - d0)


def on_facet(along, obj):
    y, z = facet_pt(along)
    return Pos(HUD_X, y, z) * Rot(X=FACET_DEG) * obj


def wedge_x(x_in, x_out, z_edge, up, y0, y1, ov):
    """a true 45 deg chamfer on a window edge in a +x wall, starting at the inside face.
    Own version of build_r3.edge_wedge_xz. That one gives no direction to extrude(): for a LOWER
    edge (up=False) the profile's winding flips and the wedge goes to y y1+2 .. y1+66 instead of
    y0-2 .. y1+2. On the printed R3 shell that left the window's lower edge square and cut a
    shallow stray groove in the skirt behind the top-left corner; here it would have cut the HUD
    pod's foot in two (found on a section drawing, not by a probe).
    `ov` = how far past the outer face the wedge runs. The lower edge sits 4 mm above the skirt,
    so its wedge must stop before it digs into the skirt roof."""
    eps = 0.02
    sgn = 1 if up else -1
    zt = z_edge + sgn * (abs(x_out - x_in) + ov)
    z0 = z_edge - sgn * eps
    prof = make_face(Plane.XZ * Polyline((x_in - eps, z0), (x_out + ov, z0), (x_out + ov, zt), (x_in - eps, z0)))
    return Pos(0, y0 - 2.0, 0) * extrude(prof, (y1 - y0) + 4.0, dir=(0, 1, 0))


def faceted(x0, x1, y0, y1, z0, z1, c_plan, c_back):
    b = Pos((x0+x1)/2, (y0+y1)/2, (z0+z1)/2) * Box(x1-x0, y1-y0, z1-z0)
    b = chamfer(b.edges().filter_by(Axis.Z), c_plan)
    return chamfer(b.edges().group_by(Axis.Z)[-1], c_back)


def hump_outer():
    return faceted(*PX, *PY, SKIRT_Z - 0.5, BACK, C_PLAN, C_BACK)


def hump_inner():
    return faceted(PX[0]+WALL, PX[1]-WALL, PY[0]+WALL, PY[1]-WALL, CAV_Z, BACK - WALL, C_PLAN - K_IN, C_BACK - K_IN)


def rear_at_y(y):
    """the rear plane's (a, z) where it crosses a given y"""
    a = (y - Y_TOPF - FIN[0] * L_REAR) / FDIR[0]
    return a, FDIR[1] * a + FIN[1] * L_REAR


def pod_outer():
    A = facet_pt(0.0)
    B = facet_pt(FLEN)
    B1 = facet_pt(FLEN, L_REAR - BROW_D)
    R1 = facet_pt(BROW_A, L_REAR - BROW_D)
    R2 = facet_pt(BROW_A, L_REAR)
    _, zf = rear_at_y(POD_BACK_Y)
    pts = [A, B, B1, R1, R2, (POD_BACK_Y, zf), (POD_BACK_Y, SKIRT_Z - 0.5), (Y_TOPF, SKIRT_Z - 0.5)]
    prof = make_face(Plane.YZ * Polyline(*pts, pts[0]))
    pod = Pos(POD_X[0], 0, 0) * extrude(prof, POD_X[1] - POD_X[0], dir=(1, 0, 0))
    hw, xc, pick = (POD_X[1] - POD_X[0]) / 2, (POD_X[0] + POD_X[1]) / 2, []
    for e in pod.edges():
        c = e.center(); a, d = facet_ad(c.Y, c.Z)
        side = abs(abs(c.X - xc) - hw) < 0.01
        if side and abs(d) < 0.01 and 0.01 < a < FLEN - 0.01:
            pick.append(e)                                   # facet, both sides
        elif side and abs(a - FLEN) < 0.01 and 0.01 < d < L_REAR - BROW_D - 0.01:
            pick.append(e)                                   # tube top, both sides (up to the brow)
        elif abs(c.X - xc) < 0.01 and abs(a - FLEN) < 0.01 and abs(d) < 0.01:
            pick.append(e)                                   # the ridge
    assert len(pick) == 5, "pod: expected 5 edges to chamfer, found %d" % len(pick)
    return chamfer(pick, POD_C)


def pod_cavity():
    """everything hollow inside the pod: the tube (a A_LO..A_HI) and the space under it down to the
    skirt roof. Open through the rear plane from A_CH up."""
    yb = POD_BACK_Y + WALL                                   # inside of the pod's rear foot
    d_in = L_REAR - WALL                                     # inside of the sill under the opening
    a_k = (yb - Y_TOPF - FIN[0] * d_in) / FDIR[0]            # where that sill meets the foot
    q_lo = facet_pt(A_LO, WALL)
    q_l7 = facet_pt(A_LO, (SKIRT_Z - FDIR[1] * A_LO) / FIN[1])
    pts = [(yb, SKIRT_Z), facet_pt(a_k, d_in), facet_pt(A_CH, d_in), facet_pt(A_CH, L_REAR + 3.0),
           facet_pt(A_HI, L_REAR + 3.0), facet_pt(A_HI, WALL), q_lo, q_l7]
    prof = make_face(Plane.YZ * Polyline(*pts, pts[0]))
    return Pos(POD_X[0] + WALL, 0, 0) * extrude(prof, POD_X[1] - POD_X[0] - 2 * WALL, dir=(1, 0, 0))


def cap_screws():
    """(x, along) of the cap's THREE screws: both upper corners and the lower corner on the handle
    side. The lower inner corner has none: the body's top-left corner stands 5 mm behind it, and no
    driver gets there (checked)."""
    return [(HUD_X - CAP_SCREW_DX, CAP_SCREW_A[1]), (HUD_X + CAP_SCREW_DX, CAP_SCREW_A[1]),
            (HUD_X + CAP_SCREW_DX, CAP_SCREW_A[0])]


def cap_bosses():
    """the LOWER boss: a wedge off the handle-side wall, in the space under the tube. Its underside
    rises at 45 deg from the wall (world x-z), so each layer rests on the last. It is cut from the
    cavity's own shape, then copied 1 mm into the side wall so the two are one piece (a boss that
    only touches its wall does not fuse - R3)."""
    xw, s = POD_X[1] - WALL, -1
    x_in = xw + s * BOSS_W
    blk = fbox(min(xw, x_in), max(xw, x_in), -60.0, BOSS_A_TOP, L_REAR - BOSS_D, L_REAR)
    pts = [(xw, SKIRT_Z), (x_in, SKIRT_Z + BOSS_W), (x_in, 80.0), (xw, 80.0)]      # keep z >= SKIRT_Z + |x - xw|
    keep = Pos(0, 120.0, 0) * extrude(make_face(Plane.XZ * Polyline(*pts, pts[0])), 120.0, dir=(0, -1, 0))
    b = (blk & keep) & pod_cavity()
    return b + Pos(-s * 1.0, 0, 0) * b


def body():
    # ---- outer solid ----
    p = extrude(rrect(-X_OUT, X_OUT, Y_BOT, Y_TOPF, R_OUT), SKIRT_Z)                 # skirt (R3)
    p += hump_outer()
    p += pod_outer()
    for sgn in (1, -1):                                                              # boss towers (R3)
        for yc in FRAME_BOSS["ys"]:
            p += Pos(sgn*(93.0+X_OUT)/2, yc, (SKIRT_Z+21.0)/2) * Box(X_OUT-93.0, 20.0, 21.0-SKIRT_Z)

    # ---- interior ----
    inner = extrude(rrect(-X_OUT+WALL, X_OUT-WALL, Y_BOT+WALL, Y_TOPF-WALL, SKIRT_CAV_R), CAV_Z+2)
    inner = Pos(0, 0, -2) * inner
    inner += hump_inner()                                                            # CLOSED at the back
    inner += pod_cavity()
    for sgn in (1, -1):                                                              # tower pockets (R3)
        for yc in FRAME_BOSS["ys"]:
            inner += Pos(sgn*(95.5+101.5)/2, yc, 22.0/2) * Box(101.5-95.5, 13.0, 22.0)
    RELIEF, RZ = 0.6, 0.8                                                            # lead-in relief (R3)
    inner += Pos(0, 0, -2) * extrude(rrect(-X_OUT+WALL-RELIEF, X_OUT-WALL+RELIEF,
                                           Y_BOT+WALL-RELIEF, Y_TOPF-WALL+RELIEF,
                                           SKIRT_CAV_R), 2 + RZ)
    for sgn in (1, -1):
        for yc in FRAME_BOSS["ys"]:
            inner += Pos(sgn*(95.5+101.5)/2, yc, (-2+RZ)/2) * \
                     Box(101.5-95.5+2*RELIEF, 13.0+2*RELIEF, 2+RZ)
    inner -= stand_cutter(WALL / math.cos(math.radians(STAND_DEG)))
    p -= inner

    # ---- the wire way: skirt roof cut away under the pod's cavity ----
    wx0, wx1 = POD_X[0] + WALL, POD_X[1] - WALL
    ty0 = POD_BACK_Y + WALL
    p -= Pos((wx0+wx1)/2, (ty0 + TROUGH_Y1)/2, (CAV_Z - 1.5 + SKIRT_Z + 0.5)/2) * \
         Box(wx1-wx0, TROUGH_Y1 - ty0, SKIRT_Z + 0.5 - (CAV_Z - 1.5))

    # ---- cap bosses + pilots ----
    p += cap_bosses()
    for (sx, a) in cap_screws():
        p -= axis_cyl(sx, a, L_REAR - CAP_PILOT_DEEP, L_REAR + 0.5, PILOT_D/2)

    # ---- openings ----
    # Eth / USB: everything outboard of the port faces, through the +x wall
    p -= Pos((ETH_FACE_X + PX[1] + 5.0)/2, (SIDE_Y[0]+SIDE_Y[1])/2, (SIDE_WIN["z"][0]+SIDE_WIN["z"][1])/2) * \
         Box(PX[1] + 5.0 - ETH_FACE_X, SIDE_Y[1]-SIDE_Y[0], SIDE_WIN["z"][1]-SIDE_WIN["z"][0])
    p -= wedge_x(PX[1]-WALL, PX[1], SIDE_WIN["z"][1], True, SIDE_Y[0], SIDE_Y[1], 3.0)     # upper edge
    p -= wedge_x(PX[1]-WALL, PX[1], SIDE_WIN["z"][0], False, SIDE_Y[0], SIDE_Y[1], 0.5)    # lower edge
    # top: 2 x HDMI + the X1201 charge socket
    p -= Pos((TOP_NOTCH_X[0]+TOP_NOTCH_X[1])/2, PY[1], (CAV_Z+TOP_WIN["z_top"])/2) * \
         Box(TOP_NOTCH_X[1]-TOP_NOTCH_X[0], 10, TOP_WIN["z_top"]-CAV_Z)
    p -= edge_wedge_yz(PY[1]-WALL, PY[1], TOP_WIN["z_top"], True, TOP_NOTCH_X[0], TOP_NOTCH_X[1])
    # vents in the blank D-side wall
    for y in VENT["ys"]:
        p -= Pos(PX[0] + WALL/2, y, (VENT["z"][0]+VENT["z"][1])/2) * Box(WALL + 3.0, VENT["w"], VENT["z"][1]-VENT["z"][0])
    # the four M3 screws into the frame's bosses (R3)
    for sgn in (1, -1):
        for yc in FRAME_BOSS["ys"]:
            p -= Pos(sgn*100.0, yc, FRAME_BOSS["pilot_z"]) * Rot(Y=90) * Cylinder(CLEAR_D/2, 14)
            p -= Pos(sgn*(X_OUT-HEAD_DEEP/2), yc, FRAME_BOSS["pilot_z"]) * Rot(Y=90) * \
                 Cylinder(HEAD_D/2, HEAD_DEEP+0.02)

    # ---- OLED seat on the facet (R3's, at HUD_X) ----
    lip, seat = OLED["lip"], OLED["seat"]
    for sx in (1, -1):
        for sy in (1, -1):
            p += on_facet(OLED_ALONG, Pos(sx*OLED["holes"]/2, sy*OLED["holes"]/2, (2.0+seat)/2) *
                          Cylinder(3.0, seat-2.0))
    ap = Pos(0, 0, (seat - 1.0)/2) * Box(OLED["apert"][0], OLED["apert"][1], seat + 1.0)
    pocket = Pos(0, 0, (lip+seat)/2) * Box(OLED["pocket"][0], OLED["pocket"][1], seat-lip)
    p -= on_facet(OLED_ALONG, ap + pocket)
    for sx in (1, -1):
        for sy in (1, -1):
            p -= on_facet(OLED_ALONG, Pos(sx*OLED["holes"]/2, sy*OLED["holes"]/2, (lip+seat+0.1)/2) *
                          Cylinder(OLED["pilot_d"]/2, seat+0.1-lip))

    p -= stand_cutter()
    return p


def hud_cap():
    """the tube's back plate, in place. Prints flat, inside face down (see cap_for_print)."""
    q = fbox(POD_X[0], POD_X[1], CAP_A[0], CAP_A[1], L_REAR, L_REAR + CAP_T)
    outer = [e for e in q.edges() if abs(facet_ad(e.center().Y, e.center().Z)[1] - (L_REAR + CAP_T)) < 0.01]
    assert len(outer) == 4, "cap: expected 4 outer edges, found %d" % len(outer)
    q = chamfer(outer, 0.8)
    for (sx, a) in cap_screws():
        q -= axis_cyl(sx, a, L_REAR - 1.0, L_REAR + CAP_T + 1.0, CLEAR_D/2)
        q -= axis_cyl(sx, a, L_REAR + CAP_T - HEAD_DEEP, L_REAR + CAP_T + 0.5, HEAD_D/2)
    return q


def cap_for_print(q):
    """lay the cap on its inside face: the axis perpendicular to the facet becomes +z"""
    r = Rot(X=-FACET_DEG) * q
    bb = r.bounding_box()
    return Pos(-(bb.min.X + bb.max.X)/2, -(bb.min.Y + bb.max.Y)/2, -bb.min.Z) * r


def export_clean_stl(shape, path):
    """export, drop zero-area triangles, insist on a watertight mesh (see r2: a slicer would
    list them as "repaired errors", and a slicer warning is a stop gate)."""
    import trimesh
    export_stl(shape, path)
    m = trimesh.load(path, force="mesh", process=False); m.merge_vertices()
    f = m.faces
    keep = (f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])
    m.update_faces(keep); m.remove_unreferenced_vertices()
    assert m.is_watertight and m.is_winding_consistent, path + ": not watertight after cleaning"
    assert (m.area_faces > 1e-9).all(), path + ": zero-area triangles remain"
    assert abs(m.volume - shape.volume) / shape.volume < 2e-3, path + ": mesh volume is off"
    m.export(path)
    return int((~keep).sum())


if __name__ == "__main__":
    import os
    os.makedirs("out/mk1", exist_ok=True)
    b, c = body(), hud_cap()
    for nm, s in (("Body", b), ("HUD-Cap (in place)", c)):
        bb = s.bounding_box()
        print("%-20s valid %s  solids %d  vol %6.1f cm3  x %7.2f..%7.2f  y %7.2f..%7.2f  z %6.2f..%6.2f" % (
            nm, s.is_valid, len(s.solids()), s.volume/1000, bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z))
    cp = cap_for_print(c)
    bb = cp.bounding_box()
    print("HUD-Cap on the plate: %.1f x %.1f x %.2f" % (bb.max.X-bb.min.X, bb.max.Y-bb.min.Y, bb.max.Z-bb.min.Z))
    export_step(b, "out/mk1/MK1-Body_r3.step"); print("  body STL: %d zero-area triangles dropped" % export_clean_stl(b, "out/mk1/MK1-Body_r3.stl"))
    export_step(cp, "out/mk1/MK1-HUD-Cap_r3.step"); print("  cap STL:  %d zero-area triangles dropped" % export_clean_stl(cp, "out/mk1/MK1-HUD-Cap_r3.stl"))
