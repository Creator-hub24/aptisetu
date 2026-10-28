// open-mock.html: live/upcoming status, leaderboard, display name, my rank (Pass feature once payments are on)
(function () {
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function init() {
    const card = $("#om-card"); if (!card) return;
    const id = card.dataset.mock, st = new Date(card.dataset.start), en = new Date(card.dataset.end), now = new Date();
    const fmt = d => d.toLocaleString("en-IN", { timeZone: "Asia/Kolkata", weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" });
    const status = $("#om-status");
    if (now < st) { status.innerHTML = `⏳ Opens <b>${fmt(st)} IST</b>. You can look at the sections now; attempts before the window are practice only.`; }
    else if (now <= en) { status.innerHTML = `🟢 <b>Live now</b> until ${fmt(en)} IST.`; }
    else { status.innerHTML = `This edition has ended. The next Open Mock is on the first Sunday of next month. You can still take the sections as practice.`; }
    const A = window.Auth, ACC = window.Account;
    if (!A || !A.configured || !ACC) return;
    (async () => {
      const u = await A.ready;
      try {
        const rows = await ACC.leaderboard(id);
        $("#om-board").innerHTML = !rows || !rows.length ? `<p class="muted">No submissions yet.</p>` :
          `<div class="table-wrap"><table class="data"><tr><th>Rank</th><th style="text-align:left">Name</th><th>Total</th><th>Sections</th></tr>${rows.map(r => `<tr><td>${r.rank}</td><td style="text-align:left">${esc(r.display_name)}</td><td>${r.total}</td><td>${r.sections}/3</td></tr>`).join("")}</table></div>`;
      } catch (e) { $("#om-board").innerHTML = `<p class="muted">The leaderboard could not load. Please try again later.</p>`; }
      if (!u) return;
      const form = $("#om-name"); form.classList.remove("hidden");
      $("#om-name-in").value = await ACC.displayName();
      form.addEventListener("submit", async e => { e.preventDefault(); const m = $("#om-name-msg"); try { await ACC.setDisplayName($("#om-name-in").value); m.textContent = "Saved."; } catch (err) { m.textContent = err.message; } });
      const me = $("#om-me");
      if (await ACC.gate(me, "Your rank")) return;
      const r = await ACC.myRank(id);
      if (r) me.innerHTML = `<p style="margin-top:12px">Your rank: <b>${r.rank}</b> of ${r.candidates}.</p>`;
    })();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
