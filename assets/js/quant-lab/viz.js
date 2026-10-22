/* Quant Lab: solution visuals and topic explainers (SVG). Colours are site CSS tokens via var(). */
(function () {
  'use strict';
  const C = { accent: 'var(--brand)', muted: 'var(--muted)', warn: 'var(--accent)', acc2: 'var(--ok)', line: 'var(--line)', bad: 'var(--bad)', text: 'var(--ink)' };
  const f = x => QGen.fmt(x);
  const svg = (w, h, body) => `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;
  const T = (x, y, s, cls = 's-txt', anchor = 'middle', extra = '') => `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}" ${extra}>${s}</text>`;
  const d = i => `style="animation-delay:${(i * 0.18).toFixed(2)}s"`;

  function bars(items, unit, opts = {}) {
    const W = 520, H = 280, max = Math.max(...items.map(i => i.value)) * 1.15, bw = Math.min(110, 360 / items.length);
    const gap = (W - 60 - bw * items.length) / (items.length + 1);
    let b = `<line x1="40" y1="240" x2="${W - 20}" y2="240" stroke="${C.line}" stroke-width="2"/>`;
    items.forEach((it, i) => {
      const h = (it.value / max) * 200, x = 40 + gap * (i + 1) + bw * i;
      b += `<rect class="grow" ${d(i)} x="${x}" y="${240 - h}" width="${bw}" height="${h}" rx="8" fill="${C[it.color] || it.color}"/>`;
      b += T(x + bw / 2, 232 - h, (unit === '₹' ? '₹' : '') + f(it.value) + (unit && unit !== '₹' ? ' ' + unit : ''), 's-txt', 'middle', `class="pop" ${d(i + 2)}`);
      b += T(x + bw / 2, 262, it.label, 's-mute');
    });
    if (opts.avg != null) { const y = 240 - (opts.avg / max) * 200; b += `<line class="draw" x1="40" x2="${W - 20}" y1="${y}" y2="${y}" stroke="${C.warn}" stroke-width="2" stroke-dasharray="6 4"/>` + T(W - 24, y - 6, 'avg ' + f(opts.avg), 's-txt', 'end', `fill="${C.warn}"`); }
    return svg(W, H, b);
  }

  function track(v) {
    const W = 520, H = 220; let b = '';
    if (v.mode === 'roundtrip') {
      b += `<line x1="70" y1="110" x2="450" y2="110" stroke="${C.line}" stroke-width="6" stroke-linecap="round"/>` + T(70, 140, 'P', 's-big') + T(450, 140, 'Q', 's-big') + T(260, 140, v.D + ' km', 's-mute');
      b += `<path class="draw" d="M70 95 Q260 30 450 95" fill="none" stroke="${C.accent}" stroke-width="3" marker-end="url(#ar)"/>` + T(260, 50, '→ ' + v.trains[0].label, 's-txt');
      b += `<path class="draw" style="animation-delay:.6s" d="M450 125 Q260 200 70 125" fill="none" stroke="${C.warn}" stroke-width="3"/>` + T(260, 192, '← ' + v.trains[1].label, 's-txt');
      b += `<circle r="9" fill="${C.acc2}"><animateMotion dur="4s" repeatCount="indefinite" path="M70 95 Q260 30 450 95 L450 125 Q260 200 70 125 Z"/></circle>`;
      return svg(W, H, b);
    }
    const tr = v.trains, total = tr.reduce((s, t) => s + t.len, 0), sc = 300 / Math.max(total, 1);
    const car = (x, y, len, col, lab) => `<g><rect x="${x}" y="${y}" width="${len}" height="26" rx="7" fill="${col}"/><rect x="${x + 6}" y="${y + 6}" width="${Math.max(len - 12, 4)}" height="7" rx="2" fill="var(--card)" fill-opacity="0.5"/>${T(x + len / 2, y - 8, lab, 's-mute')}</g>`;
    b += `<line x1="10" y1="96" x2="510" y2="96" stroke="${C.line}" stroke-width="3"/><line x1="10" y1="166" x2="510" y2="166" stroke="${C.line}" stroke-width="3"/>`;
    if (v.mode === 'pole') {
      const L = tr[0].len * sc;
      b += `<rect x="300" y="30" width="6" height="66" fill="${C.warn}"/>${T(303, 22, 'pole', 's-mute')}`;
      b += `<g>${car(0, 70, L, C.accent, tr[0].len + ' m · ' + tr[0].label)}<animateTransform attributeName="transform" type="translate" from="${300 - L - 20} 0" to="${320} 0" dur="3s" repeatCount="indefinite"/></g>`;
      b += T(260, 205, 'distance covered = train length', 's-txt');
    } else {
      const L1 = tr[0].len * sc, L2 = tr[1].len * sc;
      b += `<g>${car(0, 70, L1, C.accent, tr[0].len + ' m · ' + tr[0].label + ' →')}<animateTransform attributeName="transform" type="translate" values="${260 - L1 - L2 - 20} 0;${260 + 20} 0" dur="3.2s" repeatCount="indefinite"/></g>`;
      b += `<g>${car(0, 140, L2, C.warn, '← ' + tr[1].label + ' · ' + tr[1].len + ' m')}<animateTransform attributeName="transform" type="translate" values="${260 + 20} 0;${260 - L1 - L2 - 20} 0" dur="3.2s" repeatCount="indefinite"/></g>`;
      b += T(260, 205, 'relative speed = sum · distance = L₁ + L₂', 's-txt');
    }
    return svg(W, H, b);
  }

  function parabola(v) {
    const W = 520, H = 280, [r1, r2] = v.roots, lo = Math.min(r1, r2) - 3, hi = Math.max(r1, r2) + 3;
    const fx = x => x * x - v.s * x + v.p, ys = []; for (let x = lo; x <= hi; x += 0.1) ys.push(fx(x));
    const ymin = Math.min(...ys), ymax = Math.max(...ys);
    const X = x => 30 + (x - lo) / (hi - lo) * 460, Y = y => 250 - (y - ymin) / (ymax - ymin || 1) * 220;
    let p = ''; for (let x = lo; x <= hi + 1e-9; x += 0.1) p += (p ? 'L' : 'M') + X(x).toFixed(1) + ' ' + Y(fx(x)).toFixed(1);
    let b = `<line x1="30" x2="490" y1="${Y(0)}" y2="${Y(0)}" stroke="${C.line}" stroke-width="2"/><path class="draw" d="${p}" fill="none" stroke="${C.accent}" stroke-width="3"/>`;
    [r1, r2].forEach((r, i) => { b += `<circle class="pop" style="animation-delay:${1 + i * .3}s" cx="${X(r)}" cy="${Y(0)}" r="7" fill="${r === Math.max(r1, r2) ? C.warn : C.acc2}"/>` + T(X(r), Y(0) + 24, 'x = ' + r, 's-txt'); });
    return svg(W, H, b);
  }

  function triangle(v) {
    const [a, b0, c] = v.sides, W = 520, H = 280;
    // place side c on base; compute apex
    const x = (a * a + c * c - b0 * b0) / (2 * c), y = Math.sqrt(Math.max(a * a - x * x, 0));
    const s = Math.min(400 / Math.max(c, 1), 200 / Math.max(y, 1)); const ox = (W - c * s) / 2, oy = 240;
    const P = [[ox, oy], [ox + c * s, oy], [ox + x * s, oy - y * s]];
    let b = `<polygon class="draw" points="${P.map(p => p.join(',')).join(' ')}" fill="var(--brand)" fill-opacity="0.13" stroke="${C.accent}" stroke-width="3"/>`;
    b += T((P[0][0] + P[1][0]) / 2, oy + 24, c + ' cm', 's-txt') + T((P[0][0] + P[2][0]) / 2 - 18, (P[0][1] + P[2][1]) / 2, a + '', 's-txt') + T((P[1][0] + P[2][0]) / 2 + 18, (P[1][1] + P[2][1]) / 2, b0 + '', 's-txt');
    if (v.right) b += T(W / 2, 30, 'a² + b² = c²', 's-txt', 'middle', `fill="${C.warn}"`); else b += T(W / 2, 22, 's = (a+b+c)/2', 's-txt', 'middle', `fill="${C.warn}"`);
    return svg(W, H, b);
  }

  function circle(v) {
    const b = `<circle class="pop" cx="200" cy="140" r="110" fill="var(--brand)" fill-opacity="0.13" stroke="${C.accent}" stroke-width="3"/><line class="draw" x1="200" y1="140" x2="310" y2="140" stroke="${C.warn}" stroke-width="3"/>${T(255, 130, 'r = ' + v.r, 's-txt')}<circle cx="200" cy="140" r="4" fill="${C.text}"/>${T(430, 120, 'A = πr²', 's-big')}${T(430, 150, '22/7 × ' + v.r + '²', 's-mute')}`;
    return svg(520, 280, b);
  }

  function ratio(v) {
    const tot = v.parts.reduce((s, x) => s + x, 0), uw = 460 / tot, cols = [C.accent, C.warn, C.acc2]; let x = 30, b = '', k = 0;
    v.parts.forEach((p, i) => {
      if (tot > 40) b += `<rect class="pop" style="animation-delay:${i * 0.1}s" x="${x + 2}" y="90" width="${Math.max(1, p * uw - 4)}" height="60" rx="6" fill="${cols[i]}"/>`; // too many parts to draw one block each
      else for (let j = 0; j < p; j++, k++) b += `<rect class="pop" style="animation-delay:${k * 0.05}s" x="${x + j * uw + 2}" y="90" width="${uw - 4}" height="60" rx="6" fill="${cols[i]}"/>`;
      b += T(x + p * uw / 2, 80, `${v.labels[i]} · ${p} part${p > 1 ? 's' : ''}`, 's-txt') + T(x + p * uw / 2, 178, '= ' + f(p * v.unitVal), 's-mute');
      x += p * uw;
    });
    b += T(260, 230, `1 part = ${f(v.unitVal)}  ·  total ${tot} parts`, 's-txt', 'middle', `fill="${C.warn}"`);
    return svg(520, 260, b);
  }

  function mixture(v) {
    const tot = v.M + v.W + v.add, h = 200 / tot, x = 190, w = 140; let y = 240, b = `<rect x="${x - 4}" y="30" width="${w + 8}" height="214" rx="10" fill="none" stroke="${C.mute || 'var(--muted)'}" stroke-width="3"/>`;
    const layer = (q, col, lab, i) => { const hh = q * h; y -= hh; return `<rect class="grow" ${d(i)} x="${x}" y="${y}" width="${w}" height="${hh}" fill="${col}"/>` + T(x + w + 20, y + hh / 2 + 4, lab + ' ' + f(q) + ' L', 's-txt', 'start'); };
    b += layer(v.M, 'var(--ink)', 'Milk', 0) + layer(v.W, 'var(--reason)', 'Water', 1) + layer(v.add, C.warn, '+ Added', 3);
    b += T(100, 140, 'Milk stays', 's-mute') + T(100, 158, 'constant', 's-mute');
    return svg(520, 260, b);
  }

  function cycle(v) {
    const n = v.items.length, R = 90, cx = 200, cy = 135; let b = '';
    v.items.forEach((r, i) => { const a = -Math.PI / 2 + i * 2 * Math.PI / n, x = cx + R * Math.cos(a), y = cy + R * Math.sin(a); const hit = r === v.ans;
      b += `<circle class="pop" ${d(i)} cx="${x}" cy="${y}" r="20" fill="${hit ? C.warn : 'var(--bg)'}" stroke="${C.accent}"/>` + T(x, y + 5, r, 's-txt'); });
    b += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${C.line}" stroke-dasharray="4 6"/>` + T(cx, cy + 5, 'cycle ' + n, 's-mute') + T(400, 120, `n = ${v.n}`, 's-big') + T(400, 150, `${v.n} mod ${n} = ${v.n % n || n}`, 's-txt');
    return svg(520, 270, b);
  }

  function balance(v) {
    const b = `<polygon points="250,230 270,190 290,230" fill="${C.muted}"/><rect class="pop" x="80" y="176" width="380" height="10" rx="5" fill="${C.accent}"/>` +
      `<rect class="pop" ${d(1)} x="100" y="120" width="140" height="52" rx="10" fill="var(--bg)" stroke="${C.accent}"/>${T(170, 152, `${v.a}x ${v.b >= 0 ? '+' : '−'} ${Math.abs(v.b)}`, 's-big')}` +
      `<rect class="pop" ${d(2)} x="300" y="120" width="140" height="52" rx="10" fill="var(--bg)" stroke="${C.warn}"/>${T(370, 152, v.c, 's-big')}` +
      T(270, 60, 'Do the same to both sides', 's-txt') + T(270, 90, `x = (${v.c} ${v.b >= 0 ? '−' : '+'} ${Math.abs(v.b)}) ÷ ${v.a} = ${v.x}`, 's-txt', 'middle', `fill="${C.warn}"`);
    return svg(540, 250, b);
  }

  function cube(v) {
    // Identity bar: the known power (top) splits into the asked expression plus the cross term (bottom).
    const k = v.k, m = v.mode || 1, sq = m === 0 || m === 2 || m === 3, plus = m < 3;
    const total = sq ? (plus ? k * k : k * k + 2) : (plus ? k ** 3 : k ** 3 + 3 * k), cross = sq ? 2 : 3 * k, ans = plus ? total - cross : total;
    const topLab = plus ? `(x + 1/x)${sq ? '²' : '³'} = ${k}${sq ? '²' : '³'} = ${total}` : `x${sq ? '²' : '³'} ${sq ? '+' : '−'} 1/x${sq ? '²' : '³'} = ${total}`;
    const ansLab = (sq ? 'x² + 1/x²' : 'x³ ' + (plus ? '+' : '−') + ' 1/x³') + ' = ' + ans, crossLab = plus ? (sq ? 'cross term 2' : '3(x + 1/x) = ' + cross) : (sq ? '(x − 1/x)² + 2' : '(x − 1/x)³ + 3(x − 1/x)');
    const W = 460, wa = plus ? W * ans / total : W * (total - cross) / total, wc = W - wa; let b = '';
    b += `<rect class="growx" x="30" y="60" width="${W}" height="50" rx="10" fill="${C.accent}"/>` + T(260, 92, topLab, 's-big', 'middle', 'fill="var(--card)"');
    b += `<rect class="growx" ${d(2)} x="30" y="140" width="${Math.max(2, wa)}" height="50" rx="10" fill="${C.warn}"/>` + T(30 + wa / 2, 172, plus ? ansLab : (sq ? '(x − 1/x)² = ' : '(x − 1/x)³ = ') + (plus ? '' : sq ? k * k : k ** 3), 's-txt', 'middle', 'fill="var(--card)"');
    b += `<rect class="growx" ${d(3)} x="${30 + wa}" y="140" width="${Math.max(2, wc)}" height="50" rx="10" fill="${C.acc2}"/>` + T(Math.min(440, 30 + wa + wc / 2), 214, plus ? crossLab : (sq ? '+ 2' : '+ 3k = ' + cross), 's-mute');
    if (!plus) b += T(260, 234, ansLab, 's-txt', 'middle');
    return svg(520, 250, b);
  }

  function venn(v) {
    const b = `<circle class="pop" cx="200" cy="130" r="95" fill="var(--brand)" fill-opacity="0.20" stroke="${C.accent}" stroke-width="2"/><circle class="pop" ${d(1)} cx="320" cy="130" r="95" fill="var(--accent)" fill-opacity="0.20" stroke="${C.warn}" stroke-width="2"/>` +
      T(150, 135, '×' + v.x, 's-big') + T(370, 135, '×' + v.y, 's-big') + T(260, 128, 'HCF', 's-mute') + T(260, 150, v.h, 's-big') + T(200, 22, v.a, 's-txt') + T(320, 22, v.b, 's-txt') +
      T(260, 252, `LCM = ${v.h} × ${v.x} × ${v.y} = ${v.h * v.x * v.y}`, 's-txt', 'middle', `fill="${C.acc2}"`);
    return svg(520, 265, b);
  }

  function grid(v) {
    const [p, q, r] = v.dims; let b = '', k = 0; const s = Math.min(26, 200 / Math.max(p, q * r));
    for (let k3 = 0; k3 < r; k3++) for (let i = 0; i < p; i++) for (let j = 0; j < q; j++, k++)
      b += `<rect class="pop" style="animation-delay:${k * 0.02}s" x="${30 + k3 * (q * s + 18) + j * s}" y="${40 + i * s}" width="${s - 3}" height="${s - 3}" rx="3" fill="${[C.accent, C.warn, C.acc2][k3 % 3]}"/>`;
    b += T(260, 250, `${p} × ${q} × ${r} = ${p * q * r} divisors`, 's-big');
    return svg(520, 270, b);
  }

  function seesaw(v) {
    const lo = Math.min(v.a1, v.a2) - 5, hi = Math.max(v.a1, v.a2) + 5, X = x => 40 + (x - lo) / (hi - lo) * 440;
    let b = `<line x1="40" x2="480" y1="150" y2="150" stroke="${C.accent}" stroke-width="6" stroke-linecap="round"/>`;
    b += `<circle class="pop" cx="${X(v.a1)}" cy="${150 - 10 - v.n1}" r="${8 + v.n1 / 2}" fill="${C.acc2}"/>${T(X(v.a1), 200, 'A: ' + v.a1 + ' (' + v.n1 + ')', 's-txt')}`;
    b += `<circle class="pop" ${d(1)} cx="${X(v.a2)}" cy="${150 - 10 - v.n2}" r="${8 + v.n2 / 2}" fill="${C.warn}"/>${T(X(v.a2), 200, 'B: ' + v.a2 + ' (' + v.n2 + ')', 's-txt')}`;
    b += `<polygon class="pop" ${d(3)} points="${X(v.c)},156 ${X(v.c) - 16},186 ${X(v.c) + 16},186" fill="${C.text}"/>${T(X(v.c), 230, 'combined = ' + v.c, 's-big')}`;
    return svg(520, 250, b);
  }

  function render(v) {
    switch (v.type) {
      case 'bars': return bars(v.items, v.unit);
      case 'avgbars': return bars(v.values.map((x, i) => ({ label: '#' + (i + 1), value: x, color: 'muted' })), '', { avg: v.avg });
      case 'track': return track(v); case 'parabola': return parabola(v); case 'triangle': return triangle(v); case 'circle': return circle(v);
      case 'ratio': return ratio(v); case 'mixture': return mixture(v); case 'cycle': return cycle(v); case 'balance': return balance(v);
      case 'cube': return cube(v); case 'venn': return venn(v); case 'grid': return grid(v); case 'seesaw': return seesaw(v);
    }
    return '';
  }

  /* ---------- Explainers: each returns {title, text, formula, controls:[{id,label,min,max,step,value}], draw(vals)->svg} ---------- */
  const EX = {
    percentages: { icon: '％', title: 'Percent = parts per hundred', blurb: 'A 10×10 grid makes any percentage visible. Successive changes multiply.',
      formula: 'x% of N = x/100 × N', controls: [{ id: 'p', label: 'Percent', min: 0, max: 100, step: 1, value: 35 }, { id: 'n', label: 'Of N', min: 100, max: 1000, step: 50, value: 400 }],
      draw: ({ p, n }) => { let b = ''; for (let i = 0; i < 100; i++) { const on = i < p; b += `<rect x="${30 + (i % 10) * 24}" y="${20 + Math.floor(i / 10) * 24}" width="20" height="20" rx="4" fill="${on ? C.accent : 'var(--bg)'}" style="transition:fill .3s"/>`; }
        return svg(520, 280, b + T(400, 110, p + '%', 's-big', 'middle', 'font-size="40"') + T(400, 150, `of ${n} = ${f(p * n / 100)}`, 's-txt') + T(400, 180, `${p} of 100 cells`, 's-mute')); } },
    profitloss: { icon: '₹', title: 'MP → SP → CP: three prices, two bases', blurb: 'Discount is taken on Marked Price; profit is measured on Cost Price.',
      formula: 'SP = MP(1 − d%) = CP(1 + p%)', controls: [{ id: 'cp', label: 'CP', min: 100, max: 1000, step: 50, value: 400 }, { id: 'mk', label: 'Markup %', min: 0, max: 100, step: 5, value: 50 }, { id: 'dc', label: 'Discount %', min: 0, max: 50, step: 5, value: 20 }],
      draw: ({ cp, mk, dc }) => { const mp = cp * (1 + mk / 100), sp = mp * (1 - dc / 100), pr = (sp - cp) / cp * 100;
        return bars([{ label: 'CP', value: cp, color: 'muted' }, { label: 'MP', value: mp, color: 'acc2' }, { label: 'SP', value: sp, color: sp >= cp ? 'accent' : 'bad' }], '₹').replace('</svg>', T(260, 22, (pr >= 0 ? 'Profit ' : 'Loss ') + f(Math.abs(pr)) + '%', 's-big', 'middle', `fill="${pr >= 0 ? C.accent : C.bad}"`) + '</svg>'); } },
    tsd: { icon: '🚆', title: 'Relative speed', blurb: 'Opposite directions: speeds add. Same direction: subtract. A train crossing a pole travels its own length.',
      formula: 'Time = (L₁ + L₂) / (v₁ ± v₂)', controls: [{ id: 'v', label: 'Speed km/h', min: 18, max: 126, step: 18, value: 54 }, { id: 'L', label: 'Length m', min: 60, max: 300, step: 20, value: 180 }],
      draw: ({ v, L }) => { const ms = v * 5 / 18, t = L / ms; const w = L * 0.9;
        return svg(520, 220, `<line x1="10" y1="150" x2="510" y2="150" stroke="${C.line}" stroke-width="4"/><rect x="330" y="80" width="6" height="70" fill="${C.warn}"/><g><rect y="118" width="${w}" height="30" rx="8" fill="${C.accent}"/><animateTransform attributeName="transform" type="translate" values="${330 - w - 10} 0;${340} 0" dur="${Math.max(t / 4, 0.8)}s" repeatCount="indefinite"/></g>` + T(260, 40, `${v} km/h = ${f(ms)} m/s`, 's-big') + T(260, 190, `pole crossed in ${f(t)} s`, 's-txt', 'middle', `fill="${C.acc2}"`)); } },
    algebra: { icon: 'x', title: 'Roots = where the curve meets zero', blurb: 'For x² − Sx + P, roots have sum S and product P. Slide S and P and watch the roots move.',
      formula: 'x² − (r₁+r₂)x + r₁r₂ = 0', controls: [{ id: 'r1', label: 'Root r₁', min: -6, max: 6, step: 1, value: -2 }, { id: 'r2', label: 'Root r₂', min: -6, max: 6, step: 1, value: 4 }],
      draw: ({ r1, r2 }) => r1 === r2 ? parabola({ s: 2 * r1, p: r1 * r1, roots: [r1, r1 + 1e-9] }) : parabola({ s: r1 + r2, p: r1 * r2, roots: [r1, r2] }).replace('</svg>', T(260, 24, `x² ${-(r1 + r2) >= 0 ? '+' : '−'} ${Math.abs(r1 + r2)}x ${r1 * r2 >= 0 ? '+' : '−'} ${Math.abs(r1 * r2)}`, 's-big') + '</svg>') },
    geometry: { icon: '△', title: 'Pythagoras as areas', blurb: 'The square on the hypotenuse has exactly the area of the two leg-squares combined.',
      formula: 'a² + b² = c²', controls: [{ id: 'a', label: 'Leg a', min: 2, max: 9, step: 1, value: 3 }, { id: 'b', label: 'Leg b', min: 2, max: 9, step: 1, value: 4 }],
      draw: ({ a, b }) => { const s = 20, c = Math.hypot(a, b), ox = 150, oy = 150; const A = [ox, oy], B = [ox + b * s, oy], Cc = [ox, oy - a * s];
        const sq = (p, q, col) => { const dx = q[0] - p[0], dy = q[1] - p[1]; return `<polygon points="${p} ${q} ${q[0] - dy},${q[1] + dx} ${p[0] - dy},${p[1] + dx}" fill="${col}" opacity=".55" style="transition:all .3s"/>`; };
        return svg(520, 300, sq(A, B, C.accent) + sq(Cc, A, C.acc2) + sq(B, Cc, C.warn) + `<polygon points="${A} ${B} ${Cc}" fill="var(--card)" stroke="${C.text}" stroke-width="2"/>` + T(430, 80, `${a}² + ${b}² = ${a * a + b * b}`, 's-big') + T(430, 112, `c = √${a * a + b * b} = ${f(c)}`, 's-txt', 'middle', `fill="${C.warn}"`)); } },
    numbers: { icon: '#', title: 'Cyclicity of remainders', blurb: 'Powers of a number repeat their remainders in a cycle — so huge exponents reduce to small ones.',
      formula: 'aⁿ mod m repeats with period k', controls: [{ id: 'a', label: 'Base a', min: 2, max: 9, step: 1, value: 3 }, { id: 'm', label: 'Divisor m', min: 3, max: 13, step: 1, value: 7 }],
      draw: ({ a, m }) => { const cyc = []; let v = a % m; for (let i = 0; i < 12 && !cyc.includes(v); i++) { cyc.push(v); v = v * a % m; } return cycle({ items: cyc, n: 100, ans: -1 }).replace(/n = 100/, `${a}ⁿ mod ${m}`).replace(/100 mod \d+ = \d+/, `period ${cyc.length}`); } },
    averages: { icon: 'μ', title: 'Average = the balance point', blurb: 'Raise one value and the mean line moves by (change ÷ count). Deviations above and below always cancel.',
      formula: 'mean = Σx / n', controls: [{ id: 'x', label: 'Last value', min: 10, max: 100, step: 1, value: 70 }, { id: 'n', label: 'Count n', min: 3, max: 8, step: 1, value: 5 }],
      draw: ({ x, n }) => { const vals = [40, 55, 35, 60, 45, 50, 38].slice(0, n - 1).concat([x]); const avg = vals.reduce((s, y) => s + y, 0) / vals.length; return bars(vals.map((y, i) => ({ label: '#' + (i + 1), value: y, color: i === vals.length - 1 ? 'accent' : 'muted' })), '', { avg }); } },
    ratio: { icon: ':', title: 'Ratios are equal-sized parts', blurb: 'a:b means split the total into a+b equal blocks. Find one block and everything follows.',
      formula: 'share = total × part / Σparts', controls: [{ id: 'a', label: 'a', min: 1, max: 8, step: 1, value: 3 }, { id: 'b', label: 'b', min: 1, max: 8, step: 1, value: 5 }, { id: 't', label: 'Total', min: 40, max: 400, step: 40, value: 240 }],
      draw: ({ a, b, t }) => ratio({ parts: [a, b], unitVal: t / (a + b), labels: ['A', 'B'] }) }
  };

  window.QViz = { render, EX, bars };
})();
