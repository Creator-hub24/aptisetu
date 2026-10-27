// Renders the printable formula sheets to assets/pdf/ (needs a local server on :8765).
// NODE_PATH=/workspace/pwtools/node_modules node tools/make_pdfs.js
const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const s of ["cat-quant", "bank-ssc-quant", "reasoning"]) {
    await p.goto(`http://localhost:8765/formula-${s}.html`, { waitUntil: "networkidle" });
    await p.emulateMedia({ media: "print", colorScheme: "light" });
    await p.pdf({ path: `assets/pdf/formula-${s}.pdf`, format: "A4", printBackground: false, margin: { top: "12mm", bottom: "12mm", left: "12mm", right: "12mm" } });
    console.log("pdf", s);
  }
  await b.close();
})();
