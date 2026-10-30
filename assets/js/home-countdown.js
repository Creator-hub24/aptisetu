/* Home page: moving "CAT 2026" countdown strip. Date comes from data-date on #cd (YYYY-MM-DD).
   Without JS the strip still shows the date. Moves only if the user has not asked for reduced motion; has a Pause button. */
(function () {
  var box = document.getElementById("cd");
  if (!box) return;
  var p = (box.getAttribute("data-date") || "").split("-");
  var target = new Date(+p[0], +p[1] - 1, +p[2]), now = new Date();
  var days = Math.round((target - new Date(now.getFullYear(), now.getMonth(), now.getDate())) / 86400000);
  var txt = days > 1 ? days + " days to go" : days === 1 ? "Tomorrow!" : days === 0 ? "Today. All the best!" : "Exam done. Results soon";
  [].forEach.call(box.querySelectorAll(".cd-left"), function (e) { e.textContent = txt; });
  var btn = document.getElementById("cd-pause");
  if (btn) btn.addEventListener("click", function () {
    var on = box.classList.toggle("cd-paused");
    btn.setAttribute("aria-pressed", String(on)); btn.textContent = on ? "Play" : "Pause";
  });
})();
