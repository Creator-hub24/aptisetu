/* Reasoning Lab — sandbox: cube, dice, family tree, seating builder. Everything recomputes live. */
(function (g) {
  'use strict';
  const RL = g.RL, H = RL.H;
  const LABS = [['cube', '🧊 Cube'], ['dice', '🎲 Dice'], ['family', '👪 Family tree'], ['seating', '🪑 Seating']];
  const FACES = ['top', 'bottom', 'front', 'back', 'left', 'right'];
  const out = t => H('div', { cls: 'out', text: t || '' });
  const field = (label, el) => H('label', { cls: 'field' }, [H('span', { text: label }), el]);
  const select = (opts, val, label) => { const s = H('select', { 'aria-label': label || '' }); opts.forEach(([v, t]) => s.appendChild(H('option', { value: String(v), text: t }))); s.value = String(val); return s; };
  // ---------------- cube
  function cubeLab(host) { const st = { dims: [3, 3, 3], paint: { top: 1, bottom: 1, front: 1, back: 1, left: 1, right: 1 }, hl: 2, removeTop: false, only: false };
    const view = H('div', { cls: 'vizbox' }), table = H('div'), msg = out();
    const sliders = ['Length', 'Height', 'Depth'].map((nm, i) => { const r = H('input', { type: 'range', min: '1', max: '8', value: '3', 'aria-label': nm }); const b = H('b', { text: nm + ' 3' }); r.addEventListener('input', () => { st.dims[i] = +r.value; b.textContent = nm + ' ' + r.value; draw(); }); return H('div', { cls: 'row' }, [b, r]); });
    const paints = FACES.map(f => { const c = H('input', { type: 'checkbox', checked: 'checked' }); c.addEventListener('change', () => { st.paint[f] = c.checked ? 1 : 0; draw(); }); return H('label', { cls: 'chk' }, [c, H('span', { text: f })]); });
    const rt = H('input', { type: 'checkbox' }); rt.addEventListener('change', () => { st.removeTop = rt.checked; draw(); });
    const on = H('input', { type: 'checkbox' }); on.addEventListener('change', () => { st.only = on.checked; draw(); });
    function draw() { const paint = {}; FACES.forEach(f => { if (st.paint[f]) paint[f] = 'brand'; }); RL.ui.clear(view);
      view.appendChild(RL.render({ kind: 'cube3d', dims: st.dims.slice(), paint, hl: st.hl === -1 ? null : { faces: st.hl }, removeTop: st.removeTop, explode: st.only && st.hl !== -1 }));
      const { cubes } = RL.cubeClasses(st.dims, paint, st.removeTop); const cnt = [0, 0, 0, 0, 0, 0, 0]; cubes.forEach(u => cnt[u.faces.length]++);
      RL.ui.clear(table); table.appendChild(H('table', { cls: 'tbl' }, [H('thead', null, [H('tr', null, ['Painted faces', '0', '1', '2', '3', '4+', 'Total'].map(t => H('th', { text: t })))]),
        H('tbody', null, [H('tr', null, [H('td', { text: 'Unit cubes' })].concat([0, 1, 2, 3].map(i => H('td', { cls: i === st.hl ? 'hit' : '', text: String(cnt[i]) })), [H('td', { text: String(cnt[4] + cnt[5] + cnt[6]) }), H('td', { text: String(cubes.length) })]))])]));
      const [a, b, c] = st.dims; const all = FACES.every(f => st.paint[f]) && !st.removeTop && a > 1 && b > 1 && c > 1;
      msg.textContent = all ? `Check: corners 8 · edges 4(${a - 2}+${b - 2}+${c - 2}) = ${4 * (a + b + c - 6)} · faces 2(${a - 2}·${b - 2}+${b - 2}·${c - 2}+${a - 2}·${c - 2}) = ${2 * ((a - 2) * (b - 2) + (b - 2) * (c - 2) + (a - 2) * (c - 2))} · inside ${a - 2}·${b - 2}·${c - 2} = ${(a - 2) * (b - 2) * (c - 2)}`
        : 'Unpainted sides or a removed layer change the classes. The table counts every cube directly.'; }
    host.append(H('div', { cls: 'grid g2 lab' }, [H('section', { cls: 'card grid' }, [H('h3', { text: 'Block' })].concat(sliders, [H('h3', { text: 'Painted sides' }), H('div', { cls: 'row wrap' }, paints),
      H('h3', { text: 'Highlight' }), RL.ui.seg([[-1, 'None'], [0, '0'], [1, '1'], [2, '2'], [3, '3']], st.hl, v => { st.hl = v; draw(); }, 'Highlight cubes with this many painted faces'),
      H('div', { cls: 'row wrap' }, [H('label', { cls: 'chk' }, [rt, H('span', { text: 'Remove top layer' })]), H('label', { cls: 'chk' }, [on, H('span', { text: 'Show only highlighted' })])])])),
      H('section', { cls: 'card grid' }, [view, table, msg])])); draw(); }
  // ---------------- dice
  function diceLab(host) { let d = ['1', '6', '2', '5', '3', '4']; const hist = []; const view = H('div', { cls: 'vizbox' }), msg = out(), log = H('ol', { cls: 'log' });
    const ins = FACES.map((f, i) => { const e = H('input', { type: 'text', maxlength: '2', value: d[i], 'aria-label': f + ' face' }); e.addEventListener('input', () => { d[i] = e.value.trim() || '?'; draw(); }); return field(f, e); });
    const sync = () => ins.forEach((l, i) => { l.lastChild.value = d[i]; });
    function draw(roll) { RL.ui.clear(view); view.appendChild(RL.render({ kind: 'die3d', die: d.slice(), roll }));
      const std = d.every(x => /^[1-6]$/.test(x)) && new Set(d).size === 6; const ok = std && +d[0] + +d[1] === 7 && +d[2] + +d[3] === 7 && +d[4] + +d[5] === 7;
      msg.textContent = `Top ${d[0]}, front ${d[2]}, right ${d[5]}. Opposite pairs: ${d[0]}–${d[1]}, ${d[2]}–${d[3]}, ${d[4]}–${d[5]}.` + (std ? ok ? ' This is a standard die (opposites add to 7).' : ' Not a standard die: some opposite pair does not add to 7.' : ''); }
    const roll = dir => () => { d = RL.ROLL[dir](d); sync(); hist.push(dir); const li = H('li', { text: `${dir} → top ${d[0]}, front ${d[2]}` }); log.appendChild(li); if (log.children.length > 8) log.removeChild(log.firstChild); draw(dir); };
    host.append(H('div', { cls: 'grid g2 lab' }, [H('section', { cls: 'card grid' }, [H('h3', { text: 'Faces (type any symbol)' }), H('div', { cls: 'grid g3' }, ins), H('h3', { text: 'Roll' }),
      H('div', { cls: 'row wrap' }, [RL.ui.btn('⬆ Forward', '', roll('forward')), RL.ui.btn('⬇ Back', '', roll('back')), RL.ui.btn('⬅ Left', '', roll('left')), RL.ui.btn('➡ Right', '', roll('right'))]),
      H('div', { cls: 'row wrap' }, [RL.ui.btn('Standard die', 'ghost', () => { d = ['1', '6', '2', '5', '3', '4']; sync(); RL.ui.clear(log); draw(); }), RL.ui.btn('Letters', 'ghost', () => { d = ['A', 'F', 'B', 'E', 'C', 'D']; sync(); RL.ui.clear(log); draw(); })]), log]),
      H('section', { cls: 'card grid' }, [view, msg])])); draw(); }
  // ---------------- family tree
  function familyLab(host) { const B = RL.blood; let facts = [{ a: 'Ravi', rel: 'father', b: 'Asha' }, { a: 'Meena', rel: 'wife', b: 'Ravi' }, { a: 'Kunal', rel: 'brother', b: 'Asha' }, { a: 'Tara', rel: 'daughter', b: 'Kunal' }];
    const view = H('div', { cls: 'vizbox' }), list = H('ul', { cls: 'facts' }), ans = out();
    const A = H('input', { type: 'text', maxlength: '12', placeholder: 'Name', 'aria-label': 'First person' }), Bn = H('input', { type: 'text', maxlength: '12', placeholder: 'Name', 'aria-label': 'Second person' });
    const relSel = select(Object.keys(B.REL).map(r => [r, r]), 'son', 'Relation'); const qa = H('select', { 'aria-label': 'Who' }), qb = H('select', { 'aria-label': 'Relative to' });
    function viz(C, hl) { const people = [...C.P].map(p => ({ id: p, g: C.gen.get(p) || '?' })); const par = []; C.par.forEach((s, c) => s.forEach(p => par.push([p, c]))); const sp = []; C.sp.forEach((b, a) => { if (a < b) sp.push([a, b]); });
      const sib = []; const pl = [...C.P]; for (let i = 0; i < pl.length; i++) for (let j = i + 1; j < pl.length; j++) if (C.sib(pl[i], pl[j]) && !C.par.get(pl[i]).size) sib.push([pl[i], pl[j]]); return { kind: 'family', people, par, sp, sib, hl: hl || [] }; }
    function draw() { RL.ui.clear(list); facts.forEach((f, i) => list.appendChild(H('li', null, [H('span', { text: `${f.a} is the ${f.rel} of ${f.b}.` }), RL.ui.btn('✕', 'ghost sm', () => { facts.splice(i, 1); draw(); }, { 'aria-label': 'Remove fact' })])));
      const C = B.closure(facts); const ppl = [...C.P].sort(); [qa, qb].forEach((s, k) => { const old = s.value; RL.ui.clear(s); ppl.forEach(p => s.appendChild(H('option', { value: p, text: p }))); s.value = ppl.includes(old) ? old : ppl[Math.min(k, ppl.length - 1)] || ''; });
      RL.ui.clear(view); view.appendChild(RL.render(viz(C, [qa.value, qb.value].filter(Boolean)))); ask(C); }
    function ask(C) { C = C || B.closure(facts); const x = qa.value, y = qb.value; if (!x || !y) { ans.textContent = 'Add a fact to start the tree.'; return; } if (x === y) { ans.textContent = 'Pick two different people.'; return; }
      const r = B.relation(C, x, y); const t = [...r.terms], s = [...r.struct]; ans.textContent = t.length ? `${x} is ${y}'s ${t.join(' / ')}.` : s.length ? `${x} is ${y}'s ${s.join(' / ')}, but ${x}'s gender is not known, so a gendered word cannot be decided.` : `No direct relation word links ${x} to ${y} from these facts.`;
      RL.ui.clear(view); view.appendChild(RL.render(viz(C, [x, y]))); }
    qa.addEventListener('change', () => ask()); qb.addEventListener('change', () => ask());
    const add = () => { const a = A.value.trim(), b = Bn.value.trim(); if (!a || !b || a === b) { ans.textContent = 'Type two different names.'; return; } facts.push({ a, rel: relSel.value, b }); A.value = ''; Bn.value = ''; draw(); };
    host.append(H('div', { cls: 'grid g2 lab' }, [H('section', { cls: 'card grid' }, [H('h3', { text: 'Facts' }), list, H('div', { cls: 'row wrap' }, [A, H('span', { text: 'is the' }), relSel, H('span', { text: 'of' }), Bn, RL.ui.btn('Add', 'primary', add)]),
      H('div', { cls: 'row wrap' }, [RL.ui.btn('Clear all', 'ghost', () => { facts = []; draw(); })]), H('h3', { text: 'Ask' }), H('div', { cls: 'row wrap' }, [H('span', { text: 'How is' }), qa, H('span', { text: 'related to' }), qb, H('span', { text: '?' })]), ans]),
      H('section', { cls: 'card grid' }, [view, H('p', { cls: 'small muted', text: 'Squares are male, circles are female, a diamond means gender unknown. Hidden links (a brother\'s child, a spouse\'s parent) are inferred automatically.' })])])); draw(); }
  // ---------------- seating
  const CL = [['left', 'immediately left of'], ['right', 'immediately right of'], ['adj', 'next to'], ['notadj', 'not next to'], ['opp', 'opposite'], ['between', 'has exactly k people between them and'], ['end', 'at an end'], ['first', 'at seat 1 (left end / top)']];
  function perms(n, fix0) { const out = [], a = [...Array(n).keys()]; const rec = k => { if (k === n) { out.push(a.slice()); return; } for (let i = k; i < n; i++) { [a[k], a[i]] = [a[i], a[k]]; rec(k + 1); [a[k], a[i]] = [a[i], a[k]]; } }; if (fix0) { const r = []; const b = [...Array(n - 1).keys()].map(x => x + 1); const rec2 = k => { if (k === b.length) { r.push([0].concat(b)); return; } for (let i = k; i < b.length; i++) { [b[k], b[i]] = [b[i], b[k]]; rec2(k + 1); [b[k], b[i]] = [b[i], b[k]]; } }; rec2(0); return r; } rec(0); return out; }
  // seats[s] = person; linear: lower seat = left (everyone faces north). circle: facing the centre, left = clockwise = seat + 1.
  function test(kind, n, seats, c) { const pos = []; seats.forEach((p, s) => { pos[p] = s; }); const md = x => ((x % n) + n) % n; const a = pos[c.x], b = pos[c.y];
    const dist = kind === 'circle' ? Math.min(md(a - b), md(b - a)) : Math.abs(a - b);
    switch (c.t) { case 'left': return kind === 'circle' ? a === md(b + 1) : a === b - 1; case 'right': return kind === 'circle' ? a === md(b - 1) : a === b + 1; case 'adj': return dist === 1; case 'notadj': return dist !== 1;
      case 'opp': return kind === 'circle' && n % 2 === 0 && md(a - b) === n / 2; case 'between': return kind === 'circle' ? (md(a - b) - 1 === c.k || md(b - a) - 1 === c.k) : dist - 1 === c.k; case 'end': return kind === 'linear' && (a === 0 || a === n - 1); case 'first': return a === 0; } return false; }
  const ctext = (N, c) => c.t === 'end' || c.t === 'first' ? `${N[c.x]} sits ${CL.find(x => x[0] === c.t)[1]}.` : c.t === 'between' ? `Exactly ${c.k} ${c.k === 1 ? 'person sits' : 'people sit'} between ${N[c.x]} and ${N[c.y]}.` : `${N[c.x]} sits ${CL.find(x => x[0] === c.t)[1]} ${N[c.y]}.`;
  function seatingLab(host) { const st = { kind: 'linear', n: 5, clues: [{ t: 'end', x: 0 }, { t: 'left', x: 1, y: 2 }, { t: 'between', x: 0, y: 3, k: 2 }], idx: 0 }; const NM = 'ABCDEFGH'.split('');
    const view = H('div', { cls: 'vizbox' }), list = H('ol', { cls: 'facts' }), msg = out(), nav = H('div', { cls: 'row' });
    const sx = H('select', { 'aria-label': 'Person' }), sy = H('select', { 'aria-label': 'Other person' }), st2 = select(CL, 'left', 'Clue type'), sk = select([[0, '0'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']], 1, 'k');
    const fillPeople = () => { const N = NM.slice(0, st.n); [sx, sy].forEach((s, i) => { RL.ui.clear(s); N.forEach((p, j) => s.appendChild(H('option', { value: String(j), text: p }))); s.value = String(i); }); };
    function draw() { const N = NM.slice(0, st.n); st.clues = st.clues.filter(c => c.x < st.n && (c.y === undefined || c.y < st.n)); RL.ui.clear(list);
      st.clues.forEach((c, i) => list.appendChild(H('li', null, [H('span', { text: ctext(N, c) }), RL.ui.btn('✕', 'ghost sm', () => { st.clues.splice(i, 1); st.idx = 0; draw(); }, { 'aria-label': 'Remove clue' })])));
      const all = perms(st.n, st.kind === 'circle'); const fit = all.filter(s => st.clues.every(c => test(st.kind, st.n, s, c)));
      const fixed = new Array(st.n).fill(null); for (let s = 0; s < st.n; s++) if (fit.length && fit.every(f => f[s] === fit[0][s])) fixed[s] = fit[0][s];
      st.idx = Math.min(st.idx, Math.max(0, fit.length - 1)); const show = fit.length ? fit[st.idx] : fixed; RL.ui.clear(view);
      view.appendChild(RL.render({ kind: 'seating', layout: st.kind, n: st.n, m: 0, names: N, seats: show, count: fit.length, total: all.length, final: fit.length === 1 }));
      msg.textContent = fit.length === 0 ? 'No arrangement fits all the clues. Remove one to see where the conflict is.' : fit.length === 1 ? 'Exactly one arrangement fits: the puzzle is solved.' : `${fit.length} arrangements fit. Seats fixed in all of them: ${fixed.map((p, s) => p === null ? null : `${s + 1}:${N[p]}`).filter(Boolean).join(', ') || 'none yet'}. Add a clue to narrow it down.`;
      RL.ui.clear(nav); if (fit.length > 1) nav.append(RL.ui.btn('◀', 'ghost', () => { st.idx = (st.idx - 1 + fit.length) % fit.length; draw(); }, { 'aria-label': 'Previous arrangement' }), H('span', { cls: 'small muted', text: `Arrangement ${st.idx + 1} of ${fit.length}` }), RL.ui.btn('▶', 'ghost', () => { st.idx = (st.idx + 1) % fit.length; draw(); }, { 'aria-label': 'Next arrangement' })); }
    const add = () => { const c = { t: st2.value, x: +sx.value }; if (!['end', 'first'].includes(c.t)) { c.y = +sy.value; if (c.y === c.x) { msg.textContent = 'Pick two different people.'; return; } } if (c.t === 'between') c.k = +sk.value; st.clues.push(c); st.idx = 0; draw(); };
    const nSel = select([4, 5, 6, 7, 8].map(v => [v, v + ' people']), st.n, 'People'); nSel.addEventListener('change', () => { st.n = +nSel.value; fillPeople(); st.idx = 0; draw(); });
    host.append(H('div', { cls: 'grid g2 lab' }, [H('section', { cls: 'card grid' }, [H('div', { cls: 'row wrap' }, [RL.ui.seg([['linear', 'Row (facing north)'], ['circle', 'Circle (facing centre)']], st.kind, v => { st.kind = v; st.idx = 0; draw(); }, 'Layout'), nSel]),
      H('h3', { text: 'Clues' }), list, H('div', { cls: 'row wrap' }, [sx, st2, sy, field('k', sk), RL.ui.btn('Add clue', 'primary', add)]), H('div', { cls: 'row wrap' }, [RL.ui.btn('Clear clues', 'ghost', () => { st.clues = []; st.idx = 0; draw(); })]),
      H('p', { cls: 'small muted', text: 'Row: left means the lower seat number (everyone faces north). Circle: facing the centre, your left is clockwise, and A is fixed at the top so rotations are not counted twice.' })]),
      H('section', { cls: 'card grid' }, [view, nav, msg])])); fillPeople(); draw(); }
  const M = { cube: cubeLab, dice: diceLab, family: familyLab, seating: seatingLab };
  const FOR = { cube: 'cube', dice: 'dice', folding: 'dice', blood: 'family', seating: 'seating', puzzles: 'seating' };
  RL.lab = { page(main, which) { which = Object.prototype.hasOwnProperty.call(M, which) ? which : 'cube'; const body = H('div'); main.append(RL.ui.seg(LABS, which, v => { if (RL.go) RL.go('lab/' + v); else location.hash = '#/lab/' + v; }, 'Choose a sandbox'), body); M[which](body); },
    forTopic: k => (Object.prototype.hasOwnProperty.call(FOR, k) && FOR[k]) || null, mount(id, host) { if (Object.prototype.hasOwnProperty.call(M, id)) M[id](host); }, _test: test, _perms: perms };
})(typeof globalThis !== 'undefined' ? globalThis : this);
