"""MK-I r9 - the inputs for building the HUD in Fusion (2026-10-12): the cloud trial's tool solids (mk1_hud_r9.py), each as
its own STEP in case coordinates (mm), the new cap, the real OLED board as reference pieces, and the numbers Fusion's
scripts check against (each tool's solids, volume and box; the body's volume change at each step; probe points that are
solid / empty in the body before and after, checked here on the trial).
  python3 mk1_hud_r9_fusion_inputs.py   -> out/mk1/r9_fusion/*.step + r9_fusion_numbers.json
NOTE: a STEP file's header carries the time it was written, so every run gives new md5s - the Fusion scripts (h1, h2) check
the md5s of the files they were made with (the run of 2026-10-12 09:4x UTC); after a re-run, regenerate them."""
import json, os, hashlib
from build123d import export_step, Compound, Vector
import mk1_hud_r9 as H

OUT = "out/mk1/r9_fusion"


def bake(s):
    """the shape's placement moved into its geometry (identity location): a located solid (a plain fbox) is written as a
    one-part ASSEMBLY otherwise, and Fusion imports it as a moved sub-occurrence (h1 stopped on 2_tube_cut.step, 2026-10-12)"""
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
    from OCP.TopLoc import TopLoc_Location
    from build123d import Solid
    out = []
    for x in s.solids():
        w = x.wrapped
        out.append(Solid(BRepBuilderAPI_Transform(w.Located(TopLoc_Location()), w.Location().Transformation(), True).Shape()))
    return out[0] if len(out) == 1 else Compound(out)


def bbox(s):
    b = s.bounding_box()
    return [round(v, 4) for v in (b.min.X, b.min.Y, b.min.Z, b.max.X, b.max.Y, b.max.Z)]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    P = H.load()
    b0 = P["body"]
    TL = H.tools()
    b1, steps = H.new_body(b0, TL)
    c1 = H.new_cap()
    num = dict(body_start=round(b0.volume, 4), steps=[], cap=None, oled=None, probes=[])
    last = b0.volume
    for i, (nm, op, s) in enumerate(TL):
        fn = "%d_%s_%s.step" % (i + 1, nm, op)
        export_step(bake(s), os.path.join(OUT, fn))
        sols = s.solids()
        num["steps"].append(dict(file=fn, name=nm, op=op, solids=len(sols), volume=round(s.volume, 4), box=bbox(s),
                                 solid_volumes=sorted(round(x.volume, 4) for x in sols),
                                 change=round(steps[nm] - last, 4), body_after=round(steps[nm], 4)))
        last = steps[nm]
    export_step(c1, os.path.join(OUT, "9_hudcap_r9.step"))
    num["cap"] = dict(file="9_hudcap_r9.step", volume=round(c1.volume, 4), box=bbox(c1), faces=len(c1.faces()))
    pieces = H.board()
    names = dict(pcb="PCB 27.3 x 27.6 x 1.66 (IMG_2095)", glass="Glass 26.7 x 19.48 x 1.45", flex="Display flex round the lower edge (allowance)",
                 joints="Four solder joints on the front (allowance 2.0 high)", plugs="Four plugs on the header (allowance, 20 from the PCB front)")
    export_step(Compound([s for _, s in pieces]), os.path.join(OUT, "10_oled_real_ref.step"))        # one file, five solids
    num["oled"] = dict(file="10_oled_real_ref.step", solids=[dict(name=names[nm], volume=round(s.volume, 4)) for nm, s in pieces])
    W = H.W
    probes = [("window, through the skin", W(76.5, 18.5, 0.5)), ("glass pocket", W(76.5, 18.5, 1.5)), ("lip over the window", W(76.5, 26.3, 0.5)),
              ("the chin's flat cut", W(76.5, 25.3, 0.3)), ("solder-joint relief", W(76.5, 29.0, 2.0)), ("skin over the relief", W(76.5, 30.0, 0.5)),
              ("new tube, top end", W(76.5, 30.9, 10.0)), ("new tube top wall", W(76.5, 32.5, 10.0)), ("brow, the new 1.0", W(76.5, 37.7, 30.0)),
              ("old window, filled", W(76.5, 9.0, 0.5)), ("old pilot, filled", W(66.0, 4.5, 1.5)), ("new pilot, lower inner", W(64.82, 4.62, 2.5)),
              ("new pilot, upper handle side", W(88.18, 28.42, 3.0)), ("new post, lower inner", W(65.82, 4.62, 3.5)),
              ("new post, upper handle side", W(87.18, 28.42, 3.5)), ("lower post's foot", W(64.82, 2.0, 3.5)), ("tube 0.4 wider", W(62.3, 15.0, 10.0)),
              ("side wall", W(61.9, 15.0, 10.0)), ("tube middle", W(76.5, 15.0, 10.0)), ("facet wall below the window", W(76.5, 4.0, 1.2))]
    for nm, p in probes:
        num["probes"].append(dict(name=nm, point=[round(p.X, 5), round(p.Y, 5), round(p.Z, 5)], before=0 if b0.is_inside(p) else 2,
                                  after=0 if b1.is_inside(p) else 2))
    num["body_end"] = round(b1.volume, 4)
    num["body_end_faces"] = len(b1.faces())
    json.dump(num, open(os.path.join(OUT, "r9_fusion_numbers.json"), "w"), indent=1)
    for f in sorted(os.listdir(OUT)):
        print("%-40s %s" % (f, hashlib.md5(open(os.path.join(OUT, f), "rb").read()).hexdigest()))
    print(json.dumps(num, indent=1)[:6000])
