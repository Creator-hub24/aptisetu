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
/* q/index.html: question-level search (text, ID or topic) and a difficulty filter over data/qindex.json, the list of every /q/ page.
   Loaded only when you type 3+ characters or pick a difficulty. Respects the exam chip. Results link to each question's own page. */
(function () {
  var bar = document.querySelector('.qf-bar[data-qf="t"]'), box = document.getElementById("qf-q"), dsel = document.getElementById("qf-d"), res = document.getElementById("qf-res");
  if (!bar || !box || !dsel || !res) return;
  var idx = null, loading = null, list = document.getElementById("qf-qs"), head = document.getElementById("qf-res-h"), MAX = 40;
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  function load() { return loading || (loading = fetch("data/qindex.json").then(function (r) { return r.json(); }).then(function (j) { idx = j; return j; })); }
  function exam() { var c = bar.querySelector('.qf-chip[aria-pressed="true"]'); return c ? c.getAttribute("data-v") : ""; }
  function run() {
    var q = box.value.trim().toLowerCase(), d = dsel.value, e = exam();
    if (q.length < 3 && !d) { res.hidden = true; return; }
    load().then(function () {
      var words = q.length >= 3 ? q.split(/\s+/) : [];
      var hits = idx.filter(function (x) {
        if (e && x.e !== e) return false; if (d && x.d !== d) return false;
        var hay = (x.x + " " + x.t + " " + x.s + " " + x.id).toLowerCase();
        return words.every(function (w) { return hay.indexOf(w) >= 0; });
      });
      head.textContent = hits.length ? (hits.length > MAX ? "First " + MAX + " of " + hits.length + " matching questions" : hits.length + " matching question" + (hits.length === 1 ? "" : "s")) : "No matching questions";
      list.innerHTML = hits.slice(0, MAX).map(function (x) {
        return '<li><a href="' + esc(x.u) + '">' + esc(x.x) + (x.x.length >= 140 ? "…" : "") + '</a> <span class="muted">· ' + esc(x.e) + " · " + esc(x.t) + " · " + esc(x.d) + " · " + esc(x.id) + "</span></li>";
      }).join("");
      res.hidden = false;
    }).catch(function () { head.textContent = "Search is unavailable right now."; res.hidden = false; });
  }
  box.addEventListener("input", run); dsel.addEventListener("change", run);
  [].forEach.call(bar.querySelectorAll(".qf-chip"), function (c) { c.addEventListener("click", run); });
})();
