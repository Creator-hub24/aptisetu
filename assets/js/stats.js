// Keeps every count on the site in sync with data/questions.json (Bank/SSC/Placements) and data/cat.json (CAT)
(function () {
  if (!document.querySelector("[data-stat],[data-topic],[data-cat-topic]")) return;
  const get = u => fetch(u).then(r => r.json()).catch(() => null);
  Promise.all([get("data/questions.json"), get("data/cat.json")]).then(([bank, cat]) => {
    const set = (k, v) => document.querySelectorAll(`[data-stat="${k}"]`).forEach(e => e.textContent = v);
    const gen = bank ? Object.entries(bank).flatMap(([k, s]) => s.questions.map(q => [k, q.topic])) : [];
    const catQ = cat ? Object.entries(cat.sections).flatMap(([k, s]) => s.questions.map(q => [k, q.topic, q.type])) : [];
    if (bank) {
      set("general", gen.length);
      Object.entries(bank).forEach(([k, s]) => set(k, s.questions.length));
      document.querySelectorAll("[data-topic]").forEach(el => {
        const n = gen.filter(([, t]) => t === el.dataset.topic).length, b = el.querySelector("[data-topic-count]");
        if (b) { b.textContent = n ? n + " Qs" : "Soon"; b.classList.toggle("soon", !n); }
      });
    }
    if (cat) {
      set("cat", catQ.length); set("cat-tita", catQ.filter(x => x[2] === "tita").length);
      set("cat-mcq", catQ.filter(x => x[2] === "mcq").length);
      set("cat-topics", new Set(catQ.map(([k, t]) => k + "|" + t)).size);
      set("cat-sets", Object.keys(cat.sets).filter(k => cat.sets[k].kind === "dilr").length);
      set("cat-passages", Object.keys(cat.sets).filter(k => cat.sets[k].kind === "passage").length);
      Object.keys(cat.sections).forEach(k => set("cat-" + k, cat.sections[k].questions.length));
      document.querySelectorAll("[data-cat-topic]").forEach(el => {
        const [s, t] = el.dataset.catTopic.split("|"), n = catQ.filter(x => x[0] === s && x[1] === t).length, b = el.querySelector("[data-topic-count]");
        if (b) { b.textContent = n ? n + " Qs" : "Soon"; b.classList.toggle("soon", !n); }
      });
    }
    if (bank && cat) {
      set("questions", gen.length + catQ.length);
      set("topics", new Set(gen.map(([k, t]) => "g|" + k + "|" + t).concat(catQ.map(([k, t]) => "c|" + k + "|" + t))).size);
    }
  });
})();
