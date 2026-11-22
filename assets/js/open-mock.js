// open-mock.html: one card per edition that had not ended when the page was built. For each card: live/upcoming
// status and, for a logged-in user, their own saved scores. The Open Mock is unranked practice (no leaderboard,
// no rank); scores are visible only to their owner. A card whose edition is over is hidden when a later one is shown.
(function () {
  const NAMES = { varc: "VARC", dilr: "DILR", qa: "QA" };
  const fmt = d => d.toLocaleString("en-IN", { timeZone: "Asia/Kolkata", weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" });
  function card(el, hasLater) {
    const id = el.dataset.mock, st = new Date(el.dataset.start), en = new Date(el.dataset.end), now = new Date(), sealed = el.dataset.sealed === "1";
    const status = el.querySelector(".om-status"), mine = el.querySelector(".om-mine"), start = el.querySelector(".om-start");
    if (now > en && hasLater) { el.hidden = true; return; }
    if (now < st) {
      status.innerHTML = sealed ? `⏳ Opens <b>${fmt(st)} IST</b>. The sections cannot be started before then.`
        : `⏳ Opens <b>${fmt(st)} IST</b>. You can look at the sections now; attempts before the window are not saved as Open Mock scores.`;
      if (sealed && start) start.querySelectorAll("a").forEach(a => { a.setAttribute("aria-disabled", "true"); a.classList.add("btn-ghost"); a.removeAttribute("href"); });
    }
    else if (now <= en) { status.innerHTML = `🟢 <b>Live now</b> until ${fmt(en)} IST. Unranked practice: no leaderboard.`; }
    else {
      status.innerHTML = sealed ? `This edition has ended. Its answers and solutions are open: start a section to see your saved attempt scored, or to take it as practice. The next date will be announced on this page.`
        : `This edition has ended. The next date will be announced on this page. You can still take the sections as practice.`;
    }
    const A = window.Auth, ACC = window.Account;
    if (!A || !A.configured || !ACC || !mine) return;
    (async () => {
      const u = await A.ready;
      if (!u) { mine.innerHTML = `<p class="muted"><a href="login.html?next=open-mock.html">Log in</a> to save your Open Mock scores to your account.</p>`; return; }
      try {
        const rows = await ACC.myOpenMock(id);
        if (!rows || !rows.length) { mine.innerHTML = `<p class="muted">No saved scores yet. Your first attempt of each section during the window is saved here.</p>`; return; }
        const by = Object.fromEntries(rows.map(r => [r.section, r])), total = rows.reduce((a, r) => a + (+r.score || 0), 0);
        mine.innerHTML = `<div class="table-wrap"><table class="data"><tr><th style="text-align:left">Section</th><th>Score</th><th>Correct</th><th>Wrong</th></tr>${["varc", "dilr", "qa"].map(s => by[s] ? `<tr><td style="text-align:left">${NAMES[s]}</td><td>${by[s].score}</td><td>${by[s].correct ?? "–"}</td><td>${by[s].wrong ?? "–"}</td></tr>` : `<tr><td style="text-align:left">${NAMES[s]}</td><td colspan="3" class="muted">not taken yet</td></tr>`).join("")}</table></div><p style="margin-top:8px">Total so far: <b>${total}</b></p>`;
      } catch (e) { mine.innerHTML = `<p class="muted">Your scores could not load. Please try again later.</p>`; }
    })();
  }
  function init() {
    const cards = [...document.querySelectorAll(".om-ed")], now = new Date();
    cards.forEach((el, i) => card(el, cards.slice(i + 1).length > 0));
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
