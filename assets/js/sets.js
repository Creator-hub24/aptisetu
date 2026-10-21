// CAT practice sets: status of each set (ready / locked / done) and the hub pages.
// Unlock rule: Easy is open (guests: only Easy set 1). A level unlocks once every READY set of the previous level
// is completed; if the previous level has no ready sets, it counts as complete (otherwise VARC/DILR, which have no
// Easy sets yet, could never unlock Medium). Completion comes only from the user's set_progress rows (Supabase).
// This is a UI gate only: the question files are public.
(function () {
  const LEVELS = ["Easy", "Medium", "Hard"];   // set ranges per level come from data/cat/sets.json (per section)
  const NAME = { qa: "Quant", varc: "VARC", dilr: "DILR" };
  let meta = null;
  const getMeta = () => meta || (meta = fetch("data/cat/sets.json").then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }));

  async function status(sec) {
    const m = await getMeta(), user = await window.Auth.ready;
    let rows = [];
    if (user) { try { rows = await window.Auth.progress(); } catch (e) { console.warn("Could not load progress:", e.message || e); } }
    const done = {}; rows.filter(r => r.section === sec).forEach(r => done[r.set_no] = r);
    const lv = m.sections[sec], readyBy = {}, unlocked = {}, range = {};
    LEVELS.forEach(L => range[L] = lv[L].range);
    const levelOf = n => LEVELS.find(L => n >= range[L][0] && n <= range[L][1]);
    LEVELS.forEach(L => readyBy[L] = lv[L].ready.map(x => x.set));
    LEVELS.forEach((L, i) => {
      if (i === 0) { unlocked[L] = true; return; }
      const P = LEVELS[i - 1];
      unlocked[L] = unlocked[P] && readyBy[P].every(n => done[n]);
    });
    const sets = [];
    for (let n = 1; n <= lv.count; n++) {
      const L = levelOf(n), ready = readyBy[L].includes(n);
      let st;
      if (!ready) st = "soon";
      else if (!user) st = L === "Easy" && n === 1 ? (done[n] ? "done" : "open") : "login";
      else if (!unlocked[L]) st = "locked";
      else st = done[n] ? "done" : "open";
      sets.push({ n, level: L, state: st, row: done[n] || null });
    }
    return { sec, user, sets, unlocked, readyBy, range, count: lv.count, timer: m.timers[sec] };
  }

  function card(sec, s, info) {
    const L = s.level, prev = LEVELS[LEVELS.indexOf(L) - 1];
    const href = `set.html?sec=${sec}&set=${s.n}`, here = encodeURIComponent(location.pathname.split("/").pop());
    const head = `<b>Set ${s.n}</b><span class="muted" style="font-size:.85rem">${L} · 10 questions · ${info.timer} min</span>`;
    if (s.state === "soon") return `<div class="set-card soon">${head}<span class="sbadge soon">Coming soon</span></div>`;
    if (s.state === "login") return `<a class="set-card locked" href="login.html?next=${here}">${head}<span class="sbadge lock">🔒 Login to unlock</span></a>`;
    if (s.state === "locked") return `<div class="set-card locked">${head}<span class="sbadge lock">🔒 Locked</span><span class="muted" style="font-size:.8rem">Finish all ${prev} sets to unlock</span></div>`;
    if (s.state === "done") return `<a class="set-card" href="${href}">${head}<span class="sbadge done">✓ Done · ${s.row ? s.row.score + "/" + s.row.total : ""}</span></a>`;
    return `<a class="set-card" href="${href}">${head}<span class="sbadge open">Start →</span></a>`;
  }

  async function hub(el) {
    const sec = el.dataset.sec;
    try {
      const info = await status(sec);
      el.innerHTML = (info.user ? "" : `<div class="notice">You're browsing as a guest: Easy set 1 is open. <a href="login.html?next=${encodeURIComponent(location.pathname.split("/").pop())}">Login</a> to save progress and unlock levels.</div>`) +
        LEVELS.map(L => {
          const n = info.readyBy[L].length, lock = info.user && !info.unlocked[L];
          return `<div class="level-head"><h2>${L}</h2><span class="muted">Sets ${info.range[L][0]}–${info.range[L][1]} · ${n ? n + " ready" : "coming soon"}${lock ? " · 🔒 locked" : ""}</span></div>
            <div class="set-grid">${info.sets.filter(s => s.level === L).map(s => card(sec, s, info)).join("")}</div>`;
        }).join("");
    } catch (e) { el.innerHTML = `<div class="notice">Could not load the sets. Please check your connection and reload.</div>`; }
  }

  window.CatSets = { status, NAME, getMeta };
  document.addEventListener("DOMContentLoaded", () => {
    const el = document.getElementById("set-hub"); if (!el) return;
    hub(el); window.Auth.onChange(() => hub(el));
  });
})();
