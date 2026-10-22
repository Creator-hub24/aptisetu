// AptiSetu exam engine (CAT and CUET UG): timed sectional tests with exam marking, and untimed topic practice.
// The page sets window.EXAM ("cat" | "cuet") before loading this file; default is "cat".
(function () {
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const L = "ABCD";
  const EXAMS = {
    cat: { label: "CAT", dir: "data/cat/", secs: ["varc", "dilr", "qa"], marks: { mcq: [3, -1], tita: [3, 0] },
           target: { varc: 24, dilr: 22, qa: 22 }, time: () => 40 * 60 },
    // CUET (UG) 2026: 50 compulsory MCQs in 60 minutes per paper, +5 / −1 (NTA Information Bulletin). When the bank holds
    // fewer than 50 questions for a paper we keep the official pace of 72 seconds per question.
    cuet: { label: "CUET", dir: "data/cuet/", secs: ["gat", "english", "maths"], marks: { mcq: [5, -1] },
            target: { gat: 50, english: 50, maths: 50 }, time: n => Math.min(50, n) * 72,
            gatMix: { "Quantitative Reasoning": 15, "Logical & Analytical Reasoning": 15, "General Mental Ability": 10, "General Knowledge": 10 } }
  };
  const EX = EXAMS[window.EXAM] || EXAMS.cat, TARGET = EX.target;
  const mk = q => EX.marks[q.type] || EX.marks.mcq, sgn = v => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v);
  const marksTxt = q => `${sgn(mk(q)[0])} / ${mk(q)[1] ? sgn(mk(q)[1]) : "0"}`;
  let sectionTime = 0;
  const P = window.Progress, ENG = window.EXAM || "cat";
  let saveKey = "exam-" + ENG;
  // set page (set.html?sec=&set=): one fixed CAT practice set of 10, own save key, result saved to the account
  const SET = document.getElementById("set-info") ? (() => { const p = new URLSearchParams(location.search); return { sec: p.get("sec"), n: parseInt(p.get("set"), 10) }; })() : null;
  // fixed pack (cat-practice.html?pack=mock-1&section=qa&mode=sectional): mocks, sectionals and practice packs from tools/cat/packs
  const PACK = (new URLSearchParams(location.search).get("pack") || "").replace(/[^a-z0-9-]/g, "");
  const inPool = q => !q.pack || (!PACK && q.pack.startsWith("practice-"));   // random sectionals: original bank; topic practice adds practice packs
  let saveTick = 0;
  let bank = { sections: {}, sets: {} }, mode, sec, qs = [], cur = 0, resp = [], marked = [], visited = [], tspent = [], checked = [], timeLeft = 0, timerId = null, shownAt = 0, elapsed = 0;

  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const fmt = s => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const val = (name) => (document.querySelector(`input[name=${name}]:checked`) || {}).value;

  // ---------- data: one JSON file per section, loaded on demand ----------
  const loading = {};
  function ensure(s) {
    if (bank.sections[s]) return Promise.resolve();
    return loading[s] = loading[s] || fetch(EX.dir + s + ".json").then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(d => { bank.sections[s] = { name: d.name, questions: d.questions }; Object.assign(bank.sets, d.sets || {}); });
  }
  const fail = () => { $("#c-setup").innerHTML = "<div class='notice'>Could not load " + EX.label + " questions. Please check your connection, or open the site through a web server.</div>"; };

  // ---------- question selection ----------
  function groups(list) { // keep set questions together, in bank order
    const g = new Map(); list.forEach(q => { const k = q.set || q.id; if (!g.has(k)) g.set(k, []); g.get(k).push(q); }); return [...g.values()];
  }
  function pickSectional(s) {
    const all = bank.sections[s].questions.filter(q => !q.pack), tgt = TARGET[s];
    if (window.EXAM === "cuet") return pickCUET(s, all, tgt);
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
  // fill `quota` questions from `list`, taking whole sets (shuffled) and topping up with single questions
  function fill(list, quota) {
    const gs = shuffle(groups(list)), out = [];
    for (const g of gs) if (out.length + g.length <= quota) out.push(...g);
    return out;
  }
  function pickCUET(s, all, tgt) {
    if (s === "gat") { // our mix across the four areas (NTA does not publish a fixed split), kept in area order
      const out = []; Object.entries(EX.gatMix).forEach(([p, n]) => out.push(...fill(all.filter(q => q.part === p), n)));
      return out;
    }
    const parts = [...new Set(all.map(q => q.part))], out = [];   // English: RC then verbal ability; Maths: Section A then B1
    parts.forEach(p => out.push(...fill(all.filter(q => q.part === p), tgt - out.length)));
    return out;
  }
  function pickPractice(s, topic) {
    const all = bank.sections[s].questions.filter(inPool).filter(q => !topic || (topic.startsWith("p:") ? q.part === topic.slice(2) : q.topic === topic));
    return groups(all).flat();
  }
  const topicLabel = v => v.startsWith("p:") ? "All " + v.slice(2) : v;

  // ---------- setup ----------
  function topicsFor(s) { const c = {}; bank.sections[s].questions.filter(inPool).forEach(q => c[q.topic] = (c[q.topic] || 0) + 1); return c; }
  async function refreshSetup() {
    mode = val("cmode"); sec = val("csec");
    $("#c-start").disabled = true;
    if (!bank.sections[sec]) { $("#c-info").textContent = "Loading questions…"; try { await ensure(sec); } catch (e) { fail(); return; } if (sec !== val("csec")) return; }
    $("#c-start").disabled = false;
    $("#c-topic-wrap").classList.toggle("hidden", mode !== "practice");
    const tc = topicsFor(sec), sel = $("#c-topic"), keep = sel.dataset.want || sel.value; sel.dataset.want = "";
    const qq = bank.sections[sec].questions.filter(inPool), parts = [...new Set(qq.map(q => q.part).filter(Boolean))];
    const opt = (v, label) => `<option value="${esc(v)}">${esc(label)}</option>`;
    sel.innerHTML = `<option value="">All ${esc(bank.sections[sec].name)} topics</option>` + (parts.length > 1
      ? parts.map(p => { const pq = qq.filter(q => q.part === p), pt = {}; pq.forEach(q => pt[q.topic] = (pt[q.topic] || 0) + 1);
          return `<optgroup label="${esc(p)}">${opt("p:" + p, "All " + p, pq.length)}${Object.entries(pt).map(([t, n]) => opt(t, t, n)).join("")}</optgroup>`; }).join("")
      : Object.entries(tc).map(([t, n]) => opt(t, t, n)).join(""));
    if (keep && (tc[keep] || [...sel.options].some(o => o.value === keep))) sel.value = keep;
    let info;
    const np = PACK ? bank.sections[sec].questions.filter(q => q.pack === PACK).length : 0;
    if (np) { $("#c-topic-wrap").classList.add("hidden"); info = `<b>${esc(PACK)}:</b> ${np} fixed questions · ` + (mode === "sectional" ? "40-minute timer · +3 / −1 for a wrong MCQ / 0 for a wrong TITA." : "practice: no countdown, solution after each answer."); }
    else if (PACK) info = `<b>${esc(PACK)}</b> has no ${esc(bank.sections[sec].name)} questions; this will start a normal session.`;
    else if (mode === "practice") { info = `<b>Practice:</b> no countdown · the solution appears right after you check each answer.`; }
    else if (window.EXAM === "cuet") {
      const n = Math.min(TARGET[sec], qq.length), T = EX.time(n);
      info = `<b>Sectional:</b> ${fmt(T)} timer · +5 for a correct answer, −1 for a wrong one, 0 if unanswered. ` +
        (n >= 50 ? "Same size and time as the real paper (50 questions, 60 minutes)." : `The real paper has 50 questions in 60 minutes; our sectional for this subject is shorter, so the timer keeps the same pace (72 s per question).`) +
        (sec === "gat" ? " Mix: 15 quantitative, 15 logical &amp; analytical, 10 mental ability, 10 GK (our choice; NTA does not publish a fixed split)." : "") + " Submits automatically when time runs out.";
    } else info = `<b>Sectional:</b> 40-minute timer · +3 for correct, −1 for a wrong MCQ, 0 for a wrong TITA. Submits automatically when time runs out.`;
    $("#c-info").innerHTML = info;
  }
  function counts() {
    fetch("data/stats.json").then(r => r.json()).then(st => EX.secs.forEach(s => { const el = $(`[data-csec-count="${s}"]`), n = st.stat[ENG + "-" + s]; if (el && n === 0) el.textContent = "Soon"; })).catch(() => {});
  }

  // ---------- run ----------
  function start() {
    mode = val("cmode"); sec = val("csec");
    const pq = PACK ? bank.sections[sec].questions.filter(q => q.pack === PACK) : [];
    const picked = pq.length ? groups(pq).flat() : mode === "sectional" ? pickSectional(sec) : pickPractice(sec, $("#c-topic").value);
    qs = prep(picked);
    const n = qs.length; resp = Array(n).fill(null); marked = Array(n).fill(false); visited = Array(n).fill(false); tspent = Array(n).fill(0); checked = Array(n).fill(false);
    sectionTime = EX.time(qs.length); cur = 0; elapsed = 0; timeLeft = sectionTime;
    title = `${EX.label} ${bank.sections[sec].name} · ${pq.length ? PACK.replace(/-/g, " ").replace(/^./, c => c.toUpperCase()) + " · " : ""}${mode === "sectional" ? "Sectional" : "Practice" + (!pq.length && $("#c-topic").value ? " · " + topicLabel($("#c-topic").value) : "")}`;
    if (window.track) window.track(`${mode}-start-${ENG}-${sec}`);
    begin();
  }
  function prep(picked) {
    return picked.map(q => {
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
  }
  let title = "";
  function save() { if (P && qs.length) P.saveRun(saveKey, { mode, sec, qs, cur, resp, marked, visited, tspent, checked, timeLeft, elapsed, sectionTime, title }); }
  function begin() {
    document.querySelectorAll(".resume-bar").forEach(x => x.remove()); $("#c-progress").classList.add("hidden");
    $("#c-setup").classList.add("hidden"); $("#c-results").classList.add("hidden"); $("#c-quiz").classList.remove("hidden");
    $("#c-title").textContent = title;
    $("#c-submit").textContent = mode === "sectional" ? "Submit section" : "Finish practice";
    $("#c-mark").classList.toggle("hidden", mode !== "sectional");
    $("#c-check").classList.toggle("hidden", mode !== "practice");
    clearInterval(timerId); shownAt = Date.now(); $("#c-pane").dataset.set = ""; go(cur); tick(); timerId = setInterval(tick, 1000);
    scrollTo({ top: 0, behavior: "instant" });
  }
  function tick() {
    const t = $("#c-timer");
    if (mode === "sectional") {
      t.textContent = "⏱ " + fmt(timeLeft) + " left"; t.classList.toggle("low", timeLeft <= 300);
      if (timeLeft <= 0) { submit(true); return; } timeLeft--;
    } else { t.textContent = "⏱ " + fmt(elapsed) + " elapsed"; elapsed++; }
    if (++saveTick % 5 === 0) save();
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
    $("#c-marks").textContent = marksTxt(q);
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
    $("#c-feedback").innerHTML = done ? `<div class="fb ${isCorrect(q, resp[cur]) ? "ok" : "bad"}">${!answered(cur) ? "⏭ Skipped." : isCorrect(q, resp[cur]) ? `✅ Correct! ${sgn(mk(q)[0])}` : "❌ Not quite." + (mk(q)[1] ? ` ${sgn(mk(q)[1])} in a real test.` : " (No negative mark for TITA.)")} Correct answer: <b>${q.type === "mcq" ? showAns(q) : esc(showAns(q))}</b></div><div class="sol"><b>Solution:</b> ${q.solution}</div>` : "";
    $("#c-check").disabled = done; $("#c-check").textContent = done ? "Checked" : (answered(cur) ? "Check answer" : "Show solution");
    $("#c-prev").disabled = cur === 0;
    $("#c-next").textContent = cur === qs.length - 1 ? (mode === "sectional" ? "Save" : "Next") : "Save & Next →";
    $("#c-mark").textContent = "Mark for Review & Next";
    $("#c-report").innerHTML = report(q);
    paletteOnly(); save();
  }
  const report = q => P ? P.reportLink({ id: q.id, exam: EX.label, section: bank.sections[sec].name + " · " + q.topic }) : "";
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
    if (P) { P.clearRun(saveKey); P.record(ENG, qs.map((q, i) => ({ topic: q.topic, section: sec, attempted: answered(i), correct: isCorrect(q, resp[i]) }))); }
    if (window.track) { const ev = `${window.EXAM || "cat"}-${sec}`; window.track(`${mode}-finish-${ev}`); if (auto) window.track(`${mode}-autosubmit-${ev}`); }
    const rows = qs.map((q, i) => ({ q, i, att: answered(i), ok: isCorrect(q, resp[i]), t: tspent[i] }));
    const att = rows.filter(r => r.att), ok = att.filter(r => r.ok), wrong = att.filter(r => !r.ok);
    const score = ok.reduce((a, r) => a + mk(r.q)[0], 0) + wrong.reduce((a, r) => a + mk(r.q)[1], 0);
    const lost = -wrong.reduce((a, r) => a + mk(r.q)[1], 0), maxScore = qs.reduce((a, q) => a + mk(q)[0], 0);
    const acc = att.length ? Math.round(ok.length / att.length * 100) : 0;
    const used = mode === "sectional" ? sectionTime - Math.max(timeLeft, 0) : elapsed;
    const tSum = rows.reduce((a, r) => a + r.t, 0);
    const topics = {}; rows.forEach(r => { const t = topics[r.q.topic] = topics[r.q.topic] || { n: 0, att: 0, ok: 0, time: 0, part: r.q.part || "" }; t.n++; t.time += r.t; if (r.att) t.att++; if (r.ok) t.ok++; });
    const label = t => !t.att ? `<span class="tag-na">Not attempted</span>` : (t.ok / t.att >= 0.7 ? `<span class="tag-strong">Strong</span>` : t.ok / t.att < 0.5 ? `<span class="tag-weak">Weak</span>` : `<span class="tag-mid">Average</span>`);
    $("#c-quiz").classList.add("hidden"); $("#c-results").classList.remove("hidden");
    $("#c-res-head").innerHTML = `<h2>${auto ? "Time's up! " : ""}${esc($("#c-title").textContent)}: results</h2>
      <div class="kpis">
        <div class="kpi main"><b>${score}</b><span>Score (out of ${maxScore})</span></div>
        <div class="kpi"><b>${att.length}/${qs.length}</b><span>Attempted</span></div>
        <div class="kpi"><b>${ok.length} ✅ · ${wrong.length} ❌</b><span>Correct · wrong</span></div>
        <div class="kpi"><b>${acc}%</b><span>Accuracy (of attempts)</span></div>
        <div class="kpi"><b>${fmt(used)}</b><span>Time used${mode === "sectional" ? " of " + fmt(sectionTime) : ""}</span></div>
        <div class="kpi"><b>${Math.round(tSum / qs.length)} s</b><span>Avg time per question</span></div>
      </div>
      ${P ? (st => `<p style="margin:.8em 0 0">🔥 <b>${st.count}-day streak</b> · ${st.quizzes} quiz${st.quizzes === 1 ? "" : "zes"} finished</p>`)(P.streak()) : ""}
      ${P ? `<div class="cta-row share-row" style="margin:12px 0 0">${P.shareButton(`I scored ${score}/${maxScore} in a ${title} on ${(window.SITE || {}).BRAND || ""} (${acc}% accuracy)! Can you beat it?`, ENG + "-practice.html")}</div>` : ""}
      <p class="muted" style="font-size:.88rem;margin:.6em 0 0">Marking: ${window.EXAM === "cuet" ? "+5 correct, −1 wrong, 0 unanswered (CUET UG)" : "+3 correct, −1 wrong MCQ, 0 wrong TITA, 0 unanswered"}.${lost ? ` You lost ${lost} mark(s) to negative marking.` : ""}</p>`;
    const showPart = new Set(rows.map(r => r.q.part).filter(Boolean)).size > 1;
    const tr = Object.entries(topics).sort((a, b) => (showPart ? a[1].part.localeCompare(b[1].part) : 0) || (b[1].att ? b[1].ok / b[1].att : -1) - (a[1].att ? a[1].ok / a[1].att : -1));
    $("#c-topics").innerHTML = `<h3>Topic-wise breakdown</h3><div class="table-wrap"><table class="data topic-table"><tr>${showPart ? '<th style="text-align:left">Part</th>' : ""}<th style="text-align:left">Topic</th><th>Qs</th><th>Attempted</th><th>Correct</th><th>Accuracy</th><th>Avg time</th><th>Verdict</th></tr>` +
      tr.map(([t, v]) => `<tr>${showPart ? `<td style="text-align:left" class="muted">${esc(v.part)}</td>` : ""}<td style="text-align:left">${esc(t)}</td><td>${v.n}</td><td>${v.att}</td><td>${v.ok}</td><td>${v.att ? Math.round(v.ok / v.att * 100) + "%" : "–"}</td><td>${Math.round(v.time / v.n)} s</td><td>${label(v)}</td></tr>`).join("") + `</table></div>
      <p class="muted" style="font-size:.85rem">Strong = 70%+ accuracy on attempts · Weak = below 50% · based on this session only.</p>`;
    let last = null;
    $("#c-review").innerHTML = rows.map(({ q, i, att: a, ok: o, t }) => {
      let pane = ""; if (q.set && q.set !== last) { const s = bank.sets[q.set]; pane = `<details class="rv-pane"><summary>Show ${s.kind === "passage" ? "passage" : "data set"}: ${esc(s.title)}</summary><div class="q-data">${s.html}</div></details>`; } last = q.set || null;
      const yours = !a ? "Not answered" : q.type === "mcq" ? `${L[resp[i]]}. ${q.options[resp[i]]}` : esc(resp[i]);
      return `${pane}<div class="card review-item"><div class="muted" style="font-size:.85rem">Q${i + 1} · ${q.type.toUpperCase()} · ${esc(q.topic)} · ${q.difficulty} · ⏱ ${Math.round(t)} s · ${!a ? "⏭ Skipped (0)" : o ? `✅ Correct (${sgn(mk(q)[0])})` : `❌ Wrong (${mk(q)[1] ? sgn(mk(q)[1]) : "0"})`}</div>
        <div class="q-text">${q.question}</div>
        ${q.type === "mcq" ? q.options.map((op, j) => `<div class="opt ${j === q.answer ? "correct" : ""} ${resp[i] === j && j !== q.answer ? "wrong" : ""}"><b>${L[j]}</b><span>${op}</span></div>`).join("") : `<p>Your answer: <b>${yours}</b> · Correct answer: <b>${esc(q.answer)}</b></p>`}
        <div class="sol"><b>Solution:</b> ${q.solution}</div>${report(q)}</div>`;
    }).join("");
    $$("[data-progress]").forEach(x => P && P.panel(x, x.dataset.progress));
    if (SET) setSaved(score, maxScore);
    scrollTo({ top: 0, behavior: "instant" });
  }
  async function setSaved(score, total) {
    const el = $("#set-save"); if (!el) return;
    const A = window.Auth, u = A && await A.ready;
    if (!u) { el.innerHTML = `Not saved: you're not logged in. <a href="login.html?next=${encodeURIComponent("cat-" + { qa: "quant", varc: "varc", dilr: "dilr" }[SET.sec] + "-sets.html")}">Login</a> to save results and unlock levels.`; return; }
    try { await A.saveResult(SET.sec, SET.n, score, total); el.innerHTML = `✓ Saved to your account: Set ${SET.n} completed with ${score}/${total}.`; if (window.track) window.track(`set-finish-${SET.sec}-${SET.n}`); }
    catch (e) { el.textContent = "Could not save your result (" + (e.message || e) + "). Please try again later."; }
  }

  // ---------- set page ----------
  async function initSet() {
    const info = $("#set-info"), NAME = { qa: "Quant", varc: "VARC", dilr: "DILR" };
    if (!NAME[SET.sec] || !(SET.n >= 1)) { info.innerHTML = `<div class="notice">This set doesn't exist. <a href="cat.html">Back to CAT</a></div>`; return; }
    const hubUrl = `cat-${{ qa: "quant", varc: "varc", dilr: "dilr" }[SET.sec]}-sets.html`;
    $$("[data-hub]").forEach(a => a.href = hubUrl);
    let st;
    try { st = await window.CatSets.status(SET.sec); } catch (e) { info.innerHTML = `<div class="notice">Could not load this set. Please check your connection.</div>`; return; }
    const s = st.sets[SET.n - 1];
    if (!s) { info.innerHTML = `<div class="notice">This set doesn't exist. <a href="${hubUrl}">See all ${NAME[SET.sec]} sets</a></div>`; return; }
    const L = s.level;
    document.title = `CAT ${NAME[SET.sec]} · Set ${SET.n} (${L}) | ${(window.SITE || {}).BRAND || ""}`;
    $("#set-h1").textContent = `${NAME[SET.sec]} · Set ${SET.n}`;
    const msg = {
      soon: `This set is <b>coming soon</b>. We're still writing the questions for it.`,
      login: `🔒 Please <a href="login.html?next=${encodeURIComponent(location.pathname.split("/").pop() + location.search)}">login</a> to open this set. Guests can try Easy set 1.`,
      locked: `🔒 This set is locked. Finish all ${["Easy", "Medium", "Hard"][["Easy", "Medium", "Hard"].indexOf(L) - 1]} sets first.`
    }[s.state];
    if (msg) { info.innerHTML = `<div class="notice">${msg} <a href="${hubUrl}">See all ${NAME[SET.sec]} sets</a></div>`; return; }
    try { await ensure(SET.sec); } catch (e) { fail(); return; }
    const picked = groups(bank.sections[SET.sec].questions.filter(q => q.practiceSet === SET.n)).flat();
    if (!picked.length) { info.innerHTML = `<div class="notice">This set is empty.</div>`; return; }
    const mins = st.timer;
    info.innerHTML = `<span class="sbadge ${s.state === "done" ? "done" : "open"}">${s.state === "done" ? "✓ Done · best saved " + s.row.score + "/" + s.row.total : L}</span>
      <p style="margin:.6em 0 0"><b>${picked.length} questions · ${mins}-minute timer.</b> Marking: +3 correct, −1 wrong MCQ, 0 wrong TITA, 0 blank. Submits automatically when time runs out; solutions after you submit.</p>`;
    saveKey = `exam-cat-set-${SET.sec}-${SET.n}`;
    $("#c-start").classList.remove("hidden");
    $("#c-start").onclick = () => startSet(picked, mins, L);
    offerResume();
  }
  function startSet(picked, mins, L) {
    mode = "sectional"; sec = SET.sec;
    qs = prep(picked);
    const n = qs.length; resp = Array(n).fill(null); marked = Array(n).fill(false); visited = Array(n).fill(false); tspent = Array(n).fill(0); checked = Array(n).fill(false);
    sectionTime = mins * 60; cur = 0; elapsed = 0; timeLeft = sectionTime;
    title = `CAT ${{ qa: "Quant", varc: "VARC", dilr: "DILR" }[sec]} · Set ${SET.n} (${L})`;
    if (window.track) window.track(`set-start-${sec}-${SET.n}`);
    begin();
  }

  function offerResume() {
    const r = P && P.loadRun(saveKey); if (!r || !r.qs || !r.qs.length) return;
    const n = r.qs.filter((_, i) => r.resp[i] !== null && r.resp[i] !== "").length;
    const bar = document.createElement("div"); bar.className = "notice resume-bar";
    bar.innerHTML = `<b>Unfinished:</b> ${esc(r.title)} · ${n}/${r.qs.length} answered${r.mode === "sectional" ? ` · ${fmt(r.timeLeft)} left` : ""}. <span class="resume-actions"><button type="button" class="btn btn-sm" id="resume-go">Resume</button><button type="button" class="btn btn-ghost btn-sm" id="resume-drop">Discard</button></span>`;
    $("#c-setup").parentNode.insertBefore(bar, $("#c-setup"));
    $("#resume-go").onclick = async () => {
      try { await ensure(r.sec); } catch (e) { fail(); return; }
      ({ mode, sec, qs, cur, resp, marked, visited, tspent, checked, timeLeft, elapsed, sectionTime, title } = r); begin();
    };
    $("#resume-drop").onclick = () => { P.clearRun(saveKey); bar.remove(); };
  }

  // Opened from a card with ?mode=&section= (both valid): skip steps 1-2, show "CAT · QA · Practice" + Change.
  function collapseChooser(p) {
    const box = $("#c-choose"), sum = $("#c-summary");
    if (!box || !sum) return;
    const m = $$("input[name=cmode]").find(x => x.value === p.get("mode")), s = $$("input[name=csec]").find(x => x.value === p.get("section"));
    if (!m || !s) return;
    const name = el => el.closest("label").querySelector("b").textContent.replace(/^[^A-Za-z]+/, "").trim();
    $("#c-summary-text").innerHTML = `<b>${esc(EX.label)} · ${esc(name(s))} · ${esc(name(m))}</b>`;
    box.classList.add("hidden"); sum.classList.remove("hidden"); $("#c-setup").classList.add("collapsed");
    $("#c-change").onclick = () => { box.classList.remove("hidden"); sum.classList.add("hidden"); $("#c-setup").classList.remove("collapsed"); box.querySelector("input:checked").focus(); };
  }

  async function init() {
    if (SET) { $$("[data-progress]").forEach(x => P && P.panel(x, x.dataset.progress)); return initSet(); }
    $$("[data-progress]").forEach(x => P && P.panel(x, x.dataset.progress));
    offerResume();
    const p = new URLSearchParams(location.search);
    // match URL values against the real inputs (never build a selector from the URL)
    const tick = (name, v) => { if (!v) return; const r = $$(`input[name=${name}]`).find(x => x.value === v); if (r) r.checked = true; };
    tick("cmode", p.get("mode"));
    tick("csec", p.get("section"));
    if (p.get("topic")) $("#c-topic").dataset.want = p.get("topic");
    $$("input[name=cmode],input[name=csec]").forEach(r => r.onchange = refreshSetup);
    $("#c-topic").onchange = refreshSetup;
    collapseChooser(p);
    counts(); refreshSetup();
    $("#c-start").onclick = async () => { try { await ensure(val("csec")); } catch (e) { fail(); return; } start(); };
  }
  document.addEventListener("DOMContentLoaded", () => {
    $("#c-prev").onclick = () => { if (cur > 0) go(cur - 1); };
    $("#c-next").onclick = () => { if (mode === "sectional") marked[cur] = false; if (cur < qs.length - 1) go(cur + 1); else { leave(); render(); } };
    $("#c-mark").onclick = () => { marked[cur] = true; if (cur < qs.length - 1) go(cur + 1); else render(); };
    $("#c-clear").onclick = () => { if (mode === "practice" && checked[cur]) return; resp[cur] = null; render(); };
    $("#c-check").onclick = () => { checked[cur] = true; render(); };
    $("#c-submit").onclick = () => submit(false);
    $("#c-retry").onclick = SET ? () => location.reload() : () => { $("#c-results").classList.add("hidden"); $("#c-setup").classList.remove("hidden"); $("#c-progress").classList.remove("hidden"); refreshSetup(); scrollTo({ top: 0, behavior: "instant" }); };
    init();
  });
})();
