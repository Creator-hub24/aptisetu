// EN / हिंदी toggle for solutions on question pages. The choice is kept in this browser only.
(function () {
  const K = "aptisetu.sol-lang";
  function set(l) {
    try { localStorage.setItem(K, l); } catch (e) {}
    document.querySelectorAll(".sol").forEach(s => { const h = s.querySelector(".sol-hi"), e = s.querySelector(".sol-en"); if (!h || !e) return;
      const hi = l === "hi"; e.hidden = hi; h.hidden = !hi; const b = s.querySelector(".sol-h"); if (b) b.textContent = hi ? b.dataset.hi : b.dataset.en; });
    document.querySelectorAll(".lang-toggle button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.lang === l)));
  }
  function init() {
    document.querySelectorAll(".lang-toggle button").forEach(b => b.onclick = () => set(b.dataset.lang));
    let l = "en"; try { l = localStorage.getItem(K) || "en"; } catch (e) {} set(l);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
