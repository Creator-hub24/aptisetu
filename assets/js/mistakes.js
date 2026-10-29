/* mistakes.html: lists the notebook (notebook.js), newest first, with links to each question's /q/ page when it has one. */
(function () {
  var list = document.getElementById("mk-list"); if (!list || !window.Notebook) return;
  var sum = document.getElementById("mk-sum"), sel = document.getElementById("mk-exam"), empty = document.getElementById("mk-empty"), tools = document.getElementById("mk-tools");
  var LBL = { cat: "CAT", cuet: "CUET (UG)", general: "Bank / SSC" }, TRK = { cat: "cat", cuet: "cuet", general: "bank-ssc" }, PR = { cat: "cat-practice.html", cuet: "cuet-practice.html", general: "practice.html?exam=general" };
  var urls = {}, byId = {};
  var esc = function (t) { return String(t || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  function draw() {
    var all = Notebook.mistakes(), ids = Object.keys(all), f = sel.value;
    var rows = ids.map(function (k) { return all[k]; }).filter(function (m) { return !f || m.exam === f; }).sort(function (a, b) { return b.t - a.t; });
    sum.textContent = ids.length ? ids.length + " question" + (ids.length === 1 ? "" : "s") + " to revisit" + (f ? " · showing " + rows.length + " from " + LBL[f] : "") : "Your notebook is empty.";
    empty.hidden = !!ids.length; tools.hidden = !ids.length;
    list.innerHTML = rows.map(function (m) {
      var u = urls[(TRK[m.exam] || "") + "|" + m.id] || byId[m.id], when = new Date(m.t).toLocaleDateString("en-IN", { day: "numeric", month: "short" });
      return '<li class="card mk-item"><div class="mk-meta"><span class="tc-tag">' + esc(LBL[m.exam] || m.exam) + "</span> " + esc(m.topic) + " · " + esc(m.id) + " · wrong " + (m.n > 1 ? m.n + " times" : "once") + " · last " + esc(when) + "</div>" +
        '<p class="mk-q">' + esc(m.text) + (m.text && m.text.length >= 160 ? "…" : "") + "</p>" +
        '<div class="mk-act">' + (u ? '<a href="' + esc(u) + '">Answer and solution →</a>' : '<a href="' + PR[m.exam] + '">Practise this topic →</a> <span class="muted">(from a mock or fixed set, so its solution is in that test\'s review)</span>') +
        ' <button type="button" class="btn btn-ghost btn-sm" data-rm="' + esc(m.id) + '">Got it, remove</button></div></li>';
    }).join("");
  }
  list.addEventListener("click", function (e) { var b = e.target.closest("[data-rm]"); if (b) { Notebook.remove(b.getAttribute("data-rm")); draw(); } });
  sel.addEventListener("change", draw);
  document.getElementById("mk-clear").addEventListener("click", function () { if (confirm("Clear every question from your mistakes notebook?")) { Notebook.clear(); draw(); } });
  draw();
  fetch("data/qindex.json").then(function (r) { return r.json(); }).then(function (ix) { ix.forEach(function (x) { urls[x.k + "|" + x.id] = x.u; if (!byId[x.id]) byId[x.id] = x.u; }); draw(); }).catch(function () {});
})();
