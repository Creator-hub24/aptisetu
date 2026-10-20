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
<p class="muted" style="font-size:.9rem;margin-top:1em">If you are reporting an error in a question, please mention the page, the section and the question text so we can find it quickly. We don't have accounts or a contact form on this site, so nothing you type here is stored by us.</p>
</div></div></section>
""", desc=f"Contact {BRAND}: send feedback, report a wrong answer or suggest a topic.")

# ---------- ABOUT ----------
page("about.html","About",info_head("About",f"About {B}","A free practice site for Indian students preparing for aptitude tests.")+prose(f"""
<p><span data-brand>{B}</span> helps students practise Quantitative Aptitude, Logical Reasoning, DILR and VARC for competitive exams and campus placements. It is free to use and needs no login.</p>
<h3>What's on the site</h3><ul>
<li><b>Bank / SSC / Placements track:</b> <a href="quant.html">Quant</a>, <a href="reasoning.html">Reasoning</a> and <a href="dilr.html">DILR</a> pages with concept notes, formula sheets and <a href="practice.html?exam=general">timed quizzes</a>.</li>
<li><b>CAT track:</b> <a href="cat.html">VARC, DILR and QA</a> with 40-minute sectionals, MCQ and TITA questions and CAT marking.</li>
<li><b>CUET (UG) track:</b> <a href="cuet.html">General Aptitude Test, English and Mathematics</a> with +5 / −1 marking at the real pace.</li></ul>
<h3>Our questions</h3><p>Every question and passage on the site was written by us for practice. None are copied from past papers or coaching material. Each comes with a worked solution, and our build process checks the answers automatically before anything is published. If you still spot a mistake, please <a href="contact.html">tell us</a>.</p>
<h3>Independent</h3><p><span data-brand>{B}</span> is an independent site. It is not affiliated with, endorsed by or connected to the National Testing Agency (NTA), the IIMs, IBPS, SBI, SSC or any other exam body or company. Exam names are used only to describe what the practice is for.</p>
"""), desc=f"About {BRAND}: a free, independent aptitude practice site with original questions for CAT, CUET (UG), Bank, SSC and placements.")

# ---------- FAQ ----------
faqs=[("Is it free?","Yes. All notes, formula sheets and practice questions are free."),
("Do I need to sign up or log in?","No. There are no accounts. Open a page and start practising."),
("Which exams does it cover?","Three tracks: CAT (VARC, DILR, QA), CUET (UG) (General Aptitude Test, English, Mathematics), and Bank / SSC / Placements (Quant, Reasoning, DILR)."),
("How does timed mode work in the Bank / SSC quizzes?","Choose a section, an optional topic, the number of questions and the time per question (60, 90 or 120 seconds). The total time is shown as a countdown. You can move between questions, mark them for review, and see the score and worked solutions after you submit. CAT-style +3 / −1 marking is optional."),
("How do CAT sectionals work?","A CAT sectional is one section with a 40-minute countdown that submits automatically when time runs out. Marking is +3 for a correct answer, −1 for a wrong MCQ, and 0 for a wrong TITA or a blank. RC passages and DILR sets stay together."),
("How do CUET sectionals work?","Up to 50 questions at the real pace of 72 seconds per question, with +5 for a correct answer and −1 for a wrong one. Where our bank has fewer than 50 questions, the sectional is shorter but keeps the same pace."),
("What is practice mode?","On the CAT and CUET tracks, practice mode has no countdown. You pick a topic, check each answer and see the full solution straight away."),
("Are these real exam questions?","No. All questions were written by us for practice, in the style of each exam. They are not taken from past papers."),
("Is my progress saved?","Not at the moment. Results are shown at the end of each quiz but are not stored."),
("Are you linked to NTA or the IIMs?","No. This is an independent site, not affiliated with NTA, the IIMs or any exam body. Always check official exam websites for dates and rules."),
("I found a mistake. What should I do?","Please <a href=\"contact.html\">contact us</a> with the page and the question text.")]
page("faq.html","FAQ",info_head("FAQ","Frequently asked questions","Quick answers about how the site works.")+prose("".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in faqs)),
 desc=f"FAQ: how {BRAND} works. Free, no login, CAT, CUET (UG) and Bank / SSC tracks, timed sectionals, marking and practice mode.")

# ---------- PRIVACY ----------
if GC: ANALYTICS = """<h3>Analytics</h3><p>We use <a href="https://www.goatcounter.com/" target="_blank" rel="noopener">GoatCounter</a>, a privacy-friendly, open-source analytics service, to count visits. It does not set cookies and does not collect personal information. We see only aggregate numbers: which pages are viewed, the referring website, campaign tags in links (utm_ parameters), and general browser, screen-size and country statistics.</p>
<p>We also count a few named events, such as a quiz or sectional being started, finished, or submitted automatically when time runs out (for example <code>sectional-start-cat-qa</code>). These events record only the event name, not your answers, scores or anything about you. See GoatCounter's privacy policy for how it handles data.</p>"""
else: ANALYTICS = "<h3>Analytics</h3><p>We don't use analytics today. If we add visitor counts in future, we will use a privacy-friendly tool that does not use cookies or collect personal data, and we will update this page first.</p>"
page("privacy.html","Privacy Policy",info_head("Privacy","Privacy policy",f"Last updated: {_dt.date.today().strftime('%d %B %Y')}")+prose(f"""
<p>This page explains what happens to your information when you use <span data-brand>{B}</span>. In short: we don't collect personal information.</p>
<h3>No accounts, no forms</h3><p>There are no sign-ups or logins, and the site has no forms that send information to us. You don't need to give us your name, email or phone number to use it.</p>
<h3>Your quiz answers</h3><p>Quizzes run entirely in your browser. Your answers and scores are not sent to us or stored by us.</p>
<h3>Cookies</h3><p>The site does not set cookies.</p>
<h3>Third-party services</h3><ul>
<li><b>Hosting:</b> the site is hosted on GitHub Pages. GitHub may log technical information such as your IP address when your browser requests a page. See GitHub's privacy statement for details.</li>
<li><b>Fonts:</b> fonts are loaded from Google Fonts, so your browser connects to Google's servers to download them. See Google's privacy policy for details.</li>
<li><b>Email:</b> if you email us, we receive your email address and message and use them only to reply.</li></ul>
{ANALYTICS}
<h3>Children</h3><p>The site is meant for students, including school students preparing for CUET (UG). Because we don't collect personal information, no information about children is collected.</p>
<h3>Changes and contact</h3><p>We'll update this page if anything changes. Questions? <a href="contact.html">Contact us</a>.</p>
"""), desc=f"Privacy policy for {BRAND}: no accounts, no cookies and no personal data collected. Hosted on GitHub Pages; fonts from Google Fonts.")

# ---------- TERMS ----------
page("terms.html","Terms & Disclaimer",info_head("Terms","Terms of use &amp; disclaimer","Please read these before using the site.")+prose(f"""
<h3>Educational use</h3><p><span data-brand>{B}</span> provides practice material for personal, educational use. You may use it freely to prepare for exams. Please don't copy or republish the questions, notes or solutions as your own.</p>
<h3>Original questions</h3><p>All questions, passages and solutions were written by us for practice. They are not past exam papers and are not copied from coaching material.</p>
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

# ---------- cleanup, sitemap, robots ----------
for old in ("signup.html",):
    if os.path.exists(old): os.remove(old)
dup=[fns for d,fns in DESCS.items() if len(fns)>1]
assert not dup, ("duplicate meta descriptions", dup)
today=_dt.date.today().isoformat()
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
  + "".join(f"  <url><loc>{SITE_URL}{'' if fn=='index.html' else fn}</loc><lastmod>{today}</lastmod></url>\n" for fn,ix in PAGES if ix) + "</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
