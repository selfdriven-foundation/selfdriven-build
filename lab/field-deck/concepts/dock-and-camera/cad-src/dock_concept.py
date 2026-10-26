"""Field Deck - BASE DOCK + CAMERA POD: a CONCEPT picture for the owner (2026-10-21).
The deck is the real r9 model (Fusion read-back readback/item_r9_hud.step, version 12 = what he printed), stood on its own
12-degree stand face. Everything orange is a NEW print, drawn as plain blocks; nothing here is a print file.

World frame of this picture: X to the user's right, Y away from the user, Z up, desk at Z 0.
Model -> world: X = -x, Y = sin12*y + cos12*z + DY, Z = cos12*y - sin12*z + 87.578 + TOP
(the stand face is the plane (0, -cos12, sin12) . p = 87.578 on the body, the front and the hump - found by dock/probe_stand.py).

Parts drawn from makers' figures (none measured here):
  Royal Kludge RK61 (owned)        289 x 103 x 39 (highgroundgaming review)
  Jaycar XC5941 hub (owned)        60 x 10 x 40, 200 mm lead (Jaycar)          - inside, not drawn
  RTL-SDR Blog V3 + dipole (owned) dipole base drawn 34 x 14 x 18 (guess), rods 130 (short rods fully out: 5-13 cm)
  Adafruit 3369 USB speaker        84 x 43 x 32 (Core Electronics)              - seen through the grille
  Arducam B0292 camera             board 38 x 38 (Arducam) -> pod 44 x 44 x 22
  python3 dock/dock_concept.py [OUT]"""
import sys, os, math
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont
from build123d import import_step, Box, Cylinder, Pos, Rot, chamfer, Axis
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mock_render as M
FD_STEP = os.environ.get("FD_STEP", "readback/item_r9_hud.step")   # the printed r9 read-back (Fusion v12); in the public
# repo use cad/MK1-r9_design_public_NOT-FOR-PRINT.step, whose body (the two names filled in) is 115741.7297 mm3
def vmatch(a, v):
    return abs(a - v) < 0.01 or (abs(v - 115715.2078) < 1e-6 and abs(a - 115741.7297) < 0.05)

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/dock/FieldDeck_dock_concept.png"
C12, S12 = math.cos(math.radians(12)), math.sin(math.radians(12))
TOP = 45.0                       # the dock's top face, where the deck's stand face sits
DY = 162.1                       # puts the front of the stand face at Y 132
R = np.array([[-1.0, 0, 0], [0, S12, C12], [0, C12, -S12]])
T = np.array([0.0, DY, 87.578 + TOP])

CASE = (0.25, 0.25, 0.27)
SCREEN = (0.10, 0.13, 0.21)
NEW = (0.95, 0.55, 0.13)
KBCASE, KEY, KEY2 = (0.20, 0.20, 0.22), (0.33, 0.33, 0.36), (0.62, 0.62, 0.65)
BLACK, METAL, GLASS = (0.07, 0.07, 0.08), (0.78, 0.80, 0.83), (0.05, 0.10, 0.25)
GROUND = (1.0, 1.0, 1.0)
BOLD = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)
REG = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", s)
INK, ORANGE = (30, 32, 36), (200, 95, 10)


def to_world(P):
    return np.asarray(P, float) @ R.T + T


def vfn(V, F):
    V = np.asarray(V, float); F = np.asarray(F, np.int64)
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    VN = np.zeros_like(V)
    for k in range(3):
        np.add.at(VN, F[:, k], n)
    VN /= np.linalg.norm(VN, axis=1, keepdims=True) + 1e-12
    return V, F, VN


def obj_b3d(shape, rgb, sp=0.1, model=False, tol=0.25, ang=0.25):
    V, F, VN = M.mesh(shape, tol, ang)
    if model:
        V = to_world(V); VN = VN @ R.T
    return (V, F, VN, rgb, sp)


def obj_tm(m, rgb, sp=0.1, model=False, smooth=False):
    V, F = np.asarray(m.vertices, float), np.asarray(m.faces, np.int64)
    if model:
        V = to_world(V)
    if smooth:
        V, F, VN = vfn(V, F)
    else:                                   # flat shading: split the vertices per face
        V = V[F].reshape(-1, 3); F = np.arange(len(V)).reshape(-1, 3)
        n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        VN = np.repeat(n, 3, axis=0)
    return (V, F, VN, rgb, sp)


def tube(pts, r, rgb, sp=0.15, model=False, sections=14):
    pts = [np.asarray(p, float) for p in pts]
    if model:
        pts = [to_world(p) for p in pts]
    parts = []
    for a, b in zip(pts[:-1], pts[1:]):
        if np.linalg.norm(b - a) > 1e-6:
            parts.append(trimesh.creation.cylinder(radius=r, segment=[a, b], sections=sections))
    for p in pts[1:-1]:
        s = trimesh.creation.icosphere(subdivisions=2, radius=r); s.apply_translation(p); parts.append(s)
    return obj_tm(trimesh.util.concatenate(parts), rgb, sp, smooth=True)


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# ------------------------------------------------------------------ the deck (r9, as printed)
def deck_objects():
    sols = list(import_step(FD_STEP).solids())
    def pick(v):
        m = [s for s in sols if vmatch(s.volume, v)]
        return m
    objs = []
    for v, col, sp in ((115715.2078, CASE, 0.12), (129177.2313, CASE, 0.12), (96836.0778, CASE, 0.12),
                       (23686.9156, CASE, 0.12), (3782.2976, CASE, 0.12), (11190.0952, CASE, 0.12),
                       (195786.5680, SCREEN, 0.7), (40.8281, BLACK, 0.4), (91.4074, BLACK, 0.4),
                       (1059.4635, (0.30, 0.30, 0.32), 0.2), (1088.7435, (0.05, 0.05, 0.06), 0.5),
                       (1250.7768, (0.08, 0.20, 0.10), 0.2)):
        for s in pick(v):
            objs.append(obj_b3d(s, col, sp, model=True))
    return objs


# ------------------------------------------------------------------ the dock (new print, concept blocks)
X0, X1 = -152.0, 152.0           # base ends (the grip overhangs the left end by 12)
YK, YS, YB = 109.0, 109.0, 226.0 # keyboard well back, spine front, spine back
KNOB = (128.0, 136.0)
MAST = (134.0, 212.0, 172.0)     # x, y, top of the mast


def dock_objects():
    objs = []
    tray = box(X0, X1, 0, YK, 0, 3) + box(X0, X1, 0, 3, 0, 10) + box(X0, -146, 0, YK, 0, 12) + box(146, X1, 0, YK, 0, 12)
    sp = box(X0, X1, YS, YB, 0, TOP)
    sp = chamfer(sp.edges().group_by(Axis.Z)[-1], 3.0)
    sp -= box(X0 + 3, X1 - 3, YS + 3, YB - 3, 3, TOP - 3)
    for k in range(25):                                       # grille slots over the speaker
        x = -54.0 + k * 4.5
        sp -= box(x, x + 2.2, 113.5, 125.5, TOP - 4, TOP + 1)
    sp -= Pos(KNOB[0], KNOB[1], TOP) * Cylinder(4.0, 10)      # knob shaft hole
    sp -= Pos(-128, 189, TOP) * Cylinder(5.0, 10)             # the deck lead comes up here
    sp -= box(-0.4, 0.4, YS - 1, YB + 1, TOP - 0.7, TOP + 1)  # the seam between the two halves
    sp -= box(-0.4, 0.4, YS - 1, YS + 0.7, 0, TOP + 1)
    tray -= box(-0.4, 0.4, -1, 0.7, 0, 11) + box(-0.4, 0.4, -1, YK + 1, 2.3, 4)
    lips = box(-100, 100, 127.5, 130.5, TOP, TOP + 3) + box(105, 108, 131, 152, TOP, TOP + 3)
    posts = box(-60, -48, 205.0, 215, TOP, 76) + box(4, 16, 205.0, 215, TOP, 76)
    sock = Pos(MAST[0], MAST[1], TOP + 4) * Cylinder(11, 8)
    for s in (tray, sp, lips, posts, sock):
        objs.append(obj_b3d(s, NEW, 0.18, tol=0.15, ang=0.2))
    # the speaker under the grille (seen through the slots)
    objs.append(obj_b3d(box(-42, 42, 112.5, 130, 8, TOP - 3.2), BLACK, 0.1))
    # knob: printed cap, 24 grooves, built at the origin then moved
    kn = Pos(0, 0, 7.5) * Cylinder(12, 15)
    for k in range(24):
        kn -= Rot(0, 0, k * 15.0) * Pos(12.3, 0, 7.5) * Box(1.6, 1.6, 16)
    kn -= Pos(0, 6.5, 15) * Box(1.6, 7, 2)
    objs.append(obj_b3d(Pos(KNOB[0], KNOB[1], TOP) * kn, NEW, 0.25, tol=0.1, ang=0.15))
    objs.append(obj_b3d(Pos(KNOB[0], KNOB[1] + 6.5, TOP + 14.6) * Box(1.4, 6.6, 0.6), BLACK, 0.2))
    # mast + the SDR kit's dipole base + rods
    mx, my, mt = MAST
    objs.append(obj_b3d(Pos(mx, my, (TOP + 8 + mt) / 2) * Cylinder(7, mt - TOP - 8), NEW, 0.2, tol=0.1))
    objs.append(obj_b3d(box(mx - 17, mx + 17, my - 7, my + 7, mt, mt + 18), BLACK, 0.3))
    for sgn in (-1, 1):
        a = math.radians(32)
        base = np.array([mx + sgn * 12, my, mt + 18])
        d = np.array([sgn * math.sin(a), 0, math.cos(a)])
        segs = [(0, 40, 2.6), (38, 72, 2.0), (70, 100, 1.4)]
        for s0, s1, rr in segs:
            objs.append(tube([base + d * s0, base + d * s1], rr, METAL, 0.6))
        objs.append(tube([base + d * 99, base + d * 101], 2.2, METAL, 0.6))
    return objs


# ------------------------------------------------------------------ the RK61 (owned) - a mock-up
ROWS = [[1] * 13 + [2], [1.5] + [1] * 12 + [1.5], [1.75] + [1] * 11 + [2.25], [2.25] + [1] * 10 + [2.75],
        [1.25, 1.25, 1.25, 6.25, 1.25, 1.25, 1.25, 1.25]]


def keyboard_objects():
    U = 19.05
    yf, yb = 4.5, 107.5
    hf, hb = 17.0, 25.0                                      # case height front / back (keycaps sit on top)
    pts = []
    for x in (-144.5, 144.5):
        pts += [(x, yf, 3), (x, yb, 3), (x, yf, 3 + hf), (x, yb, 3 + hb)]
    case = trimesh.convex.convex_hull(np.array(pts, float))
    objs = [obj_tm(case, KBCASE, 0.15)]
    slope = math.atan((hb - hf) / (yb - yf))
    caps = []
    accents = []
    for r, row in enumerate(ROWS):
        x = -7.5 * U
        yc = yf + 3.9 + U / 2 + (4 - r) * U
        for k, w in enumerate(row):
            cx = x + w * U / 2
            zc = 3 + hf + (yc - yf) * math.tan(slope) + 4.5
            b = trimesh.creation.box(extents=(w * U - 1.6, U - 1.6, 9.0))
            b.apply_transform(trimesh.transformations.rotation_matrix(slope, (1, 0, 0)))
            b.apply_translation((cx, yc, zc))
            (accents if (r == 0 and k == 0) or (r == 2 and k == len(row) - 1) else caps).append(b)
            x += w * U
    objs.append(obj_tm(trimesh.util.concatenate(caps), KEY, 0.2))
    objs.append(obj_tm(trimesh.util.concatenate(accents), KEY2, 0.2))
    return objs


# ------------------------------------------------------------------ the camera pod (new print) on the back plate
POD = (51.0, 95.0, -17.0, 27.0, 55.0, 77.0)     # model x, y, z


def pod_objects():
    x0, x1, y0, y1, z0, z1 = POD
    objs = []
    plate = box(x0 - 3, x1 + 3, y0 - 3, min(y1 + 3, 28.6), 53.05, 55.0)
    pod = box(x0, x1, y0, y1, z0, z1)
    pod = chamfer(pod.edges().group_by(Axis.Z)[-1], 3.0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    objs.append(obj_b3d(plate, NEW, 0.18, model=True, tol=0.1))
    objs.append(obj_b3d(pod, NEW, 0.18, model=True, tol=0.1))
    objs.append(obj_b3d(Pos(cx, cy, z1 + 2.5) * Cylinder(8.5, 5), BLACK, 0.3, model=True, tol=0.05))
    objs.append(obj_b3d(Pos(cx, cy, z1 + 5.05) * Cylinder(5.5, 0.4), GLASS, 0.9, model=True, tol=0.05))
    return objs


def cables():
    objs = []
    # dock -> deck: the hub's own 200 mm lead, into the black port nearest the back (Pi 5 port at model y -17.9, z 26.7)
    p = lambda x, y, z: to_world((x, y, z))
    objs.append(obj_b3d(box(-90, -68, 184.5 - 4, 184.5 + 4, 109.5 - 7.5, 109.5 + 7.5), BLACK, 0.2))
    objs.append(tube([(-90, 184.5, 109.5), (-112, 184.5, 109.5), (-121, 186, 101), (-126, 188, 84), (-128, 189, 62),
                      (-128, 189, TOP - 2)], 2.0, BLACK))
    # camera lead: pod -> the other port pair (model y -1.1)
    objs.append(tube([(95.5, 8, 70), (101, 6, 66), (106.5, 3, 56), (108, -1.1, 40), (108, -1.1, 28), (100, -1.1, 26.7)],
                     1.8, BLACK, model=True))
    # charger: into the X1201's USB-C at the top (model x 30.7, y 30.1, z 35.5), up and over the back to the wall
    plug_lo, plug_hi = to_world((30.7, 36.0, 35.5)), to_world((30.7, 58.0, 35.5))
    objs.append(tube([plug_lo, plug_hi], 4.6, BLACK, 0.2, sections=8))
    top = to_world((30.7, 64.0, 37.0))
    yb = YB + 12.0
    objs.append(tube([plug_hi, top, top + np.array([0, 12, 3]), np.array([top[0], yb - 6, top[2] - 6]),
                      np.array([top[0], yb, top[2] - 30]), np.array([top[0], yb, 12.0]), np.array([top[0], yb + 6, 2.0]),
                      np.array([top[0], yb + 150, 2.0])], 1.9, BLACK))
    return objs


def ground():
    g = box(-900, 900, -700, 1000, -2.0, -0.05)
    return [obj_b3d(g, GROUND, 0.0, tol=1.0)]


def render(view, objs, W, H):
    img = M.shade(view, *M.raster(view, objs))
    im = Image.fromarray((img * 255).astype(np.uint8))
    return im.resize((W, H), Image.LANCZOS)


def label(d, view, anchor, text_xy, lines, col=INK, dot=True):
    ax, ay = view.px(np.array([anchor]))[0][:2] / M.SS
    tx, ty = text_xy
    f1, f2 = BOLD(25), REG(21)
    w = max([d.textlength(lines[0], font=f1)] + [d.textlength(t, font=f2) for t in lines[1:]])
    bw, bh = w + 24, 38 + 27 * (len(lines) - 1)
    ex, ey = min(max(ax, tx), tx + bw), min(max(ay, ty), ty + bh)
    if (ex, ey) != (ax, ay):
        d.line([(ax, ay), (ex, ey)], fill=(255, 255, 255), width=8)
        d.line([(ax, ay), (ex, ey)], fill=col, width=3)
    if dot:
        d.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=(255, 255, 255))
        d.ellipse([ax - 6, ay - 6, ax + 6, ay + 6], fill=col)
    d.rounded_rectangle([tx, ty, tx + bw, ty + bh], radius=9, fill=(255, 255, 255), outline=col, width=3)
    d.text((tx + 12, ty + 5), lines[0], font=f1, fill=col)
    for k, t in enumerate(lines[1:]):
        d.text((tx + 12, ty + 36 + 27 * k), t, font=f2, fill=(70, 72, 76))


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    objs = ground() + deck_objects() + dock_objects() + keyboard_objects() + pod_objects() + cables()
    print("objects", len(objs), "triangles", sum(len(o[1]) for o in objs), flush=True)
    W, H = 1250, 980
    # A: from the front right
    vA = M.View((-0.62, 1.0, -0.66), (0, 0, 1), (8, 118, 128), 2.3, W, H)
    imA = render(vA, objs, W, H).convert("RGB")
    dA = ImageDraw.Draw(imA)
    label(dA, vA, (-150, 60, 34), (18, 610), ["Your RK61 keyboard", "drops in, lifts out"])
    label(dA, vA, (KNOB[0], KNOB[1], TOP + 15), (930, 720), ["Knob (your EC11)", "volume, HUD pages,", "tuning, push-to-talk"])
    rod = np.array([MAST[0] + 12, MAST[1], MAST[2] + 18]) + 55 * np.array([math.sin(math.radians(32)), 0, math.cos(math.radians(32))])
    label(dA, vA, tuple(rod), (900, 110), ["Antenna", "your SDR kit's dipole"])
    label(dA, vA, (-20, 119, TOP), (300, 835), ["Speaker", "USB speaker under the grille"])
    label(dA, vA, (60, 150, TOP + 3), (700, 860), ["Hub, radio, knob board", "inside the base"])
    dA.text((18, 18), "Docked", font=BOLD(38), fill=INK)
    dA.text((18, 66), "front", font=REG(26), fill=(90, 92, 96))
    print("view A done", flush=True)
    # B: from behind, grip side
    vB = M.View((0.70, -1.0, -0.55), (0, 0, 1), (-20, 150, 128), 2.3, W, H)
    imB = render(vB, objs, W, H).convert("RGB")
    dB = ImageDraw.Draw(imB)
    cam = to_world(((POD[0] + POD[1]) / 2, (POD[2] + POD[3]) / 2, POD[5] + 4))
    label(dB, vB, tuple(cam), (40, 120), ["Camera pod", "slides on, looks backwards", "stays on when undocked"])
    label(dB, vB, (-126, 188, 84), (905, 690), ["One USB lead", "into the port", "behind the grip"])
    chg = to_world((30.7, 64.0, 37.0)) + np.array([0, 30, 2])
    label(dB, vB, tuple(chg), (700, 90), ["Charger", "top, as now"])
    label(dB, vB, (-150, 150, 160), (940, 470), ["Lift off", "by the grip"], dot=False)
    dB.text((18, 18), "Docked", font=BOLD(38), fill=INK)
    dB.text((18, 66), "back", font=REG(26), fill=(90, 92, 96))
    print("view B done", flush=True)
    g = 10
    out = Image.new("RGB", (2 * W + 3 * g, H + 2 * g + 70), (205, 205, 205))
    out.paste(imA, (g, g)); out.paste(imB, (2 * g + W, g))
    d = ImageDraw.Draw(out)
    d.rectangle([0, H + 2 * g, out.width, out.height], fill=(255, 255, 255))
    d.text((24, H + 2 * g + 16), "Concept only.  Orange = new prints (base in 2 halves, mast, knob, camera pod).  The deck is the real r9 model.",
           font=REG(27), fill=INK)
    out.save(OUT)
    print("wrote", OUT, out.size)
