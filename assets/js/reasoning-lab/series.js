/* Topic: Series — number, letter, letter-cluster, wrong-number and figure series */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle } = RL.u;
  RL.topic('series', 'Series', '🔢', 'Difference ladders that show the hidden rule, plus figure series built from rotation and counting.', 'Verbal & Coding');
  const A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', L = n => A[((n % 26) + 26) % 26];
  const PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31];
  // each family returns {t:[7 terms], d: description}
  const FAM = {
    ap: () => { const a = ri(3, 60), d = pick([3, 4, 5, 6, 7, 9, 11, 12, -4, -7]); return { t: [...Array(7)].map((_, i) => a + d * i + (d < 0 ? 60 : 0)), d: `Add ${d} each time.` }; },
    gp: () => { const a = ri(2, 7), r = pick([2, 3]); return { t: [...Array(7)].map((_, i) => a * r ** i), d: `Multiply by ${r} each time.` }; },
    sq: () => { const k = ri(1, 6), c = pick([0, 1, -1, 2, 3]); return { t: [...Array(7)].map((_, i) => (i + k) ** 2 + c), d: `n² ${c >= 0 ? '+' : '−'} ${Math.abs(c)} for n = ${k}, ${k + 1}, …` }; },
    cube: () => { const k = ri(1, 4), c = pick([0, 1, -1, 2]); return { t: [...Array(7)].map((_, i) => (i + k) ** 3 + c), d: `n³ ${c >= 0 ? '+' : '−'} ${Math.abs(c)} for n = ${k}, ${k + 1}, …` }; },
    d2: () => { const a = ri(2, 30), d0 = ri(1, 6), dd = ri(1, 4); let x = a; const t = [x]; for (let i = 0; i < 6; i++) { x += d0 + dd * i; t.push(x); } return { t, d: `The differences go up by ${dd}: ${d0}, ${d0 + dd}, ${d0 + 2 * dd}, …` }; },
    dgp: () => { const a = ri(2, 20), d0 = ri(1, 4), r = 2; let x = a, d = d0; const t = [x]; for (let i = 0; i < 6; i++) { x += d; d *= r; t.push(x); } return { t, d: `The differences double: ${d0}, ${2 * d0}, ${4 * d0}, …` }; },
    alt: () => { const a = ri(2, 20), b = ri(20, 60), d1 = ri(2, 7), d2 = pick([-3, -2, 3, 4, 5, 6]); const t = [...Array(7)].map((_, i) => i % 2 ? b + d2 * (i >> 1) : a + d1 * (i >> 1)); return { t, d: `Two series alternate: odd places add ${d1}, even places add ${d2}.` }; },
    muladd: () => { const m = pick([2, 3]), c = pick([1, -1, 2, 3, -2]), a = ri(1, 6); let x = a; const t = [x]; for (let i = 0; i < 6; i++) { x = x * m + c; t.push(x); } return t.every(v => v > 0) ? { t, d: `× ${m} then ${c >= 0 ? '+' : '−'} ${Math.abs(c)} each time.` } : null; },
    mulinc: () => { const a = ri(1, 5), v = pick([0, 1]); let x = a; const t = [x]; for (let i = 1; i <= 6; i++) { x = x * i + v * i; t.push(x); } return { t, d: v ? '×1 + 1, ×2 + 2, ×3 + 3, …' : '×1, ×2, ×3, ×4, …' }; },
    altops: () => { const m = pick([2, 3]), c = ri(2, 9), a = ri(1, 9); let x = a; const t = [x]; for (let i = 0; i < 6; i++) { x = i % 2 ? x + c : x * m; t.push(x); } return { t, d: `Alternately × ${m} and + ${c}.` }; },
    dprime: () => { const a = ri(1, 40), s = ri(0, 3); let x = a; const t = [x]; for (let i = 0; i < 6; i++) { x += PR[s + i]; t.push(x); } return { t, d: `Add consecutive primes: ${PR.slice(s, s + 3).join(', ')}, …` }; },
    dsq: () => { const a = ri(1, 40), s = ri(1, 4); let x = a; const t = [x]; for (let i = 0; i < 6; i++) { x += (s + i) ** 2; t.push(x); } return { t, d: `Add consecutive squares: ${s * s}, ${(s + 1) ** 2}, ${(s + 2) ** 2}, …` }; },
    halfadd: () => { const a = pick([2, 3, 4, 5, 6, 7]) * 64; let x = a; const t = [x]; for (let i = 0; i < 6; i++) { x = x / 2 + 4; t.push(x); } return t.every(Number.isInteger) ? { t, d: '÷ 2 then + 4 each time.' } : null; }
  };
  RL.seriesFam = FAM;
  const sviz = (terms, extra) => Object.assign({ kind: 'series', terms }, extra || {});
  const diffs = t => t.slice(1).map((v, i) => v - t[i]);
  /* originality guard: never reuse a 4-term run that already appears in AptiSetu's own question bank */
  const BANK = new Set('0,1,2,3 1,2,3,4 1,2,6,24 1,3,7,13 1,4,27,256 10,12,14,16 10,16,28,52 10,28,82,244 10,29,65,127 11,15,19,23 11,23,47,95 11,23,47,96 12,14,16,18 12,14,28,30 120,99,80,63 121,169,289,324 121,242,363,484 123,234,345,456 13,17,19,27 14,16,18,20 14,21,35,49 15,7,22,9 16,25,36,49 16,4,0,4 169,289,324,361 17,19,27,29 17,23,29,33 2,3,4,5 2,3,5,7 2,4,4,5 2,4,6,8 2,5,11,23 2,6,12,20 2,6,24,120 21,19,17,15 21,35,49,52 216,343,512,720 22,9,31,12 23,29,33,37 23,47,95,191 23,47,96,191 234,345,456,568 24,21,17,12 242,363,484,595 25,36,49,50 26,24,21,17 27,64,100,125 3,10,29,65 3,3,5,7 3,4,5,6 3,5,7,11 3,5,7,8 3,5,9,17 3,6,12,24 3,7,13,21 3,7,15,31 3,8,18,38 3,9,5,11 343,512,720,1000 35,48,63,80 4,0,4,16 4,10,28,82 4,4,5,7 4,5,6,7 4,5,7,7 4,6,12,14 4,6,12,16 4,6,8,10 4,8,12,16 4,9,25,49 48,63,80,100 5,11,23,47 5,11,3,8 5,6,7,8 5,7,11,13 5,7,7,7 5,7,8,9 5,9,17,33 54,63,70,84 6,12,14,28 6,12,20,30 6,8,10,12 7,10,16,28 7,15,31,63 7,22,9,31 7,3,9,5 7,7,7,9 7,8,9,11 7,9,3,1 8,18,38,78 8,27,64,100 8,4,2,6 9,25,49,121 9,5,11,3 99,80,63,48'.split(' '));
  const inBank = t => { for (let i = 0; i + 4 <= t.length; i++) if (BANK.has(t.slice(i, i + 4).join(','))) return true; return false; };
  function numType(id, level, name, fams, exams, missing) {
    RL.reg('series', level, id, name, exams, () => {
      const f = pick(fams), r = FAM[f](); if (!r) return null; const t = r.t, k = missing ? ri(2, 5) : 6, ans = t[k]; if (inBank(t)) return null;
      if (t.some(v => Math.abs(v) > 99999)) return null; const shown = t.slice(0, missing ? 7 : 6).map((v, i) => i === k ? '?' : v);
      const ds = [ans + 1, ans - 1, ans + 2, ans - 2, ans + (diffs(t)[k - 1] || 3), ans * 2, ans + 10, ans - 10].filter(v => v !== ans);
      return { question: `Find the ${missing ? 'missing' : 'next'} term: ${shown.join(', ')}${missing ? '' : ', ?'}`, ...RL.mcq(String(ans), shuffle(ds).map(String)), viz: sviz(shown),
        steps: [{ text: 'Look at the differences between neighbouring terms.', viz: sviz(shown, { diffs: !missing }) }, { text: `Rule: ${r.d}`, viz: sviz(t.slice(0, missing ? 7 : 7), { diffs: true, hl: k }) }, { text: `So the ${missing ? 'missing' : 'next'} term is ${ans}.`, viz: sviz(t.slice(0, 7), { hl: k }) }],
        traps: ['If the differences don\'t settle, try ratios, squares or cubes, or alternating terms.', 'Check your rule against EVERY term, not just the first three.'], params: { fam: f, shown, k } };
    });
  }
  numType('ser-e1', 'easy', 'Number series: next term', ['ap', 'gp', 'sq', 'd2', 'alt'], ['ssc', 'bank', 'cuet', 'govt']);
  numType('ser-e3', 'easy', 'Number series: missing term', ['ap', 'gp', 'sq', 'd2', 'cube'], ['ssc', 'bank', 'cuet', 'govt'], true);
  numType('ser-m3', 'medium', 'Mixed operations', ['muladd', 'altops', 'dprime', 'dsq', 'cube', 'dgp', 'halfadd'], ['ssc', 'bank', 'cuet', 'govt']);
  // letter series
  RL.reg('series', 'easy', 'ser-e2', 'Letter series', ['ssc', 'cuet', 'govt'], () => {
    const s = ri(0, 25), inc = pick([0, 1]), d = pick([2, 3, 4, 5, -2, -3]); const p = [s]; for (let i = 1; i < 7; i++) p.push(p[i - 1] + d + (inc ? (i - 1) : 0));
    const t = p.map(L), ans = t[6]; const ds = [L(p[6] + 1), L(p[6] - 1), L(p[6] + 2), L(p[5] + d), L(p[6] + 3)].filter(x => x !== ans);
    return { question: `Which letter comes next: ${t.slice(0, 6).join(', ')}, ?`, ...RL.mcq(ans, ds), viz: sviz(t.slice(0, 6), { letters: true }),
      steps: [{ text: 'Turn letters into positions (A = 1).', viz: sviz(p.slice(0, 6).map(v => ((v % 26) + 26) % 26 + 1), { diffs: true }) }, { text: inc ? `The gaps grow by 1: ${d}, ${d + 1}, ${d + 2}, …` : `Each step moves ${d}.` }, { text: `Next letter: ${ans}.`, viz: sviz(t, { letters: true, hl: 6 }) }],
      traps: ['The alphabet wraps: after Z comes A.', 'Use EJOTY (5, 10, 15, 20, 25) to count positions fast.'], params: { p } };
  });
  RL.reg('series', 'medium', 'ser-m2', 'Letter-cluster series', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const w = pick([2, 3]); const st = [...Array(w)].map(() => ri(0, 25)), dd = [...Array(w)].map(() => pick([1, 2, 3, -1, -2, 4, 5])); const T = [...Array(6)].map((_, i) => st.map((s, j) => L(s + dd[j] * i)).join(''));
    const ans = T[5]; const ds = []; for (let j = 0; j < w; j++) for (const e of [1, -1]) ds.push(st.map((s, q) => L(s + dd[q] * 5 + (q === j ? e : 0))).join('')); ds.push([...ans].reverse().join(''));
    return { question: `Find the next term: ${T.slice(0, 5).join(', ')}, ?`, ...RL.mcq(ans, shuffle(ds).filter(x => x !== ans)), viz: sviz(T.slice(0, 5), { letters: true }),
      steps: [{ text: 'Treat each letter position as its own series.', viz: sviz(T.slice(0, 5), { letters: true, cols: w }) }].concat(dd.map((d, j) => ({ text: `Letter ${j + 1}: ${T.slice(0, 5).map(x => x[j]).join(' → ')} moves ${d > 0 ? '+' : ''}${d} each time.` }))).concat([{ text: `Next: ${ans}.`, viz: sviz(T, { letters: true, hl: 5 }) }]),
      traps: ['Each position follows its own rule, so don\'t mix them.', 'Watch for wrap-around near Z.'], params: { T } };
  });
  // wrong number
  // guard: no OTHER single term may be the 'wrong' one under a simple rule (polynomial ≤ cubic, GP, two interleaved APs)
  function polyFit(pts, deg) { if (pts.length <= deg + 1) return true; const base = pts.slice(0, deg + 1);
    const at = x => base.reduce((s, [xi, yi], i) => s + yi * base.reduce((m, [xj], j) => (j === i ? m : m * (x - xj) / (xi - xj)), 1), 0);
    return pts.slice(deg + 1).every(([x, y]) => Math.abs(at(x) - y) < 1e-6); }
  function simpleFit(u) { const pts = u.map((y, x) => [x, y]).filter(q => q[1] !== null);
    if (polyFit(pts, 3)) return true; const rs = []; for (let i = 0; i + 1 < u.length; i++) if (u[i] !== null && u[i + 1] !== null && u[i]) rs.push(u[i + 1] / u[i]);
    if (rs.length && rs.every(r => Math.abs(r - rs[0]) < 1e-9) && pts.length >= 5) return true;
    return polyFit(pts.filter(q => q[0] % 2 === 0), 1) && polyFit(pts.filter(q => q[0] % 2 === 1), 1); }
  function wrongType(id, level, name, fams, exams) {
    RL.reg('series', level, id, name, exams, () => {
      const f = pick(fams), r = FAM[f](); if (!r) return null; const t = r.t.slice(0, 7); if (inBank(t)) return null; if (t.some(v => Math.abs(v) > 99999)) return null; const k = ri(1, 6);
      const bad = t.slice(); bad[k] = t[k] + pick([1, -1, 2, -2, 3, 4, -3, 5, 10]) * (Math.abs(t[k]) > 200 ? pick([1, 10]) : 1); if (bad[k] === t[k]) return null;
      const opts = shuffle([...Array(7).keys()].filter(i => i !== k)).slice(0, 3).map(i => String(bad[i]));
      if (new Set(bad).size < 7) return null;
      for (let j = 0; j < 7; j++) if (j !== k) { const u = bad.slice(); u[j] = null; if (simpleFit(u)) return null; }
      return { question: `Spot the number that breaks the pattern: ${bad.join(', ')}`, ...RL.mcq(String(bad[k]), opts), viz: sviz(bad),
        steps: [{ text: 'Find the rule that fits most of the terms.', viz: sviz(bad, { diffs: true }) }, { text: `Rule: ${r.d}`, viz: sviz(t, { diffs: true, hl: k }) }, { text: `The term at position ${k + 1} should be ${t[k]}, not ${bad[k]}.`, viz: sviz(bad, { hl: k, bad: true }) }],
        traps: ['One wrong term spoils two differences, so look for the pair that breaks the pattern.', 'Fix the suspect term and re-check the whole series.'], params: { fam: f, bad, k } };
    });
  }
  wrongType('ser-m1', 'medium', 'Wrong number (simple rules)', ['ap', 'gp', 'sq', 'd2', 'cube'], ['bank', 'ssc', 'govt']);
  wrongType('ser-h3', 'hard', 'Wrong number (two-tier rules)', ['muladd', 'mulinc', 'altops', 'dprime', 'dsq', 'dgp', 'halfadd'], ['bank', 'ssc', 'cat']);
  numType('ser-h1', 'hard', 'Two-tier number series', ['mulinc', 'dprime', 'dsq', 'muladd', 'altops', 'dgp'], ['bank', 'ssc', 'cat', 'cuet']);
  // figure series: arrow angle (45° steps), dot count, shaded corner
  const fkey = s => `${s.a}|${s.n}|${s.c}`;
  RL.reg('series', 'hard', 'ser-h2', 'Figure series (rotation + count)', ['ssc', 'cuet', 'govt', 'bank'], () => {
    const a0 = ri(0, 7), da = pick([1, 2, 3, -1, -2]), n0 = ri(1, 3), dn = pick([1, 1, 0, -1]), c0 = ri(0, 3), dc = pick([1, -1, 2]);
    const st = i => ({ a: ((a0 + da * i) % 8 + 8) % 8, n: n0 + dn * i + (dn < 0 ? 5 : 0), c: ((c0 + dc * i) % 4 + 4) % 4 });
    const S = [0, 1, 2, 3, 4].map(st); if (S.some(s => s.n < 1 || s.n > 9)) return null; const ans = st(4);
    const D = [{ a: (ans.a + 1) % 8, n: ans.n, c: ans.c }, { a: ans.a, n: ans.n + 1, c: ans.c }, { a: ans.a, n: ans.n, c: (ans.c + 1) % 4 }, { a: (ans.a + 4) % 8, n: ans.n, c: ans.c }, { a: ans.a, n: Math.max(1, ans.n - 1), c: (ans.c + 2) % 4 }];
    const mk = s => ({ label: '', key: fkey(s), viz: { kind: 'fig', s } });
    const o = RL.mcq(mk(ans), shuffle(D).map(mk));
    return { question: 'Which figure comes next in the series?', ...o, viz: { kind: 'figseries', items: S.slice(0, 4) },
      steps: [{ text: `Arrow: turns ${Math.abs(da) * 45}° ${da > 0 ? 'clockwise' : 'anticlockwise'} each step.`, viz: { kind: 'figseries', items: S.slice(0, 4), track: 'a' } }, { text: dn ? `Dots: ${dn > 0 ? 'one more' : 'one fewer'} each step.` : 'Dots: the number stays the same.', viz: { kind: 'figseries', items: S.slice(0, 4), track: 'n' } },
        { text: `Shaded corner: moves ${Math.abs(dc)} corner(s) ${dc > 0 ? 'clockwise' : 'anticlockwise'} each step.`, viz: { kind: 'figseries', items: S.slice(0, 4), track: 'c' } }, { text: 'Put all three rules together for figure 5.', viz: { kind: 'figseries', items: S } }],
      traps: ['Track each element on its own; several things change at once.', 'A 180° turn looks like a mirror image, so check the direction.'], params: { S, ans } };
  });
  RL.figKey = fkey;
})(typeof globalThis !== 'undefined' ? globalThis : this);
