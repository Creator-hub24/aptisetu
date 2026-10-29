/* Login page: move local progress between devices with a backup code (no account).
   Only AptiSetu progress keys are exported or restored; login sessions and test-only keys are never touched. */
(function () {
  var $ = function (id) { return document.getElementById(id); };
  if (!$("bk-make")) return;
  var ALLOW = /^(aptiprep\.progress\.v1|aptiprep\.resume\.v1\.|aptisetu\.history$|aptisetu\.quantlab\.v1$|aptisetu\.sol-lang$|aptisetu\.goal$|fc:)/;
  var MAX = 1500000, msg = $("bk-msg"), pending = null;
  var say = function (t) { msg.textContent = t; };
  function collect() {
    var data = {};
    for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k && ALLOW.test(k)) data[k] = localStorage.getItem(k); }
    return data;
  }
  function encode(o) { return "APTI1." + btoa(unescape(encodeURIComponent(JSON.stringify(o)))); }
  function decode(s) {
    s = String(s || "").replace(/\s+/g, "");
    if (s.indexOf("APTI1.") !== 0) throw new Error("This is not an AptiSetu backup code.");
    if (s.length > MAX) throw new Error("This code is too long to be an AptiSetu backup.");
    var o = JSON.parse(decodeURIComponent(escape(atob(s.slice(6)))));
    if (!o || o.app !== "aptisetu" || o.v !== 1 || typeof o.data !== "object") throw new Error("This code could not be read.");
    var clean = {};
    Object.keys(o.data).forEach(function (k) { if (ALLOW.test(k) && typeof o.data[k] === "string") clean[k] = o.data[k]; });
    return { at: o.at, data: clean };
  }
  $("bk-make").addEventListener("click", function () {
    try {
      var data = collect(), n = Object.keys(data).length;
      if (!n) { $("bk-code").value = ""; say("There is no saved progress in this browser yet. Practise a little, then come back."); return; }
      $("bk-code").value = encode({ app: "aptisetu", v: 1, at: new Date().toISOString().slice(0, 10), data: data });
      say("Code ready (" + n + " saved item" + (n > 1 ? "s" : "") + "). Copy it and paste it on your other device.");
    } catch (e) { say("This browser is not letting the site read its saved progress (for example in a private window)."); }
  });
  $("bk-copy").addEventListener("click", function () {
    var t = $("bk-code"); if (!t.value) { say("Make a backup code first."); return; }
    var ok = function () { say("Copied."); };
    var fb = function () { t.focus(); t.select(); var c = false; try { c = document.execCommand("copy"); } catch (e) {} say(c ? "Copied." : "Select the code and copy it."); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t.value).then(ok, fb); else fb();
  });
  $("bk-check").addEventListener("click", function () {
    try {
      pending = decode($("bk-code").value);
      var n = Object.keys(pending.data).length;
      if (!n) { pending = null; say("This code has no progress in it."); return; }
      $("bk-preview").textContent = "This code has " + n + " saved item" + (n > 1 ? "s" : "") + (pending.at ? ", made on " + pending.at : "") + ". Restoring replaces the same items in this browser.";
      $("bk-confirm").hidden = false; say("");
    } catch (e) { pending = null; $("bk-confirm").hidden = true; say(e.message && /AptiSetu|code/.test(e.message) ? e.message : "This code could not be read. Copy the whole code again."); }
  });
  $("bk-cancel").addEventListener("click", function () { pending = null; $("bk-confirm").hidden = true; say("Nothing was changed."); });
  $("bk-apply").addEventListener("click", function () {
    if (!pending) return;
    try {
      Object.keys(pending.data).forEach(function (k) { localStorage.setItem(k, pending.data[k]); });
      $("bk-confirm").hidden = true; say("Progress restored on this device.");
      try { if (window.track) window.track("backup-restore"); } catch (e) {}
    } catch (e) { say("This browser would not save the progress (storage may be full or blocked)."); }
    pending = null;
  });
})();
