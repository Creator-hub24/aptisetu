# Draws the 1200x630 og:image and favicons from the brand in assets/js/config.js.
# Run with any python3 that has Pillow:  python3 tools/make_images.py
import os, re
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
cfg = dict(re.findall(r'^\s*([A-Z_]+):\s*"((?:[^"\\]|\\.)*)"', open("assets/js/config.js").read(), re.M))
BRAND, NAVY, GOLD = cfg["BRAND"], "#0B1F3A", "#C9A227"
INTER = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
def font(size, weight=800):
    f = ImageFont.truetype(INTER, size)
    try: f.set_variation_by_axes([14 if size < 40 else 32, weight])
    except Exception: pass
    return f
W, H = 1200, 630
im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 14], fill=GOLD); d.rectangle([0, H - 14, W, H], fill=GOLD)
cx, cy, r = 1010, 315, 120   # ring motif
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline="#1E3A63", width=16)
d.arc([cx - r, cy - r, cx + r, cy + r], start=-90, end=200, fill=GOLD, width=16)
d.text((cx, cy + 6), BRAND[:1], font=font(150), fill="#FFFFFF", anchor="mm")
x = 90
bf = font(104)
while d.textlength(BRAND, font=bf) > 780: bf = font(bf.size - 4)
d.text((x, 150), BRAND, font=bf, fill="#FFFFFF")
d.rectangle([x, 290, x + 120, 298], fill=GOLD)
d.text((x, 330), "Quant · Reasoning · DILR · VARC", font=font(44, 700), fill=GOLD)
d.text((x, 395), "Free practice for CAT, CUET (UG), Bank, SSC & placements", font=font(30, 500), fill="#D6DEEA")
d.text((x, 445), "Original questions · worked solutions · no login", font=font(30, 500), fill="#D6DEEA")
im.save("assets/img/og-image.png", optimize=True)
def icon(n):
    s = Image.new("RGBA", (n, n), (0, 0, 0, 0)); g = ImageDraw.Draw(s)
    g.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * .25), fill=NAVY)
    m, w = n * .17, max(2, int(n * .07))
    g.arc([m, m, n - m, n - m], start=-90, end=200, fill=GOLD, width=w)
    g.text((n / 2, n / 2 + n * .03), BRAND[:1], font=font(int(n * .42)), fill="#FFFFFF", anchor="mm")
    return s
icon(32).save("assets/img/favicon-32.png"); icon(180).convert("RGB").save("assets/img/apple-touch-icon.png")
letter = BRAND[:1].replace("&", "&amp;").replace("<", "&lt;")
open("assets/img/favicon.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="{NAVY}"/>
<path d="M20 7 A13 13 0 1 1 7.2 17.7" fill="none" stroke="{GOLD}" stroke-width="2.8" stroke-linecap="round"/>
<text x="20" y="26" text-anchor="middle" font-size="17" font-weight="800" fill="#fff" font-family="Inter,system-ui,sans-serif">{letter}</text></svg>
''')
print("images ok")
