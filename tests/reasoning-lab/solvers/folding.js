/* Independent folding solver: physical forward simulation of paper folds; nets folded with real rotations. */
const G = require('../lib/geo');
const FOLD = { 'the left half is folded over onto the right half': 'L', 'the right half is folded over onto the left half': 'R', 'the top half is folded down onto the bottom half': 'T', 'the bottom half is folded up onto the top half': 'B' };
function paper(p) { const q = p.question; const folds = [...q.matchAll(/\(\d\) ([a-z ]+?)(?=;|\. Then)/g)].map(m => { const f = FOLD[m[1]]; if (!f) throw new Error('fold? ' + m[1]); return f; });
  const N = p.viz.N, punches = p.viz.punches; const np = /a hole is punched/.test(q) ? 1 : +q.match(/Then (\d+) holes/)[1]; if (np !== punches.length) throw new Error('punch count');
  // forward: where does each original cell land? box shrinks, flapped cells reflect onto the kept half
  let box = { x0: 0, x1: N, y0: 0, y1: N }; const pos = new Map(); for (let x = 0; x < N; x++) for (let y = 0; y < N; y++) pos.set(x + ',' + y, [x, y]);
  for (const f of folds) { const w = box.x1 - box.x0, h = box.y1 - box.y0; if (('LR'.includes(f) && w % 2) || ('TB'.includes(f) && h % 2)) throw new Error('odd fold');
    for (const [k, [x, y]] of pos) { let nx = x, ny = y;
      if (f === 'L' && x < box.x0 + w / 2) nx = 2 * (box.x0 + w / 2) - 1 - x; if (f === 'R' && x >= box.x0 + w / 2) nx = 2 * (box.x0 + w / 2) - 1 - x;
      if (f === 'T' && y < box.y0 + h / 2) ny = 2 * (box.y0 + h / 2) - 1 - y; if (f === 'B' && y >= box.y0 + h / 2) ny = 2 * (box.y0 + h / 2) - 1 - y; pos.set(k, [nx, ny]); }
    if (f === 'L') box.x0 += w / 2; if (f === 'R') box.x1 -= w / 2; if (f === 'T') box.y0 += h / 2; if (f === 'B') box.y1 -= h / 2; }
  for (const [x, y] of punches) if (x < box.x0 || x >= box.x1 || y < box.y0 || y >= box.y1) throw new Error('punch outside folded paper');
  const hit = new Set(punches.map(c => c.join(','))); const holes = [...pos].filter(([, v]) => hit.has(v.join(','))).map(([k]) => k);
  if (holes.length !== punches.length * 2 ** folds.length) throw new Error('layer count');
  return holes.sort().join(';'); }
const netOf = cells => G.foldNet(cells);
const die = p => { const r = netOf(p.viz.cells); if (!r.ok) throw new Error('not a net'); return r.die; };
const isNet = cs => netOf(cs.map(([r, c], i) => ({ r, c, label: 'abcdef'[i] }))).ok;
const parseCells = key => key.split(';').map(s => s.split(',').map(Number));
const parseView = s => { const m = s.match(/top (\w+), front (\w+), right (\w+)/); return [m[1], m[2], m[3]]; };
module.exports = {
  'fold-e2': p => o => o.key === paper(p), 'fold-m1': p => o => o.key === paper(p), 'fold-h1': p => o => o.key === paper(p),
  'fold-e1': p => G.opposite(die(p), p.question.match(/opposite (\w+)\?/)[1]),
  'fold-e3': p => o => isNet(parseCells(o.key)),
  'fold-m2': p => { const d = die(p); return o => { const [a, b] = o.label.split(' and '); return G.opposite(d, a) === b; }; },
  'fold-m3': p => { const d = die(p); return o => { const f = o.label.split(', '); return f.length === 3 && f.every((a, i) => f.every((b, j) => i === j || G.dot(d.get(a), d.get(b)) === 0)); }; },
  'fold-h2': p => { const d = die(p); return o => !G.hasView(d, parseView(o.label)); },
  'fold-h3': p => String(p.viz.shapes.filter(s => netOf(s).ok).length),
};
