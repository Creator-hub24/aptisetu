"""Practice pack z1, Quantitative Ability (original Hard items, added 12 Nov 2026).
Every answer is recomputed here by brute force or exact arithmetic; the generator stops if a check fails.
Calibration: CAT Hard = 3-5 reasoning steps, a trap or a non-routine idea, ~3-4 minutes for a well-prepared student."""
import itertools, math
from fractions import Fraction as F

def build(B):
    s = "qa"; M = lambda *a, **k: B.mcq(s, *a, **k); T = lambda *a, **k: B.tita(s, *a, **k)
    pos = iter([1, 3, 0, 2] * 20)
    def mc(t, d, text, correct, wrong, sol):
        assert len(wrong) == 3 and correct not in wrong
        o = list(wrong); o.insert(next(pos), correct); M(t, d, text, o, correct, sol)
    H = "Hard"

    n = sum(1 for k in range(1, 1001) if (k * k + k + 1) % 7 == 0); assert n == 286
    T("Number System", H, "For how many positive integers n ≤ 1000 is n² + n + 1 divisible by 7?", n,
      "Check residues mod 7: n ≡ 0,1,2,3,4,5,6 give n² + n + 1 ≡ 1, 3, 0, 6, 0, 3, 1. So 7 divides it exactly when n ≡ 2 or 4 (mod 7). "
      "1000 = 7 × 142 + 6, so each residue class appears 142 times in 1..994, and 995..1000 have residues 1..6, which include 2 and 4 once each. Total = 2 × 142 + 2 = 286.")

    def vp(N, p):
        c, q = 0, p
        while q <= N: c += N // q; q *= p
        return c
    z = min(vp(125, 2) // 2, vp(125, 3)); assert (vp(125, 2), vp(125, 3), z) == (119, 59, 59)
    T("Number System", H, "When 125! is written in base 12, how many zeros does it end with?", z,
      "12 = 2² × 3, so the number of trailing zeros is the largest k with 12ᵏ dividing 125!, i.e. min(⌊v₂/2⌋, v₃). "
      "v₂(125!) = 62 + 31 + 15 + 7 + 3 + 1 = 119, so ⌊119/2⌋ = 59. v₃(125!) = 41 + 13 + 4 + 1 = 59. Both limits give 59, so 125! ends in 59 zeros in base 12.")

    a, b = pow(2, 2026, 13), pow(3, 2026, 13); assert (a, b) == (10, 3); r = (a + b) % 13; assert r == 0
    mc("Number System", H, "What is the remainder when 2²⁰²⁶ + 3²⁰²⁶ is divided by 13?", "0", ["3", "10", "12"],
       "By Fermat, 2¹² ≡ 1 (mod 13); 2026 = 12 × 168 + 10, so 2²⁰²⁶ ≡ 2¹⁰ = 1024 = 13 × 78 + 10 ≡ 10. "
       "3³ = 27 ≡ 1 (mod 13); 2026 = 3 × 675 + 1, so 3²⁰²⁶ ≡ 3. The sum ≡ 10 + 3 = 13 ≡ 0, so the remainder is 0.")

    sols = [(x, y) for x in range(-2026, 2027) for y in range(0, 2027) if x * x - y * y == 2026]; assert sols == []
    mc("Equations & Quadratics", H, "How many ordered pairs of integers (x, y) satisfy x² − y² = 2026?", "0", ["2", "4", "8"],
       "x² − y² = (x − y)(x + y). The two factors x − y and x + y differ by 2y, so they are both even or both odd. "
       "Both odd gives an odd product; both even gives a multiple of 4. But 2026 = 2 × 1013 is even and not a multiple of 4, so no integer pair works: 0.")

    ks = sorted({-(d + 24 // d) for d in range(-24, 25) if d and 24 % d == 0}); assert len(ks) == 8 and sum(ks) == 0
    T("Equations & Quadratics", H, "For how many integer values of k does the equation x² + kx + 24 = 0 have both roots integers?", len(ks),
      "If the roots are integers p and q, then pq = 24 and k = −(p + q). The factor pairs of 24 are (1, 24), (2, 12), (3, 8), (4, 6) and the same pairs with both signs negative, "
      "giving p + q = ±25, ±14, ±11, ±10. These are 8 different values of k.")

    f = lambda x: 4 - 3 * x
    assert all(f(x) + 2 * f(2 - x) == 3 * x for x in range(-10, 11)) and f(5) == -11
    mc("Functions", H, "A function f satisfies f(x) + 2f(2 − x) = 3x for every real x. What is f(5)?", "−11", ["11", "−7", "13"],
       "Replace x by 2 − x: f(2 − x) + 2f(x) = 3(2 − x) = 6 − 3x. Call f(x) = a and f(2 − x) = b: a + 2b = 3x and 2a + b = 6 − 3x. "
       "Doubling the second and subtracting the first: 3a = 12 − 9x, so f(x) = 4 − 3x and f(5) = −11. (Check: f(5) + 2f(−3) = −11 + 26 = 15 = 3 × 5 ✓.)")

    n = sum(1 for x in range(-20, 21) if (x - 2) * (x - 5) * (x - 9) < 0); assert n == 25
    T("Inequalities", H, "How many integers x with |x| ≤ 20 satisfy (x − 2)(x − 5)(x − 9) < 0?", n,
      "The cubic changes sign at 2, 5 and 9; it is negative for x < 2 and for 5 < x < 9. Integers from −20 to 1: 22 of them. Integers 6, 7, 8: 3 more. Total 25 (x = 2, 5, 9 give 0, which is not < 0).")

    v = F(1 + 2 + 6, 6); assert v == F(3, 2)
    mc("Logarithms", H, "If log_a b = 2 and log_b c = 3 (a, b, c > 1), what is log_c (abc)?", "3/2", ["2/3", "6", "9/2"],
       "Write everything as powers of a: b = a², c = b³ = a⁶. Then abc = a¹⁺²⁺⁶ = a⁹ and c = a⁶, so log_c(abc) = 9/6 = 3/2.")

    sm = sum(k for k in range(100, 1000) if k % 7 == 3); assert sm == 70821
    T("Progressions", H, "What is the sum of all three-digit numbers that leave remainder 3 when divided by 7?", sm,
      "The numbers are 101, 108, …, 997 (101 = 7 × 14 + 3 and 997 = 7 × 142 + 3). That is an AP with 142 − 14 + 1 = 129 terms, so the sum is 129 × (101 + 997)/2 = 129 × 549 = 70,821.")

    c5 = sum(1 for d in itertools.product(range(10), repeat=5) if d[0] > 0 and sum(d) == 10); assert c5 == 714
    T("Permutations & Combinations", H, "How many five-digit numbers have digits that add up to 10?", c5,
      "Let the digits be d₁…d₅ with d₁ ≥ 1. Put e = d₁ − 1, so e + d₂ + … + d₅ = 9 with every term ≥ 0: C(13, 4) = 715 solutions. "
      "A digit cannot exceed 9; the only way to break that here is e = 9 (d₁ = 10) with the rest 0, which is 1 solution. So 715 − 1 = 714.")

    c4 = sum(1 for c in itertools.product(range(1, 5), repeat=4) if sum(c) == 10); assert c4 == 44
    T("Permutations & Combinations", H, "In how many ways can 10 identical chocolates be given to 4 children so that every child gets at least 1 and no child gets more than 4?", c4,
      "Give each child 1 first; now share 6 more with each child getting 0 to 3 extra. Without the upper limit: C(9, 3) = 84. "
      "Subtract cases where some child gets 4 or more extra: fix that child at ≥ 4, leaving 2 to share among 4: C(5, 3) = 10, times 4 children = 40. Two children cannot both get 4 (that needs 8 > 6). So 84 − 40 = 44.")

    p = F(sum(1 for a in range(1, 7) for b in range(1, 7) if math.isqrt(a * b) ** 2 == a * b), 36); assert p == F(2, 9)
    mc("Probability", H, "Two fair dice are thrown. What is the probability that the product of the two numbers is a perfect square?", "2/9", ["1/6", "7/36", "1/4"],
       "Perfect-square products from 1–36 with both factors from 1 to 6: equal numbers (1,1) … (6,6) give 6 outcomes, and 1 × 4 = 4 gives (1,4) and (4,1). "
       "No other pair works (e.g. 2 × 8 is impossible, 9 = 3 × 3 already counted). 8 favourable outcomes out of 36 = 2/9.")

    R = F(13 * 14 * 15, 4 * 84); assert R == F(65, 8)
    T("Geometry", H, "A triangle has sides 13 cm, 14 cm and 15 cm. What is the radius (in cm) of its circumcircle? (Enter as a decimal.)", R,
      "s = 21, so by Heron's formula the area is √(21 × 8 × 7 × 6) = √7056 = 84. Circumradius R = abc/(4 × area) = 2730/336 = 65/8 = 8.125.")

    lp = sum(1 for x in range(-5, 6) for y in range(-5, 6) if x * x + y * y < 25); assert lp == 69
    T("Geometry", H, "How many points with integer coordinates lie strictly inside the circle x² + y² = 25?", lp,
      "Count by x: need y² < 25 − x². x = 0: y from −4 to 4 (9). x = ±1: 24 → |y| ≤ 4 (9 each). x = ±2: 21 → |y| ≤ 4 (9 each). x = ±3: 16 → |y| ≤ 3 (7 each). x = ±4: 9 → |y| ≤ 2 (5 each). "
      "Total = 9 + 2(9 + 9 + 7 + 5) = 9 + 60 = 69.")

    D, Tm, t1 = 300, 2, F(4, 3); u, v = 90, 60
    assert (u + v) * Tm == D and F(Tm * v, u) == t1; t2 = F(Tm * u, v); assert t2 == 3
    T("Time, Speed & Distance", H, "Two trains start at the same moment from towns A and B, 300 km apart, towards each other, and meet after 2 hours. The faster train reaches the other town 1 hour 20 minutes after the meeting. How many minutes after the meeting does the slower train reach its destination?", int(t2 * 60),
      "Before meeting, together they cover 300 km in 2 h, so u + v = 150. After meeting the faster train covers the slower train's 2-hour stretch, 2v, in 4/3 h: 2v/u = 4/3, so u = 1.5v. Then 2.5v = 150 gives v = 60, u = 90. "
      "The slower train must cover the faster train's stretch 2u = 180 km at 60 km/h: 3 hours = 180 minutes. (Shortcut: T² = t₁t₂, so t₂ = 4/(4/3) = 3 h.)")

    a, b, c = F(1, 24), F(7, 120), F(1, 40); assert a + b == F(1, 10) and b + c == F(1, 12) and c + a == F(1, 15)
    days = 4 + (1 - 4 * (a + b + c)) / (b + c); assert days == 10
    T("Time & Work", H, "A and B together can finish a job in 10 days, B and C in 12 days, and C and A in 15 days. All three start together, but A leaves after 4 days and B and C finish the job. How many days does the job take in all?", days,
      "Adding the three rates: 2(A + B + C) = 1/10 + 1/12 + 1/15 = (6 + 5 + 4)/60 = 1/4, so A + B + C = 1/8 per day. In 4 days they do 4/8 = 1/2 of the job. "
      "B + C do 1/12 per day, so the other half takes 6 days. Total 4 + 6 = 10 days.")

    x = [k for k in range(1, 80) if F(80) * (1 - F(k, 80)) ** 3 == F(135, 4)]; assert x == [20]
    T("Mixtures & Alligation", H, "A container holds 80 litres of pure milk. Some litres are taken out and replaced with water; this is done three times in all, the same quantity each time. The container finally has 33.75 litres of milk. How many litres were taken out each time?", 20,
      "After three replacements, milk = 80(1 − x/80)³ = 33.75, so (1 − x/80)³ = 33.75/80 = 0.421875 = (3/4)³. Hence 1 − x/80 = 3/4 and x = 20.")

    rr = F(7986, 7260) - 1; P = F(7260) / (1 + rr) ** 2; assert rr == F(1, 10) and P == 6000
    T("Simple & Compound Interest", "Medium", "A sum lent at compound interest (compounded yearly) amounts to ₹7,260 after 2 years and ₹7,986 after 3 years. What is the sum (in ₹)?", P,
      "The third year's interest is 7986 − 7260 = 726 on 7260, so the rate is 10%. Then P × 1.1² = 7260 gives P = 7260/1.21 = 6000.")

    lo = max(0, 70 + 75 + 80 - 2 * 100); assert lo == 25
    T("Sets", "Medium", "In a survey of 100 people, 70 like tea, 75 like coffee and 80 like juice. What is the smallest possible number of people who like all three?", lo,
      "Count dislikes: 30 do not like tea, 25 not coffee, 20 not juice. Someone who misses all three must dislike at least one, so at most 30 + 25 + 20 = 75 people miss at least one drink. "
      "So at least 100 − 75 = 25 like all three, and 25 is reached when the three groups of dislikers do not overlap.")

    od = sum(1 for d in range(1, math.factorial(10) + 1, 2) if math.factorial(10) % d == 0); assert od == 30
    T("Number System", "Medium", "How many odd divisors does 10! have?", od,
      "10! = 2⁸ × 3⁴ × 5² × 7. An odd divisor uses no factor 2, so it is 3ᵃ5ᵇ7ᶜ with a ≤ 4, b ≤ 2, c ≤ 1: 5 × 3 × 2 = 30.")

    r = sum(math.factorial(k) for k in range(1, 101)) % 24; assert r == 9
    T("Number System", "Medium", "What is the remainder when 1! + 2! + 3! + … + 100! is divided by 24?", r,
      "From 4! = 24 onwards every factorial is a multiple of 24, so only 1! + 2! + 3! = 9 matters. The remainder is 9.")

    a_b = [(x, y) for x in range(1, 16) for y in range(x, 16) if x * x + y * y == 225 and (x + y - 15) == 6]; assert a_b == [(9, 12)]
    T("Geometry", H, "A right-angled triangle has hypotenuse 15 cm and inradius 3 cm. What is its area in cm²?", 54,
      "For a right triangle, r = (a + b − c)/2, so a + b = 15 + 6 = 21. Also a² + b² = 225. Then 2ab = 21² − 225 = 216, so ab = 108 and the area is ab/2 = 54. (The legs are 9 and 12.)")

    pts = sum(1 for x in range(-5, 6) for y in range(-5, 6) if abs(x) + abs(y) <= 5); assert pts == 61
    T("Geometry", H, "How many points (x, y) with integer coordinates satisfy |x| + |y| ≤ 5?", pts,
      "For each x from −5 to 5, |y| ≤ 5 − |x| gives 2(5 − |x|) + 1 values of y: x = 0 gives 11, x = ±1 give 9, ±2 give 7, ±3 give 5, ±4 give 3, ±5 give 1. Total = 11 + 2(9 + 7 + 5 + 3 + 1) = 61.")

    tri = list(itertools.combinations(range(6), 3))
    def eq(t):
        import cmath
        z = [cmath.exp(2j * math.pi * k / 6) for k in t]; d = sorted(abs(z[i] - z[j]) for i, j in ((0, 1), (1, 2), (0, 2)))
        return abs(d[0] - d[2]) < 1e-9
    pe = F(sum(map(eq, tri)), len(tri)); assert pe == F(1, 10)
    mc("Probability", H, "Three of the six vertices of a regular hexagon are chosen at random. What is the probability that they form an equilateral triangle?", "1/10", ["1/20", "1/5", "1/3"],
       "There are C(6, 3) = 20 ways to choose three vertices. An equilateral triangle needs every other vertex: {1, 3, 5} or {2, 4, 6} — only 2 choices. Probability = 2/20 = 1/10.")
