/* Topic: Mirror & water images — strings, clocks and grid figures */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample } = RL.u;
  RL.topic('mirror', 'Mirror & Water Images', '🪞', 'Flip strings, clocks and figures with a draggable mirror line, so you can see what reverses and what stays the same.', 'Visual Reasoning');
  const HS = 'AHIMOTUVWXY08', VS = 'BCDEHIKOX038', ROT = 'HINOSXZ08';
  const canon = (c, fx, fy) => { if (fx && fy && ROT.includes(c)) return [c, 0, 0]; if (fx && HS.includes(c)) fx = 0; if (fy && VS.includes(c)) fy = 0; return [c, fx ? 1 : 0, fy ? 1 : 0]; };
  const G = (chars) => { const cs = chars.map(([c, fx, fy]) => canon(c, fx, fy)); return { label: '', key: cs.map(x => x.join('')).join('|'), viz: { kind: 'glyphs', chars: cs } }; };
  const T = { mirror: s => [...s].reverse().map(c => [c, 1, 0]), water: s => [...s].map(c => [c, 0, 1]), both: s => [...s].reverse().map(c => [c, 1, 1]), revOnly: s => [...s].reverse().map(c => [c, 0, 0]), flipOnly: s => [...s].map(c => [c, 1, 0]), waterRev: s => [...s].reverse().map(c => [c, 0, 1]), plain: s => [...s].map(c => [c, 0, 0]) };
  RL.mirrorT = T; RL.glyphCanon = canon;
  const POOL = 'ABCDEFGJKLNPQRSZ2345679';
  const mkStr = n => { let s; do s = Array.from({ length: n }, () => pick([...POOL + 'HMTUOX'])).join(''); while ([...s].filter(c => !HS.includes(c) && !VS.includes(c)).length < 3 || new Set(s).size < n - 1); return s; };
  function strType(id, level, name, kind, exams, n) {
    RL.reg('mirror', level, id, name, exams, () => {
      const s = mkStr(n); const ans = G(T[kind](s)); const ds = Object.keys(T).filter(k => k !== kind).map(k => G(T[k](s)));
      const what = kind === 'mirror' ? 'mirror image (mirror placed to the right)' : kind === 'water' ? 'water image (water below)' : 'mirror image of the water image';
      return { question: `Which option is the ${what} of “${s}”?`, ...RL.mcq(ans, shuffle(ds)), viz: { kind: 'glyphs', chars: T.plain(s), mirror: kind === 'water' ? 'h' : 'v' },
        steps: [{ text: kind === 'water' ? 'Water image: left–right order stays, each character flips upside down.' : kind === 'mirror' ? 'Mirror image: the order reverses (last becomes first) and each character flips left–right.' : 'Mirror + water = a 180° rotation: the order reverses and each character turns upside down and back to front.', viz: { kind: 'glyphs', chars: T.plain(s), mirror: kind === 'water' ? 'h' : 'v' } },
          { text: `Symmetric characters (${[...new Set(s)].filter(c => (kind === 'mirror' ? HS : kind === 'water' ? VS : ROT).includes(c)).join(' ') || 'none here'}) look unchanged after the flip.`, viz: ans.viz }, { text: 'So the image is the option shown.', viz: ans.viz }],
        traps: ['Reversing the order without flipping each character is the classic wrong option.', 'A water image never changes the left–right order.'], params: { s, kind } };
    });
  }
  strType('mir-e1', 'easy', 'Mirror image of a word/code', 'mirror', ['ssc', 'cuet', 'govt', 'bank'], 5);
  strType('mir-e2', 'easy', 'Water image of a word/code', 'water', ['ssc', 'cuet', 'govt'], 5);
  strType('mir-h1', 'hard', 'Mirror image of a water image', 'both', ['ssc', 'govt', 'cuet'], 7);
  RL.reg('mirror', 'easy', 'mir-e3', 'Letters unchanged in a mirror', ['ssc', 'cuet', 'govt'], () => {
    const W = ['MOTHER', 'WITHOUT', 'AUTUMN', 'MAXIMUM', 'YOUTH', 'TIMBER', 'HAMLET', 'VOLUME', 'MATHS', 'WINTRY', 'OXYGEN', 'TOMATO', 'QUANTUM', 'HAIRCUT', 'MOVIE', 'WAXY'];
    const w = pick(W); const k = [...w].filter(c => HS.includes(c)).length;
    return { question: `How many letters of the word ${w} look the same in a vertical mirror (each letter on its own)?`, ...RL.mcq(String(k), [k + 1, k - 1, k + 2, w.length - k].filter(v => v >= 0 && v !== k).map(String)), viz: { kind: 'glyphs', chars: T.plain(w), mirror: 'v' },
      steps: [{ text: 'Letters with a vertical line of symmetry: A H I M O T U V W X Y.', viz: { kind: 'glyphs', chars: T.plain(w), hl: [...w].map(c => HS.includes(c)) } }, { text: `${w} has ${k} of them: ${[...w].filter(c => HS.includes(c)).join(', ')}.` }],
      traps: ['B, C, D, E and K are symmetric top-to-bottom, not left-to-right.', 'Count repeated letters each time they appear.'], params: { w } };
  });
  // clocks
  const fmt = (h, m) => `${h}:${String(m).padStart(2, '0')}`;
  const mirrorT = (h, m) => { let t = (720 - ((h % 12) * 60 + m)) % 720; let H = Math.floor(t / 60), M = t % 60; return [H || 12, M]; };
  const waterT = (h, m) => { let t = (((1110 - ((h % 12) * 60 + m)) % 720) + 720) % 720; return [Math.floor(t / 60) || 12, t % 60]; };
  RL.clockT = { mirrorT, waterT };
  const clockViz = (h, m, extra) => Object.assign({ kind: 'clock', h, m }, extra || {});
  const tOpts = (ans, h, m) => { const [a, b] = ans; const d = [[h, m], [(a % 12) + 1, b], [a, (b + 30) % 60], [(12 - a) || 12, (60 - b) % 60], [a, (60 - b) % 60], [((a + 10) % 12) + 1, b]]; return d.map(([x, y]) => fmt(x, y)); };
  RL.reg('mirror', 'medium', 'mir-m1', 'Clock in a mirror', ['ssc', 'cuet', 'govt', 'bank'], () => {
    const h = ri(1, 12), m = pick([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 12, 18, 24, 36, 48]); const a = mirrorT(h, m); if (fmt(...a) === fmt(h, m)) return null;
    return { question: `A clock shows ${fmt(h, m)}. What time does its mirror image show?`, ...RL.mcq(fmt(...a), tOpts(a, h, m)), viz: clockViz(h, m),
      steps: [{ text: 'A mirror flips the dial left to right, so each hand angle θ becomes 360° − θ.', viz: clockViz(h, m, { ghost: a }) }, { text: `Shortcut: 11:60 − ${fmt(h, m)} = ${fmt(...a)} (use 23:60 if the time is past 11:60).`, viz: clockViz(...a, { mirrored: true }) }],
      traps: ['12:00 and 6:00 look unchanged in a mirror; most other times do not.', 'Subtract from 11:60, not 12:00.'], params: { h, m } };
  });
  RL.reg('mirror', 'medium', 'mir-m3', 'Clock in water', ['ssc', 'govt', 'cuet'], () => {
    const h = ri(1, 12), m = pick([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]); const a = waterT(h, m); if (fmt(...a) === fmt(h, m)) return null;
    return { question: `A clock shows ${fmt(h, m)}. What time does its water image show?`, ...RL.mcq(fmt(...a), tOpts(a, h, m).concat([fmt(...mirrorT(h, m))])), viz: clockViz(h, m),
      steps: [{ text: 'Water flips the dial top to bottom: θ becomes 180° − θ, so 12 swaps with 6.', viz: clockViz(h, m, { ghost: a, axis: 'h' }) }, { text: `Exam shortcut: 18:30 − ${fmt(h, m)} (subtract 12 h if needed) = ${fmt(...a)}.`, viz: clockViz(...a) }],
      traps: ['The water rule (18:30 −) is different from the mirror rule (11:60 −).', 'In water, 12 and 6 swap places while 3 and 9 stay put, so the minute value m becomes 30 − m.'], params: { h, m } };
  });
  RL.reg('mirror', 'hard', 'mir-h3', 'Mirror clock after time passes', ['ssc', 'cat', 'govt'], () => {
    const h = ri(1, 12), m = ri(0, 11) * 5, dh = ri(1, 5), dm = ri(0, 11) * 5; const real = mirrorT(h, m); let t = ((real[0] % 12) * 60 + real[1] + dh * 60 + dm) % 720; const nr = [Math.floor(t / 60) || 12, t % 60]; const ans = mirrorT(...nr);
    const wrong1 = (() => { let t2 = ((h % 12) * 60 + m + dh * 60 + dm) % 720; return [Math.floor(t2 / 60) || 12, t2 % 60]; })();
    return { question: `In a mirror, a clock appears to show ${fmt(h, m)}. What will the mirror image show ${dh} h ${dm} min later?`, ...RL.mcq(fmt(...ans), [fmt(...wrong1), fmt(...nr), fmt(...mirrorT(...wrong1)), fmt(((ans[0]) % 12) + 1, ans[1]), fmt(ans[0], (ans[1] + 30) % 60)]), viz: clockViz(h, m, { mirrored: true }),
      steps: [{ text: `Real time = 11:60 − ${fmt(h, m)} = ${fmt(...real)}.`, viz: clockViz(...real) }, { text: `Add ${dh} h ${dm} min → ${fmt(...nr)}.`, viz: clockViz(...nr) }, { text: `Mirror it again → ${fmt(...ans)}.`, viz: clockViz(...ans, { mirrored: true }) }],
      traps: ['The mirror image runs backwards, so convert to real time before adding.', 'Adding directly to the mirror time gives a wrong option.'], params: { h, m, dh, dm } };
  });
  // grid figures
  const gkey = (N, cells) => cells.map(([r, c]) => r * N + c).sort((a, b) => a - b).join(',');
  const GT = { v: (N, [r, c]) => [r, N - 1 - c], h: (N, [r, c]) => [N - 1 - r, c], r90: (N, [r, c]) => [c, N - 1 - r], r180: (N, [r, c]) => [N - 1 - r, N - 1 - c], r270: (N, [r, c]) => [N - 1 - c, r], d: (N, [r, c]) => [c, r], ad: (N, [r, c]) => [N - 1 - c, N - 1 - r], id: (N, x) => x };
  RL.gridT = GT;
  const GV = (N, cells, extra) => Object.assign({ label: '', key: gkey(N, cells), viz: Object.assign({ kind: 'cells', N, cells }, extra || {}) });
  function asym(N) { for (;;) { const cells = []; const k = ri(5, 7); while (cells.length < k) { const c = [ri(0, N - 1), ri(0, N - 1)]; if (!cells.some(x => x[0] === c[0] && x[1] === c[1])) cells.push(c); } const keys = Object.keys(GT).map(t => gkey(N, cells.map(x => GT[t](N, x)))); if (new Set(keys).size === 8) return cells; } }
  RL.reg('mirror', 'medium', 'mir-m2', 'Mirror image of a grid figure', ['ssc', 'cuet', 'govt', 'bank'], () => {
    const N = 4, cells = asym(N), ax = pick(['v', 'h']); const ans = GV(N, cells.map(x => GT[ax](N, x)));
    return { question: `Which option is the ${ax === 'v' ? 'mirror image (mirror on the right side)' : 'water image (water below)'} of the shaded figure?`, ...RL.mcq(ans, shuffle(['h', 'v', 'r90', 'r180', 'r270', 'd'].filter(t => t !== ax)).map(t => GV(N, cells.map(x => GT[t](N, x))))),
      viz: { kind: 'cells', N, cells, axis: ax }, steps: [{ text: ax === 'v' ? 'Each cell keeps its row; column c moves to column N−1−c.' : 'Each cell keeps its column; row r moves to row N−1−r.', viz: { kind: 'cells', N, cells, axis: ax } }, { text: 'Reflect every shaded cell to get the image.', viz: ans.viz }],
      traps: ['A 180° rotation looks like a mirror image but flips both ways.', 'Track one corner cell to check the orientation quickly.'], params: { N, cells, ax } };
  });
  RL.reg('mirror', 'hard', 'mir-h2', 'Two transformations in a row', ['ssc', 'cat', 'cuet'], () => {
    const N = 5, cells = asym(N); const [t1, t2] = [pick(['v', 'h']), pick(['r90', 'r270', 'r180', 'v', 'h'])]; if (t1 === t2) return null;
    const res = cells.map(x => GT[t2](N, GT[t1](N, x))); const ans = GV(N, res); const names = { v: 'reflected in a vertical mirror', h: 'reflected in a horizontal mirror (water)', r90: 'rotated 90° clockwise', r270: 'rotated 90° anticlockwise', r180: 'rotated 180°' };
    const ds = Object.keys(GT).map(t => GV(N, cells.map(x => GT[t](N, x)))).concat([GV(N, cells.map(x => GT[t1](N, GT[t2](N, x))))]);
    return { question: `The figure is first ${names[t1]}, then ${names[t2]}. Which option shows the result?`, ...RL.mcq(ans, shuffle(ds)), viz: { kind: 'cells', N, cells },
      steps: [{ text: `Step 1: ${names[t1]}.`, viz: { kind: 'cells', N, cells: cells.map(x => GT[t1](N, x)) } }, { text: `Step 2: ${names[t2]}.`, viz: ans.viz }, { text: 'Order matters: doing the steps the other way round usually gives a different figure (a distractor).' }],
      traps: ['Do the transformations in the order given.', 'Two reflections make a rotation, which is a handy check.'], params: { N, cells, t1, t2 } };
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
