// Keeps every count on the site in sync with the question banks, via the small data/stats.json
// (written by tools/split_data.py when tools/build_questions.py runs).
(function () {
  if (!document.querySelector("[data-stat],[data-topic],[data-cat-topic],[data-cuet-topic],[data-cuet-part]")) return;
  fetch("data/stats.json").then(r => r.json()).then(st => {
    document.querySelectorAll("[data-stat]").forEach(e => { const v = st.stat[e.dataset.stat]; if (v != null) e.textContent = v; });
    const badge = (el, n) => { const b = el.querySelector("[data-topic-count]"); if (b) { b.textContent = n ? n + " Qs" : "Soon"; b.classList.toggle("soon", !n); } };
    document.querySelectorAll("[data-topic]").forEach(el => badge(el, st.topic[el.dataset.topic] || 0));
    document.querySelectorAll("[data-cat-topic]").forEach(el => badge(el, st.catTopic[el.dataset.catTopic] || 0));
    document.querySelectorAll("[data-cuet-topic]").forEach(el => badge(el, st.cuetTopic[el.dataset.cuetTopic] || 0));
    document.querySelectorAll("[data-cuet-part]").forEach(el => { el.textContent = st.cuetPart[el.dataset.cuetPart] || 0; });
  }).catch(() => {});
})();
