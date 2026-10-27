// Timed practice quiz engine (Bank / SSC / Placements). Each section loads from data/general/<section>.json on demand.
(function () {
  const $ = s => document.querySelector(s);
  const L = "ABCD", SECS = ["quant", "reasoning", "dilr"], P = window.Progress;
  let bank = {}, qs = [], cur = 0, ans = [], marked = [], timeLeft = 0, timerId = null, cfg = {}, saveTick = 0, tsp = [], shownAt = 0, lastCur = -1;

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
    sel.innerHTML = `<option value="">All topics</option>` +
      topics.map(t => `<option value="${t.replace(/"/g, "&quot;")}">${t}</option>`).join("");
    if (keep && topics.includes(keep)) sel.value = keep;
    sel.disabled = false; $("#start").disabled = false;
    updAvail();
  }
  function updAvail() { const n = poolFor(sec(), $("#topic").value).length; $("#avail").textContent = n ? "" : "No questions for this selection yet."; }

  function showProgress() { document.querySelectorAll("[data-progress]").forEach(x => P && P.panel(x, x.dataset.progress)); }

  function offerResume() {
    const r = P && P.loadRun("general"); if (!r || !r.qs || !r.qs.length) return;
    const n = r.ans.filter(a => a !== null).length;
    const bar = document.createElement("div"); bar.className = "notice resume-bar";
    bar.innerHTML = `<b>Unfinished quiz:</b> ${r.cfg.name} · ${n}/${r.qs.length} answered · ${fmt(r.timeLeft)} left. <span class="resume-actions"><button type="button" class="btn btn-sm" id="resume-go">Resume</button><button type="button" class="btn btn-ghost btn-sm" id="resume-drop">Discard</button></span>`;
    const host = $("#exam-pick"); host.parentNode.insertBefore(bar, host);
    $("#resume-go").onclick = () => { bar.remove(); qs = r.qs; ans = r.ans; marked = r.marked; cur = r.cur; timeLeft = r.timeLeft; cfg = r.cfg; tsp = r.tsp || []; lastCur = -1; begin(); };
    $("#resume-drop").onclick = () => { P.clearRun("general"); bar.remove(); };
  }
  function save() { if (P && qs.length) P.saveRun("general", { qs, ans, marked, cur, timeLeft, cfg, tsp }); }

  async function init() {
    const params = new URLSearchParams(location.search);
    const pre = params.get("section");
    if (pre) { const r = [...document.querySelectorAll("input[name=section]")].find(x => x.value === pre); if (r) r.checked = true; }
    document.querySelectorAll("input[name=section]").forEach(r => r.onchange = () => fillTopics());
    $("#topic").onchange = updAvail;
    $("#start").onclick = () => start();
    document.querySelectorAll("[data-quick]").forEach(b => b.onclick = () => quick(+b.dataset.quick));
    showProgress(); offerResume();
    if (params.get("daily") === "1") { daily(); return; }
    const qn = parseInt(params.get("quick"), 10);
    if (qn > 0) { quick(Math.min(qn, 20)); return; }
    if (params.get("exam") === "general" || pre) fillTopics(params.get("topic"));
  }

  // one tap: n mixed questions, 60 s each, simple marking
  async function quick(n) {
    try { await ensure("mixed"); } catch (e) { fail(); return; }
    start({ s: "mixed", topic: "", n, per: 60, neg: false, name: `Quick start · ${n} mixed questions` });
  }

  // Daily 10 (practice.html?daily=1): the same 10 standalone questions for everyone on a date (date-seeded shuffle), 60 s each
  async function daily() {
    try { await ensure("mixed"); } catch (e) { fail(); return; }
    const t = new Date(), d = t.getFullYear() + "-" + String(t.getMonth() + 1).padStart(2, "0") + "-" + String(t.getDate()).padStart(2, "0");
    let x = 0; for (const c of "general" + d) x = (Math.imul(x, 31) + c.charCodeAt(0)) | 0;
    const rnd = () => { x = (x + 0x6D2B79F5) | 0; let u = Math.imul(x ^ (x >>> 15), 1 | x); u = (u + Math.imul(u ^ (u >>> 7), 61 | u)) ^ u; return ((u ^ (u >>> 14)) >>> 0) / 4294967296; };
    const pool = poolFor("mixed").filter(q => !q.set).sort((a, b) => a.id < b.id ? -1 : 1);
    for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
    start({ s: "mixed", topic: "", n: 10, per: 60, neg: false, name: `Bank / SSC Daily 10 · ${d}`, pick: pool.slice(0, 10) });
  }

  function start(o) {
    o = o || { s: sec(), topic: $("#topic").value, n: +$("#count").value, per: +$("#per").value, neg: $("#neg").checked };
    const { s, topic, n, per } = o;
    const pool = poolFor(s, topic);
    if (!pool.length) return;
    let pick = o.pick || shuffle(pool).slice(0, Math.min(n, pool.length));
    // keep questions from the same DILR set together, in their original order
    const order = new Map(); pick.forEach((q, i) => { const k = q.set || q.id; if (!order.has(k)) order.set(k, i); });
    pick.sort((a, b) => (order.get(a.set || a.id) - order.get(b.set || b.id)) || (pool.indexOf(a) - pool.indexOf(b)));
    // shuffle option order unless the order is meaningful
    qs = pick.map(q => { const idx = q.fixed ? [0, 1, 2, 3] : shuffle([0, 1, 2, 3]); return { ...q, options: idx.map(i => q.options[i]), answer: idx.indexOf(q.answer) }; });
    cfg = { name: o.name || ((s === "mixed" ? "Mixed" : bank[s].name) + (topic ? " · " + topic : "")), neg: o.neg, ev: "general-" + s, per };
    ans = Array(qs.length).fill(null); marked = Array(qs.length).fill(false); cur = 0; tsp = Array(qs.length).fill(0); lastCur = -1; shownAt = 0;
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
    const q = qs[cur], now = Date.now();
    if (!tsp || tsp.length !== qs.length) tsp = Array(qs.length).fill(0);
    if (lastCur >= 0 && shownAt) tsp[lastCur] += (now - shownAt) / 1000; lastCur = cur; shownAt = now;
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
    clearInterval(timerId); if (lastCur >= 0 && shownAt) tsp[lastCur] += (Date.now() - shownAt) / 1000; shownAt = 0; lastCur = -1;
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
    $("#res-summary").insertAdjacentHTML("beforeend", extraReport(score, max, pct));
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

  // post-test report: topic accuracy, weak topics, time per question, progress graph (history kept in this browser only)
  const esc = t => String(t).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  function extraReport(score, max, pct) {
    const rows = qs.map((q, i) => ({ q, i, att: ans[i] !== null, ok: ans[i] === q.answer, t: tsp[i] || 0 }));
    const topics = {}; rows.forEach(r => { const k = r.q.topic, v = (topics[k] = topics[k] || { n: 0, att: 0, ok: 0, t: 0, sec: r.q._sec }); v.n++; v.t += r.t; if (r.att) v.att++; if (r.ok) v.ok++; });
    let h = `<div class="report-extra"><h3>Topic accuracy</h3><div class="table-wrap"><table class="topic-acc"><thead><tr><th>Topic</th><th>Correct</th><th>Accuracy</th><th>Avg time</th></tr></thead><tbody>${Object.entries(topics).map(([t, v]) => `<tr><td>${esc(t)}</td><td>${v.ok}/${v.n}</td><td>${v.att ? Math.round(v.ok / v.att * 100) + "%" : "–"}</td><td>${Math.round(v.t / v.n)} s</td></tr>`).join("")}</tbody></table></div>`;
    const weak = Object.entries(topics).filter(([, v]) => !v.att || v.ok / v.att < 0.5);
    h += `<h3>Weak topics</h3>` + (weak.length ? `<ul class="weak-list">${weak.map(([t, v]) => `<li><b>${esc(t)}</b> · ${v.att ? Math.round(v.ok / v.att * 100) + "% of " + v.att + " attempted" : "not attempted"} · <a href="practice.html?section=${encodeURIComponent(v.sec)}&topic=${encodeURIComponent(t)}">Practise this topic →</a></li>`).join("")}</ul>` : `<p class="muted">No weak topics in this quiz: every topic you attempted was 50% or better.</p>`);
    const mx = Math.max(1, ...rows.map(r => r.t));
    h += `<h3>Time per question</h3><div class="tpq" role="img" aria-label="Seconds spent on each question">${rows.map(r => `<div class="tpq-col" title="Q${r.i + 1}: ${Math.round(r.t)} s · ${!r.att ? "skipped" : r.ok ? "correct" : "wrong"}"><span class="tpq-bar ${!r.att ? "skip" : r.ok ? "ok" : "bad"}" style="height:${Math.max(4, Math.round(r.t / mx * 100))}%"></span><small>${r.i + 1}</small></div>`).join("")}</div><p class="muted" style="font-size:.85rem">Bar height = seconds spent (longest ${Math.round(mx)} s) · green correct · red wrong · grey skipped.</p>`;
    let all = {}; try { all = JSON.parse(localStorage.getItem("aptisetu.history")) || {}; } catch (e) {}
    const key = "general-" + (/Daily 10/.test(cfg.name) ? "daily" : cfg.ev), hist = (all[key] = all[key] || []);
    hist.push({ t: Date.now(), score, max, acc: pct }); if (hist.length > 30) hist.splice(0, hist.length - 30); try { localStorage.setItem("aptisetu.history", JSON.stringify(all)); } catch (e) {}
    if (hist.length >= 2) {
      const W = 320, H = 120, pts = hist.map((e, i) => [20 + i * (W - 40) / (hist.length - 1), H - 15 - (e.max ? Math.max(0, e.score) / e.max : 0) * (H - 30)]);
      h += `<h3>Your progress</h3><svg class="prog-graph" viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W * 1.5}px" role="img" aria-label="Score percentage over your last ${hist.length} attempts"><line x1="20" y1="${H - 15}" x2="${W - 20}" y2="${H - 15}" stroke="currentColor" opacity=".25"/><polyline fill="none" stroke="#4f46e5" stroke-width="2.5" points="${pts.map(p => p.map(v => v.toFixed(1)).join(",")).join(" ")}"/>${pts.map((p, i) => `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="3.5" fill="#4f46e5"><title>Attempt ${i + 1}: ${hist[i].score}/${hist[i].max}</title></circle>`).join("")}<text x="2" y="19" font-size="9" fill="currentColor">100%</text><text x="8" y="${H - 11}" font-size="9" fill="currentColor">0</text></svg><p class="muted" style="font-size:.85rem">Score as % of maximum over your last ${hist.length} quizzes of this type in this browser (latest on the right).</p>`;
    } else h += `<p class="muted" style="font-size:.85rem">Take this quiz type again to see your progress graph (saved only in this browser).</p>`;
    return h + "</div>";
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
