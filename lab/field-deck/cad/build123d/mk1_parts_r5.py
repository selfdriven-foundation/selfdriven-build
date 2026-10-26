"""MK-I r5 — the parts as they are printed.
  Body        mk1_body_r5.body at the chosen depth ("slim": the owner's pick, 2026-10-03) + the armour
  Back plate  mk1_body_r5.plate + the armour; exported lying on its inside face
  HUD cap     r4's cap, unchanged (exported again so that one revision is one complete set)
"""
from build123d import *
import time
import mk1_body_r5 as B5, mk1_armour_r5 as A5, mk1_body_r4 as B4
from mk1_body_r3 import export_clean_stl, cap_for_print

G = B5.Geo(B5.VARIANTS[B5.CHOSEN])


def body(verbose=False):
    return A5.armoured_body(G, verbose)


def plate():
    return A5.armoured_plate(G)


def hud_cap():
    return B4.hud_cap()


if __name__ == "__main__":
    import os
    os.makedirs("out/mk1", exist_ok=True)
    for f in ("MK1-Body_r5", "MK1-BackPlate_r5", "MK1-HUD-Cap_r5"):
        for ext in (".step", ".stl"):
            assert not os.path.exists("out/mk1/" + f + ext) or os.environ.get("OVERWRITE"), f + ext + " exists"
    t0 = time.time()
    b, q, c = body(verbose=True), plate(), hud_cap()
    print("built in %.0f s" % (time.time() - t0))
    for nm, s in (("Body", b), ("Back plate (in place)", q), ("HUD cap (in place)", c)):
        B5.report(nm, s)
    qp, cp = B5.plate_for_print(q, G), cap_for_print(c)
    bb = qp.bounding_box()
    print("Back plate on the bed: %.1f x %.1f x %.2f" % (bb.max.X - bb.min.X, bb.max.Y - bb.min.Y, bb.max.Z - bb.min.Z))
    for nm, s in (("Body", b), ("BackPlate", qp), ("HUD-Cap", cp)):
        export_step(s, "out/mk1/MK1-%s_r5.step" % nm)
        print("  %-9s STL: %d zero-area triangles dropped" % (nm, export_clean_stl(s, "out/mk1/MK1-%s_r5.stl" % nm)))
    print("PETG at 1.27 g/cm3: body %.0f g, back plate %.0f g, cap %.0f g" % (b.volume / 1000 * 1.27, q.volume / 1000 * 1.27, c.volume / 1000 * 1.27))
