/* Independent inequality solver: strength matrix closure (−1 none, 0 ≥, 1 >), relation-possibility sets. */
const SET = { '>': ['gt'], '≥': ['gt', 'eq'], '=': ['eq'], '<': ['lt'], '≤': ['lt', 'eq'] };
const DESC = { 'is neither smaller than nor equal to': '>', 'is not smaller than': '≥', 'is neither smaller than nor greater than': '=', 'is neither greater than nor equal to': '<', 'is not greater than': '≤' };
function legendOf(p) { const L = {}; for (const c of p.clues) { const m = c.match(/^'x (\S+) y' means x (.+) y\.$/); if (m) { if (!DESC[m[2]]) throw new Error('desc ' + m[2]); L[m[1]] = DESC[m[2]]; } } return L; }
const decode = (s, L) => s.split(' ').map(t => L[t] || t).join(' ');
function chainRel(str) { const t = str.trim().split(/\s+/), out = []; for (let i = 1; i < t.length; i += 2) { if (!SET[t[i]]) throw new Error('op ' + t[i]); out.push([t[i - 1], t[i], t[i + 1]]); } return out; }
function closure(rels) { const V = [...new Set(rels.flatMap(r => [r[0], r[2]]))], n = V.length, ix = Object.fromEntries(V.map((v, i) => [v, i]));
  const s = V.map(() => V.map(() => -1)); V.forEach((_, i) => { s[i][i] = 0; });
  const add = (a, b, st) => { s[ix[a]][ix[b]] = Math.max(s[ix[a]][ix[b]], st); };
  for (const [a, o, b] of rels) { if (o === '>') add(a, b, 1); if (o === '≥') add(a, b, 0); if (o === '<') add(b, a, 1); if (o === '≤') add(b, a, 0); if (o === '=') { add(a, b, 0); add(b, a, 0); } }
  for (let k = 0; k < n; k++) for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) if (s[i][k] >= 0 && s[k][j] >= 0) s[i][j] = Math.max(s[i][j], Math.max(s[i][k], s[k][j]));
  V.forEach((_, i) => { if (s[i][i] > 0) throw new Error('contradiction'); });
  return { poss(x, y) { if (!(x in ix) || !(y in ix)) throw new Error('unknown var ' + x + y); const a = s[ix[x]][ix[y]], b = s[ix[y]][ix[x]], P = [];
    if (b < 0) P.push('gt'); if (a < 1 && b < 1) P.push('eq'); if (a < 0) P.push('lt'); return P; } };
}
const sure = (C, [x, o, y]) => C.poss(x, y).every(r => SET[o].includes(r));
function judge(p) { const L = legendOf(p); const rels = [], concl = [];
  for (const c of p.clues) { let m; if ((m = c.match(/^Statement: (.+)$/))) rels.push(...chainRel(decode(m[1], L))); else if ((m = c.match(/^Conclusion \w+: (.+)$/))) concl.push(chainRel(decode(m[1], L))[0]); }
  return { C: closure(rels), concl }; }
function two(p) { const { C, concl: [a, b] } = judge(p); const ta = sure(C, a), tb = sure(C, b);
  if (ta && tb) return 'Both I and II are true'; if (ta) return 'Only I is true'; if (tb) return 'Only II is true';
  let bb = b; if (b[0] === a[2] && b[2] === a[0]) bb = [a[0], { '>': '<', '<': '>', '≥': '≤', '≤': '≥', '=': '=' }[b[1]], a[2]];
  if (bb[0] === a[0] && bb[2] === a[2]) { const P = C.poss(a[0], a[2]); const A = SET[a[1]], B = SET[bb[1]];
    if (P.every(r => A.includes(r) || B.includes(r)) && !P.some(r => A.includes(r) && B.includes(r))) return 'Either I or II is true'; }
  return 'Neither I nor II is true'; }
function three(p) { const { C, concl } = judge(p); const R = ['I', 'II', 'III'].filter((_, i) => sure(C, concl[i]));
  if (!R.length) return 'None is true'; if (R.length === 3) return 'All I, II and III are true'; if (R.length === 1) return `Only ${R[0]} is true`; return `Only ${R[0]} and ${R[1]} are true`; }
function targets(q) { return [...q.matchAll(/"(\w) (\S) (\w)"/g)].map(m => [m[1], m[2], m[3]]); }
const safe = f => o => { try { return f(o); } catch (e) { if (/contradiction/.test(e.message)) return false; throw e; } };
module.exports = { 'ineq-e1': two, 'ineq-e2': two, 'ineq-m1': two, 'ineq-m2': two, 'ineq-h1': two, 'ineq-h2': three,
  'ineq-e3': p => { const T = targets(p.question); return safe(o => { const C = closure(chainRel(o.label)); return T.every(t => sure(C, t)); }); },
  'ineq-h3': p => { const T = targets(p.question); return safe(o => { const C = closure(chainRel(o.label)); return T.every(t => sure(C, t)); }); },
  'ineq-m3': p => { const m = p.question.match(/blanks in "(.+)" so that both (\w) (\S) (\w) and (\w) (\S) (\w) are/); const T = [[m[2], m[3], m[4]], [m[5], m[6], m[7]]];
    return safe(o => { const f = o.label.split(', '); let i = 0; const chain = m[1].replace(/__/g, () => f[i++]); if (i !== f.length) throw new Error('blank count'); const C = closure(chainRel(chain)); return T.every(t => sure(C, t)); }); } };
