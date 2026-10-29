/* Independent syllogism solver: parses statement text, enumerates every "world" = set of inhabited
   membership profiles (each term non-empty), and judges conclusions semantically. */
function parse(s) { let m;
  if ((m = s.match(/^All (\w+) being (\w+) is a possibility\.$/))) return { q: 'pall', x: m[1], y: m[2] };
  if ((m = s.match(/^Some (\w+) being (\w+) is a possibility\.$/))) return { q: 'psome', x: m[1], y: m[2] };
  if ((m = s.match(/^All (\w+) are (\w+)\.$/))) return { q: 'all', x: m[1], y: m[2] };
  if ((m = s.match(/^Some (\w+) are not (\w+)\.$/))) return { q: 'somenot', x: m[1], y: m[2] };
  if ((m = s.match(/^Some (\w+) are (\w+)\.$/))) return { q: 'some', x: m[1], y: m[2] };
  if ((m = s.match(/^Only a few (\w+) are (\w+)\.$/))) return { q: 'few', x: m[1], y: m[2] };
  if ((m = s.match(/^No (\w+) is a (\w+)\.$/))) return { q: 'no', x: m[1] + 's', y: m[2] + 's' };
  throw new Error('cannot parse: ' + s); }
const WC = {};
function worlds(terms) { if (WC[terms.length]) return WC[terms.length]; const k = terms.length, prof = []; for (let i = 1; i < 1 << k; i++) prof.push(i); const out = [];
  for (let w = 1; w < 1 << prof.length; w++) { const inh = prof.filter((_, j) => w >> j & 1); if (terms.every((_, t) => inh.some(pf => pf >> t & 1))) out.push(inh); } return (WC[terms.length] = out); }
function truth(world, terms, st) { const X = 1 << terms.indexOf(st.x), Y = 1 << terms.indexOf(st.y); if (X < 1 || Y < 1) throw new Error('unknown term');
  const both = world.some(p => p & X && p & Y), only = world.some(p => p & X && !(p & Y));
  return { all: !only, no: !both, some: both, somenot: only, few: both && only, pall: !only, psome: both }[st.q]; }
function analyse(stmtTexts, conclTexts) { const S = stmtTexts.map(parse), C = conclTexts.map(parse); const terms = [...new Set(S.flatMap(s => [s.x, s.y]))];
  C.forEach(c => [c.x, c.y].forEach(t => { if (!terms.includes(t)) terms.push(t); }));
  const W = worlds(terms).filter(w => S.every(s => truth(w, terms, s))); if (!W.length) throw new Error('inconsistent statements');
  const res = C.map(c => { const n = W.filter(w => truth(w, terms, c)).length;
    if (c.q[0] === 'p') { if (n === W.length) throw new Error('possibility is certain (ambiguous by convention)'); return { follows: n > 0, c }; }
    return { follows: n === W.length, c }; });
  return { W, terms, res, C };
}
const split = p => ({ st: p.clues.filter(c => !/^Conclusion/.test(c)), cs: p.clues.filter(c => /^Conclusion/.test(c)).map(c => c.replace(/^Conclusion \w+: /, '')) });
function two(p) { const { st, cs } = split(p); const A = analyse(st, cs); const [a, b] = A.res;
  if (a.follows && b.follows) return 'Both I and II follow'; if (a.follows) return 'Only I follows'; if (b.follows) return 'Only II follows';
  // either-or: both categorical, and in every world exactly one is true
  if (a.c.q[0] !== 'p' && b.c.q[0] !== 'p' && A.W.every(w => truth(w, A.terms, a.c) !== truth(w, A.terms, b.c))) return 'Either I or II follows';
  return 'Neither I nor II follows'; }
function three(p) { const { st, cs } = split(p); const f = analyse(st, cs).res.map(r => r.follows); const R = ['I', 'II', 'III'].filter((_, i) => f[i]);
  if (!R.length) return 'None follows'; if (R.length === 3) return 'All I, II and III follow'; if (R.length === 1) return `Only ${R[0]} follows`; return `Only ${R[0]} and ${R[1]} follow`; }
module.exports = { 'syl-e1': two, 'syl-e3': two, 'syl-m1': two, 'syl-m2': two, 'syl-m3': two, 'syl-h1': two, 'syl-h3': three,
  'syl-e2': p => o => { const A = analyse(p.clues, [o.label]); return A.res[0].follows; },
  'syl-h2': p => { const cs = p.clues.map(c => c.replace(/^Conclusion \w+: /, ''));
    return o => { const st = o.label.match(/[^.]+\./g).map(s => s.trim()); const A = analyse(st, cs); return A.res.every(r => r.follows); }; } };
