"""Practice pack b18, Quantitative Ability (original items, added 30 Oct 2026): Functions, Permutations & Combinations,
Probability, Percentages & Profit, Inequalities, Progressions, Time Speed & Distance, Sets.
Every answer is recomputed here (brute force or exact fractions); the build stops if a check fails."""
import itertools, math
from fractions import Fraction as F

def build(B):
    s = "qa"; M = lambda *a, **k: B.mcq(s, *a, **k); T = lambda *a, **k: B.tita(s, *a, **k)
    pos = iter([1, 3, 0, 2] * 20)
    def mc(t, d, text, correct, wrong, sol):
        assert len(wrong) == 3 and correct not in wrong
        o = list(wrong); o.insert(next(pos), correct)
        M(t, d, text, o, correct, sol)

    # ---------------- Functions ----------------
    t = "Functions"
    ab = [(a, b) for a in range(1, 20) for b in range(-20, 21) if a*a == 9 and a*b + b == 8]; assert ab == [(3, 2)]
    T(t, "Medium", "f(x) = ax + b with a > 0, and f(f(x)) = 9x + 8 for every real x. What is f(5)?", 17,
      "f(f(x)) = a(ax + b) + b = a²x + (ab + b). Matching coefficients: a² = 9, so a = 3 (as a > 0), and 3b + b = 8, so b = 2. Then f(5) = 15 + 2 = 17.")
    dom = [x for x in range(-10, 11) if 12 - x - x*x >= 0 and x + 2 > 0]; assert dom == [-1, 0, 1, 2, 3]
    T(t, "Medium", "How many integers lie in the domain of f(x) = √(12 − x − x²) + 1/√(x + 2)?", 5,
      "We need 12 − x − x² ≥ 0, i.e. x² + x − 12 = (x + 4)(x − 3) ≤ 0, so −4 ≤ x ≤ 3; and x + 2 > 0 (strictly, as it is under a root in a denominator), so x > −2. The domain is −2 < x ≤ 3, containing the integers −1, 0, 1, 2, 3: five integers.")
    vals = [F(k, 1000)**2 - 4*F(k, 1000) + 7 for k in range(0, 5001)]; assert max(vals) - min(vals) == 9
    T(t, "Medium", "For 0 ≤ x ≤ 5, the function f(x) = x² − 4x + 7 takes a greatest value G and a least value L. What is G − L?", 9,
      "f(x) = (x − 2)² + 3. On [0, 5] the least value is 3, at x = 2. The greatest is at the end farther from 2, namely x = 5: f(5) = 9 + 3 = 12 (f(0) is only 7). G − L = 12 − 3 = 9.")
    f = {1: 1}
    for n in range(2, 64): f[n] = f[n // 2] + (n % 2)
    assert sum(1 for n in range(1, 64) if f[n] == 3) == 20 == math.comb(6, 3)
    T(t, "Hard", "A function on the positive integers satisfies f(1) = 1, f(2n) = f(n) and f(2n + 1) = f(n) + 1 for every n ≥ 1. For how many n with 1 ≤ n ≤ 63 is f(n) = 3?", 20,
      "Halving n (dropping a final 0 in binary) keeps f the same, and n = 2m + 1 (a final 1) adds 1, so f(n) is the number of 1s in the binary form of n. The numbers 1 to 63 are exactly the non-zero 6-bit strings, and those with exactly three 1s number C(6, 3) = 20.")
    fo, ge = {3: 4, -3: -4}, {3: 5, -3: 5}; assert fo[-3]*ge[-3] + ge[-3] == -15
    mc(t, "Easy", "f is an odd function and g is an even function, with f(3) = 4 and g(3) = 5. If h(x) = f(x)·g(x) + g(x), what is h(−3)?",
       "−15", ["25", "15", "−25"],
       "Odd means f(−x) = −f(x), so f(−3) = −4; even means g(−x) = g(x), so g(−3) = 5. h(−3) = (−4)(5) + 5 = −15.")

    # ---------------- Permutations & Combinations ----------------
    t = "Permutations & Combinations"
    n = sum(1 for p in itertools.permutations("12345") if int("".join(p)) % 4 == 0); assert n == 24
    T(t, "Medium", "The digits 1, 2, 3, 4 and 5 are each used once to form five-digit numbers. How many of these numbers are divisible by 4?", 24,
      "A number is divisible by 4 exactly when its last two digits form a multiple of 4. From distinct digits 1–5 the possible endings are 12, 24, 32 and 52: four endings. The other three digits fill the first three places in 3! = 6 ways, giving 4 × 6 = 24.")
    n = sum(1 for c in itertools.combinations(range(1, 21), 3) if sum(c) % 3 == 0); assert n == 384
    T(t, "Hard", "In how many ways can three different numbers be chosen from 1, 2, …, 20 so that their sum is divisible by 3?", 384,
      "By remainder on division by 3: six numbers leave 0 (3, …, 18), seven leave 1 (1, …, 19) and seven leave 2 (2, …, 20). The sum is a multiple of 3 when all three remainders are equal or all three differ: C(6,3) + C(7,3) + C(7,3) + 6 × 7 × 7 = 20 + 35 + 35 + 294 = 384.")
    def pairings(xs):
        if not xs: return 1
        return sum(pairings(xs[1:i] + xs[i+1:]) for i in range(1, len(xs)))
    assert pairings(list(range(8))) == 105
    T(t, "Medium", "In how many ways can 8 badminton players be split into 4 doubles pairs (the pairs are not labelled or ordered)?", 105,
      "Take the first player: she can be paired in 7 ways. Of the remaining 6, the first can be paired in 5 ways, then 3, then 1. Total = 7 × 5 × 3 × 1 = 105. (Equivalently 8!/(2⁴ × 4!) = 40320/384 = 105.)")
    n = sum(1 for k in range(1000, 10000) if len(set(str(k))) < 4); assert n == 4464
    T(t, "Medium", "How many four-digit numbers have at least one digit that appears more than once?", 4464,
      "There are 9000 four-digit numbers. Those with all digits different: 9 choices for the first digit (not 0), then 9, 8 and 7, so 4536. The rest, 9000 − 4536 = 4464, have a repeated digit.")

    # ---------------- Probability ----------------
    t = "Probability"
    p = F(sum(1 for q in itertools.permutations(range(4)) if all(q[i] != i for i in range(4))), 24); assert p == F(3, 8)
    mc(t, "Medium", "Four letters are written to four different people, and the four addressed envelopes are ready. If the letters are put into the envelopes at random, one per envelope, what is the probability that no letter goes into its correct envelope?",
       "3/8", ["1/4", "5/8", "1/3"],
       "There are 4! = 24 equally likely arrangements. Count those with at least one letter correct by inclusion–exclusion: C(4,1)·3! − C(4,2)·2! + C(4,3)·1! − C(4,4)·0! = 24 − 12 + 4 − 1 = 15. So 24 − 15 = 9 arrangements put every letter wrong, and the probability is 9/24 = 3/8.")
    p = F(sum(1 for s in itertools.product("HT", repeat=6) if "HH" not in "".join(s)), 64); assert p == F(21, 64)
    mc(t, "Hard", "A fair coin is tossed 6 times. What is the probability that no two heads come up on consecutive tosses?",
       "21/64", ["13/64", "17/64", "1/3"],
       "Let aₙ be the number of length-n H/T strings with no two adjacent Hs. A valid string ends in T (after any valid string of length n − 1) or in TH (after any valid string of length n − 2), so aₙ = aₙ₋₁ + aₙ₋₂ with a₁ = 2, a₂ = 3. Then a₃ = 5, a₄ = 8, a₅ = 13, a₆ = 21. Probability = 21/64.")
    p = F(sum(1 for r in itertools.product(range(1, 7), repeat=3) if r[0] < r[1] < r[2]), 216); assert p == F(5, 54)
    mc(t, "Medium", "A fair die is rolled three times. What is the probability that each roll shows a strictly larger number than the roll before it?",
       "5/54", ["1/6", "5/27", "1/9"],
       "Any 3 different faces can appear in increasing order in exactly one way, so the favourable outcomes number C(6, 3) = 20 out of 6³ = 216. Probability = 20/216 = 5/54.")
    p = F(sum(1 for r in itertools.product(range(1, 6), repeat=3) if len(set(r)) == 3), 125); assert p == F(12, 25)
    mc(t, "Easy", "Three friends each pick a whole number from 1 to 5 independently and at random. What is the probability that all three pick different numbers?",
       "12/25", ["3/5", "2/5", "16/25"],
       "There are 5³ = 125 equally likely outcomes. All different: 5 × 4 × 3 = 60. Probability = 60/125 = 12/25.")
    p = F(sum(1 for x in range(1, 11) for y in range(1, 11) if x > y), 100); assert p == F(9, 20)
    mc(t, "Easy", "Two numbers x and y are each picked at random from 1 to 10, independently (so they may be equal). What is the probability that x > y?",
       "9/20", ["1/2", "11/20", "2/5"],
       "Of the 100 ordered pairs, 10 have x = y. The other 90 split evenly between x > y and x < y by symmetry, so 45 have x > y. Probability = 45/100 = 9/20.")

    # ---------------- Percentages & Profit ----------------
    t = "Percentages & Profit"
    cp = [c for c in range(721, 1080) if F(c - 720, c) == F(1080 - c, c)]; assert cp == [900]
    T(t, "Easy", "Selling a lamp for ₹720 causes the same percentage loss as the percentage profit made by selling it for ₹1,080. What is its cost price, in ₹?", 900,
      "Same percentage on the same cost price means the same rupee amount: C − 720 = 1080 − C, so C = (720 + 1080)/2 = ₹900 (a 20% loss or profit).")
    xs = [x for x in range(1, 100) if (1 + F(x, 100))*(1 - F(x, 100)) == F(96, 100)]; assert xs == [20]
    T(t, "Medium", "A price is raised by x% and the new price is then cut by x%. The final price is 4% below the original. What is x?", 20,
      "(1 + x/100)(1 − x/100) = 1 − x²/10000 = 0.96, so x² = 400 and x = 20.")
    xs = [x for x in range(1, 10000) if F(20, 100)*x - F(10, 100)*(10000 - x) == 560]; assert xs == [5200]
    T(t, "Medium", "A dealer buys a scooter and a bicycle for ₹10,000 in all. He sells the scooter at a 20% profit and the bicycle at a 10% loss, and his overall profit is 5.6%. What did the scooter cost him, in ₹?", 5200,
      "Overall profit = 5.6% of 10,000 = ₹560. If the scooter cost x, then 0.2x − 0.1(10000 − x) = 560, so 0.3x = 1560 and x = ₹5,200.")
    fr = F(16, 21) * F(9, 10) / F(12, 10); assert fr == F(4, 7)
    mc(t, "Easy", "When the numerator of a fraction is increased by 20% and its denominator is decreased by 10%, the fraction becomes 16/21. What was the original fraction?",
       "4/7", ["3/7", "5/7", "2/3"],
       "The fraction is multiplied by 1.2/0.9 = 4/3. So the original fraction = (16/21) × (3/4) = 4/7.")

    # ---------------- Inequalities ----------------
    t = "Inequalities"
    xs = [x for x in range(-50, 51) if x + 6 >= 0 and (x < 0 or x + 6 > x*x)]; assert xs == list(range(-6, 3))
    T(t, "Medium", "How many integers x satisfy √(x + 6) > x?", 9,
      "The root needs x + 6 ≥ 0, so x ≥ −6. For −6 ≤ x < 0 the left side is ≥ 0 and the right side is negative, so all of −6, …, −1 work (6 integers). For x ≥ 0 both sides are non-negative and we may square: x + 6 > x², i.e. x² − x − 6 = (x − 3)(x + 2) < 0, so 0 ≤ x < 3, giving 0, 1, 2. Total 6 + 3 = 9.")
    n = sum(1 for x in range(-4, 5) for y in range(-4, 5) if x*x + y*y < 10); assert n == 29
    T(t, "Medium", "How many ordered pairs of integers (x, y) satisfy x² + y² < 10?", 29,
      "Count by x. x = 0: y² < 10, so y = −3, …, 3 (7 values). x = ±1: y² < 9, y = −2, …, 2 (5 each, 10). x = ±2: y² < 6, y = −2, …, 2 (5 each, 10). x = ±3: y² < 1, y = 0 (1 each, 2). Total = 7 + 10 + 10 + 2 = 29.")
    grid = [F(k, 4) for k in range(-80, 81) if k != -12]
    sol = [z for z in grid if F(z - 2) / (z + 3) > 1]; assert sol and all(z < -3 for z in sol) and F(-13, 4) in sol and not any(z > -3 for z in sol)
    mc(t, "Medium", "For which real values of x is (x − 2)/(x + 3) > 1?",
       "x < −3", ["x > −3", "x > 2", "−3 < x < 2"],
       "Subtract 1: (x − 2)/(x + 3) − 1 = (x − 2 − x − 3)/(x + 3) = −5/(x + 3) > 0. That holds exactly when x + 3 < 0, i.e. x < −3. (Multiplying both sides by x + 3 without knowing its sign would be a mistake.)")
    ns = [n for n in range(1, 21) if 2**n > n**3]; assert ns == [1] + list(range(10, 21))
    T(t, "Hard", "For how many integers n with 1 ≤ n ≤ 20 is 2ⁿ > n³?", 12,
      "n = 1: 2 > 1, true. For n = 2 to 9 it fails (e.g. 2⁹ = 512 < 729 = 9³). At n = 10, 1024 > 1000, and from then on 2ⁿ doubles at each step while n³ grows by the factor ((n + 1)/n)³ ≤ 1.331 < 2, so it stays true. That is n = 1 and n = 10, …, 20: 1 + 11 = 12 integers.")

    # ---------------- Progressions ----------------
    t = "Progressions"
    partial = sum(F(k, 3**(k - 1)) for k in range(1, 60)); assert abs(float(partial) - 2.25) < 1e-12
    T(t, "Medium", "What is the sum of the infinite series 1 + 2/3 + 3/9 + 4/27 + 5/81 + …, whose k-th term is k/3^(k − 1)?", F(9, 4),
      "Let S be the sum. Then S/3 = 1/3 + 2/9 + 3/27 + …, and S − S/3 = 1 + 1/3 + 1/9 + 1/27 + … = 1/(1 − 1/3) = 3/2. So (2/3)S = 3/2 and S = 9/4 = 2.25.")
    d = [dd for dd in range(-20, 21) if 10*(96 + 9*dd) == 15*(96 + 14*dd)]; assert d == [-4] and 48 + 12*(-4) == 0
    T(t, "Medium", "An arithmetic progression has first term 48, and the sum of its first 10 terms equals the sum of its first 15 terms. What is its 13th term?", 0,
      "S₁₅ − S₁₀ = 0 means the 11th to 15th terms add to 0. They are five terms of an AP, so their middle one, the 13th term, is 0. (Indeed 5(96 + 9d) = 7.5(96 + 14d) gives d = −4, and 48 + 12 × (−4) = 0.)")
    sols = [(a - dd, a, a + dd) for a in [5] for dd in range(-30, 31) if min(a - dd, a, a + dd) > 0 and (a + 4)**2 == (a - dd + 1)*(a + dd + 19)]
    assert sols == [(2, 5, 8)]
    T(t, "Medium", "Three positive numbers in arithmetic progression add up to 15. If 1, 4 and 19 are added to them respectively, the results are in geometric progression. What is the largest of the three numbers?", 8,
      "Write them as 5 − d, 5, 5 + d. Then 6 − d, 9, 24 + d are in GP, so 81 = (6 − d)(24 + d) = 144 − 18d − d², i.e. d² + 18d − 63 = 0 = (d − 3)(d + 21). d = −21 would give 26, 5, −16 (not all positive), so d = 3: the numbers are 2, 5, 8 (and 3, 9, 27 is the GP). The largest is 8.")

    # ---------------- Time, Speed & Distance ----------------
    t = "Time, Speed & Distance"
    sol = [(N, e) for N in range(1, 200) for e in [F(N - 20, 40)] if e > 0 and 30 + 30*e == N]; assert sol == [(60, 1)]
    T(t, "Hard", "An escalator moves upwards at a constant speed. Walking up it, Rhea takes 20 steps and reaches the top in 40 seconds. Walking faster, she takes 30 steps and reaches the top in 30 seconds. How many steps are visible on the escalator?", 60,
      "Let the escalator move e steps per second and let N steps be visible. Each trip covers N steps: N = 20 + 40e and N = 30 + 30e. Subtracting, 10e = 10, so e = 1 and N = 60.")
    vs = [v for v in range(1, 200) if F(360, v) - F(360, v + 20) == F(3, 2)]; assert vs == [60]
    T(t, "Medium", "If a car's average speed were 20 km/h higher, a 360 km journey would take 1 hour 30 minutes less. What is its actual average speed, in km/h?", 60,
      "360/v − 360/(v + 20) = 3/2 gives 360 × 20 × 2 = 3v(v + 20), i.e. v² + 20v − 4800 = 0 = (v − 60)(v + 80). So v = 60 km/h (6 hours, versus 4.5 hours at 80 km/h).")
    tmeet = F(60 - 6, 30); minutes = 9*60 + 30 + tmeet*60; assert minutes == 11*60 + 18
    mc(t, "Medium", "Towns P and Q are 60 km apart. Asha leaves P for Q at 9:00 a.m., cycling at 12 km/h. Bilal leaves Q for P at 9:30 a.m., riding at 18 km/h. At what time do they meet?",
       "11:18 a.m.", ["11:00 a.m.", "11:30 a.m.", "11:12 a.m."],
       "By 9:30 Asha has covered 6 km, leaving 54 km between them. They then close the gap at 12 + 18 = 30 km/h, which takes 54/30 = 1.8 hours = 1 hour 48 minutes. They meet at 9:30 + 1:48 = 11:18 a.m.")

    # ---------------- Sets ----------------
    t = "Sets"
    ex = (50 - 20 - 5, 20, 5); assert ex[0]*1 + ex[1]*2 + ex[2]*3 == 80
    T(t, "Medium", "Each of the 50 students in a class plays at least one of hockey, chess and tennis. 20 of them play exactly two of the games and 5 play all three. What is the sum of the numbers of hockey players, chess players and tennis players?", 80,
      "25 students play exactly one game. Adding the three game totals counts each student once per game played: 25 × 1 + 20 × 2 + 5 × 3 = 25 + 40 + 15 = 80.")
