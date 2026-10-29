/* Topic: Paper folding & punching, cube nets */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample } = RL.u;
  RL.topic('folding', 'Paper Folding & Cube Nets', '📄', 'Watch paper fold, get punched and unfold, and see a net fold into a cube.', '3D Visual Reasoning');
  /* ---- hexominoes ---- */
  function norm(cells) { const mr = Math.min(...cells.map(c => c[0])), mc = Math.min(...cells.map(c => c[1]));
    return cells.map(c => [c[0] - mr, c[1] - mc]).sort((a, b) => a[0] - b[0] || a[1] - b[1]); }
  const key = cs => norm(cs).map(c => c.join(',')).join(';');
  function canon(cells) { let best = null; let cs = cells;
    for (let r = 0; r < 4; r++) { cs = cs.map(([a, b]) => [b, -a]); for (const m of [cs, cs.map(([a, b]) => [a, -b])]) { const k = key(m); if (!best || k < best) best = k; } } return best; }
  function hexominoes() { let cur = new Map([[key([[0, 0]]), [[0, 0]]]]);
    for (let n = 1; n < 6; n++) { const nx = new Map(); for (const cs of cur.values()) for (const [r, c] of cs) for (const [dr, dc] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const p = [r + dr, c + dc]; if (cs.some(q => q[0] === p[0] && q[1] === p[1])) continue; const ncs = norm(cs.concat([p])); const k = canon(ncs); if (!nx.has(k)) nx.set(k, ncs); } cur = nx; }
    return [...cur.values()]; }
  // fold via rolling: returns die [T,B,F,K,L,R] with print outside, or null if cells overlap
  const tip = { e: d => [d[4], d[5], d[2], d[3], d[1], d[0]], w: d => [d[5], d[4], d[2], d[3], d[0], d[1]], n: d => [d[2], d[3], d[1], d[0], d[4], d[5]], s: d => [d[3], d[2], d[0], d[1], d[4], d[5]] };
  function foldIds(cells) { const at = new Map(cells.map((c, i) => [c.r + ',' + c.c, i])); const face = new Array(cells.length); const seen = new Set();
    (function go(i, D) { seen.add(i); face[i] = D[1]; const { r, c } = cells[i];
      for (const [dir, dr, dc] of [['e', 0, 1], ['w', 0, -1], ['n', -1, 0], ['s', 1, 0]]) { const j = at.get((r + dr) + ',' + (c + dc)); if (j !== undefined && !seen.has(j)) go(j, tip[dir](D)); } })(0, [0, 1, 2, 3, 4, 5]);
    return face; }
  RL.isNet = cs => { const f = foldIds(cs.map(([r, c]) => ({ r, c }))); return new Set(f).size === 6; };
  RL.foldNet = function (cells) { const f = foldIds(cells); if (new Set(f).size !== 6) return null; const lab = []; f.forEach((id, i) => lab[id] = cells[i].label);
    return [lab[1], lab[0], lab[2], lab[3], lab[4], lab[5]]; };
  const HEX = hexominoes(); RL.NETS = HEX.filter(RL.isNet); RL.NONNETS = HEX.filter(h => !RL.isNet(h));
  const randomOrient = cs => { let x = cs; for (let i = ri(0, 3); i > 0; i--) x = x.map(([a, b]) => [b, -a]); if (ri(0, 1)) x = x.map(([a, b]) => [a, -b]); return norm(x); };
  const LAB = [['A', 'B', 'C', 'D', 'E', 'F'], ['1', '2', '3', '4', '5', '6'], ['P', 'Q', 'R', 'S', 'T', 'U'], ['G', 'H', 'J', 'K', 'M', 'N']];
  const labelled = () => { const net = randomOrient(pick(RL.NETS)), labs = shuffle(pick(LAB)); return net.map((c, i) => ({ r: c[0], c: c[1], label: labs[i] })); };
  const opp = (d, x) => d[d.indexOf(x) ^ 1];

  /* ---- paper folding ---- */
  // fold codes: L (left half over right), R (right over left), T (top over bottom), B (bottom over top)
  const FOLD_TXT = { L: 'the left half is folded over onto the right half', R: 'the right half is folded over onto the left half', T: 'the top half is folded down onto the bottom half', B: 'the bottom half is folded up onto the top half' };
  function regions(N, folds) { const rs = [{ x0: 0, x1: N, y0: 0, y1: N }]; for (const f of folds) { const r = Object.assign({}, rs[rs.length - 1]); const mx = (r.x0 + r.x1) / 2, my = (r.y0 + r.y1) / 2;
    if (f === 'L') r.x0 = mx; if (f === 'R') r.x1 = mx; if (f === 'T') r.y0 = my; if (f === 'B') r.y1 = my; rs.push(r); } return rs; }
  function unfold(N, folds, punches) { const rs = regions(N, folds); let H = punches.map(p => p.slice());
    for (let i = folds.length - 1; i >= 0; i--) { const r = rs[i], f = folds[i]; const ref = (f === 'L' || f === 'R') ? ([x, y]) => [r.x0 + r.x1 - 1 - x, y] : ([x, y]) => [x, r.y0 + r.y1 - 1 - y];
      H = H.concat(H.map(ref)); }
    const s = new Set(H.map(h => h.join(','))); return [...s].map(k => k.split(',').map(Number)).sort((a, b) => a[1] - b[1] || a[0] - b[0]); }
  const pkey = H => H.map(h => h.join(',')).sort().join(';');
  const patOpt = (N, H) => ({ label: 'Holes at ' + H.map(([x, y]) => String.fromCharCode(65 + x) + (y + 1)).join(' '), key: pkey(H), viz: { kind: 'paper', N, holes: H, small: true } });
  RL.paper = { regions, unfold, FOLD_TXT };
  function paperProblem(N, nf, np) {
    let folds; do { folds = []; let w = N, h = N; for (let i = 0; i < nf; i++) { const opts = []; if (w > 1) opts.push('L', 'R'); if (h > 1) opts.push('T', 'B'); const f = pick(opts); folds.push(f); if (f === 'L' || f === 'R') w /= 2; else h /= 2; } }
    while (nf >= 2 && new Set(folds.map(f => 'LR'.includes(f) ? 'v' : 'h')).size < 2 && Math.random() < .7);
    const rs = regions(N, folds), r = rs[rs.length - 1]; const cellsIn = []; for (let x = r.x0; x < r.x1; x++) for (let y = r.y0; y < r.y1; y++) cellsIn.push([x, y]);
    if (cellsIn.length < np) return null;
    const punches = sample(cellsIn, np); const H = unfold(N, folds, punches);
    const ds = []; const add = h => { if (!h.length || h.some(([x, y]) => x < 0 || y < 0 || x >= N || y >= N)) return; if (pkey(h) !== pkey(H) && !ds.some(d => pkey(d) === pkey(h))) ds.push(h); };
    if (folds.length > 1) add(unfold(N, folds.slice(1), punches.filter(p => true)));
    add(unfold(N, folds.map(f => ({ L: 'T', R: 'B', T: 'L', B: 'R' })[f]), punches.map(([x, y]) => [y, x])).map(([x, y]) => [y, x]).map(([x, y]) => [N - 1 - x, y]));
    add(H.map(([x, y]) => [N - 1 - x, y])); add(H.map(([x, y]) => [x, N - 1 - y])); add(H.map(([x, y]) => [y, x])); add(punches);
    add(H.filter((h, i) => i % 2 === 0)); add(H.map(([x, y]) => [(x + 1) % N, y]));
    if (ds.length < 3) return null;
    const steps = [{ text: `Start with a square sheet (${N}×${N} grid). ${folds.map((f, i) => `Fold ${i + 1}: ${FOLD_TXT[f]}.`).join(' ')}`, viz: { kind: 'paperfold', N, folds, punches, stage: 'fold' } },
      { text: `A hole is punched through every layer at the marked spot${np > 1 ? 's' : ''}: ${2 ** nf} layers, so each punch makes ${2 ** nf} holes.`, viz: { kind: 'paperfold', N, folds, punches, stage: 'punch' } },
      { text: 'Unfold in reverse order. Each unfold mirrors the holes across that fold line.', viz: { kind: 'paperfold', N, folds, punches, stage: 'unfold' } },
      { text: `Final pattern: ${H.length} holes, symmetric about every fold line.`, viz: { kind: 'paper', N, holes: H } }];
    return { folds, punches, H, ds, steps, N };
  }
  const paperQ = (P) => `A square sheet of paper is folded: ${P.folds.map((f, i) => `(${i + 1}) ${FOLD_TXT[f]}`).join('; ')}. Then ${P.punches.length > 1 ? P.punches.length + ' holes are' : 'a hole is'} punched as shown. Which pattern appears when the sheet is unfolded?`;
  function paperType(id, level, N, nf, np, name) {
    RL.reg('folding', level, id, name, ['ssc', 'cuet', 'govt', 'bank'], () => { const P = paperProblem(N, nf, np); if (!P) return null;
      return { question: paperQ(P), ...RL.mcq(patOpt(N, P.H), shuffle(P.ds).map(h => patOpt(N, h))), viz: { kind: 'paperfold', N, folds: P.folds, punches: P.punches, stage: 'punch' }, steps: P.steps,
        traps: ['Mirroring across the wrong fold line: unfold the LAST fold first.', 'Forgetting a layer. Every fold doubles the number of holes.', 'Holes stay the same distance from a fold line on both sides.'], params: { N, folds: P.folds, punches: P.punches } }; });
  }
  paperType('fold-e2', 'easy', 4, 1, 1, 'One fold, one punch: unfolded pattern');
  paperType('fold-m1', 'medium', 4, 2, 1, 'Two folds: unfolded pattern');
  paperType('fold-h1', 'hard', 8, 3, 2, 'Three folds, two punches: unfolded pattern');

  const netQ = 'The net below folds into a cube (printed side outside).';
  RL.reg('folding', 'easy', 'fold-e1', 'Net: face opposite to a given face', ['ssc', 'cuet', 'govt'], () => {
    const cells = labelled(), d = RL.foldNet(cells), x = pick(d);
    return { question: `${netQ} Which face is opposite ${x}?`, ...RL.mcq(opp(d, x), d.filter(y => y !== x && y !== opp(d, x))), viz: { kind: 'net', cells },
      steps: [{ text: 'Two faces in the same straight row or column with exactly one face between them become opposite.', viz: { kind: 'net', cells, opp: true, mark: x } },
        { text: 'Watch the net fold to check.', viz: { kind: 'netfold', cells, mark: x } }, { text: `${x} is opposite ${opp(d, x)}.`, viz: { kind: 'die3d', die: d, show: [x, opp(d, x)] } }],
      traps: ['Faces that touch in the net, even just at a corner after folding, are adjacent and not opposite.', 'The "one gap" rule only works in a straight line. Around bends, trace the fold.'], params: { cells, x } };
  });
  RL.reg('folding', 'easy', 'fold-e3', 'Which shape folds into a cube?', ['ssc', 'cuet', 'govt'], () => {
    const good = randomOrient(pick(RL.NETS)); const bads = sample(RL.NONNETS, 6).map(randomOrient);
    const opt = cs => ({ label: 'Shape ' + norm(cs).map(([r, c]) => String.fromCharCode(65 + c) + (r + 1)).join(' '), key: key(cs), viz: { kind: 'net', cells: cs.map(([r, c]) => ({ r, c, label: '' })), small: true } });
    return { question: 'Which of these six-square shapes can be folded into a closed cube?', ...RL.mcq(opt(good), bads.map(opt)), viz: { kind: 'note', text: 'There are exactly 11 different cube nets.' },
      steps: [{ text: 'Rule-out checks: a 2×2 block of squares can never fold (two faces would overlap), and a straight run of 5 or more is impossible.' },
        { text: 'Fold the remaining shape: every square must land on a different face.', viz: { kind: 'netfold', cells: good.map(([r, c], i) => ({ r, c, label: 'ABCDEF'[i] })) } }],
      traps: ['Any 2×2 block means two squares fold onto the same face.', 'A straight run of five squares wraps round past the start and overlaps itself.'], params: { good } };
  });
  RL.reg('folding', 'medium', 'fold-m2', 'Net: which pair is opposite?', ['ssc', 'cuet', 'govt'], () => {
    const cells = labelled(), d = RL.foldNet(cells); const pairs = [[d[0], d[1]], [d[2], d[3]], [d[4], d[5]]]; const good = pick(pairs);
    const bad = []; for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) { const a = d[i], b = d[j]; if (opp(d, a) !== b) bad.push([a, b]); }
    const lab = p => p.slice().sort().join(' and ');
    return { question: `${netQ} Which pair of faces will be opposite each other?`, ...RL.mcq(lab(good), shuffle(bad).map(lab)), viz: { kind: 'net', cells },
      steps: [{ text: 'Find the faces that end up opposite: one gap apart in a straight line, or traced through the fold.', viz: { kind: 'net', cells, opp: true } },
        { text: `The opposite pairs are ${pairs.map(lab).join('; ')}.`, viz: { kind: 'netfold', cells } }],
      traps: ['Neighbouring squares in the net are always adjacent on the cube.', 'Squares that touch at a corner in the net are usually adjacent after folding.'], params: { cells } };
  });
  RL.reg('folding', 'medium', 'fold-m3', 'Net: three faces meeting at a corner', ['ssc', 'cuet', 'govt'], () => {
    const cells = labelled(), d = RL.foldNet(cells); const v = pick(RL.dice.views(d)); const good = v.slice().sort().join(', ');
    const bads = []; for (let t = 0; t < 40; t++) { const a = pick(d); const b = opp(d, a); const c = pick(d.filter(x => x !== a && x !== b)); bads.push([a, b, c].sort().join(', ')); }
    return { question: `${netQ} Which three faces meet at one corner of the cube?`, ...RL.mcq(good, bads), viz: { kind: 'net', cells },
      steps: [{ text: 'Three faces meet at a corner only if no two of them are opposite.', viz: { kind: 'net', cells, opp: true } }, { text: `Every option except ${good} contains an opposite pair.`, viz: { kind: 'netfold', cells } }],
      traps: ['Checking only two of the three pairs.', 'Faces that are far apart in the net can still be adjacent after folding.'], params: { cells } };
  });
  RL.reg('folding', 'hard', 'fold-h2', 'Net: which cube view is NOT possible?', ['ssc', 'cuet', 'govt'], () => {
    const cells = labelled(), d = RL.foldNet(cells); const vs = sample(RL.dice.views(d), 3);
    let bad = null; for (let t = 0; t < 40 && !bad; t++) { const v = pick(RL.dice.views(d)); const c = [v[0], v[2], v[1]]; if (!RL.dice.hasView(d, c)) bad = c; }
    const vo = v => ({ label: `top ${v[0]}, front ${v[1]}, right ${v[2]}`, viz: { kind: 'dieviews', views: [v], small: true } });
    return { question: `${netQ} Which of these views of the cube is NOT possible?`, ...RL.mcq(vo(bad), vs.map(vo)), viz: { kind: 'net', cells },
      steps: [{ text: 'All four options avoid opposite faces, so you have to check the order of the faces round the corner.', viz: { kind: 'net', cells, opp: true } },
        { text: 'Fold the net and look at each corner.', viz: { kind: 'netfold', cells } },
        { text: `${vo(bad).label} is the mirror image of a real corner, so it can't happen.`, viz: { kind: 'die3d', die: d, spin: true } }],
      traps: ['Opposite-face checks alone don\'t settle it, because the fake view is a mirror image.', 'Reading the net from the back reverses the order.'], params: { cells } };
  });
  RL.reg('folding', 'hard', 'fold-h3', 'How many shapes are cube nets?', ['ssc', 'cuet', 'cat'], () => {
    const n = 5, k = ri(1, 4); const shapes = shuffle(sample(RL.NETS, k).concat(sample(RL.NONNETS, n - k))).map(randomOrient);
    const cells = shapes.map((s, si) => s.map(([r, c]) => ({ r, c, label: String.fromCharCode(97 + si) })));
    return { question: 'How many of the five shapes below can be folded into a closed cube?', ...RL.mcq(String(k), ['0', '1', '2', '3', '4', '5'].filter(x => x !== String(k))), viz: { kind: 'nets', shapes: cells },
      steps: [{ text: 'Rule out any shape with a 2×2 block, a straight run of 5 or more, or a run of 4 with two squares on the same side.', viz: { kind: 'nets', shapes: cells, mark: true } },
        { text: `Fold the rest. ${k} of them close into a cube.`, viz: { kind: 'nets', shapes: cells, mark: true, reveal: true } }],
      traps: ['Some valid nets look odd, like the 2-2-2 staircase or the 3-3 step.', 'A shape with a 2×2 block can never be a net.'], params: { shapes } };
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
