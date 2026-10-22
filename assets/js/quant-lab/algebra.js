/* Algebra: Linear & Quadratic, Inequalities & Modulus, Functions, Logarithms, Progressions, Max-Min. */
(function (Q) {
  'use strict';
  const R = Q.register, { fmt, r2, gcd, isInt } = Q.H;
  const sg = (v, first) => (v < 0 ? (first ? '−' : ' − ') + -v : (first ? '' : ' + ') + v);
  const term = (c, v, first) => (c === 0 ? '' : (c < 0 ? (first ? '−' : ' − ') : (first ? '' : ' + ')) + (Math.abs(c) === 1 && v ? '' : Math.abs(c)) + v);
  const plot = (f, a, b, n = 80) => { const pts = []; for (let i = 0; i <= n; i++) { const x = a + (b - a) * i / n, y = f(x); if (isFinite(y)) pts.push([r2(x), r2(y)]); } return pts; };
  const graph = (curves, marks = [], opts = {}) => Object.assign({ type: 'graph', curves, marks }, opts);
  const numline = (min, max, intervals, points = []) => ({ type: 'numline', min, max, intervals, points });

  /* ---------- LINEAR & QUADRATIC ---------- */
  R('algebra', 'easy', 'al-e1', 'Linear equation', H => {
    const x = H.ri(-12, 15), a = H.pick([2, 3, 4, 5, 6, 7, 9]), b = H.ri(-20, 25), c = a * x + b;
    return { question: `Solve for x: ${a}x${sg(b)} = ${c}`, answer: x, params: { a, b, c }, steps: [`${a}x = ${c}${sg(-b)} = ${c - b}.`, `x = ${c - b}/${a} = ${x}.`], traps: ['Sign error moving terms.', 'Dividing only one side.'], viz: { type: 'balance', a, b, c, x } };
  });
  R('algebra', 'easy', 'al-e2', 'Two-variable system', H => {
    const x = H.ri(-10, 20), y = H.ri(-10, 20);
    return { question: `x + y = ${x + y} and x − y = ${x - y}. Find x.`, answer: x, params: { s: x + y, d: x - y }, steps: [`Add: 2x = ${2 * x}.`, `x = ${x}.`], traps: ['Subtracting instead of adding.', 'Reporting y.'], viz: graph([{ pts: plot(t => x + y - t, -15, 25) }, { pts: plot(t => t - (x - y), -15, 25), color: 'warn' }], [[x, y, `(${x}, ${y})`]]) };
  });
  R('algebra', 'easy', 'al-e3', 'Evaluate expression', H => {
    const a = H.ri(1, 5), b = H.ri(-9, 9), c = H.ri(-9, 9), x = H.ri(-5, 5), v = a * x * x + b * x + c;
    return { question: `Evaluate ${term(a, 'x²', true)}${term(b, 'x')}${c ? sg(c) : ''} at x = ${x}.`, answer: v, params: { a, b, c, x }, steps: [`${a}(${x})² = ${a * x * x}; ${b}(${x}) = ${b * x}.`, `Sum with ${c}: ${v}.`], traps: ['(−x)² is positive.', 'Order of operations: square before multiply.'], viz: graph([{ pts: plot(t => a * t * t + b * t + c, x - 4, x + 4) }], [[x, v, `${v}`]]) };
  });
  R('algebra', 'medium', 'al-m1', 'Larger root', H => H.retry(() => {
    const r1 = H.ri(-9, 12), r2_ = H.ri(-9, 12); if (r1 === r2_) return null; const s = r1 + r2_, p = r1 * r2_, big = Math.max(r1, r2_);
    return { question: `Find the LARGER root of x²${term(-s, 'x')}${p ? sg(p) : ''} = 0`, answer: big, params: { s, p }, steps: [`Need two numbers with sum ${s}, product ${p}.`, `Roots ${Math.min(r1, r2_)} and ${big}.`], traps: ['Sign flip from factors.', 'Sum of roots = −b/a.'], viz: { type: 'parabola', s, p, roots: [r1, r2_] } };
  }));
  R('algebra', 'medium', 'al-m2', 'α² + β²', H => {
    const s = H.ri(-9, 9), p = H.ri(-12, 12), v = s * s - 2 * p;
    return { question: `If α, β are roots of x²${term(-s, 'x')}${p ? sg(p) : ''} = 0, find α² + β².`, answer: v, params: { s, p }, steps: [`α+β = ${s}, αβ = ${p}.`, `α²+β² = (α+β)² − 2αβ = ${s * s} − ${2 * p} = ${v}.`], traps: ['Forgetting −2αβ.', 'Sign of α+β is −b/a.'], viz: graph([{ pts: plot(t => t * t - s * t + p, s / 2 - 6, s / 2 + 6) }]) };
  });
  R('algebra', 'medium', 'al-m3', 'Solve 2×2 system', H => H.retry(() => {
    const x = H.ri(-8, 10), y = H.ri(-8, 10), a1 = H.ri(1, 6), b1 = H.ri(-6, 6), a2 = H.ri(-6, 6), b2 = H.ri(1, 6); if (a1 * b2 - a2 * b1 === 0 || !b1 || !a2) return null;
    const c1 = a1 * x + b1 * y, c2 = a2 * x + b2 * y;
    return { question: `${term(a1, 'x', true)}${term(b1, 'y')} = ${c1} and ${term(a2, 'x', true)}${term(b2, 'y')} = ${c2}. Find x + y.`, answer: x + y, params: { a1, b1, c1, a2, b2, c2 },
      steps: [`Cramer: D = ${a1 * b2 - a2 * b1}.`, `x = ${x}, y = ${y}.`, `x + y = ${x + y}.`], traps: ['Arithmetic slip in elimination.', 'Answering x only.'], viz: graph([{ pts: plot(t => (c1 - a1 * t) / b1, x - 8, x + 8) }, { pts: plot(t => (c2 - a2 * t) / b2, x - 8, x + 8), color: 'warn' }], [[x, y, `(${x}, ${y})`]]) };
  }));
  R('algebra', 'hard', 'al-h1', 'Powers of x ± 1/x', H => {
    const mode = H.ri(0, 4), k = H.ri(mode < 3 ? 3 : 1, 12), s = mode < 3 ? '+' : '−';
    const p2 = k * k - 2, p3 = k ** 3 - 3 * k, p4 = p2 * p2 - 2, m2 = k * k + 2, m3 = k ** 3 + 3 * k;
    const [ask, v] = [['x² + 1/x²', p2], ['x³ + 1/x³', p3], ['x⁴ + 1/x⁴', p4], ['x² + 1/x²', m2], ['x³ − 1/x³', m3]][mode];
    return { question: `If x ${s} 1/x = ${k}, find ${ask}.`, answer: v, params: { k, mode }, mcq: [mode < 3 ? k ** (mode + 2) : k * k, v + 2 * (mode === 1 || mode === 4 ? k : 1), v - 4],
      steps: mode === 0 ? [`(x + 1/x)² = x² + 2 + 1/x².`, `${k * k} − 2 = ${v}.`] : mode === 1 ? [`(x + 1/x)³ = x³ + 1/x³ + 3(x + 1/x).`, `${k ** 3} − ${3 * k} = ${v}.`] : mode === 2 ? [`x² + 1/x² = ${k * k} − 2 = ${p2}.`, `Square again: ${p2}² − 2 = ${v}.`] : mode === 3 ? [`(x − 1/x)² = x² − 2 + 1/x².`, `${k * k} + 2 = ${v}.`] : [`(x − 1/x)³ = x³ − 1/x³ − 3(x − 1/x).`, `${k ** 3} + ${3 * k} = ${v}.`],
      traps: [`Cubing/squaring ${k} and stopping there.`, 'Getting the sign of the cross term wrong.'], viz: { type: 'cube', k, mode } };
  });
  R('algebra', 'hard', 'al-h2', 'Count k for real roots', H => {
    const c = H.ri(1, 30), K = H.ri(6, 15); let n = 0; for (let k = -K; k <= K; k++) if (k * k >= 4 * c) n++;
    return { question: `For how many integers k in [−${K}, ${K}] does x² + kx + ${c} = 0 have real roots?`, answer: n, params: { c, K },
      mcq: [2 * K + 1 - n, n + 2, Math.max(n - 2, 0) === n ? n + 4 : Math.max(n - 2, 0)], steps: [`Real roots ⇔ k² ≥ 4·${c} = ${4 * c}.`, `|k| ≥ ${fmt(Math.sqrt(4 * c))} → |k| ≥ ${Math.ceil(Math.sqrt(4 * c) - 1e-9)}.`, `Count in range = ${n}.`], traps: ['Forgetting negative k.', 'Strict vs non-strict at equality (repeated root is real).'], viz: numline(-K, K, [[-K, -Math.sqrt(4 * c), true], [Math.sqrt(4 * c), K, true]]) };
  });
  R('algebra', 'hard', 'al-h3', 'α³ + β³', H => {
    const s = H.ri(-7, 7), p = H.ri(-10, 10), v = s ** 3 - 3 * p * s;
    return { question: `α, β are roots of x²${term(-s, 'x')}${p ? sg(p) : ''} = 0. Find α³ + β³.`, answer: v, params: { s, p }, mcq: [s ** 3, s ** 3 + 3 * p * s, v + 3 * s || v + 9],
      steps: [`α³+β³ = (α+β)³ − 3αβ(α+β).`, `= ${s ** 3} − 3(${p})(${s}) = ${v}.`], traps: ['Using +3αβ(α+β).', 'Sign of α+β.'], viz: graph([{ pts: plot(t => t * t - s * t + p, s / 2 - 6, s / 2 + 6) }]) };
  });

  /* ---------- INEQUALITIES & MODULUS ---------- */
  R('inequalities', 'easy', 'iq-e1', '|x − a| = b', H => {
    const a = H.ri(-10, 10), b = H.ri(1, 12);
    return { question: `Sum of all solutions of |x${sg(-a)}| = ${b}?`, answer: 2 * a, params: { a, b }, steps: [`x = ${a} ± ${b} → ${a - b}, ${a + b}.`, `Sum = ${2 * a}.`], traps: ['Only taking the positive case.', 'Sum is always 2a.'], viz: numline(a - b - 3, a + b + 3, [], [a - b, a + b]) };
  });
  R('inequalities', 'easy', 'iq-e2', 'Integers with |x − a| ≤ b', H => {
    const a = H.ri(-10, 10), b = H.ri(1, 12);
    return { question: `How many integers satisfy |x${sg(-a)}| ≤ ${b}?`, answer: 2 * b + 1, params: { a, b }, steps: [`${a - b} ≤ x ≤ ${a + b}.`, `Count = ${2 * b + 1}.`], traps: [`Answering ${2 * b} (forgetting an endpoint).`], viz: numline(a - b - 3, a + b + 3, [[a - b, a + b, true]]) };
  });
  R('inequalities', 'easy', 'iq-e3', 'Smallest integer', H => {
    const a = H.ri(2, 9), b = H.ri(-20, 20), c = H.ri(-20, 40), bound = (c - b) / a, x = Math.floor(bound) + 1;
    return { question: `Smallest integer x with ${a}x${sg(b)} > ${c}?`, answer: x, params: { a, b, c }, steps: [`x > ${c - b}/${a} = ${fmt(bound)}.`, `Smallest integer = ${x}.`], traps: ['Including the boundary.', 'Rounding the wrong way for negatives.'], viz: numline(Math.floor(bound) - 4, Math.floor(bound) + 5, [[bound, Math.floor(bound) + 5, false]], [x]) };
  });
  R('inequalities', 'medium', 'iq-m1', '(x − p)(x − q) < 0', H => H.retry(() => {
    const p = H.ri(-10, 10), q = H.ri(-10, 15); if (q - p < 2) return null;
    return { question: `How many integers satisfy (x${sg(-p)})(x${sg(-q)}) < 0?`, answer: q - p - 1, params: { p, q }, steps: [`Product negative between roots: ${p} < x < ${q}.`, `Count = ${q - p - 1}.`], traps: ['Including roots.', 'Choosing the outside region.'], viz: numline(p - 3, q + 3, [[p, q, false]]) };
  }));
  R('inequalities', 'medium', 'iq-m2', 'Min |x−a| + |x−b|', H => {
    const a = H.ri(-10, 10), b = H.ri(-10, 10);
    return { question: `Minimum value of |x${sg(-a)}| + |x${sg(-b)}|?`, answer: Math.abs(a - b), params: { a, b }, steps: [`Sum of distances from ${a} and ${b}.`, `Minimised anywhere between them: ${Math.abs(a - b)}.`], traps: ['Setting x = 0.', 'Thinking the minimum is 0.'], viz: graph([{ pts: plot(x => Math.abs(x - a) + Math.abs(x - b), Math.min(a, b) - 6, Math.max(a, b) + 6) }]) };
  });
  R('inequalities', 'medium', 'iq-m3', '|2x − a| < b', H => {
    const a = H.ri(-15, 15), b = H.ri(2, 15); let n = 0; for (let x = -100; x <= 100; x++) if (Math.abs(2 * x - a) < b) n++;
    return { question: `How many integers satisfy |2x${sg(-a)}| < ${b}?`, answer: n, params: { a, b }, steps: [`${a - b} < 2x < ${a + b} → ${fmt((a - b) / 2)} < x < ${fmt((a + b) / 2)}.`, `Count = ${n}.`], traps: ['Forgetting to halve.', 'Including endpoints in a strict inequality.'], viz: numline(Math.floor((a - b) / 2) - 2, Math.ceil((a + b) / 2) + 2, [[(a - b) / 2, (a + b) / 2, false]]) };
  });
  R('inequalities', 'hard', 'iq-h1', '|x−a| + |x−b| ≤ c', H => H.retry(() => {
    const a = H.ri(-8, 8), b = H.ri(-8, 8), c = Math.abs(a - b) + H.ri(0, 12); const lo = (a + b - c) / 2, hi = (a + b + c) / 2; let n = 0; for (let x = Math.ceil(lo - 1e-9); x <= hi + 1e-9; x++) n++;
    return { question: `Number of integer solutions of |x${sg(-a)}| + |x${sg(-b)}| ≤ ${c}?`, answer: n, params: { a, b, c }, steps: [`Outside [${Math.min(a, b)}, ${Math.max(a, b)}] the sum grows with slope 2.`, `Solution: ${fmt(lo)} ≤ x ≤ ${fmt(hi)}.`, `Integers = ${n}.`], traps: ['Assuming the solution is just between a and b.', 'Endpoint counting.'], viz: graph([{ pts: plot(x => Math.abs(x - a) + Math.abs(x - b), lo - 4, hi + 4) }, { pts: [[lo - 4, c], [hi + 4, c]], color: 'warn' }]) };
  }));
  R('inequalities', 'hard', 'iq-h2', 'Quadratic ∩ modulus', H => H.retry(() => {
    const r1 = H.ri(-8, 4), r2_ = r1 + H.ri(4, 14), m = H.ri(r1, r2_), k = H.ri(1, 4); let n = 0; for (let x = r1; x <= r2_; x++) if (Math.abs(x - m) >= k) n++; if (!n) return null;
    return { question: `How many integers x satisfy both x²${term(-(r1 + r2_), 'x')}${r1 * r2_ ? sg(r1 * r2_) : ''} ≤ 0 and |x${sg(-m)}| ≥ ${k}?`, answer: n, params: { r1, r2: r2_, m, k },
      mcq: [r2_ - r1 + 1, n + 1, Math.max(n - 2, 1) === n ? n + 3 : Math.max(n - 2, 1)], steps: [`Quadratic: ${r1} ≤ x ≤ ${r2_} (${r2_ - r1 + 1} integers).`, `Remove x with |x − ${m}| < ${k}, i.e. ${m - k + 1} … ${m + k - 1} (clipped to the interval).`, `Remaining = ${n}.`], traps: ['Removing endpoints that satisfy ≥.', 'Not clipping the excluded window to the interval.'], viz: numline(r1 - 2, r2_ + 2, [[r1, r2_, true]], [m]) };
  }));
  R('inequalities', 'hard', 'iq-h3', 'Lattice points in a region', H => {
    const n = H.ri(2, 15), mode = H.ri(0, 3);
    const [cond, v, d] = [[`|x| + |y| ≤ ${n}`, 2 * n * n + 2 * n + 1, [(2 * n + 1) ** 2, 2 * n * n + 1, 4 * n * n]], [`|x| + |y| = ${n}`, 4 * n, [4 * n + 1, 4 * n - 4, 2 * n + 1]], [`|x| + |y| < ${n}`, 2 * n * n - 2 * n + 1, [2 * n * n + 2 * n + 1, (2 * n - 1) ** 2, 2 * n * n]], [`max(|x|, |y|) ≤ ${n}`, (2 * n + 1) ** 2, [4 * n * n, 2 * n * n + 2 * n + 1, (2 * n) ** 2 + 1]]][mode];
    const m = Math.min(n, 8);
    return { question: `How many integer pairs (x, y) satisfy ${cond}?`, answer: v, params: { n, mode }, mcq: d,
      steps: mode === 3 ? [`x and y each range over −${n}…${n}: ${2 * n + 1} values.`, `Total ${(2 * n + 1)}² = ${v}.`] : mode === 1 ? [`The boundary diamond has ${n} lattice points on each side (excluding one corner).`, `4 × ${n} = ${v}.`] : [`For each x, count the y values allowed: 2(${mode === 0 ? n : n - 1} − |x|) + 1.`, `Summing over x gives ${v}.`],
      traps: ['Counting the full square instead of the diamond.', 'Forgetting points on the axes.'], viz: { type: 'coord', range: m + 1, polygon: mode === 3 ? [[m, m], [-m, m], [-m, -m], [m, -m]] : [[m, 0], [0, m], [-m, 0], [0, -m]] } };
  });

  /* ---------- FUNCTIONS ---------- */
  R('functions', 'easy', 'fn-e1', 'Evaluate f(k)', H => {
    const a = H.ri(-6, 9) || 2, b = H.ri(-15, 15), k = H.ri(-8, 10);
    return { question: `f(x) = ${a}x${sg(b)}. Find f(${k}).`, answer: a * k + b, params: { a, b, k }, steps: [`f(${k}) = ${a}(${k})${sg(b)} = ${a * k + b}.`], traps: ['Sign slip with negative k.'], viz: graph([{ pts: plot(x => a * x + b, -10, 10) }], [[k, a * k + b, `f(${k})`]]) };
  });
  R('functions', 'easy', 'fn-e2', 'Composition', H => {
    const a = H.ri(1, 5), b = H.ri(-6, 6), c = H.ri(1, 4), d = H.ri(-6, 6), k = H.ri(-5, 6), g = c * k + d, v = a * g + b;
    return { question: `f(x) = ${a}x${sg(b)}, g(x) = ${c}x${sg(d)}. Find f(g(${k})).`, answer: v, params: { a, b, c, d, k }, steps: [`g(${k}) = ${g}.`, `f(${g}) = ${v}.`], traps: ['Computing g(f(k)) instead.'], viz: graph([{ pts: plot(x => a * x + b, -10, 10) }, { pts: plot(x => c * x + d, -10, 10), color: 'warn' }]) };
  });
  R('functions', 'easy', 'fn-e3', 'Inverse', H => {
    const a = H.ri(2, 7), b = H.ri(-12, 12), x = H.ri(-8, 10), k = a * x + b;
    return { question: `f(x) = ${a}x${sg(b)}. Find f⁻¹(${k}).`, answer: x, params: { a, b, k }, steps: [`f⁻¹(y) = (y${sg(-b)})/${a}.`, `(${k}${sg(-b)})/${a} = ${x}.`], traps: ['Computing 1/f(k).', 'Inverse undoes operations in reverse order.'], viz: graph([{ pts: plot(t => a * t + b, -6, 6) }, { pts: plot(t => (t - b) / a, -20, 20), color: 'warn' }, { pts: [[-10, -10], [10, 10]], color: 'muted' }]) };
  });
  R('functions', 'medium', 'fn-m1', 'Min of quadratic', H => {
    const a = H.ri(1, 4), h = H.ri(-6, 6), m = H.ri(-15, 15), b = -2 * a * h, c = a * h * h + m;
    return { question: `Minimum value of f(x) = ${term(a, 'x²', true)}${term(b, 'x')}${c ? sg(c) : ''}?`, answer: m, params: { a, b, c }, steps: [`Vertex x = −b/2a = ${h}.`, `f(${h}) = ${m}.`], traps: ['Reporting the x-coordinate.', 'Using c as the minimum.'], viz: graph([{ pts: plot(x => a * x * x + b * x + c, h - 4, h + 4) }], [[h, m, `min ${m}`]]) };
  });
  R('functions', 'medium', 'fn-m2', 'Recursive f(x+1)', H => {
    const c = H.ri(-10, 10), d = H.ri(-5, 8), n = H.ri(5, 60);
    return { question: `f(1) = ${c} and f(x+1) = f(x)${sg(d)} for all x. Find f(${n}).`, answer: c + (n - 1) * d, params: { c, d, n }, steps: [`f is an AP with difference ${d}.`, `f(${n}) = ${c} + ${n - 1}·${d} = ${c + (n - 1) * d}.`], traps: [`Using ${n} steps instead of ${n - 1}.`], viz: { type: 'seq', terms: Array.from({ length: 8 }, (_, i) => c + i * d) } };
  });
  R('functions', 'medium', 'fn-m3', 'Min of max', H => H.retry(() => {
    const a = H.ri(-10, 10), b = H.ri(-10, 10); if ((a + b) % 2) return null;
    return { question: `Minimum value of max(x${sg(a)}, ${b} − x) over all real x?`, answer: (a + b) / 2, params: { a, b }, steps: [`Lines cross where x${sg(a)} = ${b} − x → x = ${(b - a) / 2}.`, `Value there = ${(a + b) / 2}.`], traps: ['Taking min of the two lines.'], viz: graph([{ pts: plot(x => Math.max(x + a, b - x), (b - a) / 2 - 8, (b - a) / 2 + 8) }, { pts: plot(x => x + a, (b - a) / 2 - 8, (b - a) / 2 + 8), color: 'muted' }, { pts: plot(x => b - x, (b - a) / 2 - 8, (b - a) / 2 + 8), color: 'muted' }], [[(b - a) / 2, (a + b) / 2, 'min']]) };
  }));
  R('functions', 'hard', 'fn-h1', 'f(x) + 2f(1/x)', H => H.retry(() => {
    const k = H.pick([1, 2, 3, 4, -1, -2]), a = 3 * k * H.ri(1, 6), v = a * (2 - k * k) / (3 * k); if (!isInt(v)) return null;
    return { question: `f(x) + 2f(1/x) = ${a}x for all x ≠ 0. Find f(${k}).`, answer: v, params: { a, k }, steps: [`Replace x by 1/x: f(1/x) + 2f(x) = ${a}/x.`, `Solve: 3f(x) = 2·${a}/x − ${a}x.`, `f(${k}) = ${fmt(v)}.`], traps: ['Plugging x = k only once (two unknowns).', 'Sign slip solving the system.'], viz: graph([{ pts: plot(x => a * (2 / x - x) / 3, 0.3, 5) }, { pts: plot(x => a * (2 / x - x) / 3, -5, -0.3) }], [[k, v, `f(${k})`]]) };
  }));
  R('functions', 'hard', 'fn-h2', 'f(xy) = f(x) + f(y)', H => {
    const p = H.ri(1, 9), q = H.ri(1, 9), i = H.ri(1, 5), j = H.ri(1, 4), N = 2 ** i * 3 ** j;
    return { question: `f(xy) = f(x) + f(y) for positive x, y; f(2) = ${p}, f(3) = ${q}. Find f(${N}).`, answer: i * p + j * q, params: { p, q, N }, mcq: [p * q * (i + j), i * q + j * p === i * p + j * q ? i * p + j * q + 1 : i * q + j * p, (i + j) * (p + q)],
      steps: [`${N} = 2^${i} · 3^${j}.`, `f(${N}) = ${i}f(2) + ${j}f(3) = ${i * p + j * q}.`], traps: ['Multiplying f-values.', 'Mixing exponents of 2 and 3.'], viz: graph([{ pts: plot(x => p * Math.log2(x), 0.5, 20) }]) };
  });
  R('functions', 'hard', 'fn-h3', 'Roots of |x² − a| = b', H => {
    const a = H.ri(2, 20), b = H.pick([H.ri(1, a - 1), a, H.ri(a + 1, a + 10)]), n = b < a ? 4 : b === a ? 3 : 2;
    return { question: `How many real solutions does |x² − ${a}| = ${b} have?`, answer: n, params: { a, b }, mcq: [1, 2, 3, 4].filter(v => v !== n), steps: [`x² = ${a} ± ${b}.`, `x² = ${a + b} gives 2 roots; x² = ${a - b} gives ${b < a ? 2 : b === a ? 1 : 0}.`, `Total ${n}.`], traps: ['Forgetting the negative branch.', 'x² = 0 has ONE root.'], viz: graph([{ pts: plot(x => Math.abs(x * x - a), -Math.sqrt(a + b) - 1.5, Math.sqrt(a + b) + 1.5) }, { pts: [[-Math.sqrt(a + b) - 1.5, b], [Math.sqrt(a + b) + 1.5, b]], color: 'warn' }]) };
  });

  /* ---------- LOGARITHMS ---------- */
  R('logs', 'easy', 'lg-e1', 'log_b(b^k)', H => {
    const b = H.pick([2, 3, 4, 5, 6, 7, 10]), k = H.ri(1, b === 2 ? 10 : 4), N = b ** k;
    return { question: `Find log${b === 10 ? '' : '_' + b} ${N}${b === 10 ? ' (base 10)' : ''}.`, answer: k, params: { b, N }, steps: [`${N} = ${b}^${k}.`, `log = ${k}.`], traps: ['Dividing N by b.'], viz: graph([{ pts: plot(x => Math.log(x) / Math.log(b), 0.2, N * 1.1) }], [[N, k, `${k}`]]) };
  });
  R('logs', 'easy', 'lg-e2', 'Product rule', H => {
    const b = H.pick([2, 3, 5, 6]), t = H.ri(2, 6), i = H.ri(1, t - 1), m = b ** i, n = b ** (t - i);
    return { question: `Find log_${b} ${m} + log_${b} ${n}.`, answer: t, params: { b, m, n }, steps: [`= log_${b}(${m}×${n}) = log_${b} ${m * n}.`, `= ${t}.`], traps: ['log(a)+log(b) ≠ log(a+b).'], viz: graph([{ pts: plot(x => Math.log(x) / Math.log(b), 0.2, m * n * 1.1) }], [[m * n, t, `${t}`]]) };
  });
  R('logs', 'easy', 'lg-e3', 'Chain rule', H => {
    const a = H.pick([2, 3, 5]), k = H.ri(2, 5), b = H.pick([7, 11, 13]);
    return { question: `Find log_${a} ${b} × log_${b} ${a ** k}.`, answer: k, params: { a, b, c: a ** k }, steps: [`log_a b · log_b c = log_a c.`, `log_${a} ${a ** k} = ${k}.`], traps: ['Trying to compute each log separately.'], viz: graph([{ pts: plot(x => Math.log(x) / Math.log(a), 0.2, 30) }]) };
  });
  R('logs', 'medium', 'lg-m1', 'Solve log_b x = k', H => {
    const b = H.pick([2, 3, 4, 5, 6, 7, 8, 9]), k = H.ri(1, 5);
    return { question: `If log_${b} x = ${k}, find x.`, answer: b ** k, params: { b, k }, steps: [`x = ${b}^${k} = ${b ** k}.`], traps: [`Answering ${b * k}.`], viz: graph([{ pts: plot(x => Math.log(x) / Math.log(b), 0.2, b ** k * 1.1) }], [[b ** k, k, `x`]]) };
  });
  R('logs', 'medium', 'lg-m2', 'log(x−a) + log(x+a)', H => H.retry(() => {
    const b = H.pick([2, 3, 5, 6, 7, 10]), k = H.ri(2, 8), N = b ** k; if (N > 2e6) return null;
    const pairs = []; for (let d1 = 1; d1 * d1 < N; d1++) if (N % d1 === 0 && (N / d1 - d1) % 2 === 0) pairs.push([d1, N / d1]);
    if (!pairs.length) return null; const [d1, d2] = H.pick(pairs), x = (d1 + d2) / 2, a = (d2 - d1) / 2; if (a < 1 || a > 200) return null;
    return { question: `Solve log_${b}(x − ${a}) + log_${b}(x + ${a}) = ${k}.`, answer: x, params: { a, b, k }, steps: [`log_${b}(x² − ${a * a}) = ${k} → x² = ${N} + ${a * a} = ${x * x}.`, `x = ${x} (x > ${a} for valid logs).`], traps: [`Keeping x = −${x}: logs of negative numbers do not exist.`, 'Adding the arguments instead of multiplying.'], viz: { type: 'graph', curves: [{ pts: Array.from({ length: 60 }, (_, i) => { const t = a + 0.05 + i * (x + 4 - a) / 60; return [t, Math.log(t * t - a * a) / Math.log(b)]; }) }], marks: [[x, k, `x = ${x}`]] } };
  }));
  R('logs', 'medium', 'lg-m3', 'Digits in 2ⁿ', H => {
    const n = H.ri(10, 200), d = (2n ** BigInt(n)).toString().length;
    return { question: `How many digits does 2^${n} have? (log₁₀2 ≈ 0.30103)`, answer: d, params: { n }, steps: [`log₁₀ 2^${n} = ${n} × 0.30103 = ${(n * 0.30103).toFixed(3)}.`, `Digits = ⌊${(n * 0.30103).toFixed(3)}⌋ + 1 = ${d}.`], traps: ['Forgetting the +1.', 'Rounding instead of flooring.'], viz: graph([{ pts: plot(x => x * Math.log10(2), 0, n) }], [[n, n * Math.log10(2), `${(n * 0.30103).toFixed(2)}`]]) };
  });
  R('logs', 'hard', 'lg-h1', 'log_{aᵐ} bⁿ', H => H.retry(() => {
    const p = H.ri(2, 9), m = H.ri(2, 5), n = H.ri(1, 6), v = n * p / m; if (!isInt(v * 2)) return null;
    return { question: `If log_a b = ${p}, find log_(a^${m}) (b^${n}).`, answer: v, params: { p, m, n }, steps: [`log_(a^m) b^n = (n/m) log_a b.`, `= ${n}/${m} × ${p} = ${fmt(v)}.`], traps: ['Multiplying by m instead of dividing.'], viz: graph([{ pts: plot(x => Math.log(x), 0.2, 10) }, { pts: plot(x => n / m * Math.log(x), 0.2, 10), color: 'warn' }]) };
  }));
  R('logs', 'hard', 'lg-h2', 'log_x k + log_k x = t + 1/t', H => {
    const t = H.pick([2, 2, 3]), m = t === 2 ? H.ri(2, 9) : H.ri(2, 4), k = m ** t, sum = H.ri(0, 1) === 1, rhs = t === 2 ? '5/2' : '10/3';
    const v = sum ? k ** t + m : m ** (t * t + 1);
    return { question: `Find the ${sum ? 'sum' : 'product'} of all x satisfying log_x ${k} + log_${k} x = ${rhs}.`, answer: v, params: { k, t, sum }, mcq: sum ? [k ** t, k + m, k * m] : [k * k, m ** (t * t), k ** t],
      steps: [`Let u = log_${k} x: 1/u + u = ${rhs} → u = ${t} or 1/${t}.`, `x = ${k}^${t} = ${k ** t} or ${k}^(1/${t}) = ${m}.`, `${sum ? 'Sum' : 'Product'} = ${v}.`], traps: [sum ? 'Multiplying instead of adding.' : 'Adding instead of multiplying.', `Missing the u = 1/${t} root.`],
      viz: { type: 'graph', curves: [{ pts: Array.from({ length: 50 }, (_, i) => { const u = 0.2 + i * 0.08; return [u, u + 1 / u]; }) }], marks: [[t, t + 1 / t, `u = ${t}`], [1 / t, t + 1 / t, `u = 1/${t}`]] } };
  });
  R('logs', 'hard', 'lg-h3', 'Telescoping log sum', H => H.retry(() => {
    const j = H.ri(1, 3), a = H.pick([1, 2, 3, 4, 5, 8, 10, 16, 20, 25, 40, 50]), b = a * 10 ** j - 1; if (b <= a || b > 50000) return null;
    return { question: `Find Σ log₁₀(1 + 1/n) for n = ${a} to ${b}.`, answer: j, params: { a, b }, mcq: [j + 1, j - 1 || j + 2, j * 2], steps: [`log(1 + 1/n) = log(n+1) − log n.`, `Telescopes to log₁₀(${b + 1}/${a}) = log₁₀ ${10 ** j} = ${j}.`], traps: ['Off-by-one in the end term.', 'Not recognising telescoping.'], viz: { type: 'seq', terms: [1, 2, 3, 4, 5, 6].map(n => r2(Math.log10(1 + 1 / (a + n - 1)) * 100)) } };
  }));

  /* ---------- PROGRESSIONS ---------- */
  R('progressions', 'easy', 'pg-e1', 'nth term of AP', H => {
    const a = H.ri(-10, 20), d = H.ri(-5, 9) || 3, n = H.ri(5, 60);
    return { question: `AP: ${a}, ${a + d}, ${a + 2 * d}, … Find the ${H.ord(n)} term.`, answer: a + (n - 1) * d, params: { a, d, n }, steps: [`tₙ = a + (n−1)d = ${a} + ${n - 1}×${d}.`, `= ${a + (n - 1) * d}.`], traps: ['Using n·d.', 'Counting the first term as term 0.'], viz: { type: 'seq', terms: Array.from({ length: 8 }, (_, i) => a + i * d) } };
  });
  R('progressions', 'easy', 'pg-e2', 'Sum of AP', H => {
    const a = H.ri(1, 20), d = H.ri(1, 9), n = H.ri(5, 40), S = n * (2 * a + (n - 1) * d) / 2;
    return { question: `Sum of the first ${n} terms of ${a}, ${a + d}, ${a + 2 * d}, …?`, answer: S, params: { a, d, n }, steps: [`Sₙ = n/2 [2a + (n−1)d].`, `= ${n}/2 × ${2 * a + (n - 1) * d} = ${S}.`], traps: ['Using the last term wrongly.'], viz: { type: 'seq', terms: Array.from({ length: 8 }, (_, i) => a + i * d) } };
  });
  R('progressions', 'easy', 'pg-e3', 'nth term of GP', H => {
    const a = H.ri(1, 5), r = H.pick([2, 3, -2]), n = H.ri(3, 9);
    return { question: `GP: ${a}, ${a * r}, ${a * r * r}, … Find term ${n}.`, answer: a * r ** (n - 1), params: { a, r, n }, steps: [`tₙ = a·r^(n−1) = ${a}·(${r})^${n - 1} = ${a * r ** (n - 1)}.`], traps: ['Using rⁿ.'], viz: { type: 'seq', terms: Array.from({ length: Math.min(n, 8) }, (_, i) => a * r ** i) } };
  });
  R('progressions', 'medium', 'pg-m1', 'Number of terms', H => {
    const a = H.ri(1, 50), d = H.ri(2, 9), n = H.ri(10, 80), l = a + (n - 1) * d;
    return { question: `How many terms are in ${a}, ${a + d}, ${a + 2 * d}, …, ${l}?`, answer: n, params: { a, d, l }, steps: [`n = (l − a)/d + 1 = ${l - a}/${d} + 1 = ${n}.`], traps: ['Forgetting +1.'], viz: { type: 'seq', terms: Array.from({ length: 8 }, (_, i) => a + i * d) } };
  });
  R('progressions', 'medium', 'pg-m2', 'Infinite GP', H => {
    const k = H.ri(2, 6), a = (k - 1) * H.ri(1, 20), S = a * k / (k - 1);
    return { question: `Sum to infinity of ${a} + ${a}/${k} + ${a}/${k * k} + …?`, answer: S, params: { a, k }, steps: [`r = 1/${k}; S = a/(1−r) = ${a}/(${k - 1}/${k}) = ${S}.`], traps: ['Using a/r.'], viz: { type: 'seq', terms: Array.from({ length: 7 }, (_, i) => r2(a / k ** i)) } };
  });
  R('progressions', 'medium', 'pg-m3', 'Harmonic mean', H => H.retry(() => {
    const a = H.ri(2, 60), b = H.ri(2, 60), h = 2 * a * b / (a + b); if (!isInt(h) || a === b) return null;
    return { question: `Harmonic mean of ${a} and ${b}?`, answer: h, params: { a, b }, steps: [`HM = 2ab/(a+b) = ${2 * a * b}/${a + b} = ${h}.`], traps: ['Computing AM.', 'AM ≥ GM ≥ HM always.'], viz: { type: 'bars', unit: '', items: [{ label: 'AM', value: (a + b) / 2, color: 'muted' }, { label: 'GM', value: r2(Math.sqrt(a * b)), color: 'acc2' }, { label: 'HM', value: h, color: 'accent' }] } };
  }));
  R('progressions', 'hard', 'pg-h1', 'Sum of multiples in a range', H => {
    const k = H.ri(3, 19), two = H.ri(0, 1) === 1, lo = two ? 10 : 100, hi = two ? 99 : 999, f = Math.ceil(lo / k) * k, l = Math.floor(hi / k) * k, n = (l - f) / k + 1, S = n * (f + l) / 2;
    return { question: `Sum of all ${two ? '2' : '3'}-digit numbers divisible by ${k}?`, answer: S, params: { k, lo, hi }, steps: [`First ${f}, last ${l}, n = ${n}.`, `S = ${n}(${f} + ${l})/2 = ${S}.`], traps: [`Starting at ${lo} when it is not a multiple.`, 'Miscounting n.'], viz: { type: 'seq', terms: [f, f + k, f + 2 * k, f + 3 * k, l - k, l] } };
  });
  R('progressions', 'hard', 'pg-h2', 'tₘ from Sₙ', H => {
    const a = H.ri(1, 6), b = H.ri(-8, 8), m = H.ri(5, 40), t = a * (2 * m - 1) + b;
    return { question: `The sum of the first n terms of a sequence is ${a}n²${sg(b)}n. Find its ${H.ord(m)} term.`, answer: t, params: { a, b, m }, mcq: [a * m * m + b * m, t + 2 * a, a * 2 * m + b], steps: [`tₘ = Sₘ − Sₘ₋₁.`, `= ${a}(2m − 1)${sg(b)} = ${t}.`], traps: ['Giving Sₘ.', 'Using 2m instead of 2m−1.'], viz: { type: 'seq', terms: Array.from({ length: 8 }, (_, i) => a * (2 * (i + 1) - 1) + b) } };
  });
  R('progressions', 'hard', 'pg-h3', 't_p = q, t_q = p', H => H.retry(() => {
    const p = H.ri(3, 30), q = H.ri(3, 30), r = H.ri(1, 60); if (p === q || r === p || r === q) return null;
    return { question: `In an AP the ${H.ord(p)} term is ${q} and the ${H.ord(q)} term is ${p}. Find the ${H.ord(r)} term.`, answer: p + q - r, params: { p, q, r }, mcq: [p + q + r, r - p - q, p + q - r + 1], steps: [`d = (p − q)/(q − p) = −1.`, `tᵣ = t_p + (r − p)(−1) = ${q} − ${r - p} = ${p + q - r}.`], traps: ['Sign of d.', 'Mixing which term is which.'], viz: { type: 'seq', terms: Array.from({ length: 8 }, (_, i) => p + q - (Math.min(p, q) + i)) } };
  }));

  /* ---------- MAX-MIN ---------- */
  R('maxmin', 'easy', 'mm-e1', 'Max of −x² + bx + c', H => {
    const h = H.ri(-6, 6), c = H.ri(-10, 10), b = 2 * h, M = c + h * h;
    return { question: `Maximum of f(x) = −x²${term(b, 'x')}${c ? sg(c) : ''}?`, answer: M, params: { b, c }, steps: [`Vertex at x = b/2 = ${h}.`, `f(${h}) = ${M}.`], traps: ['Reporting the x-value.'], viz: graph([{ pts: plot(x => -x * x + b * x + c, h - 5, h + 5) }], [[h, M, 'max']]) };
  });
  R('maxmin', 'easy', 'mm-e2', 'Max product, fixed sum', H => {
    const S = 2 * H.ri(3, 40);
    return { question: `Two positive numbers sum to ${S}. Maximum product?`, answer: (S / 2) ** 2, params: { S }, steps: [`Product is max when equal: ${S / 2} each.`, `${S / 2}² = ${(S / 2) ** 2}.`], traps: ['Trying extremes like 1 and S−1.'], viz: graph([{ pts: plot(x => x * (S - x), 0, S) }], [[S / 2, (S / 2) ** 2, 'max']]) };
  });
  R('maxmin', 'easy', 'mm-e3', 'Min ax + b/x', H => {
    const a = H.ri(1, 5), m = H.ri(1, 10), b = a * m * m;
    return { question: `Minimum of ${a === 1 ? '' : a}x + ${b}/x for x > 0?`, answer: 2 * a * m, params: { a, b }, steps: [`AM ≥ GM: ${a === 1 ? '' : a}x + ${b}/x ≥ 2√(${a}·${b}) = ${2 * a * m}.`, `Equality at x = ${m}.`], traps: [`Answering ${m} (the x-value).`, 'Forgetting the factor 2.'], viz: { type: 'graph', curves: [{ pts: Array.from({ length: 60 }, (_, i) => { const x = m / 4 + i * (3 * m - m / 4) / 59; return [x, a * x + b / x]; }) }], marks: [[m, 2 * a * m, 'min']] } };
  });
  R('maxmin', 'medium', 'mm-m1', 'Rectangle max area', H => {
    const P = 4 * H.ri(3, 30);
    return { question: `Maximum area of a rectangle with perimeter ${P}?`, answer: (P / 4) ** 2, params: { P }, steps: [`Square is optimal: side ${P / 4}.`, `Area ${(P / 4) ** 2}.`], traps: ['Using P/2 as side.'], viz: graph([{ pts: plot(x => x * (P / 2 - x), 0, P / 2) }], [[P / 4, (P / 4) ** 2, 'square']]) };
  });
  R('maxmin', 'medium', 'mm-m2', 'Min sum of |x − aᵢ|', H => {
    const xs = [H.ri(-10, 10), H.ri(-10, 10), H.ri(-10, 10)].sort((a, b) => a - b);
    return { question: `Minimum of |x${sg(-xs[0])}| + |x${sg(-xs[1])}| + |x${sg(-xs[2])}|?`, answer: xs[2] - xs[0], params: { xs }, steps: [`Minimised at the median x = ${xs[1]}.`, `Value = ${xs[2]} − ${xs[0]} = ${xs[2] - xs[0]}.`], traps: ['Using the mean.'], viz: graph([{ pts: plot(x => xs.reduce((s, a) => s + Math.abs(x - a), 0), xs[0] - 5, xs[2] + 5) }], [[xs[1], xs[2] - xs[0], 'median']]) };
  });
  R('maxmin', 'medium', 'mm-m3', 'Max xy with ax + by = c', H => H.retry(() => {
    const a = H.ri(1, 6), b = H.ri(1, 6), c = H.ri(4, 40), v = c * c / (4 * a * b); if (!isInt(v)) return null;
    return { question: `x, y > 0 with ${a}x + ${b}y = ${c}. Maximum of xy?`, answer: v, params: { a, b, c }, steps: [`Make ${a}x = ${b}y = ${c / 2}.`, `xy = (${c}/2)²/(${a}·${b}) = ${v}.`], traps: ['Setting x = y.'], viz: graph([{ pts: plot(x => x * (c - a * x) / b, 0, c / a) }], [[c / (2 * a), v, 'max']]) };
  }));
  R('maxmin', 'hard', 'mm-h1', 'Max xᵖyᵠ, x + y = S', H => {
    const [p, q] = H.pick([[2, 1], [1, 2], [3, 1], [1, 3], [3, 2], [2, 3]]), S = (p + q) * H.ri(1, p + q > 4 ? 6 : 10), x = p * S / (p + q), y = q * S / (p + q), v = x ** p * y ** q;
    const sup = e => ({ 1: '', 2: '²', 3: '³' }[e]);
    return { question: `x, y > 0 with x + y = ${S}. Maximum of x${sup(p)}y${sup(q)}?`, answer: v, params: { p, q, S }, steps: [`AM-GM on ${p} copies of x/${p} and ${q} copies of y/${q}.`, `Equality when x/${p} = y/${q} → x = ${x}, y = ${y}.`, `Max = ${x}${sup(p)}·${y}${sup(q)} = ${v}.`], traps: ['Splitting equally (x = y).', 'Applying AM-GM without balancing the powers.'], viz: { type: 'graph', curves: [{ pts: Array.from({ length: 60 }, (_, i) => { const t = i * S / 59; return [t, t ** p * (S - t) ** q]; }) }], marks: [[x, v, 'max']] } };
  });
  R('maxmin', 'hard', 'mm-h2', 'Min Σ(x − aᵢ)²', H => H.retry(() => {
    const a = H.ri(-10, 10), b = H.ri(-10, 10), c = H.ri(-10, 10); if ((a + b + c) % 3) return null; const m = (a + b + c) / 3, v = (a - m) ** 2 + (b - m) ** 2 + (c - m) ** 2;
    return { question: `Minimum of (x${sg(-a)})² + (x${sg(-b)})² + (x${sg(-c)})²?`, answer: v, params: { a, b, c }, mcq: [0, v + 3, [a, b, c].sort((p, q) => p - q).reduce((s, t, i, arr) => s + (t - arr[1]) ** 2, 0) || v + 6], steps: [`Minimised at the mean x = ${m}.`, `Value = ${v}.`], traps: ['Using the median (that is for |x − a|).'], viz: graph([{ pts: plot(x => (x - a) ** 2 + (x - b) ** 2 + (x - c) ** 2, m - 6, m + 6) }], [[m, v, 'mean']]) };
  }));
  R('maxmin', 'hard', 'mm-h3', 'Max of min of lines', H => H.retry(() => {
    const a = H.ri(-9, 9), b = H.ri(-9, 15); if ((b - a) % 3) return null; const x = (b - a) / 3, v = x + a;
    return { question: `Maximum value of min(x${sg(a)}, ${b} − 2x)?`, answer: v, params: { a, b }, mcq: [x, (a + b) / 2 === v ? v + 2 : (a + b) / 2, v - 1], steps: [`Lines meet: x${sg(a)} = ${b} − 2x → x = ${x}.`, `Value = ${v}.`], traps: ['Reporting the x-coordinate.'], viz: graph([{ pts: plot(t => Math.min(t + a, b - 2 * t), x - 6, x + 6) }, { pts: plot(t => t + a, x - 6, x + 6), color: 'muted' }, { pts: plot(t => b - 2 * t, x - 6, x + 6), color: 'muted' }], [[x, v, 'max']]) };
  }));
})(typeof module === 'object' && module.exports ? require('./core.js') : self.QGen);
