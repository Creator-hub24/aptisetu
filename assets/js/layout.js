// Shared header/footer, logo mark and brand injection
(function () {
  const S = window.SITE;
  let n = 0;
  // "e" inside a 360° ring: clean SVG mark for edumaths360
  const logo = () => { const id = "lg" + (n++); return `<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true">
    <defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f46e5"/><stop offset="1" stop-color="#db2777"/></linearGradient></defs>
    <rect width="40" height="40" rx="11" fill="url(#${id})"/>
    <circle cx="20" cy="20" r="13" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="2.4"/>
    <path d="M20 7 A13 13 0 1 1 7.4 16.8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="20" cy="7" r="2.2" fill="#fff"/>
    <text x="20" y="25.6" text-anchor="middle" font-size="16.5" font-weight="800" fill="#fff" font-family="Inter,system-ui,sans-serif">e</text></svg>`; };
  const nav = [
    ["index.html", "Home"], ["quant.html", "Quant"], ["reasoning.html", "Reasoning"],
    ["dilr.html", "DILR"], ["practice.html", "Practice"], ["contact.html", "Contact"]
  ];
  const here = location.pathname.split("/").pop() || "index.html";
  const links = nav.map(([h, t]) => `<a href="${h}" class="${h === here ? "active" : ""}">${t}</a>`).join("");
  const header = document.getElementById("site-header");
  if (header) header.innerHTML = `
    <div class="container nav">
      <a href="index.html" class="logo">${logo()}<span data-brand></span></a>
      <button class="menu-btn" aria-label="Menu" onclick="document.body.classList.toggle('nav-open')">☰</button>
      <nav class="nav-links">${links}<a href="practice.html" class="btn btn-sm">Start practising</a></nav>
    </div>`;
  const footer = document.getElementById("site-footer");
  if (footer) footer.innerHTML = `
    <div class="container footer-grid">
      <div><a href="index.html" class="logo">${logo()}<span data-brand></span></a>
        <p class="muted">Free Quant, Reasoning and DILR practice for CAT, Bank, SSC, GMAT-style tests and campus placements.</p></div>
      <div><h4>Learn</h4><a href="quant.html">Quantitative Aptitude</a><a href="reasoning.html">Logical Reasoning</a><a href="dilr.html">DILR</a></div>
      <div><h4>Practice</h4><a href="practice.html">Timed quizzes</a><a href="practice.html?section=mixed">Mixed practice</a></div>
      <div><h4>Contact</h4><a href="contact.html">Contact us</a><a href="signup.html">Sign up</a></div>
    </div>
    <div class="container copyright">© ${S.YEAR} <span data-brand></span>. All rights reserved.</div>`;
  document.querySelectorAll("[data-brand]").forEach(e => e.textContent = S.BRAND);
  document.querySelectorAll("[data-tagline]").forEach(e => e.textContent = S.TAGLINE);
  document.querySelectorAll("[data-email]").forEach(e => { e.textContent = S.EMAIL; if (e.tagName === "A") e.href = "mailto:" + S.EMAIL; });
  if (document.title.includes("{BRAND}")) document.title = document.title.replace("{BRAND}", S.BRAND);
})();
