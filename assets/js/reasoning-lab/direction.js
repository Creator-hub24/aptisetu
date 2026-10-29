/* Topic: Direction sense — paths, turns, shadows, coded directions */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle } = RL.u;
  RL.topic('direction', 'Direction Sense', '🧭', 'Each walk is drawn step by step on a map, ending with the straight-line distance and direction from the start.', 'Logical Reasoning');
  const D4 = ['north', 'east', 'south', 'west'], V = { north: [0, 1], east: [1, 0], south: [0, -1], west: [-1, 0] };
  const D8 = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West'];
  const cap = s => s[0].toUpperCase() + s.slice(1);
  const dname = (dx, dy) => dx === 0 && dy === 0 ? 'Same point' : (dy > 0 ? 'North' : dy < 0 ? 'South' : '') + (dx && dy ? '-' : '') + (dx > 0 ? 'East' : dx < 0 ? 'West' : '');
  const dist = (dx, dy) => Math.sqrt(dx * dx + dy * dy);
  const isInt = x => Math.abs(x - Math.round(x)) < 1e-9;
  RL.dirs = { dname, D8 };
  const pathViz = (pts, extra) => Object.assign({ kind: 'path', pts }, extra || {});
  const distOpts = (d, dx, dy) => RL.numDistract(d, Math.max(4, d >> 1), [Math.abs(dx) + Math.abs(dy), Math.abs(dx), Math.abs(dy), d + 2, d - 1].filter(v => v > 0)).map(v => v + ' m');
  function absWalk(nseg, wantInt) {
    for (let t = 0; t < 400; t++) { const segs = []; let x = 0, y = 0, prev = null; const pts = [[0, 0]];
      for (let i = 0; i < nseg; i++) { let d; do d = pick(D4); while (d === prev || (prev && V[d][0] === -V[prev][0] && V[d][1] === -V[prev][1])); const L = ri(2, 15); segs.push([d, L]); x += V[d][0] * L; y += V[d][1] * L; pts.push([x, y]); prev = d; }
      if (x === 0 && y === 0) continue; const D = dist(x, y); if (wantInt && !isInt(D)) continue; if (wantInt === 'diag' && (x === 0 || y === 0)) continue; return { segs, x, y, D: Math.round(D), pts }; } return null; }
  RL.reg('direction', 'easy', 'dir-e1', 'Walk: distance from start', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const W = absWalk(ri(3, 4), 'diag'); if (!W) return null; const N = pick(['Asha', 'Rohan', 'Tara', 'Kabir', 'Isha']);
    return { question: `${N} walks ${W.segs.map(([d, l]) => `${l} m ${d}`).join(', then ')}. How far is ${N} from the starting point?`, ...RL.mcq(W.D + ' m', distOpts(W.D, W.x, W.y)), viz: pathViz([[0, 0]]),
      steps: W.segs.map((s, i) => ({ text: `Walk ${s[1]} m ${s[0]}.`, viz: pathViz(W.pts.slice(0, i + 2)) })).concat([{ text: `Net: ${Math.abs(W.x)} m ${W.x > 0 ? 'east' : 'west'} and ${Math.abs(W.y)} m ${W.y > 0 ? 'north' : 'south'}. Distance = √(${W.x * W.x} + ${W.y * W.y}) = ${W.D} m.`, viz: pathViz(W.pts, { final: true }) }]),
      traps: ['Adding up every step gives the distance walked, not the distance from the start.', 'Cancel opposite moves (north against south, east against west) before using Pythagoras.'], params: { segs: W.segs } };
  });
  const TURNS = { right: 1, left: -1, back: 2 };
  RL.reg('direction', 'easy', 'dir-e2', 'Turns: final facing direction', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const s = ri(0, 3), n = ri(3, 5), turns = Array.from({ length: n }, () => pick(['right', 'left', 'right', 'left', 'back'])); let f = s; turns.forEach(t => f = (f + TURNS[t] + 4) % 4);
    return { question: `A girl faces ${D4[s]}. She turns ${turns.map(t => t === 'back' ? 'about (180°)' : t).join(', then ')}. Which direction does she face now?`, ...RL.mcq(cap(D4[f]), D4.filter((_, i) => i !== f).map(cap)),
      viz: { kind: 'compass', face: s }, steps: turns.map((t, i) => { let q = s; turns.slice(0, i + 1).forEach(u => q = (q + TURNS[u] + 4) % 4); return { text: `Turn ${t === 'back' ? 'about' : t} → now facing ${D4[q]}.`, viz: { kind: 'compass', face: q } }; }),
      traps: ['Right means clockwise: north → east → south → west.', 'A left then a right cancel out, so pair them off quickly.'], params: { s, turns } };
  });
  RL.reg('direction', 'easy', 'dir-e3', 'Walk: direction from start', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const W = absWalk(ri(3, 4), false); if (!W) return null; const nm = dname(W.x, W.y);
    return { question: `A man walks ${W.segs.map(([d, l]) => `${l} m ${d}`).join(', then ')}. In which direction is he from the starting point?`, ...RL.mcq(nm, shuffle(D8.filter(d => d !== nm))), viz: pathViz([[0, 0]]),
      steps: W.segs.map((s, i) => ({ text: `${s[1]} m ${s[0]}.`, viz: pathViz(W.pts.slice(0, i + 2)) })).concat([{ text: `Net displacement: x = ${W.x}, y = ${W.y}. So he is ${nm} of the start.`, viz: pathViz(W.pts, { final: true }) }]),
      traps: ['The question asks where HE is relative to the start, not where the start is relative to him.', 'If either net east-west or net north-south is zero, the answer is a pure direction, not a diagonal.'], params: { segs: W.segs } };
  });
  function relWalk(n, start) { for (let t = 0; t < 400; t++) { let f = start, x = 0, y = 0; const ops = [], pts = [[0, 0]];
      for (let i = 0; i < n; i++) { const turn = i ? pick(['left', 'right']) : null; if (turn) f = (f + TURNS[turn] + 4) % 4; const L = ri(2, 14); ops.push([turn, L]); x += V[D4[f]][0] * L; y += V[D4[f]][1] * L; pts.push([x, y]); }
      const D = dist(x, y); if (x === 0 || y === 0 || !isInt(D)) continue; return { ops, x, y, D: Math.round(D), pts, end: f }; } return null; }
  const relTxt = (st, ops) => `starts facing ${D4[st]} and walks ${ops[0][1]} m, ` + ops.slice(1).map(([t, l]) => `turns ${t} and walks ${l} m`).join(', ');
  RL.reg('direction', 'medium', 'dir-m1', 'Relative turns: distance and direction', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const st = ri(0, 3), W = relWalk(ri(4, 5), st); if (!W) return null; const nm = dname(W.x, W.y); const ans = `${W.D} m, ${nm}`;
    const ds = [`${W.D} m, ${dname(-W.x, -W.y)}`, `${W.D} m, ${dname(-W.x, W.y)}`, `${W.D} m, ${dname(W.x, -W.y)}`, `${Math.abs(W.x) + Math.abs(W.y)} m, ${nm}`, `${W.D + 2} m, ${nm}`];
    return { question: `A cyclist ${relTxt(st, W.ops)}. How far and in which direction is the cyclist from the starting point?`, ...RL.mcq(ans, ds), viz: pathViz([[0, 0]]),
      steps: W.ops.map((o, i) => { let f = st; W.ops.slice(0, i + 1).forEach(q => { if (q[0]) f = (f + TURNS[q[0]] + 4) % 4; }); return { text: `${o[0] ? 'Turn ' + o[0] + ' → face ' + D4[f] + ', ' : 'Facing ' + D4[st] + ', '}walk ${o[1]} m.`, viz: pathViz(W.pts.slice(0, i + 2), { face: f }) }; })
        .concat([{ text: `Net: ${Math.abs(W.x)} m ${W.x >= 0 ? "east" : "west"}, ${Math.abs(W.y)} m ${W.y >= 0 ? "north" : "south"} → ${W.D} m, ${nm}.`, viz: pathViz(W.pts, { final: true }) }]),
      traps: ['Left and right depend on the direction you are facing at that moment.', 'Drawing the path is quicker than tracking it in your head.', 'Check the sign: a negative x means west.'], params: { st, ops: W.ops } };
  });
  RL.reg('direction', 'medium', 'dir-m2', 'Shadows and the sun', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const time = pick(['morning', 'evening']); const side = pick(['left', 'right', 'front', 'back']); const name = pick(['Vikram', 'Nisha', 'Om', 'Lata']);
    const shadow = time === 'morning' ? 3 : 1; // morning sun east → shadow west(3); evening → east(1)
    const off = { front: 0, right: 1, back: 2, left: -1 }[side]; const face = (shadow - off + 4) % 4;
    return { question: `One ${time}, ${name} noticed that ${name.match(/a$/) ? 'her' : 'his'} shadow pointed straight out to ${name.match(/a$/) ? 'her' : 'his'} ${side}. Which direction was ${name} facing?`, ...RL.mcq(cap(D4[face]), D4.filter((_, i) => i !== face).map(cap)),
      viz: { kind: 'sun', time, face, side }, steps: [{ text: `In the ${time} the sun is in the ${time === 'morning' ? 'east' : 'west'}, so shadows fall ${D4[shadow]}.`, viz: { kind: 'sun', time, face: null, side } },
        { text: `The shadow (${D4[shadow]}) is on the person's ${side}, so they face ${D4[face]}.`, viz: { kind: 'sun', time, face, side } }],
      traps: ['Shadows point AWAY from the sun.', 'At noon there is almost no shadow, which is why these questions use morning or evening.'], params: { time, side } };
  });
  const PTS = ['P', 'Q', 'R', 'S', 'T', 'U'];
  function pointChain(n) { for (let t = 0; t < 300; t++) { const P = PTS.slice(0, n); const pos = { [P[0]]: [0, 0] }; const facts = [];
      for (let i = 1; i < n; i++) { const ref = P[ri(0, i - 1)], d = pick(D4), L = ri(2, 12); pos[P[i]] = [pos[ref][0] + V[d][0] * L, pos[ref][1] + V[d][1] * L]; facts.push([P[i], L, d, ref]); }
      const [a, b] = shuffle(P).slice(0, 2); const dx = pos[a][0] - pos[b][0], dy = pos[a][1] - pos[b][1]; const D = dist(dx, dy);
      if (!dx || !dy || !isInt(D) || facts.some(f => (f[0] === a && f[3] === b) || (f[0] === b && f[3] === a))) continue;
      if (new Set(Object.values(pos).map(p => p.join())).size < n) continue; return { pos, facts, a, b, dx, dy, D: Math.round(D) }; } return null; }
  RL.reg('direction', 'medium', 'dir-m3', 'Positions of points', ['ssc', 'bank', 'cuet', 'cat'], () => {
    const C = pointChain(5); if (!C) return null; const nm = dname(C.dx, C.dy);
    const pts = Object.entries(C.pos);
    return { question: `${C.facts.map(([p, l, d, r]) => `${p} is ${l} m ${d} of ${r}`).join('. ')}. How far is ${C.a} from ${C.b}, and in which direction?`, clues: C.facts.map(([p, l, d, r]) => `${p} is ${l} m ${d} of ${r}.`),
      ...RL.mcq(`${C.D} m, ${nm}`, [`${C.D} m, ${dname(-C.dx, -C.dy)}`, `${Math.abs(C.dx) + Math.abs(C.dy)} m, ${nm}`, `${C.D} m, ${dname(C.dx, -C.dy)}`, `${C.D + 1} m, ${nm}`]),
      viz: { kind: 'points', pts: [[C.facts.length ? PTS[0] : 'P', 0, 0]], links: [] },
      steps: C.facts.map((f, i) => ({ text: `Place ${f[0]}: ${f[1]} m ${f[2]} of ${f[3]}.`, viz: { kind: 'points', pts: pts.slice(0, i + 2).map(([k, p]) => [k, p[0], p[1]]), links: C.facts.slice(0, i + 1).map(f => [f[0], f[3]]) } }))
        .concat([{ text: `${C.a} − ${C.b}: x ${C.dx}, y ${C.dy} → √(${C.dx ** 2} + ${C.dy ** 2}) = ${C.D} m, ${nm}.`, viz: { kind: 'points', pts: pts.map(([k, p]) => [k, p[0], p[1]]), links: C.facts.map(f => [f[0], f[3]]), hl: [C.a, C.b] } }]),
      traps: ['"A is north of B" places A ABOVE B. Don\'t reverse the reference.', 'Direction "of A from B" means stand at B and look towards A.'], params: { facts: C.facts, a: C.a, b: C.b } };
  });
  RL.reg('direction', 'hard', 'dir-h1', 'Degree turns (45° steps)', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const s = ri(0, 7); const n = ri(3, 5); const turns = Array.from({ length: n }, () => [pick([45, 90, 135, 180, 225, 270]), pick(['clockwise', 'anticlockwise'])]);
    let f = s; turns.forEach(([d, w]) => f = (f + (w === 'clockwise' ? 1 : -1) * d / 45 + 80) % 8);
    return { question: `A pointer faces ${D8[s]}. It turns ${turns.map(([d, w]) => `${d}° ${w}`).join(', then ')}. Which direction does it face now?`, ...RL.mcq(D8[f], shuffle(D8.filter((_, i) => i !== f))),
      viz: { kind: 'compass8', face: s }, steps: [{ text: 'Count in 45° steps: clockwise is +1 step, anticlockwise is −1.', viz: { kind: 'compass8', face: s } },
        { text: `Net turn = ${turns.map(([d, w]) => (w === 'clockwise' ? '+' : '−') + d).join(' ')} = ${turns.reduce((a, [d, w]) => a + (w === 'clockwise' ? d : -d), 0)}°.`, viz: { kind: 'compass8', face: f } },
        { text: `${D8[s]} turned by that amount → ${D8[f]}.`, viz: { kind: 'compass8', face: f } }],
      traps: ['Add the turns as signed angles first, then convert, instead of turning step by step.', 'Anything above 360° wraps around.'], params: { s, turns } };
  });
  RL.reg('direction', 'hard', 'dir-h2', 'Coded directions', ['bank', 'ssc'], () => {
    const syms = shuffle(['@', '#', '$', '%', '&', '★']).slice(0, 4); const code = Object.fromEntries(D4.map((d, i) => [syms[i], d]));
    for (let t = 0; t < 300; t++) { const P = PTS.slice(0, 5); const pos = { [P[0]]: [0, 0] }, facts = []; const dists = {};
      syms.forEach(s => dists[s] = ri(2, 9));
      for (let i = 1; i < 5; i++) { const ref = P[i - 1]; const s = pick(syms); pos[P[i]] = [pos[ref][0] + V[code[s]][0] * dists[s], pos[ref][1] + V[code[s]][1] * dists[s]]; facts.push(`${P[i]} ${s} ${ref}`); }
      const a = P[4], b = P[0]; const dx = pos[a][0] - pos[b][0], dy = pos[a][1] - pos[b][1]; const D = dist(dx, dy); if (!dx || !dy || !isInt(D)) continue;
      const nm = dname(dx, dy); const legend = syms.map(s => `'A ${s} B' means A is ${dists[s]} m ${code[s]} of B`);
      const pts = Object.entries(pos);
      return { question: `${legend.join('; ')}. If ${facts.join(', ')}, then how far and in which direction is ${a} from ${b}?`, clues: legend.map(l => l + '.').concat(['Given: ' + facts.join(', ')]),
        ...RL.mcq(`${Math.round(D)} m, ${nm}`, [`${Math.round(D)} m, ${dname(-dx, -dy)}`, `${Math.abs(dx) + Math.abs(dy)} m, ${nm}`, `${Math.round(D)} m, ${dname(-dx, dy)}`, `${Math.round(D) + 2} m, ${nm}`]),
        viz: { kind: 'points', pts: [['P', 0, 0]], links: [] },
        steps: facts.map((f, i) => ({ text: `${f}: ${P[i + 1]} is ${dists[f.split(' ')[1]]} m ${code[f.split(' ')[1]]} of ${P[i]}.`, viz: { kind: 'points', pts: pts.slice(0, i + 2).map(([k, p]) => [k, p[0], p[1]]), links: facts.slice(0, i + 1).map((_, j) => [P[j + 1], P[j]]) } }))
          .concat([{ text: `${a} from ${b}: x ${dx}, y ${dy} → ${Math.round(D)} m, ${nm}.`, viz: { kind: 'points', pts: pts.map(([k, p]) => [k, p[0], p[1]]), links: facts.map((_, j) => [P[j + 1], P[j]]), hl: [a, b] } }]),
        traps: ['Each code gives a fixed distance as well as a direction.', 'Decode one link at a time and plot it; don\'t try to net it all out mentally.'], params: { legend, facts, a, b } };
    } return null;
  });
  RL.reg('direction', 'hard', 'dir-h3', 'Long walk: direction of the start from the end', ['ssc', 'bank', 'cuet', 'cat'], () => {
    const st = ri(0, 3), W = relWalk(ri(5, 6), st); if (!W) return null; const nm = dname(-W.x, -W.y); const ans = `${W.D} m, ${nm}`;
    return { question: `A delivery rider ${relTxt(st, W.ops)}. Where is the starting point from the rider's final position?`, ...RL.mcq(ans, [`${W.D} m, ${dname(W.x, W.y)}`, `${W.D} m, ${dname(W.x, -W.y)}`, `${Math.abs(W.x) + Math.abs(W.y)} m, ${nm}`, `${W.D + 3} m, ${nm}`]),
      viz: pathViz([[0, 0]]), steps: [{ text: 'Track the facing direction at every turn.', viz: pathViz(W.pts.slice(0, 3)) }, { text: `Ending point: x = ${W.x}, y = ${W.y} from the start.`, viz: pathViz(W.pts) },
        { text: `The start, seen FROM the end, is in the opposite direction: ${nm}, ${W.D} m away.`, viz: pathViz(W.pts, { final: true, reverse: true }) }],
      traps: ['The question reverses the usual view: the start as seen from the end.', 'Turn direction is relative to the current facing, not to north.'], params: { st, ops: W.ops } };
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
