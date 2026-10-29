/* Independent DILR solver: every set is brute-forced from the text (round robins, brackets, logic grids). */
const T = ['P', 'Q', 'R', 'S', 'T', 'U'];
const pairs = n => { const o = []; for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) o.push([i, j]); return o; };
function* outcomes(m, base) { const o = new Array(m).fill(0); const tot = base ** m; for (let x = 0; x < tot; x++) { let y = x; for (let i = 0; i < m; i++) { o[i] = y % base; y = Math.floor(y / base); } yield o; } }
const pts = (n, pr, o, W) => { const s = new Array(n).fill(0); pr.forEach(([a, b], k) => { if (o[k] === 0) s[a] += W; else if (o[k] === 1) s[b] += W; else { s[a] += 1; s[b] += 1; } }); return s; };
const perms = a => a.length <= 1 ? [a] : a.flatMap((x, i) => perms(a.slice(0, i).concat(a.slice(i + 1))).map(r => [x].concat(r)));
const one = (set, what) => { const s = [...new Set(set)]; if (s.length !== 1) throw new Error(what + ' not unique: ' + s); return s[0]; };
// ---- logic grid
const PHR = { city: { is: /^is from (\w+)$/, the: /^the person from (\w+)$/ }, job: { is: /^is the (\w+)$/, the: /^the (\w+)$/ }, drink: { is: /^drinks (\w+)$/, the: /^the (\w+) drinker$/ } };
function grid(p) { const m = p.question.match(/^(.+?) each have a different (.+?) \((.+)\)\.$/); const people = m[1].split(', '); const names = m[2].split(' and a different '); const vals = m[3].split('; ').map(s => s.split('/'));
  const attrOfVal = v => { const a = vals.findIndex(vs => vs.includes(v)); if (a < 0) throw new Error('val ' + v); return a; };
  const parsePred = s => { s = s.replace(/^The /, 'the '); for (const nm of names) { const r = PHR[nm]; let mm; if ((mm = s.match(r.is))) { const a = names.indexOf(nm); if (!vals[a].includes(mm[1])) throw new Error('v'); return { a, v: mm[1] }; } } return null; };
  const parseThe = s => { s = s.charAt(0).toLowerCase() + s.slice(1); for (const nm of names) { const mm = s.match(PHR[nm].the); if (mm && vals[names.indexOf(nm)].includes(mm[1])) return { a: names.indexOf(nm), v: mm[1] }; } return null; };
  const tests = p.clues.map(c => { c = c.replace(/\.$/, ''); let mm; const P = people.find(x => c.startsWith(x + ' '));
    if (P) { const rest = c.slice(P.length + 1); const pi = people.indexOf(P);
      if ((mm = rest.match(/^either (.+) or (.+)$/))) { const A = parsePred(mm[1]), B = parsePred(mm[2]); return W => W[A.a][pi] === A.v || W[B.a][pi] === B.v; }
      const neg = rest.replace(/^is not /, 'is ').replace(/^does not drink /, 'drinks '); const A = parsePred(neg); if (!A) throw new Error('clue ' + c); const isNeg = neg !== rest; return W => (W[A.a][pi] === A.v) !== isNeg; }
    // "<The X> <pred>" — split at the verb
    mm = c.match(/^(.+?) ((?:is|drinks|does) .+)$/); const S = parseThe(mm[1]); const rest = mm[2]; const neg = rest.replace(/^is not /, 'is ').replace(/^does not drink /, 'drinks '); const B = parsePred(neg); if (!S || !B) throw new Error('clue ' + c);
    const isNeg = neg !== rest; return W => { const who = W[S.a].indexOf(S.v); return (W[B.a][who] === B.v) !== isNeg; }; });
  const ask = p.ask; let af; let mm;
  if ((mm = ask.match(/^What is (\w+)'s (\w+)\?$/))) { const pi = people.indexOf(mm[1]), a = names.indexOf(mm[2]); af = W => W[a][pi]; }
  else if ((mm = ask.match(/^Who (.+)\?$/))) { const A = parsePred(mm[1]); af = W => people[W[A.a].indexOf(A.v)]; }
  const PV = vals.map(vs => perms(vs)); const res = []; const rec = (i, W) => { if (i === vals.length) { if (tests.every(t => t(W))) res.push(af(W)); return; } for (const pv of PV[i]) rec(i + 1, W.concat([pv])); }; rec(0, []);
  if (!res.length) throw new Error('no world'); return one(res, 'grid answer'); }
// ---- knockout bracket simulator (own)
function brackets() { const out = []; for (let x = 0; x < 128; x++) { let field = [1, 8, 4, 5, 2, 7, 3, 6]; let bit = 0; const lost = {}; let upsets = 0; const stageNames = ['round 1', 'the semi-finals', 'the final'];
    for (let r = 0; field.length > 1; r++) { const nx = []; for (let i = 0; i < field.length; i += 2) { const a = field[i], b = field[i + 1]; const w = (x >> bit++) & 1 ? b : a; const l = w === a ? b : a; if (w > l) upsets++; lost[l] = stageNames[r]; nx.push(w); } field = nx; }
    const champ = field[0]; const runner = +Object.keys(lost).find(k => lost[k] === 'the final'); out.push({ champ, runner, lost, upsets }); } return out; }
const BR = brackets();
function ko(p) { const fs = p.clues.map(c => { let m;
    if ((m = c.match(/^Exactly (\d+) match(?:es)? ended in an upset/))) { const v = +m[1]; return B => B.upsets === v; }
    if ((m = c.match(/^The champion's seed number is (odd|even)\.$/))) { const odd = m[1] === 'odd'; return B => (B.champ % 2 === 1) === odd; }
    if ((m = c.match(/^Seed (\d) won the tournament\.$/))) { const s = +m[1]; return B => B.champ === s; }
    if ((m = c.match(/^Seed (\d) lost in (round 1|the semi-finals|the final)\.$/))) { const s = +m[1], st = m[2]; return B => B.lost[s] === st; }
    throw new Error('ko clue ' + c); });
  const live = BR.filter(B => fs.every(f => f(B))); if (!live.length) throw new Error('no bracket');
  return 'Seed ' + one(live.map(B => p.ask === 'Who won the tournament?' ? B.champ : B.runner), 'ko'); }
module.exports = {
  'dl-e1': p => { const q = p.question; const n = +q.match(/^(\d+) teams/)[1]; const given = [...q.match(/Wins: (.+)\. How/)[1].matchAll(/(\w): (\d+)/g)]; const x = q.match(/did (\w) win/)[1];
    if (given.length !== n - 1 || given.some(g => g[1] === x)) throw new Error('parse');
    const pr = pairs(n); const xi = T.indexOf(x); const res = []; for (const o of outcomes(pr.length, 2)) { const s = pts(n, pr, o, 1); if (given.every(g => s[T.indexOf(g[1])] === +g[2])) res.push(s[xi]); } return String(one(res, 'wins')); },
  'dl-e2': p => { const q = p.question; const n = +q.match(/^(\d+) players/)[1]; let size = 1; while (size < n) size *= 2; const byes = size - n; // simulate
    let players = n, matches = 0, rounds = 0; let r1 = true; while (players > 1) { const playing = r1 ? players - byes : players; const m = playing / 2; if (!Number.isInteger(m)) throw new Error('odd'); matches += m; players -= m; rounds++; r1 = false; }
    if (/byes are given/.test(q)) return String(byes); if (/matches are played/.test(q)) return String(matches); if (/rounds are needed/.test(q)) return String(rounds); throw new Error('q'); },
  'dl-e3': grid, 'dl-m1': grid, 'dl-h3': grid,
  'dl-m2': p => { const q = p.question; const W = +q.match(/A win earns (\d) points/)[1]; const P = [...q.match(/Final points: (.+)\.$/)[1].matchAll(/(\w) (\d+)/g)].map(m => +m[2]); const n = 4, pr = pairs(n);
    let f; let m; if (p.ask === 'How many matches ended in a draw?') f = o => String(o.filter(x => x === 2).length);
    else if ((m = p.ask.match(/^What was the result of (\w) vs (\w)\?$/))) { const k = pr.findIndex(([a, b]) => a === T.indexOf(m[1]) && b === T.indexOf(m[2])); f = o => o[k] === 0 ? `${m[1]} won` : o[k] === 1 ? `${m[2]} won` : 'Draw'; }
    const res = []; for (const o of outcomes(6, 3)) { const s = pts(n, pr, o, W); if (s.every((v, i) => v === P[i])) res.push(f(o)); } return one(res, 'm2'); },
  'dl-m3': ko,
  'dl-h1': p => { const q = p.question; const n = +q.match(/^(\d) teams/)[1], W = +q.match(/A win earns (\d) points/)[1], draws = !/there are no draws/.test(q); const k = +p.ask.match(/(?:at least|fewer than) (\d) teams/)[1]; const pr = pairs(n);
    const maxOut = /^What is the maximum/.test(p.ask); let best = null; for (const o of outcomes(pr.length, draws ? 3 : 2)) { const s = pts(n, pr, o, W); const above = s.filter(v => v > s[0]).length;
      if (maxOut ? above >= k : above < k) best = best === null ? s[0] : (maxOut ? Math.max(best, s[0]) : Math.min(best, s[0])); } if (best === null) throw new Error('none'); return String(best); },
  'dl-h2': p => { const w = [...p.question.match(/Wins: (.+)\.$/)[1].matchAll(/(\w) (\d)/g)].map(m => +m[2]); const n = 5, pr = pairs(n);
    const facts = p.clues.map(c => { const m = c.match(/^(\w) beat (\w)\.$/); return [T.indexOf(m[1]), T.indexOf(m[2])]; }); const m = p.ask.match(/^(\w) (lost|won) exactly one match/); const t = T.indexOf(m[1]), lost = m[2] === 'lost';
    const beat = (o, a, b) => { const k = pr.findIndex(([x, y]) => (x === a && y === b) || (x === b && y === a)); return pr[k][0] === a ? o[k] === 0 : o[k] === 1; };
    const res = []; for (const o of outcomes(10, 2)) { if (!pts(n, pr, o, 1).every((v, i) => v === w[i])) continue; if (!facts.every(([a, b]) => beat(o, a, b))) continue;
      const others = [0, 1, 2, 3, 4].filter(i => i !== t); const hit = others.filter(i => lost ? beat(o, i, t) : beat(o, t, i)); if (hit.length !== 1) throw new Error('premise'); res.push(T[hit[0]]); }
    return one(res, 'h2'); },
};
