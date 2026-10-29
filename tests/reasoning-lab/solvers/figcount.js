/* Independent figure counter: builds the vertex set from segment intersections, merges collinear segments,
   then brute-forces triangles / squares (incl. tilted) / rectangles whose sides are fully drawn. */
const E = 1e-7, K = v => Math.round(v * 1e6) / 1e6;
function analyse(segs) {
  const S = segs.map(([x1, y1, x2, y2]) => ({ a: [x1, y1], b: [x2, y2] }));
  const pts = new Map(); const add = p => { const k = K(p[0]) + ',' + K(p[1]); if (!pts.has(k)) pts.set(k, [K(p[0]), K(p[1])]); };
  S.forEach(s => { add(s.a); add(s.b); });
  for (let i = 0; i < S.length; i++) for (let j = i + 1; j < S.length; j++) { const p = S[i].a, r = [S[i].b[0] - p[0], S[i].b[1] - p[1]], q = S[j].a, s = [S[j].b[0] - q[0], S[j].b[1] - q[1]];
    const d = r[0] * s[1] - r[1] * s[0]; if (Math.abs(d) < E) continue; const t = ((q[0] - p[0]) * s[1] - (q[1] - p[1]) * s[0]) / d, u = ((q[0] - p[0]) * r[1] - (q[1] - p[1]) * r[0]) / d;
    if (t > -E && t < 1 + E && u > -E && u < 1 + E) add([p[0] + t * r[0], p[1] + t * r[1]]); }
  // merged lines
  const lines = []; for (const s of S) { let dx = s.b[0] - s.a[0], dy = s.b[1] - s.a[1]; const L = Math.hypot(dx, dy); dx /= L; dy /= L; if (dx < -E || (Math.abs(dx) < E && dy < 0)) { dx = -dx; dy = -dy; }
    let ln = lines.find(l => Math.abs(l.u[0] - dx) < 1e-9 && Math.abs(l.u[1] - dy) < 1e-9 && Math.abs((s.a[0] - l.o[0]) * dy - (s.a[1] - l.o[1]) * dx) < 1e-9);
    if (!ln) lines.push(ln = { u: [dx, dy], o: s.a, iv: [] }); const t1 = (s.a[0] - ln.o[0]) * dx + (s.a[1] - ln.o[1]) * dy, t2 = (s.b[0] - ln.o[0]) * dx + (s.b[1] - ln.o[1]) * dy; ln.iv.push([Math.min(t1, t2), Math.max(t1, t2)]); }
  lines.forEach(l => { l.iv.sort((a, b) => a[0] - b[0]); const m = []; for (const v of l.iv) { if (m.length && v[0] <= m[m.length - 1][1] + 1e-9) m[m.length - 1][1] = Math.max(m[m.length - 1][1], v[1]); else m.push(v.slice()); } l.iv = m; });
  const P = [...pts.values()];
  const conn = (a, b) => lines.some(l => { const off = p => (p[0] - l.o[0]) * l.u[1] - (p[1] - l.o[1]) * l.u[0]; if (Math.abs(off(a)) > 1e-6 || Math.abs(off(b)) > 1e-6) return false;
    const ta = (a[0] - l.o[0]) * l.u[0] + (a[1] - l.o[1]) * l.u[1], tb = (b[0] - l.o[0]) * l.u[0] + (b[1] - l.o[1]) * l.u[1]; const lo = Math.min(ta, tb), hi = Math.max(ta, tb); return l.iv.some(v => v[0] <= lo + 1e-6 && v[1] >= hi - 1e-6); });
  const n = P.length; const C = []; for (let i = 0; i < n; i++) { C.push([]); for (let j = 0; j < n; j++) C[i].push(i !== j && conn(P[i], P[j])); }
  return { P, C };
}
const idx = (P, p) => P.findIndex(q => Math.abs(q[0] - p[0]) < 1e-6 && Math.abs(q[1] - p[1]) < 1e-6);
function triangles({ P, C }) { let c = 0; const n = P.length; for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) if (C[i][j]) for (let k = j + 1; k < n; k++) if (C[i][k] && C[j][k]) {
  const cr = (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]); if (Math.abs(cr) > 1e-4) c++; } return c; }
function rects({ P, C }, squaresOnly) { const seen = new Set(); const n = P.length;
  for (let a = 0; a < n; a++) for (let b = 0; b < n; b++) if (C[a][b]) for (let c = 0; c < n; c++) if (c !== a && C[b][c]) {
    const ab = [P[b][0] - P[a][0], P[b][1] - P[a][1]], bc = [P[c][0] - P[b][0], P[c][1] - P[b][1]]; if (Math.abs(ab[0] * bc[0] + ab[1] * bc[1]) > 1e-9) continue;
    if (squaresOnly && Math.abs(Math.hypot(...ab) - Math.hypot(...bc)) > 1e-9) continue; const d = idx(P, [P[a][0] + bc[0], P[a][1] + bc[1]]); if (d < 0 || !C[c][d] || !C[d][a]) continue;
    seen.add([a, b, c, d].sort((x, y) => x - y).join()); } return seen.size; }
function solve(p) { const q = p.question, G = analyse(p.viz.segs);
  if (/how many triangles/i.test(q)) return String(triangles(G));
  if (/how many squares/i.test(q)) { if (/squares are there in a \d+ × \d+ grid/.test(q) || /tilted ones included/.test(q)) return String(rects(G, true)); }
  if (/how many rectangles/i.test(q)) return String(rects(G, false));
  throw new Error('q? ' + q); }
module.exports = Object.fromEntries(['fig-e1', 'fig-e2', 'fig-e3', 'fig-m1', 'fig-m2', 'fig-m3', 'fig-h1', 'fig-h2', 'fig-h3'].map(id => [id, solve]));
module.exports._dbg = { analyse };
