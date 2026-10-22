// Renders every question type's visual 300 times in Node and flags invalid SVG (negative sizes, NaN).
const Q = require('./all.js'); global.window = global; global.QGen = Q; const V = require('../../assets/js/quant-lab/viz.js'); require('../../assets/js/quant-lab/viz2.js');
const QViz = V && V.render ? V : global.QViz; let bad = 0; const N = +process.env.RUNS || 300;
for (const t of Q.listTypes()) for (let i = 0; i < N; i++) { const p = Q.generate(t.topic, t.level, { typeId: t.id }); const s = QViz.render(p.viz);
  const m = s.match(/(?:width|height|\sr|rx|ry)="-[\d.]+|NaN|undefined|Infinity/); if (m) { if (bad++ < 10) console.log(t.id, m[0]); } }
console.log(bad ? `VIZ FAIL: ${bad}` : `VIZ OK: ${Q.listTypes().length} types × ${N}`); process.exit(bad ? 1 : 0);
