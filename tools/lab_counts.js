// Writes data/lab-counts.json for the homepage Labs section. Every number is computed from the lab code
// the browser runs (same loaders the lab test suites use). Run: node tools/lab_counts.js, then build_pages.py.
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const Q = require(path.join(ROOT, 'tests/quant-lab/all.js'));
const { RL } = require(path.join(ROOT, 'tests/reasoning-lab/load.js'));
const qTopics = Q.SECTIONS.flatMap(s => s.topics);
const all = k => RL.LEVELS.flatMap(l => RL.TOPICS[k].types[l]);
const rTopics = RL.ORDER.filter(k => RL.TOPICS[k] && all(k).length);
const labSrc = fs.readFileSync(path.join(ROOT, 'assets/js/reasoning-lab/lab.js'), 'utf8');
const sandbox = [...(labSrc.match(/const LABS = \[(.*?)\];/) || ['', ''])[1].matchAll(/\['(\w+)', '[^']*?([A-Za-z][^']*)'\]/g)].map(m => m[2]);
const bp = fs.readFileSync(path.join(ROOT, 'tools/build_pages.py'), 'utf8');
const cl = bp.slice(bp.indexOf('ql_page("quant-lab-concept-lab.html"'));
const sims = [...cl.slice(0, cl.indexOf('\nql_page(', 10) > 0 ? cl.indexOf('\nql_page(', 10) : cl.length).matchAll(/<div class="card[^"]*"><h2>([^<]+)<\/h2>/g)].map(m => m[1]);
const out = {
  quant: { topics: qTopics.length, sections: Q.SECTIONS.length, types: Q.listTypes().length },
  reasoning: { topics: rTopics.length, types: rTopics.reduce((s, k) => s + all(k).length, 0) },
  concept: { sims: sims.length, names: sims },
  sandbox: { builders: sandbox.length, names: sandbox }
};
fs.writeFileSync(path.join(ROOT, 'data/lab-counts.json'), JSON.stringify(out, null, 1) + '\n');
console.log(JSON.stringify(out));
