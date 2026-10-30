// open-mock.html: live/upcoming status and, for a logged-in user, their own saved Open Mock scores.
// The Open Mock is unranked practice (no leaderboard, no rank); scores are visible only to their owner.
(function () {
  const $ = s => document.querySelector(s);
  const NAMES = { varc: "VARC", dilr: "DILR", qa: "QA" };
  function init() {
    const card = $("#om-card"); if (!card) return;
    const id = card.dataset.mock, st = new Date(card.dataset.start), en = new Date(card.dataset.end), now = new Date();
    const fmt = d => d.toLocaleString("en-IN", { timeZone: "Asia/Kolkata", weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" });
    const status = $("#om-status");
    if (now < st) { status.innerHTML = `⏳ Opens <b>${fmt(st)} IST</b>. You can look at the sections now; attempts before the window are not saved as Open Mock scores.`; }
    else if (now <= en) { status.innerHTML = `🟢 <b>Live now</b> until ${fmt(en)} IST. Unranked practice: no leaderboard.`; }
    else { status.innerHTML = `This edition has ended. The next Open Mock is on the first Sunday of next month. You can still take the sections as practice.`; }
    const A = window.Auth, ACC = window.Account, mine = $("#om-mine");
    if (!A || !A.configured || !ACC || !mine) return;
    (async () => {
      const u = await A.ready;
      if (!u) { mine.innerHTML = `<p class="muted"><a href="login.html?next=open-mock.html">Log in</a> to save your Open Mock scores to your account.</p>`; return; }
      try {
        const rows = await ACC.myOpenMock(id);
        if (!rows || !rows.length) { mine.innerHTML = `<p class="muted">No saved scores yet. Your first attempt of each section during the window is saved here.</p>`; return; }
        const by = Object.fromEntries(rows.map(r => [r.section, r])), total = rows.reduce((a, r) => a + (+r.score || 0), 0);
        mine.innerHTML = `<div class="table-wrap"><table class="data"><tr><th style="text-align:left">Section</th><th>Score</th><th>Correct</th><th>Wrong</th></tr>${["varc", "dilr", "qa"].map(s => by[s] ? `<tr><td style="text-align:left">${NAMES[s]}</td><td>${by[s].score}</td><td>${by[s].correct ?? "–"}</td><td>${by[s].wrong ?? "–"}</td></tr>` : `<tr><td style="text-align:left">${NAMES[s]}</td><td colspan="3" class="muted">not taken yet</td></tr>`).join("")}</table></div><p style="margin-top:8px">Total so far: <b>${total}</b> / 204</p>`;
      } catch (e) { mine.innerHTML = `<p class="muted">Your scores could not load. Please try again later.</p>`; }
    })();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
