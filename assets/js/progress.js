// Progress kept only in this browser (localStorage): unfinished-quiz resume, daily streak, per-topic accuracy.
// Also: "Report an error" and "Share score" links. Nothing here is sent anywhere.
(function () {
  const S = window.SITE || {}, KEY = "aptiprep.progress.v1", RKEY = "aptiprep.resume.v1.";
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const today = () => { const d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
  const dayDiff = (a, b) => Math.round((new Date(b + "T00:00:00") - new Date(a + "T00:00:00")) / 864e5);
  function read() { try { const v = JSON.parse(localStorage.getItem(KEY)); if (v && typeof v === "object") return v; } catch (e) {} return { streak: { last: "", count: 0, best: 0 }, quizzes: 0, topics: {} }; }
  function write(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); return true; } catch (e) { return false; } }
  const LABEL = { general: "Bank / SSC", cat: "CAT", cuet: "CUET" };

  const P = window.Progress = {
    get: read,
    // rows: [{topic, section, attempted:bool, correct:bool}]
    record(exam, rows) {
      const v = read(), t = today(), s = v.streak || (v.streak = { last: "", count: 0, best: 0 });
      if (s.last !== t) { s.count = s.last && dayDiff(s.last, t) === 1 ? s.count + 1 : 1; s.last = t; s.best = Math.max(s.best || 0, s.count); }
      v.quizzes = (v.quizzes || 0) + 1;
      rows.forEach(r => { if (!r.attempted) return; const k = exam + "|" + r.section + "|" + r.topic, e = v.topics[k] || (v.topics[k] = { att: 0, ok: 0 }); e.att++; if (r.correct) e.ok++; });
      write(v); return v;
    },
    streak() { const v = read(), s = v.streak || {}; const live = s.last && dayDiff(s.last, today()) <= 1; return { count: live ? s.count : 0, best: s.best || 0, today: s.last === today(), quizzes: v.quizzes || 0 }; },
    reset() { try { Object.keys(localStorage).filter(k => k === KEY || k.startsWith(RKEY)).forEach(k => localStorage.removeItem(k)); } catch (e) {} },
    // unfinished quiz
    saveRun(engine, state) { try { localStorage.setItem(RKEY + engine, JSON.stringify({ ...state, savedAt: Date.now() })); } catch (e) {} },
    loadRun(engine) { try { const v = JSON.parse(localStorage.getItem(RKEY + engine)); if (v && Date.now() - v.savedAt < 7 * 864e5) return v; localStorage.removeItem(RKEY + engine); } catch (e) {} return null; },
    clearRun(engine) { try { localStorage.removeItem(RKEY + engine); } catch (e) {} },

    panel(el, exam) {
      if (!el) return;
      const st = P.streak(), v = read();
      const rows = Object.entries(v.topics || {}).map(([k, e]) => { const [x, s, t] = k.split("|"); return { x, s, t, att: e.att, ok: e.ok, acc: e.att ? e.ok / e.att : 0 }; })
        .filter(r => !exam || r.x === exam).sort((a, b) => a.acc - b.acc || b.att - a.att);
      const empty = !st.quizzes && !rows.length;
      el.innerHTML = `<div class="prog-head"><h2 class="h3">📈 Your progress</h2>${empty ? "" : '<button type="button" class="btn btn-ghost btn-sm prog-reset">Reset my progress</button>'}</div>` +
        (empty ? `<p class="muted" style="margin:0">Finish a quiz to start your daily streak and topic-wise accuracy. Saved only in this browser. Log in (optional) to keep your test scores across devices.</p>` :
        `<div class="prog-kpis"><div><b>🔥 ${st.count}</b><span>day streak${st.today ? "" : st.count ? " (practise today to keep it)" : ""}</span></div><div><b>${st.best}</b><span>best streak</span></div><div><b>${st.quizzes}</b><span>quizzes finished</span></div></div>` +
        (rows.length ? `<div class="table-wrap"><table class="data prog-table"><tr><th style="text-align:left">Topic</th><th>Attempted</th><th>Accuracy</th></tr>${rows.slice(0, 8).map(r =>
          `<tr><td style="text-align:left">${esc(r.t)} <small class="muted">${LABEL[r.x] || ""} ${esc(r.s.toUpperCase())}</small></td><td>${r.att}</td><td><span class="${r.acc >= .7 ? "tag-strong" : r.acc < .5 ? "tag-weak" : "tag-mid"}">${Math.round(r.acc * 100)}%</span></td></tr>`).join("")}</table></div>
          <p class="muted" style="font-size:.85rem;margin:.4em 0 0">Weakest topics first${rows.length > 8 ? ` · showing 8 of ${rows.length}` : ""}. Saved only in this browser.</p>` : ""));
      const b = el.querySelector(".prog-reset");
      if (b) b.onclick = () => { if (confirm("Delete your saved streak, topic accuracy and any unfinished quiz from this browser?")) { P.reset(); document.querySelectorAll("[data-progress]").forEach(x => P.panel(x, x.dataset.progress)); document.querySelectorAll(".resume-bar").forEach(x => x.remove()); } };
    },

    // "Report an error" link. ctx: {id, exam, section}
    reportLink(ctx) {
      const lines = [`Question ID: ${ctx.id}`, `Exam / section: ${ctx.exam} · ${ctx.section}`, `Page: ${location.href.split("#")[0]}`, "", "What looks wrong:", ""];
      let href = "";
      if (S.GOOGLE_FORM_URL) href = S.GOOGLE_FORM_URL.includes("{REPORT}") ? S.GOOGLE_FORM_URL.replace("{REPORT}", encodeURIComponent(lines.join("\n"))) : S.GOOGLE_FORM_URL;
      if (S.EMAIL && !(S.GOOGLE_FORM_URL && S.GOOGLE_FORM_URL.includes("{REPORT}")))
        href = `mailto:${S.EMAIL}?subject=${encodeURIComponent(`Error report: question ${ctx.id}`)}&body=${encodeURIComponent(lines.join("\n"))}`;
      if (!href) return "";
      const ext = href.startsWith("http") ? ' target="_blank" rel="noopener"' : "";
      return `<a class="report-link" href="${esc(href)}"${ext} data-qid="${esc(ctx.id)}">⚑ Report an error</a>`;
    },

    // WhatsApp share button
    shareButton(text, page) {
      const base = (S.SITE_URL || (location.origin + location.pathname.replace(/[^/]*$/, ""))).replace(/\/?$/, "/");
      const url = base + page + "?utm_source=whatsapp&utm_medium=share";
      const href = "https://wa.me/?text=" + encodeURIComponent(text + " " + url);
      return `<a class="btn btn-share" href="${esc(href)}" target="_blank" rel="noopener">📲 Share score on WhatsApp</a>`;
    }
  };
})();
