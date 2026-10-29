/* Reasoning Lab — visual explainers for every topic (original teaching text + live visuals + worked examples). */
(function (g) {
  'use strict';
  const RL = g.RL;
  const X = {
    cube: { ideas: [
      ['Think in layers', 'Cut an n×n×n painted cube into n³ unit cubes. Only the outer shell is painted; the inner (n−2)³ block has no paint at all.'],
      ['Position decides paint', 'Corners touch 3 painted faces, edge cubes touch 2, face-centre cubes touch 1, inner cubes touch 0. Count positions, not paint.'],
      ['Cuboids and partial paint', 'For an a×b×c block each edge has (length−2) middle cubes. If a face is not painted, the cubes on it lose that coat, so redo the count for those layers.']],
      formulas: ['3 faces: 8 (always)', '2 faces: 12(n−2)', '1 face: 6(n−2)²', '0 faces: (n−2)³', 'Pieces from k cuts: split cuts as evenly as possible over 3 directions, multiply (p+1)(q+1)(r+1)'],
      widget: 'cube' },
    dice: { ideas: [
      ['Opposite faces never meet', 'Two faces that appear together in any view are adjacent, so they cannot be opposite. Eliminate, then the leftover pair is opposite.'],
      ['Common face rule', 'When two views share one face in the same place, the faces in matching places are opposite. Turn the die in your head until the shared face lines up.'],
      ['Corner order (clockwise)', 'Top, front and right read in a fixed rotation. A mirrored order is impossible on the same die, even when no opposite pair is shown.']],
      formulas: ['Standard die: opposite faces add to 7', 'Hidden faces in a stack: total − visible', 'Rolling forward: front ← top, top ← back'],
      widget: 'dice' },
    folding: { ideas: [
      ['Paper folding is reflection', 'Each fold reflects the punched holes across the fold line. Unfold in reverse order and double the holes at every step.'],
      ['Nets: skip one square', 'In a straight row of a net, squares one apart become opposite faces. Squares sharing an edge are always neighbours on the cube.'],
      ['Valid nets', 'Exactly 11 distinct nets fold into a cube. Four in a row with one square above and below (anywhere) always works; a 2×2 block never does.']],
      formulas: ['Holes after unfolding = punches × 2^(folds) (when no punch sits on a fold line)', '11 cube nets in total'], widget: 'fold' },
    mirror: { ideas: [
      ['Mirror: left and right swap', 'A vertical mirror flips left and right; top and bottom stay. Letters like A, H, I, M, O, T, U, V, W, X, Y look the same.'],
      ['Water: top and bottom swap', 'A water image flips top and bottom. Letters such as B, C, D, E, H, I, K, O, X look the same.'],
      ['Clocks', 'Mirror time = 11:60 − time (12:00 at noon). Water time = 18:30 − time. Subtract 12 h when the answer goes past 12.']],
      formulas: ['Mirror clock: 11:60 − t', 'Water clock: 18:30 − t', 'Mirror of a water image = 180° rotation'] },
    figcount: { ideas: [
      ['Count by size', 'Group shapes by size (one cell, two cells, …) and count each group. Grouping is the only reliable way to avoid double counting.'],
      ['Fans and grids', 'Lines from one point with k segments on the base give k(k+1)/2 triangles. An m×n grid of squares has C(m+1,2)·C(n+1,2) rectangles.'],
      ['Holes and diagonals', 'With a missing cell, count the rectangles in the full grid and subtract those that cross the gap. Diagonals create tilted triangles: label vertices.']],
      formulas: ['Squares in n×n: n(n+1)(2n+1)/6', 'Rectangles in m×n: m(m+1)n(n+1)/4', 'Triangles in a fan of k sections: k(k+1)/2'] },
    blood: { ideas: [
      ['Draw, don’t think', 'Write each fact as a link on a family tree: squares for males, circles for females, a double line for marriage. Generations go top to bottom.'],
      ['Read from the first person', '“A is B’s uncle” describes A as seen from B. Start at B, walk the tree to A, then name the relation.'],
      ['Gender can be unknown', 'Without a gender you can only say “parent”, “sibling” or “child”. If the question needs “father” or “mother”, it cannot be decided.']],
      formulas: ['Father’s or mother’s brother = uncle', 'Father’s or mother’s sibling’s child = cousin', 'Spouse’s parent = parent-in-law'], widget: 'family' },
    direction: { ideas: [
      ['Track facing, not just position', 'Left and right depend on where the person faces at that moment. Keep a compass arrow and turn it at each step.'],
      ['Net displacement', 'Add all east-west moves and all north-south moves separately. Distance = √(x² + y²), and the signs give the direction.'],
      ['Shadows', 'In the morning the sun is in the east, so shadows fall west. In the evening shadows fall east. At noon there is (almost) no shadow.']],
      formulas: ['Distance = √(Δx² + Δy²)', 'Right turn = +90° clockwise, left = −90°', 'Morning shadow → west, evening → east'] },
    syllogism: { ideas: [
      ['Draw the weakest diagram', 'Draw only what the statements force. Grey regions must be empty, ✕ must have members, everything else is “maybe”.'],
      ['Definite vs possible', 'A definite conclusion must hold in every valid diagram. A “possibility” conclusion follows if at least one valid diagram allows it and it is not already ruled out.'],
      ['Either–or', 'If neither conclusion is certain on its own but they cover every case (like “Some A are B” / “No A is B”) then the answer is “either I or II”.']],
      formulas: ['All + All = All', 'All + No = No', 'Some + All = Some', 'Some + No = Some … not', '“Only a few A are B” = some A are B and some A are not B'] },
    inequality: { ideas: [
      ['Follow one path', 'Two letters are comparable only along one unbroken chain. Read the signs between them in order.'],
      ['Same direction only', 'If the path mixes > and <, no relation follows. If it has a ≥, the result is ≥ (unless every sign is =).'],
      ['Either–or', 'If I is “A > B” and II is “A = B”, and the chain gives A ≥ B, then neither is certain alone but one must hold: either I or II.']],
      formulas: ['> and ≥ → >', '= and ≥ → ≥', '> and < → no relation'] },
    coding: { ideas: [
      ['Write the alphabet ranks', 'A=1 … Z=26 and the reverse rank (A=26 … Z=1). Opposite letters add to 27 (A↔Z, M↔N).'],
      ['Compare letter by letter', 'Line the word up with its code. Look for a fixed shift, an alternating shift, a reversal or a position-based shift.'],
      ['Sentence codes', 'For coded sentences, find the word that two sentences share and the code they share. Repeat until each word has its code.']],
      formulas: ['Opposite letter = 27 − rank', 'EJOTY = 5, 10, 15, 20, 25', 'Shift wraps: Z + 1 = A'] },
    series: { ideas: [
      ['Differences first', 'Write the differences between terms. If they don’t settle, take differences of differences, or check ratios.'],
      ['Mixed operations', 'Patterns like ×2+1, ×3−2, or alternating +a, ×b are common. Two interleaved series also show up.'],
      ['Wrong term', 'Find the rule that fits most terms; the single term that breaks it is the answer.']],
      formulas: ['Squares, cubes, primes ± constant', 'n² + n, n³ − n', 'Letter series: convert to numbers'] },
    ranking: { ideas: [
      ['Both ends', 'If someone is p-th from the top and q-th from the bottom, the total is p + q − 1.'],
      ['People between', 'People between two positions a < b: b − a − 1. With overlap, the minimum total can be smaller than you think; check both cases.'],
      ['Comparisons', 'Turn “older than”, “taller than” into arrows and chain them. Answer only what is fixed in every order that fits.']],
      formulas: ['Total = p + q − 1', 'From the other end = total − rank + 1', 'Between = |a − b| − 1'] },
    seating: { ideas: [
      ['Fix a reference first', 'Start with a definite clue (someone at an end, someone opposite someone). In a circle, seat the first person anywhere: every seat looks the same.'],
      ['Facing matters', 'Facing north (or the centre): their right is your right in the diagram for a row, and clockwise neighbours flip for a circle. Facing away flips left and right.'],
      ['Branch, don’t guess', 'For “exactly k between” clues, draw both cases side by side and let later clues kill one.']],
      formulas: ['Circle of n facing centre: arrangements = (n−1)!', 'Linear of n: n!', 'Opposite seat in a circle of n: +n/2'], widget: 'seating' },
    puzzles: { ideas: [
      ['Build the grid', 'Make a table of slots (floors, days, boxes) and fill it with what is certain. Mark impossible slots with ✗.'],
      ['Gaps and order', '“Immediately above” fixes a gap of one. “Somewhere above” only fixes the order. “Exactly k between” gives two cases.'],
      ['Check uniqueness', 'Once every slot is filled, check that no other arrangement fits all the clues before you answer.']],
      formulas: ['Floors are numbered bottom up', 'Vacant slots count in “between” for places, not for people'] },
    dilr: { ideas: [
      ['Round robin', 'n teams, everyone plays everyone once: n(n−1)/2 matches. Total wins = number of matches when there are no draws.'],
      ['Knockout', 'Every match removes one team, so n teams need n − 1 matches to find a winner. Byes fill the bracket up to the next power of 2.'],
      ['Logic grids', 'One ✓ per row and per column. Each ✓ crosses out the rest of its row and column, which often creates new ✓s.']],
      formulas: ['Round robin matches: n(n−1)/2', 'Knockout matches: n − 1', 'Byes: next power of 2 − n'] },
  };
  RL.EXPLAIN = X;
  const H = RL.H;
  const mk = (t, c, kids) => H(t, c, kids);
  function example(k, host) { const card = mk('section', { cls: 'card grid' }); const head = mk('div', { cls: 'row' }, [mk('h3', { text: '▶ Watch a worked example' }), mk('span', { cls: 'grow' })]); const area = mk('div');
    const types = RL.byExam(RL.LEVELS.flatMap(l => RL.TOPICS[k].types[l]), RL.store.d.exam || 'all'); if (!types.length) return;
    const sel = mk('select', { 'aria-label': 'Example type' }); types.forEach(t => sel.appendChild(mk('option', { value: t.id, text: `${t.level[0].toUpperCase() + t.level.slice(1)} · ${t.name}` })));
    const go = () => { RL.ui.clear(area); const t = RL.TYPES[sel.value]; let p; try { p = RL.generate(k, t.level, t.id); } catch (e) { return; } area.appendChild(RL.ui.qBlock(p)); area.appendChild(mk('p', { cls: 'verdict ok', text: 'Answer: ' + String.fromCharCode(65 + p.answerIndex) + (p.options[p.answerIndex].label ? ' · ' + p.options[p.answerIndex].label : '') })); area.appendChild(RL.ui.stepper(p)); };
    sel.addEventListener('change', go); head.append(sel, RL.ui.btn('Another ↻', 'ghost', go)); card.append(head, area); host.appendChild(card); go(); }
  // ---------- topic widgets
  function cubeWidget() { let n = 4, f = 2; const box = mk('section', { cls: 'card grid' }); const view = mk('div', { cls: 'vizbox' }); const out = mk('div', { cls: 'out' });
    const sl = mk('input', { type: 'range', min: '2', max: '8', value: '4', 'aria-label': 'Cube size n' }); const lab = mk('b', { text: 'n = 4' });
    const draw = () => { RL.ui.clear(view); view.appendChild(RL.render({ kind: 'cube3d', dims: [n, n, n], paint: { top: 'brand', bottom: 'brand', front: 'brand', back: 'brand', left: 'brand', right: 'brand' }, hl: { faces: f }, explode: f === 0 && n > 2 })); const c = [Math.max(0, n - 2) ** 3, 6 * Math.max(0, n - 2) ** 2, 12 * Math.max(0, n - 2), 8];
      out.textContent = `n = ${n}: ${n ** 3} cubes → 3 faces: 8 · 2 faces: 12×${n - 2} = ${c[2]} · 1 face: 6×${n - 2}² = ${c[1]} · 0 faces: ${n - 2}³ = ${c[0]}. Highlighted: ${c[f]} cube${c[f] === 1 ? '' : 's'} with ${f} painted face${f === 1 ? '' : 's'}.`; };
    sl.addEventListener('input', () => { n = +sl.value; lab.textContent = 'n = ' + n; draw(); });
    box.append(mk('h3', { text: '🧊 Try it: slide n, pick a class' }), mk('div', { cls: 'row' }, [lab, sl, RL.ui.seg([[3, '3 faces'], [2, '2 faces'], [1, '1 face'], [0, '0 faces']], f, v => { f = v; draw(); }, 'Painted faces')]), view, out); draw(); return box; }
  const ROLL = { forward: d => [d[3], d[2], d[0], d[1], d[4], d[5]], back: d => [d[2], d[3], d[1], d[0], d[4], d[5]], right: d => [d[4], d[5], d[2], d[3], d[1], d[0]], left: d => [d[5], d[4], d[2], d[3], d[0], d[1]] };
  RL.ROLL = ROLL;
  function diceWidget() { let d = ['1', '6', '2', '5', '3', '4']; const box = mk('section', { cls: 'card grid' }); const view = mk('div', { cls: 'vizbox' }); const out = mk('div', { cls: 'out' });
    const draw = roll => { RL.ui.clear(view); view.appendChild(RL.render({ kind: 'die3d', die: d, roll })); out.textContent = `Top ${d[0]} · Front ${d[2]} · Right ${d[5]} · hidden: bottom ${d[1]}, back ${d[3]}, left ${d[4]}. Opposite faces always add to 7 on a standard die.`; };
    const r = dir => () => { d = ROLL[dir](d); draw(dir); };
    box.append(mk('h3', { text: '🎲 Try it: roll the die' }), mk('div', { cls: 'row' }, [RL.ui.btn('⬆ Forward', '', r('forward')), RL.ui.btn('⬇ Back', '', r('back')), RL.ui.btn('⬅ Left', '', r('left')), RL.ui.btn('➡ Right', '', r('right')), RL.ui.btn('Reset', 'ghost', () => { d = ['1', '6', '2', '5', '3', '4']; draw(); })]), view, out);
    const net = [{ r: 0, c: 1, label: '1' }, { r: 1, c: 0, label: '3' }, { r: 1, c: 1, label: '2' }, { r: 1, c: 2, label: '4' }, { r: 1, c: 3, label: '5' }, { r: 2, c: 1, label: '6' }];
    box.append(mk('h3', { text: 'Opposite faces on a net' }), mk('div', { cls: 'vizbox' }, [RL.render({ kind: 'net', cells: net, opp: true })])); draw(); return box; }
  function foldWidget() { const box = mk('section', { cls: 'card grid' }); const v1 = mk('div', { cls: 'vizbox' }); let st = 'unfold';
    const pf = () => { RL.ui.clear(v1); v1.appendChild(RL.render({ kind: 'paperfold', N: 4, folds: ['L', 'T'], punches: [[2, 3]], stage: st })); };
    box.append(mk('h3', { text: '📄 Fold, punch, unfold' }), RL.ui.seg([['fold', '1 · Fold'], ['punch', '2 · Punch'], ['unfold', '3 · Unfold']], st, v => { st = v; pf(); }, 'Stage'), v1);
    const net = [{ r: 0, c: 1, label: 'A' }, { r: 1, c: 0, label: 'B' }, { r: 1, c: 1, label: 'C' }, { r: 1, c: 2, label: 'D' }, { r: 1, c: 3, label: 'E' }, { r: 2, c: 2, label: 'F' }];
    box.append(mk('h3', { text: '🧩 Watch a net fold into a cube' }), mk('div', { cls: 'grid g2' }, [mk('div', { cls: 'vizbox' }, [RL.render({ kind: 'net', cells: net, opp: true })]), mk('div', { cls: 'vizbox' }, [RL.render({ kind: 'netfold', cells: net })])])); pf(); return box; }
  const W = { cube: cubeWidget, dice: diceWidget, fold: foldWidget };
  RL.explain = function (k, host) { const E = X[k]; if (!E) return; const ex = Object.keys(RL.EXAMS).filter(e => RL.LEVELS.some(l => RL.TOPICS[k].types[l].some(t => t.exams.includes(e))));
    host.appendChild(mk('div', { cls: 'row' }, [mk('span', { cls: 'small muted', text: 'Tested in:' })].concat(ex.map(e => mk('span', { cls: 'chip', text: RL.EXAMS[e] })))));
    host.appendChild(mk('div', { cls: 'grid g3' }, E.ideas.map(([h, t], i) => mk('section', { cls: 'card idea' }, [mk('span', { cls: 'chip', text: `Idea ${i + 1}` }), mk('h3', { text: h }), mk('p', { text: t })]))));
    if (E.widget && W[E.widget]) host.appendChild(W[E.widget]());
    if (E.widget && RL.lab && RL.lab.forTopic(k) && !W[E.widget]) host.appendChild(mk('section', { cls: 'card row' }, [mk('span', { text: 'Build your own in the Lab sandbox.' }), mk('span', { cls: 'grow' }), (RL.ui.link ? RL.ui.link(`t/${k}/lab`, 'Open the Lab →', 'btn primary') : RL.ui.btn('Open the Lab →', 'primary', () => { location.hash = `#/t/${k}/lab`; }))]));
    host.appendChild(mk('section', { cls: 'card' }, [mk('h3', { text: '⚡ Shortcuts' }), mk('ul', { cls: 'formulas' }, E.formulas.map(f => mk('li', { text: f })))]));
    example(k, host); };
})(typeof globalThis !== 'undefined' ? globalThis : this);
