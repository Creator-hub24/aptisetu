/* Topic: DILR sets — tournaments, knockouts and logic grids (brute-force verified) */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample, perms } = RL.u;
  RL.topic('dilr', 'DILR: Tournaments & Grids', '🏆', 'Round robins, knockout brackets and logic grids. Watch the set of possible worlds shrink with each clue.', 'Arrangements & Puzzles');
  const TEAMS = ['P', 'Q', 'R', 'S', 'T', 'U'];
  const pairsOf = n => { const o = []; for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) o.push([i, j]); return o; };
  // outcome code per match: 0 = first wins, 1 = second wins, 2 = draw
  function scores(n, pr, out, W, D) { const s = new Array(n).fill(0); pr.forEach(([a, b], k) => { const o = out[k]; if (o === 0) s[a] += W; else if (o === 1) s[b] += W; else { s[a] += D; s[b] += D; } }); return s; }
  function allOutcomes(m, draws, f) { const base = draws ? 3 : 2, o = new Array(m).fill(0); const tot = base ** m; for (let x = 0; x < tot; x++) { let y = x; for (let i = 0; i < m; i++) { o[i] = y % base; y = (y / base) | 0; } f(o); } }
  RL.rr = { pairsOf, scores, allOutcomes };
  const resMatrix = (n, pr, out) => { const M = [...Array(n)].map(() => new Array(n).fill('')); pr.forEach(([a, b], k) => { const o = out[k]; M[a][b] = o === 0 ? 'W' : o === 1 ? 'L' : 'D'; M[b][a] = o === 0 ? 'L' : o === 1 ? 'W' : 'D'; }); return M; };
  const rrViz = (n, pr, out, pts, extra) => Object.assign({ kind: 'rrtable', teams: TEAMS.slice(0, n), res: out ? resMatrix(n, pr, out) : null, pts }, extra || {});

  RL.reg('dilr', 'easy', 'dl-e1', 'Round robin: missing wins', ['cat', 'bank', 'govt'], () => {
    const n = ri(4, 6), pr = pairsOf(n), out = pr.map(() => ri(0, 1)); const w = scores(n, pr, out, 1, 0); const x = ri(0, n - 1); const tot = pr.length;
    const given = TEAMS.slice(0, n).map((t, i) => i === x ? null : `${t}: ${w[i]}`).filter(Boolean).join(', ');
    return { question: `${n} teams play a round robin (each pair meets once; no draws). Wins: ${given}. How many matches did ${TEAMS[x]} win?`, ...RL.mcq(String(w[x]), RL.numDistract(w[x], 2, [tot - w[x], n - 1 - w[x], w[x] + 1])),
      viz: rrViz(n, pr, null, w.map((v, i) => i === x ? '?' : v)), steps: [{ text: `Total matches = C(${n},2) = ${tot}, and every match gives exactly one win.`, viz: rrViz(n, pr, null, w.map((v, i) => i === x ? '?' : v)) }, { text: `${TEAMS[x]} = ${tot} − (${w.filter((_, i) => i !== x).join(' + ')}) = ${w[x]}.`, viz: rrViz(n, pr, out, w) }],
      traps: ['Each team plays n − 1 matches, but the total number of matches is n(n−1)/2.', 'With no draws, total wins = total matches.'], params: { n, w, x } };
  });
  RL.reg('dilr', 'easy', 'dl-e2', 'Knockout: byes, matches, rounds', ['cat', 'bank', 'ssc', 'govt'], () => {
    const n = ri(9, 60); let P = 1; while (P < n) P *= 2; if (P === n) return null; const byes = P - n, rounds = Math.log2(P); const q = pick(['byes', 'matches', 'rounds']); const ans = q === 'byes' ? byes : q === 'matches' ? n - 1 : rounds;
    return { question: `${n} players enter a knockout. Byes are given only in round 1, so that round 2 has a power-of-2 number of players. How many ${q === 'byes' ? 'byes are given' : q === 'matches' ? 'matches are played in all' : 'rounds are needed'}?`, ...RL.mcq(String(ans), RL.numDistract(ans, 3, [n, n - 2, P - 1, n - P / 2, rounds + 1, byes + 1].filter(v => v > 0))),
      viz: { kind: 'note', text: `${n} players → next power of 2 is ${P}` }, steps: [{ text: `The next power of 2 ≥ ${n} is ${P}, so byes = ${P} − ${n} = ${byes}.` }, { text: `Each match knocks out exactly one player, so matches = ${n} − 1 = ${n - 1}.` }, { text: `Rounds = log₂ ${P} = ${rounds}.` }],
      traps: ['Matches are n − 1 whether or not there are byes.', 'Byes come from the next power of 2, not the previous one.'], params: { n, q } };
  });
  // ---- logic grid engine
  const PEOPLE = ['Asha', 'Bilal', 'Chitra', 'Dev', 'Esha'];
  const ATTR = [{ name: 'city', vals: ['Pune', 'Delhi', 'Kochi', 'Jaipur', 'Indore'], is: v => `is from ${v}`, isnt: v => `is not from ${v}`, the: v => `the person from ${v}` }, { name: 'job', vals: ['doctor', 'pilot', 'chef', 'lawyer', 'artist'], is: v => `is the ${v}`, isnt: v => `is not the ${v}`, the: v => `the ${v}` }, { name: 'drink', vals: ['tea', 'coffee', 'juice', 'milk', 'soda'], is: v => `drinks ${v}`, isnt: v => `does not drink ${v}`, the: v => `the ${v} drinker` }];
  RL.lgData = { PEOPLE, ATTR };
  const cap = s => s[0].toUpperCase() + s.slice(1);
  function lgText(c, at) { const A = at[c.a], B = c.b !== undefined ? at[c.b] : null;
    switch (c.k) { case 'is': return `${PEOPLE[c.p]} ${A.is(A.vals[c.v])}.`; case 'not': return `${PEOPLE[c.p]} ${A.isnt(A.vals[c.v])}.`; case 'link': return `${cap(A.the(A.vals[c.v]))} ${B.is(B.vals[c.w])}.`; case 'nlink': return `${cap(A.the(A.vals[c.v]))} ${B.isnt(B.vals[c.w])}.`; case 'or': return `${PEOPLE[c.p]} either ${A.is(A.vals[c.v])} or ${A.is(A.vals[c.w])}.`; } }
  RL.lgText = lgText;
  function lgSat(c, sol) { const A = sol[c.a]; switch (c.k) { case 'is': return A[c.p] === c.v; case 'not': return A[c.p] !== c.v; case 'or': return A[c.p] === c.v || A[c.p] === c.w; case 'link': case 'nlink': { const p = A.indexOf(c.v); const r = sol[c.b][p] === c.w; return c.k === 'link' ? r : !r; } } }
  function lgAll(n, na) { const P = perms([...Array(n).keys()]); if (na === 1) return P.map(p => [p]); const o = []; for (const a of P) for (const b of P) o.push([a, b]); return o; }
  function lgPool(n, na, sol, kinds) { const pool = []; for (let a = 0; a < na; a++) for (let p = 0; p < n; p++) for (let v = 0; v < n; v++) { if (sol[a][p] === v) { if (kinds.includes('is')) pool.push({ k: 'is', a, p, v }); } else { pool.push({ k: 'not', a, p, v }); if (kinds.includes('or')) pool.push({ k: 'or', a, p, v: Math.random() < 0.5 ? v : sol[a][p], w: 0, _: 1 }); } }
    pool.forEach(c => { if (c.k === 'or') { const other = c.v === sol[c.a][c.p] ? null : c.v; const t = sol[c.a][c.p]; const o = other !== null ? other : ([...Array(n).keys()].filter(x => x !== t)[ri(0, n - 2)]); const [x, y] = Math.random() < 0.5 ? [t, o] : [o, t]; c.v = x; c.w = y; delete c._; } });
    if (na === 2) for (let v = 0; v < n; v++) for (let w = 0; w < n; w++) { const p = sol[0].indexOf(v); const a = Math.random() < 0.5 ? 0 : 1; const [vv, ww] = a === 0 ? [v, w] : [w, v]; if (sol[1][p] === w) pool.push({ k: 'link', a, b: 1 - a, v: vv, w: ww }); else if (kinds.includes('nlink')) pool.push({ k: 'nlink', a, b: 1 - a, v: vv, w: ww }); }
    return shuffle(pool); }
  function lgBuild(n, na, kinds, maxC) {
    const attrs = sample([0, 1, 2], na).sort().map(i => ATTR[i]); const at = attrs.map(A => Object.assign({}, A, { vals: sample(A.vals, n) }));
    const all = lgAll(n, na); const sol = all[ri(0, all.length - 1)]; const pool = lgPool(n, na, sol, kinds);
    let live = all, chosen = [];
    while (live.length > 1 && chosen.length < 14) { let best = null, bl = null; for (const c of sample(pool, Math.min(pool.length, 12))) { if (chosen.includes(c)) continue; const l = live.filter(s => lgSat(c, s)); if (l.length === live.length) continue; const score = l.length * (c.k === 'is' ? 3 : 1); if (!best || score < bl) { best = c; bl = score; } } if (!best) return null; chosen.push(best); live = live.filter(s => lgSat(best, s)); }
    if (live.length !== 1) return null;
    for (let i = chosen.length - 1; i >= 0; i--) { const t = chosen.filter((_, j) => j !== i); if (all.filter(s => t.every(c => lgSat(c, s))).length === 1) chosen = t; }
    if (chosen.length > maxC) return null; return { n, na, at, sol, chosen, all };
  }
  RL.lgBuild = lgBuild; RL.lgSat = lgSat; RL.lgAll = lgAll;
  function lgMarks(B, live) { return B.at.map((A, a) => [...Array(B.n)].map((_, p) => [...Array(B.n)].map((_, v) => { const c = live.filter(s => s[a][p] === v).length; return c === live.length ? 'y' : c === 0 ? 'x' : ''; }))); }
  const lgViz = (B, live, hl) => ({ kind: 'lgrid', people: PEOPLE.slice(0, B.n), attrs: B.at.map(A => ({ name: A.name, vals: A.vals.slice(0, B.n) })), marks: lgMarks(B, live), hl: hl === undefined ? -1 : hl });
  function lgType(id, level, name, exams, n, na, kinds, maxC) {
    RL.reg('dilr', level, id, name, exams, () => {
      const B = lgBuild(n, na, kinds, maxC); if (!B) return null; const clues = B.chosen.map(c => lgText(c, B.at));
      const a = ri(0, na - 1), A = B.at[a]; let question, ans, opts;
      if (Math.random() < 0.5) { const p = ri(0, n - 1); question = `What is ${PEOPLE[p]}'s ${A.name}?`; ans = A.vals[B.sol[a][p]]; opts = A.vals.slice(0, n); }
      else { const v = ri(0, n - 1); question = `Who ${A.is(A.vals[v])}?`; ans = PEOPLE[B.sol[a].indexOf(v)]; opts = PEOPLE.slice(0, n); }
      const steps = []; let live = B.all; steps.push({ text: `There are ${live.length} possible arrangements at the start. Each clue crosses out cells (✗) or fixes them (✓).`, viz: lgViz(B, live) });
      B.chosen.forEach((c, i) => { live = live.filter(s => lgSat(c, s)); steps.push({ text: `Clue ${i + 1}: ${clues[i]} → ${live.length} arrangement${live.length > 1 ? 's' : ''} left.`, viz: lgViz(B, live, i) }); });
      steps.push({ text: `Answer: ${ans}.`, viz: lgViz(B, live) });
      return { question: `${PEOPLE.slice(0, n).join(', ')} each have a different ${B.at.map(x => x.name).join(' and a different ')} (${B.at.map(x => x.vals.slice(0, n).join('/')).join('; ')}).`, ask: question, clues, ...RL.mcq(ans, shuffle(opts.filter(o => o !== ans)), Math.min(5, n)), viz: lgViz(B, B.all), steps,
        traps: ['When a row has only one cell left, tick it and cross that column out for everyone else.', '“Either … or” clues only pay off after other cells are crossed out.'], params: { n, na, at: B.at.map(x => ({ name: x.name, vals: x.vals.slice(0, n) })), chosen: B.chosen, q: question } };
    });
  }
  lgType('dl-e3', 'easy', 'Logic grid (4 people × 1 attribute)', ['cat', 'bank', 'ssc', 'govt', 'cuet'], 4, 1, ['is', 'not'], 5);
  lgType('dl-m1', 'medium', 'Logic grid (4 people × 2 attributes)', ['cat', 'bank', 'govt'], 4, 2, ['not', 'link', 'nlink', 'or'], 9);
  lgType('dl-h3', 'hard', 'Logic grid (5 people × 2 attributes)', ['cat', 'bank'], 5, 2, ['not', 'link', 'nlink', 'or'], 12);

  // ---- points table (n=4 with draws)
  RL.reg('dilr', 'medium', 'dl-m2', 'Points table: decode results', ['cat', 'bank'], () => {
    const n = 4, pr = pairsOf(n), W = pick([2, 3]); const out = pr.map(() => ri(0, 2)); if (!out.includes(2)) return null; const pts = scores(n, pr, out, W, 1);
    const cons = []; allOutcomes(pr.length, true, o => { const s = scores(n, pr, o, W, 1); if (s.every((v, i) => v === pts[i])) cons.push(o.slice()); });
    const cands = []; const dr = o => o.filter(x => x === 2).length; if (cons.every(o => dr(o) === dr(out))) cands.push({ q: 'How many matches ended in a draw?', ans: String(dr(out)), opts: ['0', '1', '2', '3', '4', '5', '6'] });
    pr.forEach(([a, b], k) => { if (cons.every(o => o[k] === out[k])) cands.push({ q: `What was the result of ${TEAMS[a]} vs ${TEAMS[b]}?`, ans: out[k] === 0 ? `${TEAMS[a]} won` : out[k] === 1 ? `${TEAMS[b]} won` : 'Draw', opts: [`${TEAMS[a]} won`, `${TEAMS[b]} won`, 'Draw', 'Cannot be determined'], hard: cons.length > 1 }); });
    const good = cands.filter(c => c.hard !== false); if (!good.length) return null; const C = pick(good);
    return { question: `Four teams P, Q, R, S play a round robin. A win earns ${W} points, a draw 1, a loss 0. Final points: ${TEAMS.slice(0, n).map((t, i) => `${t} ${pts[i]}`).join(', ')}.`, ask: C.q, ...RL.mcq(C.ans, shuffle(C.opts.filter(o => o !== C.ans))), viz: rrViz(n, pr, null, pts),
      steps: [{ text: W === 3 ? 'Each team plays 3 matches. A decisive match gives 3 points in total and a draw gives 2, so draws = 18 − (sum of points).' : 'Each team plays 3 matches. Every match gives 2 points in total, so look at odd totals: a team with odd points must have an odd number of draws.', viz: rrViz(n, pr, null, pts) }, { text: `Checking all 3⁶ = 729 result patterns leaves ${cons.length} consistent table${cons.length > 1 ? 's' : ''}.`, viz: rrViz(n, pr, cons[0], pts) }, { text: `In every one of them: ${C.ans}.`, viz: rrViz(n, pr, out, pts) }],
      traps: [W === 3 ? 'With 3 points for a win, the total is 18 − (number of draws).' : 'With 2 points for a win, every match adds 2 points, so the total tells you nothing about draws.', 'Do not assume the top team won all its matches.'], params: { W, pts, q: C.q } };
  });
  // ---- knockout with seeds
  const ORDER = [1, 8, 4, 5, 2, 7, 3, 6];
  function koPlay(bits) { let cur = ORDER.slice(), k = 0; const rounds = [cur]; while (cur.length > 1) { const nx = []; for (let i = 0; i < cur.length; i += 2) nx.push(bits[k++] ? cur[i + 1] : cur[i]); cur = nx; rounds.push(cur); } return rounds; }
  RL.ko = { ORDER, koPlay };
  function koFacts(R) { const F = []; const upsets = (() => { let u = 0; for (let r = 0; r < 3; r++) for (let i = 0; i < R[r].length; i += 2) { const a = R[r][i], b = R[r][i + 1], w = R[r + 1][i / 2]; if (w === Math.max(a, b)) u++; } return u; })();
    F.push({ k: 'upsets', v: upsets }); for (let s = 1; s <= 8; s++) { const out = R[1].includes(s) ? (R[2].includes(s) ? (R[3].includes(s) ? 'won' : 'final') : 'semi') : 'r1'; F.push({ k: 'stage', s, v: out }); }
    F.push({ k: 'champParity', v: R[3][0] % 2 }); return F; }
  function koHolds(f, R) { const g2 = koFacts(R); return g2.some(x => x.k === f.k && x.s === f.s && x.v === f.v); }
  const koText = f => f.k === 'upsets' ? `Exactly ${f.v} match${f.v === 1 ? '' : 'es'} ended in an upset (the lower-ranked seed, i.e. the larger number, won).` : f.k === 'champParity' ? `The champion's seed number is ${f.v ? 'odd' : 'even'}.` : f.v === 'won' ? `Seed ${f.s} won the tournament.` : f.v === 'final' ? `Seed ${f.s} lost in the final.` : f.v === 'semi' ? `Seed ${f.s} lost in the semi-finals.` : `Seed ${f.s} lost in round 1.`;
  RL.koText = koText; RL.koHolds = koHolds;
  RL.reg('dilr', 'medium', 'dl-m3', 'Seeded knockout with upsets', ['cat'], () => {
    const ALL = [...Array(128).keys()].map(x => koPlay([...Array(7)].map((_, i) => (x >> i) & 1)));
    const R = ALL[ri(0, 127)]; const q = pick(['champ', 'runner']); const ansOf = X => q === 'champ' ? X[3][0] : X[2].find(s => s !== X[3][0]);
    const pool = shuffle(koFacts(R).filter(f => !(f.k === 'stage' && (f.v === 'won' || (q === 'runner' && f.v === 'final'))))); let live = ALL, chosen = [];
    while (new Set(live.map(ansOf)).size > 1) { let best = null, bl = 1e9; for (const f of pool) { if (chosen.includes(f)) continue; const l = live.filter(X => koHolds(f, X)); if (l.length < live.length && l.length < bl) { best = f; bl = l.length; } } if (!best) return null; chosen.push(best); live = live.filter(X => koHolds(best, X)); }
    for (let i = chosen.length - 1; i >= 0; i--) { const t = chosen.filter((_, j) => j !== i); if (new Set(ALL.filter(X => t.every(f => koHolds(f, X))).map(ansOf)).size === 1) chosen = t; }
    if (chosen.length < 2 || chosen.length > 5) return null; const live2 = ALL.filter(X => chosen.every(f => koHolds(f, X))); const ans = ansOf(R);
    const opts = shuffle([1, 2, 3, 4, 5, 6, 7, 8].filter(s => s !== ans)).slice(0, 3).map(s => `Seed ${s}`);
    return { question: 'Eight players, seeded 1 (strongest) to 8, play a knockout. Round 1 pairs 1v8, 4v5, 2v7, 3v6; the winners of 1v8 and 4v5 meet in one semi-final, and the winners of 2v7 and 3v6 in the other.', clues: chosen.map(koText), ask: q === 'champ' ? 'Who won the tournament?' : 'Who was the runner-up?', ...RL.mcq(`Seed ${ans}`, opts),
      viz: { kind: 'bracket', rounds: [ORDER] }, steps: [{ text: 'There are 2⁷ = 128 possible brackets (7 matches, 2 outcomes each).', viz: { kind: 'bracket', rounds: [ORDER] } }, ...chosen.map((f, i) => { const l = ALL.filter(X => chosen.slice(0, i + 1).every(h => koHolds(h, X))); return { text: `${koText(f)} → ${l.length} bracket${l.length > 1 ? 's' : ''} left.`, viz: { kind: 'bracket', rounds: l[0] } }; }), { text: `Every remaining bracket (${live2.length}) gives Seed ${ans}.`, viz: { kind: 'bracket', rounds: R } }],
      traps: ['An upset means the larger seed number wins.', 'Seeds 1 and 4 can only meet in a semi-final; 1 and 2 only in the final.'], params: { chosen, q } };
  });
  // ---- max / min qualification
  RL.reg('dilr', 'hard', 'dl-h1', 'Max/min points to qualify', ['cat'], () => {
    const n = ri(4, 5), pr = pairsOf(n), W = pick([2, 3]), draws = n === 4 || Math.random() < 0.5, k = ri(2, n - 2); const mode = pick(['maxOut', 'minIn']);
    let best = mode === 'maxOut' ? -1 : 1e9, ex = null;
    allOutcomes(pr.length, draws, o => { const s = scores(n, pr, o, W, 1); const above = s.filter(v => v > s[0]).length; if (mode === 'maxOut' ? (above >= k && s[0] > best) : (above < k && s[0] < best)) { best = s[0]; ex = o.slice(); } });
    if (ex === null) return null; const s = scores(n, pr, ex, W, 1);
    const q = mode === 'maxOut' ? `What is the maximum number of points team P can score and still have at least ${k} teams finish with strictly more points than P?` : `What is the minimum number of points team P can score and still have fewer than ${k} teams finish with strictly more points (so that P is in the top ${k} on points)?`;
    return { question: `${n} teams P${TEAMS.slice(1, n).map(t => ', ' + t).join('')} play a round robin. A win earns ${W} points${draws ? ', a draw 1 point each and a loss 0' : ' and a loss 0; there are no draws'}.`, ask: q, ...RL.mcq(String(best), RL.numDistract(best, W + 1, [best + 1, best - 1, best + W, best - W])), viz: rrViz(n, pr, null, null),
      steps: [{ text: `There are ${pr.length} matches, so ${(draws ? 3 : 2) ** pr.length} possible result patterns. The extreme case is found by ${mode === 'maxOut' ? 'letting P do as well as possible while ' + k + ' teams still beat it' : 'letting P do as badly as possible while still staying in the top ' + k}.`, viz: rrViz(n, pr, null, null) },
        { text: `One extreme table (points ${TEAMS.slice(0, n).map((t, i) => `${t}=${s[i]}`).join(', ')}) gives P = ${best}.`, viz: rrViz(n, pr, ex, s, { hl: 0 }) },
        { text: mode === 'maxOut' ? `Try ${best + (draws ? 1 : W)} or more: there are then not enough points left for ${k} teams to all finish above P. So the maximum is ${best}.` : `With fewer points, at least ${k} teams always finish above P. So the minimum is ${best}.` }],
      traps: ['The teams above P need to take points from each other as well as from P.', 'Strictly more points means a tie does not count as finishing above P.'], params: { n, W, draws, k, mode } };
  });
  // ---- who lost to whom (n=5 no draws)
  RL.reg('dilr', 'hard', 'dl-h2', 'Round robin: who beat whom', ['cat', 'bank'], () => {
    const n = 5, pr = pairsOf(n), out = pr.map(() => ri(0, 1)); const w = scores(n, pr, out, 1, 0); const x = w.findIndex(v => v === n - 2); const y = w.findIndex(v => v === 1); const useLoss = x >= 0 && (y < 0 || Math.random() < 0.5); const t = useLoss ? x : y; if (t < 0) return null;
    const opp = pr.map(([a, b], k) => (a === t || b === t) ? ((a === t ? (out[k] === 0) : (out[k] === 1)) ? null : (a === t ? b : a)) : null).filter(v => v !== null); const beaten = pr.map(([a, b], k) => (a === t && out[k] === 0) ? b : (b === t && out[k] === 1) ? a : null).filter(v => v !== null);
    const target = useLoss ? opp[0] : beaten[0];
    const cons0 = []; allOutcomes(pr.length, false, o => { const s = scores(n, pr, o, 1, 0); if (s.every((v, i) => v === w[i])) cons0.push(o.slice()); });
    const tgt = o => { for (let k = 0; k < pr.length; k++) { const [a, b] = pr[k]; if (a !== t && b !== t) continue; const tw = a === t ? o[k] === 0 : o[k] === 1; if (tw !== useLoss) return a === t ? b : a; } };
    const facts = shuffle(pr.map((p, k) => k).filter(k => !pr[k].includes(t))); let live = cons0, chosen = [];
    while (new Set(live.map(tgt)).size > 1) { const k = facts.find(k => !chosen.includes(k) && live.some(o => o[k] !== out[k])); if (k === undefined) return null; chosen.push(k); live = live.filter(o => o[k] === out[k]); }
    for (let i = chosen.length - 1; i >= 0; i--) { const tt = chosen.filter((_, j) => j !== i); if (new Set(cons0.filter(o => tt.every(k => o[k] === out[k])).map(tgt)).size === 1) chosen = tt; }
    if (chosen.length > 3) return null; const mt = k => { const [a, b] = pr[k]; return out[k] === 0 ? `${TEAMS[a]} beat ${TEAMS[b]}.` : `${TEAMS[b]} beat ${TEAMS[a]}.`; };
    return { question: `Five teams P, Q, R, S, T play a round robin with no draws. Wins: ${TEAMS.slice(0, n).map((tm, i) => `${tm} ${w[i]}`).join(', ')}.`, clues: chosen.map(mt), ask: useLoss ? `${TEAMS[t]} lost exactly one match. Whom did it lose to?` : `${TEAMS[t]} won exactly one match. Whom did it beat?`, ...RL.mcq(TEAMS[target], TEAMS.slice(0, n).filter((_, i) => i !== t && i !== target)),
      viz: rrViz(n, pr, null, w), steps: [{ text: `${cons0.length} result tables fit the win counts alone.`, viz: rrViz(n, pr, cons0[0], w) }, ...chosen.map((k, i) => { const l = cons0.filter(o => chosen.slice(0, i + 1).every(j => o[j] === out[j])); return { text: `${mt(k)} → ${l.length} table${l.length > 1 ? 's' : ''} left.`, viz: rrViz(n, pr, l[0], w) }; }), { text: `In all of them ${TEAMS[t]} ${useLoss ? 'lost to' : 'beat'} ${TEAMS[target]}.`, viz: rrViz(n, pr, out, w, { hl: t }) }],
      traps: ['A team with 0 wins lost to everyone, so use that first.', 'Count the remaining wins and losses in each row before guessing.'], params: { w, t, useLoss, chosen: chosen.map(k => [pr[k], out[k]]) } };
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
