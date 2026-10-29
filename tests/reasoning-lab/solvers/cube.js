/* Independent cube-painting solver: builds every unit cube explicitly and counts painted faces / colours. */
const WORD = { no: 0, 'exactly one': 1, 'exactly two': 2, 'exactly three': 3 };
function cubes(X, Y, Z, paint, skipTopLayer) { // paint: {left,right,bottom,top,front,back} -> colour
  const out = []; for (let x = 0; x < X; x++) for (let y = 0; y < Y; y++) for (let z = 0; z < Z; z++) { if (skipTopLayer && y === Y - 1) continue;
    const f = []; if (x === 0) f.push('left'); if (x === X - 1) f.push('right'); if (y === 0) f.push('bottom'); if (y === Y - 1) f.push('top'); if (z === 0) f.push('front'); if (z === Z - 1) f.push('back');
    const pf = f.filter(k => paint[k]); out.push({ n: pf.length, cols: pf.map(k => paint[k]) }); }
  return out; }
const ALL = c => ({ left: c, right: c, bottom: c, top: c, front: c, back: c });
function pred(q) { let m;
  if ((m = q.match(/have (no|exactly one|exactly two|exactly three) painted faces?\?/))) { const k = WORD[m[1]]; return u => u.n === k; }
  if (/at least one painted face/.test(q)) return u => u.n >= 1;
  if ((m = q.match(/have only (\w+) paint on them/))) { const c = m[1]; return u => u.cols.length > 0 && u.cols.every(x => x === c); }
  if ((m = q.match(/have both (\w+) and (\w+) faces but no (\w+) face/))) { const [, a, b, c] = m; return u => u.cols.includes(a) && u.cols.includes(b) && !u.cols.includes(c); }
  if (/show all three colours/.test(q)) return u => new Set(u.cols).size === 3;
  if (/have exactly two colours/.test(q)) return u => new Set(u.cols).size === 2;
  if (/have no paint at all/.test(q)) return u => u.cols.length === 0;
  if ((m = q.match(/have (\w+) paint and exactly one other colour/))) { const c = m[1]; return u => { const s = new Set(u.cols); return s.size === 2 && s.has(c); }; }
  throw new Error('pred? ' + q); }
const count = (list, f) => String(list.filter(f).length);
module.exports = {
  'cube-e1': p => { const n = +p.question.match(/side (\d+) cm/)[1]; return count(cubes(n, n, n, ALL('x')), pred(p.question)); },
  'cube-e2': p => { const c = +p.question.match(/using (\d+) straight cuts/)[1]; let best = 0; for (let a = 0; a <= c; a++) for (let b = 0; a + b <= c; b++) best = Math.max(best, (a + 1) * (b + 1) * (c - a - b + 1)); return String(best); },
  'cube-e3': p => { const N = +p.question.match(/cut into (\d+) identical/)[1]; const n = Math.round(Math.cbrt(N)); if (n ** 3 !== N) throw new Error('not a cube'); return count(cubes(n, n, n, ALL('x')), pred(p.question)); },
  'cube-m1': p => { const [, a, b, c] = p.question.match(/cuboid (\d+) cm × (\d+) cm × (\d+) cm/).map(Number); return count(cubes(a, b, c, ALL('x')), pred(p.question)); },
  'cube-m2': p => { const q = p.question, n = +q.match(/side (\d+)/)[1]; let paint = {}; let m;
    if ((m = q.match(/on all faces except the (\w+)/))) { paint = ALL('x'); delete paint[m[1]]; }
    else { m = q.match(/painted only on the (.+?) faces,/); m[1].replace(/,? and /, ', ').split(', ').forEach(f => { if (!['top', 'bottom', 'front', 'back', 'left', 'right'].includes(f)) throw new Error('face ' + f); paint[f] = 'x'; }); }
    return count(cubes(n, n, n, paint), pred(q)); },
  'cube-m3': p => { const q = p.question, n = +q.match(/side (\d+)/)[1]; const m = q.match(/top and bottom painted (\w+), front and back painted (\w+), and left and right painted (\w+)/);
    const paint = { top: m[1], bottom: m[1], front: m[2], back: m[2], left: m[3], right: m[3] }; return count(cubes(n, n, n, paint), pred(q)); },
  'cube-h1': p => { const q = p.question, n = +q.match(/side (\d+)/)[1]; if (+q.match(/top layer of (\d+) cubes/)[1] !== n * n) throw new Error('layer'); return count(cubes(n, n, n, ALL('x'), true), pred(q)); },
  'cube-h2': p => { const q = p.question; const m = q.match(/cuboid (\d+) \(left–right\) × (\d+) \(bottom–top\) × (\d+) \(front–back\) is painted: top and bottom (\w+), front and back (\w+), left face (\w+); the right face is left unpainted/);
    const paint = { top: m[4], bottom: m[4], front: m[5], back: m[5], left: m[6] }; return count(cubes(+m[1], +m[2], +m[3], paint), pred(q)); },
  'cube-h3': p => { const q = p.question; const m = q.match(/If (\d+) small cubes have (no|exactly one|exactly two|exactly three) painted faces?, how many have (no|exactly one|exactly two|exactly three) painted faces?\?/);
    const gv = +m[1], gk = WORD[m[2]], ak = WORD[m[3]]; const ns = []; for (let n = 2; n <= 40; n++) if (cubes(n, n, n, ALL('x')).filter(u => u.n === gk).length === gv) ns.push(n);
    if (ns.length !== 1) throw new Error('n not unique: ' + ns); const n = ns[0]; return count(cubes(n, n, n, ALL('x')), u => u.n === ak); },
};
