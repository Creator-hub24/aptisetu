# Month 2 pages: Bank/SSC hub + exam pages, guides, formula sheets. Executed by build_pages.py (shares globals).
exec(open("tools/guides.py").read()); exec(open("tools/sheets.py").read())
assert check_guides() and check_sheets()
TAGN={"cat":("CAT","tag-cat"),"cuet":("CUET","tag-cuet"),"bank":("Bank/SSC","tag-bank")}
def ehead(crumbs, h1, lead, cta=""):
    cr=" / ".join([f'<a href="index.html">Home</a>']+[f'<a href="{h}">{t}</a>' if h else t for h,t in crumbs])
    return f"""<div class="page-head"><div class="container"><div class="breadcrumb">{cr}</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.5rem)">{h1}</h1><p class="muted" style="max-width:740px">{lead}</p>{cta}</div></div>"""
def qlinks(items): return ", ".join(f'<a href="q/bank-ssc/{s}.html">{t}</a>' for s,t in items)
QT=[("quant-percentages","Percentages"),("quant-ratio-proportion","Ratio"),("quant-averages-alligation","Averages &amp; alligation"),("quant-profit-loss","Profit &amp; loss"),("quant-simple-compound-interest","SI &amp; CI"),("quant-time-speed-distance","Speed"),("quant-time-work","Time &amp; work"),("quant-number-system","Number system"),("quant-geometry-mensuration","Mensuration")]
RT=[("reasoning-seating-arrangement","Seating"),("reasoning-puzzles","Puzzles"),("reasoning-syllogisms","Syllogisms"),("reasoning-inequalities","Inequalities"),("reasoning-coding-decoding","Coding-decoding"),("reasoning-blood-relations","Blood relations"),("reasoning-direction-sense","Directions"),("reasoning-ranking-order","Ranking")]
DT=[("dilr-tables","Tables"),("dilr-bar-charts","Bar charts"),("dilr-pie-charts","Pie charts"),("dilr-line-graphs","Line graphs"),("dilr-caselets","Caselets")]
EXAMS=[
 ("ibps-po","IBPS PO","IBPS PO Exam Pattern &amp; Practice","IBPS PO (CRP PO/MT-XVI) exam pattern from the official notification: prelims, mains and descriptive test, with practice questions for each section.",
  [("Reasoning Ability",RT),("Quantitative Aptitude / Data Analysis &amp; Interpretation",QT+DT),("English Language",None),("General / Economy / Banking Awareness (Mains)",None)]),
 ("ibps-clerk","IBPS Clerk","IBPS Clerk Exam Pattern &amp; Practice","IBPS Clerk (CRP CSA-XVI) exam pattern from the official notification: prelims and mains sections, marks and timing, with practice questions.",
  [("Reasoning Ability",RT),("Numerical Ability / Quantitative Aptitude",QT),("English Language",None),("General / Financial Awareness (Mains)",None)]),
 ("sbi-po","SBI PO","SBI PO 2026 Exam Pattern &amp; Practice","SBI PO 2026 exam pattern from the official advertisement: Phase I, Phase II and Phase III, with practice questions for reasoning and quant.",
  [("Reasoning &amp; Computer Aptitude",RT),("Quantitative Aptitude / Data Analysis &amp; Interpretation",QT+DT),("English Language",None),("General / Economy / Banking Awareness (Phase II)",None)]),
 ("ssc-cgl","SSC CGL","SSC CGL 2026 Exam Pattern &amp; Practice","SSC CGL 2026 exam pattern from the official notice: Tier I and Tier II sections, marks, timing and negative marking, with practice questions.",
  [("General Intelligence &amp; Reasoning",RT),("Quantitative Aptitude / Mathematical Abilities",QT),("English Comprehension",None),("General Awareness",None)]),
 ("ssc-chsl","SSC CHSL","SSC CHSL 2026 Exam Pattern &amp; Practice","SSC CHSL 2026 exam pattern from the official notice: Tier I and Tier II sections, marks, timing and negative marking, with practice questions.",
  [("General Intelligence",RT),("Quantitative Aptitude (basic arithmetic)",QT),("English Language",None),("General Awareness",None)]),
]
GUIDE_FOR={"ibps-po":["bank-prelims-reasoning-puzzles","negative-marking-guessing-maths","simple-compound-interest"],"ibps-clerk":["bank-prelims-reasoning-puzzles","percentages-successive-change","negative-marking-guessing-maths"],"sbi-po":["bank-prelims-reasoning-puzzles","ratio-mixtures-alligation","negative-marking-guessing-maths"],"ssc-cgl":["negative-marking-guessing-maths","time-speed-distance","percentages-successive-change"],"ssc-chsl":["negative-marking-guessing-maths","simple-compound-interest","time-speed-distance"]}
GT={g["slug"]:g for g in GUIDES}
def glink(s): return f'<a href="guide-{s}.html">{GT[s]["h1"]}</a>'

# ---- Bank & SSC hub ----
rows="".join(f'<tr><th scope="row"><a href="{k}.html">{n}</a></th><td>{FACTS[k]["rows"][1][1]}</td><td>{FACTS[k]["rows"][-1][1]}</td><td>{srcl(FACTS[k]["src"][0])}</td></tr>' for k,n,*_ in EXAMS)
cards="".join(f'<a class="card card-link" href="{k}.html"><h3>{n}</h3><p class="muted">{FACTS[k]["rows"][0][1]}</p></a>' for k,n,*_ in EXAMS)
page("bank-ssc.html","Bank &amp; SSC Exams: IBPS, SBI, SSC Patterns",ehead([(None,"Bank &amp; SSC")],"Bank &amp; SSC exams","Official patterns for IBPS PO, IBPS Clerk, SBI PO, SSC CGL and SSC CHSL, with free Quant, Reasoning and DI practice.",'<div class="cta-row"><a class="btn" href="practice.html?exam=general">Start a timed quiz →</a></div>')+f"""
<section style="padding-top:16px"><div class="container"><aside class="facts" aria-label="Bank and SSC key facts"><h2 class="facts-h">Key facts: first stage of each exam</h2>
<div class="table-wrap"><table class="data"><thead><tr><th>Exam</th><th>First stage (prelims / Tier I)</th><th>Negative marking</th><th>Official source</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="facts-src">From the official notices, checked {CHECKED}. Exam dates are not shown because the notices give only tentative months or say “to be notified”. Always confirm on <a href="https://www.ibps.in/" rel="noopener" target="_blank">ibps.in</a>, <a href="https://sbi.bank.in/web/careers/current-openings" rel="noopener" target="_blank">sbi.bank.in</a> or <a href="https://ssc.gov.in/" rel="noopener" target="_blank">ssc.gov.in</a>.</p></aside></div></section>
<section><div class="container"><h2>Exam pages</h2><div class="grid g3">{cards}</div></div></section>
<section class="alt"><div class="container"><h2>Study material</h2><div class="grid g3">
<a class="card card-link" href="formula-bank-ssc-quant.html"><h3>Quant formula sheet</h3><p class="muted">One printable page, with a PDF.</p></a>
<a class="card card-link" href="formula-reasoning.html"><h3>Reasoning shortcuts</h3><p class="muted">Clocks, calendars, ranking, syllogisms.</p></a>
<a class="card card-link" href="guides.html"><h3>Guides</h3><p class="muted">Strategy and topic guides with worked examples.</p></a></div></div></section>
""",desc="IBPS PO, IBPS Clerk, SBI PO, SSC CGL and SSC CHSL exam patterns from the official notices, with free timed practice for Quant, Reasoning and DI.")

for k,n,title,desc,secs in EXAMS:
    syl=""
    for sname,topics in secs:
        body=("Practise: "+qlinks(topics)+".") if topics else "Not covered on this site yet. Use the official notice and standard resources for this section."
        syl+=f'<div class="card"><h3>{sname}</h3><p>{body}</p></div>'
    others=" · ".join(f'<a href="{kk}.html">{nn}</a>' for kk,nn,*_ in EXAMS if kk!=k)
    page(f"{k}.html",title,ehead([("bank-ssc.html","Bank &amp; SSC"),(None,n)],f"{n}: exam pattern and practice",f"The pattern below is taken from the official notice. The practice links go to free, original questions with worked solutions.",'<div class="cta-row"><a class="btn" href="practice.html?exam=general">Start a timed quiz →</a></div>')+f"""
<section style="padding-top:16px"><div class="container">{facts_box(k)}</div></section>
<section><div class="container"><h2>Syllabus summary and practice</h2><p class="muted" style="margin-top:-.4em">Sections as named in the official notice. The topic lists are what we cover on this site, not an official syllabus.</p><div class="grid g2">{syl}</div></div></section>
<section class="alt"><div class="container"><h2>Read next</h2><ul class="clean">{"".join(f"<li>{glink(s)}</li>" for s in GUIDE_FOR[k])}<li><a href="formula-bank-ssc-quant.html">Bank &amp; SSC Quant formula sheet</a> and <a href="formula-reasoning.html">reasoning shortcuts</a></li></ul>
<p class="muted">Other exams: {others}</p></div></section>
""",desc=desc)

# ---- Guides ----
def faq_html(faq): return "".join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q,a in faq)
for g in GUIDES:
    ids=[("s%d"%i) for i in range(len(g["sections"]))]
    toc="".join(f'<li><a href="#{i}">{h}</a></li>' for i,(h,_) in zip(ids,g["sections"]))+'<li><a href="#faq">FAQ</a></li><li><a href="#sources">Sources</a></li>'
    secs="".join(f'<h2 id="{i}">{h}</h2>{b}' for i,(h,b) in zip(ids,g["sections"]))
    srcs="".join(f"<li>{srcl(s)}</li>" for s in g["src"])+"".join(f'<li><a href="{A(u)}" rel="noopener" target="_blank">{t}</a></li>' for t,u in g["ext"])
    srcs+="<li>Worked examples and tables: calculated by us and re-checked by script when the site is built.</li>"
    tags="".join(f'<span class="exam-tag {TAGN[t][1]}">{TAGN[t][0]}</span> ' for t in g["tags"])
    rel="".join(f'<a class="btn btn-ghost btn-sm" href="{h}">{t}</a>' for h,t in g["links"])
    page(f"guide-{g['slug']}.html",g["title"],ehead([("guides.html","Guides"),(None,g["title"].split(":")[0])],g["h1"],g["lead"])+f"""
<section style="padding-top:12px"><div class="container guide">
<p>{tags}<span class="muted">Updated {CHECKED}</span></p>
<nav class="toc" aria-label="Contents"><h2 class="toc-h">Contents</h2><ol>{toc}</ol></nav>
<aside class="insight" aria-label="Key insights"><h2 class="insight-h">Key insights</h2><ul>{"".join(f"<li>{x}</li>" for x in g["insights"])}</ul></aside>
{secs}
<h2 id="faq">FAQ</h2>{faq_html(g["faq"])}
<h2 id="sources">Sources</h2><ul class="sources">{srcs}</ul>
<h2>Practise this</h2><div class="cta-row">{rel}</div>
</div></section>""",desc=g["desc"])
gcards=lambda tag:"".join(f'<a class="card card-link" href="guide-{g["slug"]}.html"><h3>{g["h1"]}</h3><p class="muted">{g["lead"]}</p></a>' for g in GUIDES if g["tags"][0]==tag)
page("guides.html","Exam Guides: CAT, CUET, Bank &amp; SSC",ehead([(None,"Guides")],"Guides","Strategy and topic guides with tables, worked examples and FAQs. Exam facts come from official notices; every calculation is re-checked by script.")+f"""
<section style="padding-top:12px"><div class="container"><h2>CAT</h2><div class="grid g3">{gcards("cat")}</div>
<h2>CUET (UG)</h2><div class="grid g3">{gcards("cuet")}</div>
<h2>Bank &amp; SSC</h2><div class="grid g3">{gcards("bank")}</div></div></section>""",desc="Free guides for CAT, CUET (UG), Bank and SSC exams: exam patterns from official notices, negative-marking maths, percentages, speed, interest, mixtures, DILR and RC.")

# ---- Formula sheets ----
for s in SHEETS:
    grp="".join(f'<div class="fs-group"><h2>{n}</h2><ul>{"".join(f"<li><span class=fs-f>{f}</span>"+(f" <span class=fs-n>{nt}</span>" if nt else "")+"</li>" for f,nt in items)}</ul></div>' for n,items in s["groups"])
    page(f"formula-{s['slug']}.html",s["title"],f"""<div class="container sheet">
<div class="breadcrumb no-print"><a href="index.html">Home</a> / <a href="formula-sheets.html">Formula sheets</a> / {s['h1']}</div>
<div class="sheet-head"><h1>{s['h1']}</h1><p class="muted">aptisetu.com · free to print and share · every formula checked by script · {CHECKED}</p>
<div class="cta-row no-print"><a class="btn" href="assets/pdf/formula-{s['slug']}.pdf" download>Download PDF</a><a class="btn btn-ghost" href="flashcards.html#{s['slug']}">Practise as flashcards</a></div></div>
<div class="fs-grid">{grp}</div>
<p class="muted sheet-foot">Practise these at aptisetu.com · <span class="no-print">Found an error? <a href="contact.html">Tell us</a>.</span></p></div>""",desc=s["desc"])
page("formula-sheets.html","Printable Formula Sheets: Quant &amp; Reasoning",ehead([(None,"Formula sheets")],"Printable formula sheets","One page each, as a web page or a PDF. Every formula on these sheets is checked numerically when the site is built.")+f"""
<section style="padding-top:12px"><div class="container"><div class="grid g3">{"".join(f'<div class="card"><h3><a href="formula-{s["slug"]}.html">{s["h1"]}</a></h3><p class="muted">{len(sum((i for _,i in s["groups"]),[]))} formulas in {len(s["groups"])} groups.</p><p><a href="assets/pdf/formula-{s["slug"]}.pdf" download>PDF</a> · <a href="flashcards.html#{s["slug"]}">Flashcards</a></p></div>' for s in SHEETS)}</div></div></section>""",desc="Free printable formula sheets (HTML and PDF): CAT Quant, Bank and SSC Quant, and reasoning shortcuts, each formula checked by script.")
