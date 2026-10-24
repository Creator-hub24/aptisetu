# Draws the 1200x630 og:image and favicons from the brand in assets/js/config.js.
# Run with any python3 that has Pillow:  python3 tools/make_images.py
import os, re
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
cfg = dict(re.findall(r'^\s*([A-Z_]+):\s*"((?:[^"\\]|\\.)*)"', open("assets/js/config.js").read(), re.M))
BRAND, NAVY, GOLD = cfg["BRAND"], "#0B1F3A", "#C9A227"
INTER = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
STATIC = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def font(size, weight=800):
    if os.path.exists(INTER):
        f = ImageFont.truetype(INTER, size)
        try: f.set_variation_by_axes([14 if size < 40 else 32, weight])
        except Exception: pass
        return f
    name = "ExtraBold" if weight >= 800 else "Bold" if weight >= 700 else "Medium" if weight >= 500 else "Regular"
    return ImageFont.truetype(STATIC % name, size)
W, H = 1200, 630
im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 14], fill=GOLD); d.rectangle([0, H - 14, W, H], fill=GOLD)
cx, cy, r = 1035, 315, 100   # mark: white tile, navy AS, gold bridge arch
d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=int(r * .5), fill="#FFFFFF")
d.text((cx, cy + 20), "AS", font=font(115), fill=NAVY, anchor="mm")
d.arc([cx - r * .7, cy - r * 1.05, cx + r * .7, cy - r * .1], start=200, end=340, fill=GOLD, width=14)
x = 90
bf = font(104)
while d.textlength(BRAND, font=bf) > 780: bf = font(bf.size - 4)
d.text((x, 150), BRAND, font=bf, fill="#FFFFFF")
d.rectangle([x, 290, x + 120, 298], fill=GOLD)
d.text((x, 330), "Quant · Reasoning · DILR · VARC", font=font(44, 700), fill=GOLD)
d.text((x, 395), "Free practice for CAT, CUET (UG), Bank, SSC & placements", font=font(30, 500), fill="#D6DEEA")
d.text((x, 445), "Login only to save progress and unlock levels", font=font(30, 500), fill="#D6DEEA")
im.save("assets/img/og-image.png", optimize=True)
def icon(n):
    s = Image.new("RGBA", (n, n), (0, 0, 0, 0)); g = ImageDraw.Draw(s)
    g.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * .25), fill="#FFFFFF", outline=NAVY, width=max(1, int(n * .05)))
    g.text((n / 2, n * .66), "AS", font=font(int(n * .47)), fill=NAVY, anchor="mm")
    w = max(2, int(n * .065))
    g.arc([n * .2, n * .06, n * .8, n * .5], start=205, end=335, fill=GOLD, width=w)
    return s
icon(32).save("assets/img/favicon-32.png"); (lambda a: (lambda bg: (bg.paste(a, (0, 0), a), bg.save("assets/img/apple-touch-icon.png")))(Image.new("RGB", (180, 180), "#FFFFFF")))(icon(180))
open("assets/img/favicon.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect x="1" y="1" width="38" height="38" rx="10" fill="#fff" stroke="{NAVY}" stroke-width="2"/>
<text x="20" y="27.5" text-anchor="middle" font-size="19" font-weight="800" fill="{NAVY}" font-family="Inter,system-ui,Arial,sans-serif" letter-spacing="-1">AS</text>
<path d="M9 11Q20 3 31 11" fill="none" stroke="{GOLD}" stroke-width="2.6" stroke-linecap="round"/></svg>
''')
print("images ok")
