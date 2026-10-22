/* Geometry & Mensuration: Triangles, Mensuration 3D, Coordinate Geometry, Circles & Polygons. */
(function (Q) {
  'use strict';
  const R = Q.register, { fmt, r2, gcd, isInt } = Q.H;
  const TRIPLES = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [9, 40, 41]];
  const coord = (o) => Object.assign({ type: 'coord' }, o);

  /* ---------- TRIANGLES ---------- */
  R('geometry', 'easy', 'gm-e1', 'Hypotenuse', H => {
    const [a, b, c] = H.pick(TRIPLES.slice(0, 4)), k = H.ri(1, 6);
    return { question: `Right triangle legs ${a * k} cm and ${b * k} cm. Hypotenuse (cm)?`, answer: c * k, unit: 'cm', params: { a: a * k, b: b * k }, steps: [`h² = ${(a * k) ** 2} + ${(b * k) ** 2} = ${(c * k) ** 2}.`, `h = ${c * k}.`], traps: ['Adding legs instead of squares.', `Spot the (${a},${b},${c}) triple.`], viz: { type: 'triangle', sides: [a * k, b * k, c * k], right: true } };
  });
  R('geometry', 'easy', 'gm-e2', 'Third angle', H => {
    const A = H.ri(20, 100), B = H.ri(20, 160 - A - 10);
    return { question: `Two angles of a triangle are ${A}° and ${B}°. The third angle (°)?`, answer: 180 - A - B, unit: '°', params: { A, B }, steps: [`Sum = 180°.`, `180 − ${A} − ${B} = ${180 - A - B}°.`], traps: ['Using 360°.'], viz: { type: 'triangle', angles: [A, B, 180 - A - B] } };
  });
  R('geometry', 'easy', 'gm-e3', '½ × base × height', H => {
    const b = H.ri(2, 30), h = 2 * H.ri(1, 15);
    return { question: `Triangle with base ${b} cm and height ${h} cm. Area (cm²)?`, answer: b * h / 2, unit: 'cm²', params: { b, h }, steps: [`Area = ½ × ${b} × ${h} = ${b * h / 2}.`], traps: ['Forgetting ½.'], viz: { type: 'triangle', base: b, height: h } };
  });
  R('geometry', 'medium', 'gm-m1', 'Heron', H => {
    const [a, b, c, A] = H.pick([[13, 14, 15, 84], [5, 5, 6, 12], [10, 13, 13, 60], [9, 10, 17, 36], [7, 15, 20, 42], [5, 5, 8, 12], [11, 13, 20, 66], [13, 20, 21, 126], [10, 17, 21, 84], [6, 25, 29, 60], [17, 25, 26, 204], [4, 13, 15, 24]]), k = H.ri(1, 3), s = (a + b + c) * k / 2;
    return { question: `Area of a triangle with sides ${a * k}, ${b * k}, ${c * k} cm?`, answer: A * k * k, unit: 'cm²', params: { a: a * k, b: b * k, c: c * k }, steps: [`s = ${s}.`, `√[${s}·${s - a * k}·${s - b * k}·${s - c * k}] = ${A * k * k}.`], traps: ['Using perimeter for s.', 'Assuming a right angle.'], viz: { type: 'triangle', sides: [a * k, b * k, c * k] } };
  });
  R('geometry', 'medium', 'gm-m2', 'Similar triangles (DE ∥ BC)', H => H.retry(() => {
    const m = H.ri(1, 6), n = H.ri(1, 6), L = (m + n) * H.ri(1, 8), DE = L * m / (m + n); if (gcd(m, n) !== 1) return null;
    return { question: `In △ABC, DE ∥ BC with D on AB, E on AC and AD:DB = ${m}:${n}. If BC = ${L} cm, DE (cm)?`, answer: DE, unit: 'cm', params: { m, n, L }, steps: [`AD/AB = ${m}/${m + n}.`, `DE = ${L} × ${m}/${m + n} = ${DE}.`], traps: [`Using ${m}/${n} instead of ${m}/${m + n}.`], viz: { type: 'triangle', sides: [L * 1.1, L * 0.9, L], inner: m / (m + n) } };
  }));
  R('geometry', 'medium', 'gm-m3', 'Equilateral triangle in surds', H => {
    const a = 2 * H.ri(1, 20), area = H.ri(0, 1) === 1;
    return area ? { question: `Area of an equilateral triangle of side ${a} cm is k√3 cm². Find k.`, answer: a * a / 4, params: { a, area }, steps: [`Area = (√3/4)a² = (√3/4)·${a * a}.`, `k = ${a * a / 4}.`], traps: ['Using √3/2.', 'Forgetting to square the side.'], viz: { type: 'triangle', sides: [a, a, a] } }
      : { question: `The height of an equilateral triangle of side ${a} cm is k√3 cm. Find k.`, answer: a / 2, params: { a, area }, steps: [`h = (√3/2)a = (√3/2)·${a}.`, `k = ${a / 2}.`], traps: ['Using √3/4 (the area factor).', 'Taking half the side as the height.'], viz: { type: 'triangle', sides: [a, a, a] } };
  });
  R('geometry', 'hard', 'gm-h1', 'r + R of right triangle', H => {
    const [a, b, c] = H.pick(TRIPLES), k = H.ri(1, 4), r = (a + b - c) * k / 2, Rr = c * k / 2;
    return { question: `Right triangle with sides ${a * k}, ${b * k}, ${c * k}. Find inradius + circumradius.`, answer: r + Rr, params: { a: a * k, b: b * k, c: c * k }, steps: [`r = (a + b − c)/2 = ${fmt(r)}.`, `R = c/2 = ${fmt(Rr)}.`, `Sum = (a+b)/2 = ${fmt(r + Rr)}.`], traps: ['R = c, not c/2.', 'r = area/s (same result).'], viz: { type: 'triangle', sides: [a * k, b * k, c * k], right: true, incircle: true } };
  });
  R('geometry', 'hard', 'gm-h2', 'Angle bisector split', H => H.retry(() => {
    const b = H.ri(4, 20), c = H.ri(4, 20), a = H.ri(Math.abs(b - c) + 1, b + c - 1), BD = a * c / (b + c); if (!isInt(BD) || b === c) return null;
    return { question: `In △ABC, AB = ${c}, AC = ${b}, BC = ${a}. The bisector of ∠A meets BC at D. Find BD.`, answer: BD, params: { a, b, c }, mcq: [a * b / (b + c), a / 2, BD + 1], steps: [`BD/DC = AB/AC = ${c}/${b}.`, `BD = ${a} × ${c}/${b + c} = ${BD}.`], traps: ['Swapping AB and AC.', 'Assuming D is the midpoint.'], viz: { type: 'triangle', sides: [c, b, a] } };
  }));
  R('geometry', 'hard', 'gm-h3', 'Median² (Apollonius)', H => H.retry(() => {
    const b = H.ri(3, 20), c = H.ri(3, 20), a = 2 * H.ri(1, 15); if (a >= b + c || b >= a + c || c >= a + b) return null; const m2 = (2 * b * b + 2 * c * c - a * a) / 4; if (!isInt(m2)) return null;
    return { question: `Triangle with BC = ${a}, CA = ${b}, AB = ${c}. Find (median from A)².`, answer: m2, params: { a, b, c }, mcq: [(b * b + c * c) / 2, m2 + a, (b * b + c * c - a * a) / 2], steps: [`m² = (2b² + 2c² − a²)/4.`, `= (${2 * b * b} + ${2 * c * c} − ${a * a})/4 = ${m2}.`], traps: ['Forgetting /4.', 'Using the wrong opposite side.'], viz: { type: 'triangle', sides: [c, b, a] } };
  }));

  /* ---------- MENSURATION 3D ---------- */
  const solid = (shape, dims, label) => ({ type: 'solid', shape, dims, label });
  R('mensuration', 'easy', 'ms-e1', 'Cuboid volume', H => {
    const l = H.ri(2, 20), b = H.ri(2, 15), h = H.ri(2, 12);
    return { question: `Volume of a cuboid ${l} × ${b} × ${h} cm (cm³)?`, answer: l * b * h, unit: 'cm³', params: { l, b, h }, steps: [`V = lbh = ${l * b * h}.`], traps: ['Adding the dimensions.'], viz: solid('cuboid', { l, b, h }) };
  });
  R('mensuration', 'easy', 'ms-e2', 'Cube surface', H => {
    const a = H.ri(2, 25);
    return { question: `Total surface area of a cube of edge ${a} cm (cm²)?`, answer: 6 * a * a, unit: 'cm²', params: { a }, steps: [`TSA = 6a² = 6 × ${a * a} = ${6 * a * a}.`], traps: ['Using 4a² (lateral only).'], viz: solid('cuboid', { l: a, b: a, h: a }) };
  });
  R('mensuration', 'easy', 'ms-e3', 'Cylinder volume', H => {
    const r = 7 * H.ri(1, 3), h = H.ri(2, 20), V = 22 / 7 * r * r * h;
    return { question: `Volume of a cylinder, r = ${r} cm, h = ${h} cm (π = 22/7)?`, answer: V, unit: 'cm³', params: { r, h }, steps: [`V = πr²h = 22/7 × ${r * r} × ${h} = ${V}.`], traps: ['Using diameter.'], viz: solid('cylinder', { r, h }) };
  });
  R('mensuration', 'medium', 'ms-m1', 'Cone volume', H => {
    const r = 7 * H.ri(1, 3), h = 3 * H.ri(1, 8), V = 22 / 7 * r * r * h / 3;
    return { question: `Volume of a cone, r = ${r} cm, h = ${h} cm (π = 22/7)?`, answer: V, unit: 'cm³', params: { r, h }, steps: [`V = ⅓πr²h = ${V}.`], traps: ['Forgetting ⅓.', 'Using slant height.'], viz: solid('cone', { r, h }) };
  });
  R('mensuration', 'medium', 'ms-m2', 'Sphere & hemisphere surface', H => {
    const r = 7 * H.ri(1, 10), kind = H.ri(0, 2), pi = 22 / 7;
    const [what, S, f] = [['surface area of a sphere', 4 * pi * r * r, '4πr²'], ['curved surface area of a hemisphere', 2 * pi * r * r, '2πr²'], ['total surface area of a solid hemisphere', 3 * pi * r * r, '3πr²']][kind];
    return { question: `Find the ${what} of radius ${r} cm (π = 22/7).`, answer: S, unit: 'cm²', params: { r, kind }, steps: [`Use ${f}.`, `= ${H.fmt(S)} cm².`], traps: ['Using 4/3 πr³ (volume).', kind === 2 ? 'Forgetting the flat circular face.' : 'Mixing up sphere and hemisphere factors.'], viz: { type: 'solid', shape: 'sphere', dims: { r } } };
  });
  R('mensuration', 'medium', 'ms-m3', 'Space diagonal', H => {
    const [l, b, h, d] = H.pick([[2, 3, 6, 7], [1, 4, 8, 9], [2, 6, 9, 11], [4, 4, 7, 9], [6, 6, 7, 11], [2, 10, 11, 15]]), k = H.ri(1, 4);
    return { question: `Longest rod that fits in a ${l * k} × ${b * k} × ${h * k} m room (m)?`, answer: d * k, unit: 'm', params: { l: l * k, b: b * k, h: h * k }, steps: [`d = √(l² + b² + h²) = √${(d * k) ** 2} = ${d * k}.`], traps: ['Using a face diagonal.'], viz: solid('cuboid', { l: l * k, b: b * k, h: h * k }, 'diag') };
  });
  R('mensuration', 'hard', 'ms-h1', 'Melt & recast spheres', H => {
    const r = H.ri(1, 6), k = H.ri(2, 7), Rr = r * k;
    return { question: `A metal sphere of radius ${Rr} cm is melted into small spheres of radius ${r} cm. How many?`, answer: k ** 3, params: { R: Rr, r }, steps: [`Volume ratio = (R/r)³ = ${k}³.`, `= ${k ** 3}.`], traps: [`Using (R/r)² = ${k * k}.`, 'Surface area is NOT conserved.'], viz: solid('sphere', { r: Rr }) };
  });
  R('mensuration', 'hard', 'ms-h2', 'Painted cube', H => {
    const n = H.ri(3, 12), kind = H.pick([2, 1, 0]), v = kind === 2 ? 12 * (n - 2) : kind === 1 ? 6 * (n - 2) ** 2 : (n - 2) ** 3;
    return { question: `A painted cube is cut into ${n ** 3} equal small cubes. How many have exactly ${kind === 0 ? 'no' : kind} painted face${kind === 1 ? '' : 's'}?`, answer: v, params: { n, kind }, mcq: [12 * (n - 2), 6 * (n - 2) ** 2, (n - 2) ** 3, 8].filter(x => x !== v), steps: [`${n} per edge; interior layers n−2 = ${n - 2}.`, kind === 2 ? `Edges: 12(n−2) = ${v}.` : kind === 1 ? `Faces: 6(n−2)² = ${v}.` : `Core: (n−2)³ = ${v}.`], traps: ['Counting corner cubes (3 faces) as edges.'], viz: solid('cuboid', { l: n, b: n, h: n }, 'grid') };
  });
  R('mensuration', 'hard', 'ms-h3', 'Sphere in cylinder: rise', H => H.retry(() => {
    const r = H.ri(1, 6) * 3, Rc = H.ri(r + 1, 30), rise = 4 * r ** 3 / (3 * Rc * Rc); if (!isInt(rise * 100)) return null;
    return { question: `A sphere of radius ${r} cm is dropped into a cylinder of radius ${Rc} cm partly filled with water. Rise in water level (cm)?`, answer: r2(rise), unit: 'cm', params: { r, Rc }, mcq: [r2(4 * r ** 3 / (Rc * Rc)), r2(rise * 2), r2(r * r / Rc)], steps: [`πR²·rise = (4/3)πr³.`, `rise = 4·${r ** 3}/(3·${Rc * Rc}) = ${fmt(rise)}.`], traps: ['Forgetting 4/3.', 'Using the cylinder diameter.'], viz: solid('cylinder', { r: Rc, h: Rc * 1.4 }, 'ball') };
  }));

  /* ---------- COORDINATE ---------- */
  R('coordinate', 'easy', 'cg-e1', 'Distance', H => {
    const [a, b, c] = H.pick(TRIPLES.slice(0, 3)), k = H.ri(1, 2), x1 = H.ri(-6, 6), y1 = H.ri(-6, 6), sx = H.pick([1, -1]), sy = H.pick([1, -1]), x2 = x1 + sx * a * k, y2 = y1 + sy * b * k;
    return { question: `Distance between (${x1}, ${y1}) and (${x2}, ${y2})?`, answer: c * k, params: { x1, y1, x2, y2 }, steps: [`√(${a * k}² + ${b * k}²) = ${c * k}.`], traps: ['Subtracting coordinates in mixed order.'], viz: coord({ points: [[x1, y1, 'P'], [x2, y2, 'Q']], segments: [[[x1, y1], [x2, y2]]] }) };
  });
  R('coordinate', 'easy', 'cg-e2', 'Midpoint', H => {
    const x1 = H.ri(-10, 10), x2 = x1 + 2 * H.ri(-8, 8), y1 = H.ri(-10, 10), y2 = H.ri(-10, 10);
    return { question: `x-coordinate of the midpoint of (${x1}, ${y1}) and (${x2}, ${y2})?`, answer: (x1 + x2) / 2, params: { x1, x2 }, steps: [`(${x1} + ${x2})/2 = ${(x1 + x2) / 2}.`], traps: ['Subtracting instead of adding.'], viz: coord({ points: [[x1, y1, 'A'], [x2, y2, 'B'], [(x1 + x2) / 2, (y1 + y2) / 2, 'M']], segments: [[[x1, y1], [x2, y2]]] }) };
  });
  R('coordinate', 'easy', 'cg-e3', 'Slope', H => {
    const m = H.ri(-5, 5), x1 = H.ri(-6, 6), y1 = H.ri(-6, 6), dx = H.ri(1, 4), x2 = x1 + dx, y2 = y1 + m * dx;
    return { question: `Slope of the line through (${x1}, ${y1}) and (${x2}, ${y2})?`, answer: m, params: { x1, y1, x2, y2 }, steps: [`m = (${y2} − ${y1})/(${x2} − ${x1}) = ${m}.`], traps: ['Δx/Δy inverted.'], viz: coord({ points: [[x1, y1, 'A'], [x2, y2, 'B']], lines: [[m, y1 - m * x1]] }) };
  });
  const shoelace = pts => Math.abs(pts.reduce((s, p, i) => { const q = pts[(i + 1) % pts.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0)) / 2;
  R('coordinate', 'medium', 'cg-m1', 'Triangle area', H => H.retry(() => {
    const P = [[H.ri(-8, 8), H.ri(-8, 8)], [H.ri(-8, 8), H.ri(-8, 8)], [H.ri(-8, 8), H.ri(-8, 8)]], A = shoelace(P); if (A < 3) return null;
    return { question: `Area of the triangle with vertices (${P[0]}), (${P[1]}), (${P[2]})?`.replace(/\((-?\d+),(-?\d+)\)/g, '($1, $2)'), answer: A, params: { P }, steps: [`Shoelace: ½|Σ(xᵢyᵢ₊₁ − xᵢ₊₁yᵢ)|.`, `= ${fmt(A)}.`], traps: ['Forgetting ½ or the absolute value.'], viz: coord({ polygon: P, points: P.map((p, i) => [p[0], p[1], 'ABC'[i]]) }) };
  }));
  R('coordinate', 'medium', 'cg-m2', 'Section formula', H => H.retry(() => {
    const m = H.ri(1, 5), n = H.ri(1, 5), x1 = H.ri(-10, 10), x2 = H.ri(-10, 10), x = (m * x2 + n * x1) / (m + n); if (!isInt(x) || x1 === x2 || gcd(m, n) !== 1) return null; const y1 = H.ri(-8, 8), y2 = H.ri(-8, 8);
    return { question: `P divides the segment from A(${x1}, ${y1}) to B(${x2}, ${y2}) internally in ratio ${m}:${n}. x-coordinate of P?`, answer: x, params: { m, n, x1, x2 }, steps: [`x = (m·x₂ + n·x₁)/(m + n) = (${m * x2} + ${n * x1})/${m + n} = ${x}.`], traps: ['Pairing m with x₁.'], viz: coord({ points: [[x1, y1, 'A'], [x2, y2, 'B'], [x, (m * y2 + n * y1) / (m + n), 'P']], segments: [[[x1, y1], [x2, y2]]] }) };
  }));
  R('coordinate', 'medium', 'cg-m3', 'Point–line distance', H => {
    const [a, b] = H.pick([[3, 4], [4, 3], [5, 12], [12, 5], [-3, 4], [6, -8]]), h = Math.hypot(a, b), x0 = H.ri(-5, 5), y0 = H.ri(-5, 5), d = H.ri(1, 6), c = d * h - a * x0 - b * y0;
    return { question: `Distance from (${x0}, ${y0}) to the line ${a}x${b < 0 ? ' − ' + -b : ' + ' + b}y${c < 0 ? ' − ' + -c : ' + ' + c} = 0?`, answer: d, params: { a, b, c, x0, y0 }, steps: [`d = |${a}·${x0} + ${b}·${y0} + ${c}|/√(${a * a} + ${b * b}) = ${d * h}/${h} = ${d}.`], traps: ['Dropping the absolute value.', 'Forgetting the denominator.'], viz: coord({ points: [[x0, y0, 'P']], lines: [[-a / b, -c / b]] }) };
  });
  R('coordinate', 'hard', 'cg-h1', 'Quadrilateral area', H => H.retry(() => {
    const P = [[H.ri(-8, -1), H.ri(-8, -1)], [H.ri(1, 8), H.ri(-8, -1)], [H.ri(1, 8), H.ri(1, 8)], [H.ri(-8, -1), H.ri(1, 8)]]; const cr = P.map((p, i) => { const q = P[(i + 1) % 4], r = P[(i + 2) % 4]; return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0]); }); if (!cr.every(c => c > 0)) return null; const A = shoelace(P);
    return { question: `Area of quadrilateral ABCD: A(${P[0].join(', ')}), B(${P[1].join(', ')}), C(${P[2].join(', ')}), D(${P[3].join(', ')})?`, answer: A, params: { P }, steps: [`Vertices in order → shoelace.`, `Area = ${fmt(A)}.`], traps: ['Listing vertices out of order (crossed polygon).', 'Forgetting ½ in the shoelace formula.'], viz: coord({ polygon: P, points: P.map((p, i) => [p[0], p[1], 'ABCD'[i]]) }) };
  }));
  R('coordinate', 'hard', 'cg-h2', 'Equal-intercept line area', H => {
    const p = H.ri(1, 9), q = H.ri(1, 9), s = p + q;
    return { question: `A line through (${p}, ${q}) has equal positive intercepts on both axes. Area of the triangle it forms with the axes?`, answer: s * s / 2, params: { p, q }, mcq: [s * s, p * q, s * s / 4], steps: [`x/a + y/a = 1 → a = ${p} + ${q} = ${s}.`, `Area = a²/2 = ${s * s / 2}.`], traps: ['Forgetting ½.', 'Using a = pq.'], viz: coord({ polygon: [[0, 0], [s, 0], [0, s]], points: [[p, q, 'P']] }) };
  });
  R('coordinate', 'hard', 'cg-h3', 'Lattice points on segment', H => {
    const x1 = H.ri(-10, 10), y1 = H.ri(-10, 10), dx = H.ri(-20, 20) || 6, dy = H.ri(-20, 20) || 9, g = gcd(dx, dy);
    return { question: `How many lattice points lie on the segment from (${x1}, ${y1}) to (${x1 + dx}, ${y1 + dy}), endpoints included?`, answer: g + 1, params: { x1, y1, dx, dy }, mcq: [g, g + 2, Math.abs(dx) + 1 === g + 1 ? g + 3 : Math.abs(dx) + 1], steps: [`Δx = ${dx}, Δy = ${dy}; gcd = ${g}.`, `Points = gcd + 1 = ${g + 1}.`], traps: ['Forgetting an endpoint.', 'Using Δx + 1.'], viz: coord({ points: [[x1, y1, ''], [x1 + dx, y1 + dy, '']], segments: [[[x1, y1], [x1 + dx, y1 + dy]]], dots: Array.from({ length: g + 1 }, (_, i) => [x1 + dx * i / g, y1 + dy * i / g]) }) };
  });

  /* ---------- CIRCLES & POLYGONS ---------- */
  const circ = o => Object.assign({ type: 'circlegeo' }, o);
  R('circles', 'easy', 'ci-e1', 'Circumference', H => {
    const r = 7 * H.ri(1, 10), mode = H.ri(0, 2), C = 44 * r / 7;
    const [q, v, st] = [[`Circumference of a circle of radius ${r} cm (π = 22/7)?`, C, `C = 2πr = 2 × 22/7 × ${r} = ${C}.`], [`Circumference of a circle of diameter ${2 * r} cm (π = 22/7)?`, C, `C = πd = 22/7 × ${2 * r} = ${C}.`], [`Perimeter of a semicircle of radius ${r} cm, including the diameter (π = 22/7)?`, C / 2 + 2 * r, `πr + 2r = ${C / 2} + ${2 * r} = ${C / 2 + 2 * r}.`]][mode];
    return { question: q, answer: v, unit: 'cm', params: { r, mode }, steps: [st], traps: ['Using πr² (area).', mode === 2 ? 'Forgetting the straight edge.' : 'Mixing up radius and diameter.'], viz: { type: 'circlegeo', r, show: 'radius' } };
  });
  R('circles', 'easy', 'ci-e2', 'Polygon angles', H => {
    const n = H.pick([3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20]), mode = H.ri(0, 2);
    const [q, v] = [[`Each interior angle of a regular ${n}-gon (°)?`, 180 * (n - 2) / n], [`Each exterior angle of a regular ${n}-gon (°)?`, 360 / n], [`Sum of the interior angles of a ${n}-sided polygon (°)?`, 180 * (n - 2)]][mode];
    return { question: q, answer: v, unit: '°', params: { n, mode }, steps: mode === 2 ? [`Split into ${n - 2} triangles from one vertex.`, `${n - 2} × 180 = ${v}.`] : [`Exterior = 360/${n} = ${360 / n}.`, mode === 0 ? `Interior = 180 − ${360 / n} = ${v}.` : `That is the answer.`], traps: [mode === 2 ? 'Using n × 180.' : 'Giving the interior SUM.', 'Mixing interior and exterior.'], viz: { type: 'polygon', n } };
  });
  R('circles', 'easy', 'ci-e3', 'Diagonals', H => {
    const n = H.ri(4, 40);
    return { question: `Number of diagonals of a ${n}-sided polygon?`, answer: n * (n - 3) / 2, params: { n }, steps: [`n(n − 3)/2 = ${n}×${n - 3}/2 = ${n * (n - 3) / 2}.`], traps: ['Using nC2 (includes sides).'], viz: { type: 'polygon', n: Math.min(n, 12), diagonals: true } };
  });
  R('circles', 'medium', 'ci-m1', 'Chord length', H => {
    const [a, b, c] = H.pick(TRIPLES), k = H.ri(1, 4), sw = H.ri(0, 1) === 1, d = (sw ? b : a) * k, h = (sw ? a : b) * k;
    return { question: `A chord is ${d} cm from the centre of a circle of radius ${c * k} cm. Chord length (cm)?`, answer: 2 * h, unit: 'cm', params: { r: c * k, d }, steps: [`Half-chord = √(${c * k}² − ${d}²) = ${h}.`, `Chord = ${2 * h}.`], traps: ['Forgetting to double.', 'Adding the squares.'], viz: { type: 'circlegeo', r: c * k, chord: d } };
  });
  R('circles', 'medium', 'ci-m2', 'Tangent length', H => {
    const [a, b, c] = H.pick(TRIPLES), k = H.ri(1, 4), sw = H.ri(0, 1) === 1, r = (sw ? b : a) * k, t = (sw ? a : b) * k;
    return { question: `From a point ${c * k} cm from the centre of a circle of radius ${r} cm, find the tangent length (cm).`, answer: t, unit: 'cm', params: { d: c * k, r }, steps: [`Radius ⟂ tangent: t = √(${c * k}² − ${r}²) = ${t}.`], traps: ['Adding squares.', 'Using the distance to the circle instead of to the centre.'], viz: { type: 'circlegeo', r, tangent: c * k } };
  });
  R('circles', 'medium', 'ci-m3', 'Sector area', H => {
    const t = H.pick([30, 45, 60, 90, 120, 180]), r = 7 * H.ri(1, 4) * (t === 45 ? 2 : 1), A = t / 360 * 22 / 7 * r * r;
    return { question: `Area of a sector of angle ${t}° in a circle of radius ${r} cm (π = 22/7, 2 decimals)?`, answer: r2(A), unit: 'cm²', params: { t, r }, steps: [`A = θ/360 × πr² = ${t}/360 × 22/7 × ${r * r} = ${fmt(A)}.`], traps: ['Using arc length formula.'], viz: circ({ r, sector: t }) };
  });
  R('circles', 'hard', 'ci-h1', 'Direct common tangent', H => H.retry(() => {
    const [a, b, c] = H.pick(TRIPLES.slice(0, 4)), k = H.ri(1, 3), r1 = H.ri(a * k + 1, a * k + 12), r2_ = r1 - a * k, d = c * k; if (d <= r1 + r2_ - 0 && false) return null; if (r2_ < 1) return null;
    return { question: `Two circles of radii ${r1} and ${r2_} cm have centres ${d} cm apart. Length of their direct common tangent (cm)?`, answer: b * k, unit: 'cm', params: { r1, r2: r2_, d }, steps: [`L = √(d² − (r₁ − r₂)²) = √(${d * d} − ${(a * k) ** 2}) = ${b * k}.`], traps: ['Using (r₁ + r₂) — that is the transverse tangent.'], viz: circ({ r: r1, second: { r: r2_, d } }) };
  }));
  R('circles', 'hard', 'ci-h2', 'Polygon from angle ratio', H => {
    const k = H.ri(1, 11), n = 2 * (k + 1), D = n * (n - 3) / 2, mode = H.ri(0, 2);
    const [ask, v, d] = [['Number of diagonals', D, [n, n * (n - 1) / 2, D + n]], ['Number of sides', n, [n + 2, k + 2, 2 * k]], ['Sum of its interior angles (°)', 180 * (n - 2), [180 * n, 180 * (n - 1), 360 * k]]][mode];
    return { question: `Each interior angle of a regular polygon is ${k} times its exterior angle. ${ask}?`, answer: v, params: { k, mode }, mcq: d, steps: [`I + E = 180, I = ${k}E → E = ${H.fmt(180 / (k + 1))}°.`, `n = 360/E = ${n}.`, mode === 0 ? `Diagonals = n(n−3)/2 = ${D}.` : mode === 2 ? `Sum = (n−2)·180 = ${v}.` : `So n = ${n}.`], traps: ['Stopping at n.', 'Using nC2 for diagonals.'], viz: { type: 'polygon', n: Math.min(n, 14), diagonals: true } };
  });
  R('circles', 'hard', 'ci-h3', 'Square and circle regions', H => {
    const a = 14 * H.ri(1, 8), mode = H.ri(0, 2), pi = 22 / 7;
    const [q, v, d] = [[`A circle is inscribed in a square of side ${a} cm. Area inside the square but outside the circle (π = 22/7)?`, a * a - pi * a * a / 4, [a * a - pi * a * a, pi * a * a / 4, 2 * (a * a - pi * a * a / 4)]],
      [`A square of side ${a} cm is inscribed in a circle. Area inside the circle but outside the square (π = 22/7)?`, pi * a * a / 2 - a * a, [pi * a * a - a * a, pi * a * a / 4, a * a / 2]],
      [`A square of side ${a} cm has an inscribed circle and a circumscribed circle. Area of the ring between the two circles (π = 22/7)?`, pi * a * a / 4, [pi * a * a / 2, pi * a * a / 8, a * a]]][mode];
    return { question: q, answer: v, unit: 'cm²', params: { a, mode }, mcq: d, steps: mode === 0 ? [`Incircle r = ${a / 2}: area ${H.fmt(pi * a * a / 4)}.`, `${a * a} − ${H.fmt(pi * a * a / 4)} = ${H.fmt(v)}.`] : mode === 1 ? [`Circumradius = diagonal/2 = ${a}/√2, so r² = ${a * a / 2}.`, `${H.fmt(pi * a * a / 2)} − ${a * a} = ${H.fmt(v)}.`] : [`R² = ${a * a / 2}, r² = ${a * a / 4}.`, `π(R² − r²) = ${H.fmt(v)}.`], traps: ['Using r = a instead of a/2.', 'Using the side, not the half-diagonal, as the circumradius.'], viz: { type: 'circlegeo', r: a / 2, square: true } };
  });
})(typeof module === 'object' && module.exports ? require('./core.js') : self.QGen);
