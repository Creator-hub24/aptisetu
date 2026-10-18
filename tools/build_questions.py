"""Builds data/questions.json. Every question is checked here:
- the correct option must appear exactly once among 4 distinct options
- quant/DILR answers are recomputed numerically (chk=(computed, expected))
- puzzles/seating/routes are verified by brute force below.
Run: python3 tools/build_questions.py"""
import json, math, itertools, datetime
from fractions import Fraction as F
from math import comb, factorial, sqrt, pi

OUT = {"quant": [], "reasoning": [], "dilr": []}
SY = ["Only I follows","Only II follows","Both I and II follow","Neither follows"]
SYE = ["Only I follows","Only II follows","Either I or II follows","Neither follows"]
def Q(sec, topic, diff, text, options, correct, solution, data=None, set_id=None, chk=None):
    assert len(options) == 4 and len(set(options)) == 4, (text, options)
    assert options.count(correct) == 1, (text, correct)
    assert diff in ("Easy", "Medium", "Hard")
    if chk is not None:
        a, b = chk
        assert abs(float(a) - float(b)) < 1e-6, (text, a, b)
    esc = lambda x: x.replace(" < ", " &lt; ")
    text = esc(text); answer_idx = options.index(correct); options = [esc(o) for o in options]; correct = options[answer_idx]
    q = dict(id=f"{sec[0].upper()}{len(OUT[sec])+1}", exam="general", topic=topic, difficulty=diff, question=text,
             options=options, answer=options.index(correct), solution=solution)
    if data: q["data"] = data
    # keep option order when it is meaningful (standard answer sets / 'cannot be determined' style)
    if options in (SY, SYE) or any(o.startswith(("Cannot","No ","None","Neither")) for o in options) or options==["None","One","Two","Three"]:
        q["fixed"] = True
    if set_id: q["set"] = set_id
    OUT[sec].append(q)

# ======================= QUANT =======================
s = "quant"
T = "Percentages"
Q(s,T,"Easy","The price of a phone is increased by 20% and the new price is then decreased by 20%. What is the net change in price?",["No change","4% decrease","4% increase","2% decrease"],"4% decrease","Net change = a + b + ab/100 = 20 − 20 − (20×20)/100 = −4%, i.e. a 4% decrease.",chk=((1.2*0.8-1)*100,-4))
Q(s,T,"Easy","A's salary is 25% more than B's. By what percentage is B's salary less than A's?",["25%","20%","15%","22.5%"],"20%","Let B = 100, so A = 125. B is less than A by 25/125 × 100 = 20%.",chk=(25/125*100,20))
Q(s,T,"Easy","If 40% of a number is 96, what is 65% of the same number?",["144","156","160","152"],"156","Number = 96/0.40 = 240. 65% of 240 = 156.",chk=(96/0.4*0.65,156))
Q(s,T,"Medium","A town's population is 50,000. It grows by 10% in the first year and 20% in the second. What is the population after 2 years?",["65,000","66,000","64,500","67,200"],"66,000","50,000 × 1.10 × 1.20 = 66,000.",chk=(50000*1.1*1.2,66000))
Q(s,T,"Medium","A student scoring 30% fails by 30 marks. Another student scoring 45% gets 15 marks more than the pass mark. What are the maximum marks?",["250","300","350","400"],"300","0.30M + 30 = 0.45M − 15 ⇒ 0.15M = 45 ⇒ M = 300.",chk=(45/0.15,300))
Q(s,T,"Hard","The price of sugar rises by 25%. By what percentage must a family cut its consumption so that its spending on sugar stays the same?",["25%","20%","15%","22%"],"20%","Required cut = r/(100 + r) × 100 = 25/125 × 100 = 20%.",chk=((1-1/1.25)*100,20))

T = "Profit & Loss"
Q(s,T,"Easy","An article bought for ₹800 is sold for ₹1,000. What is the profit percentage?",["20%","25%","22.5%","18%"],"25%","Profit = ₹200. Profit % = 200/800 × 100 = 25%.",chk=(200/800*100,25))
Q(s,T,"Easy","An item has a marked price of ₹1,200 and is sold at a 15% discount. What is the selling price?",["₹1,020","₹1,050","₹1,000","₹1,080"],"₹1,020","SP = 1200 × (1 − 0.15) = ₹1,020.",chk=(1200*0.85,1020))
Q(s,T,"Medium","A shopkeeper marks goods 40% above cost price and gives a 10% discount. What is his profit percentage?",["30%","26%","28%","24%"],"26%","SP = CP × 1.40 × 0.90 = 1.26 × CP, so profit = 26%.",chk=((1.4*0.9-1)*100,26))
Q(s,T,"Medium","Selling an item for ₹1,140 causes a loss of 5%. At what price should it be sold to make a 5% profit?",["₹1,200","₹1,260","₹1,250","₹1,197"],"₹1,260","CP = 1140/0.95 = ₹1,200. For 5% profit, SP = 1200 × 1.05 = ₹1,260.",chk=(1140/0.95*1.05,1260))
Q(s,T,"Hard","Two items are each sold for ₹990, one at a 10% profit and the other at a 10% loss. What is the overall result?",["No profit, no loss","1% profit","1% loss","2% loss"],"1% loss","CPs: 990/1.1 = 900 and 990/0.9 = 1,100, total ₹2,000. SP total = ₹1,980. Loss = 20/2000 = 1%.",chk=((1980-(990/1.1+990/0.9))/(990/1.1+990/0.9)*100,-1))
Q(s,T,"Hard","A dishonest dealer sells at cost price but uses a 900 g weight in place of 1 kg. What is his profit percentage?",["10%","11 1/9%","9 1/11%","12%"],"11 1/9%","He gives 900 g but charges for 1000 g. Profit % = 100/900 × 100 = 11 1/9%.",chk=(100/900*100,100/9))

T = "Simple & Compound Interest"
Q(s,T,"Easy","What is the simple interest on ₹5,000 at 8% per annum for 3 years?",["₹1,000","₹1,200","₹1,260","₹1,500"],"₹1,200","SI = P × R × T/100 = 5000 × 8 × 3/100 = ₹1,200.",chk=(5000*8*3/100,1200))
Q(s,T,"Easy","What is the compound interest on ₹10,000 at 10% per annum for 2 years, compounded annually?",["₹2,000","₹2,100","₹2,200","₹2,110"],"₹2,100","A = 10000 × 1.1² = ₹12,100. CI = 12,100 − 10,000 = ₹2,100.",chk=(10000*1.1**2-10000,2100))
Q(s,T,"Medium","What is the difference between compound and simple interest on ₹8,000 for 2 years at 5% per annum?",["₹10","₹20","₹40","₹25"],"₹20","For 2 years, CI − SI = P(R/100)² = 8000 × 0.05² = ₹20.",chk=(8000*1.05**2-8000-8000*0.05*2,20))
Q(s,T,"Medium","A sum of money doubles in 8 years at simple interest. What is the rate of interest per annum?",["10%","12%","12.5%","15%"],"12.5%","Interest = P in 8 years, so R = 100/8 = 12.5%.",chk=(100/8,12.5))
Q(s,T,"Hard","A sum becomes ₹8,820 in 2 years at 5% per annum compound interest. What is the principal?",["₹8,000","₹8,200","₹7,800","₹8,400"],"₹8,000","P = 8820/1.05² = 8820/1.1025 = ₹8,000.",chk=(8820/1.05**2,8000))

T = "Ratio & Proportion"
Q(s,T,"Easy","₹1,800 is divided in the ratio 2 : 3 : 4. What is the largest share?",["₹600","₹800","₹900","₹720"],"₹800","Total parts = 9, so one part = ₹200. Largest share = 4 × 200 = ₹800.",chk=(1800/9*4,800))
Q(s,T,"Easy","If A : B = 2 : 3 and B : C = 4 : 5, what is A : B : C?",["8 : 12 : 15","2 : 3 : 5","8 : 12 : 13","6 : 9 : 10"],"8 : 12 : 15","Make B equal: A:B = 8:12 and B:C = 12:15, so A:B:C = 8:12:15.",chk=(F(8,12),F(2,3)))
Q(s,T,"Medium","A and B invest ₹30,000 and ₹45,000 respectively for one year. The profit is ₹15,000. What is A's share?",["₹5,000","₹6,000","₹7,500","₹9,000"],"₹6,000","Ratio = 30000 : 45000 = 2 : 3. A's share = 2/5 × 15000 = ₹6,000.",chk=(15000*2/5,6000))
Q(s,T,"Medium","What is the mean proportional between 9 and 16?",["12","12.5","13","144"],"12","Mean proportional = √(9 × 16) = √144 = 12.",chk=(sqrt(144),12))
Q(s,T,"Hard","The ratio of boys to girls in a class is 7 : 5. When 12 more girls join, the ratio becomes 1 : 1. How many boys are there?",["35","42","49","28"],"42","7k = 5k + 12 ⇒ k = 6. Boys = 7 × 6 = 42.",chk=(7*6,5*6+12))

T = "Averages & Alligation"
Q(s,T,"Easy","The average of 5 numbers is 20. When one number is removed, the average of the rest is 18. What number was removed?",["22","28","26","30"],"28","Sum of 5 = 100. Sum of 4 = 72. Removed = 100 − 72 = 28.",chk=(100-72,28))
Q(s,T,"Easy","What is the average of the first 10 natural numbers?",["5","5.5","6","10"],"5.5","(1 + 2 + … + 10)/10 = 55/10 = 5.5.",chk=(sum(range(1,11))/10,5.5))
Q(s,T,"Medium","The average age of 30 students is 14 years. When the teacher's age is included, the average becomes 15 years. What is the teacher's age?",["44 years","45 years","46 years","31 years"],"45 years","Sum of 30 ages = 420. Sum of 31 ages = 31 × 15 = 465. Teacher = 465 − 420 = 45 years.",chk=(31*15-30*14,45))
Q(s,T,"Medium","In what ratio must rice at ₹40/kg be mixed with rice at ₹55/kg to get a mixture worth ₹45/kg?",["1 : 2","2 : 1","3 : 2","2 : 3"],"2 : 1","Alligation: (55 − 45) : (45 − 40) = 10 : 5 = 2 : 1 (cheaper : dearer).",chk=((2*40+1*55)/3,45))
Q(s,T,"Hard","A 20-litre mixture has milk and water in the ratio 3 : 1. How much water must be added to make the ratio 3 : 2?",["4 L","5 L","6 L","10 L"],"5 L","Milk = 15 L, water = 5 L. For 3 : 2, water must be 10 L, so add 5 L.",chk=(15/(5+5),1.5))

T = "Time & Work"
Q(s,T,"Easy","A can finish a job in 12 days and B in 18 days. Working together, how long will they take?",["7.2 days","7.5 days","6 days","15 days"],"7.2 days","Combined rate = 1/12 + 1/18 = 5/36 per day. Time = 36/5 = 7.2 days.",chk=(1/(1/12+1/18),7.2))
Q(s,T,"Easy","6 men can finish a piece of work in 10 days. How many days will 15 men take?",["3 days","4 days","5 days","6 days"],"4 days","Total work = 6 × 10 = 60 man-days. 60/15 = 4 days.",chk=(60/15,4))
Q(s,T,"Medium","A and B together can do a job in 10 days. A alone can do it in 15 days. How long will B take alone?",["25 days","30 days","20 days","35 days"],"30 days","B's rate = 1/10 − 1/15 = 1/30, so B takes 30 days.",chk=(1/(1/10-1/15),30))
Q(s,T,"Medium","Pipe A fills a tank in 6 hours and pipe B empties it in 9 hours. If both are opened together on an empty tank, how long will it take to fill?",["15 h","18 h","12 h","3.6 h"],"18 h","Net rate = 1/6 − 1/9 = 1/18 per hour, so 18 hours.",chk=(1/(1/6-1/9),18))
Q(s,T,"Hard","A can do a job in 20 days and B in 30 days. They work together for 6 days, then A leaves. In how many more days will B finish the job?",["12","15","18","10"],"15","In 6 days they do 6 × (1/20 + 1/30) = 1/2 of the job. B does the other 1/2 in 30 × 1/2 = 15 days.",chk=((1-6*(1/20+1/30))*30,15))

T = "Time, Speed & Distance"
Q(s,T,"Easy","A 150 m long train runs at 54 km/h. How long does it take to cross a pole?",["8 s","9 s","10 s","12 s"],"10 s","54 km/h = 54 × 5/18 = 15 m/s. Time = 150/15 = 10 s.",chk=(150/(54*5/18),10))
Q(s,T,"Medium","A car goes from A to B at 60 km/h and returns at 40 km/h. What is its average speed for the round trip?",["50 km/h","48 km/h","45 km/h","52 km/h"],"48 km/h","For equal distances, average speed = 2xy/(x + y) = 2 × 60 × 40/100 = 48 km/h.",chk=(2*60*40/100,48))
Q(s,T,"Medium","A 200 m long train running at 72 km/h crosses a 300 m long platform. How long does it take?",["20 s","25 s","15 s","30 s"],"25 s","72 km/h = 20 m/s. Distance = 200 + 300 = 500 m. Time = 500/20 = 25 s.",chk=(500/(72*5/18),25))
Q(s,T,"Medium","A boat's speed in still water is 15 km/h and the stream flows at 3 km/h. How long does the boat take to go 36 km downstream?",["2 h","2.5 h","3 h","1.5 h"],"2 h","Downstream speed = 15 + 3 = 18 km/h. Time = 36/18 = 2 h.",chk=(36/18,2))
Q(s,T,"Hard","Two trains, 120 m and 180 m long, run in opposite directions at 40 km/h and 50 km/h. How long do they take to cross each other completely?",["10 s","12 s","15 s","18 s"],"12 s","Relative speed = 90 km/h = 25 m/s. Distance = 300 m. Time = 300/25 = 12 s.",chk=(300/(90*5/18),12))

T = "Number System"
def tz(n): return sum(n//5**k for k in range(1,10))
Q(s,T,"Medium","How many trailing zeros does 50! have?",["10","11","12","13"],"12","Count the factors of 5: ⌊50/5⌋ + ⌊50/25⌋ = 10 + 2 = 12.",chk=(tz(50),12))
Q(s,T,"Medium","What is the remainder when 2¹⁰ is divided by 7?",["1","2","4","3"],"2","2³ = 8 ≡ 1 (mod 7), so 2¹⁰ = (2³)³ × 2 ≡ 2. Check: 1024 = 7 × 146 + 2.",chk=(2**10%7,2))
Q(s,T,"Easy","What is the HCF of 36 and 84?",["6","12","18","24"],"12","36 = 2² × 3², 84 = 2² × 3 × 7. HCF = 2² × 3 = 12.",chk=(math.gcd(36,84),12))
Q(s,T,"Easy","What is the LCM of 12, 18 and 30?",["90","120","180","360"],"180","12 = 2² × 3, 18 = 2 × 3², 30 = 2 × 3 × 5. LCM = 2² × 3² × 5 = 180.",chk=(math.lcm(12,18,30),180))
Q(s,T,"Medium","How many positive factors does 360 have?",["18","20","24","36"],"24","360 = 2³ × 3² × 5. Number of factors = (3+1)(2+1)(1+1) = 24.",chk=(sum(1 for d in range(1,361) if 360%d==0),24))
Q(s,T,"Hard","What is the unit digit of 7⁹⁵?",["1","3","7","9"],"3","Unit digits of powers of 7 repeat 7, 9, 3, 1. 95 mod 4 = 3, so the unit digit is the 3rd in the cycle, which is 3.",chk=(pow(7,95,10),3))

T = "Algebra"
Q(s,T,"Easy","If x + 1/x = 5, what is x² + 1/x²?",["23","25","27","21"],"23","(x + 1/x)² = x² + 1/x² + 2 ⇒ x² + 1/x² = 25 − 2 = 23.",chk=(5**2-2,23))
Q(s,T,"Easy","If 3x − 7 = 2x + 5, what is x?",["2","12","−2","10"],"12","3x − 2x = 5 + 7 ⇒ x = 12.",chk=(3*12-7,2*12+5))
Q(s,T,"Medium","If the roots of x² − 5x + 6 = 0 are a and b, what is a² + b²?",["13","25","11","37"],"13","a + b = 5 and ab = 6. a² + b² = (a + b)² − 2ab = 25 − 12 = 13. (The roots are 2 and 3.)",chk=(2**2+3**2,13))
Q(s,T,"Medium","The sum of two numbers is 25 and their difference is 7. What is their product?",["144","136","150","126"],"144","The numbers are (25 + 7)/2 = 16 and (25 − 7)/2 = 9. Product = 144.",chk=(16*9,144))
Q(s,T,"Hard","If a + b = 7 and ab = 10, what is a³ + b³?",["133","343","210","153"],"133","a³ + b³ = (a + b)³ − 3ab(a + b) = 343 − 210 = 133. (a, b are 2 and 5: 8 + 125 = 133.)",chk=(2**3+5**3,133))

T = "Geometry & Mensuration"
Q(s,T,"Medium","A right triangle has legs of 6 cm and 8 cm. What is the area of its circumcircle?",["16π cm²","25π cm²","36π cm²","100π cm²"],"25π cm²","Hypotenuse = √(36 + 64) = 10 cm. The hypotenuse is the circumdiameter, so r = 5 and area = 25π cm².",chk=((sqrt(36+64)/2)**2,25))
Q(s,T,"Easy","What is the perimeter of a rectangle 12 cm long and 8 cm wide?",["20 cm","40 cm","96 cm","48 cm"],"40 cm","Perimeter = 2(l + b) = 2(12 + 8) = 40 cm.",chk=(2*(12+8),40))
Q(s,T,"Easy","What is each interior angle of a regular hexagon?",["108°","120°","135°","144°"],"120°","Each interior angle = (n − 2) × 180°/n = 4 × 180/6 = 120°.",chk=((6-2)*180/6,120))
Q(s,T,"Medium","A cube has a total surface area of 150 cm². What is its volume?",["125 cm³","216 cm³","100 cm³","150 cm³"],"125 cm³","6a² = 150 ⇒ a = 5 cm. Volume = 5³ = 125 cm³.",chk=(sqrt(150/6)**3,125))
Q(s,T,"Medium","What is the area of an equilateral triangle with side 6 cm?",["9√3 cm²","18√3 cm²","12√3 cm²","36 cm²"],"9√3 cm²","Area = (√3/4) × a² = (√3/4) × 36 = 9√3 cm².",chk=(sqrt(3)/4*36,9*sqrt(3)))
Q(s,T,"Hard","If the radius of a circle increases by 10%, by what percentage does its area increase?",["10%","20%","21%","11%"],"21%","Area ∝ r². 1.1² = 1.21, so the area increases by 21%.",chk=((1.1**2-1)*100,21))

T = "Permutations & Combinations"
Q(s,T,"Medium","In how many ways can the letters of the word LEVEL be arranged?",["60","30","120","20"],"30","5 letters with L twice and E twice: 5!/(2! × 2!) = 30.",chk=(len(set(itertools.permutations("LEVEL"))),30))
Q(s,T,"Easy","In how many ways can 5 people sit in a row?",["25","60","120","720"],"120","5! = 120.",chk=(factorial(5),120))
Q(s,T,"Easy","In how many ways can a committee of 3 be chosen from 8 people?",["56","336","24","64"],"56","8C3 = (8 × 7 × 6)/(3 × 2 × 1) = 56.",chk=(comb(8,3),56))
Q(s,T,"Medium","How many 3-digit numbers can be formed using the digits 1, 2, 3, 4, 5 without repetition?",["125","60","80","120"],"60","5 × 4 × 3 = 60.",chk=(len(list(itertools.permutations("12345",3))),60))
Q(s,T,"Hard","A committee of 3 is chosen from 5 men and 4 women. In how many ways can this be done if it must include at least one woman?",["74","84","80","70"],"74","Total = 9C3 = 84. All-men = 5C3 = 10. At least one woman = 84 − 10 = 74.",chk=(sum(1 for c in itertools.combinations(range(9),3) if any(x>=5 for x in c)),74))
Q(s,T,"Hard","How many diagonals does a regular decagon (10 sides) have?",["35","45","40","70"],"35","Diagonals = n(n − 3)/2 = 10 × 7/2 = 35.",chk=(comb(10,2)-10,35))

T = "Probability"
dice = list(itertools.product(range(1,7),repeat=2))
Q(s,T,"Easy","Two fair dice are thrown. What is the probability that the sum is 7?",["1/6","5/36","7/36","1/9"],"1/6","Favourable outcomes: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1), which is 6 of 36, so 1/6.",chk=(F(sum(1 for a,b in dice if a+b==7),36),F(1,6)))
Q(s,T,"Easy","A card is drawn at random from a standard 52-card deck. What is the probability that it is a king?",["1/13","1/4","1/52","4/13"],"1/13","There are 4 kings: 4/52 = 1/13.",chk=(F(4,52),F(1,13)))
Q(s,T,"Medium","Three fair coins are tossed. What is the probability of getting at least two heads?",["3/8","1/2","1/4","5/8"],"1/2","Outcomes with 2 or 3 heads: HHT, HTH, THH, HHH, which is 4 of 8, so 1/2.",chk=(F(sum(1 for t in itertools.product("HT",repeat=3) if t.count("H")>=2),8),F(1,2)))
Q(s,T,"Medium","A bag has 5 red and 3 blue balls. Two balls are drawn without replacement. What is the probability that both are red?",["5/14","25/64","5/16","3/14"],"5/14","5C2/8C2 = 10/28 = 5/14.",chk=(F(comb(5,2),comb(8,2)),F(5,14)))
Q(s,T,"Hard","Two fair dice are thrown. What is the probability that the product of the numbers is even?",["1/2","3/4","1/4","2/3"],"3/4","The product is odd only when both are odd: 3 × 3 = 9 outcomes. P(even) = 1 − 9/36 = 3/4.",chk=(F(sum(1 for a,b in dice if a*b%2==0),36),F(3,4)))

# ======================= REASONING =======================
s = "reasoning"
SY = ["Only I follows","Only II follows","Both I and II follow","Neither follows"]
SYE = ["Only I follows","Only II follows","Either I or II follows","Neither follows"]
T = "Syllogisms"
Q(s,T,"Easy","Statements: All cats are dogs. All dogs are birds.<br>Conclusions: I. All cats are birds. II. Some birds are cats.",SY,"Both I and II follow","Cats ⊂ Dogs ⊂ Birds, so all cats are birds (I). Converting I gives some birds are cats (II). Both follow.")
Q(s,T,"Medium","Statements: Some pens are books. No book is a pencil.<br>Conclusions: I. Some pens are not pencils. II. No pen is a pencil.",SY,"Only I follows","The pens that are books cannot be pencils, so I follows. Pens that are not books may or may not be pencils, so II does not follow.")
Q(s,T,"Easy","Statements: All roses are flowers. Some flowers are red.<br>Conclusions: I. Some roses are red. II. All flowers are roses.",SY,"Neither follows","The red flowers may lie entirely outside the roses, so I is not certain. 'All roses are flowers' does not make all flowers roses, so II fails too.")
Q(s,T,"Medium","Statements: No apple is a mango. All mangoes are fruits.<br>Conclusions: I. Some fruits are not apples. II. No fruit is an apple.",SY,"Only I follows","The mangoes are fruits and none of them is an apple, so some fruits are not apples (I). Apples could still be fruits, so II does not follow.")
Q(s,T,"Medium","Statements: All books are pages. No page is a pen.<br>Conclusions: I. No book is a pen. II. Some pages are books.",SY,"Both I and II follow","Books ⊂ Pages and Pages ∩ Pens = ∅, so no book is a pen (I). Converting 'all books are pages' gives some pages are books (II).")
Q(s,T,"Hard","Statements: Some teachers are doctors. Some doctors are engineers.<br>Conclusions: I. Some teachers are engineers. II. No teacher is an engineer.",SYE,"Either I or II follows","Neither conclusion is definite on its own. But I ('some') and II ('no') are about the same two groups and together cover every case, so exactly one must be true: Either I or II follows (the standard rule for complementary pairs).")

T = "Seating Arrangement"
# verify linear puzzle by brute force
lin = [p for p in itertools.permutations("PQRST") if p[2]=="S" and p[1]=="T" and (p[0]=="R" or p[4]=="R") and any(p[i]=="P" and p[i+1]=="Q" for i in range(4))]
assert lin == [tuple("RTSPQ")], lin
LIN = "P, Q, R, S and T sit in a row facing north. S is in the middle. R is at one of the extreme ends. T is second from the left. Q is immediately to the right of P."
Q(s,T,"Hard",LIN+" Who sits at the extreme right?",["P","R","Q","T"],"Q","Positions 1–5 from the left: S = 3, T = 2. P and Q need two adjacent free seats, which is only 4–5, so P = 4 and Q = 5, leaving R = 1. Order: R T S P Q.")
Q(s,T,"Medium",LIN+" Who sits exactly between T and P?",["R","S","Q","No one"],"S","The order is R T S P Q, so S sits between T (2nd) and P (4th).")
# circular: seats 0..5 clockwise; facing centre, left = clockwise (+1), right = anticlockwise (-1)
sols=[]
for p in itertools.permutations("ABCDEF"):
    pos={c:i for i,c in enumerate(p)}
    if pos["A"]!=0: continue
    if (pos["D"]-pos["A"])%6!=3: continue
    if (pos["B"]-pos["A"])%6!=1: continue
    if (pos["E"]-pos["D"])%6!=5: continue
    if (pos["C"]-pos["A"])%6 in (1,5): continue
    sols.append(p)
assert len(sols)==1, sols
c=sols[0]; at=lambda i: c[i%6]; P={x:i for i,x in enumerate(c)}
CIRC = "Six friends A–F sit around a circular table facing the centre. A sits opposite D. B is immediately to the left of A. E is immediately to the right of D. C is not a neighbour of A."
Q(s,T,"Medium",CIRC+" Who sits opposite B?",["C","E","F","A"],at(P["B"]+3),"Fix A. D is opposite A. B is A's left neighbour and E is D's right neighbour. C can't sit next to A, so C takes the seat opposite B, and F sits on A's right.")
Q(s,T,"Medium",CIRC+" Who is immediately to the right of A?",["B","F","C","E"],at(P["A"]-1),"Going clockwise from A (to each person's left): A, B, E, D, C, F. So F is on A's right.")
Q(s,T,"Hard",CIRC+" Who sits between E and C?",["D","F","B","A"],at(P["E"]+1),"Clockwise order: A, B, E, D, C, F. D sits between E and C.")
assert at(P["B"]+3)=="C" and at(P["A"]-1)=="F" and at(P["E"]+1)=="D" and at(P["C"]-1)=="D"

T = "Blood Relations"
Q(s,T,"Easy","Pointing to a man, Riya says, \"He is the son of my father's father's only son.\" How is the man related to Riya?",["Cousin","Uncle","Brother","Nephew"],"Brother","Father's father's only son = Riya's father. Her father's son is her brother.")
Q(s,T,"Easy","A is B's sister. C is B's mother. D is C's father. How is A related to D?",["Daughter","Granddaughter","Niece","Grandmother"],"Granddaughter","A and B are C's children and D is C's father. A is female, so A is D's granddaughter.")
Q(s,T,"Easy","X is the wife of Y. Y is the brother of Z. How is X related to Z?",["Sister","Sister-in-law","Cousin","Aunt"],"Sister-in-law","X is married to Z's brother, so X is Z's sister-in-law.")
Q(s,T,"Medium","P is the father of Q. Q is the mother of R. How is P related to R?",["Father","Uncle","Grandfather","Brother"],"Grandfather","P is the father of R's mother, so P is R's (maternal) grandfather.")
Q(s,T,"Hard","Introducing a woman, Amit says, \"Her mother is the only daughter of my mother.\" How is Amit related to the woman?",["Father","Brother","Maternal uncle","Cousin"],"Maternal uncle","The only daughter of Amit's mother is Amit's sister. The woman's mother is Amit's sister, so Amit is her maternal uncle.")

T = "Coding-Decoding"
shift=lambda w,k: "".join(chr((ord(ch)-65+k)%26+65) for ch in w)
atb=lambda w: "".join(chr(155-ord(ch)) for ch in w)
pos=lambda w: sum(ord(ch)-64 for ch in w)
assert shift("CAT",1)=="DBU" and atb("BOOK")=="YLLP" and pos("APPLE")==50
Q(s,T,"Easy","If CAT is coded as DBU, how is DOG coded?",["EPH","CNF","EOH","DPH"],shift("DOG",1),"Each letter moves one place forward: C→D, A→B, T→U. So DOG → EPH.")
Q(s,T,"Medium","In a code, APPLE = 50 (the sum of the letters' alphabet positions). What is GRAPE?",["45","47","49","52"],str(pos("GRAPE")),"GRAPE = 7 + 18 + 1 + 16 + 5 = 47.")
Q(s,T,"Medium","If BOOK is coded as YLLP, how is DESK coded?",["WVHP","XVHP","WUHP","WVIP"],atb("DESK"),"Each letter is swapped with its mirror letter in the alphabet (A↔Z, B↔Y, …): B→Y, O→L, K→P. So D→W, E→V, S→H, K→P gives WVHP.")
Q(s,T,"Easy","In a code, PEN is written as 16-5-14. How is INK written?",["9-14-11","9-13-11","8-14-11","9-14-12"],"-".join(str(ord(ch)-64) for ch in "INK"),"Each letter is replaced by its alphabet position: I = 9, N = 14, K = 11.")
Q(s,T,"Hard","In a language, 'sky is blue' is 'ta na pa', 'blue is nice' is 'na ri ta' and 'nice day' is 'ri lo'. What is the code for 'sky'?",["ta","na","pa","ri"],"pa","Sentences 1 and 2 share 'is blue' and 'ta na', so {is, blue} = {ta, na}. The word left in sentence 1, 'sky', must be 'pa'.")

T = "Puzzles"
fl=[]
for p in itertools.permutations("PQRST"):
    f={x:i+1 for i,x in enumerate(p)}
    if f["R"]%2==0 and f["Q"]==f["R"]+1 and f["T"]==5 and f["S"]<f["P"]: fl.append(f)
assert len(fl)==1; f=fl[0]; inv={v:k for k,v in f.items()}
FLOOR="P, Q, R, S and T live on different floors of a 5-floor building (floor 1 is the lowest, floor 5 the top). R lives on an even-numbered floor. Q lives immediately above R. T lives on the top floor. S lives on a floor below P."
Q(s,T,"Medium",FLOOR+" Who lives on floor 4?",["P","Q","S","R"],inv[4],"T = 5. R is even: if R = 4 then Q = 5, which is taken, so R = 2 and Q = 3. P and S share floors 1 and 4 with S below P, so S = 1 and P = 4.")
Q(s,T,"Easy",FLOOR+" Who lives on the lowest floor?",["R","S","P","Q"],inv[1],"From the solution (S1, R2, Q3, P4, T5), S lives on floor 1.")
Q(s,T,"Medium",FLOOR+" How many people live between S and T?",["2","3","4","1"],str(f["T"]-f["S"]-1),"S is on floor 1 and T on floor 5. R, Q and P live between them, so 3 people.")
Q(s,T,"Medium",FLOOR+" Who lives immediately below T?",["Q","P","R","S"],inv[4],"T is on floor 5 and floor 4 belongs to P.")
pets=[p for p in itertools.permutations(["cat","dog","fish"]) if p[0]!="dog" and p[1]=="fish"]
assert len(pets)==1 and pets[0][2]=="dog"
Q(s,T,"Easy","Ana, Ben and Cara each own a different pet: a cat, a dog or a fish. Ana does not own the dog. Ben owns the fish. Who owns the dog?",["Ana","Ben","Cara","Cannot be determined"],"Cara","Ben has the fish, and Ana can't have the dog, so Ana has the cat and Cara has the dog.")

T = "Direction Sense"
Q(s,T,"Medium","Ravi walks 5 km north, turns right and walks 3 km, then turns right again and walks 9 km. How far is he from his starting point?",["5 km","7 km","4 km","6 km"],"5 km","Right of north is east. He ends 3 km east and 9 − 5 = 4 km south of the start. Distance = √(3² + 4²) = 5 km.",chk=(sqrt(3**2+4**2),5))
Q(s,T,"Easy","You face north, turn right, turn right again, and then turn left. Which direction are you facing now?",["North","East","South","West"],"East","North → right → East → right → South → left → East.")
Q(s,T,"Medium","Meena walks 10 m south, turns left and walks 6 m, then turns left again and walks 10 m. Where is she now with respect to her starting point?",["6 m east","6 m west","10 m north","16 m east"],"6 m east","Left of south is east, and left of east is north. She goes 10 S, then 6 E, then 10 N, so she ends 6 m east of the start.")
Q(s,T,"Medium","Early in the morning, Rohan stands with his shadow falling exactly to his right. Which direction is he facing?",["North","South","East","West"],"South","In the morning the sun is in the east, so shadows fall to the west. West is on your right when you face south.")
Q(s,T,"Hard","A man walks 3 km east, then 4 km north, then 6 km west. How far is he from the start, and in which direction?",["5 km, North-West","5 km, North-East","7 km, North-West","13 km, West"],"5 km, North-West","Net movement: 3 − 6 = 3 km west and 4 km north. Distance = √(9 + 16) = 5 km, towards the north-west.",chk=(sqrt(3**2+4**2),5))

T = "Number & Letter Series"
Q(s,T,"Easy","Find the next term: 2, 6, 12, 20, 30, ?",["40","42","44","36"],"42","The terms are n(n + 1): 1×2, 2×3, …, 5×6, so next is 6×7 = 42.",chk=(6*7,42))
Q(s,T,"Medium","Find the next term: 3, 5, 9, 17, 33, ?",["63","64","65","66"],"65","Each term = previous × 2 − 1, so 33 × 2 − 1 = 65.",chk=(33*2-1,65))
Q(s,T,"Medium","Find the next letter: A, C, F, J, O, ?",["T","U","V","S"],chr(ord("O")+6),"The gaps are +2, +3, +4, +5, +6. O (15) + 6 = 21 = U.")
Q(s,T,"Easy","Find the next term: 2, 3, 5, 7, 11, 13, ?",["15","17","19","16"],"17","These are consecutive prime numbers. The next prime after 13 is 17.")
Q(s,T,"Hard","Find the next term: 4, 6, 12, 14, 28, 30, ?",["32","60","56","62"],"60","The steps alternate +2 and ×2: 4+2 = 6, 6×2 = 12, 12+2 = 14, 14×2 = 28, 28+2 = 30, 30×2 = 60.",chk=(30*2,60))
Q(s,T,"Medium","Find the next pair: AZ, BY, CX, ?",["DW","DV","EW","CW"],"DW","The first letter moves forward (A, B, C, D) and the second moves backward (Z, Y, X, W).")

T = "Odd One Out"
isp=lambda n: n>1 and all(n%d for d in range(2,int(n**.5)+1))
Q(s,T,"Easy","Find the odd one out: 8, 27, 64, 100, 125",["27","64","100","125"],"100","8, 27, 64 and 125 are perfect cubes (2³, 3³, 4³, 5³). 100 is not a cube.")
assert [n for n in [17,23,29,33,37] if not isp(n)]==[33]
Q(s,T,"Easy","Find the odd one out: 17, 23, 29, 33, 37",["23","29","33","37"],"33","All the others are prime. 33 = 3 × 11.")
Q(s,T,"Easy","Find the odd one out: Square, Rectangle, Triangle, Rhombus",["Square","Rectangle","Triangle","Rhombus"],"Triangle","Square, rectangle and rhombus have four sides. A triangle has three.")
assert [b for b in [11,13,17,19,18] if not isp(b)]==[18]
Q(s,T,"Medium","Find the odd one out: 121, 169, 289, 324, 361",["169","289","324","361"],"324","121 = 11², 169 = 13², 289 = 17², 361 = 19² are squares of primes. 324 = 18², and 18 isn't prime.")
Q(s,T,"Medium","Find the odd one out: ACE, BDF, GIK, MOP",["ACE","BDF","GIK","MOP"],"MOP","The others skip one letter each time (A_C_E). In MOP the last step, O→P, skips nothing.")

T = "Clocks & Calendars"
ang=lambda h,m: abs(30*h-5.5*m)
Q(s,T,"Medium","What is the smaller angle between the hour and minute hands at 3:40?",["120°","130°","140°","150°"],"130°","Angle = |30H − 5.5M| = |90 − 220| = 130°.",chk=(ang(3,40),130))
Q(s,T,"Easy","What is the smaller angle between the hands of a clock at exactly 9:00?",["90°","180°","270°","45°"],"90°","At 9:00 the hands are 3 hour-marks apart: 3 × 30° = 90° (the smaller angle).",chk=(360-ang(9,0),90))
Q(s,T,"Medium","How many times do the hour and minute hands coincide in 12 hours?",["10","11","12","24"],"11","The hands coincide every 12/11 hours, so 11 times in 12 hours. There's no separate meeting between 11 and 1, because that one happens at 12:00.")
assert datetime.date(2025,1,1).strftime("%A")=="Wednesday" and datetime.date(2026,1,1).strftime("%A")=="Thursday"
Q(s,T,"Medium","1 January 2025 was a Wednesday. What day of the week is 1 January 2026?",["Wednesday","Thursday","Friday","Tuesday"],"Thursday","2025 is not a leap year: 365 days = 52 weeks + 1 odd day. Wednesday + 1 = Thursday.")
assert datetime.date(1947,8,15).strftime("%A")=="Friday"
Q(s,T,"Hard","On what day of the week did 15 August 1947 fall?",["Thursday","Friday","Saturday","Monday"],"Friday","Odd days up to 1900 = 1. Years 1901–1946 = 46 + 11 leap years = 57 ≡ 1. 1 Jan–15 Aug 1947: 31+28+31+30+31+30+31+15 = 227 ≡ 3. Total = 1 + 1 + 3 = 5, which is Friday (Sunday = 0).")
Q(s,T,"Hard","At what time between 4 and 5 o'clock are the two hands of a clock together?",["4:20","4:21 9/11","4:22 2/11","4:21 3/11"],"4:21 9/11","At 4:00 the minute hand is 20 minute-spaces behind and gains 11/12 of a space per minute. Time = 20 × 12/11 = 21 9/11 minutes past 4.",chk=(20*12/11,21+9/11))

T = "Alphabet Test"
AL="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Q(s,T,"Easy","Which letter is 7th from the left in the English alphabet?",["F","G","H","E"],AL[6],"A B C D E F G: the 7th letter is G.")
Q(s,T,"Easy","Which letter is 5th to the right of the 10th letter from the left of the English alphabet?",["N","O","P","E"],AL[9+5],"The 10th letter is J. Five to its right is the 15th letter, O.")
Q(s,T,"Medium","Which letter is 8th from the right end of the English alphabet?",["R","S","T","H"],AL[-8],"8th from the right = (27 − 8) = 19th from the left = S.")
Q(s,T,"Medium","If the English alphabet is written in reverse order, which letter is 10th from the left?",["P","Q","J","R"],AL[::-1][9],"Reversed, the 10th from the left is the 10th from the right of the normal order: 27 − 10 = 17th letter = Q.")
w="EDUCATION"; same=sum(1 for a,b in zip(w,sorted(w)) if a==b)
Q(s,T,"Hard","If the letters of the word EDUCATION are arranged in alphabetical order, how many letters stay in the same position?",["None","One","Two","Three"],["None","One","Two","Three"][same],"In alphabetical order the letters are A C D E I N O T U. Position by position against E D U C A T I O N: E/A, D/C, U/D, C/E, A/I, T/N, I/O, O/T, N/U. No position matches, so the answer is None.")
assert same==0

T = "Inequalities"
Q(s,T,"Easy","If A > B and B > C, which of these must be true?",["A < C","A > C","A = C","Cannot be determined"],"A > C","A > B > C, so A > C.")
Q(s,T,"Medium","Statements: P ≥ Q, Q > R, R = S.<br>Conclusions: I. P > S II. Q > S",SY,"Both I and II follow","P ≥ Q > R = S gives P > S and Q > S. Both follow.")
Q(s,T,"Medium","Statements: M < N ≤ O, O > P.<br>Conclusions: I. M < O II. N > P",SY,"Only I follows","M < N ≤ O gives M < O. N ≤ O and O > P don't fix how N and P compare, so II does not follow.")
Q(s,T,"Medium","Statements: X = Y > Z ≥ W.<br>Conclusions: I. X > W II. Y > W",SY,"Both I and II follow","X = Y > Z ≥ W, so both X > W and Y > W.")
Q(s,T,"Hard","Statements: A ≥ B, B ≤ C, C < D.<br>Conclusions: I. A < D II. B < D",SY,"Only II follows","B ≤ C < D gives B < D (II). A ≥ B and B ≤ C point in opposite directions, so A and D can't be compared. I does not follow.")

T = "Ranking & Order"
Q(s,T,"Easy","In a row of 30 students, Ram is 12th from the left. What is his position from the right?",["18th","19th","20th","17th"],"19th","Position from the right = 30 − 12 + 1 = 19.",chk=(30-12+1,19))
Q(s,T,"Medium","Priya is 9th from the top and 16th from the bottom in her class ranking. How many students are in the class?",["25","24","23","26"],"24","Total = 9 + 16 − 1 = 24.",chk=(9+16-1,24))
hs=[p for p in itertools.permutations("ABCD") if p.index("A")<p.index("B") and p.index("B")<p.index("C") and p.index("D")<p.index("A")]  # tallest first
assert len(hs)==1 and hs[0][-1]=="C"
Q(s,T,"Easy","A is taller than B. C is shorter than B. D is taller than A. Who is the shortest?",["A","B","C","D"],"C","D > A > B > C, so C is the shortest.")
Q(s,T,"Hard","In a row, A is 10th from the left and B is 15th from the right. When they swap places, A becomes 18th from the left. How many people are in the row?",["31","32","33","30"],"32","After the swap A is in B's old seat, which is 18th from the left and 15th from the right. Total = 18 + 15 − 1 = 32.",chk=(18+15-1,32))
er=[p for p in itertools.permutations("PQRST") if p.index("T")<p.index("Q")<p.index("R") and p.index("R")<p.index("P") and p[0]=="S"]
assert len(er)==1 and er[0][1]=="T"
Q(s,T,"Hard","Among P, Q, R, S and T: Q earns more than R but less than T. P earns less than R. S earns the most. Who earns the second highest?",["Q","T","R","P"],"T","S > T > Q > R > P, so T is second.")

# ======================= DILR =======================
s = "dilr"
sales={"A":[120,150,180,210],"B":[80,90,120,150],"C":[100,110,100,140]}; yrs=[2021,2022,2023,2024]
tot=[sum(v[i] for v in sales.values()) for i in range(4)]
TABLE = "<b>Sales of Company X (₹ lakh)</b><table class='data'><tr><th>Product</th>"+"".join(f"<th>{y}</th>" for y in yrs)+"</tr>"+"".join(f"<tr><td>{k}</td>"+"".join(f"<td>{x}</td>" for x in v)+"</tr>" for k,v in sales.items())+"<tr><th>Total</th>"+"".join(f"<th>{x}</th>" for x in tot)+"</tr></table>"
T="Tables"; S1="table-sales"
Q(s,T,"Easy","What is the percentage increase in Company X's total sales from 2023 to 2024?",["20%","25%","30%","24%"],"25%","Total: 400 → 500. Increase = 100/400 = 25%.",TABLE,S1,chk=((tot[3]-tot[2])/tot[2]*100,25))
Q(s,T,"Easy","What share of total 2024 sales came from Product B?",["25%","28%","30%","35%"],"30%","150/500 = 30%.",TABLE,S1,chk=(sales["B"][3]/tot[3]*100,30))
g={k:(v[3]-v[0])/v[0] for k,v in sales.items()}; assert max(g,key=g.get)=="B"
Q(s,T,"Medium","Which product had the highest percentage growth in sales from 2021 to 2024?",["A","B","C","A and B equally"],"B","A: 90/120 = 75%. B: 70/80 = 87.5%. C: 40/100 = 40%. B is highest.",TABLE,S1)
Q(s,T,"Easy","What were Product C's average annual sales over 2021–2024 (₹ lakh)?",["110","112.5","115","105"],"112.5","(100 + 110 + 100 + 140)/4 = 450/4 = 112.5.",TABLE,S1,chk=(sum(sales["C"])/4,112.5))
falls=[(yrs[i],k) for k,v in sales.items() for i in range(1,4) if v[i]<v[i-1]]; assert falls==[(2023,"C")]
Q(s,T,"Medium","In which year did any product's sales fall compared with the previous year?",["2022","2023","2024","No product's sales ever fell"],"2023","Only Product C fell, from 110 (2022) to 100 (2023). Every other year-on-year change is an increase.",TABLE,S1)

cities=[("Delhi",240),("Mumbai",300),("Pune",180),("Jaipur",120),("Kolkata",160)]; cv=dict(cities); ct=sum(cv.values())
BAR = "<b>Students scoring above the 90th percentile in a mock test, by city</b><div class='bars'>"+"".join(f"<div class='bar-row'><span>{c}</span><i style='width:{v/3:.1f}%'></i><span>{v}</span></div>" for c,v in cities)+"</div>"
T="Bar Charts"; S2="bar-cities"
Q(s,T,"Easy","Mumbai's count is what percentage of the total across all five cities?",["25%","28%","30%","32%"],"30%","Total = 1000. Mumbai = 300/1000 = 30%.",BAR,S2,chk=(cv["Mumbai"]/ct*100,30))
Q(s,T,"Easy","What is the ratio of Delhi's count to Pune's count?",["3 : 4","4 : 3","6 : 5","5 : 3"],"4 : 3","240 : 180 = 4 : 3.",BAR,S2,chk=(F(240,180),F(4,3)))
Q(s,T,"Medium","How many cities have a count above the five-city average?",["1","2","3","4"],str(sum(1 for v in cv.values() if v>ct/5)),"Average = 1000/5 = 200. Delhi (240) and Mumbai (300) are above it, so 2.",BAR,S2)
Q(s,T,"Easy","What is the difference between the highest and lowest city counts?",["160","180","200","140"],"180","Highest = Mumbai 300, lowest = Jaipur 120. Difference = 180.",BAR,S2,chk=(max(cv.values())-min(cv.values()),180))
Q(s,T,"Medium","By what percentage is Mumbai's count more than Pune's?",["40%","50%","66.67%","60%"],"66.67%","(300 − 180)/180 × 100 = 66.67%.",BAR,S2,chk=((300-180)/180*100,200/3))

bud={"Rent":30,"Food":25,"Education":15,"Transport":10,"Savings":20}; assert sum(bud.values())==100; INC=60000
PIE = """<b>Monthly budget of a family (total income ₹60,000)</b><div class='pie-wrap'><div class='pie' style='background:conic-gradient(#4f46e5 0 30%,#0891b2 30% 55%,#db2777 55% 70%,#f59e0b 70% 80%,#16a34a 80% 100%)'></div><div class='pie-legend'><div><i style='background:#4f46e5'></i>Rent 30%</div><div><i style='background:#0891b2'></i>Food 25%</div><div><i style='background:#db2777'></i>Education 15%</div><div><i style='background:#f59e0b'></i>Transport 10%</div><div><i style='background:#16a34a'></i>Savings 20%</div></div></div>"""
T="Pie Charts"; S3="pie-budget"
Q(s,T,"Easy","How much does the family spend on education each month?",["₹6,000","₹9,000","₹12,000","₹15,000"],"₹9,000","15% of ₹60,000 = ₹9,000.",PIE,S3,chk=(INC*.15,9000))
Q(s,T,"Easy","What is the central angle of the Food sector?",["75°","80°","90°","100°"],"90°","25% of 360° = 90°.",PIE,S3,chk=(.25*360,90))
Q(s,T,"Hard","Rent goes up by 20%. Income stays the same and the extra rent comes out of savings. What are the new monthly savings?",["₹9,600","₹8,400","₹10,800","₹7,200"],"₹8,400","Rent = ₹18,000. 20% more = ₹3,600 extra. Savings = 12,000 − 3,600 = ₹8,400.",PIE,S3,chk=(INC*.2-INC*.3*.2,8400))
Q(s,T,"Easy","What is the combined monthly spend on rent and transport?",["₹21,000","₹24,000","₹18,000","₹27,000"],"₹24,000","(30% + 10%) × 60,000 = ₹24,000.",PIE,S3,chk=(INC*.4,24000))
Q(s,T,"Medium","By how much does food spending exceed transport spending each month?",["₹6,000","₹9,000","₹12,000","₹15,000"],"₹9,000","(25% − 10%) × 60,000 = 15% × 60,000 = ₹9,000.",PIE,S3,chk=(INC*.15,9000))

months=["Jan","Feb","Mar","Apr","May","Jun"]; dl=[20,25,30,27,36,42]
def line_svg():
    W,H,px,py=360,170,36,20; mx=50
    X=lambda i: px+i*(W-px-14)/5; Y=lambda v: H-py-(v/mx)*(H-2*py)
    pts=" ".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(dl))
    grid="".join(f"<line x1='{px}' x2='{W-10}' y1='{Y(v):.1f}' y2='{Y(v):.1f}' stroke='#e2e8f0'/><text x='{px-6}' y='{Y(v)+4:.1f}' font-size='10' text-anchor='end' fill='#64748b'>{v}</text>" for v in range(0,51,10))
    lab="".join(f"<text x='{X(i):.1f}' y='{H-4}' font-size='10' text-anchor='middle' fill='#64748b'>{m}</text>" for i,m in enumerate(months))
    dots="".join(f"<circle cx='{X(i):.1f}' cy='{Y(v):.1f}' r='3.5' fill='#db2777'/><text x='{X(i):.1f}' y='{Y(v)-8:.1f}' font-size='10' text-anchor='middle' fill='#0f172a'>{v}</text>" for i,v in enumerate(dl))
    return f"<b>Monthly downloads of a study app (thousands), 2026</b><svg viewBox='0 0 {W} {H}' style='width:100%;max-width:420px;display:block'>{grid}<polyline points='{pts}' fill='none' stroke='#db2777' stroke-width='2.5'/>{dots}{lab}</svg>"
LINE=line_svg(); T="Line Graphs"; S4="line-downloads"
mom={months[i]:(dl[i]-dl[i-1])/dl[i-1] for i in range(1,6)}; assert max(mom,key=mom.get)=="May" and sorted(mom.values())[-1]!=sorted(mom.values())[-2]
Q(s,T,"Medium","Which month saw the highest percentage growth in downloads over the previous month?",["Feb","Mar","May","Jun"],"May","Feb +25%, Mar +20%, Apr −10%, May +33.3% (27→36), Jun +16.7%. May is highest.",LINE,S4)
Q(s,T,"Easy","What were the average monthly downloads from January to June (thousands)?",["28","30","32","29"],"30","(20 + 25 + 30 + 27 + 36 + 42)/6 = 180/6 = 30.",LINE,S4,chk=(sum(dl)/6,30))
Q(s,T,"Easy","In how many months did downloads fall compared with the previous month?",["0","1","2","3"],str(sum(1 for i in range(1,6) if dl[i]<dl[i-1])),"Only April fell (30 → 27).",LINE,S4)
Q(s,T,"Medium","What is the percentage increase in downloads from January to June?",["100%","110%","120%","210%"],"110%","(42 − 20)/20 × 100 = 110%.",LINE,S4,chk=((42-20)/20*100,110))
Q(s,T,"Medium","What is the ratio of March downloads to June downloads?",["5 : 7","3 : 4","4 : 7","5 : 6"],"5 : 7","30 : 42 = 5 : 7.",LINE,S4,chk=(F(30,42),F(5,7)))

T="Caselets"; S5="caselet-staff"
CAS="<b>Caselet</b><p style='margin:.3em 0 0'>A company has 120 employees in three departments. 45 work in Sales, and the rest are split between Tech and Ops in the ratio 3 : 2. 40% of Tech employees are women, and Ops has the same number of women as Tech.</p>"
tech=(120-45)*3//5; ops=(120-45)-tech; wt=tech*40//100; wo=wt
assert (tech,ops,wt)==(45,30,18)
Q(s,T,"Easy","How many employees work in Ops?",["25","30","35","45"],str(ops),"Tech + Ops = 75, split 3 : 2, so Tech = 45 and Ops = 30.",CAS,S5)
Q(s,T,"Medium","How many men work in Tech?",["18","27","30","25"],str(tech-wt),"Women in Tech = 40% of 45 = 18. Men = 45 − 18 = 27.",CAS,S5)
Q(s,T,"Medium","What percentage of Ops employees are women?",["40%","50%","60%","36%"],"60%","Women in Ops = 18 (same as Tech). 18/30 = 60%.",CAS,S5,chk=(wo/ops*100,60))
Q(s,T,"Hard","If Sales has 20 women, how many women does the company have in total?",["38","56","54","60"],str(20+wt+wo),"20 (Sales) + 18 (Tech) + 18 (Ops) = 56.",CAS,S5)

T="Arrangements"
Q(s,T,"Medium","A, B, C and D sit around a square table, one on each side, facing the centre. A sits opposite C, and B is on A's immediate left. Who is on A's immediate right?",["B","C","D","Cannot be determined"],"D","With A opposite C, A's two neighbours are B and D. B is on A's left, so D is on A's right.")
people=["Amit","Bina","Chetan","Divya"]; sols=[]
for city in itertools.permutations(["Delhi","Goa","Jaipur","Pune"]):
    for col in itertools.permutations(["red","blue","green","white"]):
        c=dict(zip(people,city)); k=dict(zip(people,col))
        if c["Amit"]!="Goa" or c["Chetan"]!="Jaipur" or k["Bina"]!="red" or c["Bina"]=="Delhi": continue
        if any(c[p]=="Pune" and k[p]!="red" for p in people): continue
        if any(c[p]=="Jaipur" and k[p]!="green" for p in people): continue
        if k["Divya"]=="white": continue
        sols.append((c,k))
assert len(sols)==1; c,k=sols[0]
MAT="<b>Matching set</b><p style='margin:.3em 0 0'>Amit, Bina, Chetan and Divya each like a different city (Delhi, Goa, Jaipur, Pune) and each drive a different coloured car (red, blue, green, white).<br>• Amit likes Goa. • Chetan likes Jaipur. • Bina drives the red car and doesn't like Delhi.<br>• The person who likes Pune drives red. • The person who likes Jaipur drives green. • Divya doesn't drive the white car.</p>"
S6="match-cities"
Q(s,T,"Easy","Who likes Delhi?",people,[p for p in people if c[p]=="Delhi"][0],"Amit = Goa and Chetan = Jaipur. Bina isn't Delhi, so Bina = Pune and Divya = Delhi.",MAT,S6)
Q(s,T,"Medium","What is the colour of Amit's car?",["Red","Blue","Green","White"],k["Amit"].capitalize(),"Bina = red and Chetan (Jaipur) = green. Divya isn't white, so Divya = blue and Amit = white.",MAT,S6)
Q(s,T,"Medium","Who drives the blue car?",people,[p for p in people if k[p]=="blue"][0],"From the solution: Amit white, Bina red, Chetan green, Divya blue.",MAT,S6)
Q(s,T,"Easy","Which city does the owner of the red car like?",["Delhi","Goa","Jaipur","Pune"],c["Bina"],"Bina drives red and likes Pune, which matches the clue that the Pune fan drives red.",MAT,S6)

T="Games & Tournaments"
Q(s,T,"Easy","In a knock-out tournament of 8 teams (no byes, no draws), how many matches are played in total?",["7","8","15","16"],"7","Every match knocks out exactly one team and 7 teams must be knocked out, so 7 matches.",chk=(8-1,7))
Q(s,T,"Easy","In a round-robin tournament of 6 teams (every team plays every other team once), how many matches are played?",["12","15","30","36"],"15","6C2 = 15.",chk=(comb(6,2),15))
RR="<b>Round robin</b><p style='margin:.3em 0 0'>Four teams A, B, C and D each play every other team once. A win earns 2 points, a loss 0, and there are no draws. Final points: A = 6, B = 4, C = 2, D = 0.</p>"; S7="rr-4"
# brute force all results
teams="ABCD"; pairs=list(itertools.combinations(teams,2)); res=[]
for w in itertools.product([0,1],repeat=6):
    pts={t:0 for t in teams}; win={}
    for (x,y),b in zip(pairs,w): win[(x,y)]= x if b==0 else y; pts[win[(x,y)]]+=2
    if pts=={"A":6,"B":4,"C":2,"D":0}: res.append(win)
assert len(res)==1; win=res[0]
Q(s,T,"Easy","How many matches did B lose?",["0","1","2","3"],str(sum(1 for (x,y),v in win.items() if "B" in (x,y) and v!="B")),"A won all 3 games (6 points), including against B. B has 4 points, so B won its other 2 games. B lost 1.",RR,S7)
Q(s,T,"Medium","Which team did C beat?",["A","B","D","No one"],[ (y if x=="C" else x) for (x,y),v in win.items() if v=="C"][0],"C has 2 points, so 1 win. C lost to A (A won all) and to B (B beat C and D). So C beat D.",RR,S7)
Q(s,T,"Easy","How many points were awarded in total across the tournament?",["10","12","14","16"],"12","6 matches × 2 points = 12 (check: 6 + 4 + 2 + 0 = 12).",RR,S7,chk=(comb(4,2)*2,12))

T="Venn Diagrams"
Q(s,T,"Medium","In a class of 60 students, 35 like tea, 30 like coffee and 10 like neither. How many like both?",["5","10","15","20"],"15","At least one = 60 − 10 = 50. Both = 35 + 30 − 50 = 15.",chk=(35+30-50,15))
VEN="<b>Sports survey of 100 students</b><table class='data'><tr><th>Cricket</th><th>Football</th><th>Hockey</th><th>C &amp; F</th><th>F &amp; H</th><th>C &amp; H</th><th>All three</th></tr><tr><td>50</td><td>40</td><td>30</td><td>15</td><td>10</td><td>12</td><td>5</td></tr></table><p class='muted' style='margin:0;font-size:.85rem'>Pair figures include those who play all three.</p>"; S8="venn-sports"
alo=50+40+30-15-10-12+5
Q(s,T,"Medium","How many students play at least one sport?",["83","88","93","78"],str(alo),"n(C∪F∪H) = 50 + 40 + 30 − 15 − 10 − 12 + 5 = 88.",VEN,S8)
Q(s,T,"Medium","How many students play only cricket?",["23","28","33","35"],str(50-15-12+5),"Only cricket = 50 − 15 − 12 + 5 = 28.",VEN,S8)
Q(s,T,"Easy","How many students play none of the three sports?",["7","12","17","10"],str(100-alo),"100 − 88 = 12.",VEN,S8)
Q(s,T,"Hard","How many students play exactly two sports?",["22","27","37","32"],str((15-5)+(10-5)+(12-5)),"Exactly two = (15 − 5) + (10 − 5) + (12 − 5) = 10 + 5 + 7 = 22.",VEN,S8)

T="Network & Routes"
roads={("P","Q"):4,("P","R"):7,("Q","R"):2,("Q","S"):6,("R","S"):3,("S","T"):5,("R","T"):9}
def sp(a,b,closed=()):
    import heapq
    adj={}
    for (x,y),d in roads.items():
        if (x,y) in closed: continue
        adj.setdefault(x,[]).append((y,d)); adj.setdefault(y,[]).append((x,d))
    dist={a:0}; h=[(0,a)]
    while h:
        d,u=heapq.heappop(h)
        if u==b: return d
        for v,w in adj.get(u,[]):
            if d+w<dist.get(v,1e9): dist[v]=d+w; heapq.heappush(h,(d+w,v))
NET="<b>Two-way roads between towns (km)</b><table class='data'><tr><th>Road</th>"+"".join(f"<th>{x}–{y}</th>" for x,y in roads)+"</tr><tr><td>Length</td>"+"".join(f"<td>{d}</td>" for d in roads.values())+"</tr></table><p class='muted' style='margin:0;font-size:.85rem'>No other roads exist.</p>"; S9="net-towns"
Q(s,T,"Medium","What is the shortest road distance from P to S?",["9 km","10 km","11 km","12 km"],f"{sp('P','S')} km","P–Q–R–S = 4 + 2 + 3 = 9. The alternatives, P–R–S and P–Q–S, are both 10.",NET,S9)
Q(s,T,"Medium","What is the shortest road distance from P to T?",["13 km","14 km","15 km","16 km"],f"{sp('P','T')} km","P–Q–R–S–T = 4 + 2 + 3 + 5 = 14. P–Q–R–T = 15.",NET,S9)
Q(s,T,"Medium","What is the shortest road distance from Q to T?",["10 km","11 km","12 km","9 km"],f"{sp('Q','T')} km","Q–R–S–T = 2 + 3 + 5 = 10. Q–R–T and Q–S–T are both 11.",NET,S9)
Q(s,T,"Hard","If road Q–R is closed, what is the shortest distance from P to S?",["9 km","10 km","11 km","13 km"],f"{sp('P','S',closed=[('Q','R')])} km","Without Q–R: P–R–S = 10 and P–Q–S = 10, so 10 km.",NET,S9)

NAMES={"quant":"Quantitative Aptitude","reasoning":"Logical Reasoning","dilr":"DILR"}
import os, collections
out={k:{"name":NAMES[k],"questions":v} for k,v in OUT.items()}
json.dump(out,open(os.path.join(os.path.dirname(__file__),"..","data","questions.json"),"w"),ensure_ascii=False,indent=1)
for k,v in OUT.items():
    c=collections.Counter(q["topic"] for q in v); d=collections.Counter(q["difficulty"] for q in v)
    print(k,len(v),dict(d)); print("  ",dict(c)); assert min(c.values())>=4
    print("   answer positions:",collections.Counter(q["answer"] for q in v))
print("TOTAL",sum(len(v) for v in OUT.values()))


# ======================= CAT TRACK =======================
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cat"))
from common import Bank
import qa as _qa, dilr as _dilr, varc as _varc
CB = Bank(); _qa.build(CB); _dilr.build(CB); _varc.build(CB)
# global checks: unique ids, every set used, every set question references a real set, DILR sets have 4-5 questions
ids = [q["id"] for v in CB.qs.values() for q in v]; assert len(ids) == len(set(ids))
used = collections.Counter(q.get("set") for v in CB.qs.values() for q in v if q.get("set"))
assert set(used) == set(CB.sets), set(CB.sets) ^ set(used)
for sid, n in used.items(): assert 4 <= n <= 5, (sid, n)
for v in CB.qs.values():
    for q in v:
        if q["type"] == "mcq": assert 0 <= q["answer"] < 4
        else: assert q["answer"].lstrip("-").replace(".", "").isdigit()
CAT_NAMES = {"varc": "Verbal Ability & Reading Comprehension", "dilr": "Data Interpretation & Logical Reasoning", "qa": "Quantitative Ability"}
cat_out = {"sections": {k: {"name": CAT_NAMES[k], "questions": CB.qs[k]} for k in ("varc", "dilr", "qa")}, "sets": CB.sets}
json.dump(cat_out, open(os.path.join(os.path.dirname(__file__), "..", "data", "cat.json"), "w"), ensure_ascii=False, indent=1)
for k in ("varc", "dilr", "qa"):
    v = CB.qs[k]
    print("CAT", k, len(v), dict(collections.Counter(q["type"] for q in v)), dict(collections.Counter(q["difficulty"] for q in v)))
    print("   ", dict(collections.Counter(q["topic"] for q in v)))
print("CAT TOTAL", len(ids), "sets:", len(CB.sets))
