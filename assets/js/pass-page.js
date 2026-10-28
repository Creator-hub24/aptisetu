// pass.html: the buy button appears only when PAYMENTS_ENABLED is "on" in config.js (off until the price is confirmed)
(function () {
  const S = window.SITE || {};
  async function init() {
    const ACC = window.Account, A = window.Auth, box = document.getElementById("pass-buy");
    if (!ACC || !ACC.payments || !box) return;
    const u = await A.ready;
    if (await ACC.hasPass()) { box.innerHTML = `<div class="notice">✓ Your AptiSetu Pass is active. <a href="account.html">My account →</a></div>`; return; }
    box.innerHTML = u ? `<button class="btn" id="pass-go" type="button">Get AptiSetu Pass · ₹${S.PASS_PRICE}</button><p id="pass-msg" class="muted" role="status"></p>`
                      : `<a class="btn" href="login.html?next=pass.html">Log in to get AptiSetu Pass · ₹${S.PASS_PRICE}</a>`;
    const b = document.getElementById("pass-go"); if (!b) return;
    b.addEventListener("click", async () => {
      const m = document.getElementById("pass-msg"); b.disabled = true; m.textContent = "Opening the payment window…";
      try { await ACC.buyPass(); box.innerHTML = `<div class="notice">✓ Payment received. Your AptiSetu Pass is active. <a href="account.html">My account →</a></div>`; }
      catch (e) { m.textContent = e.message; b.disabled = false; }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
