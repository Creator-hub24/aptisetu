/* Topic: Puzzles & scheduling — floors, boxes, days, months, flats; solved on a shrinking grid */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample } = RL.u;
  RL.topic('puzzles', 'Puzzles & Scheduling', '🧩', 'Floor, box, day and month puzzles solved on a live grid: each clue removes options until one answer remains.', 'Arrangements & Puzzles');
  const PEOPLE = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
  const COL = ['Red', 'Blue', 'Green', 'Yellow', 'White', 'Pink', 'Black'], FRUIT = ['Apple', 'Mango', 'Kiwi', 'Grapes', 'Banana', 'Guava', 'Litchi'], SUBJ = ['Physics', 'History', 'Maths', 'English', 'Biology', 'Economics'];
  const ordn = RL.ord || (n => n + 'th');
  // DOMAINS: slot text + relational text
  const DOM = {
    floor: { lvl: i => `floor ${i + 1}`, unit: 'floor', s: (X, Y, w) => ({ at: `${X} lives on floor ${Y + 1}.`, nat: `${X} does not live on floor ${Y + 1}.`, odd: `${X} lives on an odd-numbered floor.`, even: `${X} lives on an even-numbered floor.`, top: `${X} lives on the top floor.`, bot: `${X} lives on the bottom floor.`,
      adj: `${X} lives immediately above ${Y}.`, above: `${X} lives somewhere above ${Y}.`, btw: `Exactly ${w} floor${w === 1 ? ' is' : 's are'} between the floors of ${X} and ${Y}.`, vbelow: `The floor immediately below ${X}'s floor is vacant.`, same: `${X} and ${Y} live on the same floor.`, colx: `${X} lives in the ${Y} flat.` }) },
    box: { lvl: i => `position ${i + 1} from the bottom`, unit: 'box', s: (X, Y, w) => ({ at: `Box ${X} is ${ordn(Y + 1)} from the bottom.`, nat: `Box ${X} is not ${ordn(Y + 1)} from the bottom.`, odd: `Box ${X} is at an odd-numbered position from the bottom.`, even: `Box ${X} is at an even-numbered position from the bottom.`, top: `Box ${X} is at the top of the stack.`, bot: `Box ${X} is at the bottom of the stack.`,
      adj: `Box ${X} is placed immediately above box ${Y}.`, above: `Box ${X} is somewhere above box ${Y}.`, btw: `Exactly ${w} box${w === 1 ? ' is' : 'es are'} placed between box ${X} and box ${Y}.` }) },
    day: { lvl: i => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][i], unit: 'day', s: (X, Y, w) => ({ at: `${X}'s lecture is on ${['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][Y]}.`, nat: `${X}'s lecture is not on ${['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][Y]}.`, odd: `${X}'s lecture is on an odd-numbered day of the week (Monday = 1).`, even: `${X}'s lecture is on an even-numbered day of the week (Monday = 1).`, top: `${X}'s lecture is the last day of the schedule.`, bot: `${X}'s lecture is on the first day of the schedule.`,
      adj: `${X}'s lecture is the day immediately after ${Y}'s.`, above: `${X}'s lecture is on some day after ${Y}'s.`, btw: `Exactly ${w} day${w === 1 ? '' : 's'} fall${w === 1 ? 's' : ''} between the lectures of ${X} and ${Y}.`, vbelow: `No lecture is held on the day just before ${X}'s.` }) },
    month: { lvl: i => `${['March', 'June', 'September'][i >> 1]} ${i % 2 ? 21 : 8}`, unit: 'date', s: (X, Y, w) => ({ at: `${X}'s exam is on ${['March', 'June', 'September'][Y >> 1]} ${Y % 2 ? 21 : 8}.`, nat: `${X}'s exam is not on ${['March', 'June', 'September'][Y >> 1]} ${Y % 2 ? 21 : 8}.`, odd: `${X}'s exam is on the 8th of a month.`, even: `${X}'s exam is on the 21st of a month.`, top: `${X} has the last exam.`, bot: `${X} has the first exam.`,
      adj: `${X}'s exam is immediately after ${Y}'s.`, above: `${X}'s exam is some time after ${Y}'s.`, btw: `Exactly ${w} exam${w === 1 ? ' is' : 's are'} held between the exams of ${X} and ${Y}.`, same: `${X} and ${Y} have exams in the same month.`, colx: `${X}'s exam is in ${Y}.` }) }
  };
  function allPlace(n, S) { const out = [], cur = [], used = Array(S).fill(false); (function bt(i) { if (i === n) { out.push(cur.slice()); return; } for (let s = 0; s < S; s++) if (!used[s]) { used[s] = true; cur[i] = s; bt(i + 1); used[s] = false; } })(0); return out; }
  function engine(cfg) {
    const { n, S, dom, attr, flats } = cfg; const D = DOM[dom]; const P = PEOPLE.slice(0, n);
    const lv = s => flats ? s >> 1 : s, colOf = s => flats ? s & 1 : 0, L = flats ? S / 2 : S;
    const truth = shuffle([...Array(S).keys()]).slice(0, n); const tA = attr ? shuffle([...Array(n).keys()]) : null;
    const AV = attr ? attr.vals.slice(0, n) : null;
    const pos = (p, x) => p[x], occ = (p, s) => p.indexOf(s) >= 0;
    // candidate generators (each returns {k, x, y, w, f(p,a), t})
    const mk = []; const T = (k, X, Y, w) => D.s(X, Y, w)[k];
    for (let x = 0; x < n; x++) { const s = truth[x];
      mk.push({ k: 'at', x, y: s, f: p => p[x] === s, t: flats ? null : T('at', P[x], s) });
      for (let z = 0; z < L; z++) if (z !== lv(s) && !flats) mk.push({ k: 'nat', x, y: z, f: p => lv(p[x]) !== z, t: T('nat', P[x], z) });
      if (!flats && dom !== 'month') mk.push({ k: lv(s) % 2 ? 'even' : 'odd', x, f: p => lv(p[x]) % 2 === lv(s) % 2, t: T(lv(s) % 2 ? 'even' : 'odd', P[x]) });
      if (dom === 'month') mk.push({ k: s % 2 ? 'even' : 'odd', x, f: p => p[x] % 2 === s % 2, t: T(s % 2 ? 'even' : 'odd', P[x]) }, { k: 'colx', x, y: s >> 1, f: p => p[x] >> 1 === s >> 1, t: T('colx', P[x], ['March', 'June', 'September'][s >> 1]) });
      if (lv(s) === L - 1) mk.push({ k: 'top', x, f: p => lv(p[x]) === L - 1, t: T('top', P[x]) }); if (lv(s) === 0) mk.push({ k: 'bot', x, f: p => lv(p[x]) === 0, t: T('bot', P[x]) });
      if (flats) mk.push({ k: 'colx', x, y: colOf(s), f: p => colOf(p[x]) === colOf(s), t: T('colx', P[x], colOf(s) ? 'East' : 'West') });
      if (cfg.vac && lv(s) > 0 && !occ(truth, s - 1) && D.s('', '', 0).vbelow) mk.push({ k: 'vbelow', x, f: p => p[x] > 0 && !occ(p, p[x] - 1), t: T('vbelow', P[x]) });
      for (let y = 0; y < n; y++) if (y !== x) { const d = lv(s) - lv(truth[y]);
        if (dom === 'month' ? s - truth[y] === 1 : d === 1 && colOf(s) === colOf(truth[y])) mk.push({ k: 'adj', x, y, f: p => dom === 'month' ? p[x] - p[y] === 1 : lv(p[x]) - lv(p[y]) === 1 && colOf(p[x]) === colOf(p[y]), t: flats ? `${P[x]} lives in the flat directly above ${P[y]}'s flat.` : T('adj', P[x], P[y]) });
        const od = dom === 'month' ? s - truth[y] : d;
        if (od > 0) mk.push({ k: 'above', x, y, f: p => (dom === 'month' ? p[x] - p[y] : lv(p[x]) - lv(p[y])) > 0, t: flats ? `${P[x]} lives on a floor somewhere above ${P[y]}'s floor.` : T('above', P[x], P[y]) });
        if (od > 1 && x < y + 99) { const w = od - 1; mk.push({ k: 'btw', x, y, w, f: p => Math.abs(dom === 'month' ? p[x] - p[y] : lv(p[x]) - lv(p[y])) - 1 === w, t: T('btw', P[x], P[y], w) }); }
        if ((flats || dom === 'month') && x < y && (flats ? lv(s) === lv(truth[y]) : s >> 1 === truth[y] >> 1)) mk.push({ k: 'same', x, y, f: p => flats ? lv(p[x]) === lv(p[y]) : p[x] >> 1 === p[y] >> 1, t: T('same', P[x], P[y]) }); } }
    if (attr) for (let x = 0; x < n; x++) { const v = tA[x];
      mk.push({ k: 'ais', x, y: v, A: true, f: (p, a) => a[x] === v, t: attr.is(P[x], AV[v]) });
      for (let u = 0; u < n; u++) if (u !== v) mk.push({ k: 'anot', x, y: u, A: true, f: (p, a) => a[x] !== u, t: attr.not(P[x], AV[u]) });
      for (let y = 0; y < n; y++) if (y !== x) { const d = (dom === 'month' ? truth[x] - truth[y] : lv(truth[x]) - lv(truth[y]));
        if (d === 1) mk.push({ k: 'aadj', x, y, v, A: true, f: (p, a) => { const z = a.indexOf(v); return (dom === 'month' ? p[z] - p[y] : lv(p[z]) - lv(p[y])) === 1; }, t: attr.adj(AV[v], P[y], D) });
        if (d > 1) mk.push({ k: 'abtw', x, y, v, w: d - 1, A: true, f: (p, a) => { const z = a.indexOf(v); return Math.abs(dom === 'month' ? p[z] - p[y] : lv(p[z]) - lv(p[y])) - 1 === d - 1; }, t: attr.btw(AV[v], P[y], d - 1, D) }); }
      mk.push({ k: 'aat', x, v, s: truth[x], A: true, f: (p, a) => p[a.indexOf(v)] === truth[x], t: attr.at(AV[v], D.lvl(truth[x])) }); }
    const C = mk.filter(c => c.t); const aperm = attr ? allPlace(n, n) : [null];
    let sols = allPlace(n, S).map(p => ({ p, a: null })); const chosen = [], trail = [];
    const key = s => s.p.join() + '|' + (s.a ? s.a.join() : ''); const done = () => sols.length === 1;
    const expand = () => { if (!attr || sols[0].a) return; const out = []; sols.forEach(s => aperm.forEach(a => { if (chosen.every(c => c.f(s.p, a))) out.push({ p: s.p, a }); })); sols = out; };
    let guard = 0;
    while (!done() && guard++ < 40) { const exp = !attr || sols[0].a; let pool = C.filter(c => !chosen.includes(c) && (exp || !c.A)); if (!exp && sols.length <= cfg.T) { expand(); continue; }
      if (!pool.length) { if (!exp) { expand(); continue; } return null; }
      const cand = sample(pool, Math.min(pool.length, cfg.k || 4)); let best = null, bn = Infinity;
      cand.forEach(c => { const m = sols.filter(s => c.f(s.p, s.a)).length; const w = m + (c.k === 'at' || c.k === 'ais' ? sols.length * .15 : 0) + (c.k === 'nat' || c.k === 'anot' ? sols.length * .05 : 0); if (m < sols.length && w < bn) { bn = w; best = c; } });
      if (!best) continue; chosen.push(best); sols = sols.filter(s => best.f(s.p, s.a)); if (!sols.length) return null; if (exp || !attr) trail.push(null); else trail.push(null);
      if (attr && !sols[0].a && sols.length <= cfg.T) expand(); }
    if (!done()) return null; if (attr && !sols[0].a) { expand(); if (!done()) return null; }
    const ALLP = allPlace(n, S);
    const uniq = cl => { const pl = ALLP.filter(p => cl.every(c => c.A || c.f(p))); if (!attr) return pl.length === 1; if (pl.length > 200) return false; let k = 0; for (const p of pl) for (const a of aperm) if (cl.every(c => !c.A || c.f(p, a))) { if (++k > 1) return false; } return k === 1; };
    for (let i = chosen.length - 1; i >= 0; i--) { const t = chosen.filter((_, j) => j !== i); if (uniq(t)) chosen.splice(i, 1); }
    if (chosen.length > cfg.maxC || chosen.length < (cfg.minC || 0)) return null;
    return { P, AV, truth, tA, chosen, L, lv, D, dom, S, n, attr, flats };
  }
  RL.puzEngine = engine; RL.puzDom = DOM;
  const ATTR = {
    colour: { name: 'Colour', vals: COL, is: (X, v) => `${X} likes ${v}.`, not: (X, v) => `${X} does not like ${v}.`, adj: (v, Y, D) => D.unit === 'floor' ? `The person who likes ${v} lives immediately above ${Y}.` : D.unit === 'day' ? `The lecture of the person who likes ${v} is the day immediately after ${Y}'s.` : `The person who likes ${v} has the exam immediately after ${Y}'s.`,
      btw: (v, Y, w, D) => `Exactly ${w} ${D.unit}${w === 1 ? '' : 's'} ${w === 1 ? 'is' : 'are'} between ${Y} and the person who likes ${v}.`, at: (v, l) => `The person who likes ${v} is on ${l}.` },
    fruit: { name: 'Fruit', vals: FRUIT, is: (X, v) => `${X} eats ${v}.`, not: (X, v) => `${X} does not eat ${v}.`, adj: (v, Y, D) => D.unit === 'floor' ? `The one who eats ${v} lives immediately above ${Y}.` : D.unit === 'day' ? `The one who eats ${v} has a lecture the day after ${Y}.` : `The one who eats ${v} has the exam right after ${Y}'s.`,
      btw: (v, Y, w, D) => `Exactly ${w} ${D.unit}${w === 1 ? '' : 's'} ${w === 1 ? 'is' : 'are'} between ${Y} and the one who eats ${v}.`, at: (v, l) => `The one who eats ${v} is on ${l}.` },
    subject: { name: 'Subject', vals: SUBJ, is: (X, v) => `${X} takes ${v}.`, not: (X, v) => `${X} does not take ${v}.`, adj: (v, Y, D) => D.unit === 'day' ? `The ${v} lecture is the day immediately after ${Y}'s.` : `The ${v} exam is immediately after ${Y}'s.`,
      btw: (v, Y, w, D) => `Exactly ${w} ${D.unit}${w === 1 ? '' : 's'} ${w === 1 ? 'is' : 'are'} between ${Y}'s and the ${v} ${D.unit === 'day' ? 'lecture' : 'exam'}.`, at: (v, l) => `The ${v} ${l.match(/day/) ? 'lecture' : 'exam'} is on ${l}.` } };
  RL.puzAttr = ATTR;
  function grid(E, known) { // rows = slots top→bottom
    const rows = []; for (let s = E.S - 1; s >= 0; s--) { const x = E.truth.indexOf(s); rows.push({ sIdx: s, slot: E.flats ? `Floor ${(s >> 1) + 1} ${s & 1 ? 'East' : 'West'}` : E.D.lvl(s).replace(/^./, c => c.toUpperCase()), who: x >= 0 ? (known ? E.P[x] : '?') : (known ? '—' : '?'), attr: E.attr ? (x >= 0 ? (known ? E.AV[E.tA[x]] : '?') : '') : null }); }
    if (E.dom !== 'floor' && E.dom !== 'box') rows.reverse(); return { kind: 'grid', rows, attr: E.attr ? E.attr.name : null, head: E.flats ? 'Flat' : E.dom === 'floor' ? 'Floor' : E.dom === 'box' ? 'Stack' : E.dom === 'day' ? 'Day' : 'Date' };
  }
  function mkType(id, level, name, exams, cfg) {
    RL.reg('puzzles', level, id, name, exams, () => {
      const attrKey = cfg.attr ? pick(cfg.attr) : null; const E = engine(Object.assign({}, cfg, { attr: attrKey ? ATTR[attrKey] : null })); if (!E) return null;
      const qk = pick(cfg.q); let question, ans, ds;
      const sl = s => E.flats ? `Floor ${(s >> 1) + 1}, ${s & 1 ? 'East' : 'West'} flat` : E.D.lvl(s).replace(/^./, c => c.toUpperCase());
      if (qk === 'who') { const s = pick(E.truth); question = E.dom === 'box' ? `Which box is ${ordn(s + 1)} from the bottom?` : E.flats ? `Who lives in the ${sl(s)}?` : `Who is on ${E.D.lvl(s)}?`; ans = (E.dom === 'box' ? 'Box ' : '') + E.P[E.truth.indexOf(s)]; ds = E.P.filter(p => (E.dom === 'box' ? 'Box ' : '') + p !== ans).map(p => (E.dom === 'box' ? 'Box ' : '') + p); }
      else if (qk === 'where') { const x = ri(0, E.n - 1); question = E.dom === 'box' ? `What is box ${E.P[x]}'s position from the bottom?` : `Where is ${E.P[x]}?`; ans = sl(E.truth[x]); ds = [...Array(E.S).keys()].filter(s => s !== E.truth[x]).map(sl); }
      else if (qk === 'attr') { const x = ri(0, E.n - 1); question = `What is ${E.P[x]}'s ${E.attr.name.toLowerCase()}?`; ans = E.AV[E.tA[x]]; ds = E.AV.filter(v => v !== ans); }
      else if (qk === 'vacant') { const v = [...Array(E.S).keys()].filter(s => !E.truth.includes(s)); question = `Which ${E.dom === 'day' ? 'days have no lecture' : 'floors are vacant'}?`; ans = v.map(sl).join(' and '); ds = []; for (let i = 0; i < 12; i++) { const w = sample([...Array(E.S).keys()], v.length).sort((a, b) => a - b); ds.push(w.map(sl).join(' and ')); } }
      else { const [x, y] = sample([...Array(E.n).keys()], 2); const gap = Math.abs(E.lv(E.truth[x]) - E.lv(E.truth[y])); const occBetween = E.truth.filter(s => E.lv(s) > Math.min(E.lv(E.truth[x]), E.lv(E.truth[y])) && E.lv(s) < Math.max(E.lv(E.truth[x]), E.lv(E.truth[y]))).length;
        question = `How many ${E.dom === 'box' ? 'boxes' : 'people'} are between ${E.dom === 'box' ? 'box ' : ''}${E.P[x]} and ${E.dom === 'box' ? 'box ' : ''}${E.P[y]}?`; ans = String(occBetween); ds = [occBetween + 1, occBetween + 2, Math.max(0, occBetween - 1), gap, 0, 1, 2, 3, 4].map(String); }
      const intro = cfg.intro(E);
      const clues = E.chosen.map(c => c.t);
      const steps = [{ text: 'Draw an empty grid. Each clue below removes the arrangements that break it.', viz: Object.assign(grid(E, false), { count: null }) }];
      let pl = allPlace(E.n, E.S), sl2 = null; const ap = E.attr ? allPlace(E.n, E.n) : null;
      E.chosen.forEach((c, i) => { if (!c.A) { pl = pl.filter(p => c.f(p)); if (sl2) sl2 = sl2.filter(z => c.f(z.p, z.a)); }
        else { if (!sl2) { sl2 = []; pl.forEach(p => ap.forEach(a => { if (E.chosen.slice(0, i).every(q => q.f(p, a))) sl2.push({ p, a }); })); } sl2 = sl2.filter(z => c.f(z.p, z.a)); }
        const SS = sl2 || pl.map(p => ({ p, a: null })); const G = grid(E, true);
        G.rows.forEach(r => { const s = r.sIdx; const who = new Set(SS.map(z => z.p.indexOf(s))); r.who = who.size === 1 ? ([...who][0] < 0 ? '—' : E.P[[...who][0]]) : '?';
          if (E.attr) { const av = new Set(SS.map(z => { const x = z.p.indexOf(s); return x < 0 ? '' : z.a ? E.AV[z.a[x]] : '?'; })); r.attr = av.size === 1 ? [...av][0] : '?'; } });
        const cnt = sl2 ? SS.length : E.attr ? SS.length + ' placement' : SS.length;
        steps.push({ text: `Clue ${i + 1}: ${c.t} → ${sl2 ? SS.length + ' full arrangement' + (SS.length === 1 ? '' : 's') : SS.length + ' placement' + (SS.length === 1 ? '' : 's') + (E.dom === 'box' ? ' of boxes' : ' of people')} left.`, viz: Object.assign(G, { count: cnt, clue: i }) }); });
      steps.push({ text: `Only one arrangement remains. Answer: ${ans}.`, viz: Object.assign(grid(E, true), { hl: ans }) });
      return { question: `${intro} ${question}`, intro, ask: question, clues, ...RL.mcq(ans, shuffle(ds)), viz: grid(E, false), steps,
        traps: ['"Immediately above" fixes a gap of one; "somewhere above" only fixes the order.', 'Vacant slots count as floors or days in "between" clues, but people-between counts only occupied ones.', 'Don\'t stop at the first arrangement that fits; check that it is the only one.'],
        params: { cfg: { n: E.n, S: E.S, dom: E.dom, flats: !!E.flats, attr: attrKey }, P: E.P, AV: E.AV, chosen: E.chosen.map(c => ({ k: c.k, x: c.x, y: c.y, w: c.w, v: c.v, s: c.s })), qk } };
    });
  }
  const T = (n, S, extra) => Object.assign({ n, S, T: 24, maxC: 14, k: n <= 5 && !extra.attr ? 2 : 3, minC: n <= 5 && !extra.attr ? 4 : extra.attr ? 7 : 6 }, extra);
  mkType('puz-e1', 'easy', 'Five floors, five people', ['ssc', 'bank', 'cuet', 'govt'], T(5, 5, { dom: 'floor', q: ['who', 'where', 'between'], intro: E => `Five people, ${E.P.join(', ')}, live on the five floors of a building (floor 1 is the bottom), one per floor.` }));
  mkType('puz-e2', 'easy', 'Five lectures, Monday to Friday', ['ssc', 'bank', 'cuet', 'govt'], T(5, 5, { dom: 'day', q: ['who', 'where'], intro: E => `Five teachers, ${E.P.join(', ')}, each give one lecture from Monday to Friday, one per day.` }));
  mkType('puz-e3', 'easy', 'Stack of five boxes', ['bank', 'ssc', 'cuet'], T(5, 5, { dom: 'box', q: ['who', 'where', 'between'], intro: E => `Five boxes, ${E.P.join(', ')}, are stacked one above another.` }));
  mkType('puz-m1', 'medium', 'Floors + colour preference', ['bank', 'ssc', 'cuet', 'govt'], T(5, 5, { dom: 'floor', attr: ['colour', 'fruit'], q: ['attr', 'who', 'where'], maxC: 16, intro: E => `Five people, ${E.P.join(', ')}, live on floors 1 to 5 (1 is the bottom), one per floor. Each likes a different ${E.attr.name.toLowerCase()}: ${E.AV.join(', ')}.` }));
  mkType('puz-m2', 'medium', 'Stack of seven boxes', ['bank', 'ssc'], T(7, 7, { dom: 'box', q: ['who', 'where', 'between'], maxC: 12, intro: E => `Seven boxes, ${E.P.join(', ')}, are stacked one above another.` }));
  mkType('puz-m3', 'medium', 'Week schedule with a free day', ['bank', 'ssc', 'govt'], T(6, 7, { dom: 'day', vac: true, q: ['who', 'where', 'vacant'], maxC: 13, intro: E => `Six teachers, ${E.P.join(', ')}, each give one lecture on a different day from Monday to Sunday. One day has no lecture.` }));
  mkType('puz-h1', 'hard', 'Eight floors, two vacant, with colours', ['bank', 'cat', 'ssc'], T(6, 8, { dom: 'floor', vac: true, attr: ['colour', 'fruit'], T: 12, q: ['attr', 'who', 'vacant', 'where'], maxC: 18, intro: E => `Six people, ${E.P.join(', ')}, live in an 8-storey building (floor 1 is the bottom), one per floor; two floors are vacant. Each likes a different ${E.attr.name.toLowerCase()}: ${E.AV.join(', ')}.` }));
  mkType('puz-h2', 'hard', 'Months × dates with subjects', ['bank', 'cat', 'ssc'], T(6, 6, { dom: 'month', attr: ['subject'], T: 12, q: ['attr', 'who', 'where'], maxC: 16, intro: E => `Six students, ${E.P.join(', ')}, take exams on the 8th or the 21st of March, June or September, one exam per date. Each takes a different subject: ${E.AV.join(', ')}.` }));
  mkType('puz-h3', 'hard', 'Four floors × two flats', ['bank', 'cat'], T(8, 8, { dom: 'floor', flats: true, q: ['who', 'where'], maxC: 16, intro: E => `Eight people, ${E.P.join(', ')}, live in a 4-storey building with a West flat and an East flat on each floor (floor 1 is the bottom). The East flat on any floor is directly above the East flat on the floor below.` }));
})(typeof globalThis !== 'undefined' ? globalThis : this);
