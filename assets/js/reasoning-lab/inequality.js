/* Topic: Inequalities (banking style) — direct, combined, coded; checked by trying every weak ordering */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample } = RL.u;
  RL.topic('inequality', 'Inequalities', '⚖️', 'Chains drawn as a path, so you can see whether a definite relation flows from one letter to the other.', 'Logical Reasoning');
  const OPS = ['>', '≥', '=', '<', '≤'], FLIP = { '>': '<', '<': '>', '≥': '≤', '≤': '≥', '=': '=' };
  const ev = (a, op, b) => op === '>' ? a > b : op === '<' ? a < b : op === '≥' ? a >= b : op === '≤' ? a <= b : op === '≠' ? a !== b : a === b;
  // statements: array of tokens [v, op, v, op, v ...]
  const rels = st => { const r = []; for (let i = 1; i < st.length; i += 2) r.push([st[i - 1], st[i], st[i + 1]]); return r; };
  function models(vars, stmts) { const n = vars.length, out = [], val = Array(n).fill(0); const R = stmts.flatMap(rels).map(([a, o, b]) => [vars.indexOf(a), o, vars.indexOf(b)]);
    const at = [...Array(n)].map((_, i) => R.filter(([a, , b]) => Math.max(a, b) === i));
    (function bt(i) { if (i === n) { out.push(val.slice()); return; } for (let v = 0; v < n; v++) { val[i] = v; if (at[i].every(([a, o, b]) => ev(val[a], o, val[b]))) bt(i + 1); } })(0); return out; }
  const holdsAll = (vars, M, c) => M.every(m => ev(m[vars.indexOf(c[0])], c[1], m[vars.indexOf(c[2])]));
  const holdsSome = (vars, M, c) => M.some(m => ev(m[vars.indexOf(c[0])], c[1], m[vars.indexOf(c[2])]));
  RL.ineq = { models, ev };
  const FIVE = ['Only I is true', 'Only II is true', 'Either I or II is true', 'Neither I nor II is true', 'Both I and II are true'];
  function decide(vars, M, I, II) { const a = holdsAll(vars, M, I), b = holdsAll(vars, M, II); if (a && b) return 4; if (a) return 0; if (b) return 1;
    if (I[0] === II[0] && I[2] === II[2] || I[0] === II[2] && I[2] === II[0]) { if (M.every(m => ev(m[vars.indexOf(I[0])], I[1], m[vars.indexOf(I[2])]) !== ev(m[vars.indexOf(II[0])], II[1], m[vars.indexOf(II[2])]))) return 2; } return 3; }
  const related = (vars, M, x, y) => { const i = vars.indexOf(x), j = vars.indexOf(y); return M.every(m => m[i] >= m[j]) || M.every(m => m[i] <= m[j]); };
  function chain(vs, opset) { const t = [vs[0]]; for (let i = 1; i < vs.length; i++) t.push(pick(opset), vs[i]); return t; }
  function mkStmts(nv, two) { const V = sample([...'ABCDEFGHJKLMPQRSTUVWXYZ'], nv); if (!two) return { V, S: [chain(shuffle(V), OPS)] };
    const sh = shuffle(V); const k = ri(3, nv - 1); const c1 = sh.slice(0, k), c2 = [pick(c1)].concat(sh.slice(k)); return { V, S: [chain(c1, OPS), chain(shuffle(c2), OPS)] }; }
  const sTxt = s => s.join(' ');
  const cTxt = c => `${c[0]} ${c[1]} ${c[2]}`;
  const lineViz = (S, hl, extra) => Object.assign({ kind: 'ineq', stmts: S, hl: hl || null }, extra || {});
  function pathExplain(vars, M, c) { const a = holdsAll(vars, M, c); if (a) return `${cTxt(c)} holds in every ordering that fits → true.`; const i = vars.indexOf(c[0]), j = vars.indexOf(c[2]); const m = M.find(m => !ev(m[i], c[1], m[j]));
    return `${cTxt(c)} is not certain: ${c[0]} = ${m[i]}, ${c[2]} = ${m[j]} fits the statements but breaks it.`; }
  function twoType(id, level, name, nv, two, code) {
    RL.reg('inequality', level, id, name, ['bank', 'ssc', 'govt'], () => {
      const target = pick([0, 1, 2, 3, 4, 2]); const CODE = code ? codeMap() : null;
      for (let t = 0; t < 300; t++) { const { V, S } = mkStmts(nv, two); const M = models(V, S); if (!M.length) continue;
        const [x, y] = sample(V, 2), [u, w] = sample(V, 2); let I = [x, pick(OPS.filter(o => o !== '=')), y], II = [u, pick(OPS), w];
        if (target === 2) { const r = related(V, M, x, y); if (!r) continue; const pairs = [['>', '='], ['<', '='], ['≥', '<'], ['≤', '>']]; const [o1, o2] = pick(pairs); I = [x, o1, y]; II = Math.random() < .5 ? [x, o2, y] : [y, FLIP[o2], x]; }
        if (cTxt(I) === cTxt(II)) continue; const ans = decide(V, M, I, II); if (ans !== target && t < 280) continue;
        if (ans === 2 && !related(V, M, I[0], I[2])) continue;
        const show = s => code ? enc(s, CODE) : sTxt(s); const showC = c => code ? enc(c, CODE) : cTxt(c);
        return { question: `${code ? 'Decode the symbols, then decide' : 'Decide'} which conclusion(s) definitely follow from the statement${S.length > 1 ? 's' : ''}.`, clues: (code ? CODE.legend : []).concat(S.map(s => 'Statement: ' + show(s)), [`Conclusion I: ${showC(I)}`, `Conclusion II: ${showC(II)}`]),
          ...RL.fixed(FIVE, FIVE[ans]), viz: lineViz(S),
          steps: (code ? [{ text: `Decode: ${S.map(show).join(' ; ')} → ${S.map(sTxt).join(' ; ')}`, viz: lineViz(S) }] : []).concat([
            { text: `I. ${pathExplain(V, M, I)}`, viz: lineViz(S, [I[0], I[2]]) }, { text: `II. ${pathExplain(V, M, II)}`, viz: lineViz(S, [II[0], II[2]]) },
            { text: ans === 2 ? `Together, I and II cover every possibility for ${I[0]} and ${I[2]}, and they can't both hold, so it's either I or II.` : `Answer: ${FIVE[ans]}.`, viz: lineViz(S, [I[0], I[2]]) }]),
          traps: ['Opposite signs on a path (> then <) break the chain, so no relation follows.', 'Either-or needs the same two letters, the conclusions true one at a time, and together covering all cases.', 'A single ≥ on the path makes the result ≥, not >.'],
          params: { V, S, I, II, code: CODE ? CODE.map : null } }; } return null;
    });
  }
  const DESC = { '>': 'is neither smaller than nor equal to', '≥': 'is not smaller than', '=': 'is neither smaller than nor greater than', '<': 'is neither greater than nor equal to', '≤': 'is not greater than' };
  function codeMap() { const sy = shuffle(['@', '#', '$', '%', '&', '©', '★', 'δ']).slice(0, 5); const map = {}; OPS.forEach((o, i) => map[o] = sy[i]); return { map, legend: OPS.map(o => `'x ${map[o]} y' means x ${DESC[o]} y.`) }; }
  const enc = (toks, C) => toks.map((t, i) => i % 2 ? C.map[t] : t).join(' ');
  twoType('ineq-e1', 'easy', 'Direct chain, two conclusions', 5, false);
  twoType('ineq-e2', 'easy', 'Two combined statements', 6, true);
  twoType('ineq-m1', 'medium', 'Coded inequalities', 5, false, true);
  twoType('ineq-m2', 'medium', 'Combined chains with either–or', 7, true);
  twoType('ineq-h1', 'hard', 'Coded combined statements', 7, true, true);
  // which expression makes the conclusion definitely true
  RL.reg('inequality', 'easy', 'ineq-e3', 'Which expression makes the conclusion true?', ['bank', 'ssc', 'govt'], () => {
    const V = sample([...'ABCDEFGHJKLMPQRSTUVWXYZ'], 4); const [x, y] = sample(V, 2); const op = pick(['>', '<', '≥', '≤']); const C = [x, op, y];
    for (let t = 0; t < 300; t++) { const ex = []; for (let i = 0; i < 25; i++) ex.push(chain(shuffle(V), OPS)); const uniq = [...new Map(ex.map(e => [sTxt(e), e])).values()];
      const good = uniq.filter(e => { const M = models(V, [e]); return M.length && holdsAll(V, M, C); }); const bad = uniq.filter(e => { const M = models(V, [e]); return M.length && !holdsAll(V, M, C); });
      if (!good.length || bad.length < 3) continue; const g0 = good[0];
      return { question: `Which expression makes "${cTxt(C)}" definitely true?`, ...RL.mcq(sTxt(g0), bad.map(sTxt)), viz: lineViz([g0], [x, y]),
        steps: [{ text: `Follow the path from ${x} to ${y} in each option.`, viz: lineViz([g0]) }, { text: `In ${sTxt(g0)} every sign on the path from ${x} to ${y} points the same way, so ${cTxt(C)} is certain.`, viz: lineViz([g0], [x, y]) }, { text: 'Every other option has a reversed sign on the path, or one that is too weak.' }],
        traps: ['For a strict ">" you need at least one strict sign on the path.', 'Letters outside the path don\'t matter.'], params: { V, C } }; } return null;
  });
  RL.reg('inequality', 'medium', 'ineq-m3', 'Fill the blanks with symbols', ['bank', 'ssc'], () => {
    const V = sample([...'ABCDEFGHJKLMPQRSTUVWXYZ'], 5); const C1 = [V[0], pick(['>', '≥', '<', '≤']), V[4]], C2 = [V[1], pick(['>', '≥', '<', '≤', '=']), V[3]]; const known = pick([0, 2]);
    const fill = ops => { const t = [V[0]]; for (let i = 0; i < 4; i++) t.push(ops[i], V[i + 1]); return t; };
    const kop = pick(OPS); const all = []; for (const a of OPS) for (const b of OPS) for (const c of OPS) { const ops = [a, b, c]; ops.splice(known, 0, kop); all.push(ops); }
    const ok = all.filter(o => { const M = models(V, [fill(o)]); return M.length && holdsAll(V, M, C1) && holdsAll(V, M, C2); }); const bad = all.filter(o => { const M = models(V, [fill(o)]); return M.length && !(holdsAll(V, M, C1) && holdsAll(V, M, C2)); });
    if (!ok.length || bad.length < 3) return null; const right = pick(ok); const blanks = o => o.filter((_, i) => i !== known).join(', ');
    const tmpl = fill([0, 1, 2, 3].map(i => i === known ? kop : '__'));
    return { question: `Which symbols, in order, should fill the blanks in "${sTxt(tmpl)}" so that both ${cTxt(C1)} and ${cTxt(C2)} are definitely true?`, ...RL.mcq(blanks(right), shuffle(bad).map(blanks).filter(b => !ok.some(o => blanks(o) === b))),
      viz: lineViz([tmpl]), steps: [{ text: `${cTxt(C1)} needs the whole path ${V[0]}…${V[4]} to point one way.`, viz: lineViz([fill(right)], [V[0], V[4]]) }, { text: `${cTxt(C2)} needs the middle part ${V[1]}…${V[3]} to point that way too.`, viz: lineViz([fill(right)], [V[1], V[3]]) }, { text: `Filling ${blanks(right)} satisfies both.` }],
      traps: ['A single wrong-direction sign breaks the whole chain.', '"=" is always safe for direction but never gives a strict result on its own.'], params: { V, C1, C2, known, kop } };
  });
  const EIGHT = ['None is true', 'Only I is true', 'Only II is true', 'Only III is true', 'Only I and II are true', 'Only I and III are true', 'Only II and III are true', 'All I, II and III are true'];
  RL.reg('inequality', 'hard', 'ineq-h2', 'Three conclusions', ['bank', 'ssc'], () => {
    for (let t = 0; t < 100; t++) { const { V, S } = mkStmts(7, true); const M = models(V, S); if (!M.length) continue; const C = [0, 1, 2].map(() => { const [x, y] = sample(V, 2); return [x, pick(OPS), y]; });
      if (new Set(C.map(cTxt)).size < 3) continue; const f = C.map(c => holdsAll(V, M, c)); const idx = (f[0] ? 1 : 0) + (f[1] ? 2 : 0) + (f[2] ? 4 : 0); if (idx === 0 && Math.random() < .6) continue;
      const ans = EIGHT[[0, 1, 2, 4, 3, 5, 6, 7][idx]];
      return { question: 'Which of the conclusions are definitely true?', clues: S.map(s => 'Statement: ' + sTxt(s)).concat(C.map((c, i) => `Conclusion ${['I', 'II', 'III'][i]}: ${cTxt(c)}`)), ...RL.mcq(ans, shuffle(EIGHT.filter(e => e !== ans)), 5), viz: lineViz(S),
        steps: C.map((c, i) => ({ text: `${['I', 'II', 'III'][i]}. ${pathExplain(V, M, c)}`, viz: lineViz(S, [c[0], c[2]]) })), traps: ['Join the two statements at their common letter.', 'Check every conclusion on its own.'], params: { V, S, C } }; } return null;
  });
  RL.reg('inequality', 'hard', 'ineq-h3', 'Which expression makes both conclusions true?', ['bank', 'ssc'], () => {
    const V = sample([...'ABCDEFGHJKLMPQRSTUVWXYZ'], 6);
    for (let t = 0; t < 200; t++) { const [a, b, c, d] = sample(V, 4); const C = [[a, pick(['>', '≥', '<', '≤']), b], [c, pick(['>', '≥', '<', '≤', '=']), d]];
      const ex = []; for (let i = 0; i < 40; i++) ex.push(chain(shuffle(V), OPS)); const uniq = [...new Map(ex.map(e => [sTxt(e), e])).values()];
      const good = uniq.filter(e => { const M = models(V, [e]); return M.length && C.every(q => holdsAll(V, M, q)); }); const bad = uniq.filter(e => { const M = models(V, [e]); return M.length && !C.every(q => holdsAll(V, M, q)) && C.some(q => holdsAll(V, M, q)); });
      if (!good.length || bad.length < 3) continue;
      return { question: `Which expression makes both "${cTxt(C[0])}" and "${cTxt(C[1])}" definitely true?`, ...RL.mcq(sTxt(good[0]), bad.map(sTxt)), viz: lineViz([good[0]]),
        steps: [{ text: `Check ${cTxt(C[0])} on each path.`, viz: lineViz([good[0]], [a, b]) }, { text: `Check ${cTxt(C[1])}.`, viz: lineViz([good[0]], [c, d]) }, { text: `Only ${sTxt(good[0])} satisfies both; each distractor satisfies just one.` }],
        traps: ['The distractors are built to satisfy ONE conclusion, so check both.', 'Trace the path between the two letters: every sign on it must point the same way.'], params: { V, C } }; } return null;
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
