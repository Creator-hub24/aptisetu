// Account features on top of auth.js: saved test history, display name, AptiSetu Pass, Open Mock submit + leaderboard.
// Everything is a no-op for guests and while Supabase is not configured (the site then keeps using localStorage only).
// ?mock=1 (test only, see auth.js) keeps the same data in sessionStorage so the flows can be tested without a backend.
(function () {
  const S = window.SITE || {}, A = window.Auth;
  if (!A) return;
  const PAY = S.PAYMENTS_ENABLED === "on";
  const MH = "aptisetu.mock.history", MO = "aptisetu.mock.openmock", MN = "aptisetu.mock.name";
  const ss = { get: (k, d) => { try { return JSON.parse(sessionStorage.getItem(k)) ?? d; } catch (e) { return d; } }, set: (k, v) => { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
  const slug = s => String(s || "").toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 80) || "test";
  const db = () => A.client();
  async function fn(name, body) {
    const sess = await A.session(); if (!sess) throw new Error("Please log in first.");
    const r = await fetch(`${S.SUPABASE_URL}/functions/v1/${name}`, { method: "POST", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${sess.access_token}`, "apikey": S.SUPABASE_ANON_KEY }, body: JSON.stringify(body || {}) });
    const j = await r.json().catch(() => ({})); if (!r.ok) throw new Error(j.error || "Something went wrong. Please try again."); return j;
  }
  const Account = window.Account = {
    payments: PAY,
    // a finished quiz / sectional. Saved silently when logged in; never blocks the results screen.
    async saveAttempt(a) {
      const u = await A.ready; if (!u) return false;
      const row = { test_key: slug(a.key), title: String(a.title || "").slice(0, 160), score: +a.score || 0, max_score: +a.max || 0, accuracy: a.acc == null ? null : Math.round(a.acc), questions: a.questions || null, time_s: a.time_s == null ? null : Math.round(a.time_s) };
      try {
        if (A.mock) { const h = ss.get(MH, []); h.push({ ...row, created_at: new Date().toISOString() }); ss.set(MH, h.slice(-200)); return true; }
        const { error } = await db().from("test_attempts").insert({ ...row, user_id: u.id }); if (error) throw error; return true;
      } catch (e) { console.warn("history not saved:", e.message); return false; }
    },
    async history(limit = 100) {
      const u = await A.ready; if (!u) return [];
      if (A.mock) return ss.get(MH, []).slice().reverse().slice(0, limit);
      const { data, error } = await db().from("test_attempts").select("test_key,title,score,max_score,accuracy,questions,time_s,created_at").order("created_at", { ascending: false }).limit(limit);
      if (error) throw error; return data || [];
    },
    async hasPass() {
      const u = await A.ready; if (!u) return false;
      if (A.mock) return ss.get("aptisetu.mock.pass", false);
      const { data, error } = await db().rpc("has_pass", {}); return !error && !!data;
    },
    // Pass gating: while payments are off every feature is free.
    async unlocked() { return !PAY || await Account.hasPass(); },
    // Replace el with a short "needs AptiSetu Pass" note when gating is on and the user has no Pass. Returns true if locked.
    async gate(el, what) {
      if (!el || !PAY || await Account.unlocked()) return false;
      el.innerHTML = `<div class="notice pass-gate"><b>${what}</b> is part of AptiSetu Pass${S.PASS_PRICE ? ` (₹${S.PASS_PRICE})` : ""}. Free practice stays free. <a href="pass.html">See what's included →</a></div>`;
      return true;
    },
    async displayName() {
      const u = await A.ready; if (!u) return "";
      if (A.mock) return ss.get(MN, "");
      const { data } = await db().from("aptisetu_profiles").select("display_name").maybeSingle(); return (data && data.display_name) || "";
    },
    async setDisplayName(n) {
      n = String(n || "").trim().replace(/\s+/g, " ");
      if (n.length < 2 || n.length > 30) throw new Error("Use 2 to 30 characters.");
      const u = await A.ready; if (!u) throw new Error("Please log in first.");
      if (A.mock) { ss.set(MN, n); return n; }
      const { error } = await db().from("aptisetu_profiles").upsert({ user_id: u.id, display_name: n }); if (error) throw error; return n;
    },
    async submitOpenMock(mock, section, responses) {
      const u = await A.ready; if (!u) throw new Error("Please log in first.");
      if (A.mock) { const all = ss.get(MO, {}); const k = `${mock}:${section}`; const first = !all[k]; if (first) { all[k] = { score: responses.__score || 0 }; ss.set(MO, all); } return { score: all[k].score, first_attempt: first }; }
      const { data, error } = await db().rpc("submit_open_mock", { p_mock: mock, p_section: section, p_responses: responses });
      if (error) throw error; return data && data[0];
    },
    async leaderboard(mock) {
      if (A.mock) { const all = ss.get(MO, {}); const t = Object.entries(all).filter(([k]) => k.startsWith(mock + ":")).reduce((a, [, v]) => a + v.score, 0); return Object.keys(all).length ? [{ rank: 1, display_name: ss.get(MN, "") || "Aspirant", total: t, sections: Object.keys(all).length }] : []; }
      await A.ready; const c = db(); if (!c) return null;
      const { data, error } = await c.rpc("open_mock_leaderboard", { p_mock: mock, p_limit: 50 }); if (error) throw error; return data || [];
    },
    async myRank(mock) {
      const u = await A.ready; if (!u) return null;
      if (A.mock) return { rank: 1, candidates: 1 };
      const { data, error } = await db().rpc("my_open_mock_rank", { p_mock: mock }); if (error) return null; return data && data[0];
    },
    // Razorpay checkout. Only runs when PAYMENTS_ENABLED is "on" in config.js.
    async buyPass() {
      if (!PAY) throw new Error("AptiSetu Pass is not on sale yet.");
      await new Promise((ok, bad) => { if (window.Razorpay) return ok(); const s = document.createElement("script"); s.src = "https://checkout.razorpay.com/v1/checkout.js"; s.onload = ok; s.onerror = () => bad(new Error("Payment window failed to load.")); document.head.appendChild(s); });
      const o = await fn("create-order");
      const u = A.user();
      return new Promise((ok, bad) => {
        const rz = new window.Razorpay({
          key: o.key_id, order_id: o.order_id, amount: o.amount, currency: o.currency, name: S.BRAND || "AptiSetu", description: "AptiSetu Pass",
          prefill: { email: (u && u.email) || "" }, theme: { color: "#4f46e5" },
          handler: async r => { try { ok(await fn("verify-payment", r)); } catch (e) { bad(e); } },
          modal: { ondismiss: () => bad(new Error("Payment cancelled.")) }
        });
        rz.on("payment.failed", r => bad(new Error((r.error && r.error.description) || "Payment failed.")));
        rz.open();
      });
    }
  };
})();
