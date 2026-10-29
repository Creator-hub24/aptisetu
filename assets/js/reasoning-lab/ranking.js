/* Topic: Order & ranking — positions in a row/queue, interchange, comparison chains */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample, perms } = RL.u;
  RL.topic('ranking', 'Order & Ranking', '🏅', 'A queue you can see, so positions counted from either end, overlaps and swaps are no longer guesswork.', 'Arrangements & Puzzles');
  const NM = ['Ravi', 'Sona', 'Amit', 'Neha', 'Karan', 'Pooja', 'Dev', 'Meera', 'Arjun', 'Riya'];
  const ord = n => n + (n % 100 >= 11 && n % 100 <= 13 ? 'th' : ['th', 'st', 'nd', 'rd'][n % 10] || 'th');
  RL.ord = RL.ord || ord;
  const qv = (N, marks, extra) => Object.assign({ kind: 'queue', N, marks }, extra || {});
  RL.reg('ranking', 'easy', 'rank-e1', 'Total from both-end ranks', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const k = ri(4, 30), m = ri(4, 30), N = k + m - 1, [a] = sample(NM, 1), side = pick([['top', 'bottom', 'a class'], ['left', 'right', 'a row'], ['front', 'back', 'a queue']]);
    return { question: `${a} is ${ord(k)} from the ${side[0]} and ${ord(m)} from the ${side[1]} in ${side[2]}. How many people are there in ${side[2]}?`, ...RL.mcq(String(N), [N + 1, N + 2, N - 2, k + m + 1].map(String)), viz: qv(N, [{ pos: k, label: a }]),
      steps: [{ text: `${k - 1} people are on one side of ${a} and ${m - 1} on the other.`, viz: qv(N, [{ pos: k, label: a }], { brace: [[1, k - 1], [k + 1, N]] }) }, { text: `Total = ${k} + ${m} − 1 = ${N} (${a} was counted twice).`, viz: qv(N, [{ pos: k, label: a }]) }],
      traps: ['Subtract 1, because the person is counted in both ranks.', 'Don\'t add 1 out of habit.'], params: { k, m } };
  });
  RL.reg('ranking', 'easy', 'rank-e2', 'Rank from the other end', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const N = ri(20, 60), k = ri(3, N - 3), [a] = sample(NM, 1), r = N - k + 1;
    return { question: `In a row of ${N} students, ${a} is ${ord(k)} from the left end. What is ${a}'s position from the right end?`, ...RL.mcq(ord(r), [r - 1, r + 1, N - k, k].filter(x => x > 0 && x !== r).map(ord)), viz: qv(N, [{ pos: k, label: a }]),
      steps: [{ text: `Students to the right of ${a}: ${N} − ${k} = ${N - k}.`, viz: qv(N, [{ pos: k, label: a }], { brace: [[k + 1, N]] }) }, { text: `So ${a} is ${ord(N - k + 1)} from the right (${N} − ${k} + 1).` }],
      traps: ['N − k counts the people beyond, so add 1 for the person.', 'Left + right − 1 = total, so right = total − left + 1.'], params: { N, k } };
  });
  RL.reg('ranking', 'medium', 'rank-m1', 'People between two positions', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const N = ri(25, 50), p = ri(3, N - 3), qr = ri(3, N - 3), q = N - qr + 1; if (Math.abs(p - q) < 2) return null; const [a, b] = sample(NM, 2), bt = Math.abs(p - q) - 1;
    return { question: `In a row of ${N} children, ${a} is ${ord(p)} from the left and ${b} is ${ord(qr)} from the right. How many children are there between ${a} and ${b}?`, ...RL.mcq(String(bt), [bt + 1, bt + 2, Math.abs(N - p - qr), p + qr, bt - 1].filter(x => x >= 0).map(String)),
      viz: qv(N, [{ pos: p, label: a }, { pos: q, label: b }]),
      steps: [{ text: `${b} from the left = ${N} − ${qr} + 1 = ${q}.`, viz: qv(N, [{ pos: p, label: a }, { pos: q, label: b }]) }, { text: `Between positions ${Math.min(p, q)} and ${Math.max(p, q)}: ${Math.max(p, q)} − ${Math.min(p, q)} − 1 = ${bt}.`, viz: qv(N, [{ pos: p, label: a }, { pos: q, label: b }], { brace: [[Math.min(p, q) + 1, Math.max(p, q) - 1]] }) }],
      traps: ['Convert both positions to the same end before subtracting.', 'They may cross over, with B to the left of A, so draw it.'], params: { N, p, qr } };
  });
  RL.reg('ranking', 'medium', 'rank-m2', 'Interchange of positions', ['ssc', 'bank', 'govt', 'cuet'], () => {
    const N = ri(20, 50), pa = ri(2, N - 1), pb = ri(2, N - 1); if (Math.abs(pa - pb) < 2) return null; const [a, b] = sample(NM, 2), bR = N - pb + 1;
    return { question: `In a row, ${a} is ${ord(pa)} from the left and ${b} is ${ord(bR)} from the right. When they swap places, ${a} becomes ${ord(pb)} from the left. How many people are in the row?`,
      ...RL.mcq(String(N), [N + 1, N - 1, pa + bR - 1, pb + bR, N + 2].filter(x => x !== N).map(String)), viz: qv(N, [{ pos: pa, label: a }, { pos: pb, label: b }]),
      steps: [{ text: `After the swap, ${a} sits in ${b}'s old seat, so ${b}'s old seat is ${ord(pb)} from the left.`, viz: qv(N, [{ pos: pb, label: a + '→' }]) }, { text: `That same seat is ${ord(bR)} from the right, so total = ${pb} + ${bR} − 1 = ${N}.`, viz: qv(N, [{ pos: pb, label: b + '/' + a }]) }],
      traps: ['Use the new position together with the OTHER person\'s rank from the other end.', 'A\'s old position is a distractor here.'], params: { pa, bR, pb } };
  });
  // comparison chains
  const ATTR = [['taller', 'shorter', 'tallest', 'shortest'], ['heavier', 'lighter', 'heaviest', 'lightest'], ['older', 'younger', 'oldest', 'youngest'], ['richer', 'poorer', 'richest', 'poorest']];
  function cmpSolve(n, clues) { const out = []; for (const p of perms([...Array(n).keys()])) { const r = []; p.forEach((x, i) => r[x] = i); // r[x]=rank, 0 = most
      if (clues.every(c => c.t === 'gt' ? r[c.a] < r[c.b] : c.t === 'top' ? r[c.a] === 0 : c.t === 'bot' ? r[c.a] === n - 1 : c.t === 'nbot' ? r[c.a] !== n - 1 : c.t === 'ntop' ? r[c.a] !== 0 : true)) out.push(r.slice()); } return out; }
  RL.cmpSolve = cmpSolve;
  function cmpType(id, level, name, n, exams, compound) {
    RL.reg('ranking', level, id, name, exams, () => {
      const P = sample(NM, n), AT = pick(ATTR), truth = shuffle([...Array(n).keys()]); const r = []; truth.forEach((x, i) => r[x] = i);
      const ask = pick(['kth', 'count', 'kth']), K = ri(1, n - 2), X = ri(0, n - 1);
      const ansOf = R => ask === 'kth' ? R.indexOf(K) : R.filter((v, i) => v < R[X]).length;
      const all = []; for (let a = 0; a < n; a++) for (let b = 0; b < n; b++) if (r[a] < r[b] && r[b] - r[a] <= 3) all.push({ t: 'gt', a, b });
      all.push({ t: 'top', a: truth[0] }, { t: 'bot', a: truth[n - 1] }); truth.slice(1, -1).forEach(a => all.push({ t: pick(['nbot', 'ntop']), a }));
      const cl = []; let S; const pool = shuffle(all);
      for (const c of pool) { cl.push(c); S = cmpSolve(n, cl); if (new Set(S.map(ansOf)).size === 1) break; }
      if (new Set(S.map(ansOf)).size !== 1) return null;
      for (let i = cl.length - 1; i >= 0; i--) { const t = cl.filter((_, j) => j !== i); const S2 = cmpSolve(n, t); if (new Set(S2.map(ansOf)).size === 1) { cl.splice(i, 1); S = S2; } }
      if (S.length === 1 && level === 'hard' && Math.random() < .5) return null; if (cl.length < (level === 'easy' ? 3 : 4)) return null;
      // texts (compound merges two gt sharing a middle)
      const T = []; const used = new Set();
      if (compound) for (let i = 0; i < cl.length; i++) for (let j = 0; j < cl.length; j++) if (!used.has(i) && !used.has(j) && i !== j && cl[i].t === 'gt' && cl[j].t === 'gt' && cl[i].a === cl[j].b) { T.push(`${P[cl[i].a]} is ${AT[0]} than ${P[cl[i].b]} but ${AT[1]} than ${P[cl[j].a]}.`); used.add(i); used.add(j); }
      cl.forEach((c, i) => { if (used.has(i)) return; T.push(c.t === 'gt' ? `${P[c.a]} is ${AT[0]} than ${P[c.b]}.` : c.t === 'top' ? `${P[c.a]} is the ${AT[2]}.` : c.t === 'bot' ? `${P[c.a]} is the ${AT[3]}.` : c.t === 'nbot' ? `${P[c.a]} is not the ${AT[3]}.` : `${P[c.a]} is not the ${AT[2]}.`); });
      const A = ansOf(S[0]); const ansL = ask === 'kth' ? P[A] : String(A); const ds = ask === 'kth' ? P.filter((_, i) => i !== A) : [...Array(n).keys()].filter(v => v !== A).map(String);
      const known = [...Array(n).keys()].map(k => { const w = new Set(S.map(R => R.indexOf(k))); return w.size === 1 ? P[[...w][0]] : '?'; });
      return { question: `Among ${n} friends (${P.slice().sort().join(", ")}): ${shuffle(T).join(' ')} ${ask === 'kth' ? `Who is the ${K === 0 ? AT[2] : ord(K + 1) + ' ' + AT[2]}?` : `How many friends are ${AT[0]} than ${P[X]}?`}`, clues: T, ...RL.mcq(ansL, shuffle(ds)),
        viz: { kind: 'ladder', slots: known.map(() => '?'), attr: AT[2] },
        steps: [{ text: 'Write every clue as an arrow (A > B) and chain them.', viz: { kind: 'ladder', slots: known.map(() => '?'), chain: cl.filter(c => c.t === 'gt').map(c => [P[c.a], P[c.b]]), attr: AT[2] } },
          { text: `${S.length} order(s) fit all the clues. Fixed positions: ${known.map((x, i) => `${ord(i + 1)}: ${x}`).join(', ')}.`, viz: { kind: 'ladder', slots: known, attr: AT[2], count: S.length } },
          { text: `Answer: ${ansL}.`, viz: { kind: 'ladder', slots: known, attr: AT[2], hl: ask === 'kth' ? K : S[0][X] } }],
        traps: ['"Not the tallest" is weaker than it sounds. Use it only to eliminate.', 'Several orders may fit; answer only what is fixed in all of them.'], params: { P, AT, cl, ask, K, X, n } };
    });
  }
  cmpType('rank-e3', 'easy', 'Comparison chain (5 people)', 5, ['ssc', 'bank', 'cuet', 'govt'], false);
  cmpType('rank-m3', 'medium', 'Comparison with partial order', 6, ['ssc', 'bank', 'cuet', 'govt'], true);
  cmpType('rank-h3', 'hard', 'Seven-person comparison (compound clues)', 7, ['bank', 'ssc', 'cat'], true);
  RL.reg('ranking', 'hard', 'rank-h1', 'Minimum people in a queue', ['ssc', 'bank', 'cat', 'cuet'], () => {
    const f = ri(5, 20), b = ri(5, 20), k = ri(1, 8), [A, B] = sample(NM, 2);
    // configs: A ahead of B: N = f + k + 1 + b (B position f+k+1 from front) ; B ahead of A: B at f-k-1 from front (needs >=1): N = (f-k-1) + b - 1
    const cands = [f + k + b]; if (f - k - 1 >= 1 && f - k - 1 + b - 1 >= f) cands.push(f - k - 1 + b - 1); const N = Math.min(...cands); const alt = Math.max(...cands);
    return { question: `In a queue, ${A} is ${ord(f)} from the front and ${B} is ${ord(b)} from the back. Exactly ${k} people stand between ${A} and ${B}. What is the minimum possible number of people in the queue?`,
      ...RL.mcq(String(N), [alt, f + k + b + 1, N + 1, N - 1, f + b - 1].filter(x => x !== N && x > 0).map(String)), viz: qv(alt, [{ pos: f, label: A }, { pos: f + k + 1, label: B }]),
      steps: [{ text: `Case 1: ${B} is behind ${A}. Total = ${f} + ${k} + ${b} = ${f + k + b}.`, viz: qv(f + k + b, [{ pos: f, label: A }, { pos: f + k + 1, label: B }], { brace: [[f + 1, f + k]] }) },
        cands.length > 1 ? { text: `Case 2: ${B} is ahead of ${A}, at position ${f - k - 1} from the front. Total = ${f - k - 1} + ${b} − 1 = ${cands[1]}.`, viz: qv(cands[1], [{ pos: f, label: A }, { pos: f - k - 1, label: B }], { brace: [[f - k, f - 1]] }) } : { text: `Case 2 is impossible: ${B} can't be ${k + 1} places ahead of ${A}${f - k - 1 >= 1 ? ' while still being ' + ord(b) + ' from the back' : ''}.` },
        { text: `Minimum = ${N}.` }],
      traps: ['Always check the overlapping case, where they cross.', 'In the crossing case, make sure the back rank still fits behind both people.'], params: { f, b, k } };
  });
  RL.reg('ranking', 'hard', 'rank-h2', 'Rank change after students leave or join', ['ssc', 'bank', 'govt', 'cuet'], () => {
    const t = ri(8, 25), bm = ri(8, 25), N = t + bm - 1, below = ri(2, bm - 3), above = ri(0, Math.min(4, t - 2)), join = ri(0, 4), [a] = sample(NM, 1);
    const nt = t - above, nb = bm - below + join, NN = N - below - above + join; const ask = pick(['top', 'bottom', 'total']);
    const ans = ask === 'top' ? nt : ask === 'bottom' ? nb : NN;
    return { question: `${a} is ${ord(t)} from the top and ${ord(bm)} from the bottom in a class. ${below} students ranked below ${a}${above ? ` and ${above} ranked above ${a}` : ''} leave the class${join ? `, and ${join} new student${join > 1 ? 's join, all' : ' joins,'} ranked below ${a}` : ''}. ${ask === 'total' ? 'How many students are in the class now?' : `What is ${a}'s rank from the ${ask} now?`}`,
      ...RL.mcq(ask === 'total' ? String(ans) : ord(ans), [ans + 1, ans - 1, ans + join, ans - join, ans + below, ans + above, t, bm].filter(x => x > 0 && x !== ans).map(x => ask === 'total' ? String(x) : ord(x))),
      viz: qv(N, [{ pos: t, label: a }]), steps: [{ text: `Start: ${N} students (${t} + ${bm} − 1).`, viz: qv(N, [{ pos: t, label: a }]) }, { text: `Above ${a}: ${t - 1} − ${above} = ${t - 1 - above}. Below: ${bm - 1} − ${below} + ${join} = ${bm - 1 - below + join}.` },
        { text: `Now ${a} is ${ord(nt)} from the top, ${ord(nb)} from the bottom, out of ${NN} students.`, viz: qv(NN, [{ pos: nt, label: a }]) }],
      traps: ['People leaving from BELOW do not change the rank from the top.', 'Add newcomers only on the side where they rank.'], params: { t, bm, below, above, join, ask } };
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
