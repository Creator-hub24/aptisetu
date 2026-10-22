// Quant Lab browser checks (Playwright + axe-core are dev-only and never shipped).
// Serve the repo root, then: NODE_PATH=<dir with playwright+axe-core> BASE=http://127.0.0.1:8765/ node tests/quant-lab/e2e.js
// 390px and 1280px x light and dark: every Quant Lab page, every question type (fresh load), every explainer,
// the Concept Lab, practice, hostile URL params, colour-scheme switching, console errors, CSP violations and
// axe colour-contrast. Then reduced motion: no SMIL left, canvases static, no CSS animations.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const Q = require('./all.js');
const BASE = process.env.BASE || 'http://127.0.0.1:8765/', SHOTS = process.env.SHOTS || '';
const PAGES = ['quant-lab.html', 'quant-lab-explainers.html', 'quant-lab-generator.html', 'quant-lab-concept-lab.html', 'quant-lab-practice.html'];
const res = { checks: 0, fails: [], axe: [], csp: 0, consoleErrors: 0 };
const fail = (k, m) => res.fails.push(k + ': ' + m);
(async () => {
  const br = await chromium.launch(); const t0 = Date.now();
  for (const W of [1280, 390]) for (const scheme of ['light', 'dark']) {
    const ctx = await br.newContext({ viewport: { width: W, height: W > 500 ? 900 : 844 }, colorScheme: scheme });
    await ctx.addInitScript(() => { window.__csp = []; document.addEventListener('securitypolicyviolation', e => window.__csp.push(e.violatedDirective + ' ' + e.blockedURI)); });
    const page = await ctx.newPage(); let errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); page.on('pageerror', e => errs.push(e.message));
    const tag = `${W}-${scheme}`;
    async function open(url, label, fn) {
      res.checks++; errs = [];
      try {
        await page.goto(BASE + url, { waitUntil: 'load' }); await page.waitForSelector('body[data-ql-ready="1"]', { timeout: 8000 });
        if (fn) { const r = await fn(); if (r) fail(`${tag} ${label}`, r); }
        const csp = await page.evaluate(() => window.__csp); if (csp.length) { res.csp += csp.length; fail(`${tag} ${label}`, 'CSP ' + csp.join('; ')); }
      } catch (e) { fail(`${tag} ${label}`, String(e.message).split('\n')[0]); }
      if (errs.length) { res.consoleErrors += errs.length; fail(`${tag} ${label}`, 'console: ' + errs.join(' | ')); }
    }
    const axe = async label => { await page.evaluate(axeSrc); const r = await page.evaluate(async () => (await axe.run(document, { runOnly: ['color-contrast'] })).violations.map(v => v.nodes.map(n => n.target.join(' ') + ' ' + (n.any[0] && n.any[0].message || '')).join(' || '))); if (r.length) res.axe.push(`${tag} ${label}: ${r.join(' ## ')}`); };
    for (const pg of PAGES) await open(pg, pg, async () => {
      if (pg === 'quant-lab-generator.html') await page.click('#qlGenReveal');
      if (pg === 'quant-lab-practice.html') { await page.click('#qlPStart'); await page.waitForTimeout(300); }
      await page.waitForTimeout(1200); await axe(pg);
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${pg.replace('.html', '')}-${tag}.png`), fullPage: true });
      const nav = await page.$$eval('#site-header a', as => as.map(a => a.textContent.trim())); if (!nav.includes('Quant Lab')) return 'nav item missing';
      const foot = await page.$$eval('#site-footer a[href="quant-lab.html"]', a => a.length); if (foot !== 1) return 'footer link missing';
      const txt = await page.evaluate(() => document.body.innerText); if (/NaN|undefined|Living Quant/.test(txt)) return 'bad text on page';
    });
    for (const t of process.env.QUICK ? [] : Q.listTypes()) await open(`quant-lab-generator.html?t=${t.topic}&l=${t.level}&type=${t.id}&reveal=1`, 'type ' + t.id, async () => page.evaluate(name => {
      const meta = document.querySelector('#qlGenProblem .ql-meta'); if (!meta || !meta.textContent.includes(name)) return 'wrong/no type shown';
      const v = document.querySelector('#qlGenViz svg'); if (!v || v.innerHTML.length < 150) return 'empty visual';
      if (/NaN|undefined|Infinity/.test(document.querySelector('#ql').innerText + v.innerHTML)) return 'NaN/undefined';
      if (!document.querySelectorAll('#qlGenSteps li').length || document.querySelectorAll('#qlGenTraps li').length < 2) return 'missing steps/traps';
      if (document.querySelector('#qlGenProblem .ql-fmt.mcq') && document.querySelectorAll('#qlGenProblem .ql-opt').length !== 4) return 'MCQ options missing';
      if (document.documentElement.scrollWidth > innerWidth + 1) return 'horizontal overflow ' + document.documentElement.scrollWidth;
      return null; }, t.name));
    for (const k of process.env.QUICK ? [] : Object.keys(Q.TOPICS)) await open(`quant-lab-explainers.html?t=${k}`, 'explainer ' + k, async () => page.evaluate(k => {
      const on = document.querySelector('#qlExTabs button.on'); if (!on || on.dataset.k !== k) return 'wrong tab';
      const v = document.querySelector('#qlExArt svg'); if (!v || v.innerHTML.length < 150) return 'empty explainer';
      if (/NaN|undefined/.test(document.querySelector('#qlExplainer').innerHTML)) return 'NaN/undefined';
      for (const r of document.querySelectorAll('#qlExplainer input[type=range]')) for (const val of [r.min, r.max]) { r.value = val; r.dispatchEvent(new Event('input')); if (/NaN|undefined|Infinity/.test(document.querySelector('#qlExplainer').innerHTML)) return 'NaN after slider ' + r.dataset.id + '=' + val; }
      if (document.documentElement.scrollWidth > innerWidth + 1) return 'horizontal overflow'; return null; }, k));
    await open('quant-lab-concept-lab.html', 'labs', async () => {
      const r = await page.evaluate(() => { const bad = []; const T = () => /NaN|undefined|Infinity/.test(document.querySelector('#ql').innerText);
        document.querySelectorAll('#ql input[type=range]').forEach(i => { for (const v of [i.min, i.max, i.defaultValue]) { i.value = v; i.dispatchEvent(new Event('input')); if (T()) bad.push(i.id + '=' + v); } });
        document.querySelectorAll('#ql select').forEach(s => [...s.options].forEach(o => { s.value = o.value; s.dispatchEvent(new Event('change')); s.dispatchEvent(new Event('input')); if (T()) bad.push(s.id + '=' + o.value); }));
        return bad.join(', '); });
      await page.emulateMedia({ colorScheme: scheme === 'light' ? 'dark' : 'light' }); await page.waitForTimeout(300); await page.emulateMedia({ colorScheme: scheme }); await page.waitForTimeout(300);
      const px = await page.evaluate(() => { const c = document.getElementById('tsdCanvas'), d = c.getContext('2d').getImageData(2, 2, 1, 1).data; return [...d.slice(0, 3)]; });
      const bgs = await page.evaluate(() => ['--bg', '--card'].map(v => getComputedStyle(document.documentElement).getPropertyValue(v).trim()));
      const ok = bgs.some(h => { h = h.replace('#', ''); if (h.length === 3) h = [...h].map(c => c + c).join(''); const w = [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)); return w.every((x, i) => Math.abs(x - px[i]) <= 3); });
      if (!ok) return `canvas not repainted for ${scheme}: corner ${px} vs ${bgs}`;
      return r || null; });
    await open('quant-lab-practice.html', 'practice', async () => { await page.selectOption('#qlPTopic', 'sec:mod'); await page.click('#qlPLevel button[data-l=hard]'); await page.selectOption('#qlPCount', '5'); await page.click('#qlPStart');
      for (let i = 0; i < 5; i++) {
        await page.waitForFunction(() => document.querySelector('#qlPQ .ql-opt:not([disabled])') || !document.querySelector('#qlPInput').classList.contains('hidden') && !document.querySelector('#qlPFb').textContent, null, { timeout: 8000 });
        if (await page.$('#qlPQ .ql-opt:not([disabled])')) await page.click('#qlPQ .ql-opt:not([disabled]) >> nth=0'); else { await page.fill('#qlPInput', '1'); await page.click('#qlPSubmit'); }
        await page.waitForFunction(n => /Session complete/.test(document.querySelector('#qlPQ').textContent) || document.querySelector('#qlPProg').textContent.startsWith('Q ' + n + ' '), i + 2, { timeout: 8000 }).catch(() => {});
      }
      await page.waitForFunction(() => /Session complete/.test(document.querySelector('#qlPQ').textContent), null, { timeout: 8000 });
      const st = await page.evaluate(() => JSON.parse(localStorage.getItem('aptisetu.quantlab.v1') || 'null')); if (!st || st.answered < 5) return 'stats not saved: ' + JSON.stringify(st);
      if ((await ctx.cookies()).length) return 'cookie set'; return null; });
    for (const q of ['t=__proto__&l=hard', 't=algebra&l=%3Cimg%20src%3Dx%3E', 't=pnc&l=hard&type=st-h1', 't=pnc&l=hard&type=constructor', 't=%3Cscript%3E&type=..%2F&reveal=1', 'scroll=%23x%5B&t=sets']) await open('quant-lab-generator.html?' + q, 'params ' + q, async () => page.evaluate(() => { if (!document.querySelector('#qlGenProblem .ql-meta')) return 'no problem rendered'; if (document.querySelector('#ql img, #ql script')) return 'injected element'; return null; }));
    await open('quant-lab-explainers.html?t=constructor', 'explainer bad t', async () => page.evaluate(() => document.querySelector('#qlExTabs button.on').dataset.k === 'percentages' ? null : 'no fallback'));
    await ctx.close();
  }
  { const ctx = await br.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' }); const page = await ctx.newPage(); const errs = []; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => m.type() === 'error' && errs.push(m.text()));
    const smil = async url => { await page.goto(BASE + url); await page.waitForSelector('body[data-ql-ready="1"]'); await page.waitForTimeout(300); return page.evaluate(() => document.querySelectorAll('#ql animate, #ql animateMotion, #ql animateTransform').length); };
    let left = 0; for (const t of Q.listTypes()) left += await smil(`quant-lab-generator.html?t=${t.topic}&l=${t.level}&type=${t.id}&reveal=1`);
    for (const k of Object.keys(Q.TOPICS)) left += await smil(`quant-lab-explainers.html?t=${k}`); res.checks++; if (left) fail('reduced-motion', left + ' SMIL elements left');
    await page.goto(BASE + 'quant-lab-concept-lab.html'); await page.waitForSelector('body[data-ql-ready="1"]'); await page.waitForTimeout(300);
    const a = await page.locator('#tsdCanvas').screenshot(), b0 = await page.locator('#twCanvas').screenshot(); await page.waitForTimeout(900);
    const a2 = await page.locator('#tsdCanvas').screenshot(), b2 = await page.locator('#twCanvas').screenshot(); res.checks++; if (!a.equals(a2) || !b0.equals(b2)) fail('reduced-motion', 'canvas still animating');
    const anim = await page.evaluate(() => [...document.querySelectorAll('#ql *')].filter(e => getComputedStyle(e).animationName !== 'none').length); res.checks++; if (anim) fail('reduced-motion', anim + ' CSS animations running');
    if (errs.length) fail('reduced-motion', errs.join(' | ')); await ctx.close(); }
  const out = `Quant Lab browser checks (${((Date.now() - t0) / 1000).toFixed(0)} s): ${res.checks} checks, ${res.fails.length} failures, CSP violations ${res.csp}, console errors ${res.consoleErrors}, axe colour-contrast violations ${res.axe.length}\n` + res.fails.join('\n') + (res.axe.length ? '\nAXE:\n' + res.axe.join('\n') : '') + '\n';
  console.log(out); if (process.env.OUT) fs.writeFileSync(process.env.OUT, out); await br.close(); process.exit(res.fails.length || res.axe.length ? 1 : 0);
})();
