// account.html: login status, Pass status, saved history (Pass feature once payments are on)
(function () {
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const STATES = ["Andaman and Nicobar Islands","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Outside India"];
  const EXAMS = ["CAT","CLAT","Bank","SSC","CUET","Placements","Other"];
  // Optional profile card. Every field can stay empty; nothing here is shown to other users.
  async function profileCard(ACC, esc) {
    const card = $("#acct-profile"); if (!card) return;
    let p = {}; try { p = await ACC.getProfile() || {}; } catch (e) {}
    const u = window.Auth && window.Auth.user && window.Auth.user();
    const opt = (list, cur) => `<option value="">Select</option>` + list.map(x => `<option${x === cur ? " selected" : ""}>${esc(x)}</option>`).join("");
    card.hidden = false;
    card.innerHTML = `<h2 style="margin-top:0">Your profile</h2>
      <p class="muted" style="margin-top:0">Details to track your progress. <a href="privacy.html#account-data">Privacy</a></p>
      <form id="prof-form" class="form" novalidate>
        <label>Name <span class="req" title="Required">*</span><input id="prof-name" type="text" maxlength="30" autocomplete="nickname" required value="${esc(p.display_name && p.display_name !== "Aspirant" ? p.display_name : "")}" placeholder="e.g. Riya S"></label>
        <label>Email <span class="req" title="Required">*</span><input id="prof-email" type="email" value="${esc((u && u.email) || "")}" readonly aria-readonly="true"></label>
        <label>City<input id="prof-city" type="text" maxlength="60" autocomplete="address-level2" value="${esc(p.city || "")}"></label>
        <label>State<select id="prof-state">${opt(STATES, p.state)}</select></label>
        <label>Exam<select id="prof-exam">${opt(EXAMS, p.target_exam)}</select></label>
        <div class="cta-row" style="margin-top:12px"><button class="btn" type="submit">Save</button></div>
        <p id="prof-msg" class="muted" role="status" aria-live="polite" style="margin:8px 0 0"></p>
      </form>`;
    $("#prof-form").addEventListener("submit", async e => {
      e.preventDefault(); const m = $("#prof-msg"), n = $("#prof-name").value.trim();
      if (n.length < 2) { m.textContent = "Please add your name (2 to 30 letters)."; $("#prof-name").focus(); return; }
      m.textContent = "Saving…";
      try {
        await ACC.saveProfile({ display_name: n, city: $("#prof-city").value, state: $("#prof-state").value, target_exam: $("#prof-exam").value });
        m.textContent = "Saved ✓";
      } catch (err) { m.textContent = err.message || "Could not save. Try again."; }
    });
  }
  async function init() {
    const A = window.Auth, ACC = window.Account, box = $("#acct-box"), hist = $("#acct-history");
    if (!A || !A.configured) { box.innerHTML = `<div class="notice"><b>Accounts are not switched on yet.</b> Your results are still saved in this browser and shown after each test.</div>`; hist.remove(); return; }
    const u = await A.ready;
    if (!u) { box.innerHTML = `<p>Log in to see your saved history.</p><p><a class="btn" href="login.html?next=account.html">Log in</a></p>`; hist.remove(); return; }
    const pass = ACC.payments ? (await ACC.hasPass() ? "Active ✓" : `Not active · <a href="pass.html">See AptiSetu Pass</a>`) : "Not needed: everything is free right now";
    box.innerHTML = `<p>Logged in as <b>${esc(u.email || "")}</b>.</p><p class="muted">AptiSetu Pass: ${pass}</p>`;
    profileCard(ACC, esc);
    if (await ACC.gate(hist, "Saved history")) return;
    try {
      const rows = await ACC.history(100);
      hist.innerHTML = `<h2 style="margin-top:0">Saved history</h2>` + (rows.length ? `<div class="table-wrap"><table class="data" id="acct-table"><tr><th style="text-align:left">Date</th><th style="text-align:left">Test</th><th>Score</th><th>Accuracy</th></tr>${rows.map(r => `<tr><td style="text-align:left">${new Date(r.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}</td><td style="text-align:left">${esc(r.title || r.test_key)}</td><td>${+r.score}/${+r.max_score}</td><td>${r.accuracy == null ? "–" : r.accuracy + "%"}</td></tr>`).join("")}</table></div>` : `<p class="muted">Nothing saved yet. Finish any quiz while logged in and it appears here.</p><p><a class="btn" href="practice.html">Start practising</a></p>`);
    } catch (e) { hist.innerHTML = `<p class="muted">Your history could not load. Please try again later.</p>`; }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
