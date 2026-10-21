import os, json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
QB = json.load(open("data/questions.json"))
import sys; sys.path.insert(0, "tools"); from formulas import FORMULAS
CB = json.load(open("data/cat.json"))
UB = json.load(open("data/cuet.json"))
UQ = {k: s["questions"] for k, s in UB["sections"].items()}
NQ_CUET_ORIG = sum(1 for v in UQ.values() for q in v if q.get("source") != "general")
NQ_CUET_SHARED = sum(1 for v in UQ.values() for q in v if q.get("source") == "general")
CUETN = {k: len(v) for k, v in UQ.items()}
NQ_GEN = sum(len(s["questions"]) for s in QB.values())
NQ_CAT = sum(len(s["questions"]) for s in CB["sections"].values())
NQ = NQ_GEN + NQ_CAT + NQ_CUET_ORIG   # unique questions: shared CUET items are counted once, in the general bank
NT_CAT = len({(k, q["topic"]) for k, s in CB["sections"].items() for q in s["questions"]})
CATN = {k: len(s["questions"]) for k, s in CB["sections"].items()}
CAT_TITA = sum(1 for s in CB["sections"].values() for q in s["questions"] if q["type"] == "tita")
# exam relevance tags for general topic cards (default: CAT + Bank-SSC)
BANK_ONLY = {"Syllogisms","Blood Relations","Coding-Decoding","Direction Sense","Number & Letter Series","Odd One Out","Clocks & Calendars","Alphabet Test","Inequalities","Ranking & Order"}
def exam_tag(topic): return ("Bank-SSC","tag-bank") if topic in BANK_ONLY else ("CAT + Bank-SSC","tag-both")
NT = len({(k, q["topic"]) for k, s in QB.items() for q in s["questions"]}) + NT_CAT + len({(k, q["part"], q["topic"]) for k, v in UQ.items() for q in v})
import re as _re, html as _esc, datetime as _dt
def _cfg():
    t=open("assets/js/config.js").read()
    return {k:v for k,v in _re.findall(r'^\s*([A-Z_]+):\s*"((?:[^"\\]|\\.)*)"', t, _re.M)}
CFG=_cfg()
BRAND=CFG["BRAND"]; TAGLINE=CFG.get("TAGLINE",""); EMAIL=CFG.get("EMAIL",""); FORM=CFG.get("GOOGLE_FORM_URL",""); GC=CFG.get("GOATCOUNTER","").strip().lower()
assert not GC or _re.fullmatch(r"[a-z0-9][a-z0-9-]*", GC), "GOATCOUNTER must be just the code, e.g. aptisetu"
SITE_URL=CFG["SITE_URL"].rstrip("/")+"/"
from urllib.parse import urlparse as _up
BASE_PATH=_up(SITE_URL).path or "/"
YEAR=_dt.date.today().year
# ---------- Content-Security-Policy (meta tag on every page) ----------
_ph=lambda v: (not v) or v.startswith("YOUR_")
SB_URL=CFG.get("SUPABASE_URL",""); SB_ORIGIN="" if _ph(SB_URL) else "{0.scheme}://{0.netloc}".format(_up(SB_URL))
assert not SB_ORIGIN or _re.fullmatch(r"https://[a-z0-9.-]+", SB_ORIGIN), "SUPABASE_URL must be https://<project>.supabase.co"
CSP="; ".join([
    "default-src 'self'",
    "script-src 'self'" + (" https://gc.zgo.at" if GC else ""),
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src https://fonts.gstatic.com",
    "img-src 'self' data:" + (f" https://{GC}.goatcounter.com" if GC else ""),
    "connect-src 'self'" + (f" {SB_ORIGIN}" if SB_ORIGIN else "") + (f" https://{GC}.goatcounter.com" if GC else ""),
    "base-uri 'self'", "form-action 'self'", "object-src 'none'"])
import shutil as _sh
_sh.rmtree("assets/js/page", ignore_errors=True); os.makedirs("assets/js/page")
def externalize(fn, html):
    """CSP: script-src 'self' forbids inline scripts, so every inline <script> becomes assets/js/page/<page>-<n>.js."""
    n=[0]
    def rep(m):
        n[0]+=1; name=f"assets/js/page/{fn[:-5]}-{n[0]}.js"
        open(name,"w").write(m.group(1).strip()+"\n"); return f'<script src="{name}"></script>'
    html=_re.sub(r"<script>(.*?)</script>", rep, html, flags=_re.S)
    assert not _re.search(r"<script(?![^>]*\bsrc=)[^>]*>", html), ("inline script left", fn)
    m=_re.search(r"<[a-zA-Z][^<>]*\son[a-z]+\s*=\s*[\"']", html); assert not m, ("inline event handler", fn, m and m.group(0)[:80])
    return html
A=lambda s: _esc.escape(s, quote=True)
PAGES=[]   # (fn, indexed)
TITLES={}
GC_TAG=(f'<script data-goatcounter="https://{GC}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n    ' if GC else "")
def footer_html():
    contact=f'<a href="contact.html">Contact us</a>'+(f'<a href="mailto:{A(EMAIL)}">{_esc.escape(EMAIL)}</a>' if EMAIL else '')
    return f"""<div class="container footer-grid">
      <div><a href="index.html" class="logo"><img src="assets/img/favicon.svg" alt="" width="34" height="34" class="logo-mark"><span data-brand>{_esc.escape(BRAND)}</span></a>
        <p class="muted">Free Quant, Reasoning, DILR and VARC practice for CAT, CUET, Bank, SSC and campus placements. Not affiliated with NTA, the IIMs or any exam body.</p></div>
      <div><h4>Learn</h4><a href="quant.html">Quantitative Aptitude</a><a href="reasoning.html">Logical Reasoning</a><a href="dilr.html">DILR</a><a href="cat.html">CAT track</a><a href="cuet.html">CUET (UG) track</a><a href="varc.html">VARC</a></div>
      <div><h4>Practice</h4><a href="cat-practice.html">CAT sectionals</a><a href="cuet-practice.html">CUET sectionals</a><a href="practice.html?exam=general">Bank / SSC quizzes</a><a href="practice.html?section=mixed">Mixed practice</a></div>
      <div><h4>About</h4><a href="about.html">About</a><a href="faq.html">FAQ</a>{contact}<a href="privacy.html">Privacy</a><a href="terms.html">Terms &amp; disclaimer</a></div>
    </div>
    {GC_TAG}<div class="container copyright">© {YEAR} <span data-brand>{_esc.escape(BRAND)}</span>. All rights reserved.</div>"""
def page(fn, title, body, desc="Quantitative Aptitude, Logical Reasoning and DILR prep for CAT, Bank, SSC, GMAT and campus placements.", extra="", noindex=False, base=False):
    title=_esc.unescape(title)
    full=f"{title} | {BRAND}" if title else f"{BRAND}: {TAGLINE}"
    assert full not in TITLES.values(), ("duplicate title", fn)
    TITLES[fn]=full; DESCS.setdefault(desc,[]).append(fn)
    url=SITE_URL+("" if fn=="index.html" else fn)
    img=SITE_URL+"assets/img/og-image.png"
    body=body.replace("<span data-brand></span>", f"<span data-brand>{_esc.escape(BRAND)}</span>")
    robots='<meta name="robots" content="noindex">\n' if noindex else ''
    basetag=f'<base href="{BASE_PATH}">\n' if base else ''
    canon='' if fn=="404.html" else f'<link rel="canonical" href="{url}">\n'
    html=f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
{basetag}<title>{A(full)}</title>
<meta name="description" content="{A(desc)}">
{robots}{canon}<meta name="theme-color" content="#0B1F3A">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml"><link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{A(BRAND)}"><meta property="og:title" content="{A(full)}"><meta property="og:description" content="{A(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{A(full)}"><meta name="twitter:description" content="{A(desc)}"><meta name="twitter:image" content="{img}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header id="site-header"></header>
<main>
{body}
</main>
<footer id="site-footer">{footer_html()}</footer>
<script src="assets/js/config.js"></script>
<script src="assets/js/layout.js"></script>
<script src="assets/js/auth.js"></script>
<script src="assets/js/stats.js"></script>
{extra}
</body>
</html>
"""
    open(fn,"w").write(externalize(fn, html))
    if fn!="404.html": PAGES.append((fn, not noindex))
DESCS={}

# ---------- LANDING ----------
page("index.html","", f"""
<section class="hero"><div class="container hero-grid">
 <div>
  <span class="pill">🇮🇳 CAT · CUET · Bank · SSC · Placements</span>
  <h1>Master <span class="grad">Quant, Reasoning, DILR &amp; VARC</span> the smart way</h1>
  <p class="lead">Short concept notes, formula sheets and timed practice with worked solutions, for bank, SSC and placement tests, plus a separate CAT track with VARC, DILR and QA sectionals.</p>
  <div class="cta-row hero-cta"><a href="practice.html" class="btn">Start a free quiz →</a><a href="#sections" class="btn btn-ghost">Explore topics</a></div>
  <div class="stats"><div><b>3</b><span>Exam tracks</span></div><div><b data-stat="topics">{NT}</b><span>Topics</span></div><div><b data-stat="questions">{NQ}</b><span>Practice questions</span></div></div>
 </div>
 <div class="hero-card" id="sample">
  <div class="q-meta"><span>Try one · Quant · Time &amp; Work</span><span class="timer-chip">Sample</span></div>
  <p style="font-weight:600;margin:.2em 0 .6em">A finishes a job in 12 days, B in 18 days. Working together, how many days do they need?</p>
  <div class="sample-opts"><button type="button" class="mini-opt" data-ok="0">A. 6 days</button><button type="button" class="mini-opt" data-ok="1">B. 7.2 days</button><button type="button" class="mini-opt" data-ok="0">C. 7.5 days</button><button type="button" class="mini-opt" data-ok="0">D. 15 days</button></div>
  <div id="sample-fb" class="sample-fb hidden" aria-live="polite"></div>
 </div>
</div></section>

<section><div class="container">
 <div class="section-head"><h2>Who is <span data-brand></span> for?</h2><p class="muted">One place to practise for the aptitude tests you'll face.</p></div>
 <div class="grid g4 m2 compact">
  <div class="card"><div class="icon">🎯</div><h3>MBA aspirants</h3><p class="muted">CAT, XAT, SNAP, NMAT and GMAT-style Quant &amp; DILR.</p></div>
  <div class="card"><div class="icon">🏦</div><h3>Bank &amp; SSC</h3><p class="muted">IBPS, SBI, SSC CGL/CHSL arithmetic and reasoning.</p></div>
  <div class="card"><div class="icon">💼</div><h3>Campus placements</h3><p class="muted">Aptitude rounds like TCS NQT, Infosys and Accenture.</p></div>
  <div class="card"><div class="icon">🎓</div><h3>CUET (UG)</h3><p class="muted">General Aptitude Test, English and Maths for central university admissions.</p></div>
 </div>
</div></section>

<section id="sections" class="alt"><div class="container">
 <div class="section-head"><h2>Bank, SSC &amp; placements: three sections</h2><p class="muted">Start with the concepts, revise with the formula sheet, then test yourself against the clock.</p></div>
 <div class="grid g3">
  <div class="card sec-card" style="--c:var(--quant)"><div class="icon">➗</div><h3>Quantitative Aptitude</h3>
   <div class="tags"><span class="tag">Percentages</span><span class="tag">Profit &amp; Loss</span><span class="tag">TSD</span><span class="tag">Number System</span><span class="tag">Algebra</span><span class="tag">Geometry</span><span class="tag">P&amp;C</span><span class="tag">Probability</span></div>
   <p class="muted" style="flex:1"><b data-stat="quant">{len(QB['quant']['questions'])}</b> questions covering arithmetic, algebra, geometry and modern maths.</p><a class="btn btn-sm" href="quant.html">Explore Quant →</a></div>
  <div class="card sec-card" style="--c:var(--reason)"><div class="icon" style="background:#ecfeff">🧩</div><h3>Logical Reasoning</h3>
   <div class="tags"><span class="tag">Syllogisms</span><span class="tag">Seating</span><span class="tag">Blood Relations</span><span class="tag">Coding-Decoding</span><span class="tag">Puzzles</span><span class="tag">Series</span></div>
   <p class="muted" style="flex:1"><b data-stat="reasoning">{len(QB['reasoning']['questions'])}</b> questions covering verbal and analytical reasoning.</p><a class="btn btn-sm" href="reasoning.html">Explore Reasoning →</a></div>
  <div class="card sec-card" style="--c:var(--dilr)"><div class="icon" style="background:#fdf2f8">📊</div><h3>DILR</h3>
   <div class="tags"><span class="tag">Tables</span><span class="tag">Bar Charts</span><span class="tag">Pie Charts</span><span class="tag">Line Graphs</span><span class="tag">Caselets</span><span class="tag">Arrangements</span></div>
   <p class="muted" style="flex:1"><b data-stat="dilr">{len(QB['dilr']['questions'])}</b> questions, mostly in data sets with several questions each.</p><a class="btn btn-sm" href="dilr.html">Explore DILR →</a></div>
 </div>
</div></section>

<section class="cat-band"><div class="container">
 <div class="cat-band-grid">
  <div><span class="pill">🎯 CAT track</span><h2>CAT-style practice, including VARC</h2>
   <p class="muted">CAT-style questions we wrote ourselves (not taken from past papers): reading comprehension, para-jumbles, DILR puzzle sets and QA, with MCQ and TITA types. Take a 40-minute sectional with CAT marking, or practise one topic at a time with solutions straight after each answer.</p>
   <div class="cta-row" style="margin-bottom:0"><a class="btn" href="cat.html">Explore the CAT track →</a><a class="btn btn-ghost" href="cat-practice.html">Start a sectional</a></div></div>
  <div class="cat-mini">
   <a class="card" href="cat-practice.html?section=varc"><b>VARC</b><span><b data-stat="cat-varc">{CATN['varc']}</b> questions</span></a>
   <a class="card" href="cat-practice.html?section=dilr"><b>DILR</b><span><b data-stat="cat-dilr">{CATN['dilr']}</b> questions in sets</span></a>
   <a class="card" href="cat-quant-sets.html"><b>Quant</b><span><b data-stat="cat-qa">{CATN['qa']}</b> questions</span></a>
   <div class="card"><b>TITA</b><span><b data-stat="cat-tita">{CAT_TITA}</b> type-in-the-answer</span></div>
  </div>
 </div>
</div></section>

<section class="cat-band cuet-band"><div class="container">
 <div class="cat-band-grid">
  <div><span class="pill">🎓 CUET (UG) track</span><h2>CUET (UG): aptitude, English and Maths</h2>
   <p class="muted">Practice in NTA's CUET (UG) format: MCQs with +5 for a correct answer and −1 for a wrong one, sectionals at the real pace (50 questions in 60 minutes), and topic practice with worked solutions. All questions are written by us. GK covers static facts only, with no current affairs.</p>
   <div class="cta-row" style="margin-bottom:0"><a class="btn" href="cuet.html">Explore the CUET track →</a><a class="btn btn-ghost" href="cuet-practice.html">Start a sectional</a></div></div>
  <div class="cat-mini">
   <a class="card" href="cuet-practice.html?section=gat"><b>General Aptitude</b><span><b data-stat="cuet-gat">{CUETN['gat']}</b> questions</span></a>
   <a class="card" href="cuet-practice.html?section=english"><b>English</b><span><b data-stat="cuet-english">{CUETN['english']}</b> questions</span></a>
   <a class="card" href="cuet-practice.html?section=maths"><b>Mathematics</b><span><b data-stat="cuet-maths">{CUETN['maths']}</b> questions</span></a>
   <div class="card"><b>Marking</b><span><b>+5 / −1</b> per question</span></div>
  </div>
 </div>
</div></section>

<section><div class="container">
 <div class="section-head"><h2>What you get today</h2></div>
 <div class="grid g4 m2 compact">
  <div class="card"><div class="icon">⏱️</div><h3>Timed quizzes</h3><p class="muted">Palette and mark-for-review, plus CAT-style 40-minute sectionals with TITA questions and +3/−1 marking.</p></div>
  <div class="card"><div class="icon">💡</div><h3>Worked solutions</h3><p class="muted">Every question has a step-by-step solution, shown after you submit.</p></div>
  <div class="card"><div class="icon">📝</div><h3>Notes &amp; formula sheets</h3><p class="muted">Concept notes and topic-wise formula or rules sheets for Quant, Reasoning, DILR and VARC.</p></div>
  <div class="card soon-card"><div class="icon">🚧</div><h3>Coming soon</h3><ul class="soon-list"><li>Full-length CAT mocks (all 3 sections)</li><li>Company-wise placement sets</li><li>Progress analytics</li></ul></div>
 </div>
</div></section>

<section class="alt about"><div class="container" style="max-width:760px;text-align:center">
 <h2>About <span data-brand></span></h2>
 <p class="muted"><span data-brand></span> is a new, free practice site for Indian students preparing for aptitude tests: CAT and other MBA entrance exams, bank and SSC exams, and campus placements. Every question here is written by us and comes with a worked solution. We're starting small and adding more questions and topics over time.</p>
 <p class="muted" style="margin:0">Login only to save progress and unlock levels.</p>
</div></section>

<section><div class="container"><div class="cta-band">
 <h2>Start practising in under 10 seconds</h2><p style="opacity:.9">Login only to save progress and unlock levels. Pick a section and beat the clock.</p>
 <div class="cta-row" style="justify-content:center;margin-bottom:0"><a href="practice.html" class="btn">Start a free quiz →</a></div>
</div></div></section>
<script>(function(){{var box=document.getElementById('sample'),fb=document.getElementById('sample-fb'),bs=[].slice.call(box.querySelectorAll('.mini-opt'));
bs.forEach(function(b){{b.onclick=function(){{var ok=b.dataset.ok==='1';bs.forEach(function(x){{x.disabled=true;if(x.dataset.ok==='1')x.classList.add('right')}});if(!ok)b.classList.add('wrong');
fb.innerHTML=(ok?'<b>✅ Correct!</b> ':'<b>❌ Not quite.</b> The answer is B. ')+'Together they finish 1/12 + 1/18 = 5/36 of the job a day, so they need 36/5 = 7.2 days.'+
'<div class="cta-row" style="margin:.8em 0 0"><a class="btn btn-sm" href="practice.html?quick=5">Try 5 more →</a><button type="button" class="btn btn-ghost btn-sm" id="sample-again">Try again</button></div>';
fb.classList.remove('hidden');document.getElementById('sample-again').onclick=function(){{bs.forEach(function(x){{x.disabled=false;x.classList.remove('right','wrong')}});fb.classList.add('hidden')}};}}}});}})();</script>
""", desc="Free aptitude practice for CAT, CUET (UG), Bank, SSC and placements: Quant, Reasoning, DILR and VARC with timed quizzes, worked solutions and formula sheets. Login only to save progress and unlock levels.")

# ---------- SECTION PAGES ----------
def fs_section(formulas, color, heading="Formula &amp; rules sheet", unit="formulas and rules", prose=False):
    import html as _h
    esc=lambda s: _h.escape(s, quote=False)
    nf=sum(len(items) for _,_,items in formulas)
    fl="".join(f"""<details class="fs-card" open><summary><span class="fs-ic" aria-hidden="true">{ic}</span><span class="fs-t">{name}</span><span class="fs-n">{len(items)}</span></summary><ul class="fs-list">"""
       + "".join(f"<li><code class='fx'>{esc(fx)}</code>" + (f"<span class='fx-note'>{esc(nt)}</span>" if nt else "") + "</li>" for fx,nt in items)
       + "</ul></details>" for ic,name,items in formulas)
    return f"""<section id="formulas" class="fs{' fs-prose' if prose else ''}" style="--c:{color}"><div class="container">
<div class="fs-head"><div><h2>{heading}</h2><p class="muted">{len(formulas)} topics · {nf} {unit}. Tap a topic to open or close it.</p></div><button type="button" class="btn btn-ghost btn-sm" id="fs-toggle">Collapse all</button></div>
<div class="fs-grid">{fl}</div>
<p class="muted" style="margin-top:1.2em">Tip: bookmark this page and revise it for 5 minutes before each practice session.</p></div></section>
<script>(function(){{var c=[].slice.call(document.querySelectorAll('.fs-card')),b=document.getElementById('fs-toggle');
function upd(){{b.textContent=c.every(function(d){{return d.open}})?'Collapse all':'Expand all'}}
if(matchMedia('(max-width:600px)').matches)c.forEach(function(d,i){{if(i>1)d.open=false}});
c.forEach(function(d){{d.addEventListener('toggle',upd)}});b.onclick=function(){{var o=!c.every(function(d){{return d.open}});c.forEach(function(d){{d.open=o}});upd()}};upd()}})();</script>"""

def section_page(fn, key, title, color, intro, topics, note, formulas, desc):
    import html as _h
    cnt={}
    for q in QB[key]["questions"]: cnt[q["topic"]]=cnt.get(q["topic"],0)+1
    names=[_h.unescape(t) for t,d,p in topics]
    missing=[n for n in names if cnt.get(n,0)<4]; extra=set(cnt)-set(names)
    assert not missing and not extra, (key, missing, extra)
    tl="".join(f"<a class='topic' href='practice.html?section={key}&amp;topic={_h.escape(_h.unescape(t)).replace(' ','%20').replace('&amp;','%26')}' data-topic=\"{_h.escape(_h.unescape(t))}\"><h4>{t} <span class='badge' data-topic-count>{cnt[_h.unescape(t)]} Qs</span></h4><p>{d}</p><span class='exam-tag {exam_tag(_h.unescape(t))[1]}'>{exam_tag(_h.unescape(t))[0]}</span></a>" for t,d,p in topics)
    fs=fs_section(formulas, color)
    page(fn,title,f"""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / {title}</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">{title}</h1><p class="muted" style="max-width:700px">{intro}</p>
<div class="cta-row"><a class="btn" href="practice.html?section={key}">Practise {title} →</a><a class="btn btn-ghost" href="#formulas">Formula sheet</a></div></div></div>
<section style="padding-top:20px"><div class="container"><h2>Topics</h2><p class='muted' style='margin-top:-.4em'>Tap a topic to practise just that topic. Tags show which exams it suits best. For CAT-style sets, see the <a href="cat.html">CAT track</a>.</p><div class="topic-list">{tl}</div></div></section>
<section class="alt"><div class="container note" style="max-width:860px"><h2>Concept note</h2>{note}</div></section>
{fs}
""", desc=desc)

section_page("quant.html","quant","Quantitative Aptitude","var(--quant)",
"Arithmetic, algebra, geometry and modern maths for CAT, Bank/SSC, GMAT and placement tests.",
[("Percentages","Percentage change, successive change, conversions",1),("Profit &amp; Loss","CP, SP, marked price, discount",1),("Simple &amp; Compound Interest","SI, CI, effective rate",1),("Ratio &amp; Proportion","Ratios, partnership, proportions",1),("Averages &amp; Alligation","Averages, mixtures and alligation",1),("Time &amp; Work","Work rates, pipes and cisterns",1),("Time, Speed &amp; Distance","Trains, boats, relative speed",1),("Number System","Remainders, factorials, HCF/LCM, factors",1),("Algebra","Linear equations, identities, quadratics",1),("Geometry &amp; Mensuration","Triangles, circles, areas, volumes",1),("Permutations &amp; Combinations","Arrangements, selections",1),("Probability","Classical probability, dice, cards",1)],
"""<h3>Percentages: the core idea</h3><p>A percentage is a fraction with denominator 100. Learn the fraction–percentage pairs (1/8 = 12.5%, 1/6 ≈ 16.67%, 1/12 ≈ 8.33%) so you can do percentage maths mentally.</p>
<p><b>Successive change:</b> if a value changes by a% and then by b%, the net change is <b>a + b + ab/100</b>%. For example, +20% then −20% gives 20 − 20 − 4 = <b>−4%</b>.</p>
<div class="tip">💡 <b>Shortcut:</b> after a fall of x%, the rise needed to get back to the original value is x/(100 − x) × 100%. After a 20% fall you need a 25% rise.</div>
<h3>Profit &amp; Loss</h3><p>Profit % and loss % are always calculated on <b>cost price</b>. Discount is always calculated on <b>marked price</b>. Selling at a loss of x% means SP = CP × (100 − x)/100.</p>
<h3>Time, Speed &amp; Distance</h3><p>To convert km/h to m/s, multiply by 5/18. A train crossing a pole covers its own length. A train crossing a platform covers its own length plus the platform's. For equal distances at speeds x and y, the average speed is the <b>harmonic mean</b> 2xy/(x + y), not the simple average.</p>""",
FORMULAS["quant"], "Quantitative Aptitude for Bank, SSC, CAT and placements: topic-wise practice, a concept note and a formula sheet for percentages, TSD, number system, algebra, geometry and more.")

section_page("reasoning.html","reasoning","Logical Reasoning","var(--reason)",
"Verbal and analytical reasoning for Bank/SSC, CAT LR and placement tests, with methods for the most common question types.",
[("Syllogisms","All / Some / No statements, Venn method",1),("Seating Arrangement","Linear and circular",1),("Blood Relations","Family trees and coded relations",1),("Coding-Decoding","Letter shifts, number and word codes",1),("Puzzles","Floor and matching puzzles",1),("Direction Sense","Distance and final direction",1),("Number &amp; Letter Series","Find the pattern",1),("Odd One Out","Classification",1),("Clocks &amp; Calendars","Angles, odd days",1),("Alphabet Test","Letter positions and ordering",1),("Inequalities","Direct inequalities with conclusions",1),("Ranking &amp; Order","Positions in a row, comparisons",1)],
"""<h3>Syllogisms: use Venn diagrams</h3><p>Draw the <b>smallest</b> diagram that fits every statement. A conclusion follows only if it is true in <b>every</b> possible diagram.</p>
<ul><li><b>All A are B</b>: circle A sits inside circle B. It also implies <i>Some B are A</i>.</li><li><b>Some A are B</b>: the circles overlap. It implies <i>Some B are A</i>.</li><li><b>No A is B</b>: the circles don't touch. It implies <i>No B is A</i>.</li></ul>
<div class="tip">💡 "Some A are not B" never follows from "Some A are B" on its own. Look for a statement that rules it out.</div>
<h3>Seating arrangement</h3><p>Fix the most definite clue first, such as "X is in the middle" or "Y is at an end". In a row facing north, the person's <b>right</b> is your right. In a circle facing the centre, <b>left is clockwise</b>.</p>
<h3>Blood relations</h3><p>Draw a family tree. Use + for male and − for female, horizontal lines for siblings and spouses, and vertical lines for generations. Break long chains like "my father's father's only son" from the end backwards.</p>""",
FORMULAS["reasoning"], "Logical Reasoning practice for Bank, SSC and placements: syllogisms, seating, blood relations, coding-decoding and puzzles, with methods and a rules sheet.")

section_page("dilr.html","dilr","Data Interpretation &amp; Logical Reasoning (DILR)","var(--dilr)",
"Read data fast and reason carefully: tables, charts, caselets, arrangements, tournaments, Venn diagrams and routes.",
[("Tables","Multi-row data, growth, share",1),("Bar Charts","Reading and comparing bars",1),("Pie Charts","Percentages and central angles",1),("Line Graphs","Trends and month-on-month change",1),("Caselets","Paragraph-based data",1),("Arrangements","Table seating and matching grids",1),("Games &amp; Tournaments","Knock-outs, round robins",1),("Venn Diagrams","2- and 3-set problems",1),("Network &amp; Routes","Shortest routes on a road map",1)],
"""<h3>How to approach a DI set</h3><ol><li><b>Scan for 30 seconds:</b> note the units, the totals and what each axis or column means.</li><li><b>Approximate:</b> most DI options are far enough apart that rounding works (e.g. 487/1210 ≈ 40%).</li><li><b>Reuse:</b> compute totals or growth once and use them for every question in the set.</li></ol>
<h3>Growth and share</h3><p><b>Growth %</b> = (New − Old)/Old × 100. <b>Share %</b> = Part/Total × 100. Don't mix these up. A product can have the highest absolute increase but not the highest percentage growth.</p>
<div class="tip">💡 <b>Pie charts:</b> 1% = 3.6°, so 25% = 90° and 10% = 36°.</div>
<h3>Choosing LR sets (CAT)</h3><p>In CAT, set selection matters as much as solving. Spend the first 3–4 minutes scanning every set, then start with the ones that have the most definite clues and the fewest variables.</p>""",
FORMULAS["dilr"], "Data Interpretation and Logical Reasoning (DILR) practice: tables, bar, pie and line charts, caselets, arrangements, tournaments and routes, with a formula sheet.")

# ---------- PRACTICE ----------
page("practice.html","Practice","""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / Practice</div><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">Practice</h1><p class="muted">Choose your exam track to begin.</p></div></div>
<section style="padding-top:16px"><div class="container">
 <div class="quick-card card"><div><b>⚡ Quick start</b><span class="muted">10 mixed Quant, Reasoning &amp; DILR questions · 60 s each · one tap</span></div><button type="button" class="btn" data-quick="10">Start 10 questions →</button></div>
 <div id="exam-pick" class="exam-pick">
  <a class="exam-card" href="cat-practice.html" style="--c:var(--brand)"><span class="exam-ic">🎯</span><span class="exam-b"><b>CAT</b><small>VARC · DILR · QA · 40-min sectionals · MCQ + TITA · CAT marking</small><small class="exam-n"><span data-stat="cat">%NQ_CAT%</span> CAT-style questions</small></span><span class="exam-go">→</span></a>
  <a class="exam-card" href="cuet-practice.html" style="--c:var(--cuet)"><span class="exam-ic">🎓</span><span class="exam-b"><b>CUET (UG)</b><small>General Aptitude · English · Maths · +5 / −1 · real pace</small><small class="exam-n"><span data-stat="cuet">%NQ_CUET%</span> CUET questions</small></span><span class="exam-go">→</span></a>
  <button type="button" class="exam-card" id="pick-general" style="--c:var(--reason)"><span class="exam-ic">🏦</span><span class="exam-b"><b>Bank / SSC / Placements</b><small>Quant · Reasoning · DILR · timed quizzes · topic filter</small><small class="exam-n"><span data-stat="general">%NQ_GEN%</span> questions</small></span><span class="exam-go">→</span></button>
 </div>
 <div id="setup" class="card quiz-setup hidden">
  <p class="muted" style="margin:0 0 .8em;font-size:.9rem"><b>Track:</b> Bank / SSC / Placements · <a href="practice.html" id="change-track">Change track</a></p>
  <h3>1. Choose a section</h3>
  <div class="sec-pick">
   <label><input type="radio" name="section" value="quant" checked>➗ Quant</label>
   <label><input type="radio" name="section" value="reasoning">🧩 Reasoning</label>
   <label><input type="radio" name="section" value="dilr">📊 DILR</label>
   <label><input type="radio" name="section" value="mixed">🎲 Mixed</label>
  </div>
  <div class="grid g4 setup-grid" style="margin-top:18px">
   <div class="form"><label>2. Topic (optional)<select id="topic"><option value="">All topics</option></select></label></div>
   <div class="form"><label>3. Number of questions<select id="count"><option value="5">5</option><option value="10" selected>10</option><option value="15">15</option><option value="20">20</option><option value="999">All available</option></select></label></div>
   <div class="form"><label>4. Time per question<select id="per"><option value="60">60 s</option><option value="90" selected>90 s</option><option value="120">120 s</option></select></label></div>
   <div class="form"><label>5. Marking<span style="display:flex;gap:8px;align-items:center;margin-top:.8em;font-weight:500"><input type="checkbox" id="neg" style="width:auto;margin:0"> CAT-style (+3 / −1)</span></label></div>
  </div>
  <p class="muted" id="avail" style="margin:14px 0 0;font-size:.9rem"></p><button id="start" class="btn" style="margin-top:14px">Start quiz →</button>
 </div>

 <div id="quiz" class="hidden">
  <div class="quiz-bar"><h3 id="quiz-title" style="margin:0"></h3><span id="timer" class="timer">⏱ 00:00</span></div>
  <div class="progress"><i id="bar" style="width:0"></i></div>
  <div class="quiz-wrap">
   <div class="card">
    <div class="muted" style="display:flex;justify-content:space-between;font-size:.88rem;margin-bottom:10px"><b id="q-num"></b><span id="q-topic"></span></div>
    <div id="q-data" class="q-data hidden"></div>
    <div id="q-text" class="q-text"></div>
    <div id="opts"></div>
    <div id="q-report" class="q-report"></div>
    <div class="q-actions"><div style="display:flex;gap:8px"><button id="prev" class="btn btn-ghost btn-sm">← Prev</button><button id="clear" class="btn btn-ghost btn-sm">Clear</button></div>
    <div style="display:flex;gap:8px"><button id="mark" class="btn btn-ghost btn-sm">☆ Mark</button><button id="next" class="btn btn-sm">Save &amp; Next →</button></div></div>
   </div>
   <aside class="card"><b>Question palette</b><div class="muted" id="answered" style="font-size:.85rem"></div><div id="palette" class="palette"></div>
    <div class="legend"><span><i style="background:#dcfce7"></i>Answered</span><span><i style="background:#fef3c7"></i>Marked</span><span><i style="background:#fff;border:1px solid #ccc"></i>Not answered</span></div>
    <button id="submit" class="btn" style="width:100%;margin-top:16px">Submit test</button></aside>
  </div>
 </div>

 <div id="results" class="hidden">
  <div class="card" id="res-summary"></div>
  <div style="text-align:center;margin:18px 0"><button id="retry" class="btn">Try another quiz</button></div>
  <div class="card prog-card" data-progress="general"></div>
  <h2>Review &amp; solutions</h2><div id="review"></div>
 </div>
 <div id="progress-wrap" class="card prog-card" data-progress="" style="margin-top:20px"></div>
</div></section>
""".replace("%NQ_CAT%",str(NQ_CAT)).replace("%NQ_CUET%",str(sum(CUETN.values()))).replace("%NQ_GEN%",str(NQ_GEN)), extra='''<script src="assets/js/progress.js"></script><script src="assets/js/quiz.js"></script>
<script>(function(){var p=new URLSearchParams(location.search),pick=document.getElementById('exam-pick'),setup=document.getElementById('setup');
function gen(){pick.classList.add('hidden');setup.classList.remove('hidden');if(window.__quizSetupHook)window.__quizSetupHook(p.get('topic'));}
document.getElementById('pick-general').onclick=gen;
document.getElementById('change-track').onclick=function(e){e.preventDefault();setup.classList.add('hidden');pick.classList.remove('hidden');};
if(p.get('exam')==='general'||p.get('section')){pick.classList.add('hidden');setup.classList.remove('hidden');}})();</script>''', desc="Start a free timed aptitude quiz: pick the CAT, CUET (UG) or Bank / SSC / Placements track, choose a section and topic, and get worked solutions after you submit.")

# ---------- CAT TRACK ----------
import html as _hh
CAT_DESC = {
 "varc": {"Reading Comprehension":"400–550 word passages on economics, philosophy, science and literature, with 4 questions each.",
          "Para-jumbles":"Put 4 jumbled sentences in order. TITA: type the sequence.",
          "Para-summary":"Choose the option that best captures the paragraph's main point.",
          "Odd sentence out":"Find the sentence that doesn't belong. TITA: type its number."},
 "dilr": {"Scheduling":"Who does what on which day, from a list of conditions.",
          "Tournaments":"Round-robin results worked back from the points table.",
          "Tables with missing data":"Fill a partly blank table using the totals and clues given.",
          "Games with rules":"Winning and losing positions in take-away games.",
          "Distribution":"Share items among people under constraints.",
          "Logic puzzles":"Deduce a secret code from feedback on guesses.",
          "Arrangements":"Match people, pets and colours to houses.",
          "Rankings & scoring":"Rebuild rankings from points and conditions."},
 "qa": {"Percentages & Profit":"Successive changes, markups, discounts and profit.",
        "Time, Speed & Distance":"Relative speed, trains, boats and races.",
        "Time & Work":"Efficiency, pipes and work-wage problems.",
        "Mixtures & Alligation":"Replacement and mixing ratios.",
        "Simple & Compound Interest":"Instalments and CI versus SI.",
        "Ratio & Proportion":"Partnerships, variation and ratio chains.",
        "Equations & Quadratics":"Roots, integer solutions and systems of equations.",
        "Inequalities":"Ranges, AM-GM and modulus.",
        "Functions":"Composite, recursive and functional equations.",
        "Logarithms":"Log rules, equations and bases.",
        "Number System":"Remainders, factors, HCF/LCM and digits.",
        "Geometry":"Triangles, circles and coordinate geometry.",
        "Mensuration":"Areas and volumes of 2D and 3D shapes.",
        "Permutations & Combinations":"Counting with restrictions.",
        "Probability":"Conditional probability and counting-based questions.",
        "Averages":"Averages, weighted averages and what changes when an item is added or replaced.",
        "Sets":"Venn diagrams and inclusion–exclusion counting.",
        "Progressions":"AP, GP and sums of series."}}
def cat_topic_cards(sec):
    cnt={}
    for q in CB["sections"][sec]["questions"]: cnt[q["topic"]]=cnt.get(q["topic"],0)+1
    assert set(cnt)==set(CAT_DESC[sec]), (sec, set(cnt)^set(CAT_DESC[sec]))
    from urllib.parse import quote
    return "".join(f"<a class='topic' href='cat-practice.html?mode=practice&amp;section={sec}&amp;topic={quote(t)}' data-cat-topic=\"{_hh.escape(sec+'|'+t)}\"><h4>{_hh.escape(t)} <span class='badge' data-topic-count>{cnt[t]} Qs</span></h4><p>{CAT_DESC[sec][t]}</p><span class='exam-tag tag-cat'>CAT</span></a>" for t in CAT_DESC[sec])
def cat_type_counts(sec):
    qq=CB["sections"][sec]["questions"]; return sum(q["type"]=="mcq" for q in qq), sum(q["type"]=="tita" for q in qq)
NSETS=sum(1 for s in CB["sets"].values() if s["kind"]=="dilr"); NPASS=sum(1 for s in CB["sets"].values() if s["kind"]=="passage")
secblk=""
for sec,ic,col,blurb in [("varc","📖","var(--varc)",f"<span data-stat='cat-passages'>{NPASS}</span> reading passages plus para-jumbles, para-summaries and odd-sentence-out."),
                         ("dilr","📊","var(--dilr)",f"<span data-stat='cat-sets'>{NSETS}</span> puzzle sets of 4–5 questions each, every one checked by computer to have a single solution."),
                         ("qa","➗","var(--quant)","Arithmetic, algebra, number system, geometry and modern maths, from moderate to hard.")]:
    m,ti=cat_type_counts(sec)
    secblk+=f"""<div class="card sec-card" style="--c:{col}"><div class="icon">{ic}</div><h3>{CB['sections'][sec]['name']} ({sec.upper()})</h3>
<p class="muted" style="flex:1"><b data-stat="cat-{sec}">{CATN[sec]}</b> questions · {m} MCQ / {ti} TITA. {blurb}</p>
<div class="cta-row" style="margin:0"><a class="btn btn-sm" href="cat-practice.html?mode=sectional&amp;section={sec}">40-min sectional →</a><a class="btn btn-sm btn-ghost" href="cat-practice.html?mode=practice&amp;section={sec}">Practise</a></div></div>"""
page("cat.html","CAT Track: VARC, DILR & QA",f"""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / CAT track</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">CAT track <span class="exam-tag tag-cat" style="vertical-align:middle">CAT</span></h1>
<p class="muted" style="max-width:720px">A separate track for CAT aspirants: VARC, DILR and QA questions at moderate to hard level, in CAT's question formats (MCQ and TITA) with CAT marking. All <b data-stat="cat">{NQ_CAT}</b> questions and passages were written by us for practice. They are not taken from CAT papers or coaching material, and each has a worked solution.</p>
<div class="cta-row"><a class="btn" href="cat-quant-sets.html">Practice sets: Quant →</a><a class="btn btn-ghost" href="cat-varc-sets.html">VARC sets</a><a class="btn btn-ghost" href="cat-dilr-sets.html">DILR sets</a><a class="btn btn-ghost" href="cat-practice.html">40-min sectional</a><a class="btn btn-ghost" href="varc.html">VARC strategy &amp; rules</a></div></div></div>
<section style="padding-top:20px"><div class="container"><div class="grid g3">{secblk}</div></div></section>
<section class="alt"><div class="container"><div class="grid g2">
 <div class="card"><h3>⏱ Sectional mode</h3><ul class="clean">
  <li>One section, <b>40 minutes</b>, submits automatically when time runs out.</li>
  <li>About 24 VARC, 22 DILR or 22 QA questions, picked from the bank (DILR and RC sets stay together).</li>
  <li>A CAT-style palette: not visited, not answered, answered, marked, and answered &amp; marked.</li>
  <li>RC passages and DILR sets open in a side panel on desktop and above the question on mobile.</li>
  <li>Results: score, attempts, accuracy, time per question and a topic-wise strong/weak breakdown.</li></ul></div>
 <div class="card"><h3>🧠 Practice mode</h3><ul class="clean">
  <li>Pick a section and a topic; no countdown (just an elapsed clock).</li>
  <li>Check each answer and see the full solution straight away.</li>
  <li>Useful for learning one question type at a time before taking sectionals.</li></ul>
  <h3 style="margin-top:1em">📏 Marking used</h3>
  <table class="data"><tr><th style="text-align:left">Type</th><th>Correct</th><th>Wrong</th><th>Blank</th></tr>
  <tr><td style="text-align:left">MCQ</td><td>+3</td><td>−1</td><td>0</td></tr><tr><td style="text-align:left">TITA (type in the answer)</td><td>+3</td><td>0</td><td>0</td></tr></table></div>
</div></div></section>
<section><div class="container"><h2>CAT topics</h2><p class="muted" style="margin-top:-.4em">Tap a topic to practise it with instant solutions.</p>
<h3 class="cat-sub">VARC</h3><div class="topic-list">{cat_topic_cards('varc')}</div>
<h3 class="cat-sub">DILR</h3><div class="topic-list">{cat_topic_cards('dilr')}</div>
<h3 class="cat-sub">QA</h3><div class="topic-list">{cat_topic_cards('qa')}</div>
<div class="notice" style="margin-top:22px">The question bank is still small. Sectionals pick from the questions above, so you'll see repeats if you take several. Full-length 3-section mocks are not available yet. For more basic practice on Quant and DILR, see the <a href="practice.html?exam=general">Bank / SSC / Placements track</a>.</div>
</div></section>
""", desc="CAT-style VARC, DILR and QA practice with 40-minute sectionals, TITA questions, CAT marking and worked solutions. Original questions.")

page("varc.html","VARC: Reading Strategy & Rules",f"""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / <a href="cat.html">CAT</a> / VARC</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">Verbal Ability &amp; Reading Comprehension (VARC)</h1>
<p class="muted" style="max-width:720px">CAT's first section. Reading comprehension carries most of the marks; para-jumbles and odd-sentence-out are TITA, so a wrong answer costs nothing. All passages here were written by us for practice.</p>
<div class="cta-row"><a class="btn" href="cat-practice.html?mode=sectional&amp;section=varc">VARC sectional (40 min) →</a><a class="btn btn-ghost" href="#formulas">Rules sheet</a></div></div></div>
<section style="padding-top:20px"><div class="container"><h2>Topics</h2><p class='muted' style='margin-top:-.4em'>Tap a topic to practise it with instant solutions.</p><div class="topic-list">{cat_topic_cards('varc')}</div></div></section>
<section class="alt"><div class="container note" style="max-width:860px"><h2>Reading strategy</h2>
<h3>1. Read for the argument, not the facts</h3><p>CAT passages are usually arguments: the author takes a position, considers objections and qualifies the claim. As you read, keep one line in your head: <i>what is the author saying, and how sure are they?</i> Details can be looked up again; the structure cannot.</p>
<h3>2. Map each paragraph in a few words</h3><p>After each paragraph, name its job: "problem", "example", "objection", "author's answer". Most questions ask about one of these jobs. A rough map saves you from rereading the whole passage.</p>
<h3>3. Watch the signal words</h3><p><b>However, yet, but</b> mark a turn; <b>therefore, thus</b> mark a conclusion; <b>admittedly, of course</b> often mark a concession the author will then push back on. Questions on the author's view usually depend on what comes after the turn.</p>
<h3>4. Eliminate, don't hunt</h3><p>Wrong options tend to fall into a few types: <b>too extreme</b> ("always", "only"), <b>out of scope</b> (true in real life but not in the passage), <b>half right</b> (the first half fits, the second distorts), and <b>reversed</b> (cause and effect swapped). Strike out options until one survives.</p>
<h3>5. Plan the 40 minutes</h3><p>A reasonable plan is about 7–8 minutes per passage and 1–2 minutes per verbal ability question. Since TITA questions carry no negative marks, attempt every para-jumble and odd-sentence item you have time for. With MCQs, guess only if you can eliminate at least two options.</p>
</div></section>
{fs_section(FORMULAS['varc'], 'var(--varc)', heading='VARC rules sheet', unit='rules and checks', prose=True)}
""", desc="CAT VARC reading strategy, rules sheet for RC, para-jumbles, para-summary and odd-sentence-out, with original practice questions.")

def quiz_html(exam, home, label, retry, back=None):
    back = back or f"{label} track"
    return f""" <div id="c-quiz" class="hidden">
  <div class="quiz-bar"><h3 id="c-title" style="margin:0;font-size:1.05rem"></h3><span id="c-timer" class="timer">⏱ 00:00</span></div>
  <div id="c-layout" class="c-layout">
   <aside id="c-pane" class="card c-pane hidden" data-set=""><div class="c-pane-head"><b id="c-pane-label">Passage</b><span id="c-pane-meta" class="muted"></span></div><div id="c-pane-body" class="c-pane-body q-data"></div></aside>
   <div class="card c-main">
    <div class="c-qhead"><b id="c-qnum"></b><span id="c-qtype" class="qtype"></span><span class="muted" id="c-qmeta"></span><span class="c-marks">Marks <b id="c-marks"></b></span></div>
    <div id="c-qtext" class="q-text"></div>
    <div id="c-answer"></div>
    <div id="c-feedback"></div>
    <div id="c-report" class="q-report"></div>
    <div class="q-actions c-actions">
     <div style="display:flex;gap:8px;flex-wrap:wrap"><button id="c-prev" class="btn btn-ghost btn-sm">← Prev</button><button id="c-clear" class="btn btn-ghost btn-sm">Clear response</button><button id="c-mark" class="btn btn-ghost btn-sm">Mark for Review &amp; Next</button></div>
     <div style="display:flex;gap:8px;flex-wrap:wrap"><button id="c-check" class="btn btn-sm btn-check hidden">Check answer</button><button id="c-next" class="btn btn-sm">Save &amp; Next →</button></div>
    </div>
   </div>
   <aside class="card c-side"><b>Question palette</b>
    <div id="c-palette" class="palette c-palette"></div>
    <div class="c-legend">
     <span><i class="lg a"></i>Answered <b data-cnt="a">0</b></span><span><i class="lg na"></i>Not answered <b data-cnt="na">0</b></span>
     <span><i class="lg nv"></i>Not visited <b data-cnt="nv">0</b></span><span><i class="lg m"></i>Marked <b data-cnt="m">0</b></span>
     <span><i class="lg am"></i>Answered &amp; marked <b data-cnt="am">0</b></span></div>
    <button id="c-submit" class="btn" style="width:100%;margin-top:14px">Submit section</button></aside>
  </div>
 </div>

 <div id="c-results" class="hidden">
  <div class="card" id="c-res-head"></div>
  <div class="card" id="c-topics" style="margin-top:16px"></div>
  <div class="card prog-card" data-progress="{exam}" style="margin-top:16px"></div>
  <div style="text-align:center;margin:18px 0"><button id="c-retry" class="btn">{retry}</button> <a class="btn btn-ghost" href="{home}" data-hub>{back}</a></div>
  <p id="set-save" class="muted" style="text-align:center;margin:0 0 18px"></p>
  <h2>Review &amp; solutions</h2><div id="c-review"></div>
 </div>
"""

def practice_page(fn, exam, label, home, track, sect_note, secs, title, desc):
    radios = "\n".join(f'   <label><input type="radio" name="csec" value="{k}"{" checked" if i == 0 else ""}><span><b>{name}</b><small data-csec-count="{k}"></small></span></label>' for i, (k, name) in enumerate(secs))
    page(fn, title, f"""
<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / <a href="{home}">{label}</a> / Practice</div>
<h1 style="font-size:clamp(1.6rem,3.6vw,2.3rem)">{label} practice</h1></div></div>
<section style="padding-top:12px"><div class="container">
 <div id="c-setup" class="card quiz-setup">
  <p class="muted" style="margin:0 0 .8em;font-size:.9rem"><b>Track:</b> {track} · <a href="practice.html">Change track</a></p>
  <h3>1. Choose a mode</h3>
  <div class="sec-pick two">
   <label><input type="radio" name="cmode" value="sectional" checked><span><b>⏱ Sectional</b><small>{sect_note}</small></span></label>
   <label><input type="radio" name="cmode" value="practice"><span><b>🧠 Practice</b><small>No countdown · solution after each answer</small></span></label>
  </div>
  <h3 style="margin-top:18px">2. Choose a section</h3>
  <div class="sec-pick three">
{radios}
  </div>
  <div id="c-topic-wrap" class="form hidden" style="margin-top:18px;max-width:460px"><label>3. Topic<select id="c-topic"></select></label></div>
  <p class="muted" id="c-info" style="margin:16px 0 0;font-size:.92rem"></p>
  <button id="c-start" class="btn" style="margin-top:14px">Start →</button>
 </div>

{quiz_html(exam, home, label, "Take another section")} <div id="c-progress" class="card prog-card" data-progress="{exam}" style="margin-top:20px"></div>
</div></section>
""", desc=desc, extra=f'<script>window.EXAM="{exam}";</script><script src="assets/js/progress.js"></script><script src="assets/js/exam.js"></script>')

practice_page("cat-practice.html", "cat", "CAT", "cat.html", "CAT", "40 min · CAT marking · results at the end",
    [("varc", "📖 VARC"), ("dilr", "📊 DILR"), ("qa", "➗ QA")], "CAT Practice: Sectionals & Topic Practice",
    "CAT-style 40-minute sectionals for VARC, DILR and QA with TITA questions and CAT marking, plus topic practice with instant solutions.")

# ---------- CAT PRACTICE SETS (hubs, set page, login) ----------
SETS_META=json.load(open("data/cat/sets.json"))
GATE_NOTE=('<p class="muted" style="font-size:.85rem;margin-top:22px">How locks work: Easy is open (guests can try Easy set 1). A level unlocks when you have '
  'completed every set that is ready in the level before it; if that level has no ready sets yet, the next level is already open. '
  'Locks are only a convenience to guide your practice, not a security feature: all questions on this site are public.</p>')
rng=lambda rep: ", ".join(f"{L} (sets {rep[L]['range'][0]}–{rep[L]['range'][1]})" for L in ("Easy","Medium","Hard"))
for sec,slug,name,color in (("qa","quant","Quant","var(--quant)"),("varc","varc","VARC","var(--varc)"),("dilr","dilr","DILR","var(--dilr)")):
    rep=SETS_META["sections"][sec]; nready=sum(len(rep[L]["ready"]) for L in ("Easy","Medium","Hard"))
    fmt_note={"qa":"10 single questions per set, MCQ and TITA.","varc":"10 questions per set: reading-comprehension passages stay whole, topped up with verbal-ability items.",
              "dilr":"Each set is 2 data sets of 5 questions."}[sec]
    page(f"cat-{slug}-sets.html", f"CAT {name} Practice Sets", f"""
<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / <a href="cat.html">CAT</a> / {name} sets</div>
<h1 style="font-size:clamp(1.6rem,3.6vw,2.3rem)">CAT {name}: {rep["count"]} practice sets</h1>
<p class="muted" style="max-width:760px">{rng(rep)}. {fmt_note} {SETS_META["timers"][sec]}-minute timer, CAT marking (+3, −1 for a wrong MCQ, 0 for a wrong TITA), solutions after you submit. <b>{nready}</b> of {rep["count"]} sets are ready; the rest are coming soon.</p></div></div>
<section style="padding-top:12px"><div class="container">
<div id="set-hub" data-sec="{sec}"><p class="muted">Loading sets…</p></div>
<noscript><div class="notice">The practice sets need JavaScript.</div></noscript>
{GATE_NOTE}
</div></section>
""", desc=f"CAT {name} practice in {rep["count"]} sets of 10 questions at Easy, Medium and Hard level, with a timer, CAT marking and worked solutions.",
         extra='<script src="assets/js/sets.js"></script>')

page("set.html", "CAT Practice Set", f"""
<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / <a href="cat.html">CAT</a> / <a href="cat-quant-sets.html" data-hub>Sets</a></div>
<h1 id="set-h1" style="font-size:clamp(1.6rem,3.6vw,2.3rem)">CAT practice set</h1></div></div>
<section style="padding-top:12px"><div class="container">
 <div id="c-setup" class="card quiz-setup"><div id="set-info"><p class="muted">Loading…</p></div>
  <button id="c-start" class="btn hidden" style="margin-top:14px">Start set →</button></div>
{quiz_html("cat", "cat-quant-sets.html", "CAT", "Retry this set", "All sets")}
 <div id="c-progress" class="hidden"></div>
</div></section>
""", desc="A CAT practice set of 10 questions with a timer, CAT marking and worked solutions.", noindex=True,
     extra='<script src="assets/js/progress.js"></script><script src="assets/js/sets.js"></script><script src="assets/js/exam.js"></script>')

page("login.html", "Login", f"""
<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / Login</div>
<h1 style="font-size:clamp(1.6rem,3.6vw,2.3rem)">Login</h1>
<p class="muted" style="max-width:640px">Login only to save progress and unlock levels. We email you a one-time login link: no password.</p></div></div>
<section style="padding-top:12px"><div class="container"><div id="login-box" class="card login-box">
 <form id="login-form" class="form" novalidate><label>Email<input id="login-email" type="email" autocomplete="email" required placeholder="you@example.com"></label>
 <button id="login-send" class="btn" type="submit" style="margin-top:12px">Email me a login link</button></form>
 <p id="login-msg" class="muted" aria-live="polite" style="margin-top:12px"></p>
 <p class="muted" style="font-size:.85rem">We store your email address and your practice-set results to save your progress. See the <a href="privacy.html">privacy policy</a>.</p>
</div></div></section>
""", desc="Log in with an email link to save your CAT practice-set progress and unlock levels.", noindex=True, extra='<script src="assets/js/login.js"></script>')

# ---------- CUET (UG) TRACK ----------
from urllib.parse import quote as _q
OFFICIAL_IB = "https://cuet.nta.nic.in/information-bulletin/"
OFFICIAL_SYL = "https://cuet.nta.nic.in/cuetug-2026-syllabus/"
def cuet_cards(sec):
    qq = UQ[sec]; out = ""
    for part in dict.fromkeys(q["part"] for q in qq):
        pq = [q for q in qq if q["part"] == part]; tops = list(dict.fromkeys(q["topic"] for q in pq))
        cards = ""
        for tp in tops:
            tq = [q for q in pq if q["topic"] == tp]; sh = sum(1 for q in tq if q.get("source") == "general")
            diffs = " · ".join(f"{d} {n}" for d in ("Easy", "Medium", "Hard") if (n := sum(1 for q in tq if q["difficulty"] == d)))
            cards += (f"<a class='topic' href='cuet-practice.html?mode=practice&amp;section={sec}&amp;topic={_q(tp)}' data-cuet-topic=\"{_hh.escape(sec + '|' + part + '|' + tp)}\">"
                      f"<h4>{_hh.escape(tp)} <span class='badge' data-topic-count>{len(tq)} Qs</span></h4><p>{diffs}" + (f" · {sh} shared with Bank/SSC" if sh else "") + "</p><span class='exam-tag tag-cuet'>CUET</span></a>")
        out += f"<h3 class='cat-sub'>{_hh.escape(part)} <span class='muted' style='text-transform:none;letter-spacing:0'>· <span data-cuet-part=\"{_hh.escape(sec + '|' + part)}\">{len(pq)}</span> Qs</span></h3><div class='topic-list'>{cards}</div>"
    return out
gat_parts = {p: sum(1 for q in UQ["gat"] if q["part"] == p) for p in dict.fromkeys(q["part"] for q in UQ["gat"])}
csec = ""
for sec, ic, col, blurb in [
    ("gat", "🧠", "var(--cuet)", "Quantitative reasoning, logical &amp; analytical reasoning, general mental ability and static GK (science, environment, polity, geography, history)."),
    ("english", "📖", "var(--varc)", "Three short passages (factual, narrative, literary) plus synonyms and antonyms, correct-word, error spotting, rearranging parts and matching."),
    ("maths", "➗", "var(--quant)", "Section A (common) and Section B1 (Mathematics): matrices, determinants, calculus, differential equations, vectors, 3D, LPP and probability.")]:
    n = CUETN[sec]; T = min(50, n) * 72
    csec += f"""<div class="card sec-card" style="--c:{col}"><div class="icon">{ic}</div><h3>{UB['sections'][sec]['name']}</h3>
<p class="muted" style="flex:1"><b data-stat="cuet-{sec}">{n}</b> questions. {blurb}<br><small>Sectional: {min(50, n)} questions in {T // 60}:{T % 60:02d}{'' if n >= 50 else ' (same pace as the real paper: 72 s per question)'}.</small></p>
<div class="cta-row" style="margin:0"><a class="btn btn-sm" href="cuet-practice.html?mode=sectional&amp;section={sec}">Sectional →</a><a class="btn btn-sm btn-ghost" href="cuet-practice.html?mode=practice&amp;section={sec}">Practise</a></div></div>"""
page("cuet.html", "CUET (UG) Track: General Aptitude Test, English & Maths", f"""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / CUET (UG)</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">CUET (UG) track <span class="exam-tag tag-cuet" style="vertical-align:middle">CUET</span></h1>
<p class="muted" style="max-width:740px">Practice for the Common University Entrance Test (UG), run by the National Testing Agency (NTA) for admission to central and other participating universities. We cover three of its papers: the <b>General Aptitude Test</b>, <b>English</b> and <b>Mathematics</b>. All questions were written by us for practice; none are taken from NTA papers. <span data-stat="cuet-shared">{NQ_CUET_SHARED}</span> General Aptitude questions are shared with our Bank / SSC track and are marked as such.</p>
<div class="cta-row"><a class="btn" href="cuet-practice.html">Start a CUET sectional →</a><a class="btn btn-ghost" href="#pattern">Exam pattern</a></div></div></div>
<section style="padding-top:20px"><div class="container"><div class="grid g3">{csec}</div></div></section>
<section id="pattern" class="alt"><div class="container"><h2>CUET (UG) exam pattern</h2>
<p class="muted" style="margin-top:-.4em">As given in NTA's CUET (UG) 2026 Information Bulletin, the latest cycle (exam held in May–June 2026). Always check <a href="https://cuet.nta.nic.in/" rel="noopener" target="_blank">cuet.nta.nic.in</a> for the current year.</p>
<div class="grid g2">
 <div class="card"><div class="table-wrap"><table class="data"><tr><th style="text-align:left">Item</th><th style="text-align:left">CUET (UG) 2026</th></tr>
  <tr><td style="text-align:left">Subjects offered</td><td style="text-align:left">37: 13 languages, 23 domain subjects, 1 General Aptitude Test</td></tr>
  <tr><td style="text-align:left">Choice</td><td style="text-align:left">Up to 5 subjects, including languages and the General Aptitude Test</td></tr>
  <tr><td style="text-align:left">Questions per paper</td><td style="text-align:left">50 MCQs, all compulsory</td></tr>
  <tr><td style="text-align:left">Time per paper</td><td style="text-align:left">60 minutes (PwBD candidates get 20 minutes extra per hour)</td></tr>
  <tr><td style="text-align:left">Marking</td><td style="text-align:left">+5 correct, −1 wrong, 0 unanswered</td></tr>
  <tr><td style="text-align:left">Mode</td><td style="text-align:left">Computer-based test (CBT), in 13 languages</td></tr></table></div>
  <p class="muted" style="font-size:.85rem;margin:.6em 0 0">Sources: <a href="{OFFICIAL_IB}" rel="noopener" target="_blank">NTA Information Bulletin</a> and <a href="{OFFICIAL_SYL}" rel="noopener" target="_blank">CUET (UG) 2026 syllabus</a>.</p></div>
 <div class="card"><h3>What each paper covers (official syllabus)</h3><ul class="clean">
  <li><b>General Aptitude Test (501):</b> general knowledge, current affairs, general mental ability, numerical ability, quantitative reasoning (simple arithmetic, algebra, geometry, mensuration, statistics), logical and analytical reasoning, and general science and environment literacy.</li>
  <li><b>English (101):</b> reading comprehension with factual, narrative and literary passages of up to 300 words, plus verbal ability: rearranging parts, matching, choosing the correct word, synonyms and antonyms.</li>
  <li><b>Mathematics / Applied Mathematics (319):</b> Section A (common to both), then Section B1 (Mathematics) or B2 (Applied Mathematics). Coaching sites commonly describe this as 15 questions from A plus 35 from B1 or B2. NTA's bulletin itself says only that each paper has 50 compulsory questions.</li></ul>
  <div class="notice" style="margin-top:12px">We do not include current affairs, because such questions go out of date quickly. Our GK questions are static facts that we checked against official or standard references. For current affairs, follow a reliable news source.</div></div>
</div></div></section>
<section><div class="container"><h2>CUET topics</h2><p class="muted" style="margin-top:-.4em">Tap a topic to practise it with instant solutions.</p>
<h2 style="font-size:1.25rem;margin-top:1.2em">General Aptitude Test</h2>{cuet_cards('gat')}
<h2 style="font-size:1.25rem;margin-top:1.6em">English</h2>{cuet_cards('english')}
<h2 style="font-size:1.25rem;margin-top:1.6em">Mathematics</h2>{cuet_cards('maths')}
<div class="notice" style="margin-top:22px">Still to come: Section B2 (Applied Mathematics) questions, other languages and domain subjects, and full-length 50-question English and Maths papers (our bank is smaller than 50 for these, so their sectionals are shorter but keep the real pace of 72 seconds per question).</div>
</div></section>
""", desc="CUET (UG) practice: General Aptitude Test, English and Mathematics with CUET marking (+5/−1), timed sectionals and topic practice. Original questions with worked solutions.")

practice_page("cuet-practice.html", "cuet", "CUET", "cuet.html", "CUET (UG)", "Real pace · +5 / −1 marking · results at the end",
    [("gat", "🧠 General Aptitude"), ("english", "📖 English"), ("maths", "➗ Maths")], "CUET (UG) Practice: Sectionals & Topic Practice",
    "CUET (UG) sectionals for the General Aptitude Test, English and Mathematics with +5/−1 marking, plus topic practice with instant solutions.")

# ---------- PLACEHOLDERS ----------
page("mock-tests.html","Mock Tests","""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / Mock Tests</div><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">Mock tests <span class="badge soon">Coming soon</span></h1><p class="muted">We're planning full-length and sectional mocks with an exam-style interface and detailed analysis.</p></div></div>
<section style="padding-top:16px"><div class="container"><div class="grid g3">
 <div class="card"><h3>CAT Full Mock</h3><p class="muted">VARC · DILR · QA · 120 min · 66 Qs</p><button class="btn btn-sm" disabled>Coming soon</button></div>
 <div class="card"><h3>Bank PO Prelims</h3><p class="muted">Quant · Reasoning · 60 min</p><button class="btn btn-sm" disabled>Coming soon</button></div>
 <div class="card"><h3>SSC CGL Tier 1</h3><p class="muted">Quant · Reasoning · 60 min</p><button class="btn btn-sm" disabled>Coming soon</button></div>
 <div class="card"><h3>GMAT-style Quant</h3><p class="muted">21 Qs · 45 min</p><button class="btn btn-sm" disabled>Coming soon</button></div>
</div><div class="notice" style="margin-top:20px">CAT sectionals (VARC, DILR, QA) are already available on the <a href="cat-practice.html">CAT practice page</a>. Meanwhile, try the <a href="practice.html">timed practice quizzes</a>.</div></div></section>
""", desc="Full-length mock tests are coming soon. CAT sectionals and timed practice quizzes are available now.", noindex=True)

page("placements.html","Placement Prep","""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / Placement Prep</div><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">Campus placement prep <span class="badge soon">Coming soon</span></h1><p class="muted">Company-wise aptitude practice for service and product companies.</p></div></div>
<section style="padding-top:16px"><div class="container"><div class="grid g4">
 <div class="card"><h3>TCS NQT</h3><p class="muted">Numerical, verbal and reasoning ability</p></div>
 <div class="card"><h3>Infosys</h3><p class="muted">Logical reasoning, maths, pseudo-code</p></div>
 <div class="card"><h3>Accenture</h3><p class="muted">Cognitive and technical assessment</p></div>
 <div class="card"><h3>Wipro / Capgemini</h3><p class="muted">Aptitude, logical and verbal</p></div>
</div>
<div class="card" style="margin-top:20px"><h3>Most-asked placement topics</h3><div class="tags"><span class="tag">Percentages</span><span class="tag">Profit &amp; Loss</span><span class="tag">Time &amp; Work</span><span class="tag">TSD</span><span class="tag">Number Series</span><span class="tag">Coding-Decoding</span><span class="tag">Blood Relations</span><span class="tag">Seating</span><span class="tag">Data Interpretation</span></div>
<a class="btn btn-sm" href="practice.html?section=mixed">Practise mixed aptitude now →</a></div></div></section>
""", desc="Company-wise campus placement aptitude prep is coming soon. Practise mixed aptitude questions now.", noindex=True)

exec(open("tools/pages_info.py").read())
