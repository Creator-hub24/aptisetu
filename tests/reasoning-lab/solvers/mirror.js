/* Independent mirror/water solver: glyph images compared through each character's symmetry group; clocks via angles; grids via real rotations. */
const HS = new Set('AHIMOTUVWXY08'), VS = new Set('BCDEHIKOX038'), ROT = new Set('HINOSXZ08');
const sym = c => { const s = ['00']; if (HS.has(c)) s.push('10'); if (VS.has(c)) s.push('01'); if (ROT.has(c)) s.push('11'); return s; };
const sameGlyph = ([c1, x1, y1], [c2, x2, y2]) => c1 === c2 && sym(c1).includes(String((x1 ^ x2) & 1) + String((y1 ^ y2) & 1));
function image(s, kind) { let g = [...s].map(c => [c, 0, 0]); const flipX = () => { g = g.reverse().map(([c, x, y]) => [c, x ^ 1, y]); }, flipY = () => { g = g.map(([c, x, y]) => [c, x, y ^ 1]); };
  if (kind === 'mirror') flipX(); if (kind === 'water') flipY(); if (kind === 'both') { flipY(); flipX(); } return g; }
const strSolver = p => { const q = p.question; const s = q.match(/“(.+)”/)[1]; const kind = /mirror image of the water image/.test(q) ? 'both' : /mirror image \(mirror placed to the right\)/.test(q) ? 'mirror' : /water image \(water below\)/.test(q) ? 'water' : null; if (!kind) throw new Error('kind');
  const img = image(s, kind); return o => o.viz.chars.length === img.length && o.viz.chars.every((ch, i) => sameGlyph(ch, img[i])); };
const parseT = s => { const [h, m] = s.split(':').map(Number); return (h % 12) * 60 + m; };
const fmt = t => { t = ((t % 720) + 720) % 720; return `${Math.floor(t / 60) || 12}:${String(t % 60).padStart(2, '0')}`; };
// mirror: every hand angle θ -> 360° − θ, so the hour hand's position (t/2 degrees) gives 720 − t minutes
const mirrorClock = t => { const hourAngle = t / 2; const img = (360 - hourAngle) % 360; return img * 2; };
// water (exam convention): 12 and 6 swap; standard key 18:30 − t
const waterClock = t => 1110 - t;
const cellsT = { v: ([x, y]) => [-x, y], h: ([x, y]) => [x, -y], r90: ([x, y]) => [-y, x], r270: ([x, y]) => [y, -x], r180: ([x, y]) => [-x, -y] };
function applyGrid(N, cells, ts) { return cells.map(([r, c]) => { let p = [c + 0.5 - N / 2, r + 0.5 - N / 2]; for (const t of ts) p = cellsT[t](p); return [Math.round(p[1] + N / 2 - 0.5), Math.round(p[0] + N / 2 - 0.5)]; }); }
const setKey = (N, cells) => cells.map(([r, c]) => { if (r < 0 || c < 0 || r >= N || c >= N) throw new Error('out'); return r * N + c; }).sort((a, b) => a - b).join(',');
const NAMES = { 'reflected in a vertical mirror': 'v', 'reflected in a horizontal mirror (water)': 'h', 'rotated 90° clockwise': 'r90', 'rotated 90° anticlockwise': 'r270', 'rotated 180°': 'r180' };
module.exports = {
  'mir-e1': strSolver, 'mir-e2': strSolver, 'mir-h1': strSolver,
  'mir-e3': p => { const w = p.question.match(/the word (\w+) look/)[1]; return String([...w].filter(c => HS.has(c)).length); },
  'mir-m1': p => fmt(mirrorClock(parseT(p.question.match(/shows (\d+:\d+)/)[1]))),
  'mir-m3': p => fmt(waterClock(parseT(p.question.match(/shows (\d+:\d+)/)[1]))),
  'mir-h3': p => { const q = p.question; const seen = parseT(q.match(/show (\d+:\d+)/)[1]); const [, dh, dm] = q.match(/(\d+) h (\d+) min later/).map(Number); return fmt(mirrorClock(mirrorClock(seen) + dh * 60 + dm)); },
  'mir-m2': p => { const { N, cells } = p.viz; const t = /mirror on the right side/.test(p.question) ? 'v' : /water image \(water below\)/.test(p.question) ? 'h' : null; const k = setKey(N, applyGrid(N, cells, [t])); return o => setKey(N, o.viz.cells) === k; },
  'mir-h2': p => { const m = p.question.match(/first (.+?), then (.+?)\. Which/); const ts = [NAMES[m[1]], NAMES[m[2]]]; if (!ts[0] || !ts[1]) throw new Error('names'); const { N, cells } = p.viz; const k = setKey(N, applyGrid(N, cells, ts)); return o => setKey(N, o.viz.cells) === k; },
};
