/* Arithmetic: Percentages, P&L, TSD, Time & Work, SI/CI, Mixtures, Partnership, Averages, Ratio. */
(function (Q) {
  'use strict';
  const R = Q.register, { fmt, r2, gcd, lcm, isInt } = Q.H;
  const bars = (items, unit = '') => ({ type: 'bars', unit, items });

  /* ---------------- PERCENTAGES ---------------- */
  R('percentages', 'easy', 'pct-e1', 'x% of N', H => {
    const p = H.pick([5, 10, 12, 15, 20, 25, 30, 40, 45, 60, 75]), N = 20 * H.ri(3, 60), a = p * N / 100;
    return { question: `What is ${p}% of ${N}?`, answer: a, params: { p, N },
      steps: [`${p}% = ${p}/100.`, `${p}/100 × ${N} = ${fmt(a)}.`], traps: ['Dividing by 100 twice.', `Swap trick: ${p}% of ${N} = ${N}% of ${p}.`],
      viz: bars([{ label: 'Whole', value: N, color: 'muted' }, { label: p + '%', value: a, color: 'accent' }]) };
  });
  R('percentages', 'easy', 'pct-e2', 'A as % of B', H => {
    const p = H.pick([5, 10, 15, 20, 25, 40, 50, 60, 75, 80, 120, 150]), B = 20 * H.ri(2, 40), A = p * B / 100;
    return { question: `${A} is what percent of ${B}?`, answer: p, unit: '%', params: { A, B },
      steps: [`% = part/whole × 100.`, `${A}/${B} × 100 = ${p}%.`], traps: ['Putting the larger number on top by habit.', 'The number after "of" is the base.'],
      viz: bars([{ label: 'B (base)', value: B, color: 'muted' }, { label: 'A', value: A, color: 'accent' }]) };
  });
  R('percentages', 'easy', 'pct-e3', '% increase', H => {
    const p = H.pick([10, 20, 25, 40, 50, 60, 75, 100]), A = 20 * H.ri(2, 40), B = A * (100 + p) / 100;
    return { question: `A price rises from ₹${A} to ₹${B}. What is the percentage increase?`, answer: p, unit: '%', params: { A, B },
      steps: [`Increase = ${B} − ${A} = ${B - A}.`, `% increase = ${B - A}/${A} × 100 = ${p}%.`], traps: [`Dividing by the new value ${B}.`, 'Percentage change always uses the ORIGINAL as base.'],
      viz: bars([{ label: 'Old', value: A, color: 'muted' }, { label: 'New', value: B, color: 'accent' }], '₹') };
  });
  R('percentages', 'medium', 'pct-m1', 'Successive change', H => H.retry(() => {
    const P = 100 * H.ri(4, 60), a = H.pick([10, 20, 25, 30, 40, 50]), b = H.pick([10, 20, 25, 30, 40]);
    const mid = P * (100 + a) / 100, fin = mid * (100 - b) / 100; if (!isInt(fin)) return null;
    return { question: `A phone costs ₹${P}. Its price rises by ${a}% and then falls by ${b}%. Final price (₹)?`, answer: fin, unit: '₹', params: { P, a, b },
      steps: [`After +${a}%: ${P} × ${(100 + a) / 100} = ${fmt(mid)}.`, `After −${b}%: ${fmt(mid)} × ${(100 - b) / 100} = ${fmt(fin)}.`, `Net change = a + b + ab/100 = ${fmt(a - b - a * b / 100)}%.`],
      traps: [`Adding ${a}% − ${b}% directly.`, 'Second change applies to a new base.'],
      viz: bars([{ label: 'Start', value: P, color: 'muted' }, { label: `+${a}%`, value: mid, color: 'accent' }, { label: `−${b}%`, value: fin, color: 'warn' }], '₹') };
  }));
  R('percentages', 'medium', 'pct-m2', 'Reverse percentage', H => {
    const p = H.pick([10, 20, 25, 40, 50, 60]), k = H.ri(3, 40), orig = 100 * k / gcd(100, 100 + p), N = orig * (100 + p) / 100;
    return { question: `After a ${p}% increase, a salary is ₹${N}. What was it before the increase (₹)?`, answer: orig, unit: '₹', params: { p, N },
      steps: [`New = Old × ${(100 + p) / 100}.`, `Old = ${N} ÷ ${(100 + p) / 100} = ${orig}.`], traps: [`Subtracting ${p}% of ${N} — wrong base.`, 'Reverse a % change by dividing by the factor.'],
      viz: bars([{ label: 'Old', value: orig, color: 'muted' }, { label: 'New', value: N, color: 'accent' }], '₹') };
  });
  R('percentages', 'medium', 'pct-m3', 'Population growth', H => H.retry(() => {
    const r = H.pick([5, 10, 20, 25]), P = 400 * H.ri(5, 100), A = P * (100 + r) ** 2 / 10000; if (!isInt(A)) return null;
    return { question: `A town of ${P} people grows ${r}% per year. What is its population after 2 years?`, answer: A, params: { P, r },
      steps: [`Year 1: ${P} × ${(100 + r) / 100} = ${fmt(P * (100 + r) / 100)}.`, `Year 2: × ${(100 + r) / 100} again = ${A}.`], traps: [`Adding ${2 * r}% flat (simple growth).`, 'Growth compounds on the new base each year.'],
      viz: { type: 'growth', P, r, n: 2, kind: 'ci' } };
  }));
  R('percentages', 'hard', 'pct-h1', 'Base flip', H => H.retry(() => {
    const r = 5 * H.ri(1, 40), up = H.ri(0, 1) === 1; if (!up && r >= 100) return null;
    const a = up ? H.r2(100 * r / (100 + r)) : H.r2(100 * r / (100 - r));
    const question = up ? `A's salary is ${r}% more than B's. By what percent is B's salary less than A's? (2 decimals)` : `A's salary is ${r}% less than B's. By what percent is B's salary more than A's? (2 decimals)`;
    return { question, answer: a, unit: '%', params: { r, up }, mcq: [r, H.r2(r / 2), H.r2(a + 10)],
      steps: [`Let B = 100, so A = ${up ? 100 + r : 100 - r}.`, `Difference ${r} on base ${up ? 100 + r : 100 - r}.`, `${r}/${up ? 100 + r : 100 - r} × 100 = ${H.fmt(a)}%.`], traps: [`Answering ${r}% — the base flips.`, up ? 'Rule: r/(100+r) × 100.' : 'Rule: r/(100−r) × 100.'],
      viz: { type: 'bars', unit: '', items: [{ label: 'A', value: up ? 100 + r : 100 - r, color: 'accent' }, { label: 'B', value: 100, color: 'acc2' }] } };
  }));
  R('percentages', 'hard', 'pct-h2', 'Price–consumption–expenditure', H => {
    const p = H.pick([10, 15, 20, 25, 30, 40, 50, 60]), q = H.pick([0, 5, 10, 15, 20]), c = r2(((100 + q) / (100 + p)) * 100 - 100);
    return { question: `The price of sugar rises by ${p}%. A family wants its sugar expenditure to ${q ? `rise by only ${q}%` : 'stay the same'}. By what % must consumption change? (negative = reduce, 2 decimals)`, answer: c, unit: '%', params: { p, q },
      steps: [`Expenditure = Price × Consumption.`, `Consumption factor = ${(100 + q) / 100} / ${(100 + p) / 100} = ${fmt((100 + q) / (100 + p))}.`, `Change = ${fmt(c)}%.`], traps: [`Answering −${p - q}% (subtracting percentages).`, 'Use multiplying factors, never add/subtract %.'],
      viz: bars([{ label: 'Price', value: 100 + p, color: 'warn' }, { label: 'Consumption', value: 100 + c, color: 'accent' }, { label: 'Spend', value: 100 + q, color: 'muted' }]) };
  });
  R('percentages', 'hard', 'pct-h3', 'Election margin', H => H.retry(() => {
    const T = 1000 * H.ri(5, 90), v = H.pick([5, 10, 20, 25]), p = H.pick([52, 55, 56, 60, 62, 65, 70]);
    const valid = T * (100 - v) / 100, M = valid * (2 * p - 100) / 100; if (!isInt(M) || !isInt(valid)) return null;
    return { question: `In a two-candidate election, ${v}% of votes cast were invalid. The winner got ${p}% of the valid votes and won by ${M} votes. How many votes were cast in total?`, answer: T, params: { v, p, M },
      mcq: [valid, M * 100 / (2 * p - 100) * 1.25, T * 1.1], steps: [`Margin = (${p} − ${100 - p})% = ${2 * p - 100}% of valid votes.`, `Valid = ${M} ÷ ${(2 * p - 100) / 100} = ${valid}.`, `Valid = ${100 - v}% of total → total = ${T}.`],
      traps: ['Applying the margin % to total votes instead of valid votes.', 'Forgetting to undo the invalid-vote %.'],
      viz: bars([{ label: 'Total', value: T, color: 'muted' }, { label: 'Valid', value: valid, color: 'accent' }, { label: 'Margin', value: M, color: 'warn' }]) };
  }));

  /* ---------------- PROFIT & LOSS ---------------- */
  R('profitloss', 'easy', 'pl-e1', 'SP from profit %', H => H.retry(() => {
    const CP = 50 * H.ri(2, 80), p = H.pick([5, 10, 12, 15, 20, 25, 30, 40, 50]), SP = CP * (100 + p) / 100; if (!isInt(SP)) return null;
    return { question: `A bag bought for ₹${CP} is sold at ${p}% profit. Selling price (₹)?`, answer: SP, unit: '₹', params: { CP, p },
      steps: [`Profit = ${p}% of CP = ${fmt(CP * p / 100)}.`, `SP = ${CP} + ${fmt(CP * p / 100)} = ${SP}.`], traps: ['Profit % on SP instead of CP.', `Use factor ${(100 + p) / 100}.`],
      viz: bars([{ label: 'CP', value: CP, color: 'muted' }, { label: 'SP', value: SP, color: 'accent' }], '₹') };
  }));
  R('profitloss', 'easy', 'pl-e2', 'Profit % from CP, SP', H => {
    const p = H.pick([5, 10, 20, 25, 40, 50]), CP = 20 * H.ri(3, 50), SP = CP * (100 + p) / 100;
    return { question: `CP = ₹${CP}, SP = ₹${SP}. Find the profit %.`, answer: p, unit: '%', params: { CP, SP },
      steps: [`Profit = ${SP - CP}.`, `% = ${SP - CP}/${CP} × 100 = ${p}%.`], traps: ['Dividing by SP.', 'Profit % is always on CP unless stated.'],
      viz: bars([{ label: 'CP', value: CP, color: 'muted' }, { label: 'SP', value: SP, color: 'accent' }], '₹') };
  });
  R('profitloss', 'easy', 'pl-e3', 'SP at a loss', H => {
    const l = H.pick([5, 10, 20, 25, 30]), CP = 20 * H.ri(3, 50), SP = CP * (100 - l) / 100;
    return { question: `An item costing ₹${CP} is sold at a ${l}% loss. Selling price (₹)?`, answer: SP, unit: '₹', params: { CP, l },
      steps: [`Loss = ${l}% of ${CP} = ${fmt(CP * l / 100)}.`, `SP = ${fmt(SP)}.`], traps: ['Adding the loss.', `Factor = ${(100 - l) / 100}.`],
      viz: bars([{ label: 'CP', value: CP, color: 'muted' }, { label: 'SP', value: SP, color: 'bad' }], '₹') };
  });
  R('profitloss', 'medium', 'pl-m1', 'MP, discount → CP', H => H.retry(() => {
    const M = 100 * H.ri(3, 50), d = H.pick([10, 20, 25, 30, 40]), p = H.pick([8, 10, 12.5, 20, 25, 50]);
    const SP = M * (100 - d) / 100, CP = SP * 100 / (100 + p); if (!isInt(CP)) return null;
    return { question: `Marked at ₹${M}; after a ${d}% discount the seller still gains ${p}%. Cost price (₹)?`, answer: CP, unit: '₹', params: { M, d, p },
      steps: [`SP = ${M} × ${(100 - d) / 100} = ${fmt(SP)}.`, `CP = SP ÷ ${(100 + p) / 100} = ${fmt(CP)}.`], traps: ['Discount is on MP; profit is on CP.', 'Subtracting p% of SP.'],
      viz: bars([{ label: 'MP', value: M, color: 'muted' }, { label: 'SP', value: SP, color: 'accent' }, { label: 'CP', value: CP, color: 'warn' }], '₹') };
  }));
  R('profitloss', 'medium', 'pl-m2', 'Successive discounts', H => {
    const a = H.pick([5, 10, 15, 20, 25, 30, 40, 50]), b = H.pick([5, 10, 15, 20, 25, 30]), e = a + b - a * b / 100;
    return { question: `Successive discounts of ${a}% and ${b}% equal what single discount (%)?`, answer: e, unit: '%', params: { a, b },
      steps: [`Pay factor = ${(100 - a) / 100} × ${(100 - b) / 100} = ${fmt((100 - a) * (100 - b) / 10000)}.`, `Single discount = ${fmt(e)}%.`], traps: [`Answering ${a + b}%.`, 'Second discount applies to an already-reduced price.'],
      viz: bars([{ label: 'MP', value: 100, color: 'muted' }, { label: `−${a}%`, value: 100 - a, color: 'accent' }, { label: `−${b}%`, value: 100 - e, color: 'warn' }]) };
  });
  R('profitloss', 'medium', 'pl-m3', 'What-if CP', H => H.retry(() => {
    const [p, a, q] = H.pick([[20, 20, 25], [10, 10, 20], [25, 20, 40], [20, 10, 30], [30, 20, 50], [15, 20, 35], [40, 25, 60]]), x = 50 * H.ri(2, 40), item = H.pick(['lamp', 'backpack', 'kettle', 'desk fan', 'jacket', 'speaker']);
    const Rr = H.r2(x * ((100 + p) / 100 - (100 - a) * (100 + q) / 10000)); if (!H.isInt(Rr) || Rr <= 0) return null;
    return { question: `Meera sells a ${item} at a ${p}% profit. A new supplier offers the same ${item} ${a}% cheaper; buying from them, she could charge ₹${H.fmt(Rr)} less than now and still earn ${q}% profit. What did the ${item} originally cost her (₹)?`, answer: x, unit: '₹', params: { p, a, q, R: Rr },
      steps: [`Let the original cost be x. Current price = ${(100 + p) / 100}x.`, `New cost ${(100 - a) / 100}x; new price = ${(100 - a) / 100}x × ${(100 + q) / 100} = ${H.fmt((100 - a) * (100 + q) / 10000)}x.`, `Gap ${H.fmt((100 + p) / 100 - (100 - a) * (100 + q) / 10000)}x = ${H.fmt(Rr)} → x = ${x}.`],
      traps: ['Taking the new profit % on the old cost.', `Treating ₹${H.fmt(Rr)} as the change in cost instead of price.`], viz: { type: 'bars', unit: '₹', items: [{ label: 'old CP', value: x, color: 'muted' }, { label: 'old SP', value: x * (100 + p) / 100, color: 'accent' }, { label: 'new CP', value: x * (100 - a) / 100, color: 'muted' }, { label: 'new SP', value: x * (100 + p) / 100 - Rr, color: 'acc2' }] } };
  }));
  R('profitloss', 'hard', 'pl-h1', 'False weights', H => {
    const g = H.pick([800, 500, 625, 400, 750, 960, 900]), m = H.pick([0, 10, 20, 25]), a = r2(((1000 * (100 + m)) / (100 * g) - 1) * 100);
    return { question: `A dealer ${m ? `sells at ${m}% above cost` : 'sells at cost price'} but uses a ${g} g weight for 1 kg. Overall profit % (2 decimals)?`, answer: a, unit: '%', params: { g, m },
      mcq: [r2((1000 - g) / 10 + m), r2((1000 * (100 + m) / 100 - g) / 10), r2(a + 5)],
      steps: [`Gives ${g} g, charges for 1000 g × ${(100 + m) / 100}.`, `Profit % = (${fmt(10 * (100 + m))} − ${g})/${g} × 100 = ${fmt(a)}%.`], traps: [`Dividing by 1000 instead of ${g}.`, 'Mark-up and weight gain multiply.'],
      viz: bars([{ label: 'Charged', value: 1000, color: 'muted' }, { label: 'Given', value: g, color: 'accent' }], 'g') };
  });
  R('profitloss', 'hard', 'pl-h2', 'Same SP, ±p%', H => H.retry(() => {
    const p = H.pick([10, 20, 25, 50]), SP = H.ri(10, 200) * 6;
    const c1 = SP * 100 / (100 + p), c2 = SP * 100 / (100 - p); if (!isInt(c1) || !isInt(c2)) return null; const L = c1 + c2 - 2 * SP;
    return { question: `Two watches are each sold for ₹${SP}: one at ${p}% profit, the other at ${p}% loss. What is the overall loss (₹)?`, answer: L, unit: '₹', params: { p, SP },
      steps: [`CP₁ = ${SP}/${(100 + p) / 100} = ${c1}; CP₂ = ${SP}/${(100 - p) / 100} = ${c2}.`, `Total CP ${c1 + c2} vs SP ${2 * SP}.`, `Loss = ${L} (always ${p * p / 100}% of CP).`], traps: ['Assuming profit and loss cancel.', 'Equal % on equal SPs ⇒ always a loss of p²/100 %.'],
      viz: bars([{ label: 'CP₁', value: c1, color: 'muted' }, { label: 'CP₂', value: c2, color: 'muted' }, { label: 'SP each', value: SP, color: 'accent' }], '₹') };
  }));
  R('profitloss', 'hard', 'pl-h3', 'Markup + discount + free item', H => {
    const m = H.pick([25, 40, 50, 60, 80, 100]), d = H.pick([10, 20, 25]), n = H.pick([3, 4, 5, 9]);
    const a = r2(((100 + m) / 100 * (100 - d) / 100 * n / (n + 1) - 1) * 100);
    return { question: `A shop marks goods ${m}% above cost, gives ${d}% discount, and also gives 1 item free with every ${n} bought. Net profit % (2 decimals; negative = loss)?`, answer: a, unit: '%', params: { m, d, n },
      mcq: [r2(m - d - 100 / (n + 1)), r2(((100 + m) * (100 - d) / 10000 - 1) * 100), r2(((100 + m) / 100 * (100 - d) / 100 * (n - 1) / n - 1) * 100)],
      steps: [`Per ${n + 1} items given, paid for ${n}.`, `Revenue factor = ${(100 + m) / 100} × ${(100 - d) / 100} × ${n}/${n + 1}.`, `= ${fmt((100 + m) * (100 - d) * n / ((n + 1) * 10000))} → ${fmt(a)}%.`],
      traps: ['"1 free with n" is a discount of 1/(n+1), not 1/n.', 'Chain all three factors.'], viz: bars([{ label: 'CP', value: 100, color: 'muted' }, { label: 'MP', value: 100 + m, color: 'acc2' }, { label: 'Eff. SP', value: 100 + a, color: a >= 0 ? 'accent' : 'bad' }]) };
  });

  /* ---------------- TSD ---------------- */
  R('tsd', 'easy', 'tsd-e1', 'Train crosses pole', H => {
    const v = 18 * H.ri(2, 6), ms = v * 5 / 18, t = H.ri(6, 30), L = ms * t;
    return { question: `A ${L} m train runs at ${v} km/h. Time (s) to cross a pole?`, answer: t, unit: 's', params: { v, L },
      steps: [`${v} km/h × 5/18 = ${ms} m/s.`, `Time = ${L}/${ms} = ${t} s.`], traps: ['Forgetting ×5/18.', 'Pole has ~zero length.'], viz: { type: 'track', mode: 'pole', trains: [{ len: L, label: v + ' km/h' }] } };
  });
  R('tsd', 'easy', 'tsd-e2', 'Speed from distance & minutes', H => {
    const s = 6 * H.ri(5, 20), t = H.pick([10, 20, 30, 40, 50, 90]), D = s * t / 60;
    return { question: `A cyclist covers ${fmt(D)} km in ${t} minutes. Speed in km/h?`, answer: s, unit: 'km/h', params: { D, t },
      steps: [`${t} min = ${fmt(t / 60)} h.`, `Speed = ${fmt(D)} ÷ ${fmt(t / 60)} = ${s} km/h.`], traps: ['Dividing by minutes directly.', 'Check: faster than walking, slower than a car.'], viz: { type: 'track', mode: 'roundtrip', one: true, trains: [{ label: s + ' km/h' }, { label: '' }], D: fmt(D) } };
  });
  R('tsd', 'easy', 'tsd-e3', 'Train crosses platform', H => {
    const v = 18 * H.ri(2, 6), ms = v * 5 / 18, t = H.ri(12, 40), tot = ms * t, L = 10 * H.ri(5, Math.floor(tot / 20)), P = tot - L;
    return { question: `A ${L} m train at ${v} km/h crosses a ${P} m platform. Time (s)?`, answer: t, unit: 's', params: { v, L, P },
      steps: [`Distance = ${L} + ${P} = ${tot} m.`, `Speed = ${ms} m/s → ${t} s.`], traps: ['Using only the platform length.', 'Forgetting ×5/18.'], viz: { type: 'track', mode: 'pole', trains: [{ len: L, label: v + ' km/h' }] } };
  });
  R('tsd', 'medium', 'tsd-m1', 'Trains, opposite', H => H.retry(() => {
    const v1 = 18 * H.ri(2, 5), v2 = 18 * H.ri(1, 4), rel = (v1 + v2) * 5 / 18, t = H.ri(6, 20), tot = rel * t; if (tot < 120) return null; const L1 = 10 * H.ri(5, Math.floor(tot / 10) - 5), L2 = tot - L1; if (L2 < 50) return null;
    return { question: `Trains of ${L1} m and ${L2} m move in OPPOSITE directions at ${v1} and ${v2} km/h. Time (s) to cross each other?`, answer: t, unit: 's', params: { v1, v2, L1, L2 },
      steps: [`Relative speed = ${v1 + v2} km/h = ${rel} m/s.`, `Distance = ${tot} m → ${t} s.`], traps: ['Subtracting speeds.', 'Using one length.'], viz: { type: 'track', mode: 'opposite', trains: [{ len: L1, label: v1 + ' km/h' }, { len: L2, label: v2 + ' km/h' }] } };
  }));
  R('tsd', 'medium', 'tsd-m2', 'Boats & streams', H => {
    const b = H.ri(6, 20), s = H.ri(1, b - 2), t1 = H.ri(2, 6), t2 = H.ri(2, 6), D1 = (b + s) * t1, D2 = (b - s) * t2;
    return { question: `A boat goes ${D1} km downstream in ${t1} h and ${D2} km upstream in ${t2} h. Speed of the stream (km/h)?`, answer: s, unit: 'km/h', params: { D1, t1, D2, t2 },
      steps: [`Down = ${b + s}, Up = ${b - s} km/h.`, `Stream = (down − up)/2 = ${s}.`], traps: ['Giving the boat speed (sum/2).', 'Mixing up which speed is upstream.'], viz: bars([{ label: 'Down', value: b + s, color: 'accent' }, { label: 'Up', value: b - s, color: 'warn' }, { label: 'Stream', value: s, color: 'acc2' }], 'km/h') };
  });
  R('tsd', 'medium', 'tsd-m3', 'Trains, same direction', H => H.retry(() => {
    const v2 = 18 * H.ri(1, 4), v1 = v2 + 18 * H.ri(1, 3), rel = (v1 - v2) * 5 / 18, t = H.ri(10, 40), tot = rel * t; if (tot < 120) return null; const L1 = 10 * H.ri(5, Math.floor(tot / 10) - 5), L2 = tot - L1; if (L2 < 50) return null;
    return { question: `A ${L1} m train at ${v1} km/h overtakes a ${L2} m train at ${v2} km/h in the SAME direction. Time (s)?`, answer: t, unit: 's', params: { v1, v2, L1, L2 },
      steps: [`Relative speed = ${v1 - v2} km/h = ${rel} m/s.`, `Distance ${tot} m → ${t} s.`], traps: ['Adding speeds.', 'Using one length.'], viz: { type: 'track', mode: 'opposite', trains: [{ len: L1, label: v1 + ' km/h' }, { len: L2, label: v2 + ' km/h →' }] } };
  }));
  R('tsd', 'hard', 'tsd-h1', 'Average speed, 3 legs', H => H.retry(() => {
    const [a, b, c] = [H.ri(2, 15) * 5, H.ri(2, 15) * 5, H.ri(2, 15) * 5]; const avg = 3 / (1 / a + 1 / b + 1 / c); if (!isInt(avg) || (a === b && b === c)) return null;
    return { question: `A car covers three equal stretches at ${a}, ${b} and ${c} km/h. Average speed (km/h)?`, answer: avg, unit: 'km/h', params: { a, b, c },
      steps: [`Avg = 3/(1/${a} + 1/${b} + 1/${c}) (harmonic mean).`, `= ${avg} km/h.`], traps: [`Simple mean ${fmt((a + b + c) / 3)}.`, 'More time is spent at lower speed.'], viz: bars([{ label: a + '', value: a, color: 'muted' }, { label: b + '', value: b, color: 'muted' }, { label: c + '', value: c, color: 'muted' }, { label: 'avg', value: avg, color: 'accent' }], 'km/h') };
  }));
  R('tsd', 'hard', 'tsd-h2', 'Meeting, then t₁ and t₂', H => H.retry(() => {
    const k = H.ri(1, 5), j = H.ri(1, 5), m = H.pick([1, 4, 9]); if (k === j || gcd(k, j) !== 1) return null;
    const t1 = k * k * m, t2 = j * j * m, vA = j * H.ri(2, 12) * 5, vB = vA * k / j;
    return { question: `A and B start towards each other from P and Q. After meeting, A takes ${t1} h and B takes ${t2} h to reach their destinations. If A's speed is ${vA} km/h, B's speed (km/h)?`, answer: vB, unit: 'km/h', params: { t1, t2, vA },
      mcq: [vA * j / k, vA * t1 / t2, vA * t2 / t1], steps: [`vA/vB = √(t₂/t₁) = √(${t2}/${t1}) = ${j}/${k}.`, `vB = ${vA} × ${k}/${j} = ${fmt(vB)}.`], traps: ['Using the plain ratio t₂/t₁ (forgetting the square root).', 'Swapping which time goes on top.'],
      viz: { type: 'track', mode: 'roundtrip', trains: [{ label: 'A ' + vA }, { label: 'B ?' }], D: '' } };
  }));
  R('tsd', 'hard', 'tsd-h3', 'Late vs early', H => H.retry(() => {
    const v1 = H.ri(2, 8), v2 = v1 + H.ri(1, 4), m1 = H.pick([5, 10, 12, 15, 20]), m2 = H.pick([5, 6, 10, 15]);
    const D = v1 * v2 * (m1 + m2) / 60 / (v2 - v1); if (!isInt(D)) return null;
    return { question: `Walking at ${v1} km/h a student is ${m1} min late; at ${v2} km/h he is ${m2} min early. Distance to school (km)?`, answer: D, unit: 'km', params: { v1, v2, m1, m2 },
      mcq: [D * 2, D / 2, D + 3], steps: [`Time gap = ${m1 + m2} min = ${fmt((m1 + m2) / 60)} h.`, `D/${v1} − D/${v2} = ${fmt((m1 + m2) / 60)}.`, `D = ${D} km.`], traps: [`Using ${Math.abs(m1 - m2)} min (difference) instead of the sum.`, 'Convert minutes to hours.'],
      viz: bars([{ label: v1 + ' km/h', value: D / v1 * 60, color: 'bad' }, { label: v2 + ' km/h', value: D / v2 * 60, color: 'accent' }], 'min') };
  }));

  /* ---------------- TIME & WORK ---------------- */
  const wb = (rows, W, time) => ({ type: 'workbar', rows, W, time });
  R('work', 'easy', 'tw-e1', 'Together', H => H.retry(() => {
    const a = H.ri(3, 30), b = H.ri(3, 30), t = a * b / (a + b); if (!isInt(t) || a === b) return null; const W = lcm(a, b);
    return { question: `A finishes a job in ${a} days, B in ${b} days. Together, how many days?`, answer: t, unit: 'days', params: { a, b },
      steps: [`Take work = LCM = ${W} units. A = ${W / a}/day, B = ${W / b}/day.`, `Together ${W / a + W / b}/day → ${W}/${W / a + W / b} = ${t} days.`], traps: [`Averaging ${(a + b) / 2}.`, 'Add RATES, not days.'],
      viz: wb([{ label: 'A', rate: W / a }, { label: 'B', rate: W / b }], W, t) };
  }));
  R('work', 'easy', 'tw-e2', 'Man-days', H => H.retry(() => {
    const M = H.ri(4, 30), D = H.ri(4, 40), M2 = H.ri(4, 40), D2 = M * D / M2; if (!isInt(D2) || M === M2) return null;
    return { question: `${M} workers build a wall in ${D} days. How many days would ${M2} workers take?`, answer: D2, unit: 'days', params: { M, D, M2 },
      steps: [`Work = ${M} × ${D} = ${M * D} man-days.`, `${M * D}/${M2} = ${D2}.`], traps: ['Direct instead of inverse proportion.', 'More workers → fewer days.'], viz: bars([{ label: M + ' men', value: D, color: 'muted' }, { label: M2 + ' men', value: D2, color: 'accent' }], 'days') };
  }));
  R('work', 'easy', 'tw-e3', 'Pipe vs leak', H => H.retry(() => {
    const a = H.ri(2, 20), b = H.ri(a + 1, 40), t = a * b / (b - a); if (!isInt(t)) return null; const W = lcm(a, b);
    return { question: `A pipe fills a tank in ${a} h; a leak empties it in ${b} h. With both, time to fill (h)?`, answer: t, unit: 'h', params: { a, b },
      steps: [`Tank = ${W} units: pipe +${W / a}/h, leak −${W / b}/h.`, `Net ${W / a - W / b}/h → ${t} h.`], traps: ['Adding the leak rate.', 'Answer must exceed the pipe-only time.'], viz: wb([{ label: 'Pipe', rate: W / a }, { label: 'Leak', rate: -W / b }], W, t) };
  }));
  R('work', 'medium', 'tw-m1', 'B alone from A and A+B', H => H.retry(() => {
    const a = H.ri(4, 40), b = H.ri(4, 60), t = a * b / (a + b); if (!isInt(t) || a === b) return null;
    return { question: `A and B together finish a job in ${t} days; A alone takes ${a} days. B alone?`, answer: b, unit: 'days', params: { a, t },
      steps: [`1/B = 1/${t} − 1/${a}.`, `B = ${a}×${t}/(${a}−${t}) = ${b}.`], traps: [`Subtracting days: ${a} − ${t}.`, 'Work with rates (1/days).'], viz: wb([{ label: 'A', rate: lcm(a, b) / a }, { label: 'B', rate: lcm(a, b) / b }], lcm(a, b), t) };
  }));
  R('work', 'medium', 'tw-m2', 'A starts, B joins', H => H.retry(() => {
    const a = H.ri(6, 30), b = H.ri(6, 30), k = H.ri(1, a - 2), W = lcm(a, b); if (a === b) return null; const rem = W - k * W / a, t2 = rem / (W / a + W / b); if (!isInt(t2) || t2 <= 0) return null;
    return { question: `A can do a job in ${a} days and B in ${b} days. A works alone for ${k} days, then B joins. Total days to finish?`, answer: k + t2, unit: 'days', params: { a, b, k },
      steps: [`Work = ${W} units; A does ${W / a}/day → ${k * W / a} in ${k} days.`, `Remaining ${rem} at ${W / a + W / b}/day = ${t2} days.`, `Total ${k + t2}.`], traps: ['Forgetting to add the solo days.', 'Using the together-rate from day 1.'], viz: wb([{ label: 'A', rate: W / a }, { label: 'B', rate: W / b, start: k }], W, k + t2) };
  }));
  R('work', 'medium', 'tw-m3', 'Efficiency', H => H.retry(() => {
    const p = H.pick([20, 25, 50, 100]), b = H.ri(5, 60), t = b / (2 + p / 100); if (!isInt(t)) return null;
    return { question: `A is ${p}% more efficient than B. B alone takes ${b} days. Together?`, answer: t, unit: 'days', params: { p, b },
      steps: [`Rate A = ${(100 + p) / 100} × rate B.`, `Together = ${fmt(2 + p / 100)} × B's rate → ${b}/${fmt(2 + p / 100)} = ${t}.`], traps: [`A takes ${b}/${(100 + p) / 100} days, not ${b}×${(100 - p) / 100}.`, 'Efficiency ∝ 1/time.'],
      viz: wb([{ label: 'A', rate: (100 + p) }, { label: 'B', rate: 100 }], b * 100, t) };
  }));
  R('work', 'hard', 'tw-h1', 'Alternate days', H => H.retry(() => {
    const a = H.ri(4, 20), b = H.ri(4, 24); if (a === b) return null; const W = lcm(a, b), ra = W / a, rb = W / b;
    const n = Math.floor(W / (ra + rb)); const rem = W - n * (ra + rb); let d;
    if (rem === 0) d = 2 * n; else if (rem <= ra) d = 2 * n + rem / ra; else d = 2 * n + 1 + (rem - ra) / rb;
    if (!isInt(d * 4)) return null;
    return { question: `A alone takes ${a} days, B alone ${b} days. They work on alternate days, A starting. In how many days is the job done? (2 decimals if needed)`, answer: d, unit: 'days', params: { a, b },
      steps: [`Work = ${W} units; A ${ra}/day, B ${rb}/day; 2-day cycle = ${ra + rb}.`, `${n} cycles = ${2 * n} days → ${n * (ra + rb)} done, ${rem} left.`, `Finish the remainder day by day → ${fmt(d)} days.`],
      traps: ['Using the "together" answer ×2.', 'The last partial day may belong to A or B — check.'], viz: wb([{ label: 'A', rate: ra, alt: 0 }, { label: 'B', rate: rb, alt: 1 }], W, d) };
  }));
  R('work', 'hard', 'tw-h2', 'Pipes, outlet closed later', H => H.retry(() => {
    const a = H.ri(4, 20), b = H.ri(4, 20), c = H.ri(4, 30), k = H.ri(1, 6), W = lcm(lcm(a, b), c); if (a === b || c === a || c === b) return null;
    const net = W / a + W / b - W / c; if (net <= 0) return null; const done = k * net; if (done >= W) return null;
    const rest = (W - done) / (W / a + W / b); if (!isInt(rest * 2)) return null; const T = k + rest;
    return { question: `Pipes A and B fill a tank in ${a} h and ${b} h; pipe C empties it in ${c} h. All three are opened; C is closed after ${k} h. Total time to fill (h)?`, answer: T, unit: 'h', params: { a, b, c, k },
      mcq: [r2(W / (W / a + W / b)), T + k, T + 1], steps: [`Tank = ${W}; A+B−C = ${net}/h for ${k} h → ${done}.`, `Remaining ${W - done} at ${W / a + W / b}/h = ${fmt(rest)} h.`, `Total ${fmt(T)} h.`],
      traps: ['Forgetting the first phase has the outlet.', 'Not adding phase times.'], viz: wb([{ label: 'A', rate: W / a }, { label: 'B', rate: W / b }, { label: 'C', rate: -W / c, end: k }], W, T) };
  }));
  R('work', 'hard', 'tw-h3', 'Wages split', H => H.retry(() => {
    const a = H.ri(6, 30), b = H.ri(6, 30), t = H.ri(2, Math.min(a, b) - 1), fc = 1 - t / a - t / b; if (fc <= 0.05) return null;
    const Wg = H.ri(2, 20) * lcm(a, b) * 10; const C = Wg * fc; if (!isInt(C) || Wg > 200000) return null;
    return { question: `A alone takes ${a} days and B ${b} days. With C's help they finish in ${t} days and earn ₹${Wg}. C's share (₹)?`, answer: C, unit: '₹', params: { a, b, t, Wg },
      mcq: [Math.round(Wg / 3), Wg * t / a, Wg - C], steps: [`In ${t} days A does ${t}/${a}, B does ${t}/${b}.`, `C did 1 − ${t}/${a} − ${t}/${b} = ${fmt(fc)}.`, `C gets ${fmt(fc)} × ${Wg} = ${C}.`], traps: ['Splitting equally.', 'Wages follow work done, not time.'],
      viz: bars([{ label: 'A', value: Wg * t / a, color: 'muted' }, { label: 'B', value: Wg * t / b, color: 'acc2' }, { label: 'C', value: C, color: 'accent' }], '₹') };
  }));

  /* ---------------- SI & CI ---------------- */
  R('interest', 'easy', 'si-e1', 'Simple interest', H => {
    const P = 500 * H.ri(1, 40), r = H.pick([4, 5, 6, 8, 10, 12]), t = H.ri(2, 6), I = P * r * t / 100;
    return { question: `Simple interest on ₹${P} at ${r}% p.a. for ${t} years?`, answer: I, unit: '₹', params: { P, r, t },
      steps: [`SI = P·R·T/100 = ${P}·${r}·${t}/100 = ${I}.`], traps: ['Giving the amount instead of interest.', 'Rate must be per year with T in years.'], viz: { type: 'growth', P, r, n: t, kind: 'si' } };
  });
  R('interest', 'easy', 'si-e2', 'CI for 2 years', H => H.retry(() => {
    const P = 100 * H.ri(5, 200), r = H.pick([5, 10, 20]), I = P * ((100 + r) ** 2 - 10000) / 10000; if (!isInt(I)) return null;
    return { question: `Compound interest on ₹${P} at ${r}% p.a. for 2 years (annual)?`, answer: I, unit: '₹', params: { P, r },
      steps: [`A = ${P}(1 + ${r}/100)² = ${fmt(P + I)}.`, `CI = A − P = ${I}.`], traps: ['Using SI formula.', 'Reporting amount instead of interest.'], viz: { type: 'growth', P, r, n: 2, kind: 'both' } };
  }));
  R('interest', 'easy', 'si-e3', 'Find rate (SI)', H => {
    const P = 1000 * H.ri(1, 20), r = H.ri(2, 15), t = H.ri(2, 5), I = P * r * t / 100;
    return { question: `₹${P} earns ₹${I} simple interest in ${t} years. Rate % p.a.?`, answer: r, unit: '%', params: { P, I, t },
      steps: [`R = 100·SI/(P·T) = 100·${I}/(${P}·${t}) = ${r}%.`], traps: ['Forgetting to divide by time.', 'Using amount instead of interest.'], viz: { type: 'growth', P, r, n: t, kind: 'si' } };
  });
  R('interest', 'medium', 'si-m1', 'CI − SI (2 yrs)', H => {
    const r = H.pick([5, 10, 20, 4]), P = 2500 * H.ri(1, 20), d = P * r * r / 10000;
    return { question: `The difference between CI and SI on ₹${P} for 2 years at ${r}% p.a. is?`, answer: d, unit: '₹', params: { P, r },
      steps: [`CI − SI (2 yrs) = P(r/100)².`, `= ${P} × ${(r / 100) ** 2} = ${fmt(d)}.`], traps: ['Interest on interest exists only from year 2.', 'Using r/100 instead of (r/100)².'], viz: { type: 'growth', P, r, n: 2, kind: 'both' } };
  });
  R('interest', 'medium', 'si-m2', 'k-times by SI', H => H.retry(() => {
    const k = H.ri(2, 4), n = H.ri(4, 12), m = H.ri(k + 1, 8), y = n * (m - 1) / (k - 1); if (!isInt(y)) return null;
    return { question: `At simple interest a sum becomes ${k}× itself in ${n} years. In how many years will it become ${m}×?`, answer: y, unit: 'years', params: { k, n, m },
      steps: [`Interest = ${k - 1}P in ${n} yrs → P per ${fmt(n / (k - 1))} yrs.`, `Need ${m - 1}P → ${y} yrs.`], traps: [`Using ${m}/${k} ratio directly.`, 'SI grows linearly, not multiplicatively.'], viz: { type: 'growth', P: 100, r: 100 * (k - 1) / n, n: Math.min(y, 30), kind: 'si' } };
  }));
  R('interest', 'medium', 'si-m3', 'Half-yearly CI', H => H.retry(() => {
    const r = H.pick([10, 20, 8, 4]), P = 400 * H.ri(2, 50), A = P * (1 + r / 200) ** 2, I = A - P; if (!isInt(I * 100)) return null;
    return { question: `CI on ₹${P} for 1 year at ${r}% p.a. compounded half-yearly?`, answer: r2(I), unit: '₹', params: { P, r },
      steps: [`Half-yearly: rate ${r / 2}% for 2 periods.`, `A = ${P} × (${1 + r / 200})² = ${fmt(A)}.`, `CI = ${fmt(I)}.`], traps: [`Using ${r}% for 1 period.`, 'Halve the rate AND double the periods.'], viz: { type: 'growth', P, r: r / 2, n: 2, kind: 'ci' } };
  }));
  R('interest', 'hard', 'si-h1', 'P from A₂ and A₃', H => H.retry(() => {
    const r = H.pick([5, 10, 20, 25]), P = 1600 * H.ri(1, 20), A2 = P * (100 + r) ** 2 / 10000, A3 = A2 * (100 + r) / 100; if (!isInt(A3)) return null;
    return { question: `A sum at compound interest amounts to ₹${A2} in 2 years and ₹${A3} in 3 years. Find the principal.`, answer: P, unit: '₹', params: { A2, A3 },
      mcq: [A2 - (A3 - A2) * 2, r2(A2 * 100 / (100 + 2 * r)), A2 - (A3 - A2)], steps: [`r = (${A3} − ${A2})/${A2} = ${r}%.`, `P = ${A2}/(${(100 + r) / 100})² = ${P}.`], traps: ['Subtracting two years of SI from A₂.', 'Rate is on A₂, not on P.'], viz: { type: 'growth', P, r, n: 3, kind: 'ci' } };
  }));
  R('interest', 'hard', 'si-h2', 'CI − SI (3 yrs)', H => {
    const r = H.pick([10, 20, 5]), P = 8000 * H.ri(1, 10), d = r2(P * ((1 + r / 100) ** 3 - 1 - 3 * r / 100));
    return { question: `The difference between CI and SI for 3 years at ${r}% p.a. is ₹${fmt(d)}. Find the principal (₹).`, answer: P, unit: '₹', params: { d, r },
      steps: [`Diff (3 yrs) = P[(r/100)³ + 3(r/100)²] = P × ${fmt((1 + r / 100) ** 3 - 1 - 3 * r / 100)}.`, `P = ${fmt(d)}/${fmt((1 + r / 100) ** 3 - 1 - 3 * r / 100)} = ${P}.`], traps: ['Using the 2-year formula P(r/100)².', 'Missing the 3(r/100)² term.'], viz: { type: 'growth', P, r, n: 3, kind: 'both' } };
  });
  R('interest', 'hard', 'si-h3', 'Equal instalments', H => H.retry(() => {
    const r = H.pick([10, 20, 5]), P = 100 * H.ri(10, 400), X = P * (1 + r / 100) ** 2 / (2 + r / 100); if (!isInt(X)) return null;
    return { question: `A loan of ₹${P} at ${r}% p.a. CI is repaid in 2 equal annual instalments. Each instalment (₹)?`, answer: X, unit: '₹', params: { P, r },
      mcq: [P / 2 * (1 + r / 100), r2(P * (1 + r / 100) ** 2 / 2), P / 2], steps: [`P = X/${(100 + r) / 100} + X/${(100 + r) / 100}².`, `X = P(1+r)²/(2+r) = ${X}.`], traps: ['Halving the 2-year amount.', 'Each instalment is discounted back separately.'], viz: { type: 'growth', P, r, n: 2, kind: 'ci' } };
  }));

  /* ---------------- MIXTURES & ALLIGATION ---------------- */
  R('mixtures', 'easy', 'mx-e1', 'Mean price', H => H.retry(() => {
    const a = H.ri(20, 60), b = H.ri(a + 5, 120), m = H.ri(1, 5), n = H.ri(1, 5), mean = (a * m + b * n) / (m + n); if (!isInt(mean) || m === n || gcd(m, n) !== 1) return null;
    return { question: `Rice at ₹${a}/kg and ₹${b}/kg is mixed in ratio ${m}:${n}. Price of the mixture per kg?`, answer: mean, unit: '₹', params: { a, b, m, n },
      steps: [`Weighted mean = (${a}×${m} + ${b}×${n})/${m + n} = ${mean}.`], traps: [`Simple average ${fmt((a + b) / 2)}.`, 'Mean lies nearer the larger share.'], viz: { type: 'alligation', a, b, m: mean, la: '₹' + a, lb: '₹' + b } };
  }));
  R('mixtures', 'easy', 'mx-e2', 'Alligation quantity', H => H.retry(() => {
    const a = H.ri(20, 60), b = H.ri(a + 4, 100), m = H.ri(a + 1, b - 1), x = 5 * H.ri(2, 20), y = x * (m - a) / (b - m); if (!isInt(y) || y > 300) return null;
    return { question: `How many kg of tea at ₹${b}/kg must be mixed with ${x} kg at ₹${a}/kg to get a mixture worth ₹${m}/kg?`, answer: y, unit: 'kg', params: { a, b, m, x },
      steps: [`Alligation: cheap : dear = (${b} − ${m}) : (${m} − ${a}) = ${b - m}:${m - a}.`, `Dear = ${x} × ${m - a}/${b - m} = ${y} kg.`], traps: ['Crossing differences the wrong way.', 'Mean must lie between the two prices.'], viz: { type: 'alligation', a, b, m, la: '₹' + a, lb: '₹' + b } };
  }));
  R('mixtures', 'easy', 'mx-e3', 'Dilution %', H => H.retry(() => {
    const V = 10 * H.ri(2, 12), p = H.pick([20, 25, 30, 40, 50, 60]), w = 5 * H.ri(1, 8), c = V * p / (V + w); if (!isInt(c * 100)) return null;
    return { question: `${V} L of a ${p}% acid solution is diluted with ${w} L water. New concentration (%)?`, answer: r2(c), unit: '%', params: { V, p, w },
      steps: [`Acid = ${fmt(V * p / 100)} L (unchanged).`, `% = ${fmt(V * p / 100)}/${V + w} × 100 = ${fmt(c)}%.`], traps: ['Changing the acid amount.', 'Dividing by the old volume.'], viz: { type: 'mixture', M: V * p / 100, W: V * (100 - p) / 100, add: w, labels: ['Acid', 'Water'] } };
  }));
  R('mixtures', 'medium', 'mx-m1', 'Repeated replacement', H => {
    const V = H.pick([20, 40, 50, 60, 80, 100, 120, 200]), x = V / H.pick([4, 5, 10]), k = H.pick([2, 3]), liq = H.pick(['milk', 'juice', 'wine']), m = V * (1 - x / V) ** k;
    return { question: `From ${V} L of ${liq}, ${x} L is removed and replaced with water. This is done ${k === 2 ? 'twice' : 'three times'} in all. ${liq[0].toUpperCase() + liq.slice(1)} left (L, 2 decimals)?`, answer: H.r2(m), unit: 'L', params: { V, x, k },
      steps: [`Each step keeps (1 − ${x}/${V}) = ${H.fmt(1 - x / V)} of the ${liq}.`, `${V} × ${H.fmt(1 - x / V)}^${k} = ${H.fmt(m)} L.`], traps: [`Subtracting ${k * x} L.`, 'Later removals take out diluted mix.'], viz: { type: 'mixture', M: m, W: V - m, add: 0, labels: [liq[0].toUpperCase() + liq.slice(1), 'Water'] } };
  });
  R('mixtures', 'medium', 'mx-m2', 'Mix two mixtures', H => H.retry(() => {
    const a = H.ri(1, 5), b = H.ri(1, 5), c = H.ri(1, 5), d = H.ri(1, 5), k1 = H.ri(1, 4), k2 = H.ri(1, 4); if (gcd(a, b) !== 1 || gcd(c, d) !== 1 || (a === c && b === d)) return null;
    const V1 = (a + b) * k1 * 4, V2 = (c + d) * k2 * 4, milk = V1 * a / (a + b) + V2 * c / (c + d), pct = milk / (V1 + V2) * 100; if (!isInt(pct * 100)) return null;
    return { question: `Vessel 1 (${V1} L) has milk:water = ${a}:${b}; vessel 2 (${V2} L) has ${c}:${d}. They are mixed. % milk in the result (2 decimals)?`, answer: r2(pct), unit: '%', params: { V1, V2, a, b, c, d },
      steps: [`Milk = ${fmt(V1 * a / (a + b))} + ${fmt(V2 * c / (c + d))} = ${fmt(milk)} L.`, `Of ${V1 + V2} L → ${fmt(pct)}%.`], traps: ['Adding the ratios term by term.', 'Averaging percentages without weights.'], viz: { type: 'mixture', M: milk, W: V1 + V2 - milk, add: 0, labels: ['Milk', 'Water'] } };
  }));
  R('mixtures', 'medium', 'mx-m3', 'Water to change ratio', H => H.retry(() => {
    const m = H.ri(2, 7), w = H.ri(1, 5); if (gcd(m, w) !== 1 || m <= w) return null; const k = H.ri(2, 12), M = m * k, W = w * k, c = m, d = w + H.ri(1, 3); if (gcd(c, d) !== 1) return null;
    const W2 = M * d / c, add = W2 - W; if (!isInt(add)) return null;
    return { question: `A ${M + W} L mix has milk:water = ${m}:${w}. Water to add (L) to make it ${c}:${d}?`, answer: add, unit: 'L', params: { m, w, V: M + W, c, d },
      steps: [`Milk ${M}, water ${W}.`, `Need water ${M}×${d}/${c} = ${W2}.`, `Add ${add} L.`], traps: ['Keeping total fixed.', 'Milk is the invariant.'], viz: { type: 'mixture', M, W, add, labels: ['Milk', 'Water'] } };
  }));
  R('mixtures', 'hard', 'mx-h1', 'Alloy mix for total', H => H.retry(() => {
    const a = H.pick([10, 20, 30, 40]), b = H.pick([50, 60, 70, 80, 90]), m = H.ri(a + 1, b - 1), T = 10 * H.ri(3, 30), x = T * (b - m) / (b - a); if (!isInt(x)) return null;
    return { question: `Alloy X is ${a}% gold, alloy Y is ${b}% gold. How many kg of X go into ${T} kg of a ${m}% gold alloy?`, answer: x, unit: 'kg', params: { a, b, m, T },
      mcq: [T - x, T * (m - a) / (b - a) + 5, x + 10], steps: [`X:Y = (${b} − ${m}):(${m} − ${a}) = ${b - m}:${m - a}.`, `X = ${T} × ${b - m}/${b - a} = ${x}.`], traps: ['Swapping X and Y shares.', 'Using % differences from 0 instead of from the mean.'], viz: { type: 'alligation', a, b, m, la: 'X ' + a + '%', lb: 'Y ' + b + '%' } };
  }));
  R('mixtures', 'hard', 'mx-h2', 'Replacement → volume', H => {
    const [k, m] = H.pick([[2, 3], [3, 4], [4, 5], [1, 2], [3, 5], [2, 5]]), x = (m - k) * H.ri(1, 6), V = x * m / (m - k), p = k * k, q = m * m - k * k;
    return { question: `Some milk is in a can. ${x} L is replaced by water, and then ${x} L of the mix is again replaced by water. Milk:water is now ${p}:${q}. Initial milk (L)?`, answer: V, unit: 'L', params: { x, p, q },
      steps: [`(1 − ${x}/V)² = ${p}/${p + q} → 1 − ${x}/V = ${k}/${m}.`, `${x}/V = ${m - k}/${m} → V = ${V}.`], traps: ['Forgetting the square root (two replacements).', 'Treating the ratio as milk:total.'], viz: { type: 'mixture', M: V * p / (p + q), W: V * q / (p + q), add: 0, labels: ['Milk', 'Water'] } };
  });
  R('mixtures', 'hard', 'mx-h3', 'Water + markup = profit', H => H.retry(() => {
    const p = H.pick([0, 10, 20, 25]), q = H.pick([32, 50, 40, 44, 65, 37.5]), M = 10 * H.ri(2, 10), W = M * ((100 + q) / (100 + p) - 1); if (W <= 0 || !isInt(W * 4)) return null;
    return { question: `A milkman sells milk at ${p ? p + '% above cost' : 'cost price'} and adds water to ${M} L of milk so his total profit is ${q}%. Water added (L)?`, answer: W, unit: 'L', params: { p, q, M },
      mcq: [M * (q - p) / 100 === W ? W + 2 : M * (q - p) / 100, M * q / 100 === W ? W * 3 : M * q / 100, W * 2], steps: [`Revenue factor = (1 + water/milk) × ${(100 + p) / 100} = ${(100 + q) / 100}.`, `water/milk = ${fmt((100 + q) / (100 + p) - 1)} → ${fmt(W)} L.`], traps: ['Subtracting percentages.', 'Water is free; profit comes from volume × price.'], viz: { type: 'mixture', M, W: 0, add: W, labels: ['Milk', 'Water'] } };
  }));

  /* ---------------- PARTNERSHIP ---------------- */
  R('partnership', 'easy', 'pt-e1', 'Same time shares', H => H.retry(() => {
    const a = H.ri(2, 9), b = H.ri(2, 9); if (a === b) return null; const g = gcd(a, b), k = 100 * H.ri(2, 50), P = (a + b) / g * k;
    return { question: `A invests ₹${a * 1000}, B ₹${b * 1000} for a year. Profit ₹${P}. A's share?`, answer: a / g * k, unit: '₹', params: { a, b, P },
      steps: [`Ratio ${a / g}:${b / g}.`, `A = ${P} × ${a / g}/${(a + b) / g} = ${a / g * k}.`], traps: ['Splitting equally.', 'Profit ∝ capital × time.'], viz: { type: 'ratio', parts: [a / g, b / g], unitVal: k, labels: ['A', 'B'] } };
  }));
  R('partnership', 'easy', 'pt-e2', 'Different times', H => {
    const a = H.ri(2, 9), b = H.ri(2, 9), m = H.ri(3, 11), wa = a * 12, wb = b * m, g = gcd(wa, wb), k = 10 * H.ri(1, 30), P = (wa + wb) / g * k;
    return { question: `A invests ₹${a}000 for 12 months; B invests ₹${b}000 for ${m} months. Profit ₹${P}. B's share?`, answer: wb / g * k, unit: '₹', params: { a, b, m, P },
      steps: [`Capital × time: ${wa} : ${wb}.`, `B = ${P} × ${wb}/${wa + wb} = ${wb / g * k}.`], traps: ['Ignoring time.', 'Using months B was absent.'], viz: { type: 'ratio', parts: [wa / g, wb / g], unitVal: k, labels: ['A', 'B'] } };
  });
  R('partnership', 'easy', 'pt-e3', 'Three partners', H => H.retry(() => {
    const a = H.ri(1, 6), b = H.ri(1, 6), c = H.ri(1, 6), k = 50 * H.ri(1, 40), P = (a + b + c) * k; if (gcd(gcd(a, b), c) !== 1 || (a === b && b === c)) return null;
    return { question: `A, B, C invest in ratio ${a}:${b}:${c}. Profit ₹${P}. C's share?`, answer: c * k, unit: '₹', params: { a, b, c, P },
      steps: [`Parts ${a + b + c}; 1 part = ${k}.`, `C = ${c * k}.`], traps: ['Dividing by 3.', 'Check: shares add to total.'], viz: { type: 'ratio', parts: [a, b, c], unitVal: k, labels: ['A', 'B', 'C'] } };
  }));
  R('partnership', 'medium', 'pt-m1', 'Late joiner', H => {
    const a = H.ri(2, 9), b = H.ri(2, 9), k = H.ri(2, 9), wa = a * 12, wb = b * (12 - k), g = gcd(wa, wb), u = 10 * H.ri(1, 40), P = (wa + wb) / g * u;
    return { question: `A starts with ₹${a}0,000. B joins after ${k} months with ₹${b}0,000. Year-end profit ₹${P}. A's share?`, answer: wa / g * u, unit: '₹', params: { a, b, k, P },
      steps: [`A: ${a}×12 = ${wa}; B: ${b}×${12 - k} = ${wb}.`, `A = ${P}×${wa}/${wa + wb} = ${wa / g * u}.`], traps: [`Using ${k} months for B instead of ${12 - k}.`, 'Ignoring time.'], viz: { type: 'ratio', parts: [wa / g, wb / g], unitVal: u, labels: ['A', 'B'] } };
  });
  R('partnership', 'medium', 'pt-m2', 'Partial withdrawal', H => {
    const a = 2 * H.ri(1, 6), b = H.ri(2, 9), k = H.ri(2, 10), wa = a * k + a / 2 * (12 - k), wb = b * 12, g = gcd(wa, wb), u = 10 * H.ri(1, 40), P = (wa + wb) / g * u;
    return { question: `A invests ₹${a}000 and withdraws half after ${k} months; B invests ₹${b}000 all year. Profit ₹${P}. A's share?`, answer: wa / g * u, unit: '₹', params: { a, b, k, P },
      steps: [`A: ${a}×${k} + ${a / 2}×${12 - k} = ${wa}.`, `B: ${wb}. A = ${P}×${wa}/${wa + wb} = ${wa / g * u}.`], traps: ['Using the full capital all year.', 'Withdrawn half only counts for the remaining months.'], viz: { type: 'ratio', parts: [wa / g, wb / g], unitVal: u, labels: ['A', 'B'] } };
  });
  R('partnership', 'medium', 'pt-m3', 'Working partner salary', H => H.retry(() => {
    const s = H.pick([10, 20, 25]), a = H.ri(1, 5), b = H.ri(1, 5), P = 100 * (a + b) * H.ri(2, 30), rest = P * (100 - s) / 100, A = P * s / 100 + rest * a / (a + b); if (!isInt(A) || a === b || gcd(a, b) !== 1) return null;
    return { question: `A (working partner) first gets ${s}% of the profit; the rest is shared in capital ratio A:B = ${a}:${b}. Profit ₹${P}. A's total?`, answer: A, unit: '₹', params: { s, a, b, P },
      steps: [`Salary ${fmt(P * s / 100)}; remaining ${fmt(rest)}.`, `A gets ${fmt(rest * a / (a + b))} more → ${fmt(A)}.`], traps: ['Splitting the whole profit by ratio.', 'Forgetting to add the salary.'], viz: bars([{ label: 'Salary', value: P * s / 100, color: 'acc2' }, { label: 'A share', value: rest * a / (a + b), color: 'accent' }, { label: 'B', value: rest * b / (a + b), color: 'muted' }], '₹') };
  }));
  R('partnership', 'hard', 'pt-h1', 'Find B\'s time', H => H.retry(() => {
    const a = H.ri(1, 6), b = H.ri(1, 6), tB = H.ri(2, 11), p = a * 12, q = b * tB, g = gcd(p, q); if (gcd(a, b) !== 1 || p === q) return null;
    return { question: `A and B invest in ratio ${a}:${b}. A stays 12 months; profits are shared ${p / g}:${q / g}. For how many months was B's money in?`, answer: tB, unit: 'months', params: { a, b, p: p / g, q: q / g },
      steps: [`a·tA : b·tB = ${p / g}:${q / g}.`, `tB = ${q / g}·${a}·12/(${p / g}·${b}) = ${tB}.`], traps: ['Inverting the ratio.', 'Forgetting capital weights.'], viz: { type: 'ratio', parts: [p / g, q / g], unitVal: 1, labels: ['A', 'B'] } };
  }));
  R('partnership', 'hard', 'pt-h2', 'Top-up + late partner', H => {
    const x = H.ri(2, 6), y = H.ri(1, 4), z = H.ri(2, 8), c = H.ri(2, 8), wa = x * 4 + (x + y) * 8, wb = z * 12, wc = c * 6, g = gcd(gcd(wa, wb), wc), u = 50 * H.ri(1, 20), P = (wa + wb + wc) / g * u;
    return { question: `A invests ₹${x} lakh and adds ₹${y} lakh after 4 months; B invests ₹${z} lakh for the year; C joins after 6 months with ₹${c} lakh. Profit ₹${P}. C's share?`, answer: wc / g * u, unit: '₹', params: { x, y, z, c, P },
      mcq: [r2(P / 3), r2(P * c / (x + y + z + c)), wa / g * u], steps: [`A: ${x}×4 + ${x + y}×8 = ${wa}; B: ${wb}; C: ${c}×6 = ${wc}.`, `C = ${P}×${wc}/${wa + wb + wc} = ${wc / g * u}.`], traps: ['Ignoring A\'s top-up timing.', 'C\'s months = 6.'],
      viz: { type: 'ratio', parts: [wa / g, wb / g, wc / g], unitVal: u, labels: ['A', 'B', 'C'] } };
  });
  R('partnership', 'hard', 'pt-h3', 'Interest on capital', H => H.retry(() => {
    const a = 10000 * H.ri(1, 9), b = 10000 * H.ri(1, 9), i = H.pick([5, 10, 12]), P = 1000 * H.ri(20, 200); if (a === b) return null;
    const ia = a * i / 100, ib = b * i / 100, rest = P - ia - ib; if (rest <= 0) return null; const d = Math.abs(ia - ib);
    return { question: `A and B invest ₹${a} and ₹${b}. Each first gets ${i}% interest on capital; the remaining profit is split equally. Total profit ₹${P}. Difference between their total receipts (₹)?`, answer: d, unit: '₹', params: { a, b, i, P },
      mcq: [r2(Math.abs(a - b) * P / (a + b)), d * 2, rest / 2], steps: [`Interest: A ${ia}, B ${ib}.`, `Equal split of ${rest} cancels in the difference.`, `Difference = ${d}.`], traps: ['Splitting the whole profit by capital ratio.', 'Equal parts cancel in a difference.'],
      viz: bars([{ label: 'A', value: ia + rest / 2, color: 'accent' }, { label: 'B', value: ib + rest / 2, color: 'muted' }], '₹') };
  }));

  /* ---------------- AVERAGES ---------------- */
  R('averages', 'easy', 'av-e1', 'Mean of list', H => H.retry(() => {
    const n = H.ri(4, 7), avg = H.ri(10, 60), xs = []; let s = 0; for (let i = 0; i < n - 1; i++) { const v = avg + H.ri(-9, 9); xs.push(v); s += v; } xs.push(avg * n - s); if (xs[n - 1] < 1 || Math.abs(xs[n - 1] - avg) > 12) return null;
    return { question: `Average of: ${xs.join(', ')}?`, answer: avg, params: { xs }, steps: [`Sum = ${avg * n}; n = ${n}.`, `Mean = ${avg}.`], traps: ['Miscounting terms.', 'Assumed-mean shortcut: sum deviations.'], viz: { type: 'avgbars', values: xs, avg } };
  }));
  R('averages', 'easy', 'av-e2', 'Consecutive numbers', H => {
    const n = 2 * H.ri(2, 10) + 1, a = H.ri(1, 80), avg = a + (n - 1) / 2;
    return { question: `Average of ${n} consecutive integers starting at ${a}?`, answer: avg, params: { n, a }, steps: [`Middle term = ${a} + ${(n - 1) / 2} = ${avg}.`], traps: ['Using (first + n)/2.', 'Mean of an AP = middle term.'], viz: { type: 'avgbars', values: Array.from({ length: Math.min(n, 11) }, (_, i) => a + i), avg: a + (Math.min(n, 11) - 1) / 2 } };
  });
  R('averages', 'easy', 'av-e3', 'Removed number', H => H.retry(() => {
    const n = H.ri(5, 15), A = H.ri(20, 60), B = A + H.ri(-5, 5), x = n * A - (n - 1) * B; if (B === A || x <= 0 || x > 3 * A) return null;
    return { question: `The average of ${n} numbers is ${A}. Removing one number makes the average ${B}. The removed number?`, answer: x, params: { n, A, B }, steps: [`Total ${n * A}; new total ${(n - 1) * B}.`, `Removed = ${x}.`], traps: ['Using n for the new count.', 'Difference of averages ≠ removed number.'], viz: { type: 'avgbars', values: [A, A, A, x], avg: A } };
  }));
  R('averages', 'medium', 'av-m1', 'Replacement', H => H.retry(() => {
    const n = H.ri(5, 20), w = H.ri(40, 70), d = H.pick([0.5, 1, 1.5, 2, 2.5, 3]), a = w + n * d; if (!isInt(a)) return null;
    return { question: `Average weight of ${n} people rises by ${d} kg when a ${w} kg person is replaced. New person's weight (kg)?`, answer: a, unit: 'kg', params: { n, w, d },
      steps: [`Increase = ${n}×${d} = ${fmt(n * d)}.`, `New = ${w} + ${fmt(n * d)} = ${a}.`], traps: [`Adding only ${d}.`, `Using ${n + 1}.`], viz: { type: 'avgbars', values: [w, w + 3, w - 2, w + 1, a], avg: w } };
  }));
  R('averages', 'medium', 'av-m2', 'New member joins', H => {
    const n = H.ri(5, 25), A = H.ri(20, 50), d = H.ri(1, 4), x = A + (n + 1) * d;
    return { question: `The average age of ${n} players is ${A}. When the coach joins, the average rises by ${d}. Coach's age?`, answer: x, params: { n, A, d }, steps: [`New total = ${n + 1}×${A + d} = ${(n + 1) * (A + d)}.`, `Coach = ${(n + 1) * (A + d)} − ${n * A} = ${x}.`], traps: [`Using ${n}×${d}.`, 'The coach also lifts his own average.'], viz: { type: 'avgbars', values: [A - 2, A + 1, A, A + 2, x], avg: A + d } };
  });
  R('averages', 'medium', 'av-m3', 'Batting average', H => {
    const n = H.ri(8, 30), a = H.ri(20, 50), d = H.ri(1, 4), s = a + (n + 1) * d;
    return { question: `After ${n + 1} innings a batsman's average rose by ${d} when he scored ${s} in the last one. New average?`, answer: a + d, params: { n, d, s }, steps: [`s = old + (${n + 1})·${d} → old = ${a}.`, `New = ${a + d}.`], traps: ['Using n instead of n+1.', 'Answering the old average.'], viz: { type: 'avgbars', values: [a, a + 4, a - 3, s], avg: a + d } };
  });
  R('averages', 'hard', 'av-h1', 'Combined mean', H => H.retry(() => {
    const n1 = H.ri(10, 40), n2 = H.ri(10, 40), a1 = H.ri(40, 80), a2 = H.ri(40, 80), c = (n1 * a1 + n2 * a2) / (n1 + n2); if (!isInt(c) || a1 === a2) return null;
    return { question: `Section A: ${n1} students, average ${a1}; section B: ${n2}, average ${a2}. Combined average?`, answer: c, params: { n1, n2, a1, a2 },
      steps: [`Totals ${n1 * a1} + ${n2 * a2} = ${n1 * a1 + n2 * a2}.`, `÷ ${n1 + n2} = ${c}.`], traps: [`Averaging the averages ${fmt((a1 + a2) / 2)}.`, 'Mean sits closer to the bigger group.'], viz: { type: 'seesaw', n1, n2, a1, a2, c } };
  }));
  R('averages', 'hard', 'av-h2', 'Overlapping halves', H => H.retry(() => {
    const A = H.ri(30, 60), B = A + H.ri(-6, 6), C = A + H.ri(-6, 6), x = 6 * B + 6 * C - 11 * A; if (x < A / 2 || x > 2 * A || B === C) return null;
    return { question: `The average of 11 results is ${A}. The first 6 average ${B} and the last 6 average ${C}. Find the 6th result.`, answer: x, params: { A, B, C },
      mcq: [6 * B - 5 * A, 6 * B + 6 * C - 12 * A, x + 6], steps: [`6th result is counted twice.`, `6·${B} + 6·${C} − 11·${A} = ${x}.`], traps: ['Forgetting the overlap.', 'Sign slip in subtraction.'], viz: { type: 'avgbars', values: [B, B, B, x, C, C], avg: A } };
  }));
  R('averages', 'hard', 'av-h3', 'Family ages', H => H.retry(() => {
    const x = H.ri(22, 30), t = H.ri(3, 10), c = H.ri(1, t - 1), y = (2 * (x + t) + c) / 3; if (!isInt(y)) return null;
    return { question: `When married, a couple's average age was ${x}. ${t} years later, with their child, the family's average age is ${y}. Child's age?`, answer: c, params: { x, t, y },
      mcq: [3 * y - 2 * x, t, c + 2], steps: [`Couple now: 2×(${x} + ${t}) = ${2 * (x + t)}.`, `Family total ${3 * y} → child ${c}.`], traps: ['Not ageing the couple.', 'Using 2 people for the new average.'], viz: { type: 'avgbars', values: [x + t, x + t, c], avg: y } };
  }));

  /* ---------------- RATIO ---------------- */
  R('ratio', 'easy', 'ra-e1', 'Divide in ratio', H => H.retry(() => {
    const a = H.ri(1, 9), b = H.ri(1, 9); if (a === b || gcd(a, b) !== 1) return null; const k = 5 * H.ri(5, 60), S = (a + b) * k;
    return { question: `Divide ₹${S} in ratio ${a}:${b}. Larger share?`, answer: Math.max(a, b) * k, unit: '₹', params: { a, b, S }, steps: [`1 part = ${S}/${a + b} = ${k}.`, `Larger = ${Math.max(a, b) * k}.`], traps: ['Dividing by the larger term.', 'Check shares sum to total.'], viz: { type: 'ratio', parts: [a, b], unitVal: k, labels: ['1st', '2nd'] } };
  }));
  R('ratio', 'easy', 'ra-e2', 'Fourth proportional', H => {
    const a = H.ri(2, 12), k = H.ri(2, 9), b = a * k, c = H.ri(2, 20), x = c * k;
    return { question: `Find x if ${a} : ${b} = ${c} : x.`, answer: x, params: { a, b, c }, steps: [`x = ${b}×${c}/${a} = ${x}.`], traps: ['Cross-multiplying the wrong pair.', 'Product of means = product of extremes.'], viz: { type: 'ratio', parts: [a, b], unitVal: 1, labels: ['a', 'b'] } };
  });
  R('ratio', 'easy', 'ra-e3', 'Mean proportional', H => {
    const p = H.ri(2, 9), q = H.ri(2, 9), r = H.ri(1, 4), a = p * p * r, b = q * q * r, m = p * q * r;
    return { question: `Mean proportional between ${a} and ${b}?`, answer: m, params: { a, b }, steps: [`√(${a}×${b}) = √${a * b} = ${m}.`], traps: ['Taking the arithmetic mean.', 'Mean proportional = geometric mean.'], viz: { type: 'ratio', parts: [p, q], unitVal: r, labels: ['a', 'b'] } };
  });
  R('ratio', 'medium', 'ra-m1', 'Chain ratios', H => H.retry(() => {
    const a = H.ri(1, 7), b = H.ri(2, 7), c = H.ri(2, 7), d = H.ri(1, 7); if (gcd(a, b) !== 1 || gcd(c, d) !== 1) return null;
    let A = a * c, B = b * c, C = b * d; const g = gcd(gcd(A, B), C); A /= g; B /= g; C /= g; if (A + B + C > 40) return null; const k = H.ri(2, 20), T = (A + B + C) * k;
    return { question: `A:B = ${a}:${b}, B:C = ${c}:${d}, A+B+C = ${T}. Find C.`, answer: C * k, params: { a, b, c, d, T }, steps: [`Equalise B: A:B:C = ${A}:${B}:${C}.`, `C = ${C}×${k} = ${C * k}.`], traps: ['Not equalising B.', 'Writing a:b:d directly.'], viz: { type: 'ratio', parts: [A, B, C], unitVal: k, labels: ['A', 'B', 'C'] } };
  }));
  R('ratio', 'medium', 'ra-m2', 'Add to both', H => H.retry(() => {
    const a = H.ri(1, 6), b = H.ri(a + 1, 9), x = H.ri(2, 12), k = H.ri(1, 15), c = a * x + k, d = b * x + k, g = gcd(c, d); if (gcd(a, b) !== 1) return null;
    return { question: `Two numbers are in ratio ${a}:${b}. Adding ${k} to each makes it ${c / g}:${d / g}. Larger number?`, answer: b * x, params: { a, b, k, c: c / g, d: d / g },
      steps: [`(${a}x + ${k})/(${b}x + ${k}) = ${c / g}/${d / g}.`, `x = ${x} → larger ${b * x}.`], traps: ['Adding k to the ratio terms.', 'Answering x instead of bx.'], viz: { type: 'ratio', parts: [a, b], unitVal: x, labels: ['small', 'large'] } };
  }));
  R('ratio', 'medium', 'ra-m3', 'Coins', H => H.retry(() => {
    const a = H.ri(1, 6), b = H.ri(1, 6), c = H.ri(1, 6), x = 4 * H.ri(2, 30), T = a * x + b * x / 2 + c * x / 4; if (gcd(gcd(a, b), c) !== 1 || (a === b && b === c)) return null;
    return { question: `A bag has ₹1, 50p and 25p coins in ratio ${a}:${b}:${c}, total ₹${fmt(T)}. How many 50p coins?`, answer: b * x, params: { a, b, c, T }, steps: [`Value per set: ${a} + ${b / 2} + ${c / 4} = ${fmt(a + b / 2 + c / 4)}.`, `Sets = ${x} → 50p = ${b * x}.`], traps: ['Treating the count ratio as a value ratio.', 'Answering value instead of count.'], viz: { type: 'ratio', parts: [a, b, c], unitVal: x, labels: ['₹1', '50p', '25p'] } };
  }));
  R('ratio', 'hard', 'ra-h1', 'Income & savings', H => H.retry(() => {
    const a = H.ri(2, 9), b = H.ri(2, 9), c = H.ri(1, 9), d = H.ri(1, 9); if (a === b || c === d || gcd(a, b) !== 1 || gcd(c, d) !== 1) return null;
    const x = 1000 * H.ri(1, 10), y = x * (a - b) / (c - d); if (!isInt(y) || y <= 0) return null; const S = a * x - c * y; if (S <= 0 || b * x - d * y !== S) return null;
    return { question: `Incomes of A and B are in ratio ${a}:${b} and expenditures ${c}:${d}. Each saves ₹${S}. A's income (₹)?`, answer: a * x, unit: '₹', params: { a, b, c, d, S },
      mcq: [b * x, a * x + S, c * y], steps: [`${a}x − ${c}y = ${b}x − ${d}y = ${S}.`, `Solve: x = ${x}, y = ${y}.`, `A = ${a * x}.`], traps: ['Assuming savings ratio = income ratio.', 'Answering B\'s income.'], viz: bars([{ label: 'A inc', value: a * x, color: 'accent' }, { label: 'B inc', value: b * x, color: 'acc2' }, { label: 'saving', value: S, color: 'warn' }], '₹') };
  }));
  R('ratio', 'hard', 'ra-h2', 'Joint variation', H => H.retry(() => {
    const k = H.ri(1, 6), y1 = H.ri(2, 12), z1 = H.ri(1, 4), y2 = H.ri(2, 12), z2 = H.ri(1, 4), x1 = k * y1 / (z1 * z1), x2 = k * y2 / (z2 * z2); if (!isInt(x1) || !isInt(x2 * 4) || z1 === z2) return null;
    return { question: `x varies directly as y and inversely as z². x = ${x1} when y = ${y1}, z = ${z1}. Find x when y = ${y2}, z = ${z2}.`, answer: x2, params: { x1, y1, z1, y2, z2 },
      steps: [`k = x z²/y = ${x1}·${z1 * z1}/${y1} = ${k}.`, `x = ${k}·${y2}/${z2 * z2} = ${fmt(x2)}.`], traps: ['Using z instead of z².', 'Using direct variation for z.'], viz: bars([{ label: 'x₁', value: x1, color: 'muted' }, { label: 'x₂', value: x2, color: 'accent' }]) };
  }));
  R('ratio', 'hard', 'ra-h3', 'Age ratios', H => H.retry(() => {
    const a = H.ri(1, 7), b = H.ri(a + 1, 9), x = H.ri(2, 8), t = H.ri(2, 15), c = a * x + t, d = b * x + t, g = gcd(c, d); if (gcd(a, b) !== 1) return null;
    return { question: `Present ages are in ratio ${a}:${b}. After ${t} years they will be ${c / g}:${d / g}. Sum of present ages?`, answer: (a + b) * x, params: { a, b, t, c: c / g, d: d / g },
      mcq: [(a + b) * x + 2 * t, (a + b) * (x + 1), (a + b) * x - 2], steps: [`(${a}x + ${t})/(${b}x + ${t}) = ${c / g}/${d / g} → x = ${x}.`, `Sum = ${(a + b) * x}.`], traps: ['Giving future ages.', 'Adding t to only one person.'], viz: { type: 'ratio', parts: [a, b], unitVal: x, labels: ['P', 'Q'] } };
  }));
})(typeof module === 'object' && module.exports ? require('./core.js') : self.QGen);
