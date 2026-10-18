// Timed practice quiz engine. Questions load from data/questions.json
(function () {
  const $ = s => document.querySelector(s);
  const L = "ABCD";
  let bank, qs = [], cur = 0, ans = [], marked = [], timeLeft = 0, timerId = null, cfg = {};

  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const fmt = s => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;

  async function init() {
    try { bank = await (await fetch("data/questions.json")).json(); }
    catch (e) { $("#setup").innerHTML = "<div class='notice'>Could not load questions. Please open this site through a web server (e.g. <code>python3 -m http.server</code>).</div>"; return; }
    const pre = new URLSearchParams(location.search).get("section");
    if (pre) { const r = document.querySelector(`input[name=section][value=${pre}]`); if (r) r.checked = true; }
    $("#start").onclick = start;
  }

  function start() {
    const sec = document.querySelector("input[name=section]:checked").value;
    const n = +$("#count").value, per = +$("#per").value;
    let pool = sec === "mixed" ? [...bank.quant.questions, ...bank.reasoning.questions, ...bank.dilr.questions] : bank[sec].questions;
    qs = shuffle(pool).slice(0, Math.min(n, pool.length));
    cfg = { sec, name: sec === "mixed" ? "Mixed" : bank[sec].name, neg: $("#neg").checked };
    ans = Array(qs.length).fill(null); marked = Array(qs.length).fill(false); cur = 0;
    timeLeft = qs.length * per;
    $("#setup").classList.add("hidden"); $("#results").classList.add("hidden"); $("#quiz").classList.remove("hidden");
    $("#quiz-title").textContent = cfg.name + " · Practice";
    render(); tick(); timerId = setInterval(tick, 1000);
  }

  function tick() {
    const t = $("#timer"); t.textContent = "⏱ " + fmt(timeLeft); t.classList.toggle("low", timeLeft <= 30);
    if (timeLeft <= 0) { submit(true); return; } timeLeft--;
  }

  function render() {
    const q = qs[cur];
    $("#q-num").textContent = `Question ${cur + 1} of ${qs.length}`;
    $("#q-topic").textContent = `${q.topic} · ${q.difficulty}`;
    $("#bar").style.width = ((ans.filter(a => a !== null).length) / qs.length * 100) + "%";
    $("#q-data").innerHTML = q.data || ""; $("#q-data").classList.toggle("hidden", !q.data);
    $("#q-text").innerHTML = q.question;
    $("#opts").innerHTML = q.options.map((o, i) => `<button class="opt ${ans[cur] === i ? "sel" : ""}" data-i="${i}"><b>${L[i]}</b><span>${o}</span></button>`).join("");
    $("#opts").querySelectorAll(".opt").forEach(b => b.onclick = () => { ans[cur] = +b.dataset.i; render(); });
    $("#prev").disabled = cur === 0;
    $("#next").textContent = cur === qs.length - 1 ? "Finish ✓" : "Save & Next →";
    $("#mark").textContent = marked[cur] ? "★ Marked" : "☆ Mark for review";
    $("#palette").innerHTML = qs.map((_, i) => `<button class="${ans[i] !== null ? "ans" : ""} ${marked[i] ? "mark" : ""} ${i === cur ? "cur" : ""}" data-i="${i}">${i + 1}</button>`).join("");
    $("#palette").querySelectorAll("button").forEach(b => b.onclick = () => { cur = +b.dataset.i; render(); });
    $("#answered").textContent = `${ans.filter(a => a !== null).length}/${qs.length} answered`;
  }

  function submit(auto) {
    if (!auto) { const un = ans.filter(a => a === null).length; if (un && !confirm(`${un} question(s) unanswered. Submit anyway?`)) return; }
    clearInterval(timerId);
    let c = 0, w = 0;
    qs.forEach((q, i) => { if (ans[i] === null) return; ans[i] === q.answer ? c++ : w++; });
    const score = cfg.neg ? c * 3 - w : c, max = cfg.neg ? qs.length * 3 : qs.length;
    const pct = Math.round(c / qs.length * 100);
    $("#quiz").classList.add("hidden"); $("#results").classList.remove("hidden");
    $("#res-summary").innerHTML = `
      <div class="score-ring" style="--p:${pct}"><span>${pct}%</span></div>
      <h2 style="text-align:center">${auto ? "Time's up! " : ""}Score: ${score} / ${max}</h2>
      <p class="muted" style="text-align:center">✅ ${c} correct · ❌ ${w} wrong · ⏭ ${qs.length - c - w} skipped ${cfg.neg ? "· Marking: +3 / −1" : ""}</p>`;
    $("#review").innerHTML = qs.map((q, i) => `
      <div class="card review-item">
        <div class="muted" style="font-size:.85rem">Q${i + 1} · ${q.topic} · ${ans[i] === null ? "Skipped" : ans[i] === q.answer ? "✅ Correct" : "❌ Wrong"}</div>
        ${q.data ? `<div class="q-data">${q.data}</div>` : ""}
        <div class="q-text">${q.question}</div>
        ${q.options.map((o, j) => `<div class="opt ${j === q.answer ? "correct" : ""} ${ans[i] === j && j !== q.answer ? "wrong" : ""}"><b>${L[j]}</b><span>${o}</span></div>`).join("")}
        <div class="sol"><b>Solution:</b> ${q.solution}</div>
      </div>`).join("");
    scrollTo(0, 0);
  }

  document.addEventListener("DOMContentLoaded", () => {
    $("#prev").onclick = () => { if (cur > 0) { cur--; render(); } };
    $("#next").onclick = () => { if (cur < qs.length - 1) { cur++; render(); } else submit(false); };
    $("#clear").onclick = () => { ans[cur] = null; render(); };
    $("#mark").onclick = () => { marked[cur] = !marked[cur]; render(); };
    $("#submit").onclick = () => submit(false);
    $("#retry").onclick = () => { $("#results").classList.add("hidden"); $("#setup").classList.remove("hidden"); };
    init();
  });
  window.__quiz = { start }; // for testing
})();
