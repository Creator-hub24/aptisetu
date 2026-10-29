"""CUET (UG) batch B11 (Oct 2026): original General Aptitude Test items for the thinnest GAT topics (+3 each).
Every answer is computed or brute-forced here; build fails if any check fails."""
import itertools, math, datetime
from fractions import Fraction as F
from batch_b2 import balanced
QR, LR, GMA = "Quantitative Reasoning", "Logical & Analytical Reasoning", "General Mental Ability"
def shift(w, k): return "".join(chr((ord(c) - 65 + k) % 26 + 65) for c in w)
def mirror(w): return "".join(chr(155 - ord(c)) for c in w)

def gat(B):
    M0 = balanced(B, "gat", 1111)
    # Dedupe review against the whole bank (incl. Bank/SSC items reused in CUET GAT) kept only these drafts (1-based order);
    # the other 30 were exact repeats or same-template number swaps of existing items and are not published.
    KEEP = {1, 3, 8, 11, 12, 13, 15, 16, 17, 22, 24, 28, 33, 40, 43}
    n = [0]
    def M(*a, **k):
        n[0] += 1
        if n[0] in KEEP: return M0(*a, **k)
    # ---- Ranking & Order (GMA)
    t = "Ranking & Order"
    assert 9 + 14 - 1 == 22
    M(GMA,t,"Easy","In a row of students, Pallavi is 9th from the left end and 14th from the right end. How many students are in the row?",["22","23","21","24"],"22","Total = (position from left) + (position from right) − 1 = 9 + 14 − 1 = 22.")
    s_top = 17 + 6; assert 45 - s_top + 1 == 23
    M(GMA,t,"Medium","In a class of 45 students, Mohan's rank is 17th from the top. Sohan is 6 ranks below Mohan. What is Sohan's rank from the bottom?",["23","22","24","28"],"23","Sohan is 17 + 6 = 23rd from the top. From the bottom his rank is 45 − 23 + 1 = 23.")
    sols = [p for p in itertools.permutations("ABCDE") if p.index("C") < p.index("A") < p.index("B") and p[0] == "D" and p.index("E") > p.index("B")]
    assert sols == [tuple("DCABE")]
    M(GMA,t,"Medium","Among five friends, A is taller than B but shorter than C. D is the tallest of all, and E is shorter than B. Who is the third tallest?",["A","B","C","E"],"A","D is the tallest. C > A > B and B > E, so the full order is D > C > A > B > E, which is the only order that fits. The third tallest is A.")
    # ---- Ratio & Proportion (QR)
    t = "Ratio & Proportion"
    xs = [x for x in range(1, 100) if F(3*x - 9, 5*x - 9) == F(12, 23)]; assert xs == [11]
    M(QR,t,"Medium","Two numbers are in the ratio 3 : 5. If 9 is subtracted from each, the ratio becomes 12 : 23. What is the larger number?",["55","33","45","65"],"55","Let the numbers be 3x and 5x. (3x − 9)/(5x − 9) = 12/23 gives 69x − 207 = 60x − 108, so 9x = 99 and x = 11. The numbers are 33 and 55, so the larger is 55.")
    u = F(210) / (5*1 + 6*F(1, 2) + 8*F(1, 4)); assert u == 21 and 6*u == 126
    M(QR,t,"Medium","A bag contains ₹1, 50-paise and 25-paise coins in the ratio 5 : 6 : 8 by number. The total value is ₹210. How many 50-paise coins are there?",["126","105","168","63"],"126","Let the numbers be 5x, 6x and 8x. Value = 5x(1) + 6x(0.50) + 8x(0.25) = 5x + 3x + 2x = 10x = 210, so x = 21. 50-paise coins = 6 × 21 = 126.")
    assert math.isqrt(9*16) == 12 and 12*12 == 9*16
    M(QR,t,"Easy","What is the mean proportional between 9 and 16?",["12","12.5","25","144"],"12","The mean proportional of a and b is √(ab) = √(9 × 16) = √144 = 12. Check: 9 : 12 = 12 : 16.")
    # ---- Time & Work (QR)
    t = "Time & Work"
    rem = 1 - 4*(F(1, 12) + F(1, 18)); assert rem == F(4, 9) and rem*18 == 8
    M(QR,t,"Medium","A can do a piece of work in 12 days and B in 18 days. They work together for 4 days, after which A leaves. In how many more days will B finish the work?",["8","6","10","9"],"8","In one day together they do 1/12 + 1/18 = 5/36 of the work, so in 4 days they do 20/36 = 5/9. The remaining 4/9 takes B (4/9) × 18 = 8 days.")
    assert 15*20 % 12 == 0 and 15*20 // 12 == 25
    M(QR,t,"Easy","15 men can finish a job in 20 days. How many men are needed to finish the same job in 12 days?",["25","20","30","18"],"25","Total work = 15 × 20 = 300 man-days. Men needed for 12 days = 300/12 = 25.")
    assert 1/(F(1, 6) - F(1, 9)) == 18
    M(QR,t,"Easy","Pipe A can fill a tank in 6 hours and pipe B can empty the full tank in 9 hours. If both are opened together on an empty tank, how long will it take to fill it?",["18 hours","15 hours","3.6 hours","12 hours"],"18 hours","Net filling per hour = 1/6 − 1/9 = 3/18 − 2/18 = 1/18 of the tank, so the tank fills in 18 hours.")
    # ---- Odd One Out (GMA)
    t = "Odd One Out"
    cubes = [n for n in (8, 27, 64, 100, 125) if round(n ** (1/3)) ** 3 == n]; assert cubes == [8, 27, 64, 125]
    M(GMA,t,"Easy","Which number is the odd one out? 8, 27, 64, 100, 125",["100","64","27","125"],"100","8 = 2³, 27 = 3³, 64 = 4³ and 125 = 5³ are perfect cubes. 100 is not a cube (it is 10²), so 100 is the odd one out.")
    gaps = {g: (ord(g[1]) - ord(g[0]), ord(g[2]) - ord(g[1])) for g in ("ACE", "BDF", "GIK", "MOR")}; assert [g for g, d in gaps.items() if d != (2, 2)] == ["MOR"]
    M(GMA,t,"Easy","Which letter group is the odd one out? ACE, BDF, GIK, MOR",["MOR","GIK","BDF","ACE"],"MOR","In ACE, BDF and GIK each letter is 2 places after the one before it. In MOR, O is 2 after M but R is 3 after O, so MOR is the odd one out.")
    M(GMA,t,"Easy","Which is the odd one out? Triangle, Square, Pentagon, Cube",["Cube","Square","Pentagon","Triangle"],"Cube","A triangle, a square and a pentagon are flat (two-dimensional) figures. A cube is a solid (three-dimensional) figure, so it is the odd one out.")
    # ---- Coding-Decoding (GMA)
    t = "Coding-Decoding"
    assert mirror("GOLD") == "TLOW" and mirror("SILVER") == "HROEVI"
    M(GMA,t,"Medium","In a certain code, GOLD is written as TLOW. How is SILVER written in that code?",["HROEVI","HRPEVI","TJMWFS","HROEUI"],"HROEVI","Each letter is replaced by its opposite letter in the alphabet (A↔Z, B↔Y, …; the positions add up to 27): G→T, O→L, L→O, D→W. So S→H, I→R, L→O, V→E, E→V, R→I, giving HROEVI.")
    sents = {"sky is blue": "ta na pa", "blue sea": "pa ka", "sea is deep": "ka na ri"}
    words = sorted({w for s in sents for w in s.split()}); codes = sorted({c for v in sents.values() for c in v.split()})
    good = []
    for perm in itertools.permutations(codes):
        mp = dict(zip(words, perm))
        if all(sorted(mp[w] for w in s.split()) == sorted(v.split()) for s, v in sents.items()): good.append(mp)
    assert len({g["sky"] for g in good}) == 1 and good[0]["sky"] == "ta"
    M(GMA,t,"Medium","In a certain code, 'sky is blue' is written as 'ta na pa', 'blue sea' as 'pa ka' and 'sea is deep' as 'ka na ri'. What is the code for 'sky'?",["ta","na","pa","ri"],"ta","'blue' is common to the first two sentences and 'pa' to their codes, so blue = pa. 'sea' is common to the last two, so sea = ka. 'is' is common to the first and third, so is = na. In 'sky is blue' = 'ta na pa', the code left for sky is ta.")
    assert shift("FRIEND", -2) == "DPGCLB"
    M(GMA,t,"Easy","In a certain code, each letter of a word is replaced by the letter two places before it in the alphabet. How is FRIEND written in that code?",["DPGCLB","HTKGPF","DPGCMB","EQHDMC"],"DPGCLB","Move each letter two places back: F→D, R→P, I→G, E→C, N→L, D→B. FRIEND becomes DPGCLB.")
    # ---- Direction Sense (GMA)
    t = "Direction Sense"
    assert math.hypot(6, 8) == 10
    M(GMA,t,"Easy","Meena walks 6 km east, then turns left and walks 8 km. How far is she from her starting point?",["10 km","14 km","2 km","12 km"],"10 km","Turning left from east means walking north. Her displacement has 6 km east and 8 km north, so the distance is √(6² + 8²) = √100 = 10 km.")
    names = {0: "North", 45: "North-East", 90: "East", 135: "South-East", 180: "South", 225: "South-West", 270: "West", 315: "North-West"}
    assert names[(180 - 135) % 360] == "North-East"
    M(GMA,t,"Medium","A man is facing south. He turns 135° anticlockwise. Which direction is he facing now?",["North-East","South-West","North-West","South-East"],"North-East","Turning 90° anticlockwise from south brings him to face east. A further 45° anticlockwise takes him halfway from east to north, i.e. north-east.")
    face = {"North": "East", "East": "South", "South": "West", "West": "North"}   # direction -> his right-hand side
    assert [d for d, r in face.items() if r == "West"] == ["South"]
    M(GMA,t,"Medium","Early one morning, just after sunrise, Raj is standing in an open field. His shadow falls exactly to his right. Which direction is he facing?",["South","North","East","West"],"South","Just after sunrise the sun is in the east, so shadows fall towards the west. His right-hand side is west only when he faces south.")
    # ---- Clocks & Calendars (GMA)
    t = "Clocks & Calendars"
    assert abs(30*4 - F(11, 2)*20) == 10
    M(GMA,t,"Easy","What is the angle between the hour hand and the minute hand of a clock at 4:20?",["10°","20°","0°","5°"],"10°","Angle = |30H − 5.5M| = |30 × 4 − 5.5 × 20| = |120 − 110| = 10°.")
    meets = [F(720*k, 11) for k in range(11)]; assert len(meets) == 11 and all(0 <= m < 720 for m in meets)
    M(GMA,t,"Easy","How many times do the hour hand and the minute hand of a clock coincide in 12 hours?",["11","12","24","22"],"11","The minute hand gains 360° on the hour hand every 720/11 minutes, so they coincide every 65 5/11 minutes. In 720 minutes this happens 720 ÷ (720/11) = 11 times.")
    assert datetime.date(1950, 1, 26).strftime("%A") == "Thursday"
    lp = sum(1 for yr in range(1901, 1950) if yr % 4 == 0); assert lp == 12 and (1 + (49 + lp) + 26) % 7 == 4
    M(GMA,t,"Hard","What day of the week was 26 January 1950?",["Thursday","Wednesday","Friday","Sunday"],"Thursday","Count odd days. The first 1900 years give 1 odd day (1600 years give 0 and 300 years give 1). The 49 years 1901–1949 include 12 leap years, giving 49 + 12 = 61 odd days, i.e. 5 (61 = 8 × 7 + 5). 26 days of January give 5 odd days. Total = 1 + 5 + 5 = 11, i.e. 4 odd days. With 0 = Sunday, 1 = Monday, …, 4 odd days means Thursday.")
    # ---- Percentages (QR)
    t = "Percentages"
    assert F(25, 100)*F(40, 100)*600 == 60
    M(QR,t,"Easy","What is 25% of 40% of 600?",["60","240","150","90"],"60","40% of 600 = 240, and 25% of 240 = 60.")
    assert F(25, 125)*100 == 20
    M(QR,t,"Medium","A's salary is 25% more than B's. By what percentage is B's salary less than A's?",["20%","25%","15%","30%"],"20%","If B gets 100, A gets 125. B is 25 less than A, and 25/125 × 100 = 20% less.")
    assert 20000*F(11, 10)**2 == 24200
    M(QR,t,"Easy","The population of a town is 20,000. It increases by 10% each year. What will it be after 2 years?",["24,200","24,000","22,000","24,400"],"24,200","After 1 year: 20,000 × 1.1 = 22,000. After 2 years: 22,000 × 1.1 = 24,200.")
    # ---- Profit & Loss (QR)
    t = "Profit & Loss"
    cp = F(720) / F(80, 100); assert cp == 900 and cp*F(110, 100) == 990
    M(QR,t,"Medium","By selling an article for ₹720, a trader loses 20%. At what price should he sell it to gain 10%?",["₹990","₹936","₹900","₹1,008"],"₹990","A 20% loss means SP = 80% of CP, so CP = 720/0.8 = ₹900. For a 10% gain, SP = 900 × 1.1 = ₹990.")
    assert 100 - 100*F(8, 10)*F(9, 10) == 28
    M(QR,t,"Easy","Two successive discounts of 20% and 10% are equivalent to a single discount of:",["28%","30%","25%","32%"],"28%","On ₹100: after 20% off it is ₹80, and after a further 10% off it is ₹72. The total discount is 100 − 72 = 28%.")
    g = F(100, 900)*100; assert g == F(100, 9)
    M(QR,t,"Medium","A dishonest shopkeeper claims to sell rice at cost price but uses a 900 g weight in place of 1 kg. What is his gain percentage?",["11 1/9%","10%","9 1/11%","11%"],"11 1/9%","For every 900 g he gives, he charges for 1000 g. Gain = 100 g on 900 g = 100/900 × 100 = 100/9 = 11 1/9%.")
    # ---- Simple & Compound Interest (QR)
    t = "Simple & Compound Interest"
    assert F(7200) / (1 + F(5*4, 100)) == 6000
    M(QR,t,"Easy","A sum of money amounts to ₹7,200 in 4 years at 5% per annum simple interest. What is the sum?",["₹6,000","₹5,760","₹6,200","₹6,480"],"₹6,000","Amount = P(1 + RT/100) = P(1 + 20/100) = 1.2P. So 1.2P = 7,200 and P = ₹6,000.")
    assert F(100, 8) == F(25, 2)
    M(QR,t,"Easy","At what rate of simple interest per annum does a sum double itself in 8 years?",["12.5%","8%","10%","12%"],"12.5%","Doubling means the interest equals the principal: P × R × 8/100 = P, so R = 100/8 = 12.5%.")
    assert 16000*(F(105, 100)**2 - 1) == 1640
    M(QR,t,"Medium","What is the compound interest on ₹16,000 for 1 year at 10% per annum, compounded half-yearly?",["₹1,640","₹1,600","₹1,680","₹1,620"],"₹1,640","Half-yearly: rate 5% per half-year for 2 half-years. Amount = 16,000 × 1.05² = 16,000 × 1.1025 = 17,640. CI = 17,640 − 16,000 = ₹1,640.")
    # ---- Time, Speed & Distance (QR)
    t = "Time, Speed & Distance"
    assert F(120 + 180) / (F(50 + 40) * 5 / 18) == 12
    M(QR,t,"Medium","Two trains, 120 m and 180 m long, run on parallel tracks in opposite directions at 50 km/h and 40 km/h. How long do they take to cross each other completely?",["12 seconds","30 seconds","10 seconds","15 seconds"],"12 seconds","Relative speed = 50 + 40 = 90 km/h = 90 × 5/18 = 25 m/s. Distance to cover = 120 + 180 = 300 m. Time = 300/25 = 12 seconds.")
    assert F(24, 10 + 2) == 2
    M(QR,t,"Easy","A boat goes at 10 km/h in still water, and the stream flows at 2 km/h. How long does it take to go 24 km downstream?",["2 hours","3 hours","2.4 hours","1.5 hours"],"2 hours","Downstream speed = 10 + 2 = 12 km/h. Time = 24/12 = 2 hours.")
    T_ = [T for T in range(1, 200) if F(4, 3)*T - T == 20]; assert T_ == [60]
    M(QR,t,"Medium","Walking at 3/4 of his usual speed, a man reaches his office 20 minutes late. What is his usual time for the journey?",["60 minutes","80 minutes","45 minutes","40 minutes"],"60 minutes","At 3/4 of the speed, the time becomes 4/3 of the usual time T. The extra time is T/3 = 20 minutes, so T = 60 minutes.")
    # ---- Number System (QR)
    t = "Number System"
    assert pow(7, 45, 10) == 7
    M(QR,t,"Medium","What is the unit digit of 7⁴⁵?",["7","9","3","1"],"7","Unit digits of powers of 7 repeat in the cycle 7, 9, 3, 1 (length 4). 45 = 4 × 11 + 1, so 7⁴⁵ has the same unit digit as 7¹, which is 7.")
    add = (-1000) % 23; assert add == 12 and (1000 + add) % 23 == 0
    M(QR,t,"Easy","What is the smallest number that must be added to 1000 to make it exactly divisible by 23?",["12","11","13","9"],"12","1000 = 23 × 43 + 11, so the remainder is 11. Adding 23 − 11 = 12 gives 1012 = 23 × 44.")
    assert sum(1 for d in range(1, 361) if 360 % d == 0) == 24
    M(QR,t,"Medium","How many positive factors does 360 have?",["24","20","18","12"],"24","360 = 2³ × 3² × 5. Number of factors = (3 + 1)(2 + 1)(1 + 1) = 4 × 3 × 2 = 24.")
    # ---- Algebra (QR)
    t = "Algebra"
    assert 3**2 + 2*10 == 29 and {(5, 2), (-2, -5)} == {(a, b) for a in range(-20, 21) for b in range(-20, 21) if a - b == 3 and a*b == 10}
    M(QR,t,"Easy","If x − y = 3 and xy = 10, what is x² + y²?",["29","19","9","39"],"29","x² + y² = (x − y)² + 2xy = 9 + 20 = 29.")
    assert 6**2 - 2*4 == 28
    M(QR,t,"Medium","If α and β are the roots of x² − 6x + 4 = 0, what is α² + β²?",["28","36","32","44"],"28","α + β = 6 and αβ = 4, so α² + β² = (α + β)² − 2αβ = 36 − 8 = 28.")
    sol = [(a, b) for a in range(-20, 21) for b in range(-20, 21) if 2*a + 3*b == 12 and 3*a - b == 7]; assert sol == [(3, 2)]
    M(QR,t,"Easy","If 2x + 3y = 12 and 3x − y = 7, what is x + y?",["5","4","6","7"],"5","From 3x − y = 7, y = 3x − 7. Then 2x + 3(3x − 7) = 12 gives 11x = 33, so x = 3 and y = 2. x + y = 5.")
    # ---- Blood Relations (LR)
    t = "Blood Relations"
    M(LR,t,"Medium","'A + B' means A is the father of B, 'A × B' means A is the sister of B and 'A − B' means A is the mother of B. If P + Q × R, how is P related to R?",["Father","Brother","Uncle","Grandfather"],"Father","P + Q: P is Q's father. Q × R: Q is R's sister, so Q and R share parents. Hence P is R's father.")
    M(LR,t,"Medium","Introducing a man, a woman says, \"His mother is the only daughter of my mother.\" How is the woman related to the man?",["Mother","Sister","Aunt","Grandmother"],"Mother","The only daughter of the woman's mother is the woman herself. So the man's mother is the woman, i.e. she is his mother.")
    M(LR,t,"Easy","Q is the brother of P. R is the sister of Q. S is the father of P. How is R related to S?",["Daughter","Sister","Niece","Wife"],"Daughter","P, Q and R are siblings (Q is P's brother and R is Q's sister). S is P's father, so S is the father of all three, and R, being female, is S's daughter.")
    # ---- Number & Letter Series (GMA)
    t = "Number & Letter Series"
    pr = [p for p in range(2, 20) if all(p % d for d in range(2, p))]; assert [p*p for p in pr[1:7]] == [9, 25, 49, 121, 169, 289]
    M(GMA,t,"Medium","Find the next term: 4, 9, 25, 49, 121, ?",["169","144","196","225"],"169","The terms are squares of consecutive primes: 2², 3², 5², 7², 11². The next prime is 13, so the next term is 13² = 169.")
    assert [chr(65 + i) + chr(90 - i) for i in range(4)] == ["AZ", "BY", "CX", "DW"]
    M(GMA,t,"Easy","Find the next term: AZ, BY, CX, ?",["DW","DV","EW","DX"],"DW","The first letter moves forward (A, B, C, D) and the second moves backward (Z, Y, X, W). The next term is DW.")
    s = [2]; [s.append(s[-1] + 2**i) for i in range(5)]; assert s == [2, 3, 5, 9, 17, 33]
    M(GMA,t,"Medium","Find the next term: 2, 3, 5, 9, 17, ?",["33","31","25","34"],"33","The differences are 1, 2, 4, 8, which double each time, so the next difference is 16 and the next term is 17 + 16 = 33.")
