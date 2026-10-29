/* Contact page: builds a pre-filled email for a report. Nothing is sent or stored by the page itself. */
(function () {
  var f = document.getElementById("rp-form");
  if (!f) return;
  var email = (window.SITE && window.SITE.EMAIL) || "";
  var $ = function (id) { return document.getElementById(id); }, msg = $("rp-msg");
  try { var q = new URLSearchParams(location.search).get("q"); if (q && /^[\w .\/-]{1,120}$/.test(q)) $("rp-qid").value = q; } catch (e) {}
  function payload() {
    var type = $("rp-type").value, qid = $("rp-qid").value.trim(), body = $("rp-body").value.trim();
    var subject = "AptiSetu: " + type + (qid ? " (" + qid + ")" : "");
    var text = "Type: " + type + "\nQuestion ID or page: " + (qid || "not given") + "\n\n" + body;
    return { subject: subject, text: text, body: body };
  }
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var p = payload();
    if (!p.body) { msg.textContent = "Please add a few words in Details first."; $("rp-body").focus(); return; }
    location.href = "mailto:" + email + "?subject=" + encodeURIComponent(p.subject) + "&body=" + encodeURIComponent(p.text);
    msg.textContent = "Your email app should open now. If it doesn't, use Copy text and send it to " + email + ".";
    try { if (window.track) window.track("contact-report-email"); } catch (e2) {}
  });
  $("rp-copy").addEventListener("click", function () {
    var p = payload();
    if (!p.body) { msg.textContent = "Please add a few words in Details first."; $("rp-body").focus(); return; }
    var all = p.subject + "\n\n" + p.text;
    var done = function () { msg.textContent = "Copied. Paste it into an email to " + email + "."; };
    var fallback = function () {
      var t = document.createElement("textarea"); t.value = all; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select();
      var ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(t);
      msg.textContent = ok ? "Copied. Paste it into an email to " + email + "." : "Couldn't copy automatically. Select the text in Details and copy it.";
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(all).then(done, fallback); else fallback();
  });
})();
