/* Home page Open Mock strip. Times come from data-start / data-end on #om-strip (ISO with +05:30, from data/open-mock.json).
   Without JS the strip shows the date and hours. With JS: "Live now" while it is open, "Ended" after, plus the next first Sunday. */
(function () {
  var box = document.getElementById("om-strip");
  if (!box) return;
  var s = Date.parse(box.getAttribute("data-start")), e = Date.parse(box.getAttribute("data-end"));
  if (isNaN(s) || isNaN(e)) return;
  var badge = document.getElementById("om-badge"), cta = document.getElementById("om-cta"), next = document.getElementById("om-next");
  function firstSundayAfter(t) {   // first Sunday of the month after the mock, in IST
    var d = new Date(t + 5.5 * 3600000), y = d.getUTCFullYear(), m = d.getUTCMonth() + 1;
    var f = new Date(Date.UTC(y, m, 1)); f.setUTCDate(1 + (7 - f.getUTCDay()) % 7);
    return f.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
  }
  function upd() {
    var now = Date.now();
    box.classList.remove("om-live", "om-done");
    if (now >= s && now <= e) {
      box.classList.add("om-live"); badge.hidden = false; badge.textContent = "Live now";
      cta.textContent = "Start the Open Mock →";
    } else if (now > e) {
      box.classList.add("om-done"); badge.hidden = false; badge.textContent = "Ended";
      cta.textContent = "See the Open Mock";
      if (next) next.textContent = "Next Open Mock: " + firstSundayAfter(s) + " (expected), 10 am–10 pm IST. Date confirmed on the Open Mock page.";
    } else { badge.hidden = true; cta.textContent = "See the Open Mock"; }
  }
  upd(); setInterval(upd, 60000);
})();
