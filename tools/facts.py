# Verified exam facts (official sources only). Executed by build_pages.py; shares its globals (A, _esc).
# Checked on 27 Oct 2026. Do not add a fact here without an official source URL.
CHECKED = "27 Oct 2026"
SRC = {
 "cat_bulletin": ("CAT 2026 Information Bulletin (IIMs, 26 Jul 2026)", "https://iimcat.ac.in/per/g06/pub/32842/EForms/image/CAT2026/CAT2026InformationBulletin_26-07-2026_V2.pdf"),
 "cat_site": ("iimcat.ac.in (official CAT site)", "https://iimcat.ac.in/"),
 "cuet_bulletin": ("CUET (UG) 2026 Information Bulletin (NTA)", "https://cdnbbsr.s3waas.gov.in/s3d1a21da7bca4abff8b0b61b87597de73/uploads/2026/01/202601031633478370.pdf"),
 "cuet_site": ("cuet.nta.nic.in (official CUET site)", "https://cuet.nta.nic.in/"),
 "ibps_po": ("IBPS CRP PO/MT-XVI detailed notification (30 Jun 2026)", "https://www.ibps.in/wp-content/uploads/Detailed-Notification_CRP-PO-XVI_Final_V1_30.06.2026.pdf"),
 "ibps_csa": ("IBPS CRP CSA-XVI (Clerk) notification", "https://www.ibps.in/wp-content/uploads/Notification_CRP_CSA_XVI-Final.pdf"),
 "ibps_site": ("ibps.in (official IBPS site)", "https://www.ibps.in/"),
 "sbi_po": ("SBI PO 2026 detailed advertisement CRPD/PO/2026-27/09", "https://sbi.bank.in/csfile/18062026_1_Detailed_Adv.2026.pdf"),
 "sbi_site": ("SBI careers: current openings", "https://sbi.bank.in/web/careers/current-openings"),
 "cgl": ("SSC CGL Examination 2026 notice", "https://ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_cgl_2026.pdf"),
 "chsl": ("SSC CHSL (10+2) Examination 2026 notice", "https://ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_chsl_2026.pdf"),
 "ssc_site": ("ssc.gov.in (official SSC site)", "https://ssc.gov.in/"),
}
def srcl(k):
    t,u=SRC[k]; return f'<a href="{A(u)}" rel="noopener" target="_blank">{_esc.escape(t)}</a>'

# Each exam: rows of (label, html). "src": keys used. Dates appear only where an official notice fixes them.
FACTS = {
"cat": {"name":"CAT 2026","by":"the IIMs","src":["cat_bulletin","cat_site"],"rows":[
  ("Pattern","Computer-based test, one paper of <b>120 minutes</b>, held in three sessions."),
  ("Sections","VARC (Verbal Ability &amp; Reading Comprehension), DILR (Data Interpretation &amp; Logical Reasoning), QA (Quantitative Ability)."),
  ("Time","Exactly <b>40 minutes per section</b>; you cannot switch sections while answering."),
  ("Marking","Not stated in the 2026 bulletin. Recent CATs used +3 for a correct answer, −1 for a wrong MCQ and no penalty for a wrong TITA (non-MCQ) answer; confirm with the official mock on iimcat.ac.in."),
  ("Exam date","<b>Sunday, 29 November 2026</b> (as per the CAT 2026 bulletin and press release of 26 Jul 2026)."),
 ]},
"cuet": {"name":"CUET (UG) 2026","by":"the National Testing Agency (NTA)","src":["cuet_bulletin","cuet_site"],"rows":[
  ("Pattern","Computer-based test. <b>37 subjects</b>: 13 languages, 23 domain subjects and the General Aptitude Test. A candidate chooses <b>up to 5</b>."),
  ("Questions","<b>50 compulsory MCQs</b> in each subject paper."),
  ("Time","<b>60 minutes per paper</b> (PwBD candidates get 20 minutes extra per hour)."),
  ("Marking","<b>+5</b> for a correct answer, <b>−1</b> for a wrong answer, 0 for unanswered."),
  ("Dates","Not listed here. Check the official site for the 2027 cycle."),
 ]},
"ibps-po": {"name":"IBPS PO (CRP PO/MT-XVI)","by":"IBPS","src":["ibps_po","ibps_site"],"rows":[
  ("Pattern","Prelims → Mains (objective + descriptive) → Interview. Prelims is a qualifying round; its marks are not used in the final merit."),
  ("Prelims","English 30 Q / 30 marks · Quantitative Aptitude 35 Q / 30 marks · Reasoning Ability 35 Q / 40 marks. <b>100 marks, 60 minutes</b> (20 minutes per section)."),
  ("Mains","Objective: <b>170 Q, 200 marks, 160 minutes</b> (Reasoning; General/Economy/Banking Awareness; English; Data Analysis &amp; Interpretation). Descriptive: <b>2 Q, 25 marks, 30 minutes</b> (essay and comprehension)."),
  ("Marking","Wrong answers cost <b>¼ of the marks</b> for that question in the objective tests."),
 ]},
"ibps-clerk": {"name":"IBPS Clerk (CRP CSA-XVI)","by":"IBPS","src":["ibps_csa","ibps_site"],"rows":[
  ("Pattern","Online Prelims → online Mains."),
  ("Prelims","English 30 Q / 30 marks · Numerical Ability 35 / 35 · Reasoning Ability 35 / 35. <b>100 marks, 60 minutes</b> (20 minutes per section); you must qualify in each test."),
  ("Mains","General/Financial Awareness 40 Q / 50 marks / 20 min · General English 40 / 40 / 35 min · Reasoning &amp; Computer Aptitude 40 / 60 / 35 min · Quantitative Aptitude 40 / 50 / 35 min. <b>160 Q, 200 marks, 125 minutes.</b>"),
  ("Marking","Wrong answers cost <b>¼ of the marks</b> for that question."),
 ]},
"sbi-po": {"name":"SBI PO 2026 (CRPD/PO/2026-27/09)","by":"State Bank of India","src":["sbi_po","sbi_site"],"rows":[
  ("Pattern","Phase I (Prelims) → Phase II (Mains) → Phase III (psychometric test, group exercise, interview). Final merit adds Phase II and Phase III marks; Phase I marks are not added."),
  ("Phase I","English 40 Q · Quantitative Aptitude 30 Q · Reasoning 30 Q. <b>100 marks, 1 hour</b> (20 minutes per section). No sectional cut-off."),
  ("Phase II","Objective: <b>170 Q, 200 marks, 3 hours</b> (Reasoning &amp; Computer Aptitude 40 Q / 60 / 50 min; Data Analysis &amp; Interpretation 30 / 60 / 45 min; General/Economy/Banking Awareness 60 / 60 / 45 min; English 40 / 20 / 40 min). Descriptive: 3 Q, 30 marks, 30 minutes."),
  ("Marking","Wrong answers cost <b>¼ of the marks</b> for that question."),
 ]},
"ssc-cgl": {"name":"SSC CGL 2026","by":"the Staff Selection Commission","src":["cgl","ssc_site"],"rows":[
  ("Pattern","Two computer-based tiers. Tier I is for shortlisting; Tier II Paper I is compulsory for all posts."),
  ("Tier I","Reasoning, General Awareness, Quantitative Aptitude, English: <b>25 Q / 50 marks each</b>; 100 Q, 200 marks in <b>1 hour</b> (15-minute sectional timer)."),
  ("Tier II Paper I","Session I: Maths 30 Q + Reasoning 30 Q (180 marks, 1 hour); English 45 Q + General Awareness 25 Q (210 marks, 1 hour); Computer Knowledge 20 Q (60 marks, 15 min, qualifying). Session II: Data Entry Speed Test (15 min). Papers II (Statistics) and III (Finance &amp; Economics) only for specific posts."),
  ("Marking","Tier I: −0.50 per wrong answer. Tier II Paper I: 3 marks per question, −1 per wrong answer."),
 ]},
"ssc-chsl": {"name":"SSC CHSL 2026","by":"the Staff Selection Commission","src":["chsl","ssc_site"],"rows":[
  ("Pattern","Two computer-based tiers, plus a skill/typing test inside Tier II."),
  ("Tier I","English, General Intelligence, Quantitative Aptitude, General Awareness: <b>25 Q / 50 marks each</b>; 100 Q, 200 marks in <b>60 minutes</b> (15 minutes per section)."),
  ("Tier II","Session I: Maths 30 Q + Reasoning 30 Q (180 marks, 1 hour); English 40 Q + General Awareness 20 Q (180 marks, 1 hour); Computer Knowledge 15 Q (45 marks, 15 min, qualifying). Session II: skill test / typing test."),
  ("Marking","Tier I: −0.50 per wrong answer. Tier II: 3 marks per question, −1 per wrong answer."),
 ]},
}
def facts_box(k, h="h2"):
    f=FACTS[k]
    rows="".join(f'<div class="fx-row"><dt>{l}</dt><dd>{v}</dd></div>' for l,v in f["rows"])
    srcs=" · ".join(srcl(s) for s in f["src"])
    return f"""<aside class="facts" aria-label="{A(f['name'])} key facts"><{h} class="facts-h">{f['name']}: key facts</{h}>
<dl class="fx">{rows}</dl>
<p class="facts-src">Source: {srcs}. Checked {CHECKED}. Conducted by {f['by']}; we are not affiliated with them. Always confirm on the official site.</p></aside>"""
