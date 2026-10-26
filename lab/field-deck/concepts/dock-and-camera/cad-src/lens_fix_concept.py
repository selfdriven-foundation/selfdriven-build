"""Field Deck - HOW THE FILM LENS FIXES (2026-10-21, CONCEPT; the owner picked look A).

A small BASE (shoe) is held by the back plate's upper grip-side screw: the M3x8 comes out, the base goes on, an M3x10
goes back through it. The base sits on the plate's raised armour (z 53.0), its spigot in the old screw's seat, its pin in
the hex mark at (60.7, 21.6), so it cannot turn. Its top and bottom edges are a 45 deg dovetail. The LENS has the matching
channel in its back: it slides on from the grip side (-x) until a springy tongue on the base clicks into a dimple.
The camera lead leaves the lens's grip-side wall and plugs into the upper USB port of the stack at y -1.1.
Model frame of the r9 read-back: x toward the grip, y up, z toward the back. Nothing here is a print file.
  python3 dock/lens_fix_concept.py [OUT]
"""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw
from build123d import (Box, Cylinder, Cone, Sphere, Pos, Rot, chamfer, Axis, Align, RegularPolygon, Rectangle, Plane,
                       extrude, loft, Compound, import_step)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dock.dock_concept as D
FD_STEP = os.environ.get("FD_STEP", "readback/item_r9_hud.step")   # the printed r9 read-back (Fusion v12); in the public
# repo use cad/MK1-r9_design_public_NOT-FOR-PRINT.step, whose body (the two names filled in) is 115741.7297 mm3
def vmatch(a, v):
    return abs(a - v) < 0.01 or (abs(v - 115715.2078) < 1e-6 and abs(a - 115741.7297) < 0.05)

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/dock/FieldDeck_lens_fixing.png"
MIN = (Align.CENTER, Align.CENTER, Align.MIN)
D.CASE = (0.40, 0.40, 0.42)                  # black PETG drawn mid-grey (as in the looks picture)
POD_COL, BORE = D.CASE, (0.13, 0.13, 0.14)
BASE_COL = (0.95, 0.55, 0.13)                # the new base drawn orange so it can be found
SCREW_COL = (0.78, 0.80, 0.83)

# ---- where things are (model frame)
AX, AY = 73.0, 7.5                           # lens axis; the lens body is 46 x 46 round it
SCREW = (72.4, 19.1)                         # back plate's upper grip-side screw
HEXMARK = (60.7, 21.6)                       # an armour hex mark (A/F 4.0, 0.6 deep) on a raised plate
FACE = 53.0                                  # top of the back plate's raised armour
# base (shoe)
B_X0, B_X1 = 56.0, 80.0
B_Y_BOT = (7.5, 24.5)                        # underside, z 53.0
B_Y_TOP = (4.0, 28.0)                        # top, z 56.5 -> 45 deg dovetail edges
B_T = 3.5
HEAD_SEAT = FACE + 1.0                       # z 54.0: under-head seat in the base's counterbore
SPIGOT_D, SPIGOT_BOT = 6.0, 51.3             # the back plate's counterbore is d6.1, floor z 51.3
PIN_D, PIN_H = 3.6, 0.5
TONGUE = (58.0, 68.0, 9.0, 15.0)             # x0, x1 (root), y0, y1; 1.5 thick at the top
BUMP = (59.6, 12.0)
# lens
CLR = 0.25                                   # channel clearance
BACK = FACE + 0.1                            # the lens's back face floats 0.1 over the armour
CEIL = FACE + B_T + CLR                      # channel ceiling z 56.75
FLOOR = 1.5
Z_FRONT = 72.0                               # body front face
AP = 71.8                                    # lens aperture: lens block top (board front 65.8 + 6)
STEPS = [(72.0, 77.0, 7.0), (77.0, 83.0, 11.0), (83.0, 88.0, 14.6)]
# lead: into the upper port of the USB stack at y -1.1 (stack x 46.8..64.3, z 15.3..30.9; the side window x 73.2..75.7)
PORT = (-1.1, 27.0)


def P(x, y, z):
    return Pos(x, y, z)


def cyl(r, z0, z1, x=AX, y=AY):
    return Pos(x, y, z0) * Cylinder(r, z1 - z0, align=MIN)


def bx(x0, x1, y0, y1, z0, z1):
    return D.box(x0, x1, y0, y1, z0, z1)


def prism_x(x0, x1, ylo, zlo, yhi, zhi):
    """A trapezoid (ylo at zlo, yhi at zhi) swept along x."""
    a = Plane.XY.offset(zlo) * Pos((x0 + x1) / 2, (ylo[0] + ylo[1]) / 2) * Rectangle(x1 - x0, ylo[1] - ylo[0])
    b = Plane.XY.offset(zhi) * Pos((x0 + x1) / 2, (yhi[0] + yhi[1]) / 2) * Rectangle(x1 - x0, yhi[1] - yhi[0])
    return loft([a, b])


# ------------------------------------------------------------------ the base
def base():
    s = prism_x(B_X0, B_X1, B_Y_BOT, FACE, B_Y_TOP, FACE + B_T)
    s += Pos(*SCREW, SPIGOT_BOT) * Cylinder(SPIGOT_D / 2, FACE - SPIGOT_BOT + 0.01, align=MIN)
    s += Pos(*HEXMARK, FACE - PIN_H) * Cylinder(PIN_D / 2, PIN_H + 0.01, align=MIN)
    s -= Pos(*SCREW, SPIGOT_BOT - 0.1) * Cylinder(1.7, 10, align=MIN)            # d3.4 clearance
    s -= Pos(*SCREW, HEAD_SEAT) * Cylinder(3.5, 5, align=MIN)                    # d7.0 counterbore for the head
    tx0, tx1, ty0, ty1 = TONGUE                                                   # the springy tongue
    s -= bx(tx0 - 0.8, tx1, ty0 - 0.8, ty0, FACE - 1, FACE + B_T + 1)
    s -= bx(tx0 - 0.8, tx1, ty1, ty1 + 0.8, FACE - 1, FACE + B_T + 1)
    s -= bx(tx0 - 0.8, tx0, ty0 - 0.8, ty1 + 0.8, FACE - 1, FACE + B_T + 1)
    s -= bx(tx0, tx1, ty0, ty1, FACE - 1, FACE + B_T - 1.5)                       # 1.5 thick, room to bend down
    s += Pos(*BUMP, FACE + B_T) * Cone(1.5, 0.7, 0.6, align=MIN)
    return s


def screw(z_seat=HEAD_SEAT):
    """M3 x 10 pan head: head d5.5 x 2.1, shank d3.0 x 10 under the head."""
    head = Pos(*SCREW, z_seat) * Cylinder(2.75, 2.1, align=MIN)
    head = chamfer(head.edges().group_by(Axis.Z)[-1], 0.6)
    head -= Pos(*SCREW, z_seat + 1.2) * Box(3.0, 0.7, 2)
    head -= Pos(*SCREW, z_seat + 1.2) * Box(0.7, 3.0, 2)
    shank = Pos(*SCREW, z_seat - 10.0) * Cylinder(1.5, 10.0, align=MIN)
    return head + shank


# ------------------------------------------------------------------ the lens (look A) with its channel
def lens_body():
    b = Pos(AX, AY, BACK) * Box(46, 46, Z_FRONT - BACK, align=MIN)
    b = chamfer(b.edges().filter_by(Axis.Z), 5.0)
    b = chamfer(b.edges().group_by(Axis.Z)[-1], 1.5)
    for x, y in ((17, 17), (-17, 17), (17, -17), (-17, -17)):                    # the deck's fastener marks
        b -= Pos(AX + x, AY + y, Z_FRONT - 0.9) * Cylinder(3.3, 1.0, align=MIN)
        b -= Pos(AX + x, AY + y, Z_FRONT - 1.95) * extrude(RegularPolygon(3.81 / math.sqrt(3), 6), 2.0)
    ch = prism_x(AX - 23.5, B_X1 + 0.1, (B_Y_BOT[0] - CLR, B_Y_BOT[1] + CLR), FACE, (B_Y_TOP[0] - CLR, B_Y_TOP[1] + CLR), CEIL)
    b -= ch                                                                       # open at the lens's -x side
    b -= Pos(*BUMP, CEIL - 0.01) * Cylinder(1.7, 0.7, align=MIN)                  # the dimple the bump clicks into
    b -= Pos(AX, AY, CEIL + FLOOR) * Box(40, 40, Z_FRONT - 2.0 - (CEIL + FLOOR), align=MIN)   # board space (hidden)
    b -= Pos(AX, AY, Z_FRONT - 2.1) * Box(9.5, 9.5, 2.2, align=MIN)                # lens block through the front wall
    b -= bx(AX + 21, AX + 24, -10.0, -2.0, CEIL + FLOOR + 0.5, CEIL + FLOOR + 5.5)   # lead slot 8 x 5 (the plug passes)
    return b


def lens_barrel():
    zr = [Z_FRONT, Z_FRONT + 2.0, Z_FRONT + 9.0, Z_FRONT + 12.0, Z_FRONT + 16.0]
    L = (cyl(19.0, zr[0], zr[1]) + cyl(17.0, zr[1], zr[2]) + cyl(16.5, zr[2], zr[3]) + cyl(17.6, zr[3], zr[4] - 1.2)
         + cyl(18.2, zr[4] - 1.2, zr[4]))
    for k in range(30):
        L -= Pos(AX, AY, (zr[1] + zr[2]) / 2) * Rot(0, 0, k * 12.0) * Pos(17.0, 0, 0) * Box(1.8, 1.2, zr[2] - zr[1] - 1.6)
    for k in range(48):
        L -= Pos(AX, AY, zr[4] - 0.6) * Rot(0, 0, k * 7.5) * Pos(18.2, 0, 0) * Box(1.0, 0.8, 1.0)
    for k in range(13):
        a = math.radians(200 + k * 11.0)
        L += Pos(AX + 16.5 * math.cos(a), AY + 16.5 * math.sin(a), zr[3] - 2.2) * Rot(0, 0, math.degrees(a)) * Box(0.9, 0.7, 1.6 if k % 3 else 2.4, align=(Align.MIN, Align.CENTER, Align.MIN))
    L += Pos(AX, AY + 19.0, zr[0] + 0.4) * Box(1.0, 1.6, 1.2, align=MIN)
    for z0, z1, r in STEPS:
        L -= cyl(r, z0 - 0.01, z1 + 0.01)
    return L, zr[4]


def split_inner(shape, r_max, x=AX, y=AY):
    inner, outer = [], []
    for f in shape.faces():
        vs = f.vertices()
        rho = max(math.hypot(v.X - x, v.Y - y) for v in vs) if vs else 99.0
        (inner if rho <= r_max + 0.01 else outer).append(f)
    return Compound(inner), Compound(outer)


def lens_objects(dx=0.0):
    body = Pos(dx, 0, 0) * lens_body()
    barrel, _ = lens_barrel()
    barrel = Pos(dx, 0, 0) * barrel
    inner, outer = split_inner(barrel, 14.6, AX + dx, AY)
    objs = [D.obj_b3d(body, POD_COL, 0.12, model=True, tol=0.08),
            D.obj_b3d(outer, POD_COL, 0.14, model=True, tol=0.05, ang=0.12),
            D.obj_b3d(inner, BORE, 0.05, model=True, tol=0.05, ang=0.12)]
    objs.append(D.obj_b3d(Pos(AX + dx, AY, AP - 3.0) * Box(8.5, 8.5, 3.0, align=MIN), D.BLACK, 0.3, model=True, tol=0.05))
    objs.append(D.obj_b3d(cyl(2.6, AP, AP + 0.6, AX + dx), D.GLASS, 0.9, model=True))
    return objs


def lead_objects(dx=0.0):
    py, pz = PORT
    plug = bx(76.0, 95.0, py - 7.5, py + 7.5, pz - 4.0, pz + 4.0)
    ex = (AX + 23.0 + dx, AY - 13.5, CEIL + FLOOR + 3.0)                         # out of the slot in the grip-side wall
    pts = [(95.0, py, pz), (101.0, py, pz + 0.5), (105.5, py - 1.0, pz + 9.0), (106.0, -3.0, 44.0),
           (103.0, ex[1], 54.0), (ex[0] + 4.0, ex[1], ex[2]), ex]
    return [D.obj_b3d(plug, D.BLACK, 0.2, model=True, tol=0.2), D.tube(pts, 1.8, D.BLACK, model=True)]


def arrow(d, view, p0, p1, col=(200, 95, 10), w=7):
    a = view.px(D.to_world(np.array([p0])))[0][:2] / D.M.SS
    b = view.px(D.to_world(np.array([p1])))[0][:2] / D.M.SS
    d.line([tuple(a), tuple(b)], fill=(255, 255, 255), width=w + 6)
    d.line([tuple(a), tuple(b)], fill=col, width=w)
    v = (b - a) / (np.linalg.norm(b - a) + 1e-9); n = np.array([-v[1], v[0]])
    tip = [tuple(b + v * 6), tuple(b - v * 22 + n * 13), tuple(b - v * 22 - n * 13)]
    d.polygon(tip, fill=col, outline=(255, 255, 255))


def title(d, W, t, sub):
    f1, f2 = D.BOLD(40), D.REG(27)
    tw = max(d.textlength(t, font=f1), d.textlength(sub, font=f2))
    d.rounded_rectangle([14, 14, 14 + tw + 28, 116], radius=10, fill=(255, 255, 255), outline=D.INK, width=3)
    d.text((28, 20), t, font=f1, fill=D.INK)
    d.text((28, 72), sub, font=f2, fill=(80, 82, 86))


# ------------------------------------------------------------------ the cut through the screw (panel 4)
CUT_X = SCREW[0]


def cut_objects(deck_solids):
    """Everything cut at x = CUT_X, the part toward -x kept; cut faces drawn in their own colour."""
    keep = bx(CUT_X - 40, CUT_X, -40, 50, 34, 100)
    out = []
    items = [(s, D.CASE, (0.80, 0.80, 0.82)) for s in deck_solids] + [
        (base(), BASE_COL, (1.00, 0.80, 0.55)), (screw(), SCREW_COL, (0.95, 0.95, 0.97)),
        (lens_body(), POD_COL, (0.62, 0.74, 0.92)), (lens_barrel()[0], POD_COL, (0.62, 0.74, 0.92)),
        (Pos(AX, AY, AP - 7.6) * Box(38, 38, 1.6, align=MIN), (0.12, 0.40, 0.22), (0.35, 0.70, 0.45)),     # camera board (assumed)
        (Pos(AX, AY, AP - 6.0) * Box(8.5, 8.5, 6.0, align=MIN), D.BLACK, (0.25, 0.25, 0.27))]               # its lens block
    for s, col, cut_col in items:
        try:
            c = s & keep
        except Exception:
            continue
        if c is None or c.volume < 1e-3:
            continue
        cutf, rest = [], []
        for f in c.faces():
            cc = f.center()
            (cutf if abs(cc.X - CUT_X) < 1e-3 and abs(f.normal_at(cc).X) > 0.99 else rest).append(f)
        out.append(D.obj_b3d(Compound(rest), col, 0.12, model=True, tol=0.05, ang=0.12))
        if cutf:
            out.append(D.obj_b3d(Compound(cutf), cut_col, 0.0, model=True, tol=0.05, ang=0.12))
    return out


def deck_solids_near():
    sols = list(import_step(FD_STEP).solids())
    pick = lambda v: [s for s in sols if vmatch(s.volume, v)]
    return pick(115715.2078) + pick(23686.9156)                                  # body, back plate


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    deck = D.deck_objects()
    ground = [D.obj_b3d(D.box(-900, 900, -700, 1000, D.TOP - 2.0, D.TOP - 0.05), D.GROUND, 0.0, tol=1.0)]
    K = 0.5 if os.environ.get("HALF") else 1.0          # HALF=1: a quick half-size proof
    W, H = int(1000 * K), int(820 * K)
    lab = lambda d, v, p, xy, lines: D.label(d, v, tuple(D.to_world(np.array([p]))[0]), (xy[0] * K, xy[1] * K), lines)
    panels = []
    # 1: swap one screw (base and screw lifted off the back plate)
    LIFT_B, LIFT_S = 24.0, 50.0
    f1 = D.R @ (np.array([-0.62, 0.45, -0.62]) / np.linalg.norm([-0.62, 0.45, -0.62]))
    v1 = D.M.View(f1, D.R @ np.array([0.0, 0.0, 1.0]), D.to_world((68.0, 16.0, 70.0)), 8.0 * K, W, H)
    objs = deck + [D.obj_b3d(Pos(0, 0, LIFT_B) * base(), BASE_COL, 0.18, model=True, tol=0.05, ang=0.12),
                            D.obj_b3d(Pos(0, 0, LIFT_S) * screw(), SCREW_COL, 0.6, model=True, tol=0.05)]
    im = D.render(v1, objs, W, H).convert("RGB"); d = ImageDraw.Draw(im)
    title(d, W, "1  Swap one screw", "M3x8 out, the base on, an M3x10 back in")
    arrow(d, v1, (SCREW[0], SCREW[1], HEAD_SEAT + LIFT_S - 11), (SCREW[0], SCREW[1], HEAD_SEAT + LIFT_B + 3.5))
    arrow(d, v1, (B_X0 + 3, 16.0, FACE + LIFT_B - 2), (B_X0 + 3, 16.0, FACE + 2.0))
    lab(d, v1, (HEXMARK[0], HEXMARK[1], FACE - 0.3), (30, 600), ["Its pin goes in", "this hex mark"])
    lab(d, v1, (SCREW[0], SCREW[1] - 3.0, FACE - 0.8), (560, 640), ["Its spigot goes in", "the screw's seat"])
    panels.append(im); print("panel 1", flush=True)
    # 2: slide the lens on from the grip side
    DX = 36.0
    v2 = D.M.View((0.80, -1.0, -0.42), (0, 0, 1), D.to_world((AX + 20, AY, 62.0)), 5.4 * K, W, H)
    objs = ground + deck + [D.obj_b3d(base(), BASE_COL, 0.18, model=True, tol=0.05, ang=0.12),
                            D.obj_b3d(screw(), SCREW_COL, 0.6, model=True, tol=0.05)] + lens_objects(DX)
    im = D.render(v2, objs, W, H).convert("RGB"); d = ImageDraw.Draw(im)
    title(d, W, "2  Slide the lens on", "from the grip side, until it clicks")
    arrow(d, v2, (AX + DX + 26, AY - 27, 60.0), (AX + 8, AY - 27, 60.0))
    panels.append(im); print("panel 2", flush=True)
    # 3: fitted, lead plugged in
    v3 = D.M.View((0.80, -1.0, -0.42), (0, 0, 1), D.to_world((AX + 12, AY + 0, 58.0)), 6.0 * K, W, H)
    objs = ground + deck + [D.obj_b3d(base(), BASE_COL, 0.18, model=True, tol=0.05, ang=0.12)] + lens_objects(0.0) + lead_objects()
    im = D.render(v3, objs, W, H).convert("RGB"); d = ImageDraw.Draw(im)
    title(d, W, "3  Plug it in", "its lead into a USB port behind the grip")
    panels.append(im); print("panel 3", flush=True)
    # 4: the cut through the screw, seen from the grip side; the back of the deck down, the lens up
    cobjs = cut_objects(deck_solids_near())
    up = D.R @ np.array([0.0, 0.0, 1.0])
    f4 = D.R @ np.array([-1.0, 0.0, 0.0])
    v4 = D.M.View(f4, up, D.to_world((CUT_X, 12.0, 68.0)), 10.5 * K, W, H)
    im = D.render(v4, cobjs, W, H).convert("RGB"); d = ImageDraw.Draw(im)
    title(d, W, "How it holds", "cut through the screw, seen from the grip side")
    lab(d, v4, (CUT_X, 27.2, FACE + 2.6), (640, 170), ["Dovetail", "the lens can't lift off"])
    lab(d, v4, (CUT_X, 21.6, 52.0), (640, 600), ["Spigot", "in the screw's seat"])
    lab(d, v4, (CUT_X, SCREW[1] + 1.4, 46.5), (400, 730), ["M3x10: 6.5 mm into the body"])
    lab(d, v4, (CUT_X, 6.0, 55.5), (20, 560), ["Base (orange)"])
    lab(d, v4, (CUT_X, -14.5, 64.0), (20, 300), ["Lens body (blue)"])
    lab(d, v4, (CUT_X, 0.0, AP - 6.8), (20, 420), ["Camera board"])
    panels.append(im); print("panel 4", flush=True)
    g = 10
    out = Image.new("RGB", (2 * W + 3 * g, 2 * H + 3 * g + 64), (205, 205, 205))
    for k, im in enumerate(panels):
        out.paste(im, (g + (k % 2) * (W + g), g + (k // 2) * (H + g)))
    d = ImageDraw.Draw(out)
    d.rectangle([0, 2 * H + 3 * g, out.width, out.height], fill=(255, 255, 255))
    d.text((24, 2 * H + 3 * g + 14), "Concept only.  Orange = the new base.  Its pin sits in an armour hex mark, so it can't turn.  The deck is the real r9 model.",
           font=D.REG(27), fill=D.INK)
    out.save(OUT)
    print("wrote", OUT, out.size)
