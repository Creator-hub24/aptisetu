/* Number Systems + Modern Math: P&C, Probability, Set Theory. */
(function (Q) {
  'use strict';
  const R = Q.register, { fmt, r2, gcd, lcm, isInt, C, fact, frac } = Q.H;
  const P = (n, r) => fact(n) / fact(n - r);
  const prob = (n, d, extra) => Object.assign({ answer: n / d, display: frac(n, d), tol: 0.0015 }, extra);

  /* ---------- NUMBER SYSTEMS ---------- */
  R('numbers', 'easy', 'ns-e1', 'LCM', H => H.retry(() => {
    const h = H.ri(2, 12), x = H.ri(2, 9), y = H.ri(2, 9); if (gcd(x, y) !== 1 || x === y) return null;
    return { question: `LCM of ${h * x} and ${h * y}?`, answer: h * x * y, params: { a: h * x, b: h * y }, steps: [`HCF = ${h}.`, `LCM = ${h * x}×${h * y}/${h} = ${h * x * y}.`], traps: ['Multiplying the numbers.'], viz: { type: 'venn', a: h * x, b: h * y, h, x, y } };
  }));
  R('numbers', 'easy', 'ns-e2', 'Unit digit', H => {
    const a = H.ri(2, 99), n = H.ri(10, 999), cyc = []; let v = a % 10; while (!cyc.includes(v)) { cyc.push(v); v = v * (a % 10) % 10; } const start = cyc.indexOf(v), len = cyc.length - start, u = n <= cyc.length ? cyc[n - 1] : cyc[start + (n - 1 - start) % len];
    return { question: `Unit digit of ${a}^${n}?`, answer: u, params: { a, n }, steps: [`Unit digits of ${a % 10}^k cycle: ${cyc.join(', ')}.`, `Cycle length ${len}; ${n} → ${u}.`], traps: ['When n mod 4 = 0, use the 4th term.'], viz: { type: 'cycle', items: cyc, n, ans: u } };
  });
  R('numbers', 'easy', 'ns-e3', 'HCF', H => H.retry(() => {
    const h = H.ri(2, 30), x = H.ri(2, 15), y = H.ri(2, 15); if (gcd(x, y) !== 1) return null;
    return { question: `HCF of ${h * x} and ${h * y}?`, answer: h, params: { a: h * x, b: h * y }, steps: [`${h * x} = ${h}×${x}, ${h * y} = ${h}×${y}; ${x}, ${y} coprime.`, `HCF = ${h}.`], traps: ['Picking a common factor that is not the greatest.'], viz: { type: 'venn', a: h * x, b: h * y, h, x, y } };
  }));
  R('numbers', 'medium', 'ns-m1', 'Divisor count', H => {
    const ea = H.ri(1, 5), eb = H.ri(0, 3), ec = H.ri(1, 3), N = 2 ** ea * 3 ** eb * 5 ** ec;
    return { question: `Number of positive divisors of ${N}?`, answer: (ea + 1) * (eb + 1) * (ec + 1), params: { N }, steps: [`${N} = 2^${ea}·3^${eb}·5^${ec}.`, `(${ea}+1)(${eb}+1)(${ec}+1) = ${(ea + 1) * (eb + 1) * (ec + 1)}.`], traps: ['Forgetting +1.'], viz: { type: 'grid', dims: [ea + 1, eb + 1, ec + 1] } };
  });
  R('numbers', 'medium', 'ns-m2', 'Trailing zeros of n!', H => {
    const n = H.ri(20, 999); let z = 0; for (let p = 5; p <= n; p *= 5) z += Math.floor(n / p);
    return { question: `Number of trailing zeros in ${n}!?`, answer: z, params: { n }, steps: [`Count 5s: ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …`, `= ${[5, 25, 125, 625].filter(p => p <= n).map(p => Math.floor(n / p)).join(' + ')} = ${z}.`], traps: ['Only ⌊n/5⌋.', 'Counting 2s (there are more 2s than 5s).'], viz: { type: 'seq', terms: [5, 25, 125, 625].filter(p => p <= n).map(p => Math.floor(n / p)) } };
  });
  R('numbers', 'medium', 'ns-m3', 'LCM + remainder', H => {
    const xs = H.pick([[4, 6, 8], [6, 9, 12], [5, 6, 8], [12, 15, 20], [7, 14, 21], [3, 4, 5], [10, 12, 15]]), r = H.ri(1, Math.min(...xs) - 1), L = xs.reduce(lcm);
    return { question: `Smallest number > ${r} that leaves remainder ${r} when divided by ${xs.join(', ')}?`, answer: L + r, params: { xs, r }, steps: [`LCM(${xs.join(', ')}) = ${L}.`, `Answer = ${L} + ${r} = ${L + r}.`], traps: ['Answering the LCM itself.', 'Using HCF.'], viz: { type: 'seq', terms: [L, 2 * L, 3 * L].map(v => v + r) } };
  });
  R('numbers', 'hard', 'ns-h1', 'aⁿ mod m', H => {
    const a = H.pick([2, 3, 7, 13, 17]), m = H.pick([5, 7, 9, 11, 13]), n = H.ri(50, 999); let r = 1n; const M = BigInt(m); let b = BigInt(a) % M, e = BigInt(n); while (e > 0n) { if (e & 1n) r = r * b % M; b = b * b % M; e >>= 1n; }
    const cyc = []; let v = a % m; while (!cyc.includes(v)) { cyc.push(v); v = v * a % m; }
    return { question: `Remainder when ${a}^${n} is divided by ${m}?`, answer: Number(r), params: { a, m, n }, steps: [`Powers of ${a} mod ${m}: ${cyc.join(', ')} (cycle ${cyc.length}).`, `${n} mod ${cyc.length} = ${n % cyc.length || cyc.length} → ${Number(r)}.`], traps: ['n mod cycle = 0 → last element.', `Fermat: ${a}^(${m}−1) ≡ 1 if ${m} prime.`], viz: { type: 'cycle', items: cyc, n, ans: Number(r) } };
  });
  R('numbers', 'hard', 'ns-h2', 'Highest power of p in n!', H => {
    const p = H.pick([2, 3, 7]), n = H.ri(20, 500); let e = 0; for (let q = p; q <= n; q *= p) e += Math.floor(n / q);
    return { question: `Highest power of ${p} that divides ${n}!?`, answer: e, params: { p, n }, mcq: [Math.floor(n / p), e + Math.floor(n / p ** 2), e - 1], steps: [`Legendre: Σ ⌊${n}/${p}^k⌋.`, `= ${e}.`], traps: ['Stopping after ⌊n/p⌋.'], viz: { type: 'seq', terms: Array.from({ length: 6 }, (_, k) => Math.floor(n / p ** (k + 1))).filter(Boolean) } };
  });
  R('numbers', 'hard', 'ns-h3', 'Sum of divisors', H => {
    const a = H.ri(1, 6), b = H.ri(1, 4), N = 2 ** a * 3 ** b, s = (2 ** (a + 1) - 1) * (3 ** (b + 1) - 1) / 2;
    return { question: `Sum of all positive divisors of ${N}?`, answer: s, params: { N }, mcq: [(a + 1) * (b + 1), s - N, s + 1], steps: [`${N} = 2^${a}·3^${b}.`, `σ = (2^${a + 1} − 1)·(3^${b + 1} − 1)/2 = ${s}.`], traps: ['Counting divisors instead of summing.', 'Excluding N itself.'], viz: { type: 'grid', dims: [a + 1, b + 1, 1] } };
  });

  /* ---------- P & C ---------- */
  const slots = (items, note) => ({ type: 'slots', items, note });
  R('pnc', 'easy', 'pc-e1', 'Arrange r of n', H => {
    const n = H.ri(4, 10), r = H.ri(2, Math.min(n, 5));
    return { question: `In how many ways can ${r} of ${n} different books be arranged on a shelf?`, answer: P(n, r), params: { n, r }, steps: [`Slots: ${Array.from({ length: r }, (_, i) => n - i).join(' × ')} = ${P(n, r)}.`], traps: ['Using nCr (order matters).'], viz: slots(Array.from({ length: r }, (_, i) => n - i)) };
  });
  R('pnc', 'easy', 'pc-e2', 'Choose r of n', H => {
    const n = H.ri(5, 15), r = H.ri(2, 5);
    return { question: `In how many ways can a team of ${r} be chosen from ${n} people?`, answer: C(n, r), params: { n, r }, steps: [`${n}C${r} = ${C(n, r)}.`], traps: ['Using nPr (order does not matter).'], viz: slots(Array.from({ length: r }, (_, i) => n - i), `÷ ${r}! = ${C(n, r)}`) };
  });
  R('pnc', 'easy', 'pc-e3', 'Distinct-letter word', H => {
    const w = H.pick(['MATH', 'PLANE', 'TIGER', 'FORMULA', 'QUANT', 'CHAIR', 'NUMBER', 'GARDEN', 'MONTH', 'RIVAL', 'LOGIC', 'PRISM', 'SPACE', 'DREAM', 'BLANK', 'WORLD', 'FRIEND', 'CANDLE', 'PLANET', 'ORANGE', 'STUDY', 'JUMBO']), first = H.ri(0, 1) === 1, n = w.length;
    const v = first ? fact(n - 1) : fact(n);
    return { question: first ? `How many arrangements of the letters of "${w}" begin with ${w[0]}?` : `How many arrangements of the letters of "${w}"?`, answer: v, params: { w, first }, steps: first ? [`Fix ${w[0]} first; arrange the other ${n - 1} letters.`, `${n - 1}! = ${v}.`] : [`${n} distinct letters → ${n}! = ${v}.`], traps: ['Assuming repeats.', first ? `Answering ${n}!.` : 'Using nCr instead of n!.'], viz: slots(first ? [1, ...Array.from({ length: n - 1 }, (_, i) => n - 1 - i)] : Array.from({ length: n }, (_, i) => n - i)) };
  });
  R('pnc', 'medium', 'pc-m1', 'Committee', H => {
    const M = H.ri(4, 10), W = H.ri(4, 10), a = H.ri(1, 3), b = H.ri(1, 3);
    return { question: `From ${M} men and ${W} women, choose ${a} men and ${b} women. Number of ways?`, answer: C(M, a) * C(W, b), params: { M, W, a, b }, steps: [`${M}C${a} × ${W}C${b} = ${C(M, a)} × ${C(W, b)} = ${C(M, a) * C(W, b)}.`], traps: ['Adding instead of multiplying (AND → ×).'], viz: slots([C(M, a), C(W, b)], 'men × women') };
  });
  R('pnc', 'medium', 'pc-m2', 'Word with repeats', H => {
    const w = H.pick(['BANANA', 'LETTER', 'APPLE', 'BALLOON', 'SUCCESS', 'COMMITTEE', 'STATISTICS', 'ALLAHABAD', 'ASSESS', 'MISSISSIPPI', 'CALCULUS', 'PEPPER', 'COFFEE', 'LEVEL', 'CHEESE', 'ADDRESS', 'ARRANGE', 'TOMORROW', 'PARALLEL', 'CANNON', 'BUBBLE', 'DIFFERENT', 'ACCESS', 'GOOGLE', 'PIZZAZZ', 'REFERENCE', 'TATTOO']), cnt = {}; [...w].forEach(c => cnt[c] = (cnt[c] || 0) + 1);
    const v = Object.values(cnt).reduce((s, k) => s / fact(k), fact(w.length));
    return { question: `How many distinct arrangements of the letters of "${w}"?`, answer: v, params: { w }, steps: [`${w.length}! / (${Object.entries(cnt).filter(e => e[1] > 1).map(e => e[1] + '!').join('·')}).`, `= ${v}.`], traps: ['Ignoring repeated letters.', 'Dividing by the number of repeated letters instead of their factorials.'], viz: slots(Object.entries(cnt).map(e => e[1]), Object.entries(cnt).map(e => e[0] + '×' + e[1]).join(' ')) };
  });
  R('pnc', 'medium', 'pc-m3', 'Circular arrangement', H => {
    const n = H.ri(4, 8), mode = H.ri(0, 4), f = fact(n - 1);
    const [q, v, st] = [[`In how many ways can ${n} people sit around a round table?`, f, `Fix one person; arrange the rest: (${n}−1)! = ${f}.`],
      [`${n} people sit around a round table. In how many ways can they sit if two particular people must sit together?`, 2 * fact(n - 2), `Glue the pair: ${n - 1} units round a table → (${n - 2})!; × 2 for the pair's order = ${2 * fact(n - 2)}.`],
      [`${n} people sit around a round table. In how many ways if two particular people must NOT sit together?`, f - 2 * fact(n - 2), `All ${f} minus together ${2 * fact(n - 2)} = ${f - 2 * fact(n - 2)}.`],
      [`How many different necklaces can be made from ${n} distinct beads (a necklace can be flipped over)?`, f / 2, `Circular (${n}−1)! = ${f}; flipping pairs them up → ${f / 2}.`],
      [`${n} people sit around a round table. In how many ways if A must sit immediately to the right of B?`, fact(n - 2), `Glue B-A in a fixed order: (${n - 1} − 1)! = ${fact(n - 2)}.`]][mode];
    return { question: q, answer: v, params: { n, mode }, steps: [st], traps: [`Using ${n}! (rotations counted as different).`, mode === 3 ? 'Forgetting that a flip gives the same necklace.' : 'Forgetting the internal order of a glued pair.'], viz: { type: 'polygon', n, people: true } };
  });
  R('pnc', 'hard', 'pc-h1', 'Row arrangements with restrictions', H => {
    const n = H.ri(4, 9), mode = H.ri(0, 3), F = fact;
    const [q, v, st] = [[`${n} people stand in a row. In how many arrangements are two particular people NOT next to each other?`, F(n) - 2 * F(n - 1), [`Total ${n}! = ${F(n)}.`, `Together: block → 2·(${n}−1)! = ${2 * F(n - 1)}.`, `Not together = ${F(n) - 2 * F(n - 1)}.`]],
      [`${n} people stand in a row. In how many arrangements are three particular people all next to each other?`, 6 * F(n - 2), [`Glue the three: ${n - 2} units → ${n - 2}!.`, `× 3! orders inside = ${6 * F(n - 2)}.`]],
      [`${n} people stand in a row. In how many arrangements is there exactly one person between A and B?`, 2 * (n - 2) * F(n - 2), [`Choose the middle person: ${n - 2} ways; A/B order: 2.`, `Treat the 3-block as one unit: (${n - 2})! arrangements.`, `${n - 2} × 2 × ${F(n - 2)} = ${2 * (n - 2) * F(n - 2)}.`]],
      [`${n} people stand in a row. In how many arrangements is A at the left end and B NOT next to A?`, (n - 2) * F(n - 2), [`A fixed at the left end; B can take ${n - 2} of the remaining ${n - 1} places (not place 2).`, `Others: (${n - 2})!. Total ${(n - 2) * F(n - 2)}.`]]][mode];
    return { question: q, answer: v, params: { n, mode }, steps: st, traps: ['Forgetting the internal order of a block.', 'Subtracting the wrong complement.'], viz: slots(Array.from({ length: n }, (_, i) => n - i), 'restricted rows') };
  });
  R('pnc', 'hard', 'pc-h2', 'Integer solutions', H => {
    const n = H.ri(5, 25), k = H.pick([3, 4]), pos = H.pick([true, false]), v = pos ? C(n - 1, k - 1) : C(n + k - 1, k - 1);
    return { question: `Number of ${pos ? 'positive' : 'non-negative'} integer solutions of ${['x', 'y', 'z', 'w'].slice(0, k).join(' + ')} = ${n}?`, answer: v, params: { n, k, pos }, mcq: [pos ? C(n + k - 1, k - 1) : C(n - 1, k - 1), C(n, k - 1), v + n], steps: [`Stars and bars: ${pos ? `C(n−1, k−1) = C(${n - 1}, ${k - 1})` : `C(n+k−1, k−1) = C(${n + k - 1}, ${k - 1})`}.`, `= ${v}.`], traps: ['Mixing positive vs non-negative formulas.'], viz: slots([n], `${n} stars, ${k - 1} bars`) };
  });
  R('pnc', 'hard', 'pc-h3', 'Rectangles in a grid', H => {
    const m = H.ri(2, 9), n = H.ri(2, 9), v = C(m + 1, 2) * C(n + 1, 2);
    return { question: `How many rectangles (including squares) are in a ${m} × ${n} grid of unit squares?`, answer: v, params: { m, n }, mcq: [m * n, C(m, 2) * C(n, 2), v + m * n], steps: [`Choose 2 of ${m + 1} vertical and 2 of ${n + 1} horizontal lines.`, `${C(m + 1, 2)} × ${C(n + 1, 2)} = ${v}.`], traps: ['Choosing from m and n instead of m+1 and n+1.'], viz: { type: 'gridrect', m, n } };
  });

  /* ---------- PROBABILITY ---------- */
  R('probability', 'easy', 'pb-e1', 'Two dice', H => H.retry(() => {
    const mode = H.ri(0, 2), s = mode === 0 ? H.ri(2, 12) : mode === 1 ? H.ri(0, 5) : H.pick([1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 36]);
    const ok = (a, b) => mode === 0 ? a + b === s : mode === 1 ? Math.abs(a - b) === s : a * b === s; let c = 0; for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) if (ok(a, b)) c++;
    const what = ['sum', 'difference (larger − smaller)', 'product'][mode];
    return Object.assign(prob(c, 36), { question: `Two fair dice are rolled. P(${what} = ${s})? (fraction or decimal)`, params: { s, mode }, steps: [`Favourable ordered pairs: ${c} of 36.`, `P = ${frac(c, 36)}.`], traps: ['Treating the possible values as equally likely.', 'Counting (a, b) and (b, a) once.'], viz: { type: 'dice', hit: ok, s } });
  }));
  R('probability', 'easy', 'pb-e2', 'Ball colour', H => {
    const r = H.ri(1, 12), b = H.ri(1, 12), g = H.ri(0, 8);
    return Object.assign(prob(r, r + b + g), { question: `A bag has ${r} red, ${b} blue${g ? `, ${g} green` : ''} balls. P(red)?`, params: { r, b, g }, steps: [`P = ${r}/${r + b + g} = ${frac(r, r + b + g)}.`], traps: ['Dividing by non-red count (odds, not probability).'], viz: { type: 'balls', groups: [[r, 'accent'], [b, 'acc2'], [g, 'warn']] } });
  });
  R('probability', 'easy', 'pb-e3', 'k heads in n tosses', H => {
    const n = H.ri(2, 7), k = H.ri(0, n);
    return Object.assign(prob(C(n, k), 2 ** n), { question: `A fair coin is tossed ${n} times. P(exactly ${k} heads)?`, params: { n, k }, steps: [`${n}C${k} = ${C(n, k)} favourable of 2^${n} = ${2 ** n}.`, `P = ${frac(C(n, k), 2 ** n)}.`], traps: ['Using k/n.'], viz: { type: 'seq', terms: Array.from({ length: n + 1 }, (_, i) => C(n, i)), hi: k } });
  });
  R('probability', 'medium', 'pb-m1', 'Both red, no replacement', H => {
    const r = H.ri(2, 10), b = H.ri(1, 10);
    return Object.assign(prob(C(r, 2), C(r + b, 2)), { question: `${r} red and ${b} blue balls; 2 drawn without replacement. P(both red)?`, params: { r, b }, steps: [`${r}C2/${r + b}C2 = ${C(r, 2)}/${C(r + b, 2)}.`, `= ${frac(C(r, 2), C(r + b, 2))}.`], traps: ['Squaring r/(r+b) (that is with replacement).'], viz: { type: 'tree', branches: [[`R ${r}/${r + b}`, `R ${r - 1}/${r + b - 1}`], [`B ${b}/${r + b}`, '']] } });
  });
  R('probability', 'medium', 'pb-m2', 'At least one success', H => {
    const n = H.ri(2, 4), [ev, k] = H.pick([['a six', 1], ['a 5 or a 6', 2], ['a number greater than 4', 2], ['a multiple of 3', 2], ['a one', 1]]), exactly = H.ri(0, 1) === 1;
    const d = 6 ** n, num = exactly ? n * k * (6 - k) ** (n - 1) : d - (6 - k) ** n;
    return Object.assign(prob(num, d), { question: `A fair die is rolled ${n} times. P(${exactly ? 'exactly one' : 'at least one'} roll shows ${ev})?`, params: { n, k, exactly }, steps: exactly ? [`Choose which roll: ${n}; that roll ${k}/6, others ${6 - k}/6 each.`, `P = ${n} × ${k} × ${6 - k}^${n - 1} / 6^${n} = ${frac(num, d)}.`] : [`P(none) = (${6 - k}/6)^${n} = ${(6 - k) ** n}/${d}.`, `P = 1 − that = ${frac(num, d)}.`], traps: [`Adding ${n} × ${k}/6.`, exactly ? 'Forgetting to choose which roll succeeds.' : 'Computing exactly one instead of at least one.'], viz: { type: 'tree', branches: [[`hit: ${k}/6`, ''], [`miss: ${6 - k}/6`, `…(${6 - k}/6)^${n}`]] } });
  });
  R('probability', 'medium', 'pb-m3', 'Two dice inequality', H => {
    const mode = H.ri(0, 2), s = mode === 0 ? H.ri(4, 12) : mode === 1 ? H.ri(3, 11) : H.pick([6, 8, 10, 12, 15, 18, 20, 24, 30]);
    const ok = (a, b) => mode === 0 ? a + b >= s : mode === 1 ? a + b <= s : a * b >= s; let c = 0; for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) if (ok(a, b)) c++;
    return Object.assign(prob(c, 36), { question: `Two dice are rolled. P(${mode === 2 ? 'product' : 'sum'} ${mode === 1 ? '≤' : '≥'} ${s})?`, params: { s, mode }, steps: [`Count ordered pairs that qualify: ${c}.`, `P = ${frac(c, 36)}.`], traps: ['Off-by-one at the boundary.', 'Counting unordered pairs.'], viz: { type: 'dice', hit: ok, s } });
  });
  R('probability', 'hard', 'pb-h1', 'Bayes: which urn?', H => H.retry(() => {
    const r1 = H.ri(1, 8), b1 = H.ri(1, 8), r2_ = H.ri(1, 8), b2 = H.ri(1, 8), n1 = r1 * (r2_ + b2), n2 = r2_ * (r1 + b1);
    return Object.assign(prob(n1, n1 + n2), { question: `Urn I: ${r1} red, ${b1} blue. Urn II: ${r2_} red, ${b2} blue. An urn is chosen at random and a red ball is drawn. P(it came from Urn I)?`, params: { r1, b1, r2: r2_, b2 }, steps: [`P(R|I) = ${r1}/${r1 + b1}, P(R|II) = ${r2_}/${r2_ + b2}.`, `Bayes: P(I|R) = P(R|I)/(P(R|I) + P(R|II)).`, `= ${frac(n1, n1 + n2)}.`], traps: ['Answering P(R|I).', 'Pooling all balls into one urn.'], viz: { type: 'tree', branches: [[`I ½`, `R ${r1}/${r1 + b1}`], [`II ½`, `R ${r2_}/${r2_ + b2}`]] } });
  }));
  R('probability', 'hard', 'pb-h2', 'Target hit', H => {
    const [a, b] = [H.ri(1, 5), H.ri(1, 5)], [c, d] = [H.ri(a + 1, 7), H.ri(b + 1, 7)], num = c * d - (c - a) * (d - b), den = c * d;
    const p = prob(num, den, { question: `A hits a target with probability ${frac(a, c)}, B with ${frac(b, d)}, independently. Both shoot once. P(target is hit)?`, params: { a, c, b, d }, steps: [`P(both miss) = ${frac(c - a, c)} × ${frac(d - b, d)} = ${frac((c - a) * (d - b), den)}.`, `P(hit) = 1 − that = ${frac(num, den)}.`], traps: ['Adding probabilities (can exceed 1).', 'Multiplying hit probabilities (that is "both hit").'], viz: { type: 'tree', branches: [[`A hit ${frac(a, c)}`, ''], [`A miss ${frac(c - a, c)}`, `B miss ${frac(d - b, d)}`]] } });
    p.mcq = [{ v: a * b / den, label: frac(a * b, den) }, { v: Math.min(a / c + b / d, 0.99), label: frac(a * d + b * c, den) }, { v: (c - a) * (d - b) / den, label: frac((c - a) * (d - b), den) }];
    return p;
  });
  R('probability', 'hard', 'pb-h3', 'Three dice sum', H => {
    const ge = H.ri(0, 1) === 1, s = ge ? H.ri(5, 17) : H.ri(3, 18); let c = 0; for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) for (let d = 1; d <= 6; d++) if (ge ? a + b + d >= s : a + b + d === s) c++;
    const dist = Array.from({ length: 16 }, (_, i) => { let k = 0; for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) for (let d = 1; d <= 6; d++) if (a + b + d === i + 3) k++; return k; });
    const p = prob(c, 216, { question: `Three fair dice are rolled. P(sum ${ge ? '≥' : '='} ${s})?`, params: { s, ge }, steps: [ge ? `Count ordered triples with sum ≥ ${s} (use the symmetric distribution: sums s and 21 − s are equally likely): ${c}.` : `Count ordered triples with sum ${s} (stars-and-bars with cap 6): ${c}.`, `P = ${c}/216 = ${frac(c, 216)}.`], traps: ['Counting unordered triples.', 'Forgetting the cap of 6 per die.'], viz: { type: 'seq', terms: dist } });
    p.mcq = [{ v: (c + 3) / 216, label: frac(c + 3, 216) }, { v: (c + 1) / 216, label: frac(c + 1, 216) }, { v: c / 108, label: frac(c, 108) }];
    return p;
  });

  /* ---------- SETS ---------- */
  R('sets', 'easy', 'st-e1', '|A ∪ B|', H => {
    const ab = H.ri(1, 20), a = ab + H.ri(1, 30), b = ab + H.ri(1, 30);
    return { question: `${a} students like tea, ${b} like coffee, ${ab} like both. How many like at least one?`, answer: a + b - ab, params: { a, b, ab }, steps: [`|A∪B| = ${a} + ${b} − ${ab} = ${a + b - ab}.`], traps: ['Not subtracting the overlap.'], viz: { type: 'venn2', a: a - ab, ab, b: b - ab, labels: ['Tea', 'Coffee'] } };
  });
  R('sets', 'easy', 'st-e2', 'Only A', H => {
    const ab = H.ri(1, 20), a = ab + H.ri(1, 30), b = ab + H.ri(1, 30);
    return { question: `${a} play cricket, ${b} play football, ${ab} play both. How many play ONLY cricket?`, answer: a - ab, params: { a, ab }, steps: [`Only A = ${a} − ${ab} = ${a - ab}.`], traps: ['Answering total cricket players.'], viz: { type: 'venn2', a: a - ab, ab, b: b - ab, labels: ['Cricket', 'Football'] } };
  });
  R('sets', 'easy', 'st-e3', 'Neither', H => {
    const ab = H.ri(1, 15), a = ab + H.ri(1, 25), b = ab + H.ri(1, 25), T = a + b - ab + H.ri(1, 30);
    return { question: `Of ${T} people, ${a} read Hindi papers, ${b} English, ${ab} both. How many read neither?`, answer: T - (a + b - ab), params: { T, a, b, ab }, steps: [`Union = ${a + b - ab}.`, `Neither = ${T} − ${a + b - ab} = ${T - a - b + ab}.`], traps: ['Forgetting to subtract both from total.'], viz: { type: 'venn2', a: a - ab, ab, b: b - ab, labels: ['Hindi', 'English'], out: T - a - b + ab } };
  });
  R('sets', 'medium', 'st-m1', 'Three-set union', H => {
    const r = { abc: H.ri(1, 8), ab: H.ri(0, 8), bc: H.ri(0, 8), ca: H.ri(0, 8), a: H.ri(1, 15), b: H.ri(1, 15), c: H.ri(1, 15) };
    const A = r.a + r.ab + r.ca + r.abc, B = r.b + r.ab + r.bc + r.abc, Cc = r.c + r.bc + r.ca + r.abc, AB = r.ab + r.abc, BC = r.bc + r.abc, CA = r.ca + r.abc, U = A + B + Cc - AB - BC - CA + r.abc;
    return { question: `|A| = ${A}, |B| = ${B}, |C| = ${Cc}, |A∩B| = ${AB}, |B∩C| = ${BC}, |C∩A| = ${CA}, |A∩B∩C| = ${r.abc}. Find |A∪B∪C|.`, answer: U, params: { A, B, C: Cc, AB, BC, CA, ABC: r.abc }, steps: [`Σ singles − Σ pairs + triple.`, `${A + B + Cc} − ${AB + BC + CA} + ${r.abc} = ${U}.`], traps: ['Forgetting to add back the triple overlap.'], viz: { type: 'venn3', r } };
  });
  R('sets', 'medium', 'st-m2', 'Divisible by p or q', H => {
    const [p, q] = H.pick([[2, 3], [3, 5], [2, 5], [3, 7], [4, 6], [5, 7]]), N = H.ri(50, 1000), L = lcm(p, q), v = Math.floor(N / p) + Math.floor(N / q) - Math.floor(N / L);
    return { question: `How many integers from 1 to ${N} are divisible by ${p} or ${q}?`, answer: v, params: { p, q, N }, steps: [`⌊${N}/${p}⌋ + ⌊${N}/${q}⌋ − ⌊${N}/${L}⌋.`, `= ${Math.floor(N / p)} + ${Math.floor(N / q)} − ${Math.floor(N / L)} = ${v}.`], traps: [`Subtracting multiples of ${p * q} instead of LCM ${L}.`], viz: { type: 'venn2', a: Math.floor(N / p) - Math.floor(N / L), ab: Math.floor(N / L), b: Math.floor(N / q) - Math.floor(N / L), labels: ['÷' + p, '÷' + q] } };
  });
  R('sets', 'medium', 'st-m3', 'Pass both', H => H.retry(() => {
    const e = H.ri(5, 40), m = H.ri(5, 40), b = H.ri(1, Math.min(e, m)); if (e + m - b >= 100) return null;
    return { question: `${e}% failed English, ${m}% failed Maths, ${b}% failed both. What % passed both?`, answer: 100 - (e + m - b), unit: '%', params: { e, m, b }, steps: [`Failed at least one = ${e} + ${m} − ${b} = ${e + m - b}%.`, `Passed both = ${100 - e - m + b}%.`], traps: ['100 − e − m (double-subtracting "both").'], viz: { type: 'venn2', a: e - b, ab: b, b: m - b, labels: ['Fail E', 'Fail M'], out: 100 - e - m + b } };
  }));
  R('sets', 'hard', 'st-h1', 'Exactly one', H => {
    const r = { abc: H.ri(1, 8), ab: H.ri(0, 8), bc: H.ri(0, 8), ca: H.ri(0, 8), a: H.ri(1, 15), b: H.ri(1, 15), c: H.ri(1, 15) };
    const S1 = 3 * r.abc + 2 * (r.ab + r.bc + r.ca) + r.a + r.b + r.c, S2 = r.ab + r.bc + r.ca + 3 * r.abc, v = r.a + r.b + r.c;
    return { question: `In three sets, |A|+|B|+|C| = ${S1}, |A∩B|+|B∩C|+|C∩A| = ${S2}, |A∩B∩C| = ${r.abc}. How many elements are in exactly one set?`, answer: v, params: { S1, S2, S3: r.abc, r }, steps: [`Exactly one = S₁ − 2S₂ + 3S₃.`, `= ${S1} − ${2 * S2} + ${3 * r.abc} = ${v}.`], traps: ['Using the union formula.', 'Coefficients 1, −2, +3 are easy to slip.'], viz: { type: 'venn3', r } };
  });
  R('sets', 'hard', 'st-h2', 'Minimum common to all', H => H.retry(() => {
    const N = 10 * H.ri(5, 20), a = H.ri(N / 2, N), b = H.ri(N / 2, N), c = H.ri(N / 2, N), v = Math.max(0, a + b + c - 2 * N); if (v === 0) return null;
    return { question: `Of ${N} people, ${a} like tea, ${b} coffee and ${c} juice. At least how many like all three?`, answer: v, params: { N, a, b, c }, mcq: [Math.max(0, a + b - N), Math.min(a, b, c), v + N / 10], steps: [`Non-likers: ${N - a} + ${N - b} + ${N - c} = ${3 * N - a - b - c}.`, `At most that many miss something → all three ≥ ${N} − ${3 * N - a - b - c} = ${v}.`], traps: ['Using the two-set bound only.'], viz: { type: 'bars', unit: '', items: [{ label: 'Tea', value: a, color: 'accent' }, { label: 'Coffee', value: b, color: 'acc2' }, { label: 'Juice', value: c, color: 'warn' }, { label: 'All 3 ≥', value: v, color: 'muted' }] } };
  }));
  R('sets', 'hard', 'st-h3', 'Divisible by none', H => {
    const [p, q, s] = H.pick([[2, 3, 5], [2, 3, 7], [3, 5, 7], [2, 5, 7]]), N = H.ri(100, 3000), f = d => Math.floor(N / d);
    const v = N - f(p) - f(q) - f(s) + f(p * q) + f(q * s) + f(p * s) - f(p * q * s);
    return { question: `How many integers from 1 to ${N} are divisible by none of ${p}, ${q}, ${s}?`, answer: v, params: { p, q, s, N }, mcq: [N - f(p) - f(q) - f(s), v + f(p * q * s) * 2 || v + 2, N - v], steps: [`Inclusion–exclusion on multiples.`, `${N} − (${f(p)} + ${f(q)} + ${f(s)}) + (${f(p * q)} + ${f(q * s)} + ${f(p * s)}) − ${f(p * q * s)} = ${v}.`], traps: ['Forgetting to add back pairwise overlaps.'], viz: { type: 'venn3', r: { a: f(p), b: f(q), c: f(s), ab: f(p * q), bc: f(q * s), ca: f(p * s), abc: f(p * q * s) }, labels: ['÷' + p, '÷' + q, '÷' + s], raw: true } };
  });
})(typeof module === 'object' && module.exports ? require('./core.js') : self.QGen);
