/* Home page: moving exam countdown strip. Exams come from data-exams on #cd (built by tools/build_pages.py).
   Without JS the strip still shows the date. Moves only if the user has not asked for reduced motion; has a Pause button. */
(function () {
  var box = document.getElementById("cd");
  if (!box) return;
  // data-exams: [[name, YYYY-MM-DD, "29 Nov 2026"], ...] in date order. Show the first exam that is not over yet;
  // when every exam in the list is over, hide the strip instead of showing a stale date.
  var list = [];
  try { list = JSON.parse(box.getAttribute("data-exams") || "[]"); } catch (e) {}
  if (!list.length) list = [["", box.getAttribute("data-date") || "", ""]];
  var now = new Date(), today = new Date(now.getFullYear(), now.getMonth(), now.getDate()), pick = null, days = 0;
  for (var i = 0; i < list.length; i++) {
    var p = String(list[i][1]).split("-"), d = Math.round((new Date(+p[0], +p[1] - 1, +p[2]) - today) / 86400000);
    if (d >= 0) { pick = list[i]; days = d; break; }
  }
  if (!pick) { box.hidden = true; return; }
  var set = function (cls, v) { if (v) [].forEach.call(box.querySelectorAll(cls), function (e) { e.textContent = v; }); };
  set(".cd-name", pick[0]); set(".cd-date", pick[2]);
  var txt = days > 1 ? days + " days to go" : days === 1 ? "Tomorrow!" : "Today. All the best!";
  set(".cd-left", txt);
  var btn = document.getElementById("cd-pause");
  if (btn) btn.addEventListener("click", function () {
    var on = box.classList.toggle("cd-paused");
    btn.setAttribute("aria-pressed", String(on)); btn.textContent = on ? "Play" : "Pause";
  });
})();
