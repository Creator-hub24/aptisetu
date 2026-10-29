/* Home page: "What are you preparing for?" chips. Each chip shows its own short line and two links.
   Works without JS (the CAT pane is shown by default). The last choice is remembered in this browser. */
(function () {
  var box = document.getElementById("goal");
  if (!box) return;
  var chips = [].slice.call(box.querySelectorAll(".goal-chip")), panes = [].slice.call(box.querySelectorAll(".goal-pane"));
  var KEY = "aptisetu.goal";
  function pick(k, save) {
    if (!panes.some(function (p) { return p.getAttribute("data-goal-pane") === k; })) return;
    chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-goal") === k)); });
    panes.forEach(function (p) { p.hidden = p.getAttribute("data-goal-pane") !== k; });
    if (save) { try { localStorage.setItem(KEY, k); } catch (e) {} try { if (window.track) window.track("home-goal-" + k); } catch (e) {} }
  }
  chips.forEach(function (c) { c.addEventListener("click", function () { pick(c.getAttribute("data-goal"), true); }); });
  try { var saved = localStorage.getItem(KEY); if (saved) pick(saved, false); } catch (e) {}
})();
