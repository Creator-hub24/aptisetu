/* Topic: Seating arrangement — linear, circular, parallel rows, mixed facing. Clues narrowed by full enumeration. */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample, perms, range } = RL.u;
  RL.topic('seating', 'Seating Arrangement', '🪑', 'Linear, circular and two-row seating. Watch each clue knock out possibilities until one arrangement is left.', 'Arrangements & Puzzles');
  const ORD = ['', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth'];
  const md = (a, n) => ((a % n) + n) % n;
  // layout: {kind:'linear'|'circle'|'rows', n, m(rows per side), mixed}
  function seatOf(L, c, p, dir, k) { // seat k places to `dir` ('right'|'left') of person p, or -1
    const s = c.pos[p];
    if (L.kind === 'linear') { const f = L.mixed && c.face[p] ? -1 : 1; const t = s + (dir === 'right' ? k : -k) * f; return t >= 0 && t < L.n ? t : -1; }
    if (L.kind === 'circle') return md(s + (dir === 'right' ? -k : k), L.n);
    const row = s < L.m ? 0 : 1, j = s % L.m; const f = row === 0 ? -1 : 1; const t = j + (dir === 'right' ? k : -k) * f; return t >= 0 && t < L.m ? row * L.m + t : -1;
  }
  const isEnd = (L, s) => L.kind === 'rows' ? (s % L.m === 0 || s % L.m === L.m - 1) : (s === 0 || s === L.n - 1);
  const facing = (L, s) => s < L.m ? s + L.m : s - L.m;
  const neighbours = (L, s) => L.kind === 'circle' ? [md(s - 1, L.n), md(s + 1, L.n)] : L.kind === 'rows' ? [s - 1, s + 1].filter(t => t >= 0 && Math.floor(t / L.m) === Math.floor(s / L.m)) : [s - 1, s + 1].filter(t => t >= 0 && t < L.n);
  const occ = (c, s) => c.pos.indexOf(s);
  // clue = {t, a, b, k, dir}
  function evalClue(L, c, q) { const pa = c.pos[q.a], pb = q.b !== undefined ? c.pos[q.b] : -1;
    switch (q.t) {
      case 'end': return isEnd(L, pa); case 'notend': return !isEnd(L, pa);
      case 'fromleft': return pa === q.k - 1; case 'middle': return pa === (L.n - 1) / 2;
      case 'rel': return seatOf(L, c, q.b, q.dir, q.k) === pa;
      case 'adj': return neighbours(L, pa).includes(pb); case 'notadj': return !neighbours(L, pa).includes(pb);
      case 'between': return Math.abs(pa - pb) - 1 === q.k;
      case 'somewhere': return q.dir === 'right' ? pa > pb : pa < pb;
      case 'opp': return L.kind === 'rows' ? facing(L, pb) === pa : md(pa - pb, L.n) === L.n / 2;
      case 'relopp': { const o = L.kind === 'rows' ? occ(c, facing(L, pb)) : occ(c, md(pb + L.n / 2, L.n)); return seatOf(L, c, o, q.dir, q.k) === pa; }
      case 'faceN': return c.face[q.a] === 0; case 'faceS': return c.face[q.a] === 1;
      case 'same': return c.face[q.a] === c.face[q.b]; case 'diff': return c.face[q.a] !== c.face[q.b];
      case 'row': return Math.floor(pa / L.m) === q.k;
    } return false; }
  const relTxt = (k, dir) => k === 1 ? `immediately to the ${dir} of` : `${ORD[k]} to the ${dir} of`;
  function clueText(L, N, q) { const A = N[q.a], B = q.b !== undefined ? N[q.b] : '';
    switch (q.t) {
      case 'end': return `${A} sits at one of the ends${L.kind === 'rows' ? ' of a row' : ''}.`; case 'notend': return `${A} does not sit at an end${L.kind === 'rows' ? ' of a row' : ''}.`;
      case 'fromleft': return `${A} sits ${ORD[q.k]} from the ${L.mixed ? 'west' : 'left'} end.`; case 'middle': return `${A} sits exactly in the middle of the row.`;
      case 'rel': return `${A} sits ${relTxt(q.k, q.dir)} ${B}.`;
      case 'adj': return `${A} is an immediate neighbour of ${B}.`; case 'notadj': return `${A} is not an immediate neighbour of ${B}.`;
      case 'between': return `Exactly ${q.k} ${q.k === 1 ? 'person sits' : 'people sit'} between ${A} and ${B}.`;
      case 'somewhere': return `${A} sits somewhere to the ${q.dir} of ${B}.`;
      case 'opp': return L.kind === 'rows' ? `${A} faces ${B}.` : `${A} sits directly opposite ${B}.`;
      case 'relopp': return `${A} sits ${relTxt(q.k, q.dir)} the person who ${L.kind === 'rows' ? 'faces' : 'sits opposite'} ${B}.`;
      case 'faceN': return `${A} faces north.`; case 'faceS': return `${A} faces south.`;
      case 'same': return `${A} and ${B} face the same direction.`; case 'diff': return `${A} and ${B} face opposite directions.`;
      case 'row': return `${A} sits in Row ${q.k + 1}.`;
    } }
  function allCands(L) { const n = L.n, P = range(0, n - 1); let base;
    if (L.kind === 'circle') base = perms(range(1, n - 1)).map(p => [0].concat(p)); else base = perms(P);
    if (!L.mixed) return base.map(pos => ({ pos }));
    const out = []; for (const pos of base) for (let f = 0; f < 1 << n; f++) out.push({ pos, face: P.map(i => (f >> i) & 1) }); return out; }
  function randomClue(L, truth, allowed) { const n = L.n, t = pick(allowed); const a = ri(0, n - 1); let b = ri(0, n - 2); if (b >= a) b++;
    const q = { t, a }; if (['rel', 'adj', 'notadj', 'between', 'somewhere', 'opp', 'relopp', 'same', 'diff'].includes(t)) q.b = b;
    const pa = truth.pos[a], pb = truth.pos[b];
    if (t === 'fromleft') q.k = pa + 1; if (t === 'row') q.k = Math.floor(pa / L.m);
    if (t === 'between') { q.k = Math.abs(pa - pb) - 1; if (q.k < 1) return null; }
    if (t === 'somewhere') q.dir = pa > pb ? 'right' : 'left';
    if (t === 'rel' || t === 'relopp') { q.dir = pick(['right', 'left']); const max = L.kind === 'circle' ? Math.floor(L.n / 2) : 3; let ref = q.b;
      if (t === 'relopp') { ref = occ(truth, L.kind === 'rows' ? facing(L, pb) : md(pb + L.n / 2, L.n)); if (ref === a) return null; }
      let found = 0; for (let k = 1; k <= max; k++) if (seatOf(L, truth, ref, q.dir, k) === pa) found = k; if (!found) { q.dir = q.dir === 'right' ? 'left' : 'right'; for (let k = 1; k <= max; k++) if (seatOf(L, truth, ref, q.dir, k) === pa) found = k; }
      if (!found) return null; q.k = found; if (L.kind === 'circle' && q.k === L.n / 2) return null; }
    return evalClue(L, truth, q) ? q : null; }
  function build(L, allowed, opts) {
    opts = opts || {}; const all = allCands(L); const truth = pick(all); const clues = []; let C = all;
    for (let guard = 0; C.length > 1 && guard < 400; guard++) { const q = randomClue(L, truth, allowed); if (!q) continue; const C2 = C.filter(c => evalClue(L, c, q)); if (C2.length < C.length) { clues.push(q); C = C2; } }
    if (C.length !== 1) return null;
    for (let i = clues.length - 1; i >= 0; i--) { const rest = clues.filter((_, j) => j !== i); if (all.filter(c => rest.every(q => evalClue(L, c, q))).length === 1) clues.splice(i, 1); }
    if (opts.maxClues && clues.length > opts.maxClues) return null;
    const order = shuffle(clues); let cur = all; const trail = order.map(q => { cur = cur.filter(c => evalClue(L, c, q)); return { count: cur.length, fixed: fixedSeats(L, cur) }; });
    return { truth, clues: order, trail, total: all.length };
  }
  function fixedSeats(L, C) { const seats = new Array(L.n).fill(null); for (let s = 0; s < L.n; s++) { const p = occ(C[0], s); if (C.every(c => occ(c, s) === p)) seats[s] = p; } return seats; }
  const vizS = (L, N, seats, extra) => Object.assign({ kind: 'seating', layout: L.kind, n: L.n, m: L.m || 0, names: N, seats }, extra || {});
  function makeQuestion(L, N, truth, qkinds) { const n = L.n; const qk = pick(qkinds); const x = ri(0, n - 1);
    const at = s => s < 0 ? null : N[occ(truth, s)];
    if (qk === 'rel') { const dir = pick(['left', 'right']); for (const k of shuffle([1, 2, 3])) { const s = seatOf(L, truth, x, dir, k); if (s >= 0 && (L.kind !== 'circle' || k < n / 2)) return { text: `Who sits ${relTxt(k, dir)} ${N[x]}?`, ans: at(s), q: { qk, x, dir, k } }; } return null; }
    if (qk === 'between') { let y = ri(0, n - 2); if (y >= x) y++; const v = Math.abs(truth.pos[x] - truth.pos[y]) - 1; return { text: `How many people sit between ${N[x]} and ${N[y]}?`, ans: String(v), num: true, q: { qk, x, y } }; }
    if (qk === 'fromleft') { const k = ri(1, n); return { text: `Who sits ${ORD[k]} from the ${L.mixed ? 'west' : 'left'} end?`, ans: at(k - 1), q: { qk, k } }; }
    if (qk === 'opp') return { text: L.kind === 'rows' ? `Who faces ${N[x]}?` : `Who sits directly opposite ${N[x]}?`, ans: at(L.kind === 'rows' ? facing(L, truth.pos[x]) : md(truth.pos[x] + n / 2, n)), q: { qk, x } };
    if (qk === 'north') { const v = truth.face.filter(f => f === 0).length; return { text: 'How many people face north?', ans: String(v), num: true, q: { qk } }; }
    if (qk === 'ends') { const e = range(0, n - 1).filter(s => isEnd(L, s)).map(at).sort(); return { text: L.kind === 'rows' ? 'Which two people sit at the ends of Row 1?' : 'Which pair sits at the two ends of the row?', ans: L.kind === 'rows' ? [at(0), at(L.m - 1)].sort().join(' and ') : e.join(' and '), pair: true, q: { qk } }; }
    return null; }
  function seatingType(id, level, name, exams, L0, allowed, qkinds, letters, maxClues) {
    RL.reg('seating', level, id, name, exams, () => {
      const L = Object.assign({}, L0); const N = (letters || pick(['ABCDEFGH', 'PQRSTUVW', 'JKLMNOQR'])).slice(0, L.n).split('');
      const B = build(L, allowed, { maxClues }); if (!B) return null; const Q = makeQuestion(L, N, B.truth, qkinds); if (!Q || !Q.ans) return null;
      let opts; if (Q.num) opts = RL.mcq(Q.ans, ['0', '1', '2', '3', '4', '5', '6'].filter(v => v !== Q.ans && +v <= L.n - 2));
      else if (Q.pair) { const ps = []; for (let i = 0; i < L.n; i++) for (let j = i + 1; j < L.n; j++) ps.push(N[i] + ' and ' + N[j]); opts = RL.mcq(Q.ans, shuffle(ps)); }
      else opts = RL.mcq(Q.ans, shuffle(N.filter(v => v !== Q.ans)));
      const desc = L.kind === 'linear' ? `${L.n} people ${N.join(', ')} sit in a straight row${L.mixed ? '. Some face north and some face south' : ', all facing north'}.` : L.kind === 'circle' ? `${L.n} people ${N.join(', ')} sit around a circular table, all facing the centre.` :
        `${L.n} people ${N.join(', ')} sit in two parallel rows of ${L.m}. People in Row 1 face south and people in Row 2 face north, so each person in one row faces exactly one person in the other.`;
      const clueTxt = B.clues.map(q => clueText(L, N, q));
      const steps = [{ text: `Without clues there are ${B.total.toLocaleString('en-IN')} possible arrangements${L.kind === 'circle' ? ` (${N[0]} fixed at the top to remove rotations)` : ''}.`, viz: vizS(L, N, new Array(L.n).fill(null), { count: B.total, total: B.total, face: null }) }]
        .concat(B.clues.map((q, i) => ({ text: `Clue ${i + 1}: ${clueTxt[i]} → ${B.trail[i].count.toLocaleString('en-IN')} arrangement${B.trail[i].count === 1 ? '' : 's'} left.`, viz: vizS(L, N, B.trail[i].fixed, { count: B.trail[i].count, total: B.total, clue: i, face: B.trail[i].count === 1 && L.mixed ? B.truth.face : null }) })))
        .concat([{ text: `Only one arrangement fits every clue. ${Q.text} → ${Q.ans}.`, viz: vizS(L, N, B.trail[B.trail.length - 1].fixed, { count: 1, total: B.total, face: L.mixed ? B.truth.face : null, final: true }) }]);
      return { question: `${desc} ${Q.text}`, intro: desc, ask: Q.text, clues: clueTxt, ...opts, viz: vizS(L, N, new Array(L.n).fill(null), { count: B.total, total: B.total }), steps,
        traps: L.kind === 'circle' ? ['Facing the centre, your LEFT is clockwise. Mix that up and the whole table comes out mirrored.', 'Fix one person first, so you don\'t count rotations of the same table as different answers.', '"Second to the left" means skip one seat, not two.']
          : L.mixed ? ['Left and right depend on which way the REFERENCE person faces.', 'A south-facing person\'s right is towards the west end.', 'Try the strongest clue first, the one that fixes a facing or an end.']
          : L.kind === 'rows' ? ['Row 1 faces south, so a Row 1 person\'s right is the viewer\'s left.', '"Faces" links the same position in the two rows.', 'Ends of a row are the two outer seats of that row.']
          : ['Persons facing north: their right is the viewer\'s right in the diagram.', '"Exactly k people between" fits two ways (A left of B or B left of A). Keep both until another clue decides.', 'Write down negative clues (not at an end, not next to) and use them at the end.'],
        params: { layout: L, names: N, clues: B.clues, q: Q.q } };
    });
  }
  const LIN = ['end', 'notend', 'fromleft', 'rel', 'adj', 'notadj', 'between', 'middle'];
  seatingType('seat-e1', 'easy', 'Linear row of 5', ['bank', 'ssc', 'cuet', 'govt'], { kind: 'linear', n: 5 }, LIN, ['rel', 'fromleft', 'ends'], null, 6);
  seatingType('seat-e2', 'easy', 'Circular table of 6', ['bank', 'ssc', 'cuet', 'govt'], { kind: 'circle', n: 6 }, ['rel', 'adj', 'notadj', 'opp'], ['rel', 'opp'], null, 6);
  seatingType('seat-e3', 'easy', 'Linear row of 6: count between', ['bank', 'ssc', 'cuet'], { kind: 'linear', n: 6 }, LIN.filter(t => t !== 'middle'), ['between', 'rel'], null, 7);
  seatingType('seat-m1', 'medium', 'Linear row of 7 with indirect clues', ['bank', 'ssc', 'cuet', 'cat'], { kind: 'linear', n: 7 }, ['end', 'notend', 'rel', 'adj', 'notadj', 'between', 'somewhere', 'middle'], ['rel', 'between', 'fromleft']);
  seatingType('seat-m2', 'medium', 'Circular table of 8', ['bank', 'ssc', 'cuet', 'cat'], { kind: 'circle', n: 8 }, ['rel', 'adj', 'notadj', 'opp'], ['rel', 'opp']);
  seatingType('seat-m3', 'medium', 'Two parallel rows facing each other', ['bank', 'cat'], { kind: 'rows', n: 8, m: 4 }, ['end', 'notend', 'rel', 'adj', 'notadj', 'opp', 'row'], ['opp', 'rel', 'ends']);
  seatingType('seat-h1', 'hard', 'Circle of 8 with compound clues', ['bank', 'cat'], { kind: 'circle', n: 8 }, ['rel', 'notadj', 'relopp', 'relopp', 'adj'], ['rel', 'opp']);
  seatingType('seat-h2', 'hard', 'Linear row with mixed facing', ['bank', 'cat'], { kind: 'linear', n: 6, mixed: true }, ['end', 'notend', 'rel', 'rel', 'faceN', 'faceS', 'same', 'diff', 'fromleft', 'adj'], ['rel', 'north', 'fromleft']);
  seatingType('seat-h3', 'hard', 'Row of 8 with only relative clues', ['bank', 'cat', 'ssc'], { kind: 'linear', n: 8 }, ['end', 'notend', 'rel', 'adj', 'notadj', 'between', 'somewhere'], ['rel', 'between', 'fromleft']);
  RL.seatEngine = { evalClue, clueText, allCands, seatOf, build };
})(typeof globalThis !== 'undefined' ? globalThis : this);
