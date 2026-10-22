/* Quant Lab: generator core: helpers, registry, MCQ/TITA formatting, answer checking. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api; else root.QGen = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  let rand = Math.random;
  const H = {};
  H.ri = (a, b) => a + Math.floor(rand() * (b - a + 1));
  H.pick = arr => arr[Math.floor(rand() * arr.length)];
  H.isInt = x => Math.abs(x - Math.round(x)) < 1e-9;
  H.gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
  H.lcm = (a, b) => a / H.gcd(a, b) * b;
  H.fmt = x => (H.isInt(x) ? String(Math.round(x)) : String(Math.round(x * 100) / 100));
  H.r2 = x => Math.round(x * 100) / 100;
  H.frac = (n, d) => { const g = H.gcd(n, d) || 1; n /= g; d /= g; if (d < 0) { n = -n; d = -d; } return d === 1 ? String(n) : `${n}/${d}`; };
  H.fact = n => { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; };
  H.C = (n, k) => { if (k < 0 || k > n) return 0; let r = 1; for (let i = 1; i <= k; i++) r = r * (n - k + i) / i; return Math.round(r); };
  H.retry = fn => { for (let i = 0; i < 5000; i++) { const r = fn(); if (r) return r; } throw new Error('generator exhausted'); };
  H.ord = n => { const v = n % 100; return n + (v >= 11 && v <= 13 ? 'th' : ({ 1: 'st', 2: 'nd', 3: 'rd' }[n % 10] || 'th')); };
  H.shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  const SECTIONS = [
    { id: 'arith', name: 'Arithmetic', topics: ['percentages', 'profitloss', 'tsd', 'work', 'interest', 'mixtures', 'partnership', 'averages', 'ratio'] },
    { id: 'alg', name: 'Algebra', topics: ['algebra', 'inequalities', 'functions', 'logs', 'progressions', 'maxmin'] },
    { id: 'geo', name: 'Geometry & Mensuration', topics: ['geometry', 'mensuration', 'coordinate', 'circles'] },
    { id: 'num', name: 'Number Systems', topics: ['numbers'] },
    { id: 'mod', name: 'Modern Math', topics: ['pnc', 'probability', 'sets'] }
  ];
  const TOPICS = {
    percentages: ['Percentages', '％', 'Successive change, base flips, elections'], profitloss: ['Profit & Loss', '₹', 'MP·SP·CP, discounts, false weights'],
    tsd: ['Time-Speed-Distance', '🚆', 'Trains, boats, meeting points'], work: ['Time & Work', '⚙', 'Rates, pipes & cisterns, wages'],
    interest: ['SI & CI', '📈', 'Simple vs compound growth, instalments'], mixtures: ['Mixtures & Alligation', '⚗', 'Alligation cross, replacement'],
    partnership: ['Partnership', '🤝', 'Capital × time, salaries, interest'], averages: ['Averages', 'μ', 'Replacement, weighted mean'],
    ratio: ['Ratio-Proportion', ':', 'Chaining, savings, variation'], algebra: ['Linear & Quadratic', 'x', 'Equations, roots, identities'],
    inequalities: ['Inequalities & Modulus', '|x|', 'Number line, intervals, lattice'], functions: ['Functions & Graphs', 'ƒ', 'Composition, inverse, functional eqns'],
    logs: ['Logarithms', 'log', 'Laws, equations, digit counts'], progressions: ['Progressions', 'Σ', 'AP, GP, HP, sums'],
    maxmin: ['Maxima & Minima', '⛰', 'AM-GM, vertex, min of max'], geometry: ['Triangles', '△', 'Pythagoras, Heron, similarity'],
    mensuration: ['Mensuration 3D', '⬛', 'Cuboid, cylinder, cone, sphere'], coordinate: ['Coordinate Geometry', '⌗', 'Distance, area, lattice points'],
    circles: ['Circles & Polygons', '◯', 'Chords, tangents, polygons'], numbers: ['Number Systems', '#', 'Remainders, factorials, HCF/LCM, divisors'],
    pnc: ['Permutations & Combinations', '⁂', 'Slots, words, circular, grids'], probability: ['Probability', '🎲', 'Dice, urns, Bayes'],
    sets: ['Set Theory & Venn', '◎', 'Inclusion–exclusion, overlaps']
  };
  const TOPIC_TRAPS = {
    percentages: 'Always ask: percent OF WHAT? The base decides everything.', profitloss: 'Profit/loss % is on CP; discount % is on MP.',
    tsd: 'Keep units consistent (km/h × 5/18 = m/s).', work: 'Add rates (work per day), never days.', interest: 'SI is linear, CI is exponential — do not mix formulas.',
    mixtures: 'Track the component that does not change.', partnership: 'Profit share ∝ capital × time.', averages: 'Work with totals, not averages.',
    ratio: 'Ratios are parts — find the value of one part first.', algebra: 'Check your answer by substituting back.',
    inequalities: 'Watch strict (<) vs inclusive (≤) endpoints.', functions: 'Respect the domain; apply inner functions first.',
    logs: 'Log arguments must be positive; check every root.', progressions: 'n terms means n − 1 gaps.', maxmin: 'Report the VALUE, not the point where it occurs (unless asked).',
    geometry: 'Draw the figure; label what is given.', mensuration: 'Area scales by k², volume by k³.', coordinate: 'Keep vertex order consistent.',
    circles: 'Radius ⟂ tangent and ⟂ bisects a chord.', numbers: 'Prime-factorise first.', pnc: 'Order matters → permutation; groups → combination.',
    probability: 'Probabilities lie in [0, 1]; use complements for "at least".', sets: 'Draw the Venn diagram and fill from the innermost region outward.'
  };
  const TYPES = {};
  function register(topic, level, id, name, fn) {
    ((TYPES[topic] = TYPES[topic] || {})[level] = TYPES[topic][level] || []).push({ id, name, fn });
  }
  function mcq(p, distract) {
    const ansLabel = p.display || H.fmt(p.answer);
    const opts = [{ v: p.answer, label: ansLabel }]; const seen = new Set([ansLabel]);
    const add = (v, label) => { if (v == null || !isFinite(v)) return; label = label || H.fmt(v); if (seen.has(label) || Math.abs(v - p.answer) <= Math.max(p.tol || 0.011, 1e-9)) return; seen.add(label); opts.push({ v, label }); };
    (distract || []).forEach(d => (typeof d === 'object' ? add(d.v, d.label) : add(d)));
    const step = Math.max(1, Math.round(Math.abs(p.answer) * 0.1));
    for (let k = 1; opts.length < 4 && k < 50; k++) { add(p.answer + k * step); if (opts.length < 4) add(p.answer - k * step); }
    p.options = H.shuffle(opts.slice(0, 4)); p.answerIndex = p.options.findIndex(o => o.label === ansLabel); p.format = 'mcq';
    return p;
  }
  function generate(topic, level, opts = {}) {
    if (opts.rng) rand = opts.rng;
    try {
      const lv = ['easy', 'medium', 'hard'].includes(level) ? level : 'easy';
      const list = (TYPES[topic] || {})[lv]; if (!list) throw new Error('Unknown topic ' + topic);
      const t = opts.typeId ? list.find(x => x.id === opts.typeId) : H.pick(list);
      if (!t) throw new Error('Unknown type ' + opts.typeId);
      const p = t.fn(H);
      p.topic = topic; p.level = lv; p.typeId = t.id; p.typeName = t.name; p.topicName = TOPICS[topic][0];
      p.format = 'tita'; p.unit = p.unit || ''; p.tol = p.tol || 0.011;
      while (p.traps.length < 2) p.traps.push(TOPIC_TRAPS[topic]);
      if (p.mcq) { mcq(p, p.mcq); delete p.mcq; }
      if (!p.display) p.display = H.fmt(p.answer);
      return p;
    } finally { rand = Math.random; }
  }
  const LETTERS = ['A', 'B', 'C', 'D'];
  function parseNum(s) {
    s = String(s).trim().replace(/[₹,\s%]/g, '').replace(/(cm²|cm³|cm|km\/h|kg|days|hours|h|L|m²|m)$/i, '');
    const f = s.match(/^(-?\d+(?:\.\d+)?)\/(\d+(?:\.\d+)?)$/); if (f) return +f[1] / +f[2];
    if (!/^-?\d*\.?\d+$/.test(s)) return NaN; return parseFloat(s);
  }
  function check(p, input) {
    if (input == null) return false;
    const s = String(input).trim();
    if (p.format === 'mcq' && /^[A-Da-d]$/.test(s)) return LETTERS.indexOf(s.toUpperCase()) === p.answerIndex;
    const v = parseNum(s); if (!isFinite(v)) return false;
    return Math.abs(v - p.answer) <= Math.max(p.tol, Math.abs(p.answer) * 1e-9);
  }
  function listTypes() { const out = []; for (const t in TYPES) for (const l in TYPES[t]) TYPES[t][l].forEach(x => out.push({ topic: t, level: l, id: x.id, name: x.name })); return out; }
  return { H, SECTIONS, TOPICS, TYPES, register, generate, check, listTypes, fmt: H.fmt, LETTERS };
});
