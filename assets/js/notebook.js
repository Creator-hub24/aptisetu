// Mistakes notebook, no-repeat pool and the header chips row (Mistakes · streak · Sign in / Sync).
// Everything lives in this browser's localStorage; counts are real and start at 0. Nothing is sent anywhere.
(function () {
  const MK = "aptisetu.mistakes.v1", SK = "aptisetu.seen.v1", PK = "aptiprep.progress.v1", MAXM = 300, MAXS = 4000;
  const rd = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v && typeof v === "object" ? v : d; } catch (e) { return d; } };
  const wr = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const plain = h => String(h || "").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/\s+/g, " ").trim();
  const todayS = () => { const d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
  let seenSet = null;
  const seenAll = () => seenSet || (seenSet = new Set(rd(SK, { ids: [] }).ids || []));
  const N = window.Notebook = {
    // ---- mistakes: {id: {id, exam, sec, topic, text, t, n}} ----
    mistakes() { return rd(MK, {}); },
    count() { return Object.keys(N.mistakes()).length; },
    // rows: [{q, attempted, correct, exam}] — a wrong answer adds the question, a later right answer removes it
    record(rows) {
      const m = N.mistakes(), now = Date.now();
      rows.forEach(r => { const q = r.q; if (!q || !q.id || !r.attempted) return;
        if (r.correct) { delete m[q.id]; return; }
        const e = m[q.id] || { id: q.id, n: 0 }; Object.assign(e, { exam: r.exam, sec: q._sec || "", topic: plain(q.topic), text: plain(q.question).slice(0, 160), t: now }); e.n++; m[q.id] = e; });
      const ks = Object.keys(m); if (ks.length > MAXM) ks.sort((a, b) => m[a].t - m[b].t).slice(0, ks.length - MAXM).forEach(k => delete m[k]);
      wr(MK, m); N.paint();
    },
    remove(id) { const m = N.mistakes(); delete m[id]; wr(MK, m); N.paint(); },
    clear() { try { localStorage.removeItem(MK); } catch (e) {} N.paint(); },
    // ---- no-repeat pool: questions you have already been shown go to the back of the queue ----
    seen(ids) { const s = seenAll(); ids.forEach(i => { if (i) { s.delete(i); s.add(i); } }); let a = [...s]; if (a.length > MAXS) a = a.slice(a.length - MAXS); seenSet = new Set(a); wr(SK, { ids: a }); },
    isSeen(id) { return seenAll().has(id); },
    seenCount() { return seenAll().size; },
    resetSeen() { seenSet = new Set(); try { localStorage.removeItem(SK); } catch (e) {} },
    // stable partition after a shuffle: unseen first (questions, or groups of questions from one set)
    unseenFirst(a) {
      if (!a.length || typeof a[0] !== "object") return a;
      const id = x => Array.isArray(x) ? (x[0] && x[0].id) : x && x.id, un = [], se = [];
      a.forEach(x => (N.isSeen(id(x)) ? se : un).push(x)); return un.concat(se);
    },
    streak() { const s = (rd(PK, {}).streak) || {}; if (!s.last) return 0; const d = Math.round((new Date(todayS() + "T00:00:00") - new Date(s.last + "T00:00:00")) / 864e5); return d <= 1 ? (s.count || 0) : 0; },
    // ---- chips row under the header ----
    paint() {
      const row = document.getElementById("chips-row"); if (!row) return;
      const n = N.count(), st = N.streak();
      row.querySelector("[data-chip=m] b").textContent = n;
      row.querySelector("[data-chip=m]").setAttribute("aria-label", `Mistakes notebook: ${n} question${n === 1 ? "" : "s"}`);
      row.querySelector("[data-chip=s] b").textContent = st;
      row.querySelector("[data-chip=s]").setAttribute("aria-label", `Practice streak: ${st} day${st === 1 ? "" : "s"}`);
    }
  };
  function chips() {
    const h = document.getElementById("site-header"); if (!h || document.getElementById("chips-row")) return;
    h.insertAdjacentHTML("beforeend", `<div class="container chips-row" id="chips-row">
      <a class="chip chip-m" data-chip="m" href="mistakes.html">📓 Mistakes <b>0</b></a>
      <a class="chip chip-s" data-chip="s" href="practice.html?daily=1">🔥 <b>0</b>-day streak</a>
      <a class="chip chip-sync" data-chip="a" href="login.html">Sign in / Sync</a></div>`);
    N.paint();
    const A = window.Auth; if (A && A.ready) A.ready.then(u => { if (u) { const a = h.querySelector("[data-chip=a]"); a.textContent = "✓ Synced"; a.href = "account.html"; } }).catch(() => {});
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", chips); else chips();
  addEventListener("storage", e => { if (e.key === MK || e.key === PK) N.paint(); });
})();
