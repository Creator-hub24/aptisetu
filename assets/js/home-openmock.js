/* Home page Open Mock strip. Times come from data-start / data-end on #om-strip (ISO with +05:30, from data/open-mock.json).
   Without JS the strip shows the date and hours. With JS: "Live now" while it is open, "Ended" after, plus the next Sunday.
   On a Sunday, today's edition stays up until 10 pm IST; after that the next Sunday is shown. */
(function () {
  var box = document.getElementById("om-strip");
  if (!box) return;
  var s = Date.parse(box.getAttribute("data-start")), e = Date.parse(box.getAttribute("data-end"));
  if (isNaN(s) || isNaN(e)) return;
  var badge = document.getElementById("om-badge"), cta = document.getElementById("om-cta"), next = document.getElementById("om-next");
  function nextSunday(t) {   // next Sunday in IST; if t is a Sunday at or before 10 pm IST, return that Sunday
    var d = new Date(t + 5.5 * 3600000);
    var dow = d.getUTCDay();
    var pastEnd = dow !== 0 || d.getUTCHours() > 22 || (d.getUTCHours() === 22 && (d.getUTCMinutes() > 0 || d.getUTCSeconds() > 0 || d.getUTCMilliseconds() > 0));
    var add = pastEnd ? ((7 - dow) % 7 || 7) : 0;
    var f = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() + add));
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
      if (next) next.textContent = "Next Open Mock: " + nextSunday(now) + " (expected), 10 am–10 pm IST. Date confirmed on the Open Mock page.";
    } else { badge.hidden = true; cta.textContent = "See the Open Mock"; }
  }
  upd(); setInterval(upd, 60000);
})();
