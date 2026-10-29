/* Reasoning Lab (AptiSetu site build) — mounts in a shadow root on #rl-app so its styles never touch the site's.
   One file serves six pages; each page says which view it is via data-page. Hash parts are validated against the topic/level/lab tables. */
(function (g) {
  'use strict';
  const RL = g.RL, H = RL.H, KEY = 'aptisetu.reasoninglab.v1';
  // ---------- storage (localStorage only; no cookies, no network)
  const store = { d: {}, load() { try { this.d = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { this.d = {}; } this.d.stats = this.d.stats || {}; this.d.sessions = this.d.sessions || []; return this; },
    save() { try { localStorage.setItem(KEY, JSON.stringify(this.d)); } catch (e) { /* quota or blocked */ } } }.load();
  RL.store = store;
  const record = (p, ok) => { const s = store.d.stats[p.typeId] || (store.d.stats[p.typeId] = { a: 0, c: 0 }); s.a++; if (ok) s.c++; store.save(); };
  const exam = () => store.d.exam || 'all';
  const typesOf = (topic, level) => RL.byExam(level ? RL.TOPICS[topic].types[level] : RL.LEVELS.flatMap(l => RL.TOPICS[topic].types[l]), exam());
  const topicsForExam = () => RL.ORDER.filter(k => typesOf(k).length);
  const own = (o, k) => typeof k === 'string' && /^[a-z0-9-]{1,24}$/.test(k) && Object.prototype.hasOwnProperty.call(o, k);
  const hostEl = document.getElementById('rl-app'); if (!hostEl || !hostEl.attachShadow) return;
  const PAGES = { overview: 'reasoning-lab.html', learn: 'reasoning-lab-learn.html', practice: 'reasoning-lab-practice.html', lab: 'reasoning-lab-lab.html', timed: 'reasoning-lab-timed.html', progress: 'reasoning-lab-progress.html' };
  const PAGE = own(PAGES, hostEl.getAttribute('data-page')) ? hostEl.getAttribute('data-page') : 'overview';
  const shadow = hostEl.attachShadow({ mode: 'open' }); RL.cssRoot = hostEl;
  shadow.appendChild(H('link', { rel: 'stylesheet', href: 'assets/css/reasoning-lab.css' }));
  const tbar = H('div', { cls: 'tbar' }); const main = H('div', { cls: 'main', tabindex: '-1' }); shadow.append(tbar, main);
  while (hostEl.firstChild) hostEl.removeChild(hostEl.firstChild); // drop the noscript/loading text once the app is live
  /* internal route -> page URL (+ hash). Everything else in the app navigates through RL.go / RL.href. */
  function href(r) { const h = String(r || '').replace(/^#?\/?/, '').split('/');
    if (h[0] === 't' && own(RL.TOPICS, h[1])) { if (h[2] === 'practice') return PAGES.practice + '#' + h[1] + (RL.LEVELS.includes(h[3]) ? '/' + h[3] : ''); if (h[2] === 'lab') return PAGES.lab + '#' + ((RL.lab && RL.lab.forTopic(h[1])) || 'cube'); return PAGES.learn + '#' + h[1]; }
    if (h[0] === 'lab') return PAGES.lab + (h[1] && /^[a-z]{1,12}$/.test(h[1]) ? '#' + h[1] : '');
    if (h[0] === 'timed' || h[0] === 'progress') return PAGES[h[0]]; if (h[0] === 'learn' || h[0] === 'practice') return PAGES[h[0]];
    return PAGES.overview; }
  function go(r) { const u = href(r), i = u.indexOf('#'), file = i < 0 ? u : u.slice(0, i), hash = i < 0 ? '' : u.slice(i);
    if (file === PAGES[PAGE]) { if (hash && hash !== location.hash) location.hash = hash; else { route(); top(); } } else location.href = u; }
  const link = (r, text, cls, attrs) => H('a', Object.assign({ href: href(r), cls: cls || '', text }, attrs || {}));
  RL.href = href; RL.go = go;
  const clear = el => { while (el.firstChild) el.removeChild(el.firstChild); return el; };
  const LV = { easy: 'Easy', medium: 'Medium', hard: 'Hard' };
  const btn = (text, cls, on, attrs) => { const b = H('button', Object.assign({ type: 'button', cls: 'btn ' + (cls || ''), text }, attrs || {})); if (on) b.addEventListener('click', on); return b; };
  function seg(items, cur, on, label) { const s = H('div', { cls: 'seg', role: 'group', 'aria-label': label || '' }); items.forEach(([v, t]) => { const b = H('button', { type: 'button', 'aria-pressed': String(v === cur), text: t }); b.addEventListener('click', () => { [...s.children].forEach(x => x.setAttribute('aria-pressed', 'false')); b.setAttribute('aria-pressed', 'true'); on(v); }); s.appendChild(b); }); return s; }
  RL.ui = { btn, seg, clear, store, link };

  // ---------- in-app toolbar (exam filter + motion). Theme comes from the site's own toggle (html[data-theme] + 'themechange').
  const examSel = H('select', { id: 'rl-exam' });
  [['all', 'All exams']].concat(Object.entries(RL.EXAMS)).forEach(([k, v]) => examSel.appendChild(H('option', { value: k, text: v })));
  examSel.value = own(RL.EXAMS, exam()) ? exam() : 'all'; examSel.addEventListener('change', () => { store.d.exam = own(RL.EXAMS, examSel.value) ? examSel.value : 'all'; store.save(); route(); });
  const motionBtn = btn('Reduce motion', 'ghost sm', () => { store.d.reduce = !store.d.reduce; store.save(); syncMotion(); route(); });
  const syncMotion = () => { RL.motionOff = !!store.d.reduce; hostEl.classList.toggle('reduce', RL.motionOff); motionBtn.setAttribute('aria-pressed', String(RL.motionOff)); };
  const syncTheme = () => { hostEl.classList.toggle('dark', document.documentElement.getAttribute('data-theme') === 'dark'); if (RL.redrawAll) RL.redrawAll(); };
  document.addEventListener('themechange', syncTheme); syncTheme(); syncMotion();
  tbar.append(H('label', { cls: 'chk', for: 'rl-exam' }, [H('span', { cls: 'small muted', text: 'Exam' })]), examSel, H('span', { cls: 'grow' }), motionBtn);

  // ---------- question card (shared by topic practice and timed mode)
  function qBlock(p) { const box = H('div', { cls: 'grid' });
    const tags = H('div', { cls: 'row' }, [H('span', { cls: 'chip ' + p.level, text: LV[p.level] }), H('span', { cls: 'chip', text: p.typeName })].concat(p.exams.map(e => H('span', { cls: 'chip', text: RL.EXAMS[e].split(' ')[0] }))));
    box.appendChild(tags); box.appendChild(H('div', { cls: 'qtext', text: p.question }));
    if (p.clues && p.clues.length) box.appendChild(H('ol', { cls: 'clues' }, p.clues.map(c => H('li', { text: c }))));
    if (p.ask && p.question.indexOf(p.ask) < 0) box.appendChild(H('div', { cls: 'ask', text: p.ask }));
    if (p.viz) { const vb = H('div', { cls: 'vizbox' }); vb.appendChild(RL.render(p.viz)); box.appendChild(vb); }
    return box; }
  function optionsBlock(p, onAnswer) { const wrap = H('div', { cls: 'opts', role: 'group', 'aria-label': 'Options' }); const btns = p.options.map((o, i) => { const b = H('button', { type: 'button', cls: 'opt', 'aria-label': `Option ${i + 1}${o.label ? ': ' + o.label : ''}` }, [H('span', { cls: 'k', text: String.fromCharCode(65 + i) })]);
      const ov = H('span', { cls: 'ov' }); if (o.viz) ov.appendChild(RL.render(Object.assign({ small: true }, o.viz), { small: true, static: true })); if (o.label) ov.appendChild(H('span', { text: o.label })); b.appendChild(ov);
      b.addEventListener('click', () => onAnswer(i)); wrap.appendChild(b); return b; });
    const mark = chosen => { btns.forEach((b, i) => { b.disabled = true; if (i === p.answerIndex) b.classList.add('ok'); else if (i === chosen) b.classList.add('bad'); }); };
    return { el: wrap, mark, btns }; }
  function stepper(p) { const box = H('div', { cls: 'solve fade-in' }); const list = H('ol', { cls: 'steplist' }); const vb = H('div', { cls: 'vizbox' }); const ctl = H('div', { cls: 'row' }); let k = 0, timer = 0;
    const steps = p.steps.length ? p.steps : [{ text: 'Answer: ' + (p.options[p.answerIndex].label || String.fromCharCode(65 + p.answerIndex)) }];
    const lastViz = i => { for (let j = i; j >= 0; j--) if (steps[j].viz) return steps[j].viz; return p.viz; };
    const show = i => { k = Math.max(0, Math.min(steps.length - 1, i)); [...list.children].forEach((li, j) => { li.className = j === k ? 'on' : j < k ? 'done' : ''; li.setAttribute('aria-current', j === k ? 'step' : 'false'); }); clear(vb); const v = lastViz(k); if (v) vb.appendChild(RL.render(v)); prev.disabled = k === 0; next.disabled = k === steps.length - 1; cnt.textContent = `Step ${k + 1} / ${steps.length}`; };
    steps.forEach((s, i) => { const li = H('li', { tabindex: '0', text: s.text }); li.addEventListener('click', () => { stop(); show(i); }); li.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); stop(); show(i); } }); list.appendChild(li); });
    const prev = btn('◀ Prev', 'ghost', () => { stop(); show(k - 1); }), next = btn('Next ▶', 'primary', () => { stop(); show(k + 1); }); const cnt = H('span', { cls: 'small muted' });
    const stop = () => { clearInterval(timer); timer = 0; play.textContent = '▶ Auto-play'; };
    const play = btn('▶ Auto-play', 'ghost', () => { if (timer) return stop(); if (k === steps.length - 1) show(0); play.textContent = '⏸ Pause'; timer = setInterval(() => { if (!box.isConnected || k >= steps.length - 1) return stop(); show(k + 1); }, RL.reduced() ? 4000 : 2600); });
    ctl.append(prev, next, play, cnt); const left = H('div', { cls: 'grid' }, [H('h3', { text: 'Step-by-step solution' }), list, ctl]);
    if (p.traps && p.traps.length) left.appendChild(H('div', { cls: 'traps' }, [H('b', { text: '⚠ Traps to avoid' }), H('ul', null, p.traps.map(t => H('li', { text: t })))]));
    box.append(left, vb); show(0); box.keyNav = e => { if (e.key === 'ArrowRight') { stop(); show(k + 1); } if (e.key === 'ArrowLeft') { stop(); show(k - 1); } }; return box; }
  RL.ui.qBlock = qBlock; RL.ui.stepper = stepper;

  // ---------- generator panel (topic → Practice tab)
  function generator(topic, host, initLevel) { let level = initLevel || 'easy', typeId = '', cur = null, sol = null;
    const ctl = H('div', { cls: 'row' }); const sel = H('select', { 'aria-label': 'Question type' }); const area = H('div', { cls: 'grid' });
    const fillTypes = () => { clear(sel); sel.appendChild(H('option', { value: '', text: 'Any type' })); typesOf(topic, level).forEach(t => sel.appendChild(H('option', { value: t.id, text: t.name }))); sel.value = typeId && [...sel.options].some(o => o.value === typeId) ? typeId : ''; typeId = sel.value; };
    const levelSeg = seg(RL.LEVELS.map(l => [l, LV[l]]), level, l => { level = l; fillTypes(); fresh(); }, 'Level');
    sel.addEventListener('change', () => { typeId = sel.value; fresh(); });
    ctl.append(levelSeg, sel, btn('New question ↻', 'primary', () => fresh()));
    function fresh() { clear(area); const list = typesOf(topic, level); if (!list.length) { area.appendChild(H('div', { cls: 'card empty', text: `No ${LV[level].toLowerCase()} types for this exam filter. Try another level or “All exams”.` })); return; }
      const t = typeId ? RL.TYPES[typeId] : list[Math.floor(Math.random() * list.length)]; let p; try { p = RL.generate(topic, level, t.id); } catch (e) { area.appendChild(H('div', { cls: 'card empty', text: 'Could not build a question, press New question.' })); return; }
      cur = p; sol = null; const card = H('section', { cls: 'card grid', 'aria-live': 'polite' }); card.appendChild(qBlock(p)); const verdict = H('div'); const solHost = H('div');
      const ob = optionsBlock(p, i => { if (sol) return; const ok = i === p.answerIndex; ob.mark(i); record(p, ok); verdict.className = 'verdict ' + (ok ? 'ok' : 'bad'); verdict.textContent = ok ? '✓ Correct!' : `✗ Not quite. The answer is ${String.fromCharCode(65 + p.answerIndex)}${p.options[p.answerIndex].label ? ' (' + p.options[p.answerIndex].label + ')' : ''}.`; reveal(); });
      const reveal = () => { if (sol) return; sol = stepper(p); solHost.appendChild(sol); showBtn.disabled = true; };
      const showBtn = btn('Show solution', 'ghost', () => { ob.mark(-1); reveal(); });
      card.append(ob.el, H('div', { cls: 'row' }, [verdict, H('span', { cls: 'grow' }), showBtn, btn('Next question →', '', () => fresh())]), solHost); area.appendChild(card); }
    host.append(ctl, area); fillTypes(); fresh();
    return { key: e => { if (!cur) return; if (/^[1-5a-eA-E]$/.test(e.key) && !sol) { const i = /\d/.test(e.key) ? +e.key - 1 : e.key.toLowerCase().charCodeAt(0) - 97; const b = area.querySelectorAll('.opt')[i]; if (b) b.click(); } else if (e.key === 'n' || e.key === 'N') fresh(); else if (sol && sol.keyNav) sol.keyNav(e); } }; }

  // ---------- pages
  let keyHandler = null; document.addEventListener('keydown', e => { if (e.ctrlKey || e.metaKey || e.altKey) return; const t = (e.composedPath && e.composedPath()[0]) || e.target; if (t && (/INPUT|SELECT|TEXTAREA/.test(t.tagName) || t.isContentEditable)) return; if (!t || (t !== document.body && !hostEl.contains(t) && !shadow.contains(t))) return; if (keyHandler) keyHandler(e); });
  function home() {
    const tops = topicsForExam(); const nTypes = tops.reduce((s, k) => s + typesOf(k).length, 0);
    const hero = H('section', { cls: 'hero' }); const left = H('div');
    left.append(H('span', { cls: 'chip', text: exam() === 'all' ? 'CAT · SSC · Banking · Govt · CUET' : RL.EXAMS[exam()] }), H('h2', { cls: 'h-hero', text: 'See the logic. Then solve it.' }),
      H('p', { cls: 'muted', text: 'Rotate cubes and dice in 3D, fold nets and paper, watch seating clues knock out arrangements one by one, and practise with endless fresh questions at three levels, each with a step-by-step visual solution and the traps examiners love.' }),
      H('div', { cls: 'stats' }, [H('div', { cls: 'stat' }, [H('b', { text: String(tops.length) }), 'topics']), H('div', { cls: 'stat' }, [H('b', { text: String(nTypes) }), 'question types']), H('div', { cls: 'stat' }, [H('b', { text: '∞' }), 'fresh questions'])]),
      H('div', { cls: 'row' }, [link('timed', 'Start timed practice', 'btn primary'), link('lab', 'Open the Lab', 'btn')]));
    const stage = H('div', { cls: 'card stage grid g2' }); stage.appendChild(RL.render({ kind: 'cube3d', dims: [4, 4, 4], paint: { top: 'brand', bottom: 'brand', front: 'brand', back: 'brand', left: 'brand', right: 'brand' }, hl: { faces: 2 } }));
    stage.appendChild(RL.render({ kind: 'die3d', die: ['1', '6', '2', '5', '3', '4'], spin: true })); hero.append(left, stage); main.appendChild(hero); topicGrid('learn'); }
  function topicGrid(cards) { const tops = topicsForExam();
    RL.SECTIONS.forEach(sec => { const ks = sec.topics.filter(k => tops.includes(k)); if (!ks.length) return; main.appendChild(H('h3', { cls: 'section-title', text: sec.name })); const gr = H('div', { cls: 'grid g3' });
      ks.forEach(k => { const T = RL.TOPICS[k]; const st = typesOf(k).map(t => store.d.stats[t.id]).filter(Boolean); const a = st.reduce((s, x) => s + x.a, 0), c = st.reduce((s, x) => s + x.c, 0);
        const card = H('a', { href: href(cards === 'practice' ? 't/' + k + '/practice' : 't/' + k), cls: 'card topic' }, [H('span', { cls: 'ic', 'aria-hidden': 'true', text: T.icon }), H('h4', { text: T.name }), H('span', { cls: 'small muted', text: T.blurb }),
          H('span', { cls: 'meta' }, RL.LEVELS.map(l => H('span', { cls: 'chip ' + l, text: `${LV[l]} ${typesOf(k, l).length}` })).concat(a ? [H('span', { cls: 'chip', text: `${Math.round(100 * c / a)}% of ${a}` })] : []))]);
        gr.appendChild(card); }); main.appendChild(gr); });
  }
  function chooser(kind) { main.appendChild(H('h2', { text: kind === 'practice' ? 'Pick a topic to practise' : 'Pick a topic to learn' }));
    main.appendChild(H('p', { cls: 'muted', text: kind === 'practice' ? 'Every topic has Easy, Medium and Hard question types, each with a step-by-step visual solution.' : 'Each explainer has the key ideas, the shortcuts and a worked example you can step through.' })); topicGrid(kind); }
  function topicPage(k, tab, level) { if (!own(RL.TOPICS, k)) return chooser(tab); const T = RL.TOPICS[k]; tab = tab || 'learn';
    main.appendChild(H('div', { cls: 'row' }, [link(tab === 'practice' ? 'practice' : 'learn', '← All topics', 'btn ghost'), H('span', { cls: 'chip', text: T.section })]));
    main.appendChild(H('h2', { cls: 'h-topic' }, [T.icon + ' ' + T.name])); main.appendChild(H('p', { cls: 'muted', text: T.blurb }));
    const tabs = H('nav', { cls: 'tabs', 'aria-label': T.name + ' views' }); const body = H('div'); const items = [['learn', 'Learn (visual explainer)'], ['practice', 'Generator & solutions']]; if (RL.lab && RL.lab.forTopic(k)) items.push(['lab', 'Try it in the Lab']);
    items.forEach(([id, txt]) => { tabs.appendChild(link(`t/${k}/${id}`, txt, '', id === tab ? { 'aria-current': 'page' } : null)); });
    main.append(tabs, body); keyHandler = null;
    if (tab === 'practice') { if (!typesOf(k).length) { body.appendChild(H('div', { cls: 'card empty', text: 'This topic has no question types for the selected exam. Choose “All exams” in the header.' })); return; } const gen = generator(k, body, level); keyHandler = gen.key; }
    else if (tab === 'lab' && RL.lab) { RL.lab.mount(RL.lab.forTopic(k), body); }
    else { (RL.explain ? RL.explain(k, body) : body.appendChild(H('p', { text: 'Explainer loading…' }))); body.appendChild(H('div', { cls: 'row' }, [link(`t/${k}/practice`, 'Practise this topic →', 'btn primary')])); }
  }
  // ---------- timed practice
  const SECS = { easy: 45, medium: 75, hard: 110 };
  function timed() { const cfg = store.d.timedCfg || (store.d.timedCfg = { level: 'easy', n: 10, topics: [] }); const tops = topicsForExam(); cfg.topics = cfg.topics.filter(k => tops.includes(k));
    main.appendChild(H('h2', { text: '⏱ Set up a timed round' })); main.appendChild(H('p', { cls: 'muted', text: `Mixed questions from the topics you pick, filtered for ${own(RL.EXAMS, exam()) ? RL.EXAMS[exam()] : 'all exams'}. Time per question: Easy ${SECS.easy}s, Medium ${SECS.medium}s, Hard ${SECS.hard}s. Scores are saved on this device only.` }));
    const card = H('section', { cls: 'card grid' }); const chips = H('div', { cls: 'row' });
    const draw = () => { clear(chips); tops.forEach(k => { const on = !cfg.topics.length || cfg.topics.includes(k); const c = H('button', { type: 'button', cls: 'pill' + (cfg.topics.includes(k) ? ' sel' : ''), 'aria-pressed': String(cfg.topics.includes(k)), text: RL.TOPICS[k].icon + ' ' + RL.TOPICS[k].name }); void on; c.addEventListener('click', () => { const i = cfg.topics.indexOf(k); if (i >= 0) cfg.topics.splice(i, 1); else cfg.topics.push(k); store.save(); draw(); }); chips.appendChild(c); }); };
    draw(); card.append(H('h3', { text: 'Topics (none selected = all)' }), chips, H('div', { cls: 'row' }, [seg(RL.LEVELS.map(l => [l, LV[l]]).concat([['mixed', 'Mixed']]), cfg.level, v => { cfg.level = v; store.save(); }, 'Level'), seg([[5, '5'], [10, '10'], [15, '15'], [20, '20']], cfg.n, v => { cfg.n = v; store.save(); }, 'Questions'), btn('Start ▶', 'primary', () => run(cfg))]));
    main.appendChild(card); const hist = store.d.sessions.slice(-5).reverse(); if (hist.length) { main.appendChild(H('h3', { cls: 'section-title', text: 'Recent sessions' })); main.appendChild(sessTable(hist)); } }
  function sessTable(rows) { return H('div', { cls: 'card' }, [H('table', { cls: 'tbl' }, [H('thead', null, [H('tr', null, ['When', 'Exam', 'Level', 'Score', 'Time'].map(t => H('th', { text: t })))]), H('tbody', null, rows.map(s => H('tr', null, [new Date(s.at).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' }), s.exam === 'all' ? 'All' : (RL.EXAMS[s.exam] || s.exam).split(' ')[0], LV[s.level] || 'Mixed', `${s.score}/${s.total} (${Math.round(100 * s.score / s.total)}%)`, fmt(s.secs)].map(t => H('td', { text: t })))))])]); }
  const fmt = s => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;
  function run(cfg) { const tops = cfg.topics.length ? cfg.topics : topicsForExam(); const qs = []; let guard = 0;
    while (qs.length < cfg.n && guard++ < cfg.n * 20) { const k = tops[Math.floor(Math.random() * tops.length)]; const lv = cfg.level === 'mixed' ? RL.LEVELS[Math.floor(Math.random() * 3)] : cfg.level; const ts = typesOf(k, lv); if (!ts.length) continue; const t = ts[Math.floor(Math.random() * ts.length)]; try { qs.push(RL.generate(k, lv, t.id)); } catch (e) { /* retry */ } }
    if (!qs.length) { alertCard('No questions match these settings.'); return; }
    const total = qs.reduce((s, p) => s + SECS[p.level], 0); let i = 0, left = total; const ans = []; const t0 = Date.now(); clear(main); keyHandler = null;
    const top = H('div', { cls: 'card grid' }); const timer = H('span', { cls: 'timer' }); const bar = H('div', { cls: 'bar' }, [H('i')]); const prog = H('span', { cls: 'small muted' });
    top.append(H('div', { cls: 'row' }, [H('b', { text: '⏱ Timed practice' }), H('span', { cls: 'grow' }), prog, timer]), bar); const host = H('div', { cls: 'grid' }); main.append(top, host);
    const tick = () => { left = total - (Date.now() - t0) / 1000; if (!top.isConnected) return clearInterval(iv); timer.textContent = fmt(Math.max(0, left)); bar.firstChild.style.width = (100 * Math.max(0, left) / total).toFixed(1) + '%'; bar.classList.toggle('warn', left < total * 0.15); if (left <= 0) { clearInterval(iv); finish(); } };
    const iv = setInterval(tick, 250); tick();
    const show = () => { clear(host); prog.textContent = `Question ${i + 1} of ${qs.length}`; const p = qs[i]; const card = H('section', { cls: 'card grid' }); card.appendChild(qBlock(p));
      const ob = optionsBlock(p, k => { ans[i] = k; record(p, k === p.answerIndex); next(); }); card.append(ob.el, H('div', { cls: 'row' }, [btn('Skip →', 'ghost', () => { ans[i] = -1; next(); }), btn('Finish now', 'ghost', () => { clearInterval(iv); finish(); })])); host.appendChild(card);
      keyHandler = e => { if (/^[1-5a-eA-E]$/.test(e.key)) { const j = /\d/.test(e.key) ? +e.key - 1 : e.key.toLowerCase().charCodeAt(0) - 97; if (ob.btns[j]) ob.btns[j].click(); } }; };
    const next = () => { i++; if (i >= qs.length) { clearInterval(iv); finish(); } else show(); };
    let done = false; const finish = () => { if (done) return; done = true; keyHandler = null; const secs = Math.min(total, (Date.now() - t0) / 1000); const score = qs.filter((p, j) => ans[j] === p.answerIndex).length;
      store.d.sessions.push({ at: Date.now(), exam: exam(), level: cfg.level, score, total: qs.length, secs: Math.round(secs) }); store.d.sessions = store.d.sessions.slice(-100); store.save();
      clear(host); top.querySelector('.row').lastChild.textContent = 'Done'; const best = Math.max(...store.d.sessions.map(s => s.score / s.total));
      host.appendChild(H('section', { cls: 'card grid' }, [H('h2', { text: `Score ${score} / ${qs.length}` }), H('p', { cls: 'muted', text: `Accuracy ${Math.round(100 * score / qs.length)}% · time ${fmt(secs)} · personal best ${Math.round(100 * best)}%` }), H('div', { cls: 'row' }, [btn('Practise again', 'primary', () => run(cfg)), btn('Change settings', '', () => route())])]));
      qs.forEach((p, j) => { const ok = ans[j] === p.answerIndex; const d = H('details', { cls: 'card' }); d.appendChild(H('summary', null, [H('b', { text: `${j + 1}. ${ok ? '✓' : ans[j] === undefined || ans[j] === -1 ? '–' : '✗'} ` }), `${RL.TOPICS[p.topic].name} · ${p.typeName}`])); let filled = false; d.addEventListener('toggle', () => { if (!d.open || filled) return; filled = true; d.append(qBlock(p), H('p', { cls: 'verdict ' + (ok ? 'ok' : 'bad'), text: `Answer: ${String.fromCharCode(65 + p.answerIndex)}${p.options[p.answerIndex].label ? ' (' + p.options[p.answerIndex].label + ')' : ''}${ans[j] >= 0 && !ok ? ` · you chose ${String.fromCharCode(65 + ans[j])}` : ''}` }), stepper(p)); }); host.appendChild(d); }); };
    show(); }
  function alertCard(t) { main.appendChild(H('div', { cls: 'card empty', text: t })); }
  function progress() { main.appendChild(H('h2', { text: '📈 Your accuracy by topic' })); main.appendChild(H('p', { cls: 'muted', text: 'Stored only in this browser (localStorage). Nothing leaves your device.' }));
    const rows = RL.ORDER.map(k => { const ts = RL.LEVELS.flatMap(l => RL.TOPICS[k].types[l]); const st = ts.map(t => store.d.stats[t.id]).filter(Boolean); const a = st.reduce((s, x) => s + x.a, 0), c = st.reduce((s, x) => s + x.c, 0); return { k, a, c }; });
    const tb = H('table', { cls: 'tbl' }, [H('thead', null, [H('tr', null, ['Topic', 'Attempted', 'Correct', 'Accuracy', ''].map(t => H('th', { text: t })))]), H('tbody', null, rows.map(r => { const bar = H('div', { cls: 'bar' }, [H('i')]); bar.firstChild.style.width = (r.a ? 100 * r.c / r.a : 0) + '%'; return H('tr', null, [H('td', { text: RL.TOPICS[r.k].icon + ' ' + RL.TOPICS[r.k].name }), H('td', { text: String(r.a) }), H('td', { text: String(r.c) }), H('td', { text: r.a ? Math.round(100 * r.c / r.a) + '%' : '—' }), H('td', null, [bar])]); }))]);
    main.appendChild(H('div', { cls: 'card' }, [tb])); if (store.d.sessions.length) { main.appendChild(H('h3', { cls: 'section-title', text: 'Timed sessions' })); main.appendChild(sessTable(store.d.sessions.slice().reverse().slice(0, 20))); }
    main.appendChild(H('div', { cls: 'row' }, [btn('Reset all progress', 'ghost', () => { if (g.confirm('Delete all saved scores on this device?')) { store.d.stats = {}; store.d.sessions = []; store.save(); route(); } })])); }
  function lab(which) { main.appendChild(H('h2', { text: '🧪 Lab sandbox' })); main.appendChild(H('p', { cls: 'muted', text: 'Build your own cubes, dice, family trees and seating plans. Everything updates live.' })); if (RL.lab) RL.lab.page(main, which); }
  // ---------- router: the page decides the view; the hash only picks a topic / level / sandbox, and is validated first.
  const BASE_TITLE = document.title;
  function parts() { let h = location.hash.replace(/^#\/?/, '').slice(0, 80); try { h = decodeURIComponent(h); } catch (e) { h = ''; } return h.split('/').slice(0, 3); }
  function route() { clear(main); keyHandler = null; const h = parts(); let title = BASE_TITLE;
    if (PAGE === 'learn' || PAGE === 'practice') { const k = own(RL.TOPICS, h[0]) ? h[0] : ''; const lv = RL.LEVELS.includes(h[1]) ? h[1] : undefined; topicPage(k, PAGE, lv); if (k) title = RL.TOPICS[k].name + ' · ' + BASE_TITLE; }
    else if (PAGE === 'lab') lab(own({ cube: 1, dice: 1, family: 1, seating: 1 }, h[0]) ? h[0] : 'cube');
    else if (PAGE === 'timed') timed(); else if (PAGE === 'progress') progress(); else home();
    document.title = title; }
  const top = () => { const hd = document.getElementById('site-header'), off = (hd ? Math.max(0, hd.getBoundingClientRect().bottom) : 0) + 8; // clear the sticky site header
    const y = hostEl.getBoundingClientRect().top + g.scrollY - off; if (g.scrollY > y) g.scrollTo(0, Math.max(0, y)); main.focus({ preventScroll: true }); };
  g.addEventListener('hashchange', () => { route(); top(); });
  route();
})(typeof globalThis !== 'undefined' ? globalThis : this);
