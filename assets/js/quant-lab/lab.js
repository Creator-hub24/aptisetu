/* AptiSetu Quant Lab: explainers, problem generator, Concept Lab and timed practice.
   Each Quant Lab page contains some of these blocks; the script wires whatever it finds.
   Security: every innerHTML template is built from generator output (escaped) or internal numbers;
   URL parameters are only ever compared against allowlists. Respects prefers-reduced-motion and the colour scheme. */
(function () {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  if (!document.getElementById('ql') || !window.QGen) return;
  const TOPICS = QGen.TOPICS, SECTIONS = QGen.SECTIONS, keys = SECTIONS.flatMap(s => s.topics), LEVELS = ['easy', 'medium', 'hard'];
  const ALLTYPES = QGen.listTypes();
  const TN = k => TOPICS[k][0], ICON = k => TOPICS[k][1];
  const STORE = 'aptisetu.quantlab.v1';
  const RM = matchMedia('(prefers-reduced-motion: reduce)'), DARK = matchMedia('(prefers-color-scheme: dark)');
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const params = new URLSearchParams(location.search);
  const qp = (k, allowed, def) => { const v = params.get(k); return v != null && allowed.includes(v) ? v : def; };
  // colour tokens for <canvas> (SVG uses var(--token) directly)
  const P = {};
  const readP = () => { const cs = getComputedStyle(document.documentElement); ['brand', 'brand2', 'ok', 'accent', 'bad', 'ink', 'muted', 'line', 'card', 'bg', 'reason'].forEach(k => P[k] = cs.getPropertyValue('--' + k).trim() || '#888'); };
  readP();
  // reduced motion: replace SMIL animation with a representative static frame
  function freeze(el) {
    if (!RM.matches || !el) return;
    el.querySelectorAll('animateTransform').forEach(a => { const vals = (a.getAttribute('values') || `${a.getAttribute('from')};${a.getAttribute('to')}`).split(';').map(v => v.trim().split(/[\s,]+/).map(Number)); const A = vals[0], B = vals[vals.length - 1]; const mid = A.map((v, i) => (v + (B[i] ?? v)) / 2); a.parentNode.setAttribute('transform', `translate(${mid.join(' ')})`); a.remove(); });
    el.querySelectorAll('animateMotion').forEach(a => { const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', a.getAttribute('path') || ''); let pt = { x: 0, y: 0 }; try { pt = p.getPointAtLength(0); } catch (e) { } const host = a.parentNode; if (host.tagName === 'circle') { host.setAttribute('cx', pt.x); host.setAttribute('cy', pt.y); } a.remove(); });
    el.querySelectorAll('animate').forEach(a => { const host = a.parentNode, name = a.getAttribute('attributeName'), from = a.getAttribute('from'), to = a.getAttribute('to'); if (name && from != null && to != null && !isNaN(+from) && !isNaN(+to)) host.setAttribute(name, (+from + +to) / 2); a.remove(); });
  }
  const setHTML = (el, html) => { el.innerHTML = html; freeze(el); };
  const safe = (name, fn) => { try { fn(); } catch (e) { console.warn('[quant-lab] ' + name + ' could not start', e); } };
  const optgroups = (extra = '') => extra + SECTIONS.map(s => `<optgroup label="${esc(s.name)}">${s.topics.map(k => `<option value="${k}">${esc(TN(k))}</option>`).join('')}</optgroup>`).join('');
  const redraw = [];   // callbacks to repaint when the colour scheme changes

  /* ---------- hub: topics by section ---------- */
  safe('topics', () => {
    const grid = $('#qlTopics'); if (!grid) return;
    const counts = {}; ALLTYPES.forEach(t => counts[t.topic] = (counts[t.topic] || 0) + 1);
    grid.innerHTML = SECTIONS.map(s => `<div class="ql-section"><h3 class="ql-section-h">${esc(s.name)} <small>${s.topics.length} topic${s.topics.length > 1 ? 's' : ''} · ${s.topics.reduce((n, k) => n + counts[k], 0)} question types</small></h3>
      <div class="grid g4 ql-topic-grid">${s.topics.map(k => `<div class="card ql-tcard"><div class="ql-ic" aria-hidden="true">${esc(ICON(k))}</div><h4>${esc(TN(k))}</h4><p class="muted">${esc(TOPICS[k][2])}</p><div class="ql-tlinks"><a href="quant-lab-explainers.html?t=${k}">Explainer</a><a href="quant-lab-generator.html?t=${k}">Generate a question</a></div></div>`).join('')}</div></div>`).join('');
    const st = $('#qlStats'); if (st) st.textContent = `${keys.length} topics · ${SECTIONS.length} sections · ${ALLTYPES.length} question types`;
  });

  /* ---------- explainers ---------- */
  safe('explainers', () => {
    const tabs = $('#qlExTabs'); if (!tabs) return;
    let exKey = qp('t', keys, 'percentages');
    tabs.innerHTML = SECTIONS.map(s => `<div class="ql-tabgroup" role="group" aria-label="${esc(s.name)}"><span class="ql-tg-name">${esc(s.name)}</span>${s.topics.map(k => `<button type="button" data-k="${k}">${esc(TN(k))}</button>`).join('')}</div>`).join('');
    tabs.addEventListener('click', e => { const b = e.target.closest('button[data-k]'); if (b && keys.includes(b.dataset.k)) show(b.dataset.k, true); });
    function show(k, push) {
      exKey = k; const E = QViz.EX[k]; $$('#qlExTabs button').forEach(b => { b.classList.toggle('on', b.dataset.k === k); b.setAttribute('aria-pressed', b.dataset.k === k); });
      const box = $('#qlExplainer');
      box.innerHTML = `<div class="ql-viz" id="qlExArt"></div><div><span class="ql-pill">${esc(TN(k))}</span><h2 class="ql-ex-title">${esc(E.title)}</h2><p>${esc(E.blurb)}</p><div class="ql-formula">${esc(E.formula)}</div>
        ${E.controls.map(c => `<label class="ql-ctl">${esc(c.label)} <input type="range" data-id="${esc(c.id)}" min="${+c.min}" max="${+c.max}" step="${+c.step}" value="${+c.value}"><output>${+c.value}</output></label>`).join('')}
        <p><a class="btn btn-sm" href="quant-lab-generator.html?t=${k}">Try a ${esc(TN(k))} question</a></p></div>`;
      const draw = () => { const v = {}; box.querySelectorAll('input[type=range]').forEach(i => { v[i.dataset.id] = +i.value; i.nextElementSibling.textContent = i.value; }); setHTML($('#qlExArt'), E.draw(v)); };
      box.querySelectorAll('input[type=range]').forEach(i => i.addEventListener('input', draw)); draw();
      if (push) history.replaceState(null, '', '?t=' + k);
    }
    redraw.push(() => show(exKey, false));
    show(exKey, false);
  });

  /* ---------- generator ---------- */
  const optionsHTML = (p) => p.format === 'mcq' ? `<div class="ql-options">${p.options.map((o, i) => `<button type="button" class="ql-opt" data-i="${i}"><b>${QGen.LETTERS[i]}</b> ${esc(o.label)}${p.unit && p.unit.length < 6 ? ' <span class="ql-u">' + esc(p.unit) + '</span>' : ''}</button>`).join('')}</div>` : '';
  safe('generator', () => {
    const sel = $('#qlGenTopic'); if (!sel) return;
    let cur = null;
    sel.innerHTML = optgroups();
    const t0 = qp('t', keys, 'percentages'), l0 = qp('l', LEVELS, 'easy');
    sel.value = t0; setSeg('#qlGenLevel', l0);
    const typeOk = (t, l, id) => ALLTYPES.some(x => x.topic === t && x.level === l && x.id === id);
    function newProblem(typeId) {
      const t = keys.includes(sel.value) ? sel.value : 'percentages', l = segVal('#qlGenLevel');
      cur = QGen.generate(t, l, typeId && typeOk(t, l, typeId) ? { typeId } : {});
      $('#qlGenProblem').innerHTML = `<div class="ql-meta">${esc(cur.topicName)} · ${esc(cur.level)} · ${esc(cur.typeName)} <span class="ql-fmt ${cur.format}">${cur.format === 'mcq' ? 'MCQ' : 'TITA'}</span></div><p class="ql-q">${esc(cur.question)}</p>${optionsHTML(cur)}`;
      ['#qlGenInput', '#qlGenCheck'].forEach(id => $(id).classList.toggle('hidden', cur.format === 'mcq'));
      $('#qlGenSolution').classList.add('hidden'); $('#qlGenInput').value = ''; const fb = $('#qlGenFeedback'); fb.textContent = ''; fb.className = 'ql-feedback';
      $('#qlGenHint').textContent = cur.format === 'mcq' ? 'Pick one option (A to D).' : 'Type in the answer (TITA). Fractions like 3/8 are accepted.';
    }
    function reveal() {
      setHTML($('#qlGenViz'), QViz.render(cur.viz));
      $('#qlGenAnswer').textContent = 'Answer: ' + (cur.format === 'mcq' ? QGen.LETTERS[cur.answerIndex] + ') ' : '') + cur.display + (cur.unit ? ' ' + cur.unit : '');
      $('#qlGenSteps').innerHTML = cur.steps.map(s => `<li>${esc(s)}</li>`).join('');
      $('#qlGenTraps').innerHTML = cur.traps.map(t => `<li>${esc(t)}</li>`).join('');
      if (cur.format === 'mcq') $$('#qlGenProblem .ql-opt').forEach((b, i) => b.classList.toggle('right', i === cur.answerIndex));
      $('#qlGenSolution').classList.remove('hidden');
    }
    const check = val => { const ok = QGen.check(cur, val != null ? val : $('#qlGenInput').value); const fb = $('#qlGenFeedback'); fb.className = 'ql-feedback ' + (ok ? 'ok' : 'no'); fb.textContent = ok ? 'Correct. The worked solution is below.' : 'Not quite. Look at the traps below.'; reveal(); };
    $('#qlGenProblem').addEventListener('click', e => { const b = e.target.closest('.ql-opt'); if (!b) return; $$('#qlGenProblem .ql-opt').forEach(x => x.classList.remove('picked')); b.classList.add('picked'); check(QGen.LETTERS[+b.dataset.i]); });
    sel.addEventListener('change', () => newProblem()); $('#qlGenBtn').addEventListener('click', () => newProblem());
    $('#qlGenLevel').addEventListener('click', e => { const b = e.target.closest('button[data-l]'); if (b && LEVELS.includes(b.dataset.l)) { setSeg('#qlGenLevel', b.dataset.l); newProblem(); } });
    $('#qlGenReveal').addEventListener('click', reveal); $('#qlGenCheck').addEventListener('click', () => check());
    $('#qlGenInput').addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
    newProblem(params.get('type'));
    if (params.get('reveal') === '1') reveal();
    redraw.push(() => { if (!$('#qlGenSolution').classList.contains('hidden')) setHTML($('#qlGenViz'), QViz.render(cur.viz)); });
  });
  function setSeg(sel, l) { $$(sel + ' button').forEach(b => { const on = b.dataset.l === l; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); }); }
  function segVal(sel) { const b = $(sel + ' button.on'); return b && LEVELS.includes(b.dataset.l) ? b.dataset.l : 'easy'; }

  /* ---------- concept lab ---------- */
  const labs = [];
  safe('concept lab', () => { if (!$('#tsdCanvas')) return;
    const lab0 = (() => {
      const cv = $('#tsdCanvas'), ctx = cv.getContext('2d'); let raf = 0, t0 = 0, running = false, sim = 0;
      const val = id => +$('#' + id).value;
      const bind = (ids, fn) => ids.forEach(id => $('#' + id).addEventListener('input', fn));
      const outs = () => [['vA', ' km/h'], ['vB', ' km/h'], ['lA', ' m'], ['lB', ' m'], ['cp', ''], ['mk', '%'], ['dc', '%'], ['ra', ''], ['rb', ''], ['aa', ''], ['ab', '']].forEach(([id, u]) => $('#' + id + 'o').textContent = $('#' + id).value + u);
      const info = () => { const a = val('vA') * 5 / 18, b = val('vB') * 5 / 18, opp = $('#dir').value === 'opp', rel = opp ? a + b : Math.abs(a - b), D = val('lA') + val('lB'); return { a, b, opp, rel, D, t: rel ? D / rel : Infinity }; };
      function drawTSD() {
        const W = cv.width, H = cv.height, I = info(), sc = 1.1; ctx.clearRect(0, 0, W, H);
        ctx.fillStyle = P.bg; ctx.fillRect(0, 0, W, H);
        ctx.strokeStyle = P.line; ctx.lineWidth = 3; [95, 175].forEach(y => { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); ctx.fillStyle = P.line; for (let x = (-sim * 40) % 30; x < W; x += 30) ctx.fillRect(x, y + 3, 14, 4); });
        const LA = val('lA') * sc, LB = val('lB') * sc, mid = W / 2; let xa, xb;
        if (I.opp) { xa = mid + I.a * sim * sc; xb = mid - I.b * sim * sc; } else if (I.a >= I.b) { xa = 200 - LB + I.a * sim * sc; xb = 200 + I.b * sim * sc; } else { xa = 200 + I.a * sim * sc; xb = 200 - LA + I.b * sim * sc; }
        const train = (x, y, L, col, right, label) => { const x0 = right ? x - L : x; ctx.fillStyle = col; ctx.beginPath(); ctx.roundRect(x0, y, L, 34, 9); ctx.fill(); ctx.globalAlpha = 0.45; ctx.fillStyle = P.card; for (let w = x0 + 10; w < x0 + L - 22; w += 26) ctx.fillRect(w, y + 8, 16, 10); ctx.globalAlpha = 1; ctx.fillStyle = P.ink; ctx.font = '600 15px Inter, system-ui, sans-serif'; ctx.fillText(label, x0 + 6, y - 10); };
        train(xa, 58, LA, P.brand, true, `A · ${val('vA')} km/h →`);
        if (I.opp) train(xb, 138, LB, P.accent, false, `← B · ${val('vB')} km/h`); else train(xb, 138, LB, P.accent, true, `B · ${val('vB')} km/h →`);
        const crossed = Math.min(I.rel * sim, I.D);
        ctx.fillStyle = P.muted; ctx.font = '14px Inter, system-ui, sans-serif'; ctx.fillText(`t = ${sim.toFixed(1)} s`, 14, 24);
        ctx.fillStyle = P.line; ctx.fillRect(14, H - 22, W - 28, 8); ctx.fillStyle = P.ok; ctx.fillRect(14, H - 22, (W - 28) * (I.D ? crossed / I.D : 0), 8);
        ctx.fillStyle = P.ink; ctx.fillText(`relative distance covered ${crossed.toFixed(0)} / ${I.D} m`, W - 330, 24);
        $('#tsdOut').textContent = `Relative speed = ${I.opp ? 'vA + vB' : '|vA − vB|'} = ${(I.rel * 18 / 5).toFixed(0)} km/h = ${I.rel.toFixed(2)} m/s · Distance = LA + LB = ${I.D} m · Crossing time = ${isFinite(I.t) ? I.t.toFixed(2) + ' s' : 'never (equal speeds)'}`;
      }
      const staticFrame = () => { const I = info(); sim = isFinite(I.t) ? I.t / 2 : 0; drawTSD(); };
      function loop(ts) { if (!t0) t0 = ts; const dt = (ts - t0) / 1000; t0 = ts; if (running) { const I = info(); sim += dt * Math.max(1, I.t / 6); if (sim * I.rel >= I.D + 60 || !isFinite(I.t)) sim = 0; } drawTSD(); raf = requestAnimationFrame(loop); }
      function drawPL() {
        const cp = val('cp'), mk = val('mk'), dc = val('dc'), mp = cp * (1 + mk / 100), sp = mp * (1 - dc / 100), pr = (sp - cp) / cp * 100;
        const max = Math.max(mp, cp) * 1.2, items = [['CP', cp, 'var(--muted)'], ['MP', mp, 'var(--ok)'], ['SP', sp, sp >= cp ? 'var(--brand)' : 'var(--bad)']];
        let b = `<line x1="30" x2="500" y1="240" y2="240" stroke="var(--line)" stroke-width="2"/><line x1="30" x2="500" y1="${240 - cp / max * 200}" y2="${240 - cp / max * 200}" stroke="var(--muted)" stroke-dasharray="5 5"/>`;
        items.forEach(([l, v, c], i) => { const h = v / max * 200, x = 70 + i * 145; b += `<rect x="${x}" y="${240 - h}" width="90" height="${h}" rx="8" fill="${c}"/><text x="${x + 45}" y="${232 - h}" class="s-txt" text-anchor="middle">₹${v.toFixed(0)}</text><text x="${x + 45}" y="262" class="s-mute" text-anchor="middle">${l}</text>`; });
        b += `<text x="260" y="24" class="s-big" text-anchor="middle">${pr >= 0 ? 'Profit' : 'Loss'} ${Math.abs(pr).toFixed(2)}%</text>`;
        $('#plSvg').innerHTML = b;
        $('#plOut').textContent = `MP = ${cp}×${(1 + mk / 100).toFixed(2)} = ${mp.toFixed(0)} · SP = MP×${(1 - dc / 100).toFixed(2)} = ${sp.toFixed(0)} · net = ${mk}% − ${dc}% − ${mk}×${dc}/100 = ${pr.toFixed(2)}%`;
      }
      function drawRA() {
        const a = val('ra'), b = val('rb'), A = val('aa'), B = val('ab'), avg = (a * A + b * B) / (a + b); let s = '';
        const uw = 440 / (a + b); for (let i = 0; i < a + b; i++) s += `<rect x="${40 + i * uw + 2}" y="40" width="${uw - 4}" height="44" rx="6" fill="${i < a ? 'var(--brand)' : 'var(--accent)'}"/>`;
        s += `<text x="${40 + a * uw / 2}" y="30" class="s-txt" text-anchor="middle">A: ${a} parts (${(100 * a / (a + b)).toFixed(0)}%)</text><text x="${40 + a * uw + b * uw / 2}" y="104" class="s-txt" text-anchor="middle">B: ${b} parts</text>`;
        const X = v => 40 + (v - 20) / 80 * 440;
        s += `<line x1="40" x2="480" y1="190" y2="190" stroke="var(--line)" stroke-width="6" stroke-linecap="round"/>`;
        s += `<circle cx="${X(A)}" cy="${180 - a * 2}" r="${6 + a * 2}" fill="var(--brand)"/><circle cx="${X(B)}" cy="${180 - b * 2}" r="${6 + b * 2}" fill="var(--accent)"/>`;
        s += `<polygon points="${X(avg)},196 ${X(avg) - 14},224 ${X(avg) + 14},224" fill="var(--ink)"/><text x="${X(avg)}" y="250" class="s-big" text-anchor="middle">weighted avg ${avg.toFixed(2)}</text>`;
        s += `<text x="40" y="270" class="s-mute">20</text><text x="480" y="270" class="s-mute" text-anchor="end">100</text>`;
        $('#raSvg').innerHTML = s;
        $('#raOut').textContent = `Weighted mean = (${a}×${A} + ${b}×${B}) / ${a + b} = ${avg.toFixed(2)} · simple mean would be ${((A + B) / 2).toFixed(1)} · the average splits the gap B:A = ${b}:${a}`;
      }
      bind(['vA', 'vB', 'lA', 'lB', 'dir'], () => { outs(); if (RM.matches) staticFrame(); else sim = 0; }); bind(['cp', 'mk', 'dc'], () => { outs(); drawPL(); }); bind(['ra', 'rb', 'aa', 'ab'], () => { outs(); drawRA(); });
      $('#dir').addEventListener('change', () => { if (RM.matches) staticFrame(); else sim = 0; });
      $('#tsdRun').addEventListener('click', () => { if (RM.matches) return; running = !running; $('#tsdRun').textContent = running ? 'Pause' : 'Run'; });
      outs(); drawPL(); drawRA();
      return {
        start() { if (RM.matches) { running = false; const b = $('#tsdRun'); b.disabled = true; b.textContent = 'Animation off (reduced motion)'; staticFrame(); return; } const b = $('#tsdRun'); b.disabled = false; if (!raf) { t0 = 0; running = true; b.textContent = 'Pause'; raf = requestAnimationFrame(loop); } },
        stop() { cancelAnimationFrame(raf); raf = 0; },
        paint() { if (RM.matches) staticFrame(); else drawTSD(); drawPL(); drawRA(); }
      };
    })();
    labs.push(lab0);
  });
  safe('concept lab 2', () => { if (!$('#twCanvas')) return;
    const lab2 = (() => {
      const cv = $('#twCanvas'), ctx = cv.getContext('2d'); let t = 0, level = 0, last = 0, raf = 0;
      const v = id => +$('#' + id).value;
      const twInfo = () => { const a = v('twA'), b = v('twB'), c = v('twC'); const net = 1 / a + 1 / b - (c ? 1 / c : 0); return { a, b, c, net, T: net > 0 ? 1 / net : Infinity }; };
      function drawTW() {
        const W = cv.width, H = cv.height, I = twInfo(); ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; ctx.fillRect(0, 0, W, H);
        const tx = 180, ty = 40, tw = 200, th = 170;
        const pipe = (x, label, color, out) => { ctx.fillStyle = color; ctx.fillRect(x, out ? ty + th - 10 : ty - 22, 60, 12); ctx.fillStyle = P.ink; ctx.font = '600 13px Inter, system-ui, sans-serif'; ctx.fillText(label, x, out ? ty + th + 22 : ty - 28); };
        pipe(tx - 70, `A: fills in ${I.a} h`, P.brand); pipe(tx + tw + 10, `B: fills in ${I.b} h`, P.ok); if (I.c) pipe(tx + tw / 2 - 30, `C: empties in ${I.c} h`, P.bad, true);
        ctx.strokeStyle = P.muted; ctx.lineWidth = 4; ctx.strokeRect(tx, ty, tw, th);
        ctx.fillStyle = P.reason; const lh = th * Math.min(level, 1); ctx.fillRect(tx + 2, ty + th - lh, tw - 4, lh);
        ctx.fillStyle = P.ink; ctx.font = '700 22px Inter, system-ui, sans-serif'; ctx.fillText(Math.round(Math.min(level, 1) * 100) + '%', tx + tw / 2 - 24, ty + th / 2);
        ctx.font = '14px Inter, system-ui, sans-serif'; ctx.fillStyle = P.muted; ctx.fillText(`t = ${t.toFixed(1)} h`, 16, 24);
        const bx = 470; [['A', 1 / I.a, P.brand], ['B', 1 / I.b, P.ok], ['C', I.c ? -1 / I.c : 0, P.bad], ['net', I.net, P.accent]].forEach(([l, r, col], i) => { const w = Math.abs(r) * 900; ctx.fillStyle = col; ctx.fillRect(bx + 40, 50 + i * 36, Math.min(w, 200), 22); ctx.fillStyle = P.ink; ctx.font = '13px Inter, system-ui, sans-serif'; ctx.fillText(l, bx, 66 + i * 36); ctx.fillText(`${r >= 0 ? '+' : ''}${(r * 100).toFixed(1)}%/h`, bx + 50 + Math.min(w, 200), 66 + i * 36); });
        $('#twOut').textContent = `Net rate = 1/${I.a} + 1/${I.b}${I.c ? ' − 1/' + I.c : ''} = ${(I.net * 100).toFixed(2)}% of the tank per hour → ${isFinite(I.T) ? 'full in ' + I.T.toFixed(2) + ' h' : 'never fills (the leak is too strong)'}`;
      }
      const staticFrame = () => { const I = twInfo(); t = isFinite(I.T) ? I.T / 2 : 0; level = isFinite(I.T) ? 0.5 : 0; drawTW(); };
      function loop(ts) { const dt = last ? (ts - last) / 1000 : 0; last = ts; const I = twInfo(); if (isFinite(I.T)) { t += dt * I.T / 6; level = Math.max(0, t * I.net); if (level >= 1.15) { t = 0; level = 0; } } drawTW(); raf = requestAnimationFrame(loop); }
      function drawCI() {
        const Pp = v('ciP'), r = v('ciR') / 100, n = v('ciN'), comp = [1, 2, 4, 12].includes(+$('#ciK').value) ? +$('#ciK').value : 1, ci = k => Pp * (1 + r / comp) ** (comp * k), si = k => Pp * (1 + r * k), max = ci(n) * 1.08;
        const sx = k => 50 + k / n * 440, sy = y => 250 - (y - Pp * 0.9) / (max - Pp * 0.9) * 220; let b = `<line x1="50" x2="495" y1="250" y2="250" stroke="var(--line)" stroke-width="2"/>`;
        const path = fn => Array.from({ length: 101 }, (_, i) => { const k = n * i / 100; return (i ? 'L' : 'M') + sx(k).toFixed(1) + ' ' + sy(fn(k)).toFixed(1); }).join('');
        b += `<path d="${path(ci)} L${sx(n)} 250 L50 250 Z" fill="var(--ok)" fill-opacity="0.12"/><path d="${path(ci)}" fill="none" stroke="var(--ok)" stroke-width="3"/><path d="${path(si)}" fill="none" stroke="var(--accent)" stroke-width="3" stroke-dasharray="7 5"/>`;
        for (let k = 0; k <= n; k += Math.max(1, Math.round(n / 10))) b += `<text x="${sx(k)}" y="268" class="s-mute" text-anchor="middle">${k}</text>`;
        b += `<line x1="${sx(n)}" x2="${sx(n)}" y1="${sy(ci(n))}" y2="${sy(si(n))}" stroke="var(--ink)" stroke-dasharray="3 3"/><text x="${sx(n) - 6}" y="${(sy(ci(n)) + sy(si(n))) / 2}" class="s-txt" text-anchor="end">gap ₹${Math.round(ci(n) - si(n)).toLocaleString('en-IN')}</text>`;
        b += `<text x="60" y="26" class="s-txt">— CI ₹${Math.round(ci(n)).toLocaleString('en-IN')}</text><text x="60" y="46" class="s-txt">- - SI ₹${Math.round(si(n)).toLocaleString('en-IN')}</text>`;
        $('#ciSvg').innerHTML = b; $('#ciOut').textContent = `CI = P(1 + r/${comp})^(${comp}·t) vs SI = P(1 + rt) · doubling time ≈ 72/${(r * 100).toFixed(0)} ≈ ${(72 / (r * 100)).toFixed(1)} years (rule of 72)`;
      }
      const BASES = { sq: [x => x * x - 3, 'x² − 3'], abs: [x => Math.abs(x) - 2, '|x| − 2'], lin: [x => x - 1, 'x − 1'], cube: [x => x * x * x / 4 - x, 'x³/4 − x'] };
      function drawFN() {
        const [F, nm] = BASES[$('#fnBase').value] || BASES.sq, h = v('fnH'), k = v('fnK'), a = v('fnA'), abs = $('#fnAbs').checked;
        const G = x => { const y = a * F(x - h) + k; return abs ? Math.abs(y) : y; };
        const pts = fn => Array.from({ length: 161 }, (_, i) => { const x = -8 + i * 0.1; return [x, fn(x)]; });
        setHTML($('#fnSvg'), QViz.render({ type: 'graph', curves: [{ pts: pts(F), color: 'muted' }, { pts: pts(G) }], marks: [], clipY: [-10, 12] }));
        $('#fnOut').textContent = `g(x) = ${abs ? '|' : ''}${a}·f(x ${h >= 0 ? '−' : '+'} ${Math.abs(h)}) ${k >= 0 ? '+' : '−'} ${Math.abs(k)}${abs ? '|' : ''}, f(x) = ${nm} · dashed = original`;
      }
      const outs = () => [['twA', ' h'], ['twB', ' h'], ['twC', ' h'], ['ciP', ''], ['ciR', '%'], ['ciN', ' years'], ['fnH', ''], ['fnK', ''], ['fnA', '']].forEach(([id, u]) => $('#' + id + 'o').textContent = (id === 'twC' && +$('#' + id).value === 0 ? 'none' : $('#' + id).value + u));
      ['twA', 'twB', 'twC'].forEach(id => $('#' + id).addEventListener('input', () => { outs(); t = 0; level = 0; if (RM.matches) staticFrame(); }));
      ['ciP', 'ciR', 'ciN'].forEach(id => $('#' + id).addEventListener('input', () => { outs(); drawCI(); }));
      ['fnH', 'fnK', 'fnA'].forEach(id => $('#' + id).addEventListener('input', () => { outs(); drawFN(); }));
      $('#fnBase').addEventListener('change', drawFN); $('#fnAbs').addEventListener('change', drawFN); $('#ciK').addEventListener('change', drawCI);
      outs(); drawCI(); drawFN(); drawTW();
      return { start() { if (RM.matches) { staticFrame(); return; } if (!raf) { last = 0; raf = requestAnimationFrame(loop); } }, stop() { cancelAnimationFrame(raf); raf = 0; }, paint() { if (RM.matches) staticFrame(); else drawTW(); drawCI(); drawFN(); } };
    })();
    labs.push(lab2);
  });
  labs.forEach(l => l.start());
  redraw.push(() => labs.forEach(l => l.paint()));
  document.addEventListener('visibilitychange', () => labs.forEach(l => document.hidden ? l.stop() : l.start()));

  /* ---------- practice ---------- */
  safe('practice', () => {
    const pTopic = $('#qlPTopic'); if (!pTopic) return;
    pTopic.innerHTML = optgroups('<option value="mixed">Mixed (all topics)</option>') + SECTIONS.map(s => `<option value="sec:${s.id}">Section: ${esc(s.name)}</option>`).join('');
    $('#qlPLevel').addEventListener('click', e => { const b = e.target.closest('button[data-l]'); if (b && LEVELS.includes(b.dataset.l)) setSeg('#qlPLevel', b.dataset.l); });
    const load = () => { const d = { answered: 0, correct: 0, best: 0, sessions: [], byTopic: {} }; try { const o = JSON.parse(localStorage.getItem(STORE) || '{}'); return o && typeof o === 'object' ? Object.assign(d, o) : d; } catch (e) { return d; } };
    const save = s => { try { localStorage.setItem(STORE, JSON.stringify(s)); } catch (e) { } };
    const num = v => (Number.isFinite(+v) ? +v : 0);
    function renderStats() {
      const s = load(), ans = num(s.answered), acc = ans ? Math.round(100 * num(s.correct) / ans) : 0;
      const weak = Object.entries(s.byTopic || {}).filter(([k, v]) => TOPICS[k] && v && num(v.n) >= 2).sort((a, b) => a[1].c / a[1].n - b[1].c / b[1].n)[0];
      const hist = (Array.isArray(s.sessions) ? s.sessions : []).slice(-6).reverse();
      $('#qlPStatsBody').innerHTML = `<div class="ql-stat-row"><div><b>${ans}</b><span>answered</span></div><div><b>${acc}%</b><span>accuracy</span></div><div><b>${num(s.best)}</b><span>best session score</span></div><div><b>${weak ? esc(TN(weak[0])) : '–'}</b><span>focus area</span></div></div>
        <div class="ql-hist">${hist.map(x => `<div><span>${esc(new Date(num(x.at)).toLocaleString())} · ${esc(x.topic)} · ${esc(x.level)}</span><b>${num(x.score)}/${num(x.total)} · ${num(x.secs)} s</b></div>`).join('') || '<div>No sessions yet. Start one above.</div>'}</div>`;
    }
    let S = null, tick = 0;
    const secOf = v => SECTIONS.find(x => 'sec:' + x.id === v);
    function pickTopic() { if (S.topic === 'mixed') return keys[Math.floor(Math.random() * keys.length)]; const sec = secOf(S.topic); if (sec) return sec.topics[Math.floor(Math.random() * sec.topics.length)]; return keys.includes(S.topic) ? S.topic : 'percentages'; }
    function upd() { $('#qlPProg').textContent = `Q ${Math.min(S.i + 1, S.total)} / ${S.total}`; $('#qlPScore').textContent = `Score ${S.score}`; $('#qlPTimer').textContent = `${S.left} s`; $('#qlPTimer').classList.toggle('low', S.left <= 10); $('#qlPBar').style.width = (100 * S.left / S.per) + '%'; }
    function nextQ() {
      if (S.i >= S.total) return finish();
      S.q = QGen.generate(pickTopic(), S.level); S.left = S.per; S.locked = false;
      $('#qlPQ').innerHTML = `<div class="ql-meta">${esc(S.q.topicName)} · ${esc(S.q.typeName)} <span class="ql-fmt ${S.q.format}">${S.q.format === 'mcq' ? 'MCQ' : 'TITA'}</span></div><p class="ql-q">${esc(S.q.question)}</p>${optionsHTML(S.q)}`;
      ['#qlPInput', '#qlPSubmit'].forEach(id => $(id).classList.toggle('hidden', S.q.format === 'mcq'));
      $('#qlPInput').value = ''; $('#qlPFb').textContent = ''; $('#qlPFb').className = 'ql-feedback'; upd();
      clearInterval(tick); tick = setInterval(() => { S.left--; upd(); if (S.left <= 0) answer(null); }, 1000);
    }
    function answer(val) {
      if (!S || S.locked) return; S.locked = true; clearInterval(tick);
      const ok = val != null && QGen.check(S.q, val); if (ok) S.score++;
      const s = load(); s.answered = num(s.answered) + 1; if (ok) s.correct = num(s.correct) + 1; s.byTopic = s.byTopic || {}; const bt = s.byTopic[S.q.topic] || { n: 0, c: 0 }; bt.n++; if (ok) bt.c++; s.byTopic[S.q.topic] = bt; save(s);
      if (S.q.format === 'mcq') $$('#qlPQ .ql-opt').forEach((b, i) => { b.disabled = true; b.classList.toggle('right', i === S.q.answerIndex); });
      const fb = $('#qlPFb'); fb.className = 'ql-feedback ' + (ok ? 'ok' : 'no'); fb.textContent = ok ? 'Correct.' : `${val == null ? "Time's up" : 'Not quite'}. Answer: ${S.q.display}${S.q.unit ? ' ' + S.q.unit : ''}. Trap: ${S.q.traps[0]}`;
      upd(); S.i++; setTimeout(nextQ, ok ? 900 : 2800); renderStats();
    }
    function finish() {
      clearInterval(tick); const secs = Math.round((Date.now() - S.start) / 1000), s = load();
      const label = S.topic === 'mixed' ? 'Mixed' : secOf(S.topic) ? secOf(S.topic).name : TN(S.topic);
      s.sessions = (Array.isArray(s.sessions) ? s.sessions : []).concat({ at: Date.now(), topic: label, level: S.level, score: S.score, total: S.total, secs }).slice(-30); s.best = Math.max(num(s.best), S.score); save(s);
      $('#qlPQ').innerHTML = `<h3>Session complete</h3><p>You scored <b>${S.score}/${S.total}</b> in ${secs} s.</p>`; $('#qlPFb').textContent = '';
      ['#qlPInput', '#qlPSubmit', '#qlPSkip'].forEach(id => $(id).classList.add('hidden')); renderStats(); S = null;
    }
    $('#qlPStart').addEventListener('click', () => {
      const tv = pTopic.value, valid = tv === 'mixed' || keys.includes(tv) || !!secOf(tv);
      S = { topic: valid ? tv : 'mixed', level: segVal('#qlPLevel'), total: [5, 10, 15].includes(+$('#qlPCount').value) ? +$('#qlPCount').value : 10, per: [45, 90, 150].includes(+$('#qlPTime').value) ? +$('#qlPTime').value : 90, i: 0, score: 0, start: Date.now() };
      $('#qlPRun').classList.remove('hidden'); $('#qlPSkip').classList.remove('hidden'); nextQ();
    });
    $('#qlPQ').addEventListener('click', e => { const b = e.target.closest('.ql-opt'); if (b && S && !S.locked) answer(QGen.LETTERS[+b.dataset.i]); });
    $('#qlPSubmit').addEventListener('click', () => answer($('#qlPInput').value)); $('#qlPInput').addEventListener('keydown', e => { if (e.key === 'Enter') answer($('#qlPInput').value); });
    $('#qlPSkip').addEventListener('click', () => answer(null));
    $('#qlPReset').addEventListener('click', () => { if (confirm('Reset all saved Quant Lab practice stats on this device?')) { try { localStorage.removeItem(STORE); } catch (e) { } renderStats(); } });
    renderStats();
  });

  const onScheme = () => { readP(); redraw.forEach(f => { try { f(); } catch (e) { } }); };
  if (DARK.addEventListener) DARK.addEventListener('change', onScheme);
  if (RM.addEventListener) RM.addEventListener('change', () => { labs.forEach(l => { l.stop(); l.start(); }); onScheme(); });
  document.body.dataset.qlReady = '1';
})();
