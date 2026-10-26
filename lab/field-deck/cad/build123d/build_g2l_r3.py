"""NEXT CASE — left side handle r3: r2's position and clearances, restyled.

Owner, 2026-10-01: "is the handle grip looking good? or adding any value? I am trying to get a
retro/vintage/sci-fi feel." r2 was a plain black tube on two plain arms — a bolted-on grab bar
that did not speak the armoured front's language.

r3 = the classic equipment handle, in the armour's language:
  * two flat, CHAMFERED BRACKETS flush with the frame face (plate edges + hex bolts, like the
    front), each ending in a collar round the grip with a bolt head on its end;
  * a RIBBED GRIP between them (the only rounded part). It is oval, 30 x 34, not round: the deck
    hangs off to one side of the hand, and a round bar would turn in the fist.
Unchanged from r2: left side (x+), arms above and below the port band, 30 mm finger gap, grip
length 108, grip back at z 10 so cables on the desk pass behind it.
Case coords: x+ = user's LEFT. Exported rotated for Fusion: (X, Y, Z) = (-x, z, y).
"""
from build123d import *
import math, os
import c1_params as C
import r3_params as R
from build_concepts import box, hexbolt, to_fusion, stand_cutter

OUT = "/home/claude/fielddeck_redo/out/grips"
os.makedirs(OUT, exist_ok=True)
REV = "r3"

GAP = 30.0                                        # clear finger gap, frame edge -> grip
A_RIB, B_RIB = 15.0, 17.0                         # grip half-sizes over the ribs: 30 wide (x), 34 deep (z)
RIB_H = 2.0                                       # rib height over the core
GRIP_X = C.X_OUT + GAP + A_RIB                    # 149
GRIP_Z = -7.0                                     # grip z -24..10: back stays in front of the cables (z 11+)
ARMS = ((40.0, 56.0), (-84.0, -68.0))             # y ranges, clear of the port band (-26..34.1)
ARM_X0 = 102.0                                    # 2 mm seat in the frame edge, clear of its rear bosses
ARM_Z = (C.FRONT, R.SKIRT_Z)                      # -11.6..7: flush with the frame face and the skirt back
A_COL, B_COL = A_RIB + 3.0, B_RIB + 3.0           # collar round each grip end
N_RIB, CREST = 11, 4.5                            # 11 flat-topped rings; sharp ridges looked like a bellows
FINGER = 22.0                                     # finger thickness + clearance round the grip
PLUGS = dict(x=(R.ETH_FACE_X, 112.0), y=(-26.0, 34.1), z=(11.0, 36.0))   # straight plugs incl. boots
CABLES_OUT = dict(x=(112.0, 200.0), y=(-26.0, 34.1), z=(11.0, 36.0))     # cables left sticking out

def oval(a, b, h):
    """oval prism along +y, from y = 0 to h (local)."""
    return Rot(X=-90) * extrude(Ellipse(a, b), amount=h)

def hex_y(af, h, sign):
    """hex head whose axis is y; sign +1 = sticks out toward +y."""
    p = extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h)
    return (Rot(X=-90) if sign > 0 else Rot(X=90)) * p

def try_chamfer(shape, edges, sizes):
    for d in sizes:
        try:
            return chamfer(edges, d)
        except Exception:
            pass
    print("  chamfer skipped")
    return shape

def brackets():
    out = None
    for (y0, y1) in ARMS:
        arm = box(ARM_X0, GRIP_X - A_RIB, y0, y1, ARM_Z[0], ARM_Z[1])
        arm = try_chamfer(arm, arm.edges().filter_by(Axis.X), (2.0, 1.5))
        col = Pos(GRIP_X, y0, GRIP_Z) * oval(A_COL, B_COL, y1 - y0)
        col = try_chamfer(col, col.edges().filter_by(GeomType.ELLIPSE), (2.0, 1.5))
        b = arm + col
        for x in (110.0, 121.0):                     # plate bolts on the front face, as on the frame
            b = b + hexbolt(x, (y0 + y1) / 2, ARM_Z[0], af=5.0, h=1.0, up=-1)
        out = b if out is None else out + b
    top, bot = ARMS[0][1], ARMS[1][0]                # a bolt head on each end of the grip
    out = out + Pos(GRIP_X, top - 0.5, GRIP_Z) * hex_y(9.0, 2.0, +1)
    out = out + Pos(GRIP_X, bot + 0.5, GRIP_Z) * hex_y(9.0, 2.0, -1)
    return out

def grip():
    y0, y1 = ARMS[1][1], ARMS[0][0]                  # -68..40
    a0, b0 = A_RIB - RIB_H, B_RIB - RIB_H            # core
    g = Pos(GRIP_X, y0 - 2.0, GRIP_Z) * oval(a0, b0, (y1 - y0) + 4.0)     # 2 mm into each collar
    n = N_RIB
    groove = ((y1 - y0) - n * CREST) / (n + 1)       # same groove at both ends and between rings
    ch = RIB_H + 0.5                                 # 45 deg flanks, rooted 0.5 inside the core
    w = CREST + 2 * ch
    secs = [(0.0, a0 - 0.5, b0 - 0.5), (ch, A_RIB, B_RIB), (w - ch, A_RIB, B_RIB), (w, a0 - 0.5, b0 - 0.5)]
    rib = Rot(X=-90) * loft([Pos(0, 0, z) * Ellipse(a, b) for (z, a, b) in secs], ruled=True)
    for k in range(n):
        g = g + Pos(GRIP_X, y0 + groove + k * (CREST + groove) - ch, GRIP_Z) * rib
    return g, n

def hand():
    """where the fingers go: 22 mm round the grip, between the brackets."""
    y0, y1 = ARMS[1][1], ARMS[0][0]
    ring = oval(A_RIB + FINGER, B_RIB + FINGER, y1 - y0) - oval(A_RIB, B_RIB, y1 - y0)
    return Pos(GRIP_X, y0, GRIP_Z) * ring

def zone(d):
    return box(d["x"][0], d["x"][1], d["y"][0], d["y"][1], d["z"][0], d["z"][1])

if __name__ == "__main__":
    case = to_fusion(import_step("/home/claude/fielddeck_redo/out/grips/G0_none_r1.step")).solids()[0]
    front = to_fusion(import_step("/home/claude/fielddeck_redo/out/concepts/front.step")).solids()[0]
    br = brackets()
    gr, n = grip()
    hd, plugs, tail = hand(), zone(PLUGS), zone(CABLES_OUT)
    for nm, s in (("brackets", br), ("grip", gr)):
        bb = s.bounding_box()
        print("%-9s valid %s  solids %d  vol %.1f cm3  x %.1f..%.1f  y %.1f..%.1f  z %.1f..%.1f" % (
            nm, s.is_valid, len(s.solids()), s.volume / 1000, bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z))
    print("ribs:", n, "| finger gap:", GRIP_X - A_RIB - C.X_OUT, "| grip length:", ARMS[0][0] - ARMS[1][1],
          "| grip", 2 * A_RIB, "x", 2 * B_RIB, "| sticks out past the frame:", GRIP_X + A_COL - C.X_OUT)
    both = br + gr
    print("handle into front frame :", round((br & front).volume, 1), "mm3 (the 2 mm seat only)")
    print("handle into back body   :", round((br & case).volume, 1), "mm3 (the 2 mm seat only)")
    print("handle vs plugs         :", round((both & plugs).volume, 1), "mm3 (must be 0)")
    print("handle vs cables on desk:", round((both & tail).volume, 1), "mm3 (must be 0: cables pass behind the grip)")
    print("handle below stand plane:", round((both & stand_cutter()).volume, 1), "mm3 (must be 0)")
    print("hand vs case            :", round((hd & case).volume + (hd & front).volume, 1), "mm3 (must be 0)")
    print("hand vs plugs           :", round((hd & plugs).volume, 1), "mm3 (must be 0)")
    print("hand vs cables sticking straight out:", round((hd & tail).volume / 1000, 1), "cm3 (>0: the clash when HOLDING it with a cable in)")
    export_step(to_fusion(br), f"{OUT}/G2L_brackets_{REV}.step")
    export_step(to_fusion(gr), f"{OUT}/G2L_grip_{REV}.step")
    export_step(to_fusion(hd), f"{OUT}/G2L_hand_{REV}.step")
    print("exported", REV)
