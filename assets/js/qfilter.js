/* Question bank filters: difficulty chips on topic hubs (li[data-d]) and exam chips + topic search on q/index.html (.card[data-t]). */
(function () {
  var bar = document.querySelector(".qf-bar");
  if (!bar) return;
  var mode = bar.getAttribute("data-qf"), sel = "", q = "";
  var chips = [].slice.call(bar.querySelectorAll(".qf-chip")), count = bar.querySelector(".qf-count"), box = document.getElementById("qf-q");
  var items = mode === "d" ? [].slice.call(document.querySelectorAll("[data-qf-list] > li")) : [].slice.call(document.querySelectorAll(".card[data-t]"));
  function apply() {
    var shown = 0, total = 0;
    items.forEach(function (el) {
      if (mode === "d") {
        var ok = !sel || el.getAttribute("data-d") === sel;
        el.classList.toggle("qf-hide", !ok); total++; if (ok) shown++;
      } else {
        var cardOk = !sel || el.getAttribute("data-t") === sel, any = false;
        [].forEach.call(el.querySelectorAll("li"), function (li) {
          var ok = cardOk && (!q || li.textContent.toLowerCase().indexOf(q) >= 0);
          li.classList.toggle("qf-hide", !ok); total++; if (ok) { shown++; any = true; }
        });
        el.classList.toggle("qf-hide", !any);
      }
    });
    if (count) count.textContent = shown === total ? "" : shown + " of " + total + (mode === "d" ? " questions" : " topics");
  }
  chips.forEach(function (c) {
    c.onclick = function () {
      sel = c.getAttribute("data-v");
      chips.forEach(function (x) { x.setAttribute("aria-pressed", String(x === c)); });
      apply();
    };
  });
  if (box) box.oninput = function () { q = box.value.trim().toLowerCase(); apply(); };
})();
