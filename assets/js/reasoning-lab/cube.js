/* Topic: Cube painting & cutting */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle } = RL.u;
  RL.topic('cube', 'Cube Painting & Cutting', '🧊', 'Rotate an n×n×n cube, paint faces, slice layers and count small cubes by painted faces.', '3D Visual Reasoning');
  const FACES = ['top', 'bottom', 'front', 'back', 'left', 'right'];
  const OPP = { top: 'bottom', bottom: 'top', front: 'back', back: 'front', left: 'right', right: 'left' };
  // per-axis classification counts: x→left/right, y→bottom/top, z→front/back
  const AX = [['left', 'right'], ['bottom', 'top'], ['front', 'back']];
  function classify(dims, paint, skipTop) { // returns list of {count, faces:[face], colors:[...]} groups
    const groups = []; const cats = d => d === 1 ? [['both', 1]] : [['lo', 1], ['hi', 1], ['mid', d - 2]].filter(c => c[1] > 0);
    const [a, b, c] = dims;
    for (const cx of cats(a)) for (const cy of cats(b)) for (const cz of cats(c)) {
      const faces = []; [cx, cy, cz].forEach((cat, i) => { if (cat[0] === 'lo' || cat[0] === 'both') faces.push(AX[i][0]); if (cat[0] === 'hi' || cat[0] === 'both') faces.push(AX[i][1]); });
      const pf = faces.filter(f => paint[f]); groups.push({ count: cx[1] * cy[1] * cz[1], faces: pf, colors: pf.map(f => paint[f]) });
    }
    return groups;
  }
  const countK = (dims, paint, k) => classify(dims, paint).filter(g => g.faces.length === k).reduce((s, g) => s + g.count, 0);
  const allPaint = col => Object.fromEntries(FACES.map(f => [f, col]));
  const viz = (dims, paint, hl, extra) => Object.assign({ kind: 'cube3d', dims, paint, hl }, extra || {});
  const word = k => ['no', 'exactly one', 'exactly two', 'exactly three'][k];
  RL.cubeHelpers = { classify, FACES, OPP };

  RL.reg('cube', 'easy', 'cube-e1', 'Painted cube: count by painted faces', ['ssc', 'bank', 'govt', 'cuet'], () => {
    const n = ri(3, 9), k = ri(0, 3), ans = countK([n, n, n], allPaint('brand'), k);
    const f = [(n - 2) ** 3, 6 * (n - 2) ** 2, 12 * (n - 2), 8];
    return { question: `A cube of side ${n} cm is painted on all six faces and then cut into 1 cm cubes. How many small cubes have ${word(k)} painted face${k === 1 ? '' : 's'}?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(6, ans >> 2), f.concat([n ** 3 - ans, ans + 8, 4 * (n - 2), (n - 1) ** 3]))),
      viz: viz([n, n, n], allPaint('brand'), { faces: k }),
      steps: [{ text: `Total small cubes = ${n}³ = ${n ** 3}. Each edge has ${n} cubes; the two end cubes are corners, the ${n - 2} in between are edge cubes.`, viz: viz([n, n, n], allPaint('brand'), null) },
        { text: `3 painted faces → only the 8 corners. 2 painted faces → 12 edges × (${n}−2) = ${f[2]}.`, viz: viz([n, n, n], allPaint('brand'), { faces: k >= 2 ? k : 3 }) },
        { text: `1 painted face → 6 faces × (${n}−2)² = ${f[1]}. 0 painted faces → the hidden core (${n}−2)³ = ${f[0]}.`, viz: viz([n, n, n], allPaint('brand'), { faces: k < 2 ? k : 1 }, { explode: k === 0 }) },
        { text: `So the answer is ${ans}. Check: ${f[3]} + ${f[2]} + ${f[1]} + ${f[0]} = ${n ** 3}.`, viz: viz([n, n, n], allPaint('brand'), { faces: k }, { explode: k === 0 }) }],
      traps: ['Using n instead of (n − 2) for edge and face-centre cubes.', 'Forgetting there are 12 edges and only 8 corners, whatever the size.', 'The 0-painted count is the inner cube (n − 2)³, not n³ minus the painted ones on one face.'],
      params: { n, k } };
  });
  RL.reg('cube', 'easy', 'cube-e2', 'Maximum identical pieces from cuts', ['ssc', 'govt', 'cuet'], () => {
    const c = ri(4, 15), q = Math.floor(c / 3), r = c % 3; const parts = [q, q, q].map((v, i) => v + (i < r ? 1 : 0));
    const ans = parts.reduce((s, v) => s * (v + 1), 1);
    const n0 = Math.round(Math.cbrt(ans));
    return { question: `What is the maximum number of identical pieces a cube can be cut into using ${c} straight cuts, each parallel to a face (pieces are not moved between cuts)?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(6, ans >> 2), [c + 1, (c + 1) ** 2, 2 ** c, ans + parts[0] + 1, (parts[0] + 1) * (parts[1] + 1) * parts[2]])),
      viz: viz(parts.map(v => v + 1), {}, null, { cutsOnly: true }),
      steps: [{ text: `Cuts along one direction add pieces one at a time: x cuts make (x + 1) slabs. With cuts x, y, z in the three directions you get (x+1)(y+1)(z+1) pieces.` },
        { text: `For a fixed total x + y + z = ${c}, the product is largest when the cuts are split as evenly as possible: ${parts.join(' + ')}.`, viz: viz(parts.map(v => v + 1), {}, null, { cutsOnly: true }) },
        { text: `Pieces = ${parts.map(v => v + 1).join(' × ')} = ${ans}.` }],
      traps: ['Putting all cuts in one direction gives only c + 1 pieces.', 'Doubling pieces per cut (2^c) only works if you restack pieces, which is not allowed here.', 'Splitting the cuts unevenly between the three directions gives fewer pieces.'],
      params: { c } };
  });
  RL.reg('cube', 'easy', 'cube-e3', 'At least one painted face', ['ssc', 'bank', 'govt', 'cuet'], () => {
    const n = ri(3, 10), ans = n ** 3 - (n - 2) ** 3;
    return { question: `A painted cube (all faces painted) is cut into ${n ** 3} identical small cubes. How many small cubes have at least one painted face?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(8, ans >> 2), [(n - 2) ** 3, 6 * n * n, 6 * (n - 2) ** 2, ans - 8, n ** 3 - (n - 1) ** 3])),
      viz: viz([n, n, n], allPaint('brand'), { atleast: 1 }),
      steps: [{ text: `${n ** 3} = ${n}³, so each edge is split into ${n} pieces.` },
        { text: `Unpainted cubes form the inner core of side ${n} − 2 = ${n - 2}: (${n - 2})³ = ${(n - 2) ** 3}.`, viz: viz([n, n, n], allPaint('brand'), { faces: 0 }, { explode: true }) },
        { text: `At least one painted face = ${n ** 3} − ${(n - 2) ** 3} = ${ans}.`, viz: viz([n, n, n], allPaint('brand'), { atleast: 1 }) }],
      traps: ['6n² counts the edge and corner cubes more than once.', 'The core has side n − 2, not n − 1: you lose one layer on each side.'], params: { n } };
  });

  RL.reg('cube', 'medium', 'cube-m1', 'Painted cuboid: count by painted faces', ['ssc', 'govt', 'cuet'], () => {
    let d; do { d = [ri(3, 8), ri(3, 8), ri(2, 7)]; } while (d[0] === d[1] && d[1] === d[2]);
    const k = ri(0, 3), ans = countK(d, allPaint('brand'), k); const [a, b, c] = d;
    const parts = [(a - 2) * (b - 2) * (c - 2), 2 * ((a - 2) * (b - 2) + (b - 2) * (c - 2) + (a - 2) * (c - 2)), 4 * ((a - 2) + (b - 2) + (c - 2)), 8];
    return { question: `A cuboid ${a} cm × ${b} cm × ${c} cm is painted on all faces and cut into 1 cm cubes. How many cubes have ${word(k)} painted face${k === 1 ? '' : 's'}?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(6, ans >> 2), parts.concat([a * b * c - ans, ans + 4, ans * 2]))),
      viz: viz(d, allPaint('brand'), { faces: k }),
      steps: [{ text: `Treat each dimension separately: along a length L, 2 cubes are on the ends and L − 2 are inside. Here: ${a - 2}, ${b - 2}, ${c - 2}.`, viz: viz(d, allPaint('brand'), null) },
        { text: `3 faces: 8 corners. 2 faces: 4 edges of each length → 4(${a - 2} + ${b - 2} + ${c - 2}) = ${parts[2]}.`, viz: viz(d, allPaint('brand'), { faces: 2 }) },
        { text: `1 face: 2(${a - 2}×${b - 2} + ${b - 2}×${c - 2} + ${a - 2}×${c - 2}) = ${parts[1]}. 0 faces: ${a - 2}×${b - 2}×${c - 2} = ${parts[0]}.`, viz: viz(d, allPaint('brand'), { faces: k < 2 ? k : 1 }, { explode: k === 0 }) },
        { text: `Answer: ${ans}.`, viz: viz(d, allPaint('brand'), { faces: k }, { explode: k === 0 }) }],
      traps: ['A cuboid has three edge lengths: each appears on 4 edges.', 'Using the cube formula 12(n − 2) with one side only.', 'Opposite faces come in pairs, so the 1-face count is 2 × (sum of the three inner face areas).'], params: { d, k } };
  });
  const SETS = [['top', 'bottom'], ['top', 'front'], ['top', 'bottom', 'front'], ['top', 'front', 'right'], ['front', 'back', 'left', 'right'], ['top', 'bottom', 'front', 'back', 'left']];
  const setTxt = s => s.length === 5 ? `on all faces except the ${FACES.find(f => !s.includes(f))}` : 'only on the ' + s.slice(0, -1).join(', ') + (s.length > 2 ? ',' : '') + ' and ' + s[s.length - 1] + ' faces';
  RL.reg('cube', 'medium', 'cube-m2', 'Partly painted cube', ['ssc', 'govt', 'cuet'], () => {
    const n = ri(3, 7), s = pick(SETS), paint = Object.fromEntries(s.map(f => [f, 'brand'])), maxk = Math.max(...classify([n, n, n], paint).map(g => g.faces.length));
    const k = ri(0, maxk), ans = countK([n, n, n], paint, k);
    const full = countK([n, n, n], allPaint('brand'), k);
    return { question: `A cube of side ${n} is painted ${setTxt(s)}, then cut into ${n ** 3} unit cubes. How many unit cubes have ${word(k)} painted face${k === 1 ? '' : 's'}?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(6, ans >> 1), [full, ans + n, ans - n, ans + 2 * n - 2, n * n, (n - 1) ** 2])),
      viz: viz([n, n, n], paint, { faces: k }),
      steps: [{ text: `Only ${s.length} face${s.length > 1 ? 's are' : ' is'} painted, so the all-faces formula does not apply. Look at which painted faces meet.`, viz: viz([n, n, n], paint, null) },
        { text: `A unit cube's painted-face count = how many painted faces it touches. Cubes on an edge where two painted faces meet get 2; on a corner of three painted faces, 3.`, viz: viz([n, n, n], paint, { faces: Math.min(maxk, 2) }) },
        { text: `Counting layer by layer gives ${ans} cubes with ${word(k)} painted face${k === 1 ? '' : 's'}.`, viz: viz([n, n, n], paint, { faces: k }, { explode: k === 0 }) }],
      traps: ['Applying the all-six-faces formula.', 'Two opposite painted faces never meet, so they create no 2-face cubes.', 'Unpainted faces still have cubes on them: they can have 0 or 1 painted faces.'], params: { n, s, k } };
  });
  const COLS = ['red', 'blue', 'green'];
  RL.reg('cube', 'medium', 'cube-m3', 'Three colours on opposite faces', ['ssc', 'bank', 'govt'], () => {
    const n = ri(3, 7), cs = shuffle(COLS), paint = { top: cs[0], bottom: cs[0], front: cs[1], back: cs[1], left: cs[2], right: cs[2] };
    const v = ri(0, 2); let q, pred, hl;
    if (v === 0) { const c = pick(COLS); q = `have only ${c} paint on them (at least one ${c} face and no other colour)`; pred = g => g.colors.length > 0 && g.colors.every(x => x === c); hl = { colorset: [c] }; }
    else if (v === 1) { const [c1, c2] = shuffle(COLS); q = `have both ${c1} and ${c2} faces but no ${COLS.find(x => x !== c1 && x !== c2)} face`; pred = g => { const s = new Set(g.colors); return s.size === 2 && s.has(c1) && s.has(c2); }; hl = { colorset: [c1, c2] }; }
    else { q = 'show all three colours'; pred = g => new Set(g.colors).size === 3; hl = { ncolors: 3 }; }
    const ans = classify([n, n, n], paint).filter(pred).reduce((s, g) => s + g.count, 0);
    return { question: `A cube of side ${n} has its top and bottom painted ${cs[0]}, front and back painted ${cs[1]}, and left and right painted ${cs[2]}. It is cut into unit cubes. How many unit cubes ${q}?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(6, ans >> 1), [2 * (n - 2) ** 2, 4 * (n - 2), 8, 6 * (n - 2) ** 2, ans * 2, ans + 4])),
      viz: viz([n, n, n], paint, hl),
      steps: [{ text: `Opposite faces share a colour, so a corner shows 3 colours, an edge cube shows the 2 colours of the faces meeting there, and a face-centre cube shows 1.`, viz: viz([n, n, n], paint, null) },
        { text: v === 0 ? `Only-one-colour cubes are the face centres of the two faces of that colour: 2 × (${n}−2)².` : v === 1 ? `Edges where those two colours meet: there are 4 such edges, each with ${n}−2 cubes.` : `Only the 8 corners touch three mutually adjacent faces.`, viz: viz([n, n, n], paint, hl) },
        { text: `Answer: ${ans}.`, viz: viz([n, n, n], paint, hl) }],
      traps: ['Counting all 12 edges instead of the 4 edges where the two chosen colours meet.', 'A corner shows three colours, so it never counts as "only two".'], params: { n, paint, v, q } };
  });

  RL.reg('cube', 'hard', 'cube-h1', 'Painted cube with a layer removed', ['ssc', 'cuet', 'govt'], () => {
    const n = ri(4, 8), k = ri(0, 3);
    // remaining (n-1) layers keep original paint: counts within remaining
    let ans = 0; const g = classify([n, n, n], allPaint('brand'));
    // simulate quickly by layers (y index 0..n-2 kept; top layer y=n-1 removed)
    for (let x = 0; x < n; x++) for (let y = 0; y < n - 1; y++) for (let z = 0; z < n; z++) { const f = (x === 0) + (x === n - 1) + (y === 0) + (z === 0) + (z === n - 1); if (f === k) ans++; }
    const naive = countK([n, n, n], allPaint('brand'), k);
    return { question: `A cube of side ${n} is painted on all faces and cut into unit cubes. The entire top layer of ${n * n} cubes is removed. Among the remaining cubes (counting only the original paint), how many have ${word(k)} painted face${k === 1 ? '' : 's'}?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(6, ans >> 1), [naive, naive - (k === 3 ? 4 : n), ans + 4, ans + n - 2, ans - 4].filter(x => x >= 0))),
      viz: viz([n, n, n], allPaint('brand'), { faces: k }, { removeTop: 1 }),
      steps: [{ text: `Removing the top layer leaves ${n} × ${n} × ${n - 1}. Its top is now an unpainted cut surface, while the other 5 faces keep their paint.`, viz: viz([n, n, n], allPaint('brand'), null, { removeTop: 1 }) },
        { text: `Corners: the 4 bottom corners keep 3 faces; the 4 new top corners only have 2 (the side faces).`, viz: viz([n, n, n], allPaint('brand'), { faces: 3 }, { removeTop: 1 }) },
        { text: `Count each class in the ${n}×${n}×${n - 1} block with 5 painted faces: answer ${ans}.`, viz: viz([n, n, n], allPaint('brand'), { faces: k }, { removeTop: 1, explode: k === 0 }) }],
      traps: ['The newly exposed top surface is not painted.', 'Using the full-cube count, or simply subtracting n² from it.', 'The old second layer\'s edge cubes now sit on the top rim but still have only their original paint.'], params: { n, k } };
  });
  RL.reg('cube', 'hard', 'cube-h2', 'Coloured cuboid: colour combinations', ['ssc', 'cat', 'govt'], () => {
    let d; do { d = [ri(3, 8), ri(3, 8), ri(3, 8)]; } while (new Set(d).size < 2);
    const cs = shuffle(COLS); const paint = { top: cs[0], bottom: cs[0], front: cs[1], back: cs[1], left: cs[2] }; // right unpainted
    const v = ri(0, 2); let q, pred, hl;
    if (v === 0) { q = 'have exactly two colours'; pred = g => new Set(g.colors).size === 2; hl = { ncolors: 2 }; }
    else if (v === 1) { q = 'have no paint at all'; pred = g => g.colors.length === 0; hl = { faces: 0 }; }
    else { q = `have ${cs[2]} paint and exactly one other colour`; pred = g => { const s = new Set(g.colors); return s.size === 2 && s.has(cs[2]); }; hl = { ncolors: 2, has: cs[2] }; }
    const ans = classify(d, paint).filter(pred).reduce((s, g) => s + g.count, 0);
    const [a, b, c] = d;
    return { question: `A cuboid ${a} (left–right) × ${b} (bottom–top) × ${c} (front–back) is painted: top and bottom ${cs[0]}, front and back ${cs[1]}, left face ${cs[2]}; the right face is left unpainted. It is cut into unit cubes. How many unit cubes ${q}?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(6, ans >> 1), [ans + 4, ans + b - 2, ans + a - 2, ans - 2, (a - 2) * (b - 2) * (c - 2), (a - 1) * (b - 2) * (c - 2), 2 * ans])),
      viz: viz(d, paint, hl),
      steps: [{ text: `Classify by position along each axis. Left–right: the left end is ${cs[2]}, the right end is unpainted, and ${a - 2} cubes lie between.`, viz: viz(d, paint, null) },
        { text: v === 1 ? `Unpainted cubes: not on top, bottom, front, back or left. That's (${a - 1}) × (${b - 2}) × (${c - 2}), because the right column is unpainted.` : `Combine one category per axis and keep the cubes whose set of colours matches.`, viz: viz(d, paint, hl) },
        { text: `Total = ${ans}.`, viz: viz(d, paint, hl, { explode: v === 1 }) }],
      traps: ['The unpainted right face means cubes in the right column lose a colour.', 'Mixing up which dimension goes with which pair of faces.', 'Counting by faces rather than by distinct colours: top and bottom are the same colour.'], params: { d, paint, v } };
  });
  RL.reg('cube', 'hard', 'cube-h3', 'Reverse: find the cube from a count', ['ssc', 'cat', 'cuet'], () => {
    const n = ri(4, 12), given = ri(0, 2), ask = pick([0, 1, 2].filter(x => x !== given));
    const f = m => [(m - 2) ** 3, 6 * (m - 2) ** 2, 12 * (m - 2)];
    const gv = f(n)[given], ans = f(n)[ask];
    return { question: `A cube painted on all faces is cut into identical small cubes. If ${gv} small cubes have ${word(given)} painted face${given === 1 ? '' : 's'}, how many have ${word(ask)} painted face${ask === 1 ? '' : 's'}?`,
      ...RL.mcq(String(ans), RL.numDistract(ans, Math.max(6, ans >> 2), [f(n + 1)[ask], f(n - 1)[ask], n ** 3 - gv, gv, f(n)[3 - given - ask]])),
      viz: viz([n, n, n], allPaint('brand'), { faces: ask }, { explode: ask === 0 }),
      steps: [{ text: `Write the given count in terms of n: ${['(n−2)³', '6(n−2)²', '12(n−2)'][given]} = ${gv}.` },
        { text: `Solve: n − 2 = ${n - 2}, so n = ${n} and the cube is ${n}×${n}×${n}.`, viz: viz([n, n, n], allPaint('brand'), { faces: given }, { explode: given === 0 }) },
        { text: `Then ${['(n−2)³', '6(n−2)²', '12(n−2)'][ask]} = ${ans}.`, viz: viz([n, n, n], allPaint('brand'), { faces: ask }, { explode: ask === 0 }) }],
      traps: ['Solving for n − 2 and forgetting to add 2 back.', 'Mixing up 6(n − 2)² (1-face) with 12(n − 2) (2-face).'], params: { n, given, gv, ask } };
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
