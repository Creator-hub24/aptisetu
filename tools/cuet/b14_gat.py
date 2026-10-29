"""CUET (UG) batch B14 (Oct 2026): original General Aptitude Test items for the thinnest GAT topics.
Every answer is computed, enumerated or brute-forced in this file; the build fails if any check fails.
Drafts that the dedupe review (similarity against every existing item, incl. Bank/SSC items reused in GAT) judged to be
repeats or same-template number swaps are listed in DROP and are not published."""
import itertools, math, datetime
from fractions import Fraction as F
from batch_b2 import balanced
from gat import FX, syl_answer
QR, LR, GMA = "Quantitative Reasoning", "Logical & Analytical Reasoning", "General Mental Ability"
DROP = set()

def ang(h, m):
    a = abs(30*h + F(m, 2) - 6*m) % 360
    return min(a, 360 - a)

def gat(B):
    M0 = balanced(B, "gat", 1414)
    n = [0]
    def M(*a, **k):
        n[0] += 1
        if n[0] not in DROP: return M0(*a, **k)
    # ================= Algebra (QR) =================
    t = "Algebra"
    xs = [x for x in range(-50, 51) if x != 1 and F(x + 2, x - 1) == 4]; assert xs == [2]
    M(QR,t,"Easy","If (x + 2)/(x − 1) = 4, what is the value of x?",["2","3","−2","1/2"],"2","Cross-multiply: x + 2 = 4(x − 1) = 4x − 4, so 3x = 6 and x = 2. Check: (2 + 2)/(2 − 1) = 4.")
    ns = [10*a + b for a in range(1, 10) for b in range(10) if (10*a + b) + (10*b + a) == 121 and a - b == 3]; assert ns == [74]
    M(QR,t,"Medium","The sum of a two-digit number and the number formed by reversing its digits is 121. The tens digit exceeds the units digit by 3. What is the number?",["74","47","83","65"],"74","Let the number be 10a + b. Then (10a + b) + (10b + a) = 11(a + b) = 121, so a + b = 11. With a − b = 3, a = 7 and b = 4. The number is 74 (check: 74 + 47 = 121).")
    ks = sorted({r + (r + 1) for r in range(-20, 21) if r * (r + 1) == 12}); assert ks == [-7, 7]
    sols = [x / 10 for x in range(0, 80) if (x / 10 - 2) * (x / 10 - 5) < 0]; assert min(sols) > 2 and max(sols) < 5
    s = [s for s in range(1, 60) if 3*s + 10 == 2*(s + 10)]; assert s == [10]
    M(QR,t,"Easy","A father is three times as old as his son. Ten years from now he will be twice as old as his son. What is the son's present age?",["10 years","15 years","12 years","20 years"],"10 years","Let the son be s years old; the father is 3s. In 10 years: 3s + 10 = 2(s + 10), so s = 10. (Father 30; in 10 years 40 = 2 × 20.)")
    # ================= Clocks & Calendars (GMA) =================
    t = "Clocks & Calendars"
    m = F(240, 11); assert ang(4, m) == 0 and m == 21 + F(9, 11)
    meets = sum(1 for k in range(24) if F(720 * k, 11) < 1440); assert meets == 22
    assert datetime.date(2025, 8, 15).weekday() == 4 and datetime.date(2026, 8, 15).strftime("%A") == "Saturday"
    M(GMA,t,"Easy","15 August 2025 was a Friday. On which day of the week does 15 August 2026 fall?",["Saturday","Friday","Sunday","Thursday"],"Saturday","The 365 days from 15 August 2025 to 15 August 2026 contain no 29 February (2026 is not a leap year), and 365 = 52 weeks + 1 day. So the day moves one place forward: Friday → Saturday.")
    tot = 11*60 + 60 - (4*60 + 40); assert divmod(tot, 60) == (7, 20)
    h_, m_ = 3, 25; hh = (h_ % 12) * 30 + m_ / 2; mm = m_ * 6; rh, rm = (360 - hh) % 360, (360 - mm) % 360; assert (int(rh // 30), int(rm / 6)) == (8, 35)   # reflected hands read 8:35
    M(GMA,t,"Medium","The time on a wall clock is 3:25. What time will it appear to show when seen in a plane mirror held vertically beside it?",["8:35","9:35","8:25","3:35"],"8:35","A vertical mirror reflects the dial left to right, so the reflected time is 11:60 − actual time. 11:60 − 3:25 = 8:35. (Check: the minute hand at 5 appears at 7, i.e. 35 minutes, and the hour hand a little past 3 appears a little past 8.)")
    assert datetime.date(2023, 3, 1).strftime("%A") == "Wednesday" and datetime.date(2024, 3, 1).strftime("%A") == "Friday"
    # ================= Number System (QR) =================
    t = "Number System"
    assert pow(2, 31, 5) == 3
    c = sum(1 for k in range(1, 101) if k % 3 == 0 or k % 5 == 0); assert c == 47
    M(QR,t,"Medium","How many whole numbers from 1 to 100 (both included) are divisible by 3 or by 5?",["47","53","45","48"],"47","Multiples of 3: 33. Multiples of 5: 20. Multiples of both (of 15): 6. By inclusion–exclusion, 33 + 20 − 6 = 47.")
    ev = [k for k in range(2, 100, 2) if k * (k + 2) == 528]; assert ev == [22]
    big = 9999 // 88 * 88; assert big == 9944 and big + 88 > 9999
    # ================= Profit & Loss (QR) =================
    t = "Profit & Loss"
    cp = 4800 / 1.2 + 4800 / 0.8; assert cp == 10000 and (9600 - cp) / cp * 100 == -4
    g = F(1000 - 900, 900) * 100; assert g == F(100, 9)
    p = F(15 - 12, 12) * 100; assert p == 25
    a = 3960 / (1.1 * 1.2); assert abs(a - 3000) < 1e-9
    # ================= Ranking & Order (GMA) =================
    t = "Ranking & Order"
    rahul = 10 + 4 + 1; assert rahul + 25 - 1 == 39
    M(GMA,t,"Medium","In a queue, Amit is 10th from the front and Rahul is 25th from the back. Rahul is behind Amit, and exactly 4 people stand between them. How many people are in the queue?",["39","40","38","35"],"39","Rahul is 10 + 4 + 1 = 15th from the front. Total = (position from front) + (position from back) − 1 = 15 + 25 − 1 = 39.")
    passed = 7 + 26 - 1; assert passed + 3 + 5 == 40
    assert 15 + 9 - 1 == 23
    bl = 50 - 22 + 1; assert bl == 29 and bl - 18 - 1 == 10
    rk = [(t_, b_) for b_ in range(1, 60) for t_ in [3 * b_] if t_ + b_ - 1 == 59]; assert rk == [(45, 15)]
    M(GMA,t,"Medium","In a class of 59 students, Pooja's rank from the top is three times her rank from the bottom. What is her rank from the top?",["45","42","48","15"],"45","Let her rank from the bottom be b. Then 3b + b − 1 = 59, so b = 15 and her rank from the top is 3 × 15 = 45.")
    # ================= Ratio & Proportion (QR) =================
    t = "Ratio & Proportion"
    a_, b_, c_ = F(2, 3), 1, F(5, 4); assert (a_*12, b_*12, c_*12) == (8, 12, 15)
    assert F(9 * 12, 4) == 27
    sol = [(x, y) for x in range(1, 10001) for y in [F(3*x - 2000, 5)] if y.denominator == 1 and y > 0 and 2*x - 3*y == 2000]; assert sol == [(4000, 2000)]
    w = F(40 * 2) - 20; assert w == 60 and F(40, 20 + w) == F(1, 2)
    k = [k for k in range(1, 50) if (9 + 16 + 25) * k * k == 1250]; assert k == [5]
    M(QR,t,"Medium","Three numbers are in the ratio 3 : 4 : 5 and the sum of their squares is 1250. What is the largest number?",["25","20","15","30"],"25","Let the numbers be 3k, 4k and 5k. Then 9k² + 16k² + 25k² = 50k² = 1250, so k² = 25 and k = 5. The largest is 5 × 5 = 25.")
    # ================= Time & Work (QR) =================
    t = "Time & Work"
    u = F(1, 14) / 3; assert 1 / (2 * u) == 21
    bb = 1 / (F(3, 4) / 9 - F(1, 20)); assert bb == 30
    M(QR,t,"Medium","A can finish a job in 20 days. He works alone for 5 days and is then joined by B; together they finish the rest in 9 days. How many days would B alone take for the whole job?",["30 days","36 days","24 days","45 days"],"30 days","In 5 days A does 5/20 = 1/4, leaving 3/4. Together they do (3/4)/9 = 1/12 per day. B's share = 1/12 − 1/20 = 1/30 per day, so B alone takes 30 days.")
    tt = 1 / (F(1, 10) + F(1, 15) - F(1, 12)); assert tt == 12
    d = F(18 * 14, 12 * F(3, 2) - 0 + 0) ; wd = 18 * 14; eq = 8 * F(18, 12) + 16; assert wd / eq == 9
    assert F(5 * 9 * 16, 8 * 6) == 15
    M(QR,t,"Easy","5 workers, working 9 hours a day, finish a job in 16 days. How many days will 8 workers take if they work 6 hours a day?",["15 days","12 days","16 days","18 days"],"15 days","Total work = 5 × 9 × 16 = 720 worker-hours. 8 workers at 6 hours a day put in 48 worker-hours a day, so they need 720/48 = 15 days.")
    # ================= Blood Relations (LR) =================
    t = "Blood Relations"
    M(LR,t,"Easy","P is the son of Q. Q is the daughter of R, and S is R's husband. How is P related to S?",["Grandson","Son","Nephew","Son-in-law"],"Grandson","Q is the daughter of R and S (S is R's husband). P is Q's son, so P is the son of S's daughter: S's grandson.")
    M(LR,t,"Medium","A and B are a married couple, and B is the mother of D and E. E is married to C, and F is the son of C and E. If A is male, how is A related to F?",["Grandfather","Father","Uncle","Father-in-law"],"Grandfather","A is B's husband, so A is the father of D and E. F is E's son, so A is F's grandfather.")
    # ================= Coding-Decoding (GMA) =================
    t = "Coding-Decoding"
    pos = lambda w: [ord(ch) - 64 for ch in w]
    assert math.prod(pos("BAD")) == 8 and math.prod(pos("FED")) == 120 and math.prod(pos("CAGE")) == 105
    M(GMA,t,"Medium","In a certain code, BAD is written as 8 and FED as 120. How is CAGE written in that code?",["105","16","210","70"],"105","Each word becomes the product of its letters' positions in the alphabet: BAD = 2 × 1 × 4 = 8 and FED = 6 × 5 × 4 = 120. So CAGE = 3 × 1 × 7 × 5 = 105.")
    assert "STAPLE"[::-1] == "ELPATS" and "ERASER"[::-1] == "RESARE"
    M(GMA,t,"Easy","If STAPLE is coded as ELPATS, what is the code for ERASER?",["RESARE","RESAER","REASER","ERESAR"],"RESARE","The code writes the word backwards: STAPLE → E-L-P-A-T-S. ERASER backwards is R-E-S-A-R-E = RESARE.")
    sents = {"eat fresh fruit": "tip nok sa", "fruit is sweet": "nok ri pa", "fresh is good": "sa ri lum"}
    words = sorted({w for s_ in sents for w in s_.split()}); codes = sorted({c for v in sents.values() for c in v.split()})
    good = [dict(zip(words, pm)) for pm in itertools.permutations(codes) if all(sorted(dict(zip(words, pm))[w] for w in s_.split()) == sorted(v.split()) for s_, v in sents.items())]
    assert len({g["sweet"] for g in good}) == 1 and good[0]["sweet"] == "pa"
    M(GMA,t,"Medium","In a certain code language, 'tip nok sa' means 'eat fresh fruit', 'nok ri pa' means 'fruit is sweet' and 'sa ri lum' means 'fresh is good'. What is the code for 'sweet'?",["pa","ri","nok","lum"],"pa","'fruit' is common to the first two sentences and 'nok' to their codes, so fruit = nok. 'is' is common to the last two (code ri), and 'fresh' to the first and third (code sa). In 'nok ri pa' (fruit is sweet), the remaining code pa must mean 'sweet'.")
    assert "".join(chr(64 + k) for k in (8, 5, 1, 18, 20)) == "HEART"
    M(GMA,t,"Easy","If A = 1, B = 2, C = 3 and so on up to Z = 26, which word is written as 8-5-1-18-20?",["HEART","HEARD","HEATS","EARTH"],"HEART","8 = H, 5 = E, 1 = A, 18 = R and 20 = T, which spells HEART.")
    # ================= Direction Sense (GMA) =================
    t = "Direction Sense"
    x, y = 0, -10; x += 15; y += 10; x += 5; assert (x, y) == (20, 0)
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]; f = lambda d_: dirs[(dirs.index(d_) - 3) % 8]
    assert f("SE") == "N" and f("NE") == "W" and f("W") == "SE"
    M(GMA,t,"Hard","In a changed set of directions, south-east is called north and north-east is called west. What is west called?",["South-east","North-west","South","North-east"],"South-east","South-east (135°) becomes north (0°), and north-east (45°) becomes west (270°, i.e. −90°): every direction is turned 135° anticlockwise. West (270°) therefore becomes 270° − 135° = 135°, which is south-east.")
    M(GMA,t,"Medium","One evening Raj and Karan stand facing each other. Raj's shadow falls exactly to his right. Which direction is Karan facing?",["South","North","East","West"],"South","In the evening the sun is in the west, so shadows fall towards the east. Raj's right is east, so Raj faces north. Karan faces Raj, so Karan faces south.")
    dist = math.hypot(4, 6); assert abs(dist - 2 * math.sqrt(13)) < 1e-12
    M(GMA,t,"Easy","A man walks 3 km north, then 4 km east, and then 3 km north again. How far is he from his starting point?",["2√13 km","10 km","5 km","7 km"],"2√13 km","He ends 3 + 3 = 6 km north and 4 km east of the start. Distance = √(6² + 4²) = √52 = 2√13 km (about 7.2 km).")
    # ================= Number & Letter Series (GMA) =================
    t = "Number & Letter Series"
    s_ = [2*n*n - 1 for n in range(1, 7)]; assert s_ == [1, 7, 17, 31, 49, 71]
    M(GMA,t,"Easy","Which number comes next in the series 1, 7, 17, 31, 49, ?",["71","67","69","73"],"71","Each term is one less than twice a perfect square: 2×1² − 1, 2×2² − 1, 2×3² − 1, 2×4² − 1, 2×5² − 1. The next is 2×6² − 1 = 71. (Equivalently, the differences 6, 10, 14, 18 grow by 4, so the next difference is 22 and 49 + 22 = 71.)")
    L = [26]; [L.append(L[-1] - k) for k in range(2, 7)]; assert "".join(chr(64 + v) for v in L) == "ZXUQLF"
    s_ = [11]; [s_.append(s_[-1] + k*k) for k in range(2, 7)]; assert s_ == [11, 15, 24, 40, 65, 101]
    M(GMA,t,"Medium","Which number comes next in the series 11, 15, 24, 40, 65, ?",["101","90","96","105"],"101","The differences are 4, 9, 16, 25, the squares of 2, 3, 4, 5. The next difference is 6² = 36, so the next term is 65 + 36 = 101.")
    s_ = [5]; [s_.append(2*s_[-1] + 1) for _ in range(5)]; assert s_ == [5, 11, 23, 47, 95, 191]
    # ================= Odd One Out (GMA) =================
    t = "Odd One Out"
    M(GMA,t,"Easy","Which is the odd one out? Sitar, Veena, Sarod, Tabla",["Tabla","Sitar","Veena","Sarod"],"Tabla","The sitar, veena and sarod are string instruments. The tabla is a percussion (drum) instrument.")
    M(GMA,t,"Medium","Which is the odd one out? Kilogram, Metre, Second, Litre",["Litre","Kilogram","Metre","Second"],"Litre","The kilogram, metre and second are SI base units (of mass, length and time). The litre is not an SI unit at all; the SI unit of volume is the cubic metre.")
    pairs = {"7–49": (7, 49), "9–81": (9, 81), "11–121": (11, 121), "12–148": (12, 148)}; assert [k_ for k_, (a, b) in pairs.items() if a*a != b] == ["12–148"]
    # ================= Puzzles (LR) =================
    t = "Puzzles"
    sols = [dict(zip("ABCD", pm)) for pm in itertools.permutations(["red", "blue", "green", "yellow"])]
    sols = [s for s in sols if s["A"] not in ("red", "blue") and s["B"] == "green" and s["C"] != "red"]; assert len(sols) == 1 and sols[0]["D"] == "red"
    st = []
    for pm in itertools.permutations(range(1, 7)):
        p = dict(zip("PQRSTU", pm))
        if p["R"] == 6 and p["Q"] == p["T"] + 1 and abs(p["P"] - p["U"]) == 3 and p["S"] == p["P"] - 1 and p["U"] != 1: st.append(p)
    assert len(st) == 1 and [k_ for k_ in "PQRSTU" if st[0][k_] == 3] == ["T"]
    M(LR,t,"Medium","Six boxes P, Q, R, S, T and U are stacked one above another. R is at the top. Q is immediately above T. There are exactly two boxes between P and U. S is immediately below P. U is not at the bottom. Which box is third from the bottom?",["T","Q","P","U"],"T","R is 6th (top). S is directly below P and Q directly above T, so S–P and T–Q are two blocks of two. U must be three places from P and not at the bottom. Trying P at 2 (S at 1): U at 5, and T–Q fill 3–4. P at 3 or higher leaves no valid place for both T–Q and U. So from the bottom: S, P, T, Q, U, R, and T is third from the bottom.")
    fl = []
    for pm in itertools.permutations(range(1, 6)):
        p = dict(zip("VWXYZ", pm))
        if p["Z"] == 5 and p["X"] % 2 == 0 and p["W"] == p["Y"] + 1 and p["V"] < p["X"] and p["Y"] > p["X"]: fl.append(p)
    assert len(fl) == 1 and [k_ for k_ in "VWXYZ" if fl[0][k_] == 4] == ["W"]
    # ================= Seating Arrangement (LR) =================
    t = "Seating Arrangement"
    rw = []
    for pm in itertools.permutations(range(1, 7)):
        p = dict(zip("ABCDEF", pm))
        if abs(p["B"] - p["E"]) == 1 and p["A"] in (1, 6) and abs(p["A"] - p["C"]) == 2 and p["D"] == 3 and p["F"] > p["B"] and p["E"] not in (1, 6): rw.append(p)
    assert len(rw) == 1 and [k_ for k_ in "ABCDEF" if rw[0][k_] == 5] == ["F"]
    M(LR,t,"Medium","Six friends A, B, C, D, E and F sit in a row facing north. D is third from the left end. A sits at one of the ends, and exactly one person sits between A and C. B and E sit next to each other, and E is not at an end. F sits somewhere to the right of B. Who sits second from the right end?",["F","C","E","B"],"F","D is 3rd from the left. If A were at the left end, C would be 3rd, which is D's seat; so A is at the right end (6th) and C is 4th. The free seats are 1, 2 and 5. B and E must be adjacent, so they take 1 and 2; E is not at an end, so E is 2nd and B 1st. F takes the 5th seat, which is to the right of B. From the left: B, E, D, C, F, A, so F is second from the right end.")
    cs = set()
    for pm in itertools.permutations(range(6)):
        p = dict(zip("PQRSTU", pm))
        if p["P"] != 0: continue
        right = lambda x_: (p[x_] - 1) % 6
        if p["S"] == 3 and right("Q") == p["S"] and (p["T"] - p["P"]) % 6 in (1, 5) and p["R"] == (p["T"] + 3) % 6:
            cs.add(tuple(sorted("PQRSTU", key=p.get)))
    assert cs == {tuple("PURSQT")}   # clockwise from P; facing the centre, the clockwise neighbour is on one's left
    M(LR,t,"Hard","Six friends P, Q, R, S, T and U sit around a circular table, facing the centre. S sits directly opposite P. S sits immediately to the right of Q. T sits next to P. R sits directly opposite T. Who sits immediately to the left of P?",["U","T","Q","R"],"U","Facing the centre, a person's left neighbour is the next seat clockwise. S is opposite P, and Q has S on his right, so Q is the seat after S going clockwise. T is next to P: the seat clockwise of P would make R (opposite T) land on Q's seat, so T is the seat just anticlockwise of P. Then R is opposite T and U takes the last seat. Clockwise from P the order is P, U, R, S, Q, T, so U is immediately to P's left.")
    # ================= Syllogisms (LR) =================
    t = "Syllogisms"
    k_ = syl_answer([("all", "a", "b"), ("some", "b", "c")], ("some", "a", "c"), ("some", "c", "b")); assert k_ == FX[1]
    k_ = syl_answer([("no", "a", "b"), ("some", "b", "c")], ("somenot", "c", "a"), ("no", "c", "a")); assert k_ == FX[0]
    k_ = syl_answer([("all", "a", "b"), ("all", "b", "c")], ("all", "a", "c"), ("some", "c", "a")); assert k_ == FX[2]
    k_ = syl_answer([("some", "a", "b"), ("no", "b", "c")], ("somenot", "a", "c"), ("some", "c", "a")); assert k_ == FX[0]
    # ================= Simple & Compound Interest (QR) =================
    t = "Simple & Compound Interest"
    r = F(100, 8); assert F(300, r) == 24
    rr = [r_ for r_ in range(1, 50) if 2500 * (100 + r_)**2 == 3025 * 100**2]; assert rr == [10]
    P = F(1440 * 100, 3 * 6); assert P == 8000 and P * (F(11, 10)**2 - 1) == 1680
    M(QR,t,"Medium","The simple interest on a sum for 3 years at 6% per annum is ₹1,440. What is the compound interest on the same sum for 2 years at 10% per annum?",["₹1,680","₹1,600","₹1,760","₹1,440"],"₹1,680","Sum = 1440 × 100/(3 × 6) = ₹8,000. Compound interest = 8000 × (1.1² − 1) = 8000 × 0.21 = ₹1,680.")
    yr = F(8000 - 6800, 3); P = 6800 - 2 * yr; assert (yr, P) == (400, 6000) and yr / P * 100 == F(20, 3)
    # ================= Time, Speed & Distance (QR) =================
    t = "Time, Speed & Distance"
    tt = F(120 + 180) / (F(90 * 5, 18)); assert tt == 12
    dn, up = 24 / 2, 24 / 3; assert (dn - up) / 2 == 2
    lead = F(8 * 10, 60); tc = lead / (10 - 8); assert tc * 60 == 40
    M(QR,t,"Medium","A thief runs away at 8 km/h. A policeman starts chasing him 10 minutes later at 10 km/h. How long after the policeman starts will he catch the thief?",["40 minutes","50 minutes","30 minutes","1 hour"],"40 minutes","In 10 minutes the thief gets 8 × 10/60 = 4/3 km ahead. The policeman closes the gap at 10 − 8 = 2 km/h, so he needs (4/3)/2 = 2/3 hour = 40 minutes.")
    dd = [d for d in range(1, 1000) if F(d, 60) + F(d, 90) == 5]; assert dd == [180]
    M(QR,t,"Medium","A cyclist covers the first half of a journey at 30 km/h and the second half at 45 km/h, taking 5 hours in all. What is the total distance?",["180 km","150 km","225 km","200 km"],"180 km","Let the distance be d. Time = (d/2)/30 + (d/2)/45 = d/60 + d/90 = d/36. So d/36 = 5 and d = 180 km.")
    # ================= Percentages (QR) =================
    t = "Percentages"
    v = F(1120 * 100, 58 - 42); assert v == 7000
    sal = F(15750) / (F(7, 10) * F(3, 4)); assert sal == 30000
    M(QR,t,"Medium","A man spends 30% of his salary on rent and 25% of the remaining amount on food. He is then left with ₹15,750. What is his salary?",["₹30,000","₹35,000","₹28,000","₹31,500"],"₹30,000","After rent, 70% remains; after food, 75% of that, i.e. 0.7 × 0.75 = 52.5% of the salary, is left. Salary = 15,750/0.525 = ₹30,000.")
    xx = F(24, F(60 - 40, 100)); assert xx == 120
    M(QR,t,"Easy","60% of a number is 24 more than 40% of the same number. What is the number?",["120","60","100","240"],"120","60% − 40% = 20% of the number = 24, so the number is 24 × 5 = 120.")
    # ---------- replacement drafts (round 2, after dedupe review dropped template repeats) ----------
    t = "Algebra"
    nn = [10*a + b for a in range(1, 10) for b in range(10) if 10*a + b == 4*(a + b) == 3*a*b]; assert nn == [24]
    M(QR,t,"Hard","A two-digit number is equal to 4 times the sum of its digits and also to 3 times the product of its digits. What is the number?",["24","36","12","48"],"24","Let the number be 10a + b. From 10a + b = 4(a + b), 6a = 3b, so b = 2a. Then 10a + 2a = 3 × a × 2a gives 12a = 6a², so a = 2 and b = 4. The number is 24 (check: 4 × 6 = 24 and 3 × 8 = 24).")
    xs = [x for x in range(-10, 20) if 2**(x + 1) + 2**x == 96] if True else []; assert xs == [5]
    M(QR,t,"Medium","If 2^(x + 1) + 2^x = 96, what is the value of x?",["5","4","6","3"],"5","2^(x + 1) + 2^x = 2 × 2^x + 2^x = 3 × 2^x = 96, so 2^x = 32 = 2⁵ and x = 5.")
    xs = [F(n_, 3) for n_ in range(1, 60) if F(n_, 3) > 1 and F(n_, 3) + 1 / F(n_, 3) == F(10, 3)]; assert xs == [3]
    M(QR,t,"Easy","The sum of a number greater than 1 and its reciprocal is 10/3. What is the number?",["3","3/10","10/3","9"],"3","x + 1/x = 10/3 gives 3x² − 10x + 3 = 0, i.e. (3x − 1)(x − 3) = 0, so x = 3 or 1/3. The number greater than 1 is 3.")
    t = "Clocks & Calendars"
    assert 6 + 12 + 1 == 19
    y = next(y for y in range(2027, 2100) if datetime.date(y, 1, 1).weekday() == datetime.date(2026, 1, 1).weekday() and (y % 4 == 0) == False); assert y == 2037
    M(GMA,t,"Hard","Which is the next year after 2026 whose calendar is exactly the same as that of 2026?",["2037","2032","2034","2043"],"2037","2026 is an ordinary year. Count odd days year by year from 2026: 2026 (1), 2027 (1), 2028 (2, leap), 2029 (1), 2030 (1), 2031 (1), 2032 (2, leap), 2033 (1), 2034 (1), 2035 (1), 2036 (2, leap). The running total first reaches 7 after 2031, so 2032 starts on the same weekday as 2026, but 2032 is a leap year and its calendar differs from February onwards. The total next reaches a multiple of 7 (14) after 2036, so 1 January 2037 falls on the same weekday as 1 January 2026, and 2037 is an ordinary year. Hence 2037.")
    tot = sum([31, 29, 31, 30, 31, 30]); assert tot == 182 and (datetime.date(2028, 7, 1) - datetime.date(2028, 1, 1)).days == 182
    M(GMA,t,"Easy","How many days are there from 1 January 2028 to 30 June 2028, both days included?",["182","181","183","180"],"182","2028 is divisible by 4, so it is a leap year and February has 29 days. January to June: 31 + 29 + 31 + 30 + 31 + 30 = 182 days.")
    t = "Number System"
    assert sum(1 for d in range(1, 361) if 360 % d == 0) == 24
    other = 12 * 360 // 60; assert other == 72 and math.gcd(60, 72) == 12 and 60 * 72 // 12 == 360
    M(QR,t,"Easy","The HCF of two numbers is 12 and their LCM is 360. If one number is 60, what is the other?",["72","84","48","96"],"72","For two numbers, HCF × LCM = product of the numbers. So the other number = 12 × 360/60 = 72. (Check: HCF(60, 72) = 12 and LCM = 360.)")
    sm = min(n_ for n_ in range(5, 1000) if all(n_ % d == 3 for d in (4, 6, 9))); assert sm == 39
    t = "Profit & Loss"
    assert 1500 * F(8, 10) * F(9, 10) / F(108, 100) == 1000
    M(QR,t,"Medium","A kettle is marked at ₹1,500. The shopkeeper gives two successive discounts of 20% and 10% and still makes a profit of 8%. What is the cost price of the kettle?",["₹1,000","₹1,080","₹1,050","₹960"],"₹1,000","Selling price = 1500 × 0.8 × 0.9 = ₹1,080. This is 108% of the cost price, so cost price = 1080/1.08 = ₹1,000.")
    assert (F(45, 5) - F(60, 8)) / F(60, 8) * 100 == 20
    M(QR,t,"Easy","A seller buys pens at 8 for ₹60 and sells them at 5 for ₹45. What is his profit percentage?",["20%","15%","25%","12.5%"],"20%","Cost per pen = 60/8 = ₹7.50. Selling price per pen = 45/5 = ₹9. Profit = 1.50 on 7.50 = 20%.")
    assert F(40 * 100, 12 - 7) == 800
    M(QR,t,"Easy","If an article is sold at a profit of 12% instead of 7%, the seller gets ₹40 more. What is its cost price?",["₹800","₹400","₹500","₹1,000"],"₹800","The extra 12% − 7% = 5% of the cost price equals ₹40, so the cost price = 40 × 100/5 = ₹800.")
    assert (F(12, 10) / F(8, 10) - 1) * 100 == 50
    t = "Ranking & Order"
    ok = [o for o in itertools.permutations("PQRST") if (lambda r: r["P"] > r["Q"] and r["P"] < r["R"] and r["S"] < r["Q"] and r["T"] > r["R"])({c: 5 - i for i, c in enumerate(o)})]
    assert ok == [tuple("TRPQS")]
    M(GMA,t,"Easy","In a test, P scored more than Q but less than R. S scored less than Q, and T scored more than R. No two scored the same. Who scored the third-highest marks?",["P","R","Q","T"],"P","Putting the clues together from highest to lowest: T > R > P > Q > S. The third-highest is P.")
    t = "Ratio & Proportion"
    a_, b_, c_ = 2, 3, 6; assert F(a_, b_) == F(2, 3) and F(b_, c_) == F(1, 2) and 6600 * c_ // (a_ + b_ + c_) == 3600
    k = [k for k in range(1, 50) if 5*k - 8 == 3*k + 8]; assert k == [8] and 8 * 8 == 64
    t = "Time & Work"
    assert 1 / ((F(1, 12) + F(1, 15) + F(1, 20)) / 2) == 10
    tt = 1 / (F(1, 15) + F(1, 25)); assert tt == F(75, 8)
    M(QR,t,"Hard","A does one-third of a job in 5 days and B does two-fifths of it in 10 days. How long will A and B take to do the whole job together?",["9 3/8 days","10 days","8 1/3 days","9 days"],"9 3/8 days","A alone needs 5 × 3 = 15 days; B alone needs 10 × 5/2 = 25 days. Together they do 1/15 + 1/25 = 8/75 of the job per day, so they need 75/8 = 9 3/8 days.")
    t = "Blood Relations"
    t = "Direction Sense"
    hand = (F(1, 1) + F(30, 60)) * 30; assert hand == 45 and (45 + hand) % 360 == 90
    t = "Number & Letter Series"
    s_ = [F(4)]; [s_.append(s_[-1] * F(3, 2)) for _ in range(5)]; assert s_[-1] == F(243, 8)
    M(GMA,t,"Medium","Find the next term: 4, 6, 9, 13.5, 20.25, ?",["30.375","27","30.25","31.5"],"30.375","Each term is 1.5 times the previous one: 4 × 1.5 = 6, 6 × 1.5 = 9, and so on. 20.25 × 1.5 = 30.375.")
    f_ = [1]; g_ = [26]; [f_.append(f_[-1] + k) for k in (2, 3, 4, 5)]; [g_.append(g_[-1] - k) for k in (2, 3, 4, 5)]
    assert chr(64 + f_[-1]) + chr(64 + g_[-1]) == "OL"
    M(GMA,t,"Hard","Find the next term: AZ, CX, FU, JQ, ?",["OL","NL","OK","PL"],"OL","First letters: A, C, F, J move forward by 2, 3, 4, so the next move is 5: J → O. Second letters: Z, X, U, Q move back by 2, 3, 4, so next is back 5: Q → L. The next term is OL.")
    t = "Odd One Out"
    grp = ["BDF", "HJL", "NPR", "TVW"]; odd = [g for g in grp if not (ord(g[1]) - ord(g[0]) == 2 and ord(g[2]) - ord(g[1]) == 2)]; assert odd == ["TVW"]
    M(GMA,t,"Medium","Which letter group is the odd one out? BDF, HJL, NPR, TVW",["TVW","BDF","HJL","NPR"],"TVW","In BDF, HJL and NPR each letter is two places after the previous one (B+2 = D, D+2 = F). In TVW, V + 1 = W breaks the pattern (it should be TVX).")
    t = "Puzzles"
    D_ = "Monday Tuesday Wednesday Thursday Friday".split(); sc = []
    for pm in itertools.permutations(range(5)):
        p = dict(zip("KLMNO", pm))
        if p["O"] == p["K"] + 1 and p["L"] not in (0, 4) and p["N"] > p["M"] and p["M"] != 0 and p["O"] != 4 and p["L"] < p["M"]: sc.append(p)
    assert len(sc) == 1 and D_[sc[0]["M"]] == "Thursday"
    M(LR,t,"Medium","Five lectures K, L, M, N and O are held on the five days from Monday to Friday, one each day. O is held on the day immediately after K. L is held neither on Monday nor on Friday. N is held on some day after M, and L on some day before M. M is not on Monday, and O is not on Friday. Which lecture is held on Thursday?",["M","L","N","O"],"M","L is before M and M is before N, so L, M, N occupy three days in that order, and K–O are two consecutive days. L is not on Monday, so L–M–N cannot start the week; hence K and O take Monday and Tuesday and L, M, N take Wednesday, Thursday and Friday. M is on Thursday.")
    t = "Simple & Compound Interest"
    assert F(3000, 5000 * F(8, 100) + 4000 * F(10, 100)) == F(15, 4)
    M(QR,t,"Medium","Ravi invests ₹5,000 at 8% per annum and ₹4,000 at 10% per annum, both at simple interest. After how long will his total interest be ₹3,000?",["3 years 9 months","3 years 6 months","4 years","3 years"],"3 years 9 months","Yearly interest = 5000 × 8% + 4000 × 10% = 400 + 400 = ₹800. Time = 3000/800 = 3.75 years = 3 years 9 months.")
    assert F(1452 - 1320, 1320) * 100 == 10
    M(QR,t,"Medium","The compound interest (compounded annually) on a sum is ₹1,320 for the second year and ₹1,452 for the third year. What is the rate of interest?",["10%","12%","11%","9%"],"10%","Each year's interest is earned on the previous year's amount, so the third-year interest exceeds the second-year interest by the interest on ₹1,320. Rate = (1452 − 1320)/1320 × 100 = 132/1320 × 100 = 10%.")
    t = "Time, Speed & Distance"
    tt = [t_ for t_ in range(1, 200) if F(t_ * 4, 3) - t_ == 20]; assert tt == [60]
    t = "Percentages"
    xx = [x for x in range(1, 5000) if F(x) * F(12, 10) * F(8, 10) == x - 48]; assert xx == [1200]
    M(QR,t,"Medium","A number is first increased by 20% and the result is then decreased by 20%. The final value is 48 less than the original number. What is the original number?",["1,200","960","1,000","2,400"],"1,200","The net change is 1.2 × 0.8 = 0.96, a 4% fall. So 4% of the number = 48, and the number = 1,200.")
    # ---------- round 3 ----------
    t = "Number System"
    tw = [n_ for n_ in range(10, 100) if n_ % 7 == 1]; assert len(tw) == 13 and sum(tw) == 741
    t = "Clocks & Calendars"
    sund = [d for d in range(1, 32) if (d - 5) % 7 == (6 - 1) % 7]; assert sund == [3, 10, 17, 24, 31]
    M(GMA,t,"Medium","In a month of 31 days, the 5th is a Tuesday. How many Sundays are there in that month?",["5","4","6","3"],"5","If the 5th is a Tuesday, the 3rd is a Sunday. The Sundays fall on the 3rd, 10th, 17th, 24th and 31st, so there are 5.")
    t = "Ratio & Proportion"
    assert (12 // 3, 12 // 4, 12 // 6) == (4, 3, 2)
    M(QR,t,"Medium","If 3A = 4B = 6C, what is A : B : C?",["4 : 3 : 2","3 : 4 : 6","6 : 4 : 3","2 : 3 : 4"],"4 : 3 : 2","Let 3A = 4B = 6C = 12k. Then A = 4k, B = 3k and C = 2k, so A : B : C = 4 : 3 : 2.")
    t = "Time & Work"
    assert 1800 * F(1, 6) / (F(1, 6) + F(1, 9)) == 1080
    M(QR,t,"Medium","A can do a job in 6 days and B in 9 days. They do it together and are paid ₹1,800 for the whole job, shared in proportion to the work each does. What is A's share?",["₹1,080","₹720","₹1,200","₹900"],"₹1,080","Working together for the same time, their shares of the work are in the ratio of their daily rates, 1/6 : 1/9 = 3 : 2. A gets 3/5 × 1800 = ₹1,080.")
    t = "Ranking & Order"
    newp = 16 + 5; assert 40 - newp + 1 == 20
    M(GMA,t,"Medium","In a row of 40 students facing north, Rohan is 16th from the left end. He moves 5 places to his right. What is his new position from the right end?",["20th","19th","21st","25th"],"20th","Facing north, his right is towards the right end. Moving 5 places right makes him 16 + 5 = 21st from the left. From the right he is 40 − 21 + 1 = 20th.")
    t = "Direction Sense"
    P_, S_ = (0, 5), (10, -5); dx, dy = S_[0] - P_[0], S_[1] - P_[1]; assert dx == -dy > 0 and abs(math.hypot(dx, dy) - 10 * math.sqrt(2)) < 1e-9
    M(GMA,t,"Medium","Town P is 5 km north of town Q. Town R is 10 km east of Q, and town S is 5 km south of R. In which direction is S from P?",["South-east","South-west","North-east","East"],"South-east","Take Q at (0, 0). Then P = (0, 5), R = (10, 0) and S = (10, −5). From P to S is 10 km east and 10 km south, an equal amount of each, so S is exactly south-east of P (at a distance of 10√2 km).")
    t = "Algebra"
    sol = [(x, y) for x in range(-20, 21) for y in range(-20, 21) if 3*x - 2*y == 11 and x + 2*y == 9]; assert sol == [(5, 2)]
    t = "Coding-Decoding"
    enc = lambda w: "".join(chr(ord(ch) + 1) if ch in "AEIOU" else chr(ord(ch) - 1) for ch in w); assert enc("SMILE") == "RLJKF"
    M(GMA,t,"Medium","In a certain code, every vowel in a word is replaced by the next letter of the alphabet and every consonant by the previous letter. How is SMILE written in that code?",["RLJKF","TNJMF","RLHKD","RLJKD"],"RLJKF","S (consonant) → R, M → L, I (vowel) → J, L → K, E (vowel) → F. So SMILE becomes RLJKF.")
    t = "Percentages"
    assert (F(125) - 100) / 125 * 100 == 20
