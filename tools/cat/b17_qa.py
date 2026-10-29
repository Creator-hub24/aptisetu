"""Practice pack b17, Quantitative Ability (original items, added 30 Oct 2026) for the thinner topics:
Sets, Simple & Compound Interest, Averages, Time & Work, Mixtures & Alligation, Ratio & Proportion, Mensuration.
Every answer is recomputed here (brute force or exact fractions); the build stops if a check fails."""
import itertools, math
from fractions import Fraction as F

def build(B):
    s = "qa"; M = lambda *a, **k: B.mcq(s, *a, **k); T = lambda *a, **k: B.tita(s, *a, **k)
    pos = iter([2, 0, 3, 1] * 20)
    def mc(t, d, text, correct, wrong, sol):
        assert len(wrong) == 3 and correct not in wrong
        o = list(wrong); o.insert(next(pos), correct)
        M(t, d, text, o, correct, sol)

    # ---------------- Sets ----------------
    t = "Sets"
    sols = [(y, w, b) for b in range(1, 41) for y in [3*b] for w in [2*b] if y + w - b == 40]; assert sols == [(30, 20, 10)]
    T(t, "Easy", "Each of the 40 members of a gym does yoga or weight training or both. The number doing yoga is three times the number doing both, and the number doing weight training is twice the number doing both. How many members do yoga but not weight training?", 20,
      "Let b members do both. Then yoga = 3b and weights = 2b, and 3b + 2b − b = 4b = 40, so b = 10. Yoga only = 30 − 10 = 20.")

    # three apps: exactly-one 50, exactly-two 30, all three 10; |A|=55,|B|=45,|C|=40; |A∩B|=20,|B∩C|=15
    sols = set()
    for ab, bc, ca, abc in itertools.product(range(0, 41), repeat=4):
        if ab + bc + ca == 30 and abc == 10 and ab + abc == 20 and bc + abc == 15:
            a1, b1, c1 = 55 - ab - ca - abc, 45 - ab - bc - abc, 40 - bc - ca - abc
            if min(a1, b1, c1) >= 0 and a1 + b1 + c1 == 50: sols.add(ca + abc)
    assert sols == {25}
    mc(t, "Medium", "In a survey of users of three apps A, B and C, 50 people use exactly one of the apps, 30 use exactly two and 10 use all three. A has 55 users, B has 45 and C has 40. If 20 people use both A and B and 15 use both B and C (each figure including those who use all three), how many use both C and A?",
       "25", ["15", "20", "30"],
       "Count memberships two ways: 55 + 45 + 40 = 140 = 50 + 2 × 30 + 3 × 10, so the data are consistent. The three 'both' figures (each including the all-three group) add up to (exactly two) + 3 × (all three) = 30 + 30 = 60. So |C ∩ A| = 60 − 20 − 15 = 25. Check: only-A = 55 − 20 − 25 + 10 = 20, only-B = 45 − 20 − 15 + 10 = 20, only-C = 40 − 15 − 25 + 10 = 10, total 50.")

    best = 0
    for abc in range(0, 31):
        for ab in range(0, 41 - abc):
            for bc in range(0, 31 - abc):
                for ca in range(0, 31 - abc):
                    d1, m1, s1 = 40 - ab - ca - abc, 45 - ab - bc - abc, 30 - bc - ca - abc
                    if min(d1, m1, s1) < 0: continue
                    if d1 + m1 + s1 + ab + bc + ca + abc != 70: continue
                    best = max(best, d1 + m1 + s1)
    assert best == 47
    T(t, "Hard", "Each of the 70 students in a hostel joins at least one of three clubs: 40 join Drama, 45 join Music and 30 join Sports. What is the largest possible number of students who join exactly one club?", best,
      "Let e₁, e₂, e₃ be the numbers in exactly one, two and three clubs. Then e₁ + e₂ + e₃ = 70 and e₁ + 2e₂ + 3e₃ = 40 + 45 + 30 = 115, so e₂ + 2e₃ = 45 and e₁ = 70 − (e₂ + e₃) = 25 + e₃. To make e₁ large, make e₃ large: e₃ = 22 forces e₂ = 1 (e₃ = 22.5 is impossible), giving e₁ = 47. This is achievable: 22 in all three, 1 in Drama and Music only, 17 in Drama only, 22 in Music only and 8 in Sports only.")

    cnt = sum(1 for m in range(64) if m & 0b11); assert cnt == 48
    T(t, "Easy", "A set S has 6 elements, two of which are p and q. How many subsets of S contain p or q (or both)?", 48,
      "S has 2⁶ = 64 subsets. Those containing neither p nor q are the subsets of the other 4 elements: 2⁴ = 16. So 64 − 16 = 48 subsets contain at least one of p and q.")

    sols = [(c, b) for c in range(121) for b in range(121) if c + b - 25 == 105 and c == b + 30]
    assert sols == [(80, 50)]
    T(t, "Easy", "In a colony of 120 households, 15 own neither a car nor a bike and 25 own both. The number of households owning a car is 30 more than the number owning a bike. How many households own a car but not a bike?", 55,
      "Households with at least one vehicle = 120 − 15 = 105 = C + B − 25, so C + B = 130. With C = B + 30, B = 50 and C = 80. Car but not bike = 80 − 25 = 55.")

    best = 10**9
    for ab, bc, ca, abc in itertools.product(range(0, 31), repeat=4):
        a1, b1, c1 = 30 - ab - ca - abc, 25 - ab - bc - abc, 20 - bc - ca - abc
        if min(a1, b1, c1) < 0: continue
        if a1 + b1 + c1 + ab + bc + ca + abc != 40: continue
        best = min(best, a1 + b1 + c1)
    assert best == 5
    T(t, "Hard", "In a group of 50 people, 30 like Assamese tea, 25 like Bengal sweets and 20 like Coorg coffee, while 10 like none of the three. What is the smallest possible number of people who like exactly one of the three?", best,
      "40 people like at least one. With e₁, e₂, e₃ as the numbers liking exactly one, two and three: e₁ + e₂ + e₃ = 40 and e₁ + 2e₂ + 3e₃ = 75, so e₂ + 2e₃ = 35 and e₁ = 40 − e₂ − e₃ = 5 + e₃ ≥ 5. The value 5 is reached with e₃ = 0: 20 like tea and sweets only, 10 tea and coffee only, 5 sweets and coffee only, and 5 like coffee alone (no one likes only tea or only sweets).")

    # ---------------- Simple & Compound Interest ----------------
    t = "Simple & Compound Interest"
    P = [p for p in range(1, 100001) if p * F(44, 100) == (p + 3000) * F(40, 100)]; assert P == [30000]
    T(t, "Medium", "The compound interest on a sum for 2 years at 20% per annum (compounded annually) equals the simple interest on ₹3,000 more than that sum for 4 years at 10% per annum. What is the sum, in ₹?", 30000,
      "CI for 2 years at 20% = P(1.2² − 1) = 0.44P. SI = (P + 3000) × 10% × 4 = 0.4(P + 3000). So 0.44P = 0.4P + 1200, giving 0.04P = 1200 and P = ₹30,000.")

    eff = (F(103, 100)**4 - 1) * 100; assert round(float(eff), 2) == 12.55 and round((1.06**2 - 1)*100, 2) == 12.36
    mc(t, "Medium", "A deposit earns 12% per annum compounded quarterly. Correct to two decimal places, what is the equivalent annual rate of interest (compounded once a year)?",
       "12.55%", ["12.36%", "12.00%", "12.68%"],
       "Each quarter the money grows by 3%, so in a year it grows by a factor 1.03⁴ = 1.0609² = 1.12550881. The equivalent annual rate is about 12.55%. (12.36% would be the figure for half-yearly compounding at 12%.)")

    P = [p for p in range(100, 100001, 100) if p*F(16, 100) - p*(F(106, 100)**2 - 1) == 1092]; assert P == [30000]
    T(t, "Medium", "Two equal sums are invested for 2 years, one at 8% per annum simple interest and the other at 6% per annum compound interest (compounded annually). The simple interest exceeds the compound interest by ₹1,092. What is each sum, in ₹?", 30000,
      "SI = P × 0.08 × 2 = 0.16P. CI = P(1.06² − 1) = 0.1236P. The difference is 0.0364P = 1092, so P = ₹30,000.")

    x = [a for a in range(1, 22100) if a * F(11, 10)**5 == (22100 - a) * F(11, 10)**3]; assert x == [10000]
    T(t, "Medium", "₹22,100 is split between two sisters aged 13 and 15 and invested at 10% per annum compound interest (compounded annually) so that each receives the same amount on turning 18. How much (in ₹) is invested for the younger sister?", 10000,
      "The younger sister's share x grows for 5 years and the elder's share y for 3, so x(1.1)⁵ = y(1.1)³, i.e. y = 1.21x. Then x + 1.21x = 2.21x = 22,100, so x = ₹10,000 (and y = ₹12,100).")

    v0 = F(256000) / F(4, 5)**3; assert v0 == 500000
    T(t, "Easy", "A machine loses 20% of its value at the start of each year compared with the year before. Three years after purchase it is worth ₹2,56,000. What was its purchase price, in ₹?", 500000,
      "After three years its value is P × 0.8³ = 0.512P = 2,56,000, so P = ₹5,00,000.")

    bal = F(50000)
    for _ in range(2): bal = bal * F(11, 10) - 20000
    bal *= F(11, 10); assert bal == 20350
    T(t, "Medium", "Kabir borrows ₹50,000 at 10% per annum compound interest (compounded annually). He repays ₹20,000 at the end of the first year and ₹20,000 at the end of the second year. How much (in ₹) must he pay at the end of the third year to clear the loan?", 20350,
      "End of year 1: 50,000 × 1.1 − 20,000 = 35,000. End of year 2: 35,000 × 1.1 − 20,000 = 18,500. End of year 3: 18,500 × 1.1 = ₹20,350.")

    # ---------------- Averages ----------------
    t = "Averages"
    L = [k for k in range(100, 1000) if all(int(c) % 2 for c in str(k))]; assert len(L) == 125 and F(sum(L), len(L)) == 555
    T(t, "Medium", "What is the average of all three-digit numbers whose digits are all odd?", 555,
      "Each digit is chosen from 1, 3, 5, 7, 9, and every combination occurs (125 numbers). In each place the five digits occur equally often, so the average digit in every place is 5. The average number is therefore 555.")

    a = [z for z in (F(k, 10) for k in range(0, 1000)) if 30*z + 10*(z + 14) == 40*32]; assert a == [F(57, 2)]
    mc(t, "Medium", "A batter's average after 40 innings is 32. His average over the last 10 of those innings is 14 runs more than his average over the first 30. What was his average over the first 30 innings?",
       "28.5", ["27", "29", "30.5"],
       "Let the first-30 average be a. Then 30a + 10(a + 14) = 40 × 32 = 1280, so 40a = 1140 and a = 28.5.")

    L = list(range(38, 63)); assert F(sum(L), 25) == 50 and F(sum(L[5:]), 20) == F(105, 2)
    T(t, "Easy", "The average of 25 consecutive integers is 50. If the five smallest of them are removed, what is the average of the rest?", F(105, 2),
      "The middle (13th) integer is 50, so the integers run from 38 to 62. Removing 38–42 leaves 43, …, 62, whose average is (43 + 62)/2 = 52.5.")

    rest = (60 - F(1, 10)*90 - F(3, 10)*40) / F(6, 10); assert rest == 65
    T(t, "Medium", "In a test, the class average was 60. The top 10% of the class averaged 90 and the bottom 30% averaged 40. What was the average of the remaining students?", 65,
      "Per student, 60 = 0.1 × 90 + 0.3 × 40 + 0.6 × x = 9 + 12 + 0.6x, so 0.6x = 39 and x = 65.")

    ns = [n for n in range(1, 500) if F(n*(n+1)*(2*n+1), 6*n) == 295]; assert ns == [29]
    T(t, "Medium", "The average of the squares of the first n natural numbers (1², 2², …, n²) is 295. What is n?", 29,
      "The average is [n(n + 1)(2n + 1)/6]/n = (n + 1)(2n + 1)/6 = 295, so (n + 1)(2n + 1) = 1770 = 30 × 59. That gives n = 29 (n + 1 = 30, 2n + 1 = 59).")
    T(t, "Medium", "The average age of an 8-member committee today is the same as it was 4 years ago, because in the meantime one member was replaced by a new one. How many years younger is the new member than the member who left?", 32,
      "Without the change, the total age would have grown by 8 × 4 = 32 years in four years. Since the total (and so the average) is unchanged, the new member must be 32 years younger than the one replaced (comparing their ages today).")

    # ---------------- Time & Work ----------------
    t = "Time & Work"
    ab = [(a, b) for a in range(1, 200) for b in range(1, 200) if b == 3*a and b - a == 40]; assert ab == [(20, 60)] and 1/(F(1, 20) + F(1, 60)) == 15
    T(t, "Easy", "A works three times as fast as B and so takes 40 days fewer than B to finish a job alone. In how many days can they finish it working together?", 15,
      "If A takes a days, B takes 3a days, and 3a − a = 40 gives a = 20 (B: 60). Together they do 1/20 + 1/60 = 4/60 = 1/15 per day, so 15 days.")

    ts = [tt for tt in range(1, 200) if F(1, tt + 6) + F(1, tt + 24) == F(1, tt)]; assert ts == [12]
    T(t, "Hard", "Working alone, A would take 6 days more than A and B take together, and B alone would take 24 days more than they take together. How many days do A and B take together?", 12,
      "Let the joint time be t. Then 1/(t + 6) + 1/(t + 24) = 1/t. Clearing denominators: t(2t + 30) = (t + 6)(t + 24), i.e. 2t² + 30t = t² + 30t + 144, so t² = 144 and t = 12 days (A alone 18, B alone 36; check 1/18 + 1/36 = 1/12).")

    xs = [x for x in range(1, 100) if F(1, x) + F(1, x + 5) == F(1, 6)]; assert xs == [10]
    T(t, "Medium", "Two pipes together fill a tank in 6 hours. Alone, one of them takes 5 hours longer than the other. How many hours does the faster pipe take alone?", 10,
      "If the faster pipe takes x hours, 1/x + 1/(x + 5) = 1/6, so 6(2x + 5) = x(x + 5), i.e. x² − 7x − 30 = 0 = (x − 10)(x + 3). So x = 10 hours (the slower takes 15).")

    md = 60 * 20 * 3; extra = F(md * F(2, 3), 20) - 60; assert extra == 60
    T(t, "Medium", "A contractor undertakes to finish a road in 40 days and puts 60 workers on it. After 20 days only one-third of the road is finished. How many additional workers must he employ to finish on time, assuming all workers are equally efficient?", 60,
      "60 × 20 = 1200 worker-days built one-third, so the whole road needs 3600 worker-days and 2400 remain. In the remaining 20 days that needs 2400/20 = 120 workers, i.e. 60 more.")

    sol = [(a, b) for a in (F(1, k) for k in range(1, 200)) for b in [F(1, 15) - a] if b > 0 and 2*a + b/2 == F(1, 12)]
    assert sol == [(F(1, 30), F(1, 30))]
    T(t, "Hard", "A and B together finish a job in 15 days. If A worked at twice his usual speed and B at half her usual speed, together they would finish it in 12 days. How many days would A alone take at his usual speed?", 30,
      "Let their daily rates be a and b. Then a + b = 1/15 and 2a + b/2 = 1/12. Substituting b = 1/15 − a: 2a + 1/30 − a/2 = 1/12, so 1.5a = 1/12 − 1/30 = 1/20 and a = 1/30. A alone takes 30 days (and B also 30).")

    ns = [n for n in range(1, 200) if n*30 == (n + 6)*20]; assert ns == [12]
    T(t, "Medium", "A group of workers can finish a job in 30 days. If there were 6 more workers (all equally efficient), the job would be finished 10 days sooner. How many workers are in the group?", 12,
      "The job needs a fixed number of worker-days: 30n = 20(n + 6), so 10n = 120 and n = 12.")

    # ---------------- Mixtures & Alligation ----------------
    t = "Mixtures & Alligation"
    cp = F(96*1 + 120*2 + 144*3, 6); assert cp == 128 and (F(160) - cp) / cp == F(1, 4)
    mc(t, "Easy", "A shopkeeper blends three teas costing ₹96, ₹120 and ₹144 per kg in the ratio 1 : 2 : 3 by weight and sells the blend at ₹160 per kg. What is his profit percentage?",
       "25%", ["20%", "33⅓%", "28%"],
       "Cost of 6 kg = 96 + 240 + 432 = ₹768, i.e. ₹128 per kg. Profit = (160 − 128)/128 = 32/128 = 25%.")

    xs = [x for x in range(0, 41) if F(3, 10)*(40 - x) + F(8, 10)*x == F(45, 100)*40]; assert xs == [12]
    T(t, "Medium", "A 40-litre container holds a 30% acid solution. Some of it is drained and replaced by the same volume of an 80% acid solution, and the result is 45% acid. How many litres were replaced?", 12,
      "If x litres are replaced: 0.3(40 − x) + 0.8x = 0.45 × 40 = 18, so 12 + 0.5x = 18 and x = 12 litres.")

    Am, Bm, Bw = F(30), F(0), F(20)
    Am -= 10; Bm += 10
    back = F(10) / (Bm + Bw); Am += Bm * back; frac = Am / 30
    assert frac == F(7, 9)
    mc(t, "Hard", "Jar A holds 30 litres of pure milk and jar B holds 20 litres of pure water. 10 litres are poured from A into B and mixed thoroughly; then 10 litres of B's mixture are poured back into A. What fraction of the liquid now in A is milk?",
       "7/9", ["2/3", "5/6", "8/9"],
       "After the first pour, A has 20 L milk and B has 10 L milk + 20 L water (one-third milk). The 10 L poured back carry 10/3 L of milk, so A ends with 20 + 10/3 = 70/3 L of milk in 30 L. Fraction = (70/3)/30 = 7/9.")

    cpm = F(66) / F(11, 8); assert cpm == 48 and (F(60) - cpm) / cpm == F(1, 4)
    mc(t, "Medium", "A dairy buys milk at ₹60 per litre, adds water (which costs nothing) and sells the mixture at ₹66 per litre, making a profit of 37.5% on its cost. What is the ratio of water to milk in the mixture?",
       "1 : 4", ["1 : 5", "1 : 3", "2 : 5"],
       "Cost price of the mixture = 66/1.375 = ₹48 per litre. Since water is free, milk forms 48/60 = 4/5 of the mixture, so water : milk = 1/5 : 4/5 = 1 : 4.")

    sol = [(d1, 100 - d1) for d1 in range(0, 101) if F(d1, 20) + F(100 - d1, 30) == 4]; assert sol == [(40, 60)]
    mc(t, "Medium", "A cyclist covers 100 km in 4 hours, riding part of the way at 20 km/h and the rest at 30 km/h. How many kilometres does she ride at 20 km/h?",
       "40 km", ["50 km", "60 km", "45 km"],
       "Her average speed is 100/4 = 25 km/h, which is exactly midway between 20 and 30, so by alligation the times at the two speeds are equal: 2 hours each. Distance at 20 km/h = 20 × 2 = 40 km (and 60 km at 30 km/h; total 100 km).")

    salt = F(5, 100) * 60; left = salt / F(8, 100); assert 60 - left == F(45, 2)
    T(t, "Easy", "60 litres of brine contain 5% salt by volume. How many litres of water must evaporate for the salt to make up 8% of the brine?", F(45, 2),
      "The salt stays at 0.05 × 60 = 3 litres. For it to be 8%, the brine must be 3/0.08 = 37.5 litres, so 60 − 37.5 = 22.5 litres of water must evaporate.")

    # ---------------- Ratio & Proportion ----------------
    t = "Ratio & Proportion"
    xs = [x for x in range(-50, 7) if (11 - x)**2 == (7 - x)*(19 - x)]; assert xs == [3]
    T(t, "Medium", "What number must be subtracted from each of 7, 11 and 19 so that the three results are in continued proportion (that is, the first is to the second as the second is to the third)?", 3,
      "We need (11 − x)² = (7 − x)(19 − x): 121 − 22x + x² = 133 − 26x + x², so 4x = 12 and x = 3. Check: 4, 8, 16 and 4 : 8 = 8 : 16.")

    r = (5*3 - 2*4, 3*3 + 2*4); assert r == (7, 17)
    xs = [(F(5*x - 2*y, 3*x + 2*y)) for x, y in ((3, 4), (6, 8), (F(3, 2), 2))]; assert set(xs) == {F(7, 17)}
    mc(t, "Easy", "If x : y = 3 : 4, what is (5x − 2y) : (3x + 2y)?",
       "7 : 17", ["7 : 18", "1 : 2", "11 : 17"],
       "Put x = 3k and y = 4k. Then 5x − 2y = 15k − 8k = 7k and 3x + 2y = 9k + 8k = 17k, so the ratio is 7 : 17.")

    pr = [(a, b) for a in range(1, 100) for b in range(1, a) if 3*(a + b) == 7*(a - b) and a*b == 360]; assert pr == [(30, 12)]
    T(t, "Medium", "The sum and the difference of two positive numbers are in the ratio 7 : 3, and their product is 360. What is the larger number?", 30,
      "(a + b) : (a − b) = 7 : 3 gives 3a + 3b = 7a − 7b, so 4a = 10b and a : b = 5 : 2. Write a = 5k, b = 2k: 10k² = 360, k = 6, so the numbers are 30 and 12.")

    # ---------------- Mensuration ----------------
    t = "Mensuration"
    flow = F(22, 7) * F(7, 100)**2 * 5; assert flow == F(77, 1000) and F(154, 10) / flow == 200
    T(t, "Medium", "Water flows at 5 m/s through a pipe whose internal radius is 7 cm. How many seconds does it take to fill an empty tank of capacity 15.4 m³? (Take π = 22/7.)", 200,
      "Volume delivered per second = πr² × speed = (22/7) × 0.07² × 5 = (22/7) × 0.0049 × 5 = 0.077 m³. Time = 15.4/0.077 = 200 seconds.")

    d2 = [q for q in range(1, 30) if 12**2 + q**2 == 13**2]; assert d2 == [5] and F(24 * 10, 2) == 120
    T(t, "Easy", "A rhombus has perimeter 52 cm and one diagonal of 24 cm. What is its area, in cm²?", 120,
      "Side = 52/4 = 13 cm. The diagonals bisect each other at right angles, so half the other diagonal is √(13² − 12²) = 5 and that diagonal is 10 cm. Area = (24 × 10)/2 = 120 cm².")

    v = F(1, 3) * F(22, 7) * 7**2 * 14; assert v == F(2156, 3)
    assert F(22, 7) * 49 * 14 == 2156 and F(4, 3) * F(22, 7) * 343 == F(4312, 3)
    mc(t, "Medium", "What is the volume (in cm³) of the largest right circular cone that can be carved out of a solid cube of edge 14 cm? (Take π = 22/7.)",
       "718⅔", ["1437⅓", "2156", "1078"],
       "The largest cone has its base inscribed in one face (radius 7 cm) and its apex at the centre of the opposite face (height 14 cm). Volume = (1/3) × (22/7) × 7² × 14 = 2156/3 = 718⅔ cm³.")
