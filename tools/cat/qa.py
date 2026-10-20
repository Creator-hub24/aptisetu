"""CAT Quantitative Ability: original questions. Answers recomputed below."""
import itertools, math
from math import comb, factorial, sqrt, pi
from fractions import Fraction as F

def build(B):
    s = "qa"
    M = lambda *a, **k: B.mcq(s, *a, **k)
    T = lambda *a, **k: B.tita(s, *a, **k)

    # ---------- Percentages & Profit ----------
    t = "Percentages & Profit"
    T(t,"Medium","A trader marks his goods 50% above cost price and then allows two successive discounts of 10% and 20%. What is his profit percentage?",
      round((1.5*0.9*0.8-1)*100), "SP = CP × 1.5 × 0.9 × 0.8 = 1.08 × CP, so the profit is 8%.", chk=(round((1.5*.9*.8-1)*100,9), 8))
    # savings: I=100, E: 120-1.1E = 1.5(100-E)
    E = [e for e in range(1,100) if abs((120-1.1*e) - 1.5*(100-e))<1e-9][0]
    M(t,"Medium","Ravi's income rises by 20% and his expenditure rises by 10%. As a result, his savings rise by 50%. What percentage of his original income did he originally save?",
      ["20%","25%","30%","40%"], f"{100-E}%", f"Let income = 100 and expenditure = E. New savings: 120 − 1.1E = 1.5(100 − E) ⇒ 0.4E = 30 ⇒ E = 75. Savings = 25% of income.")
    C = [c for c in range(1,2000) if abs((1.2*c-18) - 1.25*0.9*c) < 1e-9][0]
    T(t,"Medium","A shopkeeper sells an article at a 20% profit. Had he bought it for 10% less and sold it for ₹18 less, his profit would have been 25%. What is the cost price (in ₹)?",
      C, "Let CP = C, so SP = 1.2C. New CP = 0.9C and new SP = 1.2C − 18 = 1.25 × 0.9C = 1.125C. So 0.075C = 18 ⇒ C = ₹240.", chk=(C,240))
    N = [n for n in range(1000,100000,100) if abs(0.81*n*0.08 - 1620) < 1e-6][0]
    M(t,"Hard","In a two-candidate election, 10% of registered voters did not vote and 10% of the votes cast were invalid. The winner got 54% of the valid votes and won by 1,620 votes. How many registered voters were there?",
      ["20,000","25,000","27,000","30,000"], f"{N:,}", "Valid votes = 0.9 × 0.9 × N = 0.81N. The margin is 54% − 46% = 8% of valid votes: 0.08 × 0.81N = 0.0648N = 1620 ⇒ N = 25,000.")

    # ---------- TSD ----------
    t = "Time, Speed & Distance"
    va, tA, tB = 45, 4, 9; vb = va*sqrt(tA/tB); tm = sqrt(tA*tB); D = (va+vb)*tm
    assert close_(va*tm/vb, tB) and close_(vb*tm/va, tA)
    T(t,"Hard","Two cars start at the same time from P and Q and drive towards each other. After they meet, the car from P takes 4 hours to reach Q and the car from Q takes 9 hours to reach P. If the car from P travels at 45 km/h, what is the distance PQ (in km)?",
      round(D), "If the meeting happens after t hours: t² = 4 × 9 ⇒ t = 6 h, and speed ratio = √(9/4) = 3 : 2, so the other car does 30 km/h. PQ = (45 + 30) × 6 = 450 km. Check: P-car covers 270 km before meeting, then the remaining 180 km at 45 km/h = 4 h ✓.", chk=(D,450))
    v = [v for v in range(4,200) if abs((v-3)*10 - (v+6)*8) < 1e-9][0]; L = (v-3)*5/18*10
    M(t,"Medium","A train passes a man walking at 3 km/h in the same direction in 10 seconds, and a man walking at 6 km/h towards it in 8 seconds. What is the length of the train?",
      ["90 m","100 m","110 m","120 m"], f"{round(L)} m", f"(v − 3) × 10 = (v + 6) × 8 (in km/h × s) ⇒ 2v = 78 ⇒ v = 39 km/h. Length = 36 × 5/18 × 10 = 100 m.", chk=(L,100))
    # circular track
    a = next(a for a in range(1,100) if (240*a*7) % 1200 == 0)  # A at start every 240 s; B every 1200/7 s
    M(t,"Medium","A and B start together from the same point on a 1,200 m circular track and run in the same direction at 5 m/s and 7 m/s. After how many seconds will they first be together at the starting point again?",
      ["600 s","840 s","1,200 s","1,680 s"], f"{240*a:,} s", "A completes a lap every 240 s and B every 1200/7 s. Both are at the start at times that are multiples of both: 240a = 1200b/7 ⇒ 7a = 5b, smallest a = 5 ⇒ 1,200 s. (They do meet at 600 s too, but halfway round the track, not at the start.)")
    # boat: 30u+44d=10, 40u+55d=13
    sol = [(up,dn) for up in range(1,30) for dn in range(up+1,40) if abs(30/up+44/dn-10)<1e-9 and abs(40/up+55/dn-13)<1e-9]
    assert sol == [(5,11)]
    M(t,"Medium","A boat goes 30 km upstream and 44 km downstream in 10 hours. It goes 40 km upstream and 55 km downstream in 13 hours. What is the speed of the stream?",
      ["2 km/h","3 km/h","4 km/h","5 km/h"], "3 km/h", "Let u = 1/upstream speed and d = 1/downstream speed: 30u + 44d = 10 and 40u + 55d = 13. Solving gives u = 1/5 and d = 1/11, so the upstream speed is 5 and the downstream speed 11. Stream = (11 − 5)/2 = 3 km/h.")
    d = next(x for x in range(1,100) if abs(x/5 - x/6 - 10/60) < 1e-9)
    M(t,"Medium","Walking at 5 km/h, Meera reaches office 6 minutes late. Walking at 6 km/h, she reaches 4 minutes early. How far is her office?",
      ["4 km","5 km","6 km","7.5 km"], f"{d} km", "The time difference is 10 min = 1/6 h. d/5 − d/6 = 1/6 ⇒ d/30 = 1/6 ⇒ d = 5 km.")

    # ---------- Time & Work ----------
    t = "Time & Work"
    tot = F(1,12)+F(1,15)+F(1,20); A = tot/2 - F(1,15)
    T(t,"Medium","A and B together can finish a job in 12 days, B and C in 15 days, and C and A in 20 days. In how many days can A alone finish it?",
      int(1/A), "2(A + B + C) = 1/12 + 1/15 + 1/20 = 1/5 ⇒ A + B + C = 1/10. A = 1/10 − (B + C) = 1/10 − 1/15 = 1/30 ⇒ 30 days.", chk=(1/A,30))
    M(t,"Medium","12 men or 18 women can finish a piece of work in 14 days. How many days will 8 men and 16 women take to finish it?",
      ["8","9","10","12"], str(int(18*14/(8*1.5+16))), "1 man = 18/12 = 1.5 women. 8 men + 16 women = 28 women. Work = 18 × 14 = 252 woman-days ⇒ 252/28 = 9 days.")
    rate_all = F(1,20)+F(1,30)-F(1,15); left = 1 - 10*rate_all; t2 = left/(F(1,20)+F(1,30)); total = 10 + t2
    M(t,"Hard","Pipes A and B fill a tank in 20 and 30 minutes respectively, and pipe C empties it in 15 minutes. All three are opened on an empty tank, and C is closed after 10 minutes. How many minutes in total does it take to fill the tank?",
      ["18","20","22","25"], str(int(total)), "With all three open: 1/20 + 1/30 − 1/15 = 1/60 per minute, so 10 minutes fill 1/6. The remaining 5/6 at A + B = 1/12 per minute takes 10 minutes. Total = 20 minutes.", chk=(total,20))
    M(t,"Medium","A is twice as efficient as B, and together they finish a job in 14 days. How many days would A alone take?",
      ["21","28","35","42"], "21", "If B does b per day, A does 2b, so 3b = 1/14 ⇒ b = 1/42 and A = 1/21 ⇒ 21 days.")

    # ---------- Mixtures ----------
    t = "Mixtures & Alligation"
    add = 48/0.75 - 60
    T(t,"Medium","A 60-litre mixture of milk and water contains 20% water. How many litres of water must be added so that water becomes 25% of the new mixture?",
      round(add), "Milk = 48 L and stays fixed. For 75% milk, total = 48/0.75 = 64 L, so add 4 L of water.", chk=(add,4))
    w = 80*0.9**3
    M(t,"Medium","A vessel contains 80 litres of pure wine. 8 litres are taken out and replaced with water, and this is done three times in all. How much wine is left?",
      ["57.6 L","58.32 L","60 L","56.32 L"], "58.32 L", "Each operation keeps 72/80 = 0.9 of the wine. Wine left = 80 × 0.9³ = 58.32 L.", chk=(w,58.32))
    r = (F(1,2)-F(1,4))/(F(3,5)-F(1,2))
    M(t,"Hard","Alloy X has copper and zinc in the ratio 3 : 2, and alloy Y has them in the ratio 1 : 3. In what ratio (X : Y) must they be mixed to get an alloy with equal amounts of copper and zinc?",
      ["5 : 2","2 : 5","3 : 2","5 : 3"], f"{r.numerator} : {r.denominator}", "Copper fraction: X = 0.6, Y = 0.25, target 0.5. By alligation, X : Y = (0.5 − 0.25) : (0.6 − 0.5) = 0.25 : 0.1 = 5 : 2.")

    # ---------- SI & CI ----------
    t = "Simple & Compound Interest"
    M(t,"Medium","A sum grows to ₹13,310 in 3 years and to ₹14,641 in 4 years at compound interest (compounded annually). What is the principal?",
      ["₹9,000","₹10,000","₹11,000","₹12,100"], "₹10,000", "Growth factor = 14641/13310 = 1.1, so the rate is 10%. P = 13310/1.1³ = 13310/1.331 = ₹10,000.", chk=(13310/1.1**3,10000))
    P = 93/(1.1**3-1-0.3)
    M(t,"Medium","The difference between compound and simple interest on a sum for 3 years at 10% per annum is ₹93. What is the sum?",
      ["₹2,500","₹3,000","₹3,100","₹3,300"], "₹3,000", "CI − SI = P[(1.1³ − 1) − 0.3] = P(0.331 − 0.3) = 0.031P = 93 ⇒ P = ₹3,000.", chk=(P,3000))
    amt = 1000*1.1**2 + 1000*1.1
    T(t,"Hard","Riya deposits ₹1,000 at the start of each year for 2 years in an account paying 10% per annum compounded annually. What is the balance (in ₹) at the end of the second year?",
      round(amt), "The first deposit grows for 2 years: 1000 × 1.21 = 1210. The second grows for 1 year: 1000 × 1.1 = 1100. Total = ₹2,310.", chk=(amt,2310))

    # ---------- Ratio ----------
    t = "Ratio & Proportion"
    k = next(k for k in range(1,50) if 3*(5*k-6) == 2*(7*k-6))
    M(t,"Medium","The present ages of A and B are in the ratio 5 : 7. Six years ago they were in the ratio 2 : 3. What is the sum of their present ages?",
      ["60","66","72","84"], str(12*k), "(5k − 6)/(7k − 6) = 2/3 ⇒ 15k − 18 = 14k − 12 ⇒ k = 6. The ages are 30 and 42, so the sum is 72.")
    k2 = 216/(2+1.5+1)
    M(t,"Medium","A bag has ₹1, 50-paise and 25-paise coins in the ratio 2 : 3 : 4 by number, worth ₹216 in total. How many 50-paise coins are there?",
      ["96","120","144","192"], str(int(3*k2)), "Value per set of (2, 3, 4) coins = 2 + 1.5 + 1 = ₹4.5. Sets = 216/4.5 = 48. 50-paise coins = 3 × 48 = 144.")
    kk = F(12*3, 2**2); x = kk*16/8
    T(t,"Hard","x varies directly as y² and inversely as z. When y = 2 and z = 3, x = 12. Find x when y = 4 and z = 8.",
      int(x), "x = k·y²/z ⇒ 12 = 4k/3 ⇒ k = 9. Then x = 9 × 16/8 = 18.", chk=(x,18))

    # ---------- Equations & Quadratics ----------
    t = "Equations & Quadratics"
    p = next(p for p in range(1,50) if p*p-48 == 1)
    M(t,"Medium","The roots of x² − px + 12 = 0 differ by 1, and p > 0. What is p?",
      ["5","6","7","8"], str(p), "(r₁ − r₂)² = (r₁ + r₂)² − 4r₁r₂ = p² − 48 = 1 ⇒ p = 7. (The roots are 3 and 4.)")
    ks = [k for k in range(-50,51) if k*k - 64 < 0]
    T(t,"Medium","For how many integer values of k does x² + kx + 16 = 0 have no real roots?",
      len(ks), "No real roots ⇔ discriminant < 0 ⇔ k² < 64 ⇔ −8 < k < 8. The integers −7 to 7 make 15 values.", chk=(len(ks),15))
    # alpha^3+beta^3 for x^2-5x+3
    r1 = (5+sqrt(13))/2; r2 = (5-sqrt(13))/2
    M(t,"Medium","If α and β are the roots of x² − 5x + 3 = 0, what is α³ + β³?",
      ["70","80","95","110"], "80", "α + β = 5 and αβ = 3. α³ + β³ = (α + β)³ − 3αβ(α + β) = 125 − 45 = 80.", chk=(r1**3+r2**3,80))
    n = sum(1 for x in range(1,100) for y in range(1,100) if 3*x+5*y == 100)
    T(t,"Hard","How many ordered pairs of positive integers (x, y) satisfy 3x + 5y = 100?",
      n, "100 − 5y must be a positive multiple of 3. That needs y ≡ 2 (mod 3) with 5y < 100: y = 2, 5, 8, 11, 14, 17, giving 6 pairs (e.g. y = 2, x = 30; y = 17, x = 5).", chk=(n,6))
    num = [10*a+b for a in range(1,10) for b in range(10) if a+b == 9 and (10*b+a)-(10*a+b) == 27]
    M(t,"Medium","The digits of a two-digit number add up to 9. Reversing the digits increases the number by 27. What is the number?",
      ["27","36","45","63"], str(num[0]), "Let the number be 10a + b with a + b = 9. Reversing adds 9(b − a) = 27 ⇒ b − a = 3. So a = 3, b = 6, and the number is 36.")
    assert len(num) == 1

    # ---------- Inequalities ----------
    t = "Inequalities"
    xs = [x for x in range(-100,101) if abs(x-3)+abs(x+2) < 9]
    T(t,"Medium","How many integers x satisfy |x − 3| + |x + 2| < 9?",
      len(xs), "For −2 ≤ x ≤ 3 the sum is always 5 (6 integers). For x > 3: 2x − 1 < 9 ⇒ x < 5, so x = 4. For x < −2: 1 − 2x < 9 ⇒ x > −4, so x = −3. The answer is x = −3 to 4, which is 8 integers.", chk=(len(xs),8))
    M(t,"Medium","For which values of x is x² − 7x + 10 < 0?",
      ["x < 2 or x > 5","2 < x < 5","−5 < x < −2","x > 5"], "2 < x < 5", "x² − 7x + 10 = (x − 2)(x − 5) is negative strictly between its roots, so 2 < x < 5.")
    mn = min((x*x+2*x+9)/(x+1) for x in [i/10000-1+1e-9 for i in range(1,100000)])
    M(t,"Hard","What is the minimum value of (x² + 2x + 9)/(x + 1) for x > −1?",
      ["4","4√2","6","8"], "4√2", "(x² + 2x + 9)/(x + 1) = (x + 1) + 8/(x + 1). By AM–GM this is at least 2√8 = 4√2, with equality when x + 1 = 2√2.", chk=(round(mn,6), round(4*sqrt(2),6)))

    # ---------- Functions ----------
    t = "Functions"
    # 2(x^2-1)+3 = (2x+3)^2-1 -> 2x^2+12x+7=0
    disc = 144-56; roots = [(-12+sqrt(disc))/4, (-12-sqrt(disc))/4]
    assert all(close_(2*(x*x-1)+3, (2*x+3)**2-1) for x in roots)
    T(t,"Hard","f(x) = 2x + 3 and g(x) = x² − 1. What is the sum of all real x for which f(g(x)) = g(f(x))?",
      round(sum(roots)), "f(g(x)) = 2x² + 1 and g(f(x)) = (2x + 3)² − 1 = 4x² + 12x + 8. Setting them equal gives 2x² + 12x + 7 = 0. The discriminant is 144 − 56 > 0, so both roots are real, and their sum is −12/2 = −6.", chk=(sum(roots),-6))
    # f(x)+2f(1/x)=3x
    f2 = F(-1); fh = F(3,2) - 2*f2
    assert f2 + 2*fh == 6 and fh + 2*f2 == F(3,2)
    M(t,"Hard","f(x) + 2f(1/x) = 3x for every non-zero real x. What is f(2)?",
      ["−1","1","2","−2"], "−1", "x = 2: f(2) + 2f(1/2) = 6. x = 1/2: f(1/2) + 2f(2) = 3/2. From the second, f(1/2) = 3/2 − 2f(2). Substituting: f(2) + 3 − 4f(2) = 6 ⇒ f(2) = −1.")
    mn = min(abs(x/100-2)+abs(x/100-5) for x in range(-1000,1000))
    M(t,"Medium","What is the minimum value of f(x) = |x − 2| + |x − 5|?",
      ["0","2","3","7"], "3", "The sum of distances from x to 2 and to 5 is smallest (= 5 − 2 = 3) for any x between 2 and 5.", chk=(mn,3))

    # ---------- Logarithms ----------
    t = "Logarithms"
    x = 2**(3**2)
    M(t,"Medium","If log₂(log₃(log₂ x)) = 1, what is x?",
      ["64","256","512","1024"], str(x), "log₃(log₂ x) = 2 ⇒ log₂ x = 9 ⇒ x = 2⁹ = 512.", chk=(math.log2(math.log(math.log2(x),3)),1))
    T(t,"Medium","Given log₁₀ 2 = 0.3010, how many digits does 2⁵⁰ have?",
      len(str(2**50)), "log₁₀ 2⁵⁰ = 50 × 0.3010 = 15.05. The number of digits = ⌊15.05⌋ + 1 = 16.", chk=(len(str(2**50)),16))
    sols = [x for x in range(2,100) if (x-1)*(x+1) == 8]
    M(t,"Medium","Solve log₂(x − 1) + log₂(x + 1) = 3.",
      ["x = 3","x = −3","x = ±3","x = 9"], "x = 3", "log₂[(x − 1)(x + 1)] = 3 ⇒ x² − 1 = 8 ⇒ x = ±3. But x − 1 > 0 is needed for the log, so only x = 3 works.")
    assert sols == [3]

    # ---------- Number System ----------
    t = "Number System"
    T(t,"Medium","What is the remainder when 7¹⁰⁰ is divided by 13?",
      pow(7,100,13), f"7¹² ≡ 1 (mod 13) by Fermat's little theorem. 100 = 12 × 8 + 4, so 7¹⁰⁰ ≡ 7⁴ = 2401 = 13 × 184 + 9 ≡ 9.", chk=(pow(7,100,13),9))
    N = 2**4*3**3*5**2; sq = sum(1 for d in range(1,N+1) if N%d==0 and math.isqrt(d)**2==d)
    T(t,"Medium","How many divisors of 2⁴ × 3³ × 5² are perfect squares?",
      sq, "A square divisor needs even exponents: 2 ∈ {0, 2, 4} (3 ways), 3 ∈ {0, 2} (2 ways), 5 ∈ {0, 2} (2 ways). 3 × 2 × 2 = 12.", chk=(sq,12))
    sd = sum(d for d in range(1,73) if 72%d==0)
    M(t,"Medium","What is the sum of all positive divisors of 72?",
      ["168","180","195","210"], str(sd), "72 = 2³ × 3². Sum = (1 + 2 + 4 + 8)(1 + 3 + 9) = 15 × 13 = 195.")
    p3 = sum(100//3**k for k in range(1,6))
    M(t,"Medium","What is the highest power of 3 that divides 100!?",
      ["33","44","48","50"], str(p3), "⌊100/3⌋ + ⌊100/9⌋ + ⌊100/27⌋ + ⌊100/81⌋ = 33 + 11 + 3 + 1 = 48.")
    n = next(n for n in range(1,10000) if all(n%m==3 for m in (5,6,8)) and n%9==0)
    M(t,"Hard","What is the smallest number that leaves remainder 3 when divided by 5, 6 or 8, and is divisible by 9?",
      ["123","243","363","483"], str(n), "Such numbers are 120k + 3. We need 120k + 3 ≡ 0 (mod 9). 120 ≡ 3, so 3k + 3 ≡ 0 (mod 9) ⇒ k ≡ 2 (mod 3). Smallest k = 2 ⇒ 243.")
    M(t,"Hard","What are the last two digits of 3⁴⁰?",
      ["01","21","41","81"], f"{pow(3,40,100):02d}", "3²⁰ ≡ 1 (mod 100) (Carmichael's λ(100) = 20; check 3¹⁰ = 59049 ≡ 49 and 49² = 2401 ≡ 01). So 3⁴⁰ ≡ 1 ⇒ last two digits 01.")
    c = sum(1 for n in range(100,1000) if n%6==0 and n%9)
    T(t,"Hard","How many three-digit numbers are divisible by 6 but not by 9?",
      c, "Multiples of 6 in 100–999: 166 − 16 = 150. Those also divisible by 9 are multiples of 18: 55 − 5 = 50. 150 − 50 = 100.", chk=(c,100))

    # ---------- Geometry ----------
    t = "Geometry"
    area = 0.5*10*12; s_ = 18; r = F(60,18)
    M(t,"Medium","In triangle ABC, AB = AC = 13 cm and BC = 10 cm. What is the inradius?",
      ["3 cm","10/3 cm","4 cm","13/4 cm"], "10/3 cm", "The height to BC is √(13² − 5²) = 12, so area = 60. s = (13 + 13 + 10)/2 = 18. r = Area/s = 60/18 = 10/3 cm.", chk=(area/s_, 10/3))
    T(t,"Medium","A chord of a circle of radius 10 cm is 6 cm from the centre. What is the length of the chord (in cm)?",
      int(2*sqrt(100-36)), "Half-chord = √(10² − 6²) = 8, so the chord is 16 cm.", chk=(2*sqrt(64),16))
    M(t,"Hard","From a point P 13 cm from the centre O of a circle of radius 5 cm, tangents PA and PB are drawn. What is the area of quadrilateral OAPB?",
      ["30 cm²","60 cm²","65 cm²","120 cm²"], "60 cm²", "Tangent length = √(13² − 5²) = 12. OAPB is two right triangles, each (1/2) × 5 × 12 = 30, so the area is 60 cm².", chk=(2*0.5*5*12,60))
    M(t,"Medium","What is the area of a regular hexagon with side 6 cm?",
      ["36√3 cm²","54√3 cm²","72√3 cm²","108 cm²"], "54√3 cm²", "A regular hexagon is 6 equilateral triangles: 6 × (√3/4) × 36 = 54√3 cm².", chk=(6*sqrt(3)/4*36, 54*sqrt(3)))
    # circumcentre (3,4), incentre (2,2)
    a_,b_,c_ = 10,8,6  # opposite to A(0,0)? compute generally
    A_,B_,C_ = (0,0),(6,0),(0,8)
    la = math.dist(B_,C_); lb = math.dist(A_,C_); lc = math.dist(A_,B_)
    I = ((la*A_[0]+lb*B_[0]+lc*C_[0])/(la+lb+lc), (la*A_[1]+lb*B_[1]+lc*C_[1])/(la+lb+lc))
    O = (3,4); d = math.dist(I,O)
    M(t,"Hard","A triangle has vertices (0, 0), (6, 0) and (0, 8). What is the distance between its circumcentre and its incentre?",
      ["√3","2","√5","3"], "√5", "It's right-angled at the origin, so the circumcentre is the hypotenuse midpoint (3, 4) and R = 5. Inradius r = (6 + 8 − 10)/2 = 2, so the incentre is (2, 2). Distance = √(1² + 2²) = √5. (Check: Euler's OI² = R² − 2Rr = 25 − 20 = 5.)", chk=(d,sqrt(5)))

    # ---------- Mensuration ----------
    t = "Mensuration"
    n = (4/3*pi*6**3)/(1/3*pi*9*4)
    T(t,"Medium","A solid metal sphere of radius 6 cm is melted and recast into solid cones of base radius 3 cm and height 4 cm. How many cones are made?",
      round(n), "Sphere volume = (4/3)π × 216 = 288π. Cone volume = (1/3)π × 9 × 4 = 12π. 288π/12π = 24 cones.", chk=(n,24))
    M(t,"Hard","A 12 × 8 × 6 cm cuboid is painted on all faces and cut into 1 cm cubes. How many cubes have no painted face?",
      ["192","240","280","320"], str(10*6*4), "The unpainted cubes form the inner block (12 − 2) × (8 − 2) × (6 − 2) = 10 × 6 × 4 = 240.", chk=(sum(1 for x in range(12) for y in range(8) for z in range(6) if 0<x<11 and 0<y<7 and 0<z<5),240))
    M(t,"Medium","The space diagonal of a cube is 6√3 cm. What is its total surface area?",
      ["108 cm²","144 cm²","216 cm²","324 cm²"], "216 cm²", "Diagonal = a√3 ⇒ a = 6. TSA = 6a² = 216 cm².")

    # ---------- P&C ----------
    t = "Permutations & Combinations"
    arr = set(itertools.permutations("BANANA")); notog = sum(1 for p in arr if "NN" not in "".join(p))
    T(t,"Medium","In how many arrangements of the letters of BANANA are the two N's not next to each other?",
      notog, "Total = 6!/(3! 2!) = 60. With the N's together (treat NN as one block): 5!/3! = 20. Not together = 60 − 20 = 40.", chk=(notog,40))
    ways = sum(1 for c in itertools.product(range(1,11),repeat=4) if sum(c)==10)
    T(t,"Medium","In how many ways can 10 identical chocolates be distributed among 4 children so that each child gets at least one?",
      ways, "Give each child one first, then share the remaining 6 freely: C(6 + 3, 3) = C(9, 3) = 84. (Equivalently, C(9, 3) by stars and bars.)", chk=(ways,84))
    M(t,"Medium","How many rectangles (including squares) are there on an 8 × 8 chessboard?",
      ["1,024","1,296","2,016","204"], f"{comb(9,2)**2:,}", "Pick 2 of the 9 horizontal lines and 2 of the 9 vertical lines: C(9, 2)² = 36² = 1,296. (204 is the number of squares.)")
    inc = sum(1 for n in range(1000,10000) if all(a<b for a,b in zip(str(n),str(n)[1:])))
    M(t,"Hard","How many four-digit numbers have digits that strictly increase from left to right (e.g. 1357)?",
      ["84","120","126","210"], str(inc), "0 can't appear (it would have to come first). Any 4 distinct digits from 1–9 can be arranged in increasing order in exactly one way: C(9, 4) = 126.", chk=(inc,comb(9,4)))

    # ---------- Probability ----------
    t = "Probability"
    p = F(sum(1 for d in itertools.product(range(1,7),repeat=3) if sum(d)==10), 216)
    M(t,"Medium","Three fair dice are rolled. What is the probability that the sum is 10?",
      ["1/8","1/9","5/36","1/6"], f"{p.numerator}/{p.denominator}", "There are 27 ordered triples summing to 10 (e.g. permutations of (1,3,6), (1,4,5), (2,2,6), (2,3,5), (2,4,4), (3,3,4) give 6+6+3+6+3+3 = 27). 27/216 = 1/8.")
    p = F(2*comb(4,2), comb(52,2))
    M(t,"Medium","Two cards are drawn at random from a standard 52-card deck. What is the probability that both are aces or both are kings?",
      ["1/221","2/221","4/663","1/169"], f"{p.numerator}/{p.denominator}", "P = [C(4, 2) + C(4, 2)]/C(52, 2) = 12/1326 = 2/221.")
    pA = sum(F(1,2)**(2*k+1) for k in range(200))
    M(t,"Hard","A and B take turns tossing a fair coin, A first. The first to get a head wins. What is the probability that A wins?",
      ["1/2","2/3","3/4","3/5"], "2/3", "A wins on toss 1, 3, 5, …: 1/2 + 1/8 + 1/32 + … = (1/2)/(1 − 1/4) = 2/3.", chk=(float(pA),2/3))

    # ---------- Progressions ----------
    t = "Progressions"
    sm = sum(n for n in range(10,100) if n%5==2)
    T(t,"Medium","What is the sum of all two-digit numbers that leave remainder 2 when divided by 5?",
      sm, "The numbers are 12, 17, …, 97: an AP with 18 terms. Sum = 18 × (12 + 97)/2 = 981.", chk=(sm,981))
    a, d = 5, 3; assert a+4*d == 17 and a+11*d == 38
    M(t,"Medium","The 5th term of an AP is 17 and the 12th term is 38. What is the 20th term?",
      ["59","62","65","68"], str(a+19*d), "7d = 38 − 17 = 21 ⇒ d = 3, and a = 17 − 12 = 5. T₂₀ = 5 + 19 × 3 = 62.")
    r = 1 - F(4,12); s3 = 4*(1+r+r*r)
    M(t,"Hard","An infinite GP has first term 4 and sum 12. What is the sum of its first three terms?",
      ["76/9","8","26/3","28/3"], f"{s3.numerator}/{s3.denominator}", "4/(1 − r) = 12 ⇒ r = 2/3. S₃ = 4 + 8/3 + 16/9 = (36 + 24 + 16)/9 = 76/9.")
    tri = sum(k*(k+1)//2 for k in range(1,21))
    T(t,"Hard","What is the sum of the first 20 terms of the series 1, 3, 6, 10, 15, …?",
      tri, "The terms are triangular numbers k(k + 1)/2. Their sum up to n is n(n + 1)(n + 2)/6 = 20 × 21 × 22/6 = 1,540.", chk=(tri,1540))

def close_(a,b): return abs(a-b) < 1e-9


# ======================= EASY LEVEL (appended so existing IDs never shift) =======================
def fmt(x): return str(int(x)) if F(x).denominator == 1 else str(float(x))
def build_easy(B):
    s = "qa"
    M = lambda *a, **k: B.mcq(s, *a, **k)
    T = lambda *a, **k: B.tita(s, *a, **k)

    # ----- 25 questions from the user's reference set "CAT Quant: 25 Easy-level Questions" (AptiSetu Set E1),
    # transcribed with their solutions; every answer is recomputed here.
    x = 100 * (1 - F(110, 125)); assert x == 12
    M("Percentages & Profit", "Easy", "The price of a gadget is first raised by 25% and then reduced by x%, so that the final price is 10% above the original price. What is x?",
      ["10%", "12%", "12.5%", "15%"], "12%", "1.25 × (1 − x/100) = 1.10, so 1 − x/100 = 0.88 and x = 12.")
    mp = F(108, 100) / (F(8, 10) * F(9, 10)); assert (mp - 1) * 100 == 50
    M("Percentages & Profit", "Easy", "A shopkeeper allows successive discounts of 20% and 10% on the marked price and still earns a profit of 8% on cost price. By what percentage is the marked price above the cost price?",
      ["40%", "45%", "50%", "55%"], "50%", "Selling price = 0.8 × 0.9 × MP = 0.72 MP = 1.08 CP. So MP = 1.5 CP, i.e. 50% above cost.")
    v = next(v for v in range(1, 200) if F(2, F(1, 20) + F(1, v)) == 24)
    T("Time, Speed & Distance", "Easy", "A cyclist covers the first half of a journey at 20 km/h. At what speed (in km/h) must he cover the second half so that his average speed for the whole journey is 24 km/h?",
      v, "Average speed is the harmonic mean for equal distances: 2/(1/20 + 1/v) = 24, so 1/20 + 1/v = 1/12 and 1/v = 1/30. Hence v = 30.", chk=(v, 30))
    d = 4 + (1 - 4 * (F(1, 12) + F(1, 18))) / F(1, 18); assert d == 12
    M("Time & Work", "Easy", "A can finish a job in 12 days and B in 18 days. They work together for 4 days, after which A leaves. In how many days in all is the job completed?",
      ["10", "11", "12", "14"], "12", "In 4 days together: 4 × (1/12 + 1/18) = 4 × 5/36 = 5/9 of the work. The remaining 4/9 is done by B at 1/18 per day, which takes 8 days. Total = 4 + 8 = 12 days.")
    x = next(x for x in range(1, 120) if 72 - F(3, 5) * x == 48 - F(2, 5) * x + x)
    T("Mixtures & Alligation", "Easy", "A vessel holds 120 litres of milk and water in the ratio 3 : 2. How many litres of the mixture must be drawn out and replaced by water so that milk and water become equal in quantity?",
      x, "Milk = 72 L. Removing x litres of mixture removes 0.6x litres of milk. We need 72 − 0.6x = 60, so x = 20.", chk=(x, 20))
    T("Averages", "Easy", "The average of 11 numbers is 30. The average of the first six is 28 and the average of the last six is 33. What is the sixth number?",
      6 * 28 + 6 * 33 - 330, "Sum of all = 330. The sixth number is counted in both groups: 6×28 + 6×33 = 168 + 198 = 366. So the sixth number = 366 − 330 = 36.", chk=(6 * 28 + 6 * 33 - 330, 36))
    M("Number System", "Easy", "What is the remainder when 2<sup>100</sup> is divided by 7?",
      ["1", "2", "4", "6"], str(pow(2, 100, 7)), "2³ = 8 ≡ 1 (mod 7). 100 = 3 × 33 + 1, so 2¹⁰⁰ ≡ 2¹ = 2.")
    z = len(str(math.factorial(75))) - len(str(math.factorial(75)).rstrip("0"))
    T("Number System", "Easy", "How many zeroes does 75! end with?",
      z, "Count the factors of 5: ⌊75/5⌋ + ⌊75/25⌋ = 15 + 3 = 18.", chk=(z, 18))
    xr = (5 + sqrt(21)) / 2; assert close_(xr ** 3 + 1 / xr ** 3, 110)
    T("Equations & Quadratics", "Easy", "If x + 1/x = 5, find the value of x³ + 1/x³.",
      110, "x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x) = 125 − 15 = 110.", chk=(xr ** 3 + 1 / xr ** 3, 110))
    k = next(k for k in range(-50, 50) if 49 - 4 * k == 9)
    M("Equations & Quadratics", "Easy", "The roots of x² − 7x + k = 0 differ by 3. What is the value of k?",
      ["8", "10", "12", "14"], str(k), "Let the roots be a and a + 3. Sum = 2a + 3 = 7, so a = 2. The roots are 2 and 5, so k = product = 10.")
    s_ = 21; ar = sqrt(s_ * 8 * 7 * 6); assert ar == 84 and ar / s_ == 4
    M("Geometry", "Easy", "The sides of a triangle are 13 cm, 14 cm and 15 cm. What is the radius of its incircle?",
      ["3 cm", "3.5 cm", "4 cm", "4.5 cm"], "4 cm", "s = 21; area = √(21×8×7×6) = 84. Inradius = area / s = 84/21 = 4 cm.")
    assert sqrt(12 ** 2 + 5 ** 2) == 13
    M("Geometry", "Easy", "A chord of length 24 cm is at a distance of 5 cm from the centre of a circle. What is the radius of the circle?",
      ["12 cm", "13 cm", "14 cm", "15 cm"], "13 cm", "Half-chord = 12. Radius² = 12² + 5² = 169, so r = 13 cm.")
    inc = (F(6, 5) ** 3 - 1) * 100
    T("Mensuration", "Easy", "Each edge of a cube is increased by 20%. By what percentage (to one decimal place) does its volume increase?",
      inc, "New volume = 1.2³ = 1.728 times the old one, so the increase is 72.8%.", chk=(inc, F(728, 10)))
    dd = 10000 * (F(11, 10) ** 3 - 1) - 3000
    T("Simple & Compound Interest", "Easy", "A sum of ₹10,000 is invested for 3 years at 10% per annum. Find (in ₹) the difference between the compound interest (annual compounding) and the simple interest.",
      dd, "CI = 10000 × (1.1³ − 1) = 3310. SI = 3000. Difference = ₹310.", chk=(dd, 310))
    ban = sum(1 for p in set(itertools.permutations("BANANA")) if "AA" not in "".join(p))
    M("Permutations & Combinations", "Easy", "In how many ways can the letters of the word BANANA be arranged so that no two A's are adjacent?",
      ["6", "10", "12", "20"], str(ban), "Arrange B, N, N first: 3!/2! = 3 ways. This creates 4 gaps; choose 3 of them for the A's: C(4,3) = 4. Total = 3 × 4 = 12.")
    pp = F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b in (2, 3, 5, 7, 11)), 36)
    M("Probability", "Easy", "Two fair dice are thrown. What is the probability that the sum of the numbers is a prime number?",
      ["1/3", "5/12", "7/18", "1/2"], f"{pp.numerator}/{pp.denominator}", "Prime sums: 2 (1 way), 3 (2), 5 (4), 7 (6), 11 (2) = 15 favourable outcomes out of 36. Probability = 15/36 = 5/12.")
    S_ = lambda n: 3 * n * n + 2 * n
    T("Progressions", "Easy", "The sum of the first n terms of a sequence is 3n² + 2n. Find its 10th term.",
      S_(10) - S_(9), "T₁₀ = S₁₀ − S₉ = (300 + 20) − (243 + 18) = 320 − 261 = 59.", chk=(S_(10) - S_(9), 59))
    gp = [t for t in itertools.combinations_with_replacement(range(1, 22), 3) if sum(t) == 21 and t[0] * t[1] * t[2] == 216 and t[1] * t[1] == t[0] * t[2]]
    assert gp == [(3, 6, 12)], gp
    T("Progressions", "Easy", "Three numbers in geometric progression have a sum of 21 and a product of 216. What is the largest of them?",
      12, "Let them be 6/r, 6, 6r (the middle term is the cube root of 216). Then 6/r + 6 + 6r = 21, so r + 1/r = 5/2, giving r = 2 or 1/2. The numbers are 3, 6, 12, so the largest is 12.", chk=(max(gp[0]), 12))
    xl = next(x for x in range(1, 1000) if close_(math.log2(x) + math.log(x, 4), 6))
    M("Logarithms", "Easy", "If log₂ x + log₄ x = 6, what is x?",
      ["8", "12", "16", "32"], str(xl), "log₄ x = (1/2) log₂ x, so (3/2) log₂ x = 6, giving log₂ x = 4 and x = 16.")
    ni = sum(1 for x in range(-50, 50) if abs(x - 3) < 5 and x * x <= 16)
    T("Inequalities", "Easy", "How many integers x satisfy both |x − 3| &lt; 5 and x² ≤ 16?",
      ni, "|x − 3| &lt; 5 gives −2 &lt; x &lt; 8. x² ≤ 16 gives −4 ≤ x ≤ 4. Common integers: −1, 0, 1, 2, 3, 4, which is 6.", chk=(ni, 6))
    c_ = F(54) / F(6, 5); r_ = (55 - c_) / (c_ - 40); assert r_ == 2
    M("Mixtures & Alligation", "Easy", "Two varieties of rice costing ₹40/kg and ₹55/kg are mixed and the mixture is sold at ₹54/kg at a profit of 20%. In what ratio were the cheaper and dearer varieties mixed?",
      ["1 : 2", "2 : 1", "3 : 2", "3 : 1"], "2 : 1", "Cost price of the mixture = 54/1.2 = ₹45. By alligation, cheaper : dearer = (55 − 45) : (45 − 40) = 10 : 5 = 2 : 1.")
    st = (F(36, 3) - F(36, F(9, 2))) / 2
    T("Time, Speed & Distance", "Easy", "A boat travels 36 km downstream in 3 hours and returns the same 36 km upstream in 4.5 hours. What is the speed of the stream in km/h?",
      st, "Downstream = 12 km/h, upstream = 8 km/h. Stream = (12 − 8)/2 = 2 km/h.", chk=(st, 2))
    tm = 1 / (F(1, 20) + F(1, 30) - F(1, 60))
    M("Time & Work", "Easy", "Pipe A fills a tank in 20 minutes, pipe B in 30 minutes, and pipe C empties it in 60 minutes. If all three are opened together, in how many minutes is the empty tank filled?",
      ["12", "15", "18", "24"], str(tm), "Net rate = 1/20 + 1/30 − 1/60 = (3 + 2 − 1)/60 = 4/60 = 1/15. Time = 15 minutes.")
    son = next(s for s in range(13, 100) if 3 * s - 12 == 7 * (s - 12))
    T("Equations & Quadratics", "Easy", "A father is three times as old as his son. Twelve years ago he was seven times as old as the son was then. What is the father's present age (in years)?",
      3 * son, "F = 3S and F − 12 = 7(S − 12). So 3S − 12 = 7S − 84, giving S = 18 and F = 54.", chk=(3 * son, 54))
    M("Sets", "Easy", "In a class of 60 students, 35 play cricket, 30 play football and 10 play neither. How many students play both games?",
      ["10", "15", "20", "25"], str(35 + 30 - (60 - 10)), "Students playing at least one game = 60 − 10 = 50. Both = 35 + 30 − 50 = 15.")

    # ----- 25 AptiSetu-written Easy questions (drafts E1-E25, verified by easy_qa_check.py and again below)
    assert (fmt((1 - F(4, 5)) * 100) + "%") == "20%", "E1"
    M("Percentages & Profit", "Easy", "The price of sugar rises by 25%. By what percentage must a family cut its sugar consumption so that its spending on sugar stays the same?",
      ["20%", "25%", "22.5%", "16.67%"], "20%",
      "New price = 1.25 × old. To keep spending equal, consumption must become 1/1.25 = 0.8 of the old, a cut of 20%.")
    assert ("Loss of ₹100" if 2400 - (F(1200) / F(6, 5) + F(1200) / F(4, 5)) == -100 else "?") == "Loss of ₹100", "E2"
    M("Percentages & Profit", "Easy", "A shopkeeper sells two phones for ₹1,200 each, making a 20% profit on one and a 20% loss on the other. What is his overall result?",
      ["No profit, no loss", "Loss of ₹100", "Loss of ₹48", "Profit of ₹100"], "Loss of ₹100",
      "Cost prices are 1200/1.2 = ₹1,000 and 1200/0.8 = ₹1,500. Total cost ₹2,500, total revenue ₹2,400, so a loss of ₹100.")
    assert (str(next(w for w in range(100) if F(30, 10 + w) == F(3, 2)))) == "10", "E3"
    T("Mixtures & Alligation", "Easy", "A 40-litre mixture contains milk and water in the ratio 3 : 1. How many litres of water must be added to make the ratio 3 : 2?",
      10, "Milk = 30 L and water = 10 L. Milk stays 30 L, so for 3 : 2 water must be 20 L. Add 20 − 10 = 10 litres.")
    assert (str(next(t for t in range(1, 100) if 1 + t * F(1, 5) == 4))) == "15", "E4"
    T("Simple & Compound Interest", "Easy", "A sum of money doubles itself in 5 years at simple interest. In how many years will it become four times itself at the same rate?",
      15, "Doubling means the interest equals the principal in 5 years, so the rate is 20% a year. Four times needs interest of 300%, which takes 300/20 = 15 years (not 10: simple interest does not compound).")
    assert (str(next(d for d in range(1, 50) if F(d, 5) - F(d, 6) == F(1, 6))) + " km") == "5 km", "E5"
    M("Time, Speed & Distance", "Easy", "Walking at 5 km/h, Meena reaches her office 6 minutes late. Walking at 6 km/h, she reaches 4 minutes early. How far is her office?",
      ["6 km", "4 km", "5 km", "7.5 km"], "5 km",
      "The two times differ by 6 + 4 = 10 minutes = 1/6 h. So d/5 − d/6 = d/30 = 1/6, giving d = 5 km.")
    assert (fmt(F(250) / ((54 + 36) * F(5, 18))) + " seconds") == "10 seconds", "E6"
    M("Time, Speed & Distance", "Easy", "Two trains, 150 m and 100 m long, run on parallel tracks in opposite directions at 54 km/h and 36 km/h. How long do they take to cross each other completely?",
      ["12.5 seconds", "25 seconds", "50 seconds", "10 seconds"], "10 seconds",
      "Relative speed = 90 km/h = 25 m/s. Distance to cover = 150 + 100 = 250 m. Time = 250/25 = 10 s.")
    assert (fmt(F(108) / (4 * F(3, 2) + 6))) == "9", "E7"
    M("Time & Work", "Easy", "6 men or 9 women can finish a job in 12 days. In how many days will 4 men and 6 women together finish it?",
      ["9", "8", "10", "12"], "9",
      "6 men = 9 women, so 1 man = 1.5 women. The job is 9 × 12 = 108 woman-days. 4 men + 6 women = 6 + 6 = 12 women, so 108/12 = 9 days.")
    assert (str(31 * 16 - 30 * 15)) == "46", "E8"
    T("Averages", "Easy", "The average age of 30 students in a class is 15 years. When the teacher's age is included, the average rises by 1 year. What is the teacher's age in years?",
      46, "Students' total = 450. With the teacher, 31 people average 16, total 496. Teacher = 496 − 450 = 46 (the trap is 16: the teacher must also lift everyone else's average by 1).")
    assert ("₹" + str(2100 * 15 // 35)) == "₹900", "E9"
    M("Ratio & Proportion", "Easy", "₹2,100 is divided among A, B and C such that A : B = 2 : 3 and B : C = 4 : 5. What is C's share?",
      ["₹750", "₹900", "₹600", "₹840"], "₹900",
      "Make B common: A : B = 8 : 12 and B : C = 12 : 15, so A : B : C = 8 : 12 : 15 (35 parts). C = 2100 × 15/35 = ₹900.")
    assert (fmt((120 - 75 * F(11, 10) - 25) / 25 * 100) + "%") == "50%", "E10"
    M("Percentages & Profit", "Easy", "Ravi spends 75% of his income. His income rises by 20% and his spending rises by 10%. By what percentage do his savings increase?",
      ["30%", "40%", "50%", "10%"], "50%",
      "Take income 100: spending 75, savings 25. New income 120, new spending 82.5, new savings 37.5. Increase = 12.5/25 = 50%.")
    assert (str(round(sum(((5 + s * sqrt(13)) / 2) ** 2 for s in (1, -1))))) == "19", "E11"
    T("Equations & Quadratics", "Easy", "If α and β are the roots of x² − 5x + 3 = 0, find the value of α² + β².",
      19, "α + β = 5 and αβ = 3, so α² + β² = (α + β)² − 2αβ = 25 − 6 = 19. No need to find the roots.")
    assert (str(sum(1 for x in range(-100, 101) if abs(x - 3) + abs(x + 2) <= 9))) == "10", "E12"
    T("Inequalities", "Easy", "How many integers x satisfy |x − 3| + |x + 2| ≤ 9?",
      10, "Between −2 and 3 the sum is always 5. For x > 3 it is 2x − 1 ≤ 9, so x ≤ 5; for x < −2 it is 1 − 2x ≤ 9, so x ≥ −4. So x runs from −4 to 5: 10 integers.")
    assert (fmt((6 * 1 - 2 * F(3, 2)) / (1 * 1 - 2 * 2)).replace("-", "−")) == "−1", "E13"
    M("Functions", "Easy", "A function satisfies f(x) + 2f(1/x) = 3x for every x ≠ 0. What is f(2)?",
      ["1", "2", "−2", "−1"], "−1",
      "Put x = 2: f(2) + 2f(1/2) = 6. Put x = 1/2: f(1/2) + 2f(2) = 3/2. From the second, f(1/2) = 3/2 − 2f(2); substitute: f(2) + 3 − 4f(2) = 6, so f(2) = −1.")
    assert (str(len(str(2 ** 50)))) == "16", "E14"
    M("Logarithms", "Easy", "Given log₁₀2 = 0.301, how many digits does 2<sup>50</sup> have?",
      ["16", "15", "17", "50"], "16",
      "log₁₀(2<sup>50</sup>) = 50 × 0.301 = 15.05. A number whose log lies between 15 and 16 has 15 + 1 = 16 digits.")
    assert (str(int(10 * (2 * 2 + 19 * 4)))) == "800", "E15"
    T("Progressions", "Easy", "In an arithmetic progression the 4th term is 14 and the 9th term is 34. What is the sum of its first 20 terms?",
      800, "5d = 34 − 14 = 20, so d = 4 and the first term is 14 − 12 = 2. The 20th term is 2 + 76 = 78, so S₂₀ = 20 × (2 + 78)/2 = 800.")
    assert (str(sum(3 * 2 ** i for i in range(5)))) == "93", "E16"
    M("Progressions", "Easy", "In a geometric progression with real terms, the 3rd term is 12 and the 6th term is 96. What is the sum of the first 5 terms?",
      ["96", "93", "186", "90"], "93",
      "r³ = 96/12 = 8, so r = 2 and the first term is 12/4 = 3. Sum = 3(2⁵ − 1)/(2 − 1) = 93.")
    assert (str(sum(1 for x in range(1, 100) for y in range(1, 100) if 3 * x + 5 * y == 100))) == "6", "E17"
    M("Equations & Quadratics", "Easy", "How many ordered pairs of positive integers (x, y) satisfy 3x + 5y = 100?",
      ["7", "5", "6", "20"], "6",
      "100 − 5y must be a positive multiple of 3. 5y ≡ 1 (mod 3) means y ≡ 2 (mod 3): y = 2, 5, 8, 11, 14, 17 (y = 20 gives x = 0). That is 6 pairs.")
    assert (fmt(F(48, 10)) + " cm") == "4.8 cm", "E18"
    M("Geometry", "Easy", "A right triangle has legs 6 cm and 8 cm. What is the length of the altitude drawn to the hypotenuse?",
      ["5 cm", "4.5 cm", "5.2 cm", "4.8 cm"], "4.8 cm",
      "Hypotenuse = 10. Twice the area = 6 × 8 = 10 × h, so h = 4.8 cm.")
    assert (str(int(sqrt(100 - 36))) + " cm") == "8 cm", "E19"
    M("Geometry", "Easy", "Two circles of radii 7 cm and 1 cm have their centres 10 cm apart. What is the length of a direct (outer) common tangent?",
      ["8 cm", "6 cm", "4√6 cm", "10 cm"], "8 cm",
      "Direct common tangent = √(d² − (r₁ − r₂)²) = √(100 − 36) = 8 cm. (The trap is 6 cm, which uses r₁ + r₂: that is the transverse common tangent, √(100 − 64) = 6.)")
    assert (str(27 * 24)) == "648", "E20"
    T("Mensuration", "Easy", "A solid cube of side 6 cm is cut into identical cubes of side 2 cm. What is the total surface area, in cm², of all the small cubes together?",
      648, "There are (6/2)³ = 27 small cubes, each with surface area 6 × 2² = 24 cm². Total = 27 × 24 = 648 cm² (three times the original 216 cm²).")
    assert (str(next(k for k in range(3, 50) if F(180 * (k - 2), k) == 150) * 9 // 2)) == "54", "E21"
    M("Geometry", "Easy", "Each interior angle of a regular polygon is 150°. How many diagonals does it have?",
      ["66", "54", "48", "60"], "54",
      "Each exterior angle is 30°, so there are 360/30 = 12 sides. Diagonals = 12 × 9/2 = 54.")
    assert (f"{pow(7, 42, 100):02d}") == "49", "E22"
    M("Number System", "Easy", "What are the last two digits of 7<sup>42</sup>?",
      ["43", "07", "49", "01"], "49",
      "7⁴ = 2401 ends in 01, so 7⁴⁰ = (7⁴)¹⁰ also ends in 01. Then 7⁴² ends like 01 × 49 = 49.")
    assert (str(sum(1 for d in range(1, 721) if 720 % d == 0 and math.isqrt(d) ** 2 == d))) == "6", "E23"
    T("Number System", "Easy", "How many divisors of 720 are perfect squares?",
      6, "720 = 2⁴ × 3² × 5. A square divisor uses even exponents: 2 in {0, 2, 4} (3 ways), 3 in {0, 2} (2 ways), 5 in {0} (1 way). 3 × 2 × 1 = 6.")
    assert (str(sum(1 for c in itertools.combinations("MMMMMWWWW", 4) if c.count("W") >= 2))) == "81", "E24"
    M("Permutations & Combinations", "Easy", "A committee of 4 is to be chosen from 5 men and 4 women so that it has at least 2 women. In how many ways can this be done?",
      ["91", "60", "126", "81"], "81",
      "2 women: C(4,2) × C(5,2) = 60. 3 women: C(4,3) × 5 = 20. 4 women: 1. Total = 81. (126 is all committees, with no condition.)")
    assert ((lambda f: f"{f.numerator}/{f.denominator}")(F(sum(1 for k in range(1, 51) if k % 3 == 0 or k % 5 == 0), 50))) == "23/50", "E25"
    M("Probability", "Easy", "A number is picked at random from 1 to 50. What is the probability that it is divisible by 3 or by 5?",
      ["23/50", "13/25", "1/2", "2/5"], "23/50",
      "Multiples of 3: 16, of 5: 10, of both (15): 3. By inclusion–exclusion, 16 + 10 − 3 = 23, so 23/50.")

_build_main = build
def build(B):
    _build_main(B)
    build_easy(B)
