"""NEXT CASE — three rough concepts (massing only, solid bodies, NOT printable parts).

Case coords (unchanged): x+ -> C side = ports = user's LEFT, y+ -> top, z=0 display back,
z+ -> case back. Viewer-right (facing x up = +z x +y) = -x  => the GRIP lives at x < 0.

All three share the constraints that killed earlier versions:
  * top ports (x -20..46, faces at y 30.1) and side ports (x 67.7, z 15..32) stay at the
    surface: the body hugs the stack there (R3 envelope), no full-width box (v3 / C1 lesson);
  * the bottom keeps the 12 deg stand plane;
  * the grip only uses the free D side (x -104..-34.7);
  * the front is the C1 FaceFrame, copied exactly, with armour added on the outside only.
Export is rotated for Fusion (Z-up): (X, Y, Z)_fusion = (-x, z, y)_case, so Fusion's
FRONT view shows the screen and the grip appears on the viewer's right.
"""
from build123d import *
import math, os
import c1_params as C
import r3_params as R

OUT = "/home/claude/fielddeck_redo/out/concepts"
os.makedirs(OUT, exist_ok=True)

STACK = R.STACK
BX, BY = R.BX, R.BY            # island envelope around the stack (-34.7..73.0, -80.1..34.1)
TAN = math.tan(math.radians(C.STAND_DEG))

def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0+x1)/2, (y0+y1)/2, (z0+z1)/2) * Box(x1-x0, y1-y0, z1-z0)

def stand_cutter():
    return Pos(0, C.Y_BOT, C.FRONT) * Rot(X=-C.STAND_DEG) * Pos(0, -250, 0) * Box(600, 500, 900)

def safe_fillet(shape, edges, r, tag=""):
    try:
        return fillet(edges, r)
    except Exception as e:
        print(f"  fillet skip {tag} r={r}: {str(e)[:60]}")
        return shape

def safe_chamfer(shape, edges, d, tag=""):
    try:
        return chamfer(edges, d)
    except Exception as e:
        print(f"  chamfer skip {tag} d={d}: {str(e)[:60]}")
        return shape

def hexbolt(cx, cy, z, af=5.5, h=1.2, up=+1):
    """hex head on a face whose outward normal is +z (up=+1) or -z (up=-1)."""
    r = af / math.sqrt(3)            # circumradius from across-flats
    hx = extrude(RegularPolygon(r, 6), amount=h)
    hx = Pos(cx, cy, z if up > 0 else z - h) * hx
    return hx

def plate(x0, x1, y0, y1, z, t=1.0):
    p = box(x0, x1, y0, y1, z, z + t)
    top = p.edges().group_by(Axis.Z)[-1]
    return safe_chamfer(p, top, 0.6, "plate")

def skirt():
    s = box(-C.X_OUT, C.X_OUT, C.Y_BOT, C.Y_TOPF, 0, R.SKIRT_Z)
    s = safe_fillet(s, s.edges().filter_by(Axis.Z), C.R_OUT, "skirt-xy")
    s = safe_fillet(s, s.edges().group_by(Axis.Z)[-1], 2.4, "skirt-top")
    return s

def port_cuts(depth_back):
    """keep the ports at the surface: top window over the 4 top ports, side bay for Eth/USB."""
    top = box(R.TOP_WIN["x"][0], R.TOP_WIN["x"][1], STACK["y"][1] - 2, BY[1] + 40,
              R.SKIRT_Z, R.TOP_WIN["z_top"])
    side = box(STACK["x"][1] + 1.0, 140, R.SIDE_WIN["y"][0], R.SIDE_WIN["y"][1] + 40,
               R.SIDE_WIN["z"][0], R.SIDE_WIN["z"][1])
    return top + side

# ------------------------------------------------------------------ front (same for all)
def armoured_front():
    f = import_step("/mnt/user-data/outputs/C1/C1-FaceFrame.step")
    z = C.FRONT                                  # outward normal is -z
    add = []
    pts = [(-98, 65.7), (98, 65.7), (-98, -66.5), (98, -66.5),        # corners
           (-50, 65.7), (0, 65.7), (50, 65.7),                         # top
           (-50, -76.0), (0, -76.0), (50, -76.0),                      # chin
           (-98, 0), (98, 0)]                                          # sides
    for (x, y) in pts:
        add.append(hexbolt(x, y, z, af=5.0, h=1.0, up=-1))
    for b in add:
        f = f + b
    # mitred corners + segment joints: 0.8 wide, 0.6 deep grooves in the front face
    g = []
    for sx in (1, -1):
        for sy, yy in ((1, (60.0, 71.5)), (-1, (-60.0, -88.0))):
            # diagonal from the aperture corner toward the outer corner
            x0, y0 = sx*92.0, yy[0]
            x1, y1 = sx*103.0, yy[1] if sy > 0 else -82.0
            L = math.hypot(x1-x0, y1-y0); ang = math.degrees(math.atan2(y1-y0, x1-x0))
            g.append(Pos((x0+x1)/2, (y0+y1)/2, z) * Rot(Z=ang) * Box(L, 0.8, 1.2))
    for x in (-75, -25, 25, 75):
        g.append(Pos(x, 66.0, z) * Box(0.8, 11.0, 1.2))
        g.append(Pos(x, -72.0, z) * Box(0.8, 22.0, 1.2))
    for sx in (1, -1):
        for y in (-30, 30):
            g.append(Pos(sx*98.0, y, z) * Box(11.0, 0.8, 1.2))
    for c in g:
        f = f - c
    return f

# ------------------------------------------------------------------ A: armoured pebble
# One continuous pebble: an L-shaped plan (tall on the grip side, low over the top ports)
# capped by one ellipsoid dome whose crown sits over the grip, so the grip is the thickest
# part and the dome falls away toward the port side. Stack corners stay >= 53 (stack 46).
EC = (-60.0, -10.0, -40.0); EA = (290.0, 260.0, 108.0)
def zsurf(x, y, grow=0.0):
    a, b, c = EA[0] + grow, EA[1] + grow, EA[2] + grow
    v = 1 - ((x - EC[0]) / a) ** 2 - ((y - EC[1]) / b) ** 2
    return EC[2] + c * math.sqrt(max(v, 0.0))
def ellipsoid(grow=0.0):
    # poles turned to +-y (far outside the part) and the seam to the equator (z=-40):
    # a pole at the crown made every later boolean on the dome fail silently
    return Pos(*EC) * scale(Rot(X=90) * Sphere(1.0), by=(EA[0] + grow, EA[1] + grow, EA[2] + grow))
def concept_a():
    pts = [(-C.X_OUT, -88), (BX[1], -88), (BX[1], BY[1]), (-30, BY[1]), (-30, 66), (-C.X_OUT, 66)]
    with BuildSketch() as sk:
        Polygon(*pts, align=None)
        fillet(sk.vertices(), radius=10)
    pebble = extrude(sk.sketch, amount=90) & ellipsoid()
    rim = [e for e in pebble.edges() if e.center().Z > 30 and e.geom_type != GeomType.LINE]
    pebble = safe_fillet(pebble, rim, 10, "A-dome-rim")
    body = skirt() + pebble
    body -= port_cuts(60.0)
    body -= box(-74, -46, 60, 70, 10, 34)                 # HUD window on the grip's top
    # conformal armour plates (1.0 mm proud, following the dome) + hex bolts
    # all >= 12 mm inside the outline: a plate crossing the rim fillet band would meet it near-tangent
    plates = [(-90, -44, -72, 52), (-24, 18, -4, 22), (22, 61, -4, 22), (-24, 61, -72, -10)]
    for (x0, x1, y0, y1) in plates:
        # embedded 1.5 mm below the dome so the fuse never meets coincident curved faces
        patch = (ellipsoid(1.0) & box(x0, x1, y0, y1, 20, 95)) - ellipsoid(-1.5)
        body = body + patch
        for (bx, by) in ((x0 + 4.5, y0 + 4.5), (x1 - 4.5, y0 + 4.5), (x0 + 4.5, y1 - 4.5), (x1 - 4.5, y1 - 4.5)):
            zt = zsurf(bx, by, 1.0)
            body = body + Pos(0, 0, -1.5) * hexbolt(bx, by, zt, af=5.5, h=2.5)
    body -= stand_cutter()
    return body

# ------------------------------------------------------------------ B: camera
def concept_b():
    island = box(BX[0], BX[1], BY[0], BY[1], 0, 54.0)
    island = safe_fillet(island, island.edges().filter_by(Axis.Z), 4, "B-island-v")
    island = safe_fillet(island, island.edges().group_by(Axis.Z)[-1], 3, "B-island-back")
    grip = box(-C.X_OUT, -34.7, -88.0, C.Y_TOPF, 0, 74.0)
    grip = safe_fillet(grip, grip.edges().filter_by(Axis.Z), 12, "B-grip-v")
    grip = safe_fillet(grip, grip.edges().group_by(Axis.Z)[-1], 9, "B-grip-back")
    body = skirt() + island + grip
    # finger groove on the grip's inner face, where the fingers wrap toward the lens
    body -= Pos(-34.7, -8, 62) * Rot(X=90) * Cylinder(9.0, 120)
    body -= port_cuts(54.0)
    # lens on the back, centred on the stack
    lc = ((STACK["x"][0] + STACK["x"][1]) / 2, (STACK["y"][0] + STACK["y"][1]) / 2)   # (18.5, -23)
    lens = Pos(lc[0], lc[1], 54.0) * Cylinder(42.0, 10.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    lens -= Pos(lc[0], lc[1], 59.0) * Cylinder(33.0, 10.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    for zr in (56.0, 58.0):                                  # two grip rings on the barrel
        lens -= Pos(lc[0], lc[1], zr) * (Cylinder(43.0, 0.8) - Cylinder(41.4, 0.8))
    body = body + lens
    # top plate: HUD window, shutter button and a dial on the grip top (y = 71.5)
    yt = C.Y_TOPF
    body -= box(-66, -40, yt - 1.0, yt + 1, 8, 26)                                   # HUD window
    body = body + Pos(-78, yt, 56) * Rot(X=-90) * Cylinder(5.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    body = body + Pos(-92, yt, 36) * Rot(X=-90) * Cylinder(8.0, 5.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # armour panel replaces the leatherette on the grip's outer back
    body = body + plate(-96, -48, -66, 52, 74.0)
    for (bx, by) in ((-92, -62), (-52, -62), (-92, 48), (-52, 48)):
        body = body + hexbolt(bx, by, 75.0)
    body -= stand_cutter()
    return body

# ------------------------------------------------------------------ C: tape recorder
def concept_c():
    island = box(BX[0], BX[1], BY[0], BY[1], 0, 52.0)
    island = safe_chamfer(island, island.edges().group_by(Axis.Z)[-1], 5.0, "C-island-back")
    grip = box(-C.X_OUT, -34.7, -88.0, C.Y_TOPF, 0, 58.0)
    grip = safe_chamfer(grip, grip.edges().group_by(Axis.Z)[-1], 6.0, "C-grip-back")
    body = skirt() + island + grip
    # grip ridge along the outer edge (solid, no handle loop -> no bridge to print)
    ridge = box(-C.X_OUT + 2, -C.X_OUT + 16, -70, 50, 0, 66.0)
    ridge = safe_fillet(ridge, ridge.edges().group_by(Axis.Z)[-1], 6.0, "C-ridge")
    body = body + ridge
    body -= port_cuts(52.0)
    # cassette door on the island back with two reels
    cx, cy = 19.0, -23.0
    door = Pos(cx, cy, 52.0) * Box(90, 56, 3.0)
    door = safe_fillet(door, door.edges().filter_by(Axis.Z), 6, "C-door")
    body -= door
    body = body + (Pos(cx, cy, 50.5) * Box(60, 14, 1.5))                                   # tape window
    for dx in (-22, 22):
        ring_ = Pos(cx + dx, cy, 50.5) * (Cylinder(11.0, 3.0) - Cylinder(6.0, 3.0))
        hub = Pos(cx + dx, cy, 50.5) * Cylinder(3.0, 3.0)
        body = body + ring_ + hub
    # speaker grille on the grip back: shallow dimples (not through)
    holes = []
    for ix in range(8):
        for iy in range(17):
            holes.append(Pos(-84 + ix * 6.0, -64 + iy * 6.4, 58.0) * Cylinder(1.6, 2.0))
    body -= Compound(holes)
    # piano keys + counter-window HUD on the grip top
    yt = C.Y_TOPF
    for i in range(3):
        x0 = -100 + i * 11.5
        body = body + box(x0, x0 + 10, yt, yt + 3.0, 24, 44)
    body -= box(-62, -38, yt - 1.0, yt + 1, 8, 26)
    # armour: corner bolts on both backs
    for (bx, by, zz) in ((-27, -72, 52.0), (66, -72, 52.0), (-27, 27, 52.0), (66, 27, 52.0),
                         (-84, -78, 58.0), (-44, -78, 58.0), (-84, 62, 58.0), (-44, 62, 58.0)):
        body = body + hexbolt(bx, by, zz)
    body -= stand_cutter()
    return body

def refs():
    stack = box(STACK["x"][0], STACK["x"][1], STACK["y"][0], STACK["y"][1], STACK["z"][0], STACK["z"][1])
    display = box(-94.7, 94.7, -60.1, 60.1, -8.6, 0.0)
    return stack, display

def to_fusion(s):
    # (X, Y, Z) = (-x, z, y): 180 deg about the (0,1,1) axis
    return s.rotate(Axis((0, 0, 0), (0, 1, 1)), 180)

if __name__ == "__main__":
    front = armoured_front()
    print("front", round(front.volume/1000, 1), "cm3")
    parts = {"front": front}
    for k, fn in (("A_pebble", concept_a), ("B_camera", concept_b), ("C_taperecorder", concept_c)):
        b = fn()
        print(k, "valid", b.is_valid, "vol", round(b.volume/1000, 1), "cm3",
              "bbox", [round(v, 1) for v in (b.bounding_box().min.X, b.bounding_box().min.Y, b.bounding_box().min.Z,
                                             b.bounding_box().max.X, b.bounding_box().max.Y, b.bounding_box().max.Z)])
        parts[k] = b
    stack, display = refs()
    parts["ref_stack"], parts["ref_display"] = stack, display
    # sanity: handedness of the grip before rotation
    a = parts["A_pebble"]
    left_vol = (a & box(-110, -40, -95, 80, 0, 80)).volume
    right_vol = (a & box(40, 110, -95, 80, 0, 80)).volume
    print("grip check (case coords): x<-40 vol", round(left_vol/1000, 1), " x>40 vol", round(right_vol/1000, 1))
    for k, s in parts.items():
        export_step(to_fusion(s), f"{OUT}/{k}.step")
    print("exported", sorted(os.listdir(OUT)))
