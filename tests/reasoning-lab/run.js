/* Correctness harness: every type × N runs, checked by an INDEPENDENT solver plus integrity checks.
   usage: node tests/run.js [N=1000] [typeFilterRegex] */
const { RL } = require('./load');
const fs = require('fs'), path = require('path');
const SOLVERS = {};
fs.readdirSync(path.join(__dirname, 'solvers')).filter(f => f.endsWith('.js')).forEach(f => Object.assign(SOLVERS, require('./solvers/' + f)));
const N = +(process.argv[2] || 1000), filt = process.argv[3] ? new RegExp(process.argv[3]) : null;
const okey = o => o.key || o.label;
function scan(x, where, errs) { // NaN / undefined / null / "undefined" / "NaN" anywhere in the problem
  if (x === undefined) return errs.push('undefined at ' + where);
  if (x === null) return errs.push('null at ' + where);
  if (typeof x === 'number' && !Number.isFinite(x)) return errs.push('non-finite at ' + where);
  if (typeof x === 'string') { if (/\bundefined\b|\bNaN\b|\[object Object\]|\bnull\b/.test(x)) errs.push('bad text at ' + where + ': ' + x.slice(0, 80)); return; }
  if (Array.isArray(x)) return x.forEach((v, i) => { if (v === null && /\.seats$/.test(where)) return; scan(v, where + '[' + i + ']', errs); }); // null seat = not yet fixed
  if (typeof x === 'object') for (const k of Object.keys(x)) { if (k === 'params' || k === 'fn') continue; if (x[k] === null && /^(hl|face|alt|clue|count|hc|ghost|final|to|attr|res|pts)$/.test(k)) continue; scan(x[k], where + '.' + k, errs); }
}
const report = []; let totalFail = 0; const t0 = Date.now();
for (const T of RL.listTypes()) {
  if (filt && !filt.test(T.id)) continue;
  const S = SOLVERS[T.id]; const fails = []; let ms = 0;
  if (!S) { report.push({ id: T.id, runs: 0, fails: 1, note: 'NO SOLVER' }); totalFail++; continue; }
  for (let i = 0; i < N && fails.length < 5; i++) {
    let p; const a = Date.now();
    try { p = RL.generate(T.topic, T.level, T.id); } catch (e) { fails.push('generate threw: ' + e.message); continue; } finally { ms += Date.now() - a; }
    if (!p) { fails.push('generate returned undefined'); continue; }
    const errs = [];
    if (p.typeId !== T.id) errs.push('wrong type');
    if (!Array.isArray(p.options) || p.options.length < 4) errs.push('fewer than 4 options');
    else {
      const ks = p.options.map(okey), ls = p.options.map(o => o.label);
      if (new Set(ks).size !== ks.length) errs.push('duplicate option keys');
      if (ls.some(l => l !== '') && new Set(ls).size !== ls.length) errs.push('duplicate option labels');
      if (!(p.answerIndex >= 0 && p.answerIndex < p.options.length)) errs.push('bad answerIndex');
    }
    if (!p.question || typeof p.question !== 'string') errs.push('no question');
    if (!p.steps || p.steps.length < 1) errs.push('no steps');
    if (!p.traps || p.traps.length < 2) errs.push('fewer than 2 traps');
    scan(Object.assign({ question: p.question, clues: p.clues, options: p.options, viz: p.viz, steps: p.steps, traps: p.traps }, p.intro !== undefined ? { intro: p.intro } : {}, p.ask !== undefined ? { ask: p.ask } : {}), 'p', errs);
    if (!errs.length) {
      try {
        const r = S(p); let correct;
        if (typeof r === 'function') correct = p.options.map((o, i) => r(o) ? i : -1).filter(i => i >= 0);
        else correct = p.options.map((o, i) => (okey(o) === r || o.label === r) ? i : -1).filter(i => i >= 0);
        if (correct.length !== 1) errs.push(`solver found ${correct.length} correct options (solver: ${typeof r === 'function' ? 'pred' : JSON.stringify(r)})`);
        else if (correct[0] !== p.answerIndex) errs.push(`solver says "${okey(p.options[correct[0]])}", generator says "${okey(p.options[p.answerIndex])}"`);
      } catch (e) { errs.push('solver error: ' + (e.stack || e).toString().split('\n').slice(0, 3).join(' | ')); }
    }
    if (errs.length) fails.push(errs.join('; ') + '\n      Q: ' + p.question.slice(0, 300) + (p.clues && p.clues.length ? '\n      clues: ' + p.clues.join(' / ').slice(0, 600) : '') + '\n      opts: ' + p.options.map(okey).join(' | ').slice(0, 300) + ' [ans ' + p.answerIndex + ']');
  }
  report.push({ id: T.id, runs: N, fails: fails.length, avgms: +(ms / N).toFixed(2), sample: fails.slice(0, 2) });
  if (fails.length) totalFail++;
}
for (const r of report) { console.log(`${r.fails ? 'FAIL' : 'ok  '} ${r.id.padEnd(10)} runs=${r.runs} ${r.note || ''} ${r.avgms !== undefined ? 'avg ' + r.avgms + 'ms' : ''}`); (r.sample || []).forEach(s => console.log('   - ' + String(s).split('\n').map(l => l.length > 500 ? l.slice(0, 500) + '…' : l).join('\n'))); }
console.log(`\n${report.length} types checked, ${totalFail} failing, ${((Date.now() - t0) / 1000).toFixed(1)}s`);
fs.writeFileSync(path.join(__dirname, 'last-run.json'), JSON.stringify({ N, when: new Date().toISOString(), totalTypes: report.length, failing: totalFail, report }, null, 1));
process.exit(totalFail ? 1 : 0);
