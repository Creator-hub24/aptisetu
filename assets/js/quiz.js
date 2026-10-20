// Timed practice quiz engine (Bank / SSC / Placements). Each section loads from data/general/<section>.json on demand.
(function () {
  const $ = s => document.querySelector(s);
  const L = "ABCD", SECS = ["quant", "reasoning", "dilr"], P = window.Progress;
  let bank = {}, qs = [], cur = 0, ans = [], marked = [], timeLeft = 0, timerId = null, cfg = {}, saveTick = 0;

  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const fmt = s => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
  const sec = () => document.querySelector("input[name=section]:checked").value;
  const need = s => s === "mixed" ? SECS : [s];
  const loading = {};
  function ensure(s) {
    return Promise.all(need(s).map(k => bank[k] ? null : (loading[k] = loading[k] || fetch(`data/general/${k}.json`).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(d => { d.questions.forEach(q => q._sec = k); bank[k] = d; }))));
  }
  const poolFor = (s, topic) => {
    const p = need(s).flatMap(k => bank[k] ? bank[k].questions : []);
    return topic ? p.filter(q => q.topic === topic) : p;
  };
  const fail = () => { $("#setup").innerHTML = "<div class='notice'>Could not load questions. Please check your connection, or open this site through a web server (e.g. <code>python3 -m http.server</code>).</div>"; };

  async function fillTopics(keep) {
    const s = sec(), sel = $("#topic");
    sel.disabled = true; $("#start").disabled = true; $("#avail").textContent = "Loading questions…";
    try { await ensure(s); } catch (e) { fail(); return; }
    if (s !== sec()) return;
    const topics = [...new Set(poolFor(s).map(q => q.topic))];
    sel.innerHTML = `<option value="">All topics (${poolFor(s).length})</option>` +
      topics.map(t => `<option value="${t.replace(/"/g, "&quot;")}">${t} (${poolFor(s, t).length})</option>`).join("");
    if (keep && topics.includes(keep)) sel.value = keep;
    sel.disabled = false; $("#start").disabled = false;
    updAvail();
  }
  function updAvail() { const n = poolFor(sec(), $("#topic").value).length; $("#avail").textContent = `${n} question${n === 1 ? "" : "s"} available for this selection.`; }

  function showProgress() { document.querySelectorAll("[data-progress]").forEach(x => P && P.panel(x, x.dataset.progress)); }

  function offerResume() {
    const r = P && P.loadRun("general"); if (!r || !r.qs || !r.qs.length) return;
    const n = r.ans.filter(a => a !== null).length;
    const bar = document.createElement("div"); bar.className = "notice resume-bar";
    bar.innerHTML = `<b>Unfinished quiz:</b> ${r.cfg.name} · ${n}/${r.qs.length} answered · ${fmt(r.timeLeft)} left. <span class="resume-actions"><button type="button" class="btn btn-sm" id="resume-go">Resume</button><button type="button" class="btn btn-ghost btn-sm" id="resume-drop">Discard</button></span>`;
    const host = $("#exam-pick"); host.parentNode.insertBefore(bar, host);
    $("#resume-go").onclick = () => { bar.remove(); qs = r.qs; ans = r.ans; marked = r.marked; cur = r.cur; timeLeft = r.timeLeft; cfg = r.cfg; begin(); };
    $("#resume-drop").onclick = () => { P.clearRun("general"); bar.remove(); };
  }
  function save() { if (P && qs.length) P.saveRun("general", { qs, ans, marked, cur, timeLeft, cfg }); }

  async function init() {
    const params = new URLSearchParams(location.search);
    const pre = params.get("section");
    if (pre) { const r = document.querySelector(`input[name=section][value=${pre}]`); if (r) r.checked = true; }
    document.querySelectorAll("input[name=section]").forEach(r => r.onchange = () => fillTopics());
    $("#topic").onchange = updAvail;
    $("#start").onclick = () => start();
    document.querySelectorAll("[data-quick]").forEach(b => b.onclick = () => quick(+b.dataset.quick));
    showProgress(); offerResume();
    const qn = parseInt(params.get("quick"), 10);
    if (qn > 0) { quick(Math.min(qn, 20)); return; }
    if (params.get("exam") === "general" || pre) fillTopics(params.get("topic"));
  }

  // one tap: n mixed questions, 60 s each, simple marking
  async function quick(n) {
    try { await ensure("mixed"); } catch (e) { fail(); return; }
    start({ s: "mixed", topic: "", n, per: 60, neg: false, name: `Quick start · ${n} mixed questions` });
  }

  function start(o) {
    o = o || { s: sec(), topic: $("#topic").value, n: +$("#count").value, per: +$("#per").value, neg: $("#neg").checked };
    const { s, topic, n, per } = o;
    const pool = poolFor(s, topic);
    if (!pool.length) return;
    let pick = shuffle(pool).slice(0, Math.min(n, pool.length));
    // keep questions from the same DILR set together, in their original order
    const order = new Map(); pick.forEach((q, i) => { const k = q.set || q.id; if (!order.has(k)) order.set(k, i); });
    pick.sort((a, b) => (order.get(a.set || a.id) - order.get(b.set || b.id)) || (pool.indexOf(a) - pool.indexOf(b)));
    // shuffle option order unless the order is meaningful
    qs = pick.map(q => { const idx = q.fixed ? [0, 1, 2, 3] : shuffle([0, 1, 2, 3]); return { ...q, options: idx.map(i => q.options[i]), answer: idx.indexOf(q.answer) }; });
    cfg = { name: o.name || ((s === "mixed" ? "Mixed" : bank[s].name) + (topic ? " · " + topic : "")), neg: o.neg, ev: "general-" + s, per };
    ans = Array(qs.length).fill(null); marked = Array(qs.length).fill(false); cur = 0;
    timeLeft = qs.length * per;
    window.track && window.track("quiz-start-" + cfg.ev);
    begin();
  }
  function begin() {
    document.querySelectorAll(".resume-bar").forEach(x => x.remove());
    $("#exam-pick").classList.add("hidden"); $("#progress-wrap").classList.add("hidden");
    $("#setup").classList.add("hidden"); $("#results").classList.add("hidden"); $("#quiz").classList.remove("hidden");
    $("#quiz-title").textContent = cfg.name;
    clearInterval(timerId); render(); tick(); timerId = setInterval(tick, 1000);
    scrollTo(0, 0);
  }

  function tick() {
    const t = $("#timer"); t.textContent = "⏱ " + fmt(Math.max(timeLeft, 0)); t.classList.toggle("low", timeLeft <= 30);
    if (timeLeft <= 0) { submit(true); return; } timeLeft--;
    if (++saveTick % 5 === 0) save();
  }
  const secName = q => (bank[q._sec] && bank[q._sec].name) || q._sec;
  const report = q => P ? P.reportLink({ id: q.id, exam: "Bank / SSC / Placements", section: secName(q) + " · " + q.topic }) : "";

  function render() {
    const q = qs[cur];
    $("#q-num").textContent = `Question ${cur + 1} of ${qs.length}`;
    $("#q-topic").textContent = `${q.topic} · ${q.difficulty}`;
    $("#bar").style.width = ((ans.filter(a => a !== null).length) / qs.length * 100) + "%";
    $("#q-data").innerHTML = q.data || ""; $("#q-data").classList.toggle("hidden", !q.data);
    $("#q-text").innerHTML = q.question;
    $("#opts").innerHTML = q.options.map((o, i) => `<button class="opt ${ans[cur] === i ? "sel" : ""}" data-i="${i}"><b>${L[i]}</b><span>${o}</span></button>`).join("");
    $("#opts").querySelectorAll(".opt").forEach(b => b.onclick = () => { ans[cur] = +b.dataset.i; render(); });
    $("#q-report").innerHTML = report(q);
    $("#prev").disabled = cur === 0;
    $("#next").textContent = cur === qs.length - 1 ? "Finish ✓" : "Save & Next →";
    $("#mark").textContent = marked[cur] ? "★ Marked" : "☆ Mark";
    $("#palette").innerHTML = qs.map((_, i) => `<button class="${ans[i] !== null ? "ans" : ""} ${marked[i] ? "mark" : ""} ${i === cur ? "cur" : ""}" data-i="${i}" aria-label="Question ${i + 1}">${i + 1}</button>`).join("");
    $("#palette").querySelectorAll("button").forEach(b => b.onclick = () => { cur = +b.dataset.i; render(); });
    $("#answered").textContent = `${ans.filter(a => a !== null).length}/${qs.length} answered`;
    save();
  }

  function submit(auto) {
    if (!auto) { const un = ans.filter(a => a === null).length; if (un && !confirm(`${un} question(s) unanswered. Submit anyway?`)) return; }
    clearInterval(timerId);
    if (window.track) { window.track("quiz-finish-" + cfg.ev); if (auto) window.track("quiz-autosubmit-" + cfg.ev); }
    let c = 0, w = 0;
    qs.forEach((q, i) => { if (ans[i] === null) return; ans[i] === q.answer ? c++ : w++; });
    const score = cfg.neg ? c * 3 - w : c, max = cfg.neg ? qs.length * 3 : qs.length;
    const pct = Math.round(c / qs.length * 100);
    if (P) { P.clearRun("general"); P.record("general", qs.map((q, i) => ({ topic: q.topic, section: q._sec, attempted: ans[i] !== null, correct: ans[i] === q.answer }))); }
    const st = P ? P.streak() : null;
    $("#quiz").classList.add("hidden"); $("#results").classList.remove("hidden");
    const brand = (window.SITE || {}).BRAND || "";
    $("#res-summary").innerHTML = `
      <div class="score-ring" style="--p:${pct}"><span>${pct}%</span></div>
      <h2 style="text-align:center">${auto ? "Time's up! " : ""}Score: ${score} / ${max}</h2>
      <p class="muted" style="text-align:center">✅ ${c} correct · ❌ ${w} wrong · ⏭ ${qs.length - c - w} skipped ${cfg.neg ? "· Marking: +3 / −1" : ""}</p>
      ${st ? `<p style="text-align:center;margin:.2em 0 0">🔥 <b>${st.count}-day streak</b> · ${st.quizzes} quiz${st.quizzes === 1 ? "" : "zes"} finished</p>` : ""}
      ${P ? `<div class="cta-row share-row" style="justify-content:center;margin:14px 0 0">${P.shareButton(`I scored ${score}/${max} (${pct}%) in a ${cfg.name} aptitude quiz on ${brand}! Can you beat it?`, "practice.html")}</div>` : ""}`;
    let lastSet = null;
    $("#review").innerHTML = qs.map((q, i) => {
      const showData = q.data && (!q.set || q.set !== lastSet); lastSet = q.set || null;
      return `<div class="card review-item">
        <div class="muted" style="font-size:.85rem">Q${i + 1} · ${q.topic} · ${q.difficulty} · ${ans[i] === null ? "Skipped" : ans[i] === q.answer ? "✅ Correct" : "❌ Wrong"}</div>
        ${showData ? `<div class="q-data">${q.data}</div>` : (q.data ? `<div class="muted" style="font-size:.85rem;margin:.3em 0">Same data as the previous question.</div>` : "")}
        <div class="q-text">${q.question}</div>
        ${q.options.map((o, j) => `<div class="opt ${j === q.answer ? "correct" : ""} ${ans[i] === j && j !== q.answer ? "wrong" : ""}"><b>${L[j]}</b><span>${o}</span></div>`).join("")}
        <div class="sol"><b>Solution:</b> ${q.solution}</div>${report(q)}
      </div>`; }).join("");
    showProgress();
    scrollTo(0, 0);
  }

  document.addEventListener("DOMContentLoaded", () => {
    $("#prev").onclick = () => { if (cur > 0) { cur--; render(); } };
    $("#next").onclick = () => { if (cur < qs.length - 1) { cur++; render(); } else submit(false); };
    $("#clear").onclick = () => { ans[cur] = null; render(); };
    $("#mark").onclick = () => { marked[cur] = !marked[cur]; render(); };
    $("#submit").onclick = () => submit(false);
    $("#retry").onclick = () => { $("#results").classList.add("hidden"); $("#setup").classList.remove("hidden"); $("#progress-wrap").classList.remove("hidden"); fillTopics($("#topic").value); scrollTo(0, 0); };
    window.__quizSetupHook = fillTopics;
    init();
  });
})();
