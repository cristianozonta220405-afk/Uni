"""Sfondi e texture 'pixel' in stile riferimento (blu acciaio / navy / lavanda)."""
import numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(7)
W, H = 1920, 1080
def lerp(a, b, t): return a + (b - a) * t[..., None]
def hexrgb(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
def pixel_layer(w, h, cell, mask, lo, hi, alpha=1.0):
    gw, gh = w // cell + 1, h // cell + 1
    v = rng.random((gh, gw)); v = np.kron(v, np.ones((cell, cell)))[:h, :w]
    col = lerp(hexrgb(lo), hexrgb(hi), v)
    return col, mask * alpha
# --- sfondo scuro
y, x = np.mgrid[0:H, 0:W]; y = y / H; x = x / W
d = np.clip(np.sqrt((x - 0.75) ** 2 * 1.2 + (y - 0.05) ** 2), 0, 1)
base = lerp(hexrgb('#6F90A8'), hexrgb('#0F1B2A'), np.clip(d * 1.25, 0, 1) ** 0.8)
col, m = pixel_layer(W, H, 36, np.clip(1 - d * 1.6, 0, 1) ** 1.5, '#2E4A63', '#A9C3D6', 0.55)
img = base * (1 - m[..., None]) + col * m[..., None]
col2, m2 = pixel_layer(W, H, 18, np.clip(1 - d * 2.2, 0, 1) ** 2, '#4C6C86', '#C9DAE6', 0.35)
img = img * (1 - m2[..., None]) + col2 * m2[..., None]
Image.fromarray(img.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2)).save('assets/bg_dark.png')
# variante scura più uniforme (per slide dense)
d2 = np.clip(np.sqrt((x - 0.15) ** 2 + (y - 0.0) ** 2 * 1.5), 0, 1)
base = lerp(hexrgb('#4F6F88'), hexrgb('#0E1826'), np.clip(d2 * 1.4, 0, 1) ** 0.7)
col, m = pixel_layer(W, H, 30, np.clip(1 - d2 * 2.0, 0, 1) ** 1.6, '#2B4660', '#9DB8CC', 0.45)
img = base * (1 - m[..., None]) + col * m[..., None]
Image.fromarray(img.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2)).save('assets/bg_dark2.png')
# --- sfondo chiaro
base = lerp(hexrgb('#EEF0F6'), hexrgb('#E2E6EE'), y)
Image.fromarray(base.clip(0, 255).astype('uint8')).save('assets/bg_light.png')
# --- card sfumata (verticale)
cw, ch = 600, 800
yy, xx = np.mgrid[0:ch, 0:cw]; yy = yy / ch; xx = xx / cw
base = lerp(hexrgb('#8FA9BE'), hexrgb('#16263A'), np.clip(yy * 1.1, 0, 1) ** 0.9)
col, m = pixel_layer(cw, ch, 28, np.clip(1 - yy * 1.8, 0, 1) ** 1.3 * (0.4 + 0.6 * xx), '#5C7A93', '#D3E1EA', 0.5)
img = base * (1 - m[..., None]) + col * m[..., None]
Image.fromarray(img.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8)).save('assets/card_grad.png')
# card sfumata scura (per immagini bento)
base = lerp(hexrgb('#5E7C94'), hexrgb('#0D1724'), np.clip((1 - xx) * 0.5 + yy * 0.7, 0, 1))
col, m = pixel_layer(cw, ch, 40, np.clip(1 - (yy * 1.2 + (1 - xx) * 0.6), 0, 1) ** 1.2, '#2A465E', '#B8CDDC', 0.7)
img = base * (1 - m[..., None]) + col * m[..., None]
Image.fromarray(img.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6)).save('assets/card_dark.png')
# --- cluster di cubi pixel (trasparente) per slide chiare
S = 700; cell = 22; g = S // cell
yy, xx = np.mgrid[0:g, 0:g]; yy = yy / g; xx = xx / g
r = np.sqrt((xx - 0.55) ** 2 + (yy - 0.45) ** 2)
mask = (r + rng.normal(0, 0.06, (g, g))) < 0.33
rgba = np.zeros((S, S, 4))
for i in range(g):
    for j in range(g):
        if not mask[i, j]: continue
        shade = rng.uniform(0.15, 1.0); c = lerp(hexrgb('#132233'), hexrgb('#B9CCDA'), np.array([shade]))[0]
        y0, x0 = i * cell, j * cell
        rgba[y0+1:y0+cell-1, x0+1:x0+cell-1, :3] = c; rgba[y0+1:y0+cell-1, x0+1:x0+cell-1, 3] = 255
        rgba[y0+1:y0+4, x0+1:x0+cell-1, :3] = np.minimum(c + 45, 255)  # bordo luce
im = Image.fromarray(rgba.astype('uint8'), 'RGBA')
im.save('assets/cubes.png')
print('ok')
