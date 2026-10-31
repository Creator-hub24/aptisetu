# Month 3 pages: Open Mock, account (saved history), AptiSetu Pass, refund policy (draft). exec'd by build_pages.py.
import json as _json
_OM = _json.load(open("data/open-mock.json", encoding="utf8"))["mocks"]
_om = _OM[-1]
_omd = _dt.date.fromisoformat(_om["date"])
_omsecs = [("varc", "VARC", _om["questions"]["varc"]), ("dilr", "DILR", _om["questions"]["dilr"]), ("qa", "QA", _om["questions"]["qa"])]
_ombtn = "".join(f'<a class="btn{"" if i == 0 else " btn-ghost"} btn-sm" style="margin:4px 6px 0 0" href="cat-practice.html?mode=sectional&amp;section={s}&amp;pack={_om["pack"]}&amp;open={_om["id"]}">{i+1}. {n} · {q} Qs</a>' for i, (s, n, q) in enumerate(_omsecs))
_pack_name = _om["pack"].replace("mock-", "CAT Mock ")
_omlabel = _om.get("label") or f"Unranked practice, {_pack_name} questions"
_omlabel_short = _omlabel.replace("CAT Mock ", "Mock ")
page("open-mock.html", "AptiSetu Open Mock", f"""
<div class="page-head"><div class="container"><div class="breadcrumb"><a href="index.html">Home</a> / <a href="mock-tests.html">Mock Tests</a> / Open Mock</div>
<h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">AptiSetu Open Mock</h1>
<p class="om-label" style="margin:4px 0 8px"><span class="sbadge soon" style="font-size:.9rem">{_esc.escape(_omlabel_short)}</span></p>
<p class="muted" style="max-width:720px">One free CAT-pattern mock that everyone can take on the same day. It runs on the <b>first Sunday of every month, 10:00 am to 10:00 pm IST</b>. This edition is <b>unranked practice</b>: there is no leaderboard and no rank.</p></div></div>
<section style="padding-top:16px"><div class="container" style="max-width:860px">
 <div class="card" id="om-card" data-mock="{_om['id']}" data-start="{_om['starts_at']}" data-end="{_om['ends_at']}">
  <h2 style="margin-top:0">{_esc.escape(_om['title'])}</h2>
  <div class="notice" style="margin:0 0 12px"><b>{_esc.escape(_omlabel_short)}.</b> This edition uses the questions of <b>{_pack_name}</b>, which is already free on the <a href="mock-tests.html">mock tests page</a>, so some people may have seen it. That is why there is <b>no leaderboard and no rank</b> this time. Take it as timed practice under CAT conditions. From the next edition we plan to release a fresh, unpublished mock.</div>
  <p><b>Sunday {_omd.day} {_omd.strftime('%B %Y')}</b> · 10:00 am to 10:00 pm IST · VARC, DILR and QA, 40 minutes each · +3 / −1 for a wrong MCQ, 0 for a wrong TITA.</p>
  <p id="om-status" class="muted" role="status">Checking the time…</p>
  <div id="om-start">{_ombtn}</div>
  <p class="muted" style="font-size:.88rem;margin-top:12px">Take the sections in order. If you <a href="login.html?next=open-mock.html">log in</a>, your <b>first attempt of each section</b> during the window is scored on our server and saved to your account, so you can see it on any device. Without login you still get your score on screen.</p>
 </div>
 <div class="card" style="margin-top:18px"><h2 style="margin-top:0">Your Open Mock scores</h2><div id="om-mine" aria-live="polite"><p class="muted">Log in to see the scores saved to your account.</p></div>
  <p class="muted" style="font-size:.85rem">Only you can see these. Nothing is shown to other people.</p></div>
</div></section>
""", desc=f"AptiSetu Open Mock: a free CAT-pattern mock on the first Sunday of every month, 10 am to 10 pm IST. This edition: {_esc.escape(_omlabel_short)}, no leaderboard and no rank.",
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
