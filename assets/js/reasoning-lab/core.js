/* Reasoning Lab — core: RNG helpers, type registry, MCQ builder. Works in the browser and in Node. */
(function (g) {
  'use strict';
  const RL = g.RL || (g.RL = {});
  const R = Math.random;
  const ri = (a, b) => a + Math.floor(R() * (b - a + 1));
  const pick = a => a[Math.floor(R() * a.length)];
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(R() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const sample = (a, k) => shuffle(a).slice(0, k);
  const range = (a, b) => { const r = []; for (let i = a; i <= b; i++) r.push(i); return r; };
  function perms(arr) { const out = []; const a = arr.slice(); const c = new Array(a.length).fill(0); out.push(a.slice()); let i = 0;
    while (i < a.length) { if (c[i] < i) { const k = i % 2 ? c[i] : 0; [a[k], a[i]] = [a[i], a[k]]; out.push(a.slice()); c[i]++; i = 0; } else { c[i] = 0; i++; } } return out; }
  RL.u = { ri, pick, shuffle, sample, range, perms };

  RL.EXAMS = { cat: 'CAT', ssc: 'SSC CGL/CHSL', bank: 'Banking (IBPS/SBI)', govt: 'Other Govt', cuet: 'CUET GT' };
  RL.LEVELS = ['easy', 'medium', 'hard'];
  RL.TOPICS = {}; RL.TYPES = {}; RL.ORDER = [];
  RL.SECTIONS = [];
  RL.topic = function (key, name, icon, blurb, section) { RL.TOPICS[key] = { key, name, icon, blurb, section, types: { easy: [], medium: [], hard: [] } }; RL.ORDER.push(key);
    let s = RL.SECTIONS.find(x => x.name === section); if (!s) RL.SECTIONS.push(s = { name: section, topics: [] }); s.topics.push(key); };
  RL.reg = function (topic, level, id, name, exams, fn) { const t = { id, topic, level, name, exams, fn }; RL.TOPICS[topic].types[level].push(t); RL.TYPES[id] = t; };
  RL.listTypes = () => RL.ORDER.flatMap(k => RL.LEVELS.flatMap(l => RL.TOPICS[k].types[l]));

  /* options: correct label + distractor labels (strings) or {label, viz} objects. Deduped, shuffled. */
  RL.mcq = function (correct, distractors, n) {
    n = n || 4; const norm = o => typeof o === 'string' ? { label: o } : o; const key = o => o.key || o.label;
    const c = norm(correct); const seen = new Set([key(c)]); const ds = [];
    for (const d0 of distractors) { const d = norm(d0); if (d.label === undefined || d.label === null) continue; const k = key(d); if (seen.has(k)) continue; seen.add(k); ds.push(d); if (ds.length === n - 1) break; }
    if (ds.length < n - 1) throw new Error('not enough distractors');
    const opts = shuffle([c, ...ds]); return { options: opts, answerIndex: opts.indexOf(c) };
  };
  /* fixed option list (banking style) — order kept */
  RL.fixed = function (labels, correctLabel) { const i = labels.indexOf(correctLabel); if (i < 0) throw new Error('bad fixed'); return { options: labels.map(l => ({ label: l })), answerIndex: i }; };
  RL.numDistract = function (ans, spread, extra) { const s = new Set(); (extra || []).forEach(v => { if (Number.isFinite(v) && v !== ans && v >= 0) s.add(v); });
    let guard = 0; while (s.size < 8 && guard++ < 200) { const v = ans + ri(-spread, spread); if (v !== ans && v >= 0) s.add(v); } return [...s].map(String); };

  RL.generate = function (topic, level, typeId) {
    const T = RL.TOPICS[topic]; if (!T) throw new Error('topic ' + topic);
    const list = T.types[level] || T.types.easy; const t = (typeId && RL.TYPES[typeId] && RL.TYPES[typeId].topic === topic) ? RL.TYPES[typeId] : pick(list);
    for (let tries = 0; tries < 300; tries++) {
      try { const p = t.fn(); if (!p) continue; return Object.assign({ topic, level: t.level, typeId: t.id, typeName: t.name, exams: t.exams, clues: [], steps: [], traps: [] }, p); }
      catch (e) { if (tries === 299) throw e; }
    }
    throw new Error('Could not generate ' + t.id);
  };
  RL.byExam = (types, ex) => ex && ex !== 'all' ? types.filter(t => t.exams.includes(ex)) : types;
  if (typeof module !== 'undefined' && module.exports) module.exports = RL;
})(typeof globalThis !== 'undefined' ? globalThis : this);
