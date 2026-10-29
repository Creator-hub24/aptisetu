/* Topic: Syllogisms — conclusions checked by enumerating every Venn model of the statements. */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample } = RL.u;
  RL.topic('syllogism', 'Syllogisms', '⭕', 'Venn diagrams that show what must be true and what is only possible, the way banking and SSC exams test it.', 'Logical Reasoning');
  const NOUNS = ['pens', 'books', 'bags', 'cups', 'lamps', 'chairs', 'tables', 'phones', 'clocks', 'rings', 'coins', 'birds', 'trees', 'stones', 'kites', 'cars', 'doors', 'roses', 'boats', 'drums', 'shirts', 'tiles'];
  const sing = w => w.slice(0, -1);
  // statement: {q:'all'|'some'|'no'|'somenot'|'few', x, y}; possibility: {q:'pall'|'psome', x, y}
  function models(k, stmts) { const R = (1 << k) - 1; const out = [];
    for (let m = 0; m < 1 << R; m++) { const has = r => (m >> (r - 1)) & 1; let ok = true;
      for (let s = 0; s < k && ok; s++) { let any = false; for (let r = 1; r <= R; r++) if (has(r) && (r >> s) & 1) any = true; if (!any) ok = false; }
      if (ok && stmts.every(st => holds(m, R, st))) out.push(m); } return out; }
  function holds(m, R, st) { const X = 1 << st.x, Y = 1 << st.y; let xy = false, xny = false;
    for (let r = 1; r <= R; r++) if ((m >> (r - 1)) & 1) { if (r & X && r & Y) xy = true; if (r & X && !(r & Y)) xny = true; }
    switch (st.q) { case 'all': return !xny; case 'no': return !xy; case 'some': return xy; case 'somenot': return xny; case 'few': return xy && xny; } }
  const base = c => ({ pall: 'all', psome: 'some' })[c.q];
  function judge(k, stmts, c, M) { M = M || models(k, stmts); const R = (1 << k) - 1;
    if (c.q === 'pall' || c.q === 'psome') { const b = { q: base(c), x: c.x, y: c.y }; const n = M.filter(m => holds(m, R, b)).length; return { follows: n > 0, definite: n === M.length, impossible: n === 0 }; }
    const n = M.filter(m => holds(m, R, c)).length; return { follows: n === M.length, never: n === 0 }; }
  const contra = (a, b) => a.x === b.x && a.y === b.y && ((a.q === 'some' && b.q === 'no') || (a.q === 'no' && b.q === 'some') || (a.q === 'all' && b.q === 'somenot') || (a.q === 'somenot' && b.q === 'all')) ||
    (a.x === b.y && a.y === b.x && ((a.q === 'some' && b.q === 'no') || (a.q === 'no' && b.q === 'some')));
  function text(st, T) { const X = T[st.x], Y = T[st.y];
    switch (st.q) { case 'all': return `All ${X} are ${Y}.`; case 'some': return `Some ${X} are ${Y}.`; case 'no': return `No ${sing(X)} is a ${sing(Y)}.`; case 'somenot': return `Some ${X} are not ${Y}.`;
      case 'few': return `Only a few ${X} are ${Y}.`; case 'pall': return `All ${X} being ${Y} is a possibility.`; case 'psome': return `Some ${X} being ${Y} is a possibility.`; } }
  RL.syl = { models, holds, judge, text };
  const FIVE = ['Only I follows', 'Only II follows', 'Either I or II follows', 'Neither I nor II follows', 'Both I and II follow'];
  function vennViz(k, T, M, hl, extra) { const R = (1 << k) - 1; const st = []; for (let r = 1; r <= R; r++) { const n = M.filter(m => (m >> (r - 1)) & 1).length; st.push(n === 0 ? 'empty' : n === M.length ? 'some' : 'maybe'); }
    // "spread" members: at least one of several regions is non-empty in every model, but no single region is forced.
    const groups = []; const cand = []; for (let i = 0; i < k; i++) for (let j = 0; j < k; j++) if (i !== j) { if (i < j) cand.push(r => ((r >> i) & 1) && ((r >> j) & 1)); cand.push(r => ((r >> i) & 1) && !((r >> j) & 1)); }
    for (const f of cand) { const G = []; for (let r = 1; r <= R; r++) if (f(r)) G.push(r); if (G.some(r => st[r - 1] === 'some')) continue; const live = G.filter(r => st[r - 1] === 'maybe'); if (live.length < 2) continue;
      if (!M.every(m => live.some(r => (m >> (r - 1)) & 1))) continue; if (groups.some(g2 => g2.every(r => live.includes(r)))) continue; for (let q = groups.length - 1; q >= 0; q--) if (live.every(r => groups[q].includes(r))) groups.splice(q, 1); groups.push(live); }
    return Object.assign({ kind: 'venn', sets: T.slice(0, k), regions: st, spread: groups.slice(0, 3), hl: hl || null }, extra || {}); }
  function example(k, M, pred) { const R = (1 << k) - 1; const m = M.find(pred); if (m === undefined) return null; const st = []; for (let r = 1; r <= R; r++) st.push((m >> (r - 1)) & 1 ? 'some' : 'empty'); return st; }
  function chainStmts(k, qs) { const order = shuffle([...Array(k).keys()]); const st = [];
    for (let i = 0; i < k - 1; i++) { const q = pick(qs); let x = order[i], y = order[i + 1]; if (Math.random() < .5 && q !== 'all' && q !== 'somenot' && q !== 'few') [x, y] = [y, x]; st.push({ q, x, y }); } return st; }
  function randConcl(k, kinds) { const x = ri(0, k - 1); let y = ri(0, k - 2); if (y >= x) y++; return { q: pick(kinds), x, y }; }
  function decide(k, stmts, I, II, M) { const a = judge(k, stmts, I, M), b = judge(k, stmts, II, M);
    if (a.follows && b.follows) return FIVE[4]; if (a.follows) return FIVE[0]; if (b.follows) return FIVE[1]; if (contra(I, II) && !a.never && !b.never) return FIVE[2]; return FIVE[3]; }
  const okPoss = (k, stmts, c, M) => !(c.q === 'pall' || c.q === 'psome') || !judge(k, stmts, c, M).definite;
  function twoConcl(id, level, name, k, sq, cq, wantEither) {
    RL.reg('syllogism', level, id, name, ['bank', 'ssc', 'cuet', 'govt'], () => {
      const T = sample(NOUNS, k); const target = pick(FIVE.filter(f => wantEither || f !== FIVE[2]).concat(wantEither ? [FIVE[2], FIVE[2]] : []));
      for (let t = 0; t < 400; t++) { const stmts = chainStmts(k, sq); const M = models(k, stmts); if (!M.length) continue;
        let I = randConcl(k, cq), II = randConcl(k, cq); if (target === FIVE[2] && Math.random() < .8) { II = Object.assign({}, I, { q: ({ some: 'no', no: 'some', all: 'somenot', somenot: 'all' })[I.q] || 'no' }); if (!['some', 'no', 'all', 'somenot'].includes(I.q)) continue; }
        if (text(I, T) === text(II, T) || !okPoss(k, stmts, I, M) || !okPoss(k, stmts, II, M)) continue;
        const ans = decide(k, stmts, I, II, M); if (ans !== target && t < 380) continue;
        const ja = judge(k, stmts, I, M), jb = judge(k, stmts, II, M); const ex = c => example(k, M, m => !holds(m, (1 << k) - 1, c.q[0] === 'p' ? { q: base(c), x: c.x, y: c.y } : c));
        const why = (c, j, n) => `Conclusion ${n} (${text(c, T)}): ${c.q[0] === 'p' ? (j.follows ? 'at least one valid diagram has it, so it is possible → follows.' : 'no valid diagram allows it → does not follow.') : j.follows ? 'true in every valid diagram → follows.' : 'some valid diagram breaks it → does not follow.'}`;
        return { question: 'Statements are true even if they seem odd. Which conclusion(s) follow?', clues: stmts.map(s => text(s, T)).concat([`Conclusion I: ${text(I, T)}`, `Conclusion II: ${text(II, T)}`]),
          ...RL.fixed(FIVE, ans), viz: vennViz(k, T, M, null),
          steps: [{ text: 'Draw the minimal diagram: shaded regions must be empty, ✕ regions must have members, ? regions could go either way.', viz: vennViz(k, T, M, null) },
            { text: why(I, ja, 'I'), viz: vennViz(k, T, M, [I.x, I.y], { alt: ja.follows && I.q[0] !== 'p' ? null : ex(I) }) },
            { text: why(II, jb, 'II'), viz: vennViz(k, T, M, [II.x, II.y], { alt: jb.follows && II.q[0] !== 'p' ? null : ex(II) }) },
            { text: ans === FIVE[2] ? 'Neither is certain alone, but they are a complementary pair (one of them must be true), so "either I or II" follows.' : `Answer: ${ans}.`, viz: vennViz(k, T, M, null) }],
          traps: ['"Some A are B" never tells you "Some A are not B".', 'Either-or needs the two conclusions to be about the same two terms, and exactly one of them must be true.', 'A possibility follows only if at least one valid diagram allows it, and it isn\'t already certain.'],
          params: { T, stmts, I, II } }; } return null;
    });
  }
  const DEF = ['all', 'some', 'no', 'somenot'];
  twoConcl('syl-e1', 'easy', 'Two statements, two conclusions', 3, ['all', 'some', 'no'], DEF, false);
  twoConcl('syl-e3', 'easy', 'Either–or pairs', 3, ['all', 'some', 'no'], ['some', 'no', 'all', 'somenot'], true);
  twoConcl('syl-m1', 'medium', 'Possibility conclusions', 3, ['all', 'some', 'no'], ['pall', 'psome', 'some', 'no', 'all'], false);
  twoConcl('syl-m2', 'medium', 'Three statements, four terms', 4, ['all', 'some', 'no'], DEF, true);
  twoConcl('syl-m3', 'medium', '"Only a few" statements', 3, ['few', 'all', 'no', 'some'], ['some', 'somenot', 'all', 'pall', 'psome'], false);
  twoConcl('syl-h1', 'hard', 'Four terms with "only a few" and possibilities', 4, ['few', 'all', 'no', 'some'], ['pall', 'psome', 'some', 'no', 'somenot', 'all'], true);
  RL.reg('syllogism', 'easy', 'syl-e2', 'Which conclusion definitely follows?', ['bank', 'ssc', 'cuet', 'govt'], () => {
    const k = 3, T = sample(NOUNS, k);
    for (let t = 0; t < 300; t++) { const stmts = chainStmts(k, ['all', 'some', 'no']); const M = models(k, stmts); if (!M.length) continue;
      const cs = []; for (let x = 0; x < k; x++) for (let y = 0; y < k; y++) if (x !== y) DEF.forEach(q => cs.push({ q, x, y }));
      const good = shuffle(cs.filter(c => judge(k, stmts, c, M).follows && !stmts.some(s => text(s, T) === text(c, T)))); const bad = shuffle(cs.filter(c => !judge(k, stmts, c, M).follows));
      if (!good.length || bad.length < 3) continue; const c = good[0];
      return { question: 'Which one of the following conclusions definitely follows from the statements?', clues: stmts.map(s => text(s, T)), ...RL.mcq(text(c, T), bad.map(b => text(b, T))), viz: vennViz(k, T, M, null),
        steps: [{ text: 'Draw the forced diagram.', viz: vennViz(k, T, M, null) }, { text: `"${text(c, T)}" is true in every diagram that fits the statements.`, viz: vennViz(k, T, M, [c.x, c.y]) },
          { text: 'Each other option fails in at least one valid diagram.', viz: vennViz(k, T, M, null, { alt: example(k, M, () => true) }) }],
        traps: ['Statements can be reversed: "Some A are B" also means "Some B are A".', '"All A are B" means "Some B are A", but not "All B are A".'], params: { T, stmts } }; } return null;
  });
  RL.reg('syllogism', 'hard', 'syl-h2', 'Reverse: which statements give the conclusions?', ['bank', 'ssc'], () => {
    const k = 3, T = sample(NOUNS, k);
    for (let t = 0; t < 300; t++) { const I = randConcl(k, DEF), II = randConcl(k, DEF); if (text(I, T) === text(II, T)) continue;
      const sets = []; for (let i = 0; i < 40; i++) { const s = chainStmts(k, ['all', 'some', 'no']); if (!models(k, s).length) continue; const key = s.map(x => text(x, T)).join(' '); if (!sets.some(z => z.key === key)) sets.push({ s, key }); }
      const fit = sets.filter(z => { const M = models(k, z.s); return judge(k, z.s, I, M).follows && judge(k, z.s, II, M).follows; }); const no = sets.filter(z => !fit.includes(z));
      if (!fit.length || no.length < 3) continue; const g0 = fit[0]; const M = models(k, g0.s);
      return { question: `Conclusions: I. ${text(I, T)} II. ${text(II, T)} Which pair of statements makes BOTH conclusions follow?`, clues: [`Conclusion I: ${text(I, T)}`, `Conclusion II: ${text(II, T)}`], ...RL.mcq(g0.key, no.map(z => z.key)), viz: vennViz(k, T, M, null),
        steps: [{ text: 'Test each option: draw its diagram and check both conclusions.' }, { text: `With "${g0.key}", both conclusions hold in every valid diagram.`, viz: vennViz(k, T, M, [I.x, I.y]) }],
        traps: ['An option where one conclusion only might be true doesn\'t count.', 'Check both conclusions for every option.'], params: { T, I, II } }; } return null;
  });
  const EIGHT = ['None follows', 'Only I follows', 'Only II follows', 'Only III follows', 'Only I and II follow', 'Only I and III follow', 'Only II and III follow', 'All I, II and III follow'];
  RL.reg('syllogism', 'hard', 'syl-h3', 'Three conclusions', ['bank', 'ssc', 'cuet'], () => {
    const k = 4, T = sample(NOUNS, k);
    for (let t = 0; t < 300; t++) { const stmts = chainStmts(k, ['all', 'some', 'no', 'few']); const M = models(k, stmts); if (!M.length) continue;
      const C = [0, 1, 2].map(() => randConcl(k, ['all', 'some', 'no', 'somenot', 'psome', 'pall'])); if (new Set(C.map(c => text(c, T))).size < 3 || C.some(c => !okPoss(k, stmts, c, M))) continue;
      const f = C.map(c => judge(k, stmts, c, M).follows); const idx = (f[0] ? 1 : 0) + (f[1] ? 2 : 0) + (f[2] ? 4 : 0); const map = [0, 1, 2, 4, 3, 5, 6, 7]; const ans = EIGHT[map[idx]];
      if (idx === 0 && Math.random() < .7) continue;
      const opts = RL.mcq(ans, shuffle(EIGHT.filter(e => e !== ans)), 5);
      return { question: 'Which of the conclusions follow from the statements?', clues: stmts.map(s => text(s, T)).concat(C.map((c, i) => `Conclusion ${['I', 'II', 'III'][i]}: ${text(c, T)}`)), ...opts, viz: vennViz(k, T, M, null),
        steps: [{ text: 'Draw the forced four-set diagram.', viz: vennViz(k, T, M, null) }].concat(C.map((c, i) => ({ text: `${['I', 'II', 'III'][i]}. ${text(c, T)} → ${f[i] ? 'follows' : 'does not follow'}.`, viz: vennViz(k, T, M, [c.x, c.y]) }))),
        traps: ['With four terms, a chain only links neighbouring terms, so the end terms are often undetermined.', '"Only a few A are B" means some A are B AND some A are not B, so "All A being B" is impossible.'], params: { T, stmts, C } }; } return null;
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
