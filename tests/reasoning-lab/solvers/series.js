/* Independent series solver: brute-forces recurrence families x[i+1] = F(x[i], x[i-1], i; params) from x[0]
   over wide parameter grids and matches every known term. */
const PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47];
const R = (a, b) => { const o = []; for (let i = a; i <= b; i++) o.push(i); return o; };
const FAMS = [];
const add = (name, grid, F) => grid.forEach(P => FAMS.push({ name, P, F }));
add('ap', R(-30, 30).filter(Boolean).map(d => [d]), (x, y, i, [d]) => x + d);
add('gp', [[2], [3], [4], [0.5]], (x, y, i, [r]) => x * r);
add('sq', R(0, 15).map(k => [k]), (x, y, i, [k]) => x + 2 * (i + k) + 1);
add('cube', R(0, 10).map(k => [k]), (x, y, i, [k]) => x + 3 * (i + k) ** 2 + 3 * (i + k) + 1);
add('d2', R(-20, 20).flatMap(d0 => R(-10, 10).filter(Boolean).map(dd => [d0, dd])), (x, y, i, [d0, dd]) => x + d0 + dd * i);
add('dgp', R(1, 20).flatMap(d0 => [2, 3].map(r => [d0, r])), (x, y, i, [d0, r]) => x + d0 * r ** i);
add('muladd', [2, 3, 4, 0.5].flatMap(m => R(-12, 12).map(c => [m, c])), (x, y, i, [m, c]) => x * m + c);
add('mulinc', R(0, 3).map(v => [v]), (x, y, i, [v]) => x * (i + 1) + v * (i + 1));
add('altops', [2, 3, 4].flatMap(m => R(1, 12).map(c => [m, c])), (x, y, i, [m, c]) => (i % 2 ? x + c : x * m));
add('dprime', R(0, 8).map(s => [s]), (x, y, i, [s]) => x + PR[s + i]);
add('dsq', R(0, 8).map(s => [s]), (x, y, i, [s]) => x + (s + i) ** 2);
// two interleaved APs: x[i+1] = x[i-1] + (i odd ? d1 : d2); x[1] taken from the data
add('alt', R(-10, 10).flatMap(d1 => R(-10, 10).map(d2 => [d1, d2])), (x, y, i, [d1, d2]) => (i === 0 ? null : y + ((i + 1) % 2 ? d2 : d1)));
function run(f, t, n) { const s = [t[0]]; for (let i = 0; i + 1 < n; i++) { let v = f.F(s[i], s[i - 1], i, f.P); if (v === null) { if (t[1] == null) return null; v = t[1]; } s.push(v); } return s; }
const fitsAll = (t, n) => { const out = []; for (const f of FAMS) { const s = run(f, t, n); if (s && t.every((v, i) => v == null || v === s[i])) out.push(s); } return out; };
const nums = q => q.split(':')[1].split(',').map(x => x.trim()).map(x => (x === '?' ? null : +x));
module.exports = {};
for (const id of ['ser-e1', 'ser-m3', 'ser-h1']) module.exports[id] = p => { const t = nums(p.question).filter(x => x !== null); const pr = new Set(fitsAll(t, 7).map(s => s[6]));
  if (pr.size !== 1) throw new Error('next term not unique: ' + [...pr].join('/')); return String([...pr][0]); };
module.exports['ser-e3'] = p => { const t = nums(p.question); const k = t.indexOf(null); const pr = new Set(fitsAll(t, 7).map(s => s[k]));
  if (pr.size !== 1) throw new Error('missing term not unique: ' + [...pr].join('/')); return String([...pr][0]); };
for (const id of ['ser-m1', 'ser-h3']) module.exports[id] = p => { const t = nums(p.question); if (fitsAll(t, 7).length) throw new Error('series already fits');
  return o => { const k = t.indexOf(+o.label); if (k < 0 || t.indexOf(+o.label, k + 1) >= 0) throw new Error('option value ambiguous'); const u = t.slice(); u[k] = null; return fitsAll(u, 7).length > 0; }; };
const AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', ix = c => AL.indexOf(c);
module.exports['ser-e2'] = p => { const L = p.question.split(':')[1].split(',').map(s => s.trim()).filter(s => s !== '?').map(ix);
  const d = L.slice(1).map((x, i) => ((x - L[i]) % 26 + 26) % 26); const dd = d.slice(1).map((x, i) => x - d[i]);
  // constant step (mod 26) or steps growing by +1 (mod 26)
  if (d.every(x => x === d[0])) return AL[(L[5] + d[0]) % 26]; if (dd.every(x => ((x - 1) % 26 + 26) % 26 === 0)) return AL[(L[5] + d[4] + 1) % 26]; throw new Error('no letter rule'); };
module.exports['ser-m2'] = p => { const T = p.question.split(':')[1].split(',').map(s => s.trim()).filter(s => s !== '?'); let out = '';
  for (let j = 0; j < T[0].length; j++) { const c = T.map(w => ix(w[j])); const d = c.slice(1).map((x, i) => ((x - c[i]) % 26 + 26) % 26); if (!d.every(x => x === d[0])) throw new Error('column rule'); out += AL[(c[4] + d[0]) % 26]; } return out; };
module.exports['ser-h2'] = p => { const S = p.viz.items; const step = (k, m) => { const ds = S.slice(1).map((s, i) => m ? ((s[k] - S[i][k]) % m + m) % m : s[k] - S[i][k]); if (!ds.every(x => x === ds[0])) throw new Error('fig rule ' + k); return ds[0]; };
  const a = (S[3].a + step('a', 8)) % 8, n = S[3].n + step('n', 0), c = (S[3].c + step('c', 4)) % 4; return o => o.key === `${a}|${n}|${c}`; };
