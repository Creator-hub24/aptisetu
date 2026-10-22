# Info pages, 404, sitemap and robots. Executed at the end of build_pages.py (shares its globals).
def info_head(crumb, h1, lead):
    return f"""<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / {crumb}</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">{h1}</h1><p class="muted" style="max-width:720px">{lead}</p></div></div>"""
def prose(inner): return f'<section style="padding-top:16px"><div class="container note" style="max-width:820px">{inner}</div></section>'
B=_esc.escape(BRAND)

# ---------- CONTACT ----------
btns=""
if EMAIL: btns+=f'<a class="btn" href="mailto:{A(EMAIL)}?subject={A(BRAND)}%20enquiry">📧 Email us</a>'
if FORM: btns+=f'<a class="btn btn-ghost" href="{A(FORM)}" target="_blank" rel="noopener">📝 Feedback form</a>'
reach=(f'<p>📧 <a href="mailto:{A(EMAIL)}">{_esc.escape(EMAIL)}</a></p>' if EMAIL else '')
if not btns: reach='<div class="notice">Contact details are coming soon.</div>'
page("contact.html","Contact",info_head("Contact","Contact us","Questions, feedback, a wrong answer you spotted, or a topic you'd like us to add? Get in touch.")+f"""
<section style="padding-top:16px"><div class="container" style="max-width:820px"><div class="card">
<h3>Reach us</h3>{reach}<p>📍 India (online)</p>
{f'<div class="cta-row" style="margin-bottom:0">{btns}</div>' if btns else ''}
<p class="muted" style="font-size:.9rem;margin-top:1em">If you are reporting an error in a question, please mention the page, the section and the question text so we can find it quickly. There is no contact form on this site, so nothing you type here is stored by us. (Login is used only to save practice-set progress.)</p>
</div></div></section>
""", desc=f"Contact {BRAND}: send feedback, report a wrong answer or suggest a topic.")

# ---------- ABOUT ----------
page("about.html","About",info_head("About",f"About {B}","A free practice site for Indian students preparing for aptitude tests.")+prose(f"""
<p><span data-brand>{B}</span> helps students practise Quantitative Aptitude, Logical Reasoning, DILR and VARC for competitive exams and campus placements. It is free to use. Login only to save progress and unlock levels.</p>
<h3>What's on the site</h3><ul>
<li><b>Bank / SSC / Placements track:</b> <a href="quant.html">Quant</a>, <a href="reasoning.html">Reasoning</a> and <a href="dilr.html">DILR</a> pages with concept notes, formula sheets and <a href="practice.html?exam=general">timed quizzes</a>.</li>
<li><b>CAT track:</b> <a href="cat.html">VARC, DILR and QA</a> with 40-minute sectionals, MCQ and TITA questions and CAT marking.</li>
<li><b>CUET (UG) track:</b> <a href="cuet.html">General Aptitude Test, English and Mathematics</a> with +5 / −1 marking at the real pace.</li></ul>
<h3>Our questions</h3><p>Every question and passage on the site was written by our team. None are taken from past papers or any coaching material. Each comes with a worked solution, and our build process checks the answers automatically before anything is published. If you still spot a mistake, please <a href="contact.html">tell us</a>; see our <a href="corrections.html">corrections &amp; editorial policy</a>.</p>
<h3>Independent</h3><p><span data-brand>{B}</span> is an independent site. It is not affiliated with, endorsed by or connected to the National Testing Agency (NTA), the IIMs, IBPS, SBI, SSC or any other exam body or company. Exam names are used only to describe what the practice is for.</p>
"""), desc=f"About {BRAND}: a free, independent aptitude practice site with original questions for CAT, CUET (UG), Bank, SSC and placements.")

# ---------- FAQ ----------
faqs=[("Is it free?","Yes. All notes, formula sheets and practice questions are free."),
("Do I need to sign up or log in?","Login only to save progress and unlock levels. Notes, quizzes, sectionals and Easy Quant set 1 of the CAT practice sets work without an account. Login uses a one-time link sent to your email; there is no password."),
("How do the CAT practice sets work?","Each CAT section has sets of 10 questions in three levels, Easy, then Medium, then Hard (Quant has 18 sets: Easy 1–5, Medium 6–13, Hard 14–18; VARC and DILR have 15), with a 20-minute timer (25 for DILR). A level unlocks when you have finished every ready set in the level before it. Sets we are still writing show <i>Coming soon</i>."),
("Which exams does it cover?","Three tracks: CAT (VARC, DILR, QA), CUET (UG) (General Aptitude Test, English, Mathematics), and Bank / SSC / Placements (Quant, Reasoning, DILR)."),
("How does timed mode work in the Bank / SSC quizzes?","Choose a section, an optional topic, the number of questions and the time per question (60, 90 or 120 seconds). The total time is shown as a countdown. You can move between questions, mark them for review, and see the score and worked solutions after you submit. CAT-style +3 / −1 marking is optional."),
("How do CAT sectionals work?","A CAT sectional is one section with a 40-minute countdown that submits automatically when time runs out. Marking is +3 for a correct answer, −1 for a wrong MCQ, and 0 for a wrong TITA or a blank. RC passages and DILR sets stay together."),
("How do CUET sectionals work?","Up to 50 questions at the real pace of 72 seconds per question, with +5 for a correct answer and −1 for a wrong one. Where our bank has fewer than 50 questions, the sectional is shorter but keeps the same pace."),
("What is practice mode?","On the CAT and CUET tracks, practice mode has no countdown. You pick a topic, check each answer and see the full solution straight away."),
("Are these real exam questions?","No. All questions were written by our team, in the style of each exam. They are not taken from past papers or any coaching material."),
("Is my progress saved?","Yes, but only in your own browser. The site remembers an unfinished quiz so you can resume it, your daily practice streak, and your accuracy for each topic. This is stored in your browser's local storage on this device; it is never sent to us, and it won't follow you to another phone or browser. To delete it, use <b>Reset my progress</b> on the <a href=\"practice.html\">Practice page</a>, or clear this site's data in your browser settings."),
("What is Quick start?","On the <a href=\"practice.html\">Practice page</a>, Quick start gives you 10 mixed Quant, Reasoning and DILR questions with 60 seconds each, in one tap."),
("Are you linked to NTA or the IIMs?","No. This is an independent site, not affiliated with NTA, the IIMs or any exam body. Always check official exam websites for dates and rules."),
("I found a mistake. What should I do?","Use the <b>⚑ Report an error</b> link under any question, or <a href=\"contact.html\">contact us</a> with the page and the question text. Fixes are listed on our <a href=\"corrections.html\">corrections page</a>.")]
page("faq.html","FAQ",info_head("FAQ","Frequently asked questions","Quick answers about how the site works.")+prose("".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in faqs)),
 desc=f"FAQ: how {BRAND} works. Free; login only to save progress and unlock levels. CAT, CUET (UG) and Bank / SSC tracks, timed sectionals, marking and practice mode.")

# ---------- CORRECTIONS & EDITORIAL POLICY ----------
page("corrections.html","Corrections & Editorial Policy",info_head("Corrections","Corrections &amp; editorial policy","How our questions are made, how to report a mistake, and a public record of what we fixed.")+prose(f"""
<h3>How our questions are made</h3>
<p>Every question, passage and data set on <span data-brand>{B}</span> was written by our team. None are copied from past papers, coaching material or other websites. Each question has a worked solution, and our build process checks the stored answers automatically before anything is published. We are an independent site, not affiliated with NTA, the IIMs, IBPS, SBI, SSC or any exam body.</p>
<h3>Found a mistake?</h3>
<p>Every question on a quiz page, a sectional or a practice set has a <b>⚑ Report an error</b> link. It opens an email with the question ID and page already filled in, so you only need to say what looks wrong. You can also write to us from the <a href="contact.html">Contact page</a>. A wrong answer key, an unclear question, a typo or a broken chart are all worth reporting.</p>
<h3>What we do with a report</h3>
<ul><li>We check the question and its solution again.</li>
<li>If it is wrong, we fix it and add an entry to the log below, with the date and what changed.</li>
<li>If it is correct, we will explain why where we can, and improve the solution if it was unclear.</li></ul>
<p>Practice questions are written by people and can contain mistakes. If you are preparing for an exam, please treat our solutions as a study aid and cross-check anything that surprises you.</p>
<h3>Corrections log</h3>
<p class="muted">No corrections have been published yet. When we fix a reported mistake, it will be listed here with the date, the page, and what changed.</p>
"""), desc=f"How {BRAND} writes and checks its practice questions, how to report an error, and the public corrections log.")

# ---------- PRIVACY ----------
if GC: ANALYTICS = """<h3>Analytics</h3><p>We use <a href="https://www.goatcounter.com/" target="_blank" rel="noopener">GoatCounter</a>, a privacy-friendly, open-source analytics service, to count visits. It does not set cookies and does not collect personal information. We see only aggregate numbers: which pages are viewed, the referring website, campaign tags in links (utm_ parameters), and general browser, screen-size and country statistics.</p>
<p>We also count a few named events, such as a quiz or sectional being started, finished, or submitted automatically when time runs out (for example <code>sectional-start-cat-qa</code>). These events record only the event name, not your answers, scores or anything about you. See GoatCounter's privacy policy for how it handles data.</p>"""
else: ANALYTICS = "<h3>Analytics</h3><p>We don't use analytics today. If we add visitor counts in future, we will use a privacy-friendly tool that does not use cookies or collect personal data, and we will update this page first.</p>"
page("privacy.html","Privacy Policy",info_head("Privacy","Privacy policy",f"Last updated: {_dt.date.today().strftime('%d %B %Y')}")+prose(f"""
<p>This page explains what happens to your information when you use <span data-brand>{B}</span>. In short: you can use most of the site without giving us anything. If you log in, we store your email address and your CAT practice-set results, and nothing else.</p>
<h3>Login (optional)</h3><p>Login is only needed to save progress and unlock levels in the CAT practice sets. When you log in, we use <b>Supabase</b> (our login and database provider) to send you a one-time login link and to store:</p><ul><li>your <b>email address</b> (to log you in), and</li><li>your <b>set results</b>: the section, set number, score, total and the time you finished.</li></ul><p>We use this only to show your progress and unlock levels. We don't sell it or use it for marketing. To have your account and results deleted, email <a href="mailto:{EMAIL}">{EMAIL}</a> from the address you log in with. Supabase keeps a login session in your browser's local storage while you are logged in; logging out removes it.</p>
<h3>Your quiz answers and progress</h3><p>Quizzes run in your browser. Your answers are never sent to us. The only thing sent is the final score of a CAT practice set, and only when you are logged in (see above).</p>
<p>To let you resume an unfinished quiz and see your daily streak and topic-wise accuracy, the site saves this information in your browser's <b>local storage</b> on your device. It contains only quiz data (questions in progress, your answers, dates you practised and accuracy counts), never your name or contact details, and it is not sent to us or anyone else. You can delete it at any time with the <b>Reset my progress</b> button on the <a href="practice.html">Practice page</a>, or by clearing this site's data (cookies and site data) in your browser settings.</p>
<h3>Cookies</h3><p>The site does not set cookies. Local storage (above) is kept only on your device.</p>
<h3>Third-party services</h3><ul>
<li><b>Login and saved results:</b> handled by Supabase (supabase.com) when you log in. See Supabase's privacy policy for details.</li>
<li><b>Hosting:</b> the site is hosted on GitHub Pages. GitHub may log technical information such as your IP address when your browser requests a page. See GitHub's privacy statement for details.</li>
<li><b>Fonts:</b> fonts are loaded from Google Fonts, so your browser connects to Google's servers to download them. See Google's privacy policy for details.</li>
<li><b>Email:</b> if you email us (including through a "Report an error" link, which opens your own email app with the question ID filled in), we receive your email address and message and use them only to reply.</li></ul>
{ANALYTICS}
<h3>Children</h3><p>The site is meant for students, including school students preparing for CUET (UG). Because we don't collect personal information, no information about children is collected.</p>
<h3>Changes and contact</h3><p>We'll update this page if anything changes. Questions? <a href="contact.html">Contact us</a>.</p>
"""), desc=f"Privacy policy for {BRAND}: login is optional and only stores your email and CAT practice-set results (via Supabase); no cookies. Hosted on GitHub Pages; fonts from Google Fonts.")

# ---------- TERMS ----------
page("terms.html","Terms & Disclaimer",info_head("Terms","Terms of use &amp; disclaimer","Please read these before using the site.")+prose(f"""
<h3>Educational use</h3><p><span data-brand>{B}</span> provides practice material for personal, educational use. You may use it freely to prepare for exams. Please don't copy or republish the questions, notes or solutions as your own.</p>
<h3>Original questions</h3><p>All questions, passages and solutions were written by our team. They are not past exam papers and are not taken from any coaching material.</p>
<h3>No guarantee of results</h3><p>Practising here does not guarantee any score, rank, admission or job. The difficulty and format of our questions may differ from the real exams.</p>
<h3>Accuracy</h3><p>We check answers carefully, including automatic checks when the site is built, but mistakes can still happen. The material is provided "as is". Exam patterns, syllabi and marking schemes change, so always confirm details on the official exam website.</p>
<h3>Not affiliated</h3><p><span data-brand>{B}</span> is independent. It is not affiliated with, endorsed by or connected to the National Testing Agency (NTA), the IIMs, IBPS, SBI, SSC, or any other exam body, university or company. All exam and company names belong to their owners and are used only to describe what the practice is for.</p>
<h3>External links</h3><p>Some pages link to official websites. We aren't responsible for their content.</p>
<h3>Changes</h3><p>We may update the site and these terms at any time. Questions? <a href="contact.html">Contact us</a>.</p>
"""), desc=f"Terms of use and disclaimer for {BRAND}: educational use, original questions, no guarantee of results, not affiliated with NTA, the IIMs or any exam body.")

# ---------- 404 ----------
page("404.html","Page not found",f"""<section><div class="container" style="max-width:640px;text-align:center;padding:40px 0">
<div style="font-size:3rem">🧭</div><h1>Page not found</h1><p class="muted">This page doesn't exist or has moved.</p>
<div class="cta-row" style="justify-content:center"><a class="btn" href="index.html">Go to home</a><a class="btn btn-ghost" href="practice.html">Start practising</a></div></div></section>""",
 desc=f"Page not found on {BRAND}.", noindex=True, base=True)

# ---------- AFTER 12 / AFTER GRADUATION (shared table engine: assets/js/paths.js) ----------
def paths_page(fn, title, crumb, h1, lead, chip_label, chips, search_hint, reviewed, footnote, desc, data_js):
    chip_html="".join(f'<button type="button" class="a12-chip" data-stream="{c}" aria-pressed="{"true" if c=="ALL" else "false"}">{lbl} <span class="n"></span></button>' for c,lbl in chips)
    page(fn, title, f"""
<link rel="stylesheet" href="assets/css/after12.css">
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / {crumb}</div><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">{h1}</h1><p class="muted">{lead}</p></div></div>
<section style="padding-top:16px"><div class="container">
 <div class="card a12-panel">
  <div>
   <span class="a12-lbl" id="a12-stream-lbl">{chip_label}</span>
   <div class="a12-chips" role="group" aria-labelledby="a12-stream-lbl" id="a12-streams">{chip_html}</div>
  </div>
  <div class="a12-controls">
   <div><label class="a12-lbl" for="a12-field">Field</label><select id="a12-field"><option value="">All fields</option></select></div>
   <div><label class="a12-lbl" for="a12-q">Search</label><input id="a12-q" type="search" placeholder="{search_hint}" autocomplete="off"></div>
   <div><label class="a12-lbl" for="a12-sort">Sort by</label><select id="a12-sort"><option value="field">Field</option><option value="az">Course name A to Z</option><option value="short">Shortest first</option><option value="long">Longest first</option></select></div>
  </div>
  <div class="a12-status"><p id="a12-count" aria-live="polite" class="muted"></p><button type="button" class="a12-reset" id="a12-reset">Clear all filters</button></div>
 </div>
 <div class="a12-results" id="a12-results">
  <div class="table-wrap a12-wrap"><table class="a12-table"><caption class="a12-sr">{h1}</caption>
   <thead><tr><th scope="col">Course or path</th><th scope="col">Open to</th><th scope="col">Duration</th><th scope="col">How you get in</th><th scope="col">Where it leads</th></tr></thead>
   <tbody id="a12-rows"></tbody></table></div>
 </div>
 <div class="notice" style="margin-top:20px">Exam names, eligibility rules and seat numbers change every year, and durations here are typical, not fixed. Confirm on the official website of the exam or college before you apply. Last reviewed {reviewed}.</div>
 <p class="muted" style="margin-top:12px;max-width:70ch">{footnote}</p>
</div></section>
""", desc=desc, extra=f'<script src="assets/js/{data_js}"></script><script src="assets/js/paths.js"></script>')

paths_page("after12.html", "After 12: Courses &amp; Careers", "After 12", "After 12: every path in one table",
 'Pick your Class 12 stream, narrow by field, and compare who can apply, how long each path takes, how you get in and where it leads. Already in college? See <a href="after-graduation.html">After Graduation</a>.',
 "Your Class 12 stream", [("ALL","All streams"),("M","Science (PCM)"),("B","Science (PCB)"),("C","Commerce"),("A","Arts")],
 "Try NEET, CLAT, pilot, design", "20 October 2026",
 "UPSC and state civil services start after graduation, so choose any degree you can do well in and begin preparing early.",
 "Every path after Class 12 in one table: engineering, medical, commerce, law, arts, design, defence and more. Filter by your stream and compare entry exams and careers.",
 "after12-data.js")

paths_page("after-graduation.html", "After Graduation: Courses, Exams &amp; Jobs", "After Graduation", "After graduation: every path in one table",
 'Pick your degree, narrow by field, and compare master\'s courses, government exams and jobs: who can apply, how long it takes, how you get in and where it leads. Still in school? See <a href="after12.html">After 12</a>.',
 "Your degree", [("ALL","All degrees"),("E","Engineering"),("S","Science"),("C","Commerce / BBA"),("A","Arts"),("M","Medical &amp; health"),("L","Law")],
 "Try GATE, UPSC, MBA, NET", "21 October 2026",
 "Most government exams have age limits and a fixed number of attempts, and many accept final-year students. Check the official notification early so you don't miss a window.",
 "Every path after graduation in one table: MBA, M.Tech, M.Sc, UPSC, SSC, bank exams, law, medicine, teaching, defence and jobs. Filter by your degree and compare entry exams and careers.",
 "aftergrad-data.js")

# ---------- cleanup, sitemap, robots ----------
for old in ("signup.html",):
    if os.path.exists(old): os.remove(old)
dup=[fns for d,fns in DESCS.items() if len(fns)>1]
assert not dup, ("duplicate meta descriptions", dup)
today=_dt.date.today().isoformat()
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
  + "".join(f"  <url><loc>{SITE_URL}{'' if fn=='index.html' else fn}</loc><lastmod>{today}</lastmod></url>\n" for fn,ix in PAGES if ix) + "</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
