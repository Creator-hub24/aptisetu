// Login (Supabase email magic link) and CAT practice-set progress.
// Unlocking uses only the set_progress rows stored in Supabase, never localStorage.
// If SUPABASE_URL / SUPABASE_ANON_KEY in config.js are still placeholders, login shows "Login not configured yet".
// TEST ONLY: ?mock=1 turns on a fake login + in-tab progress store (sessionStorage) so the lock/unlock flow can be
// tested without a Supabase project; ?mock=0 turns it off. It is not linked anywhere and unlocks nothing that the
// public question files don't already contain (the locks are a UI gate only).
(function () {
  const S = window.SITE || {}, VER = "2.118.0";
  const ph = v => !v || /^YOUR_/.test(v);
  const MK = "aptisetu.mock", MU = "aptisetu.mock.user", MP = "aptisetu.mock.progress";
  try {
    const m = new URLSearchParams(location.search).get("mock");
    if (m === "1") sessionStorage.setItem(MK, "1"); else if (m === "0") [MK, MU, MP].forEach(k => sessionStorage.removeItem(k));
  } catch (e) {}
  const mock = (() => { try { return sessionStorage.getItem(MK) === "1"; } catch (e) { return false; } })();
  const real = !mock && !ph(S.SUPABASE_URL) && !ph(S.SUPABASE_ANON_KEY);
  const listeners = [];
  let client = null, user = null;
  const emit = () => listeners.forEach(f => { try { f(user); } catch (e) {} });

  function loadLib() {
    return new Promise((ok, bad) => {
      if (window.supabase) return ok();
      const s = document.createElement("script"); s.src = `assets/js/vendor/supabase-js-${VER}.min.js`;
      s.onload = ok; s.onerror = () => bad(new Error("supabase-js failed to load")); document.head.appendChild(s);
    });
  }
  const ready = (async () => {
    if (mock) { try { user = JSON.parse(sessionStorage.getItem(MU)); } catch (e) { user = null; } return user; }
    if (!real) return null;
    try {
      await loadLib();
      client = window.supabase.createClient(S.SUPABASE_URL, S.SUPABASE_ANON_KEY, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: "implicit" } });
      const { data } = await client.auth.getSession(); user = data.session ? data.session.user : null;
      client.auth.onAuthStateChange((_e, session) => { const u = session ? session.user : null; if ((u && u.id) !== (user && user.id)) { user = u; emit(); } });
    } catch (e) { console.warn("Login unavailable:", e.message); client = null; user = null; }
    return user;
  })();

  const mockRows = () => { try { return JSON.parse(sessionStorage.getItem(MP)) || []; } catch (e) { return []; } };
  const Auth = window.Auth = {
    configured: mock || real, mock, ready,
    user: () => user,
    client: () => client,
    async session() { await ready; if (!client) return null; const { data } = await client.auth.getSession(); return data.session; },
    async loginGoogle(next) {
      if (mock) throw new Error("Google login is not available in test mode.");
      await ready; if (!client) throw new Error("Login not configured yet.");
      const base = location.href.replace(/[^/]*([?#].*)?$/, "");
      const { error } = await client.auth.signInWithOAuth({ provider: "google", options: { redirectTo: base + (next || "login.html") } });
      if (error) throw error;
    },
    onChange(f) { listeners.push(f); },
    async login(email, next) {
      email = String(email || "").trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new Error("Please enter a valid email address.");
      if (mock) { user = { id: "mock-" + email, email }; sessionStorage.setItem(MU, JSON.stringify(user)); emit(); return "mock"; }
      if (!real) throw new Error("Login not configured yet.");
      await ready; if (!client) throw new Error("Login is unavailable right now. Please try again later.");
      const base = location.href.replace(/[^/]*([?#].*)?$/, "");
      const { error } = await client.auth.signInWithOtp({ email, options: { emailRedirectTo: base + (next || "login.html") } });
      if (error) throw error; return "sent";
    },
    async logout() {
      if (mock) { sessionStorage.removeItem(MU); user = null; emit(); return; }
      if (client) await client.auth.signOut(); user = null; emit();
    },
    // rows: [{section, set_no, score, total, updated_at}] for the logged-in user only (RLS enforces this server-side)
    async progress() {
      await ready; if (!user) return [];
      if (mock) return mockRows();
      const { data, error } = await client.from("set_progress").select("section,set_no,score,total,updated_at");
      if (error) throw error; return data || [];
    },
    async saveResult(section, setNo, score, total) {
      await ready; if (!user) return false;
      const row = { user_id: user.id, section, set_no: setNo, score, total, updated_at: new Date().toISOString() };
      if (mock) { const r = mockRows().filter(x => !(x.section === section && x.set_no === setNo)); r.push(row); sessionStorage.setItem(MP, JSON.stringify(r)); return true; }
      const { error } = await client.from("set_progress").upsert(row, { onConflict: "user_id,section,set_no" });
      if (error) throw error; return true;
    }
  };

  // header Login / Logout
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function paint() {
    const slot = document.getElementById("auth-slot"); if (!slot) return;
    const here = location.pathname.split("/").pop() + location.search;
    if (user) {
      slot.innerHTML = `<a class="who" href="account.html" title="My account: ${esc(user.email || "")}">${esc(user.email || "My account")}</a><button type="button" class="link" id="auth-logout">Logout</button>`;
      document.getElementById("auth-logout").addEventListener("click", async () => { await Auth.logout(); location.reload(); });
    } else slot.innerHTML = "";   // logged out: the "Login / Sync" chip under the header is the only login entry
  }
  Auth.onChange(paint);
  const go = () => ready.then(paint);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go); else go();
})();
