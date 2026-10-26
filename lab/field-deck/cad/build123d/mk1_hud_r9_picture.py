"""MK-I r9 - the HUD for the real OLED board: the picture for the owner (2026-10-12), made FROM THE SOLIDS
(the body read back from Fusion, readback/item_r8_vents.step, and the cloud's trial, mk1_hud_r9.py).
  top     the HUD window seen square on from outside (the board behind it drawn dashed): now | new
  bottom  a cut through the middle of the HUD (x 76.5), turned so the screen faces up: now | new
  python3 mk1_hud_r9_picture.py [OUT]"""
import sys, os, math, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
import trimesh
from shapely.geometry import Polygon
from build123d import Box, Pos, export_stl
import mock_render as M
import mk1_hud_r9 as H
import mk1_body_r3 as R3
import mk1_body_r4 as B4
from build_r3 import facet_pt, FDIR, FIN

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/mk1/MK1_r9_hud_proposal.png"
BOLD = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)
REG = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", s)
PLASTIC = (0.50, 0.52, 0.56)
ORANGE, RED, GREEN, INK = (214, 96, 16), (190, 20, 20), (20, 130, 60), "#1d1f22"
CLIP = Pos(76.5, 87.0, 27.5) * Box(43.0, 46.0, 61.0)          # x 55 .. 98, y 64 .. 110, z -3 .. 58: the pod


def shade_fine(view, depth, oid, nrm, base, shine, jump=0.25):
    img = M.shade(view, depth, oid, nrm, base, shine)
    dz = np.where(np.isinf(depth), 1e4, depth)
    e = np.zeros(oid.shape, bool)
    for ax in (0, 1):
        e |= (np.abs(dz - np.roll(dz, 1, ax)) > jump) & (oid >= 0)
    e[0, :] = e[:, 0] = False
    img[e] = img[e] * 0.35
    return img


def facet_view(body, title, new):
    W, Hh, s = 640, 760, 13.0
    v = M.View((0, FIN[0], FIN[1]), (0, FDIR[0], FDIR[1]), tuple(H.W(76.5, 17.0, 0.0)), s, W, Hh)
    clip = body & CLIP
    img = shade_fine(v, *M.raster(v, [M.mesh(clip, 0.03, 0.1) + (PLASTIC, 0.05)]))
    im = Image.fromarray((img * 255).astype(np.uint8)).resize((W, Hh), Image.LANCZOS).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    P = lambda x, a, dp=4.2: tuple(v.px(np.array([list(H.W(x, a, dp))]))[0][:2] / M.SS)

    def rect(x0, x1, a0, a1, **kw):
        pts = [P(x0, a0), P(x1, a0), P(x1, a1), P(x0, a1)]
        d.polygon(pts, **kw)

    def dashed(x0, x1, a0, a1, col, w=3, dash=10):
        pts = [P(x0, a0), P(x1, a0), P(x1, a1), P(x0, a1), P(x0, a0)]
        for p, q in zip(pts[:-1], pts[1:]):
            L = math.hypot(q[0] - p[0], q[1] - p[1]); n = max(1, int(L / dash))
            for k in range(0, n, 2):
                t0, t1 = k / n, min(1.0, (k + 1) / n)
                d.line([(p[0] + (q[0] - p[0]) * t0, p[1] + (q[1] - p[1]) * t0), (p[0] + (q[0] - p[0]) * t1, p[1] + (q[1] - p[1]) * t1)], fill=col, width=w)

    hx = H.HUD_X
    if new:
        hdr = H.HEADER_A
        dashed(hx - H.PCB[0] / 2, hx + H.PCB[0] / 2, hdr - H.PCB[1], hdr, GREEN + (255,))
        la0, la1 = H.LIT_A
        yb = la1 - 16 * 0.1698                                   # the yellow band: the top 16 rows (header side)
        rect(hx - H.LIT[0] / 2, hx + H.LIT[0] / 2, la0, yb, fill=(40, 170, 230, 150))
        rect(hx - H.LIT[0] / 2, hx + H.LIT[0] / 2, yb, la1, fill=(250, 200, 30, 170))
        for x, a in H.POSTS:
            c = P(x, a)
            d.ellipse([c[0] - 13, c[1] - 13, c[0] + 13, c[1] + 13], outline=GREEN + (255,), width=4)
        for k in (-1.5, -0.5, 0.5, 1.5):
            c = P(hx + k * 2.54, hdr - 1.47)
            d.ellipse([c[0] - 6, c[1] - 6, c[0] + 6, c[1] + 6], fill=(200, 200, 200, 255), outline=(60, 60, 60, 255))
    else:
        dashed(hx - 25.66 / 2, hx + 25.66 / 2, 15.0 - 25.56 / 2, 15.0 + 25.56 / 2, (90, 90, 90, 255), w=3)
        dashed(hx - H.PCB[0] / 2, hx + H.PCB[0] / 2, 15.0 - H.PCB[1] / 2, 15.0 + H.PCB[1] / 2, RED + (255,), w=3)
        for sx in (-1, 1):
            for sa in (-1, 1):
                c = P(hx + sx * 10.5, 15.0 + sa * 10.5)
                d.ellipse([c[0] - 13, c[1] - 13, c[0] + 13, c[1] + 13], outline=(90, 90, 90, 255), width=4)
                q = P(hx + sx * H.HOLES[0] / 2, 15.0 + sa * H.HOLES[1] / 2)
                d.line([q[0] - 9, q[1] - 9, q[0] + 9, q[1] + 9], fill=RED + (255,), width=4)
                d.line([q[0] - 9, q[1] + 9, q[0] + 9, q[1] - 9], fill=RED + (255,), width=4)
    im = Image.alpha_composite(im, ov).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 64], fill=(255, 255, 255))
    d.text((16, 8), title, font=BOLD(30), fill=(0, 0, 0))
    d.text((16, 44), "the HUD window from outside; the board behind it dashed", font=REG(17), fill=(110, 110, 110), anchor="lm")
    if new:
        notes = [("real board 27.3 x 27.6 (dashed)", GREEN), ("window on the lit screen (yellow / blue)", (30, 110, 170)),
                 ("4 screw posts at the real holes", GREEN), ("room for the 4 solder blobs", (90, 90, 90))]
    else:
        notes = [("drawn for 25.7 x 25.6 (grey dashed)", (90, 90, 90)), ("real board 27.3 x 27.6: too big (red)", RED),
                 ("real holes (x) miss the posts (o)", RED)]
    y0 = Hh - 30 * len(notes) - 12
    d.rectangle([0, y0 - 8, W, Hh], fill=(255, 255, 255))
    for i, (t, c) in enumerate(notes):
        d.text((16, y0 + 30 * i), t, font=BOLD(21), fill=c)
    return im


def sections(b0, c0, b1, c1, path):
    """a cut through the middle of the HUD (x 76.5), TURNED so the screen faces up: across = along the screen (its lower
    edge on the left, the header edge on the right), down = into the HUD (the window at the top, the cap at the bottom)"""
    tmp = tempfile.mkdtemp(prefix="mk1_hud9pic_")
    clipf = R3.fbox(55.0, 98.0, -2.5, 41.0, -3.0, 40.0)

    def mesh_of(s_, nm):
        p = os.path.join(tmp, nm + ".stl"); export_stl(s_, p, tolerance=0.01, angular_tolerance=0.05)
        return trimesh.load(p, force="mesh")

    def cut(m, x=76.5):
        sec = m.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0])
        if sec is None:
            return []
        planar, T = sec.to_2D()
        out = []
        for p in planar.polygons_full:
            def tw(coords):
                q = np.array([[c[0], c[1], 0, 1] for c in coords]) @ np.asarray(T).T
                return [(lambda ad: (ad[0], -ad[1]))(R3.facet_ad(r[1], r[2])) for r in q]
            out.append(Polygon(tw(p.exterior.coords), [tw(k.coords) for k in p.interiors]))
        return out

    def draw(ax, polys, fc, ec=INK, lw=0.9, z=1, ls="-"):
        for p in polys:
            ax.add_patch(MPoly(list(p.exterior.coords), closed=True, fc=fc, ec=ec, lw=lw, zorder=z, ls=ls))
            for k in p.interiors:
                ax.add_patch(MPoly(list(k.coords), closed=True, fc="white", ec=ec, lw=lw, zorder=z + 0.1))

    fig, axs = plt.subplots(1, 2, figsize=(13.6, 7.4))
    fig.patch.set_facecolor("white")
    old_board = [("pcb", R3.fbox(76.5 - 25.66 / 2, 76.5 + 25.66 / 2, 15.0 - 25.56 / 2, 15.0 + 25.56 / 2, 4.2, 5.86))]
    cfg = [("cut through the HUD's middle - now", b0, c0, old_board, False), ("cut through the HUD's middle - new", b1, c1, H.board(), True)]
    col = dict(pcb="#2e8b57", glass="#222222", flex="#8a6d3b", joints="#b8b8b8", plugs="#4a4a4a")
    for ax, (t, b, c, brd, new) in zip(axs, cfg):
        draw(ax, cut(mesh_of(b & clipf, "b")), "#a7a297")
        draw(ax, cut(mesh_of(c, "c")), "#7f9fbf")
        for nm, s_ in brd:
            draw(ax, cut(mesh_of(s_, nm)), col[nm], lw=0.6, z=3)
        if not new:
            hdr = 15.0 + H.PCB[1] / 2
            real = [R3.fbox(76.5 - H.PCB[0] / 2, 76.5 + H.PCB[0] / 2, hdr - H.PCB[1], hdr, 4.2, 5.86),
                    R3.fbox(76.5 - 5.1, 76.5 + 5.1, hdr - 2.7, hdr - 0.3, 4.2 - 2.0, 4.2)]
            for k, r in enumerate(real):
                draw(ax, cut(mesh_of(r, "real%d" % k)), "none", ec="#be1414", lw=2.2, z=4, ls="--")
        ax.set_xlim(-3.5, 41.5); ax.set_ylim(-39.0, 7.0); ax.set_aspect("equal"); ax.grid(alpha=0.2)
        ax.set_title(t, fontsize=15, fontweight="bold", color=("#c25400" if new else INK))
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(-3.0, 6.0, "outside (you look in here)", fontsize=10.5, color="#555", va="center")
        ax.text(-3.0, -38.3, "inside the deck", fontsize=10.5, color="#555", va="center")
        ax.text(41.0, -38.3, "screen's top edge  >", fontsize=10.5, color="#555", va="center", ha="right")
    o = "#c25400"
    kw = dict(fontsize=12, color=o, arrowprops=dict(arrowstyle="->", color=o, lw=1.5), zorder=6)
    ax = axs[1]
    ax.annotate("window over the lit screen", xy=(18.5, 0.2), xytext=(9.0, 3.2), **kw)
    ax.annotate("window top flat\n(prints clean)", xy=(25.7, -0.4), xytext=(29.0, 2.6), **kw)
    ax.annotate("room for\nthe solder\nblobs", xy=(29.3, -3.1), xytext=(35.0, -10.5), **kw)
    ax.annotate("real board, header up", xy=(12.0, -5.0), xytext=(1.0, -13.5), **kw)
    ax.annotate("plugs + wires", xy=(28.6, -16.0), xytext=(13.0, -22.0), **kw)
    ax.annotate("pod 2.4 mm\nlonger", xy=(33.3, -15.5), xytext=(34.0, -22.0), **kw)
    ax.annotate("cap 1 mm longer", xy=(37.8, -35.8), xytext=(19.0, -31.5), **kw)
    r_ = "#be1414"
    kr = dict(fontsize=12, color=r_, arrowprops=dict(arrowstyle="->", color=r_, lw=1.5), zorder=6)
    ax = axs[0]
    ax.annotate("real board (red dashed):\nno room at the ends", xy=(28.6, -5.0), xytext=(4.0, -15.0), **kr)
    ax.annotate("its solder blobs\nwould hit the wall", xy=(26.0, -2.3), xytext=(27.0, -12.0), **kr)
    plt.tight_layout(); plt.savefig(path, dpi=100); plt.close(fig)


if __name__ == "__main__":
    P = H.load()
    b0, c0 = P["body"], P["cap"]
    b1, _ = H.new_body(b0)
    c1 = H.new_cap()
    imA = facet_view(b0, "HUD window - now", False)
    imB = facet_view(b1, "HUD window - new", True)
    tmp = tempfile.mkdtemp(prefix="mk1_hud9pic2_")
    sp = os.path.join(tmp, "sec.png")
    sections(b0, c0, b1, c1, sp)
    S = Image.open(sp).convert("RGB")
    g = 16
    top_w = imA.width + imB.width + g
    Wt = max(top_w, S.width) + 2 * g
    sheet = Image.new("RGB", (Wt, 70 + imA.height + g + S.height + 2 * g), (236, 236, 233))
    dd = ImageDraw.Draw(sheet)
    dd.text((g, 14), "MK-I r9: the HUD made for your real screen board (cloud trial, all checks pass)", font=BOLD(30), fill=(0, 0, 0))
    x0 = (Wt - top_w) // 2
    sheet.paste(imA, (x0, 70)); sheet.paste(imB, (x0 + imA.width + g, 70))
    sheet.paste(S, ((Wt - S.width) // 2, 70 + imA.height + g))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sheet.save(OUT)
    print("wrote", OUT, sheet.size)
