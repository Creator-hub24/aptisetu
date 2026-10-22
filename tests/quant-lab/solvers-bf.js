/* Brute-force / enumeration / numerical-construction solvers. They override the closed-form solvers in solvers.js.
   Principle: re-derive each answer WITHOUT the textbook formula the generator uses. Methods: enumerate sample
   spaces and permutations, count lattice points (Pick's theorem from raw counts), build triangles from side
   lengths by bisection and measure, integrate areas/volumes numerically (Simpson), search for parameters. */
const r2 = x => Math.round(x * 100) / 100;
const memo = new Map(); const M = (key, fn) => { if (!memo.has(key)) memo.set(key, fn()); return memo.get(key); };
const bisect = (f, lo, hi, it = 200) => { let flo = f(lo); for (let i = 0; i < it; i++) { const m = (lo + hi) / 2, fm = f(m); if ((fm < 0) === (flo < 0)) { lo = m; flo = fm; } else hi = m; } return (lo + hi) / 2; };
const ternary = (f, lo, hi, max = true) => { for (let i = 0; i < 300; i++) { const a = lo + (hi - lo) / 3, b = hi - (hi - lo) / 3; if ((f(a) < f(b)) === max) lo = a; else hi = b; } return (lo + hi) / 2; };
const simpson = (f, a, b, n = 2000) => { const h = (b - a) / n; let s = f(a) + f(b); for (let i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2); return s * h / 3; };
const K = (22 / 7) / Math.PI;                     // the questions fix π = 22/7, so numerical results are rescaled
const discArea = r => simpson(t => 2 * r * r * Math.cos(t) ** 2, -Math.PI / 2, Math.PI / 2);   // ∫2√(r²−x²)dx with x = r sin t
const dist = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]);
// Build a triangle from its sides: B = (0,0), C = (a,0), A found by bisection on the angle at B so that |AC| = b.
const tri = (a, b, c) => { const th = bisect(t => dist([c * Math.cos(t), c * Math.sin(t)], [a, 0]) - b, 1e-12, Math.PI - 1e-12); return { A: [c * Math.cos(th), c * Math.sin(th)], B: [0, 0], C: [a, 0] }; };
const lineDist = (P, U, V) => { const d = [V[0] - U[0], V[1] - U[1]], t = ((P[0] - U[0]) * d[0] + (P[1] - U[1]) * d[1]) / (d[0] * d[0] + d[1] * d[1]); return dist(P, [U[0] + t * d[0], U[1] + t * d[1]]); };   // foot of perpendicular by projection
function perms(n, visit) { const a = [...Array(n).keys()], c = Array(n).fill(0); visit(a); let i = 0; while (i < n) { if (c[i] < i) { const j = i % 2 ? c[i] : 0; [a[j], a[i]] = [a[i], a[j]]; visit(a); c[i]++; i = 0; } else { c[i] = 0; i++; } } }
const pointInPoly = (x, y, P) => { let inside = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside; } return inside; };
const onSeg = (x, y, p, q) => (q[0] - p[0]) * (y - p[1]) === (q[1] - p[1]) * (x - p[0]) && x >= Math.min(p[0], q[0]) && x <= Math.max(p[0], q[0]) && y >= Math.min(p[1], q[1]) && y <= Math.max(p[1], q[1]);
const pick = P => { let I = 0, Bd = 0; const xs = P.map(p => p[0]), ys = P.map(p => p[1]); for (let x = Math.min(...xs); x <= Math.max(...xs); x++) for (let y = Math.min(...ys); y <= Math.max(...ys); y++) { if (P.some((p, i) => onSeg(x, y, p, P[(i + 1) % P.length]))) Bd++; else if (pointInPoly(x, y, P)) I++; } return I + Bd / 2 - 1; };
const dice = (n, f) => { let c = 0, t = 0; const rec = (k, acc) => { if (k === n) { t++; if (f(acc)) c++; return; } for (let v = 1; v <= 6; v++) rec(k + 1, [...acc, v]); }; rec(0, []); return c / t; };
const regPoly = n => Array.from({ length: n }, (_, i) => [Math.cos(2 * Math.PI * i / n), Math.sin(2 * Math.PI * i / n)]);
const angleAt = (P, Q, R) => { const u = [P[0] - Q[0], P[1] - Q[1]], v = [R[0] - Q[0], R[1] - Q[1]]; return Math.acos(Math.max(-1, Math.min(1, (u[0] * v[0] + u[1] * v[1]) / Math.hypot(...u) / Math.hypot(...v)))) * 180 / Math.PI; };

const S = {
  'pct-h1': ({ r, up }) => { const B = 1000, A = up ? B + B * r / 100 : B - B * r / 100; return r2((up ? A - B : B - A) / (up ? A : A) * 100); },
  'mx-m1': ({ V, x, k }) => { let milk = V, water = 0; for (let i = 0; i < k; i++) { const f = x / V; milk -= milk * f; water -= water * f; water += x; } return r2(milk); },
  'al-h1': ({ k, mode }) => { const x = mode < 3 ? bisect(t => t + 1 / t - k, 1, k + 1) : bisect(t => t - 1 / t - k, 1e-9, k + 2); const v = [x ** 2 + x ** -2, x ** 3 + x ** -3, x ** 4 + x ** -4, x ** 2 + x ** -2, x ** 3 - x ** -3][mode]; return Math.round(v * 1e6) / 1e6; },
  'iq-h3': ({ n, mode }) => { let c = 0; for (let x = -n - 1; x <= n + 1; x++) for (let y = -n - 1; y <= n + 1; y++) { const s = Math.abs(x) + Math.abs(y); if ([s <= n, s === n, s < n, Math.max(Math.abs(x), Math.abs(y)) <= n][mode]) c++; } return c; },
  'lg-h2': ({ k, t, sum }) => { const f = x => Math.log(k) / Math.log(x) + Math.log(x) / Math.log(k) - (t + 1 / t); const roots = []; let px = 1.0005; for (let x = 1.0006; x < k ** (t + 1); x *= 1.0007) { if (Math.sign(f(x)) !== Math.sign(f(px))) roots.push(Math.round(bisect(f, px, x))); px = x; } return sum ? roots.reduce((s, v) => s + v, 0) : roots.reduce((s, v) => s * v, 1); },
  'pg-h1': ({ k, lo, hi }) => { let s = 0; for (let x = lo; x <= hi; x++) if (x % k === 0) s += x; return s; },
  'pg-h2': ({ a, b, m }) => M(`pgh2${a},${b}`, () => { for (let t1 = -200; t1 <= 200; t1++) for (let d = -60; d <= 60; d++) { let ok = true, s = 0, t = t1; for (let n = 1; n <= 6 && ok; n++) { s += t; t += d; if (s !== a * n * n + b * n) ok = false; } if (ok) return [t1, d]; } return [NaN, NaN]; }).reduce((t1, d) => { let t = t1; for (let i = 1; i < m; i++) t += d; return t; }),
  'pg-h3': ({ p, q, r }) => { for (let a = -300; a <= 300; a++) for (let d = -5; d <= 5; d++) { let tp = a, tq = a; for (let i = 1; i < p; i++) tp += d; for (let i = 1; i < q; i++) tq += d; if (tp === q && tq === p) { let t = a; for (let i = 1; i < r; i++) t += d; return t; } } return NaN; },
  'mm-e3': ({ a, b }) => { const x = ternary(x => -(a * x + b / x), 1e-6, 1e4); return Math.round((a * x + b / x) * 1e4) / 1e4; },
  'mm-h1': ({ p, q, S: s }) => { const x = ternary(x => x ** p * (s - x) ** q, 0, s); return Math.round(x ** p * (s - x) ** q * 1e3) / 1e3; },
  // geometry: construct and measure
  'gm-e2': ({ A, B }) => { const a = A * Math.PI / 180, b = B * Math.PI / 180; const t = bisect(s => Math.atan2(s * Math.sin(a), s * Math.cos(a) - 1) - (Math.PI - b), 1e-9, 1e6); const P = [t * Math.cos(a), t * Math.sin(a)]; return Math.round(angleAt([0, 0], P, [1, 0])); },
  'gm-e3': ({ b, h }) => pick([[0, 0], [b, 0], [Math.floor(b / 3), h]]),
  'gm-m1': ({ a, b, c }) => { const T = tri(a, b, c); return r2(a * T.A[1] / 2); },
  'gm-m2': ({ m, n, L }) => { const A = [0.3 * L, 0.8 * L], B = [0, 0], C = [L, 0], f = m / (m + n), D = [A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f]; const s = bisect(u => (A[1] + (C[1] - A[1]) * u) - D[1], 0, 1); const E = [A[0] + (C[0] - A[0]) * s, A[1] + (C[1] - A[1]) * s]; return r2(dist(D, E)); },
  'gm-m3': ({ a, area }) => { const T = tri(a, a, a); return Math.round((area ? a * T.A[1] / 2 : T.A[1]) / Math.sqrt(3) * 1e6) / 1e6; },
  'gm-h1': ({ a, b, c }) => M(`gmh1${a},${b},${c}`, () => { const T = tri(a, b, c), sides = [[T.B, T.C, T.A], [T.C, T.A, T.B], [T.A, T.B, T.C]];
    // signed distance to each side (positive on the side of the opposite vertex): its minimum is concave, so nested ternary search finds the incentre
    const sd = (P, U, V, W) => { const cr = (X) => (V[0] - U[0]) * (X[1] - U[1]) - (V[1] - U[1]) * (X[0] - U[0]); return Math.sign(cr(W)) * cr(P) / dist(U, V); };
    const md = P => Math.min(...sides.map(([U, V, W]) => sd(P, U, V, W)));
    const bestY = x => ternary(y => md([x, y]), -10, T.A[1] + 10); const xs = ternary(x => md([x, bestY(x)]), Math.min(0, T.A[0]) - 10, Math.max(a, T.A[0]) + 10); const r = md([xs, bestY(xs)]);
    const yc = bisect(y => dist([a / 2, y], T.A) - dist([a / 2, y], T.B), -1e4, 1e4); return r2(r + dist([a / 2, yc], T.B)); }),
  'gm-h2': ({ a, b, c }) => { const T = tri(a, b, c); const x = bisect(x => angleAt(T.B, T.A, [x, 0]) - angleAt([x, 0], T.A, T.C), 1e-9, a - 1e-9); return r2(x); },
  'gm-h3': ({ a, b, c }) => { const T = tri(a, b, c); return Math.round(dist(T.A, [a / 2, 0]) ** 2); },
  // mensuration: count unit cubes / integrate
  'ms-e1': ({ l, b, h }) => { let n = 0; for (let x = 0; x < l; x++) for (let y = 0; y < b; y++) for (let z = 0; z < h; z++) n++; return n; },
  'ms-e2': ({ a }) => { let f = 0; for (let x = 0; x < a; x++) for (let y = 0; y < a; y++) for (let z = 0; z < a; z++) for (const [dx, dy, dz] of [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]) { const X = x + dx, Y = y + dy, Z = z + dz; if (X < 0 || Y < 0 || Z < 0 || X >= a || Y >= a || Z >= a) f++; } return f; },
  'ms-e3': ({ r, h }) => r2(simpson(() => discArea(r), 0, h, 2) * K),
  'ms-m1': ({ r, h }) => M(`msm1${r},${h}`, () => r2(simpson(z => discArea(r * (1 - z / h)), 0, h, 200) * K)),
  'ms-m2': ({ r, kind }) => { const cap = (t0, t1) => simpson(t => 2 * Math.PI * r * Math.sin(t) * r, t0, t1); const v = kind === 0 ? cap(0, Math.PI) : kind === 1 ? cap(0, Math.PI / 2) : cap(0, Math.PI / 2) + discArea(r); return r2(v * K); },
  'ms-h1': ({ R, r }) => M(`msh1${R},${r}`, () => { const vol = q => simpson(z => discArea(Math.sqrt(Math.max(0, q * q - z * z))), -q, q, 400); return Math.round(vol(R) / vol(r)); }),
  'ms-h3': ({ r, Rc }) => M(`msh3${r},${Rc}`, () => { const vs = simpson(z => discArea(Math.sqrt(Math.max(0, r * r - z * z))), -r, r, 400); return r2(vs / discArea(Rc)); }),
  // coordinate: Pick's theorem from raw lattice counts, parametric searches
  'cg-m1': ({ P }) => pick(P),
  'cg-h1': ({ P }) => pick(P),
  'cg-m2': ({ m, n, x1, x2 }) => { const t = bisect(t => t / (1 - t) - m / n, 1e-12, 1 - 1e-12); return Math.round((x1 + t * (x2 - x1)) * 1e6) / 1e6; },
  'cg-m3': ({ a, b, c, x0, y0 }) => { const U = Math.abs(b) > 1e-9 ? [0, -c / b] : [-c / a, 0], V = Math.abs(b) > 1e-9 ? [1, -(c + a) / b] : [-c / a, 1]; return r2(lineDist([x0, y0], U, V)); },
  'cg-h2': ({ p, q }) => { for (let A = 1; A <= 100; A++) if (p / A + q / A === 1) { let pts = 0; for (let x = 0; x <= A; x++) for (let y = 0; y <= A; y++) if (x + y <= A) pts++; return pick([[0, 0], [A, 0], [0, A]]); } return NaN; },
  // circles: polygons, bisection, integration
  'ci-e1': ({ r, mode }) => { const N = 200000, per = N * 2 * r * Math.sin(Math.PI / N) * K; return r2(mode === 2 ? per / 2 + 2 * r : per); },
  'ci-e2': ({ n, mode }) => { const P = regPoly(n), I = angleAt(P[n - 1], P[0], P[1]); return Math.round([I, 180 - I, I * n][mode] * 1e6) / 1e6; },
  'ci-e3': ({ n }) => { let c = 0; for (let i = 0; i < n; i++) for (let j = i + 2; j < n; j++) if (!(i === 0 && j === n - 1)) c++; return c; },
  'ci-m1': ({ r, d }) => r2(2 * bisect(x => x * x + d * d - r * r, 0, r)),
  'ci-m2': ({ d, r }) => { const th = bisect(t => r * r - r * d * Math.cos(t), 0, Math.PI / 2); return r2(dist([r * Math.cos(th), r * Math.sin(th)], [d, 0])); },
  'ci-m3': ({ t, r }) => r2(simpson(() => simpson(rho => rho, 0, r, 200), 0, t * Math.PI / 180, 2) * K),
  'ci-h1': ({ r1, r2: q, d }) => { const ph = bisect(f => d * Math.cos(f) - (r1 - q), 0, Math.PI); const n = [Math.cos(ph), Math.sin(ph)]; return r2(dist([r1 * n[0], r1 * n[1]], [d + q * n[0], q * n[1]])); },
  'ci-h2': ({ k, mode }) => { let n = 3; while (n < 400 && Math.abs(angleAt(regPoly(n)[n - 1], regPoly(n)[0], regPoly(n)[1]) - k * (180 - angleAt(regPoly(n)[n - 1], regPoly(n)[0], regPoly(n)[1]))) > 1e-6) n++; return [S['ci-e3']({ n }), n, Math.round(n * angleAt(regPoly(n)[n - 1], regPoly(n)[0], regPoly(n)[1]))][mode]; },
  'ci-h3': ({ a, mode }) => { const inc = discArea(a / 2) * K, circ = discArea(a / Math.SQRT2) * K; return r2([a * a - inc, circ - a * a, circ - inc][mode]); },
  // permutations and combinations: enumerate
  'pc-e3': ({ w, first }) => M('pce3' + w + first, () => { let c = 0; perms(w.length, p => { if (!first || p[0] === 0) c++; }); return c; }),
  'pc-m2': ({ w }) => M('pcm2' + w, () => { const cnt = {}; [...w].forEach(ch => cnt[ch] = (cnt[ch] || 0) + 1); const keys = Object.keys(cnt); let c = 0; const rec = left => { if (!left) { c++; return; } for (const k of keys) if (cnt[k]) { cnt[k]--; rec(left - 1); cnt[k]++; } }; rec(w.length); return c; }),
  'pc-m3': ({ n, mode }) => M(`pcm3${n},${mode}`, () => { let c = 0; const seen = new Set();
    perms(n - 1, q => { const seat = [0, ...q.map(v => v + 1)], pos = []; seat.forEach((p, i) => pos[p] = i); const adj = Math.abs(pos[1] - pos[2]) === 1 || Math.abs(pos[1] - pos[2]) === n - 1;
      if (mode === 0) c++; else if (mode === 1) { if (adj) c++; } else if (mode === 2) { if (!adj) c++; } else if (mode === 4) { if (pos[1] === (pos[2] + 1) % n) c++; } else { const s1 = seat.join(','), s2 = [0, ...seat.slice(1).reverse()].join(','); seen.add(s1 < s2 ? s1 : s2); } });
    return mode === 3 ? seen.size : c; }),
  'pc-h1': ({ n, mode }) => M(`pch1${n},${mode}`, () => { let c = 0; perms(n, p => { const pos = []; p.forEach((v, i) => pos[v] = i); const g = Math.abs(pos[0] - pos[1]);
    if ([g !== 1, Math.max(pos[0], pos[1], pos[2]) - Math.min(pos[0], pos[1], pos[2]) === 2, g === 2, pos[0] === 0 && pos[1] !== 1][mode]) c++; }); return c; }),
  // probability: enumerate sample spaces
  'pb-e1': ({ s, mode }) => dice(2, ([a, b]) => [a + b === s, Math.abs(a - b) === s, a * b === s][mode]),
  'pb-e2': ({ r, b, g }) => { const balls = [...Array(r).fill('R'), ...Array(b).fill('B'), ...Array(g).fill('G')]; return balls.filter(x => x === 'R').length / balls.length; },
  'pb-m1': ({ r, b }) => { let c = 0, t = 0; const n = r + b; for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) if (i !== j) { t++; if (i < r && j < r) c++; } return c / t; },
  'pb-m2': ({ n, k, exactly }) => dice(n, xs => { const hits = xs.filter(v => v > 6 - k).length; return exactly ? hits === 1 : hits >= 1; }),
  'pb-m3': ({ s, mode }) => dice(2, ([a, b]) => [a + b >= s, a + b <= s, a * b >= s][mode]),
  'pb-h1': ({ r1, b1, r2: q, b2 }) => { const L = (r1 + b1) * (q + b2); let red1 = 0, red = 0; for (let u = 0; u < 2; u++) { const R = u ? q : r1, Bn = u ? b2 : b1, w = L / (R + Bn); for (let i = 0; i < R + Bn; i++) if (i < R) { red += w; if (!u) red1 += w; } } return red1 / red; },
  'pb-h2': ({ a, c, b, d }) => { let hit = 0; for (let i = 0; i < c; i++) for (let j = 0; j < d; j++) if (i < a || j < b) hit++; return hit / (c * d); },
  'pb-h3': ({ s, ge }) => dice(3, xs => { const t = xs[0] + xs[1] + xs[2]; return ge ? t >= s : t === s; }),
  // sets: build the actual sets / exhaustive search over arrangements
  'st-h1': ({ S1, S2, S3, r }) => { const A = new Set(), Bs = new Set(), Cs = new Set(); let id = 0; const put = (k, sets) => { for (let i = 0; i < k; i++) { sets.forEach(s => s.add(id)); id++; } };
    put(r.abc, [A, Bs, Cs]); put(r.ab, [A, Bs]); put(r.bc, [Bs, Cs]); put(r.ca, [Cs, A]); put(r.a, [A]); put(r.b, [Bs]); put(r.c, [Cs]);
    const inter = (X, Y) => [...X].filter(v => Y.has(v)).length; if (A.size + Bs.size + Cs.size !== S1 || inter(A, Bs) + inter(Bs, Cs) + inter(Cs, A) !== S2 || [...A].filter(v => Bs.has(v) && Cs.has(v)).length !== S3) return NaN;
    let one = 0; for (let v = 0; v < id; v++) if ((A.has(v) ? 1 : 0) + (Bs.has(v) ? 1 : 0) + (Cs.has(v) ? 1 : 0) === 1) one++; return one; },
  'st-h2': ({ N, a, b, c }) => M(`sth2${N},${a},${b},${c}`, () => { let best = Infinity; const inA = i => i < a;
    for (let ob = 0; ob < N; ob++) { const pre = [0]; for (let i = 0; i < 2 * N; i++) { const p = i % N; pre.push(pre[i] + (inA(p) && ((p - ob + N) % N) < b ? 1 : 0)); }
      for (let oc = 0; oc < N; oc++) { const t = pre[oc + c] - pre[oc]; if (t < best) best = t; } } return best; }),
};
module.exports = S;
