/* Topic: Coding–decoding — letter shifts, rule families, number codes, sentence codes, conditional codes */
(function (g) {
  'use strict';
  const RL = g.RL, { ri, pick, shuffle, sample } = RL.u;
  RL.topic('coding', 'Coding–Decoding', '🔤', 'Each letter shift is drawn as an arrow on the alphabet strip, so the code rule is easy to see.', 'Verbal & Coding');
  const A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', pos = c => A.indexOf(c) + 1, ch = n => A[((n - 1) % 26 + 26) % 26];
  const WORDS = ['GARDEN', 'BASKET', 'MIRROR', 'SHIELD', 'BRIGHT', 'FOREST', 'CANDLE', 'MARKET', 'WINTER', 'POCKET', 'THRONE', 'SPRING', 'HUNTER', 'JACKET', 'FLOWER', 'ORANGE', 'PENCIL', 'CASTLE', 'DRAGON', 'TICKET', 'VELVET', 'ZEBRA', 'QUIET', 'MELON', 'TIGER', 'LEMON', 'PIANO', 'CLOUD', 'STORM', 'BREAD', 'CHAIR', 'EAGLE', 'FROST', 'WATER', 'NIGHT', 'PLANT', 'SUGAR', 'HOUSE', 'MAGIC', 'PRIDE', 'RIVER', 'TOWER', 'BLADE', 'CROWN', 'FIELD', 'GLASS', 'HONEY', 'JUICE', 'KNIFE', 'LIGHT'];
  const shiftW = (w, d) => [...w].map((c, i) => ch(pos(c) + d(i))).join('');
  const halves = w => { const h = w.length >> 1; return [...w.slice(0, h)].reverse().join('') + (w.length % 2 ? w[h] : '') + [...w.slice(w.length - h)].reverse().join(''); };
  const pairs = w => { const a = [...w]; for (let i = 0; i + 1 < a.length; i += 2) [a[i], a[i + 1]] = [a[i + 1], a[i]]; return a.join(''); };
  const rev = w => [...w].reverse().join(''), opp = w => [...w].map(c => ch(27 - pos(c))).join('');
  const sg = k => (k >= 0 ? '+' : '−') + Math.abs(k);
  const RULES = [];
  for (let k = -5; k <= 5; k++) if (k) RULES.push({ id: 'shift' + k, fam: 'shift', f: w => shiftW(w, () => k), d: `Each letter moves ${sg(k)}.` });
  for (let k = -3; k <= 3; k++) RULES.push({ id: 'rev' + k, fam: 'rev', f: w => shiftW(rev(w), () => k), d: `Reverse the word${k ? ', then move each letter ' + sg(k) : ''}.` });
  for (let a = 1; a <= 3; a++) for (let b = 1; b <= 3; b++) RULES.push({ id: `alt${a}_${b}`, fam: 'alt', f: w => shiftW(w, i => i % 2 ? -b : a), d: `Letters alternately move +${a} and −${b}.` });
  for (const s of [1, -1]) for (const c of [0, 1]) RULES.push({ id: `pos${s}_${c}`, fam: 'pos', f: w => shiftW(w, i => s * (i + c)), d: `The letter in position i moves ${s > 0 ? '+' : '−'}(i${c ? '' : '−1'}): ${s > 0 ? '+' : '−'}${c}, ${s > 0 ? '+' : '−'}${c + 1}, ${s > 0 ? '+' : '−'}${c + 2}, …` });
  for (const k of [0, 1, -1]) RULES.push({ id: 'opp' + k, fam: 'opp', f: w => shiftW(opp(w), () => k), d: `Replace each letter with its opposite (A↔Z, B↔Y, …)${k ? ', then move ' + sg(k) : ''}.` });
  for (const k of [-2, -1, 0, 1, 2]) RULES.push({ id: 'half' + k, fam: 'half', f: w => shiftW(halves(w), () => k), d: `Reverse each half of the word${k ? ', then move each letter ' + sg(k) : ''}.` });
  for (const k of [-1, 0, 1]) RULES.push({ id: 'pair' + k, fam: 'pair', f: w => shiftW(pairs(w), () => k), d: `Swap each adjacent pair of letters${k ? ', then move each letter ' + sg(k) : ''}.` });
  RL.codeRules = RULES;
  const shiftViz = (from, to, extra) => Object.assign({ kind: 'shift', from, to }, extra || {});
  function ruleProblem(id, level, name, fams, exams, decode) {
    RL.reg('coding', level, id, name, exams, () => {
      const R = pick(RULES.filter(r => fams.includes(r.fam) && !(r.fam === 'rev' && r.id === 'rev0' && Math.random() < .5)));
      for (let t = 0; t < 60; t++) { const [w1, w2] = sample(WORDS.filter(w => w.length >= 5), 2); const c1 = R.f(w1), c2 = R.f(w2);
        const match = RULES.filter(r => r.f(w1) === c1); if (new Set(match.map(r => r.f(w2))).size !== 1) continue; if (c1 === w1 || c2 === w2) continue;
        if (w1.length !== w2.length && (R.fam === 'half' || R.fam === 'pair') && Math.random() < .3) continue;
        const ans = decode ? w2 : c2; const ds = decode ? [] : RULES.filter(r => r.f(w2) !== c2).map(r => r.f(w2));
        if (decode) { RULES.forEach(r => { if (r.f(c2) !== w2) ds.push(r.f(c2)); }); ds.push(shiftW(w2, i => (i === 1 ? 1 : 0))); }
        const near = [shiftW(ans, i => (i === ans.length - 1 ? 1 : 0)), shiftW(ans, i => (i === 0 ? -1 : 0)), rev(ans)];
        const pool = shuffle(near).slice(0, 2).concat(shuffle(ds)).filter(x => x !== ans && x.length === ans.length);
        const qtxt = decode ? `In a certain code, ${w1} is written as ${c1}. Which word is written as ${c2} in that code?` : `In a certain code, ${w1} is written as ${c1}. How is ${w2} written in that code?`;
        const stA = decode ? { text: `Undo the rule on ${c2} to get the word back: ${w2}.`, viz: shiftViz(w2, c2, { rule: R.id, back: true }) } : { text: `Apply the same rule to ${w2}: ${c2}.`, viz: shiftViz(w2, c2, { rule: R.id }) };
        return { question: qtxt, ...RL.mcq(ans, pool), viz: shiftViz(w1, c1, { rule: R.id }),
          steps: [{ text: `Compare ${w1} → ${c1} letter by letter.`, viz: shiftViz(w1, c1, { rule: R.id, arrows: true }) }, { text: `Rule: ${R.d}`, viz: shiftViz(w1, c1, { rule: R.id, arrows: true, explain: true }) }, stA],
          traps: ['Check the rule on every letter, not just the first two.', 'Count shifts on the alphabet strip and remember it wraps: Z + 1 = A.', R.fam === 'rev' || R.fam === 'half' ? 'Reversed codes look like random shifts until you line them up from the other end.' : 'Shifts may alternate or grow with position, so write down each letter\'s difference.'],
          params: { w1, c1, w2, rule: R.id } }; } return null;
    });
  }
  ruleProblem('code-e1', 'easy', 'Uniform letter shift', ['shift'], ['ssc', 'bank', 'cuet', 'govt']);
  ruleProblem('code-e2', 'easy', 'Reverse or opposite letters', ['rev', 'opp'], ['ssc', 'bank', 'cuet', 'govt']);
  ruleProblem('code-m1', 'medium', 'Alternating and positional shifts', ['alt', 'pos'], ['ssc', 'bank', 'cuet', 'govt']);
  ruleProblem('code-h2', 'hard', 'Halves and pair swaps with a shift', ['half', 'pair'], ['ssc', 'bank', 'cat']);
  ruleProblem('code-h3', 'hard', 'Decode: find the original word', ['alt', 'pos', 'rev', 'half', 'opp'], ['ssc', 'bank', 'cuet'], true);
  const NUMR = [{ id: 'sum', f: w => [...w].reduce((s, c) => s + pos(c), 0), d: 'Add the letter positions (A = 1 … Z = 26).' },
    { id: 'rsum', f: w => [...w].reduce((s, c) => s + 27 - pos(c), 0), d: 'Add the reverse positions (A = 26 … Z = 1).' },
    { id: 'sumlen', f: w => [...w].reduce((s, c) => s + pos(c), 0) + w.length, d: 'Add the letter positions, then add the number of letters.' },
    { id: 'sum2', f: w => 2 * [...w].reduce((s, c) => s + pos(c), 0), d: 'Add the letter positions, then double the total.' },
    { id: 'sumlenx', f: w => [...w].reduce((s, c) => s + pos(c), 0) * w.length, d: 'Add the letter positions, then multiply by the number of letters.' }];
  RL.numRules = NUMR;
  RL.reg('coding', 'easy', 'code-e3', 'Number value of a word', ['ssc', 'cuet', 'govt'], () => {
    const R = pick(NUMR); for (let t = 0; t < 60; t++) { const [w1, w2] = sample(WORDS.filter(w => w.length <= 5), 2);
      const m = NUMR.filter(r => r.f(w1) === R.f(w1)); if (new Set(m.map(r => r.f(w2))).size !== 1) continue; const ans = R.f(w2);
      return { question: `If ${w1} is coded as ${R.f(w1)}, what is the code for ${w2}?`, ...RL.mcq(String(ans), NUMR.map(r => String(r.f(w2))).concat(RL.numDistract(ans, 6, []).map(String))), viz: shiftViz(w1, null, { nums: [...w1].map(pos), rev: R.id === 'rsum' }),
        steps: [{ text: `Positions in ${w1}: ${[...w1].map(c => `${c}=${R.id === 'rsum' ? 27 - pos(c) : pos(c)}`).join(', ')}.`, viz: shiftViz(w1, null, { nums: [...w1].map(c => R.id === 'rsum' ? 27 - pos(c) : pos(c)) }) },
          { text: `Rule: ${R.d} ${w1} → ${R.f(w1)}.` }, { text: `${w2}: ${[...w2].map(c => R.id === 'rsum' ? 27 - pos(c) : pos(c)).join(' + ')} → ${ans}.`, viz: shiftViz(w2, null, { nums: [...w2].map(c => R.id === 'rsum' ? 27 - pos(c) : pos(c)) }) }],
        traps: ['Remember EJOTY: E = 5, J = 10, O = 15, T = 20, Y = 25.', 'Check whether the total also involves the word length.'], params: { w1, w2, rule: R.id } }; } return null;
  });
  const VOC = ['sky', 'is', 'blue', 'sun', 'hot', 'red', 'rose', 'grows', 'fast', 'tall', 'tree', 'green', 'sea', 'deep', 'wide', 'birds', 'fly', 'high', 'rain', 'falls'];
  const CODES = ['ka', 'pi', 'to', 'mu', 'ze', 'lo', 'ra', 'ni', 'su', 'te', 'bo', 'fa', 'qi', 'de'];
  function sentenceSolve(sents, words) { // all bijections consistent with unordered code sets
    const sol = []; const asg = {}; const used = new Set(); const cand = w => { let s = null; sents.forEach(([ws, cs]) => { if (ws.includes(w)) s = s ? s.filter(c => cs.includes(c)) : cs.slice(); }); return s; };
    const C = Object.fromEntries(words.map(w => [w, cand(w)])); const order = words.slice().sort((a, b) => C[a].length - C[b].length);
    (function bt(i) { if (sol.length > 50) return; if (i === order.length) { if (sents.every(([ws, cs]) => ws.every(w => cs.includes(asg[w])))) sol.push(Object.assign({}, asg)); return; }
      const w = order[i]; for (const c of C[w]) if (!used.has(c)) { asg[w] = c; used.add(c); bt(i + 1); used.delete(c); delete asg[w]; } })(0); return sol; }
  RL.reg('coding', 'medium', 'code-m3', 'Sentence codes (common words)', ['bank', 'ssc', 'cuet', 'govt'], () => {
    for (let t = 0; t < 200; t++) { const words = sample(VOC, ri(6, 7)), codes = sample(CODES, words.length), map = Object.fromEntries(words.map((w, i) => [w, codes[i]]));
      const sents = []; for (let i = 0; i < 4; i++) { const ws = sample(words, ri(3, 4)); sents.push([ws, shuffle(ws.map(w => map[w]))]); }
      const inS = words.filter(w => sents.some(s => s[0].includes(w))); if (inS.length < 5) continue; const S = sentenceSolve(sents, inS); if (!S.length) continue;
      const det = inS.filter(w => S.every(s => s[w] === S[0][w])); if (!det.length) continue; const x = pick(det); const ans = map[x];
      const sx = sents.filter(s => s[0].includes(x)); const ds = sx.flatMap(s => s[1]).concat(codes).filter(c => c !== ans);
      return { question: `In a code language, ${sents.map(([ws, cs]) => `"${ws.join(' ')}" is written as "${cs.join(' ')}"`).join('; ')}. What is the code for "${x}"?`, clues: sents.map(([ws, cs]) => `"${ws.join(' ')}" → "${cs.join(' ')}"`),
        ...RL.mcq(ans, shuffle([...new Set(ds)])), viz: { kind: 'codetable', sents, hl: null },
        steps: [{ text: 'Codes in a sentence are jumbled, so match by common words: a word shared by sentences keeps the code they share.', viz: { kind: 'codetable', sents, hl: null } },
          { text: `"${x}" appears in ${sx.length} sentence(s). Intersect their codes and remove codes already fixed for other words.`, viz: { kind: 'codetable', sents, hl: x, hc: ans } },
          { text: `Only "${ans}" survives → "${x}" = ${ans}.`, viz: { kind: 'codetable', sents, hl: x, hc: ans, done: true } }],
        traps: ['Code order is not word order.', 'One sentence alone never fixes a code. You need overlaps or eliminations.'], params: { sents, x } }; } return null;
  });
  RL.sentenceSolve = sentenceSolve;
  ruleProblem('code-m2', 'medium', 'Reverse then shift', ['rev'], ['ssc', 'bank', 'cuet']);
  // conditional letter → symbol coding (banking)
  const SYM = ['3', '7', '@', '5', '%', '9', '$', '2', '&', '4', '©', '8', '#', '6', '1'];
  const isV = c => 'AEIOU'.includes(c);
  RL.condCode = function (word, tbl) { const c = [...word].map(x => tbl[x]); const f = word[0], l = word[word.length - 1];
    if (isV(f) && !isV(l)) { [c[0], c[c.length - 1]] = [c[c.length - 1], c[0]]; return [c.join(''), 1]; }
    if (!isV(f) && !isV(l)) { c[0] = '*'; c[c.length - 1] = '*'; return [c.join(''), 2]; }
    if (!isV(f) && isV(l)) { c[c.length - 1] = c[0]; return [c.join(''), 3]; } return [c.join(''), 0]; };
  const COND = ['(i) If the first letter is a vowel and the last letter is a consonant, swap their codes.', '(ii) If the first and last letters are both consonants, code both as *.', '(iii) If the first letter is a consonant and the last letter is a vowel, code the last letter with the first letter\'s code.'];
  RL.reg('coding', 'hard', 'code-h1', 'Letter–symbol coding with conditions', ['bank', 'ssc'], () => {
    const L = sample([...'BDEFHIKMPRTAUW'], 10); if (!L.some(isV) || L.filter(isV).length < 2) return null; const S = sample(SYM, 10); const tbl = Object.fromEntries(L.map((x, i) => [x, S[i]]));
    const word = Array.from({ length: ri(5, 6) }, () => pick(L)).join(''); if (new Set(word).size < 4) return null; const [ans, cond] = RL.condCode(word, tbl);
    const raw = [...word].map(x => tbl[x]).join(''); const r = [...raw]; const ds = [raw, raw[raw.length - 1] + raw.slice(1, -1) + raw[0], '*' + raw.slice(1, -1) + '*', raw.slice(0, -1) + raw[0], [...ans].reverse().join('')];
    return { question: `Letters are coded using the table, subject to the conditions. What is the code for ${word}?`, clues: [`Letter: ${L.join(' ')}`, `Code:   ${S.join(' ')}`].concat(COND),
      ...RL.mcq(ans, ds), viz: { kind: 'symtable', L, S, word },
      steps: [{ text: `Plain codes: ${word} → ${raw}.`, viz: { kind: 'symtable', L, S, word, hl: [...word] } },
        { text: cond ? `First letter ${word[0]} is a ${isV(word[0]) ? 'vowel' : 'consonant'}; last letter ${word.slice(-1)} is a ${isV(word.slice(-1)) ? 'vowel' : 'consonant'} → condition ${['', '(i)', '(ii)', '(iii)'][cond]} applies.` : 'First and last letters are both vowels, so no condition applies.' },
        { text: `Final code: ${ans}.` }],
      traps: ['Check the conditions before writing the plain code.', 'A vowel-vowel ending triggers no condition.'], params: { L, S, word } };
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
