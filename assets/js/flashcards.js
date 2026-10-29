/* Formula flashcards (flashcards.html). Data: window.FC_DECKS from flashcards-data.js.
   Progress ("known" cards) is kept per deck in localStorage, wrapped in try/catch so the page works without it. */
(function () {
  var D = window.FC_DECKS || [];
  if (!D.length) return;
  var $ = function (id) { return document.getElementById(id); };
  var store = {
    get: function (k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var track = function (n) { try { if (window.track) window.track(n); } catch (e) {} };
  var deck, order, pos, known, missed, flipped = false;

  function keyOf(c) { return c.q; }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function saveKnown() { store.set("fc:" + deck.id, Object.keys(known)); }

  function tabs() {
    $("fc-tabs").innerHTML = D.map(function (d) {
      return '<button type="button" role="tab" class="fc-tab" data-id="' + d.id + '" aria-selected="' + (deck && d.id === deck.id) + '">' + d.name + ' <span class="fc-count">' + d.cards.length + "</span></button>";
    }).join("");
    [].forEach.call(document.querySelectorAll(".fc-tab"), function (b) {
      b.onclick = function () { open(b.getAttribute("data-id"), true); };
    });
  }

  function open(id, user) {
    deck = D.filter(function (d) { return d.id === id; })[0] || D[0];
    known = {}; (store.get("fc:" + deck.id) || []).forEach(function (k) { known[k] = 1; });
    // unknown cards first, in sheet order; known cards after them
    var all = deck.cards.map(function (_, i) { return i; });
    order = all.filter(function (i) { return !known[keyOf(deck.cards[i])]; }).concat(all.filter(function (i) { return known[keyOf(deck.cards[i])]; }));
    pos = 0; missed = {};
    store.set("fc:last", deck.id);
    if (user) { try { history.replaceState(null, "", "#" + deck.id); } catch (e) {} track("flashcards-" + deck.id); }
    $("fc-sheet").innerHTML = 'Print this deck: <a href="' + deck.sheet + '">' + deck.name + " formula sheet</a>.";
    tabs(); show();
  }

  function show() {
    var done = pos >= order.length;
    $("fc-done").hidden = !done;
    $("fc-card").hidden = done; $("fc-actions").hidden = done;
    var nk = deck.cards.filter(function (c) { return known[keyOf(c)]; }).length;
    $("fc-known").textContent = nk + " of " + deck.cards.length + " known";
    if (done) {
      var nm = Object.keys(missed).length;
      $("fc-pos").textContent = "Finished";
      $("fc-sum").textContent = nm ? nm + " card" + (nm > 1 ? "s" : "") + " to review again. " + nk + " of " + deck.cards.length + " known in this deck." : "No cards left to review. " + nk + " of " + deck.cards.length + " known in this deck.";
      $("fc-review").hidden = !nm;
      return;
    }
    var c = deck.cards[order[pos]];
    flipped = false; $("fc-card").classList.remove("flipped");
    $("fc-g1").textContent = c.g; $("fc-g2").textContent = c.g;
    $("fc-q").textContent = c.q; $("fc-a").textContent = c.a; $("fc-n").textContent = c.n || "";
    $("fc-card").setAttribute("aria-label", "Card " + (pos + 1) + ". " + c.q + ". Press to flip.");
    $("fc-pos").textContent = "Card " + (pos + 1) + " of " + order.length;
  }

  function flip() {
    if (pos >= order.length) return;
    flipped = !flipped; $("fc-card").classList.toggle("flipped", flipped);
    var c = deck.cards[order[pos]];
    $("fc-card").setAttribute("aria-label", flipped ? "Answer: " + c.a + (c.n ? ". " + c.n : "") : "Card " + (pos + 1) + ". " + c.q + ". Press to flip.");
  }
  function mark(ok) {
    if (pos >= order.length) return;
    var c = deck.cards[order[pos]], k = keyOf(c);
    if (ok) { known[k] = 1; delete missed[k]; } else { delete known[k]; missed[k] = order[pos]; }
    saveKnown(); pos++; show();
  }
  function step(d) { if (!order.length) return; pos = Math.max(0, Math.min(order.length - 1, Math.min(pos, order.length - 1) + d)); show(); }

  $("fc-card").onclick = flip;
  $("fc-know").onclick = function () { mark(true); };
  $("fc-again").onclick = function () { mark(false); };
  $("fc-next").onclick = function () { step(1); };
  $("fc-prev").onclick = function () { step(-1); };
  $("fc-shuffle").onclick = function () { order = shuffle(order.slice(Math.min(pos, order.length))); pos = 0; show(); };
  $("fc-reset").onclick = function () { known = {}; missed = {}; saveKnown(); open(deck.id, false); };
  $("fc-restart").onclick = function () { open(deck.id, false); };
  $("fc-review").onclick = function () { order = Object.keys(missed).map(function (k) { return missed[k]; }); missed = {}; pos = 0; show(); };
  document.addEventListener("keydown", function (e) {
    if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
    if (e.key === "ArrowRight") step(1);
    else if (e.key === "ArrowLeft") step(-1);
    else if (e.key === "k" || e.key === "K") mark(true);
    else if (e.key === "a" || e.key === "A") mark(false);
    else if ((e.key === " " || e.key === "Enter") && e.target === document.body) { e.preventDefault(); flip(); }
  });

  var h = (location.hash || "").replace("#", "");
  open(D.some(function (d) { return d.id === h; }) ? h : (store.get("fc:last") || D[0].id), false);
})();
