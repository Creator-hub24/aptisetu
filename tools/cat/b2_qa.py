"""Practice pack b2, Quantitative Ability (30 original items, added 29 Oct 2026). Every answer is recomputed here,
by brute force or exact arithmetic, and the build stops if a check fails."""
import itertools, math
from fractions import Fraction as F

def build(B):
    s = "qa"; M = lambda *a, **k: B.mcq(s, *a, **k); T = lambda *a, **k: B.tita(s, *a, **k)
    # ---------------- Averages ----------------
    t = "Averages"
    sols = []
    for n in range(1, 300):
        a = F(84 - 3 * n)            # from (na+87)/(n+1) = a+3
        if a <= 0: continue
        assert (n * a + 87) / (n + 1) == a + 3
        if ((n + 1) * (a + 3) + 33) / (n + 2) == a + 1: sols.append((n, a))
    assert sols == [(10, 54)], sols
    T(t, "Medium", "A batsman scores 87 runs in an innings and his batting average goes up by 3. In his very next innings he scores 33 and his average falls by 2. How many innings had he played before the innings in which he scored 87?", 10,
      "Let him have played n innings with average a. After 87: (na + 87)/(n + 1) = a + 3, so 87 = a + 3n + 3, i.e. a = 84 − 3n. After 33 the average is a + 1 over n + 2 innings: (n + 1)(a + 3) + 33 = (n + 2)(a + 1), which simplifies to 33 = a − 2n − 1, i.e. a = 2n + 34. So 84 − 3n = 2n + 34, giving n = 10 (and a = 54). Check: 540 + 87 = 627 = 11 × 57; 627 + 33 = 660 = 12 × 55.")
    sols = [(n, k) for n in range(2, 2000) for k in range(1, n + 1) if F(n * (n + 1) // 2 - k, n - 1) == F(35 * 69 + 47, 69)]
    assert sols == [(70, 23)], sols
    T(t, "Hard", "The integers 1, 2, 3, …, n are written on a board and one of them is erased. The average of the numbers left is 35 47/69. Which number was erased?", 23,
      "Erasing one number from 1…n leaves an average between n/2 (if n is erased) and (n + 2)/2 (if 1 is erased). So n/2 ≤ 35.68 ≤ (n + 2)/2, i.e. n = 70 or 71. The remaining count n − 1 must be a multiple of 69 for the average to have denominator 69, so n = 70. The sum 1 + … + 70 = 2485, and the remaining sum is 69 × (35 + 47/69) = 2415 + 47 = 2462. The erased number is 2485 − 2462 = 23. A full search over all n and all erased numbers confirms this is the only possibility.")
    sols = []
    for P in range(1, 400):
        for Fl in range(1, 400):
            if F(65 * P + 35 * Fl, P + Fl) == 53 and F(65 * P + 5 * 40, P + 5) == F(125, 2) and Fl >= 5 and F(35 * Fl - 200, Fl - 5) < 35: sols.append((P, Fl))
    assert sols == [(45, 30)], sols
    T(t, "Hard", "In an examination, the students who passed averaged 65 marks, those who failed averaged 35, and the whole group averaged 53. On re-evaluation, five students who had failed, with an average of 40, were declared passed; the average of all passed students then became 62.5. How many students took the examination?", 75,
      "Passed : failed = (53 − 35) : (65 − 53) = 18 : 12 = 3 : 2. If P students passed originally, (65P + 5 × 40)/(P + 5) = 62.5, so 65P + 200 = 62.5P + 312.5 and P = 45. Then 30 failed, and the total is 45 + 30 = 75. (Check: (45 × 65 + 30 × 35)/75 = 53.)")
    vals = [(A, B_, C, D, E) for A in [24] for E in [46] for B_ in range(0, 100) for C in range(0, 100) for D in range(0, 100)
            if A + B_ + C == 90 and B_ + C + D == 102 and C + D + E == 114]
    assert {v[2] for v in vals} == {32}
    M(t, "Medium", "For five numbers A, B, C, D and E, the average of A, B and C is 30, the average of B, C and D is 34, and the average of C, D and E is 38. If A = 24 and E = 46, what is C?", ["28", "32", "34", "36"], "32",
      "A + B + C = 90 and B + C + D = 102, so D − A = 12 and D = 36. Then C + D + E = 114 gives C = 114 − 36 − 46 = 32. (B is then 34, and every average checks.)")
    # ---------------- Sets ----------------
    t = "Sets"
    sols = {(150 - 30 - e3 - e3, 30, e3)[2] for e3 in range(0, 151) if (150 - 30 - e3) + 2 * 30 + 3 * e3 == 210}
    assert sols == {15}
    T(t, "Medium", "Each of the 150 students of a college studies at least one of French, German and Spanish. 80 study French, 70 study German and 60 study Spanish. If exactly 30 students study exactly two of these languages, how many study all three?", 15,
      "Let e₁, e₂, e₃ be the numbers studying exactly one, two and three languages. Then e₁ + e₂ + e₃ = 150 and e₁ + 2e₂ + 3e₃ = 80 + 70 + 60 = 210. Subtracting, e₂ + 2e₃ = 60. With e₂ = 30, e₃ = 15.")
    best = None
    for abc in range(0, 91):
        for ab in range(0, 111):
            for ca in range(0, 91):
                bc = 120 - ab - ca - 2 * abc
                if bc < 0: continue
                a = 120 - ab - ca - abc; b = 110 - ab - bc - abc; c = 90 - bc - ca - abc
                if min(a, b, c) < 0: continue
                assert a + b + c + ab + bc + ca + abc == 200
                if best is None or a + b + c > best: best = a + b + c
    assert best == 140
    M(t, "Hard", "Each of 200 people reads at least one of three newspapers A, B and C. A is read by 120 people, B by 110 and C by 90. What is the maximum possible number of people who read exactly one newspaper?", ["110", "125", "140", "150"], "140",
      "With e₁, e₂, e₃ as the numbers reading exactly one, two and three papers: e₁ + e₂ + e₃ = 200 and e₁ + 2e₂ + 3e₃ = 320, so e₂ + 2e₃ = 120. e₁ = 200 − (e₂ + e₃) is largest when e₂ + e₃ is smallest, i.e. when e₂ = 0 and e₃ = 60, giving e₁ = 140. This is achievable: 60 read all three, and 60, 50 and 30 read only A, only B and only C.")
    best = None
    for x3 in range(0, 59):
        for x2 in range(0, 101):
            x1 = 195 - 2 * x2 - 3 * x3; x0 = 100 - x1 - x2 - x3
            if x1 < 0 or x0 < 0: continue
            # feasibility for the given sport totals: check with region search (pair regions)
            ok = False
            for cf in range(0, x2 + 1):
                for fh in range(0, x2 - cf + 1):
                    hc = x2 - cf - fh
                    c1 = 72 - cf - hc - x3; f1 = 65 - cf - fh - x3; h1 = 58 - fh - hc - x3
                    if min(c1, f1, h1) >= 0 and c1 + f1 + h1 == x1: ok = True; break
                if ok: break
            if ok and (best is None or x2 + x3 < best): best = x2 + x3
    assert best == 48
    M(t, "Hard", "Of a group of 100 tourists, 72 have visited Goa, 65 have visited Jaipur and 58 have visited Kochi. What is the minimum possible number of tourists who have visited at least two of these three cities?", ["43", "48", "50", "95"], "48",
      "Total visits = 72 + 65 + 58 = 195 among at most 100 tourists. With x₁, x₂, x₃ tourists who visited exactly one, two and three cities, x₁ + 2x₂ + 3x₃ = 195 and x₁ + x₂ + x₃ ≤ 100, so x₂ + 2x₃ ≥ 95. To make x₂ + x₃ small, make x₃ as large as possible: x₃ = 47 and x₂ = 1 gives 48, and nothing smaller works because x₂ + x₃ ≥ (x₂ + 2x₃)/2 ≥ 47.5. A valid split: 47 visited all three, 1 visited Goa and Jaipur only, and 24, 17 and 11 visited only Goa, only Jaipur and only Kochi (total 100).")
    tot = F(32) / F(20, 100); onlyS = tot * F(55 - 20, 100)
    assert tot == 160 and onlyS == 56 and F(45 + 55 - 20, 100) + F(20, 100) == 1
    M(t, "Medium", "In a class, 45% of the students like Mathematics, 55% like Science and 20% like both. If 32 students like neither subject, how many like Science but not Mathematics?", ["44", "56", "64", "72"], "56",
      "Students liking at least one = 45% + 55% − 20% = 80%, so 20% like neither: 20% = 32 gives a class of 160. Science only = 55% − 20% = 35% of 160 = 56.")
    # ---------------- Ratio & Proportion ----------------
    t = "Ratio & Proportion"
    sols = []
    for k in range(1, 5000):
        A, Bv, C = 3 * k, 4 * k, 5 * k
        for g10 in range(0, 11):   # C gives g10/10 of his savings
            a = F(2, 3) * A + F(g10, 10) * C; c = C - F(g10, 10) * C; b = F(6, 10) * Bv
            if a == c and c - b == 1320: sols.append((k, g10))
    assert sols == [(1200, 3)], sols
    T(t, "Hard", "The savings of A, B and C are in the ratio 3 : 4 : 5. A spends one-third of his savings and B spends 40% of hers. C then gives a part of his savings to A, after which A and C have equal amounts and B has ₹1,320 less than C. What were their total savings at the start, in ₹?", 14400,
      "Let the savings be 3k, 4k and 5k. A has 2k left and B has 2.4k. If C gives a fraction f of 5k to A, then 2k + 5kf = 5k − 5kf, so f = 0.3 and A = C = 3.5k. C − B = 3.5k − 2.4k = 1.1k = 1320, so k = 1200 and the total was 12k = ₹14,400.")
    Fx, v = None, None
    for vv in range(0, 5000):
        ff = 40 * 3000 - 40 * vv
        if ff + 60 * vv == 60 * 2500: Fx, v = ff, vv
    assert (Fx, v) == (60000, 1500) and (Fx + 100 * v) / 100 == 2100
    M(t, "Medium", "A hostel's monthly cost is partly fixed and partly proportional to the number of students. With 40 students the cost per student is ₹3,000 a month; with 60 students it is ₹2,500. What is the cost per student with 100 students?", ["₹1,800", "₹2,000", "₹2,100", "₹2,250"], "₹2,100",
      "Total cost = F + nv. 40 students: F + 40v = 1,20,000; 60 students: F + 60v = 1,50,000. So v = 1,500 and F = 60,000. For 100 students the total is 60,000 + 1,50,000 = 2,10,000, i.e. ₹2,100 per student.")
    xs = [x for x in range(1, 100000) if 12 * x == 8 * (x + 5000)]
    assert xs == [10000]; x = xs[0]; caps = [12 * x, 8 * (x + 5000), 6 * 2 * x]
    assert caps[2] * 45000 // sum(caps) == 15000
    T(t, "Medium", "A invests ₹x for 12 months, B invests ₹(x + 5,000) for 8 months and C invests ₹2x for 6 months in a business. A and B receive equal shares of the profit. If the total profit is ₹45,000, what is C's share, in ₹?", 15000,
      "Profit is shared in the ratio of (capital × time). A and B equal: 12x = 8(x + 5000), so x = 10,000. The products are A: 1,20,000, B: 8 × 15,000 = 1,20,000 and C: 6 × 20,000 = 1,20,000, all equal. So C gets one-third of ₹45,000 = ₹15,000.")
    # ---------------- Functions ----------------
    t = "Functions"
    f = {0: 0, 1: 3}
    for n in range(1, 10): f[n + 1] = f[n] + f[1] + 2 * n     # f(n+1) = f(n) + f(1) + 2n
    assert f[10] == 120 and all(f[n] == n * n + 2 * n for n in f)
    T(t, "Medium", "A function f satisfies f(x + y) = f(x) + f(y) + 2xy for all real x and y, and f(1) = 3. What is f(10)?", 120,
      "Putting y = 1: f(x + 1) = f(x) + 3 + 2x. With x = y = 0, f(0) = 0. Then f(n) = 3n + 2(0 + 1 + … + (n − 1)) = 3n + n(n − 1) = n² + 2n. So f(10) = 100 + 20 = 120.")
    def nroots(k):
        r = set()
        for c in (5 - k, 5 + k):         # x² − 6x + c = 0
            disc = 36 - 4 * c
            if disc > 0: r |= {(6 + math.sqrt(disc)) / 2, (6 - math.sqrt(disc)) / 2}
            elif disc == 0: r.add(3.0)
        return len({round(z, 9) for z in r})
    ks = [k for k in range(1, 50) if nroots(k) == 4]
    assert ks == [1, 2, 3] and nroots(4) == 3 and nroots(0) == 2
    M(t, "Hard", "For how many positive integer values of k does the equation |x² − 6x + 5| = k have exactly four distinct real solutions?", ["2", "3", "4", "Infinitely many"], "3",
      "y = x² − 6x + 5 = (x − 3)² − 4 dips to −4 at x = 3, so |y| has a 'hump' of height 4 at x = 3 between the roots 1 and 5. A horizontal line y = k meets the graph of |y| in four points when 0 < k < 4, in three points when k = 4 and in two points when k > 4. The positive integers with 0 < k < 4 are 1, 2 and 3: three values.")
    g = lambda x: max(2 * x - 3, 9 - x, x + 1)
    grid = min(g(F(i, 100)) for i in range(-2000, 2000)); assert grid == 5 and g(4) == 5 and 2 * 4 - 3 == 9 - 4 == 4 + 1
    M(t, "Medium", "What is the minimum value of f(x) = max(2x − 3, 9 − x, x + 1) over all real x?", ["4", "5", "13/3", "6"], "5",
      "9 − x decreases while 2x − 3 and x + 1 increase, so the maximum is smallest where the decreasing line meets the higher of the two rising lines. At x = 4 all three are equal: 2(4) − 3 = 5, 9 − 4 = 5, 4 + 1 = 5. For x < 4, 9 − x > 5; for x > 4, x + 1 > 5. So the minimum is 5.")
    # ---------------- Mixtures & Alligation ----------------
    t = "Mixtures & Alligation"
    xs = [x for x in range(0, 1000) if F(6 + F(x, 2), 30 + x) == F(38, 100)]
    assert xs == [45]
    T(t, "Medium", "A container holds 30 litres of a solution that is 20% acid. How many litres of a 50% acid solution must be added to it to obtain a solution that is 38% acid?", 45,
      "Acid: 0.2 × 30 + 0.5x = 0.38(30 + x), so 6 + 0.5x = 11.4 + 0.38x and 0.12x = 5.4, giving x = 45. (Alligation check: (50 − 38) : (38 − 20) = 12 : 18 = 2 : 3 = 30 : 45.)")
    milk = F(100); 
    for r in (20, 25, 40): milk = milk * (100 - r) / 100
    assert milk == 36
    M(t, "Medium", "A tank holds 100 litres of pure milk. 20 litres are drawn off and replaced with water. Then 25 litres of the mixture are drawn off and replaced with water. Finally 40 litres of the mixture are drawn off and replaced with water. What percentage of the final mixture is milk?", ["36%", "40%", "45%", "48%"], "36%",
      "Each draw-and-replace keeps the volume at 100 L and multiplies the milk by (1 − drawn/100): 100 × 0.80 × 0.75 × 0.60 = 36 L of milk in 100 L, i.e. 36%.")
    sols = [(xx, 25 - xx) for xx in range(0, 26) if F(80, 100) * xx + F(55, 100) * (25 - xx) == F(60, 100) * 30]
    assert sols == [(17, 8)]
    T(t, "Medium", "Vessel P contains a mixture that is 80% milk and vessel Q a mixture that is 55% milk (the rest is water in both). Some litres from P and some from Q are poured into an empty jar, and 5 litres of pure water are added, giving 30 litres of a mixture that is 60% milk. How many litres were taken from P?", 17,
      "The P and Q parts total 30 − 5 = 25 L, and they must contain all the milk, 60% of 30 = 18 L. With x litres from P: 0.8x + 0.55(25 − x) = 18, so 0.25x = 4.25 and x = 17 (and 8 L from Q).")
    # ---------------- Mensuration ----------------
    t = "Mensuration"
    r_, h_ = 6, 8; l_ = math.hypot(r_, h_); area = r_ * h_; semi = (2 * l_ + 2 * r_) / 2
    assert l_ == 10 and area / semi == 3
    T(t, "Medium", "A sphere is placed inside a right circular cone of base radius 6 cm and height 8 cm so that it touches the base and the curved surface all round. What is the radius of the sphere, in cm?", 3,
      "A vertical section through the axis is an isosceles triangle with base 12 and height 8, so each slant side is √(6² + 8²) = 10. The sphere's section is the circle inscribed in this triangle, with radius = area / semi-perimeter = (½ × 12 × 8)/((10 + 10 + 12)/2) = 48/16 = 3 cm.")
    # tank 2 m × 1.5 m, water 1 m deep; block 1.5 × 1 × 2 m (height 2 m) stood upright on the base
    h_part = F(3) / (F(3) - F(3, 2)); h_full = (F(3) + F(3)) / F(3)
    assert h_part == 2 and h_full == 2   # either way the level is exactly 2 m (the block's top)
    T(t, "Hard", "A rectangular tank with a base of 2 m × 1.5 m contains water to a depth of 1 m. A solid rectangular block measuring 1.5 m × 1 m × 2 m is stood upright on the floor of the tank on its 1.5 m × 1 m face. Assuming no water overflows, by how many centimetres does the water level rise?", 100,
      "The water volume is 2 × 1.5 × 1 = 3 m³. With the block standing in the tank, the free floor area is 3 − 1.5 = 1.5 m², so if the water stays below the block's top, its depth is 3/1.5 = 2 m. That equals the block's height of 2 m, so the assumption holds (and the block is just covered). The level rises from 1 m to 2 m, i.e. by 100 cm.")
    import sympy as sp
    hexa = sp.Rational(3, 2) * sp.sqrt(3) * 36; rin = 3 * sp.sqrt(3); diffA = sp.simplify(hexa - sp.pi * rin ** 2)
    assert sp.simplify(diffA - (54 * sp.sqrt(3) - 27 * sp.pi)) == 0
    M(t, "Medium", "A circle is inscribed in a regular hexagon of side 6 cm. What is the area of the region inside the hexagon but outside the circle, in cm²?", ["54√3 − 27π", "54√3 − 36π", "36√3 − 27π", "54√3 − 18π"], "54√3 − 27π",
      "Hexagon area = 6 × (√3/4) × 6² = 54√3. The inscribed circle's radius is the distance from the centre to a side, which is the height of one equilateral triangle: (√3/2) × 6 = 3√3, so its area is 27π. The region = 54√3 − 27π.")
    # ---------------- Logarithms ----------------
    t = "Logarithms"
    good = [x for x in range(-50, 50) if x - 2 > 0 and x - 2 != 1 and 10 - x > 0 and math.log(10 - x) / math.log(x - 2) > 0]
    assert good == [4, 5, 6, 7, 8]
    T(t, "Medium", "For how many integers x is log<sub>(x − 2)</sub>(10 − x) defined and positive?", 5,
      "Defined: base x − 2 > 0 and ≠ 1, and 10 − x > 0, so 2 < x < 10 with x ≠ 3. There is no integer with 0 < x − 2 < 1, so the base is greater than 1 for the integers left (x = 4 to 9), and the log is positive when 10 − x > 1, i.e. x < 9. So x = 4, 5, 6, 7, 8: five integers.")
    t_ = sp.symbols("t"); roots = sp.solve(t_ ** 2 - 5 * t_ + 6, t_); xs = sorted(2 ** r for r in roots); assert xs == [4, 8] and 4 * 8 == 32
    M(t, "Medium", "What is the product of all real x that satisfy (log₂ x)² − log₂(x⁵) + 6 = 0?", ["5", "12", "32", "64"], "32",
      "Let t = log₂ x. Then log₂(x⁵) = 5t, so t² − 5t + 6 = 0 and t = 2 or 3, i.e. x = 4 or 8. The product is 32. (Shortcut: the product of the roots is 2^(t₁ + t₂) = 2⁵.)")
    # ---------------- Simple & Compound Interest ----------------
    t = "Simple & Compound Interest"
    sols2 = [r for r in range(1, 1001) if (F(1000) / (2 * F(r, 100))) * (1 + F(r, 100)) ** 2 == 6050]
    assert sols2 == [10, 1000] and [r for r in sols2 if r < 100] == [10], sols2
    T(t, "Hard", "A sum of money amounts to ₹6,050 in 2 years at compound interest (compounded annually). The simple interest on the same sum for 2 years at the same rate is ₹1,000. If the rate is below 100% per annum, what is the rate, in % per annum?", 10,
      "Let the sum be P and the rate r (as a fraction). SI: 2Pr = 1000, so Pr = 500. CI amount: P(1 + r)² = P + 2Pr + Pr² = P + 1000 + 500r = 6050, so P + 500r = 5050. With P = 500/r: 500/r + 500r = 5050, i.e. r² − 10.1r + 1 = 0, so r = 0.1 or r = 10. r = 10 means 1000% a year, which the question rules out, so r = 10% and P = ₹5,000. Check: 5000 × 1.21 = 6050; SI = 5000 × 0.1 × 2 = 1000.")
    d = 20000 * (F(11, 10) ** 4 - F(12, 10) ** 2); assert d == 482
    M(t, "Medium", "₹20,000 is invested for 2 years at 20% per annum. How much more interest is earned if interest is compounded half-yearly instead of annually?", ["₹400", "₹441", "₹482", "₹520"], "₹482",
      "Annual: 20000 × 1.2² = ₹28,800. Half-yearly: 10% for 4 half-years, 20000 × 1.1⁴ = 20000 × 1.4641 = ₹29,282. Difference = ₹482.")
    # ---------------- Time & Work ----------------
    t = "Time & Work"
    done, day = 0, 0
    while done < 36: day += 1; done += day
    assert day == 8 and done == 36
    T(t, "Medium", "A worker can finish a job alone in 36 days. She starts the job alone on day 1, and from day 2 onwards one more worker of the same efficiency joins at the start of every day (so 2 work on day 2, 3 on day 3, and so on). On which day is the job completed?", 8,
      "Measure work in worker-days: the job is 36. After k days the work done is 1 + 2 + … + k = k(k + 1)/2. This first reaches 36 at k = 8 (8 × 9/2 = 36), so the job is finished at the end of day 8.")
    xs = [x for x in range(3, 100) if F(x, 18) + F(x - 3, 12) == 1]; assert xs == [9]
    M(t, "Medium", "A and B can finish a job in 12 and 18 days respectively. They start together, but A leaves 3 days before the job is finished. In how many days is the whole job finished?", ["7.2 days", "9 days", "10 days", "10.8 days"], "9 days",
      "If the job takes x days, B works x days and A works x − 3 days: x/18 + (x − 3)/12 = 1. Multiply by 36: 2x + 3x − 9 = 36, so x = 9.")
    # ---------------- Probability ----------------
    t = "Probability"
    tri = list(itertools.combinations(range(1, 11), 3)); ap = [c for c in tri if c[0] + c[2] == 2 * c[1]]
    assert len(ap) == 20 and F(len(ap), len(tri)) == F(1, 6)
    M(t, "Hard", "Three different numbers are chosen at random from 1, 2, …, 10. What is the probability that they can be arranged to form an arithmetic progression?", ["1/6", "1/8", "1/5", "1/12"], "1/6",
      "There are C(10, 3) = 120 choices. A set a < b < c is an AP when a + c = 2b, i.e. a and c have the same parity and b is their average. Pairs of the same parity: C(5, 2) + C(5, 2) = 20, each giving exactly one b. Probability = 20/120 = 1/6.")
    N = 400; inside = sum(1 for i in range(N) for j in range(N) if ((i + .5) / N * 2 - 1) ** 2 + ((j + .5) / N * 2 - 1) ** 2 < 1) / N ** 2
    assert abs(inside - math.pi / 4) < 0.002
    M(t, "Medium", "A point is chosen at random inside a square of side 2 cm. What is the probability that it is less than 1 cm from the centre of the square?", ["π/4", "π/2", "1/2", "π/8"], "π/4",
      "The favourable region is the circle of radius 1 cm centred at the square's centre; it fits inside the square (it touches the sides). Probability = π × 1²/2² = π/4.")
    # ---------------- Permutations & Combinations ----------------
    t = "Permutations & Combinations"
    cnt = sum(1 for n in range(1, 1000) if sum(map(int, str(n))) == 10); assert cnt == 63
    T(t, "Hard", "How many positive integers less than 1000 have digits that add up to 10?", cnt,
      "Write each number as a three-digit string abc with leading zeros allowed (0 itself has digit sum 0, so it is not counted). We need a + b + c = 10 with each digit 0 to 9. Without the upper limit there are C(12, 2) = 66 solutions; the ones with a digit equal to 10 (10, 0, 0 in some order) are not allowed, and there are 3 of them. 66 − 3 = 63.")
    cnt2 = sum(1 for n in range(100, 1000) if (n // 10) % 10 > n // 100 and (n // 10) % 10 > n % 10); assert cnt2 == 240
    T(t, "Medium", "How many three-digit numbers have a middle digit that is strictly greater than both the first digit and the last digit?", cnt2,
      "If the middle digit is m, the first digit can be 1 to m − 1 (m − 1 choices) and the last 0 to m − 1 (m choices). Sum over m = 2 to 9 of m(m − 1) = 2 + 6 + 12 + 20 + 30 + 42 + 56 + 72 = 240.")
