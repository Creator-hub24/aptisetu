import os, json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
QB = json.load(open("data/questions.json"))
NQ = sum(len(s["questions"]) for s in QB.values())
NT = len({(k, q["topic"]) for k, s in QB.items() for q in s["questions"]})
def page(fn, title, body, desc="Quantitative Aptitude, Logical Reasoning and DILR prep for CAT, Bank, SSC, GMAT and campus placements.", extra=""):
    html=f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | {{BRAND}}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header id="site-header"></header>
<main>
{body}
</main>
<footer id="site-footer"></footer>
<script src="assets/js/config.js"></script>
<script src="assets/js/layout.js"></script>
<script src="assets/js/stats.js"></script>
{extra}
</body>
</html>
"""
    open(fn,"w").write(html)

# ---------- LANDING ----------
page("index.html","Aptitude, Reasoning & DILR Prep", f"""
<section class="hero"><div class="container hero-grid">
 <div>
  <span class="pill">🇮🇳 CAT · Bank · SSC · Placements</span>
  <h1>Master <span class="grad">Quant, Reasoning &amp; DILR</span> the smart way</h1>
  <p class="lead">Short concept notes, formula sheets and timed practice with worked solutions, for competitive exams and campus placement tests.</p>
  <div class="cta-row hero-cta"><a href="practice.html" class="btn">Start a free quiz →</a><a href="#sections" class="btn btn-ghost">Explore topics</a></div>
  <div class="stats"><div><b>3</b><span>Sections</span></div><div><b data-stat="topics">{NT}</b><span>Topics</span></div><div><b data-stat="questions">{NQ}</b><span>Practice questions</span></div></div>
 </div>
 <div class="hero-card" aria-hidden="true">
  <div class="q-meta"><span>Quant · Time &amp; Work</span><span class="timer-chip">⏱ 01:24</span></div>
  <p style="font-weight:600;margin:.2em 0 .6em">A finishes a job in 12 days, B in 18 days. Together they need?</p>
  <div class="mini-opt">A. 6 days</div><div class="mini-opt sel">B. 7.2 days ✓</div><div class="mini-opt">C. 7.5 days</div><div class="mini-opt">D. 15 days</div>
  <div class="progress" style="margin:14px 0 0"><i style="width:60%"></i></div>
 </div>
</div></section>

<section><div class="container">
 <div class="section-head"><h2>Who is <span data-brand></span> for?</h2><p class="muted">One place to practise for the aptitude tests you'll face.</p></div>
 <div class="grid g4 m2 compact">
  <div class="card"><div class="icon">🎯</div><h3>MBA aspirants</h3><p class="muted">CAT, XAT, SNAP, NMAT and GMAT-style Quant &amp; DILR.</p></div>
  <div class="card"><div class="icon">🏦</div><h3>Bank &amp; SSC</h3><p class="muted">IBPS, SBI, SSC CGL/CHSL arithmetic and reasoning.</p></div>
  <div class="card"><div class="icon">💼</div><h3>Campus placements</h3><p class="muted">Aptitude rounds like TCS NQT, Infosys and Accenture.</p></div>
  <div class="card"><div class="icon">📚</div><h3>College students</h3><p class="muted">Build strong fundamentals early with short practice.</p></div>
 </div>
</div></section>

<section id="sections" class="alt"><div class="container">
 <div class="section-head"><h2>Three sections. The topics that matter.</h2><p class="muted">Start with the concepts, revise with the formula sheet, then test yourself against the clock.</p></div>
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

<section><div class="container">
 <div class="section-head"><h2>What you get today</h2></div>
 <div class="grid g4 m2 compact">
  <div class="card"><div class="icon">⏱️</div><h3>Timed quizzes</h3><p class="muted">Timer, question palette, mark-for-review and optional +3/−1 marking.</p></div>
  <div class="card"><div class="icon">💡</div><h3>Worked solutions</h3><p class="muted">Every question has a step-by-step solution, shown after you submit.</p></div>
  <div class="card"><div class="icon">📝</div><h3>Notes &amp; formula sheets</h3><p class="muted">A concept note and a formula sheet for each of the three sections.</p></div>
  <div class="card soon-card"><div class="icon">🚧</div><h3>Coming soon</h3><ul class="soon-list"><li>Full-length mock tests</li><li>Company-wise placement sets</li><li>Progress analytics</li></ul></div>
 </div>
</div></section>

<section class="alt about"><div class="container" style="max-width:760px;text-align:center">
 <h2>About <span data-brand></span></h2>
 <p class="muted"><span data-brand></span> is a new, free practice site for Indian students preparing for aptitude tests: MBA entrance exams, bank and SSC exams, and campus placements. Every question here is written by us and comes with a worked solution. We're starting small and adding more questions and topics over time.</p>
 <p class="muted" style="margin:0">No login is needed to practise.</p>
</div></section>

<section><div class="container"><div class="cta-band">
 <h2>Start practising in under 10 seconds</h2><p style="opacity:.9">No signup needed. Pick a section and beat the clock.</p>
 <div class="cta-row" style="justify-content:center;margin-bottom:0"><a href="practice.html" class="btn">Start a free quiz →</a></div>
</div></div></section>
""")

# ---------- SECTION PAGES ----------
def section_page(fn, key, title, color, intro, topics, note, formulas):
    import html as _h
    cnt={}
    for q in QB[key]["questions"]: cnt[q["topic"]]=cnt.get(q["topic"],0)+1
    names=[_h.unescape(t) for t,d,p in topics]
    missing=[n for n in names if cnt.get(n,0)<4]; extra=set(cnt)-set(names)
    assert not missing and not extra, (key, missing, extra)
    tl="".join(f"<a class='topic' href='practice.html?section={key}&amp;topic={_h.escape(_h.unescape(t)).replace(' ','%20').replace('&amp;','%26')}' data-topic=\"{_h.escape(_h.unescape(t))}\"><h4>{t} <span class='badge' data-topic-count>{cnt[_h.unescape(t)]} Qs</span></h4><p>{d}</p></a>" for t,d,p in topics)
    fl="".join(f"<div>{f}</div>" for f in formulas)
    page(fn,title,f"""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / {title}</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">{title}</h1><p class="muted" style="max-width:700px">{intro}</p>
<div class="cta-row"><a class="btn" href="practice.html?section={key}">Practise {title} →</a><a class="btn btn-ghost" href="#formulas">Formula sheet</a></div></div></div>
<section style="padding-top:20px"><div class="container"><h2>Topics</h2><p class='muted' style='margin-top:-.4em'>Tap a topic to practise just that topic.</p><div class="topic-list">{tl}</div></div></section>
<section class="alt"><div class="container note" style="max-width:860px"><h2>Concept note</h2>{note}</div></section>
<section id="formulas"><div class="container" style="max-width:860px"><h2>Formula &amp; rules sheet</h2><div class="formula">{fl}</div>
<p class="muted" style="margin-top:1em">Tip: bookmark this page and revise it for 5 minutes before each practice session.</p></div></section>
""")

section_page("quant.html","quant","Quantitative Aptitude","var(--quant)",
"Arithmetic, algebra, geometry and modern maths for CAT, Bank/SSC, GMAT and placement tests.",
[("Percentages","Percentage change, successive change, conversions",1),("Profit &amp; Loss","CP, SP, marked price, discount",1),("Simple &amp; Compound Interest","SI, CI, effective rate",1),("Ratio &amp; Proportion","Ratios, partnership, proportions",1),("Averages &amp; Alligation","Averages, mixtures and alligation",1),("Time &amp; Work","Work rates, pipes and cisterns",1),("Time, Speed &amp; Distance","Trains, boats, relative speed",1),("Number System","Remainders, factorials, HCF/LCM, factors",1),("Algebra","Linear equations, identities, quadratics",1),("Geometry &amp; Mensuration","Triangles, circles, areas, volumes",1),("Permutations &amp; Combinations","Arrangements, selections",1),("Probability","Classical probability, dice, cards",1)],
"""<h3>Percentages: the core idea</h3><p>A percentage is a fraction with denominator 100. Learn the fraction–percentage pairs (1/8 = 12.5%, 1/6 ≈ 16.67%, 1/12 ≈ 8.33%) so you can do percentage maths mentally.</p>
<p><b>Successive change:</b> if a value changes by a% and then by b%, the net change is <b>a + b + ab/100</b>%. For example, +20% then −20% gives 20 − 20 − 4 = <b>−4%</b>.</p>
<div class="tip">💡 <b>Shortcut:</b> after a fall of x%, the rise needed to get back to the original value is x/(100 − x) × 100%. After a 20% fall you need a 25% rise.</div>
<h3>Profit &amp; Loss</h3><p>Profit % and loss % are always calculated on <b>cost price</b>. Discount is always calculated on <b>marked price</b>. Selling at a loss of x% means SP = CP × (100 − x)/100.</p>
<h3>Time, Speed &amp; Distance</h3><p>To convert km/h to m/s, multiply by 5/18. A train crossing a pole covers its own length. A train crossing a platform covers its own length plus the platform's. For equal distances at speeds x and y, the average speed is the <b>harmonic mean</b> 2xy/(x + y), not the simple average.</p>""",
["Successive % change = a + b + ab/100","Profit % = (SP − CP)/CP × 100","SP = MP × (1 − d/100)","SI = P × R × T / 100","CI: A = P(1 + R/100)ⁿ","Speed = Distance / Time ; 1 km/h = 5/18 m/s","Avg speed (equal distances) = 2xy/(x + y)","Work: if A takes a days and B takes b days, together = ab/(a + b)","Trailing zeros of n! = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …","(a + b)² = a² + 2ab + b² ; a² − b² = (a + b)(a − b)","x² + 1/x² = (x + 1/x)² − 2","nPr = n!/(n − r)! ; nCr = n!/(r!(n − r)!)","Arrangements with repeats = n!/(p! q! …)","P(E) = favourable / total outcomes","Circle: area πr², circumference 2πr ; right triangle circumradius = hypotenuse/2"])

section_page("reasoning.html","reasoning","Logical Reasoning","var(--reason)",
"Verbal and analytical reasoning for Bank/SSC, CAT LR and placement tests, with methods for the most common question types.",
[("Syllogisms","All / Some / No statements, Venn method",1),("Seating Arrangement","Linear and circular",1),("Blood Relations","Family trees and coded relations",1),("Coding-Decoding","Letter shifts, number and word codes",1),("Puzzles","Floor and matching puzzles",1),("Direction Sense","Distance and final direction",1),("Number &amp; Letter Series","Find the pattern",1),("Odd One Out","Classification",1),("Clocks &amp; Calendars","Angles, odd days",1),("Alphabet Test","Letter positions and ordering",1),("Inequalities","Direct inequalities with conclusions",1),("Ranking &amp; Order","Positions in a row, comparisons",1)],
"""<h3>Syllogisms: use Venn diagrams</h3><p>Draw the <b>smallest</b> diagram that fits every statement. A conclusion follows only if it is true in <b>every</b> possible diagram.</p>
<ul><li><b>All A are B</b>: circle A sits inside circle B. It also implies <i>Some B are A</i>.</li><li><b>Some A are B</b>: the circles overlap. It implies <i>Some B are A</i>.</li><li><b>No A is B</b>: the circles don't touch. It implies <i>No B is A</i>.</li></ul>
<div class="tip">💡 "Some A are not B" never follows from "Some A are B" on its own. Look for a statement that rules it out.</div>
<h3>Seating arrangement</h3><p>Fix the most definite clue first, such as "X is in the middle" or "Y is at an end". In a row facing north, the person's <b>right</b> is your right. In a circle facing the centre, <b>left is clockwise</b>.</p>
<h3>Blood relations</h3><p>Draw a family tree. Use + for male and − for female, horizontal lines for siblings and spouses, and vertical lines for generations. Break long chains like "my father's father's only son" from the end backwards.</p>""",
["Syllogism: All A→B ⇒ Some B→A (conversion)","Some A→B ⇒ Some B→A ; No A→B ⇒ No B→A","Coding: A=1 … Z=26 ; reverse position = 27 − n","EJOTY → 5, 10, 15, 20, 25 (position anchors)","Clock angle = |30H − 5.5M|°","Hands overlap every 65 5/11 minutes","Odd days: normal year = 1, leap year = 2","Direction: right turn from N → E → S → W","Distance after turns: use Pythagoras √(x² + y²)","Series checks: differences, ratios, squares/cubes, n(n+1), ×2±1"])

section_page("dilr.html","dilr","Data Interpretation &amp; Logical Reasoning (DILR)","var(--dilr)",
"Read data fast and reason carefully: tables, charts, caselets, arrangements, tournaments, Venn diagrams and routes.",
[("Tables","Multi-row data, growth, share",1),("Bar Charts","Reading and comparing bars",1),("Pie Charts","Percentages and central angles",1),("Line Graphs","Trends and month-on-month change",1),("Caselets","Paragraph-based data",1),("Arrangements","Table seating and matching grids",1),("Games &amp; Tournaments","Knock-outs, round robins",1),("Venn Diagrams","2- and 3-set problems",1),("Network &amp; Routes","Shortest routes on a road map",1)],
"""<h3>How to approach a DI set</h3><ol><li><b>Scan for 30 seconds:</b> note the units, the totals and what each axis or column means.</li><li><b>Approximate:</b> most DI options are far enough apart that rounding works (e.g. 487/1210 ≈ 40%).</li><li><b>Reuse:</b> compute totals or growth once and use them for every question in the set.</li></ol>
<h3>Growth and share</h3><p><b>Growth %</b> = (New − Old)/Old × 100. <b>Share %</b> = Part/Total × 100. Don't mix these up. A product can have the highest absolute increase but not the highest percentage growth.</p>
<div class="tip">💡 <b>Pie charts:</b> 1% = 3.6°, so 25% = 90° and 10% = 36°.</div>
<h3>Choosing LR sets (CAT)</h3><p>In CAT, set selection matters as much as solving. Spend the first 3–4 minutes scanning every set, then start with the ones that have the most definite clues and the fewest variables.</p>""",
["Growth % = (New − Old)/Old × 100","Share % = Part / Total × 100","CAGR = (End/Start)^(1/n) − 1","Pie: angle = % × 3.6° ; value = % × Total","Average = Sum / Count","Two sets: n(A∪B) = n(A) + n(B) − n(A∩B)","Three sets: n(A∪B∪C) = ΣA − Σ(pairs) + n(A∩B∩C)","Ratio A:B → compare A/B with common factors removed","Round-robin among n teams: nC2 matches","Knock-out among n teams: n − 1 matches"])

# ---------- PRACTICE ----------
page("practice.html","Timed Practice Quiz","""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / Practice</div><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">Timed practice quiz</h1><p class="muted">Choose a section, set the timer and start. Solutions are shown at the end.</p></div></div>
<section style="padding-top:16px"><div class="container">
 <div id="setup" class="card quiz-setup">
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
  <h2>Review &amp; solutions</h2><div id="review"></div>
 </div>
</div></section>
""", extra='<script src="assets/js/quiz.js"></script>')

# ---------- PLACEHOLDERS ----------
page("mock-tests.html","Mock Tests","""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / Mock Tests</div><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">Mock tests <span class="badge soon">Coming soon</span></h1><p class="muted">We're planning full-length and sectional mocks with an exam-style interface and detailed analysis.</p></div></div>
<section style="padding-top:16px"><div class="container"><div class="grid g3">
 <div class="card"><h3>CAT Full Mock</h3><p class="muted">VARC · DILR · QA · 120 min · 66 Qs</p><button class="btn btn-sm" disabled>Coming soon</button></div>
 <div class="card"><h3>DILR Sectional</h3><p class="muted">4 sets · 40 min</p><button class="btn btn-sm" disabled>Coming soon</button></div>
 <div class="card"><h3>Quant Sectional</h3><p class="muted">22 Qs · 40 min</p><button class="btn btn-sm" disabled>Coming soon</button></div>
 <div class="card"><h3>Bank PO Prelims</h3><p class="muted">Quant · Reasoning · 60 min</p><button class="btn btn-sm" disabled>Coming soon</button></div>
 <div class="card"><h3>SSC CGL Tier 1</h3><p class="muted">Quant · Reasoning · 60 min</p><button class="btn btn-sm" disabled>Coming soon</button></div>
 <div class="card"><h3>GMAT-style Quant</h3><p class="muted">21 Qs · 45 min</p><button class="btn btn-sm" disabled>Coming soon</button></div>
</div><div class="notice" style="margin-top:20px">Until then, try the <a href="practice.html">timed practice quizzes</a>.</div></div></section>
""")

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
""")

page("signup.html","Sign up","""
<section><div class="container" style="max-width:480px"><div class="card">
 <h2>Create your free account</h2><p class="muted">Accounts aren't live yet. This form is a preview of signup and doesn't save anything.</p>
 <div id="ok" class="notice hidden">✅ Thanks! This is a preview only. Accounts aren't live yet, so nothing was saved.</div>
 <form class="form" id="signup" onsubmit="event.preventDefault();document.getElementById('ok').classList.remove('hidden');this.reset();">
  <label>Full name<input required placeholder="e.g. Priya Sharma"></label>
  <label>Email<input type="email" required placeholder="you@example.com"></label>
  <label>Mobile (optional)<input type="tel" placeholder="+91 98xxxxxxxx"></label>
  <label>Preparing for<select><option>CAT / MBA entrance</option><option>Bank exams</option><option>SSC exams</option><option>Campus placements</option><option>GMAT</option><option>Other</option></select></label>
  <label>Password<input type="password" required minlength="6" placeholder="At least 6 characters"></label>
  <button class="btn" type="submit">Sign up free</button>
  <p class="muted" style="font-size:.85rem;margin:0">Login will be available when accounts launch.</p>
 </form></div></div></section>
""")

page("contact.html","Contact","""
<div class="page-head"><div class="container"><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">Contact us</h1><p class="muted">Questions, feedback or partnership ideas? We'd love to hear from you.</p></div></div>
<section style="padding-top:16px"><div class="container grid g2">
 <div class="card"><div id="sent" class="notice hidden">✅ Message captured (demo only, nothing was sent).</div>
 <form class="form" onsubmit="event.preventDefault();document.getElementById('sent').classList.remove('hidden');this.reset();">
  <label>Name<input required></label><label>Email<input type="email" required></label>
  <label>Message<textarea rows="5" required></textarea></label><button class="btn" type="submit">Send message</button></form></div>
 <div class="card"><h3>Reach us</h3><p>📧 <a data-email></a></p><p>📍 India (online)</p><p class="muted">Placeholder contact details. Replace them in <code>assets/js/config.js</code>.</p></div>
</div></section>
""")
print("ok")
