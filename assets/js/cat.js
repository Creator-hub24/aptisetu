// edumaths360 CAT engine: sectional tests (40 min, CAT marking) and untimed topic practice.
(function () {
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const L = "ABCD", SECTION_TIME = 40 * 60;
  const TARGET = { varc: 24, dilr: 22, qa: 22 };
  let bank, mode, sec, qs = [], cur = 0, resp = [], marked = [], visited = [], tspent = [], checked = [], timeLeft = 0, timerId = null, shownAt = 0, elapsed = 0;

  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const fmt = s => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const val = (name) => (document.querySelector(`input[name=${name}]:checked`) || {}).value;

  // ---------- question selection ----------
  function groups(list) { // keep set questions together, in bank order
    const g = new Map(); list.forEach(q => { const k = q.set || q.id; if (!g.has(k)) g.set(k, []); g.get(k).push(q); }); return [...g.values()];
  }
  function pickSectional(s) {
    const all = bank.sections[s].questions, tgt = TARGET[s];
    if (s === "qa") {
      const t = shuffle(all.filter(q => q.type === "tita")).slice(0, 7), m = shuffle(all.filter(q => q.type === "mcq")).slice(0, tgt - 7);
      return shuffle([...t, ...m]);
    }
    let out = [], gs = shuffle(groups(all));
    if (s === "varc") { // all RC passages + verbal ability items to fill
      const rc = gs.filter(g => g[0].set), va = gs.filter(g => !g[0].set);
      rc.forEach(g => out.push(...g)); const need = tgt - out.length;
      const vaPick = va.slice(0, Math.max(0, need));
      // interleave: passage, a few VA, passage ...
      const res = []; const rcG = groups(out); let vi = 0;
      rcG.forEach(g => { res.push(...g); for (let k = 0; k < Math.ceil(vaPick.length / rcG.length) && vi < vaPick.length; k++) res.push(...vaPick[vi++]); });
      while (vi < vaPick.length) res.push(...vaPick[vi++]);
      return res;
    }
    // DILR: choose, at random, one of the combinations of whole sets whose size is closest to the target without exceeding it
    let best = -1, picks = [];
    for (let mask = 1; mask < (1 << gs.length); mask++) {
      let sz = 0; for (let i = 0; i < gs.length; i++) if (mask & (1 << i)) sz += gs[i].length;
      if (sz > tgt) continue; if (sz > best) { best = sz; picks = []; } if (sz === best) picks.push(mask);
    }
    const mask = picks[Math.floor(Math.random() * picks.length)];
    gs.forEach((g, i) => { if (mask & (1 << i)) out.push(...g); });
    return out;
  }
  function pickPractice(s, topic) {
    const all = bank.sections[s].questions.filter(q => !topic || q.topic === topic);
    return groups(all).flat();
  }

  // ---------- setup ----------
  function topicsFor(s) { const c = {}; bank.sections[s].questions.forEach(q => c[q.topic] = (c[q.topic] || 0) + 1); return c; }
  function refreshSetup() {
    mode = val("cmode"); sec = val("csec");
    $("#c-topic-wrap").classList.toggle("hidden", mode !== "practice");
    const tc = topicsFor(sec), sel = $("#c-topic"), keep = sel.dataset.want || sel.value; sel.dataset.want = "";
    sel.innerHTML = `<option value="">All ${sec.toUpperCase()} topics (${bank.sections[sec].questions.length})</option>` + Object.entries(tc).map(([t, n]) => `<option value="${esc(t)}">${esc(t)} (${n})</option>`).join("");
    if (keep && tc[keep]) sel.value = keep;
    const n = mode === "sectional" ? (sec === "qa" ? TARGET.qa : null) : pickPractice(sec, sel.value).length;
    $("#c-info").innerHTML = mode === "sectional"
      ? `<b>Sectional:</b> about ${TARGET[sec]} questions · 40-minute timer · +3 for correct, −1 for a wrong MCQ, 0 for a wrong TITA. Submits automatically when time runs out.`
      : `<b>Practice:</b> ${n} question${n === 1 ? "" : "s"} · no countdown · the solution appears right after you check each answer.`;
  }
  function counts() {
    ["varc", "dilr", "qa"].forEach(s => { const el = $(`[data-csec-count="${s}"]`); if (el) el.textContent = bank.sections[s].questions.length + " Qs"; });
  }

  // ---------- run ----------
  function start() {
    mode = val("cmode"); sec = val("csec");
    const picked = mode === "sectional" ? pickSectional(sec) : pickPractice(sec, $("#c-topic").value);
    qs = picked.map(q => {
      if (q.type !== "mcq") return { ...q };
      const idx = q.fixed ? [0, 1, 2, 3] : shuffle([0, 1, 2, 3]);
      // solutions refer to options as "Option 1" … "Option 4" (bank order); rewrite them as the letters actually shown
      const letter = d => L[idx.indexOf(+d - 1)];
      const solution = q.solution.replace(/\b([Oo]ptions?) ([1-4](?:(?:, | and | or )[1-4])*)\b/g, (m, w, list) => {
        const ds = list.match(/[1-4]/g), seps = list.split(/[1-4]/).slice(1, -1), ls = ds.map(letter).sort();
        return w + " " + ls.map((x, i) => x + (i < seps.length ? seps[i] : "")).join("");
      });
      return { ...q, options: idx.map(i => q.options[i]), answer: idx.indexOf(q.answer), solution };
    });
    const n = qs.length; resp = Array(n).fill(null); marked = Array(n).fill(false); visited = Array(n).fill(false); tspent = Array(n).fill(0); checked = Array(n).fill(false);
    cur = 0; elapsed = 0; timeLeft = SECTION_TIME;
    $("#c-setup").classList.add("hidden"); $("#c-results").classList.add("hidden"); $("#c-quiz").classList.remove("hidden");
    $("#c-title").textContent = `CAT ${bank.sections[sec].name} · ${mode === "sectional" ? "Sectional" : "Practice" + ($("#c-topic").value ? " · " + $("#c-topic").value : "")}`;
    $("#c-submit").textContent = mode === "sectional" ? "Submit section" : "Finish practice";
    $("#c-mark").classList.toggle("hidden", mode !== "sectional");
    $("#c-check").classList.toggle("hidden", mode !== "practice");
    clearInterval(timerId); shownAt = Date.now(); go(0); tick(); timerId = setInterval(tick, 1000);
    scrollTo({ top: 0, behavior: "instant" });
  }
  function tick() {
    const t = $("#c-timer");
    if (mode === "sectional") {
      t.textContent = "⏱ " + fmt(timeLeft) + " left"; t.classList.toggle("low", timeLeft <= 300);
      if (timeLeft <= 0) { submit(true); return; } timeLeft--;
    } else { t.textContent = "⏱ " + fmt(elapsed) + " elapsed"; elapsed++; }
  }
  function leave() { if (qs.length) tspent[cur] += (Date.now() - shownAt) / 1000; shownAt = Date.now(); }
  function go(i) { leave(); cur = i; visited[i] = true; render(); }

  function isCorrect(q, r) {
    if (r === null || r === "") return false;
    if (q.type === "mcq") return r === q.answer;
    if (q.kind === "sequence") return String(r).replace(/\s/g, "") === q.answer;
    const x = parseFloat(r); return !isNaN(x) && Math.abs(x - parseFloat(q.answer)) < 1e-9;
  }
  const answered = i => resp[i] !== null && resp[i] !== "";
  const showAns = q => q.type === "mcq" ? `${L[q.answer]}. ${q.options[q.answer]}` : q.answer;

  function render() {
    const q = qs[cur], set = q.set ? bank.sets[q.set] : null;
    const lay = $("#c-layout"); lay.classList.toggle("has-pane", !!set);
    $("#c-pane").classList.toggle("hidden", !set);
    if (set) {
      if ($("#c-pane").dataset.set !== q.set) { $("#c-pane-body").innerHTML = set.html; $("#c-pane").dataset.set = q.set; $("#c-pane-body").scrollTop = 0; }
      $("#c-pane-label").textContent = set.kind === "passage" ? "Passage" : "Data set";
      const inSet = qs.map((x, i) => [x, i]).filter(([x]) => x.set === q.set); const pos = inSet.findIndex(([, i]) => i === cur) + 1;
      $("#c-pane-meta").textContent = `Questions ${inSet[0][1] + 1}–${inSet[inSet.length - 1][1] + 1} (this is ${pos} of ${inSet.length})`;
    }
    $("#c-qnum").textContent = `Question ${cur + 1} of ${qs.length}`;
    $("#c-qtype").textContent = q.type === "mcq" ? "MCQ" : "TITA";
    $("#c-qtype").className = "qtype " + q.type;
    $("#c-qmeta").textContent = `${q.topic} · ${q.difficulty}`;
    $("#c-marks").textContent = q.type === "mcq" ? "+3 / −1" : "+3 / 0";
    $("#c-qtext").innerHTML = q.question;
    const done = mode === "practice" && checked[cur];
    if (q.type === "mcq") {
      $("#c-answer").innerHTML = q.options.map((o, i) => `<button class="opt ${resp[cur] === i ? "sel" : ""} ${done && i === q.answer ? "correct" : ""} ${done && resp[cur] === i && i !== q.answer ? "wrong" : ""}" data-i="${i}" ${done ? "disabled" : ""}><b>${L[i]}</b><span>${o}</span></button>`).join("");
      $$("#c-answer .opt").forEach(b => b.onclick = () => { resp[cur] = +b.dataset.i; render(); });
    } else {
      const seq = q.kind === "sequence", v = resp[cur] == null ? "" : esc(resp[cur]);
      $("#c-answer").innerHTML = `<div class="tita"><label for="c-tita">${seq ? "Type the sequence of sentence numbers (e.g. 2143)" : "Type your answer (numbers only)"}</label>
        <input id="c-tita" class="tita-input" autocomplete="off" value="${v}" ${seq ? 'inputmode="numeric" placeholder="e.g. 2143"' : 'inputmode="none" placeholder="Use the keypad"'} ${done ? "disabled" : ""}>
        ${seq ? "" : `<div class="keypad" ${done ? 'aria-disabled="true"' : ""}>${["7","8","9","4","5","6","1","2","3","0",".","−"].map(k => `<button type="button" data-k="${k}">${k}</button>`).join("")}<button type="button" data-k="bk" class="wide">⌫ Backspace</button><button type="button" data-k="clr" class="wide">Clear all</button></div>`}</div>`;
      const inp = $("#c-tita");
      const set_ = s => { s = seq ? s.replace(/[^1-9]/g, "").slice(0, 5) : s.replace(/[^0-9.\-]/g, "").replace(/(?!^)-/g, "").slice(0, 12); inp.value = s; resp[cur] = s === "" ? null : s; if (!done) $("#c-check").textContent = answered(cur) ? "Check answer" : "Show solution"; paletteOnly(); };
      inp.oninput = () => set_(inp.value);
      $$("#c-answer .keypad button").forEach(b => b.onclick = () => {
        if (done) return; const k = b.dataset.k;
        if (k === "bk") set_(inp.value.slice(0, -1)); else if (k === "clr") set_("");
        else if (k === "−") set_(inp.value.startsWith("-") ? inp.value.slice(1) : "-" + inp.value); else set_(inp.value + k);
      });
    }
    $("#c-feedback").innerHTML = done ? `<div class="fb ${isCorrect(q, resp[cur]) ? "ok" : "bad"}">${!answered(cur) ? "⏭ Skipped." : isCorrect(q, resp[cur]) ? "✅ Correct! +3" : "❌ Not quite." + (q.type === "mcq" ? " −1 in a real test." : " (No negative mark for TITA.)")} Correct answer: <b>${esc(showAns(q))}</b></div><div class="sol"><b>Solution:</b> ${q.solution}</div>` : "";
    $("#c-check").disabled = done; $("#c-check").textContent = done ? "Checked" : (answered(cur) ? "Check answer" : "Show solution");
    $("#c-prev").disabled = cur === 0;
    $("#c-next").textContent = cur === qs.length - 1 ? (mode === "sectional" ? "Save" : "Next") : "Save & Next →";
    $("#c-mark").textContent = "Mark for Review & Next";
    paletteOnly();
  }
  function stat(i) { return !visited[i] ? "nv" : marked[i] ? (answered(i) ? "am" : "m") : answered(i) ? "a" : "na"; }
  function paletteOnly() {
    $("#c-palette").innerHTML = qs.map((_, i) => `<button class="${stat(i)} ${i === cur ? "cur" : ""} ${mode === "practice" && checked[i] ? (isCorrect(qs[i], resp[i]) ? "ok" : "bad") : ""}" data-i="${i}" title="Question ${i + 1}">${i + 1}</button>`).join("");
    $$("#c-palette button").forEach(b => b.onclick = () => go(+b.dataset.i));
    const c = { a: 0, na: 0, nv: 0, m: 0, am: 0 }; qs.forEach((_, i) => c[stat(i)]++);
    Object.entries(c).forEach(([k, v]) => { const e = $(`[data-cnt="${k}"]`); if (e) e.textContent = v; });
  }

  function submit(auto) {
    if (!auto) {
      const un = qs.filter((_, i) => !answered(i)).length;
      if (!confirm(mode === "sectional" ? `Submit this section?${un ? ` ${un} question(s) unanswered.` : ""}` : "Finish this practice session?")) return;
    }
    leave(); clearInterval(timerId);
    const rows = qs.map((q, i) => ({ q, i, att: answered(i), ok: isCorrect(q, resp[i]), t: tspent[i] }));
    const att = rows.filter(r => r.att), ok = att.filter(r => r.ok), wrong = att.filter(r => !r.ok);
    const score = ok.length * 3 - wrong.filter(r => r.q.type === "mcq").length;
    const acc = att.length ? Math.round(ok.length / att.length * 100) : 0;
    const used = mode === "sectional" ? SECTION_TIME - Math.max(timeLeft, 0) : elapsed;
    const tSum = rows.reduce((a, r) => a + r.t, 0);
    const topics = {}; rows.forEach(r => { const t = topics[r.q.topic] = topics[r.q.topic] || { n: 0, att: 0, ok: 0, time: 0 }; t.n++; t.time += r.t; if (r.att) t.att++; if (r.ok) t.ok++; });
    const label = t => !t.att ? `<span class="tag-na">Not attempted</span>` : (t.ok / t.att >= 0.7 ? `<span class="tag-strong">Strong</span>` : t.ok / t.att < 0.5 ? `<span class="tag-weak">Weak</span>` : `<span class="tag-mid">Average</span>`);
    $("#c-quiz").classList.add("hidden"); $("#c-results").classList.remove("hidden");
    $("#c-res-head").innerHTML = `<h2>${auto ? "Time's up! " : ""}${esc($("#c-title").textContent)}: results</h2>
      <div class="kpis">
        <div class="kpi main"><b>${score}</b><span>Score (out of ${qs.length * 3})</span></div>
        <div class="kpi"><b>${att.length}/${qs.length}</b><span>Attempted</span></div>
        <div class="kpi"><b>${ok.length} ✅ · ${wrong.length} ❌</b><span>Correct · wrong</span></div>
        <div class="kpi"><b>${acc}%</b><span>Accuracy (of attempts)</span></div>
        <div class="kpi"><b>${fmt(used)}</b><span>Time used${mode === "sectional" ? " of 40:00" : ""}</span></div>
        <div class="kpi"><b>${Math.round(tSum / qs.length)} s</b><span>Avg time per question</span></div>
      </div>
      <p class="muted" style="font-size:.88rem;margin:.6em 0 0">Marking: +3 correct, −1 wrong MCQ, 0 wrong TITA, 0 unanswered.${wrong.filter(r => r.q.type === "mcq").length ? ` You lost ${wrong.filter(r => r.q.type === "mcq").length} mark(s) to negative marking.` : ""}</p>`;
    const tr = Object.entries(topics).sort((a, b) => (b[1].att ? b[1].ok / b[1].att : -1) - (a[1].att ? a[1].ok / a[1].att : -1));
    $("#c-topics").innerHTML = `<h3>Topic-wise breakdown</h3><div class="table-wrap"><table class="data topic-table"><tr><th style="text-align:left">Topic</th><th>Qs</th><th>Attempted</th><th>Correct</th><th>Accuracy</th><th>Avg time</th><th>Verdict</th></tr>` +
      tr.map(([t, v]) => `<tr><td style="text-align:left">${esc(t)}</td><td>${v.n}</td><td>${v.att}</td><td>${v.ok}</td><td>${v.att ? Math.round(v.ok / v.att * 100) + "%" : "–"}</td><td>${Math.round(v.time / v.n)} s</td><td>${label(v)}</td></tr>`).join("") + `</table></div>
      <p class="muted" style="font-size:.85rem">Strong = 70%+ accuracy on attempts · Weak = below 50% · based on this session only.</p>`;
    let last = null;
    $("#c-review").innerHTML = rows.map(({ q, i, att: a, ok: o, t }) => {
      let pane = ""; if (q.set && q.set !== last) { const s = bank.sets[q.set]; pane = `<details class="rv-pane"><summary>Show ${s.kind === "passage" ? "passage" : "data set"}: ${esc(s.title)}</summary><div class="q-data">${s.html}</div></details>`; } last = q.set || null;
      const yours = !a ? "Not answered" : q.type === "mcq" ? `${L[resp[i]]}. ${q.options[resp[i]]}` : esc(resp[i]);
      return `${pane}<div class="card review-item"><div class="muted" style="font-size:.85rem">Q${i + 1} · ${q.type.toUpperCase()} · ${esc(q.topic)} · ${q.difficulty} · ⏱ ${Math.round(t)} s · ${!a ? "⏭ Skipped (0)" : o ? "✅ Correct (+3)" : q.type === "mcq" ? "❌ Wrong (−1)" : "❌ Wrong (0)"}</div>
        <div class="q-text">${q.question}</div>
        ${q.type === "mcq" ? q.options.map((op, j) => `<div class="opt ${j === q.answer ? "correct" : ""} ${resp[i] === j && j !== q.answer ? "wrong" : ""}"><b>${L[j]}</b><span>${op}</span></div>`).join("") : `<p>Your answer: <b>${yours}</b> · Correct answer: <b>${esc(q.answer)}</b></p>`}
        <div class="sol"><b>Solution:</b> ${q.solution}</div></div>`;
    }).join("");
    scrollTo({ top: 0, behavior: "instant" });
  }

  async function init() {
    try { bank = await (await fetch("data/cat.json")).json(); }
    catch (e) { $("#c-setup").innerHTML = "<div class='notice'>Could not load CAT questions. Please open the site through a web server.</div>"; return; }
    const p = new URLSearchParams(location.search);
    if (p.get("mode")) { const r = $(`input[name=cmode][value=${p.get("mode")}]`); if (r) r.checked = true; }
    if (p.get("section")) { const r = $(`input[name=csec][value=${p.get("section")}]`); if (r) r.checked = true; }
    if (p.get("topic")) $("#c-topic").dataset.want = p.get("topic");
    $$("input[name=cmode],input[name=csec]").forEach(r => r.onchange = refreshSetup);
    $("#c-topic").onchange = refreshSetup;
    counts(); refreshSetup();
    $("#c-start").onclick = start;
  }
  document.addEventListener("DOMContentLoaded", () => {
    $("#c-prev").onclick = () => { if (cur > 0) go(cur - 1); };
    $("#c-next").onclick = () => { if (mode === "sectional") marked[cur] = false; if (cur < qs.length - 1) go(cur + 1); else { leave(); render(); } };
    $("#c-mark").onclick = () => { marked[cur] = true; if (cur < qs.length - 1) go(cur + 1); else render(); };
    $("#c-clear").onclick = () => { if (mode === "practice" && checked[cur]) return; resp[cur] = null; render(); };
    $("#c-check").onclick = () => { checked[cur] = true; render(); };
    $("#c-submit").onclick = () => submit(false);
    $("#c-retry").onclick = () => { $("#c-results").classList.add("hidden"); $("#c-setup").classList.remove("hidden"); refreshSetup(); scrollTo({ top: 0, behavior: "instant" }); };
    init();
  });
})();
