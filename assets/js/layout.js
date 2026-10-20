// Shared header/footer, logo mark and brand injection
(function () {
  const S = window.SITE;
  let n = 0;
  // Header mark: same navy #0B1F3A / gold #C9A227 icon as the favicon (drawn by tools/make_images.py)
  const logo = () => `<img src="assets/img/favicon.svg" alt="" width="36" height="36" class="logo-mark">`;
  const nav = [
    ["index.html", "Home"], ["quant.html", "Quant"], ["reasoning.html", "Reasoning"],
    ["dilr.html", "DILR"], ["cat.html", "CAT"], ["cuet.html", "CUET"], ["varc.html", "VARC"],
    ["practice.html", "Practice"],
    { label: "Careers", items: [["after12.html", "After 12"], ["after-graduation.html", "After Graduation"]] },
    ["about.html", "About"], ["contact.html", "Contact"]
  ];
  const here = location.pathname.split("/").pop() || "index.html";
  const alias = { "cat-practice.html": "cat.html", "cuet-practice.html": "cuet.html" };
  const active = alias[here] || here;
  const a = ([h, t]) => `<a href="${h}" class="${h === active ? "active" : ""}">${t}</a>`;
  // an entry with items is a small dropdown on desktop; on phones its links show inline in the menu
  const links = nav.map(n => !n.items ? a(n) :
    `<div class="nav-drop"><button type="button" class="nav-drop-btn${n.items.some(([h]) => h === active) ? " active" : ""}" aria-expanded="false" aria-haspopup="true">${n.label} <span aria-hidden="true">▾</span></button>` +
    `<div class="nav-drop-menu">${n.items.map(a).join("")}</div></div>`).join("");
  const header = document.getElementById("site-header");
  if (header) header.innerHTML = `
    <div class="container nav">
      <a href="index.html" class="logo">${logo()}<span data-brand></span></a>
      <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false">☰</button>
      <nav class="nav-links">${links}<a href="practice.html" class="btn btn-sm">Start practising</a></nav>
    </div>`;
  const menuBtn = header && header.querySelector(".menu-btn");
  if (menuBtn) menuBtn.addEventListener("click", () => {
    const open = document.body.classList.toggle("nav-open");
    menuBtn.setAttribute("aria-expanded", String(open));
  });
  if (header) header.querySelectorAll(".nav-drop").forEach(d => {
    const btn = d.querySelector(".nav-drop-btn");
    const set = open => { d.classList.toggle("open", open); btn.setAttribute("aria-expanded", String(open)); };
    btn.addEventListener("click", e => { e.stopPropagation(); set(!d.classList.contains("open")); });
    document.addEventListener("click", e => { if (!d.contains(e.target)) set(false); });
    d.addEventListener("keydown", e => { if (e.key === "Escape") { set(false); btn.focus(); } });
  });
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
