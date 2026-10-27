# Ten original guides. Executed by m2pages.py (shares globals). Every number used below is re-checked in check_guides().
# Section bodies are HTML. "src" keys refer to SRC in facts.py; "ext" are extra (title,url) sources.
NCERT=("NCERT textbooks (Mathematics, Classes 7–8: Comparing Quantities; Class 10: Arithmetic Progressions)","https://ncert.nic.in/textbook.php")
def tbl(head, rows, cap=""):
    th="".join(f"<th>{h}</th>" for h in head)
    tr="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<div class="table-wrap"><table class="data">{f"<caption>{cap}</caption>" if cap else ""}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

GUIDES = [
{"slug":"cat-2026-pattern-section-plan","tags":["cat"],"title":"CAT 2026 Pattern and a 40-Minute Section Plan",
 "h1":"CAT 2026: the pattern, and how to plan each 40 minutes",
 "desc":"CAT 2026 exam pattern from the official bulletin (120 minutes, three 40-minute sections, 29 Nov 2026) and a practical time plan for VARC, DILR and QA.",
 "lead":"What the official CAT 2026 bulletin actually says about the test, what it leaves out, and a simple way to spend each locked 40-minute section.",
 "insights":["CAT 2026 is on <b>Sunday, 29 November 2026</b>, in three sessions (official bulletin).","Each section is locked for exactly <b>40 minutes</b>. Time you save in one section cannot be used in another.","The bulletin does not publish question counts or marking. Check the official mock before test day.","In DILR, choosing the right sets matters more than speed."],
 "sections":[
  ("What the bulletin confirms", "<p>The CAT 2026 Information Bulletin and the press release of 26 July 2026 confirm the points below. Anything else you read about CAT 2026 is a forecast.</p>"+tbl(["Item","CAT 2026 (official)"],[["Mode","Computer-based test"],["Duration","120 minutes"],["Sections","VARC, DILR, QA (in this order)"],["Time per section","40 minutes, no switching between sections"],["Test date","Sunday, 29 November 2026, three sessions"],["Registration","3 August to 15 September 2026 (closed)"],["Result","Likely in the first week of January 2027"]],"CAT 2026 facts from the official bulletin")),
  ("What it does not say", "<p>The bulletin does not give the number of questions or the marking scheme. Recent CAT papers used +3 for a correct answer, −1 for a wrong MCQ and 0 for a wrong TITA (type-in-the-answer) question, but this is not stated for 2026, so treat it as a working assumption. The official mock test on iimcat.ac.in is the best way to confirm the 2026 format before test day.</p>"),
  ("A plan for each 40 minutes", "<p>The lock changes how you should think about time. You cannot bank minutes, so the goal in every section is to use all 40 on the questions you are most likely to get right.</p>"+tbl(["Section","First pass","Second pass","Last 3–4 minutes"],[["VARC","Read the passages you find comfortable first, about 6–8 minutes each including questions","Verbal ability (TITA para-jumbles, odd sentence out)","Answer any TITA you narrowed down; TITA has no penalty"],["DILR","Spend 3–4 minutes scanning every set and rank them","Solve the two or three easiest sets fully","Pick up single questions from a half-done set"],["QA","Take every question you can solve in under 2 minutes","Return to the ones you marked as doable","Check TITA answers for unit and rounding errors"]],"A suggested time plan (our recommendation, not an official rule)")),
  ("Why blind guessing on MCQs is not worth it", "<p>With +3 for a correct answer and −1 for a wrong one on a 4-option MCQ, a blind guess has an expected score of 3 × ¼ − 1 × ¾ = <b>0</b>. It costs time and adds nothing on average. If you can eliminate one option, the expected score becomes 3 × ⅓ − 1 × ⅔ = <b>+⅓</b>, so an educated guess does pay. TITA questions carry no penalty, so never leave one blank if you have a reasonable answer. See our <a href=\"guide-negative-marking-guessing-maths.html\">negative marking guide</a> for the full calculation.</p>"),
 ],
 "faq":[("How many questions will CAT 2026 have?","The official bulletin does not say. Check the official mock on iimcat.ac.in for the 2026 format."),("Can I go back to VARC after it ends?","No. Each section is locked for 40 minutes and you cannot switch while answering a section."),("Is there negative marking for TITA questions?","In recent CATs there was none for TITA. The 2026 bulletin does not state the marking, so confirm it with the official mock.")],
 "src":["cat_bulletin","cat_site"],"ext":[],
 "links":[("cat.html","CAT track"),("cat-practice.html","40-minute CAT sectional"),("cat-dilr-sets.html","CAT DILR sets")]},

{"slug":"negative-marking-guessing-maths","tags":["cat","cuet","bank"],"title":"Negative Marking Maths: When Guessing Pays",
 "h1":"Negative marking: when does a guess pay off?",
 "desc":"Expected-value maths for guessing under CAT, CUET, IBPS, SBI and SSC negative marking, with break-even probabilities worked out exam by exam.",
 "lead":"A short, exact way to decide whether to guess, using each exam's official marking scheme.",
 "insights":["A guess pays when your chance of being right is above <b>penalty ÷ (marks + penalty)</b>.","CUET (+5/−1) has a low break-even of <b>1 in 6</b>, so an educated guess usually pays.","Under CAT-style +3/−1, a blind guess on 4 options is worth exactly 0 on average.","Bank and SSC sectional cut-offs make a few extra wrong answers more costly than the averages suggest."],
 "sections":[
  ("The one formula you need", "<p>Say a correct answer earns <i>M</i> marks and a wrong one loses <i>N</i>. If your chance of being right is <i>p</i>, the expected score of attempting is <i>pM − (1 − p)N</i>. This is positive when <b><i>p</i> &gt; <i>N</i> / (<i>M</i> + <i>N</i>)</b>. That value is the break-even probability. Above it, attempt. Below it, skip.</p>"),
  ("Exam by exam", "<p>The marks and penalties below come from each exam's official notice (CAT is the recent pattern; see the CAT guide). The last two columns assume 4 options; for a 5-option paper a blind guess is right 1 time in 5.</p>"+tbl(["Exam","Correct","Wrong","Break-even p","Blind guess, 4 options","Blind guess, 5 options"],[["CAT (recent pattern, MCQ)","+3","−1","1/4 = 25%","0","−0.2"],["CUET (UG) 2026","+5","−1","1/6 ≈ 16.7%","+0.5","+0.2"],["IBPS / SBI (1-mark question)","+1","−0.25","1/5 = 20%","+0.0625","0"],["SSC CGL / CHSL Tier I","+2","−0.5","1/5 = 20%","+0.125","0"],["SSC Tier II Paper I","+3","−1","1/4 = 25%","0","−0.2"]],"Break-even probability and expected score of one blind guess")),
  ("Eliminating options changes everything", "<p>Each option you can rule out raises <i>p</i>. Under +3/−1 with 4 options, a blind guess is worth 0. Remove one option and it is worth +⅓; remove two and it is worth +1. Under CUET marking, removing two options makes a guess worth 5 × ½ − 1 × ½ = +2.</p>"+tbl(["Options left","p","CAT +3/−1","CUET +5/−1","SSC +2/−0.5"],[["4","1/4","0","+0.5","+0.125"],["3","1/3","+0.33","+1","+0.33"],["2","1/2","+1","+2","+0.75"]],"Expected score of a guess after eliminating options")),
  ("When the average misleads", "<p>Expected value is an average over many questions. In a single paper, wrong guesses can pull a section below its cut-off. IBPS PO and IBPS Clerk prelims require you to qualify in each section. So guess when you have eliminated options, not across a whole section in the last minute.</p>"),
 ],
 "faq":[("Should I guess blindly in CUET?","The maths says a blind guess on 4 options is worth +0.5 on average under +5/−1, but an educated guess is far better. Use the time to eliminate options first."),("What is the penalty in IBPS exams?","One quarter of the marks assigned to the question, as stated in the IBPS notifications."),("Are TITA questions penalised in CAT?","Not in recent CATs. The 2026 bulletin does not state the marking.")],
 "src":["cuet_bulletin","ibps_po","ibps_csa","sbi_po","cgl","chsl"],"ext":[],
 "links":[("cuet-practice.html","CUET sectional"),("cat-practice.html","CAT sectional"),("practice.html?exam=general","Bank / SSC timed quiz")]},

{"slug":"percentages-successive-change","tags":["cat","cuet","bank"],"title":"Percentages: Successive Change and Fraction Tables",
 "h1":"Percentages: successive change, reversals and the fraction table",
 "desc":"Successive percentage change, the recovery formula, consumption–price changes and a fraction-to-percent table, with worked examples checked by script.",
 "lead":"Most percentage questions in CAT, CUET and Bank/SSC papers use one of four ideas. Learn them once and you can solve these questions fast.",
 "insights":["Two changes of a% and b% give a net change of <b>a + b + ab/100</b> percent.","A 20% fall needs a <b>25%</b> rise to recover, not 20%.","Knowing 1/7 ≈ 14.29% and 1/9 ≈ 11.11% saves a lot of division.","A rise followed by an equal fall always leaves a net loss of a²/100 %."],
 "sections":[
  ("Successive change", "<p>If a value changes by <i>a</i>% and then by <i>b</i>%, the overall change is <b><i>a</i> + <i>b</i> + <i>ab</i>/100</b> percent. Use a negative number for a decrease.</p><p><b>Example.</b> A price rises 20% and then falls 10%. The net change is 20 − 10 + (20 × −10)/100 = <b>+8%</b>. Check: 100 → 120 → 108.</p><p><b>Example.</b> A rise of 30% followed by a fall of 30% gives 30 − 30 − 900/100 = <b>−9%</b>.</p>"),
  ("Getting back to the start", "<p>After a fall of <i>x</i>%, the rise needed to recover is <b><i>x</i> / (100 − <i>x</i>) × 100</b> percent.</p>"+tbl(["Fall","Rise needed to recover"],[["10%","11.11%"],["20%","25%"],["25%","33.33%"],["40%","66.67%"],["50%","100%"]],"Recovery after a fall")),
  ("Price and consumption", "<p>If the price rises by <i>r</i>% and spending must stay the same, consumption must fall by <b><i>r</i> / (100 + <i>r</i>) × 100</b> percent. A 25% price rise needs a 20% cut in use.</p>"),
  ("The fraction table", tbl(["Fraction","Percent","Fraction","Percent"],[["1/2","50%","1/7","14.29%"],["1/3","33.33%","1/8","12.5%"],["1/4","25%","1/9","11.11%"],["1/5","20%","1/11","9.09%"],["1/6","16.67%","1/12","8.33%"]],"Common fractions as percentages (rounded to 2 decimals)")),
 ],
 "faq":[("Is a 10% rise then a 10% fall the same as no change?","No. The net is 10 − 10 − 100/100 = −1%, a 1% loss."),("Why is the percentage on the old value?","Percentage change is always measured against the starting value, which is why the recovery rise is larger than the fall.")],
 "src":[],"ext":[NCERT],
 "links":[("q/bank-ssc/quant-percentages.html","Percentage questions (Bank/SSC)"),("q/cat/qa-percentages-profit.html","CAT percentages & profit questions"),("formula-bank-ssc-quant.html","Bank/SSC Quant formula sheet")]},

{"slug":"time-speed-distance","tags":["cat","cuet","bank"],"title":"Time, Speed and Distance: Relative Speed, Trains and Boats",
 "h1":"Time, speed and distance: relative speed, trains and boats",
 "desc":"Relative speed, trains crossing, boats and streams and average speed explained with worked examples whose answers are checked by script.",
 "lead":"Speed questions look different on the surface, but they all use distance = speed × time. These are the main variations.",
 "insights":["To convert km/h to m/s, multiply by <b>5/18</b>.","Average speed over equal distances is <b>2xy/(x + y)</b>, not (x + y)/2.","Same direction: subtract speeds. Opposite directions: add them.","Downstream speed = boat + stream; upstream speed = boat − stream."],
 "sections":[
  ("Units first", "<p>1 km/h = 1000 m ÷ 3600 s = <b>5/18 m/s</b>. So 72 km/h = 20 m/s and 54 km/h = 15 m/s. Convert before you do anything else.</p>"),
  ("Average speed", "<p>If you cover the same distance at <i>x</i> and then at <i>y</i>, the average speed is <b>2<i>xy</i>/(<i>x</i> + <i>y</i>)</b>. Going at 60 km/h and returning at 40 km/h gives 2 × 60 × 40 / 100 = <b>48 km/h</b>, not 50.</p>"),
  ("Relative speed and trains", tbl(["Situation","Distance to cover","Speed to use"],[["Train passes a pole or a person","Length of the train","Train speed"],["Train passes a platform or bridge","Train + platform length","Train speed"],["Two trains, opposite directions","Sum of both lengths","Sum of speeds"],["Two trains, same direction","Sum of both lengths","Difference of speeds"]],"Which distance and speed to use")+"<p><b>Example.</b> A 150 m train at 54 km/h (15 m/s) crosses a 300 m platform in (150 + 300) ÷ 15 = <b>30 seconds</b>.</p><p><b>Example.</b> Trains of 120 m and 180 m run in opposite directions at 40 and 50 km/h. The relative speed is 90 km/h = 25 m/s, so they cross in 300 ÷ 25 = <b>12 seconds</b>.</p>"),
  ("Boats and streams", "<p>With boat speed <i>b</i> in still water and stream speed <i>s</i>: downstream = <i>b</i> + <i>s</i>, upstream = <i>b</i> − <i>s</i>. So <i>b</i> = (down + up)/2 and <i>s</i> = (down − up)/2.</p><p><b>Example.</b> A boat goes 36 km downstream in 2 hours and returns in 3 hours. Down = 18 km/h, up = 12 km/h, so the boat's speed is <b>15 km/h</b> and the stream's is <b>3 km/h</b>.</p>"),
 ],
 "faq":[("Why isn't average speed the simple average?","You spend more time at the slower speed, so it counts for more. The harmonic mean 2xy/(x+y) accounts for that."),("Do I add train lengths when one train overtakes another?","Yes. To pass fully, the faster train covers both lengths at the difference of the speeds.")],
 "src":[],"ext":[NCERT],
 "links":[("q/bank-ssc/quant-time-speed-distance.html","TSD questions (Bank/SSC)"),("q/cat/qa-time-speed-distance.html","CAT TSD questions"),("q/cuet/gat-time-speed-distance.html","CUET GAT TSD questions")]},

{"slug":"simple-compound-interest","tags":["bank","cuet","cat"],"title":"Simple and Compound Interest: Formulas and Shortcuts",
 "h1":"Simple and compound interest: formulas and the CI − SI shortcut",
 "desc":"Simple and compound interest, half-yearly compounding and the CI − SI difference for 2 and 3 years, with growth-factor tables and checked examples.",
 "lead":"Interest questions appear in almost every Bank and SSC paper. These are the formulas and shortcuts that cover nearly all of them.",
 "insights":["SI grows by the same amount every year; CI grows by the same <b>percentage</b> every year.","For 2 years, CI − SI = <b>P(R/100)²</b>.","For 3 years, CI − SI = <b>P(R/100)²(3 + R/100)</b>.","Half-yearly compounding: halve the rate and double the number of periods."],
 "sections":[
  ("The two formulas", "<p>Simple interest: <b>SI = P × R × T / 100</b>. Compound interest (annual): <b>A = P(1 + R/100)<sup>n</sup></b> and CI = A − P.</p><p><b>Example.</b> ₹8,000 at 5% for 2 years: SI = ₹800; A = 8000 × 1.05² = ₹8,820, so CI = ₹820. The difference is ₹20, which is 8000 × 0.05² = ₹20.</p>"),
  ("The CI − SI shortcut", tbl(["Period","CI − SI"],[["2 years","P (R/100)²"],["3 years","P (R/100)² (3 + R/100)"]],"Difference between compound and simple interest")+"<p><b>Example.</b> ₹10,000 at 10% for 3 years: SI = ₹3,000, CI = 10000 × (1.1³ − 1) = ₹3,310. The difference is ₹310 = 10000 × 0.01 × 3.1.</p>"),
  ("Growth factors to remember", tbl(["Rate","After 2 years","After 3 years"],[["5%","1.1025","1.157625"],["10%","1.21","1.331"],["20%","1.44","1.728"]],"(1 + R/100)ⁿ for common rates")),
  ("Half-yearly and quarterly", "<p>For half-yearly compounding, use R/2 per period and 2n periods. ₹10,000 at 10% a year for 1 year, compounded half-yearly, becomes 10000 × 1.05² = <b>₹11,025</b>, against ₹11,000 with annual compounding. For quarterly, use R/4 and 4n.</p>"),
 ],
 "faq":[("When is CI equal to SI?","For the first year with annual compounding, they are equal. They differ from the second year on."),("What does 'doubles in n years' tell me under SI?","It means R × n = 100, so the rate is 100/n percent.")],
 "src":[],"ext":[NCERT],
 "links":[("q/bank-ssc/quant-simple-compound-interest.html","Interest questions (Bank/SSC)"),("q/cuet/gat-simple-compound-interest.html","CUET GAT interest questions"),("formula-bank-ssc-quant.html","Bank/SSC Quant formula sheet")]},

{"slug":"ratio-mixtures-alligation","tags":["cat","bank","cuet"],"title":"Ratio, Mixtures and Alligation Made Simple",
 "h1":"Ratio, mixtures and alligation",
 "desc":"Ratios, partnership, weighted averages and the alligation rule, plus the repeated-replacement formula, with worked examples checked by script.",
 "lead":"Alligation is a quick way to find a weighted average. Once you see that, most mixture questions become one-line calculations.",
 "insights":["Alligation: cheaper : dearer = <b>(d − m) : (m − c)</b>.","After replacing a fraction <i>f</i> of a mixture <i>n</i> times, the original liquid left is <b>(1 − f)<sup>n</sup></b>.","In a partnership, profit is shared in the ratio of capital × time.","A ratio a : b means the parts are a/(a+b) and b/(a+b) of the whole."],
 "sections":[
  ("Ratios as parts of a whole", "<p>If ₹1,200 is shared in the ratio 3 : 5, the shares are 1200 × 3/8 = ₹450 and 1200 × 5/8 = ₹750. In a partnership, A invests ₹40,000 for 12 months and B ₹60,000 for 6 months. The ratio is 480,000 : 360,000 = <b>4 : 3</b>.</p>"),
  ("The alligation rule", "<p>Mix a cheaper item at price <i>c</i> with a dearer one at <i>d</i> to get a mixture at <i>m</i>. The quantities are in the ratio <b>(d − m) : (m − c)</b>.</p><p><b>Example.</b> Rice at ₹40/kg and ₹55/kg is mixed to sell at ₹45/kg (cost). The ratio is (55 − 45) : (45 − 40) = <b>2 : 1</b>. Check: (2 × 40 + 1 × 55)/3 = ₹45.</p>"),
  ("Repeated replacement", "<p>A vessel holds 40 litres of milk. 4 litres are taken out and replaced with water, and this is done three times. The fraction removed each time is 4/40 = 1/10. The milk left is 40 × (9/10)³ = <b>29.16 litres</b>.</p>"+tbl(["Replacements","Milk left (of 40 L)"],[["1","36"],["2","32.4"],["3","29.16"]],"Milk left after each replacement")),
 ],
 "faq":[("Does alligation work for percentages and speeds?","Yes, it works for any weighted average: concentrations, average marks, or average speeds over equal times."),("Why does the ratio look 'crossed'?","Each quantity is proportional to how far the other price is from the mean, which is why the differences swap sides.")],
 "src":[],"ext":[NCERT],
 "links":[("q/bank-ssc/quant-averages-alligation.html","Averages & alligation questions"),("q/cat/qa-mixtures-alligation.html","CAT mixtures questions"),("q/bank-ssc/quant-ratio-proportion.html","Ratio questions")]},

{"slug":"cat-dilr-set-selection","tags":["cat"],"title":"CAT DILR: How to Choose Which Sets to Solve",
 "h1":"CAT DILR: choosing which sets to solve",
 "desc":"A method for scanning and ranking CAT DILR sets in the first minutes of the 40-minute section, with a checklist for spotting easy and hard sets.",
 "lead":"In CAT DILR, the sets you choose matter more than how fast you solve them. Here is a simple way to choose.",
 "insights":["Spend the first <b>3–4 minutes</b> reading every set's setup, not solving.","Two sets solved fully usually score better than four sets half done.","A set with many clear numbers and few conditions is often faster than it looks.","Leave a set after 2–3 minutes of no progress. The time lock means every minute counts."],
 "sections":[
  ("Why selection matters", "<p>DILR has its own 40-minute lock. Each set has several questions that depend on the same setup. If you solve the setup, most of the questions follow; if you don't, you get almost nothing for your time. So choose sets you can finish.</p>"),
  ("A 3-minute scan", "<p>Read the first paragraph and the conditions of each set and give it a score out of 3:</p>"+tbl(["Signal","Usually easier","Usually harder"],[["Data given","Complete table or chart","Many blanks to fill"],["Conditions","Few, direct (\"A is left of B\")","Many, with 'not' and 'if… then'"],["Variables","One or two dimensions","Three or more linked dimensions"],["Questions","Direct read-off questions","'Which must be true' across cases"]],"Signals to look for while scanning")),
  ("While solving", "<ul class=\"clean\"><li>Draw the grid or table before reading the questions.</li><li>Write each condition in short form next to the grid.</li><li>If you reach two cases, carry both until a condition rules one out.</li><li>After 2–3 minutes with no progress, move on and come back later if there is time.</li></ul>"),
 ],
 "faq":[("How many DILR sets should I attempt?","It depends on the paper. Aim to solve two or three sets well rather than skimming all of them."),("Should I solve the sets in order?","No. The order in the paper means nothing. Start with the set you ranked highest.")],
 "src":["cat_bulletin"],"ext":[],
 "links":[("cat-dilr-sets.html","CAT DILR practice sets"),("dilr.html","DILR notes"),("q/cat/dilr-arrangements.html","CAT arrangement sets")]},

{"slug":"reading-comprehension-method","tags":["cat","cuet"],"title":"Reading Comprehension: A Method for CAT and CUET",
 "h1":"Reading comprehension: a method that works for CAT and CUET",
 "desc":"How to read a passage once, map its structure, and answer main-idea, inference and tone questions in CAT VARC and the CUET English paper.",
 "lead":"RC rewards careful reading. Read once, carefully, then answer from the text.",
 "insights":["Read once, carefully. Rereading the whole passage costs more than reading it well.","Write a 3–5 word note for each paragraph's job.","Correct options are supported by the passage, not by general knowledge.","Extreme words (always, never, only) are usually wrong."],
 "sections":[
  ("Read for structure", "<p>As you read, ask what each paragraph does: does it state a view, give an example, raise an objection or conclude? Write a short note such as \"P2: example, the railways\". Most main-idea questions are answered by these notes.</p>"),
  ("Question types", tbl(["Type","What it asks","How to answer"],[["Main idea","The point the whole passage serves","Test each option against every paragraph"],["Detail","What the text says about X","Find the line and paraphrase it"],["Inference","What must be true, given the text","Reject options that are only possibly true"],["Tone / attitude","The author's stance","Look at the adjectives and qualifiers"],["Strengthen / weaken","What affects the argument","Target the link from evidence to conclusion"]],"Common RC question types")),
  ("CAT and CUET differences", "<p>In CAT, RC is part of a 40-minute VARC section and you can choose the order of passages. In CUET (UG), the English paper tests reading comprehension using factual, literary and narrative passages (official bulletin), at a pace of 50 questions in 60 minutes, or 72 seconds a question. That pace means shorter, faster reads.</p>"),
 ],
 "faq":[("Should I read the questions first?","Glancing at them can help you notice the right lines, but don't skip the reading itself."),("How do I improve speed?","Practise reading with notes. Speed comes from understanding structure, not from skimming.")],
 "src":["cat_bulletin","cuet_bulletin"],"ext":[],
 "links":[("varc.html","VARC strategy & rules"),("q/cat/varc-reading-comprehension.html","CAT RC passages"),("q/cuet/english-reading-comprehension.html","CUET English RC")]},

{"slug":"cuet-general-aptitude-test-2026","tags":["cuet"],"title":"CUET (UG) General Aptitude Test: Syllabus and Pace",
 "h1":"CUET (UG) General Aptitude Test: syllabus, pace and a study plan",
 "desc":"What the NTA bulletin says about the CUET (UG) General Aptitude Test (50 questions, 60 minutes, +5/−1), the official syllabus areas, and how to prepare.",
 "lead":"The General Aptitude Test is one of the 37 CUET (UG) subjects. Here is what the official bulletin lists, and what that means for your preparation.",
 "insights":["50 compulsory questions in 60 minutes: <b>72 seconds per question</b>.","Marking is +5 / −1, so a guess pays once you are more than 1 in 6 sure.","The syllabus mixes general knowledge and current affairs with mental ability, numerical ability and reasoning.","Quant in the GAT is basic: arithmetic, algebra, geometry, mensuration and statistics."],
 "sections":[
  ("The official syllabus", "<p>The CUET (UG) 2026 bulletin lists the General Aptitude Test syllabus as: general knowledge, current affairs, general mental ability, numerical ability, quantitative reasoning (simple use of basic maths: arithmetic, algebra, geometry, mensuration, statistics) and logical and analytical reasoning.</p>"+tbl(["Area","Topics to practise on this site"],[["Numerical ability","<a href=\"q/cuet/gat-percentages.html\">Percentages</a>, <a href=\"q/cuet/gat-profit-loss.html\">profit &amp; loss</a>, <a href=\"q/cuet/gat-time-work.html\">time &amp; work</a>"],["Quantitative reasoning","<a href=\"q/cuet/gat-algebra.html\">Algebra</a>, <a href=\"q/cuet/gat-geometry.html\">geometry</a>, <a href=\"q/cuet/gat-statistics.html\">statistics</a>"],["Logical &amp; analytical reasoning","<a href=\"q/cuet/gat-syllogisms.html\">Syllogisms</a>, <a href=\"q/cuet/gat-seating-arrangement.html\">seating</a>, <a href=\"q/cuet/gat-coding-decoding.html\">coding-decoding</a>"],["General knowledge","<a href=\"q/cuet/gat-indian-polity.html\">Polity</a>, <a href=\"q/cuet/gat-history.html\">history</a>, <a href=\"q/cuet/gat-general-science.html\">science</a>"]],"Official syllabus areas and where to practise")),
  ("The pace", "<p>60 minutes for 50 questions is 72 seconds each. GK questions take 10–20 seconds if you know them. Use the time you save on the reasoning and quant questions.</p>"),
  ("A four-week plan", tbl(["Week","Focus"],[["1","Arithmetic basics: percentages, ratios, averages"],["2","Reasoning: series, coding, arrangements, syllogisms"],["3","GK and current affairs every day; algebra and geometry"],["4","Full 50-question timed papers, then review every mistake"]],"A suggested plan (our recommendation)")),
 ],
 "faq":[("Is the GAT compulsory?","No. It is one of the subjects you may choose, up to five in total. Check whether your target course requires it."),("Is there negative marking?","Yes, −1 for a wrong answer and +5 for a correct one, according to the 2026 bulletin.")],
 "src":["cuet_bulletin","cuet_site"],"ext":[],
 "links":[("cuet.html","CUET (UG) track"),("cuet-practice.html","CUET sectional"),("cuet-practice.html?daily=1","CUET Daily 10")]},

{"slug":"bank-prelims-reasoning-puzzles","tags":["bank"],"title":"Bank Prelims Reasoning: Puzzles and Seating Under Time",
 "h1":"Bank prelims reasoning: puzzles and seating under time pressure",
 "desc":"Time per question in IBPS PO, IBPS Clerk and SBI PO prelims reasoning (from the official notices) and a method for seating and puzzle sets.",
 "lead":"Reasoning in bank prelims is a race against a 20-minute sectional timer. Here is the time you actually have, and how to spend it.",
 "insights":["IBPS PO and Clerk prelims: <b>35 reasoning questions in 20 minutes</b>, about 34 seconds each.","SBI PO prelims: <b>30 reasoning questions in 20 minutes</b>, 40 seconds each.","A 5-question puzzle you crack in 4 minutes is cheaper per question than most single questions.","Attempt the single questions (inequality, coding, direction) first."],
 "sections":[
  ("The time you have", "<p>The figures below come from the official notifications.</p>"+tbl(["Exam","Reasoning questions","Time","Seconds per question"],[["IBPS PO prelims","35","20 min","≈ 34.3"],["IBPS Clerk prelims","35","20 min","≈ 34.3"],["SBI PO Phase I","30","20 min","40"]],"Reasoning time in bank prelims")),
  ("Order of attack", "<ol><li>Single questions first: inequalities, coding-decoding, direction sense, blood relations. Each takes 20–40 seconds.</li><li>Then the puzzle or seating set that looks most complete.</li><li>Leave the set with the most 'not' conditions for last.</li></ol>"),
  ("Solving a seating set", "<ul class=\"clean\"><li>Draw the layout first: a line, circle or rectangle, and note which way people face.</li><li>Place the fixed facts (\"A sits at an end\") before the relative ones.</li><li>When a condition gives two places, draw both cases side by side.</li><li>Use the negative conditions to eliminate one case.</li></ul>"),
 ],
 "faq":[("Is there a sectional cut-off in IBPS prelims?","Yes. The IBPS notifications say candidates must qualify in each test. SBI PO Phase I has no sectional cut-off."),("How many puzzles should I attempt?","As many as you can finish. A half-solved puzzle usually scores nothing.")],
 "src":["ibps_po","ibps_csa","sbi_po"],"ext":[],
 "links":[("q/bank-ssc/reasoning-seating-arrangement.html","Seating arrangement questions"),("q/bank-ssc/reasoning-puzzles.html","Puzzle questions"),("formula-reasoning.html","Reasoning shortcuts sheet")]},
]

def check_guides():
    from math import isclose
    # negative marking table
    ev=lambda p,M,N: p*M-(1-p)*N
    assert ev(.25,3,1)==0 and isclose(ev(1/3,3,1),1/3) and isclose(ev(.5,3,1),1)
    assert isclose(ev(.25,5,1),.5) and isclose(ev(.2,5,1),.2) and isclose(ev(1/3,5,1),1) and isclose(ev(.5,5,1),2)
    assert isclose(ev(.25,1,.25),.0625) and isclose(ev(.2,1,.25),0,abs_tol=1e-12)
    assert isclose(ev(.25,2,.5),.125) and isclose(ev(.2,2,.5),0,abs_tol=1e-12) and isclose(ev(1/3,2,.5),1/3) and isclose(ev(.5,2,.5),.75)
    assert isclose(ev(.2,3,1),-.2) and isclose(1/(5+1),1/6) and isclose(.25/1.25,.2) and isclose(.5/2.5,.2)
    # percentages
    net=lambda a,b:a+b+a*b/100
    assert net(20,-10)==8 and isclose(120*.9,108) and net(30,-30)==-9 and net(10,-10)==-1
    rec=lambda x:x/(100-x)*100
    assert [round(rec(x),2) for x in (10,20,25,40,50)]==[11.11,25,33.33,66.67,100]
    assert isclose(25/125*100,20)
    assert [round(100/k,2) for k in (2,3,4,5,6,7,8,9,11,12)]==[50,33.33,25,20,16.67,14.29,12.5,11.11,9.09,8.33]
    # TSD
    assert isclose(72*5/18,20) and isclose(54*5/18,15) and 2*60*40/100==48
    assert (150+300)/15==30 and isclose((40+50)*5/18,25) and 300/25==12
    assert 36/2==18 and 36/3==12 and (18+12)/2==15 and (18-12)/2==3
    # interest
    assert 8000*5*2/100==800 and isclose(8000*1.05**2,8820) and isclose(8000*.05**2,20)
    assert isclose(10000*(1.1**3-1),3310) and isclose(10000*.01*3.1,310) and isclose(3310-3000,310)
    for r,f2,f3 in ((5,1.1025,1.157625),(10,1.21,1.331),(20,1.44,1.728)):
        assert isclose((1+r/100)**2,f2) and isclose((1+r/100)**3,f3)
    assert isclose(10000*1.05**2,11025)
    for P,R in ((10000,10),(5000,8)):
        assert isclose(P*(1+R/100)**3-P-P*R*3/100, P*(R/100)**2*(3+R/100))
    # ratio & mixtures
    assert 1200*3/8==450 and 1200*5/8==750 and 40000*12*3==60000*6*4
    assert (55-45,45-40)==(10,5) and (2*40+55)/3==45
    assert [round(40*.9**k,2) for k in (1,2,3)]==[36,32.4,29.16]
    # CUET / bank pace
    assert 60*60/50==72 and round(1200/35,1)==34.3 and 1200/30==40
    return True
