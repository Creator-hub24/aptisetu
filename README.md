# edumaths360 – Quant, Reasoning & DILR prep portal (v0.1)

Static site (plain HTML/CSS/JS, no build step). Deployable as-is to GitHub Pages.

- **Rename brand / email:** edit `assets/js/config.js` (`BRAND`, `TAGLINE`, `EMAIL`).
- **Add questions:** edit `data/questions.json` (`answer` is the 0-based option index; optional `data` holds HTML for tables or charts).
- **Run locally:** `python3 -m http.server 8765`, then open http://localhost:8765. The quiz loads JSON via fetch, so it needs a server and won't work from file://.

Pages: index, quant, reasoning, dilr (topics, concept note, formula sheet), practice (quiz engine),
mock-tests / placements (placeholders), signup / contact (UI only, no backend).
