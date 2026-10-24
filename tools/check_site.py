# Site health check. Run after `python3 tools/build_pages.py`:  python3 tools/check_site.py
# Fails (exit 1) on: broken internal links/assets, missing title/description/canonical, duplicate titles,
# indexable pages missing from sitemap.xml, or secret-looking strings in site files.
import os, re, sys, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
pages = sorted(f for f in os.listdir(".") if f.endswith(".html") and not f.startswith("google"))
errors, titles = [], {}
sitemap = open("sitemap.xml").read() if os.path.exists("sitemap.xml") else ""
for f in pages:
    s = open(f, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', s)
    c = re.search(r'<link rel="canonical" href="(.*?)"', s)
    noindex = "noindex" in s
    if not t: errors.append(f"{f}: missing <title>")
    else: titles.setdefault(html.unescape(t.group(1)), []).append(f)
    if not d: errors.append(f"{f}: missing meta description")
    if not c and not noindex: errors.append(f"{f}: missing canonical")
    if not noindex and c and c.group(1) not in sitemap: errors.append(f"{f}: not in sitemap.xml ({c.group(1)})")
    for m in re.finditer(r'(?:href|src)="([^"#?]+)', s):
        u = m.group(1)
        if re.match(r"(https?:|mailto:|tel:|data:|//|javascript:)", u): continue
        if not os.path.exists(u): errors.append(f"{f}: broken link/asset -> {u}")
for t, fs in titles.items():
    if len(fs) > 1: errors.append(f"duplicate title '{t}': {', '.join(fs)}")
secret = re.compile(r"service_role|sk_live_|BEGIN (RSA |EC )?PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}")
for root in (".", "assets/js", "tools"):
    for f in os.listdir(root):
        p = os.path.join(root, f)
        if os.path.isfile(p) and p.endswith((".js", ".html", ".py", ".json")) and "vendor" not in p and f != "check_site.py":
            if secret.search(open(p, encoding="utf-8", errors="ignore").read()): errors.append(f"{p}: secret-looking string")
print(f"{len(pages)} pages checked")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("OK")
