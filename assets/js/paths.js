/* Shared table engine for the After 12 and After Graduation pages.
   Each page loads its data file first (it sets window.PATHS), then this file.
   PATHS = { streams: {code: "short label"}, who: {code: "… students"}, allWho, anyLabel,
             cats: [field names], rows: [...], links: {key: {href, text}}, track } */
(function () {
  var P = window.PATHS;
  if (!P) return;
  var D = P.rows, CATS = P.cats, SL = P.streams, NALL = Object.keys(SL).length, LINKS = P.links || {};

  var state = { stream: "ALL", field: "", q: "", sort: "field" };
  var $ = function (s) { return document.querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var track = function (n) { try { if (window.track) window.track(n); } catch (e) {} };

  function pills(s) {
    if (s.length === NALL) return '<span class="a12-pill any">' + esc(P.anyLabel) + "</span>";
    return s.map(function (x) { return '<span class="a12-pill">' + esc(SL[x]) + "</span>"; }).join("");
  }
  function link(key) {
    var L = key && LINKS[key];
    return L ? '<a class="a12-link" href="' + esc(L.href) + '">' + esc(L.text) + " &rarr;</a>" : "";
  }
  function rowHtml(r) {
    return '<tr><td class="a12-course" data-label="Course"><b>' + esc(r.n) + '</b><span class="a12-cat">' + esc(r.c) + "</span></td>" +
      '<td data-label="Open to"><div>' + pills(r.s) + (r.x ? '<span class="a12-note">' + esc(r.x) + "</span>" : "") + "</div></td>" +
      '<td class="a12-dur" data-label="Duration">' + esc(r.d) + "</td>" +
      '<td data-label="How you get in"><div>' + esc(r.e) + link(r.u) + "</div></td>" +
      '<td data-label="Where it leads">' + esc(r.o) + "</td></tr>";
  }
  function view() {
    var q = state.q.trim().toLowerCase();
    var list = D.map(function (r, i) { r._i = i; return r; }).filter(function (r) {
      if (state.stream !== "ALL" && r.s.indexOf(state.stream) < 0) return false;
      if (state.field && r.c !== state.field) return false;
      if (q && (r.n + " " + r.c + " " + r.e + " " + r.o + " " + (r.x || "")).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    var yv = function (r, dir) { return r.y == null ? (dir > 0 ? 99 : -1) : r.y; };
    list.sort(function (a, b) {
      if (state.sort === "az") return a.n.localeCompare(b.n);
      if (state.sort === "short") return yv(a, 1) - yv(b, 1) || a._i - b._i;
      if (state.sort === "long") return yv(b, -1) - yv(a, -1) || a._i - b._i;
      return CATS.indexOf(a.c) - CATS.indexOf(b.c) || a._i - b._i;
    });
    return list;
  }
  function reveal() {
    var t = $("#a12-results");
    if (t && t.getBoundingClientRect().top > window.innerHeight * 0.55) {
      try { t.scrollIntoView({ behavior: "smooth", block: "start" }); } catch (e) { t.scrollIntoView(); }
    }
  }
  function update() {
    var list = view();
    $("#a12-rows").innerHTML = list.length ? list.map(rowHtml).join("") :
      '<tr class="a12-empty"><td colspan="5">Nothing matches these filters. Clear the search, pick another field, or choose ' + esc(P.allChip || "All") + ".</td></tr>";
    var who = state.stream === "ALL" ? P.allWho : P.who[state.stream];
    $("#a12-count").innerHTML = "Showing <strong>" + list.length + "</strong> of " + D.length + " options for " + esc(who);
    document.querySelectorAll("#a12-streams .a12-chip").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.stream === state.stream)); });
  }

  document.querySelectorAll("#a12-streams .a12-chip").forEach(function (b) {
    var s = b.dataset.stream;
    b.querySelector(".n").textContent = s === "ALL" ? D.length : D.filter(function (r) { return r.s.indexOf(s) >= 0; }).length;
    b.addEventListener("click", function () { state.stream = s; update(); reveal(); track(P.track + "-stream-" + s); });
  });
  CATS.forEach(function (c) {
    var n = D.filter(function (r) { return r.c === c; }).length;
    var o = document.createElement("option"); o.value = c; o.textContent = c + " (" + n + ")"; $("#a12-field").appendChild(o);
  });
  $("#a12-field").addEventListener("change", function (e) { state.field = e.target.value; update(); reveal(); track(P.track + "-field"); });
  $("#a12-q").addEventListener("input", function (e) { state.q = e.target.value; update(); });
  $("#a12-sort").addEventListener("change", function (e) { state.sort = e.target.value; update(); reveal(); });
  $("#a12-reset").addEventListener("click", function () {
    state = { stream: "ALL", field: "", q: "", sort: "field" };
    $("#a12-field").value = ""; $("#a12-q").value = ""; $("#a12-sort").value = "field"; update();
  });
  update();
})();
