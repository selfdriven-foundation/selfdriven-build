"""Field Deck - CAMERA POD LOOKS: the plain box vs three retro looks, on the real r9 deck (2026-10-21, CONCEPT).

Owner: "the camera module, does it look ok as an add on? can we do something more retro?"
All four sit where the dock concept put the pod: a 2 mm plate under the back plate's upper screw on the grip side
(screw at model x 72.4, y 19.1), the pod slid onto it, looking backwards (model +z). Camera = Arducam B0292
(board 38 x 38 per Arducam; lens assumed in the middle; 60 deg H, 47 deg V, 72 deg diagonal). Nothing here is a print file.

Model frame (the r9 read-back): x toward the grip, y up, z toward the back; the back plate's face is z 53.0.
The pod body: x 50..96, y -18..28 (46 x 46), on the plate (z 53..55).
  python3 dock/cam_retro_concept.py [OUT]
"""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw
from build123d import (Box, Cylinder, Cone, Pos, Rot, chamfer, fillet, Axis, Align, RegularPolygon, Circle, Rectangle,
                       Plane, extrude, loft)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dock.dock_concept as D

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/dock/FieldDeck_camera_pod_looks.png"
CX, CY = 73.0, 5.0              # the pod's middle = the lens axis (model x, y)
ZP = 55.0                       # top of the 2 mm plate; the pod starts here
HALF = 23.0                     # pod body 46 x 46
# Black PETG drawn as a mid-dark grey so the shapes read (the deck and every pod alike); the bores darker still.
D.CASE = (0.40, 0.40, 0.42)
POD_COL = D.CASE                # printed in the same black PETG as the deck
BORE = (0.13, 0.13, 0.14)
PLEAT = (0.30, 0.30, 0.32)
MIN = (Align.CENTER, Align.CENTER, Align.MIN)

# The camera: lens aperture height above the plate and the view frustum (used by the check script too)
AP_R = 1.5                      # lens aperture radius (estimate)
H_HALF, V_HALF = math.radians(30.0), math.radians(23.5)


def P(x, y, z):
    return Pos(CX + x, CY + y, z)


def cyl(r, z0, z1, x=0.0, y=0.0):
    return P(x, y, z0) * Cylinder(r, z1 - z0, align=MIN)


def cone(r0, r1, z0, z1, x=0.0, y=0.0):
    if abs(r0 - r1) < 1e-3:
        return cyl(r0, z0, z1, x, y)
    return P(x, y, z0) * Cone(r0, r1, z1 - z0, align=MIN)


def body(z1, chamf=5.0, front_chamf=1.5):
    b = P(0, 0, ZP) * Box(2 * HALF, 2 * HALF, z1 - ZP, align=MIN)
    b = chamfer(b.edges().filter_by(Axis.Z), chamf)
    b = chamfer(b.edges().group_by(Axis.Z)[-1], front_chamf)
    return b


def bolts(shape, z_face, pts=((17, 17), (-17, 17), (17, -17), (-17, -17))):
    """The deck's own fastener mark (mk1_front): a round recess d6.6 x 0.9 with a hex socket A/F 3.81 to 1.95 deep."""
    for x, y in pts:
        shape -= P(x, y, z_face - 0.9) * Cylinder(3.3, 1.0, align=MIN)
        shape -= P(x, y, z_face - 1.95) * extrude(RegularPolygon(3.81 / math.sqrt(3), 6), 2.0)
    return shape


def knurl(shape, r, z0, z1, n, w=1.2, d=0.9, x=0.0, y=0.0):
    for k in range(n):
        shape -= P(x, y, (z0 + z1) / 2) * Rot(0, 0, k * 360.0 / n) * Pos(r, 0, 0) * Box(2 * d, w, z1 - z0 + 0.02)
    return shape


def camera_bits(z_top, objs):
    """What you would see of the camera: its square lens block and the glass."""
    objs.append(D.obj_b3d(P(0, 0, z_top - 3.0) * Box(8.5, 8.5, 3.0, align=MIN), D.BLACK, 0.3, model=True, tol=0.05))
    objs.append(D.obj_b3d(cyl(2.6, z_top, z_top + 0.6), D.GLASS, 0.9, model=True))
    objs.append(D.obj_b3d(cyl(1.2, z_top + 0.6, z_top + 0.8), (0.02, 0.02, 0.03), 0.9, model=True))


def plate():
    return Pos(CX, (CY - 25 + 28.6) / 2, 53.05) * Box(50, 28.6 - (CY - 25), 1.95, align=MIN)


# ------------------------------------------------------------------ NOW: the concept's plain box (dock_concept.POD)
def pod_now():
    objs = [D.obj_b3d(plate(), POD_COL, 0.12, model=True, tol=0.1)]
    b = P(0, 0, ZP) * Box(44, 44, 22, align=MIN)
    b = chamfer(b.edges().group_by(Axis.Z)[-1], 3.0)
    objs.append(D.obj_b3d(b, POD_COL, 0.12, model=True, tol=0.1))
    objs.append(D.obj_b3d(cyl(8.5, ZP + 22, ZP + 27), D.BLACK, 0.3, model=True, tol=0.05))
    objs.append(D.obj_b3d(cyl(5.5, ZP + 27, ZP + 27.4), D.GLASS, 0.9, model=True, tol=0.05))
    return objs, ZP + 27.0, None


# ------------------------------------------------------------------ A: FILM LENS (a 1960s cine lens on a bolted body)
A_AP = 68.6                     # lens aperture: back wall 2 + plug room 4 + board 1.6 + lens block 6 above the plate


def bore_r(z, margin=1.0):
    """Radius a round opening needs at height z so the 72 deg diagonal view passes it."""
    return AP_R + math.tan(math.radians(36.0)) * max(z - A_AP, 0.0) + margin


def split_inner(shape, r_max, x=0.0, y=0.0):
    """Faces lying within r_max of the lens axis (the bore and its steps) vs the rest. The renderer has no ambient
    shadow, so the bore is drawn darker - as a black hole looks."""
    from build123d import Compound
    ax, ay = CX + x, CY + y
    inner, outer = [], []
    for f in shape.faces():
        rho = max(math.hypot(v.X - ax, v.Y - ay) for v in f.vertices()) if f.vertices() else 99.0
        (inner if rho <= r_max + 0.01 else outer).append(f)
    return Compound(inner), Compound(outer)


A_STEPS = [(69.0, 74.0, 7.0), (74.0, 80.0, 11.0), (80.0, 85.0, 14.6)]   # stepped bore: z0, z1, radius


def pod_film():
    objs = [D.obj_b3d(plate(), POD_COL, 0.12, model=True, tol=0.1)]
    z_b = ZP + 14.0                                            # body front face 69.0
    b = bolts(body(z_b), z_b)
    zr = [z_b, z_b + 2.0, z_b + 9.0, z_b + 12.0, z_b + 16.0]   # mount ring | focus ring | scale ring | front barrel
    lens = (cyl(19.0, zr[0], zr[1]) + cyl(17.0, zr[1], zr[2]) + cyl(16.5, zr[2], zr[3]) + cyl(17.6, zr[3], zr[4] - 1.2)
            + cyl(18.2, zr[4] - 1.2, zr[4]))
    lens = knurl(lens, 17.0, zr[1] + 0.8, zr[2] - 0.8, 30)
    lens = knurl(lens, 18.2, zr[4] - 1.1, zr[4] - 0.1, 48, w=0.8, d=0.5)
    for k in range(13):                                        # distance scale: raised ticks round the scale ring
        a = math.radians(200 + k * 11.0)
        lens += P(16.5 * math.cos(a), 16.5 * math.sin(a), zr[3] - 2.2) * Rot(0, 0, math.degrees(a)) * Box(0.9, 0.7, 1.6 if k % 3 else 2.4, align=(Align.MIN, Align.CENTER, Align.MIN))
    lens += P(0, 19.0, zr[0] + 0.4) * Box(1.0, 1.6, 1.2, align=MIN)  # index mark on the mount ring
    for z0, z1, r in A_STEPS:                                  # the opening: steps, each wide enough for the full view
        lens -= cyl(r, z0 - 0.01, z1 + 0.01)
    b -= P(0, 0, z_b - 2.0) * Box(9.5, 9.5, 2.1, align=MIN)  # the lens block pokes through the front wall
    inner, outer = split_inner(lens, 14.6)
    objs.append(D.obj_b3d(b, POD_COL, 0.12, model=True, tol=0.08))
    objs.append(D.obj_b3d(outer, POD_COL, 0.14, model=True, tol=0.05, ang=0.12))
    objs.append(D.obj_b3d(inner, BORE, 0.05, model=True, tol=0.05, ang=0.12))
    camera_bits(A_AP, objs)
    return objs, zr[4], lens


# ------------------------------------------------------------------ B: BELLOWS (a 1930s folding camera; the camera rides on the front panel)
B_AP = 84.6


def pod_bellows():
    objs = [D.obj_b3d(plate(), POD_COL, 0.12, model=True, tol=0.1)]
    rear = body(ZP + 4.0, chamf=5.0, front_chamf=0.6)
    z0, n, pitch = ZP + 4.0, 5, 2.8                            # pleats 1.4 mm in per side over 1.4 mm = 45 deg: prints lens-up
    secs = []
    for k in range(2 * n):
        za, zb = z0 + k * pitch / 2, z0 + (k + 1) * pitch / 2
        a, b = (43.0, 40.2) if k % 2 == 0 else (40.2, 43.0)
        secs.append(loft([Plane.XY.offset(za) * Pos(CX, CY) * Rectangle(a, a), Plane.XY.offset(zb) * Pos(CX, CY) * Rectangle(b, b)]))
    bel = secs[0]
    for s in secs[1:]:
        bel += s
    zf = z0 + n * pitch                                        # 73.0: front panel
    front = P(0, 0, zf) * Box(46, 46, 11.0, align=MIN)
    front = chamfer(front.edges().filter_by(Axis.Z), 4.0)
    front = chamfer(front.edges().group_by(Axis.Z)[-1], 1.2)
    front = bolts(front, zf + 11.0)
    zt = zf + 11.0                                             # 84.0
    ring = cyl(12.0, zt, zt + 2.6) - cyl(7.2, zt - 0.1, zt + 2.7)
    ring = knurl(ring, 12.0, zt + 0.3, zt + 2.3, 24, w=1.0, d=0.6)
    front -= P(0, 0, zt - 2.0) * Box(9.5, 9.5, 2.1, align=MIN)
    lever = P(12.5, -6.5, zt) * Rot(0, 0, -30) * Box(9.0, 2.2, 1.4, align=(Align.MIN, Align.CENTER, Align.MIN))  # shutter lever
    objs.append(D.obj_b3d(rear, POD_COL, 0.12, model=True, tol=0.08))
    objs.append(D.obj_b3d(bel, PLEAT, 0.05, model=True, tol=0.05))
    objs.append(D.obj_b3d(front, POD_COL, 0.12, model=True, tol=0.08))
    inner, outer = split_inner(ring, 7.2)
    objs.append(D.obj_b3d(outer, POD_COL, 0.16, model=True, tol=0.05, ang=0.12))
    objs.append(D.obj_b3d(inner, BORE, 0.05, model=True, tol=0.05, ang=0.12))
    objs.append(D.obj_b3d(lever, POD_COL, 0.16, model=True, tol=0.05))
    camera_bits(B_AP, objs)
    return objs, zt + 2.6, ring


# ------------------------------------------------------------------ C: LENS TURRET (a 1950s cine turret; turn it to cover the camera)
C_AP = 68.6
T_R = 11.0                                                     # barrels' circle round the turret's pivot
T_PIV = (-T_R * math.cos(math.radians(30)), -T_R * math.sin(math.radians(30)))   # pivot down-left of the lens


def pod_turret():
    objs = [D.obj_b3d(plate(), POD_COL, 0.12, model=True, tol=0.1)]
    z_b = ZP + 14.0
    b = bolts(body(z_b), z_b, pts=((17, 17), (17, -17), (-17, 17)))
    b -= P(0, 0, z_b - 2.0) * Box(9.5, 9.5, 2.1, align=MIN)
    px, py = T_PIV
    disc = cyl(21.0, z_b + 0.4, z_b + 3.4, px, py)
    disc = knurl(disc, 21.0, z_b + 0.4, z_b + 3.4, 40, w=1.1, d=0.6, x=px, y=py)
    barrels = []
    for k, (r_out, h, open_) in enumerate(((9.2, 3.0, True), (6.5, 13.0, False), (7.5, 7.0, False))):
        a = math.radians(30 + 120 * k)                         # k = 0 sits on the lens axis
        bx, by = px + T_R * math.cos(a), py + T_R * math.sin(a)
        zb0 = z_b + 3.4
        barrel = cyl(r_out, zb0, zb0 + h, bx, by) + cyl(r_out + 1.0, zb0 + h - 1.6, zb0 + h, bx, by)
        if open_:
            barrel -= cone(6.6, 7.6, z_b - 0.1, zb0 + h + 0.1, bx, by)
            r_in = 7.6
        else:
            barrel -= cyl(r_out - 2.0, zb0 + h - 1.0, zb0 + h + 0.1, bx, by)     # a dummy: shallow dish, no hole
            r_in = r_out - 2.0
        inner, outer = split_inner(barrel, r_in, bx, by)       # bx, by are offsets from the lens axis, like cyl()'s
        objs.append(D.obj_b3d(outer, POD_COL, 0.16, model=True, tol=0.05, ang=0.12))
        objs.append(D.obj_b3d(inner, BORE, 0.05, model=True, tol=0.05, ang=0.12))
        barrels.append(barrel)
    disc -= cyl(6.6, z_b - 0.1, z_b + 3.5)                     # the opening over the camera
    piv = cyl(3.0, z_b + 3.4, z_b + 4.6, px, py) - P(px, py, z_b + 3.6) * extrude(RegularPolygon(3.81 / math.sqrt(3), 6), 1.2)
    objs.append(D.obj_b3d(b, POD_COL, 0.12, model=True, tol=0.08))
    objs.append(D.obj_b3d(disc + piv, POD_COL, 0.14, model=True, tol=0.05, ang=0.12))
    camera_bits(C_AP, objs)
    return objs, z_b + 3.4 + 13.0, barrels[0]


DESIGNS = [("Now", "a plain box", pod_now),
           ("A  Film lens", "like a 1960s cine camera", pod_film),
           ("B  Bellows", "like a 1930s folding camera", pod_bellows),
           ("C  Lens turret", "like a 1950s film camera", pod_turret)]
PICK = "A  Film lens"
VIEW_F = (0.80, -1.0, -0.42)     # from behind, grip side, a little above


def deck_near():
    """The deck parts near the pod (all six case parts + the screen, as in the dock concept)."""
    return D.deck_objects()


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    deck = deck_near()
    ground = [D.obj_b3d(D.box(-900, 900, -700, 1000, D.TOP - 2.0, D.TOP - 0.05), D.GROUND, 0.0, tol=1.0)]
    W, H = 1000, 820
    tgt = D.to_world((CX + 8, CY + 4, 60.0))
    view = D.M.View(VIEW_F, (0, 0, 1), tgt, 7.0, W, H)
    panels = []
    for title, sub, fn in DESIGNS:
        objs, ztop, _ = fn()
        im = D.render(view, ground + deck + objs, W, H).convert("RGB")
        d = ImageDraw.Draw(im)
        tw = max(d.textlength(title, font=D.BOLD(40)), d.textlength(sub, font=D.REG(27)))
        d.rounded_rectangle([14, 14, 14 + tw + 28, 116], radius=10, fill=(255, 255, 255), outline=D.INK, width=3)
        d.text((28, 20), title, font=D.BOLD(40), fill=D.INK)
        d.text((28, 72), sub, font=D.REG(27), fill=(80, 82, 86))
        if title == PICK:
            tw = d.textlength("my pick", font=D.BOLD(26))
            d.rounded_rectangle([W - tw - 52, 20, W - 20, 64], radius=10, fill=D.ORANGE)
            d.text((W - tw - 36, 26), "my pick", font=D.BOLD(26), fill=(255, 255, 255))
        panels.append(im)
        print("rendered", title, flush=True)
    g = 10
    out = Image.new("RGB", (2 * W + 3 * g, 2 * H + 3 * g + 64), (205, 205, 205))
    for k, im in enumerate(panels):
        out.paste(im, (g + (k % 2) * (W + g), g + (k // 2) * (H + g)))
    d = ImageDraw.Draw(out)
    d.rectangle([0, 2 * H + 3 * g, out.width, out.height], fill=(255, 255, 255))
    d.text((24, 2 * H + 3 * g + 14), "Concept only.  Seen from behind, grip side.  Same spot, same camera, printed in your black PETG.  The deck is the real r9 model.",
           font=D.REG(27), fill=D.INK)
    out.save(OUT)
    print("wrote", OUT, out.size)
