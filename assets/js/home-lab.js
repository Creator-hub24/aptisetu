/* Home page: live Quant Lab preview (two pipes filling one tank). Exact fractions; the link opens the same values in Concept Lab. */
(function () {
  var a = document.getElementById("pk-a"), b = document.getElementById("pk-b");
  if (!a || !b) return;
  var $ = function (id) { return document.getElementById(id); };
  function gcd(x, y) { return y ? gcd(y, x % y) : x; }
  function frac(n, d) { var g = gcd(n, d); n /= g; d /= g; return d === 1 ? String(n) : n + "/" + d; }
  function hm(n, d) { var mins = Math.round(n * 60 / d), h = Math.floor(mins / 60), m = mins % 60; return (h ? h + " h" : "") + (h && m ? " " : "") + (m ? m + " min" : ""); }
  function draw() {
    var A = +a.value, B = +b.value, n = A + B, d = A * B;      // together per hour = (A+B)/(AB); time = AB/(A+B)
    $("pk-ao").textContent = A; $("pk-bo").textContent = B;
    var T = d / n, max = 20;
    $("pk-ba").style.width = (A / max * 100) + "%"; $("pk-bb").style.width = (B / max * 100) + "%"; $("pk-bt").style.width = (T / max * 100) + "%";
    var tf = frac(d, n), exact = tf.indexOf("/") < 0;
    $("pk-out").innerHTML = "Together they fill 1/" + A + " + 1/" + B + " = " + frac(n, d) + " of the tank an hour, so <b>" + tf + " h</b>" + (exact ? "" : " (about " + hm(d, n) + ")") + ".";
    $("pk-link").href = "quant-lab-concept-lab.html?s=twA:" + A + ",twB:" + B + ",twC:0";
  }
  a.addEventListener("input", draw); b.addEventListener("input", draw); draw();
})();
