"""MK-I BODY r4 + HUD CAP r4 = r3's parts, unchanged in shape and function, with the ARMOUR cut
into the outside (mk1_armour_r4.py). Nothing is added: every clearance of r3 still holds.
The cap gets a fourth "bolt" at the corner that cannot carry a real screw (see r3): a ring groove
round a flush island with a hex socket, so the cap reads as a four-bolt plate."""
from build123d import *
import math, time
import r3_params as R
import mk1_body_r3 as B3
import mk1_armour_r4 as AR
from mk1_body_r3 import export_clean_stl, cap_for_print

DUMMY = dict(ring_out=6.4, ring_in=5.2, ring_deep=1.0, hex_af=2.0, hex_deep=0.6)


def armour_cutters():
    out = []
    for name in AR.FACES:
        pocket, hexes = AR.face_cutters(name)
        out.append((name, pocket, hexes))
    return out


def body(verbose=False):
    p = B3.body()
    for name, pocket, hexes in armour_cutters():
        t = time.time()
        p -= pocket
        if hexes is not None:
            p -= hexes
        if verbose:
            print("   %-3s cut in %.1f s  (valid %s, solids %d)" % (name, time.time() - t, p.is_valid, len(p.solids())), flush=True)
    return p


def hud_cap():
    q = B3.hud_cap()
    sx, a = B3.HUD_X - B3.CAP_SCREW_DX, B3.CAP_SCREW_A[0]          # the corner with no real screw
    top = B3.L_REAR + B3.CAP_T
    ring = B3.axis_cyl(sx, a, top - DUMMY["ring_deep"], top + 0.5, DUMMY["ring_out"] / 2) - \
           B3.axis_cyl(sx, a, top - DUMMY["ring_deep"] - 0.5, top + 1.0, DUMMY["ring_in"] / 2)
    q -= ring
    y, z = B3.facet_pt(a, top - DUMMY["hex_deep"])
    q -= Pos(sx, y, z) * Rot(X=R.FACET_DEG) * extrude(RegularPolygon(DUMMY["hex_af"] / math.sqrt(3), 6), amount=DUMMY["hex_deep"] + 0.5, dir=(0, 0, 1))
    return q


if __name__ == "__main__":
    import os
    os.makedirs("out/mk1", exist_ok=True)
    t0 = time.time()
    b = body(verbose=True)
    c = hud_cap()
    print("built in %.0f s" % (time.time() - t0))
    for nm, s in (("Body", b), ("HUD-Cap (in place)", c)):
        bb = s.bounding_box()
        print("%-20s valid %s  solids %d  vol %6.1f cm3  x %7.2f..%7.2f  y %7.2f..%7.2f  z %6.2f..%6.2f" % (
            nm, s.is_valid, len(s.solids()), s.volume/1000, bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z))
    cp = cap_for_print(c)
    export_step(b, "out/mk1/MK1-Body_r4.step"); print("  body STL: %d zero-area triangles dropped" % export_clean_stl(b, "out/mk1/MK1-Body_r4.stl"))
    export_step(cp, "out/mk1/MK1-HUD-Cap_r4.step"); print("  cap STL:  %d zero-area triangles dropped" % export_clean_stl(cp, "out/mk1/MK1-HUD-Cap_r4.stl"))
