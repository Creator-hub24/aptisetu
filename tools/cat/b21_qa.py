"""Practice pack b21, Quantitative Ability (original items, added 30 Oct 2026): Sets, Ratio & Proportion, Mensuration,
Simple & Compound Interest, Logarithms, Averages, Time & Work.
Every answer is recomputed here (brute force, exact fractions or high-precision numerics); the build stops if a check fails."""
import itertools, math
from fractions import Fraction as F

def build(B):
    s = "qa"; M = lambda *a, **k: B.mcq(s, *a, **k); T = lambda *a, **k: B.tita(s, *a, **k)
    pos = iter([2, 0, 3, 1] * 20)
    def mc(t, d, text, correct, wrong, sol, chk=None):
        assert len(wrong) == 3 and correct not in wrong
        o = list(wrong); o.insert(next(pos), correct)
        M(t, d, text, o, correct, sol, chk=chk)

    # ---------------- Sets ----------------
    t = "Sets"
    vals = sorted({k for k in range(0, 51) if 32 + 28 - k <= 50 and k <= 28}); assert vals == list(range(10, 29))
    T(t, "Medium", "In a universal set of 50 elements, set A has 32 elements and set B has 28. How many different values can n(A ∩ B) take?", len(vals),
      "n(A ∪ B) = 32 + 28 − n(A ∩ B) cannot exceed 50, so n(A ∩ B) ≥ 10. It also cannot exceed the smaller set, so n(A ∩ B) ≤ 28. Every whole number from 10 to 28 is possible (shift elements between the sets), "
      "giving 28 − 10 + 1 = 19 values.")
    k = F(82 - 10, 9); assert k == 8; car = 6 * k
    T(t, "Easy", "A club has 82 members. 10 of them play neither badminton nor table tennis. Among the rest, the numbers who play only badminton, only table tennis, and both games are in the ratio 3 : 4 : 2. How many members play table tennis?", int(car),
      "82 − 10 = 72 members play at least one game. With parts 3k, 4k and 2k, 9k = 72, so k = 8. Table-tennis players = only table tennis + both = 4k + 2k = 48.")
    a = [x for x in range(0, 121) if 4 * x + 60 == 120]; assert a == [15]; nA = a[0] + (a[0] + 20)
    T(t, "Medium", "120 people were asked whether they own a laptop (L) and a tablet (T). The numbers owning only L, only T, both, and neither are, in that order, four terms of an increasing arithmetic progression with common difference 10. How many people own a laptop?", nA,
      "Let the four numbers be a, a + 10, a + 20, a + 30. They add to 120: 4a + 60 = 120, so a = 15. Laptop owners = only L + both = 15 + 35 = 50.")
    nn = [n for n in range(1, 20) if 2 ** n == 64]; assert nn == [6]; c2 = 64 - 1 - 6
    mc(t, "Easy", "The power set of a set A has 64 elements. How many subsets of A have at least two elements?", str(c2), ["58", "62", "63"],
       "2ⁿ = 64 gives n = 6. Of the 64 subsets, one is empty and 6 have a single element, so 64 − 1 − 6 = 57 have at least two elements.")

    A1 = {1, 2, 3, 4}; B1 = {3, 4, 5}; assert len(A1 & B1) == 2
    pp = {(x, y) for x in A1 for y in B1} & {(x, y) for x in B1 for y in A1}; assert len(pp) == 4
    T(t, "Medium", "Sets A and B have 4 and 3 elements respectively, and exactly 2 elements are common to both. How many elements does (A × B) ∩ (B × A) have?", len(pp),
      "An ordered pair (x, y) is in A × B and also in B × A exactly when x is in both A and B and y is in both B and A. So (A × B) ∩ (B × A) = (A ∩ B) × (A ∩ B), which has 2 × 2 = 4 elements.")
    S4 = range(4); subs = [frozenset(c) for r_ in range(5) for c in itertools.combinations(S4, r_)]
    npairs = sum(1 for X in subs for Y in subs if X <= Y); assert npairs == 81 == 3 ** 4
    T(t, "Medium", "How many ordered pairs (X, Y) are there, where X and Y are subsets of {1, 2, 3, 4} and X ⊆ Y?", npairs,
      "Decide each element separately. It can be in neither set, in Y only, or in both X and Y (it cannot be in X without being in Y). That is 3 choices for each of the 4 elements, so 3⁴ = 81 pairs. A direct count of all 16 × 16 pairs gives the same 81.")

    # ---------------- Ratio & Proportion ----------------
    t = "Ratio & Proportion"
    mw = [(m, w) for m in range(1, 1001) for w in range(1, 1001) if 3 * m + 4 * w == 1700 and 5 * m + 2 * w == 1900]; assert mw == [(300, 200)]
    mc(t, "Easy", "3 men and 4 women together earn ₹1,700 a day, and 5 men and 2 women together earn ₹1,900 a day. What is the ratio of a man's daily wage to a woman's?", "3 : 2", ["2 : 1", "4 : 3", "5 : 3"],
       "Doubling the second equation: 10m + 4w = 3,800. Subtracting 3m + 4w = 1,700 gives 7m = 2,100, so m = 300 and then 4w = 1,700 − 900, w = 200. Ratio 300 : 200 = 3 : 2.")
    for (a, b, c, d) in [(F(2), F(6), F(18), F(54)), (F(3), F(-6), F(12), F(-24)), (F(5), F(10, 3), F(20, 9), F(40, 27))]:
        assert a / b == b / c == c / d and (a**3 + b**3 + c**3) / (b**3 + c**3 + d**3) == a / d
    mc(t, "Hard", "If a/b = b/c = c/d (all non-zero, and b³ + c³ + d³ ≠ 0), then (a³ + b³ + c³)/(b³ + c³ + d³) equals", "a/d", ["a³/d³", "a²/d²", "(a + b + c)/(b + c + d)"],
       "Let each ratio be k: a = bk, b = ck, c = dk. Then a³ + b³ + c³ = k³(b³ + c³ + d³), so the expression is k³. Also a/d = (a/b)(b/c)(c/d) = k³. Hence it equals a/d. "
       "(For a = 2, b = 6, c = 18, d = 54: (8 + 216 + 5832)/(216 + 5832 + 157464) = 1/27 = 2/54 ✓, while a³/d³ = 1/19683.)")
    xv = F(15, 4); r = math.sqrt(xv + 3) / math.sqrt(xv - 3); assert abs((r + 1) / (r - 1) - 2) < 1e-12
    mc(t, "Medium", "If (√(x + 3) + √(x − 3)) / (√(x + 3) − √(x − 3)) = 2, what is x?", "15/4", ["9/2", "5", "13/4"],
       "By componendo and dividendo, √(x + 3)/√(x − 3) = (2 + 1)/(2 − 1) = 3. Squaring: x + 3 = 9(x − 3), so 8x = 30 and x = 15/4. (Check: √(27/4) = 3√3/2 and √(3/4) = √3/2, ratio 3 ✓.)")

    cr = F(2, 3) ** 2 * F(math.isqrt(81), math.isqrt(64)); assert cr == F(1, 2)
    mc(t, "Easy", "What is the ratio compounded of the duplicate ratio of 2 : 3 and the sub-duplicate ratio of 81 : 64?", "1 : 2", ["2 : 3", "3 : 4", "8 : 9"],
       "The duplicate ratio of 2 : 3 is 2² : 3² = 4 : 9. The sub-duplicate ratio of 81 : 64 is √81 : √64 = 9 : 8. Compounding means multiplying: (4 × 9) : (9 × 8) = 36 : 72 = 1 : 2.")
    tot = [S for S in range(60, 100001, 60) if F(5 * S, 12) - F(6 * S, 15) == 50]; assert tot == [3000]
    T(t, "Medium", "A sum of money was to be divided among P, Q and R in the ratio 3 : 4 : 5. By mistake it was divided in the ratio 4 : 5 : 6, and as a result R received ₹50 less than his due share. What was the sum, in ₹?", tot[0],
      "R's due share is 5/12 of the sum S; he actually got 6/15 = 2/5 of it. The shortfall is S(5/12 − 2/5) = S(25 − 24)/60 = S/60 = 50, so S = ₹3,000 (R was due 1,250 and got 1,200).")

    # ---------------- Mensuration ----------------
    t = "Mensuration"
    h = math.sqrt(10**2 - 6**2); assert h == 8 and (10 + 22) / 2 * h == 128
    T(t, "Easy", "An isosceles trapezium has parallel sides of 10 cm and 22 cm, and each of its other two sides is 10 cm. What is its area, in cm²?", 128,
      "Dropping perpendiculars from the ends of the shorter side cuts off (22 − 10)/2 = 6 cm on each side. Height = √(10² − 6²) = 8 cm. Area = ½ × (10 + 22) × 8 = 128 cm².")
    v = F(22, 7) * (49 - 36) * 21; assert v == 858
    T(t, "Easy", "A metal pipe is 21 cm long, with an outer radius of 7 cm and an inner radius of 6 cm. What is the volume of metal in it, in cm³? (Take π = 22/7.)", 858,
      "Metal volume = π(R² − r²)h = (22/7)(49 − 36)(21) = 22 × 13 × 3 = 858 cm³.")
    r_ = 1.0; l_ = 2 * r_; assert abs(math.pi * r_ * l_ - 2 * math.pi * r_ ** 2) < 1e-12 and abs(math.degrees(math.asin(r_ / l_)) - 30) < 1e-9
    mc(t, "Medium", "The curved surface area of a right circular cone is twice the area of its base. What is the semi-vertical angle of the cone (the angle between its axis and a slant edge)?", "30°", ["45°", "60°", "15°"],
       "πrl = 2πr² gives slant height l = 2r. In the right triangle formed by the axis, a base radius and a slant edge, sin(semi-vertical angle) = r/l = 1/2, so the angle is 30°.")
    dims = [(a, b, c) for a in range(1, 49) for b in range(a, 49) for c in range(b, 49) if sorted([a * b, b * c, c * a]) == [24, 32, 48]]; assert dims == [(4, 6, 8)]
    assert math.isqrt(24 * 32 * 48) ** 2 == 24 * 32 * 48 == 192 ** 2
    T(t, "Medium", "The three different faces of a cuboid have areas 24 cm², 32 cm² and 48 cm². What is its volume, in cm³?", 192,
      "If the edges are a, b, c, the face areas are ab, bc, ca, and their product is (abc)². So volume = √(24 × 32 × 48) = √36,864 = 192 cm³ (the edges are 4, 6 and 8 cm).")
    rc = F(21 * 120, 360); assert rc == 7; hc = math.sqrt(21 ** 2 - 7 ** 2); assert abs(hc - 14 * math.sqrt(2)) < 1e-12
    T(t, "Medium", "A sector of a circle with radius 21 cm and angle 120° is bent so that its two straight edges meet, forming the curved surface of a cone. What is the base radius of the cone, in cm?", int(rc),
      "The arc of the sector becomes the circumference of the base: arc = (120/360) × 2π × 21 = 14π, so 2πr = 14π and r = 7 cm. (The radius 21 cm becomes the slant height.)")
    def cubes_hit(a, b, c, N=200000):
        hit = set()
        for i in range(1, N):
            u = i / N; hit.add((math.floor(a * u), math.floor(b * u), math.floor(c * u)))
        return len(hit)
    assert cubes_hit(3, 4, 5) == 10 == 3 + 4 + 5 - 1 - 1 - 1 + 1
    T(t, "Hard", "A 3 × 4 × 5 cuboid is made of 60 unit cubes. A straight line is drawn from one corner of the cuboid to the opposite corner. Through the interiors of how many of the unit cubes does it pass?", 10,
      "Moving along the diagonal, the line enters a new cube each time it crosses a grid plane: 3 − 1 = 2 planes across the length, 3 across the width and 4 across the height, 9 crossings, giving 1 + 9 = 10 cubes "
      "— provided no two crossings happen at the same point. Two plane crossings coincide only at fractions of the way that are multiples of both 1/a and 1/b; with 3, 4 and 5 pairwise coprime that happens only at the ends. "
      "(General count a + b + c − gcd(a,b) − gcd(b,c) − gcd(c,a) + gcd(a,b,c) = 12 − 1 − 1 − 1 + 1 = 10.) A fine numerical trace of the line confirms 10 cubes.")

    rr = 3.0; vc_, vh_, vk_ = math.pi * rr**2 * rr, 2 / 3 * math.pi * rr**3, 1 / 3 * math.pi * rr**2 * rr
    assert abs(vc_ / vk_ - 3) < 1e-12 and abs(vh_ / vk_ - 2) < 1e-12
    mc(t, "Easy", "A cylinder, a hemisphere and a cone all have the same base radius r, and the cylinder and the cone each have height r. What is the ratio of their volumes (cylinder : hemisphere : cone)?", "3 : 2 : 1", ["1 : 2 : 3", "3 : 1 : 2", "2 : 3 : 1"],
       "Cylinder = πr² × r = πr³. Hemisphere = (2/3)πr³. Cone = (1/3)πr² × r = (1/3)πr³. Ratio 1 : 2/3 : 1/3 = 3 : 2 : 1.")
    a_ = 6.0; ri = a_ / (2 * math.sqrt(3)); Rc = a_ / math.sqrt(3); assert abs((ri / Rc) ** 2 - 0.25) < 1e-12
    mc(t, "Easy", "What is the ratio of the area of the incircle of an equilateral triangle to the area of its circumcircle?", "1 : 4", ["1 : 2", "1 : 3", "1 : √3"],
       "In an equilateral triangle the centre of both circles is the centroid, which divides each median in the ratio 2 : 1. The circumradius is 2/3 of the median and the inradius 1/3, so the radii are in the ratio 1 : 2 and the areas in the ratio 1² : 2² = 1 : 4.")

    # ---------------- Simple & Compound Interest ----------------
    t = "Simple & Compound Interest"
    r = F(9200 - 8000, 8000 * 3) * 100; assert r == 5; amt = 8000 + 8000 * (r + 2) * 3 / 100; assert amt == 9680
    T(t, "Easy", "At simple interest, ₹8,000 amounts to ₹9,200 in 3 years. If the rate of interest were 2 percentage points higher, what would ₹8,000 amount to in 3 years, in ₹?", int(amt),
      "Interest 1,200 in 3 years on 8,000 means a rate of 1,200/(8,000 × 3) = 5%. At 7%: interest = 8,000 × 7% × 3 = 1,680, amount ₹9,680.")
    si = 5000 * (6 * 3 + 8 * 4 + 9 * 3) // 100; assert si == 3850
    T(t, "Medium", "A bank pays simple interest at 6% per annum for the first 3 years, 8% per annum for the next 4 years and 9% per annum after that. What is the total interest, in ₹, on ₹5,000 for 10 years?", si,
      "Interest = 5,000 × (6% × 3 + 8% × 4 + 9% × 3) = 5,000 × 77% = ₹3,850.")
    rs = (F(11, 10) ** 2 - 1) / 2 * 100; assert rs == F(21, 2)
    T(t, "Medium", "What rate of simple interest per annum gives the same amount after 2 years as 10% per annum compound interest (compounded annually)?", rs,
      "At 10% compound interest a sum grows by the factor 1.1² = 1.21 in 2 years, i.e. 21% interest. Simple interest giving 21% in 2 years needs 21/2 = 10.5% per annum.")

    Pp = F(300); Ii = [I for I in [Pp * k / 3 for k in range(1, 6)] if I == F(2, 5) * (Pp + I)]; assert Ii == [200]
    rate = Ii[0] / Pp / 5 * 100; assert rate == F(40, 3)
    mc(t, "Medium", "At what rate of simple interest per annum will the interest on a sum for 5 years be two-fifths of the amount (principal plus interest) at the end of those 5 years?", "13⅓%", ["8%", "10%", "12½%"],
       "Let the interest be I and the principal P. I = (2/5)(P + I) gives 3I = 2P, so I = (2/3)P. Over 5 years the rate is (2/3)/5 = 2/15 = 13⅓% per annum. (Check: on ₹300, interest ₹200, amount ₹500, and 200 = (2/5) × 500.)")

    # ---------------- Logarithms ----------------
    t = "Logarithms"
    v1 = math.log2(8) + math.log(1 / 9, 3) + math.log(math.sqrt(5), 5); assert abs(v1 - 1.5) < 1e-12
    T(t, "Easy", "What is the value of log₂8 + log₃(1/9) + log₅√5?", F(3, 2),
      "log₂8 = 3, log₃(1/9) = −2 and log₅√5 = 1/2. Sum = 3 − 2 + 0.5 = 1.5.")
    a2, b3 = math.log10(2), math.log10(3); assert abs(math.log10(75) - (b3 + 2 - 2 * a2)) < 1e-12
    mc(t, "Medium", "If log 2 = a and log 3 = b (logs to base 10), then log 75 equals", "b + 2 − 2a", ["b + 2a", "2b + 1 − a", "b − 2 + 2a"],
       "75 = 3 × 25 = 3 × 100/4. So log 75 = log 3 + log 100 − log 4 = b + 2 − 2a.")
    xs = [x for x in (0, 1, 2, 3, -1) if abs(math.log2(4 ** x + 4) - (x + math.log2(5))) < 1e-12]; assert xs == [0, 2]
    T(t, "Medium", "What is the sum of all real x satisfying log₂(4ˣ + 4) = x + log₂5?", 2,
      "Exponentiate: 4ˣ + 4 = 5 · 2ˣ. With t = 2ˣ > 0: t² − 5t + 4 = 0, so t = 1 or 4, i.e. x = 0 or x = 2. Both satisfy the original equation (4ˣ + 4 > 0 always). Sum = 2.")
    assert abs(3 ** math.log(16, 9) - 4) < 1e-12
    mc(t, "Easy", "What is the value of 3^(log₉16)?", "4", ["2", "8", "16"],
       "log₉16 = log₃16 / log₃9 = (log₃16)/2 = log₃4. So 3^(log₉16) = 3^(log₃4) = 4.")
    for (a, b, c) in [(2, 6, 18), (3, 12, 48), (5, 15, 45)]:
        x = 7.0; u = [math.log(x, a), math.log(x, b), math.log(x, c)]
        assert abs(2 / u[1] - (1 / u[0] + 1 / u[2])) < 1e-12 and abs(2 * u[1] - (u[0] + u[2])) > 1e-6 and abs(u[1] ** 2 - u[0] * u[2]) > 1e-6
    mc(t, "Medium", "a, b and c are positive numbers, none equal to 1, in geometric progression, and x is a positive number other than 1. Then logₐx, log_b x and log_c x are in", "harmonic progression",
       ["arithmetic progression", "geometric progression", "none of these, in general"],
       "b² = ac gives 2 log b = log a + log c, so 1/logₐx = log a/log x, 1/log_b x and 1/log_c x are in AP. Numbers whose reciprocals are in AP are in harmonic progression. "
       "(For a, b, c = 2, 6, 18 and x = 7 they are not in AP or GP in general, which a numerical check confirms.)")
    grid = [4 / tt + tt / 2 for tt in [i / 10000 for i in range(1, 200000)]]; mn = min(grid); assert abs(mn - 2 * math.sqrt(2)) < 1e-6
    mc(t, "Hard", "For x > 1, what is the minimum value of logₓ16 + log₄x?", "2√2", ["2", "4", "√2"],
       "Let t = log₂x > 0. Then logₓ16 = 4/t and log₄x = t/2. By AM–GM, 4/t + t/2 ≥ 2√(4/t × t/2) = 2√2, with equality when 4/t = t/2, i.e. t = 2√2 (x = 2^(2√2) > 1). Minimum 2√2.", chk=(mn, 2 * math.sqrt(2)))

    # ---------------- Averages ----------------
    t = "Averages"
    nums = [14, 16, 18, 20, 22, 24, 26, 28]; assert sum(nums) / 8 == 21 and sum(3 * n + 4 for n in nums) / 8 == 67
    T(t, "Easy", "Eight numbers have an average of 21. Each number is multiplied by 3 and then 4 is added to it. What is the average of the new numbers?", 67,
      "Multiplying every number by 3 multiplies the average by 3, and adding 4 to each adds 4 to it: 3 × 21 + 4 = 67.")
    vc = F(11 * 25 - 28 - 9 * F(49, 2)); assert vc == F(53, 2)
    T(t, "Easy", "The average age of an 11-member cricket team is 25 years. The captain is 28. Leaving out the captain and the vice-captain, the other nine players average 24.5 years. How old is the vice-captain, in years?", vc,
      "Team total = 11 × 25 = 275. The nine others total 9 × 24.5 = 220.5. Vice-captain = 275 − 28 − 220.5 = 26.5 years.")
    newavg = F(6 * 75 - (64 - 46) - (85 - 58), 6); assert newavg == F(135, 2)
    T(t, "Medium", "A student's average over 6 papers was worked out as 75. Later it was found that a mark of 46 had been entered as 64 and a mark of 58 as 85. What is the correct average?", newavg,
      "The wrong total was too high by (64 − 46) + (85 − 58) = 18 + 27 = 45. Correct total = 450 − 45 = 405, average 405/6 = 67.5.")
    xy = [(x, y) for x in range(-50, 51) for y in range(-50, 51) if x + y == 20 and x * x + y * y == 272]; assert {abs(x - y) for x, y in xy} == {12}
    T(t, "Medium", "The average of two numbers x and y is 10, and the average of their squares is 136. What is the positive difference between x and y?", 12,
      "x + y = 20 and x² + y² = 272. Then 2xy = 400 − 272 = 128, and (x − y)² = 272 − 128 = 144, so |x − y| = 12 (the numbers are 16 and 4).")

    ab = [(a, b) for a in range(1, 100) for b in range(a, 100) if a + b == 50 and a * b == 225]; assert ab == [(5, 45)]
    hm = F(2 * 5 * 45, 50); assert hm == 9 == F(15 * 15, 25)
    T(t, "Medium", "The arithmetic mean of two positive numbers is 25 and their geometric mean is 15. What is their harmonic mean?", hm,
      "For two positive numbers, AM × HM = (a + b)/2 × 2ab/(a + b) = ab = GM². So HM = 15²/25 = 9. (The numbers are 45 and 5: AM 25, GM 15, HM 2 × 225/50 = 9.)")
    seq = [10]
    for n in range(2, 7): seq.append(n * (10 + 2 * (n - 1)) - sum(seq))
    assert all(F(sum(seq[:n]), n) == 10 + 2 * (n - 1) for n in range(1, 7)) and seq[5] == 30
    T(t, "Medium", "The first term of a sequence is 10. Each later term is chosen so that, once it is added, the average of all the terms so far is exactly 2 more than it was before. What is the 6th term?", seq[5],
      "After n terms the average is 10 + 2(n − 1), so the total of the first n terms is n(2n + 8) = 2n² + 8n. The 6th term = (total of 6) − (total of 5) = (72 + 48) − (50 + 40) = 120 − 90 = 30. (The terms are 10, 14, 18, 22, 26, 30.)")

    # ---------------- Time & Work ----------------
    t = "Time & Work"
    ts = [F(k, 100) for k in range(1, 400) if 1 - F(k, 100) / 6 == 2 * (1 - F(k, 100) / 4)]; assert ts == [3]
    T(t, "Medium", "Two candles of the same length are lit at the same moment. The first would burn out completely in 4 hours and the second in 6 hours, each burning at a steady rate. After how many hours will the second candle be exactly twice as long as the first?", int(ts[0]),
      "Take the length as 1. After t hours the first has 1 − t/4 left and the second 1 − t/6. Setting 1 − t/6 = 2(1 − t/4) gives 1 − t/6 = 2 − t/2, so t/3 = 1 and t = 3 hours. (Then the first has 1/4 left and the second 1/2.)")
    done, tm = F(0), F(0)
    while done < F(1, 4): done += F(1, 12) * F(1, 100); tm += F(1, 100)
    assert tm == 3 and done == F(1, 4); rest = (1 - done) / (F(1, 12) * F(3, 4)); assert rest == 12 and tm + rest == 15
    T(t, "Medium", "A pump can empty a full pool in 12 hours. After it has worked for 3 hours, a fault cuts its efficiency to 75% of normal for the rest of the job. How many hours in all does it take to empty the pool?", int(tm + rest),
      "In 3 hours the pump empties 3/12 = 1/4 of the pool. At 75% efficiency it empties (3/4)(1/12) = 1/16 per hour, so the remaining 3/4 takes (3/4) ÷ (1/16) = 12 hours. Total = 3 + 12 = 15 hours.")
    pages, mins = 0, 0
    while pages < 1200: pages += 30 + (20 if mins >= 10 else 0); mins += 1
    assert pages == 1200 and mins == 28
    T(t, "Easy", "Printer P prints 1,200 pages in 40 minutes and printer Q prints 1,200 pages in 60 minutes. P starts on a 1,200-page job, and Q joins it 10 minutes later. How many minutes after the start is the job finished?", mins,
      "P prints 30 pages a minute and Q 20. In the first 10 minutes P alone prints 300 pages. The remaining 900 pages at 30 + 20 = 50 pages a minute take 18 minutes. Total = 10 + 18 = 28 minutes.")
