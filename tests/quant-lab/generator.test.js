// Quant Lab correctness suite (run: node tests/quant-lab/generator.test.js; RUNS=1000 for the full check).
// For EVERY question type: ≥200 generated problems, each re-solved by an independent solver (tests/solvers.js),
// plus: no NaN/undefined/Infinity anywhere, steps ≥ 1, traps ≥ 2, a visual spec, and the checker must
// accept the right answer (value, displayed form, and MCQ letter) and reject wrong ones.
const Q = require('./all.js'), S = require('./solvers.js');
const RUNS = +(process.env.RUNS || 200);
const types = Q.listTypes(); let pass = 0, fail = 0; const fails = [], perType = {}, missing = types.filter(t => !S[t.id]).map(t => t.id);
if (missing.length) { console.error('No solver for: ' + missing.join(', ')); process.exit(1); }
const t0 = Date.now();
for (const t of types) {
  let ok = 0;
  for (let i = 0; i < RUNS; i++) {
    const p = Q.generate(t.topic, t.level, { typeId: t.id }); const errs = [];
    const exp = S[t.id](JSON.parse(JSON.stringify(p.params)));
    const tol = Math.max(p.tol, 0.011);
    if (!(Math.abs(exp - p.answer) <= (p.tol < 0.011 ? 1e-6 : tol))) errs.push(`solver ${exp} ≠ ${p.answer}`);
    const blob = JSON.stringify(p); if (/NaN|undefined|Infinity/.test(blob)) errs.push('NaN/undefined in output');
    if (!(p.steps.length >= 1 && p.traps.length >= 2 && p.viz && p.viz.type)) errs.push('missing steps/traps/viz');
    if (!Q.check(p, String(p.answer)) || !Q.check(p, p.display)) errs.push('checker rejects right answer');
    if (Q.check(p, String(p.answer + 0.5)) || Q.check(p, String(p.answer - 1)) || Q.check(p, 'abc') || Q.check(p, '')) errs.push('checker accepts wrong answer');
    if (p.format === 'mcq') {
      if (p.options.length !== 4 || new Set(p.options.map(o => o.label)).size !== 4) errs.push('bad options');
      if (!Q.check(p, Q.LETTERS[p.answerIndex])) errs.push('MCQ right letter rejected');
      Q.LETTERS.forEach((L, k) => { if (k !== p.answerIndex && Q.check(p, L)) errs.push('MCQ wrong letter accepted'); });
      if (p.options.filter(o => Math.abs(o.v - p.answer) <= p.tol).length !== 1) errs.push('ambiguous MCQ');
    }
    if (errs.length) { fail++; if (fails.length < 25) fails.push({ id: t.id, q: p.question, errs, params: p.params }); } else { pass++; ok++; }
  }
  perType[t.id] = ok;
}
const formats = {}; types.forEach(t => { const f = Q.generate(t.topic, t.level, { typeId: t.id }).format; formats[t.level + '-' + f] = (formats[t.level + '-' + f] || 0) + 1; });
const summary = { topics: Object.keys(Q.TYPES).length, questionTypes: types.length, runsPerType: RUNS, totalRuns: pass + fail, pass, fail, formats, seconds: (Date.now() - t0) / 1000,
  minPerTopicLevel: Math.min(...Object.values(Q.TYPES).flatMap(l => Object.values(l).map(a => a.length))) };
console.log(JSON.stringify(summary, null, 1));
const weak = Object.entries(perType).filter(([, v]) => v < RUNS); if (weak.length) console.log('Types with failures:', weak);
if (fails.length) { console.log(JSON.stringify(fails, null, 1)); process.exit(1); }
console.log(`ALL ${pass} RUNS PASSED (${types.length} question types × ${RUNS})`);
