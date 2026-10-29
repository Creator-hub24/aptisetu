// Shared header/footer, logo mark and brand injection
(function () {
  const S = window.SITE;
  let n = 0;
  // Header mark: same navy #0B1F3A / gold #C9A227 icon as the favicon (drawn by tools/make_images.py)
  const logo = () => `<img src="assets/img/favicon.svg" alt="" width="36" height="36" class="logo-mark">`;
  // Grouped nav (v2): Home · Quant Lab · Tracks & Practice · Question Bank · Flashcards & Guides · Careers · About & Legal
  const nav = [
    ["index.html", "Home"],
    ["quant-lab.html", "Quant Lab"],
    ["tracks", "Tracks &amp; Practice", [["tracks.html", "All tracks"], ["cat.html", "CAT"], ["cuet.html", "CUET (UG)"], ["bank-ssc.html", "Bank &amp; SSC"], ["placements.html", "Placements"], ["practice.html", "Practice quizzes"], ["mock-tests.html", "CAT mock tests"], ["open-mock.html", "Open Mock"], ["mistakes.html", "Mistakes notebook"]]],
    ["q/index.html", "Question Bank"],
    ["study", "Flashcards &amp; Guides", [["flashcards.html", "Formula flashcards"], ["formula-sheets.html", "Formula sheets"], ["guides.html", "Guides"], ["quant.html", "Quant notes"], ["reasoning.html", "Reasoning notes"], ["dilr.html", "DILR notes"]]],
    ["careers", "Careers", [["after12.html", "After 12th"], ["after-graduation.html", "After graduation"]]],
    ["about", "About &amp; Legal", [["about.html", "About"], ["faq.html", "FAQ"], ["corrections.html", "Corrections"], ["contact.html", "Contact"], ["privacy.html", "Privacy"], ["terms.html", "Terms"], ["refund.html", "Refunds"]]]
  ];
  const here = location.pathname.split("/").pop() || "index.html", inQ = /\/q\//.test(location.pathname);
  const alias = { "quant-lab-explainers.html": "quant-lab.html", "quant-lab-generator.html": "quant-lab.html", "quant-lab-concept-lab.html": "quant-lab.html", "quant-lab-practice.html": "quant-lab.html", "cat-practice.html": "cat.html", "cuet-practice.html": "cuet.html", "varc.html": "cat.html",
                  "set.html": "cat-" + ({ qa: "quant", varc: "varc", dilr: "dilr" }[new URLSearchParams(location.search).get("sec")] || "quant") + "-sets.html" };
  const fam = h => /^cat-.*sets\.html$|^set\.html$/.test(h) ? "cat.html" : /^(ibps|sbi|ssc)-/.test(h) ? "bank-ssc.html" : /^formula-/.test(h) ? "formula-sheets.html" : /^(guide|g-)/.test(h) ? "guides.html" : null;
  const active = inQ ? "q/index.html" : (alias[here] && alias[here].indexOf("-sets") < 0 ? alias[here] : fam(here) || alias[here] || here);
  const links = nav.map(([h, t, kids]) => {
    if (!kids) return `<a href="${h}" class="${h === active ? "active" : ""}">${t}</a>`;
    const on = kids.some(([k]) => k === active);
    return `<div class="nav-dd${on ? " active" : ""}"><button type="button" class="nav-dd-btn" aria-expanded="false" aria-controls="dd-${h}">${t} <span aria-hidden="true">▾</span></button>
      <div class="nav-dd-menu" id="dd-${h}">${kids.map(([k, kt]) => `<a href="${k}" class="${k === active ? "active" : ""}">${kt}</a>`).join("")}</div></div>`;
  }).join("");
  const header = document.getElementById("site-header");
  if (header) {
    header.innerHTML = `
    <div class="container nav">
      <a href="index.html" class="logo">${logo()}<span data-brand></span></a>
      <button type="button" class="theme-btn" aria-label="Dark theme" aria-pressed="${window.Theme && Theme.get() === "dark" ? "true" : "false"}"><span class="ti-moon" aria-hidden="true">☾</span><span class="ti-sun" aria-hidden="true">☀</span></button>
      <button type="button" class="menu-btn" aria-label="Menu" aria-expanded="false">☰</button>
      <nav class="nav-links">${links}<span class="auth-slot" id="auth-slot"></span></nav>
    </div>`;
    const tb = header.querySelector(".theme-btn");
    tb.addEventListener("click", () => { if (window.Theme) Theme.toggle(); });
    const mb = header.querySelector(".menu-btn");
    mb.addEventListener("click", () => mb.setAttribute("aria-expanded", document.body.classList.toggle("nav-open")));
    header.querySelectorAll(".nav-dd").forEach(dd => {
      const b = dd.querySelector(".nav-dd-btn");
      const set = open => { dd.classList.toggle("open", open); b.setAttribute("aria-expanded", open); };
      b.addEventListener("click", e => { e.stopPropagation(); set(!dd.classList.contains("open")); });
      dd.addEventListener("keydown", e => { if (e.key === "Escape") { set(false); b.focus(); } });
      dd.addEventListener("focusout", e => { if (!dd.contains(e.relatedTarget) && matchMedia("(min-width:1061px)").matches) set(false); });
      document.addEventListener("click", e => { if (!dd.contains(e.target)) set(false); });
    });
  }
  // footer is written into each page by tools/build_pages.py

  // Analytics events: no-op unless GoatCounter loaded (GOATCOUNTER in config.js). No personal data is sent.
  window.track = function (name) {
    try { if (window.goatcounter && typeof window.goatcounter.count === "function") window.goatcounter.count({ path: name, title: name, event: true }); } catch (e) {}
  };

  // Keep utm_* parameters on same-site links so a campaign visit is attributed across pages.
  try {
    const utm = [...new URLSearchParams(location.search)].filter(([k]) => /^utm_/i.test(k));
    if (utm.length) document.addEventListener("click", function (ev) {
      const a = ev.target.closest && ev.target.closest("a[href]");
      if (!a || a.target === "_blank" || a.hasAttribute("download")) return;
      const raw = a.getAttribute("href");
      if (!raw || raw.charAt(0) === "#" || /^(mailto|tel|javascript):/i.test(raw)) return;
      const u = new URL(a.href, location.href);
      if (u.origin !== location.origin) return;
      if (u.pathname === location.pathname && u.search === location.search && u.hash) return; // in-page anchor
      let changed = false;
      utm.forEach(([k, v]) => { if (!u.searchParams.has(k)) { u.searchParams.set(k, v); changed = true; } });
      if (changed) a.href = u.href;   // updated before the browser follows the link
    }, true);
  } catch (e) {}
  document.querySelectorAll("[data-brand]").forEach(e => e.textContent = S.BRAND);
  document.querySelectorAll("[data-tagline]").forEach(e => e.textContent = S.TAGLINE);
})();
