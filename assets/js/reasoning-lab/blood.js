/* Topic: Blood relations — fact lists, coded relations, pointing chains, auto-drawn family tree. */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample } = RL.u;
  RL.topic('blood', 'Blood Relations', '👪', 'Facts become an auto-drawn family tree. Read off any relation, in-laws included.', 'Logical Reasoning');
  const REL = { father: ['up', 'M'], mother: ['up', 'F'], son: ['down', 'M'], daughter: ['down', 'F'], brother: ['sib', 'M'], sister: ['sib', 'F'], husband: ['sp', 'M'], wife: ['sp', 'F'] };
  // facts: {a, rel, b}  meaning "a is the <rel> of b"
  function closure(facts) {
    const P = new Set(); facts.forEach(f => { P.add(f.a); P.add(f.b); });
    const par = new Map(), sp = new Map(), gen = new Map(), uf = new Map();
    const find = x => { while (uf.get(x) !== x) x = uf.get(x); return x; }; P.forEach(p => { uf.set(p, p); par.set(p, new Set()); });
    const union = (a, b) => { a = find(a); b = find(b); if (a !== b) { uf.set(a, b); return true; } return false; };
    for (const f of facts) { const [k, gd] = REL[f.rel]; gen.set(f.a, gd);
      if (k === 'up') par.get(f.b).add(f.a); if (k === 'down') par.get(f.a).add(f.b); if (k === 'sib') union(f.a, f.b); if (k === 'sp') { sp.set(f.a, f.b); sp.set(f.b, f.a); } }
    let ch = true; let guard = 0;
    while (ch && guard++ < 50) { ch = false;
      const groups = new Map(); P.forEach(p => { const r = find(p); if (!groups.has(r)) groups.set(r, []); groups.get(r).push(p); });
      for (const mem of groups.values()) { const all = new Set(); mem.forEach(m => par.get(m).forEach(x => all.add(x))); mem.forEach(m => all.forEach(x => { if (!par.get(m).has(x)) { par.get(m).add(x); ch = true; } })); }
      for (const p of P) { const ps = [...par.get(p)]; ps.forEach(x => { const s = sp.get(x); if (s && !par.get(p).has(s)) { par.get(p).add(s); ch = true; } });
        if (ps.length === 2 && !sp.has(ps[0])) { sp.set(ps[0], ps[1]); sp.set(ps[1], ps[0]); ch = true; } }
      const pl = [...P]; for (let i = 0; i < pl.length; i++) for (let j = i + 1; j < pl.length; j++) { const a = pl[i], b = pl[j]; if ([...par.get(a)].some(x => par.get(b).has(x)) && union(a, b)) ch = true; }
      for (const [a, b] of sp) { if (gen.has(a) && !gen.has(b)) { gen.set(b, gen.get(a) === 'M' ? 'F' : 'M'); ch = true; } }
    }
    const sib = (a, b) => a !== b && find(a) === find(b);
    return { P, par, sp, gen, sib, find };
  }
  const TERMS = { father: 0, mother: 0, son: 0, daughter: 0, brother: 0, sister: 0, husband: 0, wife: 0, grandfather: 0, grandmother: 0, grandson: 0, granddaughter: 0, uncle: 0, aunt: 0, nephew: 0, niece: 0, cousin: 0,
    'father-in-law': 0, 'mother-in-law': 0, 'son-in-law': 0, 'daughter-in-law': 0, 'brother-in-law': 0, 'sister-in-law': 0 };
  const TERM_LIST = Object.keys(TERMS);
  // returns {terms:Set, struct:Set} for X relative to Y
  function relation(C, x, y) { const { par, sp, gen, sib } = C; const out = new Set(), st = new Set(); const G = gen.get(x); const gn = (m, f) => G === 'M' ? m : G === 'F' ? f : null;
    const pY = [...par.get(y)], pX = [...par.get(x)]; const add = (s, t) => { st.add(s); if (t) out.add(t); };
    const isPar = (a, b) => par.get(b).has(a);
    if (isPar(x, y)) add('parent', gn('father', 'mother')); if (isPar(y, x)) add('child', gn('son', 'daughter')); if (sib(x, y)) add('sibling', gn('brother', 'sister'));
    if (sp.get(x) === y) add('spouse', gn('husband', 'wife'));
    if (pY.some(p => isPar(x, p))) add('grandparent', gn('grandfather', 'grandmother')); if (pX.some(p => isPar(y, p))) add('grandchild', gn('grandson', 'granddaughter'));
    const sibOrSpSib = (a, b) => sib(a, b) || [...C.P].some(s => sib(s, b) && sp.get(s) === a);
    if (pY.some(p => sibOrSpSib(x, p))) add('auncle', gn('uncle', 'aunt')); if (pX.some(p => sibOrSpSib(y, p))) add('nibling', gn('nephew', 'niece'));
    if (pX.some(a => pY.some(b => sib(a, b)))) add('cousin', 'cousin');
    if (sp.has(y) && isPar(x, sp.get(y))) add('parent-in-law', gn('father-in-law', 'mother-in-law'));
    if (sp.has(x) && isPar(y, sp.get(x))) add('child-in-law', gn('son-in-law', 'daughter-in-law'));
    if ((sp.has(y) && sib(x, sp.get(y))) || (sp.has(x) && sib(sp.get(x), y))) add('sibling-in-law', gn('brother-in-law', 'sister-in-law'));
    return { terms: out, struct: st }; }
  RL.blood = { closure, relation, REL };
  function family(names) { // random 3-generation family
    const N = shuffle(names); let i = 0; const ppl = []; const mk = gd => { const p = { name: N[i++], g: gd }; ppl.push(p); return p; };
    const facts = []; const g1 = mk('M'), g2 = mk('F'); const kids = [];
    for (let k = ri(2, 3); k > 0; k--) kids.push(mk(pick(['M', 'F'])));
    const all = { par: [], sp: [[g1, g2]] }; kids.forEach(c => { all.par.push([g1, c], [g2, c]); });
    kids.forEach(c => { if (i < N.length - 1 && Math.random() < .75) { const s = mk(c.g === 'M' ? 'F' : 'M'); all.sp.push([c, s]); for (let k = ri(1, 2); k > 0 && i < N.length; k--) { const gc = mk(pick(['M', 'F'])); all.par.push([c, gc], [s, gc]); } } });
    // atomic true facts
    const rel = (gd, m, f) => gd === 'M' ? m : f;
    all.par.forEach(([p, c]) => { facts.push({ a: p.name, rel: rel(p.g, 'father', 'mother'), b: c.name }); facts.push({ a: c.name, rel: rel(c.g, 'son', 'daughter'), b: p.name }); });
    all.sp.forEach(([a, b]) => { facts.push({ a: a.name, rel: rel(a.g, 'husband', 'wife'), b: b.name }); facts.push({ a: b.name, rel: rel(b.g, 'husband', 'wife'), b: a.name }); });
    for (const a of ppl) for (const b of ppl) if (a !== b) { const pa = all.par.filter(e => e[1] === a).map(e => e[0]), pb = all.par.filter(e => e[1] === b).map(e => e[0]); if (pa.length && pa[0] === pb[0]) facts.push({ a: a.name, rel: rel(a.g, 'brother', 'sister'), b: b.name }); }
    return { ppl, facts };
  }
  const factTxt = f => `${f.a} is the ${f.rel} of ${f.b}.`;
  const NAMES = ['ABCDEFGHJK', 'PQRSTUVWXY', 'KLMNOPQRST'];
  function treeViz(facts, hl) { const C = closure(facts); const people = [...C.P].map(p => ({ id: p, g: C.gen.get(p) || '?' })); const par = []; C.par.forEach((s, c) => s.forEach(p => par.push([p, c])));
    const sp = []; C.sp.forEach((b, a) => { if (a < b) sp.push([a, b]); }); const sib = []; const pl = [...C.P]; for (let i = 0; i < pl.length; i++) for (let j = i + 1; j < pl.length; j++) if (C.sib(pl[i], pl[j]) && !C.par.get(pl[i]).size) sib.push([pl[i], pl[j]]);
    return { kind: 'family', people, par, sp, sib, hl: hl || [] }; }
  function factsProblem(nmin, nmax, wantFar, allowCBD) {
    const F = family(pick(NAMES).split('')); const names = F.ppl.map(p => p.name);
    for (let t = 0; t < 60; t++) { const x = pick(names), y = pick(names.filter(n => n !== x));
      const truth = closure(F.facts); const r = relation(truth, x, y); if (r.terms.size !== 1) continue; const term = [...r.terms][0];
      if (wantFar && ['father', 'mother', 'son', 'daughter', 'husband', 'wife', 'brother', 'sister'].includes(term)) continue;
      let chosen = []; const pool = shuffle(F.facts.filter(f => true)); let ok = false;
      for (const f of pool) { chosen.push(f); const C = closure(chosen); if (!C.P.has(x) || !C.P.has(y)) continue; const rr = relation(C, x, y); if (rr.terms.size === 1 && [...rr.terms][0] === term) { ok = true; break; } }
      if (!ok) continue;
      for (let i = chosen.length - 1; i >= 0; i--) { const rest = chosen.filter((_, j) => j !== i); const C = closure(rest); if (C.P.has(x) && C.P.has(y)) { const rr = relation(C, x, y); if (rr.terms.size === 1 && [...rr.terms][0] === term) chosen = rest; } }
      // relevance: keep only facts in the connected component; drop facts not needed
      if (chosen.length < nmin || chosen.length > nmax) continue;
      let cbd = false, facts = chosen;
      if (allowCBD && Math.random() < .3) { // drop the fact that fixes x's gender, if structure survives
        for (let i = 0; i < facts.length; i++) { const rest = facts.filter((_, j) => j !== i); const C = closure(rest); if (C.P.has(x) && C.P.has(y) && !C.gen.has(x)) { const rr = relation(C, x, y); if (rr.terms.size === 0 && rr.struct.size === 1) { facts = rest; cbd = true; break; } } } }
      return { facts: shuffle(facts), x, y, term: cbd ? 'Cannot be determined' : term, real: term, cbd };
    } return null; }
  const termDistract = (term, x) => { const g = ['father', 'son', 'brother', 'husband', 'grandfather', 'grandson', 'uncle', 'nephew', 'father-in-law', 'son-in-law', 'brother-in-law'];
    const f = ['mother', 'daughter', 'sister', 'wife', 'grandmother', 'granddaughter', 'aunt', 'niece', 'mother-in-law', 'daughter-in-law', 'sister-in-law']; const i = g.indexOf(term) >= 0 ? g.indexOf(term) : f.indexOf(term);
    const near = i >= 0 ? [g[i], f[i], g[(i + 1) % g.length], f[(i + 1) % f.length], g[(i + 10) % 11]] : []; return shuffle(near).concat(shuffle(TERM_LIST)).filter(t => t !== term); };
  function factSteps(P) { const out = []; for (let i = 1; i <= P.facts.length; i++) out.push({ text: `Fact ${i}: ${factTxt(P.facts[i - 1])}`, viz: treeViz(P.facts.slice(0, i), i === P.facts.length ? [P.x, P.y] : []) });
    out.push({ text: P.cbd ? `The tree fixes how ${P.x} and ${P.y} are linked, but not ${P.x}'s gender, so the relation can't be determined.` : `Read the tree from ${P.y} to ${P.x}: ${P.x} is ${P.y}'s ${P.real}.`, viz: treeViz(P.facts, [P.x, P.y]) }); return out; }
  const TRAPS = ['Name the relation of the FIRST person to the SECOND. Reversing it is the most common slip.', 'A relation word needs a gender: without it you can only say "sibling" or "parent".', 'A parent\'s spouse is also that child\'s parent in these puzzles; siblings share both parents.'];
  function factsType(id, level, name, nmin, nmax, far, cbd) {
    RL.reg('blood', level, id, name, ['ssc', 'bank', 'cuet', 'govt'], () => { const P = factsProblem(nmin, nmax, far, cbd); if (!P) return null;
      const ds = termDistract(P.real).filter(t => t !== P.term); if (cbd) ds.unshift(P.cbd ? P.real : 'Cannot be determined');
      return { question: `Read the facts. How is ${P.x} related to ${P.y}?`, clues: P.facts.map(factTxt), ...RL.mcq(P.term, ds), viz: treeViz([], []), steps: factSteps(P), traps: TRAPS, params: { facts: P.facts, x: P.x, y: P.y } }; });
  }
  factsType('blood-e2', 'easy', 'Fact list: direct relation', 2, 4, false, false);
  factsType('blood-m1', 'medium', 'Fact list: uncles, cousins, in-laws', 3, 7, true, false);
  factsType('blood-h1', 'hard', 'Fact list with a possible "cannot be determined"', 4, 9, true, true);

  RL.reg('blood', 'medium', 'blood-m2', 'Who is X\'s relative?', ['ssc', 'bank', 'cuet', 'govt'], () => {
    const P = factsProblem(3, 7, true, false); if (!P) return null; const C = closure(P.facts);
    const others = [...C.P].filter(p => p !== P.y && p !== P.x && relation(C, p, P.y).terms.has(P.real)); if (others.length) return null;
    return { question: `Read the facts. Who is the ${P.real} of ${P.y}?`, clues: P.facts.map(factTxt), ...RL.mcq(P.x, shuffle([...C.P].filter(p => p !== P.x && p !== P.y))), viz: treeViz([], []), steps: factSteps(P), traps: TRAPS, params: { facts: P.facts, y: P.y, term: P.real } };
  });
  const SYMS = ['+', '−', '×', '÷', '@', '#', '$', '%'];
  function codedType(id, level, name, len) {
    RL.reg('blood', level, id, name, ['bank', 'ssc', 'govt'], () => {
      const F = family(pick(NAMES).split('')); const rels = sample(Object.keys(REL), 6); const syms = sample(SYMS, 6); const code = Object.fromEntries(rels.map((r, i) => [r, syms[i]]));
      const usable = F.facts.filter(f => code[f.rel]);
      for (let t = 0; t < 80; t++) { // random walk path
        let cur = pick(F.ppl).name; const path = [cur], used = []; for (let k = 0; k < len; k++) { const nx = shuffle(usable.filter(f => f.a === cur && !path.includes(f.b)))[0]; if (!nx) break; used.push(nx); path.push(nx.b); cur = nx.b; }
        if (used.length !== len) continue; const [x, y] = Math.random() < .5 ? [path[0], path[len]] : [path[len], path[0]];
        const C = closure(used); const r = relation(C, x, y); if (r.terms.size !== 1) continue; const term = [...r.terms][0];
        const expr = path.map((p, i) => i ? code[used[i - 1].rel] + ' ' + p : p).join(' ');
        const legend = rels.map(r => `'A ${code[r]} B' means A is the ${r} of B`);
        return { question: `In a code, ${legend.join('; ')}. If ${expr}, how is ${x} related to ${y}?`, clues: legend.map(s => s + '.').concat([`Expression: ${expr}`]),
          ...RL.mcq(term, termDistract(term)), viz: { kind: 'coderel', expr, legend }, steps: [{ text: `Decode the pairs left to right: ${used.map(factTxt).join(' ')}`, viz: treeViz(used.slice(0, 1)) },
            { text: 'Draw each pair into the family tree.', viz: treeViz(used, []) }, { text: `${x} is ${y}'s ${term}.`, viz: treeViz(used, [x, y]) }],
          traps: ['Each symbol links only the two names on either side of it.', 'Check the direction asked: X related to Y, not Y to X.', 'Gender comes from the code word for that person (father = male), so look for it.'], params: { legend, expr, x, y } };
      } return null;
    });
  }
  codedType('blood-e3', 'easy', 'Coded relations (3 people)', 2);
  codedType('blood-m3', 'medium', 'Coded relations (4–5 people)', 3);
  codedType('blood-h2', 'hard', 'Coded relations (5–6 people)', 5);
  // pointing chains
  const STEPW = ['father', 'mother', 'son', 'daughter', 'brother', 'sister', 'husband', 'wife'];
  const BAN = [['up', 'down'], ['down', 'up'], ['sib', 'sib'], ['sp', 'sp'], ['sp', 'down'], ['down', 'sp_'], ['up', 'up', 'down']];
  function chainProblem(minL, maxL) {
    for (let t = 0; t < 200; t++) { const L = ri(minL, maxL); const st = Array.from({ length: L }, () => pick(STEPW)); const ks = st.map(s => REL[s][0]);
      if (ks.some((k, i) => i && BAN.some(b => b.length === 2 && b[0] === ks[i - 1] && b[1] === k))) continue;
      if (st.some((s, i) => i && REL[s][0] === 'sp' && REL[st[i - 1]][1] === REL[s][1])) continue;
      const facts = []; let prev = 'S'; st.forEach((s, i) => { const id = 'p' + i; facts.push({ a: id, rel: s, b: prev }); prev = id; });
      const C = closure(facts); const r = relation(C, prev, 'S'); if (r.terms.size !== 1) continue; return { st, term: [...r.terms][0], facts }; } return null; }
  const SPK = [['Ravi', 'his'], ['Meena', 'her'], ['Arjun', 'his'], ['Kavya', 'her'], ['Imran', 'his'], ['Sara', 'her'], ['Neel', 'his'], ['Diya', 'her']];
  function pointType(id, level, name, a, b) {
    RL.reg('blood', level, id, name, ['ssc', 'bank', 'cuet', 'govt'], () => { const P = chainProblem(a, b); if (!P) return null; const need = P.st[0] === 'husband' ? 'her' : P.st[0] === 'wife' ? 'his' : null; const [sp] = pick(SPK.filter(s => !need || s[1] === need)); const gd = REL[P.st[P.st.length - 1]][1];
      const phrase = 'my ' + P.st.map((s, i) => i < P.st.length - 1 ? s + "'s" : s).join(' ');
      const who = gd === 'M' ? 'a man' : 'a woman';
      const nm = s => s === 'S' ? sp : 'P' + (+s.slice(1) + 1); const vf = P.facts.map(f => ({ a: nm(f.a), rel: f.rel, b: nm(f.b) }));
      return { question: `Pointing to ${who}, ${sp} said, "${gd === 'M' ? 'He' : 'She'} is ${phrase}." How is that ${gd === 'M' ? 'man' : 'woman'} related to ${sp}?`,
        ...RL.mcq(P.term, termDistract(P.term)), viz: treeViz([], []),
        steps: [{ text: `Start from ${sp} and build the chain one word at a time, from the end nearest "my".`, viz: treeViz(vf.slice(0, 1), [sp]) },
          ...vf.slice(1).map((f, i) => ({ text: `${f.a} is the ${f.rel} of ${f.b}.`, viz: treeViz(vf.slice(0, i + 2), []) })),
          { text: `So the ${gd === 'M' ? 'man' : 'woman'} (${vf[vf.length - 1].a}) is ${sp}'s ${P.term}.`, viz: treeViz(vf, [vf[vf.length - 1].a, sp]) }],
        traps: ['Read "my X\'s Y" from "my" outward: first X, then that person\'s Y.', '"My father\'s son" could be me, so these chains avoid such loops. Watch for them in exams.', 'In-law words describe a link through marriage, so check which spouse it goes through.'], params: { st: P.st, speaker: sp } }; });
  }
  pointType('blood-e1', 'easy', 'Pointing to a person (2 links)', 2, 2);
  pointType('blood-h3', 'hard', 'Pointing to a person (3–4 links, in-laws)', 3, 4);
})(typeof globalThis !== 'undefined' ? globalThis : this);
