/* extended visual library (graphs, number lines, 3D solids, Venn, P&C slots, trees…)
   and explainers for the CAT-syllabus topics. Patches QViz.render and QViz.EX. */
(function () {
  'use strict';
  const C = { accent: 'var(--brand)', muted: 'var(--muted)', warn: 'var(--accent)', acc2: 'var(--ok)', line: 'var(--line)', bad: 'var(--bad)', text: 'var(--ink)', sky: 'var(--reason)', bg: 'var(--card)' };
  const col = c => C[c] || c || C.accent;
  const f = x => (Math.abs(x - Math.round(x)) < 1e-9 ? String(Math.round(x)) : String(Math.round(x * 100) / 100));
  const svg = (w, h, body) => `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;
  const T = (x, y, s, cls = 's-txt', anchor = 'middle', extra = '') => `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}" ${extra}>${s}</text>`;
  const d = i => `style="animation-delay:${(i * 0.15).toFixed(2)}s"`;
  const X = {};

  /* ---------- function graph on a plane ---------- */
  X.graph = v => {
    const W = 520, H = 290, pts = v.curves.flatMap(c => c.pts).concat((v.marks || []).map(m => [m[0], m[1]]));
    let x0 = Math.min(...pts.map(p => p[0])), x1 = Math.max(...pts.map(p => p[0])), y0 = Math.min(...pts.map(p => p[1])), y1 = Math.max(...pts.map(p => p[1]));
    if (v.clipY) { y0 = Math.max(y0, v.clipY[0]); y1 = Math.min(y1, v.clipY[1]); }
    const py = (y1 - y0) * 0.12 || 1, px = (x1 - x0) * 0.04 || 1; y0 -= py; y1 += py; x0 -= px; x1 += px;
    const sx = x => 40 + (x - x0) / (x1 - x0) * 460, sy = y => 265 - (y - y0) / (y1 - y0) * 245;
    let b = '';
    if (y0 < 0 && y1 > 0) b += `<line x1="40" x2="500" y1="${sy(0)}" y2="${sy(0)}" stroke="var(--muted)" stroke-width="1.5"/>`;
    if (x0 < 0 && x1 > 0) b += `<line y1="15" y2="270" x1="${sx(0)}" x2="${sx(0)}" stroke="var(--muted)" stroke-width="1.5"/>`;
    v.curves.forEach((c, i) => { const p = c.pts.filter(q => q[1] >= y0 - 1e6 && q[1] <= y1 + 1e6).map((q, j) => (j ? 'L' : 'M') + sx(q[0]).toFixed(1) + ' ' + Math.max(-50, Math.min(340, sy(q[1]))).toFixed(1)).join('');
      b += `<path class="draw" ${d(i)} d="${p}" fill="none" stroke="${col(c.color || (i ? 'warn' : 'accent'))}" stroke-width="${c.color === 'muted' ? 1.5 : 3}" ${c.color === 'muted' ? 'stroke-dasharray="5 5"' : ''}/>`; });
    (v.marks || []).forEach((m, i) => { b += `<circle class="pop" style="animation-delay:${1 + i * .2}s" cx="${sx(m[0])}" cy="${sy(m[1])}" r="6" fill="${C.warn}"/>` + (m[2] ? T(sx(m[0]), sy(m[1]) - 12, m[2], 's-txt') : ''); });
    b += T(44, 28, `y ∈ [${f(y0 + py)}, ${f(y1 - py)}]`, 's-mute', 'start');
    return svg(W, H, b);
  };
  /* ---------- number line ---------- */
  X.numline = v => {
    const { min, max } = v, sx = x => 30 + (x - min) / (max - min) * 460; let b = `<line x1="20" x2="500" y1="130" y2="130" stroke="${C.text}" stroke-width="2"/>`;
    const step = Math.max(1, Math.ceil((max - min) / 20));
    for (let x = Math.ceil(min); x <= max; x += step) b += `<line x1="${sx(x)}" x2="${sx(x)}" y1="124" y2="136" stroke="${C.muted}"/>` + T(sx(x), 156, x, 's-mute');
    (v.intervals || []).forEach(([a, c, closed], i) => { a = Math.max(a, min); c = Math.min(c, max);
      b += `<rect class="growx" ${d(i)} x="${sx(a)}" y="118" width="${Math.max(sx(c) - sx(a), 2)}" height="24" rx="12" fill="var(--brand)" fill-opacity="0.33"/>`;
      [a, c].forEach(e => b += `<circle cx="${sx(e)}" cy="130" r="7" fill="${closed ? C.accent : C.bg}" stroke="${C.accent}" stroke-width="2.5"/>`); });
    (v.points || []).forEach((p, i) => b += `<circle class="pop" ${d(i + 2)} cx="${sx(p)}" cy="130" r="8" fill="${C.warn}"/>` + T(sx(p), 104, p, 's-txt', 'middle', `fill="${C.warn}"`));
    b += T(260, 40, '● included   ○ excluded', 's-mute');
    return svg(520, 190, b);
  };
  /* ---------- coordinate plane ---------- */
  X.coord = v => {
    const all = [].concat(v.points || [], v.polygon || [], (v.segments || []).flat(), v.dots || []).map(p => [p[0], p[1]]);
    const Rg = v.range || Math.max(4, ...all.map(p => Math.max(Math.abs(p[0]), Math.abs(p[1])))) + 1, s = 125 / Rg, cx = 260, cy = 145, sx = x => cx + x * s, sy = y => cy - y * s;
    let b = '';
    for (let i = -Rg; i <= Rg; i++) b += `<line x1="${sx(i)}" x2="${sx(i)}" y1="${sy(-Rg)}" y2="${sy(Rg)}" stroke="var(--line)"/><line y1="${sy(i)}" y2="${sy(i)}" x1="${sx(-Rg)}" x2="${sx(Rg)}" stroke="var(--line)"/>`;
    b += `<line x1="${sx(-Rg)}" x2="${sx(Rg)}" y1="${cy}" y2="${cy}" stroke="var(--muted)" stroke-width="2"/><line y1="${sy(-Rg)}" y2="${sy(Rg)}" x1="${cx}" x2="${cx}" stroke="var(--muted)" stroke-width="2"/>`;
    if (v.lattice) for (let i = -v.lattice; i <= v.lattice; i++) for (let j = -v.lattice; j <= v.lattice; j++) if (Math.abs(i) + Math.abs(j) <= v.lattice) b += `<circle class="pop" style="animation-delay:${(Math.abs(i) + Math.abs(j)) * .06}s" cx="${sx(i)}" cy="${sy(j)}" r="3" fill="${C.acc2}"/>`;
    if (v.polygon) b += `<polygon class="draw" points="${v.polygon.map(p => sx(p[0]) + ',' + sy(p[1])).join(' ')}" fill="var(--brand)" fill-opacity="0.16" stroke="${C.accent}" stroke-width="2.5"/>`;
    (v.segments || []).forEach(([p, q]) => b += `<line class="draw" x1="${sx(p[0])}" y1="${sy(p[1])}" x2="${sx(q[0])}" y2="${sy(q[1])}" stroke="${C.accent}" stroke-width="3"/>`);
    (v.lines || []).forEach(([m, c]) => { const xa = -Rg, xb = Rg; b += `<line class="draw" x1="${sx(xa)}" y1="${sy(m * xa + c)}" x2="${sx(xb)}" y2="${sy(m * xb + c)}" stroke="${C.warn}" stroke-width="2.5"/>`; });
    (v.dots || []).forEach((p, i) => b += `<circle class="pop" ${d(i)} cx="${sx(p[0])}" cy="${sy(p[1])}" r="5" fill="${C.warn}"/>`);
    (v.points || []).forEach((p, i) => b += `<circle class="pop" ${d(i)} cx="${sx(p[0])}" cy="${sy(p[1])}" r="6" fill="${C.text}"/>` + (p[2] ? T(sx(p[0]) + 12, sy(p[1]) - 10, `${p[2]}(${f(p[0])}, ${f(p[1])})`, 's-txt', 'start') : ''));
    return svg(520, 290, `<clipPath id="cp"><rect x="0" y="0" width="520" height="290"/></clipPath><g clip-path="url(#cp)">${b}</g>`);
  };
  /* ---------- isometric 3D solids ---------- */
  X.solid = v => {
    const iso = (x, y, z, k) => [260 + (x - y) * 0.866 * k, 175 + (x + y) * 0.5 * k - z * k];
    let b = '';
    if (v.shape === 'cuboid') {
      const { l, b: w, h } = v.dims, k = 150 / Math.max(l + w, h * 1.6); const P = (x, y, z) => iso(x - l / 2, y - w / 2, z - h / 2, k).join(',');
      b += `<polygon class="pop" points="${P(0, 0, h)} ${P(l, 0, h)} ${P(l, w, h)} ${P(0, w, h)}" fill="var(--ok)" fill-opacity="0.33" stroke="${C.acc2}" stroke-width="2"/>`;
      b += `<polygon class="pop" ${d(1)} points="${P(l, 0, 0)} ${P(l, w, 0)} ${P(l, w, h)} ${P(l, 0, h)}" fill="var(--brand)" fill-opacity="0.27" stroke="${C.accent}" stroke-width="2"/>`;
      b += `<polygon class="pop" ${d(2)} points="${P(0, w, 0)} ${P(l, w, 0)} ${P(l, w, h)} ${P(0, w, h)}" fill="var(--brand)" fill-opacity="0.18" stroke="${C.accent}" stroke-width="2"/>`;
      if (v.label === 'grid') { for (let i = 1; i < l; i++) b += `<line x1="${P(i, 0, h).split(',')[0]}" y1="${P(i, 0, h).split(',')[1]}" x2="${P(i, w, h).split(',')[0]}" y2="${P(i, w, h).split(',')[1]}" stroke="${C.bg}"/><line x1="${P(i, w, 0).split(',')[0]}" y1="${P(i, w, 0).split(',')[1]}" x2="${P(i, w, h).split(',')[0]}" y2="${P(i, w, h).split(',')[1]}" stroke="${C.bg}"/>`; for (let j = 1; j < h; j++) b += `<line x1="${P(0, w, j).split(',')[0]}" y1="${P(0, w, j).split(',')[1]}" x2="${P(l, w, j).split(',')[0]}" y2="${P(l, w, j).split(',')[1]}" stroke="${C.bg}"/><line x1="${P(l, 0, j).split(',')[0]}" y1="${P(l, 0, j).split(',')[1]}" x2="${P(l, w, j).split(',')[0]}" y2="${P(l, w, j).split(',')[1]}" stroke="${C.bg}"/>`; }
      if (v.label === 'diag') b += `<line class="draw" x1="${P(0, 0, 0).split(',')[0]}" y1="${P(0, 0, 0).split(',')[1]}" x2="${P(l, w, h).split(',')[0]}" y2="${P(l, w, h).split(',')[1]}" stroke="${C.warn}" stroke-width="3" stroke-dasharray="6 4"/>`;
      b += T(460, 60, `${f(l)} × ${f(w)} × ${f(h)}`, 's-txt');
    } else if (v.shape === 'cylinder' || v.shape === 'cone') {
      const { r, h } = v.dims, k = Math.min(110 / r, 190 / h), rx = r * k, ry = rx * 0.32, top = 245 - h * k;
      if (v.shape === 'cylinder') {
        b += `<path class="pop" d="M${260 - rx} ${top} L${260 - rx} 245 A${rx} ${ry} 0 0 0 ${260 + rx} 245 L${260 + rx} ${top}" fill="var(--brand)" fill-opacity="0.20" stroke="${C.accent}" stroke-width="2"/>`;
        b += `<ellipse class="pop" ${d(1)} cx="260" cy="${top}" rx="${rx}" ry="${ry}" fill="var(--ok)" fill-opacity="0.40" stroke="${C.acc2}" stroke-width="2"/>`;
        if (v.label === 'ball') b += `<rect x="${260 - rx + 2}" y="${top + h * k * 0.35}" width="${2 * rx - 4}" height="${h * k * 0.65}" fill="var(--reason)" fill-opacity="0.20"/><circle class="pop" ${d(3)} cx="260" cy="${245 - h * k * 0.25}" r="${Math.min(rx * 0.5, 40)}" fill="${C.warn}"/>`;
      } else {
        b += `<path class="pop" d="M${260 - rx} 245 L260 ${top} L${260 + rx} 245 A${rx} ${ry} 0 0 1 ${260 - rx} 245" fill="var(--brand)" fill-opacity="0.20" stroke="${C.accent}" stroke-width="2"/><ellipse cx="260" cy="245" rx="${rx}" ry="${ry}" fill="none" stroke="${C.accent}" stroke-dasharray="4 4"/>`;
      }
      b += `<line class="draw" x1="260" y1="245" x2="${260 + rx}" y2="245" stroke="${C.warn}" stroke-width="2.5"/>` + T(260 + rx / 2, 268, 'r = ' + f(r), 's-txt') + `<line x1="${260 + rx + 22}" x2="${260 + rx + 22}" y1="${top}" y2="245" stroke="${C.warn}" stroke-dasharray="4 3"/>` + T(260 + rx + 30, (top + 245) / 2, 'h = ' + f(h), 's-txt', 'start');
    } else if (v.shape === 'sphere') {
      const rr = 100; b += `<defs><radialGradient id="sg" cx="35%" cy="35%"><stop offset="0" stop-color="var(--card)"/><stop offset="1" stop-color="var(--brand)"/></radialGradient></defs><circle class="pop" cx="260" cy="145" r="${rr}" fill="url(#sg)"/><ellipse cx="260" cy="145" rx="${rr}" ry="${rr * 0.3}" fill="none" stroke="${C.text}" stroke-opacity=".5" stroke-dasharray="5 5"/><line class="draw" x1="260" y1="145" x2="${260 + rr}" y2="145" stroke="${C.warn}" stroke-width="3"/>` + T(310, 136, 'r = ' + f(v.dims.r), 's-txt');
    }
    return svg(520, 290, b);
  };
  /* ---------- work-rate bars ---------- */
  X.workbar = v => {
    const W = 520, rows = v.rows, maxR = Math.max(...rows.map(r => Math.abs(r.rate))), unitW = 260 / maxR; let b = T(20, 26, `Total work = ${f(v.W)} units`, 's-txt', 'start');
    rows.forEach((r, i) => { const y = 50 + i * 44, w = Math.abs(r.rate) * unitW, neg = r.rate < 0;
      b += T(20, y + 20, r.label, 's-txt', 'start') + `<rect class="growx" ${d(i)} x="70" y="${y}" width="${w}" height="28" rx="6" fill="${neg ? C.bad : [C.accent, C.acc2, C.warn][i % 3]}"/>` + T(80 + w, y + 19, `${neg ? '−' : '+'}${f(Math.abs(r.rate))}/unit time${r.start ? ` from t=${r.start}` : ''}${r.end ? ` until t=${r.end}` : ''}${r.alt != null ? (r.alt ? ' (even days)' : ' (odd days)') : ''}`, 's-mute', 'start'); });
    const y = 60 + rows.length * 44; b += `<rect x="20" y="${y}" width="480" height="22" rx="11" fill="var(--bg)"/><rect class="growx" ${d(rows.length + 1)} x="20" y="${y}" width="480" height="22" rx="11" fill="url(#wg)"/><defs><linearGradient id="wg"><stop offset="0" stop-color="${C.accent}"/><stop offset="1" stop-color="${C.acc2}"/></linearGradient></defs>` + T(260, y + 48, `done in ${f(v.time)} time units`, 's-big', 'middle', `fill="${C.warn}"`);
    return svg(W, y + 64, b);
  };
  /* ---------- SI vs CI growth ---------- */
  X.growth = v => {
    const n = Math.max(1, Math.min(v.n, 30)), P = v.P, r = v.r / 100, ci = k => P * (1 + r) ** k, si = k => P * (1 + r * k), max = Math.max(ci(n), si(n)) * 1.08, bw = Math.min(40, 400 / (n + 1) - 6);
    const sx = k => 60 + k * (420 / n), sy = y => 250 - y / max * 220; let b = `<line x1="50" x2="500" y1="250" y2="250" stroke="${C.line}" stroke-width="2"/>`;
    for (let k = 0; k <= n; k++) { if (v.kind !== 'si') b += `<rect class="grow" style="animation-delay:${k * .08}s" x="${sx(k) - bw / 2}" y="${sy(ci(k))}" width="${bw}" height="${250 - sy(ci(k))}" rx="4" fill="${C.accent}" opacity=".85"/>`; if (n <= 12 || k % Math.ceil(n / 12) === 0) b += T(sx(k), 268, k, 's-mute'); }
    if (v.kind !== 'ci') b += `<path class="draw" d="${Array.from({ length: n + 1 }, (_, k) => (k ? 'L' : 'M') + sx(k) + ' ' + sy(si(k))).join('')}" fill="none" stroke="${C.warn}" stroke-width="3"/>`;
    b += T(60, 24, v.kind === 'si' ? `SI: +${f(P * r)} every period` : v.kind === 'ci' ? `CI: ×${f(1 + r)} every period` : `bars = CI, line = SI`, 's-txt', 'start') + T(500, 24, `after ${n}: ${v.kind === 'si' ? f(si(n)) : f(ci(n))}`, 's-txt', 'end', `fill="${C.acc2}"`);
    return svg(520, 285, b);
  };
  /* ---------- alligation cross ---------- */
  X.alligation = v => {
    const { a, b: bb, m } = v; let b = '';
    b += `<rect class="pop" x="40" y="30" width="130" height="50" rx="10" fill="var(--bg)" stroke="${C.accent}"/>` + T(105, 61, v.la, 's-big');
    b += `<rect class="pop" ${d(1)} x="350" y="30" width="130" height="50" rx="10" fill="var(--bg)" stroke="${C.warn}"/>` + T(415, 61, v.lb, 's-big');
    b += `<circle class="pop" ${d(2)} cx="260" cy="140" r="38" fill="var(--bg)" stroke="${C.acc2}" stroke-width="2"/>` + T(260, 137, 'mean', 's-mute') + T(260, 157, f(m), 's-big');
    b += `<line class="draw" x1="140" y1="80" x2="380" y2="210" stroke="${C.accent}" stroke-width="2.5"/><line class="draw" x1="380" y1="80" x2="140" y2="210" stroke="${C.warn}" stroke-width="2.5"/>`;
    b += `<rect class="pop" ${d(4)} x="40" y="205" width="160" height="46" rx="10" fill="var(--brand)" fill-opacity="0.20"/>` + T(120, 234, `${f(bb)} − ${f(m)} = ${f(bb - m)}`, 's-txt');
    b += `<rect class="pop" ${d(5)} x="320" y="205" width="160" height="46" rx="10" fill="var(--accent)" fill-opacity="0.20"/>` + T(400, 234, `${f(m)} − ${f(a)} = ${f(m - a)}`, 's-txt');
    b += T(260, 280, `ratio  ${f(bb - m)} : ${f(m - a)}`, 's-big', 'middle', `fill="${C.acc2}"`);
    return svg(520, 295, b);
  };
  /* ---------- regular polygon / circular seating ---------- */
  X.polygon = v => {
    const n = v.n, R = 110, P = Array.from({ length: n }, (_, i) => [260 + R * Math.cos(-Math.PI / 2 + i * 2 * Math.PI / n), 145 + R * Math.sin(-Math.PI / 2 + i * 2 * Math.PI / n)]); let b = '';
    if (v.diagonals) { let k = 0; for (let i = 0; i < n; i++) for (let j = i + 2; j < n; j++) if (!(i === 0 && j === n - 1)) b += `<line class="draw" style="animation-delay:${(k++ * 0.02).toFixed(2)}s" x1="${P[i][0]}" y1="${P[i][1]}" x2="${P[j][0]}" y2="${P[j][1]}" stroke="${C.warn}" stroke-opacity=".55"/>`; }
    if (v.people) b += `<circle cx="260" cy="145" r="${R - 30}" fill="var(--bg)" stroke="${C.line}"/>` + T(260, 150, 'table', 's-mute');
    else b += `<polygon class="draw" points="${P.map(p => p.join(',')).join(' ')}" fill="var(--brand)" fill-opacity="0.13" stroke="${C.accent}" stroke-width="3"/>`;
    P.forEach((p, i) => b += `<circle class="pop" ${d(i)} cx="${p[0]}" cy="${p[1]}" r="${v.people ? 14 : 5}" fill="${v.people ? (i ? C.acc2 : C.warn) : C.text}"/>` + (v.people ? T(p[0], p[1] + 5, i ? i + 1 : '★', 's-txt', 'middle', 'fill="var(--card)"') : ''));
    b += T(450, 40, `n = ${n}`, 's-big') + (v.people ? T(450, 66, 'fix ★, arrange rest', 's-mute') : T(450, 66, `exterior ${f(360 / n)}°`, 's-mute'));
    return svg(520, 290, b);
  };
  /* ---------- circle geometry (chord, tangent, sector, two circles, square) ---------- */
  X.circlegeo = v => {
    const R = 100, k = R / v.r, cx = v.second ? 190 : 230, cy = 145; let b = `<circle class="pop" cx="${cx}" cy="${cy}" r="${R}" fill="var(--brand)" fill-opacity="0.10" stroke="${C.accent}" stroke-width="3"/><circle cx="${cx}" cy="${cy}" r="4" fill="${C.text}"/>`;
    if (v.show === 'radius') b += `<line class="draw" x1="${cx}" y1="${cy}" x2="${cx + R}" y2="${cy}" stroke="${C.warn}" stroke-width="3"/>` + T(cx + R / 2, cy - 10, 'r = ' + f(v.r), 's-txt');
    if (v.chord != null) { const dd = v.chord * k, h = Math.sqrt(R * R - dd * dd); b += `<line class="draw" x1="${cx - h}" y1="${cy + dd}" x2="${cx + h}" y2="${cy + dd}" stroke="${C.warn}" stroke-width="3"/><line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy + dd}" stroke="${C.acc2}" stroke-dasharray="5 4" stroke-width="2"/><line x1="${cx}" y1="${cy}" x2="${cx + h}" y2="${cy + dd}" stroke="${C.text}" stroke-width="1.5"/>` + T(cx + 8, cy + dd / 2, 'd = ' + f(v.chord), 's-txt', 'start') + T(cx + h / 2 + 10, cy + dd / 2 - 8, 'r', 's-mute'); }
    if (v.tangent != null) { const D = Math.min(v.tangent * k, 260), px = cx + D, t = Math.acos(R / D), tx = cx + R * Math.cos(t), ty = cy - R * Math.sin(t); b += `<line class="draw" x1="${px}" y1="${cy}" x2="${tx}" y2="${ty}" stroke="${C.warn}" stroke-width="3"/><line x1="${cx}" y1="${cy}" x2="${tx}" y2="${ty}" stroke="${C.text}"/><line x1="${cx}" y1="${cy}" x2="${px}" y2="${cy}" stroke="${C.acc2}" stroke-dasharray="5 4"/><circle cx="${px}" cy="${cy}" r="5" fill="${C.warn}"/>` + T(px, cy + 22, 'P', 's-txt'); }
    if (v.sector != null) { const a = v.sector * Math.PI / 180, ex = cx + R * Math.cos(-a), ey = cy + R * Math.sin(-a); b += `<path class="pop" d="M${cx} ${cy} L${cx + R} ${cy} A${R} ${R} 0 ${v.sector > 180 ? 1 : 0} 0 ${ex} ${ey} Z" fill="${C.warn}" opacity=".7"/>` + T(cx + 30, cy - 12, v.sector + '°', 's-txt'); }
    if (v.square) b += `<rect class="pop" x="${cx - R}" y="${cy - R}" width="${2 * R}" height="${2 * R}" fill="var(--accent)" fill-opacity="0.20" stroke="${C.warn}" stroke-width="2"/><circle cx="${cx}" cy="${cy}" r="${R}" fill="var(--card)" stroke="${C.accent}" stroke-width="3"/>`;
    if (v.second) { const D = 220, r2 = R * v.second.r / v.r; b += `<circle class="pop" ${d(1)} cx="${cx + D}" cy="${cy}" r="${r2}" fill="var(--accent)" fill-opacity="0.10" stroke="${C.warn}" stroke-width="3"/><line class="draw" x1="${cx}" y1="${cy - R}" x2="${cx + D}" y2="${cy - r2}" stroke="${C.acc2}" stroke-width="3"/><line x1="${cx}" y1="${cy}" x2="${cx + D}" y2="${cy}" stroke="${C.text}" stroke-dasharray="5 4"/>` + T(cx + D / 2, cy + 20, 'd = ' + f(v.second.d), 's-txt'); }
    if (!v.second) b += T(440, 40, 'r = ' + f(v.r), 's-big');
    return svg(520, 290, b);
  };
  /* ---------- P&C slots ---------- */
  X.slots = v => {
    const n = v.items.length, w = Math.min(64, 440 / n - 10); let b = '';
    v.items.forEach((c, i) => { const x = 260 - (n * (w + 10)) / 2 + i * (w + 10); b += `<rect class="pop" ${d(i)} x="${x}" y="90" width="${w}" height="${w}" rx="10" fill="var(--bg)" stroke="${C.accent}" stroke-width="2"/>` + T(x + w / 2, 90 + w / 2 + 6, c, 's-big') + (i < n - 1 ? T(x + w + 5, 90 + w / 2 + 6, '×', 's-mute') : ''); });
    const prod = v.items.reduce((s, x) => s * x, 1);
    b += T(260, 60, 'fill the slots left → right', 's-mute') + T(260, 210, v.note || `= ${prod.toLocaleString('en-IN')}`, 's-big', 'middle', `fill="${C.warn}"`);
    return svg(520, 250, b);
  };
  /* ---------- probability tree ---------- */
  X.tree = v => {
    let b = `<circle cx="50" cy="145" r="8" fill="${C.text}"/>`; const n = v.branches.length;
    v.branches.forEach(([l1, l2], i) => { const y = 145 + (i - (n - 1) / 2) * 120;
      b += `<line class="draw" ${d(i)} x1="58" y1="145" x2="220" y2="${y}" stroke="${C.accent}" stroke-width="2.5"/><circle class="pop" ${d(i + 1)} cx="225" cy="${y}" r="7" fill="${C.acc2}"/>` + T(140, (145 + y) / 2 - 10, l1, 's-txt');
      if (l2) b += `<line class="draw" ${d(i + 2)} x1="232" y1="${y}" x2="420" y2="${y - 25}" stroke="${C.warn}" stroke-width="2.5"/><circle class="pop" ${d(i + 3)} cx="425" cy="${y - 25}" r="7" fill="${C.warn}"/>` + T(330, y - 30, l2, 's-txt'); });
    b += T(470, 280, 'multiply along, add across', 's-mute', 'end');
    return svg(520, 290, b);
  };
  /* ---------- dice grid ---------- */
  X.dice = v => {
    let b = '', c = 0;
    for (let i = 1; i <= 6; i++) for (let j = 1; j <= 6; j++) { const hit = typeof v.hit === 'function' ? v.hit(i, j) : v.s != null ? i + j === v.s : i + j >= v.ge; if (hit) c++; b += `<rect class="pop" style="animation-delay:${((i + j) * 0.03).toFixed(2)}s" x="${100 + (j - 1) * 36}" y="${35 + (i - 1) * 36}" width="32" height="32" rx="6" fill="${hit ? C.accent : 'var(--bg)'}"/>` + T(116 + (j - 1) * 36, 56 + (i - 1) * 36, i + j, hit ? 's-txt' : 's-mute', 'middle', hit ? 'fill="var(--card)"' : ''); }
    for (let k = 1; k <= 6; k++) b += T(116 + (k - 1) * 36, 26, k, 's-mute') + T(86, 56 + (k - 1) * 36, k, 's-mute');
    b += T(420, 140, `${c}/36`, 's-big', 'middle', 'font-size="30"') + T(420, 170, 'favourable cells', 's-mute');
    return svg(520, 265, b);
  };
  X.balls = v => {
    let b = '', k = 0; v.groups.forEach(([n, c]) => { for (let i = 0; i < n; i++, k++) b += `<circle class="pop" style="animation-delay:${k * .03}s" cx="${70 + (k % 12) * 34}" cy="${60 + Math.floor(k / 12) * 34}" r="13" fill="${col(c)}"/>`; });
    b += T(260, 230, v.groups.map(g => g[0]).join(' + ') + ` = ${v.groups.reduce((s, g) => s + g[0], 0)} balls`, 's-txt');
    return svg(520, 250, b);
  };
  /* ---------- Venn diagrams ---------- */
  X.venn2 = v => {
    let b = `<rect x="20" y="20" width="480" height="250" rx="16" fill="none" stroke="${C.line}" stroke-width="2"/><circle class="pop" cx="200" cy="145" r="100" fill="var(--brand)" fill-opacity="0.20" stroke="${C.accent}" stroke-width="2"/><circle class="pop" ${d(1)} cx="320" cy="145" r="100" fill="var(--accent)" fill-opacity="0.20" stroke="${C.warn}" stroke-width="2"/>`;
    b += T(150, 150, f(v.a), 's-big') + T(260, 150, f(v.ab), 's-big') + T(370, 150, f(v.b), 's-big') + T(160, 40, v.labels[0], 's-txt') + T(360, 40, v.labels[1], 's-txt');
    if (v.out != null) b += T(470, 255, 'outside ' + f(v.out), 's-txt', 'end');
    return svg(520, 290, b);
  };
  X.venn3 = v => {
    const r = v.r, L = v.labels || ['A', 'B', 'C'];
    let b = `<circle class="pop" cx="210" cy="115" r="90" fill="var(--brand)" fill-opacity="0.16" stroke="${C.accent}" stroke-width="2"/><circle class="pop" ${d(1)} cx="310" cy="115" r="90" fill="var(--accent)" fill-opacity="0.16" stroke="${C.warn}" stroke-width="2"/><circle class="pop" ${d(2)} cx="260" cy="195" r="90" fill="var(--reason)" fill-opacity="0.16" stroke="${C.sky}" stroke-width="2"/>`;
    if (v.raw) b += T(260, 280, `|A|=${r.a} |B|=${r.b} |C|=${r.c} · pairs ${r.ab}, ${r.bc}, ${r.ca} · all ${r.abc}`, 's-mute');
    else b += T(175, 95, r.a, 's-big') + T(345, 95, r.b, 's-big') + T(260, 245, r.c, 's-big') + T(260, 88, r.ab, 's-txt') + T(310, 175, r.bc, 's-txt') + T(210, 175, r.ca, 's-txt') + T(260, 145, r.abc, 's-big', 'middle', `fill="${C.warn}"`);
    b += T(140, 30, L[0], 's-txt') + T(380, 30, L[1], 's-txt') + T(380, 270, L[2], 's-txt');
    return svg(520, 290, b);
  };
  /* ---------- sequence bars ---------- */
  X.seq = v => {
    const t = v.terms, n = t.length, mx = Math.max(...t.map(Math.abs), 1), w = Math.min(54, 440 / n - 8), base = t.some(x => x < 0) ? 150 : 240, sc = (t.some(x => x < 0) ? 100 : 200) / mx; let b = `<line x1="30" x2="500" y1="${base}" y2="${base}" stroke="${C.line}" stroke-width="2"/>`;
    t.forEach((x, i) => { const h = Math.abs(x) * sc, X0 = 40 + i * (440 / n); b += `<rect class="grow" ${d(i)} x="${X0}" y="${x >= 0 ? base - h : base}" width="${w}" height="${Math.max(h, 1)}" rx="5" fill="${i === v.hi ? C.warn : i % 2 ? C.acc2 : C.accent}"/>` + T(X0 + w / 2, x >= 0 ? base - h - 6 : base + h + 16, f(x), 's-txt'); });
    return svg(520, 270, b);
  };
  X.gridrect = v => {
    const { m, n } = v, s = Math.min(380 / m, 200 / n), ox = 260 - m * s / 2, oy = 140 - n * s / 2; let b = '';
    for (let i = 0; i <= m; i++) b += `<line x1="${ox + i * s}" x2="${ox + i * s}" y1="${oy}" y2="${oy + n * s}" stroke="${C.accent}" stroke-width="2"/>`;
    for (let j = 0; j <= n; j++) b += `<line y1="${oy + j * s}" y2="${oy + j * s}" x1="${ox}" x2="${ox + m * s}" stroke="${C.acc2}" stroke-width="2"/>`;
    b += `<rect class="pop" x="${ox + s}" y="${oy}" width="${Math.min(2, m - 1) * s}" height="${Math.min(2, n) * s}" fill="${C.warn}" opacity=".55"/>` + T(260, oy + n * s + 30, `choose 2 of ${m + 1} × 2 of ${n + 1} lines`, 's-txt');
    return svg(520, 290, b);
  };
  /* ---------- triangle (sides / angles / base-height / inner line / incircle) ---------- */
  X.triangle = v => {
    let A, B, Cp, b = '';
    if (v.angles) { const [a1, a2] = v.angles.map(x => x * Math.PI / 180), base = 300; const h = base / (1 / Math.tan(a1) + 1 / Math.tan(a2)); A = [110, 240]; B = [410, 240]; Cp = [110 + h / Math.tan(a1), 240 - h]; if (Cp[1] < 20) { const s = 220 / (240 - Cp[1]); Cp = [260 + (Cp[0] - 260) * s, 240 - (240 - Cp[1]) * s]; }
      b += T(A[0] + 34, A[1] - 8, v.angles[0] + '°', 's-txt') + T(B[0] - 34, B[1] - 8, v.angles[1] + '°', 's-txt') + T(Cp[0], Cp[1] + 30, '?', 's-big', 'middle', `fill="${C.warn}"`); }
    else if (v.base) { const s = Math.min(320 / v.base, 200 / v.height); A = [260 - v.base * s / 2, 240]; B = [260 + v.base * s / 2, 240]; Cp = [A[0] + v.base * s * 0.3, 240 - v.height * s]; b += `<line class="draw" x1="${Cp[0]}" y1="${Cp[1]}" x2="${Cp[0]}" y2="240" stroke="${C.warn}" stroke-dasharray="5 4" stroke-width="2"/>` + T(Cp[0] + 8, (Cp[1] + 240) / 2, 'h = ' + v.height, 's-txt', 'start') + T(260, 265, 'b = ' + v.base, 's-txt'); }
    else { const [a, bb, c] = v.sides; const x = (a * a + c * c - bb * bb) / (2 * c), y = Math.sqrt(Math.max(a * a - x * x, 0)), s = Math.min(380 / Math.max(c, Math.abs(x), 1), 200 / Math.max(y, 1)); const ox = 260 - c * s / 2;
      A = [ox, 240]; B = [ox + c * s, 240]; Cp = [ox + x * s, 240 - y * s];
      b += T((A[0] + B[0]) / 2, 262, f(c), 's-txt') + T((A[0] + Cp[0]) / 2 - 16, (A[1] + Cp[1]) / 2, f(a), 's-txt') + T((B[0] + Cp[0]) / 2 + 16, (B[1] + Cp[1]) / 2, f(bb), 's-txt');
      if (v.inner) { const t = v.inner, D = [Cp[0] + (A[0] - Cp[0]) * t, Cp[1] + (A[1] - Cp[1]) * t], E = [Cp[0] + (B[0] - Cp[0]) * t, Cp[1] + (B[1] - Cp[1]) * t]; b += `<line class="draw" x1="${D[0]}" y1="${D[1]}" x2="${E[0]}" y2="${E[1]}" stroke="${C.warn}" stroke-width="3"/>` + T(D[0] - 12, D[1], 'D', 's-txt') + T(E[0] + 12, E[1], 'E', 's-txt'); }
      if (v.incircle) { const la = Math.hypot(B[0] - Cp[0], B[1] - Cp[1]), lb = Math.hypot(A[0] - Cp[0], A[1] - Cp[1]), lc = c * s, p = la + lb + lc, I = [(la * A[0] + lb * B[0] + lc * Cp[0]) / p, (la * A[1] + lb * B[1] + lc * Cp[1]) / p], ar = Math.abs((B[0] - A[0]) * (Cp[1] - A[1]) - (Cp[0] - A[0]) * (B[1] - A[1])) / 2; b += `<circle class="pop" cx="${I[0]}" cy="${I[1]}" r="${2 * ar / p}" fill="none" stroke="${C.warn}" stroke-width="2.5"/>`; }
      if (v.right) b += T(260, 26, 'a² + b² = c²', 's-txt', 'middle', `fill="${C.warn}"`); }
    return svg(520, 280, `<polygon class="draw" points="${[A, B, Cp].map(p => p.join(',')).join(' ')}" fill="var(--brand)" fill-opacity="0.13" stroke="${C.accent}" stroke-width="3"/>` + b);
  };
  X.mixture = v => {
    const tot = v.M + v.W + v.add || 1, h = 200 / tot, x = 190, w = 140, L = v.labels || ['Milk', 'Water']; let y = 240, b = `<rect x="${x - 4}" y="30" width="${w + 8}" height="214" rx="10" fill="none" stroke="var(--muted)" stroke-width="3"/>`;
    const layer = (q, c, lab, i) => { if (q <= 0) return ''; const hh = q * h; y -= hh; return `<rect class="grow" ${d(i)} x="${x}" y="${y}" width="${w}" height="${hh}" fill="${c}"/>` + T(x + w + 18, y + hh / 2 + 5, `${lab} ${f(q)}`, 's-txt', 'start'); };
    b += layer(v.M, 'var(--ink)', L[0], 0) + layer(v.W, 'var(--reason)', L[1], 1) + layer(v.add, C.warn, '+ added', 3) + T(100, 140, L[0] + ' is', 's-mute') + T(100, 158, 'the invariant', 's-mute');
    return svg(520, 260, b);
  };
  const tr0 = QViz.render;
  X.track = v => (v.one ? svg(520, 160, `<line x1="60" y1="90" x2="460" y2="90" stroke="${C.line}" stroke-width="6" stroke-linecap="round"/><circle r="10" cy="90" fill="${C.accent}"><animate attributeName="cx" from="60" to="460" dur="2.5s" repeatCount="indefinite"/></circle>` + T(260, 60, `${v.D} km`, 's-big') + T(260, 130, v.trains[0].label, 's-txt')) : tr0(v));
  QViz.render = v => { try { return X[v.type] ? X[v.type](v) : tr0(v); } catch (e) { console.error(e); return svg(520, 80, T(260, 45, 'visual unavailable', 's-mute')); } };
  QViz.X = X;

  /* ---------- explainers for new topics ---------- */
  const g = (fn, a, b, n = 80) => { const p = []; for (let i = 0; i <= n; i++) { const x = a + (b - a) * i / n, y = fn(x); if (isFinite(y)) p.push([x, y]); } return p; };
  Object.assign(QViz.EX, {
    work: { icon: '⚙', title: 'Work = rate × time', blurb: 'Give the whole job LCM units; each worker contributes units per day. A leak is just a negative rate.', formula: 'T = W / (r₁ + r₂ − r_leak)',
      controls: [{ id: 'a', label: 'A alone (days)', min: 2, max: 30, step: 1, value: 12 }, { id: 'b', label: 'B alone (days)', min: 2, max: 30, step: 1, value: 15 }, { id: 'c', label: 'Leak empties in (0 = none)', min: 0, max: 60, step: 5, value: 0 }],
      draw: ({ a, b, c }) => { const W = 60; const rows = [{ label: 'A', rate: W / a }, { label: 'B', rate: W / b }]; if (c) rows.push({ label: 'Leak', rate: -W / c }); const net = rows.reduce((s, r) => s + r.rate, 0); return X.workbar({ rows: rows.map(r => ({ ...r, rate: Math.round(r.rate * 100) / 100 })), W, time: net > 0 ? Math.round(W / net * 100) / 100 : '∞ (never)' }); } },
    interest: { icon: '📈', title: 'Simple adds, compound multiplies', blurb: 'SI adds the same interest every year (a line). CI earns interest on interest (a curve that pulls away).', formula: 'SI: P(1 + rt) · CI: P(1 + r)ᵗ',
      controls: [{ id: 'r', label: 'Rate % p.a.', min: 1, max: 30, step: 1, value: 10 }, { id: 'n', label: 'Years', min: 1, max: 20, step: 1, value: 8 }],
      draw: ({ r, n }) => X.growth({ P: 1000, r, n, kind: 'both' }) },
    mixtures: { icon: '⚗', title: 'The alligation cross', blurb: 'Write the two ingredients and the target mean; subtract diagonally; the differences give the mixing ratio.', formula: 'cheap : dear = (d − m) : (m − c)',
      controls: [{ id: 'a', label: 'Cheaper (₹)', min: 10, max: 60, step: 1, value: 30 }, { id: 'b', label: 'Dearer (₹)', min: 61, max: 120, step: 1, value: 80 }, { id: 'm', label: 'Target mean', min: 11, max: 119, step: 1, value: 50 }],
      draw: ({ a, b, m }) => X.alligation({ a, b, m: Math.min(Math.max(m, a + 1), b - 1), la: '₹' + a, lb: '₹' + b }) },
    partnership: { icon: '🤝', title: 'Capital × months', blurb: 'Profit is split in the ratio of capital multiplied by the time it stayed invested.', formula: 'share ∝ Cᵢ × tᵢ',
      controls: [{ id: 'a', label: "A's capital (k)", min: 1, max: 10, step: 1, value: 5 }, { id: 'b', label: "B's capital (k)", min: 1, max: 10, step: 1, value: 6 }, { id: 't', label: 'B joins after (months)', min: 0, max: 11, step: 1, value: 4 }],
      draw: ({ a, b, t }) => QViz.render({ type: 'ratio', parts: [a * 12, b * (12 - t)].map(x => Math.max(1, Math.round(x / Math.max(1, gcdv(a * 12, b * (12 - t)))))), unitVal: 1, labels: ['A', 'B'] }) },
    inequalities: { icon: '|x|', title: '|x − a| is distance from a', blurb: '|x − a| ≤ b is everything within b of a — an interval centred at a on the number line.', formula: '|x − a| ≤ b ⇔ a − b ≤ x ≤ a + b',
      controls: [{ id: 'a', label: 'Centre a', min: -8, max: 8, step: 1, value: 2 }, { id: 'b', label: 'Radius b', min: 0, max: 8, step: 1, value: 3 }],
      draw: ({ a, b }) => X.numline({ min: -12, max: 12, intervals: [[a - b, a + b, true]], points: [a] }).replace('</svg>', T(260, 75, `${2 * b + 1} integers`, 's-big', 'middle', `fill="${C.acc2}"`) + '</svg>') },
    functions: { icon: 'ƒ', title: 'Graph transformations', blurb: 'f(x − h) + k shifts right by h and up by k; a·f(x) stretches; |f(x)| reflects the negative part upward.', formula: 'y = a·f(x − h) + k',
      controls: [{ id: 'h', label: 'Shift h', min: -5, max: 5, step: 0.5, value: 1 }, { id: 'k', label: 'Shift k', min: -5, max: 5, step: 0.5, value: -2 }, { id: 'a', label: 'Stretch a', min: -2, max: 2, step: 0.5, value: 1 }],
      draw: ({ h, k, a }) => X.graph({ curves: [{ pts: g(x => x * x - 4, -6, 6), color: 'muted' }, { pts: g(x => a * ((x - h) ** 2 - 4) + k, -6, 6) }], marks: [[h, a * -4 + k, 'vertex']], clipY: [-14, 20] }) },
    logs: { icon: 'log', title: 'Logs undo powers', blurb: 'log_b x asks “b to what power gives x?”. The curve grows ever more slowly and exists only for x > 0.', formula: 'log_b x = y ⇔ bʸ = x',
      controls: [{ id: 'b', label: 'Base b', min: 1.5, max: 10, step: 0.5, value: 2 }, { id: 'x', label: 'x', min: 1, max: 64, step: 1, value: 32 }],
      draw: ({ b, x }) => X.graph({ curves: [{ pts: g(t => Math.log(t) / Math.log(b), 0.2, 64) }], marks: [[x, Math.log(x) / Math.log(b), `log = ${f(Math.log(x) / Math.log(b))}`]] }) },
    progressions: { icon: 'Σ', title: 'AP adds, GP multiplies', blurb: 'An AP climbs in equal steps; a GP grows (or shrinks) by a constant factor. Compare their growth.', formula: 'AP: a + (n−1)d · GP: a·rⁿ⁻¹',
      controls: [{ id: 'd', label: 'AP difference d', min: -5, max: 10, step: 1, value: 3 }, { id: 'r', label: 'GP ratio r', min: 0.5, max: 2.5, step: 0.1, value: 1.5 }],
      draw: ({ d: dd, r }) => X.graph({ curves: [{ pts: Array.from({ length: 10 }, (_, i) => [i + 1, 2 + i * dd]) }, { pts: Array.from({ length: 10 }, (_, i) => [i + 1, 2 * r ** i]), color: 'warn' }], marks: [[10, 2 + 9 * dd, 'AP'], [10, 2 * r ** 9, 'GP']] }) },
    maxmin: { icon: '⛰', title: 'Equal parts maximise products', blurb: 'For a fixed sum, a product is largest when the parts are equal (AM ≥ GM). Slide the split and watch the product.', formula: 'x + y = S ⇒ xy ≤ (S/2)²',
      controls: [{ id: 'S', label: 'Sum S', min: 4, max: 40, step: 2, value: 20 }, { id: 'x', label: 'x', min: 0, max: 40, step: 1, value: 6 }],
      draw: ({ S, x }) => { x = Math.min(x, S); return X.graph({ curves: [{ pts: g(t => t * (S - t), 0, S) }], marks: [[x, x * (S - x), `${x}×${S - x} = ${x * (S - x)}`], [S / 2, S * S / 4, 'max']] }); } },
    mensuration: { icon: '⬛', title: 'Scaling solids', blurb: 'Double every length of a solid and its surface area ×4 but its volume ×8. Change the dimensions and watch.', formula: 'V = lbh · TSA = 2(lb + bh + hl)',
      controls: [{ id: 'l', label: 'Length', min: 1, max: 10, step: 1, value: 6 }, { id: 'b', label: 'Breadth', min: 1, max: 10, step: 1, value: 4 }, { id: 'h', label: 'Height', min: 1, max: 10, step: 1, value: 3 }],
      draw: ({ l, b, h }) => X.solid({ shape: 'cuboid', dims: { l, b, h }, label: 'diag' }).replace('</svg>', T(80, 40, `V = ${l * b * h}`, 's-big', 'start') + T(80, 66, `TSA = ${2 * (l * b + b * h + h * l)}`, 's-txt', 'start') + T(80, 90, `diag = ${f(Math.hypot(l, b, h))}`, 's-txt', 'start') + '</svg>') },
    coordinate: { icon: '⌗', title: 'Lines on the plane', blurb: 'y = mx + c: m sets the tilt, c the y-intercept. Drag both and track where the line meets the axes.', formula: 'y = mx + c',
      controls: [{ id: 'm', label: 'Slope m', min: -3, max: 3, step: 0.5, value: 1 }, { id: 'c', label: 'Intercept c', min: -5, max: 5, step: 1, value: 2 }],
      draw: ({ m, c }) => X.coord({ range: 7, lines: [[m, c]], points: [[0, c, 'y-int']].concat(m ? [[-c / m, 0, 'x-int']] : []) }) },
    circles: { icon: '◯', title: 'Chord & perpendicular', blurb: 'The perpendicular from the centre bisects any chord, giving a right triangle: (half-chord)² + d² = r².', formula: 'chord = 2√(r² − d²)',
      controls: [{ id: 'r', label: 'Radius r', min: 3, max: 15, step: 1, value: 10 }, { id: 'd', label: 'Distance d', min: 0, max: 14, step: 1, value: 6 }],
      draw: ({ r, d: dd }) => { dd = Math.min(dd, r - 1); return X.circlegeo({ r, chord: dd }).replace('</svg>', T(440, 70, `chord = ${f(2 * Math.sqrt(r * r - dd * dd))}`, 's-txt') + '</svg>'); } },
    pnc: { icon: '⁂', title: 'Slots: multiply the choices', blurb: 'Fill positions one by one; each slot has one fewer option. Divide by r! when order does not matter.', formula: 'ⁿPᵣ = n!/(n−r)! · ⁿCᵣ = ⁿPᵣ / r!',
      controls: [{ id: 'n', label: 'Items n', min: 2, max: 10, step: 1, value: 6 }, { id: 'r', label: 'Slots r', min: 1, max: 6, step: 1, value: 3 }],
      draw: ({ n, r }) => { r = Math.min(r, n); const items = Array.from({ length: r }, (_, i) => n - i), P = items.reduce((s, x) => s * x, 1); let fr = 1; for (let i = 2; i <= r; i++) fr *= i; return X.slots({ items, note: `P = ${P} · C = ${P / fr}` }); } },
    probability: { icon: '🎲', title: 'Count the favourable cells', blurb: 'With two dice there are 36 equally likely cells. Highlight the event and count.', formula: 'P(E) = favourable / total',
      controls: [{ id: 's', label: 'Sum ≥', min: 2, max: 12, step: 1, value: 9 }],
      draw: ({ s }) => X.dice({ ge: s }) },
    sets: { icon: '◎', title: 'Inclusion–exclusion', blurb: 'Add the sets, subtract what you double-counted, add back what you removed too often.', formula: '|A∪B| = |A| + |B| − |A∩B|',
      controls: [{ id: 'a', label: '|A|', min: 5, max: 60, step: 1, value: 40 }, { id: 'b', label: '|B|', min: 5, max: 60, step: 1, value: 30 }, { id: 'ab', label: '|A∩B|', min: 0, max: 30, step: 1, value: 12 }],
      draw: ({ a, b, ab }) => { ab = Math.min(ab, a, b); return X.venn2({ a: a - ab, ab, b: b - ab, labels: [`A (${a})`, `B (${b})`] }).replace('</svg>', T(260, 282, `|A∪B| = ${a} + ${b} − ${ab} = ${a + b - ab}`, 's-txt', 'middle', `fill="${C.acc2}"`) + '</svg>'); } }
  });
  QViz.EX.geometry.title = 'Pythagoras as areas'; QViz.EX.algebra.icon = 'x'; QViz.EX.numbers.blurb = 'Powers repeat their remainders in a cycle — so huge exponents reduce to small ones. The same idea gives unit digits.';
  function gcdv(a, b) { while (b) [a, b] = [b, a % b]; return a || 1; }
})();
