"""Comparison pictures of the six style mock-ups (build_styles.py), all from one camera.
Same z-buffer renderer as render_g2l.py, plus a shine value per part (metal vs plastic).
"""
import math, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
import build_styles as S

SS = 2

def unit(a):
    a = np.asarray(a, float); return a / np.linalg.norm(a)

def mesh(shape, tol=0.12, ang=0.18):
    v, t = shape.tessellate(tol, ang)
    V = np.array([[p.X, p.Y, p.Z] for p in v], float); F = np.array(t, np.int64)
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    VN = np.zeros_like(V)
    for k in range(3):
        np.add.at(VN, F[:, k], n)
    VN /= np.linalg.norm(VN, axis=1, keepdims=True) + 1e-12
    return V, F, VN

class View:
    def __init__(self, f, up, center, scale, W, H):
        self.f = unit(f); self.r = unit(np.cross(self.f, up)); self.u = np.cross(self.r, self.f)
        self.c = np.asarray(center, float); self.s = scale * SS; self.W, self.H = W * SS, H * SS
    def px(self, P):
        P = np.atleast_2d(P) - self.c
        return np.column_stack([P @ self.r * self.s + self.W / 2, self.H / 2 - P @ self.u * self.s, P @ self.f])

def raster(view, objs):
    W, H = view.W, view.H
    depth = np.full((H, W), np.inf); oid = np.full((H, W), -1, np.int32)
    nrm = np.zeros((H, W, 3)); base = np.ones((H, W, 3)); shine = np.zeros((H, W))
    for k, (V, F, VN, rgb, sp) in enumerate(objs):
        Q = view.px(V)
        for tri in F:
            a, b, c = Q[tri]
            x0, x1 = max(int(math.floor(min(a[0], b[0], c[0]))), 0), min(int(math.ceil(max(a[0], b[0], c[0]))), W - 1)
            y0, y1 = max(int(math.floor(min(a[1], b[1], c[1]))), 0), min(int(math.ceil(max(a[1], b[1], c[1]))), H - 1)
            if x0 > x1 or y0 > y1:
                continue
            area = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
            if abs(area) < 1e-9:
                continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            w0 = ((b[0] - gx) * (c[1] - gy) - (c[0] - gx) * (b[1] - gy)) / area
            w1 = ((c[0] - gx) * (a[1] - gy) - (a[0] - gx) * (c[1] - gy)) / area
            w2 = 1.0 - w0 - w1
            m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            if not m.any():
                continue
            z = w0 * a[2] + w1 * b[2] + w2 * c[2]
            sub = depth[y0:y1 + 1, x0:x1 + 1]
            upd = m & (z < sub)
            if not upd.any():
                continue
            sub[upd] = z[upd]
            oid[y0:y1 + 1, x0:x1 + 1][upd] = k
            n = w0[..., None] * VN[tri[0]] + w1[..., None] * VN[tri[1]] + w2[..., None] * VN[tri[2]]
            nrm[y0:y1 + 1, x0:x1 + 1][upd] = n[upd]
            base[y0:y1 + 1, x0:x1 + 1][upd] = rgb
            shine[y0:y1 + 1, x0:x1 + 1][upd] = sp
    return depth, oid, nrm, base, shine

def shade(view, depth, oid, nrm, base, shine):
    n = nrm / (np.linalg.norm(nrm, axis=2, keepdims=True) + 1e-12)
    n[(n @ view.f) > 0] *= -1
    L = unit(-view.f + 0.65 * view.u + 0.45 * view.r); L2 = unit(-view.f - 0.3 * view.u - 0.6 * view.r)
    d = np.clip(n @ L, 0, 1); d2 = np.clip(n @ L2, 0, 1)
    spec = np.clip(n @ unit(L - view.f), 0, 1) ** 35
    img = base * (0.32 + 0.60 * d + 0.16 * d2)[..., None] + (0.10 + shine)[..., None] * spec[..., None]
    img[oid < 0] = 1.0
    e = np.zeros(oid.shape, bool)
    dz = np.where(np.isinf(depth), 1e4, depth)
    for ax in (0, 1):
        o1 = np.roll(oid, 1, ax); z1 = np.roll(dz, 1, ax); n1 = np.roll(n, 1, ax)
        e |= (oid != o1)
        e |= (np.abs(dz - z1) > 2.5) & (oid >= 0)
        e |= ((n * n1).sum(2) < math.cos(math.radians(32))) & (oid >= 0) & (o1 >= 0)
    e[0, :] = e[:, 0] = False
    e = e | np.roll(e, 1, 0) | np.roll(e, 1, 1)
    img[e] = img[e] * 0.28
    return np.clip(img, 0, 1)

def picture(parts, view):
    objs = [mesh(s) + (S.COL[c], S.SHINY.get(c, 0.0)) for _, s, c in parts]
    im = Image.fromarray((shade(view, *raster(view, objs)) * 255).astype(np.uint8))
    return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)

FRONT_LEFT = dict(f=-np.array((1.0, 0.55, -1.2)), c=(25.4, 5.7, 0.0), s=2.2)
BACK_LEFT = dict(f=-np.array((1.0, 0.62, 1.05)), c=(20.0, 5.0, 20.0), s=2.2)

def sheet(camera, path, W=820, H=640, cols=3):
    bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    panels = []
    for k, (code, name, fn) in enumerate(S.STYLES):
        im = picture(fn(), View(camera["f"], (0, 1, 0), camera["c"], camera["s"], W, H))
        dr = ImageDraw.Draw(im); cap = "%d  %s" % (k + 1, name)
        dr.rounded_rectangle([8, 8, 30 + dr.textlength(cap, font=bold), 54], radius=8, fill=(255, 255, 255), outline=(120, 120, 120))
        dr.text((18, 13), cap, font=bold, fill=(0, 0, 0))
        panels.append(im); print("rendered", code, flush=True)
    rows = (len(panels) + cols - 1) // cols
    g = 8
    out = Image.new("RGB", (cols * W + (cols + 1) * g, rows * H + (rows + 1) * g), (205, 205, 205))
    for k, im in enumerate(panels):
        out.paste(im, (g + (k % cols) * (W + g), g + (k // cols) * (H + g)))
    out.save(path); print("wrote", path, out.size)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "front"
    if which == "front":
        sheet(FRONT_LEFT, S.OUT + "/styles_front_r1.png")
    else:
        sheet(BACK_LEFT, S.OUT + "/styles_back_r1.png")
