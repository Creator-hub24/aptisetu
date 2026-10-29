/* Independent coding solver: own implementations of the rule families, number rules, bijection search and condition table. */
const AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', v = c => AL.indexOf(c), L = n => AL[((n % 26) + 26) % 26];
const mv = (arr, fn) => arr.map((c, i) => L(v(c) + fn(i))).join('');
const fam = {};
const reverseHalves = s => { const n = s.length, h = Math.floor(n / 2), a = s.slice(0, h).split('').reverse(), m = n % 2 ? [s[h]] : [], b = s.slice(n - h).split('').reverse(); return a.concat(m, b); };
const swapPairs = s => { const a = s.split(''); for (let i = 0; i < a.length - 1; i += 2) { const t = a[i]; a[i] = a[i + 1]; a[i + 1] = t; } return a; };
const R = [];
for (let k = -5; k <= 5; k++) if (k) R.push(w => mv(w.split(''), () => k));
for (let k = -3; k <= 3; k++) R.push(w => mv(w.split('').reverse(), () => k));
for (let a = 1; a <= 3; a++) for (let b = 1; b <= 3; b++) R.push(w => mv(w.split(''), i => (i & 1 ? -b : a)));
for (const s of [1, -1]) for (const c of [0, 1]) R.push(w => mv(w.split(''), i => s * (i + c)));
for (const k of [-1, 0, 1]) R.push(w => mv(w.split('').map(c => L(25 - v(c))), () => k));
for (let k = -2; k <= 2; k++) R.push(w => mv(reverseHalves(w), () => k));
for (const k of [-1, 0, 1]) R.push(w => mv(swapPairs(w), () => k));
function encode(p) { const m = p.question.match(/In a certain code, (\w+) is written as (\w+)\. How is (\w+) written/); const fits = R.filter(f => f(m[1]) === m[2]);
  const outs = new Set(fits.map(f => f(m[3]))); if (outs.size !== 1) throw new Error('rule ambiguous/none: ' + outs.size); return [...outs][0]; }
const sum = w => [...w].reduce((s, c) => s + v(c) + 1, 0);
const NR = [w => sum(w), w => w.length * 27 - sum(w), w => sum(w) + w.length, w => 2 * sum(w), w => sum(w) * w.length];
const isV = c => /[AEIOU]/.test(c);
module.exports = {
  'code-e1': encode, 'code-e2': encode, 'code-m1': encode, 'code-m2': encode, 'code-h2': encode,
  'code-h3': p => { const m = p.question.match(/In a certain code, (\w+) is written as (\w+)\. Which word is written as (\w+) in/); const fits = R.filter(f => f(m[1]) === m[2]);
    return o => fits.length > 0 && fits.every(f => f(o.label) === m[3]); },
  'code-e3': p => { const m = p.question.match(/If (\w+) is coded as (\d+), what is the code for (\w+)\?/); const outs = new Set(NR.filter(f => f(m[1]) === +m[2]).map(f => f(m[3])));
    if (outs.size !== 1) throw new Error('num ambiguous'); return String([...outs][0]); },
  'code-m3': p => { const S = p.clues.map(c => { const m = c.match(/^"(.+)" → "(.+)"$/); return [m[1].split(' '), m[2].split(' ')]; }); const x = p.question.match(/What is the code for "(\w+)"\?/)[1];
    const words = [...new Set(S.flatMap(s => s[0]))], codes = [...new Set(S.flatMap(s => s[1]))]; const found = new Set(); const asg = {}, used = new Set();
    (function go(i) { if (i === words.length) { // each sentence's code multiset must be exactly its words' codes
        if (S.every(([ws, cs]) => ws.map(w => asg[w]).sort().join() === cs.slice().sort().join())) found.add(asg[x]); return; }
      for (const c of codes) if (!used.has(c) && S.every(([ws, cs]) => !ws.includes(words[i]) || cs.includes(c))) { asg[words[i]] = c; used.add(c); go(i + 1); used.delete(c); } })(0);
    if (found.size !== 1) throw new Error('code not unique: ' + found.size); return [...found][0]; },
  'code-h1': p => { const Ls = p.clues[0].replace('Letter:', '').trim().split(/\s+/), Ss = p.clues[1].replace('Code:', '').trim().split(/\s+/); const t = {}; Ls.forEach((l, i) => { t[l] = Ss[i]; });
    const w = p.question.match(/code for (\w+)\?/)[1]; const c = [...w].map(x => t[x]); const n = c.length - 1, f = isV(w[0]), l = isV(w[n]);
    if (f && !l) { const z = c[0]; c[0] = c[n]; c[n] = z; } else if (!f && !l) { c[0] = '*'; c[n] = '*'; } else if (!f && l) c[n] = c[0]; return c.join(''); },
};
