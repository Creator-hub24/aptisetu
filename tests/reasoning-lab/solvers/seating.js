/* Independent seating solver: people get real 2D seats and facing vectors; "right" = facing rotated clockwise.
   Every arrangement (and facing pattern) is enumerated; all survivors must give the same answer. */
const ORD = { first: 1, second: 2, third: 3, fourth: 4, fifth: 5, sixth: 6, seventh: 7, eighth: 8 };
function perms(a) { if (a.length <= 1) return [a]; return a.flatMap((x, i) => perms(a.slice(0, i).concat(a.slice(i + 1))).map(r => [x].concat(r))); }
function layout(q) { let m;
  if ((m = q.match(/^(\d+) people (.+?) sit in a straight row(\. Some face north and some face south|, all facing north)\./))) return { kind: 'line', n: +m[1], names: m[2].split(', '), mixed: /Some face/.test(m[3]) };
  if ((m = q.match(/^(\d+) people (.+?) sit around a circular table, all facing the centre\./))) return { kind: 'circle', n: +m[1], names: m[2].split(', ') };
  if ((m = q.match(/^(\d+) people (.+?) sit in two parallel rows of (\d+)\. People in Row 1 face south and people in Row 2 face north/))) return { kind: 'rows', n: +m[1], names: m[2].split(', '), m: +m[3] };
  throw new Error('layout'); }
// seats: {p:[x,y], f:[fx,fy], row}
function seats(L, faceBits) { const S = [];
  if (L.kind === 'line') for (let i = 0; i < L.n; i++) S.push({ p: [i, 0], row: 0 });
  if (L.kind === 'circle') for (let i = 0; i < L.n; i++) { const a = 2 * Math.PI * i / L.n; S.push({ p: [Math.cos(a), Math.sin(a)], f: [-Math.cos(a), -Math.sin(a)], row: 0 }); }
  if (L.kind === 'rows') { for (let i = 0; i < L.m; i++) S.push({ p: [i, 1], f: [0, -1], row: 1 }); for (let i = 0; i < L.m; i++) S.push({ p: [i, 0], f: [0, 1], row: 2 }); }
  return S; }
const right = f => [f[1], -f[0]];
function makeWorld(L, assign, face) { // assign[person] = seat index; face[person] = 'N'|'S' (line only)
  const S = seats(L); const who = new Array(S.length); assign.forEach((s, p) => who[s] = p);
  const fOf = p => L.kind === 'line' ? (L.mixed && face[p] === 'S' ? [0, -1] : [0, 1]) : S[assign[p]].f;
  // k-th seat to the given side of person p; null if it runs out of seats
  const step = (p, dir, k) => { const f = fOf(p), r = right(f), d = dir === 'right' ? r : [-r[0], -r[1]]; let s = assign[p];
    if (L.kind === 'circle') { // pick the neighbouring seat that lies on side d, then keep going round the same way
      const n = L.n, nb = [(s + 1) % n, (s - 1 + n) % n]; const v = t => (S[t].p[0] - S[s].p[0]) * d[0] + (S[t].p[1] - S[s].p[1]) * d[1]; const inc = v(nb[0]) > 0 ? 1 : -1; return who[((s + inc * k) % n + n) % n]; }
    const x = S[s].p[0] + d[0] * k, y = S[s].p[1]; const t = S.findIndex(z => Math.abs(z.p[0] - x) < 1e-9 && z.p[1] === y); return t < 0 ? null : who[t]; };
  const across = p => { const s = assign[p]; if (L.kind === 'circle') return who[(s + L.n / 2) % L.n]; const t = S.findIndex(z => z.p[0] === S[s].p[0] && z.row !== S[s].row); return who[t]; };
  const isEnd = p => { const s = S[assign[p]]; const same = S.filter(z => z.row === s.row).map(z => z.p[0]); return s.p[0] === Math.min(...same) || s.p[0] === Math.max(...same); };
  const adj = (a, b) => { if (L.kind === 'circle') { const d = Math.abs(assign[a] - assign[b]); return d === 1 || d === L.n - 1; } const A = S[assign[a]], B = S[assign[b]]; return A.row === B.row && Math.abs(A.p[0] - B.p[0]) === 1; };
  const x = p => S[assign[p]].p[0], row = p => S[assign[p]].row;
  return { step, across, isEnd, adj, x, row, who, S, face, fOf };
}
function clueFn(L, txt) { const I = nm => { const i = L.names.indexOf(nm); if (i < 0) throw new Error('name ' + nm); return i; }; let m;
  const rel = s => { const mm = s.match(/^(immediately|(\w+)) to the (left|right) of$/); const k = mm[1] === 'immediately' ? 1 : ORD[mm[2]]; if (!k) throw new Error('ord ' + s); return { k, dir: mm[3] }; };
  if ((m = txt.match(/^(\w) sits at one of the ends( of a row)?\.$/))) { const a = I(m[1]); return W => W.isEnd(a); }
  if ((m = txt.match(/^(\w) does not sit at an end( of a row)?\.$/))) { const a = I(m[1]); return W => !W.isEnd(a); }
  if ((m = txt.match(/^(\w) sits (\w+) from the (left|west) end\.$/))) { const a = I(m[1]), k = ORD[m[2]]; return W => W.x(a) === k - 1; }
  if ((m = txt.match(/^(\w) sits exactly in the middle of the row\.$/))) { const a = I(m[1]); return W => W.x(a) === (L.n - 1) / 2; }
  if ((m = txt.match(/^(\w) sits somewhere to the (left|right) of (\w)\.$/))) { const a = I(m[1]), b = I(m[3]), dir = m[2]; if (L.mixed) throw new Error('somewhere+mixed'); return W => dir === 'right' ? W.x(a) > W.x(b) : W.x(a) < W.x(b); }
  if ((m = txt.match(/^(\w) sits (.+?) the person who (faces|sits opposite) (\w)\.$/))) { const a = I(m[1]), r = rel(m[2]), b = I(m[4]); return W => { const o = W.across(b); return o !== a && W.step(o, r.dir, r.k) === a; }; }
  if ((m = txt.match(/^(\w) sits (.+?) (\w)\.$/)) && /to the (left|right) of$/.test(m[2])) { const a = I(m[1]), r = rel(m[2]), b = I(m[3]); return W => W.step(b, r.dir, r.k) === a; }
  if ((m = txt.match(/^(\w) is an immediate neighbour of (\w)\.$/))) { const a = I(m[1]), b = I(m[2]); return W => W.adj(a, b); }
  if ((m = txt.match(/^(\w) is not an immediate neighbour of (\w)\.$/))) { const a = I(m[1]), b = I(m[2]); return W => !W.adj(a, b); }
  if ((m = txt.match(/^Exactly (\d+) (?:person sits|people sit) between (\w) and (\w)\.$/))) { const k = +m[1], a = I(m[2]), b = I(m[3]); if (L.kind !== 'line') throw new Error('between'); return W => Math.abs(W.x(a) - W.x(b)) - 1 === k; }
  if ((m = txt.match(/^(\w) (faces|sits directly opposite) (\w)\.$/))) { const a = I(m[1]), b = I(m[3]); return W => W.across(b) === a; }
  if ((m = txt.match(/^(\w) faces (north|south)\.$/))) { const a = I(m[1]), f = m[2] === 'north' ? 'N' : 'S'; return W => W.face[a] === f; }
  if ((m = txt.match(/^(\w) and (\w) face (the same|opposite) directions?\.$/))) { const a = I(m[1]), b = I(m[2]), same = m[3] === 'the same'; return W => (W.face[a] === W.face[b]) === same; }
  if ((m = txt.match(/^(\w) sits in Row (\d)\.$/))) { const a = I(m[1]), r = +m[2]; return W => W.row(a) === r; }
  throw new Error('clue? ' + txt); }
function answerFn(L, ask) { const I = nm => L.names.indexOf(nm); const nm = p => p === null || p === undefined ? null : L.names[p]; let m;
  if ((m = ask.match(/^Who sits (immediately|\w+) to the (left|right) of (\w)\?$/))) { const k = m[1] === 'immediately' ? 1 : ORD[m[1]], dir = m[2], x = I(m[3]); return W => nm(W.step(x, dir, k)); }
  if ((m = ask.match(/^How many people sit between (\w) and (\w)\?$/))) { const a = I(m[1]), b = I(m[2]); return W => String(Math.abs(W.x(a) - W.x(b)) - 1); }
  if ((m = ask.match(/^Who sits (\w+) from the (left|west) end\?$/))) { const k = ORD[m[1]]; return W => nm(W.who[W.S.findIndex(s => s.p[0] === k - 1)]); }
  if ((m = ask.match(/^Who (faces|sits directly opposite) (\w)\?$/))) { const x = I(m[2]); return W => nm(W.across(x)); }
  if (ask === 'How many people face north?') return W => String(W.face.filter(f => f === 'N').length);
  if (ask === 'Which pair sits at the two ends of the row?') return W => [W.who[0], W.who[L.n - 1]].map(nm).sort().join(' and ');
  if (ask === 'Which two people sit at the ends of Row 1?') return W => { const r1 = W.S.map((s, i) => i).filter(i => W.S[i].row === 1); const xs = r1.map(i => W.S[i].p[0]); const e = [r1[xs.indexOf(Math.min(...xs))], r1[xs.indexOf(Math.max(...xs))]]; return e.map(i => nm(W.who[i])).sort().join(' and '); };
  throw new Error('ask? ' + ask); }
function solve(p) { const L = layout(p.question); const ask = p.question.slice(p.question.lastIndexOf('. ') + 2); const fs = p.clues.map(c => clueFn(L, c)); const af = answerFn(L, ask);
  const people = [...Array(L.n).keys()]; const answers = new Set(); let count = 0;
  const seatPerms = L.kind === 'circle' ? perms(people.slice(1)).map(r => [0].concat(r)) : perms(people); // circle: rotations are the same table
  const faceSets = L.mixed ? [...Array(1 << L.n).keys()].map(b => people.map(i => (b >> i) & 1 ? 'S' : 'N')) : [people.map(() => 'N')];
  for (const sp of seatPerms) { const assign = sp; for (const face of faceSets) { const W = makeWorld(L, assign, face); if (fs.every(f => f(W))) { count++; answers.add(af(W)); } } }
  if (!count) throw new Error('no arrangement fits'); if (answers.size !== 1) throw new Error('answer not unique: ' + [...answers]); const a = [...answers][0]; if (a === null) throw new Error('null answer'); return a; }
module.exports = Object.fromEntries(['seat-e1', 'seat-e2', 'seat-e3', 'seat-m1', 'seat-m2', 'seat-m3', 'seat-h1', 'seat-h2', 'seat-h3'].map(id => [id, solve]));
