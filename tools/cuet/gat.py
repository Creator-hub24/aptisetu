"""CUET (UG) General Aptitude Test (501): original questions. Answers are computed, puzzles brute-forced."""
import itertools, math, datetime
from fractions import Fraction as F

QR, LR, GMA, GK = "Quantitative Reasoning", "Logical & Analytical Reasoning", "General Mental Ability", "General Knowledge"
FX = ["Only I follows", "Only II follows", "Both I and II follow", "Neither I nor II follows"]
AR = ["Both A and R are true, and R is the correct explanation of A", "Both A and R are true, but R is not the correct explanation of A", "A is true, but R is false", "A is false, but R is true"]
DS = ["Statement I alone is sufficient, but II alone is not", "Statement II alone is sufficient, but I alone is not", "Both statements together are needed; neither alone is sufficient", "Each statement alone is sufficient"]
def rs(x): return f"₹{x:,}"

# ---------- syllogism checker: brute force over all Venn-region models of three non-empty sets ----------
def syl(premises, conclusion):
    """terms are 'a','b','c'. statements: ('all',x,y) ('some',x,y) ('no',x,y) ('somenot',x,y). True iff conclusion holds in every model."""
    regions = [r for r in itertools.product([0, 1], repeat=3) if any(r)]   # membership in (a,b,c)
    idx = {"a": 0, "b": 1, "c": 2}
    def holds(model, s):
        k, x, y = s; X = [r for r in model if r[idx[x]]]; XY = [r for r in X if r[idx[y]]]
        return {"all": len(X) == len(XY), "some": len(XY) > 0, "no": len(XY) == 0, "somenot": len(XY) < len(X)}[k]
    ok = True; seen = False
    for bits in itertools.product([0, 1], repeat=len(regions)):
        model = [r for r, b in zip(regions, bits) if b]
        if not all(any(r[i] for r in model) for i in range(3)): continue      # every term non-empty
        if all(holds(model, p) for p in premises):
            seen = True
            if not holds(model, conclusion): ok = False
    assert seen
    return ok
def syl_answer(prem, c1, c2):
    return FX[{(True, False): 0, (False, True): 1, (True, True): 2, (False, False): 3}[(syl(prem, c1), syl(prem, c2))]]

def build(B):
    M = lambda *a, **k: B.mcq("gat", *a, **k)
    # ======================= QUANTITATIVE REASONING (30) =======================
    p = QR
    t = "Percentages"
    net = (1.2 * 0.8 - 1) * 100
    M(p,t,"Easy","A number is first increased by 20% and then the result is decreased by 20%. What is the net change?",["4% decrease","No change","4% increase","2% decrease"],"4% decrease","Take the number as 100. After +20%: 120. After −20% of 120: 120 − 24 = 96. Net change = 4% decrease.",chk=(net,-4))
    girls, boys = 24, 16; pct = (girls * 0.25 + boys * 0.5) / 40 * 100
    M(p,t,"Medium","In a class of 40 students, 60% are girls. If 25% of the girls and 50% of the boys wear spectacles, what percentage of the class wears spectacles?",["35%","37.5%","30%","40%"],"35%","Girls = 60% of 40 = 24, boys = 16. Spectacles: 25% of 24 = 6 girls and 50% of 16 = 8 boys, so 14 students. 14/40 = 35%.",chk=(pct,35))
    cut = (1 - 1 / 1.25) * 100
    M(p,t,"Medium","The price of sugar rises by 25%. By what percentage must a family reduce its sugar consumption so that its spending on sugar stays the same?",["20%","25%","15%","22.5%"],"20%","Spending = price × quantity. If price becomes 1.25 times, quantity must become 1/1.25 = 0.8 times, a reduction of 20%.",chk=(cut,20))
    t = "Profit & Loss"
    M(p,t,"Easy","A shopkeeper buys an article for ₹480 and sells it for ₹552. What is his profit percentage?",["15%","12%","18%","72%"],"15%","Profit = 552 − 480 = ₹72. Profit % = 72/480 × 100 = 15%.",chk=(72/480*100,15))
    cp = F(800 * 85, 100) / (1 + F(2, 15))
    M(p,t,"Medium","An article is marked at ₹800 and sold at a 15% discount. The seller still makes a profit of 13⅓%. What is the cost price?",[rs(600),rs(640),rs(580),rs(680)],rs(600),"Selling price = 85% of 800 = ₹680. A profit of 13⅓% = 2/15 means SP = CP × 17/15, so CP = 680 × 15/17 = ₹600.",chk=(cp,600))
    M(p,t,"Medium","By selling 12 pens, a seller gains an amount equal to the cost price of 3 pens. What is the gain percentage?",["25%","20%","33⅓%","30%"],"25%","Let one pen cost ₹1. Cost of 12 pens = ₹12 and gain = ₹3. Gain % = 3/12 × 100 = 25%.",chk=(3/12*100,25))
    t = "Ratio & Proportion"
    M(p,t,"Easy","₹3,600 is divided among A, B and C in the ratio 2 : 3 : 4. What is B's share?",[rs(1200),rs(800),rs(1600),rs(900)],rs(1200),"Total parts = 2 + 3 + 4 = 9. One part = 3600/9 = ₹400. B gets 3 parts = ₹1,200.",chk=(3600*3/9,1200))
    xs = [x for x in range(1, 50) if 4 * (5 * x + 6) == 3 * (7 * x + 6)]; assert xs == [6]
    M(p,t,"Medium","The present ages of A and B are in the ratio 5 : 7. After 6 years, the ratio will be 3 : 4. What is A's present age?",["30 years","25 years","35 years","42 years"],"30 years","Let the ages be 5x and 7x. Then (5x + 6)/(7x + 6) = 3/4, so 20x + 24 = 21x + 18 and x = 6. A is 5 × 6 = 30 years old.",chk=(5*xs[0],30))
    t = "Simple & Compound Interest"
    M(p,t,"Easy","What is the simple interest on ₹5,000 at 8% per annum for 3 years?",[rs(1200),rs(1000),rs(1260),rs(400)],rs(1200),"SI = P × R × T / 100 = 5000 × 8 × 3 / 100 = ₹1,200.",chk=(5000*8*3/100,1200))
    ci = 10000 * 1.1 ** 2 - 10000
    M(p,t,"Medium","What is the compound interest on ₹10,000 at 10% per annum for 2 years, compounded annually?",[rs(2100),rs(2000),rs(2210),rs(1100)],rs(2100),"Amount = 10000 × (1.1)² = ₹12,100. CI = 12,100 − 10,000 = ₹2,100.",chk=(ci,2100))
    d = 8000 * 1.05 ** 2 - 8000 - 8000 * 5 * 2 / 100
    M(p,t,"Hard","What is the difference between the compound interest and the simple interest on ₹8,000 for 2 years at 5% per annum (compounded annually)?",[rs(20),rs(40),rs(10),rs(80)],rs(20),"For 2 years, CI − SI = P × (R/100)² = 8000 × (0.05)² = ₹20. Check: CI = 8000 × 1.1025 − 8000 = ₹820; SI = ₹800; difference ₹20.",chk=(d,20))
    t = "Averages"
    M(p,t,"Easy","The average of five numbers is 18. When one number is removed, the average of the remaining four is 16. Which number was removed?",["26","2","18","34"],"26","Sum of five = 5 × 18 = 90. Sum of four = 4 × 16 = 64. Removed number = 90 − 64 = 26.",chk=(90-64,26))
    tw = 31 * 40.5 - 30 * 40
    M(p,t,"Medium","The average weight of 30 students is 40 kg. When the teacher's weight is included, the average rises by 0.5 kg. What is the teacher's weight?",["55.5 kg","40.5 kg","45 kg","70.5 kg"],"55.5 kg","Total of 30 students = 1200 kg. New total of 31 people = 31 × 40.5 = 1255.5 kg. Teacher = 1255.5 − 1200 = 55.5 kg.",chk=(tw,55.5))
    t = "Time, Speed & Distance"
    M(p,t,"Easy","A speed of 72 km/h is equal to:",["20 m/s","25 m/s","72 m/s","12 m/s"],"20 m/s","Multiply km/h by 5/18 to get m/s: 72 × 5/18 = 20 m/s.",chk=(72*5/18,20))
    M(p,t,"Medium","A 150 m long train passes a pole in 10 seconds. How long will it take to cross a 300 m long platform at the same speed?",["30 s","20 s","25 s","45 s"],"30 s","Speed = 150/10 = 15 m/s. To cross a platform the train covers its own length plus the platform: 150 + 300 = 450 m. Time = 450/15 = 30 s.",chk=(450/15,30))
    M(p,t,"Medium","A car goes from town A to town B at 60 km/h and returns along the same road at 40 km/h. What is its average speed for the whole journey?",["48 km/h","50 km/h","45 km/h","52 km/h"],"48 km/h","For equal distances, average speed = 2ab/(a + b) = 2 × 60 × 40 / 100 = 48 km/h. (Check with 120 km each way: 2 h + 3 h = 5 h for 240 km.)",chk=(2*60*40/100,48))
    t = "Time & Work"
    M(p,t,"Easy","A can finish a piece of work in 10 days and B in 15 days. Working together, in how many days will they finish it?",["6 days","12.5 days","5 days","8 days"],"6 days","Together they do 1/10 + 1/15 = 3/30 + 2/30 = 1/6 of the work per day, so they need 6 days.",chk=(1/(F(1,10)+F(1,15)),6))
    M(p,t,"Medium","A and B together can finish a job in 12 days. A alone can finish it in 20 days. How long would B alone take?",["30 days","8 days","32 days","24 days"],"30 days","B's rate = 1/12 − 1/20 = 5/60 − 3/60 = 2/60 = 1/30, so B alone takes 30 days.",chk=(1/(F(1,12)-F(1,20)),30))
    t = "Number System"
    M(p,t,"Easy","What is the LCM of 12, 18 and 30?",["180","90","360","6"],"180","12 = 2²·3, 18 = 2·3², 30 = 2·3·5. LCM = 2²·3²·5 = 180.",chk=(math.lcm(12,18,30),180))
    sm = min(n for n in range(5, 1000) if all(n % d == 4 for d in (6, 8, 12)))
    M(p,t,"Medium","What is the smallest number that leaves a remainder of 4 when divided by 6, by 8 and by 12?",["28","24","52","20"],"28","The number is (a multiple of LCM(6, 8, 12)) + 4. LCM = 24, so the smallest such number is 24 + 4 = 28.",chk=(sm,28))
    M(p,t,"Medium","The HCF of two numbers is 12 and their product is 2,160. What is their LCM?",["180","120","216","2,148"],"180","For two numbers, HCF × LCM = product. LCM = 2160/12 = 180.",chk=(2160/12,180))
    t = "Algebra"
    M(p,t,"Easy","If 3x − 7 = 2x + 5, what is x?",["12","−2","2","−12"],"12","Subtract 2x from both sides: x − 7 = 5, so x = 12.",chk=(12*3-7,12*2+5))
    x = (5 + math.sqrt(21)) / 2
    M(p,t,"Medium","If x + 1/x = 5, what is the value of x² + 1/x²?",["23","25","27","21"],"23","Square both sides: x² + 2 + 1/x² = 25, so x² + 1/x² = 23.",chk=(x*x+1/(x*x),23))
    roots = sorted(r for r in (F(1, 2), 3, -3, F(-1, 2), 6, 1) if 2 * r * r - 7 * r + 3 == 0); assert roots == [F(1, 2), 3]
    M(p,t,"Medium","What are the roots of 2x² − 7x + 3 = 0?",["3 and 1/2","−3 and −1/2","3 and −1/2","6 and 1"],"3 and 1/2","Factorise: 2x² − 6x − x + 3 = 2x(x − 3) − 1(x − 3) = (2x − 1)(x − 3). So x = 1/2 or x = 3.")
    t = "Geometry"
    M(p,t,"Easy","The angles of a triangle are in the ratio 2 : 3 : 4. What is the largest angle?",["80°","60°","90°","100°"],"80°","The angles add up to 180°. 2 + 3 + 4 = 9 parts, so one part = 20°. The largest angle = 4 × 20° = 80°.",chk=(180*4/9,80))
    M(p,t,"Medium","A point P is 13 cm from the centre of a circle of radius 5 cm. What is the length of the tangent drawn from P to the circle?",["12 cm","8 cm","18 cm","√194 cm"],"12 cm","The radius is perpendicular to the tangent at the point of contact, so tangent² = 13² − 5² = 169 − 25 = 144. Tangent = 12 cm.",chk=(math.sqrt(13**2-5**2),12))
    t = "Mensuration"
    M(p,t,"Easy","A rectangular field measures 40 m by 25 m. What does it cost to fence it at ₹12 per metre?",[rs(1560),rs(12000),rs(780),rs(1300)],rs(1560),"Perimeter = 2 × (40 + 25) = 130 m. Cost = 130 × 12 = ₹1,560.",chk=(2*(40+25)*12,1560))
    M(p,t,"Medium","What is the volume of a cylinder of radius 7 cm and height 10 cm? (Use π = 22/7.)",["1,540 cm³","440 cm³","3,080 cm³","154 cm³"],"1,540 cm³","V = πr²h = 22/7 × 49 × 10 = 22 × 7 × 10 = 1,540 cm³.",chk=(F(22,7)*49*10,1540))
    t = "Statistics"
    data = [7, 3, 9, 5, 11, 3, 8]; med = sorted(data)[3]
    M(p,t,"Easy","What is the median of 7, 3, 9, 5, 11, 3, 8?",["7","5","6.57","8"],"7","Arrange in order: 3, 3, 5, 7, 8, 9, 11. There are 7 values, so the median is the 4th: 7. (6.57 is the mean, rounded.)",chk=(med,7))
    d2 = [2, 4, 4, 5, 7, 7, 7, 9]; mode = max(set(d2), key=d2.count); med2 = (d2[3] + d2[4]) / 2
    M(p,t,"Medium","For the data 2, 4, 4, 5, 7, 7, 7, 9, what are the mode and the median?",["Mode 7, median 6","Mode 4, median 6","Mode 7, median 5","Mode 7, median 7"],"Mode 7, median 6","7 occurs most often (three times), so the mode is 7. There are 8 values, so the median is the average of the 4th and 5th: (5 + 7)/2 = 6.",chk=[(mode,7),(med2,6)])

    # ======================= LOGICAL & ANALYTICAL REASONING (30) =======================
    p = LR
    t = "Syllogisms"
    def SYQ(diff, s1, s2, c1, c2, prem, k1, k2, sol):
        ans = syl_answer(prem, k1, k2)
        M(p,t,diff,f"Statements: {s1} {s2}<br>Conclusions: I. {c1} II. {c2}",FX,ans,sol,fixed=True)
        return ans
    a = SYQ("Easy","All pens are books.","Some books are copies.","Some pens are copies.","Some copies are books.",
        [("all","a","b"),("some","b","c")],("some","a","c"),("some","c","b"),
        "II is just 'Some books are copies' read the other way round, so it follows. I need not follow: the books that are copies may all be books that are not pens. Only II follows.")
    assert a == FX[1]
    a = SYQ("Medium","No cat is a dog.","All dogs are animals.","Some animals are not cats.","No animal is a cat.",
        [("no","a","b"),("all","b","c")],("somenot","c","a"),("no","c","a"),
        "Every dog is an animal and no dog is a cat, so those animals (the dogs) are not cats: I follows. II need not follow, since cats could also be animals. Only I follows.")
    assert a == FX[0]
    a = SYQ("Easy","Some flowers are red.","All red things are bright.","Some flowers are bright.","All bright things are flowers.",
        [("some","a","b"),("all","b","c")],("some","a","c"),("all","c","a"),
        "The red flowers are bright, so some flowers are bright: I follows. Nothing says that every bright thing is a flower, so II does not follow. Only I follows.")
    assert a == FX[0]
    a = SYQ("Medium","All teachers are graduates.","No graduate is lazy.","No teacher is lazy.","Some graduates are teachers.",
        [("all","a","b"),("no","b","c")],("no","a","c"),("some","b","a"),
        "Every teacher is a graduate and no graduate is lazy, so no teacher is lazy: I follows. Since all teachers are graduates (and teachers exist), some graduates are teachers: II follows. Both follow.")
    assert a == FX[2]
    t = "Statements & Conclusions"
    M(p,t,"Medium","Statement: Most of the increase in the city's metro ridership last year came from passengers on the newly opened airport line.<br>Conclusions: I. The new airport line contributed to the rise in metro ridership. II. Road traffic in the city fell by half last year.",FX,FX[0],"I restates the statement: most of the increase came from the new line, so it contributed. II is about road traffic, which the statement does not mention. Only I follows.",fixed=True)
    M(p,t,"Medium","Statement: All candidates must carry a valid photo identity card; candidates without one will not be allowed into the examination hall.<br>Conclusions: I. Any candidate carrying a valid photo identity card will certainly be allowed in. II. A candidate without a valid photo identity card will not be allowed in.",FX,FX[1],"II is stated directly. I does not follow: the ID card is a necessary condition, not a guarantee. A candidate could still be refused for another reason, such as arriving late. Only II follows.",fixed=True)
    M(p,t,"Easy","Statement: In a survey of 200 students of a school, 150 said that they prefer online classes.<br>Conclusions: I. Most of the students surveyed prefer online classes. II. All schools should shift to online classes.",FX,FX[0],"150 out of 200 is 75%, so I follows. II is a sweeping recommendation for all schools based on one school's survey, so it does not follow. Only I follows.",fixed=True)
    t = "Statements & Assumptions"
    AS = ["Only assumption I is implicit", "Only assumption II is implicit", "Both I and II are implicit", "Neither I nor II is implicit"]
    M(p,t,"Medium","Statement: \"Book your train tickets in under a minute with our new app,\" says an advertisement.<br>Assumptions: I. People would like to book tickets quickly. II. Some people have access to a phone or computer that can run the app.",AS,AS[2],"The advertisement only makes sense if speed is something people value (I), and if at least some people can use the app (II). Both are implicit.",fixed=True)
    M(p,t,"Medium","Statement: The school has introduced a library period every Friday so that students read more.<br>Assumptions: I. Time set aside for reading at school can encourage students to read more. II. Students do not read at all at home.",AS,AS[0],"The decision assumes that a library period will help (I). It does not need to assume that students never read at home; the school may simply want them to read more. Only I is implicit.",fixed=True)
    t = "Assertion & Reason"
    M(p,t,"Easy","Assertion (A): Ice floats on water.<br>Reason (R): Ice is less dense than liquid water.",AR,AR[0],"Both statements are true. Objects less dense than water float, so the lower density of ice explains why it floats.",fixed=True)
    M(p,t,"Medium","Assertion (A): Metals are generally good conductors of electricity.<br>Reason (R): All metals are liquid at room temperature.",AR,AR[2],"A is true. R is false: mercury is the well-known liquid metal, but most metals, such as iron, copper and aluminium, are solid at room temperature.",fixed=True)
    M(p,t,"Medium","Assertion (A): Sound can travel through a vacuum.<br>Reason (R): Sound needs a material medium, such as air or water, to travel.",AR,AR[3],"Sound is a mechanical wave that needs a medium, so R is true and A is false. Sound cannot travel through a vacuum.",fixed=True)
    M(p,t,"Hard","Assertion (A): Mount Everest is the highest mountain above sea level.<br>Reason (R): Mount Everest lies in the Himalayas.",AR,AR[1],"Both statements are true. But lying in the Himalayas does not explain why Everest is the highest, since many lower peaks are also in the Himalayas. So R is not the correct explanation of A.",fixed=True)
    t = "Seating Arrangement"
    P5 = "PQRST"; sols = []
    for o in itertools.permutations(P5):
        pos = {x: i + 1 for i, x in enumerate(o)}
        if pos["S"] == 3 and pos["P"] == pos["S"] + 1 and pos["Q"] not in (1, 5) and pos["T"] < pos["R"]: sols.append(o)
    assert len(sols) == 1; row = sols[0]
    M(p,t,"Easy","Five friends P, Q, R, S and T sit in a row facing north. S sits in the middle. P sits immediately to the right of S. Q does not sit at either end. T sits somewhere to the left of R. Who sits at the extreme right end?",list("RTQP"),row[-1],f"S is 3rd and P is 4th. Q can't be at an end, so Q is 2nd. T and R take positions 1 and 5, and T is to the left of R, so T is 1st and R is 5th. Order: {' '.join(row)}. R is at the extreme right.")
    # circular set: positions 0..5 clockwise (seen from above); facing the centre, a person's LEFT neighbour is the next seat clockwise
    PE = "ABCDEF"; csol = []
    for o in itertools.permutations("BCDEF"):
        seat = {"A": 0, **{x: i + 1 for i, x in enumerate(o)}}
        L = lambda x: (seat[x] + 1) % 6; R_ = lambda x: (seat[x] - 1) % 6
        nb = lambda x, y: (seat[x] - seat[y]) % 6 in (1, 5)
        if (seat["D"] - seat["A"]) % 6 != 3: continue
        if L("A") != seat["B"]: continue
        if R_("D") != seat["E"]: continue
        if not (nb("F", "A") and nb("F", "C")): continue
        csol.append(seat)
    assert len(csol) == 1; s = csol[0]; who = {v: k for k, v in s.items()}
    B.add_set("cu-circle", "lr", "Round table", "<b>Round table</b><p>Six friends A, B, C, D, E and F sit around a circular table, facing the centre.</p><ul class='clues'><li>A sits directly opposite D.</li><li>B sits immediately to the left of A.</li><li>E sits immediately to the right of D.</li><li>F sits between A and C.</li></ul>")
    base = ("Going round the table so that each person's left-hand neighbour comes next: A, B, E, D, C, F. "
            "Place A first; D is opposite A. B is A's immediate left and E is D's immediate right. That leaves two seats, both next to each other, between D and A. "
            "F must be next to A and to C, so F takes the seat beside A and C the seat beside D. ")
    opp = lambda x: who[(s[x] + 3) % 6]
    M(p,t,"Medium","Who sits directly opposite B?",["C","E","F","D"],opp("B"),base + "Opposite B is C.",set_id="cu-circle")
    M(p,t,"Medium","Who sits immediately to the right of B?",["A","E","C","F"],who[(s["B"] - 1) % 6],base + "B's immediate right is A (B is A's immediate left).",set_id="cu-circle")
    pairs = {"E and F": ("E", "F"), "B and E": ("B", "E"), "A and C": ("A", "C"), "C and E": ("C", "E")}
    ok = [k for k, (x, y) in pairs.items() if opp(x) == y]; assert len(ok) == 1
    M(p,t,"Medium","Which of the following pairs sit directly opposite each other?",list(pairs),ok[0],base + "The opposite pairs are A–D, B–C and E–F.",set_id="cu-circle")
    nbE = sorted(who[(s["E"] + d) % 6] for d in (1, 5))
    M(p,t,"Easy","Who are E's two neighbours?",["B and D","A and D","B and C","D and F"]," and ".join(nbE),base + "E sits between B and D.",set_id="cu-circle")
    t = "Blood Relations"
    M(p,t,"Medium","Pointing to a boy, Riya says, \"He is the son of the only son of my grandfather.\" Riya's grandfather is her father's father. How is the boy related to Riya?",["Brother","Cousin","Nephew","Uncle"],"Brother","Riya's grandfather is her father's father, and his only son must be Riya's father. The boy is her father's son, so he is Riya's brother.")
    M(p,t,"Easy","A is B's sister. C is B's mother. D is C's father. How is A related to D?",["Granddaughter","Daughter","Niece","Sister"],"Granddaughter","A is B's sister, so C is also A's mother. D is C's father, so D is A's grandfather, and A is D's granddaughter.")
    M(p,t,"Medium","X is the husband of Y. Y is the daughter of Z. W is Z's only son. How is W related to X?",["Brother-in-law","Father-in-law","Brother","Son-in-law"],"Brother-in-law","Y is Z's daughter and W is Z's son, so W is Y's brother. W is the brother of X's wife, so W is X's brother-in-law.")
    t = "Puzzles"
    hs = [o for o in itertools.permutations("ABCDE") if o.index("A") < o.index("B") and o.index("C") < o.index("A") and o.index("D") < o.index("C") and o[-1] == "E"]  # tallest first
    assert len(hs) == 1; h = hs[0]
    hb = "A is taller than B but shorter than C, and D is taller than C, so D > C > A > B. E is the shortest. Order, tallest first: " + " > ".join(h) + ". "
    M(p,t,"Easy","Among five friends A, B, C, D and E: A is taller than B but shorter than C. D is taller than C. E is the shortest. Who is the tallest?",["D","C","A","Cannot be determined"],h[0],hb + "D is the tallest.",fixed=True)
    M(p,t,"Medium","Among five friends A, B, C, D and E: A is taller than B but shorter than C. D is taller than C. E is the shortest. Who is the second shortest?",["B","A","E","C"],h[-2],hb + "The second shortest is B.")
    st = [o for o in itertools.permutations("PQRST") if o[0] == "R" and o.index("Q") == o.index("P") + 1 and o.index("S") < o.index("T") < o.index("P")]  # bottom first
    assert len(st) == 1
    M(p,t,"Medium","Five books P, Q, R, S and T are stacked one on top of another. R is at the bottom. Q is directly above P. T is above S but below P. Which book is at the top?",["Q","P","T","S"],st[0][-1],"R is at position 1 (bottom). Of the remaining four books, S is below T and T is below P, and Q sits directly on P. So from the bottom: R, S, T, P, Q. Q is at the top.")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]; ds = []
    for o in itertools.permutations(["Maths", "Physics", "Chemistry", "Biology", "English"]):
        d = {x: i for i, x in enumerate(o)}
        if d["Chemistry"] == 2 and d["Physics"] == d["Maths"] + 1 and d["English"] not in (0, 4) and d["Biology"] > d["Physics"]: ds.append(d)
    assert len(ds) == 1
    M(p,t,"Hard","Five lectures (Maths, Physics, Chemistry, Biology and English) are held one per day from Monday to Friday. Chemistry is on Wednesday. Maths is on the day just before Physics. English is not on Monday or Friday. Biology is on some day after Physics. On which day is English?",["Thursday","Tuesday","Monday","Friday"],days[ds[0]["English"]],"English must be on Tuesday or Thursday. If English is on Tuesday, Maths and Physics need two consecutive free days from Monday, Thursday and Friday, which means Thursday and Friday. That leaves no day after Physics for Biology. So English is on Thursday, with Maths on Monday, Physics on Tuesday and Biology on Friday.")
    t = "Venn Diagrams"
    M(p,t,"Easy","In a group of 60 people, 35 like tea, 30 like coffee and 10 like both. How many like neither?",["5","15","25","0"],"5","People who like at least one = 35 + 30 − 10 = 55. Neither = 60 − 55 = 5.",chk=(60-(35+30-10),5))
    M(p,t,"Medium","Of 100 students, 45 play cricket, 40 play football and 25 play neither. How many play both?",["10","15","5","20"],"10","At least one game = 100 − 25 = 75. Both = 45 + 40 − 75 = 10.",chk=(45+40-(100-25),10))
    t = "Data Sufficiency"
    s1 = [x for x in range(-20, 21) if 2 * x + 3 == 11]; s2 = [x for x in range(-20, 21) if x * x == 16]; assert s1 == [4] and s2 == [-4, 4]
    M(p,t,"Medium","Question: What is the value of x?<br>Statement I: 2x + 3 = 11.<br>Statement II: x² = 16.",DS,DS[0],"I gives x = 4 exactly. II gives x = 4 or x = −4, which is not a unique value. So I alone is sufficient, but II alone is not.",fixed=True)
    e1 = all(n % 2 == 0 for n in range(-40, 41) if n % 4 == 0); e2 = all(n % 2 == 0 for n in range(-40, 41) if (n + 1) % 2 == 1); assert e1 and e2
    M(p,t,"Medium","Question: Is the integer n even?<br>Statement I: n is a multiple of 4.<br>Statement II: n + 1 is odd.",DS,DS[3],"I: every multiple of 4 is even, so the answer is yes. II: if n + 1 is odd, then n is even, so again yes. Each statement alone is sufficient.",fixed=True)
    M(p,t,"Medium","Question: What is the area of a rectangle?<br>Statement I: Its length is 8 cm.<br>Statement II: Its perimeter is 28 cm.",DS,DS[2],"Neither statement alone fixes both sides. Together: 2(8 + b) = 28, so b = 6 and the area = 8 × 6 = 48 cm². Both statements are needed.",fixed=True,chk=(8*(28/2-8),48))

    # ======================= GENERAL MENTAL ABILITY (15) =======================
    p = GMA
    t = "Number & Letter Series"
    s = [3]; [s.append(s[-1] * 2 + 1) for _ in range(5)]
    M(p,t,"Easy","Find the next term: 3, 7, 15, 31, 63, ?",["127","126","95","125"],str(s[5]),"Each term is double the previous term plus 1: 63 × 2 + 1 = 127.",chk=(s[5],127))
    M(p,t,"Medium","Find the next term: 2, 6, 12, 20, 30, ?",["42","40","36","44"],"42","The terms are 1×2, 2×3, 3×4, 4×5, 5×6, so the next is 6 × 7 = 42. (The differences are 4, 6, 8, 10, 12.)",chk=(6*7,42))
    nxt = chr(ord("K") + 3)
    M(p,t,"Easy","Find the next letter: B, E, H, K, ?",["N","M","O","L"],nxt,"Each letter moves 3 places forward: B → E → H → K → N.",chk=(nxt,"N"))
    t = "Analogies"
    M(p,t,"Easy","8 : 64 :: 11 : ?",["121","88","111","132"],"121","64 is the square of 8, so the answer is the square of 11 = 121.",chk=(11**2,121))
    M(p,t,"Easy","Pen : Write :: Knife : ?",["Cut","Sharp","Kitchen","Steel"],"Cut","A pen is used to write; a knife is used to cut. The relationship is tool : its function.")
    t = "Odd One Out"
    isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
    opts = ["23", "29", "33", "37"]; odd = [o for o in opts if not isprime(int(o))]; assert odd == ["33"]
    M(p,t,"Easy","Which number is the odd one out? 23, 29, 33, 37",opts,"33","23, 29 and 37 are prime. 33 = 3 × 11 is not.")
    M(p,t,"Easy","Which is the odd one out? Mercury, Venus, Moon, Mars",["Moon","Mercury","Venus","Mars"],"Moon","Mercury, Venus and Mars are planets. The Moon is a natural satellite of the Earth.")
    t = "Coding-Decoding"
    enc = lambda w: "".join(chr((ord(c) - 65 + 1) % 26 + 65) for c in w); assert enc("MANGO") == "NBOHP"
    M(p,t,"Easy","In a certain code, MANGO is written as NBOHP. How is APPLE written in that code?",["BQQMF","BOOKD","ZOOKD","BQQME"],enc("APPLE"),"Each letter is replaced by the next letter of the alphabet (M→N, A→B, N→O, G→H, O→P). So APPLE → BQQMF.")
    val = lambda w: sum(ord(c) - 64 for c in w); assert val("RED") == 27
    M(p,t,"Medium","If RED is coded as 27, how is BLUE coded?",["40","38","42","36"],str(val("BLUE")),"The code is the sum of the letters' alphabet positions: R(18) + E(5) + D(4) = 27. BLUE = B(2) + L(12) + U(21) + E(5) = 40.")
    t = "Direction Sense"
    x, y = 3, 5 - 9; dist = math.hypot(x, y)
    M(p,t,"Medium","Ravi walks 5 km north, turns right and walks 3 km, then turns right again and walks 9 km. How far is he from his starting point, and in which direction?",["5 km, South-East","5 km, North-East","7 km, South","4 km, East"],"5 km, South-East","Take the start as (0, 0). North 5 → (0, 5). Turning right from north means facing east, so 3 km → (3, 5). Turning right again means facing south, so 9 km → (3, −4). Distance = √(3² + 4²) = 5 km, to the south-east.",chk=(dist,5))
    face = ["North", "East", "South", "West"][(0 + 1 - 2) % 4]
    M(p,t,"Easy","A girl faces north. She turns 90° clockwise, and then 180° anticlockwise. Which direction is she facing now?",["West","East","South","North"],face,"90° clockwise from north takes her to east. 180° anticlockwise from east takes her to west.")
    t = "Clocks & Calendars"
    ang = abs(30 * 3 - 5.5 * 30)
    M(p,t,"Medium","What is the angle between the hour hand and the minute hand of a clock at 3:30?",["75°","90°","60°","105°"],"75°","At 3:30 the minute hand is at 180° (pointing to 6). The hour hand has moved half-way from 3 to 4: 90° + 15° = 105°. The angle = 180° − 105° = 75°. (Formula: |30H − 5.5M| = |90 − 165| = 75°.)",chk=(ang,75))
    y0 = next(yy for yy in range(2001, 2100) if datetime.date(yy, 1, 1).weekday() == 0 and not (yy % 4 == 0 and (yy % 100 or yy % 400 == 0)))
    nd = datetime.date(y0 + 1, 1, 1).strftime("%A")
    M(p,t,"Medium","1 January of a certain year (not a leap year) is a Monday. What day of the week is 1 January of the following year?",["Tuesday","Monday","Wednesday","Sunday"],nd,f"A non-leap year has 365 days = 52 weeks + 1 day, so the date moves one weekday forward: Monday → Tuesday. (For example, 1 January {y0} was a Monday and 1 January {y0+1} was a Tuesday.)")
    t = "Mathematical Operations"
    expr = "8 + 3 × 12 − 4 ÷ 2"; m = {"+": "*", "×": "-", "−": "/", "÷": "+"}
    val2 = eval("".join(m.get(c, c) for c in expr.replace(" ", "")))
    M(p,t,"Medium","If + means ×, × means −, − means ÷ and ÷ means +, what is the value of 8 + 3 × 12 − 4 ÷ 2?",["23","26","20","30"],str(int(val2)),"Replace the symbols: 8 × 3 − 12 ÷ 4 + 2. Then apply BODMAS: 24 − 3 + 2 = 23.",chk=(val2,23))
    t = "Ranking & Order"
    M(p,t,"Easy","In a row of 40 students, Asha is 12th from the left. What is her position from the right?",["29th","28th","30th","27th"],f"{40-12+1}th","Position from right = total − position from left + 1 = 40 − 12 + 1 = 29th.",chk=(40-12+1,29))

    # ======================= GENERAL KNOWLEDGE (15, static facts only; each checked against an official or standard reference) =======================
    p = GK
    t = "Indian Polity"
    M(p,t,"Easy","On which date did the Constitution of India come into force?",["26 January 1950","26 November 1949","15 August 1947","26 January 1949"],"26 January 1950","The Constituent Assembly adopted the Constitution on 26 November 1949, and it came into force on 26 January 1950, which is celebrated as Republic Day.")
    M(p,t,"Medium","The Fundamental Duties of citizens are listed in which Article of the Constitution of India?",["Article 51A","Article 21","Article 32","Article 44"],"Article 51A","Article 51A (Part IVA) lists the Fundamental Duties. It was inserted by the 42nd Constitutional Amendment Act, 1976.")
    M(p,t,"Medium","Which Article of the Constitution gives a person the right to move the Supreme Court to enforce Fundamental Rights?",["Article 32","Article 14","Article 19","Article 368"],"Article 32","Article 32 is the Right to Constitutional Remedies. Dr B. R. Ambedkar called it the 'heart and soul' of the Constitution.")
    M(p,t,"Medium","Under the Constitution, what is the maximum strength of the Rajya Sabha?",["250","245","238","552"],"250","Article 80: not more than 250 members, of whom 12 are nominated by the President and not more than 238 represent the States and Union Territories. (245 is the number of seats actually filled at present, not the maximum.)")
    M(p,t,"Easy","What is the minimum age for election as President of India?",["35 years","25 years","30 years","40 years"],"35 years","Article 58 requires a candidate to be a citizen of India who has completed 35 years of age and is qualified for election to the Lok Sabha.")
    t = "Geography"
    TOC = {"Gujarat", "Rajasthan", "Madhya Pradesh", "Chhattisgarh", "Jharkhand", "West Bengal", "Tripura", "Mizoram"}; assert len(TOC) == 8
    o = ["Odisha", "Gujarat", "Tripura", "Mizoram"]; assert [x for x in o if x not in TOC] == ["Odisha"]
    M(p,t,"Medium","The Tropic of Cancer does NOT pass through which of these states?",o,"Odisha","The Tropic of Cancer passes through eight states: Gujarat, Rajasthan, Madhya Pradesh, Chhattisgarh, Jharkhand, West Bengal, Tripura and Mizoram. Odisha lies entirely south of it.")
    M(p,t,"Easy","Which river is often called the 'Dakshin Ganga' (Ganga of the South)?",["Godavari","Krishna","Kaveri","Narmada"],"Godavari","The Godavari, about 1,465 km long, is the longest river of peninsular India and is known as the Dakshin Ganga. It rises at Trimbakeshwar near Nashik in Maharashtra.")
    M(p,t,"Easy","The Palk Strait separates India from which country?",["Sri Lanka","Maldives","Myanmar","Bangladesh"],"Sri Lanka","The Palk Strait lies between Tamil Nadu and the Northern Province of Sri Lanka, linking the Bay of Bengal with Palk Bay and the Gulf of Mannar.")
    t = "History"
    M(p,t,"Easy","From where did Mahatma Gandhi begin the Dandi March (Salt Satyagraha) on 12 March 1930?",["Sabarmati Ashram","Champaran","Bardoli","Kheda"],"Sabarmati Ashram","Gandhi and 78 followers set out from Sabarmati Ashram, Ahmedabad, on 12 March 1930 and reached Dandi on the Gujarat coast to break the salt law.")
    M(p,t,"Medium","Who presided over the first session of the Indian National Congress, held in Bombay in 1885?",["W. C. Bonnerjee","Dadabhai Naoroji","A. O. Hume","Surendranath Banerjee"],"W. C. Bonnerjee","The first session (Bombay, December 1885) was presided over by W. C. Bonnerjee. A. O. Hume helped found the Congress; Dadabhai Naoroji presided over the second session in 1886.")
    M(p,t,"Easy","In the First Battle of Panipat (1526), Babur defeated:",["Ibrahim Lodi","Hemu","Rana Sanga","Sher Shah Suri"],"Ibrahim Lodi","Babur's victory over Ibrahim Lodi at Panipat in 1526 ended the Lodi dynasty and founded Mughal rule in India. Hemu was defeated in the Second Battle (1556), and Rana Sanga at Khanwa (1527).")
    t = "General Science"
    M(p,t,"Easy","A deficiency of which vitamin causes scurvy?",["Vitamin C","Vitamin A","Vitamin D","Vitamin K"],"Vitamin C","Scurvy is caused by a severe, long-term lack of vitamin C (ascorbic acid), which the body needs to make collagen. Citrus fruits and amla are good sources.")
    M(p,t,"Easy","What is the SI unit of electric current?",["Ampere","Volt","Ohm","Watt"],"Ampere","The ampere (A) is one of the seven SI base units. The volt measures potential difference, the ohm resistance and the watt power.")
    t = "Environment"
    M(p,t,"Medium","The Montreal Protocol (1987) is an international agreement to:",["Phase out substances that deplete the ozone layer","Protect wetlands of international importance","Ban trade in endangered species","Set targets for forest cover"],"Phase out substances that deplete the ozone layer","The Montreal Protocol controls ozone-depleting substances such as CFCs and halons, to protect the ozone layer in the stratosphere. (Wetlands are covered by the Ramsar Convention, and trade in endangered species by CITES.)")
    M(p,t,"Medium","The Ramsar Convention (1971) is concerned with the conservation of:",["Wetlands","Tigers","Coral reefs only","Mountain glaciers"],"Wetlands","The Convention on Wetlands, signed at Ramsar, Iran, in 1971, promotes the conservation and wise use of wetlands. Sites listed under it are called Ramsar sites.")
