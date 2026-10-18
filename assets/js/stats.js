// Keeps every count on the site in sync with data/questions.json (Bank/SSC/Placements) data/cat.json (CAT) and data/cuet.json (CUET UG)
(function () {
  if (!document.querySelector("[data-stat],[data-topic],[data-cat-topic],[data-cuet-topic]")) return;
  const get = u => fetch(u).then(r => r.json()).catch(() => null);
  Promise.all([get("data/questions.json"), get("data/cat.json"), get("data/cuet.json")]).then(([bank, cat, cuet]) => {
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
    const uQ = cuet ? Object.entries(cuet.sections).flatMap(([k, s]) => s.questions.map(q => [k, q.part, q.topic, q.source === "general"])) : [];
    if (cuet) {
      set("cuet", uQ.length); set("cuet-original", uQ.filter(x => !x[3]).length); set("cuet-shared", uQ.filter(x => x[3]).length);
      Object.keys(cuet.sections).forEach(k => set("cuet-" + k, cuet.sections[k].questions.length));
      document.querySelectorAll("[data-cuet-part]").forEach(el => { const [s, p] = el.dataset.cuetPart.split("|"); el.textContent = uQ.filter(x => x[0] === s && x[1] === p).length; });
      document.querySelectorAll("[data-cuet-topic]").forEach(el => {
        const [s, p, t] = el.dataset.cuetTopic.split("|"), n = uQ.filter(x => x[0] === s && x[1] === p && x[2] === t).length, b = el.querySelector("[data-topic-count]");
        if (b) { b.textContent = n ? n + " Qs" : "Soon"; b.classList.toggle("soon", !n); }
      });
    }
    if (bank && cat && cuet) {
      // unique questions: CUET items shared from the general bank are counted once
      set("questions", gen.length + catQ.length + uQ.filter(x => !x[3]).length);
      set("topics", new Set(gen.map(([k, t]) => "g|" + k + "|" + t).concat(catQ.map(([k, t]) => "c|" + k + "|" + t), uQ.map(([k, p, t]) => "u|" + k + "|" + p + "|" + t))).size);
    }
  });
})();
