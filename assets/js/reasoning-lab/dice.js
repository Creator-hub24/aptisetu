/* Topic: Dice (and shared die geometry) */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample, perms } = RL.u;
  RL.topic('dice', 'Dice', '🎲', 'A rotatable 3D die: opposite faces from several views, standard vs non-standard dice, rolling.', '3D Visual Reasoning');
  // die = [T,B,F,K,L,R] (top, bottom, front, back, left, right)
  const tipF = d => [d[3], d[2], d[0], d[1], d[4], d[5]];      // tip towards viewer: top→front
  const tipB = d => [d[2], d[3], d[1], d[0], d[4], d[5]];      // tip away: top→back
  const tipR = d => [d[4], d[5], d[2], d[3], d[1], d[0]];      // tip right: top→right
  const tipL = d => [d[5], d[4], d[2], d[3], d[0], d[1]];      // tip left: top→left
  const spin = d => [d[0], d[1], d[4], d[5], d[3], d[2]];      // turn about vertical: left→front
  function orients(d) { const out = [], seen = new Set(); const st = [d];
    while (st.length) { const x = st.pop(), k = x.join(); if (seen.has(k)) continue; seen.add(k); out.push(x); st.push(tipF(x), spin(x)); } return out; }
  const views = d => orients(d).map(o => [o[0], o[2], o[5]]);
  const hasView = (d, v) => views(d).some(w => w[0] === v[0] && w[1] === v[1] && w[2] === v[2]);
  const opp = (d, x) => { const i = d.indexOf(x); return d[i ^ 1]; };
  const consistent = (labels, vs) => perms(labels).filter(d => vs.every(v => hasView(d, v)));
  const MOVES = { forward: tipF, back: tipB, right: tipR, left: tipL };
  const MOVE_TXT = { forward: 'tips forward (towards you)', back: 'tips backward (away from you)', right: 'tips to the right', left: 'tips to the left' };
  const LABELSETS = [['1', '2', '3', '4', '5', '6'], ['A', 'B', 'C', 'D', 'E', 'F'], ['P', 'Q', 'R', 'S', 'T', 'U'], ['K', 'L', 'M', 'N', 'O', 'W']];
  const vtxt = v => `top ${v[0]}, front ${v[1]}, right ${v[2]}`;
  const viewOpt = v => ({ label: vtxt(v), viz: { kind: 'dieviews', views: [v], small: true } });
  RL.dice = { orients, views, hasView, opp, consistent, tipF, tipB, tipR, tipL, spin, MOVES, MOVE_TXT };
  // standard die with random chirality
  function standard() { const pr = shuffle([[1, 6], [2, 5], [3, 4]]).map(p => shuffle(p)); return [pr[0][0], pr[0][1], pr[1][0], pr[1][1], pr[2][0], pr[2][1]].map(String); }
  const randDie = labs => { const s = shuffle(labs); return s; };
  const die3d = (d, extra) => Object.assign({ kind: 'die3d', die: d }, extra || {});

  RL.reg('dice', 'easy', 'dice-e1', 'Standard die: hidden faces', ['ssc', 'govt', 'cuet'], () => {
    const d = standard(), v = pick(views(d)), ans = 21 - (+v[0] + +v[1] + +v[2]);
    return { question: `A standard die (opposite faces add up to 7) is placed so that ${vtxt(v)} are visible. What is the sum of the three faces you cannot see?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, 5, [+v[0] + +v[1] + +v[2], 21, 7, ans + 1, ans - 1])), viz: { kind: 'dieviews', views: [v] },
      steps: [{ text: `Hidden faces are the opposites of the visible ones: bottom = 7 − ${v[0]}, back = 7 − ${v[1]}, left = 7 − ${v[2]}.` },
        { text: `Sum = 21 − (${v[0]} + ${v[1]} + ${v[2]}) = ${ans}. Shortcut: all six faces add to 21.`, viz: die3d(d) }],
      traps: ['Adding the visible faces instead of the hidden ones.', 'On a standard die 1–6, 2–5 and 3–4 are opposite, so they are never seen together.'], params: { v } };
  });
  function viewsProblem(nViews, labs) {
    for (let t = 0; t < 60; t++) {
      const d = randDie(labs); const vs = sample(views(d), nViews); const C = consistent(labs, vs);
      const det = labs.filter(x => C.every(c => opp(c, x) === opp(d, x)));
      const notShown = labs.filter(x => det.includes(x) && vs.every(v => true));
      if (det.length) return { d, vs, C, x: pick(notShown) };
    }
    return null;
  }
  function oppSteps(d, vs, x) { const seen = new Set(); vs.forEach(v => { if (v.includes(x)) v.forEach(y => y !== x && seen.add(y)); });
    return [{ text: `Faces shown in the same view as ${x} are adjacent to it, never opposite: ${[...seen].join(', ') || 'none directly'}.`, viz: { kind: 'dieviews', views: vs, mark: x } },
      { text: `Line up the views so a common face is in the same place, then read off what sits where. Only one die fits all the views.`, viz: die3d(d, { spin: true }) },
      { text: `So the face opposite ${x} is ${opp(d, x)}.`, viz: die3d(d, { show: [x, opp(d, x)] }) }]; }
  RL.reg('dice', 'easy', 'dice-e2', 'Two views: find the opposite face', ['ssc', 'govt', 'cuet', 'bank'], () => {
    const r = viewsProblem(2, pick(LABELSETS)); if (!r) return null; const { d, vs, x } = r;
    return { question: `Two views of the same die are shown: (1) ${vtxt(vs[0])}; (2) ${vtxt(vs[1])}. Which face is opposite ${x}?`,
      ...RL.mcq(opp(d, x), d.filter(y => y !== x && y !== opp(d, x))), viz: { kind: 'dieviews', views: vs },
      steps: oppSteps(d, vs, x), traps: ['Assuming the faces in the same position in two views must be opposite. That rule only works when the views share a common face.', 'Picking a face that appears next to it in one of the views.'], params: { vs, x } };
  });
  RL.reg('dice', 'easy', 'dice-e3', 'Standard die: one or two tips', ['ssc', 'cuet', 'govt'], () => {
    const d = standard(), o = pick(orients(d)), v = [o[0], o[2], o[5]]; const mv = sample(Object.keys(MOVES), ri(1, 2));
    let s = o; mv.forEach(m => s = MOVES[m](s)); const ans = s[0];
    return { question: `A standard die (opposite faces add up to 7) shows ${vtxt(v)}. It ${mv.map(m => MOVE_TXT[m]).join(', then ')}. Which number is now on top?`,
      ...RL.mcq(ans, ['1', '2', '3', '4', '5', '6'].filter(x => x !== ans)), viz: { kind: 'dieviews', views: [v] },
      steps: [{ text: `Fill in the hidden faces: bottom ${7 - v[0]}, back ${7 - v[1]}, left ${7 - v[2]}.`, viz: die3d(o) },
        ...mv.map((m, i) => { let t = o; mv.slice(0, i + 1).forEach(q => t = MOVES[q](t)); return { text: `It ${MOVE_TXT[m]}: the face that was on the ${({ forward: 'back', back: 'front', right: 'left', left: 'right' })[m]} comes to the top. Top = ${t[0]}.`, viz: die3d(t, { roll: m }) }; })],
      traps: ['Tipping forward brings the BACK face up, not the front.', 'The die moves as a whole, so after the first tip, re-read the new front and right before the second.'], params: { v, mv } };
  });
  RL.reg('dice', 'medium', 'dice-m1', 'Three views: opposite face', ['ssc', 'govt', 'cuet', 'bank'], () => {
    const r = viewsProblem(3, pick(LABELSETS)); if (!r) return null; const { d, vs, x } = r;
    return { question: `Three views of one die: (1) ${vtxt(vs[0])}; (2) ${vtxt(vs[1])}; (3) ${vtxt(vs[2])}. Which face is opposite ${x}?`,
      ...RL.mcq(opp(d, x), d.filter(y => y !== x && y !== opp(d, x))), viz: { kind: 'dieviews', views: vs }, steps: oppSteps(d, vs, x),
      traps: ['A face seen with X in any view is adjacent to it, so cross those off first.', 'Don\'t mix up the views: rotate one so that a shared face lines up.'], params: { vs, x } };
  });
  function pinned(labs, k) { for (let t = 0; t < 80; t++) { const d = randDie(labs); const vs = sample(views(d), k); if (consistent(labs, vs).length === 24) return { d, vs }; } return null; }
  RL.reg('dice', 'medium', 'dice-m2', 'Which view is impossible?', ['ssc', 'cuet', 'govt'], () => {
    const labs = pick(LABELSETS); const r = pinned(labs, 3); if (!r) return null; const { d, vs } = r;
    const all = views(d).filter(v => !vs.some(w => w.join() === v.join())); const good = sample(all, 3);
    let bad = null; for (let t = 0; t < 40 && !bad; t++) { const v = pick(all); const cand = pick([[v[0], v[2], v[1]], [v[0], opp(d, v[1]), v[2]], [v[1], v[0], v[2]]]); if (!hasView(d, cand) && new Set(cand).size === 3) bad = cand; }
    if (!bad) return null;
    return { question: `Three views of a die: (1) ${vtxt(vs[0])}; (2) ${vtxt(vs[1])}; (3) ${vtxt(vs[2])}. Which of the following views is NOT possible for this die?`,
      ...RL.mcq(viewOpt(bad), good.map(viewOpt)), viz: { kind: 'dieviews', views: vs },
      steps: [{ text: 'Use the views to rebuild the whole die: which faces are opposite, and the order they go around each corner.', viz: die3d(d, { spin: true }) },
        { text: `The view ${vtxt(bad)} ${bad.some((x, i) => bad.some((y, j) => j > i && opp(d, x) === y)) ? 'shows two opposite faces together' : 'has the right faces but in mirror order, going round the corner the wrong way'}, so this die can't show it.`, viz: { kind: 'dieviews', views: [bad], mark: bad[0] } }],
      traps: ['A view can have three faces that really are adjacent but still be the mirror image, with the faces going round the corner the wrong way.', 'Checking only for opposite faces and ignoring the order.'], params: { vs } };
  });
  RL.reg('dice', 'medium', 'dice-m3', 'Non-standard die: rolling', ['ssc', 'govt', 'cuet'], () => {
    const labs = pick(LABELSETS), d = randDie(labs), o = pick(orients(d)); const v = [o[0], o[2], o[5]]; const mv = Array.from({ length: ri(3, 4) }, () => pick(Object.keys(MOVES)));
    let s = o; mv.forEach(m => s = MOVES[m](s));
    const pairs = [[o[0], o[1]], [o[2], o[3]], [o[4], o[5]]];
    return { question: `A die has opposite pairs ${pairs.map(p => p.join('–')).join(', ')}. It starts showing ${vtxt(v)}, then ${mv.map(m => MOVE_TXT[m]).join(', then ')}. Which face is on top at the end?`,
      ...RL.mcq(s[0], labs.filter(x => x !== s[0])), viz: die3d(o),
      steps: [{ text: `Start: top ${o[0]}, bottom ${o[1]}, front ${o[2]}, back ${o[3]}, left ${o[4]}, right ${o[5]}.`, viz: die3d(o) },
        ...mv.map((m, i) => { let t = o; mv.slice(0, i + 1).forEach(q => t = MOVES[q](t)); return { text: `Move ${i + 1}: ${MOVE_TXT[m]} → top ${t[0]}, front ${t[2]}, right ${t[5]}.`, viz: die3d(t, { roll: m }) }; })],
      traps: ['Each tip only changes four faces; the two faces on the tipping axis stay put.', 'Moves undo each other in pairs, e.g. forward then back, which is a quick check.'], params: { pairs, v, mv } };
  });
  RL.reg('dice', 'hard', 'dice-h1', 'Views: right face for a given top and front', ['ssc', 'cuet', 'govt'], () => {
    const labs = pick(LABELSETS); const r = pinned(labs, ri(2, 3)); if (!r) return null; const { d, vs } = r;
    const all = views(d).filter(v => !vs.some(w => w.join() === v.join())); const t = pick(all);
    const o = orients(d).find(o => o[0] === t[0] && o[2] === t[1]); const ans = o[5];
    return { question: `Views of a die: ${vs.map((v, i) => `(${i + 1}) ${vtxt(v)}`).join('; ')}. If the die is placed with ${t[0]} on top and ${t[1]} at the front, which face is on the right?`,
      ...RL.mcq(ans, labs.filter(x => x !== ans && x !== t[0] && x !== t[1])), viz: { kind: 'dieviews', views: vs },
      steps: [{ text: 'First work out the opposite pairs, then use one view to fix the order around a corner.', viz: die3d(d, { spin: true }) },
        { text: `Put ${t[0]} on top and turn the die until ${t[1]} faces you. The right face is ${ans}, and the left is its opposite, ${opp(d, ans)}.`, viz: die3d(o) }],
      traps: [`Two faces can sit to the right: ${ans} or its opposite ${opp(d, ans)}. Only the corner order tells you which.`, 'Using the opposite pair alone gives the right pair of faces but not which one is on the right.'], params: { vs, t } };
  });
  RL.reg('dice', 'hard', 'dice-h2', 'Die net: which view is possible?', ['ssc', 'cuet', 'govt'], () => {
    const net = pick(RL.NETS), labs = shuffle(pick(LABELSETS)); const cells = net.map((c, i) => ({ r: c[0], c: c[1], label: labs[i] }));
    const d = RL.foldNet(cells); const good = pick(views(d));
    const bads = []; for (let t = 0; t < 60 && bads.length < 3; t++) { const v = pick(views(d)); const cand = pick([[v[0], v[2], v[1]], [v[0], opp(d, v[1]), v[2]], [v[2], v[1], v[0]], [opp(d, v[0]), v[1], v[2]]]);
      if (!hasView(d, cand) && new Set(cand).size === 3 && !bads.some(b => b.join() === cand.join())) bads.push(cand); }
    if (bads.length < 3) return null;
    return { question: 'The net below is folded into a die with the printed side outside. Which view is possible?',
      ...RL.mcq(viewOpt(good), bads.map(viewOpt)), viz: { kind: 'net', cells },
      steps: [{ text: 'In a net, faces separated by exactly one face in a straight row or column end up opposite.', viz: { kind: 'net', cells, opp: true } },
        { text: 'Fold the net in your head (or watch it fold). Cross off any option showing two opposite faces together.', viz: { kind: 'netfold', cells } },
        { text: `Check the corner order for the rest. Only ${vtxt(good)} matches.`, viz: die3d(d, { spin: true }) }],
      traps: ['Opposite faces can never be seen together.', 'An option can avoid opposite faces and still be the mirror image, so check the order around the corner.'], params: { cells } };
  });
  RL.reg('dice', 'hard', 'dice-h3', 'Die rolled along a path', ['ssc', 'cuet', 'cat'], () => {
    const net = pick(RL.NETS), labs = shuffle(pick(LABELSETS)); const cells = net.map((c, i) => ({ r: c[0], c: c[1], label: labs[i] }));
    const d = RL.foldNet(cells); const o = pick(orients(d)); const v = [o[0], o[2], o[5]];
    const steps = ri(4, 6); const mv = Array.from({ length: steps }, () => pick(['forward', 'right', 'back', 'left']));
    let s = o; const tops = []; mv.forEach(m => { s = MOVES[m](s); tops.push(s[0]); }); const ask = pick(['top', 'bottom']); const ans = ask === 'top' ? s[0] : s[1];
    return { question: `A die is made from the net shown (printed side outside). It starts with ${vtxt(v)} and is then rolled: ${mv.map(m => ({ forward: 'towards you', back: 'away', right: 'right', left: 'left' })[m]).join(', ')}. Which face is at the ${ask} at the end?`,
      ...RL.mcq(ans, labs.filter(x => x !== ans)), viz: { kind: 'net', cells },
      steps: [{ text: `From the net: the opposite pairs are ${[[d[0], d[1]], [d[2], d[3]], [d[4], d[5]]].map(p => p.join('–')).join(', ')}.`, viz: { kind: 'net', cells, opp: true } },
        { text: `Start: top ${o[0]}, front ${o[2]}, right ${o[5]}.`, viz: die3d(o) },
        { text: `After each roll the top is ${tops.join(' → ')}, so the final ${ask} is ${ans}.`, viz: die3d(s, { roll: mv[mv.length - 1] }) }],
      traps: ['Rolling "towards you" brings the back face up.', 'The bottom is always opposite the top, so just track the top.'], params: { cells, v, mv, ask } };
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
