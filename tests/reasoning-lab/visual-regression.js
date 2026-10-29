// Visual regression of EXISTING pages: baseline (origin/main) vs this branch, 1280/390 x light/dark.
// Usage: NODE_PATH=<playwright,pixelmatch,pngjs> BASE_A=http://127.0.0.1:8962/ BASE_B=http://127.0.0.1:8961/ PAGES_FILE=list.txt OUT=dir node tests/reasoning-lab/visual-regression.js
// Allowed differences: inside #site-header (the Labs dropdown) and #site-footer (the new link). Anything else fails.
const { chromium } = require('playwright'); const { PNG } = require('pngjs'); const pixelmatch = require('pixelmatch').default || require('pixelmatch');
const fs = require('fs'), path = require('path');
const A = process.env.BASE_A, B = process.env.BASE_B, OUT = process.env.OUT || '/tmp/vr';
const PAGES = fs.readFileSync(process.env.PAGES_FILE, 'utf8').split('\n').filter(Boolean);
const FIX = 'Date.now=(()=>{const t=Date.parse("2026-10-29T12:00:00+05:30");let k=0;return()=>t+(k++)})();Math.random=(()=>{let s=42;return()=>(s=(s*16807)%2147483647)/2147483647})();';
const res = { pages: PAGES.length, shots: 0, identical: 0, allowedOnly: 0, unexpected: [], heightChanges: [] };
(async () => {
  const br = await chromium.launch(); fs.mkdirSync(OUT, { recursive: true });
  for (const W of [1280, 390]) for (const scheme of ['light', 'dark']) {
    const mk = async () => { const c = await br.newContext({ viewport: { width: W, height: W > 500 ? 900 : 844 }, colorScheme: scheme, reducedMotion: 'reduce' });
      await c.route(u => !/^http:\/\/127\.0\.0\.1/.test(u), r => r.fulfill({ status: 204, body: '' })); await c.addInitScript(FIX); return c.newPage(); };
    const pa = await mk(), pb = await mk();
    const grab = async (p, base, u) => { await p.goto(base + u, { waitUntil: 'load' }); await p.waitForTimeout(500); await p.evaluate(() => window.scrollTo(0, 0));
      const box = await p.evaluate(() => { const r = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return { y0: b.top + scrollY, y1: b.bottom + scrollY }; }; return { h: r('#site-header'), f: r('#site-footer') }; });
      return { png: PNG.sync.read(await p.screenshot({ fullPage: true, animations: 'disabled', caret: 'hide' })), box }; };
    for (const u of PAGES) {
      res.shots++; const tag = `${W}-${scheme}`;
      try {
        const a = await grab(pa, A, u), b = await grab(pb, B, u);
        const w = a.png.width, h = Math.min(a.png.height, b.png.height);
        if (a.png.height !== b.png.height) res.heightChanges.push(`${tag} ${u}: ${a.png.height}→${b.png.height}`);
        const crop = (p) => { const o = new PNG({ width: w, height: h }); PNG.bitblt(p, o, 0, 0, w, h, 0, 0); return o; };
        // compare the part above the footer top-aligned, and the footer bottom-aligned (it may grow by one line)
        const fa = a.box.f ? Math.floor(a.box.f.y0) : a.png.height, fb = b.box.f ? Math.floor(b.box.f.y0) : b.png.height;
        const top = Math.min(fa, fb, h); const ca = crop(a.png), cb = crop(b.png), d = new PNG({ width: w, height: h });
        const n = pixelmatch(ca.data, cb.data, d.data, w, h, { threshold: 0.1 });
        if (!n && a.png.height === b.png.height) { res.identical++; continue; }
        // rows with diffs outside the header, above the footer
        const hdr = a.box.h ? [Math.floor(a.box.h.y0), Math.ceil(a.box.h.y1)] : [0, 0]; let bad = 0, firstBad = -1;
        for (let y = 0; y < top; y++) { if (y >= hdr[0] && y < hdr[1]) continue; for (let x = 0; x < w; x++) { const i = (y * w + x) * 4; if (d.data[i] === 255 && d.data[i + 1] === 0 && d.data[i + 2] === 0) { bad++; if (firstBad < 0) firstBad = y; } } }
        if (fa !== fb) bad += 1e6; // content above the footer changed height
        if (bad) { res.unexpected.push(`${tag} ${u}: ${bad} px outside header/footer, first at y=${firstBad}, footer ${fa}/${fb}`); fs.writeFileSync(path.join(OUT, `${tag}-${u.replace(/\//g, '_')}-diff.png`), PNG.sync.write(d)); }
        else res.allowedOnly++;
      } catch (e) { res.unexpected.push(`${tag} ${u}: ERROR ${String(e.message).split('\n')[0]}`); }
    }
    await pa.context().close(); await pb.context().close();
  }
  await br.close(); console.log(JSON.stringify(res, null, 1)); process.exit(res.unexpected.length ? 1 : 0);
})();
