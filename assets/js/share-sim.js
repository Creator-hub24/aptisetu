/* Quant Lab: shareable simulation links. ?s=id:value,id:value sets the sliders (clamped to each slider's range) when the page opens;
   "Copy simulation link" makes a link with the current slider values. Loaded after lab.js on Explainers and Concept Lab. */
(function () {
  var root = document.getElementById("ql"); if (!root) return;
  var raw = new URLSearchParams(location.search).get("s") || "";
  var ctl = function (id) { return root.querySelector('input[type=range][data-id="' + id + '"]') || root.querySelector('#' + id + ':is(input[type=range],select)'); };
  function apply() {
    var first = null;
    raw.split(",").forEach(function (pair) {
      var m = /^([A-Za-z][A-Za-z0-9]{0,7}):(-?[0-9.]+|[a-z]{1,8})$/.exec(pair.trim()); if (!m) return;
      var el = ctl(m[1]); if (!el) return;
      if (el.tagName === "SELECT") { if ([].some.call(el.options, function (o) { return o.value === m[2]; })) { el.value = m[2]; el.dispatchEvent(new Event("change", { bubbles: true })); } return; }
      var v = parseFloat(m[2]); if (!isFinite(v)) return;
      var lo = +el.min, hi = +el.max, st = +el.step || 1;
      v = Math.min(hi, Math.max(lo, v)); v = lo + Math.round((v - lo) / st) * st; v = +v.toFixed(6);
      el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); first = first || el;
    });
    if (first) { var c = first.closest(".card"); if (c && c.scrollIntoView) c.scrollIntoView({ block: "start" }); }
  }
  function link(scope) {
    var parts = [].map.call((scope || root).querySelectorAll("input[type=range], select#dir"), function (el) { return (el.dataset.id || el.id) + ":" + el.value; }).filter(function (x) { return !/^:/.test(x); });
    var q = new URLSearchParams(location.search); q.set("s", parts.join(","));
    return location.origin + location.pathname + "?" + q.toString().replace(/%3A/g, ":").replace(/%2C/g, ",");
  }
  function bar(where, scopeFn) {
    var d = document.createElement("div"); d.className = "share-sim";
    d.innerHTML = '<button type="button" class="btn btn-ghost btn-sm">🔗 Copy simulation link</button><span class="share-msg muted" aria-live="polite"></span>';
    where.appendChild(d);
    var msg = d.querySelector(".share-msg");
    d.querySelector("button").addEventListener("click", function () {
      var u = link(scopeFn && scopeFn());
      var done = function () { msg.textContent = "Link copied. Anyone who opens it sees these exact values."; };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(u).then(done, function () { msg.textContent = u; });
      else msg.textContent = u;
      if (window.track) window.track("quantlab-share");
    });
  }
  var ex = document.getElementById("qlExplainer");
  if (ex) {   // Explainers: one bar under the explainer card; the link keeps ?t=<topic>
    bar(ex.parentNode, function () { return ex; });
    ex.parentNode.appendChild(ex.parentNode.querySelector(".share-sim"));
  } else {     // Concept Lab: one bar per card, linking that card's sliders
    [].forEach.call(root.querySelectorAll(".ql-lab-grid > .card"), function (c) { if (c.querySelector("input[type=range]")) bar(c, function () { return c; }); });
  }
  if (raw) apply();
})();
