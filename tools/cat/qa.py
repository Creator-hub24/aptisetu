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
