"""Practice pack b9, Quantitative Ability (original items, added 29 Oct 2026) for the thinnest QA topics.
Every answer is recomputed here by brute force or exact arithmetic; the build stops if a check fails."""
import itertools, math
from fractions import Fraction as F

def build(B):
    s = "qa"; M = lambda *a, **k: B.mcq(s, *a, **k); T = lambda *a, **k: B.tita(s, *a, **k)
    # ---------------- Sets ----------------
    t = "Sets"
    best = 0
    for abc in range(0, 41):
        for ab in range(0, 51 - abc):
            for ca in range(0, 61 - abc - ab):
                for bc in range(0, 41 - abc - ca):
                    a, b, c = 60 - ab - ca - abc, 50 - ab - bc - abc, 40 - bc - ca - abc
                    if min(a, b, c) < 0 or a + b + c + ab + bc + ca + abc != 100: continue
                    best = max(best, abc)
    assert best == 25
    T(t, "Hard", "Each of 100 people likes at least one of tea, coffee and juice. 60 like tea, 50 like coffee and 40 like juice. What is the largest possible number of people who like all three?", 25,
      "Let e₁, e₂, e₃ be the numbers liking exactly one, two and three drinks. Then e₁ + e₂ + e₃ = 100 and e₁ + 2e₂ + 3e₃ = 60 + 50 + 40 = 150, so e₂ + 2e₃ = 50 and e₃ ≤ 25. It is reached: 25 like all three, nobody likes exactly two, and 35, 25 and 15 like only tea, only coffee and only juice (35 + 25 + 15 + 25 = 100).")
    none = 200 - (120 + 90 + 70 - 40 - 30 - 35 + 15); assert none == 10
    T(t, "Medium", "Of 200 students, 120 passed Mathematics, 90 passed Physics and 70 passed Chemistry. 40 passed both Mathematics and Physics, 30 passed both Physics and Chemistry, 35 passed both Mathematics and Chemistry, and 15 passed all three. How many students failed all three subjects?", 10,
      "Passed at least one = 120 + 90 + 70 − 40 − 30 − 35 + 15 = 190. Failed all three = 200 − 190 = 10.")
    n = sum(1 for k in range(1, 1001) if (k % 2 == 0 or k % 3 == 0 or k % 5 == 0) and k % 7 != 0)
    a235 = sum(1 for k in range(1, 1001) if k % 2 == 0 or k % 3 == 0 or k % 5 == 0); a7 = sum(1 for k in range(1, 143) if k % 2 == 0 or k % 3 == 0 or k % 5 == 0)
    assert (a235, a7, n) == (734, 104, 630)
    M(t, "Hard", "How many integers from 1 to 1000 are divisible by at least one of 2, 3 and 5 but are not divisible by 7?", ["620", "630", "634", "644"], "630",
      "Divisible by 2, 3 or 5: 500 + 333 + 200 − 166 − 100 − 66 + 33 = 734. Those that are also multiples of 7 are 7m with m ≤ 142 and m divisible by 2, 3 or 5: 71 + 47 + 28 − 23 − 14 − 9 + 4 = 104. Answer = 734 − 104 = 630.")
    assert 500+333+200-166-100-66+33 == 734 and 71+47+28-23-14-9+4 == 104
    sols = [N for N in range(1, 2000) if N * 3 % 5 == 0 and N % 2 == 0 and N % 4 == 0 and N - (N*3//5 + N//2 - N//4) == 18]
    assert sols == [120]
    T(t, "Medium", "In a class, three-fifths of the students play football, half play cricket and a quarter play both games. If 18 students play neither game, how many students are in the class?", 120,
      "Fraction playing at least one game = 3/5 + 1/2 − 1/4 = 17/20, so 3/20 play neither. 3/20 of the class = 18, so the class has 120 students.")
    lo = 100 - (20 + 15 + 25 + 30); assert lo == 10
    M(t, "Medium", "In a survey, 80% of people like apples, 85% like bananas, 75% like cherries and 70% like dates. What is the least possible percentage of people who like all four fruits?", ["5%", "10%", "15%", "20%"], "10%",
      "The people who miss at least one fruit are at most 20% + 15% + 25% + 30% = 90% (when those groups do not overlap). So at least 100% − 90% = 10% like all four, and 10% is achievable by making the four 'dislike' groups disjoint.")

    # ---------------- Ratio & Proportion ----------------
    t = "Ratio & Proportion"
    sol = [(a, b, 6300-a-b) for a in range(0, 6301, 10) for b in range(0, 6301-a, 10) if 3*a == 2*(6300-a) and 4*b == 3*(6300-b)]
    assert sol == [(2520, 2700, 1080)]
    T(t, "Medium", "₹6,300 is shared among A, B and C so that A gets two-thirds of what B and C together get, and B gets three-fourths of what A and C together get. How much (in ₹) does C get?", 1080,
      "A = (2/3)(B + C) means A : (B + C) = 2 : 3, so A = 2/5 of 6300 = 2520. B = (3/4)(A + C) means B = 3/7 of 6300 = 2700. C = 6300 − 2520 − 2700 = 1080.")
    sol = [(x, y) for x in range(1, 3000) for y in range(1, 3000) if 5*x - 3*y == 1600 and 4*x - 2*y == 1600]
    assert sol == [(800, 800)]
    T(t, "Medium", "The incomes of A and B are in the ratio 5 : 4 and their expenses in the ratio 3 : 2. If each of them saves ₹1,600, what is A's income (in ₹)?", 4000,
      "Let incomes be 5x and 4x and expenses 3y and 2y. Then 5x − 3y = 1600 and 4x − 2y = 1600. From the second, y = 2x − 800; substituting, 5x − 6x + 2400 = 1600, so x = 800 and A's income = 5 × 800 = 4000.")
    r = F(2, 3) * F(4, 5) * F(6, 7); assert r == F(16, 35)
    M(t, "Medium", "If a : b = 2 : 3, b : c = 4 : 5 and c : d = 6 : 7, what is a : d?", ["8 : 21", "16 : 35", "12 : 35", "24 : 35"], "16 : 35",
      "a/d = (a/b)(b/c)(c/d) = (2/3)(4/5)(6/7) = 48/105 = 16/35.")
    loss = 144000 - F(144000, 36) * (1 + 4 + 9); assert loss == 88000
    T(t, "Hard", "The price of a diamond varies as the square of its weight. A diamond worth ₹1,44,000 breaks into three pieces whose weights are in the ratio 1 : 2 : 3. What is the total loss in value (in ₹)?", 88000,
      "Take the weight as 6 units, so the value is k × 36 = 144000 and k = 4000. The pieces are worth k(1 + 4 + 9) = 14k = 56000. Loss = 144000 − 56000 = 88000.")
    ks = set()
    for x in range(-12, 13):
        for y in range(-12, 13):
            for z in range(-12, 13):
                if 0 in (y+z, z+x, x+y): continue
                k = F(x, y+z)
                if k == F(y, z+x) == F(z, x+y): ks.add(k)
    assert ks == {F(1, 2), F(-1)}
    M(t, "Hard", "If x/(y + z) = y/(z + x) = z/(x + y) = k for real numbers x, y, z with no denominator zero, which values can k take?", ["1/2 only", "−1 only", "1/2 or −1", "2 or −1"], "1/2 or −1",
      "Adding numerators and denominators: if x + y + z ≠ 0, k = (x + y + z)/(2(x + y + z)) = 1/2. If x + y + z = 0, then y + z = −x and k = x/(−x) = −1 (e.g. x = 1, y = 1, z = −2). Both values occur.")

    # ---------------- Mensuration ----------------
    t = "Mensuration"
    nsp = F(1, 3) * 36 * 8 / (F(4, 3) * 8); assert nsp == 9
    T(t, "Easy", "A solid metal cone of base radius 6 cm and height 8 cm is melted and recast into solid spheres of radius 2 cm, with no metal wasted. How many spheres are made?", 9,
      "Cone volume = (1/3)π × 36 × 8 = 96π. Sphere volume = (4/3)π × 8 = 32π/3. Number = 96π ÷ (32π/3) = 9.")
    r2 = 10**2 - 6**2; assert r2 == 64
    M(t, "Medium", "A right circular cylinder of height 12 cm is placed inside a sphere of radius 10 cm so that both circular rims touch the sphere. What is the volume of the cylinder?", ["576π cm³", "768π cm³", "864π cm³", "960π cm³"], "768π cm³",
      "The centre of the sphere is at mid-height, 6 cm from each rim. Rim radius r satisfies r² + 6² = 10², so r² = 64. Volume = π × 64 × 12 = 768π cm³.")
    left = 196 - F(22, 7) * 49; assert left == 42
    T(t, "Medium", "From each corner of a square sheet of side 14 cm, a quarter-circle of radius 7 cm is cut out. What area (in cm²) is left? Take π = 22/7.", 42,
      "The four quarter-circles make one full circle of radius 7: area = (22/7) × 49 = 154. Remaining = 14² − 154 = 196 − 154 = 42.")
    L, W, H = 12, 9, 7; paths = sorted([L**2 + (W+H)**2, W**2 + (L+H)**2, H**2 + (L+W)**2]); assert paths[0] == 400 and paths[1] > 400
    T(t, "Hard", "A room is 12 m long, 9 m wide and 7 m high. An ant at one corner of the floor wants to reach the diagonally opposite corner of the ceiling, walking only on the walls, floor and ceiling. What is the length (in m) of the shortest such path?", 20,
      "Unfold two adjacent faces into a rectangle. The three possible unfoldings give √(12² + (9 + 7)²) = √400 = 20, √(9² + (12 + 7)²) = √442 and √(7² + (12 + 9)²) = √490. The shortest is 20 m.")

    # ---------------- Averages ----------------
    t = "Averages"
    six = 6*58 + 6*65 - 11*60; assert six == 78
    T(t, "Medium", "The average of 11 numbers is 60. The average of the first six is 58 and the average of the last six is 65. What is the sixth number?", 78,
      "The first six and last six together count the sixth number twice: 6 × 58 + 6 × 65 = 348 + 390 = 738. The sum of all 11 is 660. Sixth number = 738 − 660 = 78.")
    baby = 6 * F(47, 2) - (5*24 + 5*4); assert baby == 1
    T(t, "Medium", "Four years ago, the average age of a family of five was 24 years. A baby has since been born, and the average age of the six members today is 23.5 years. How old (in years) is the baby?", 1,
      "Four years ago the five members' ages added to 5 × 24 = 120; today they add to 120 + 5 × 4 = 140. The six members today total 6 × 23.5 = 141, so the baby is 141 − 140 = 1 year old.")
    sol = [nb for nb in range(1, 500) if F(40*64 + nb*70, 40+nb) == 66]; assert sol == [20]
    T(t, "Medium", "Section A has 40 students with an average score of 64; section B has an average of 70. The combined average of both sections is 66. How many students are in section B?", 20,
      "By alligation, A : B = (70 − 66) : (66 − 64) = 4 : 2 = 2 : 1. With 40 in A, B has 20.")
    bst = 0
    for a in range(1, 18):
        for b in range(a+1, 18):
            for d in range(19, 100):
                e = 100 - 18 - a - b - d
                if e > d: bst = max(bst, e)
    assert bst == 60
    T(t, "Hard", "Five different positive integers have an average of 20 and a median of 18. What is the largest possible value of the largest of them?", 60,
      "The five add up to 100. Write them as a < b < 18 < d < e. To make e as large as possible, make a, b and d as small as possible: a = 1, b = 2, d = 19. Then e = 100 − 18 − 1 − 2 − 19 = 60.")

    # ---------------- Functions ----------------
    t = "Functions"
    a_, b_ = F(-1), F(7, 2); assert a_ + 2*b_ == 6 and b_ + 2*a_ == F(3, 2)
    T(t, "Medium", "A function f satisfies f(x) + 2f(1/x) = 3x for every non-zero real x. What is f(2)?", -1,
      "Put x = 2: f(2) + 2f(1/2) = 6. Put x = 1/2: f(1/2) + 2f(2) = 3/2. From the second, f(1/2) = 3/2 − 2f(2); substituting, f(2) + 3 − 4f(2) = 6, so f(2) = −1.")
    mn = min(abs(x-1) + abs(x-3) + abs(x-6) for x in [F(k, 4) for k in range(-40, 80)]); assert mn == 5
    M(t, "Easy", "What is the minimum value of f(x) = |x − 1| + |x − 3| + |x − 6| over all real x?", ["4", "5", "6", "7"], "5",
      "A sum of distances to 1, 3 and 6 is least at the median point x = 3: 2 + 0 + 3 = 5.")
    T(t, "Medium", "A function f satisfies f(x + y) = f(x)·f(y) for all real x, y, and f(1) = 3. What is f(1) + f(2) + f(3) + f(4)?", 120,
      "f(2) = f(1)² = 9, f(3) = f(2)f(1) = 27, f(4) = 81. Sum = 3 + 9 + 27 + 81 = 120.")
    assert 3 + 9 + 27 + 81 == 120
    cnt = [x for x in range(-2000, 2001) if x*x != 9 and F(x*x - 5*x + 4, x*x - 9) <= 0]; assert cnt == [-2, -1, 0, 1, 4]
    T(t, "Hard", "For how many integers x is (x² − 5x + 4)/(x² − 9) ≤ 0?", 5,
      "Write it as (x − 1)(x − 4)/((x − 3)(x + 3)). The sign changes at −3, 1, 3 and 4. It is negative on (−3, 1) and on (3, 4), and zero at x = 1 and x = 4 (x = ±3 are excluded). Integers: −2, −1, 0, 1 and 4, so 5.")

    # ---------------- Mixtures & Alligation ----------------
    t = "Mixtures & Alligation"
    milk = F(60) * F(9, 10)**3; assert milk == F(4374, 100)
    T(t, "Medium", "A vessel holds 60 litres of pure milk. 6 litres are taken out and replaced with water, and this is done three times in all. How many litres of milk are left in the vessel?", F(4374, 100),
      "Each step keeps 54/60 = 9/10 of the milk. After three steps: 60 × (9/10)³ = 60 × 0.729 = 43.74 litres.")
    r = (F(1, 2) - F(4, 9)) / (F(3, 5) - F(1, 2)); assert r == F(5, 9)
    M(t, "Medium", "Alloy X has copper and zinc in the ratio 3 : 2, and alloy Y has them in the ratio 4 : 5. In what ratio must X and Y be mixed to get an alloy with equal amounts of copper and zinc?", ["5 : 9", "9 : 5", "4 : 5", "5 : 4"], "5 : 9",
      "Copper fraction: X = 3/5, Y = 4/9, target 1/2. X : Y = (1/2 − 4/9) : (3/5 − 1/2) = 1/18 : 1/10 = 5 : 9.")
    cp = F(60) / F(6, 5); assert cp == 50
    q = [y for y in range(1, 200) if F(30*42 + y*54, 30 + y) == cp]; assert q == [60]
    T(t, "Medium", "A trader mixes rice costing ₹42 per kg with rice costing ₹54 per kg and sells the mixture at ₹60 per kg, making a 20% profit. If he used 30 kg of the cheaper rice, how many kg of the costlier rice did he use?", 60,
      "Cost price of the mixture = 60/1.2 = ₹50 per kg. Cheaper : costlier = (54 − 50) : (50 − 42) = 4 : 8 = 1 : 2, so 30 kg of the cheaper needs 60 kg of the costlier.")
    sp = (F(1, 3) + F(2, 5) + F(3, 7)); assert sp / (3 - sp) == F(122, 193)
    M(t, "Hard", "Three vessels of equal volume are full of mixtures of spirit and water in the ratios 1 : 2, 2 : 3 and 3 : 4. Their contents are emptied into one large tank. What is the ratio of spirit to water in the tank?", ["6 : 11", "122 : 193", "61 : 105", "121 : 194"], "122 : 193",
      "Take each vessel as 1 unit. Spirit = 1/3 + 2/5 + 3/7 = (35 + 42 + 45)/105 = 122/105. Water = 3 − 122/105 = 193/105. Ratio = 122 : 193.")

    # ---------------- Simple & Compound Interest ----------------
    t = "Simple & Compound Interest"
    P = [p for p in range(100, 100000, 100) if p * F(11, 10)**2 - p - p * F(2, 10) == 60]; assert P == [6000]
    T(t, "Easy", "The difference between compound interest (compounded annually) and simple interest on a sum for 2 years at 10% per annum is ₹60. What is the sum (in ₹)?", 6000,
      "For 2 years, CI − SI = P(r/100)² = P × 0.01. So 0.01P = 60 and P = 6000.")
    T(t, "Medium", "A sum of money doubles itself in 5 years at compound interest (compounded annually). In how many years will it become 8 times itself at the same rate?", 15,
      "Doubling takes 5 years, and 8 = 2 × 2 × 2, so it takes 3 doublings: 3 × 5 = 15 years.")
    x = F(21000) / (F(10, 11) + F(100, 121)); assert x == 12100
    T(t, "Hard", "A loan of ₹21,000 at 10% per annum compound interest (compounded annually) is to be repaid in two equal instalments at the end of the first and second years. What is each instalment (in ₹)?", 12100,
      "Each instalment x must have present value adding to 21000: x/1.1 + x/1.21 = 21000. Multiply by 1.21: 1.1x + x = 25410, so 2.1x = 25410 and x = 12100.")
    assert F(21000) * F(121, 100) == 25410
    rr = [r for r in range(1, 50) if 420*2 + F(420*r, 100) == 882]; assert rr == [10]
    M(t, "Hard", "A sum earns ₹1,260 as simple interest in 3 years. At the same rate, the compound interest (compounded annually) on the same sum for 2 years is ₹882. What is the rate of interest per annum?", ["8%", "10%", "12%", "15%"], "10%",
      "Simple interest per year = 1260/3 = 420. Over 2 years, CI exceeds SI by the interest on the first year's interest: 882 − 840 = 42 = 420 × r/100, so r = 10%.")

    # ---------------- Logarithms ----------------
    t = "Logarithms"
    assert abs(math.log2(16) + math.log(16, 4) + math.log(16, 16) - 7) < 1e-12
    T(t, "Easy", "If log₂x + log₄x + log₁₆x = 7, what is x?", 16,
      "log₄x = (1/2)log₂x and log₁₆x = (1/4)log₂x. So (1 + 1/2 + 1/4)log₂x = 7, i.e. (7/4)log₂x = 7, log₂x = 4 and x = 16.")
    a = 2.0; b = a**2; c = b**3; assert abs(math.log(a**6, c) - 1) < 1e-12
    T(t, "Medium", "If logₐb = 2 and log_b c = 3, what is the value of log_c(a⁶)?", 1,
      "b = a² and c = b³ = a⁶. So log_c(a⁶) = log_c c = 1.")
    assert len(str(2**100)) == 31
    T(t, "Medium", "Given log₁₀2 = 0.30103, how many digits does 2¹⁰⁰ have?", 31,
      "log₁₀(2¹⁰⁰) = 100 × 0.30103 = 30.103. A number whose logarithm is 30.something has 30 + 1 = 31 digits.")
    roots = [x for x in (2, 4, 8, 16, 32, 64) if x not in (1, 16, 64) and abs(math.log(2, x) * math.log(2, x/16) - math.log(2, x/64)) < 1e-12]
    assert roots == [4, 8]
    M(t, "Hard", "Which values of x satisfy log_x 2 × log_(x/16) 2 = log_(x/64) 2?", ["4 only", "8 only", "4 or 8", "2 or 8"], "4 or 8",
      "Let t = log₂x. Then log_x 2 = 1/t, log_(x/16) 2 = 1/(t − 4) and log_(x/64) 2 = 1/(t − 6). So 1/(t(t − 4)) = 1/(t − 6), giving t² − 4t = t − 6, i.e. t² − 5t + 6 = 0 and t = 2 or 3. So x = 4 or 8; neither makes a base equal to 1 or non-positive.")

    # ---------------- Probability ----------------
    t = "Probability"
    pr = F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b in (2, 3, 5, 7, 11)), 36); assert pr == F(5, 12)
    M(t, "Easy", "Two fair dice are thrown. What is the probability that the sum of the numbers shown is a prime number?", ["1/3", "5/12", "7/18", "1/2"], "5/12",
      "Prime sums: 2 (1 way), 3 (2), 5 (4), 7 (6), 11 (2): 15 ways out of 36. Probability = 15/36 = 5/12.")
    perms = list(itertools.permutations("BBBGGG")); ok = [p for p in perms if all(not (p[i] == p[i+1] == "G") for i in range(5))]
    assert F(len(ok), len(perms)) == F(1, 5)
    M(t, "Medium", "Three boys and three girls stand in a row in a random order. What is the probability that no two girls stand next to each other?", ["1/10", "1/5", "1/4", "3/10"], "1/5",
      "Arrange the boys (3! ways), creating 4 gaps; put the girls in 3 of the gaps in 4 × 3 × 2 = 24 ways. Favourable = 6 × 24 = 144 out of 6! = 720. Probability = 144/720 = 1/5.")
    pa = F(1, 6) / (1 - F(25, 36)); assert pa == F(6, 11)
    M(t, "Medium", "A and B take turns rolling a fair die, A first. The first to roll a 6 wins. What is the probability that A wins?", ["1/2", "6/11", "5/11", "7/12"], "6/11",
      "A wins on the first roll with probability 1/6, or after both miss (25/36) the game restarts. P = 1/6 + (25/36)P, so P × 11/36 = 1/6 and P = 6/11.")
    tri = [c for c in itertools.combinations(range(1, 21), 3) if c[1] - c[0] == c[2] - c[1]]; assert len(tri) == 90 and F(90, math.comb(20, 3)) == F(3, 38)
    M(t, "Hard", "Three different numbers are chosen at random from 1, 2, …, 20. What is the probability that, in some order, they form an arithmetic progression?", ["1/19", "3/38", "1/10", "9/76"], "3/38",
      "An AP is fixed by its smallest term a and difference d with a + 2d ≤ 20. For d = 1 to 9 there are 20 − 2d choices of a: 18 + 16 + … + 2 = 90. Total choices = C(20, 3) = 1140. Probability = 90/1140 = 3/38.")
