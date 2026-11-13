# Month 3 pages: Open Mock, account (saved history), AptiSetu Pass, refund policy (draft). exec'd by build_pages.py.
import json as _json
_OM = sorted(_json.load(open("data/open-mock.json", encoding="utf8"))["mocks"], key=lambda m: m["starts_at"])
# Editions shown: every edition that has not ended when the pages are built (the next one first). If all have ended,
# the last one. open-mock.js hides a card once its edition is over and a later card is on the page, so the page stays
# right between rebuilds. No question counts are shown anywhere (site rule).
_omnow3 = _dt.datetime.now(_dt.timezone.utc)
_oms = [m for m in _OM if _dt.datetime.fromisoformat(m["ends_at"]) > _omnow3] or _OM[-1:]
def _om_label(m): return (m.get("label") or "Unranked practice").replace("CAT Mock ", "Mock ")
def _om_card(m, first):
    d = _dt.date.fromisoformat(m["date"]); lab = _esc.escape(_om_label(m))
    btn = "".join(f'<a class="btn{"" if i == 0 else " btn-ghost"} btn-sm" style="margin:4px 6px 0 0" href="cat-practice.html?mode=sectional&amp;section={s}&amp;pack={m["pack"]}&amp;open={m["id"]}">{i+1}. {n}</a>' for i, (s, n) in enumerate([("varc", "VARC"), ("dilr", "DILR"), ("qa", "QA")]))
    if m.get("sealed"):
        note = (f'<b>{lab}.</b> This edition uses a <b>new mock</b> written for the Open Mock. It is not on the <a href="mock-tests.html">mock tests page</a> or in any practice set. '
                'It is still <b>unranked</b>: there is <b>no leaderboard and no rank</b>. The sections open at 10:00 am. Answers and worked solutions open after the edition ends at 10:00 pm.')
        how = ('Take the sections in order. <a href="login.html?next=open-mock.html">Log in</a> before you start: your <b>first attempt of each section</b> during the window is scored on our server and the score is shown as soon as you submit, and saved to your account. '
               'Without login your responses are saved in your browser and scored on this device after 10:00 pm, when the answers open.')
    else:
        pk = m["pack"].replace("mock-", "CAT Mock ")
        note = (f'<b>{lab}.</b> This edition uses the questions of <b>{pk}</b>, which is already free on the <a href="mock-tests.html">mock tests page</a>, so some people may have seen it. '
                'That is why there is <b>no leaderboard and no rank</b> this time. Take it as timed practice under CAT conditions.')
        how = ('Take the sections in order. If you <a href="login.html?next=open-mock.html">log in</a>, your <b>first attempt of each section</b> during the window is scored on our server and saved to your account, so you can see it on any device. Without login you still get your score on screen.')
    return f"""
 <div class="card om-ed"{' id="om-card"' if first else ''} style="margin-bottom:18px" data-mock="{m['id']}" data-start="{m['starts_at']}" data-end="{m['ends_at']}"{' data-sealed="1"' if m.get('sealed') else ''}>
  <h2 style="margin-top:0">{_esc.escape(m['title'])}</h2>
  <div class="notice" style="margin:0 0 12px">{note}</div>
  <p><b>Sunday {d.day} {d.strftime('%B %Y')}</b> · 10:00 am to 10:00 pm IST · VARC, DILR and QA, 40 minutes each · +3 / −1 for a wrong MCQ, 0 for a wrong TITA.</p>
  <p class="om-status muted" role="status">Checking the time…</p>
  <div class="om-start">{btn}</div>
  <p class="muted" style="font-size:.88rem;margin-top:12px">{how}</p>
  <div class="om-mine-wrap" style="margin-top:14px"><h3 style="margin:0 0 6px;font-size:1rem">Your scores for this edition</h3><div class="om-mine" aria-live="polite"><p class="muted">Log in to see the scores saved to your account.</p></div></div>
 </div>"""
_om = _oms[0]
_omlabel_short = _om_label(_om)
page("open-mock.html", "AptiSetu Open Mock", f"""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / <a href="mock-tests.html">Mock Tests</a> / Open Mock</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">AptiSetu Open Mock</h1>
<p class="om-label" style="margin:4px 0 8px"><span class="sbadge soon" style="font-size:.9rem">Unranked practice</span></p>
<p class="muted" style="max-width:720px">One free CAT-pattern mock that everyone can take on the same day. It runs every <b>Sunday, 10:00 am to 10:00 pm IST</b>. Every edition is <b>unranked practice</b>: there is no leaderboard and no rank.</p></div></div>
<section style="padding-top:16px"><div class="container" style="max-width:860px">
{"".join(_om_card(m, i == 0) for i, m in enumerate(_oms))}
 <p class="muted" style="font-size:.85rem">Only you can see your scores. Nothing is shown to other people.</p>
</div></section>
""", desc="AptiSetu Open Mock: a free CAT-pattern mock, every Sunday, 10 am to 10 pm IST. Unranked practice, with no leaderboard and no rank.",
     extra='<script src="assets/js/open-mock.js"></script>')

page("account.html", "My account", f"""
<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / My account</div>
<h1 style="font-size:clamp(1.6rem,3.6vw,2.3rem)">My account</h1><p class="muted" style="max-width:640px">Your saved test history across devices. Results are saved when you finish a quiz, sectional or mock while logged in.</p></div></div>
<section style="padding-top:12px"><div class="container" style="max-width:860px">
 <div id="acct-box" class="card"><p class="muted">Loading…</p></div>
 <div id="acct-profile" class="card" style="margin-top:18px" hidden></div>
 <div id="acct-history" class="card" style="margin-top:18px"></div>
</div></section>
""", desc="Your AptiSetu account: saved test history and AptiSetu Pass status.", noindex=True, extra='<script src="assets/js/account-page.js"></script>')

page("pass.html", "AptiSetu Pass", f"""
<div class="page-head compact-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / AptiSetu Pass</div>
<h1 style="font-size:clamp(1.6rem,3.6vw,2.3rem)">AptiSetu Pass</h1><p class="muted" style="max-width:680px">Free practice stays free: every question, solution, quiz, sectional and the Open Mock itself. When it launches, the Pass will add the extras below.</p></div></div>
<section style="padding-top:12px"><div class="container" style="max-width:860px">
 <div class="card"><h2 style="margin-top:0"><span class="status st-soon">Coming soon</span> What the Pass is planned to add</h2><ul>
  <li><b>Detailed report</b> after every test: weak topics, time per question and your progress graph.</li>
  <li><b>Saved history</b> across devices on <a href="account.html">My account</a>.</li>
  <li><b>Full-length CAT mocks</b> (all three sections with CAT marking).</li></ul>
  <div id="pass-buy"><div class="notice"><b>Not on sale yet.</b> Everything above is <b>free right now</b>: the report after each test, saved history when you log in, and the full mocks on the <a href="mock-tests.html">Mock Tests page</a>. We'll announce the price here first.</div></div>
  <p class="muted" style="font-size:.85rem;margin-top:12px">See the <a href="refund.html">refund policy (draft)</a> and <a href="terms.html">terms</a>.</p></div>
</div></section>
""", desc="AptiSetu Pass: detailed reports, saved history and full CAT mocks. Free practice stays free.", noindex=True, extra='<script src="assets/js/pass-page.js"></script>')

page("refund.html", "Refund policy (draft)", info_head("Refund policy", "Refund policy (draft)", "Draft: this applies only once AptiSetu Pass goes on sale. Nothing is sold today.")+prose(f"""
<div class="notice"><b>Draft.</b> AptiSetu Pass is not on sale yet. This policy will be finalised and dated before the first sale.</div>
<h3>7-day refund, no questions asked</h3><p>If you buy AptiSetu Pass and change your mind, email <a href="mailto:{EMAIL}">{EMAIL}</a> from the email address you log in with within <b>7 days of payment</b>. We will refund the full amount to the original payment method.</p>
<h3>Payment problems</h3><p>If money was deducted but your Pass did not activate, it is usually fixed automatically within a few minutes. If not, email us with the Razorpay payment ID from your receipt and we'll activate it or refund you in full.</p>
<h3>How long refunds take</h3><p>We start the refund within 2 working days of your request. Your bank or card issuer usually credits it within 5 to 7 working days after that.</p>
<h3>After a refund</h3><p>Pass features stop when the refund is processed. Free practice is not affected.</p>
<h3>Payments</h3><p>Payments are processed by Razorpay. We never see or store your card, UPI or bank details.</p>
"""), desc="Draft refund policy for AptiSetu Pass: 7-day full refund, help with failed payments, refund timelines.", noindex=True)
