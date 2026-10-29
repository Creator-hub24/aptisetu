// Theme (light/dark): loaded synchronously in <head> so the right theme is applied before first paint (no inline script; CSP 'self').
// The saved choice is a UI preference only (localStorage "aptisetu.theme"); with no saved choice the device setting is followed.
(function () {
  var KEY = "aptisetu.theme", root = document.documentElement, mq = window.matchMedia ? matchMedia("(prefers-color-scheme: dark)") : null;
  function saved() { try { var t = localStorage.getItem(KEY); return t === "light" || t === "dark" ? t : null; } catch (e) { return null; } }
  function apply(t) {
    root.setAttribute("data-theme", t); root.style.colorScheme = t;
    var m = document.querySelector('meta[name="theme-color"]'); if (m) m.setAttribute("content", t === "dark" ? "#0b1220" : "#FAF7F0");
    document.querySelectorAll(".theme-btn").forEach(function (b) { b.setAttribute("aria-pressed", t === "dark" ? "true" : "false"); });
    try { document.dispatchEvent(new CustomEvent("themechange", { detail: t })); } catch (e) {}
  }
  apply(saved() || (mq && mq.matches ? "dark" : "light"));
  if (mq && mq.addEventListener) mq.addEventListener("change", function (e) { if (!saved()) apply(e.matches ? "dark" : "light"); });
  window.Theme = {
    get: function () { return root.getAttribute("data-theme"); },
    set: function (t) { try { localStorage.setItem(KEY, t); } catch (e) {} apply(t); },
    toggle: function () { this.set(this.get() === "dark" ? "light" : "dark"); }
  };
})();
