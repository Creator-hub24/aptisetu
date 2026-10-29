/* Independent blood-relation solver: parses the TEXT, derives facts with a rule-based fixpoint, then
   reads the relation off by definition. Gender unknown → tries both genders ("Cannot be determined"). */
const G = { father: 'M', mother: 'F', son: 'M', daughter: 'F', brother: 'M', sister: 'F', husband: 'M', wife: 'F' };
function derive(facts) { // facts: [a, rel, b]  "a is the rel of b"
  const P = new Set(), parent = new Set(), spouse = new Set(), sib = new Set(), sex = {};
  const k = (a, b) => a + '>' + b;
  for (const [a, r, b] of facts) { P.add(a); P.add(b); sex[a] = G[r];
    if (r === 'father' || r === 'mother') parent.add(k(a, b)); if (r === 'son' || r === 'daughter') parent.add(k(b, a));
    if (r === 'brother' || r === 'sister') { sib.add(k(a, b)); sib.add(k(b, a)); } if (r === 'husband' || r === 'wife') { spouse.add(k(a, b)); spouse.add(k(b, a)); } }
  const L = [...P]; let changed = true;
  const add = (S, x) => { if (!S.has(x)) { S.add(x); changed = true; } };
  while (changed) { changed = false;
    for (const p of L) for (const c of L) if (parent.has(k(p, c))) {
      for (const q of L) { if (spouse.has(k(p, q))) add(parent, k(q, c)); if (sib.has(k(c, q))) add(parent, k(p, q)); if (q !== c && parent.has(k(p, q))) { add(sib, k(c, q)); } }
      for (const q of L) if (q !== p && parent.has(k(q, c))) { add(spouse, k(p, q)); }
    }
    for (const a of L) for (const b of L) if (sib.has(k(a, b))) for (const c of L) if (c !== a && sib.has(k(b, c))) add(sib, k(a, c));
    for (const a of L) for (const b of L) if (spouse.has(k(a, b)) && sex[a] && !sex[b]) { sex[b] = sex[a] === 'M' ? 'F' : 'M'; changed = true; }
  }
  return { P: L, isPar: (a, b) => parent.has(k(a, b)), isSp: (a, b) => spouse.has(k(a, b)), isSib: (a, b) => a !== b && sib.has(k(a, b)), sex };
}
function terms(W, x, y, sx) { const t = new Set(), g = (m, f) => sx === 'M' ? m : f; const L = W.P;
  const parOf = c => L.filter(p => W.isPar(p, c));
  if (W.isPar(x, y)) t.add(g('father', 'mother')); if (W.isPar(y, x)) t.add(g('son', 'daughter')); if (W.isSib(x, y)) t.add(g('brother', 'sister')); if (W.isSp(x, y)) t.add(g('husband', 'wife'));
  if (parOf(y).some(p => W.isPar(x, p))) t.add(g('grandfather', 'grandmother')); if (parOf(x).some(p => W.isPar(y, p))) t.add(g('grandson', 'granddaughter'));
  // uncle/aunt: sibling of a parent, or spouse of a parent's sibling
  if (parOf(y).some(p => W.isSib(x, p) || L.some(s => W.isSib(s, p) && W.isSp(x, s)))) t.add(g('uncle', 'aunt'));
  if (parOf(x).some(p => W.isSib(y, p) || L.some(s => W.isSib(s, p) && W.isSp(y, s)))) t.add(g('nephew', 'niece'));
  if (parOf(x).some(a => parOf(y).some(b => W.isSib(a, b)))) t.add('cousin');
  if (L.some(s => W.isSp(s, y) && W.isPar(x, s))) t.add(g('father-in-law', 'mother-in-law'));
  if (L.some(s => W.isSp(s, x) && W.isPar(y, s))) t.add(g('son-in-law', 'daughter-in-law'));
  if (L.some(s => (W.isSp(s, y) && W.isSib(x, s)) || (W.isSp(s, x) && W.isSib(s, y)))) t.add(g('brother-in-law', 'sister-in-law'));
  return t; }
function answer(facts, x, y) { const W = derive(facts);
  if (W.sex[x]) { const t = terms(W, x, y, W.sex[x]); if (t.size !== 1) throw new Error('solver: relation not unique: ' + [...t]); return [...t][0]; }
  const a = terms(W, x, y, 'M'), b = terms(W, x, y, 'F'); const both = [...a].filter(t => b.has(t));
  if (a.size === 1 && b.size === 1 && both.length === 1) return both[0]; if (a.size || b.size) return 'Cannot be determined'; throw new Error('solver: no relation'); }
const parseFacts = clues => clues.map(c => { const m = c.match(/^(\w+) is the ([\w-]+) of (\w+)\.$/); if (!m) throw new Error('bad fact ' + c); return [m[1], m[2], m[3]]; });
const factsQ = p => { const m = p.question.match(/How is (\w+) related to (\w+)\?/); return answer(parseFacts(p.clues), m[1], m[2]); };
const coded = p => { const leg = {}; for (const m of p.question.matchAll(/'A (\S+) B' stands for: A is B's (\w+)/g)) leg[m[1]] = m[2];
  const m = p.question.match(/If (.+), how is (\w+) related to (\w+)\?/); const tk = m[1].split(' '); const facts = [];
  for (let i = 1; i < tk.length; i += 2) { if (!leg[tk[i]]) throw new Error('bad sym'); facts.push([tk[i - 1], leg[tk[i]], tk[i + 1]]); }
  return answer(facts, m[2], m[3]); };
const point = p => { const m = p.question.match(/Pointing to a (man|woman), (\w+) said, "(He|She) is my (.+)\." How is/); const words = m[4].split(' ').map(w => w.replace(/'s$/, ''));
  // my w1's w2's ... wk : chain from speaker outward
  const facts = []; let prev = m[2]; words.forEach((w, i) => { const id = 'Q' + i; facts.push([id, w, prev]); prev = id; });
  const W = derive(facts); const sx = m[1] === 'man' ? 'M' : 'F'; if (W.sex[prev] !== sx) throw new Error('gender mismatch');
  const t = terms(W, prev, m[2], sx); if (t.size !== 1) throw new Error('not unique ' + [...t]); return [...t][0]; };
const who = p => { const m = p.question.match(/Who is the ([\w-]+) of (\w+)\?/); const W = derive(parseFacts(p.clues));
  return o => W.P.includes(o.label) && o.label !== m[2] && (W.sex[o.label] ? terms(W, o.label, m[2], W.sex[o.label]).has(m[1]) : terms(W, o.label, m[2], 'M').has(m[1]) && terms(W, o.label, m[2], 'F').has(m[1])); };
module.exports = { 'blood-e1': point, 'blood-h3': point, 'blood-e2': factsQ, 'blood-m1': factsQ, 'blood-h1': factsQ, 'blood-m2': who, 'blood-e3': coded, 'blood-m3': coded, 'blood-h2': coded };
