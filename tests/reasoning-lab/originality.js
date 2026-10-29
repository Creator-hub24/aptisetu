/* Originality scan: generated Reasoning Lab questions vs the site's existing question bank (data/), plus PYQ markers.
   usage: node tests/reasoning-lab/originality.js [samplesPerType=200] */
const fs = require('fs'), path = require('path');
const { RL } = require('./load');
const ROOT = path.join(__dirname, '..', '..');
const N = +(process.argv[2] || 200);
const norm = s => String(s).replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/g, ' ').toLowerCase().replace(/([+×÷−\-@#$%&*=<>≤≥?!])/g, ' $1 ').replace(/[^a-z0-9+×÷−\-@#$%&*=<>≤≥?!]+/g, ' ').trim(); // symbols kept: they carry the meaning in coded-relation questions
const FILES = ['data/general/reasoning.json', 'data/general/dilr.json', 'data/cat/dilr.json', 'data/cat/sets.json', 'data/cuet/gat.json', 'data/questions.json', 'data/cat.json', 'data/cuet.json', 'data/open-mock.json'].filter(f => fs.existsSync(path.join(ROOT, f)));
const corpus = []; const walk = (x, src) => { if (typeof x === 'string') { const t = norm(x); if (t.split(' ').length >= 8) corpus.push({ t, src }); } else if (Array.isArray(x)) x.forEach(v => walk(v, src)); else if (x && typeof x === 'object') Object.values(x).forEach(v => walk(v, src)); };
FILES.forEach(f => walk(JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8')), f));
const K = 8; const sh = t => { const w = t.split(' '), o = []; for (let i = 0; i + K <= w.length; i++) o.push(w.slice(i, i + K).join(' ')); return o; };
const C = new Map(); corpus.forEach((c, i) => sh(c.t).forEach(g => { if (!C.has(g)) C.set(g, i); }));
const exact = new Set(corpus.map(c => c.t));
let worst = [], total = 0, exactHits = 0;
for (const T of RL.listTypes()) {
  let best = { r: 0, id: T.id };
  for (let i = 0; i < N; i++) { const p = RL.generate(T.topic, T.level, T.id); total++;
    const text = norm([p.question].concat(p.clues || [], p.ask ? [p.ask] : []).join(' ')); if (exact.has(text)) exactHits++;
    const g = sh(text); if (!g.length) continue; const hit = g.filter(x => C.has(x)); const r = hit.length / g.length;
    if (r > best.r) best = { r, id: T.id, text: text.slice(0, 160), hits: hit.slice(0, 3), src: hit.length ? corpus[C.get(hit[0])].src + ': ' + corpus[C.get(hit[0])].t.slice(0, 160) : '' }; }
  worst.push(best);
}
worst.sort((a, b) => b.r - a.r);
const MARK = /\bPYQs?\b|previous[- ]year|asked in (the )?(cat|ssc|ibps|sbi|cuet)|\b(CAT|CGL|CHSL|IBPS|SBI|CUET|RRB)\s*(PO|Clerk|Mains|Prelims)?\s*['’]?(19|20)\d\d\b|\b(shift|slot)\s*[123]\b|memory[- ]based/i;
const DIR = path.join(ROOT, 'assets', 'js', 'reasoning-lab'); const marks = [];
fs.readdirSync(DIR).forEach(f => fs.readFileSync(path.join(DIR, f), 'utf8').split('\n').forEach((l, i) => { const m = l.match(MARK); if (m) marks.push(`${f}:${i + 1}: ${m[0]}`); }));
const out = { samples: total, corpusStrings: corpus.length, files: FILES, exactMatches: exactHits, maxOverlap: worst[0].r, over25: worst.filter(w => w.r > 0.25).length, top8: worst.slice(0, 8), over25ids: worst.filter(w => w.r > 0.25).map(w => w.id + " " + w.r.toFixed(2) + " | " + w.text.slice(0, 90)), pyqMarkers: marks };
console.log(JSON.stringify(out, null, 1));
fs.writeFileSync(path.join(__dirname, 'originality-last.json'), JSON.stringify(out, null, 1));
process.exit(exactHits || worst[0].r > 0.25 || marks.length ? 1 : 0);
