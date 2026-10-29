// Reasoning Lab browser checks (Playwright + axe-core are dev-only and never shipped).
// Serve the repo root, then: NODE_PATH=<dir with playwright+axe-core> BASE=http://127.0.0.1:8765/ [SHOTS=dir] node tests/reasoning-lab/e2e.js
// 390px and 1280px x light and dark: every Reasoning Lab page with real interaction (answer, solution stepper, sandbox switch,
// a full timed round, progress), hostile hashes, live theme switching, keyboard answers, the Labs dropdown (desktop + mobile),
// console errors, CSP violations, requests leaving the site, and axe colour-contrast (inside the shadow root too).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const BASE = process.env.BASE || 'http://127.0.0.1:8765/', SHOTS = process.env.SHOTS || '';
const HOST = new URL(BASE).host;
const PAGES = ['reasoning-lab.html', 'reasoning-lab-learn.html', 'reasoning-lab-learn.html#cube', 'reasoning-lab-practice.html', 'reasoning-lab-practice.html#seating/medium', 'reasoning-lab-lab.html', 'reasoning-lab-timed.html', 'reasoning-lab-progress.html'];
const HOSTILE = ['reasoning-lab-learn.html#__proto__', 'reasoning-lab-learn.html#constructor', 'reasoning-lab-practice.html#cube/__proto__', 'reasoning-lab-practice.html#toString/hard', 'reasoning-lab-lab.html#hasOwnProperty',
  'reasoning-lab-learn.html#%E0%A4%A', 'reasoning-lab-learn.html#<img src=x onerror=alert(1)>', 'reasoning-lab-practice.html#' + 'a'.repeat(5000), 'reasoning-lab-lab.html#../../etc/passwd', 'reasoning-lab.html#/t/cube/practice', 'reasoning-lab-timed.html#x/y/z'];
const res = { checks: 0, fails: [], axeViolations: 0, csp: 0, consoleErrors: 0, offsite: new Set() };
const fail = (k, m) => res.fails.push(k + ': ' + m);
const sr = (page, js) => page.evaluate(js);
(async () => {
  const br = await chromium.launch(); const t0 = Date.now();
  for (const W of [1280, 390]) for (const scheme of ['light', 'dark']) {
    const ctx = await br.newContext({ viewport: { width: W, height: W > 500 ? 900 : 844 }, colorScheme: scheme });
    // Nothing should leave the site from the lab. The site template's optional analytics is answered locally so tests stay offline.
    await ctx.route(u => new URL(u).host !== HOST, r => { res.offsite.add(new URL(r.request().url()).host); return r.fulfill({ status: 204, body: '' }); });
    await ctx.addInitScript(() => { window.__csp = []; document.addEventListener('securitypolicyviolation', e => window.__csp.push(e.violatedDirective + ' ' + e.blockedURI)); window.alert = () => { window.__alerted = 1; }; });
    const page = await ctx.newPage(); let errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); page.on('pageerror', e => errs.push(e.message)); page.on('dialog', d => d.accept());
    const tag = `${W}-${scheme}`;
    const ready = () => page.waitForFunction(() => { const r = document.getElementById('rl-app'); return r && r.shadowRoot && r.shadowRoot.querySelector('.main') && r.shadowRoot.querySelector('.main').childElementCount > 0; }, null, { timeout: 8000 });
    async function open(url, label, fn) {
      res.checks++; errs = [];
      try {
        await page.goto(BASE + url, { waitUntil: 'load' }); await ready();
        if (fn) { const r = await fn(); if (r) fail(`${tag} ${label}`, r); }
        const csp = await page.evaluate(() => window.__csp); if (csp.length) { res.csp += csp.length; fail(`${tag} ${label}`, 'CSP ' + csp.join('; ')); }
        if (await page.evaluate(() => window.__alerted)) fail(`${tag} ${label}`, 'script injection ran');
      } catch (e) { fail(`${tag} ${label}`, String(e.message).split('\n')[0]); }
      if (errs.length) { res.consoleErrors += errs.length; fail(`${tag} ${label}`, 'console: ' + errs.join(' | ')); }
    }
    const axe = async label => { await page.evaluate(axeSrc); const v = await page.evaluate(async () => (await axe.run(document, { runOnly: ['color-contrast'] })).violations.flatMap(v => v.nodes.map(n => JSON.stringify(n.target) + ' ' + (n.any[0] && n.any[0].message || '').slice(0, 120))));
      if (v.length) { res.axeViolations += v.length; fail(`${tag} axe ${label}`, v.slice(0, 4).join(' || ')); } };
    const text = () => sr(page, () => document.getElementById('rl-app').shadowRoot.querySelector('.main').innerText);
    const shot = async name => { if (SHOTS) { await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(150); } if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${name}-${W === 1280 ? 'desktop' : 'mobile'}-${scheme}.png`), fullPage: true }); };
    for (const pg of PAGES) await open(pg, pg, async () => {
      const app = page.locator('#rl-app');
      if (pg === 'reasoning-lab-practice.html#seating/medium') {
        await app.locator('.opt').first().waitFor(); await page.keyboard.press('1'); await app.locator('.verdict.ok, .verdict.bad').first().waitFor({ timeout: 3000 });
        await app.locator('.steplist li').first().waitFor(); await app.getByRole('button', { name: 'Next ▶' }).click();
      }
      if (pg === 'reasoning-lab-learn.html#cube') { const b = app.getByRole('button', { name: /Next/ }).first(); if (await b.count()) await b.click(); }
      if (pg === 'reasoning-lab-lab.html') { await app.getByRole('button', { name: /Family/ }).click(); await page.waitForTimeout(300); if (!/#family$/.test(page.url())) return 'sandbox switch did not set #family'; await app.getByRole('button', { name: /Seating/ }).click(); await page.waitForTimeout(300); }
      if (pg === 'reasoning-lab-timed.html') {
        await app.getByRole('group', { name: 'Questions' }).getByRole('button', { name: '5', exact: true }).click(); await app.getByRole('button', { name: 'Start ▶' }).click();
        for (let i = 0; i < 5; i++) { await app.locator('.opt').first().waitFor(); await app.locator('.opt').nth(i % 4).click(); }
        await app.getByText(/Score \d+ \/ 5/).waitFor({ timeout: 3000 }); await app.locator('details summary').first().click(); await page.waitForTimeout(300);
      }
      await page.waitForTimeout(900); await axe(pg);
      if (pg === 'reasoning-lab-practice.html#seating/medium') await shot('practice-answered');
      else if (pg === 'reasoning-lab-learn.html#cube') await shot('learn-cube');
      else if (pg === 'reasoning-lab-timed.html') await shot('timed-review');
      else await shot(pg.replace('.html', '').replace('reasoning-lab-', '').replace('reasoning-lab', 'overview'));
      const nav = await page.$$eval('#site-header .nav-dd-menu a', as => as.map(a => a.textContent.trim())); if (!nav.includes('Reasoning Lab') || !nav.includes('Quant Lab')) return 'Labs dropdown items missing';
      const top = await page.$$eval('#site-header .nav-links > a', as => as.map(a => a.textContent.trim())); if (top.includes('Quant Lab')) return 'Quant Lab still top-level';
      const foot = await page.$$eval('#site-footer a[href="reasoning-lab.html"]', a => a.length); if (foot !== 1) return 'footer link missing';
      const credit = await page.$$eval('.rl-credit', a => a.map(x => x.textContent)); if (!credit.length || !/generated by software and checked by our team/.test(credit[0])) return 'credit line missing';
      const h1 = await page.$$eval('h1', a => a.length); const h1s = await sr(page, () => document.getElementById('rl-app').shadowRoot.querySelectorAll('h1').length); if (h1 !== 1 || h1s) return `h1 count ${h1}+${h1s}`;
      const t = await text(); if (/\bNaN\b|\bundefined\b|\[object/.test(t)) return 'bad text: ' + t.slice(0, 100);
    });
    if (W === 1280) {
      for (const h of HOSTILE) await open(h, 'hostile ' + h.slice(0, 60), async () => { const t = await text(); if (!t.trim()) return 'empty app'; });
      // live theme switch from the site header: host class follows, canvases repaint without errors
      await open('reasoning-lab.html', 'theme switch', async () => { const before = await sr(page, () => document.getElementById('rl-app').classList.contains('dark')); await page.click('#site-header .theme-btn'); await page.waitForTimeout(300);
        const after = await sr(page, () => document.getElementById('rl-app').classList.contains('dark')); if (before === after) return 'host theme class did not follow site toggle'; await axe('after theme switch'); await page.click('#site-header .theme-btn'); });
      // keyboard: typing in the exam <select> must not answer; N gives a new question
      await open('reasoning-lab-practice.html#cube/easy', 'keyboard', async () => { const app = page.locator('#rl-app'); await app.locator('select#rl-exam').focus(); await page.keyboard.press('a'); if (await app.locator('.opt.ok, .opt.bad').count()) return 'key in select answered'; await app.locator('.opt').first().focus(); await page.keyboard.press('b'); if (!(await app.locator('.opt.ok').count())) return 'B did not answer'; });
      // Labs dropdown (desktop): aria-expanded, Escape returns focus, focus-out closes
      await open('reasoning-lab.html', 'labs dropdown desktop', async () => { const b = page.locator('#site-header .nav-dd-btn', { hasText: 'Labs' }); await b.click(); if (await b.getAttribute('aria-expanded') !== 'true') return 'not expanded'; if (!(await page.locator('#dd-labs').isVisible())) return 'menu hidden';
        if (await page.locator('#site-header .nav-dd.active .nav-dd-btn', { hasText: 'Labs' }).count() !== 1) return 'Labs not marked active on a Reasoning Lab page';
        if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `labs-dropdown-open-desktop-${scheme}.png`), clip: { x: 0, y: 0, width: 1280, height: 260 } });
        await page.locator('#dd-labs a').first().focus(); await page.keyboard.press('Escape'); if (await b.getAttribute('aria-expanded') !== 'false') return 'Escape did not close'; if (!(await b.evaluate(el => el === document.activeElement))) return 'focus not returned';
        await b.click(); await page.locator('#dd-labs a').last().focus(); await page.keyboard.press('Tab'); await page.waitForTimeout(100); if (await b.getAttribute('aria-expanded') !== 'false') return 'focus-out did not close'; });
    } else {
      await open('reasoning-lab-practice.html', 'labs dropdown mobile', async () => { await page.click('#site-header .menu-btn'); const b = page.locator('#site-header .nav-dd-btn', { hasText: 'Labs' }); await b.click(); if (await b.getAttribute('aria-expanded') !== 'true') return 'not expanded';
        if (!(await page.locator('#dd-labs a', { hasText: 'Reasoning Lab' }).isVisible())) return 'Reasoning Lab link hidden';
        if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `labs-dropdown-open-mobile-${scheme}.png`) });
        await page.keyboard.press('Escape'); if (await b.getAttribute('aria-expanded') !== 'false') return 'Escape did not close'; await page.locator('#dd-labs a', { hasText: 'Quant Lab' }).count(); });
    }
    await ctx.close();
  }
  // reduced motion: no CSS animations, the spinning die stays still
  const ctx = await br.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' }); await ctx.route(u => new URL(u).host !== HOST, r => r.fulfill({ status: 204, body: '' }));
  const page = await ctx.newPage(); await page.goto(BASE + 'reasoning-lab.html'); await page.waitForTimeout(800); res.checks++;
  const anims = await page.evaluate(() => document.getElementById('rl-app').shadowRoot.getAnimations ? document.getElementById('rl-app').shadowRoot.getAnimations().filter(a => a.playState === 'running').length : 0); if (anims) fail('reduced-motion', anims + ' running animations');
  await br.close();
  res.offsite = [...res.offsite]; res.seconds = Math.round((Date.now() - t0) / 1000);
  console.log(JSON.stringify(res, null, 1)); process.exit(res.fails.length ? 1 : 0);
})();
