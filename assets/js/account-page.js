// account.html: login status, Pass status, saved history (Pass feature once payments are on)
(function () {
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  async function init() {
    const A = window.Auth, ACC = window.Account, box = $("#acct-box"), hist = $("#acct-history");
    if (!A || !A.configured) { box.innerHTML = `<div class="notice"><b>Accounts are not switched on yet.</b> Your results are still saved in this browser and shown after each test.</div>`; hist.remove(); return; }
    const u = await A.ready;
    if (!u) { box.innerHTML = `<p>Log in to see your saved history.</p><p><a class="btn" href="login.html?next=account.html">Log in</a></p>`; hist.remove(); return; }
    const pass = ACC.payments ? (await ACC.hasPass() ? "Active ✓" : `Not active · <a href="pass.html">See AptiSetu Pass</a>`) : "Not needed: everything is free right now";
    box.innerHTML = `<p>Logged in as <b>${esc(u.email || "")}</b>.</p><p class="muted">AptiSetu Pass: ${pass}</p>`;
    if (await ACC.gate(hist, "Saved history")) return;
    try {
      const rows = await ACC.history(100);
      hist.innerHTML = `<h2 style="margin-top:0">Saved history</h2>` + (rows.length ? `<div class="table-wrap"><table class="data" id="acct-table"><tr><th style="text-align:left">Date</th><th style="text-align:left">Test</th><th>Score</th><th>Accuracy</th></tr>${rows.map(r => `<tr><td style="text-align:left">${new Date(r.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}</td><td style="text-align:left">${esc(r.title || r.test_key)}</td><td>${+r.score}/${+r.max_score}</td><td>${r.accuracy == null ? "–" : r.accuracy + "%"}</td></tr>`).join("")}</table></div>` : `<p class="muted">Nothing saved yet. Finish any quiz while logged in and it appears here.</p><p><a class="btn" href="practice.html">Start practising</a></p>`);
    } catch (e) { hist.innerHTML = `<p class="muted">Your history could not load. Please try again later.</p>`; }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
