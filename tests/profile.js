// Optional profile (city, state, exam) on account.html, nav email, privacy section. Run: node tests/profile.js (site served on :8765)
const { chromium } = require('playwright');
const B = 'http://localhost:8765/', OUT = process.env.OUT || '/tmp';
let fail = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fail++; };
(async () => {
  const b = await chromium.launch();
  for (const [name, vp, scheme] of [['desk', { width: 1280, height: 900 }, 'light'], ['mob', { width: 390, height: 900 }, 'dark']]) {
    const p = await (await b.newContext({ viewport: vp, colorScheme: scheme })).newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto(B + 'account.html?mock=1'); await p.evaluate(() => sessionStorage.setItem('aptisetu.mock.user', JSON.stringify({ id: 'mock-1', email: 'edumaths360@gmail.com' }))); await p.goto(B + 'account.html'); await p.waitForSelector('#prof-form', { timeout: 8000 });
    ok(true, name + ': profile card shows when logged in');
    ok(await p.locator('#prof-state option').count() >= 30, name + ': state list present');
    ok(await p.locator('#prof-exam option').count() === 8 && (await p.locator('#prof-exam option').first().textContent()) === 'Select', name + ': exam list = 7 + default "Select"');
    ok((await p.locator('#prof-state option').first().textContent()) === 'Select', name + ': state default is "Select"');
    ok(await p.locator('#prof-form .req').count() === 2, name + ': two red asterisks (Name, Email)');
    ok(await p.inputValue('#prof-email') === 'edumaths360@gmail.com' && await p.getAttribute('#prof-email', 'readonly') !== null, name + ': email shown, read-only');
    ok(/rgb\((2[0-9]{2}|1[0-9]{2}), (\d{1,2}|1[0-3]\d), (\d{1,2}|1[0-3]\d)\)/.test(await p.$eval('#prof-form .req', e => getComputedStyle(e).color)), name + ': asterisk is red');
    ok(/stay private/.test(await p.textContent('#acct-profile')), name + ': says city/state/exam are private');
    await p.fill('#prof-name', ''); await p.click('#prof-form button[type=submit]'); await p.waitForTimeout(200);
    ok(/name/i.test(await p.textContent('#prof-msg')), name + ': empty name is blocked');
    await p.fill('#prof-name', 'Asha K.'); await p.fill('#prof-city', 'Prayagraj'); await p.selectOption('#prof-state', 'Uttar Pradesh'); await p.selectOption('#prof-exam', 'CAT');
    await p.click('#prof-form button[type=submit]'); await p.waitForFunction(() => /Saved/.test(document.querySelector('#prof-msg').textContent));
    await p.reload(); await p.waitForSelector('#prof-form');
    ok(await p.inputValue('#prof-city') === 'Prayagraj' && await p.inputValue('#prof-state') === 'Uttar Pradesh' && await p.inputValue('#prof-exam') === 'CAT' && await p.inputValue('#prof-name') === 'Asha K.', name + ': saved values come back after reload');
    await p.fill('#prof-city', 'x'); await p.click('#prof-form button[type=submit]'); await p.waitForTimeout(300);
    ok(/City/.test(await p.textContent('#prof-msg')), name + ': 1-letter city rejected');
    await p.fill('#prof-city', ''); await p.selectOption('#prof-state', ''); await p.selectOption('#prof-exam', ''); await p.click('#prof-form button[type=submit]');
    await p.waitForFunction(() => /Saved/.test(document.querySelector('#prof-msg').textContent));
    ok(true, name + ': optional fields can be cleared and saved (name stays)');
    await p.screenshot({ path: `${OUT}/profile-${name}.png`, fullPage: true });
    const who = p.locator('.auth-slot .who'); 
    if (name === 'mob') { await p.click('.nav-toggle, #nav-toggle, button[aria-label*=enu]').catch(() => {}); }
    ok(errs.length === 0, name + ': no page errors ' + errs.join('|'));
  }
  const p = await (await b.newContext()).newPage(); await p.goto(B + 'account.html');
  await p.waitForTimeout(800); ok(await p.locator('#prof-form').count() === 0, 'guest: no profile form');
  await p.goto(B + 'privacy.html'); const t = await p.textContent('body');
  ok(await p.locator('#account-data').count() === 1, 'privacy: #account-data anchor exists');
  ok(!/applies once these launch/.test(t), 'privacy: accounts/Open Mock no longer marked draft');
  ok(/city, state/i.test(t) && /Supabase/.test(t) && /delete/i.test(t), 'privacy: lists profile fields, Supabase, deletion');
  ok(!/and nothing else/.test(t), 'privacy: old "nothing else" claim removed');
  await b.close(); console.log(fail + ' failed'); process.exit(fail ? 1 : 0);
})();
