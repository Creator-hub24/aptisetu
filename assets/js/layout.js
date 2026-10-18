// Shared header/footer + brand injection
(function () {
  const S = window.SITE;
  const nav = [
    ["index.html", "Home"], ["quant.html", "Quant"], ["reasoning.html", "Reasoning"],
    ["dilr.html", "DILR"], ["practice.html", "Practice"], ["mock-tests.html", "Mock Tests"],
    ["placements.html", "Placements"], ["contact.html", "Contact"]
  ];
  const here = location.pathname.split("/").pop() || "index.html";
  const links = nav.map(([h, t]) => `<a href="${h}" class="${h === here ? "active" : ""}">${t}</a>`).join("");
  const header = document.getElementById("site-header");
  if (header) header.innerHTML = `
    <div class="container nav">
      <a href="index.html" class="logo"><span class="logo-mark">A</span><span data-brand></span></a>
      <button class="menu-btn" aria-label="Menu" onclick="document.body.classList.toggle('nav-open')">☰</button>
      <nav class="nav-links">${links}<a href="signup.html" class="btn btn-sm">Sign up free</a></nav>
    </div>`;
  const footer = document.getElementById("site-footer");
  if (footer) footer.innerHTML = `
    <div class="container footer-grid">
      <div><a href="index.html" class="logo"><span class="logo-mark">A</span><span data-brand></span></a>
        <p class="muted">${S.TAGLINE}. Built for CAT, Bank, SSC, GMAT and campus placements.</p></div>
      <div><h4>Learn</h4><a href="quant.html">Quantitative Aptitude</a><a href="reasoning.html">Logical Reasoning</a><a href="dilr.html">DILR</a></div>
      <div><h4>Practice</h4><a href="practice.html">Timed Quizzes</a><a href="mock-tests.html">Mock Tests</a><a href="placements.html">Placement Prep</a></div>
      <div><h4>Company</h4><a href="contact.html">Contact</a><a href="signup.html">Sign up</a></div>
    </div>
    <div class="container copyright">© ${S.YEAR} <span data-brand></span>. All rights reserved.</div>`;
  document.querySelectorAll("[data-brand]").forEach(e => e.textContent = S.BRAND);
  document.querySelectorAll("[data-tagline]").forEach(e => e.textContent = S.TAGLINE);
  document.querySelectorAll("[data-email]").forEach(e => { e.textContent = S.EMAIL; if (e.tagName === "A") e.href = "mailto:" + S.EMAIL; });
  if (document.title.includes("{BRAND}")) document.title = document.title.replace("{BRAND}", S.BRAND);
})();
