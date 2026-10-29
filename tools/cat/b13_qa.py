"""Practice pack b13, Quantitative Ability (original items, added 29 Oct 2026), weighted towards Hard items in thinner topics.
Every answer is recomputed here by brute force, exact fractions or sympy; the build stops if a check fails."""
import itertools, math
from fractions import Fraction as F

def build(B):
    s = "qa"; M = lambda *a, **k: B.mcq(s, *a, **k); T = lambda *a, **k: B.tita(s, *a, **k)
    # ---------------- Logarithms ----------------
    t = "Logarithms"
    sol = [(a, b) for a in range(-20, 21) for b in range(-20, 21) if 2*a + b == 8 and a + 2*b == 10]
    assert sol == [(2, 4)]
    T(t, "Medium", "If log₂x + log₄y = 4 and log₄x + log₂y = 5, what is the value of xy?", 64,
      "Write a = log₂x and b = log₂y. Since log₄ = ½ log₂, the equations are a + b/2 = 4 and a/2 + b = 5, i.e. 2a + b = 8 and a + 2b = 10. So a = 2 and b = 4, giving x = 4, y = 16 and xy = 64.")
    n = sum(1 for k in range(2, 1000) if 1 < math.log2(math.log(k, 3)) < 2)
    assert n == 71 and [k for k in range(9, 82) if 1 < math.log2(math.log(k, 3)) < 2] == list(range(10, 81))
    T(t, "Medium", "How many integers n satisfy 1 < log₂(log₃ n) < 2?", 71,
      "1 < log₂(log₃ n) < 2 means 2 < log₃ n < 4, i.e. 9 < n < 81. The integers are 10, 11, …, 80, which is 71 integers.")
    assert len(str(6**30)) == 24
    import sympy as sp
    x = sp.symbols('x', positive=True)
    roots = sorted(sp.solve(sp.Eq(sp.log(x, 10)**2, 2 + sp.log(x, 10)), x))
    assert roots == [sp.Rational(1, 10), 100] and roots[0]*roots[1] == 10
    T(t, "Hard", "What is the product of all real values of x for which x^(log₁₀x) = 100x?", 10,
      "Take log₁₀ of both sides and write t = log₁₀x: t·t = 2 + t, so t² − t − 2 = 0 and t = 2 or t = −1. Then x = 100 or x = 1/10 (both positive, so both valid), and the product is 100 × 1/10 = 10.")
    a = math.log(18, 12); target = math.log(16, 24)
    opts = {"4(2 − a)/(5 − a)": 4*(2-a)/(5-a), "4(2 + a)/(5 + a)": 4*(2+a)/(5+a), "(2 − a)/(5 − a)": (2-a)/(5-a), "4(a − 2)/(a + 5)": 4*(a-2)/(a+5)}
    assert [k for k, v in opts.items() if abs(v - target) < 1e-12] == ["4(2 − a)/(5 − a)"]
    M(t, "Hard", "If log₁₂18 = a, then log₂₄16 equals", list(opts), "4(2 − a)/(5 − a)",
      "Let r = log 3 / log 2. Then a = log 18 / log 12 = (1 + 2r)/(2 + r), so r = (2a − 1)/(2 − a). Next, log₂₄16 = 4 log 2/(3 log 2 + log 3) = 4/(3 + r) = 4(2 − a)/(3(2 − a) + 2a − 1) = 4(2 − a)/(5 − a).")

    # ---------------- Functions ----------------
    t = "Functions"
    f = lambda v: v / (1 + v); v = F(1)
    for _ in range(10): v = f(v)
    assert v == F(1, 11)
    M(t, "Medium", "Let f(x) = x/(1 + x) for x > 0, and let fⁿ denote f applied n times (so f²(x) = f(f(x))). What is f¹⁰(1)?", ["1/11", "1/12", "1/20", "1/2"], "1/11",
      "f(f(x)) = (x/(1 + x))/(1 + x/(1 + x)) = x/(1 + 2x), and in general fⁿ(x) = x/(1 + nx), as each step adds x to the denominator. So f¹⁰(1) = 1/(1 + 10) = 1/11.")
    p, q = sp.symbols('p q')
    sl = sp.solve([2*p + q - 9, 2*q + p - 4], [p, q]); assert sl[p] == sp.Rational(14, 3)
    inv = sum(1 for g in itertools.product(range(4), repeat=4) if all(g[g[i]] == i for i in range(4)))
    assert inv == 10
    T(t, "Hard", "How many functions f from {1, 2, 3, 4} to itself satisfy f(f(x)) = x for every x in the set?", 10,
      "Such an f pairs the elements up and fixes the rest (any element not fixed is swapped with its partner). No swaps: 1 function. Exactly one swapped pair: C(4,2) = 6. Two swapped pairs: 3. Total = 1 + 6 + 3 = 10.")
    grid = [F(k, 100) for k in range(-1000, 1001)]
    best = max(min(2*z + 1, 7 - z, z + 4) for z in grid); assert best == 5
    M(t, "Medium", "For real x, let g(x) = min(2x + 1, x + 4, 7 − x). What is the largest value g(x) can take?", ["3", "4", "4.5", "5"], "5",
      "7 − x falls as x grows while the other two rise, so the maximum of the minimum is where 7 − x meets the smaller rising line. 2x + 1 = 7 − x at x = 2, where both equal 5 and x + 4 = 6 is larger. (Where x + 4 = 7 − x, at x = 1.5, 2x + 1 is only 4.) So the largest value is 5, at x = 2.")

    # ---------------- Averages ----------------
    t = "Averages"
    best = max(e for a1 in range(1, 18) for b1 in range(a1+1, 18) for d in range(19, 101) for e in [100 - a1 - b1 - 18 - d] if e > d)
    assert best == 60
    Sx = 30*62 - 25*63; assert Sx == 285 and F(45*58 + Sx, 50) == F(579, 10)
    M(t, "Medium", "Section A has 30 students with an average score of 62, and Section B has 45 students with an average of 58. Five students move from A to B, after which A's average rises to 63. What is B's new average?", ["57.9", "58.1", "58.3", "58.5"], "57.9",
      "The five movers' total = 30 × 62 − 25 × 63 = 1860 − 1575 = 285. B's new total = 45 × 58 + 285 = 2610 + 285 = 2895 for 50 students, so its average is 2895/50 = 57.9.")

    # ---------------- Simple & Compound Interest ----------------
    t = "Simple & Compound Interest"
    xi = F(33100) / sum(F(10, 11)**k for k in (1, 2, 3)); assert xi == 13310
    d = 10000*(F(103, 100)**4 - F(106, 100)**2); assert abs(float(d) - 19.0881) < 1e-4

    # ---------------- Ratio & Proportion ----------------
    t = "Ratio & Proportion"
    wA, wB, wC = 3*4 + 6*8, 4*12, F(5*6) + F(5, 2)*6; assert (wA, wB, wC) == (60, 48, 45)
    assert F(15300) * wC / (wA + wB + wC) == 4500
    T(t, "Medium", "A, B and C start a business with capitals in the ratio 3 : 4 : 5. After 4 months A doubles his capital, and after 6 months C withdraws half of hers. B's capital is unchanged. Out of a year-end profit of ₹15,300, what is C's share (in ₹)?", 4500,
      "Take capitals 3, 4, 5 units. Capital × months: A = 3 × 4 + 6 × 8 = 60; B = 4 × 12 = 48; C = 5 × 6 + 2.5 × 6 = 45. Total = 153. C's share = 15,300 × 45/153 = ₹4,500.")

    # ---------------- Mixtures & Alligation ----------------
    t = "Mixtures & Alligation"
    milk = F(2, 3) + F(3, 5) + F(4, 7); water = 3 - milk; assert (milk / water) == F(193, 122)
    a_ = F(7, 9); b_ = F(7, 18); kA = F(35) * (F(1, 2) - b_) / (a_ - b_); assert kA == 10
    j = F(40) * F(36, 40) * F(35, 40) * F(32, 40); assert j == F(252, 10)

    # ---------------- Time & Work ----------------
    t = "Time & Work"
    done, day = F(0), 0
    while done < 1:
        day += 1; r = F(1, 12) if day % 2 else F(1, 18)
        if done + r >= 1: tot = day - 1 + (1 - done) / r; break
        done += r
    assert tot == F(43, 3)
    half = 30 * (F(1, 20) + F(1, 30) - F(1, 15)); rest = (1 - half) / (F(1, 20) + F(1, 30)); assert half == F(1, 2) and 30 + rest == 36

    # ---------------- Permutations & Combinations ----------------
    t = "Permutations & Combinations"
    w = {p_ for p_ in itertools.permutations("ALABAMA") if "AA" not in "".join(p_)}; assert len(w) == 6
    tr = [c for c in itertools.combinations(range(1, 13), 3) if sum(c) == 12]; assert len(tr) == 7
    T(t, "Hard", "In how many ways can 12 be written as a sum of three different positive integers, if the order of the terms does not matter?", 7,
      "List a < b < c with a + b + c = 12. a = 1: (2, 9), (3, 8), (4, 7), (5, 6), so 4 ways. a = 2: (3, 7), (4, 6), so 2. a = 3: (4, 5), so 1. Since 3a + 3 ≤ 12, a ≤ 3. Total = 7.")
    inc = sum(1 for n_ in range(1000, 10000) if all(a1 < b1 for a1, b1 in zip(str(n_), str(n_)[1:]))); assert inc == math.comb(9, 4) == 126

    # ---------------- Probability ----------------
    t = "Probability"
    ap = [c for c in itertools.combinations(range(1, 11), 3) if c[1] - c[0] == c[2] - c[1]]; assert (len(ap), math.comb(10, 3)) == (20, 120)
    pr = F(math.comb(4, 2)*6 + math.comb(4, 3), math.comb(10, 3)); assert pr == F(1, 3)
    pa = F(1, 6) / (1 - F(5, 6) * F(1, 2)); assert pa == F(2, 7)
    sim = sum((F(5, 6)*F(1, 2))**k * F(1, 6) for k in range(200)); assert abs(float(sim) - 2/7) < 1e-12
    M(t, "Hard", "A and B take turns, A first. On each of A's turns A rolls a fair die and wins on a six; on each of B's turns B tosses a fair coin and wins on heads. They continue until someone wins. What is the probability that A wins?", ["2/7", "1/3", "1/6", "5/12"], "2/7",
      "A round in which nobody wins has probability (5/6)(1/2) = 5/12. A wins on the first turn of a round with probability 1/6, so P(A) = (1/6)(1 + 5/12 + (5/12)² + …) = (1/6)/(7/12) = 2/7.")

    # ---------------- Progressions ----------------
    t = "Progressions"
    L = [k for k in range(100, 1000) if k % 5 == 2]; assert (len(L), sum(L)) == (180, 98910)
    gp = [(a1, r) for a1 in range(1, 100) for r in range(2, 10) if a1*(1 + r + r*r) == 26 and a1*r**3*(1 + r + r*r) == 702]; assert gp == [(2, 3)]
    T(t, "Medium", "In a geometric progression with positive terms, the sum of the first three terms is 26 and the sum of the next three terms is 702. What is the fifth term?", 162,
      "The next three terms are the first three multiplied by r³, so r³ = 702/26 = 27 and r = 3. Then a(1 + 3 + 9) = 26 gives a = 2, and the fifth term is 2 × 3⁴ = 162.")
    assert sum(k*(k+1) for k in range(1, 21)) == 3080 == 20*21*22//3
    T(t, "Hard", "What is the value of 1×2 + 2×3 + 3×4 + … + 20×21?", 3080,
      "k(k + 1) = [k(k + 1)(k + 2) − (k − 1)k(k + 1)]/3, so the sum telescopes to n(n + 1)(n + 2)/3. With n = 20: 20 × 21 × 22/3 = 3080.")
    assert sum(F(1, k*(k+2)) for k in range(1, 50, 2)) == F(25, 51)
    M(t, "Medium", "What is the value of 1/(1×3) + 1/(3×5) + 1/(5×7) + … + 1/(49×51)?", ["25/51", "26/51", "50/51", "1"], "25/51",
      "1/(k(k + 2)) = ½(1/k − 1/(k + 2)), so the sum telescopes to ½(1 − 1/51) = ½ × 50/51 = 25/51.")

    # ---------------- Mensuration ----------------
    t = "Mensuration"
    cnt = {0: 0, 1: 0, 2: 0, 3: 0}
    for i in range(4):
        for j_ in range(5):
            for k in range(6):
                cnt[(i in (0, 3)) + (j_ in (0, 4)) + (k in (0, 5))] += 1
    assert cnt == {0: 24, 1: 52, 2: 36, 3: 8}
    ws = [w_ for w_ in range(1, 20) if 60*40 - (60 - 2*w_)*(40 - 2*w_) == 736]; assert ws == [4]
    T(t, "Medium", "A rectangular lawn is 60 m by 40 m. A path of uniform width runs inside it along all four edges, and the path's area is 736 m². What is the width of the path (in m)?", 4,
      "The grass left is (60 − 2w)(40 − 2w) = 2400 − 736 = 1664. Expanding, 4w² − 200w + 2400 = 1664, i.e. w² − 50w + 184 = 0, so w = (50 ± 42)/2 = 4 or 46. The width must be under 20 m, so w = 4.")
    assert F(1, 3)*36*8 / (F(4, 3)*1) == 72

    # ---------------- Number System ----------------
    t = "Number System"
    assert pow(7, 2026, 100) == 49
    e = 0; m = math.factorial(50)
    while m % 6 == 0: m //= 6; e += 1
    assert e == 22

    # ---------------- Equations, Inequalities, Geometry, TSD ----------------
    t = "Equations & Quadratics"
    pairs = [(a1, b1) for a1 in range(-100, 101) for b1 in range(-100, 101) if a1*a1 - b1*b1 == 45]; assert len(pairs) == 12
    t = "Inequalities"
    xs = [z for z in range(-100, 101) if abs(z - 3) + abs(z + 2) <= 9]; assert xs == list(range(-4, 6))
    t = "Geometry"
    tri = [(a1, b1, c) for a1 in range(1, 20) for b1 in range(a1, 20) for c in [20 - a1 - b1] if c >= b1 and a1 + b1 > c]; assert len(tri) == 8
    T(t, "Hard", "How many non-congruent triangles with integer side lengths have a perimeter of 20?", 8,
      "Let a ≤ b ≤ c with a + b + c = 20 and a + b > c, so c < 10 and c ≥ 7. c = 9: (2,9), (3,8), (4,7), (5,6), so 4. c = 8: (4,8), (5,7), (6,6), so 3. c = 7: (6,7), so 1. Total = 8.")
    t = "Time, Speed & Distance"
    pts = set(); tt = F(0)
    for k in range(1, 100): pts.add((5 * k * 50) % 400)
    assert len(pts) == 8 and 400 / (5 + 3) == 50

    # ---------------- Replacement items (the first drafts that repeated existing templates were removed) ----------------
    t = "Number System"
    assert sum(1 for k in range(1, 501) if math.gcd(k, 500) == 1) == 200
    assert sum(math.factorial(k) for k in range(1, 101)) % 12 == 9
    T(t, "Medium", "What is the remainder when 1! + 2! + 3! + … + 100! is divided by 12?", 9,
      "From 4! = 24 onwards every factorial is a multiple of 12, so only 1! + 2! + 3! = 1 + 2 + 6 = 9 matters. The remainder is 9.")
    sc = {k*k for k in range(1, 40) if k*k <= 1000} | {k**3 for k in range(1, 11)}; assert len(sc) == 38
    T(t, "Medium", "How many integers from 1 to 1000 are perfect squares or perfect cubes (or both)?", 38,
      "Squares: 1², …, 31² (32² = 1024 is too big), so 31. Cubes: 1³, …, 10³, so 10. Both means sixth powers: 1, 64 and 729, so 3. Total = 31 + 10 − 3 = 38.")
    t = "Equations & Quadratics"
    for n_ in range(-20, 20):
        pp, qq = 2*n_ + 1, n_*(n_ + 1); assert pp*pp - 4*qq == 1
    M(t, "Medium", "The roots of x² − px + q = 0 are two consecutive integers. What is the value of p² − 4q?", ["0", "1", "4", "It depends on p"], "1",
      "If the roots are n and n + 1, then p = 2n + 1 and q = n(n + 1). So p² − 4q = 4n² + 4n + 1 − 4n² − 4n = 1. (p² − 4q is also the square of the difference of the roots, which is 1² = 1.)", fixed=True)
    sr = sorted({z for z in range(-10, 11) if z*z - 5*abs(z) + 6 == 0}); assert sr == [-3, -2, 2, 3]
    T(t, "Medium", "How many real numbers x satisfy x² − 5|x| + 6 = 0?", 4,
      "Since x² = |x|², the equation is |x|² − 5|x| + 6 = 0, so |x| = 2 or |x| = 3. That gives x = ±2 and ±3: 4 solutions.")
    t = "Inequalities"
    X = sp.symbols('X', positive=True); expr = (1 + 1/X)*(1 + 1/(10 - X))
    crit = [c for c in sp.solve(sp.diff(expr, X), X) if 0 < c < 10]; assert crit == [5] and sp.nsimplify(expr.subs(X, 5)) == sp.Rational(36, 25)
    assert min(float(expr.subs(X, sp.Rational(k, 100))) for k in range(1, 1000)) >= 1.44 - 1e-12
    M(t, "Hard", "x and y are positive real numbers with x + y = 10. What is the smallest possible value of (1 + 1/x)(1 + 1/y)?", ["1.44", "1.5", "1.6", "2"], "1.44",
      "(1 + 1/x)(1 + 1/y) = 1 + 1/x + 1/y + 1/(xy) = 1 + (x + y + 1)/(xy) = 1 + 11/(xy). This is smallest when xy is largest, and with x + y = 10 the largest product is 5 × 5 = 25. So the minimum is 1 + 11/25 = 36/25 = 1.44.", fixed=True)
    t = "Permutations & Combinations"
    oc = [c for c in itertools.combinations(range(8), 3) if all((b1 - a1) % 8 not in (1, 7) for a1, b1 in itertools.combinations(c, 2))]; assert len(oc) == 16
    T(t, "Hard", "Three vertices of a regular octagon are chosen to form a triangle. In how many ways can this be done so that no side of the triangle is a side of the octagon?", 16,
      "Count choices of 3 vertices with no two adjacent. Total C(8,3) = 56. With at least one adjacent pair: a pair of adjacent vertices can be chosen in 8 ways and the third vertex in 6 ways, but the 8 triangles made of three consecutive vertices are counted twice, so 8 × 6 − 8 = 40. Answer = 56 − 40 = 16.")
    t = "Logarithms"
    assert abs(math.log(5, 3) * math.log(27, 25) - 1.5) < 1e-12
    M(t, "Easy", "What is the value of log₃5 × log₂₅27?", ["1/2", "2/3", "1", "3/2"], "3/2",
      "log₃5 × log₂₅27 = (log 5/log 3) × (3 log 3/2 log 5) = 3/2.", fixed=True)
    t = "Averages"
    v20 = [1]*19 + [-19]; assert sum(v20) == 0 and sum(1 for z in v20 if z > 0) == 19
    T(t, "Medium", "The average of 20 numbers is 0. At most how many of them can be greater than 0?", 19,
      "Not all 20 can be positive, because then the sum would be positive. 19 can be: take nineteen 1s and one −19, whose sum is 0. So the answer is 19.")
    t = "Progressions"
    a1, d1 = sp.symbols('a1 d1')
    sl = sp.solve(sp.expand((a1 + 2*d1)*(a1 + 8*d1) - (a1 + 4*d1)**2), a1); assert sl == [0]
    T(t, "Hard", "The 3rd, 5th and 9th terms of a non-constant arithmetic progression are, in that order, three consecutive terms of a geometric progression. What is the common ratio of the geometric progression?", 2,
      "With first term a and difference d ≠ 0: (a + 4d)² = (a + 2d)(a + 8d). Expanding, a² + 8ad + 16d² = a² + 10ad + 16d², so 2ad = 0 and a = 0. The three terms are 2d, 4d and 8d, so the ratio is 2.")
    t = "Probability"
    dv = [k for k in range(1, 721) if 720 % k == 0]; assert F(sum(1 for k in dv if k % 12 == 0), len(dv)) == F(2, 5)
    M(t, "Hard", "A positive divisor of 720 is chosen at random, all divisors being equally likely. What is the probability that it is a multiple of 12?", ["1/3", "2/5", "1/4", "3/10"], "2/5",
      "720 = 2⁴ × 3² × 5 has 5 × 3 × 2 = 30 divisors. A multiple of 12 = 2² × 3 needs the power of 2 to be 2, 3 or 4 (3 ways), the power of 3 to be 1 or 2 (2 ways) and any power of 5 (2 ways): 12 divisors. Probability = 12/30 = 2/5.")
    t = "Time, Speed & Distance"
    assert F(300, 40 + 60) * 80 == 240
    T(t, "Medium", "Two cyclists start at the same time from towns 300 km apart and ride towards each other at 40 km/h and 60 km/h. A drone starts with the first cyclist and flies at 80 km/h back and forth between the two, turning instantly, until the cyclists meet. How many km does the drone fly?", 240,
      "The cyclists close the gap at 40 + 60 = 100 km/h, so they meet after 300/100 = 3 hours. The drone flies the whole 3 hours at 80 km/h, i.e. 240 km. There is no need to add up the individual trips.")
    t = "Geometry"
    rr = [(a_, r2) for a_ in range(0, 24) for r2 in [64 + a_*a_] if r2 == 225 + (23 - a_)**2]; assert rr == [(15, 289)]
    T(t, "Hard", "Two parallel chords of a circle have lengths 16 cm and 30 cm and lie on opposite sides of the centre, 23 cm apart. What is the radius of the circle (in cm)?", 17,
      "Let the 16 cm chord be a cm from the centre and the 30 cm chord (23 − a) cm away. Then r² = 8² + a² = 15² + (23 − a)². So 64 + a² = 225 + 529 − 46a + a², giving 46a = 690 and a = 15. r² = 64 + 225 = 289, so r = 17.")
    t = "Functions"
    assert min(abs(z - 1) + abs(z - 2) + abs(z - 6) for z in [F(k, 10) for k in range(-100, 101)]) == 5
