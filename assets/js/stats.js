// Keeps every count on the site in sync with data/questions.json
(function () {
  if (!document.querySelector("[data-stat],[data-topic]")) return;
  fetch("data/questions.json").then(r => r.json()).then(bank => {
    const all = Object.entries(bank).flatMap(([k, s]) => s.questions.map(q => [k, q.topic]));
    const set = (k, v) => document.querySelectorAll(`[data-stat="${k}"]`).forEach(e => e.textContent = v);
    set("questions", all.length);
    set("topics", new Set(all.map(([k, t]) => k + "|" + t)).size);
    Object.entries(bank).forEach(([k, s]) => set(k, s.questions.length));
    document.querySelectorAll("[data-topic]").forEach(el => {
      const n = all.filter(([, t]) => t === el.dataset.topic).length;
      const b = el.querySelector("[data-topic-count]");
      if (b) { b.textContent = n ? n + " Qs" : "Soon"; b.classList.toggle("soon", !n); }
    });
  }).catch(() => {});
})();
