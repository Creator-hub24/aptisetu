/* Reasoning Lab — visual renderers. Every viz object from a generator becomes SVG (or a 3D canvas). No inline styles: classes + SVG attributes only. */
(function (g) {
  'use strict';
  const RL = g.RL, NS = 'http://www.w3.org/2000/svg';
  let uid = 0;
  function S(tag, a, kids) { const e = document.createElementNS(NS, tag); if (a) for (const k in a) { const v = a[k]; if (v === undefined || v === null || v === false) continue; if (k === 'cls') e.setAttribute('class', v); else if (k === 'text') e.textContent = v; else e.setAttribute(k, v); } (kids || []).forEach(c => c && e.appendChild(c)); return e; }
  function H(tag, a, kids) { const e = document.createElement(tag); if (a) for (const k in a) { const v = a[k]; if (v === undefined || v === null || v === false) continue; if (k === 'cls') e.className = v; else if (k === 'text') e.textContent = v; else e.setAttribute(k, v); } (kids || []).forEach(c => c && e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c)); return e; }
  RL.S = S; RL.H = H;
  const svg = (w, h, kids, label, cls) => { const e = S('svg', { viewBox: `0 0 ${w} ${h}`, role: 'img', 'aria-label': label || 'diagram', cls: cls || '', width: w, height: h, preserveAspectRatio: 'xMidYMid meet' }, kids); e.style.maxWidth = Math.round(Math.max(w * 1.5, Math.min(w * 2.4, 360))) + 'px'; return e; };
  const T = (x, y, s, cls, extra) => S('text', Object.assign({ x, y, cls: 't ' + (cls || ''), 'text-anchor': 'middle', 'dominant-baseline': 'central', text: String(s) }, extra || {}));
  const L = (x1, y1, x2, y2, cls) => S('line', { x1, y1, x2, y2, cls: cls || 's-ink w2' });
  const R = (x, y, w, h, cls, rx) => S('rect', { x, y, width: w, height: h, rx: rx || 0, cls: cls || 'f-card s-line w1' });
  const C = (cx, cy, r, cls) => S('circle', { cx, cy, r, cls: cls || 'f-card s-ink w2' });
  const P = (pts, cls) => S('polygon', { points: pts.map(p => p.join(',')).join(' '), cls: cls || 'f-card s-ink w2' });
  const PL = (pts, cls) => S('polyline', { points: pts.map(p => p.join(',')).join(' '), cls: cls || 'f-none s-ink w2' });
  function arrowHead(x1, y1, x2, y2, size, cls) { const a = Math.atan2(y2 - y1, x2 - x1), s = size || 8; return P([[x2, y2], [x2 - s * Math.cos(a - 0.45), y2 - s * Math.sin(a - 0.45)], [x2 - s * Math.cos(a + 0.45), y2 - s * Math.sin(a + 0.45)]], cls || 'f-ink s-none'); }
  const arrow = (x1, y1, x2, y2, lcls, hcls, size) => S('g', null, [L(x1, y1, x2, y2, lcls || 'f-none s-ink w2'), arrowHead(x1, y1, x2, y2, size, hcls)]);
  const PAINT = c => ({ brand: 'brand', red: 'red', blue: 'blue', green: 'green' })[c] || 'brand';
  const wrap = (el, cap) => { const d = H('div', { cls: 'vizwrap fade-in' }, [el]); if (cap) d.appendChild(H('div', { cls: 'vizcap', text: cap })); return d; };

  // ================= 3D: cube made of unit cubes =================
  const FACES = ['top', 'bottom', 'front', 'back', 'left', 'right'];
  function cubeClasses(dims, paint, removeTop) { const [a, b0, c] = dims; const b = removeTop ? b0 - 1 : b0; const out = [];
    for (let i = 0; i < a; i++) for (let j = 0; j < b; j++) for (let k = 0; k < c; k++) { const f = []; if (j === b - 1 && !removeTop) f.push('top'); if (j === 0) f.push('bottom'); if (k === c - 1) f.push('front'); if (k === 0) f.push('back'); if (i === 0) f.push('left'); if (i === a - 1) f.push('right');
      const pf = f.filter(x => paint[x]); out.push({ i, j, k, faces: pf, colors: [...new Set(pf.map(x => paint[x]))] }); } return { a, b, c, cubes: out }; }
  RL.cubeClasses = cubeClasses;
  function hlTest(hl) { if (!hl) return null; if (hl.faces !== undefined) return u => u.faces.length === hl.faces; if (hl.atleast !== undefined) return u => u.faces.length >= hl.atleast;
    if (hl.colorset) return u => u.colors.length === hl.colorset.length && hl.colorset.every(c => u.colors.includes(c)); if (hl.ncolors !== undefined) return u => u.colors.length === hl.ncolors && (!hl.has || u.colors.includes(hl.has)); return null; }
  function cube3d(v, opt) {
    const cv = H('canvas', { 'aria-label': `3D block ${v.dims.join('×')}${v.hl ? ', highlighted cubes in amber' : ''}. Drag or use arrow keys to rotate.`, role: 'img' });
    const { a, b, c, cubes } = cubeClasses(v.dims, v.paint || {}, v.removeTop); const test = hlTest(v.hl); const nHl = test ? cubes.filter(test).length : 0;
    const build = () => { const col = n => RL.css(n); const key = (i, j, k) => i + ',' + j + ',' + k; const solid = new Map();
      cubes.forEach(u => { const on = test && test(u); if (v.explode && !on) return; solid.set(key(u.i, u.j, u.k), Object.assign({ on }, u)); });
      const ox = -a / 2, oy = -v.dims[1] / 2, oz = -c / 2; const quads = [], lines = []; const D = { top: [0, 1, 0], bottom: [0, -1, 0], front: [0, 0, 1], back: [0, 0, -1], left: [-1, 0, 0], right: [1, 0, 0] };
      const line = col('line'), ink = col('ink'), acc = col('accent'), unp = col('unp');
      for (const u of solid.values()) { const F = RL.boxFaces(ox + u.i, ox + u.i + 1, oy + u.j, oy + u.j + 1, oz + u.k, oz + u.k + 1);
        for (const f of FACES) { const d = D[f]; if (solid.has(key(u.i + d[0], u.j + d[1], u.k + d[2]))) continue; const painted = u.faces.includes(f) && !v.cutsOnly;
          let fill = painted ? col(PAINT(v.paint[f])) : unp; if (u.on) fill = painted ? mix(fill, acc, 0.22) : acc; quads.push({ p: F[f], fill, stroke: u.on ? ink : line, lw: u.on ? 1.4 : 1 }); } }
      const box = RL.boxFaces(ox, ox + a, oy, oy + v.dims[1], oz, oz + c); if (v.explode || v.removeTop) { const E = edges(ox, ox + a, oy, oy + v.dims[1], oz, oz + c); E.forEach(([p, q]) => lines.push({ a: p, b: q, color: col('muted'), dash: true })); }
      void box; return { quads, lines, size: Math.max(a, v.dims[1], c) * 1.85 }; };
    const sc = RL.Scene(cv, build, { spin: !opt.small && !opt.static }); void sc;
    const cap = v.cutsOnly ? `${v.dims.join(' × ')} pieces` : `${v.dims.join(' × ')} block${v.removeTop ? ' (top layer removed)' : ''}${test ? ` · ${nHl} cube${nHl === 1 ? '' : 's'} highlighted` : ''} · drag to rotate`;
    return wrap(cv, cap);
  }
  function hex(c) { c = c.trim(); if (c[0] === '#') { if (c.length === 4) c = '#' + [...c.slice(1)].map(x => x + x).join(''); return [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)); } const m = c.match(/\d+(\.\d+)?/g); return m ? m.slice(0, 3).map(Number) : [128, 128, 128]; }
  function mix(c1, c2, w) { w = w === undefined ? 0.45 : w; const a = hex(c1), b = hex(c2); return 'rgb(' + a.map((x, i) => Math.round(x * w + b[i] * (1 - w))).join(',') + ')'; }
  RL.mix = mix;
  function edges(x0, x1, y0, y1, z0, z1) { const P = [[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0], [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]]; return [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]].map(([i, j]) => [P[i], P[j]]); }

  // ================= 3D die =================
  function die3d(v, opt) {
    const cv = H('canvas', { role: 'img', 'aria-label': `Die: top ${v.die[0]}, front ${v.die[2]}, right ${v.die[5]}. Drag to rotate.` });
    const lab = { top: v.die[0], bottom: v.die[1], front: v.die[2], back: v.die[3], left: v.die[4], right: v.die[5] }; const show = v.show || [];
    const M = RL.m3; const ease = t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    const pre = t => { const k = 1 - ease(t), q = Math.PI / 2 * k; switch (v.roll) { case 'forward': return M.rx(-q); case 'back': return M.rx(q); case 'right': return M.rz(q); case 'left': return M.rz(-q); default: return M.I3; } };
    const build = t => { const F = RL.boxFaces(-1, 1, -1, 1, -1, 1); const Rm = pre(t); const card = RL.css('card'), ink = RL.css('ink'), acc = RL.css('accent'), br = RL.css('brand');
      const quads = FACES.map(f => { const on = show.includes(lab[f]); return { p: F[f].map(p => M.ap(Rm, p)), fill: on ? mix(card, acc) : card, stroke: on ? acc : ink, lw: on ? 3 : 2, label: lab[f], labelColor: on ? ink : br, labelSize: String(lab[f]).length > 1 ? 34 : 56 }; });
      return { quads, size: 4.6 }; };
    RL.Scene(cv, build, { spin: !!v.spin && !opt.static, dur: v.roll ? 1.1 : 0, yaw: -0.62, pitch: 0.5 });
    const cap = v.roll ? `Rolled ${v.roll}: top ${v.die[0]}, front ${v.die[2]}, right ${v.die[5]}` : show.length ? `${show.join(' and ')} highlighted (opposite faces)` : 'Drag to rotate · arrow keys work too';
    return wrap(cv, cap);
  }
  // ================= 2D dice views =================
  function dieIso(x, y, s, [top, front, right], mark) { const d = s * 0.45; const on = l => l === mark;
    const fr = P([[x, y + d], [x + s, y + d], [x + s, y + d + s], [x, y + d + s]], on(front) ? 'f-accentsoft s-accent w3' : 'f-card s-ink w2');
    const tp = P([[x, y + d], [x + d, y], [x + s + d, y], [x + s, y + d]], on(top) ? 'f-accentsoft s-accent w3' : 'f-brandsoft s-ink w2');
    const rt = P([[x + s, y + d], [x + s + d, y], [x + s + d, y + s], [x + s, y + d + s]], on(right) ? 'f-accentsoft s-accent w3' : 'f-line s-ink w2');
    return S('g', null, [fr, tp, rt, T(x + s / 2, y + d + s / 2, front, 'lg b'), T(x + s / 2 + d / 2, y + d / 2, top, 'b', { transform: `translate(0,0)` }), T(x + s + d / 2, y + d / 2 + s / 2, right, 'b')]); }
  function dieviews(v) { const s = v.small ? 54 : 70, d = s * 0.45, gap = 26, w = v.views.length * (s + d + gap) - gap + 10, h = s + d + (v.small ? 10 : 30);
    const kids = v.views.map((vw, i) => S('g', null, [dieIso(5 + i * (s + d + gap), 5, s, vw, v.mark), v.small ? null : T(5 + i * (s + d + gap) + (s + d) / 2, s + d + 20, v.views.length > 1 ? `View ${i + 1}` : 'View', 'sm mu')]));
    return wrap(svg(w, h, kids, 'Dice views: ' + v.views.map(x => `top ${x[0]}, front ${x[1]}, right ${x[2]}`).join('; '))); }
  // ================= nets =================
  const OPPC = ['f-brandsoft', 'f-accentsoft', 'f-oksoft'];
  function netSvg(cells, o) { o = o || {}; const s = o.s || 44; const R0 = Math.min(...cells.map(c => c.r)), C0 = Math.min(...cells.map(c => c.c)); const R1 = Math.max(...cells.map(c => c.r)), C1 = Math.max(...cells.map(c => c.c));
    let pairOf = null; if (o.opp && RL.foldNet) { const d = RL.foldNet(cells); if (d) { pairOf = {}; [[0, 1], [2, 3], [4, 5]].forEach(([i, j], k) => { pairOf[d[i]] = k; pairOf[d[j]] = k; }); } }
    const kids = cells.map(c => { const x = (c.c - C0) * s + 2, y = (c.r - R0) * s + 2; const m = o.mark !== undefined && c.label === o.mark; const cls = (m ? 'f-accent' : pairOf && c.label in pairOf ? OPPC[pairOf[c.label]] : (o.fill || 'f-card')) + ' s-ink w2';
      return S('g', null, [R(x, y, s, s, cls), c.label ? T(x + s / 2, y + s / 2, c.label, s > 30 ? 'lg b' : 'b') : null]); });
    return { el: S('g', null, kids), w: (C1 - C0 + 1) * s + 4, h: (R1 - R0 + 1) * s + 4 }; }
  function net(v) { const n = netSvg(v.cells, { opp: v.opp, mark: v.mark, s: v.small ? 22 : 44 }); return wrap(svg(n.w, n.h, [n.el], 'Cube net'), v.opp ? 'Same colour = opposite faces (they never touch once folded)' : null); }
  function nets(v) { const items = v.shapes.map((cells, i) => { const n = netSvg(cells, { s: 22, fill: v.reveal ? (RL.foldNet(cells) ? 'f-oksoft' : 'f-badsoft') : 'f-card' }); return { n, i, ok: RL.foldNet(cells) }; });
    let x = 4; const kids = []; const H0 = Math.max(...items.map(t => t.n.h)) + 26; items.forEach(t => { kids.push(S('g', { transform: `translate(${x},4)` }, [t.n.el])); kids.push(T(x + t.n.w / 2, H0 - 8, `(${String.fromCharCode(97 + t.i)})${v.reveal ? (t.ok ? ' ✓' : ' ✗') : ''}`, 'sm b' + (v.reveal ? (t.ok ? ' okc' : ' badc') : ''))); x += t.n.w + 16; });
    return wrap(svg(x, H0, kids, 'Candidate nets')); }
  function netfold(v) {
    const cells = v.cells.map(c => Object.assign({}, c)); const idx = (r, c) => cells.findIndex(x => x.r === r && x.c === c);
    const nb = i => [[0, 1], [1, 0], [0, -1], [-1, 0]].map(([dr, dc]) => idx(cells[i].r + dr, cells[i].c + dc)).filter(j => j >= 0);
    let root = 0; cells.forEach((_, i) => { if (nb(i).length > nb(root).length) root = i; }); const par = new Array(cells.length).fill(-2); par[root] = -1; const order = [root];
    for (let q = 0; q < order.length; q++) for (const j of nb(order[q])) if (par[j] === -2) { par[j] = order[q]; order.push(j); }
    const flat = (r, c) => [c, -r, 0]; let amt = RL.reduced() ? 1 : 0;
    const hinge = i => { const p = cells[par[i]], q = cells[i]; let a, b; if (q.r === p.r) { const x = Math.max(p.c, q.c); a = [x, -p.r, 0]; b = [x, -p.r - 1, 0]; } else { const y = -Math.max(p.r, q.r); a = [p.c, y, 0]; b = [p.c + 1, y, 0]; }
      const u = [b[0] - a[0], b[1] - a[1], 0]; const ctr = [q.c + 0.5, -q.r - 0.5, 0]; const test = RL.m3.axisRot(a, u, 0.3)(ctr); const sgn = test[2] < 0 ? 1 : -1; return { a, u, sgn }; };
    const H_ = cells.map((_, i) => par[i] >= 0 ? hinge(i) : null);
    const xf = (i, p, ang) => { let cur = p, k = i; while (par[k] >= 0) { const h = H_[k]; cur = RL.m3.axisRot(h.a, h.u, h.sgn * ang)(cur); k = par[k]; } return cur; };
    const fc = cells.reduce((s, c) => [s[0] + c.c + 0.5, s[1] - c.r - 0.5], [0, 0]).map(x => x / cells.length); const rc = [cells[root].c + 0.5, -cells[root].r - 0.5];
    const build = () => { const ang = amt * Math.PI / 2; const shift = [fc[0] + (rc[0] - fc[0]) * amt, fc[1] + (rc[1] - fc[1]) * amt, -0.5 * amt]; const card = RL.css('card'), ink = RL.css('ink'), br = RL.css('brand'), soft = RL.css('line'), acc = RL.css('accent');
      const quads = cells.map((c, i) => { const p0 = flat(c.r, c.c); const corners = [p0, [p0[0] + 1, p0[1], 0], [p0[0] + 1, p0[1] - 1, 0], [p0[0], p0[1] - 1, 0]].map(p => xf(i, p, ang)).map(p => [p[0] - shift[0], p[1] - shift[1], p[2] - shift[2]]);
        const on = v.mark !== undefined && c.label === v.mark; return { p: corners, fill: on ? mix(card, acc) : card, stroke: ink, lw: 2, label: c.label, labelColor: br, labelSize: 50, both: true, backFill: soft }; });
      return { quads: quads.map(q => q), size: 2.3 + (1 - amt) * 3.6 }; };
    const cv = H('canvas', { role: 'img', 'aria-label': 'Net folding into a cube. Use the slider to fold and unfold.' });
    const sc = RL.Scene(cv, build, { yaw: -0.5, pitch: 0.45 });
    const sl = H('input', { type: 'range', min: '0', max: '100', value: String(amt * 100), 'aria-label': 'Fold amount' }); sl.addEventListener('input', () => { amt = sl.value / 100; sc.redraw(); });
    const play = H('button', { cls: 'btn ghost small', type: 'button', text: '▶ Fold' }); let tm = 0;
    play.addEventListener('click', () => { if (RL.reduced()) { amt = amt > 0.5 ? 0 : 1; sl.value = amt * 100; sc.redraw(); return; } cancelAnimationFrame(tm); const start = performance.now(), from = amt > 0.95 ? 0 : amt; const step = now => { amt = Math.min(1, from + (now - start) / 2200); sl.value = amt * 100; sc.redraw(); if (amt < 1 && cv.isConnected) tm = requestAnimationFrame(step); }; tm = requestAnimationFrame(step); });
    const box = H("div", { cls: "c3wrap" }, [cv, H("div", { cls: "row" }, [play, sl])]);
    if (!RL.reduced() && !v.noauto) setTimeout(() => { if (cv.isConnected) play.click(); }, 500);
    return wrap(box, 'Printed side stays outside · drag to rotate');
  }
  // ================= paper folding =================
  function regions(N, folds) { const rs = [{ x0: 0, x1: N, y0: 0, y1: N }]; for (const f of folds) { const r = Object.assign({}, rs[rs.length - 1]); const mx = (r.x0 + r.x1) / 2, my = (r.y0 + r.y1) / 2; if (f === 'L') r.x0 = mx; if (f === 'R') r.x1 = mx; if (f === 'T') r.y0 = my; if (f === 'B') r.y1 = my; rs.push(r); } return rs; }
  function unfoldHoles(N, folds, punches) { const rs = regions(N, folds); let Hs = punches.map(p => p.slice()); for (let i = folds.length - 1; i >= 0; i--) { const r = rs[i], f = folds[i]; const ref = (f === 'L' || f === 'R') ? ([x, y]) => [r.x0 + r.x1 - 1 - x, y] : ([x, y]) => [x, r.y0 + r.y1 - 1 - y]; Hs = Hs.concat(Hs.map(ref)); } const k = new Set(); return Hs.filter(h => { const s = h.join(); if (k.has(s)) return false; k.add(s); return true; }); }
  RL.unfoldHoles = unfoldHoles;
  function sheet(N, s, region, holes, foldLine, foldDir, title) { const cs = s / N, kids = [R(0, 0, s, s, 'f-none s-line w1 dash')];
    for (let i = 1; i < N; i++) { kids.push(L(i * cs, 0, i * cs, s, 's-line w1')); kids.push(L(0, i * cs, s, i * cs, 's-line w1')); }
    kids.push(R(region.x0 * cs, region.y0 * cs, (region.x1 - region.x0) * cs, (region.y1 - region.y0) * cs, 'f-brandsoft s-brand w2'));
    (holes || []).forEach(([x, y]) => kids.push(C((x + 0.5) * cs, (y + 0.5) * cs, cs * 0.28, 'f-ink s-none anim-pop')));
    if (foldLine) { const r = region, mx = (r.x0 + r.x1) / 2 * cs, my = (r.y0 + r.y1) / 2 * cs; const vx = foldDir === 'L' || foldDir === 'R';
      kids.push(vx ? L(mx, r.y0 * cs - 4, mx, r.y1 * cs + 4, 's-accent w3 dash') : L(r.x0 * cs - 4, my, r.x1 * cs + 4, my, 's-accent w3 dash'));
      const cy = (r.y0 + r.y1) / 2 * cs, cx = (r.x0 + r.x1) / 2 * cs; const q = cs * 1.2;
      if (foldDir === 'L') kids.push(arrow(mx - q, cy, mx + q * 0.6, cy, 's-accent w3', 'f-accent')); if (foldDir === 'R') kids.push(arrow(mx + q, cy, mx - q * 0.6, cy, 's-accent w3', 'f-accent'));
      if (foldDir === 'T') kids.push(arrow(cx, my - q, cx, my + q * 0.6, 's-accent w3', 'f-accent')); if (foldDir === 'B') kids.push(arrow(cx, my + q, cx, my - q * 0.6, 's-accent w3', 'f-accent')); }
    return { kids, title }; }
  const FOLDW = { L: 'left half over the right', R: 'right half over the left', T: 'top half down', B: 'bottom half up' };
  function paperfold(v) { const s = 120, gap = 28; const rs = regions(v.N, v.folds); const panels = [];
    v.folds.forEach((f, i) => panels.push(sheet(v.N, s, rs[i], null, true, f, `Fold ${i + 1}`)));
    if (v.stage !== 'fold') panels.push(sheet(v.N, s, rs[rs.length - 1], v.punches, false, null, 'Punch'));
    if (v.stage === 'unfold') panels.push(sheet(v.N, s, { x0: 0, x1: v.N, y0: 0, y1: v.N }, unfoldHoles(v.N, v.folds, v.punches), false, null, 'Unfolded'));
    const kids = panels.map((p, i) => S('g', { transform: `translate(${10 + i * (s + gap)},10)` }, p.kids.concat([T(s / 2, s + 16, p.title, 'sm b mu')])));
    return wrap(svg(panels.length * (s + gap) - gap + 20, s + 34, kids, 'Paper folding: ' + v.folds.map(f => FOLDW[f]).join(', ')), v.folds.map((f, i) => `${i + 1}: ${FOLDW[f]}`).join(' · ')); }
  function paper(v) { const s = v.small ? 80 : 150; const p = sheet(v.N, s, { x0: 0, x1: v.N, y0: 0, y1: v.N }, v.holes, false); return wrap(svg(s + 8, s + 8, [S('g', { transform: 'translate(4,4)' }, p.kids)], `Unfolded sheet with ${v.holes.length} holes`)); }
  function note(v) { return H('div', { cls: 'out', text: v.text }); }
  // ================= mirror =================
  function glyphs(v) { const n = v.chars.length, w = 40, h = 60, pad = 16; const W = n * w + pad * 2 + (v.mirror === 'v' ? 24 : 0), Hh = h + pad * 2 + (v.mirror === 'h' ? 20 : 0);
    const kids = v.chars.map(([ch, fx, fy], i) => { const cx = pad + i * w + w / 2, cy = pad + h / 2; const t = S('text', { x: 0, y: 0, cls: 't xl b mono', 'text-anchor': 'middle', 'dominant-baseline': 'central', transform: `translate(${cx},${cy}) scale(${fx ? -1 : 1},${fy ? -1 : 1})`, text: ch });
      return S('g', null, [v.hl ? R(pad + i * w + 2, pad + 2, w - 4, h - 4, v.hl[i] ? 'f-oksoft s-ok w1' : 'f-badsoft s-bad w1', 6) : null, t]); });
    if (v.mirror === 'v') kids.push(L(W - 14, 6, W - 14, Hh - 6, 's-brand w3 dash')); if (v.mirror === 'h') kids.push(L(6, Hh - 12, W - 6, Hh - 12, 's-brand w3 dash'));
    return wrap(svg(W, Hh, kids, 'Letters: ' + v.chars.map(c => c[0]).join(''))); }
  function clockFace(cx, cy, r, h, m, cls) { const kids = [C(cx, cy, r, 'f-card s-ink w3')]; for (let i = 0; i < 60; i++) { const a = i * Math.PI / 30, big = i % 5 === 0; kids.push(L(cx + Math.sin(a) * r * (big ? 0.85 : 0.92), cy - Math.cos(a) * r * (big ? 0.85 : 0.92), cx + Math.sin(a) * r * 0.97, cy - Math.cos(a) * r * 0.97, big ? 's-ink w2' : 's-line w1')); }
    for (let i = 1; i <= 12; i++) { const a = i * Math.PI / 6; kids.push(T(cx + Math.sin(a) * r * 0.7, cy - Math.cos(a) * r * 0.7, i, 'sm b mu')); }
    return kids; }
  function hands(cx, cy, r, h, m, ghost) { const ha = ((h % 12) * 30 + m * 0.5) * Math.PI / 180, ma = m * 6 * Math.PI / 180; const c1 = ghost ? 's-muted w3 dash op5' : 's-brand w4', c2 = ghost ? 's-muted w2 dash op5' : 's-ink w3';
    return [L(cx, cy, cx + Math.sin(ha) * r * 0.5, cy - Math.cos(ha) * r * 0.5, c1), L(cx, cy, cx + Math.sin(ma) * r * 0.8, cy - Math.cos(ma) * r * 0.8, c2)]; }
  function clock(v) { const s = 200, r = 88; const kids = clockFace(100, 100, r); if (v.ghost) kids.push(...hands(100, 100, r, v.ghost[0], v.ghost[1], true)); kids.push(...hands(100, 100, r, v.h, v.m)); kids.push(C(100, 100, 4, 'f-ink s-none'));
    if (v.mirrored) kids.push(v.axis === 'h' ? L(8, 196, 192, 196, 's-brand w3 dash') : L(196, 8, 196, 192, 's-brand w3 dash'));
    const pad = n => String(n).padStart(2, '0'); return wrap(svg(s, s, kids, `Clock showing ${v.h}:${pad(v.m)}`), `${v.h}:${pad(v.m)}${v.ghost ? ` (dashed: ${v.ghost[0]}:${pad(v.ghost[1])})` : ''}`); }
  function cells(v) { const s = v.small ? 18 : 30, N = v.N, W = N * s + 4 + (v.axis ? 14 : 0); const kids = []; for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) kids.push(R(2 + c * s, 2 + r * s, s, s, v.cells.some(x => x[0] === r && x[1] === c) ? 'f-brand s-line w1' : 'f-card s-line w1'));
    if (v.axis === 'v') kids.push(L(N * s + 10, 0, N * s + 10, N * s + 4, 's-accent w3 dash')); if (v.axis === 'h') kids.push(L(0, N * s + 10, N * s + 4, N * s + 10, 's-accent w3 dash'));
    return wrap(svg(W, N * s + 4 + (v.axis ? 14 : 0), kids, 'Shaded grid')); }
  // ================= figure counting =================
  function segFrame(segs, w) { const xs = segs.flatMap(s => [s[0], s[2]]), ys = segs.flatMap(s => [s[1], s[3]]); const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys); const k = (w - 16) / Math.max(x1 - x0, y1 - y0, 1); return { k, f: (x, y) => [8 + (x - x0) * k, 8 + (y - y0) * k], h: (y1 - y0) * k + 16, w: (x1 - x0) * k + 16 }; }
  function segs(v) { const F = segFrame(v.segs, 240); const draw = (hlPoly, scale) => { const kids = []; if (hlPoly) kids.push(P(hlPoly.map(([x, y]) => F.f(x, y)), 'f-accent s-accent w2 op5')); v.segs.forEach(s => { const a = F.f(s[0], s[1]), b = F.f(s[2], s[3]); kids.push(L(a[0], a[1], b[0], b[1], 's-ink w2')); }); return kids; };
    if (!v.hl || !v.hl.length) return wrap(svg(F.w, F.h, draw(null), 'Figure made of line segments'));
    const items = v.hl.map((poly, i) => S('g', { transform: `translate(${i * (F.w * 0.55 + 8)},0) scale(0.55)` }, draw(poly)));
    return wrap(svg(v.hl.length * (F.w * 0.55 + 8), F.h * 0.55, items, 'Highlighted shapes'), `${v.hl.length} example${v.hl.length > 1 ? 's' : ''} highlighted`); }
  // ================= blood relations =================
  function family(v) { const ppl = v.people; if (!ppl.length) return note({ text: 'Start with the person the question is about and add one relation at a time.' });
    const gen = {}; ppl.forEach(p => gen[p.id] = 0); for (let it = 0; it < 40; it++) { let ch = false; v.par.forEach(([a, b]) => { if (gen[b] < gen[a] + 1) { gen[b] = gen[a] + 1; ch = true; } }); v.sp.concat(v.sib).forEach(([a, b]) => { const m = Math.max(gen[a], gen[b]); if (gen[a] !== m || gen[b] !== m) { gen[a] = gen[b] = m; ch = true; } }); if (!ch) break; }
    const G = Math.max(...Object.values(gen)); const rows = []; for (let k = 0; k <= G; k++) rows.push(ppl.filter(p => gen[p.id] === k).map(p => p.id));
    const pos = {}; const dx = 84, dy = 92;
    rows.forEach((row, k) => { const parentX = id => { const ps = v.par.filter(e => e[1] === id).map(e => pos[e[0]]).filter(x => x !== undefined); return ps.length ? ps.reduce((s, x) => s + x, 0) / ps.length : 1e3 + row.indexOf(id); };
      row.sort((a, b) => parentX(a) - parentX(b)); // keep spouses adjacent
      const ordered = []; row.forEach(id => { if (ordered.includes(id)) return; ordered.push(id); v.sp.forEach(([a, b]) => { const o = a === id ? b : b === id ? a : null; if (o && row.includes(o) && !ordered.includes(o)) ordered.push(o); }); });
      rows[k] = ordered; ordered.forEach((id, i) => pos[id] = i); });
    const W = Math.max(...rows.map(r => r.length)) * dx + 30; const X = id => { const row = rows[gen[id]]; return (W - row.length * dx) / 2 + pos[id] * dx + dx / 2; }; const Y = id => 36 + gen[id] * dy;
    const kids = []; const hl = v.hl || [];
    v.sp.forEach(([a, b]) => { kids.push(L(X(a), Y(a) - 3, X(b), Y(b) - 3, 's-ink w2')); kids.push(L(X(a), Y(a) + 3, X(b), Y(b) + 3, 's-ink w2')); });
    v.par.forEach(([a, b]) => { const spouse = v.sp.find(e => e.includes(a)); const o = spouse ? (spouse[0] === a ? spouse[1] : spouse[0]) : null; const both = o && v.par.some(e => e[0] === o && e[1] === b); const sx = both ? (X(a) + X(o)) / 2 : X(a);
      kids.push(PL([[sx, Y(a) + (both ? 0 : 22)], [sx, (Y(a) + Y(b)) / 2], [X(b), (Y(a) + Y(b)) / 2], [X(b), Y(b) - 22]], 'f-none s-muted w2')); });
    v.sib.forEach(([a, b]) => kids.push(PL([[X(a), Y(a) - 22], [X(a), Y(a) - 34], [X(b), Y(b) - 34], [X(b), Y(b) - 22]], 'f-none s-muted w2 dash')));
    ppl.forEach(p => { const x = X(p.id), y = Y(p.id), on = hl.includes(p.id); const cls = on ? 'f-accentsoft s-accent w3' : 'f-card s-ink w2';
      kids.push(p.g === 'M' ? R(x - 20, y - 20, 40, 40, cls, 6) : p.g === 'F' ? C(x, y, 21, cls) : P([[x, y - 23], [x + 23, y], [x, y + 23], [x - 23, y]], cls)); kids.push(T(x, y, p.id, 'b')); });
    const H0 = 36 + G * dy + 40; return wrap(svg(W, H0, kids, 'Family tree'), '□ male · ○ female · ◇ unknown · = married · dashed = siblings'); }
  function coderel(v) { return H('div', { cls: 'card' }, [H('div', { cls: 'mono qtext b', text: v.expr }), H('ul', { cls: 'list small' }, v.legend.map(l => H('li', { text: l })))]); }
  // ================= directions =================
  const DIRS4 = ['N', 'E', 'S', 'W'], DIRS8 = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  function rose(cx, cy, r, n, face) { const kids = [C(cx, cy, r, 'f-card s-line w2')]; const names = n === 8 ? DIRS8 : DIRS4;
    names.forEach((d, i) => { const a = i * 2 * Math.PI / names.length; kids.push(L(cx + Math.sin(a) * r * 0.82, cy - Math.cos(a) * r * 0.82, cx + Math.sin(a) * r, cy - Math.cos(a) * r, 's-muted w2')); kids.push(T(cx + Math.sin(a) * (r + 16), cy - Math.cos(a) * (r + 16), d, 'sm b ' + (i === face ? 'br' : 'mu'))); });
    if (face !== null && face !== undefined) { const a = face * 2 * Math.PI / names.length; kids.push(arrow(cx, cy, cx + Math.sin(a) * r * 0.78, cy - Math.cos(a) * r * 0.78, 's-brand w4', 'f-brand', 14)); }
    kids.push(C(cx, cy, 5, 'f-ink s-none')); return kids; }
  function compass(v) { return wrap(svg(200, 200, rose(100, 100, 68, 4, v.face), 'Compass, facing ' + DIRS4[v.face]), 'Facing ' + ['north', 'east', 'south', 'west'][v.face]); }
  function compass8(v) { return wrap(svg(200, 200, rose(100, 100, 68, 8, v.face), 'Compass, facing ' + DIRS8[v.face]), 'Facing ' + DIRS8[v.face]); }
  function sun(v) { const kids = rose(110, 110, 64, 4, v.face); const sx = v.time === 'morning' ? 205 : 15; kids.push(C(sx, 110, 13, 'f-accent s-accent w2')); for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; kids.push(L(sx + Math.cos(a) * 17, 110 + Math.sin(a) * 17, sx + Math.cos(a) * 23, 110 + Math.sin(a) * 23, 's-accent w2')); }
    const shx = v.time === 'morning' ? 40 : 180; kids.push(L(110, 110, shx, 110, 's-muted w4 dash'));
    return wrap(svg(220, 220, kids, `${v.time} sun; shadow falls ${v.time === 'morning' ? 'west' : 'east'}`), `${v.time === 'morning' ? 'Morning: sun in the east, shadow to the west' : 'Evening: sun in the west, shadow to the east'}${v.side ? ` · shadow on the ${v.side}` : ''}`); }
  function fit(pts, w, h, pad) { const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]); const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys); const k = Math.min((w - 2 * pad) / Math.max(x1 - x0, 1), (h - 2 * pad) / Math.max(y1 - y0, 1), 26);
    const ox = (w - (x1 - x0) * k) / 2, oy = (h - (y1 - y0) * k) / 2; return (x, y) => [ox + (x - x0) * k, oy + (y1 - y) * k]; }
  function path(v) { const w = 300, h = 240; const f = fit(v.pts, w, h, 34); const kids = [northMark(w - 22, 30)]; const Q = v.pts.map(p => f(p[0], p[1]));
    for (let i = 1; i < Q.length; i++) { kids.push(arrow(Q[i - 1][0], Q[i - 1][1], Q[i][0], Q[i][1], 's-brand w3', 'f-brand', 10)); const d = Math.hypot(v.pts[i][0] - v.pts[i - 1][0], v.pts[i][1] - v.pts[i - 1][1]); kids.push(T((Q[i - 1][0] + Q[i][0]) / 2 + (Q[i][1] === Q[i - 1][1] ? 0 : 14), (Q[i - 1][1] + Q[i][1]) / 2 + (Q[i][1] === Q[i - 1][1] ? -11 : 0), Math.round(d * 10) / 10, 'sm mu')); }
    const e = Q[Q.length - 1]; if (v.final && Q.length > 1) kids.push(L(Q[0][0], Q[0][1], e[0], e[1], 's-accent w3 dash'));
    kids.push(C(Q[0][0], Q[0][1], 7, 'f-ok s-none')); kids.push(T(Q[0][0], Q[0][1] + 16, 'Start', 'sm b okc')); if (Q.length > 1) { kids.push(C(e[0], e[1], 7, 'f-bad s-none')); kids.push(T(e[0], e[1] - 16, 'End', 'sm b badc')); }
    if (v.face !== undefined && v.face !== null) { const a = v.face * Math.PI / 2; kids.push(arrow(e[0], e[1], e[0] + Math.sin(a) * 30, e[1] - Math.cos(a) * 30, 's-accent w3', 'f-accent', 10)); }
    const sx = v.pts[v.pts.length - 1][0] - v.pts[0][0], sy = v.pts[v.pts.length - 1][1] - v.pts[0][1];
    return wrap(svg(w, h, kids, 'Walking path'), v.final ? `Straight-line distance √(${Math.abs(sx)}² + ${Math.abs(sy)}²) = ${Math.round(Math.hypot(sx, sy) * 100) / 100}` : null); }
  const northMark = (x, y) => S('g', null, [arrow(x, y + 14, x, y - 10, 's-muted w2', 'f-muted', 8), T(x, y + 24, 'N', 'sm b mu')]);
  function points(v) { const w = 300, h = 240; const f = fit(v.pts.map(p => [p[1], p[2]]), w, h, 36); const at = {}; v.pts.forEach(p => at[p[0]] = f(p[1], p[2])); const raw = {}; v.pts.forEach(p => raw[p[0]] = [p[1], p[2]]); const kids = [northMark(w - 22, 30)];
    v.links.forEach(([a, b]) => { kids.push(L(at[a][0], at[a][1], at[b][0], at[b][1], 's-muted w2')); const d = Math.hypot(raw[a][0] - raw[b][0], raw[a][1] - raw[b][1]); kids.push(T((at[a][0] + at[b][0]) / 2 + 9, (at[a][1] + at[b][1]) / 2 - 9, Math.round(d * 10) / 10, 'sm mu')); });
    if (v.hl) { const [a, b] = v.hl; kids.push(L(at[a][0], at[a][1], at[b][0], at[b][1], 's-accent w3 dash')); }
    v.pts.forEach(([n]) => { const on = v.hl && v.hl.includes(n); kids.push(C(at[n][0], at[n][1], 12, on ? 'f-accent s-ink w2' : 'f-card s-ink w2')); kids.push(T(at[n][0], at[n][1], n, 'sm b')); });
    return wrap(svg(w, h, kids, 'Points map')); }
  // ================= syllogism Venn =================
  function venn(v, opt) { const k = v.sets.length; const Wd = 300, Hd = k === 4 ? 250 : 230;
    const shapes = k === 2 ? [{ cx: 115, cy: 115, rx: 75, ry: 75, rot: 0 }, { cx: 185, cy: 115, rx: 75, ry: 75, rot: 0 }]
      : k === 3 ? [{ cx: 118, cy: 92, rx: 68, ry: 68, rot: 0 }, { cx: 182, cy: 92, rx: 68, ry: 68, rot: 0 }, { cx: 150, cy: 148, rx: 68, ry: 68, rot: 0 }]
      : [{ cx: 128, cy: 140, rx: 112, ry: 60, rot: 45 }, { cx: 172, cy: 140, rx: 112, ry: 60, rot: -45 }, { cx: 150, cy: 110, rx: 112, ry: 60, rot: 45 }, { cx: 150, cy: 110, rx: 112, ry: 60, rot: -45 }];
    if (k === 4) { shapes[0] = { cx: 120, cy: 145, rx: 110, ry: 58, rot: 45 }; shapes[1] = { cx: 180, cy: 145, rx: 110, ry: 58, rot: -45 }; shapes[2] = { cx: 150, cy: 112, rx: 110, ry: 58, rot: 45 }; shapes[3] = { cx: 150, cy: 112, rx: 110, ry: 58, rot: -45 }; shapes[2].cx = 165; shapes[3].cx = 135; }
    const inS = (s, x, y) => { const a = -s.rot * Math.PI / 180, dx = x - s.cx, dy = y - s.cy; const u = dx * Math.cos(a) - dy * Math.sin(a), w = dx * Math.sin(a) + dy * Math.cos(a); return (u * u) / (s.rx * s.rx) + (w * w) / (s.ry * s.ry) <= 1; };
    const shp = (s, cls) => S('ellipse', { cx: s.cx, cy: s.cy, rx: s.rx, ry: s.ry, transform: s.rot ? `rotate(${s.rot} ${s.cx} ${s.cy})` : null, cls });
    const id = 'v' + (++uid); const defs = S('defs'); const kids = [defs];
    const regs = v.regions; const R_ = (1 << k) - 1;
    // centroids by sampling
    const acc = {}; for (let x = 0; x < Wd; x += 3) for (let y = 0; y < Hd; y += 3) { let m = 0; shapes.forEach((s, i) => { if (inS(s, x, y)) m |= 1 << i; }); if (!m) continue; (acc[m] = acc[m] || []).push([x, y]); }
    const cen = m => { const a = acc[m]; if (!a) return null; // pick the sample point deepest inside (max distance to region boundary approx = median)
      const mx = a.reduce((s, p) => s + p[0], 0) / a.length, my = a.reduce((s, p) => s + p[1], 0) / a.length; let best = a[0], bd = 1e9; a.forEach(p => { const d = Math.hypot(p[0] - mx, p[1] - my); if (d < bd) { bd = d; best = p; } }); return best; };
    for (let r = 1; r <= R_; r++) { const st = regs[r - 1]; if (st === 'maybe') continue; const cls = st === 'empty' ? 'f-empty' : 'f-brandsoft'; let inner = R(0, 0, Wd, Hd, cls + ' s-none');
      const ex = shapes.filter((_, i) => !((r >> i) & 1)); if (ex.length) { const mk = S('mask', { id: id + 'm' + r }, [R(0, 0, Wd, Hd, 'f-white')].concat(ex.map(s => shp(s, '')))); mk.firstChild.setAttribute('fill', '#fff'); [...mk.childNodes].slice(1).forEach(n => n.setAttribute('fill', '#000')); defs.appendChild(mk); inner = S('g', { mask: `url(#${id}m${r})` }, [inner]); }
      shapes.forEach((s, i) => { if ((r >> i) & 1) { const cp = S('clipPath', { id: id + 'c' + r + '_' + i }, [shp(s, '')]); defs.appendChild(cp); inner = S('g', { 'clip-path': `url(#${id}c${r}_${i})` }, [inner]); } });
      kids.push(inner); }
    shapes.forEach((s, i) => kids.push(shp(s, 'f-none ' + (v.hl && v.hl.includes(i) ? 's-accent w4' : 's-ink w2'))));
    for (let r = 1; r <= R_; r++) { const p = cen(r); if (!p) continue; const st = regs[r - 1]; if (st === 'some') kids.push(T(p[0], p[1], '✕', 'b br')); else if (st === 'maybe') kids.push(T(p[0], p[1], '?', 'sm mu')); }
    (v.spread || []).forEach(G => { const pts = G.map(cen).filter(Boolean); if (pts.length < 2) return; for (let q = 1; q < pts.length; q++) kids.push(L(pts[q - 1][0], pts[q - 1][1], pts[q][0], pts[q][1], 's-accent w2 dash'));
      const a = pts[0], b = pts[1]; kids.push(T((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, '✕', 'b ac')); });
    const lp = k === 2 ? [[70, 26], [230, 26]] : k === 3 ? [[62, 24], [238, 24], [150, 228]] : [[22, 236], [278, 236], [262, 16], [38, 16]];
    shapes.forEach((s, i) => kids.push(T(lp[i][0], lp[i][1], v.sets[i], 'b' + (v.hl && v.hl.includes(i) ? ' ac' : ''), { 'text-anchor': k === 4 ? (i % 3 === 0 ? 'start' : 'end') : 'middle' })));
    const main = svg(Wd, Hd + 6, kids, 'Venn diagram of ' + v.sets.join(', '));
    const box = H('div', null, [main]); if (v.alt && !opt.nested) { box.appendChild(H('div', { cls: 'vizcap', text: 'A possible case that breaks the conclusion:' })); box.appendChild(venn({ sets: v.sets, regions: v.alt, hl: v.hl }, { nested: true })); }
    return opt.nested ? main : wrap(box, 'Grey = must be empty · ✕ = must have members · ? = may or may not' + (v.spread && v.spread.length ? ' · amber ✕ on a dashed line = at least one linked region has members' : '')); }
  // ================= inequality =================
  function ineq(v) { const rows = v.stmts.map(st => H('div', { cls: 'row' }, st.map((t, i) => i % 2 ? H('span', { cls: 'chip', text: t }) : H('span', { cls: 'pill' + (v.hl && v.hl.includes(t) ? ' sel' : ''), text: t }))));
    return wrap(H('div', { cls: 'grid' }, rows), v.hl ? `Compare ${v.hl.join(' and ')} along one chain` : 'Read each chain left to right'); }
  // ================= coding =================
  const A1 = ch => ch.charCodeAt(0) - 64;
  function shift(v) { const n = v.from.length, w = 40; const kids = []; const W = n * w + 20;
    [...v.from].forEach((ch, i) => { const x = 10 + i * w + w / 2; kids.push(R(x - 16, 8, 32, 32, 'f-brandsoft s-brand w1', 6)); kids.push(T(x, 24, ch, 'lg b mono')); kids.push(T(x, 52, v.nums ? v.nums[i] : A1(ch), 'sm mu'));
      if (v.to) { const t = v.to[i]; kids.push(arrow(x, 62, x, 84, 's-muted w2', 'f-muted', 6)); kids.push(R(x - 16, 88, 32, 32, 'f-accentsoft s-accent w1', 6)); kids.push(T(x, 104, t, 'lg b mono')); } });
    const rule = /^shift(-?\d+)$/.exec(v.rule || ''); return wrap(svg(W, v.to ? 128 : 64, kids, `${v.from} coded`), rule ? `Each letter moves ${Math.abs(+rule[1])} place${Math.abs(+rule[1]) > 1 ? 's' : ''} ${+rule[1] > 0 ? 'forward' : 'back'} (A=1 … Z=26)` : 'Letter positions: A=1 … Z=26'); }
  function codetable(v) { const tb = H('table', { cls: 'tbl' }, [H('thead', null, [H('tr', null, [H('th', { text: 'Words' }), H('th', { text: 'Codes' })])]), H('tbody', null, v.sents.map(([ws, cs]) => H('tr', null, [H('td', null, ws.map(w => H('span', { cls: 'pill' + (w === v.hl ? ' sel' : ''), text: w }))), H('td', null, cs.map(c => H('span', { cls: 'pill mono' + (c === v.hc ? ' sel' : ''), text: c })))])))]);
    return wrap(tb, v.hl ? `“${v.hl}” appears in these sentences; the common code is ${v.hc || '…'}` : 'Find a word that appears in two sentences and intersect their codes'); }
  function symtable(v) { const tb = H('table', { cls: 'tbl' }, [H('tbody', null, [H('tr', null, [H('th', { text: 'Letter' })].concat(v.L.map(l => H('td', { cls: 'b' + (v.hl && v.hl.includes(l) ? ' out' : ''), text: l })))), H('tr', null, [H('th', { text: 'Symbol' })].concat(v.S.map((s, i) => H('td', { cls: 'mono' + (v.hl && v.hl.includes(v.L[i]) ? ' out' : ''), text: s }))))])]);
    return wrap(H('div', null, [tb, H('p', { cls: 'small muted', text: 'Word: ' + v.word })])); }
  // ================= series =================
  function series(v) { const n = v.terms.length; const multi = v.terms.some(t => String(t).length > 2 && v.letters); const maxL = Math.max(...v.terms.map(t => String(t === null ? '?' : t).length)); const w = v.letters ? Math.max(52, maxL * 20 + 22) : multi ? 62 : 52, W = n * w + 20; const kids = [];
    v.terms.forEach((t, i) => { const x = 10 + i * w + w / 2; const on = v.hl === i; kids.push(R(x - w / 2 + 4, 10, w - 8, 38, on ? (v.bad ? 'f-badsoft s-bad w2' : 'f-accentsoft s-accent w2') : 'f-card s-line w1', 8)); kids.push(T(x, 29, t === null ? '?' : t, (multi ? '' : 'lg ') + 'b mono'));
      if (v.letters && /^[A-Z]+$/.test(String(t))) kids.push(T(x, 64, [...String(t)].map(A1).join('·'), 'sm mu')); });
    if (v.diffs && v.terms.every(t => typeof t === 'number')) for (let i = 1; i < n; i++) { const d = v.terms[i] - v.terms[i - 1]; kids.push(T(10 + (i - 0.5) * w + w / 2 - w / 2 + w / 2, 66, (d > 0 ? '+' : '') + d, 'sm b br')); }
    return wrap(svg(W, 76, kids, 'Series: ' + v.terms.join(', ')), v.diffs ? 'Differences between neighbours shown below' : v.letters ? 'Letter positions shown below (A=1)' : null); }
  function figure(s, x, y, size, track) { const k = []; const h = size; k.push(R(x, y, h, h, 'f-card s-ink w2', 6)); const cs = [[x, y], [x + h, y], [x + h, y + h], [x, y + h]]; const c = cs[s.c], q = h * 0.32; const dxs = [1, -1, -1, 1][s.c], dys = [1, 1, -1, -1][s.c];
    k.push(P([c, [c[0] + dxs * q, c[1]], [c[0], c[1] + dys * q]], track === 'c' ? 'f-accent s-none' : 'f-brand s-none'));
    const cx = x + h / 2, cy = y + h * 0.42, a = s.a * Math.PI / 4, r = h * 0.26; k.push(arrow(cx - Math.sin(a) * r * 0.6, cy + Math.cos(a) * r * 0.6, cx + Math.sin(a) * r, cy - Math.cos(a) * r, track === 'a' ? 's-accent w3' : 's-ink w3', track === 'a' ? 'f-accent' : 'f-ink', 8));
    const n = s.n, dr = h * 0.05; for (let i = 0; i < n; i++) { const col = i % 5, row = Math.floor(i / 5); const per = Math.min(5, n - row * 5); k.push(C(x + h / 2 + (col - (per - 1) / 2) * dr * 2.6, y + h * 0.8 + row * dr * 2.6 - (n > 5 ? dr * 1.5 : 0), dr, track === 'n' ? 'f-accent s-none' : 'f-ink s-none')); }
    return S('g', null, k); }
  function figseries(v) { const s = 70, gap = 12, n = v.items.length; const kids = v.items.map((it, i) => figure(it, 6 + i * (s + gap), 6, s, v.track)); kids.push(R(6 + n * (s + gap), 6, s, s, 'f-none s-muted w2 dash', 6)); kids.push(T(6 + n * (s + gap) + s / 2, 6 + s / 2, '?', 'xl mu'));
    return wrap(svg((n + 1) * (s + gap) + 4, s + 12, kids, 'Figure series'), v.track ? { a: 'Track the arrow', n: 'Track the dots', c: 'Track the shaded corner' }[v.track] : 'Arrow · dots · shaded corner each follow a rule'); }
  function fig(v) { return svg(76, 76, [figure(v.s, 3, 3, 70)], 'Figure option'); }
  // ================= ranking =================
  function queue(v) { const N = v.N, W = 640, step = Math.min(18, (W - 40) / N), w = N * step + 40; const kids = []; const y = 60;
    for (let i = 1; i <= N; i++) { const x = 20 + (i - 0.5) * step; const m = v.marks.find(q => q.pos === i); kids.push(C(x, y, Math.min(7, step * 0.4), m ? 'f-accent s-ink w1' : 'f-brandsoft s-brand w1')); if (m) { kids.push(L(x, y - 10, x, y - 26, 's-accent w2')); kids.push(T(x, y - 36, m.label, 'sm b')); kids.push(T(x, y + 20, i, 'sm b ac')); } }
    (v.brace || []).forEach(([a, b]) => { const x1 = 20 + (a - 1) * step, x2 = 20 + b * step; kids.push(PL([[x1, y + 32], [x1, y + 38], [x2, y + 38], [x2, y + 32]], 'f-none s-muted w2')); kids.push(T((x1 + x2) / 2, y + 52, `${b - a + 1}`, 'sm b mu')); });
    kids.push(T(20, y + 74, '← left / front', 'sm mu', { 'text-anchor': 'start' })); kids.push(T(w - 20, y + 74, 'right / back →', 'sm mu', { 'text-anchor': 'end' }));
    return wrap(svg(w, y + 86, kids, `Row of ${N}`), `${N} people in a row`); }
  function ladder(v) { const n = v.slots.length, h = 36, w = 220; const kids = [];
    v.slots.forEach((s, i) => { const y = 8 + i * h, on = v.hl === i || v.hl === s; kids.push(R(40, y, w - 50, h - 6, on ? 'f-accentsoft s-accent w2' : 'f-card s-line w1', 8)); kids.push(T(22, y + (h - 6) / 2, i + 1, 'sm b mu')); kids.push(T(40 + (w - 50) / 2, y + (h - 6) / 2, s, 'b')); });
    const box = H('div', { cls: 'grid' }, [svg(w, n * h + 12, kids, 'Ranking ladder')]);
    if (v.chain) box.appendChild(H('div', { cls: 'row' }, v.chain.map(([a, b]) => H('span', { cls: 'chip', text: `${a} > ${b}` }))));
    return wrap(box, `Top = ${v.attr}${v.count ? ` · ${v.count} order${v.count > 1 ? 's' : ''} still possible` : ''}`); }
  // ================= seating =================
  function seating(v) { const n = v.n, names = v.names, kids = []; const nm = s => v.seats[s] === null || v.seats[s] === undefined ? null : names[v.seats[s]];
    const seat = (x, y, s, dir) => { const who = nm(s); const fc = v.face && who !== null ? v.face[v.seats[s]] : null; const d = dir !== undefined ? dir : (fc === 1 ? 2 : fc === 0 ? 0 : null);
      const g2 = [C(x, y, 19, who !== null ? (v.final ? 'f-oksoft s-ok w2' : 'f-brandsoft s-brand w2') : 'f-card s-line w2'), T(x, y, who !== null ? who : '?', who !== null ? 'b' : 'mu')];
      if (d !== null && who !== null) { const ax = [0, 1, 0, -1][d], ay = [-1, 0, 1, 0][d]; g2.push(arrowHead(x + ax * 20, y + ay * 20, x + ax * 30, y + ay * 30, 8, 'f-accent s-none')); }
      return S('g', null, g2); };
    let W, Hh;
    if (v.layout === 'linear') { W = n * 56 + 40; Hh = 120; kids.push(R(14, 50, W - 28, 16, 'f-line s-none', 8)); for (let s = 0; s < n; s++) kids.push(seat(34 + s * 56, 58, s, v.face ? undefined : 0)); kids.push(T(20, 104, v.face ? 'West' : 'Left end', 'sm mu', { 'text-anchor': 'start' })); kids.push(T(W - 20, 104, v.face ? 'East' : 'Right end', 'sm mu', { 'text-anchor': 'end' })); kids.push(T(W / 2, 16, v.face ? 'North ↑' : 'All face north ↑', 'sm b mu')); }
    else if (v.layout === 'circle') { W = 280; Hh = 280; const cx = 140, cy = 140, r = 100; kids.push(C(cx, cy, 64, 'f-line s-none')); kids.push(T(cx, cy, 'table', 'sm mu'));
      for (let s = 0; s < n; s++) { const a = -Math.PI / 2 + s * 2 * Math.PI / n; const x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r; kids.push(seat(x, y, s, null)); if (nm(s) !== null) kids.push(arrowHead(x, y, x + (cx - x) * 0.3, y + (cy - y) * 0.3, 8, 'f-accent s-none')); } }
    else { const m = v.m; W = m * 64 + 60; Hh = 210; kids.push(R(20, 92, W - 40, 26, 'f-line s-none', 8)); kids.push(T(W / 2, 105, 'Row 1 faces south ↓ · Row 2 faces north ↑', 'sm mu'));
      for (let j = 0; j < m; j++) { kids.push(seat(50 + j * 64, 50, j, 2)); kids.push(seat(50 + j * 64, 160, m + j, 0)); } kids.push(T(10, 50, '1', 'sm b mu')); kids.push(T(10, 160, '2', 'sm b mu')); }
    const cap = v.count !== undefined ? `${v.count.toLocaleString('en-IN')} of ${v.total.toLocaleString('en-IN')} arrangements still possible${v.clue !== undefined && v.clue !== null ? ` after clue ${v.clue + 1}` : ''}` : null;
    const fill = v.total ? Math.max(0.02, v.count / v.total) : 0; const bar = H('div', { cls: 'bar' }, [H('i')]); bar.firstChild.style.width = (fill * 100).toFixed(1) + '%';
    const box = H('div', null, [svg(W, Hh, kids, 'Seating diagram')]); if (v.total) box.appendChild(bar);
    return wrap(box, cap); }
  // ================= puzzle grid =================
  function grid(v) { const head = [v.head || 'Slot', v.head === 'Stack' ? 'Box' : 'Person'].concat(v.attr ? [v.attr] : []); const on = r => v.hl !== undefined && v.hl !== null && (v.hl === r.slot || v.hl === r.who || v.hl === r.sIdx || v.hl === r.attr);
    const tb = H('table', { cls: 'tbl' }, [H('thead', null, [H('tr', null, head.map(h => H('th', { text: h })))]), H('tbody', null, v.rows.map(r => H('tr', { cls: on(r) ? 'out' : '' }, [H('td', { cls: 'b', text: r.slot }), H('td', { cls: r.who === '?' ? 'muted' : 'b', text: r.who })].concat(v.attr ? [H('td', { text: r.attr === null || r.attr === undefined ? '?' : r.attr })] : []))))]);
    return wrap(tb, v.count ? `${v.count} arrangement${v.count > 1 ? 's' : ''} still possible${v.clue !== undefined && v.clue !== null ? ` after clue ${v.clue + 1}` : ''}` : null); }
  // ================= DILR =================
  function rrtable(v) { const n = v.teams.length; const head = [''].concat(v.teams, ['Pts']); const cls = r => r === 'W' ? 'b okc' : r === 'L' ? 'badc' : r === 'D' ? 'muted' : '';
    const tb = H('table', { cls: 'tbl' }, [H('thead', null, [H('tr', null, head.map(h => H('th', { text: h })))]), H('tbody', null, v.teams.map((t, i) => H('tr', { cls: v.hl === i ? 'out' : '' }, [H('th', { text: t })].concat(v.teams.map((_, j) => { const td = H('td', { text: i === j ? '—' : v.res ? v.res[i][j] : '' }); if (v.res && i !== j) td.className = cls(v.res[i][j]); return td; }), [H('td', { cls: 'b', text: v.pts ? String(v.pts[i]) : '' })]))))]);
    void n; return wrap(tb, v.res ? 'Row team’s result against column team (W / L / D)' : 'Results table to fill in'); }
  function lgrid(v) { const blocks = v.attrs.map((A, a) => H('table', { cls: 'tbl' }, [H('thead', null, [H('tr', null, [H('th', { text: A.name })].concat(A.vals.map(x => H('th', { text: x }))))]), H('tbody', null, v.people.map((p, i) => H('tr', null, [H('th', { text: p })].concat(A.vals.map((_, j) => { const m = v.marks[a][i][j]; return H('td', { cls: m === 'y' ? 'b okc' : m === 'x' ? 'badc' : '', text: m === 'y' ? '✓' : m === 'x' ? '✗' : '·' }); })))))]));
    return wrap(H('div', { cls: 'grid' }, blocks), '✓ = certain · ✗ = ruled out'); }
  function bracket(v) { const R0 = v.rounds[0], kids = []; const H0 = 260, colw = 90; const ys = R0.map((_, i) => 20 + i * 30);
    v.rounds.forEach((rd, r) => { const yy = r === 0 ? ys : rd.map((_, i) => { const span = 2 ** r; let s = 0; for (let k = 0; k < span; k++) s += ys[i * span + k]; return s / span; }); rd.forEach((s, i) => { const x = 10 + r * colw; kids.push(R(x, yy[i] - 11, 60, 22, r === v.rounds.length - 1 && r > 0 ? 'f-accentsoft s-accent w2' : 'f-card s-line w1', 6)); kids.push(T(x + 30, yy[i], 'Seed ' + s, 'sm b'));
        if (r > 0) { const prev = [0, 1].map(k => { const span = 2 ** (r - 1); let t = 0; for (let q = 0; q < span; q++) t += ys[(i * 2 + k) * span + q]; return t / span; }); prev.forEach(py => kids.push(PL([[x - colw + 60, py], [x - 15, py], [x - 15, yy[i]], [x, yy[i]]], 'f-none s-muted w1')));
        } }); });
    return wrap(svg(10 + 4 * colw, H0, kids, 'Knockout bracket'), v.rounds.length === 4 ? 'Full bracket' : 'Round 1 pairings'); }

  const KIND = { cube3d, die3d, dieviews, net, nets, netfold, paperfold, paper, note, glyphs, clock, cells, segs, family, coderel, path, compass, compass8, sun, points, venn, ineq, shift, codetable, symtable, series, figseries, fig, queue, ladder, seating, grid, rrtable, lgrid, bracket };
  RL.render = function (v, opt) { opt = opt || {}; if (!v) return H('div'); const f = KIND[v.kind]; if (!f) return H('div', { cls: 'muted small', text: '[' + v.kind + ']' }); try { return f(v, opt); } catch (e) { if (g.console) console.warn('viz', v.kind, e); return H('div', { cls: 'muted small', text: 'Diagram unavailable' }); } };
  RL.KINDS = Object.keys(KIND);
})(typeof globalThis !== 'undefined' ? globalThis : this);
