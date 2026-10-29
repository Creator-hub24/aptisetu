/* Independent puzzle solver: parses the intro, every clue sentence and the question text, then brute-forces
   placements (and attribute assignments) to check there is exactly one arrangement. */
const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const MON = ['March', 'June', 'September'];
const ordv = s => +s.replace(/\D/g, '');
function setup(intro) {
  const P = intro.match(/, ((?:[A-H], )+[A-H]),/)[1].split(', ');
  let dom, S, flats = false;
  if (/West flat/.test(intro)) { dom = 'floor'; S = 8; flats = true; }
  else if (/boxes/.test(intro)) { dom = 'box'; S = P.length; }
  else if (/lecture/.test(intro)) { dom = 'day'; S = /Monday to Friday/.test(intro) ? 5 : 7; }
  else if (/exams/.test(intro)) { dom = 'month'; S = 6; }
  else { dom = 'floor'; S = /8-storey/.test(intro) ? 8 : 5; }
  const am = intro.match(/Each (?:likes|takes) a different \w+: ([^.]+)\./); const AV = am ? am[1].split(', ') : null;
  const lv = s => (flats ? s >> 1 : s), side = s => (flats ? s & 1 : 0), L = flats ? 4 : S;
  const slotName = s => dom === 'floor' ? (flats ? `Floor ${(s >> 1) + 1}, ${s & 1 ? 'East' : 'West'} flat` : `Floor ${s + 1}`) : dom === 'box' ? `Position ${s + 1} from the bottom` : dom === 'day' ? DAYS[s] : `${MON[s >> 1]} ${s % 2 ? 21 : 8}`;
  return { P, dom, S, flats, AV, lv, side, L, slotName };
}
function parseSlot(G, txt) { // "floor 3", "Wednesday", "June 21", "position 2 from the bottom"
  let m; if ((m = txt.match(/^floor (\d+)$/))) return +m[1] - 1; if (DAYS.includes(txt)) return DAYS.indexOf(txt);
  if ((m = txt.match(/^(March|June|September) (8|21)$/))) return MON.indexOf(m[1]) * 2 + (m[2] === '21' ? 1 : 0);
  if ((m = txt.match(/^position (\d+) from the bottom$/))) return +m[1] - 1; throw new Error('slot ' + txt); }
function clue(G, c) {
  const I = x => { const i = G.P.indexOf(x); if (i < 0) throw new Error('who ' + x); return i; }, V = v => { const i = G.AV.indexOf(v); if (i < 0) throw new Error('val ' + v); return i; };
  const { lv, side, L } = G; const occ = (p, s) => p.includes(s); const gap = (p, a, b) => Math.abs(lv(p[a]) - lv(p[b])) - 1; let m;
  const R = (re) => (m = c.match(re));
  // ---- placement clues
  if (R(/^(?:Box )?(\w) (?:lives on|is) (floor \d+)\.$/) || R(/^(\w)'s (?:lecture|exam) is on ((?:\w+day)|(?:\w+ (?:8|21)))\.$/)) { const x = I(m[1]), s = parseSlot(G, m[2]); return { f: p => p[x] === s }; }
  if (R(/^Box (\w) is (\d+\w\w) from the bottom\.$/)) { const x = I(m[1]), s = ordv(m[2]) - 1; return { f: p => p[x] === s }; }
  if (R(/^Box (\w) is not (\d+\w\w) from the bottom\.$/)) { const x = I(m[1]), s = ordv(m[2]) - 1; return { f: p => p[x] !== s }; }
  if (R(/^(\w) does not live on floor (\d+)\.$/)) { const x = I(m[1]), z = +m[2] - 1; return { f: p => lv(p[x]) !== z }; }
  if (R(/^(\w)'s (?:lecture|exam) is not on ((?:\w+day)|(?:\w+ (?:8|21)))\.$/)) { const x = I(m[1]), s = parseSlot(G, m[2]); return { f: p => p[x] !== s }; }
  if (R(/^(?:Box )?(\w)(?:'s lecture)? (?:lives on|is at|is on) an (odd|even)-numbered (?:floor|position from the bottom|day of the week \(Monday = 1\))\.$/)) { const x = I(m[1]), par = m[2] === 'odd' ? 1 : 0; return { f: p => (lv(p[x]) + 1) % 2 === par }; }
  if (R(/^(\w)'s exam is on the (8th|21st) of a month\.$/)) { const x = I(m[1]), r = m[2] === '21st' ? 1 : 0; return { f: p => p[x] % 2 === r }; }
  if (R(/^(\w) lives on the top floor\.$/) || R(/^Box (\w) is at the top of the stack\.$/) || R(/^(\w)'s lecture is the last day of the schedule\.$/) || R(/^(\w) has the last exam\.$/)) { const x = I(m[1]); return { f: p => lv(p[x]) === L - 1 }; }
  if (R(/^(\w) lives on the bottom floor\.$/) || R(/^Box (\w) is at the bottom of the stack\.$/) || R(/^(\w)'s lecture is on the first day of the schedule\.$/) || R(/^(\w) has the first exam\.$/)) { const x = I(m[1]); return { f: p => lv(p[x]) === 0 }; }
  if (R(/^(\w) lives in the flat directly above (\w)'s flat\.$/)) { const x = I(m[1]), y = I(m[2]); return { f: p => lv(p[x]) - lv(p[y]) === 1 && side(p[x]) === side(p[y]) }; }
  if (R(/^(\w) lives immediately above (\w)\.$/) || R(/^Box (\w) is placed immediately above box (\w)\.$/) || R(/^(\w)'s lecture is the day immediately after (\w)'s\.$/) || R(/^(\w)'s exam is immediately after (\w)'s\.$/)) {
    if (G.flats) throw new Error('ambiguous flats adj'); const x = I(m[1]), y = I(m[2]); return { f: p => p[x] - p[y] === 1 }; }
  if (R(/^(\w) lives somewhere above (\w)\.$/) || R(/^(\w) lives on a floor somewhere above (\w)'s floor\.$/) || R(/^Box (\w) is somewhere above box (\w)\.$/) || R(/^(\w)'s lecture is on some day after (\w)'s\.$/) || R(/^(\w)'s exam is some time after (\w)'s\.$/)) {
    if (G.flats && !/a floor somewhere/.test(c)) throw new Error('ambiguous flats above'); const x = I(m[1]), y = I(m[2]); return { f: p => lv(p[x]) > lv(p[y]) }; }
  if (R(/^Exactly (\d+) (?:floors? (?:is|are) between the floors of|box(?:es)? (?:is|are) placed between box|days? falls? between the lectures of|exams? (?:is|are) held between the exams of) (\w) and (?:box )?(\w)\.$/)) { const w = +m[1], x = I(m[2]), y = I(m[3]); return { f: p => gap(p, x, y) === w }; }
  if (R(/^The floor immediately below (\w)'s floor is vacant\.$/) || R(/^No lecture is held on the day just before (\w)'s\.$/)) { const x = I(m[1]); return { f: p => p[x] > 0 && !occ(p, p[x] - 1) }; }
  if (R(/^(\w) and (\w) live on the same floor\.$/)) { const x = I(m[1]), y = I(m[2]); return { f: p => lv(p[x]) === lv(p[y]) }; }
  if (R(/^(\w) and (\w) have exams in the same month\.$/)) { const x = I(m[1]), y = I(m[2]); return { f: p => p[x] >> 1 === p[y] >> 1 }; }
  if (R(/^(\w) lives in the (East|West) flat\.$/)) { const x = I(m[1]), sd = m[2] === 'East' ? 1 : 0; return { f: p => side(p[x]) === sd }; }
  if (R(/^(\w)'s exam is in (March|June|September)\.$/)) { const x = I(m[1]), mo = MON.indexOf(m[2]); return { f: p => p[x] >> 1 === mo }; }
  // ---- attribute clues
  if (R(/^(\w) (?:likes|eats|takes) (\w+)\.$/)) { const x = I(m[1]), v = V(m[2]); return { A: 1, f: (p, a) => a[x] === v }; }
  if (R(/^(\w) does not (?:like|eat|take) (\w+)\.$/)) { const x = I(m[1]), v = V(m[2]); return { A: 1, f: (p, a) => a[x] !== v }; }
  const who = v => (p, a) => p[a.indexOf(V(v))];
  if (R(/^The (?:person who likes|one who eats) (\w+) lives immediately above (\w)\.$/) || R(/^The lecture of the person who likes (\w+) is the day immediately after (\w)'s\.$/) || R(/^The one who eats (\w+) has a lecture the day after (\w)\.$/) || R(/^The (\w+) (?:exam|lecture) is (?:immediately after|the day immediately after) (\w)'s\.$/) || R(/^The person who likes (\w+) has the exam immediately after (\w)'s\.$/) || R(/^The one who eats (\w+) has the exam right after (\w)'s\.$/)) {
    const W = who(m[1]), y = I(m[2]); return { A: 1, f: (p, a) => lv(W(p, a)) - lv(p[y]) === 1 }; }
  if (R(/^Exactly (\d+) (?:floor|day|date)s? (?:is|are) between (\w)(?:'s)? and the (?:person who likes |one who eats )?(\w+)(?: exam| lecture)?\.$/)) { const w = +m[1], y = I(m[2]), W = who(m[3]); return { A: 1, f: (p, a) => Math.abs(lv(W(p, a)) - lv(p[y])) - 1 === w }; }
  if (R(/^The (?:person who likes|one who eats) (\w+) is on (.+)\.$/) || R(/^The (\w+) (?:exam|lecture) is on (.+)\.$/)) { const W = who(m[1]), s = parseSlot(G, m[2]); return { A: 1, f: (p, a) => W(p, a) === s }; }
  throw new Error('unparsed clue: ' + c);
}
function places(n, S) { const out = [], cur = [], used = Array(S).fill(0); (function bt(i) { if (i === n) { out.push(cur.slice()); return; } for (let s = 0; s < S; s++) if (!used[s]) { used[s] = 1; cur[i] = s; bt(i + 1); used[s] = 0; } })(0); return out; }
function solve(p) {
  const G = setup(p.intro); const C = p.clues.map(c => clue(G, c)); const n = G.P.length;
  const base = places(n, G.S).filter(pl => C.every(c => c.A || c.f(pl)));
  let sols = base.map(pl => ({ p: pl, a: null }));
  if (G.AV) { const AP = places(n, n); sols = []; base.forEach(pl => AP.forEach(a => { if (C.every(c => !c.A || c.f(pl, a))) sols.push({ p: pl, a }); })); }
  if (sols.length !== 1) throw new Error('arrangements: ' + sols.length); return { G, s: sols[0] };
}
module.exports = {};
for (const id of ['puz-e1', 'puz-e2', 'puz-e3', 'puz-m1', 'puz-m2', 'puz-m3', 'puz-h1', 'puz-h2', 'puz-h3']) module.exports[id] = p => {
  const { G, s } = solve(p); const q = p.ask; let m; const box = G.dom === 'box' ? 'Box ' : '';
  if ((m = q.match(/^Who is on (.+)\?$/))) { const sl = parseSlot(G, m[1]); return G.P[s.p.indexOf(sl)]; }
  if ((m = q.match(/^Which box is (\d+\w\w) from the bottom\?$/))) return 'Box ' + G.P[s.p.indexOf(ordv(m[1]) - 1)];
  if ((m = q.match(/^Who lives in the Floor (\d), (East|West) flat\?$/))) return G.P[s.p.indexOf((+m[1] - 1) * 2 + (m[2] === 'East' ? 1 : 0))];
  if ((m = q.match(/^Where is (\w)\?$/)) || (m = q.match(/^What is box (\w)'s position from the bottom\?$/))) return G.slotName(s.p[G.P.indexOf(m[1])]);
  if ((m = q.match(/^What is (\w)'s \w+\?$/))) return G.AV[s.a[G.P.indexOf(m[1])]];
  if (/^Which (?:days have no lecture|floors are vacant)\?$/.test(q)) return [...Array(G.S).keys()].filter(k => !s.p.includes(k)).map(G.slotName).join(' and ');
  if ((m = q.match(/^How many (?:boxes|people) are between (?:box )?(\w) and (?:box )?(\w)\?$/))) { const a = G.lv(s.p[G.P.indexOf(m[1])]), b = G.lv(s.p[G.P.indexOf(m[2])]);
    return String(s.p.filter(z => G.lv(z) > Math.min(a, b) && G.lv(z) < Math.max(a, b)).length); }
  throw new Error('ask? ' + q);
};
