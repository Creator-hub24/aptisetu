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

# ======================= BANK / SSC EXPANSION (added Oct 2026; new questions append, so earlier ids never change) =======================
import random as _rnd
_pos = [t for _ in range(14) for t in range(4)]; _rnd.Random(11).shuffle(_pos); _pi = iter(_pos)
def QB(sec, topic, diff, text, options, correct, *a, **k):
    """Q() with the correct option moved (by swapping) to a balanced, deterministic position, so the answer is not mostly B.
    Standard answer sets (Only I follows ...) and 'No/None/Neither/Cannot ...' sets keep their fixed order."""
    options = list(options)
    if options not in (SY, SYE) and not any(o.startswith(("Cannot", "No ", "None", "Neither")) for o in options):
        t = next(_pi); c = options.index(correct); options[c], options[t] = options[t], options[c]
    Q(sec, topic, diff, text, options, correct, *a, **k)
s = "quant"
QB(s,"Percentages","Easy","The price of an article is reduced by 15% and then by a further 20%. What is the overall reduction?",["35%","32%","30%","34%"],"32%","Price after both cuts = 0.85 × 0.80 = 0.68 of the original, so the overall reduction is 32%.",chk=(100*(1-.85*.8),32))
QB(s,"Percentages","Medium","In an election between two candidates the winner got 55% of the votes cast and won by 1,200 votes. How many votes were cast in all?",["10,000","12,000","15,000","14,400"],"12,000","The winner got 55% and the loser 45%, a margin of 10% of the votes. 10% of the total = 1,200, so the total = 12,000.",chk=(1200/0.10,12000))
QB(s,"Permutations & Combinations","Medium","In how many ways can 5 people be seated in a row if two particular people must sit together?",["24","48","60","72"],"48","Treat the two people as one block. 4 units can be arranged in 4! = 24 ways, and the two can swap inside the block in 2 ways. Total = 24 × 2 = 48.",chk=(2*math.factorial(4),48))
QB(s,"Profit & Loss","Medium","A shopkeeper marks an article 20% above its cost price and then allows a discount of 10%. What is his profit percentage?",["8%","10%","12%","6%"],"8%","Take cost = 100. Marked price = 120. Selling price = 120 × 0.90 = 108. Profit = 8%.",chk=((1.2*.9-1)*100,8))
QB(s,"Profit & Loss","Hard","A trader sells two articles at ₹1,200 each. On one he gains 20% and on the other he loses 20%. What is his overall result?",["No overall change","4% loss","4% profit","2% loss"],"4% loss","The first cost 1,200/1.2 = ₹1,000. The second cost 1,200/0.8 = ₹1,500. Total cost = ₹2,500 and total sale = ₹2,400, a loss of ₹100, which is 4% of 2,500.",chk=((2500-2400)/2500*100,4))
QB(s,"Simple & Compound Interest","Easy","What is the simple interest on ₹5,000 at 8% per annum for 3 years?",["₹1,000","₹1,200","₹1,400","₹1,600"],"₹1,200","SI = P × R × T / 100 = 5,000 × 8 × 3 / 100 = ₹1,200.",chk=(5000*8*3/100,1200))
QB(s,"Simple & Compound Interest","Medium","What is the difference between the compound interest and the simple interest on ₹10,000 for 2 years at 10% per annum?",["₹50","₹100","₹110","₹200"],"₹100","For 2 years the difference = P × (R/100)² = 10,000 × (0.1)² = ₹100.",chk=(10000*1.1**2-10000-10000*.1*2,100))
QB(s,"Simple & Compound Interest","Hard","A sum of money doubles itself in 5 years at simple interest. In how many years will it become four times itself?",["10 years","12 years","15 years","20 years"],"15 years","Doubling in 5 years means the interest in 5 years equals the principal, so the interest per year is P/5. To reach 4P the interest must be 3P, which takes 3 × 5 = 15 years.",chk=(3*5,15))
QB(s,"Ratio & Proportion","Medium","If A : B = 3 : 4 and B : C = 6 : 5, what is A : B : C?",["9 : 12 : 10","3 : 4 : 5","9 : 8 : 10","6 : 8 : 5"],"9 : 12 : 10","Make B equal in both ratios. A : B = 3 : 4 = 9 : 12 and B : C = 6 : 5 = 12 : 10. So A : B : C = 9 : 12 : 10.",chk=(F(3,4)*F(12,1),9))
QB(s,"Averages & Alligation","Easy","The average of five numbers is 24. When one number is removed, the average of the remaining four becomes 22. What is the number removed?",["30","32","34","36"],"32","Sum of five = 5 × 24 = 120. Sum of four = 4 × 22 = 88. The removed number = 120 − 88 = 32.",chk=(5*24-4*22,32))
QB(s,"Averages & Alligation","Medium","In what ratio should rice costing ₹40 per kg be mixed with rice costing ₹60 per kg to get a mixture worth ₹48 per kg?",["2 : 3","3 : 2","1 : 2","4 : 3"],"3 : 2","By alligation, cheaper : dearer = (60 − 48) : (48 − 40) = 12 : 8 = 3 : 2.",chk=((60-48)/(48-40),1.5))
QB(s,"Time & Work","Easy","A can complete a job in 10 days and B in 15 days. Working together, in how many days will they finish it?",["5 days","6 days","7.5 days","8 days"],"6 days","Together they do 1/10 + 1/15 = 5/30 = 1/6 of the job per day, so they take 6 days.",chk=(1/(1/10+1/15),6))
QB(s,"Time & Work","Medium","A and B together can finish a job in 12 days. A alone can finish it in 20 days. In how many days can B alone finish it?",["28 days","30 days","32 days","36 days"],"30 days","B's daily work = 1/12 − 1/20 = 5/60 − 3/60 = 2/60 = 1/30, so B alone takes 30 days.",chk=(1/(1/12-1/20),30))
QB(s,"Time, Speed & Distance","Easy","A train 150 m long passes a pole in 10 seconds. What is its speed?",["45 km/h","54 km/h","60 km/h","72 km/h"],"54 km/h","Speed = 150/10 = 15 m/s. In km/h that is 15 × 18/5 = 54 km/h.",chk=(150/10*3.6,54))
QB(s,"Time, Speed & Distance","Medium","A man goes 60 km at 30 km/h and returns the same 60 km at 20 km/h. What is his average speed for the whole trip?",["24 km/h","25 km/h","26 km/h","22.5 km/h"],"24 km/h","Total distance = 120 km. Time = 60/30 + 60/20 = 2 + 3 = 5 hours. Average speed = 120/5 = 24 km/h.",chk=(120/(60/30+60/20),24))
QB(s,"Time, Speed & Distance","Hard","Two trains of length 120 m and 180 m run in opposite directions at 54 km/h and 36 km/h. How long do they take to cross each other?",["10 s","12 s","15 s","18 s"],"12 s","Relative speed = 54 + 36 = 90 km/h = 25 m/s. Distance to cover = 120 + 180 = 300 m. Time = 300/25 = 12 s.",chk=(300/(90/3.6),12))
QB(s,"Number System","Medium","What is the remainder when 2^50 is divided by 7?",["1","2","4","6"],"4","Powers of 2 repeat their remainders modulo 7 in a cycle of 3: 2, 4, 1. Since 50 = 3 × 16 + 2, the remainder is the 2nd in the cycle, which is 4.",chk=(pow(2,50,7),4))
QB(s,"Algebra","Easy","If x + 1/x = 5, what is the value of x² + 1/x²?",["21","23","25","27"],"23","Square both sides: x² + 2 + 1/x² = 25, so x² + 1/x² = 23.",chk=(5**2-2,23))
QB(s,"Geometry & Mensuration","Medium","The circumference of a circle is 44 cm. What is its area? (Take π = 22/7)",["144 cm²","154 cm²","164 cm²","176 cm²"],"154 cm²","2πr = 44 gives r = 44 × 7/(2 × 22) = 7 cm. Area = πr² = 22/7 × 49 = 154 cm².",chk=(22/7*7*7,154))
QB(s,"Probability","Medium","A bag has 4 red and 6 blue balls. Two balls are drawn at random without replacement. What is the probability that both are red?",["2/15","4/25","1/5","3/10"],"2/15","Favourable = 4C2 = 6. Total = 10C2 = 45. Probability = 6/45 = 2/15.",chk=(comb(4,2)/comb(10,2),2/15))

s = "reasoning"
QB(s,"Syllogisms","Medium","Statements: Some pens are books. All books are tables.<br>Conclusions: I. Some pens are tables II. All tables are books",SY,"Only I follows","The pens that are books are also tables, so some pens are tables (I). Nothing says every table is a book, so II does not follow.")
QB(s,"Syllogisms","Medium","Statements: Some A are B. Some B are C.<br>Conclusions: I. Some A are C II. Some C are A",SY,"Neither follows","Two 'some' statements do not connect A and C: the A's that are B may not be the B's that are C. Neither conclusion follows.")
QB(s,"Syllogisms","Hard","Statements: No doctor is a teacher. All teachers are writers.<br>Conclusions: I. Some writers are not doctors II. No writer is a doctor",SY,"Only I follows","Teachers are writers and no teacher is a doctor, so those writers are not doctors (I). Other writers may still be doctors, so II does not follow.")
QB(s,"Number & Letter Series","Easy","Find the next number: 3, 6, 12, 24, ?",["36","42","48","54"],"48","Each term is double the previous one, so the next is 24 × 2 = 48.")
QB(s,"Number & Letter Series","Medium","Find the next number: 2, 6, 12, 20, 30, ?",["40","42","44","46"],"42","The terms are 1×2, 2×3, 3×4, 4×5, 5×6, so the next is 6 × 7 = 42.")
QB(s,"Number & Letter Series","Medium","Find the next letter: B, E, H, K, ?",["L","M","N","O"],"N","Each letter is 3 places after the previous one: B(2), E(5), H(8), K(11), so the next is the 14th letter, N.")
QB(s,"Coding-Decoding","Easy","In a certain code, CAT is written as DBU. How is DOG written in that code?",["EPH","EPG","DPH","FPI"],"EPH","Each letter is moved one place forward: C→D, A→B, T→U. So D→E, O→P, G→H, giving EPH.")
QB(s,"Coding-Decoding","Medium","In a certain code, PEN is written as QGQ. How is BAG written in that code?",["CCJ","CBJ","CCH","DCJ"],"CCJ","The 1st, 2nd and 3rd letters are moved forward by 1, 2 and 3 places: P→Q, E→G, N→Q. So B→C, A→C, G→J, giving CCJ.")
QB(s,"Blood Relations","Easy","Pointing to a man, a woman says, 'His mother is the only daughter of my mother.' How is the woman related to the man?",["Sister","Mother","Aunt","Grandmother"],"Mother","The only daughter of the woman's mother is the woman herself. So the man's mother is the woman, and she is his mother.")
QB(s,"Blood Relations","Medium","A is B's brother. C is A's father. D is C's father. E is B's son. How is D related to E?",["Grandfather","Great-grandfather","Uncle","Father"],"Great-grandfather","C is the father of both A and B. D is C's father, so D is B's grandfather. E is B's son, so D is E's great-grandfather.")
QB(s,"Direction Sense","Easy","A man walks 5 km north, then 3 km east, and then 5 km south. How far is he from the starting point and in which direction?",["3 km east","3 km west","5 km north","8 km east"],"3 km east","The north and south walks cancel out. Only the 3 km east remains, so he is 3 km east of the start.")
QB(s,"Direction Sense","Medium","A person walks 10 m south, turns right and walks 20 m, turns right and walks 10 m, then turns left and walks 5 m. How far is he from the starting point and in which direction?",["25 m west","25 m east","20 m west","15 m west"],"25 m west","South 10 m, then right (west) 20 m, then right (north) 10 m brings him back to the start's latitude, 20 m west. Turning left from north is west, so 5 m more makes 25 m west of the start.")
QB(s,"Clocks & Calendars","Medium","What is the angle between the hands of a clock at 3:30?",["60°","75°","90°","105°"],"75°","At 3:30 the hour hand is at 3 × 30 + 30 × 0.5 = 105°. The minute hand is at 30 × 6 = 180°. The angle = 180 − 105 = 75°.")
QB(s,"Clocks & Calendars","Medium","If 1 January 2024 was a Monday, on which day was 1 January 2025?",["Tuesday","Wednesday","Thursday","Monday"],datetime.date(2025,1,1).strftime("%A"),"2024 is a leap year with 366 days = 52 weeks + 2 days. So 1 January 2025 falls 2 days after Monday, a Wednesday.")
assert datetime.date(2024,1,1).strftime("%A")=="Monday" and datetime.date(2025,1,1).strftime("%A")=="Wednesday"
QB(s,"Alphabet Test","Easy","Which letter is the 5th to the right of the 12th letter from the left in the English alphabet?",["P","Q","R","O"],AL[11+5],"The 12th letter is L. Counting 5 places to the right gives the 17th letter, Q.")
QB(s,"Alphabet Test","Medium","Which letter is exactly midway between G and S in the English alphabet?",["L","M","N","K"],AL[(6+18)//2],"G is the 7th letter and S is the 19th. The midpoint is the (7 + 19)/2 = 13th letter, M.")
QB(s,"Inequalities","Medium","Statements: P > Q ≥ R, R > S, T < Q.<br>Conclusions: I. P > S II. T < P",SY,"Both I and II follow","P > Q ≥ R > S gives P > S (I). T < Q and Q < P give T < P (II). Both follow.")
QB(s,"Inequalities","Hard","Statements: A ≥ B > C, D < C, A = E.<br>Conclusions: I. E > D II. B ≥ E",SY,"Only I follows","A ≥ B > C > D gives A > D, and E = A, so E > D (I). B ≥ E would mean B ≥ A, but A ≥ B; they could differ, so II does not follow.")
QB(s,"Ranking & Order","Medium","In a row of 40 students, Rahul is 15th from the left. What is his position from the right?",["24th","25th","26th","27th"],"26th","Position from the right = 40 − 15 + 1 = 26.",chk=(40-15+1,26))
sd=[p for p in itertools.permutations("PQRST") if {p[0],p[4]}=={"R","T"} and p.index("Q")==p.index("P")+1 and p.index("Q")!=2]
assert len(sd)==2 and all(p[2]=="P" for p in sd)
QB(s,"Seating Arrangement","Medium","Five friends P, Q, R, S and T sit in a row facing north. R and T sit at the two ends. P sits immediately to the left of Q. Q does not sit in the middle. Who sits in the middle?",["P","Q","S","T"],"P","R and T occupy the ends, so P, Q and S fill the three middle seats. P is immediately left of Q, which gives S P Q or P Q S. In P Q S, Q is in the middle, which is not allowed. So the order is S P Q and P sits in the middle.")

s = "dilr"
ex={"Exam P":[400,450,500,600],"Exam Q":[300,360,420,480],"Exam R":[200,220,330,300]}; ey=[2022,2023,2024,2025]
etot=[sum(v[i] for v in ex.values()) for i in range(4)]
ETAB="<b>Applicants for three bank recruitment exams (thousands)</b><table class='data'><tr><th>Exam</th>"+"".join(f"<th>{y}</th>" for y in ey)+"</tr>"+"".join(f"<tr><td>{k}</td>"+"".join(f"<td>{x}</td>" for x in v)+"</tr>" for k,v in ex.items())+"</table>"
T="Tables"; SE="table-exams"
QB(s,T,"Easy","How many thousand applicants were there in total across the three exams in 2024?",["1,150","1,250","1,300","1,380"],"1,250","2024: 500 + 420 + 330 = 1,250 thousand.",ETAB,SE,chk=(etot[2],1250))
QB(s,T,"Easy","What is the percentage increase in Exam P's applicants from 2022 to 2025?",["40%","50%","60%","75%"],"50%","(600 − 400)/400 = 200/400 = 50%.",ETAB,SE,chk=((600-400)/400*100,50))
gr={y:(ex["Exam R"][i]-ex["Exam R"][i-1])/ex["Exam R"][i-1] for i,y in enumerate(ey) if i}; assert max(gr,key=gr.get)==2024
QB(s,T,"Medium","In which year did Exam R's applicants show the highest percentage increase over the previous year?",["2023","2024","2025","Same in two years"],"2024","2023: 20/200 = 10%. 2024: 110/220 = 50%. 2025: a fall of 30. So 2024 is the highest.",ETAB,SE)
QB(s,T,"Medium","What is the ratio of Exam Q's applicants in 2025 to Exam R's applicants in 2023?",["24 : 11","12 : 11","2 : 1","16 : 7"],"24 : 11","480 : 220 = 48 : 22 = 24 : 11.",ETAB,SE,chk=(F(480,220),F(24,11)))
ptot=sum(ex["Exam P"]); gtot=sum(etot); assert (ptot,gtot)==(1950,4560)
QB(s,T,"Hard","Over 2022–2025, what percentage of the combined applicants of all three exams belonged to Exam P?",["38.5%","40.2%","42.8%","45.0%"],"42.8%","Exam P total = 400 + 450 + 500 + 600 = 1,950. All exams = 1,950 + 1,560 + 1,050 = 4,560. Share = 1,950/4,560 = 42.8%.",ETAB,SE,chk=(round(ptot/gtot*100,1),42.8))
br=[("Lucknow",120),("Kanpur",90),("Varanasi",150),("Prayagraj",60),("Agra",80)]; bv=dict(br); bt=sum(bv.values()); assert bt==500
BBAR="<b>Loan applications received by five bank branches in a month</b><div class='bars'>"+"".join(f"<div class='bar-row'><span>{c}</span><i style='width:{v/150*100:.1f}%'></i><span>{v}</span></div>" for c,v in br)+"</div>"
T="Bar Charts"; SB="bar-branches"
QB(s,T,"Easy","How many applications did the five branches receive in total?",["480","500","520","540"],"500","120 + 90 + 150 + 60 + 80 = 500.",BBAR,SB,chk=(bt,500))
QB(s,T,"Easy","Varanasi's applications are what percentage of the total?",["28%","30%","32%","35%"],"30%","Varanasi received 150 of the 500 applications in total, so its share is 150/500 = 30%.",BBAR,SB,chk=(150/bt*100,30))
QB(s,T,"Medium","How many branches received more applications than the five-branch average?",["1","2","3","4"],str(sum(1 for v in bv.values() if v>bt/5)),"Average = 500/5 = 100. Lucknow (120) and Varanasi (150) are above it, so 2 branches.",BBAR,SB)
QB(s,T,"Medium","By what percentage are Kanpur's applications less than Lucknow's?",["20%","25%","30%","33.3%"],"25%","(120 − 90)/120 = 30/120 = 25%.",BBAR,SB,chk=((120-90)/120*100,25))
QB(s,T,"Hard","If Prayagraj's applications double and Agra's fall by 25%, what is the new total for the five branches?",["520","530","540","550"],"540","Prayagraj becomes 120 (+60). Agra becomes 80 × 0.75 = 60 (−20). New total = 500 + 60 − 20 = 540.",BBAR,SB,chk=(bt+60-20,540))

# ======================= BANK / SSC EXPANSION 2 (+100: 40 Quant, 40 Reasoning, 20 DILR) =======================
s = "quant"
_pos = [t for _ in range(30) for t in range(4)]; _rnd.Random(23).shuffle(_pos); _pi = iter(_pos)
Q_=QB
Q_(s,"Percentages","Easy","What is 35% of 240?",["80","84","88","96"],"84","35% of 240 = 35 × 240/100 = 84.",chk=(.35*240,84))
Q_(s,"Percentages","Medium","A number is increased by 30% and the result is then decreased by 10%. What is the net percentage change?",["20%","17%","3%","27%"],"17%","Take the number as 100. After +30%: 130. After −10% of 130: 130 − 13 = 117. The net change is a 17% increase.",chk=(100*1.3*.9-100,17))
Q_(s,"Percentages","Medium","A's income is 20% more than B's. By what percentage is B's income less than A's?",["20%","16.67%","15%","18%"],"16.67%","Let B = 100, so A = 120. B is less than A by 20/120 = 16.67%.",chk=(20/120*100,100/6))
Q_(s,"Percentages","Medium","In an exam 40% of the candidates failed. If 300 candidates passed, how many appeared?",["450","500","550","600"],"500","The pass percentage is 60%. 60% of the candidates = 300, so the total = 300/0.60 = 500.",chk=(300/.6,500))
Q_(s,"Percentages","Hard","The population of a town grows by 10% every year. Its present population is 21,780. What was it two years ago?",["17,500","18,000","18,500","19,000"],"18,000","Present = P × 1.1 × 1.1 = 1.21P. So P = 21,780/1.21 = 18,000.",chk=(21780/1.21,18000))
Q_(s,"Profit & Loss","Easy","An article bought for ₹480 is sold for ₹552. What is the profit percentage?",["12%","15%","18%","20%"],"15%","Profit = 552 − 480 = ₹72. Profit % = 72/480 × 100 = 15%.",chk=(72/480*100,15))
Q_(s,"Profit & Loss","Medium","A shopkeeper gives a discount of 12% on the marked price and still gains 10%. If the cost price is ₹800, what is the marked price?",["₹950","₹1,000","₹1,050","₹1,100"],"₹1,000","Selling price = 800 × 1.10 = ₹880. This is 88% of the marked price, so the marked price = 880/0.88 = ₹1,000.",chk=(880/.88,1000))
Q_(s,"Profit & Loss","Medium","By selling an article for ₹720 a man loses 10%. At what price should he sell it to gain 10%?",["₹800","₹860","₹880","₹900"],"₹880","720 is 90% of the cost, so cost = 720/0.9 = ₹800. For a 10% gain, selling price = 800 × 1.1 = ₹880.",chk=(720/.9*1.1,880))
Q_(s,"Profit & Loss","Hard","A sells an article to B at a 20% profit, and B sells it to C at a 25% profit. If C pays ₹1,500, what did it cost A?",["₹900","₹1,000","₹1,100","₹1,200"],"₹1,000","C's price = A's cost × 1.20 × 1.25 = 1.5 × A's cost. So A's cost = 1,500/1.5 = ₹1,000.",chk=(1500/(1.2*1.25),1000))
Q_(s,"Profit & Loss","Medium","Two successive discounts of 20% and 10% are equal to a single discount of:",["28%","30%","25%","32%"],"28%","Price after both = 0.80 × 0.90 = 0.72 of the marked price, so the single discount is 28%.",chk=((1-.8*.9)*100,28))
Q_(s,"Simple & Compound Interest","Easy","₹2,000 becomes ₹2,480 in 3 years at simple interest. What is the rate per annum?",["6%","8%","9%","10%"],"8%","Interest = 2,480 − 2,000 = ₹480. Rate = 480 × 100/(2,000 × 3) = 8%.",chk=(480*100/(2000*3),8))
Q_(s,"Simple & Compound Interest","Medium","What is the compound interest on ₹5,000 at 8% per annum for 2 years?",["₹800","₹832","₹864","₹900"],"₹832","Amount = 5,000 × 1.08 × 1.08 = ₹5,832. Compound interest = 5,832 − 5,000 = ₹832.",chk=(5000*1.08**2-5000,832))
Q_(s,"Simple & Compound Interest","Medium","A sum becomes ₹7,986 in 3 years at 10% per annum compound interest. What is the sum?",["₹5,800","₹6,000","₹6,200","₹6,500"],"₹6,000","Amount = P × 1.1³ = 1.331P. So P = 7,986/1.331 = ₹6,000.",chk=(7986/1.331,6000))
Q_(s,"Simple & Compound Interest","Hard","A sum lent at simple interest amounts to ₹1,200 in 2 years and ₹1,350 in 5 years. What is the sum?",["₹1,000","₹1,050","₹1,100","₹1,150"],"₹1,100","Interest for 3 years (years 2 to 5) = 1,350 − 1,200 = ₹150, so ₹50 a year. Interest for 2 years = ₹100, so the sum = 1,200 − 100 = ₹1,100.",chk=(1200-2*(1350-1200)/3,1100))
Q_(s,"Ratio & Proportion","Easy","₹2,400 is divided between A and B in the ratio 5 : 3. How much does A get?",["₹1,200","₹1,400","₹1,500","₹1,600"],"₹1,500","A's share = 5/8 × 2,400 = ₹1,500.",chk=(5/8*2400,1500))
Q_(s,"Ratio & Proportion","Medium","Two numbers are in the ratio 3 : 5. If 10 is added to each, the ratio becomes 5 : 7. What is the smaller number?",["9","12","15","18"],"15","Let the numbers be 3x and 5x. (3x + 10)/(5x + 10) = 5/7 gives 21x + 70 = 25x + 50, so x = 5. The smaller number = 15.",chk=(3*5,15))
Q_(s,"Ratio & Proportion","Medium","A 50-litre mixture has milk and water in the ratio 4 : 1. How much water must be added to make the ratio 2 : 1?",["8 L","10 L","12 L","15 L"],"10 L","Milk = 40 L and water = 10 L. For a 2 : 1 ratio the water must be 20 L, so add 10 L.",chk=(40/2-10,10))
Q_(s,"Averages & Alligation","Easy","What is the average of 11, 15, 19, 23 and 27?",["17","19","21","23"],"19","The numbers are evenly spaced, so the average is the middle number, 19. Check: 95/5 = 19.",chk=((11+15+19+23+27)/5,19))
Q_(s,"Averages & Alligation","Medium","The average weight of 20 students is 52 kg. When a new student joins, the average becomes 53 kg. What is the weight of the new student?",["70 kg","72 kg","73 kg","75 kg"],"73 kg","New total = 21 × 53 = 1,113 kg. Old total = 20 × 52 = 1,040 kg. The new student weighs 1,113 − 1,040 = 73 kg.",chk=(21*53-20*52,73))
Q_(s,"Averages & Alligation","Medium","Sugar costing ₹30 per kg is mixed with sugar costing ₹45 per kg in the ratio 2 : 3. What is the cost per kg of the mixture?",["₹36","₹38","₹39","₹40"],"₹39","Cost of 5 kg = 2 × 30 + 3 × 45 = 60 + 135 = ₹195. Per kg = 195/5 = ₹39.",chk=((2*30+3*45)/5,39))
Q_(s,"Time & Work","Easy","12 men can complete a work in 20 days. In how many days will 8 men complete it?",["24 days","28 days","30 days","32 days"],"30 days","Total work = 12 × 20 = 240 man-days. With 8 men, time = 240/8 = 30 days.",chk=(12*20/8,30))
Q_(s,"Time & Work","Medium","A, B and C can do a job alone in 10, 12 and 15 days respectively. In how many days will they finish it working together?",["3 days","4 days","5 days","6 days"],"4 days","Work per day = 1/10 + 1/12 + 1/15 = (6 + 5 + 4)/60 = 15/60 = 1/4. They finish in 4 days.",chk=(1/(1/10+1/12+1/15),4))
Q_(s,"Time & Work","Medium","Pipe A fills a tank in 12 hours and pipe B fills it in 15 hours. Pipe C empties it in 20 hours. If all three are opened together, how long will the empty tank take to fill?",["8 hours","10 hours","12 hours","15 hours"],"10 hours","Net rate = 1/12 + 1/15 − 1/20 = (5 + 4 − 3)/60 = 6/60 = 1/10. The tank fills in 10 hours.",chk=(1/(1/12+1/15-1/20),10))
Q_(s,"Time, Speed & Distance","Easy","A car travelling at 45 km/h covers a distance of 270 km. How long does it take?",["5 hours","6 hours","7 hours","8 hours"],"6 hours","Time = distance/speed = 270/45 = 6 hours.",chk=(270/45,6))
Q_(s,"Time, Speed & Distance","Medium","A boat's speed in still water is 10 km/h and the stream flows at 2 km/h. How long does it take to go 24 km downstream and return 24 km upstream?",["4 hours","5 hours","6 hours","7.5 hours"],"5 hours","Downstream speed = 12 km/h, so 24/12 = 2 hours. Upstream speed = 8 km/h, so 24/8 = 3 hours. Total = 5 hours.",chk=(24/12+24/8,5))
Q_(s,"Time, Speed & Distance","Medium","A walks at 5 km/h. Two hours later B starts from the same point in the same direction at 7 km/h. How many hours after B starts will B catch A?",["4 hours","5 hours","6 hours","7 hours"],"5 hours","A has a head start of 5 × 2 = 10 km. B gains 7 − 5 = 2 km every hour, so B catches A in 10/2 = 5 hours.",chk=(10/2,5))
Q_(s,"Time, Speed & Distance","Hard","A train crosses a 200 m platform in 25 seconds and a pole in 15 seconds. What is the length of the train?",["250 m","300 m","350 m","400 m"],"300 m","Let the length be L and the speed v. v = L/15 and v = (L + 200)/25. So 25L = 15L + 3,000, which gives L = 300 m.",chk=(3000/10,300))
Q_(s,"Number System","Medium","What is the greatest number that divides 1,657 and 2,037 leaving remainders 6 and 5 respectively?",["113","121","127","131"],"127","The number divides 1,657 − 6 = 1,651 and 2,037 − 5 = 2,032. 1,651 = 13 × 127 and 2,032 = 16 × 127, so the HCF is 127 (which is larger than both remainders).",chk=(math.gcd(1651,2032),127))
Q_(s,"Number System","Medium","What is the unit digit of 8^35?",["2","4","6","8"],"2","The unit digits of powers of 8 repeat in a cycle of 4: 8, 4, 2, 6. Since 35 = 4 × 8 + 3, the unit digit is the 3rd in the cycle, 2.",chk=(pow(8,35,10),2))
Q_(s,"Algebra","Medium","The sum of two numbers is 24 and their product is 143. What is their difference?",["1","2","3","4"],"2","(a − b)² = (a + b)² − 4ab = 576 − 572 = 4, so the difference is 2. (The numbers are 13 and 11.)",chk=(math.sqrt(24**2-4*143),2))
Q_(s,"Algebra","Medium","If the roots of x² − 9x + 14 = 0 are a and b, what is a² + b²?",["49","51","53","55"],"53","a + b = 9 and ab = 14. a² + b² = (a + b)² − 2ab = 81 − 28 = 53.",chk=(9**2-2*14,53))
Q_(s,"Geometry & Mensuration","Medium","What is the area of a triangle whose sides are 13 cm, 14 cm and 15 cm?",["72 cm²","78 cm²","84 cm²","90 cm²"],"84 cm²","Semi-perimeter = 21. Area = √(21 × 8 × 7 × 6) = √7,056 = 84 cm².",chk=(math.sqrt(21*8*7*6),84))
Q_(s,"Geometry & Mensuration","Easy","The total surface area of a cube is 150 cm². What is its volume?",["100 cm³","125 cm³","150 cm³","216 cm³"],"125 cm³","6a² = 150 gives a² = 25, so a = 5 cm. Volume = 5³ = 125 cm³.",chk=(5**3,125))
Q_(s,"Geometry & Mensuration","Medium","What is the curved surface area of a cylinder of radius 7 cm and height 10 cm? (Take π = 22/7)",["340 cm²","400 cm²","440 cm²","480 cm²"],"440 cm²","Curved surface area = 2πrh = 2 × 22/7 × 7 × 10 = 440 cm².",chk=(2*22/7*7*10,440))
Q_(s,"Permutations & Combinations","Easy","How many 3-digit numbers can be formed from the digits 1, 2, 3, 4 and 5 if no digit is repeated?",["30","60","90","125"],"60","Choose and arrange 3 of the 5 digits: 5 × 4 × 3 = 60.",chk=(5*4*3,60))
Q_(s,"Permutations & Combinations","Medium","A committee of 3 is to be chosen from 5 men and 4 women, with at least one woman. In how many ways can this be done?",["64","74","84","94"],"74","All committees: 9C3 = 84. Committees with no woman: 5C3 = 10. With at least one woman: 84 − 10 = 74.",chk=(comb(9,3)-comb(5,3),74))
Q_(s,"Permutations & Combinations","Medium","In how many ways can the letters of the word BANANA be arranged?",["30","60","90","120"],"60","BANANA has 6 letters with A three times and N twice. Arrangements = 6!/(3! × 2!) = 720/12 = 60.",chk=(math.factorial(6)/(6*2),60))
Q_(s,"Probability","Easy","One card is drawn from a well-shuffled pack of 52 cards. What is the probability that it is a king or a queen?",["1/13","2/13","3/13","4/13"],"2/13","There are 4 kings and 4 queens, so 8 favourable cards. Probability = 8/52 = 2/13.",chk=(8/52,2/13))
Q_(s,"Probability","Medium","Two fair coins and one fair die are thrown together. What is the probability of getting two heads and an even number?",["1/8","1/6","1/4","1/12"],"1/8","P(two heads) = 1/4 and P(even number) = 1/2. They are independent, so the probability = 1/4 × 1/2 = 1/8.",chk=(.25*.5,1/8))
Q_(s,"Probability","Hard","Two fair dice are thrown. What is the probability that the sum is a multiple of 5?",["5/36","7/36","1/6","2/9"],"7/36","Sum 5: 4 ways (1,4), (2,3), (3,2), (4,1). Sum 10: 3 ways (4,6), (5,5), (6,4). Favourable = 7 out of 36, so the probability = 7/36.",chk=(sum(1 for a in range(1,7) for b in range(1,7) if (a+b)%5==0),7))

s = "reasoning"
Q_(s,"Syllogisms","Medium","Statements: All roses are flowers. All flowers are plants.<br>Conclusions: I. All roses are plants II. Some plants are roses",SY,"Both I and II follow","Roses ⊂ flowers ⊂ plants, so all roses are plants (I). Converting I gives some plants are roses (II). Both follow.")
Q_(s,"Syllogisms","Medium","Statements: Some cars are bikes. No bike is a bus.<br>Conclusions: I. Some cars are not buses II. No car is a bus",SY,"Only I follows","The cars that are bikes cannot be buses, so some cars are not buses (I). Other cars may still be buses, so II does not follow.")
Q_(s,"Syllogisms","Hard","Statements: All pencils are pens. Some pens are erasers.<br>Conclusions: I. Some pencils are erasers II. Some erasers are pens",SY,"Only II follows","Converting 'some pens are erasers' gives some erasers are pens (II). The pens that are erasers may not be pencils, so I does not follow.")
Q_(s,"Syllogisms","Hard","Statements: Some tables are chairs. All chairs are wooden. Some wooden things are boxes.<br>Conclusions: I. Some tables are wooden II. Some chairs are boxes",SY,"Only I follows","The tables that are chairs are also wooden, so some tables are wooden (I). 'Some wooden things are boxes' does not connect boxes to chairs, so II does not follow.")
sq=[p for p in itertools.permutations("ABCDE") if p.index("A")==1 and p.index("C")==2 and p.index("B") in (0,4) and abs(p.index("D")-p.index("C"))>1 and p.index("E")>p.index("D")]
assert len(sq)==1 and sq[0][4]=="B"
Q_(s,"Seating Arrangement","Medium","Five friends A, B, C, D and E sit in a row facing north. A sits second from the left end. C sits immediately to the right of A. B sits at one of the ends. D does not sit next to C. E sits somewhere to the right of D. Who sits at the extreme right end?",["A","B","C","E"],"B","A is 2nd and C is 3rd. D cannot sit next to C, so D is not 4th, and the 2nd seat is taken, so D is in the 1st or 5th seat. E sits to the right of D, so D cannot be 5th. D is 1st. B must be at an end, so B is 5th and E is 4th: D A C E B. B sits at the extreme right.")
c6=[p for p in itertools.permutations("PQRSTU") if p[0]=="P" and ((p.index("R")-p.index("P"))%6 in (1,5)) and ((p.index("R")-p.index("T"))%6 in (1,5)) and ((p.index("U")-p.index("R"))%6==3) and ((p.index("S")-p.index("P"))%6 not in (1,5))]
assert len(c6)==2 and all(p[3]=="S" for p in c6)
Q_(s,"Seating Arrangement","Hard","Six persons P, Q, R, S, T and U sit around a circular table, equally spaced and facing the centre. R sits between P and T. U sits opposite R. S is not next to P. Who sits opposite P?",["Q","S","T","U"],"S","R sits between P and T, so P and T are R's two neighbours. Number the seats 1 to 6 around the table with P in seat 1, R in seat 2, T in seat 3 and U opposite R in seat 5. Seats 4 and 6 are left for Q and S. Seat 6 is next to P and S cannot be next to P, so S takes seat 4, directly opposite P. The mirror-image arrangement gives the same result.")
fl=[p for p in itertools.permutations("ABCDEF") if (p.index("B")+1)%2==0 and p.index("B")>p.index("C") and p.index("E")==p.index("D")+1 and p.index("A")==0 and p.index("F")>p.index("E")]
assert len(fl)==3 and all(p[5]=="B" for p in fl)
Q_(s,"Seating Arrangement","Medium","Six persons A to F live on six different floors of a building (1 is the lowest, 6 the highest). A lives on floor 1. B lives on an even-numbered floor above C. D lives immediately below E. F lives above E. Who lives on the top floor?",["C","D","E","B"],"B","A is on floor 1. F is above E and E is above D, so F, E and D are three of floors 2 to 6, and F cannot be on floor 6 if B is to sit on an even floor above C with room left for the D-E pair. Checking every arrangement that fits all four clues, B always ends up on floor 6, the top floor.")
Q_(s,"Blood Relations","Easy","A's mother is B's sister. How is A related to B?",["Nephew or niece","Cousin","Brother or sister","Uncle"],"Nephew or niece","B's sister is A's mother, so B is A's maternal uncle or aunt. A is B's nephew or niece.")
Q_(s,"Blood Relations","Medium","Pointing to a photograph, Ravi says, 'She is the daughter of my grandfather's only son.' How is she related to Ravi?",["Cousin","Sister","Aunt","Niece"],"Sister","Ravi's grandfather's only son is Ravi's father. The daughter of Ravi's father is Ravi's sister.")
Q_(s,"Blood Relations","Medium","X is Y's father. Z is X's sister. W is Z's son. How is W related to Y?",["Brother","Uncle","Cousin","Nephew"],"Cousin","Z is Y's paternal aunt. Z's son W is the child of Y's aunt, so W is Y's cousin.")
Q_(s,"Coding-Decoding","Easy","In a certain code, STONE is written as RSNMD. How is PLATE written in that code?",["OKZSD","OKZSF","QMBUF","OLZSD"],"OKZSD","Each letter is moved one place back: S→R, T→S, O→N, N→M, E→D. So P→O, L→K, A→Z, T→S, E→D, giving OKZSD.")
Q_(s,"Coding-Decoding","Medium","In a certain code, 'pen ink' is written as 'ta ma', 'ink pot' as 'ma ki' and 'pot cup' as 'ki lo'. How is 'pen' written in that code?",["ta","ma","ki","lo"],"ta","'ink' is common to the first two statements and 'ma' is common to the two codes, so ink = ma. Then pen = ta.")
Q_(s,"Coding-Decoding","Hard","If MADRAS is coded as NBESBT, how is BOMBAY coded?",["CPNCBZ","CPNCBX","CPMCBZ","DPNCBZ"],"CPNCBZ","Each letter is moved one place forward: M→N, A→B, D→E, R→S, A→B, S→T. So B→C, O→P, M→N, B→C, A→B, Y→Z, giving CPNCBZ.")

# --- seating (unique, brute-forced)
ed=[p for p in itertools.permutations(range(5)) if p[2]==p[1]+1 and p[3] in (1,2,3) and p[4]>p[3] and p[0]<p[1] and p[4]!=4]
assert len(ed)==1 and ed[0]==(0,3,4,1,2)
Q_(s,"Seating Arrangement","Hard","Five exams P, Q, R, S and T are held on five consecutive days, Monday to Friday, one exam a day. R is held the day right after Q. P is held before Q. S is held on Tuesday, Wednesday or Thursday. T is held after S but not on Friday. Which exam is held on Wednesday?",["P","Q","S","T"],"T","Q and R are consecutive days with P earlier. If Q is Tuesday, P is Monday, S and T fill Thursday and Friday, which forces T onto Friday. If Q is Wednesday, S must be Tuesday and T Friday, again not allowed. So Q is Thursday and R is Friday. P, S and T take Monday to Wednesday with S before T: S is Tuesday, T is Wednesday and P is Monday.")
# --- puzzles
Q_(s,"Puzzles","Easy","The sum of the ages of a father and his son is 50 years. Five years ago the father was four times as old as the son. What is the son's present age?",["11 years","12 years","13 years","14 years"],"13 years","Let the son be s now, so the father is 50 − s. Five years ago: 50 − s − 5 = 4(s − 5), so 45 − s = 4s − 20 and 5s = 65, giving s = 13.",chk=(65/5,13))
Q_(s,"Puzzles","Medium","Among five boxes P, Q, R, S and T: P is heavier than Q but lighter than R. S is heavier than R. T is lighter than Q. Which box is the second heaviest?",["P","Q","R","S"],"R","From the clues S > R > P > Q > T. The second heaviest is R.")
cl=["red","blue","green","yellow"]; cs=[p for p in itertools.permutations(range(4)) if p[0] not in (0,1) and p[1] not in (1,2) and p[2] not in (0,3,2) and p[3] not in (2,3)]
assert len(cs)==1 and cl[cs[0][3]]=="red"
Q_(s,"Puzzles","Hard","Four friends A, B, C and D each like a different colour out of red, blue, green and yellow. A likes neither red nor blue. B likes neither blue nor green. C likes neither red, green nor yellow. D likes neither green nor yellow. Who likes red?",["A","B","C","D"],"D","C can like only blue. Then A (not red, not blue) must like green or yellow, and B (not blue, not green) must like red or yellow. D (not green, not yellow) must like red or blue, and blue is taken, so D likes red. B then likes yellow and A likes green.")
# --- direction sense
Q_(s,"Direction Sense","Easy","A man walks 10 m west, turns left and walks 6 m, turns left and walks 10 m, then turns right and walks 4 m. How far and in which direction is he from the starting point?",["10 m south","10 m north","6 m south","14 m south"],"10 m south","Take the start as (0, 0). West 10 m: (−10, 0). Left (south) 6 m: (−10, −6). Left (east) 10 m: (0, −6). Right (south) 4 m: (0, −10). He is 10 m south of the start.")
Q_(s,"Direction Sense","Medium","Rohan faces north, turns 90° to his right and then 135° to his left. Which direction is he facing now?",["North-East","North-West","South-West","South-East"],"North-West","Facing north, 90° right is east. Turning 135° left (anticlockwise) from east passes north and ends 45° beyond it, which is north-west.")
Q_(s,"Direction Sense","Medium","Rohan walks 8 km south, turns left and walks 6 km, then turns left again and walks 8 km. How far and in which direction is he from his starting point?",["6 km east","6 km west","8 km east","10 km east"],"6 km east","Facing south, a left turn points east, so he goes 6 km east. Another left turn points north, and the 8 km north cancels the 8 km south. He ends 6 km east of the start.")
# --- series
Q_(s,"Number & Letter Series","Medium","Find the next term: 3, 8, 18, 38, 78, ?",["148","156","158","162"],"158","Each term is double the previous term plus 2: 78 × 2 + 2 = 158.",chk=(78*2+2,158))
Q_(s,"Number & Letter Series","Medium","Find the next term: 5, 11, 23, 47, 95, ?",["181","189","191","193"],"191","Each term is double the previous term plus 1: 95 × 2 + 1 = 191.",chk=(95*2+1,191))
Q_(s,"Number & Letter Series","Easy","Find the next term: 1, 3, 7, 13, 21, ?",["29","31","33","35"],"31","The differences are 2, 4, 6, 8, so the next difference is 10: 21 + 10 = 31.",chk=(21+10,31))
Q_(s,"Number & Letter Series","Hard","Find the next term: 120, 99, 80, 63, 48, ?",["33","35","37","39"],"35","The differences are 21, 19, 17, 15, so the next difference is 13: 48 − 13 = 35.",chk=(48-13,35))
# --- odd one out
Q_(s,"Odd One Out","Easy","Find the odd one out: 16, 25, 36, 49, 50",["16","25","49","50"],"50","16, 25, 36 and 49 are perfect squares (4², 5², 6², 7²). 50 is not.")
Q_(s,"Odd One Out","Easy","Find the odd one out: Mercury, Venus, Moon, Mars, Jupiter",["Mercury","Venus","Moon","Jupiter"],"Moon","Mercury, Venus, Mars and Jupiter are planets. The Moon is a satellite of the Earth.")
Q_(s,"Odd One Out","Medium","Find the odd one out: 14, 21, 35, 49, 52",["14","35","49","52"],"52","14, 21, 35 and 49 are multiples of 7. 52 is not.",chk=(52%7,3))
# --- clocks and calendars
Q_(s,"Clocks & Calendars","Medium","What is the angle between the hands of a clock at 7:20?",["90°","100°","110°","120°"],"100°","At 7:20 the hour hand is at 7 × 30 + 20 × 0.5 = 220°. The minute hand is at 20 × 6 = 120°. The angle is 220 − 120 = 100°.",chk=(abs((7*30+20*.5)-120),100))
assert datetime.date(2026,8,15).strftime("%A")=="Saturday" and datetime.date(2027,1,26).strftime("%A")=="Tuesday"
Q_(s,"Clocks & Calendars","Medium","If 15 August 2026 is a Saturday, what day of the week is 26 January 2027?",["Sunday","Monday","Tuesday","Wednesday"],"Tuesday","From 15 August to 26 January: 16 (rest of August) + 30 + 31 + 30 + 31 + 26 = 164 days. 164 = 7 × 23 + 3, so move 3 days forward from Saturday: Tuesday.",chk=((datetime.date(2027,1,26)-datetime.date(2026,8,15)).days,164))
Q_(s,"Clocks & Calendars","Hard","How many times do the hour hand and the minute hand of a clock overlap in 12 hours?",["10","11","12","13"],"11","The hands overlap every 12/11 hours, so in 12 hours they overlap 11 times (the 12 o'clock overlap counts once for 11 and 12).")
# --- alphabet
Q_(s,"Alphabet Test","Easy","How many letters are there between G and R in the English alphabet?",["9","10","11","12"],"10","G is the 7th letter and R is the 18th. The letters between are 18 − 7 − 1 = 10.",chk=(18-7-1,10))
Q_(s,"Alphabet Test","Medium","Which letter is exactly as far from the end of the alphabet as K is from the beginning?",["O","P","Q","R"],"P","K is the 11th letter from the left. The letter 11th from the right is 27 − 11 = 16th from the left, which is P.",chk=(27-11,16))
Q_(s,"Alphabet Test","Medium","If the letters of the word BRIGHT are arranged in alphabetical order, which letter is third from the left?",["G","H","I","R"],"H","Alphabetical order: B, G, H, I, R, T. The third letter is H.")
# --- inequalities
Q_(s,"Inequalities","Medium","Statements: A ≤ B < C = D > E<br>Conclusions: I. A < D II. B < E",SY,"Only I follows","A ≤ B < C = D, so A < D (I follows). B and E are both below D but nothing links them, so II does not follow.")
Q_(s,"Inequalities","Medium","Statements: J ≥ K > L = M ≥ N<br>Conclusions: I. J = M II. N ≤ K",SY,"Only II follows","J ≥ K > L = M, so J > M and I (J = M) is false. K > L = M ≥ N gives K > N, so N ≤ K holds (II follows).")
Q_(s,"Inequalities","Hard","Statements: F < G ≤ H = I < J<br>Conclusions: I. G < J II. F ≤ H",SY,"Both I and II follow","G ≤ H = I < J gives G < J (I). F < G ≤ H gives F < H, so F ≤ H (II). Both follow.")
# --- ranking
Q_(s,"Ranking & Order","Easy","In a row of 40 students, Anil is 12th from the left and Sunil is 15th from the right. How many students are between them?",["12","13","14","15"],"13","Sunil is 40 − 15 + 1 = 26th from the left. Students between = 26 − 12 − 1 = 13.",chk=(26-12-1,13))
Q_(s,"Ranking & Order","Easy","Sanjay ranks 11th from the top and 29th from the bottom in a class. How many students are there in the class?",["38","39","40","41"],"39","Total = 11 + 29 − 1 = 39.",chk=(11+29-1,39))
Q_(s,"Ranking & Order","Medium","In a class of 35, Priya is 12th from the top and Neha is 9th from the bottom. How many students are between them?",["12","13","14","15"],"14","Neha is 35 − 9 + 1 = 27th from the top. Between them: 27 − 12 − 1 = 14.",chk=(27-12-1,14))
# --- coding
Q_(s,"Coding-Decoding","Medium","In a certain code, each word is coded as the sum of the position values of its letters (A = 1, B = 2, … Z = 26). PEN is coded as 35. How is INK coded?",["32","33","34","36"],"34","PEN = 16 + 5 + 14 = 35, which confirms the rule. INK = 9 + 14 + 11 = 34.",chk=(9+14+11,34))

# ================= DILR sets =================
s = "dilr"
bx={"Salaries":40,"Rent":15,"Technology":20,"Marketing":10,"Others":15}; assert sum(bx.values())==100
cols=["#4f46e5","#0891b2","#db2777","#f59e0b","#16a34a"]; acc=0; segs=[]
for (k,v),c in zip(bx.items(),cols):
    segs.append(f"{c} {acc}% {acc+v}%"); acc+=v
PIE2="<b>Annual expenditure of a bank branch (total ₹80 lakh)</b><div class='pie-wrap'><div class='pie' style='background:conic-gradient("+",".join(segs)+")'></div><div class='pie-legend'>"+"".join(f"<div><i style='background:{c}'></i>{k} {v}%</div>" for (k,v),c in zip(bx.items(),cols))+"</div></div>"
T="Pie Charts"; SP="pie-branch-exp"
Q_(s,T,"Easy","How much does the branch spend on technology in a year?",["₹12 lakh","₹14 lakh","₹16 lakh","₹18 lakh"],"₹16 lakh","20% of ₹80 lakh = ₹16 lakh.",PIE2,SP,chk=(80*.2,16))
Q_(s,T,"Easy","What is the central angle of the Salaries sector?",["120°","132°","144°","150°"],"144°","The Salaries sector is 40% of the whole circle. 40% of 360° = 0.4 × 360° = 144°.",PIE2,SP,chk=(.4*360,144))
Q_(s,T,"Medium","By how much does the spend on Salaries exceed the combined spend on Rent and Marketing?",["₹10 lakh","₹12 lakh","₹14 lakh","₹16 lakh"],"₹12 lakh","Salaries = 40%. Rent + Marketing = 15% + 10% = 25%. The difference is 15% of ₹80 lakh = ₹12 lakh.",PIE2,SP,chk=(80*.15,12))
Q_(s,T,"Medium","If the Marketing spend rises by 50% and every other item stays the same, what is the new total expenditure?",["₹82 lakh","₹84 lakh","₹86 lakh","₹88 lakh"],"₹84 lakh","Marketing = ₹8 lakh. A 50% rise adds ₹4 lakh, so the new total = 80 + 4 = ₹84 lakh.",PIE2,SP,chk=(80+80*.1*.5,84))
Q_(s,T,"Hard","Technology spend rises by 10% and Rent falls by 20%, with all else unchanged. What is the new total expenditure?",["₹78.4 lakh","₹79.2 lakh","₹80.8 lakh","₹81.6 lakh"],"₹79.2 lakh","Technology = ₹16 lakh, up by 1.6. Rent = ₹12 lakh, down by 2.4. Net change = −0.8, so the new total = 80 − 0.8 = ₹79.2 lakh.",PIE2,SP,chk=(80+1.6-2.4,79.2))

mo=["Jan","Feb","Mar","Apr","May","Jun"]; ac=[18,24,30,27,37,44]
def line2():
    W,H,px,py=360,170,36,20; mx=50
    X=lambda i: px+i*(W-px-14)/5; Y=lambda v: H-py-(v/mx)*(H-2*py)
    pts=" ".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(ac))
    grid="".join(f"<line x1='{px}' x2='{W-10}' y1='{Y(v):.1f}' y2='{Y(v):.1f}' stroke='#e2e8f0'/><text x='{px-6}' y='{Y(v)+4:.1f}' font-size='10' text-anchor='end' fill='#64748b'>{v}</text>" for v in range(0,51,10))
    lab="".join(f"<text x='{X(i):.1f}' y='{H-4}' font-size='10' text-anchor='middle' fill='#64748b'>{m}</text>" for i,m in enumerate(mo))
    dots="".join(f"<circle cx='{X(i):.1f}' cy='{Y(v):.1f}' r='3.5' fill='#0891b2'/><text x='{X(i):.1f}' y='{Y(v)-8:.1f}' font-size='10' text-anchor='middle' fill='#0f172a'>{v}</text>" for i,v in enumerate(ac))
    return f"<b>New savings accounts opened at a bank each month, 2026 (in hundreds)</b><svg viewBox='0 0 {W} {H}' style='width:100%;max-width:420px;display:block'>{grid}<polyline points='{pts}' fill='none' stroke='#0891b2' stroke-width='2.5'/>{dots}{lab}</svg>"
LN2=line2(); T="Line Graphs"; SL="line-accounts"
Q_(s,T,"Easy","How many accounts (in hundreds) were opened from January to June in total?",["170","175","180","185"],"180","18 + 24 + 30 + 27 + 37 + 44 = 180 hundred.",LN2,SL,chk=(sum(ac),180))
Q_(s,T,"Easy","In which month did the number of new accounts fall compared with the previous month?",["February","March","April","May"],"April","Accounts rose in Feb, Mar, May and Jun. In April they fell from 30 to 27.",LN2,SL)
Q_(s,T,"Medium","What is the average monthly number of accounts (in hundreds) opened from January to March?",["22","24","26","28"],"24","(18 + 24 + 30)/3 = 72/3 = 24.",LN2,SL,chk=((18+24+30)/3,24))
Q_(s,T,"Medium","By roughly what percentage did the accounts opened in June exceed those in April?",["53%","58%","63%","68%"],"63%","(44 − 27)/27 = 17/27 = 63%.",LN2,SL,chk=(round((44-27)/27*100),63))
mom2={mo[i]:(ac[i]-ac[i-1])/ac[i-1] for i in range(1,6)}; assert max(mom2,key=mom2.get)=="May"
Q_(s,T,"Hard","In which month was the percentage growth over the previous month the highest?",["February","March","May","June"],"May","Growth: Feb 6/18 = 33.3%, Mar 6/24 = 25%, May 10/27 = 37.0%, Jun 7/37 = 18.9%. May is the highest.",LN2,SL)

mk={"Aman":[42,39,30,25],"Bhavna":[36,44,40,30],"Chirag":[28,35,45,32],"Divya":[38,41,35,37],"Esha":[33,30,38,27]}
mt={k:sum(v) for k,v in mk.items()}; assert max(mt,key=mt.get)=="Divya" and mt["Divya"]==151 and sorted(mt.values())[-2]==150
MKT="<b>Marks of five candidates in a mock test (each section out of 50)</b><table class='data'><tr><th>Candidate</th><th>Quant</th><th>Reasoning</th><th>English</th><th>GK</th></tr>"+"".join(f"<tr><td>{k}</td>"+"".join(f"<td>{x}</td>" for x in v)+"</tr>" for k,v in mk.items())+"</table>"
T="Tables"; SM="table-mock-marks"
Q_(s,T,"Easy","Who has the highest total across the four sections?",["Bhavna","Chirag","Divya","Esha"],"Divya","Totals: Aman 136, Bhavna 150, Chirag 140, Divya 151, Esha 128. Divya is highest.",MKT,SM)
Q_(s,T,"Easy","What is Bhavna's combined score in Reasoning and English?",["80","82","84","86"],"84","Read Bhavna's row: Reasoning 44 and English 40. Their sum is 44 + 40 = 84.",MKT,SM,chk=(44+40,84))
gk=sum(v[3] for v in mk.values()); assert gk==151
Q_(s,T,"Medium","What is the average GK score of the five candidates?",["29.6","30.2","31.0","31.4"],"30.2","GK total = 25 + 30 + 32 + 37 + 27 = 151. Average = 151/5 = 30.2.",MKT,SM,chk=(gk/5,30.2))
cnt=sum(1 for v in mk.values() if sum(1 for x in v if x>35)>=3); assert cnt==2
Q_(s,T,"Medium","How many candidates scored more than 35 in at least three sections?",["1","2","3","4"],"2","More than 35 in three sections: Bhavna (36, 44, 40) and Divya (38, 41, 37). Aman has only two (42, 39). Chirag has one (45) and Esha has one (38). So 2 candidates.",MKT,SM)
Q_(s,T,"Hard","What percentage of Chirag's total score comes from English?",["30.5%","32.1%","33.3%","35.0%"],"32.1%","Chirag's total = 28 + 35 + 45 + 32 = 140. English share = 45/140 = 32.1%.",MKT,SM,chk=(round(45/140*100,1),32.1))

VN="<p>In a survey of 200 students, 120 are preparing for the Bank exam, 90 are preparing for the SSC exam and 40 are preparing for both. Some students are preparing for neither.</p>"
T="Venn Diagrams"; SV="venn-bank-ssc"
Q_(s,T,"Easy","How many students are preparing only for the Bank exam?",["70","80","90","120"],"80","Only Bank = 120 − 40 = 80.",VN,SV,chk=(120-40,80))
Q_(s,T,"Easy","How many students are preparing for neither exam?",["20","30","40","50"],"30","Bank or SSC = 120 + 90 − 40 = 170. Neither = 200 − 170 = 30.",VN,SV,chk=(200-(120+90-40),30))
Q_(s,T,"Medium","What percentage of all the students are preparing for exactly one of the two exams?",["55%","60%","65%","70%"],"65%","Only Bank = 80 and only SSC = 90 − 40 = 50. Exactly one = 130. 130/200 = 65%.",VN,SV,chk=(130/200*100,65))
Q_(s,T,"Medium","Of the students preparing for the Bank exam, what percentage also prepare for the SSC exam?",["25%","30%","33.3%","40%"],"33.3%","40 of the 120 Bank students also prepare for SSC: 40/120 = 33.3%.",VN,SV,chk=(40/120*100,100/3))
Q_(s,T,"Hard","Suppose 20 of the students preparing only for the Bank exam also start preparing for the SSC exam. What is then the ratio of students preparing exactly one exam to those preparing both?",["11 : 6","13 : 4","5 : 3","7 : 4"],"11 : 6","Only Bank becomes 80 − 20 = 60 and both becomes 40 + 20 = 60. Only SSC stays 50. Exactly one = 60 + 50 = 110. Ratio = 110 : 60 = 11 : 6.",VN,SV,chk=(F(110,60),F(11,6)))


# ======================= PLACEMENT PRACTICE (+60: 30 Quant, 20 Reasoning, 10 DILR) =======================
_pos = [t for _ in range(20) for t in range(4)]; _rnd.Random(31).shuffle(_pos); _pi = iter(_pos)
Q_=QB
s = "quant"
Q_(s,"Percentages","Easy","A company's headcount rises from 800 to 920. What is the percentage increase?",["12%","14%","15%","18%"],"15%","Increase = 920 − 800 = 120. Percentage increase = 120/800 × 100 = 15%.",chk=(120/800*100,15))
Q_(s,"Percentages","Medium","In a campus drive, 25% of 640 students were shortlisted and 40% of the shortlisted students received offers. How many students received offers?",["56","64","72","80"],"64","Shortlisted = 25% of 640 = 160. Offers = 40% of 160 = 64.",chk=(640*.25*.4,64))
Q_(s,"Percentages","Medium","A package of ₹6 lakh is raised by 20% and then cut by 20%. What is the final package?",["₹5.60 lakh","₹5.76 lakh","₹5.88 lakh","₹6.00 lakh"],"₹5.76 lakh","After the raise: 6 × 1.2 = 7.2. After the cut: 7.2 × 0.8 = ₹5.76 lakh.",chk=(6*1.2*.8,5.76))
Q_(s,"Profit & Loss","Easy","A laptop bought for ₹40,000 is sold at a 15% profit. What is the selling price?",["₹44,000","₹45,000","₹46,000","₹47,500"],"₹46,000","Profit = 15% of 40,000 = ₹6,000. Selling price = 40,000 + 6,000 = ₹46,000.",chk=(40000*1.15,46000))
Q_(s,"Profit & Loss","Medium","An item is marked at ₹1,250 and sold after a 20% discount, still giving a 25% profit. What is the cost price?",["₹750","₹800","₹850","₹900"],"₹800","Selling price = 1,250 × 0.8 = ₹1,000. Cost price = 1,000/1.25 = ₹800.",chk=(1250*.8/1.25,800))
Q_(s,"Profit & Loss","Hard","An item costs ₹500 and is marked 40% above cost. After a 15% discount, what is the profit percentage?",["15%","17%","19%","21%"],"19%","Marked price = 500 × 1.4 = ₹700. Selling price = 700 × 0.85 = ₹595. Profit = 95, which is 95/500 = 19%.",chk=((700*.85-500)/500*100,19))
Q_(s,"Simple & Compound Interest","Easy","What is the simple interest on ₹12,000 at 7.5% per annum for 4 years?",["₹3,000","₹3,200","₹3,600","₹3,900"],"₹3,600","SI = 12,000 × 7.5 × 4/100 = ₹3,600.",chk=(12000*7.5*4/100,3600))
Q_(s,"Simple & Compound Interest","Medium","At what rate of simple interest per annum will a sum of money double itself in 8 years?",["10%","12%","12.5%","15%"],"12.5%","The interest equals the principal: P = P × r × 8/100, so r = 100/8 = 12.5%.",chk=(100/8,12.5))
Q_(s,"Ratio & Proportion","Easy","Two employees' salaries are in the ratio 5 : 7 and together amount to ₹60,000. What is the difference between them?",["₹8,000","₹10,000","₹12,000","₹15,000"],"₹10,000","One part = 60,000/12 = ₹5,000. The salaries are ₹25,000 and ₹35,000, a difference of ₹10,000.",chk=(2*60000/12,10000))
Q_(s,"Ratio & Proportion","Medium","Among 240 candidates the ratio of boys to girls is 7 : 5. If 20 more girls join, what is the new ratio of boys to girls?",["7 : 5","7 : 6","6 : 5","5 : 4"],"7 : 6","Boys = 140 and girls = 100. After 20 more girls: 140 : 120 = 7 : 6.",chk=(F(140,120),F(7,6)))
Q_(s,"Averages & Alligation","Medium","The average of six consecutive even numbers is 15. What is the largest of them?",["18","20","22","24"],"20","For consecutive even numbers the average is the middle of the list: the 3rd and 4th numbers are 14 and 16. So the numbers are 10, 12, 14, 16, 18, 20 and the largest is 20.",chk=(15+5,20))
Q_(s,"Averages & Alligation","Medium","Thirty students have an average score of 60 and twenty students have an average of 70. What is the average of all fifty students?",["63","64","65","66"],"64","Total = 30 × 60 + 20 × 70 = 1,800 + 1,400 = 3,200. Average = 3,200/50 = 64.",chk=((1800+1400)/50,64))
Q_(s,"Averages & Alligation","Hard","In what ratio should a 20% salt solution be mixed with a 50% salt solution to get a 30% solution?",["1 : 2","2 : 1","3 : 2","3 : 1"],"2 : 1","Using alligation: (50 − 30) : (30 − 20) = 20 : 10 = 2 : 1, the 20% solution to the 50% solution.",chk=(F(50-30,30-20),2))
Q_(s,"Time & Work","Easy","A can finish a task in 12 days and B can finish it in 24 days. How long will they take working together?",["6 days","8 days","9 days","10 days"],"8 days","Work per day = 1/12 + 1/24 = 3/24 = 1/8. They finish in 8 days.",chk=(1/(1/12+1/24),8))
Q_(s,"Time & Work","Medium","8 workers can finish a job in 15 days. After 5 days, 8 more workers join. How many more days will it take to finish the job?",["4 days","5 days","6 days","7 days"],"5 days","Total work = 8 × 15 = 120 worker-days. In 5 days 40 are done, leaving 80. With 16 workers the rest takes 80/16 = 5 days.",chk=((120-40)/16,5))
Q_(s,"Time & Work","Medium","Pipe A can fill a tank in 8 hours and pipe B in 12 hours. Both are opened for 3 hours and then B is closed. How many more hours will A take to fill the rest?",["2 hours","3 hours","4 hours","5 hours"],"3 hours","In 3 hours both fill 3 × (1/8 + 1/12) = 3 × 5/24 = 5/8 of the tank. The remaining 3/8 is filled by A alone in 3/8 × 8 = 3 hours.",chk=((1-3*(1/8+1/12))*8,3))
Q_(s,"Time, Speed & Distance","Medium","A car travels 120 km at 60 km/h and returns the same 120 km at 40 km/h. What is its average speed for the whole trip?",["45 km/h","48 km/h","50 km/h","52 km/h"],"48 km/h","Time going = 2 h and time returning = 3 h. Average speed = 240/5 = 48 km/h.",chk=(240/(120/60+120/40),48))
Q_(s,"Time, Speed & Distance","Easy","A 150 m long train running at 54 km/h passes a pole. How long does it take?",["8 seconds","10 seconds","12 seconds","15 seconds"],"10 seconds","54 km/h = 54 × 5/18 = 15 m/s. Time = 150/15 = 10 seconds.",chk=(150/(54*5/18),10))
Q_(s,"Time, Speed & Distance","Hard","Two trains of lengths 100 m and 125 m run in opposite directions at 36 km/h and 54 km/h. How long do they take to cross each other?",["8 seconds","9 seconds","10 seconds","12 seconds"],"9 seconds","Relative speed = 90 km/h = 25 m/s. Distance = 225 m. Time = 225/25 = 9 seconds.",chk=(225/((36+54)*5/18),9))
Q_(s,"Time, Speed & Distance","Medium","A boat goes upstream at 12 km/h and downstream at 20 km/h. What is its speed in still water?",["14 km/h","15 km/h","16 km/h","18 km/h"],"16 km/h","Speed in still water = (20 + 12)/2 = 16 km/h.",chk=((20+12)/2,16))
Q_(s,"Number System","Medium","What is the smallest number which leaves a remainder of 5 when divided by 6, 8 and 12?",["24","29","41","53"],"29","LCM of 6, 8 and 12 = 24. The smallest such number is 24 + 5 = 29.",chk=(math.lcm(6,8,12)+5,29))
Q_(s,"Number System","Medium","What is the sum of all multiples of 7 from 1 to 100?",["665","700","735","770"],"735","The multiples are 7 × 1 up to 7 × 14 (98). Sum = 7 × (14 × 15/2) = 7 × 105 = 735.",chk=(sum(range(7,101,7)),735))
Q_(s,"Algebra","Medium","If a + b = 10 and ab = 21, what is the value of a² + b²?",["56","58","60","62"],"58","a² + b² = (a + b)² − 2ab = 100 − 42 = 58.",chk=(100-42,58))
Q_(s,"Algebra","Hard","The product of two consecutive positive integers is 342. What is their sum?",["35","37","39","41"],"37","18 × 19 = 342, so the integers are 18 and 19 and their sum is 37.",chk=(18+19,37))
Q_(s,"Geometry & Mensuration","Medium","The perimeter of a rectangle is 36 cm and its length is twice its breadth. What is its area?",["64 cm²","72 cm²","80 cm²","96 cm²"],"72 cm²","2(l + b) = 36 with l = 2b gives 6b = 36, so b = 6 and l = 12. Area = 72 cm².",chk=(6*12,72))
Q_(s,"Geometry & Mensuration","Easy","The area of a circle is 154 cm². What is its circumference? (Take π = 22/7)",["33 cm","44 cm","55 cm","66 cm"],"44 cm","πr² = 154 gives r² = 49, so r = 7. Circumference = 2 × 22/7 × 7 = 44 cm.",chk=(2*22/7*7,44))
Q_(s,"Permutations & Combinations","Medium","In how many ways can the letters of the word CAMPUS be arranged so that the two vowels are together?",["120","180","240","360"],"240","Treat the vowels A and U as one block. The 5 units (C, M, P, S and the block) can be arranged in 5! = 120 ways, and the vowels in the block can swap in 2 ways. Total = 240.",chk=(math.factorial(5)*2,240))
Q_(s,"Permutations & Combinations","Easy","In how many ways can a team of 4 be chosen from 10 candidates?",["120","180","210","240"],"210","10C4 = (10 × 9 × 8 × 7)/(4 × 3 × 2 × 1) = 210.",chk=(comb(10,4),210))
Q_(s,"Probability","Easy","A bag has 5 red, 3 blue and 2 green balls. One ball is drawn at random. What is the probability that it is not blue?",["3/10","1/2","7/10","4/5"],"7/10","Not blue = 5 + 2 = 7 balls out of 10. Probability = 7/10.",chk=(7/10,.7))
Q_(s,"Probability","Medium","A committee of 2 is chosen at random from 4 men and 3 women. What is the probability that both are women?",["1/7","2/7","3/7","1/3"],"1/7","Total ways = 7C2 = 21. Both women: 3C2 = 3. Probability = 3/21 = 1/7.",chk=(comb(3,2)/comb(7,2),1/7))

s = "reasoning"
Q_(s,"Syllogisms","Medium","Statements: All engineers are graduates. Some graduates are managers.<br>Conclusions: I. Some engineers are managers II. Some managers are graduates",SY,"Only II follows","Converting 'some graduates are managers' gives some managers are graduates (II). The managers may not be engineers, so I does not follow.")
Q_(s,"Syllogisms","Hard","Statements: No coder is a tester. All testers are analysts.<br>Conclusions: I. No coder is an analyst II. Some analysts are not coders",SY,"Only II follows","Testers are analysts and no tester is a coder, so some analysts (the testers) are not coders (II). Other analysts may be coders, so I does not follow.")
rw=[p for p in itertools.permutations("ABCDEF") if p[0]=="B" and p[2]=="A" and p[3]=="C" and p[5]!="D" and p.index("E")<p.index("D")]
assert len(rw)==1 and rw[0][5]=="F"
Q_(s,"Seating Arrangement","Medium","Six interns A, B, C, D, E and F sit in a row facing north. B sits at the left end. A sits two places to the right of B. C sits immediately to the right of A. D does not sit at the right end. E sits to the left of D. Who sits at the right end?",["D","E","F","C"],"F","B is 1st, A is 3rd and C is 4th. The free seats are 2nd, 5th and 6th for D, E and F. D is not 6th and E is to the left of D, so D is 5th and E is 2nd. That leaves F in the 6th seat, at the right end.")
cs5=[]
for perm in itertools.permutations("QSTR"):
    st=dict(zip([1,2,3,4],perm)); st[0]="P"
    seat={v:k for k,v in st.items()}
    if seat["R"]==1 and seat["Q"]==4 and abs(seat["S"]-seat["R"])%5 not in (1,4): cs5.append(seat)
assert len(cs5)==1 and cs5[0]["S"]==3
Q_(s,"Seating Arrangement","Hard","Five persons P, Q, R, S and T sit around a circular table facing the centre. P sits between Q and R. R sits immediately clockwise of P. S does not sit next to R. Who sits between T and Q?",["P","R","S","Cannot be determined"],"S","Going clockwise from P: R is next, and Q is on P's other side, so Q is last. S and T take the two middle seats. S cannot be next to R, so S is the fourth seat and T the third. The order clockwise is P, R, T, S, Q. S sits between T and Q.")
Q_(s,"Blood Relations","Easy","A is the brother of B. B is the sister of C. D is the father of A. How is C related to D?",["Son","Daughter","Son or daughter","Nephew"],"Son or daughter","A, B and C are siblings, and D is the father of A, so D is the father of all three. C's gender is not given, so C is D's son or daughter.")
Q_(s,"Blood Relations","Medium","Pointing to a man, Sita says, 'He is the son of my mother's only brother.' How is the man related to Sita?",["Brother","Cousin","Nephew","Uncle"],"Cousin","Sita's mother's only brother is her maternal uncle. His son is Sita's cousin.")
Q_(s,"Coding-Decoding","Medium","In a certain code, WORK is written as XQUO, where the letters are moved forward by 1, 2, 3 and 4 places respectively. How is PLAY written in that code?",["QNDC","QNCD","OJXU","QMDC"],"QNDC","P+1 = Q, L+2 = N, A+3 = D, Y+4 = C (after Z comes A, B, C). So PLAY is written QNDC.")
Q_(s,"Coding-Decoding","Medium","In a certain code, 'bright red car' is written as 'ka mi to', 'red car park' as 'mi to se' and 'park fast' as 'se ju'. How is 'bright' written in that code?",["ka","mi","to","se"],"ka","'red car' is common to the first two statements and 'mi to' is common to the codes, so red and car are mi and to in some order. The remaining code in the first statement, 'ka', stands for bright.")
Q_(s,"Number & Letter Series","Medium","Find the next term: 7, 10, 16, 28, 52, ?",["88","96","100","104"],"100","The differences are 3, 6, 12, 24, doubling each time, so the next difference is 48: 52 + 48 = 100.",chk=(52+48,100))
Q_(s,"Number & Letter Series","Easy","Find the next term: 1, 2, 6, 24, 120, ?",["240","600","720","840"],"720","The terms are factorials: 1!, 2!, 3!, 4!, 5!. The next is 6! = 720.",chk=(math.factorial(6),720))
Q_(s,"Number & Letter Series","Medium","Find the next term: Z, X, U, Q, L, ?",["E","F","G","H"],"F","The positions are 26, 24, 21, 17, 12. The differences are −2, −3, −4, −5, so the next is −6: 12 − 6 = 6, which is F.")
Q_(s,"Direction Sense","Medium","A man starts walking east, covers 10 m, turns right and walks 4 m, then turns right again and walks 10 m. How far and in which direction is he from the starting point?",["4 m south","4 m north","10 m south","14 m west"],"4 m south","East 10 m, then right (south) 4 m, then right (west) 10 m. The east and west moves cancel, so he is 4 m south of the start.")
Q_(s,"Direction Sense","Medium","Facing south-west, Anil turns 180° and then 90° anticlockwise. Which direction is he facing now?",["North-East","North-West","South-East","South-West"],"North-West","Turning 180° from south-west gives north-east. Turning 90° anticlockwise from north-east gives north-west.")
Q_(s,"Clocks & Calendars","Hard","A clock gains 5 minutes every hour. It is set correctly at 6 AM. What time will it show when the true time is 2 PM?",["2:30 PM","2:40 PM","2:45 PM","2:50 PM"],"2:40 PM","From 6 AM to 2 PM is 8 hours. The clock gains 8 × 5 = 40 minutes, so it shows 2:40 PM.",chk=(8*5,40))
assert datetime.date(2026,1,1).strftime("%A")=="Thursday" and datetime.date(2027,1,1).strftime("%A")=="Friday"
Q_(s,"Clocks & Calendars","Easy","If 1 January 2026 is a Thursday, what day is 1 January 2027?",["Thursday","Friday","Saturday","Sunday"],"Friday","2026 is not a leap year, so it has 365 days = 52 weeks + 1 day. The day moves forward by 1: Thursday → Friday.",chk=((datetime.date(2027,1,1)-datetime.date(2026,1,1)).days,365))
Q_(s,"Alphabet Test","Medium","Which letter is the 5th to the left of the 20th letter from the left end of the alphabet?",["N","O","P","Q"],"O","The 20th letter is T. Five places to its left is the 15th letter, which is O.",chk=(20-5,15))
Q_(s,"Ranking & Order","Medium","In a group of 45, Arun is 14th from the top and Bimal is 5 places below Arun. What is Bimal's position from the bottom?",["25th","26th","27th","28th"],"27th","Bimal is 14 + 5 = 19th from the top. From the bottom: 45 − 19 + 1 = 27th.",chk=(45-19+1,27))
Q_(s,"Odd One Out","Easy","Find the odd one out: Python, Java, Ruby, Excel, C++",["Python","Ruby","Excel","C++"],"Excel","Python, Java, Ruby and C++ are programming languages. Excel is a spreadsheet application.")
Q_(s,"Puzzles","Medium","Five interns Ravi, Sita, Tarun, Uma and Vikas earn different stipends. Uma earns more than Ravi. Ravi earns more than Tarun. Sita earns less than Tarun. Vikas earns more than Uma. Who earns the least?",["Ravi","Sita","Tarun","Uma"],"Sita","The clues give Vikas > Uma > Ravi > Tarun > Sita. Sita earns the least.")
Q_(s,"Inequalities","Medium","Statements: G > H ≥ I = J ≥ K<br>Conclusions: I. G > K II. K < H",SY,"Only I follows","G > H ≥ I = J ≥ K gives G > K (I follows). H ≥ K only, so K < H is not certain (II does not follow).")

s = "dilr"
cmp_={"A":(400,120,30),"B":(500,200,50),"C":(300,90,36),"D":(600,240,48),"E":(200,80,24)}
sel=sum(v[2] for v in cmp_.values()); app=sum(v[0] for v in cmp_.values()); assert (sel,app)==(188,2000)
rt={k:v[2]/v[1] for k,v in cmp_.items()}; assert max(rt,key=rt.get)=="C" and sorted(rt.values())[-2]<rt["C"]
PT="<b>Campus recruitment drive: five companies</b><table class='data'><tr><th>Company</th><th>Applied</th><th>Shortlisted</th><th>Selected</th></tr>"+"".join(f"<tr><td>{k}</td><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for k,(a,b,c) in cmp_.items())+"</table>"
T="Tables"; SPT="table-drive"
Q_(s,T,"Easy","How many candidates were selected in total across the five companies?",["180","184","188","192"],"188","30 + 50 + 36 + 48 + 24 = 188.",PT,SPT,chk=(sel,188))
Q_(s,T,"Easy","What percentage of Company B's applicants were shortlisted?",["30%","35%","40%","45%"],"40%","Company B had 500 applicants and 200 were shortlisted. The percentage is 200/500 × 100 = 40%.",PT,SPT,chk=(200/500*100,40))
Q_(s,T,"Medium","For which company is the ratio of selected to shortlisted candidates the highest?",["Company A","Company C","Company D","Company E"],"Company C","Selected/shortlisted: A 25%, B 25%, C 40%, D 20%, E 30%. Company C is the highest.",PT,SPT)
Q_(s,T,"Medium","What percentage of all applicants across the five companies were selected?",["8.4%","9.4%","10.4%","11.4%"],"9.4%","Total applicants = 2,000 and total selected = 188. 188/2,000 = 9.4%.",PT,SPT,chk=(188/2000*100,9.4))
Q_(s,T,"Hard","If the selections at Company D rise by 25% and those at Company E fall by 25%, what is the new total number of selections?",["190","192","194","196"],"194","D: 48 × 1.25 = 60 (+12). E: 24 × 0.75 = 18 (−6). New total = 188 + 12 − 6 = 194.",PT,SPT,chk=(188+12-6,194))
of_=[("A",80),("B",120),("C",60),("D",100),("E",40)]; ov=dict(of_)
OB="<b>Job offers made by five companies this season</b><div class='bars'>"+"".join(f"<div class='bar-row'><span>Company {c}</span><i style='width:{v/120*100:.1f}%'></i><span>{v}</span></div>" for c,v in of_)+"</div>"
T="Bar Charts"; SOB="bar-offers"
Q_(s,T,"Easy","How many offers were made by the five companies in total?",["380","400","420","440"],"400","80 + 120 + 60 + 100 + 40 = 400.",OB,SOB,chk=(sum(ov.values()),400))
Q_(s,T,"Easy","Company B's offers are what percentage of the total?",["25%","28%","30%","32%"],"30%","Company B made 120 of the 400 offers in total. The percentage is 120/400 × 100 = 30%.",OB,SOB,chk=(120/400*100,30))
Q_(s,T,"Medium","How many companies made more offers than the average of the five?",["1","2","3","4"],"2","Average = 400/5 = 80. Only Company B (120) and Company D (100) are above 80; Company A is equal to it. So 2 companies.",OB,SOB)
Q_(s,T,"Medium","What is the ratio of the highest number of offers to the lowest?",["2 : 1","5 : 2","3 : 1","4 : 1"],"3 : 1","Highest = 120 (Company B) and lowest = 40 (Company E). 120 : 40 = 3 : 1.",OB,SOB,chk=(F(120,40),3))
Q_(s,T,"Hard","If Company A's offers rise by 25% and Company C's rise by 50%, what percentage of the new total do these two companies make together?",["40.0%","42.2%","44.4%","46.7%"],"42.2%","A becomes 100 (+20) and C becomes 90 (+30). New total = 400 + 50 = 450. A + C = 190. 190/450 = 42.2%.",OB,SOB,chk=(round(190/450*100,1),42.2))


NAMES={"quant":"Quantitative Aptitude","reasoning":"Logical Reasoning","dilr":"DILR"}
import os, collections
# ---- CUET reuse tags: Easy/Medium general items that sit within the CUET General Aptitude Test syllabus ----
CUET_QR_SKIP = {"Permutations & Combinations", "Probability"}   # not in the GAT syllabus list (arithmetic, algebra, geometry, mensuration, statistics)
CUET_LR = {"Syllogisms", "Seating Arrangement", "Puzzles", "Blood Relations", "Inequalities"}
CUET_GMA = {"Alphabet Test", "Clocks & Calendars", "Coding-Decoding", "Direction Sense", "Number & Letter Series", "Odd One Out", "Ranking & Order"}
assert CUET_LR | CUET_GMA == {q["topic"] for q in OUT["reasoning"]}
for q in OUT["quant"] + OUT["reasoning"]:
    if q["difficulty"] == "Hard": continue
    if q in OUT["quant"]:
        if q["topic"] in CUET_QR_SKIP: continue
        q["cuet_part"] = "Quantitative Reasoning"
    else:
        q["cuet_part"] = "Logical & Analytical Reasoning" if q["topic"] in CUET_LR else "General Mental Ability"
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
import qa as _qa, dilr as _dilr, varc as _varc, packs as _packs
CB = Bank(); _qa.build(CB); _dilr.build(CB); _varc.build(CB); _packs.build(CB)   # packs: mocks, sectionals, practice packs
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
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assign_levels as _al   # deterministic CAT practice sets (level + practiceSet), writes data/cat/sets.json
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_al.assign(cat_out, os.path.join(os.path.dirname(__file__), "..", "data", "cat", "sets.json"))
json.dump(cat_out, open(os.path.join(os.path.dirname(__file__), "..", "data", "cat.json"), "w"), ensure_ascii=False, indent=1)
for k in ("varc", "dilr", "qa"):
    v = CB.qs[k]
    print("CAT", k, len(v), dict(collections.Counter(q["type"] for q in v)), dict(collections.Counter(q["difficulty"] for q in v)))
    print("   ", dict(collections.Counter(q["topic"] for q in v)))
print("CAT TOTAL", len(ids), "sets:", len(CB.sets))


# ======================= CUET (UG) TRACK =======================
_sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cuet"))
try:
    import sympy  # noqa: F401  (needed to verify the Maths answers)
except ImportError:
    raise SystemExit("CUET maths checks need sympy: run with a Python that has it, e.g. /workspace/.venv-edu/bin/python tools/build_questions.py")
from ucommon import UBank
import gat as _gat, english as _eng, maths as _maths
UB = UBank(); _gat.build(UB); _eng.build(UB); _maths.build(UB)
# reuse: tagged general items join the GAT pool (copied, with their original id kept for traceability)
reused = []
for q in OUT["quant"] + OUT["reasoning"]:
    if "cuet_part" in q:
        r = {k: v for k, v in q.items() if k != "cuet_part"}
        r.update(id="G-" + q["id"], exam="cuet", section="gat", part=q["cuet_part"], type="mcq", source="general", orig_id=q["id"])
        reused.append(r)
uq = {"gat": UB.qs["gat"] + reused, "english": UB.qs["english"], "maths": UB.qs["maths"]}
# global checks
uids = [q["id"] for v in uq.values() for q in v]; assert len(uids) == len(set(uids))
uused = collections.Counter(q.get("set") for v in uq.values() for q in v if q.get("set"))
assert set(uused) == set(UB.sets), set(UB.sets) ^ set(uused)
for sid, n in uused.items(): assert 4 <= n <= 5, (sid, n)
for v in uq.values():
    for q in v:
        assert q["type"] == "mcq" and len(q["options"]) == 4 and len(set(q["options"])) == 4 and 0 <= q["answer"] < 4, q["id"]
        assert q["difficulty"] in ("Easy", "Medium", "Hard") and q["topic"] and q["part"] and len(q["solution"]) > 15, q["id"]
        assert "Option " not in q["solution"], q["id"]          # solutions name options by content, never by position
CUET_NAMES = {"gat": "General Aptitude Test", "english": "English", "maths": "Mathematics / Applied Mathematics"}
cuet_out = {"sections": {k: {"name": CUET_NAMES[k], "questions": uq[k]} for k in ("gat", "english", "maths")}, "sets": UB.sets}
json.dump(cuet_out, open(os.path.join(os.path.dirname(__file__), "..", "data", "cuet.json"), "w"), ensure_ascii=False, indent=1)
for k in ("gat", "english", "maths"):
    v = uq[k]; orig = [q for q in v if q.get("source") != "general"]
    print("CUET", k, len(v), "(original", len(orig), "+ reused", len(v) - len(orig), ")", dict(collections.Counter(q["difficulty"] for q in v)))
    for part in dict.fromkeys(q["part"] for q in v):
        pv = [q for q in v if q["part"] == part]
        print("    ", part, len(pv), "(reused", sum(1 for q in pv if q.get("source") == "general"), ")", dict(collections.Counter(q["topic"] for q in pv)))
print("CUET TOTAL", len(uids), "original", sum(1 for v in uq.values() for q in v if q.get("source") != "general"), "sets:", len(UB.sets))

# per-section files + data/stats.json for the site
import importlib.util as _iu, os as _os
_sp = _iu.spec_from_file_location("split_data", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "split_data.py")); _m = _iu.module_from_spec(_sp); _sp.loader.exec_module(_m); _m.main()
