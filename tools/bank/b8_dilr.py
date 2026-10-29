"""Bank/SSC DILR batch 8 (Oct 2026): 15 original sets x 5 questions. Every answer is recomputed below
(asserts / brute force over all arrangements, results or routes) before the item is added."""
import itertools as it
from fractions import Fraction as F

def bars(title, rows, scale):
    return f"<b>{title}</b><div class='bars'>" + "".join(f"<div class='bar-row'><span>{c}</span><i style='width:{v*scale:.1f}%'></i><span>{v}</span></div>" for c, v in rows) + "</div>"

COLS = ["#4f46e5", "#0891b2", "#db2777", "#f59e0b", "#16a34a", "#7c3aed", "#64748b"]
def pie(title, parts):
    assert sum(v for _, v in parts) == 100
    seg, acc = [], 0
    for i, (_, v) in enumerate(parts): seg.append(f"{COLS[i]} {acc}% {acc+v}%"); acc += v
    leg = "".join(f"<div><i style='background:{COLS[i]}'></i>{k} {v}%</div>" for i, (k, v) in enumerate(parts))
    return f"<b>{title}</b><div class='pie-wrap'><div class='pie' style='background:conic-gradient({','.join(seg)})'></div><div class='pie-legend'>{leg}</div></div>"

def lines(title, xs, series, mx):
    W, H, px, py = 360, 180, 36, 22; n = len(xs)
    X = lambda i: px + i * (W - px - 14) / (n - 1); Y = lambda v: H - py - (v / mx) * (H - 2 * py)
    grid = "".join(f"<line x1='{px}' x2='{W-10}' y1='{Y(v):.1f}' y2='{Y(v):.1f}' stroke='#e2e8f0'/><text x='{px-6}' y='{Y(v)+4:.1f}' font-size='10' text-anchor='end' fill='#64748b'>{v}</text>" for v in range(0, mx + 1, mx // 5))
    lab = "".join(f"<text x='{X(i):.1f}' y='{H-4}' font-size='10' text-anchor='middle' fill='#64748b'>{m}</text>" for i, m in enumerate(xs))
    body, leg = "", ""
    for j, (name, vals, col) in enumerate(series):
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
        off = -8 if j == 0 else 14
        body += f"<polyline points='{pts}' fill='none' stroke='{col}' stroke-width='2.5'/>" + "".join(f"<circle cx='{X(i):.1f}' cy='{Y(v):.1f}' r='3.5' fill='{col}'/><text x='{X(i):.1f}' y='{Y(v)+off:.1f}' font-size='10' text-anchor='middle' fill='{col}'>{v}</text>" for i, v in enumerate(vals))
        leg += f"<span style='color:{col};margin-right:1em'>● {name}</span>"
    return f"<b>{title}</b><div style='font-size:.85rem'>{leg}</div><svg viewBox='0 0 {W} {H}' style='width:100%;max-width:420px;display:block'>{grid}{body}{lab}</svg>"

def P(txt): return f"<p style='margin:.3em 0 0'>{txt}</p>"

def build(A):
    s = "dilr"
    # ---------------- Bar chart: car sales ----------------
    T = "Bar Charts"; S = "bar-cars-b8"
    yr = [2020, 2021, 2022, 2023, 2024, 2025]; cs = [120, 150, 135, 180, 216, 240]; c = dict(zip(yr, cs))
    D = bars("Cars sold by a dealer, 2020–2025", [(y, v) for y, v in c.items()], 0.38)
    A(s,T,"Easy","By what percentage did the dealer's car sales rise from 2023 to 2024?",["15%","18%","20%","24%"],"20%",
      "2023 = 180, 2024 = 216. Rise = 36/180 × 100 = 20%.","2023 = 180, 2024 = 216. वृद्धि = 36/180 × 100 = 20%.",chk=((c[2024]-c[2023])/c[2023]*100,20),data=D,set_id=S)
    assert sum(cs) == 1041
    A(s,T,"Medium","What was the average number of cars sold per year over 2020–2025?",["170","173.5","175.5","180"],"173.5",
      "Total = 120 + 150 + 135 + 180 + 216 + 240 = 1041. Average = 1041/6 = 173.5.","कुल = 120 + 150 + 135 + 180 + 216 + 240 = 1041. औसत = 1041/6 = 173.5.",chk=(sum(cs)/6,173.5),data=D,set_id=S)
    fall = [yr[i] for i in range(1, 6) if cs[i] < cs[i-1]]; assert fall == [2022]
    A(s,T,"Medium","In how many years were sales lower than in the previous year?",["0","1","2","3"],str(len(fall)),
      "Only 2022 (135) is below the year before it (150 in 2021). Every other year is higher, so the answer is 1.","केवल 2022 (135) अपने पिछले वर्ष (2021 में 150) से कम है। बाकी हर वर्ष बिक्री बढ़ी, इसलिए उत्तर 1 है।",chk=(len(fall),1),data=D,set_id=S)
    A(s,T,"Medium","What is the ratio of cars sold in 2021 to cars sold in 2025?",["3 : 5","5 : 8","4 : 7","5 : 7"],"5 : 8",
      "150 : 240 = 5 : 8 (dividing both by 30).","150 : 240 = 5 : 8 (दोनों को 30 से भाग देने पर)।",chk=(F(150,240),F(5,8)),data=D,set_id=S)
    r22, r25 = c[2022]*8, c[2025]*9; assert (r22, r25) == (1080, 2160)
    A(s,T,"Hard","The average price per car was ₹8 lakh in 2022 and ₹9 lakh in 2025. By what percentage did the dealer's total sales revenue rise from 2022 to 2025?",["77.8%","88.9%","100%","125%"],"100%",
      "Revenue 2022 = 135 × 8 = ₹1080 lakh. Revenue 2025 = 240 × 9 = ₹2160 lakh. Rise = 1080/1080 × 100 = 100%.","राजस्व 2022 = 135 × 8 = ₹1080 लाख। राजस्व 2025 = 240 × 9 = ₹2160 लाख। वृद्धि = 1080/1080 × 100 = 100%।",chk=((r25-r22)/r22*100,100),data=D,set_id=S)

    # ---------------- Pie: employees ----------------
    T = "Pie Charts"; S = "pie-staff-b8"
    pc = {"Production": 35, "Sales": 20, "HR": 5, "Finance": 15, "IT": 25}; N = 3600; e = {k: N*v//100 for k, v in pc.items()}
    D = pie("Employees of a company by department (total 3,600)", list(pc.items()))
    A(s,T,"Easy","How many employees work in IT?",["720","810","900","960"],"900","25% of 3600 = 900.","3600 का 25% = 900.",chk=(e["IT"],900),data=D,set_id=S)
    A(s,T,"Easy","What is the central angle of the Finance sector?",["48°","54°","60°","72°"],"54°","15% of 360° = 54°.","360° का 15% = 54°.",chk=(.15*360,54),data=D,set_id=S)
    A(s,T,"Medium","How many more employees work in Production than in Sales?",["450","540","600","720"],"540",
      "Production − Sales = (35% − 20%) of 3600 = 15% of 3600 = 540.","उत्पादन − बिक्री = (35% − 20%) × 3600 = 3600 का 15% = 540.",chk=(e["Production"]-e["Sales"],540),data=D,set_id=S)
    A(s,T,"Medium","What is the ratio of HR employees to IT employees?",["1 : 4","1 : 5","2 : 9","1 : 6"],"1 : 5","5% : 25% = 1 : 5.","अनुपात = 5% : 25% = 1 : 5.",chk=(F(e["HR"],e["IT"]),F(1,5)),data=D,set_id=S)
    w_other = 1350 - e["Production"]*40//100 - e["Sales"]*30//100; assert (e["Production"], e["Sales"], w_other) == (1260, 720, 630)
    A(s,T,"Hard","40% of Production staff and 30% of Sales staff are women. If the company has 1,350 women in all, how many women work in HR, Finance and IT together?",["540","585","630","675"],"630",
      "Production = 1260, so women there = 40% of 1260 = 504. Sales = 720, so women = 30% of 720 = 216. Others = 1350 − 504 − 216 = 630.",
      "उत्पादन = 1260, महिलाएँ = 1260 का 40% = 504. बिक्री = 720, महिलाएँ = 720 का 30% = 216. बाकी = 1350 − 504 − 216 = 630.",chk=(w_other,630),data=D,set_id=S)

    # ---------------- Pie: book cost ----------------
    S = "pie-book-b8"
    bk = {"Paper": 25, "Printing": 20, "Binding": 10, "Royalty": 15, "Promotion": 12, "Transport": 8, "Miscellaneous": 10}; TC = 400000
    D = pie("Cost of publishing 5,000 copies of a book (total ₹4,00,000)", list(bk.items()))
    A(s,T,"Easy","How much is paid as royalty?",["₹48,000","₹54,000","₹60,000","₹64,000"],"₹60,000","15% of ₹4,00,000 = ₹60,000.","₹4,00,000 का 15% = ₹60,000.",chk=(TC*.15,60000),data=D,set_id=S)
    A(s,T,"Medium","What is the central angle of the Promotion sector?",["40.8°","43.2°","45°","48.6°"],"43.2°","12% of 360° = 43.2°.","360° का 12% = 43.2°.",chk=(round(.12*360,1),43.2),data=D,set_id=S)
    A(s,T,"Medium","If the cost of paper rises by 20% and all other costs stay the same, by what percentage does the total cost rise?",["4%","5%","6%","20%"],"5%",
      "Paper is 25% of the total. A 20% rise in it adds 20% of 25% = 5% to the total.","कागज़ कुल का 25% है। इसमें 20% वृद्धि से कुल में 25% का 20% = 5% जुड़ता है।",chk=(25*.2,5),data=D,set_id=S)
    A(s,T,"Medium","The publisher sells every copy at a price that gives a 25% profit on cost. What is the price of one copy?",["₹90","₹96","₹100","₹125"],"₹100",
      "Cost per copy = 400000/5000 = ₹80. Price = 80 × 1.25 = ₹100.","प्रति प्रति लागत = 400000/5000 = ₹80. मूल्य = 80 × 1.25 = ₹100.",chk=(TC/5000*1.25,100),data=D,set_id=S)
    A(s,T,"Hard","By what percentage is the combined cost of printing and binding more than the cost of transport?",["225%","250%","275%","300%"],"275%",
      "Printing + binding = 20% + 10% = 30%. Transport = 8%. (30 − 8)/8 × 100 = 275%.","छपाई + बाइंडिंग = 20% + 10% = 30%. परिवहन = 8%. (30 − 8)/8 × 100 = 275%.",chk=((30-8)/8*100,275),data=D,set_id=S)

    # ---------------- Line: exports of two companies ----------------
    T = "Line Graphs"; S = "line-exports-b8"
    ly = [2020, 2021, 2022, 2023, 2024, 2025]; xa = [40, 48, 45, 60, 72, 90]; xb = [50, 45, 54, 63, 70, 84]
    D = lines("Exports of companies A and B (₹ crore)", ly, [("A", xa, "#db2777"), ("B", xb, "#0891b2")], 100)
    fb = [ly[i] for i in range(1, 6) if xb[i] < xb[i-1]]; assert fb == [2021]
    A(s,T,"Easy","In which year did B's exports fall compared with the previous year?",["2021","2022","2023","2024"],"2021",
      "B: 50 → 45 from 2020 to 2021 is the only fall; every later year rises (54, 63, 70, 84).","B: 2020 से 2021 में 50 → 45 ही एकमात्र गिरावट है; बाद के सभी वर्षों में वृद्धि है (54, 63, 70, 84)।",data=D,set_id=S)
    ab = [ly[i] for i in range(6) if xa[i] > xb[i]]; assert ab == [2021, 2024, 2025]
    A(s,T,"Medium","In how many of the six years were A's exports higher than B's?",["2","3","4","5"],"3",
      "A > B in 2021 (48 vs 45), 2024 (72 vs 70) and 2025 (90 vs 84). In 2020, 2022 and 2023 B is higher. So 3 years.",
      "A > B: 2021 (48 बनाम 45), 2024 (72 बनाम 70) और 2025 (90 बनाम 84)। 2020, 2022 और 2023 में B अधिक है। अतः 3 वर्ष।",chk=(len(ab),3),data=D,set_id=S)
    g = {ly[i]: (xa[i]-xa[i-1])/xa[i-1] for i in range(1, 6)}; assert max(g, key=g.get) == 2023 and sorted(g.values())[-2] < g[2023]
    A(s,T,"Medium","In which year was A's year-on-year percentage growth in exports the highest?",["2021","2023","2024","2025"],"2023",
      "A's growth: 2021: 8/40 = 20%; 2022: a fall; 2023: 15/45 = 33.3%; 2024: 12/60 = 20%; 2025: 18/72 = 25%. Highest is 2023.",
      "A की वृद्धि: 2021: 8/40 = 20%; 2022: गिरावट; 2023: 15/45 = 33.3%; 2024: 12/60 = 20%; 2025: 18/72 = 25%. सबसे अधिक 2023 में।",data=D,set_id=S)
    assert sum(xb) == 366
    A(s,T,"Medium","What were B's average annual exports over the six years (₹ crore)?",["58","60","61","63"],"61",
      "B total = 50 + 45 + 54 + 63 + 70 + 84 = 366. Average = 366/6 = 61.","B का योग = 50 + 45 + 54 + 63 + 70 + 84 = 366. औसत = 366/6 = 61.",chk=(sum(xb)/6,61),data=D,set_id=S)
    A(s,T,"Hard","By what percentage did the combined exports of A and B rise from 2020 to 2025?",["86.7%","90%","93.3%","96.7%"],"93.3%",
      "2020: 40 + 50 = 90. 2025: 90 + 84 = 174. Rise = 84/90 × 100 = 93.3%.","2020: 40 + 50 = 90. 2025: 90 + 84 = 174. वृद्धि = 84/90 × 100 = 93.3%.",chk=(round((174-90)/90*100,1),93.3),data=D,set_id=S)

    # ---------------- Line: exam appeared vs qualified ----------------
    S = "line-exam-b8"
    ey = [2019, 2020, 2021, 2022, 2023, 2024]; ap = [50, 60, 64, 72, 80, 90]; qu = [20, 21, 32, 27, 36, 45]
    qp = [F(q*100, a) for q, a in zip(qu, ap)]; assert qp == [40, 35, 50, F(75,2), 45, 50]
    D = lines("Candidates who appeared and qualified in an exam (hundreds)", ey, [("Appeared", ap, "#4f46e5"), ("Qualified", qu, "#16a34a")], 100)
    A(s,T,"Easy","What was the qualifying percentage in 2022?",["35%","37.5%","40%","42.5%"],"37.5%","27/72 × 100 = 37.5%.","उत्तीर्ण प्रतिशत = 27/72 × 100 = 37.5%.",chk=(27/72*100,37.5),data=D,set_id=S)
    assert min(range(6), key=lambda i: qp[i]) == 1
    A(s,T,"Medium","In which year was the qualifying percentage the lowest?",["2019","2020","2022","2023"],"2020",
      "Qualifying %: 2019 40%, 2020 21/60 = 35%, 2021 50%, 2022 37.5%, 2023 45%, 2024 50%. Lowest is 2020.",
      "उत्तीर्ण %: 2019 40%, 2020 21/60 = 35%, 2021 50%, 2022 37.5%, 2023 45%, 2024 50%. सबसे कम 2020 में।",data=D,set_id=S)
    k45 = sum(1 for x in qp if x >= 45); assert k45 == 3
    A(s,T,"Medium","In how many years was the qualifying percentage 45% or more?",["2","3","4","5"],"3",
      "2021 (32/64 = 50%), 2023 (36/80 = 45%) and 2024 (45/90 = 50%). So 3 years.","2021 (32/64 = 50%), 2023 (36/80 = 45%) और 2024 (45/90 = 50%)। अतः 3 वर्ष।",chk=(k45,3),data=D,set_id=S)
    nq = (sum(ap) - sum(qu)) * 100; assert (sum(ap), sum(qu), nq) == (416, 181, 23500)
    A(s,T,"Medium","How many candidates in all failed to qualify over the six years?",["22,500","23,500","24,500","25,000"],"23,500",
      "Appeared = 416 hundred, qualified = 181 hundred. Not qualified = 235 hundred = 23,500.","उपस्थित = 416 सौ, उत्तीर्ण = 181 सौ। अनुत्तीर्ण = 235 सौ = 23,500.",chk=(nq,23500),data=D,set_id=S)
    A(s,T,"Hard","By what percentage did the number of qualified candidates rise from 2019 to 2024?",["100%","112.5%","125%","150%"],"125%",
      "20 → 45 hundred. Rise = 25/20 × 100 = 125%.","20 → 45 सौ। वृद्धि = 25/20 × 100 = 125%.",chk=((45-20)/20*100,125),data=D,set_id=S)

    # ---------------- Caselet: school streams ----------------
    T = "Caselets"; S = "caselet-streams-b8"
    tot = 1200; bo, gi = tot*7//12, tot*5//12; sci, com, art = tot*45//100, tot*35//100, tot*20//100
    sb, sg = sci*5//9, sci*4//9; cg = com*40//100; cb = com - cg; ag = gi - sg - cg; ab_ = art - ag
    assert (bo, gi, sci, com, art, sb, sg, cg, cb, ag, ab_) == (700, 500, 540, 420, 240, 300, 240, 168, 252, 92, 148) and sb + cb + ab_ == bo
    D = "<b>Caselet</b>" + P("A school has 1,200 senior students; boys and girls are in the ratio 7 : 5. Each student is in exactly one stream: Science (45% of students), Commerce (35%) or Arts (the rest). In Science, boys and girls are in the ratio 5 : 4. In Commerce, 40% of the students are girls.")
    SS = "Boys = 700, girls = 500. Science = 540 (boys 300, girls 240), Commerce = 420 (girls 168, boys 252), Arts = 240."
    SH = "लड़के = 700, लड़कियाँ = 500. विज्ञान = 540 (लड़के 300, लड़कियाँ 240), वाणिज्य = 420 (लड़कियाँ 168, लड़के 252), कला = 240."
    A(s,T,"Easy","How many girls are in the Commerce stream?",["148","168","176","252"],"168",SS+" Commerce girls = 40% of 420 = 168.",SH+" वाणिज्य में लड़कियाँ = 420 का 40% = 168.",chk=(cg,168),data=D,set_id=S)
    A(s,T,"Medium","How many boys are in the Arts stream?",["92","132","148","160"],"148",SS+" Arts girls = 500 − 240 − 168 = 92, so Arts boys = 240 − 92 = 148.",SH+" कला में लड़कियाँ = 500 − 240 − 168 = 92, अतः कला में लड़के = 240 − 92 = 148.",chk=(ab_,148),data=D,set_id=S)
    A(s,T,"Medium","What percentage of the Arts students are girls (approximately)?",["35.0%","38.3%","40.0%","42.5%"],"38.3%",SS+" Arts girls = 500 − 240 − 168 = 92. 92/240 × 100 = 38.3%.",SH+" कला में लड़कियाँ = 500 − 240 − 168 = 92. 92/240 × 100 = 38.3%.",chk=(round(ag/art*100,1),38.3),data=D,set_id=S)
    A(s,T,"Medium","What is the ratio of boys in Science to boys in Commerce?",["5 : 4","25 : 21","6 : 5","20 : 17"],"25 : 21",SS+" 300 : 252 = 25 : 21 (dividing by 12).",SH+" 300 : 252 = 25 : 21 (12 से भाग देने पर)।",chk=(F(sb,cb),F(25,21)),data=D,set_id=S)
    nb = F(ab_+60, art+60); assert nb == F(208,300)
    A(s,T,"Hard","If 60 boys move from Science to Arts, what percentage of the Arts stream will then be boys (approximately)?",["61.7%","65.0%","69.3%","72.0%"],"69.3%",
      SS+" Arts boys = 240 − 92 = 148. After the move: Arts boys = 148 + 60 = 208, Arts total = 240 + 60 = 300. 208/300 × 100 = 69.3%.",
      SH+" कला में लड़के = 240 − 92 = 148. स्थानांतरण के बाद: कला में लड़के = 148 + 60 = 208, कुल = 240 + 60 = 300. 208/300 × 100 = 69.3%.",chk=(round(float(nb)*100,1),69.3),data=D,set_id=S)

    # ---------------- Caselet: phone shops ----------------
    S = "caselet-phones-b8"
    X = 1800 // 3; Z = (1800 - X - 50) // 2; Y = Z + 50; xp, yp = X*60//100, Y*40//100; zp = 1000 - xp - yp
    assert (X, Y, Z, xp, yp, zp) == (600, 625, 575, 360, 250, 390) and X + Y + Z == 1800
    xq, yq, zq = X - xp, Y - yp, Z - zp; assert (xq, yq, zq) == (240, 375, 185)
    D = "<b>Caselet</b>" + P("Three shops X, Y and Z together sold 1,800 phones of two brands, P and Q, in a month. X sold one-third of all the phones, and Y sold 50 more phones than Z. Brand P made up 60% of X's sales and 40% of Y's sales. In all, 1,000 phones of brand P were sold.")
    SS = "X = 600, so Y + Z = 1200 with Y = Z + 50: Z = 575, Y = 625. Brand P: X 360, Y 250, so Z = 1000 − 360 − 250 = 390. Brand Q: X 240, Y 375, Z 185."
    SH = "X = 600, अतः Y + Z = 1200 तथा Y = Z + 50: Z = 575, Y = 625. ब्रांड P: X 360, Y 250, अतः Z = 1000 − 360 − 250 = 390. ब्रांड Q: X 240, Y 375, Z 185."
    A(s,T,"Easy","How many brand Q phones did shop Y sell?",["250","325","375","400"],"375",SS+" Y's brand Q = 625 − 250 = 375.",SH+" Y का ब्रांड Q = 625 − 250 = 375.",chk=(yq,375),data=D,set_id=S)
    A(s,T,"Medium","How many brand P phones did shop Z sell?",["360","375","390","410"],"390",SS,SH,chk=(zp,390),data=D,set_id=S)
    assert max({"X": xq, "Y": yq, "Z": zq}.items(), key=lambda kv: kv[1])[0] == "Y"
    A(s,T,"Medium","Which shop sold the most brand Q phones?",["X","Y","Z","X and Y equally"],"Y",SS+" So Y sold the most.",SH+" अतः Y ने सबसे अधिक बेचे।",data=D,set_id=S)
    A(s,T,"Medium","Brand P made up roughly what percentage of shop Z's sales?",["62.5%","65.2%","67.8%","70.4%"],"67.8%",SS+" 390/575 × 100 = 67.8%.",SH+" 390/575 × 100 = 67.8%.",chk=(round(zp/Z*100,1),67.8),data=D,set_id=S)
    pr = xp*1500 + xq*1200; assert pr == 828000
    A(s,T,"Hard","The profit is ₹1,500 on each brand P phone and ₹1,200 on each brand Q phone. What was shop X's total profit for the month?",["₹7,92,000","₹8,10,000","₹8,28,000","₹8,64,000"],"₹8,28,000",
      "X = 600 phones: P = 60% = 360, Q = 240. Profit = 360 × 1500 + 240 × 1200 = 540000 + 288000 = ₹8,28,000.",
      "X = 600 फ़ोन: P = 60% = 360, Q = 240. लाभ = 360 × 1500 + 240 × 1200 = 540000 + 288000 = ₹8,28,000.",chk=(pr,828000),data=D,set_id=S)

    # ---------------- Arrangement: 4-floor building, two flats per floor ----------------
    T = "Arrangements"; S = "floors-flats-b8"
    names = "JKLMNOPQ"; slots = [(f, sd) for f in range(1, 5) for sd in "WE"]; sols = []
    for p in it.permutations(slots):
        a = dict(zip(names, p)); fl = lambda x: a[x][0]; sd = lambda x: a[x][1]
        if fl("K") == 4 and a["Q"] == (1, "E") and a["L"] == (fl("Q")+1, sd("Q")) and a["P"] == (fl("M")-1, sd("M")) \
           and fl("N") == fl("L") and sd("O") == "W" and fl("O") < fl("J") and sd("M") == "E": sols.append(a)
    assert len(sols) == 1; a = sols[0]; at = {v: k for k, v in a.items()}
    assert [at[(f, "W")] + at[(f, "E")] for f in (4, 3, 2, 1)] == ["KM", "JP", "NL", "OQ"]
    D = "<b>Building puzzle</b>" + P("Eight people J, K, L, M, N, O, P and Q live in a four-storey building (floor 1 is the lowest, floor 4 the top). Each floor has two flats, West and East, and each person lives in a different flat.<br>• K lives on the top floor.<br>• Q lives in the East flat of floor 1.<br>• L lives in the flat directly above Q's flat.<br>• P lives in the flat directly below M's flat, and M lives in an East flat.<br>• N lives on the same floor as L.<br>• O lives in a West flat on a floor below J's floor.")
    SS = "Q is in floor 1 East, so L is in floor 2 East and N in floor 2 West. M is in an East flat with P directly below it, so M is in floor 4 East and P in floor 3 East. K takes floor 4 West. O must be below J in a West flat: the West flats left are on floors 3 and 1, so J is in floor 3 West and O in floor 1 West."
    SH = "Q मंज़िल 1 पूर्व में है, अतः L मंज़िल 2 पूर्व में और N मंज़िल 2 पश्चिम में। M पूर्वी फ़्लैट में है और P ठीक उसके नीचे, अतः M मंज़िल 4 पूर्व और P मंज़िल 3 पूर्व में। K मंज़िल 4 पश्चिम में। O, J से नीचे पश्चिमी फ़्लैट में: बचे पश्चिमी फ़्लैट मंज़िल 3 और 1 पर हैं, अतः J मंज़िल 3 पश्चिम और O मंज़िल 1 पश्चिम में।"
    A(s,T,"Medium","Who lives in the West flat of floor 3?",["J","N","O","P"],at[(3, "W")],SS+" So J.",SH+" अतः J।",data=D,set_id=S)
    A(s,T,"Easy","Who lives on the same floor as O?",["N","Q","L","J"],at[(1, "E")],SS+" O shares floor 1 with Q.",SH+" O के साथ मंज़िल 1 पर Q है।",data=D,set_id=S)
    A(s,T,"Medium","Who lives in the flat directly below K?",["P","N","J","O"],at[(3, "W")],SS+" Below floor 4 West is floor 3 West: J.",SH+" मंज़िल 4 पश्चिम के नीचे मंज़िल 3 पश्चिम है: J।",data=D,set_id=S)
    A(s,T,"Medium","On which floor does N live?",["1","2","3","4"],str(a["N"][0]),SS+" N is on floor 2.",SH+" N मंज़िल 2 पर है।",chk=(a["N"][0],2),data=D,set_id=S)
    east = "".join(at[(f, "E")] for f in (4, 3, 2, 1)); assert east == "MPLQ"
    A(s,T,"Hard","Which of these groups lives entirely in East flats?",["M, P, N","K, P, L","M, L, Q","J, L, Q"],"M, L, Q",SS+" East flats from top: M, P, L, Q. Of the groups, only M, L, Q are all East.",SH+" ऊपर से पूर्वी फ़्लैट: M, P, L, Q। विकल्पों में केवल M, L, Q सभी पूर्व में हैं।",data=D,set_id=S)

    # ---------------- Arrangement: row of six with colours ----------------
    S = "row-colours-b8"
    N6 = "RSTUVW"; CL = ["Red", "Blue", "Green", "Black", "White", "Pink"]; out = []
    for p in it.permutations(range(6)):
        a = dict(zip(N6, p))
        if not (a["T"] == a["V"]-2 and a["R"] == a["T"]-2 and abs(a["U"]-a["W"]) == 2 and a["S"] in (0, 5)): continue
        at = {v: k for k, v in a.items()}
        for q in it.permutations(CL):
            c = dict(zip(N6, q)); cp = {c[n]: a[n] for n in N6}
            if cp["Black"] in (0, 5) and c["V"] == "Black" and cp["Pink"] == a["W"]+1 and cp["Green"] in (0, 5) and c["U"] == "Red" and cp["White"] == cp["Blue"]-1:
                out.append(("".join(at[i] for i in range(6)), [c[at[i]] for i in range(6)]))
    assert out == [("SRWTUV", ["Green", "White", "Blue", "Pink", "Red", "Black"])]
    D = "<b>Row arrangement</b>" + P("Six people R, S, T, U, V and W sit in a row facing north. Each likes a different colour: Red, Blue, Green, Black, White or Pink.<br>• V likes Black, and the person who likes Black sits at one end of the row.<br>• T sits second to the left of V.<br>• R sits second to the left of T.<br>• Exactly one person sits between U and W.<br>• S sits at one end of the row.<br>• The person who likes Pink sits immediately to the right of W.<br>• U likes Red.<br>• The person who likes White sits immediately to the left of the person who likes Blue.<br>• The person who likes Green sits at one end of the row.")
    SS = "V (Black) is at an end; T is second to its left and R second to T's left, so V cannot be at the left end: V is 6th, T 4th, R 2nd (counting from the left). S is at an end, so S is 1st. U and W take the 3rd and 5th seats. Pink is just right of W: if W were 5th, Pink would be V, who likes Black; so W is 3rd, U 5th and T likes Pink. Green is at an end, so S likes Green. White is just left of Blue: only R (2nd) and W (3rd) remain, so R likes White and W likes Blue. Order: S, R, W, T, U, V."
    SH = "V (काला) एक छोर पर है; T उसके बाएँ से दूसरा और R, T के बाएँ से दूसरा है, अतः V बाएँ छोर पर नहीं हो सकता: V 6वें, T 4थे, R 2रे स्थान पर (बाएँ से)। S छोर पर है, अतः S 1ले स्थान पर। U और W 3रे और 5वें स्थान पर। गुलाबी W के ठीक दाएँ है: यदि W 5वें होता तो गुलाबी V होता, जिसे काला पसंद है; अतः W 3रे, U 5वें और T को गुलाबी पसंद है। हरा छोर पर है, अतः S को हरा। सफ़ेद, नीले के ठीक बाएँ है: केवल R (2रे) और W (3रे) बचे हैं, अतः R को सफ़ेद और W को नीला। क्रम: S, R, W, T, U, V।"
    A(s,T,"Medium","Which colour does R like?",["Blue","Green","White","Pink"],"White",SS,SH,data=D,set_id=S)
    A(s,T,"Easy","Who likes Pink?",["T","U","W","S"],"T",SS,SH,data=D,set_id=S)
    A(s,T,"Medium","How many people sit between S and U?",["2","3","4","1"],"3",SS+" Between S (1st) and U (5th) sit R, W and T: 3 people.",SH+" S (1ले) और U (5वें) के बीच R, W और T बैठे हैं: 3 व्यक्ति।",chk=(3,3),data=D,set_id=S)
    A(s,T,"Medium","Who sits immediately to the right of the person who likes Blue?",["R","T","U","V"],"T",SS+" W likes Blue; T sits just to W's right.",SH+" W को नीला पसंद है; T ठीक W के दाएँ बैठा है।",data=D,set_id=S)
    A(s,T,"Hard","Which person and colour are correctly matched?",["U – Green","W – Blue","S – White","R – Pink"],"W – Blue",SS,SH,data=D,set_id=S)

    # ---------------- Games: four-team league, 3-1-0 points ----------------
    T = "Games & Tournaments"; S = "league-four-b8"
    tm = "ABCD"; pr = list(it.combinations(tm, 2)); res = []
    for r in it.product((0, 1, 2), repeat=6):     # 0: first team wins, 1: draw, 2: second wins
        pt = dict.fromkeys(tm, 0)
        for (x, y), v in zip(pr, r):
            if v == 1: pt[x] += 1; pt[y] += 1
            else: pt[x if v == 0 else y] += 3
        if [pt[t] for t in tm] == [7, 5, 4, 0]: res.append(dict(zip(pr, r)))
    assert res == [{("A","B"):1,("A","C"):0,("A","D"):0,("B","C"):1,("B","D"):0,("C","D"):0}]
    D = "<b>League table</b>" + P("Four teams A, B, C and D play a league in which each team plays every other team once. A win earns 3 points, a draw 1 point and a loss 0. The final points were A 7, B 5, C 4 and D 0.")
    SS = "6 matches were played and 16 points were awarded. A decided match gives 3 points and a draw 2, so with d decided matches 3d + 2(6 − d) = 16, giving d = 4 and 2 draws. D has 0, so D lost all 3 matches. A = 7 = two wins + one draw, B = 5 = one win + two draws, C = 4 = one win + one draw. B's two draws must be against A and C (D drew nothing), so B beat D, C beat D, and A beat C."
    SH = "6 मैच खेले गए और 16 अंक बँटे। निर्णायक मैच से 3 और ड्रॉ से 2 अंक मिलते हैं, अतः d निर्णायक मैचों पर 3d + 2(6 − d) = 16, जिससे d = 4 और 2 ड्रॉ। D के 0 अंक हैं, अतः D तीनों 3 मैच हारा। A = 7 = दो जीत + एक ड्रॉ, B = 5 = एक जीत + दो ड्रॉ, C = 4 = एक जीत + एक ड्रॉ। B के दोनों ड्रॉ A और C से ही हो सकते हैं (D ने कोई ड्रॉ नहीं खेला), अतः B ने D को, C ने D को और A ने C को हराया।"
    A(s,T,"Easy","How many matches in the league were drawn?",["1","2","3","4"],"2",SS,SH,chk=(2,2),data=D,set_id=S)
    A(s,T,"Medium","What was the result of the match between A and C?",["A won","C won","It was drawn","Cannot be determined"],"A won",SS,SH,data=D,set_id=S)
    A(s,T,"Medium","Which team drew the most matches?",["A","B","C","D"],"B",SS+" B drew 2 matches; A and C drew 1 each.",SH+" B ने 2 मैच ड्रॉ किए; A और C ने 1 मैच प्रत्येक।",data=D,set_id=S)
    A(s,T,"Medium","Against which team did C record its only win?",["A","B","D","C did not win any match"],"D",SS,SH,data=D,set_id=S)
    p2 = {t: 0 for t in tm}
    for (x, y), v in res[0].items():
        if v == 1: p2[x] += 1; p2[y] += 1
        else: p2[x if v == 0 else y] += 2
    assert p2 == {"A": 5, "B": 4, "C": 3, "D": 0}
    A(s,T,"Hard","If the same results were scored with 2 points for a win (draw 1, loss 0), how many points would B have?",["3","4","5","6"],"4",
      SS+" B has 1 win and 2 draws: 2 + 1 + 1 = 4.",SH+" B की 1 जीत और 2 ड्रॉ: 2 + 1 + 1 = 4.",chk=(p2["B"],4),data=D,set_id=S)

    # ---------------- Games: knockout with byes ----------------
    S = "knockout-byes-b8"
    n = 40; full = 1 << (n-1).bit_length(); by = full - n; r1 = (n - by)//2; r2 = by + r1; rounds = (full).bit_length() - 1
    assert (full, by, r1, r2, rounds) == (64, 24, 8, 32, 6)
    D = "<b>Knockout draw</b>" + P("A badminton tournament has 40 players in a single-elimination (knockout) draw: every match has one winner, who goes on, and the loser is out. The draw is made up to the next power of 2 by giving byes in round 1 only (a player with a bye goes straight to round 2). The two semi-final losers also play one extra match for third place.")
    A(s,T,"Easy","How many players get a bye in round 1?",["8","16","24","32"],"24","The next power of 2 above 40 is 64. Byes = 64 − 40 = 24.","40 से ऊपर 2 की अगली घात 64 है। बाई = 64 − 40 = 24.",chk=(by,24),data=D,set_id=S)
    A(s,T,"Medium","How many matches are played in round 1?",["8","12","16","20"],"8","Byes = 64 − 40 = 24, so 40 − 24 = 16 players play in round 1, making 16/2 = 8 matches.","बाई = 64 − 40 = 24, अतः 40 − 24 = 16 खिलाड़ी दौर 1 में खेलते हैं, यानी 16/2 = 8 मैच।",chk=(r1,8),data=D,set_id=S)
    A(s,T,"Medium","How many players take part in round 2?",["24","28","32","36"],"32","The 24 bye players join the 8 winners of round 1: 24 + 8 = 32.","24 बाई वाले खिलाड़ी दौर 1 के 8 विजेताओं से मिलते हैं: 24 + 8 = 32.",chk=(r2,32),data=D,set_id=S)
    A(s,T,"Medium","How many rounds does the knockout need to produce a champion?",["5","6","7","8"],"6","The draw has 64 = 2^6 slots, so 6 rounds (64 → 32 → 16 → 8 → 4 → 2 → 1).","ड्रॉ में 64 = 2^6 स्थान हैं, अतः 6 दौर (64 → 32 → 16 → 8 → 4 → 2 → 1)।",chk=(rounds,6),data=D,set_id=S)
    A(s,T,"Hard","How many matches are played in the whole tournament, including the third-place match?",["39","40","41","63"],"40",
      "Every knockout match eliminates exactly one player, and 39 of the 40 players must be eliminated: 39 matches. Adding the third-place match gives 40.",
      "हर नॉकआउट मैच में ठीक एक खिलाड़ी बाहर होता है, और 40 में से 39 को बाहर होना है: 39 मैच। तीसरे स्थान का मैच जोड़कर 40.",chk=(n-1+1,40),data=D,set_id=S)

    # ---------------- Venn: three newspapers ----------------
    T = "Venn Diagrams"; S = "venn-papers-b8"
    oA, oB, oC, AB, BC, AC, ABC = 120, 90, 70, 40, 30, 25, 20; TOT = 500
    nA, nB, nC = oA+AB+AC+ABC, oB+AB+BC+ABC, oC+BC+AC+ABC; nAB, nBC, nAC = AB+ABC, BC+ABC, AC+ABC
    assert (nA, nB, nC, nAB, nBC, nAC) == (205, 180, 145, 60, 50, 45)
    none = TOT - (nA+nB+nC-nAB-nBC-nAC+ABC); assert none == 105
    D = "<b>Survey</b>" + P("500 people were asked which of three newspapers A, B and C they read. 205 read A, 180 read B and 145 read C. 60 read both A and B, 50 read both B and C, 45 read both A and C, and 20 read all three.")
    SS = "Only A and B = 60 − 20 = 40, only B and C = 50 − 20 = 30, only A and C = 45 − 20 = 25. Only A = 205 − 40 − 25 − 20 = 120, only B = 180 − 40 − 30 − 20 = 90, only C = 145 − 30 − 25 − 20 = 70."
    SH = "केवल A और B = 60 − 20 = 40, केवल B और C = 50 − 20 = 30, केवल A और C = 45 − 20 = 25. केवल A = 205 − 40 − 25 − 20 = 120, केवल B = 180 − 40 − 30 − 20 = 90, केवल C = 145 − 30 − 25 − 20 = 70."
    A(s,T,"Easy","How many people read none of the three newspapers?",["95","105","115","125"],"105","At least one = 205 + 180 + 145 − 60 − 50 − 45 + 20 = 395. None = 500 − 395 = 105.","कम से कम एक = 205 + 180 + 145 − 60 − 50 − 45 + 20 = 395. कोई नहीं = 500 − 395 = 105.",chk=(none,105),data=D,set_id=S)
    A(s,T,"Medium","How many people read exactly one newspaper?",["260","270","280","290"],"280",SS+" Exactly one = 120 + 90 + 70 = 280.",SH+" ठीक एक = 120 + 90 + 70 = 280.",chk=(oA+oB+oC,280),data=D,set_id=S)
    A(s,T,"Medium","How many people read at least two newspapers?",["95","105","115","125"],"115",SS+" At least two = 40 + 30 + 25 + 20 = 115.",SH+" कम से कम दो = 40 + 30 + 25 + 20 = 115.",chk=(AB+BC+AC+ABC,115),data=D,set_id=S)
    A(s,T,"Medium","How many people read B but not C?",["110","120","130","140"],"130",SS+" B but not C = only B + only A and B = 90 + 40 = 130.",SH+" B परंतु C नहीं = केवल B + केवल A और B = 90 + 40 = 130.",chk=(oB+AB,130),data=D,set_id=S)
    A(s,T,"Hard","Among the readers of A, what percentage read only A (approximately)?",["52.4%","55.6%","58.5%","61.0%"],"58.5%",SS+" 120/205 × 100 = 58.5%.",SH+" 120/205 × 100 = 58.5%.",chk=(round(oA/nA*100,1),58.5),data=D,set_id=S)

    # ---------------- Venn: sports club (two sets + overlap bounds) ----------------
    S = "venn-club-b8"
    tot, cr, fb_, nei = 120, 70, 54, 14; both = cr + fb_ - (tot - nei); assert both == 18
    D = "<b>Sports club</b>" + P("A club has 120 members. 70 play cricket, 54 play football and 14 play neither game.")
    A(s,T,"Easy","How many members play both games?",["14","16","18","20"],"18","At least one game = 120 − 14 = 106. Both = 70 + 54 − 106 = 18.","कम से कम एक खेल = 120 − 14 = 106. दोनों = 70 + 54 − 106 = 18.",chk=(both,18),data=D,set_id=S)
    A(s,T,"Medium","How many members play only cricket?",["48","52","56","60"],"52","Both = 70 + 54 − (120 − 14) = 18. Only cricket = 70 − 18 = 52.","दोनों = 70 + 54 − (120 − 14) = 18. केवल क्रिकेट = 70 − 18 = 52.",chk=(cr-both,52),data=D,set_id=S)
    A(s,T,"Medium","How many members play exactly one of the two games?",["84","86","88","90"],"88","Both = 70 + 54 − (120 − 14) = 18. Exactly one = (70 − 18) + (54 − 18) = 52 + 36 = 88.","दोनों = 70 + 54 − (120 − 14) = 18. ठीक एक = (70 − 18) + (54 − 18) = 52 + 36 = 88.",chk=(cr+fb_-2*both,88),data=D,set_id=S)
    A(s,T,"Medium","What percentage of the football players also play cricket (approximately)?",["25.7%","30.0%","33.3%","36.0%"],"33.3%","Both = 70 + 54 − (120 − 14) = 18. 18/54 × 100 = 33.3%.","दोनों = 70 + 54 − (120 − 14) = 18. 18/54 × 100 = 33.3%.",chk=(round(both/fb_*100,1),33.3),data=D,set_id=S)
    # if 'neither' were unknown, minimum overlap = max(0, 70+54-120) = 4
    lo = max(0, cr + fb_ - tot); assert lo == 4
    A(s,T,"Hard","Suppose the number of members playing neither game were not known. What is the least possible number of members who play both games?",["0","4","14","18"],"4",
      "Members playing at least one game can be at most 120. Both = 70 + 54 − (at least one) ≥ 124 − 120 = 4.","कम से कम एक खेल खेलने वाले अधिकतम 120 हो सकते हैं। दोनों = 70 + 54 − (कम से कम एक) ≥ 124 − 120 = 4.",chk=(lo,4),data=D,set_id=S)

    # ---------------- Network: seven towns, all simple paths enumerated ----------------
    T = "Network & Routes"; S = "net-seven-b8"
    rd = {("P","Q"):5,("P","R"):9,("Q","R"):3,("Q","S"):8,("R","S"):4,("R","T"):10,("S","T"):5,("S","U"):9,("T","U"):3,("T","V"):7,("U","V"):2}
    def paths(a, b, closed=(), avoid=()):
        adj = {}
        for (x, y), d in rd.items():
            if (x, y) in closed: continue
            adj.setdefault(x, []).append((y, d)); adj.setdefault(y, []).append((x, d))
        out = []
        def go(u, path, dist):
            if u == b: out.append((dist, "".join(path))); return
            for v, w in adj.get(u, []):
                if v not in path and v not in avoid: go(v, path+[v], dist+w)
        go(a, [a], 0); return sorted(out)
    pv = paths("P","V"); pt = paths("P","T"); qu_ = paths("Q","U"); pvc = paths("P","V",closed=[("S","T")]); pvs = paths("P","V",avoid="S")
    assert pv[0] == (22,"PQRSTUV") and pv[1][0] > 22, pv[:3]
    assert pt[0] == (17,"PQRST") and pt[1][0] > 17, pt[:3]
    assert qu_[0] == (15,"QRSTU") and qu_[1][0] > 15, qu_[:3]
    assert pvc[0][0] == 23 and {p for d, p in pvc if d == 23} == {"PQRSUV", "PQRTUV"}, pvc[:3]
    assert pvs[0] == (23,"PQRTUV") and pvs[1][0] > 23, pvs[:3]
    D = "<b>Two-way roads between seven towns (km)</b><table class='data'><tr><th>Road</th><th>Length</th><th>Road</th><th>Length</th></tr>" + "".join(
        f"<tr><td>{k1[0]}–{k1[1]}</td><td>{v1}</td>" + (f"<td>{k2[0]}–{k2[1]}</td><td>{v2}</td>" if k2 else "<td></td><td></td>") + "</tr>"
        for (k1, v1), (k2, v2) in it.zip_longest(list(rd.items())[:6], list(rd.items())[6:], fillvalue=(None, None))) + "</table><p class='muted' style='margin:0;font-size:.85rem'>No other roads exist.</p>"
    A(s,T,"Medium","What is the shortest road distance from P to T?",["16 km","17 km","18 km","19 km"],"17 km","P–Q–R–S–T = 5 + 3 + 4 + 5 = 17. Other routes, such as P–Q–R–T = 18 and P–R–S–T = 18, are longer.","P–Q–R–S–T = 5 + 3 + 4 + 5 = 17. अन्य मार्ग, जैसे P–Q–R–T = 18 और P–R–S–T = 18, लंबे हैं।",chk=(pt[0][0],17),data=D,set_id=S)
    assert pt[1][0] == 18
    A(s,T,"Medium","What is the shortest road distance from P to V?",["21 km","22 km","23 km","24 km"],"22 km","P–Q–R–S–T–U–V = 5 + 3 + 4 + 5 + 3 + 2 = 22. Every other route is at least 23 km (for example P–Q–R–S–U–V or P–R–S–T–U–V).","P–Q–R–S–T–U–V = 5 + 3 + 4 + 5 + 3 + 2 = 22. बाकी हर मार्ग कम से कम 23 किमी का है (जैसे P–Q–R–S–U–V या P–R–S–T–U–V)।",chk=(pv[0][0],22),data=D,set_id=S)
    assert pv[1][0] == 23 and {"PQRSUV", "PRSTUV"} <= {p for d, p in pv if d == 23}
    A(s,T,"Easy","What is the shortest road distance from Q to U?",["14 km","15 km","16 km","17 km"],"15 km","Q–R–S–T–U = 3 + 4 + 5 + 3 = 15. Every other route is at least 16 km (for example Q–S–T–U = 8 + 5 + 3 = 16).","Q–R–S–T–U = 3 + 4 + 5 + 3 = 15. बाकी हर मार्ग कम से कम 16 किमी का है (जैसे Q–S–T–U = 8 + 5 + 3 = 16)।",chk=(qu_[0][0],15),data=D,set_id=S)
    assert qu_[1][0] == 16 and (16, "QSTU") in qu_
    A(s,T,"Hard","If the road S–T is closed, by how many km does the shortest road distance from P to V increase?",["1 km","2 km","3 km","4 km"],"1 km","With every road open, the best is P–Q–R–S–T–U–V = 5 + 3 + 4 + 5 + 3 + 2 = 22. Without S–T: P–Q–R–S–U–V = 5 + 3 + 4 + 9 + 2 = 23, and P–Q–R–T–U–V = 5 + 3 + 10 + 3 + 2 = 23 as well. Nothing shorter exists, so the increase is 23 − 22 = 1 km.","सभी सड़कें खुली होने पर सबसे छोटा P–Q–R–S–T–U–V = 5 + 3 + 4 + 5 + 3 + 2 = 22. S–T बंद होने पर: P–Q–R–S–U–V = 5 + 3 + 4 + 9 + 2 = 23, और P–Q–R–T–U–V = 5 + 3 + 10 + 3 + 2 = 23 भी। इससे छोटा कोई मार्ग नहीं, अतः वृद्धि = 23 − 22 = 1 किमी।",chk=(pvc[0][0]-pv[0][0],1),data=D,set_id=S)
    A(s,T,"Hard","A truck must go from P to V without passing through town S. What is the shortest distance it can drive?",["21 km","22 km","23 km","25 km"],"23 km","Avoiding S, the route must use R–T: P–Q–R–T–U–V = 5 + 3 + 10 + 3 + 2 = 23. P–R–T–U–V = 9 + 10 + 3 + 2 = 24 is longer.","S से बचते हुए R–T का उपयोग करना होगा: P–Q–R–T–U–V = 5 + 3 + 10 + 3 + 2 = 23. P–R–T–U–V = 9 + 10 + 3 + 2 = 24 लंबा है।",chk=(pvs[0][0],23),data=D,set_id=S)
    assert pvs[1] == (24,"PRTUV")

    # ---------------- Network: delivery round from a depot (all tours enumerated) ----------------
    S = "tour-depot-b8"
    dm = {("O","A"):6,("O","B"):8,("O","C"):10,("O","D"):7,("A","B"):5,("A","C"):9,("A","D"):11,("B","C"):4,("B","D"):12,("C","D"):6}
    dd = lambda x, y: dm.get((x, y), dm.get((y, x)))
    def tours(towns):
        return sorted((sum(dd(a, b) for a, b in zip(("O",)+p, p+("O",))), "O"+"".join(p)+"O") for p in it.permutations(towns))
    t4 = tours("ABCD"); t3 = tours("ABC"); best = t4[0][0]
    assert best == 28 and {p for d, p in t4 if d == 28} == {"OABCDO", "ODCBAO"}, t4[:4]
    assert t3[0] == (25, "OABCO") and t3[1][0] == 25 and t3[2][0] > 25, t3
    D = "<b>Delivery round</b><table class='data'><tr><th>km</th><th>O</th><th>A</th><th>B</th><th>C</th><th>D</th></tr>" + "".join(
        "<tr><th>" + x + "</th>" + "".join(f"<td>{'–' if x == y else dd(x, y)}</td>" for y in "OABCD") + "</tr>" for x in "OABCD") + "</table>" + P("A van starts at depot O, must visit each of the shops A, B, C and D exactly once, and return to O. The table gives the direct distance between every pair of places; the van always drives directly from one place to the next.")
    A(s,T,"Medium","What is the length of the shortest possible round?",["26 km","28 km","30 km","31 km"],"28 km","Checking all 24 orders, the best is O–A–B–C–D–O = 6 + 5 + 4 + 6 + 7 = 28 (or the same round driven in reverse).","सभी 24 क्रम जाँचने पर सबसे छोटा O–A–B–C–D–O = 6 + 5 + 4 + 6 + 7 = 28 है (या यही उलटी दिशा में)।",chk=(best,28),data=D,set_id=S)
    oabdc = dd("O","A")+dd("A","B")+dd("B","D")+dd("D","C")+dd("C","O"); assert oabdc == 39
    A(s,T,"Easy","What is the length of the round O–A–B–D–C–O?",["35 km","37 km","39 km","41 km"],"39 km","6 + 5 + 12 + 6 + 10 = 39.","दूरी = 6 + 5 + 12 + 6 + 10 = 39 किमी।",chk=(oabdc,39),data=D,set_id=S)
    cons = {frozenset(x) for _, p in t4[:2] for x in zip(p, p[1:])}
    assert frozenset("CD") in cons and not {frozenset("AC"), frozenset("BD"), frozenset("AD")} & cons
    A(s,T,"Medium","On the shortest round, which two shops are visited one right after the other?",["A and C","B and D","C and D","A and D"],"C and D","The shortest round is O–A–B–C–D–O (28 km), driven either way. Consecutive shops on it: A–B, B–C and C–D. Of the options, only C and D.","सबसे छोटा चक्कर O–A–B–C–D–O (28 किमी) है, किसी भी दिशा में। इसमें लगातार दुकानें: A–B, B–C और C–D। विकल्पों में केवल C और D।",data=D,set_id=S)
    A(s,T,"Medium","Shop D is closed for the day, so the van visits only A, B and C. What is the shortest round now?",["21 km","23 km","25 km","27 km"],"25 km","There are 3 different rounds (each can be driven either way): O–A–B–C–O = 6 + 5 + 4 + 10 = 25, O–A–C–B–O = 6 + 9 + 4 + 8 = 27, O–B–A–C–O = 8 + 5 + 9 + 10 = 32. Shortest = 25.","3 अलग चक्कर हैं (हर एक दोनों दिशाओं में): O–A–B–C–O = 6 + 5 + 4 + 10 = 25, O–A–C–B–O = 6 + 9 + 4 + 8 = 27, O–B–A–C–O = 8 + 5 + 9 + 10 = 32. सबसे छोटा = 25.",chk=(t3[0][0],25),data=D,set_id=S)
    t3s = {p: d for d, p in t3}; assert (t3s["OABCO"], t3s["OACBO"], t3s["OBACO"]) == (25, 27, 32)
    nobc = [(d, p) for d, p in t4 if "BC" not in p and "CB" not in p]; assert nobc[0] == (35, "OBACDO") and nobc[1][0] == 35 and nobc[2][0] > 35, nobc[:4]
    A(s,T,"Hard","All four shops are open again, but the direct road between B and C is closed, so the van cannot drive straight from B to C or from C to B. What is the shortest round now?",["32 km","33 km","35 km","39 km"],"35 km",
      "Among the 24 orders, drop every round that has B and C next to each other. The best remaining is O–B–A–C–D–O = 8 + 5 + 9 + 6 + 7 = 35 (or its reverse). The next best, O–A–B–D–C–O, is 6 + 5 + 12 + 6 + 10 = 39.",
      "24 क्रमों में से वे सभी चक्कर हटाएँ जिनमें B और C लगातार हैं। बचे हुए में सबसे छोटा O–B–A–C–D–O = 8 + 5 + 9 + 6 + 7 = 35 (या उलटा)। अगला O–A–B–D–C–O = 6 + 5 + 12 + 6 + 10 = 39 है।",chk=(nobc[0][0],35),data=D,set_id=S)
    assert nobc[2][0] == 39 and nobc[2][1] == "OABDCO"
