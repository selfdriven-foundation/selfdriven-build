"""MK-I r9 - THE PRINT FILES (2026-10-12), cut from FUSION's read-back of the final candidate (readback/item_r9_hud.step =
mk1/MK1_r9_hud_fusion_readback_item_NOT-FOR-PRINT.step, version 12 as saved), which passed mk1_final_r9_check.py (ALL CHECKS
PASS) and mk1_hud_r9_fusion_check.py. Each part lying as it prints (the orientations of the final check's section 4), its
lowest face at z 0, centred on x 0 / y 0, written as a cleaned watertight STL; then each file is READ BACK and checked
against its solid (volume, size, one closed mesh) - the file on disk is what is checked, not the solid.
The power lever is not here: it is the r8fix2 lever he printed and tried on 2026-10-09 (three printed, the same solid).
The retainer ring is the printed one, reused.
  python3 mk1_print_files_r9.py [OUTDIR]   -> MK1-r9-<part>_PRINT-THIS.stl + a picture of the parts as they lie"""
import sys, os, hashlib, tempfile
import numpy as np, trimesh
from build123d import import_step, Pos
from mk1_body_r3 import export_clean_stl, cap_for_print
import mk1_sound_r8 as S8

READBACK = "readback/item_r9_hud.step"
OUT = sys.argv[1] if len(sys.argv) > 1 else "out/mk1/print_r9"
# (file name, volume in the read-back, how it lies on the plate, what goes down)
PARTS = [("MK1-r9-Body_PRINT-THIS.stl", 115715.2078, lambda s: s, "the open front side (the skirt) down"),
         ("MK1-r9-Front_PRINT-THIS.stl", 129177.2313, lambda s: s, "the face (screen side) down"),
         ("MK1-r9-Handle_PRINT-THIS.stl", 96836.0778, lambda s: s, "as the file lies"),
         ("MK1-r9-BackPlate_PRINT-THIS.stl", 23686.9156, lambda s: s, "the inside down, the words up"),
         ("MK1-r9-HUD-Cap_PRINT-THIS.stl", 3782.2976, cap_for_print, "the inside down, the screw holes up"),
         ("MK1-r9-SpeakerCover_PRINT-THIS.stl", 11190.0952, S8.cover_for_print, "the roof down")]
FAILS = []


def expect(name, value, lo, hi, unit="   "):
    ok = (value == value) and lo <= value <= hi
    print("  %-100s %12.4f %s  %s" % (name, value, unit, "ok" if ok else "*** FAIL ***"), flush=True)
    if not ok:
        FAILS.append(name)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sols = list(import_step(READBACK).solids())
    print("THE PRINT FILES from %s (md5 %s)" % (READBACK, hashlib.md5(open(READBACK, "rb").read()).hexdigest()))
    rows, meshes = [], []
    for fn, v, orient, down in PARTS:
        m = [s for s in sols if abs(s.volume - v) < 0.01]
        expect("%s: one solid of %.4f mm3 in the read-back" % (fn, v), len(m), 1, 1)
        if len(m) != 1:
            continue
        s = orient(m[0])
        bb = s.bounding_box()
        s = Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * s
        p = os.path.join(OUT, fn)
        export_clean_stl(s, p)
        mm = trimesh.load(p, force="mesh", process=False); mm.merge_vertices()
        ex = mm.bounds[1] - mm.bounds[0]
        expect("  read back: one closed mesh (watertight, consistent, one piece)", 1.0 if (mm.is_watertight and mm.is_winding_consistent and len(mm.split(only_watertight=False)) == 1) else 0.0, 1, 1)
        expect("  read back: mesh volume against the solid's (relative)", abs(mm.volume - v) / v, 0, 2e-3)
        expect("  read back: lowest point on the plate (z)", mm.bounds[0][2], -1e-6, 1e-6, "mm ")
        expect("  read back: fits the Bambu A1 (256 x 256 x 256): largest side", max(ex), 0, 256, "mm ")
        md = hashlib.md5(open(p, "rb").read()).hexdigest()
        rows.append((fn, ex, v * 1.27e-3, down, md, os.path.getsize(p)))
        meshes.append((fn, mm))
    print("\n  %-38s %-24s %8s  %-38s %s" % ("file", "size on the plate (mm)", "PETG", "lies", "md5"))
    for fn, ex, g, down, md, sz in rows:
        print("  %-38s %6.1f x %6.1f x %5.1f  %6.1f g  %-38s %s" % (fn, ex[0], ex[1], ex[2], g, down, md))
    # ---- a picture: each part as it lies on the plate, seen from above at an angle
    try:
        from PIL import Image, ImageDraw, ImageFont
        import mock_render as M
        BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        REG = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
        tiles = []
        for (fn, mm), (_, ex, g, down, md, sz) in zip(meshes, rows):
            V, F = np.asarray(mm.vertices), np.asarray(mm.faces)
            n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
            VN = np.zeros_like(V)
            for k in range(3):
                np.add.at(VN, F[:, k], n)
            VN /= np.linalg.norm(VN, axis=1, keepdims=True) + 1e-12
            W, Hh = 620, 470
            span = max(ex[0], ex[1], 1.0)
            s = 0.62 * W / (span * 1.15)
            v = M.View((-0.45, 0.55, -0.70), (0, 0, 1), (0, 0, ex[2] / 2), s, W, Hh)
            plate = trimesh.creation.box(bounds=[[-ex[0] / 2 - 6, -ex[1] / 2 - 6, -1.2], [ex[0] / 2 + 6, ex[1] / 2 + 6, -0.2]])
            PV, PF = np.asarray(plate.vertices), np.asarray(plate.faces)
            pn = np.cross(PV[PF[:, 1]] - PV[PF[:, 0]], PV[PF[:, 2]] - PV[PF[:, 0]])
            PVN = np.zeros_like(PV)
            for k in range(3):
                np.add.at(PVN, PF[:, k], pn)
            PVN /= np.linalg.norm(PVN, axis=1, keepdims=True) + 1e-12
            img = M.shade(v, *M.raster(v, [(PV, PF, PVN, (0.80, 0.78, 0.72), 0.0), (V, F, VN, (0.93, 0.47, 0.13), 0.05)]))
            im = Image.fromarray((img * 255).astype(np.uint8)).resize((W, Hh), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 0, W, 66], fill=(255, 255, 255))
            d.text((14, 6), fn.replace("_PRINT-THIS.stl", "").replace("MK1-r9-", ""), font=BOLD, fill=(0, 0, 0))
            d.text((14, 38), "%s  -  %.0f x %.0f x %.0f mm, %.0f g" % (down, ex[0], ex[1], ex[2], g), font=REG, fill=(90, 90, 90))
            tiles.append(im)
        g_ = 14
        cols = 3
        rows_n = (len(tiles) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (620 + g_) + g_, 70 + rows_n * (470 + g_) + g_), (236, 236, 233))
        dd = ImageDraw.Draw(sheet)
        dd.text((g_, 16), "MK-I r9 print files: each part as it lies on the plate (orange = the part, beige = the plate). Do not turn them.", font=BOLD, fill=(0, 0, 0))
        for i, t in enumerate(tiles):
            sheet.paste(t, (g_ + (i % cols) * (620 + g_), 70 + (i // cols) * (470 + g_)))
        pic = os.path.join(OUT, "MK1-r9_parts_as_they_lie.png")
        sheet.save(pic)
        print("\n  picture: %s (md5 %s)" % (pic, hashlib.md5(open(pic, "rb").read()).hexdigest()))
    except Exception as ex_:
        print("  (picture not made: %s)" % ex_)
    print("\n%s" % ("ALL CHECKS PASS" if not FAILS else "FAILED: %d -> %s" % (len(FAILS), FAILS)))
    sys.exit(1 if FAILS else 0)
