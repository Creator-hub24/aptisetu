# v2 pages: Tracks & practice, Mistakes notebook. Executed from pages_info.py before the sitemap (shares build_pages.py globals).
page("tracks.html","Tracks &amp; Practice: CAT, CUET, Bank, SSC and Placements",ehead([(None,"Tracks &amp; Practice")],"Tracks &amp; practice",
 "Every practice track in one place. Exam facts below come from each exam's official notice; the track pages cite the source and date.")+"""
<section style="padding-top:12px"><div class="container">
 <div class="grid g2 tr-tools">
  <div class="card tr-tool"><h2>Solution language</h2><p class="muted">Bank &amp; SSC questions have a worked solution in English and in Hindi. Your choice is used in quizzes and on question pages.</p>
   <div class="lang-toggle" role="group" aria-label="Solution language"><span class="muted">Solution in:</span><button type="button" data-lang="en">EN</button><button type="button" data-lang="hi" lang="hi">हिंदी</button></div></div>
  <div class="card tr-tool"><h2>No-repeat pool <span class="tr-on">On</span></h2><p class="muted">Quizzes and sectionals pick questions you have not been shown yet first, and repeat only when a pool runs out. The Daily 10 is the same for everyone, so it is not affected.</p>
   <p id="nr-count" class="tr-count" aria-live="polite">Questions seen on this device: 0</p><button type="button" class="btn btn-ghost btn-sm" id="nr-reset">Start the pool afresh</button></div>
 </div>

 <div class="grid g2 tr-grid">
  <article class="card trk trk-cat"><span class="tc-tag">MBA entrance</span><h2>CAT &amp; OMETs</h2>
   <div class="tags"><span class="tag">VARC ≈ 24 Q</span><span class="tag">DILR ≈ 22 Q</span><span class="tag">QA ≈ 22 Q</span><span class="tag">40 min a section</span><span class="tag">+3 / −1, TITA 0</span></div>
   <p class="muted">Levelled sets, 40-minute sectionals, full mocks and the monthly Open Mock. Pattern as in the CAT 2026 bulletin; see the <a href="cat.html">CAT page</a> for the source.</p>
   <ul class="tr-links"><li><a href="cat-quant-sets.html">QA sets</a></li><li><a href="cat-dilr-sets.html">DILR sets</a></li><li><a href="cat-varc-sets.html">VARC sets</a></li><li><a href="cat-practice.html">Sectionals &amp; topic practice</a></li><li><a href="mock-tests.html">Mock tests</a></li><li><a href="open-mock.html">Open Mock</a></li><li><a href="cat-practice.html?daily=1">Today's 10</a></li></ul></article>
  <article class="card trk trk-cuet"><span class="tc-tag">Central universities</span><h2>CUET (UG)</h2>
   <div class="tags"><span class="tag">50 compulsory MCQs a paper</span><span class="tag">60 min a paper</span><span class="tag">+5 / −1</span></div>
   <p class="muted">General Aptitude Test, English and Mathematics at the real pace. Pattern from NTA's CUET (UG) 2026 bulletin; see the <a href="cuet.html">CUET page</a> for the source.</p>
   <ul class="tr-links"><li><a href="cuet-practice.html">Sectionals &amp; topic practice</a></li><li><a href="cuet-practice.html?daily=1">Today's 10</a></li><li><a href="q/index.html">Question bank</a></li></ul></article>
  <article class="card trk trk-bank"><span class="tc-tag">Bank · SSC</span><h2>Bank &amp; SSC <span lang="hi" class="tr-hi">हिंदी समाधान</span></h2>
   <div class="tags"><span class="tag">Quant</span><span class="tag">Reasoning</span><span class="tag">Data interpretation</span><span class="tag">EN + हिंदी solutions</span></div>
   <p class="muted">Timed quizzes with 60, 90 or 120 seconds a question. Each exam page lists the official pattern with its source.</p>
   <ul class="tr-links"><li><a href="practice.html?exam=general">Timed quiz</a></li><li><a href="ibps-po.html">IBPS PO</a></li><li><a href="ibps-clerk.html">IBPS Clerk</a></li><li><a href="sbi-po.html">SBI PO</a></li><li><a href="ssc-cgl.html">SSC CGL</a></li><li><a href="ssc-chsl.html">SSC CHSL</a></li><li><a href="practice.html?daily=1">Today's 10</a></li></ul></article>
  <article class="card trk trk-pl"><span class="tc-tag">Campus hiring</span><h2>Placements</h2>
   <div class="tags"><span class="tag">Numerical ability</span><span class="tag">Reasoning</span><span class="tag">DI</span></div>
   <p class="muted">Topic practice for the aptitude round of IT-services hiring tests. Patterns change, so check the company's official hiring page. Not affiliated with any company.</p>
   <ul class="tr-links"><li><a href="placements.html">Placement prep</a></li><li><a href="practice.html?section=quant">Quant quiz</a></li><li><a href="practice.html?section=reasoning">Reasoning quiz</a></li></ul></article>
 </div>
 <p class="muted tr-note">Cutoffs are not listed here. We only publish a number when we can cite an official, dated source for it; check each exam body's result notice for cutoffs.</p>
 <div class="cta-row"><a class="btn" href="practice.html">Start a free quiz →</a><a class="btn btn-ghost" href="mistakes.html">Mistakes notebook</a></div>
</div></section>
""",desc="All AptiSetu practice tracks: CAT and OMETs, CUET (UG), Bank and SSC with Hindi solutions, and campus placements, with official exam patterns and a no-repeat question pool.",
 extra='<script src="assets/js/sol-lang.js"></script>\n<script src="assets/js/tracks.js"></script>')

page("mistakes.html","Mistakes notebook",ehead([(None,"Mistakes notebook")],"Mistakes notebook",
 "Every question you got wrong in a quiz, sectional, set or Daily 10 lands here. Get it right in a later attempt and it leaves the notebook. Kept in this browser only.")+"""
<section style="padding-top:12px"><div class="container" style="max-width:860px">
 <div class="mk-bar"><p id="mk-sum" class="mk-sum" aria-live="polite">Loading…</p>
  <label class="qf-dl">Exam <select id="mk-exam"><option value="">All</option><option value="cat">CAT</option><option value="cuet">CUET (UG)</option><option value="general">Bank / SSC</option></select></label></div>
 <ol class="mk-list" id="mk-list"></ol>
 <div class="card mk-empty" id="mk-empty" hidden><h2>No mistakes yet</h2><p class="muted">Take a quiz; any question you answer wrongly is saved here with a link to its worked solution.</p><a class="btn" href="practice.html?daily=1">Start today's 10</a></div>
 <div class="cta-row mk-tools" id="mk-tools" hidden><a class="btn btn-ghost" href="login.html#backup">Move to another device</a><button type="button" class="btn btn-ghost" id="mk-clear">Clear notebook</button></div>
</div></section>
""",desc="Your AptiSetu mistakes notebook: questions you answered wrongly, with links to their worked solutions.",noindex=True,extra='<script src="assets/js/mistakes.js"></script>')
