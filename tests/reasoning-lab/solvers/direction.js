/* Independent direction solver: parses the text and simulates with complex numbers (heading as i^k). */
const UNIT = { north: [0, 1], east: [1, 0], south: [0, -1], west: [-1, 0] };
const name8 = (x, y) => { if (!x && !y) return 'Same point'; const a = Math.atan2(y, x) * 180 / Math.PI; const n = ['East', 'North-East', 'North', 'North-West', 'West', 'South-West', 'South', 'South-East'];
  return n[((Math.round(a / 45) % 8) + 8) % 8] + (Math.abs(a / 45 - Math.round(a / 45)) > 1e-9 ? '?' : ''); };
const dirOf = (x, y) => { // general (not only 45°) direction words
  if (!x && !y) return 'Same point'; const ns = y > 0 ? 'North' : y < 0 ? 'South' : '', ew = x > 0 ? 'East' : x < 0 ? 'West' : ''; return ns && ew ? ns + '-' + ew : ns || ew; };
const absWalk = q => { let x = 0, y = 0; for (const m of q.matchAll(/(\d+) m (north|south|east|west)/g)) { x += UNIT[m[2]][0] * +m[1]; y += UNIT[m[2]][1] * +m[1]; } return [x, y]; };
const relWalk = q => { const m = q.match(/starts facing (\w+) and walks (\d+) m(.*)\. (How|Where)/); let h = UNIT[m[1]].slice(); let x = h[0] * +m[2], y = h[1] * +m[2];
  for (const t of m[3].matchAll(/turns (left|right) and walks (\d+) m/g)) { h = t[1] === 'left' ? [-h[1], h[0]] : [h[1], -h[0]]; x += h[0] * +t[2]; y += h[1] * +t[2]; } return [x, y]; };
const fmt = (x, y) => `${Math.hypot(x, y)} m, ${dirOf(x, y)}`;
const D8 = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West'];
module.exports = {
  'dir-e1': p => { const [x, y] = absWalk(p.question); return Math.hypot(x, y) + ' m'; },
  'dir-e3': p => { const [x, y] = absWalk(p.question); return dirOf(x, y); },
  'dir-e2': p => { const m = p.question.match(/faces (\w+)\. She turns (.+)\. Which/); let a = { north: 90, east: 0, south: 270, west: 180 }[m[1]];
    m[2].split(', then ').forEach(t => { a += t === 'right' ? -90 : t === 'left' ? 90 : 180; }); const [x, y] = [Math.round(Math.cos(a * Math.PI / 180)), Math.round(Math.sin(a * Math.PI / 180))]; return dirOf(x, y); },
  'dir-m1': p => { const [x, y] = relWalk(p.question); return fmt(x, y); },
  'dir-h3': p => { const [x, y] = relWalk(p.question); return fmt(-x, -y); },
  'dir-m2': p => { const m = p.question.match(/One (morning|evening), (\w+) stood with \w+ shadow falling exactly to \w+ (left|right|front|back)\./);
    const sun = m[1] === 'morning' ? [1, 0] : [-1, 0]; const shadow = [-sun[0], -sun[1]];
    // facing f; the shadow must equal the body-relative vector: front = f, right = rotate f clockwise, etc.
    for (const [nm, f] of Object.entries(UNIT)) { const rel = { front: f, back: [-f[0], -f[1]], right: [f[1], -f[0]], left: [-f[1], f[0]] }[m[3]];
      if (rel[0] === shadow[0] && rel[1] === shadow[1]) return nm[0].toUpperCase() + nm.slice(1); } },
  'dir-m3': p => { const pos = { P: [0, 0] }; const facts = p.clues.map(c => c.match(/^(\w) is (\d+) m (\w+) of (\w)\.$/));
    let guard = 0; while (facts.some(f => !pos[f[1]]) && guard++ < 20) facts.forEach(f => { if (pos[f[4]] && !pos[f[1]]) pos[f[1]] = [pos[f[4]][0] + UNIT[f[3]][0] * f[2], pos[f[4]][1] + UNIT[f[3]][1] * f[2]]; });
    const q = p.question.match(/How far is (\w) from (\w),/); const a = pos[q[1]], b = pos[q[2]]; return fmt(a[0] - b[0], a[1] - b[1]); },
  'dir-h1': p => { const m = p.question.match(/faces ([\w-]+)\. It turns (.+)\. Which/); let k = D8.indexOf(m[1]) * 45;
    for (const t of m[2].matchAll(/(\d+)° (clockwise|anticlockwise)/g)) k += (t[2] === 'clockwise' ? 1 : -1) * +t[1]; return D8[(((k % 360) + 360) % 360) / 45]; },
  'dir-h2': p => { const leg = {}; for (const m of p.question.matchAll(/'A (\S+) B' means A is (\d+) m (\w+) of B/g)) leg[m[1]] = [+m[2], m[3]];
    const m = p.question.match(/If (.+), then how far and in which direction is (\w) from (\w)\?/); const pos = {}; const facts = m[1].split(', ').map(s => s.split(' '));
    pos[facts[0][2]] = [0, 0]; let guard = 0; while (facts.some(f => !pos[f[0]]) && guard++ < 20) facts.forEach(([a, s, b]) => { if (pos[b] && !pos[a]) { const [L, d] = leg[s]; pos[a] = [pos[b][0] + UNIT[d][0] * L, pos[b][1] + UNIT[d][1] * L]; } });
    const A = pos[m[2]], B = pos[m[3]]; return fmt(A[0] - B[0], A[1] - B[1]); },
};
