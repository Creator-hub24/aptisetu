# Question pages: one static, indexable page per question (q/<track>/<id>-<topic>.html) plus topic hubs and q/index.html.
# Executed by build_pages.py before pages_info.py (shares its globals: page(), A, _esc, _re, SITE_URL, EMAIL, FORM), so
# every page lands in sitemap.xml. Reads the per-section files in data/ (written by build_questions.py); never edits them.
# Excluded on purpose: CAT mock and sectional packs (fixed tests that should stay unseen until attempted; only the open
# bank and practice-* packs, i.e. what guests can already reach through topic practice, are published) and CUET items
# reused from the general bank (source "general"; their page is the general-bank page).
import json as _json, os as _os, shutil as _shq
from urllib.parse import quote as _q
_shq.rmtree("q", ignore_errors=True)
QL = "ABCD"
QTRACKS = [  # track, label, sections, practice URL builder
  ("cat", "CAT", "data/cat/", ["qa", "dilr", "varc"], lambda s, t: f"cat-practice.html?mode=practice&section={s}&topic={_q(t)}"),
  ("cuet", "CUET (UG)", "data/cuet/", ["gat", "english", "maths"], lambda s, t: f"cuet-practice.html?mode=practice&section={s}&topic={_q(t)}"),
  ("bank-ssc", "Bank / SSC", "data/general/", ["quant", "reasoning", "dilr"], lambda s, t: f"practice.html?exam=general&section={s}&topic={_q(t)}"),
]
def _slug(s): return _re.sub(r"[^a-z0-9]+", "-", _esc.unescape(s).lower()).strip("-")[:48]
def _plain(h): return _re.sub(r"\s+", " ", _esc.unescape(_re.sub(r"<[^>]+>", " ", h))).strip()
_HI = _json.load(open("data/hi/general-solutions.json", encoding="utf8"))
def _solhtml(qq, sol, trk):
    """English solution, plus the Hindi translation and an EN/हिंदी toggle for Bank/SSC questions (assets/js/sol-lang.js)."""
    h = _HI.get(qq["id"]) if trk == "bank-ssc" else None
    if not h: return f'<div class="sol"><b>Solution:</b> {sol}</div>'
    return ('<div class="lang-toggle" role="group" aria-label="Solution language"><span class="muted">Solution in:</span><button type="button" data-lang="en">EN</button><button type="button" data-lang="hi" lang="hi">हिंदी</button></div>'
            f'<div class="sol"><b class="sol-h" data-en="Solution:" data-hi="हल:">Solution:</b> <span class="sol-en">{sol}</span><span class="sol-hi" lang="hi" hidden>{h}</span></div>'
            '<script src="assets/js/sol-lang.js" defer></script>')
def _optfix(sol):  # solutions say "Option 1".."Option 4" (bank order); pages show bank order as A-D
    return _re.sub(r"\b([Oo]ptions?) ([1-4](?:(?:, | and | or )[1-4])*)\b", lambda m: m.group(1) + " " + _re.sub(r"[1-4]", lambda d: QL[int(d.group(0)) - 1], m.group(2)), sol)
def _qf_diff(tq):  # difficulty chips for a topic hub (only levels present; none when a hub has a single level)
    lv = [d for d in ("Easy", "Medium", "Hard") if any(x.get("difficulty") == d for x in tq)]
    if len(lv) < 2: return ""
    return ('<div class="qf-bar" data-qf="d" role="group" aria-label="Filter by difficulty"><button type="button" class="qf-chip" data-v="" aria-pressed="true">All</button>'
            + "".join(f'<button type="button" class="qf-chip" data-v="{d}" aria-pressed="false">{d}</button>' for d in lv) + '<span class="qf-count" aria-live="polite"></span></div>')
def _report(qid, ctx, url):
    body = f"Question ID: {qid}\nExam / section: {ctx}\nPage: {url}\n\nWhat looks wrong:\n"
    if FORM: href = FORM.replace("{REPORT}", _q(body)) if "{REPORT}" in FORM else FORM
    if EMAIL and not (FORM and "{REPORT}" in FORM): href = f"mailto:{EMAIL}?subject={_q('Error report: question ' + qid)}&body={_q(body)}"
    ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return f'<a class="report-link" href="{A(href)}"{ext} data-qid="{A(qid)}">⚑ Report an error</a>'
QSTATS = {"pages": 0, "hubs": 0, "excluded": {}}
_hubs = []
QINDEX = []   # data/qindex.json: question-bank search and Mistakes-notebook links
for trk, tlabel, ddir, secs, purl in QTRACKS:
    _os.makedirs(f"q/{trk}", exist_ok=True)
    for s in secs:
        d = _json.load(open(ddir + s + ".json")); sets = d.get("sets", {}); sname = d["name"]
        keep = []
        for qq in d["questions"]:
            pk = qq.get("pack", "")
            if pk and not pk.startswith("practice-"): QSTATS["excluded"][f"{trk} {s} pack {pk.split('-')[0]}"] = QSTATS["excluded"].get(f"{trk} {s} pack {pk.split('-')[0]}", 0) + 1; continue
            if qq.get("source") == "general": QSTATS["excluded"]["cuet reused from bank-ssc"] = QSTATS["excluded"].get("cuet reused from bank-ssc", 0) + 1; continue
            keep.append(qq)
        fn_of = {qq["id"]: f"q/{trk}/{_slug(qq['id'])}-{_slug(qq['topic'])}.html" for qq in keep}
        for qq in keep: QINDEX.append({"k": trk, "id": qq["id"], "u": fn_of[qq["id"]], "e": tlabel, "s": _plain(sname), "t": _plain(qq["topic"]), "d": qq.get("difficulty", ""), "x": _plain(qq["question"])[:140]})
        bytopic = {}
        for qq in keep: bytopic.setdefault(qq["topic"], []).append(qq)
        for topic, tq in bytopic.items():
            hub = f"q/{trk}/{s}-{_slug(topic)}.html"
            _hubs.append((trk, tlabel, sname, topic, hub, len(tq)))
            for i, qq in enumerate(tq):
                fn = fn_of[qq["id"]]; url = SITE_URL + fn
                # similar: same topic, prefer other data sets/passages, nearest in bank order; up to 5
                others = [x for x in tq[i + 1:] + tq[:i] if not qq.get("set") or x.get("set") != qq.get("set")] or [x for x in tq if x is not qq]
                sim = others[:5]
                ctx_html = ""
                if qq.get("set") and qq["set"] in sets:
                    st = sets[qq["set"]]; ctx_html = f'<details class="rv-pane" open><summary>{"Passage" if st["kind"] == "passage" else "Data set"}: {_esc.escape(st["title"])}</summary><div class="q-data">{st["html"]}</div></details>'
                elif qq.get("data"): ctx_html = f'<div class="q-data">{qq["data"]}</div>'
                if qq.get("type", "mcq") == "mcq":
                    opts = "".join(f'<div class="opt"><b>{QL[j]}</b><span>{o}</span></div>' for j, o in enumerate(qq["options"]))
                    ans = f'{QL[qq["answer"]]}. {qq["options"][qq["answer"]]}'; ans_txt = f'{QL[qq["answer"]]}. {_plain(qq["options"][qq["answer"]])}'
                    qtype = "MCQ"
                else:
                    opts = '<p class="muted">Type in the answer (TITA): no options.</p>'; ans = _esc.escape(qq["answer"]); ans_txt = qq["answer"]; qtype = "TITA"
                sol = _optfix(qq["solution"]); ptxt = _plain(qq["question"])
                ctx = f"{tlabel} · {sname} · {topic}"
                title = f"{tlabel} {sname}: {_esc.unescape(topic)} question {qq['id']}"
                desc = f"{tlabel} {_plain(topic)} practice question {qq['id']} with answer and worked solution: {ptxt[:110]}".rstrip() + ("…" if len(ptxt) > 110 else "")
                ld = {"@context": "https://schema.org", "@type": "Quiz", "name": title, "educationalLevel": qq.get("difficulty", ""), "about": {"@type": "Thing", "name": _plain(topic)},
                      "hasPart": [{"@type": "Question", "eduQuestionType": "Multiple choice" if qtype == "MCQ" else "Short answer", "text": ptxt,
                                   **({"suggestedAnswer": [{"@type": "Answer", "text": _plain(o)} for j, o in enumerate(qq["options"]) if j != qq["answer"]]} if qtype == "MCQ" else {}),
                                   "acceptedAnswer": {"@type": "Answer", "text": ans_txt, "answerExplanation": {"@type": "Comment", "text": _plain(sol)}}}]}
                ldj = _json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
                simh = "".join(f'<li><a href="{fn_of[x["id"]]}">{_esc.escape(_plain(x["question"])[:90])}{"…" if len(_plain(x["question"])) > 90 else ""}</a> <span class="muted">· {x.get("difficulty", "")}</span></li>' for x in sim)
                body = f"""<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / <a href="q/index.html">Question bank</a> / <a href="{hub}">{tlabel} {sname}: {topic}</a> / {qq['id']}</div>
<h1 style="font-size:clamp(1.4rem,3.4vw,2rem)">{tlabel} {sname}: {topic} <span class="muted" style="font-weight:500">· {qq['id']}</span></h1>
<p class="muted">{qtype} · {qq.get('difficulty', '')}{(' · ' + _esc.escape(qq['part'])) if qq.get('part') else ''}</p></div></div>
<section style="padding-top:12px"><div class="container" style="max-width:820px"><article class="card qpage" data-qid="{A(qq['id'])}">
{ctx_html}<div class="q-text">{qq['question']}</div>{opts}
<details class="qp-ans"><summary class="btn btn-ghost btn-sm">Show answer &amp; solution</summary>
<p style="margin:.8em 0 .4em">Correct answer: <b>{ans}</b></p>{_solhtml(qq, sol, trk)}</details>
<div style="margin-top:6px">{_report(qq['id'], ctx, url)}</div></article>
<div class="cta-row" style="margin:18px 0"><a class="btn" href="{purl(s, topic)}">Start practice: {topic} →</a><a class="btn btn-ghost" href="{hub}">All {topic} questions</a></div>
{f'<h2 style="font-size:1.2rem">Similar questions</h2><ul class="qp-sim">{simh}</ul>' if simh else ''}
</div></section>"""
                page(fn, _esc.escape(title), body, desc=desc, base=True, head_extra=f'<script type="application/ld+json">{ldj}</script>\n')
                QSTATS["pages"] += 1
            items = "".join(f'<li data-d="{x.get("difficulty", "")}"><a href="{fn_of[x["id"]]}">{_esc.escape(_plain(x["question"])[:110])}{"…" if len(_plain(x["question"])) > 110 else ""}</a> <span class="muted">· {x["id"]} · {x.get("difficulty", "")}</span></li>' for x in tq)
            page(hub, f"{tlabel} {sname}: {topic} questions with solutions", f"""<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / <a href="q/index.html">Question bank</a> / {tlabel} {sname}</div>
<h1 style="font-size:clamp(1.5rem,3.6vw,2.2rem)">{tlabel} {sname}: {topic}</h1><p class="muted">{len(tq)} practice questions, each with the answer and a worked solution.</p>
<div class="cta-row" style="margin:12px 0 0"><a class="btn" href="{purl(s, topic)}">Start practice →</a></div></div></div>
<section style="padding-top:12px"><div class="container">{_qf_diff(tq)}<ol class="qp-list" data-qf-list>{items}</ol></div></section>""", extra='<script src="assets/js/qfilter.js"></script>',
                 desc=f"{len(tq)} free {tlabel} {_plain(sname)} questions on {_plain(topic)}, each with the answer and a worked solution.", base=True)
            QSTATS["hubs"] += 1
_groups = {}
for trk, tlabel, sname, topic, hub, n in _hubs: _groups.setdefault((tlabel, sname), []).append((topic, hub, n))
page("q/index.html", "Question bank: every practice question with solutions", '<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / Question bank</div><h1 style="font-size:clamp(1.6rem,4vw,2.4rem)">Question bank</h1>'
     f'<p class="muted">{QSTATS["pages"]} practice questions by exam and topic, each on its own page with the answer and a worked solution. Full mocks and fixed sectionals are not listed here, so they stay unseen until you take them.</p></div></div><section style="padding-top:12px">'
     + '<div class="container"><div class="qf-bar" data-qf="t" role="group" aria-label="Filter by exam"><button type="button" class="qf-chip" data-v="" aria-pressed="true">All exams</button>' + "".join(f'<button type="button" class="qf-chip" data-v="{t}" aria-pressed="false">{t}</button>' for t in dict.fromkeys(tl for tl, _ in _groups)) + '<input type="search" id="qf-q" placeholder="Search topics or questions, e.g. percentages" aria-label="Search topics and questions"><label class="qf-dl">Difficulty <select id="qf-d"><option value="">Any</option><option>Easy</option><option>Medium</option><option>Hard</option></select></label><span class="qf-count" aria-live="polite"></span></div><div id="qf-res" class="qf-res" hidden><h2 class="qf-res-h" id="qf-res-h">Matching questions</h2><ol class="qf-qs" id="qf-qs"></ol></div><h2 class="qf-res-h" id="qf-topics-h">Topics</h2></div><div class="container grid g3">'
     + "".join(f'<div class="card" data-t="{tl}"><h3>{tl} · {sn}</h3><ul class="qp-hubs">' + "".join(f'<li><a href="{h}">{t}</a> <span class="muted">({n})</span></li>' for t, h, n in v) + "</ul></div>" for (tl, sn), v in _groups.items()) + "</div></section>",
     extra='<script src="assets/js/qfilter.js"></script>',
     desc="Browse every AptiSetu practice question by exam and topic: CAT, CUET (UG), Bank and SSC, each with the answer and a worked solution.", base=True)
_os.makedirs("data", exist_ok=True)
_json.dump(QINDEX, open("data/qindex.json", "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
print("question pages:", QSTATS)
