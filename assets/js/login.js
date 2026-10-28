// login.html: email magic-link form
(function () {
  const $ = s => document.querySelector(s);
  const next = (() => { const n = new URLSearchParams(location.search).get("next") || "cat-quant-sets.html"; return /^[a-z0-9-]+\.html(\?[\w=&%-]*)?$/i.test(n) ? n : "cat-quant-sets.html"; })();
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  async function paint() {
    const A = window.Auth, box = $("#login-box"), msg = $("#login-msg");
    if (!A.configured) {
      box.innerHTML = `<div class="notice"><b>Login not configured yet.</b> You can still practise everything that doesn't need an account, including Easy Quant set 1. <a href="${esc(next)}">Continue →</a></div>`;
      return;
    }
    const u = await A.ready;
    if (u) { box.innerHTML = `<p>You're logged in as <b>${esc(u.email || "")}</b>.</p><p><a class="btn" href="${esc(next)}">Continue →</a></p>`; return; }
    if ((window.SITE || {}).GOOGLE_LOGIN === "on" && !A.mock) {
      const g = document.createElement("p"); g.innerHTML = `<button type="button" class="btn btn-ghost" id="login-google">Continue with Google</button>`;
      $("#login-form").after(g);
      $("#login-google").addEventListener("click", async () => { try { await A.loginGoogle(next); } catch (err) { msg.className = "notice"; msg.textContent = err.message; } });
    }
    $("#login-form").addEventListener("submit", async e => {
      e.preventDefault(); const btn = $("#login-send"); btn.disabled = true; msg.className = "muted"; msg.textContent = "Sending…";
      try {
        const r = await A.login($("#login-email").value, next);
        if (r === "mock") { location.href = next; return; }
        msg.className = "notice"; msg.innerHTML = "📧 Check your inbox: we've sent you a login link. Open it on this device to finish logging in.";
      } catch (err) { msg.className = "notice"; msg.textContent = err.message || "Something went wrong. Please try again."; btn.disabled = false; }
    });
  }
  document.addEventListener("DOMContentLoaded", paint);
  if (window.Auth) window.Auth.onChange(u => { if (u) location.href = next; });
})();
