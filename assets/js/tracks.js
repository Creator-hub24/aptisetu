/* tracks.html: no-repeat pool count and reset (data from notebook.js). */
(function () {
  var c = document.getElementById("nr-count"), r = document.getElementById("nr-reset"); if (!c || !r) return;
  function show() { var n = window.Notebook ? Notebook.seenCount() : 0; c.textContent = "Questions seen on this device: " + n; r.hidden = !n; }
  r.addEventListener("click", function () { if (window.Notebook && confirm("Start the no-repeat pool afresh? Questions you have seen can be picked again.")) { Notebook.resetSeen(); show(); } });
  show();
})();
