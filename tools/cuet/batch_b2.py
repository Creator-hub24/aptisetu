"""CUET (UG) batch B2 (Oct 2026): original items that bring every thin topic up to at least 6.
Maths answers are verified with sympy; reasoning items by enumeration; GK items are static textbook facts."""
import itertools, math
import sympy as sp
from sympy import Rational as Q, pi, sqrt, symbols, Matrix, integrate, simplify, atan, asin, acos, exp, log, sin, cos
from fractions import Fraction as F
A1, B1 = "Section A (common)", "Section B1 (Mathematics)"
x, y = symbols("x y")
def eq(a, b): return simplify(a - b) == 0

import random as _r
def balanced(B, sec, seed):
    """mcq() wrapper that moves the correct option (by a swap) to a deterministic, balanced position unless fixed=True."""
    pos = [i for _ in range(40) for i in range(4)]; _r.Random(seed).shuffle(pos); it = iter(pos)
    def M(part, topic, diff, text, options, correct, solution, **k):
        options = list(options)
        if not k.get("fixed"):
            t_ = next(it); c_ = options.index(correct); options[c_], options[t_] = options[t_], options[c_]
        return B.mcq(sec, part, topic, diff, text, options, correct, solution, **k)
    return M

def lp_vertices(cons):
    """cons: list of linear expressions in (X, Y) that must be <= 0. Returns the corner points."""
    X, Y = symbols("X Y"); vs = set()
    for c1, c2 in itertools.combinations(cons, 2):
        s_ = sp.solve([c1, c2], [X, Y], dict=True)
        if s_ and all(c.subs(s_[0]) <= 0 for c in cons): vs.add((s_[0][X], s_[0][Y]))
    return vs

def maths(B):
    M = balanced(B, "maths", 2601)
    X, Y = symbols("X Y")
    # ---- Application of Integrals (+4)
    t = "Application of Integrals"
    a1 = integrate(4 - x**2, (x, -2, 2)); assert a1 == Q(32, 3)
    M(A1,t,"Easy","What is the area of the region bounded by the parabola y = 4 − x² and the x-axis?",["32/3 square units","16/3 square units","8 square units","64/3 square units"],"32/3 square units","The parabola meets the x-axis at x = ±2. Area = ∫₋₂² (4 − x²) dx = [4x − x³/3] from −2 to 2 = (8 − 8/3) − (−8 + 8/3) = 32/3.")
    a2 = integrate(sp.sqrt(x), (x, 0, 4)); assert a2 == Q(16, 3)
    M(A1,t,"Medium","What is the area of the region bounded by y = √x, the x-axis and the line x = 4?",["16/3 square units","8/3 square units","4 square units","32/3 square units"],"16/3 square units","Area = ∫₀⁴ x^{1/2} dx = [(2/3) x^{3/2}] from 0 to 4 = (2/3)(8) = 16/3.")
    a3 = integrate((x + 2) - x**2, (x, -1, 2)); assert a3 == Q(9, 2) and set(sp.solve(x**2 - x - 2)) == {-1, 2}
    M(A1,t,"Hard","What is the area of the region enclosed by the parabola y = x² and the line y = x + 2?",["9/2 square units","7/2 square units","5 square units","11/2 square units"],"9/2 square units","The curves meet where x² = x + 2, i.e. x = −1 and x = 2, and the line lies above the parabola in between. Area = ∫₋₁² (x + 2 − x²) dx = [x²/2 + 2x − x³/3] from −1 to 2 = 10/3 − (−7/6) = 9/2.")
    a4 = integrate(sp.sqrt(9 - x**2), (x, 0, 3)); assert eq(a4, 9 * pi / 4)
    M(A1,t,"Medium","What is the area of the region in the first quadrant bounded by the circle x² + y² = 9 and the coordinate axes?",["9π/4 square units","9π/2 square units","3π/4 square units","9π square units"],"9π/4 square units","The region is a quarter of a circle of radius 3. Area = ∫₀³ √(9 − x²) dx = (1/4)π(3)² = 9π/4.")
    # ---- Linear Programming (+4)
    t = "Linear Programming"
    v = lp_vertices([X + 2*Y - 8, 3*X + Y - 9, -X, -Y]); assert v == {(0, 0), (3, 0), (0, 4), (2, 3)}
    z = {p: 4*p[0] + 5*p[1] for p in v}; assert max(z.values()) == 23 and max(z, key=z.get) == (2, 3)
    M(A1,t,"Medium","Maximise Z = 4x + 5y subject to x + 2y ≤ 8, 3x + y ≤ 9, x ≥ 0, y ≥ 0. The maximum value of Z is:",["23","20","12","24"],"23","Corner points: (0, 0), (3, 0), (0, 4) and the meeting point of x + 2y = 8 and 3x + y = 9, which is (2, 3). Z = 0, 12, 20 and 8 + 15 = 23. The maximum is 23 at (2, 3).")
    v = lp_vertices([2 - X - Y, 1 - X, -Y, X - 4, Y - 4]); z = {p: 3*p[0] + p[1] for p in v}
    assert v == {(1, 1), (2, 0), (4, 0), (4, 4), (1, 4)} and min(z.values()) == 4 and [p for p in z if z[p] == 4] == [(1, 1)]
    M(A1,t,"Medium","Minimise Z = 3x + y subject to x + y ≥ 2, 1 ≤ x ≤ 4 and 0 ≤ y ≤ 4. The minimum value of Z is:",["4","6","5","3"],"4","The corner points are (1, 1), (2, 0), (4, 0), (4, 4) and (1, 4). Z = 4, 6, 12, 16 and 7. The minimum is 4 at (1, 1).")
    v = lp_vertices([X + Y - 6, -X, -Y, X - 4]); z = {p: 2*p[0] + 2*p[1] for p in v}
    assert max(z.values()) == 12 and sorted(p for p in z if z[p] == 12) == [(0, 6), (4, 2)]
    M(A1,t,"Hard","For Z = 2x + 2y subject to x + y ≤ 6, x ≤ 4, x ≥ 0, y ≥ 0, which statement is true?",["The maximum 12 occurs at every point of the segment joining (4, 2) and (0, 6)","The maximum 12 occurs only at (0, 6)","The maximum 16 occurs at (4, 4)","Z has no maximum value"],"The maximum 12 occurs at every point of the segment joining (4, 2) and (0, 6)","Corner points: (0, 0), (4, 0), (4, 2) and (0, 6). Z = 0, 8, 12 and 12. Two adjacent corners give the same largest value and Z = 2(x + y) is constant along x + y = 6, so the maximum 12 is attained at every point of the segment joining (4, 2) and (0, 6).")
    M(A1,t,"Easy","In a linear programming problem, the feasible region is:",["the set of points that satisfy all the constraints, including the non-negativity constraints","the set of corner points only","the region where the objective function is zero","the set of points that satisfy at least one constraint"],"the set of points that satisfy all the constraints, including the non-negativity constraints","By definition the feasible region is the common region of all the constraints of the problem (including x ≥ 0, y ≥ 0). An optimal value, if it exists, occurs at a corner point of this region.")
    # ---- Three-dimensional Geometry (+3)
    t = "Three-dimensional Geometry"
    P1, P2 = Matrix([1, -2, 3]), Matrix([3, 4, -1]); mid = (P1 + P2) / 2; d12 = (P2 - P1).norm(); assert list(mid) == [2, 1, 1] and d12 == 2 * sqrt(14)
    M(B1,t,"Easy","What is the distance between the points (1, −2, 3) and (3, 4, −1)?",["2√14 units","√14 units","14 units","4√7 units"],"2√14 units","Distance = √((3 − 1)² + (4 + 2)² + (−1 − 3)²) = √(4 + 36 + 16) = √56 = 2√14.")
    n1, n2 = Matrix([2, -1, 2]), Matrix([1, 2, -2]); cth = abs(n1.dot(n2)) / (n1.norm() * n2.norm()); assert cth == Q(4, 9)
    M(B1,t,"Medium","The cosine of the angle between the planes 2x − y + 2z = 5 and x + 2y − 2z = 1 is:",["4/9","2/9","1/3","5/9"],"4/9","The angle between planes is the angle between their normals (2, −1, 2) and (1, 2, −2). cos θ = |2 − 2 − 4| / (3 × 3) = 4/9.")
    # skew lines r = (1,2,3) + λ(1,0,1), r = (0,1,0) + μ(0,1,1)
    a_, b_ = Matrix([1, 2, 3]), Matrix([0, 1, 0]); d1, d2 = Matrix([1, 0, 1]), Matrix([0, 1, 1]); cr = d1.cross(d2)
    sd = abs((b_ - a_).dot(cr)) / cr.norm(); assert list(cr) == [-1, -1, 1] and list(b_ - a_) == [-1, -1, -3] and eq(sd, 1 / sqrt(3))
    M(B1,t,"Hard","What is the shortest distance between the lines r = (î + 2ĵ + 3k̂) + λ(î + k̂) and r = ĵ + μ(ĵ + k̂)?",["1/√3 units","2/√3 units","√3 units","1 unit"],"1/√3 units","With a₁ = (1, 2, 3), a₂ = (0, 1, 0), b₁ = (1, 0, 1) and b₂ = (0, 1, 1): b₁ × b₂ = (−1, −1, 1), whose length is √3, and a₂ − a₁ = (−1, −1, −3). The dot product (a₂ − a₁) · (b₁ × b₂) = 1 + 1 − 3 = −1. Shortest distance = |−1|/√3 = 1/√3.")
    # ---- Vectors (+3)
    t = "Vectors"
    a, b = Matrix([2, -1, 2]), Matrix([1, 1, 0]); pr = a.dot(b) / b.norm(); assert eq(pr, 1 / sqrt(2))
    M(B1,t,"Medium","The projection of a = 2î − ĵ + 2k̂ on b = î + ĵ is:",["1/√2","1","√2","1/3"],"1/√2","Projection of a on b = (a · b)/|b| = (2 − 1 + 0)/√2 = 1/√2.")
    a, b, c = Matrix([1, 1, 1]), Matrix([1, -1, 0]), Matrix([0, 1, 2]); trip = Matrix.hstack(a, b, c).det(); assert trip == -3
    M(B1,t,"Medium","What is the volume of the parallelepiped whose edges are a = î + ĵ + k̂, b = î − ĵ and c = ĵ + 2k̂?",["3 cubic units","2 cubic units","6 cubic units","1 cubic unit"],"3 cubic units","Volume = |[a b c]| = |det of rows (1, 1, 1), (1, −1, 0), (0, 1, 2)| = |1(−2 − 0) − 1(2 − 0) + 1(1 − 0)| = |−3| = 3.")
    u = Matrix([3, -4, 0]); uh = u / u.norm(); assert list(uh) == [Q(3, 5), Q(-4, 5), 0]
    M(B1,t,"Easy","The unit vector in the direction of 3î − 4ĵ is:",["(3î − 4ĵ)/5","(3î − 4ĵ)/7","(3î + 4ĵ)/5","(4î − 3ĵ)/5"],"(3î − 4ĵ)/5","|3î − 4ĵ| = √(9 + 16) = 5, so the unit vector is (3î − 4ĵ)/5.")
    # ---- Determinants (+2)
    t = "Determinants"
    k = symbols("k"); sk = sp.solve(Matrix([[k, 2], [3, k - 1]]).det(), k); assert set(sk) == {3, -2}
    M(A1,t,"Medium","For which values of k is the matrix [[k, 2], [3, k − 1]] singular?",["k = 3 or k = −2","k = −3 or k = 2","k = 2 or k = 3","k = 1 only"],"k = 3 or k = −2","Singular means the determinant is zero: k(k − 1) − 6 = 0, i.e. k² − k − 6 = 0 = (k − 3)(k + 2). So k = 3 or k = −2.")
    xs = sp.solve([2*x + 3*y - 8, x - y + 1], [x, y]); D = Matrix([[2, 3], [1, -1]]).det(); Dx = Matrix([[8, 3], [-1, -1]]).det(); Dy = Matrix([[2, 8], [1, -1]]).det()
    assert (D, Dx, Dy) == (-5, -5, -10) and xs == {x: 1, y: 2}
    M(A1,t,"Easy","By Cramer's rule, the solution of 2x + 3y = 8 and x − y = −1 is:",["x = 1, y = 2","x = 2, y = 1","x = −1, y = 2","x = 1, y = −2"],"x = 1, y = 2","D = (2)(−1) − (3)(1) = −5. Dx = (8)(−1) − (3)(−1) = −5. Dy = (2)(−1) − (8)(1) = −10. x = Dx/D = 1 and y = Dy/D = 2.")
    # ---- Differential Equations (+2)
    t = "Differential Equations"
    yf = sp.Function("y"); s1 = sp.dsolve(sp.Eq(yf(x).diff(x) + yf(x), exp(-x)), yf(x), ics={yf(0): 2}); assert eq(s1.rhs, (x + 2) * exp(-x))
    M(A1,t,"Hard","The solution of dy/dx + y = e^{−x} with y(0) = 2 is:",["y = (x + 2)e^{−x}","y = (x − 2)e^{−x}","y = 2e^{−x} + x","y = (2x + 1)e^{−x}"],"y = (x + 2)e^{−x}","The integrating factor is eˣ. Then d(y eˣ)/dx = e^{−x} · eˣ = 1, so y eˣ = x + c. y(0) = 2 gives c = 2, so y = (x + 2)e^{−x}.")
    s2 = sp.dsolve(sp.Eq(yf(x).diff(x), 2 * x * yf(x)), yf(x), ics={yf(0): 3}); assert eq(s2.rhs, 3 * exp(x**2))
    M(A1,t,"Medium","The solution of dy/dx = 2xy with y(0) = 3 is:",["y = 3e^{x²}","y = e^{3x²}","y = 3e^{2x}","y = x² + 3"],"y = 3e^{x²}","Separate the variables: dy/y = 2x dx, so log|y| = x² + c and y = Ae^{x²}. y(0) = 3 gives A = 3.")
    # ---- Inverse Trigonometric Functions (+2)
    t = "Inverse Trigonometric Functions"
    assert abs(float(asin(Q(3, 5)) + acos(Q(3, 5)) - pi / 2)) < 1e-12
    v2 = sp.expand_trig(sp.tan(2 * sp.Symbol("u"))).subs(sp.tan(sp.Symbol("u")), Q(1, 3)); assert v2 == Q(3, 4) and abs(math.tan(2 * math.atan(1 / 3)) - 0.75) < 1e-12
    M(B1,t,"Medium","The value of tan(2 tan⁻¹(1/3)) is:",["3/4","2/3","4/3","1/3"],"3/4","Let θ = tan⁻¹(1/3), so tan θ = 1/3. tan 2θ = 2 tan θ / (1 − tan²θ) = (2/3)/(8/9) = 3/4.")
    v3 = acos(cos(7 * pi / 6)); assert eq(v3, 5 * pi / 6)
    M(B1,t,"Hard","The value of cos⁻¹(cos(7π/6)) is:",["5π/6","7π/6","π/6","−π/6"],"5π/6","The principal range of cos⁻¹ is [0, π], and 7π/6 is outside it. cos(7π/6) = cos(2π − 7π/6) = cos(5π/6), and 5π/6 lies in [0, π]. So the value is 5π/6.")
    # ---- Relations & Functions (+1)
    t = "Relations & Functions"
    A = [1, 2, 3]; n_eq = 0
    allp = list(itertools.product(A, A)); others = [p for p in allp if p[0] != p[1]]
    for bits in itertools.product([0, 1], repeat=len(others)):
        R = {p for p in allp if p[0] == p[1]} | {p for p, b_ in zip(others, bits) if b_}
        if all((b2, a2) in R for a2, b2 in R) and all((a2, d2) in R for a2, b2 in R for c2, d2 in R if b2 == c2): n_eq += 1
    assert n_eq == 5
    M(B1,t,"Hard","How many equivalence relations can be defined on the set {1, 2, 3}?",["5","3","4","8"],"5","An equivalence relation corresponds to a partition of the set. {1, 2, 3} has 5 partitions: all three separate (1 way), one pair together with the third alone (3 ways), and all three together (1 way). So there are 5.")

ROMAN = ["i", "ii", "iii", "iv"]
def match_item(M, diff, head, pairs, distractors, why):
    """pairs: list of (word, meaning) in List I order; List II is shown in a fixed scrambled order.
    distractors: three alternative mappings (lists of List-II positions). The key is computed, never typed."""
    order = [3, 0, 2, 1] if len(pairs) == 4 else None
    l2 = [None] * 4
    for li, pos in enumerate(order): l2[pos] = pairs[li][1]
    key = [order[i] for i in range(4)]
    fmt = lambda m: ", ".join(f"{'abcd'[i]}–{ROMAN[m[i]]}" for i in range(4))
    opts = [fmt(key)] + [fmt(d) for d in distractors]
    assert len(set(opts)) == 4 and all(sorted(d) == [0, 1, 2, 3] for d in distractors)
    text = head + "<br>List I: " + " ".join(f"({'abcd'[i]}) {w}" for i, (w, _) in enumerate(pairs)) + "<br>List II: " + " ".join(f"({ROMAN[i]}) {m}" for i, m in enumerate(l2))
    sol = "; ".join(f"{w} = {m} ({ROMAN[order[i]]})" for i, (w, m) in enumerate(pairs)) + ". " + why
    M("Verbal Ability", "Match the following", diff, text, opts, opts[0], sol)

def english(B):
    M = balanced(B, "english", 2602)
    VA = "Verbal Ability"
    # ---- Match the following (+5); key a–iv, b–i, c–iii, d–ii in every item (List II order is derived), distractors vary
    D1 = [[0, 3, 2, 1], [3, 2, 0, 1], [1, 0, 2, 3]]
    match_item(M, "Easy", "Match each word in List I with its meaning in List II.", [("Candid", "frank and honest"), ("Frugal", "careful not to waste money"), ("Lethargic", "sluggish and without energy"), ("Obstinate", "stubbornly refusing to change")], D1, "These are the standard dictionary senses of the four words.")
    match_item(M, "Medium", "Match each phrase in List I with its meaning in List II.", [("A blessing in disguise", "something good that first seemed bad"), ("To burn the midnight oil", "to work or study late into the night"), ("To beat about the bush", "to avoid coming to the point"), ("A red-letter day", "a memorable, happy day")], [[3, 0, 1, 2], [2, 0, 3, 1], [3, 1, 0, 2]], "These are the accepted meanings of the four idioms.")
    match_item(M, "Medium", "Match each word in List I with its antonym in List II.", [("Transparent", "opaque"), ("Ancient", "modern"), ("Expand", "contract"), ("Humble", "arrogant")], [[0, 3, 2, 1], [3, 0, 1, 2], [2, 1, 3, 0]], "Each pair is a standard pair of opposites.")
    match_item(M, "Medium", "Match each literary device in List I with its example in List II.", [("Simile", "Her smile was like sunshine."), ("Metaphor", "Time is a thief."), ("Personification", "The wind whispered through the trees."), ("Alliteration", "Peter picked a peck of pickled peppers.")], [[3, 0, 1, 2], [3, 2, 0, 1], [1, 0, 2, 3]], "A simile compares using 'like' or 'as'; a metaphor states that one thing is another; personification gives human actions to a non-human thing; alliteration repeats the opening consonant sound.")
    match_item(M, "Hard", "Match each word in List I with its meaning in List II.", [("Ubiquitous", "found everywhere"), ("Pragmatic", "dealing with things in a practical way"), ("Ambivalent", "having mixed feelings"), ("Laconic", "using very few words")], [[3, 2, 0, 1], [0, 1, 2, 3], [3, 0, 1, 2]], "These are the standard dictionary senses of the four words.")
    # ---- One-word substitution (+4)
    M(VA,"One-word substitution","Easy","Choose the one word that can replace the phrase: a person who does not believe in the existence of God.",["Atheist","Agnostic","Heretic","Pagan"],"Atheist","An atheist denies that God exists. An agnostic holds that it cannot be known, a heretic rejects the accepted teaching of a religion, and a pagan follows a non-mainstream or older faith.")
    M(VA,"One-word substitution","Easy","Choose the one word that can replace the phrase: a speech made by a character alone on the stage, speaking their thoughts aloud.",["Soliloquy","Dialogue","Epilogue","Monograph"],"Soliloquy","A soliloquy is spoken alone, voicing one's thoughts. A dialogue needs two or more speakers, an epilogue is a closing section, and a monograph is a detailed written study.")
    M(VA,"One-word substitution","Medium","Choose the one word that can replace the phrase: a government by a small group of powerful people.",["Oligarchy","Monarchy","Democracy","Anarchy"],"Oligarchy","Oligarchy is rule by a few. Monarchy is rule by one sovereign, democracy is rule by the people, and anarchy is the absence of government.")
    M(VA,"One-word substitution","Medium","Choose the one word that can replace the phrase: a word or phrase that reads the same backwards as forwards.",["Palindrome","Anagram","Acronym","Homonym"],"Palindrome","'Level' and 'madam' are palindromes. An anagram rearranges letters, an acronym is formed from initial letters, and a homonym shares spelling or sound with a different word.")
    # ---- Error spotting (+1)
    M(VA,"Error spotting","Medium","Identify the part of the sentence that contains an error: (A) Although she is / (B) senior than me / (C) by three years, / (D) we joined the firm together.",["A","B","C","D"],"B","Adjectives such as senior, junior, superior and inferior take 'to', not 'than'. The correct phrase is 'senior to me', so the error is in part B.",fixed=True)
    # ---- Rearranging the parts (+2)
    M(VA,"Rearranging the parts","Easy","Rearrange the parts to form a meaningful sentence:<br>P: before sunrise &nbsp; Q: my grandfather &nbsp; R: every morning &nbsp; S: goes for a walk",["QSRP","QRPS","SQRP","SPQR"],"QSRP","'My grandfather (Q) goes for a walk (S) every morning (R) before sunrise (P).' Subject, verb phrase, then how often, then when.")
    M(VA,"Rearranging the parts","Medium","Rearrange the parts to form a meaningful sentence:<br>P: although it was raining heavily &nbsp; Q: reached the station &nbsp; R: on time &nbsp; S: the students",["PSQR","SQPR","PQSR","SPQR"],"PSQR","'Although it was raining heavily (P), the students (S) reached the station (Q) on time (R).' The concessive clause comes first; the main clause has its subject before the verb and object.")

def gat(B):
    from gat import FX, AR, DS
    SA = ["Only assumption I is implicit", "Only assumption II is implicit", "Both I and II are implicit", "Neither I nor II is implicit"]
    M = balanced(B, "gat", 2603)
    QR, LR, GMA, GK = "Quantitative Reasoning", "Logical & Analytical Reasoning", "General Mental Ability", "General Knowledge"
    # ======== QR: Averages (+4)
    t = "Averages"
    assert 55 + 8 * 2.5 == 75
    M(QR,t,"Medium","The average weight of 8 people goes up by 2.5 kg when one of them, who weighs 55 kg, is replaced by a new person. What is the weight of the new person?",["75 kg","57.5 kg","65 kg","80 kg"],"75 kg","The total weight goes up by 8 × 2.5 = 20 kg, so the new person weighs 20 kg more than the person replaced: 55 + 20 = 75 kg.",chk=(55 + 8 * 2.5, 75))
    odd = [o for o in range(1, 100, 2) if (o + o + 2 + o + 4) == 81]; assert odd == [25]
    M(QR,t,"Easy","The average of three consecutive odd numbers is 27. What is the largest of them?",["29","27","31","25"],"29","For consecutive odd numbers the average is the middle number, 27. The numbers are 25, 27 and 29, so the largest is 29.",chk=(odd[0] + 4, 29))
    M(QR,t,"Medium","A student's average mark in 5 subjects is 72. How many marks must the student score in a sixth subject to raise the average of all six to 75?",["90","78","85","95"],"90","Total needed for 6 subjects = 6 × 75 = 450. Total so far = 5 × 72 = 360. Marks needed = 450 − 360 = 90.",chk=(6 * 75 - 5 * 72, 90))
    M(QR,t,"Medium","The average age of the 5 members of a family is 30 years. A baby is born, and one year later the average age of the 6 members is:",["26 years","25 years","25.8 years","31 years"],"26 years","Total age now = 5 × 30 = 150. One year later the 5 members add 5 years (155) and the baby is 1, so the total is 156. Average = 156/6 = 26.",chk=((150 + 5 + 1) / 6, 26))
    # ======== QR: Geometry (+4)
    t = "Geometry"
    M(QR,t,"Easy","What is the sum of the interior angles of a hexagon?",["720°","540°","900°","360°"],"720°","Sum of interior angles = (n − 2) × 180° = (6 − 2) × 180° = 720°.",chk=((6 - 2) * 180, 720))
    M(QR,t,"Easy","The two shorter sides of a right-angled triangle are 9 cm and 12 cm. What is the length of the hypotenuse?",["15 cm","21 cm","13 cm","√63 cm"],"15 cm","By Pythagoras, hypotenuse = √(9² + 12²) = √(81 + 144) = √225 = 15 cm.",chk=(math.hypot(9, 12), 15))
    M(QR,t,"Medium","Each exterior angle of a regular polygon is 40°. How many sides does it have?",["9","8","10","12"],"9","The exterior angles of any convex polygon add up to 360°. Number of sides = 360°/40° = 9.",chk=(360 / 40, 9))
    M(QR,t,"Medium","An arc of a circle subtends an angle of 110° at the centre. What angle does it subtend at a point on the remaining part of the circle?",["55°","110°","70°","125°"],"55°","The angle subtended by an arc at the centre is twice the angle it subtends at any point on the remaining part of the circle. So the angle is 110°/2 = 55°.",chk=(110 / 2, 55))
    # ======== QR: Mensuration (+4)
    t = "Mensuration"
    v = 22 / 7 * 7 * 7 * 10; assert abs(v - 1540) < 1e-9
    M(QR,t,"Medium","A cylindrical tank has a base radius of 7 m and a height of 10 m. How many litres of water can it hold when full? (Use π = 22/7 and 1 m³ = 1000 litres.)",["15,40,000 litres","1,54,000 litres","15,400 litres","4,40,000 litres"],"15,40,000 litres","Volume = πr²h = 22/7 × 7 × 7 × 10 = 1540 m³. In litres: 1540 × 1000 = 15,40,000 litres.",chk=(v * 1000, 1540000))
    M(QR,t,"Medium","A cuboid measures 12 cm by 8 cm by 5 cm. What is its total surface area?",["392 cm²","480 cm²","196 cm²","296 cm²"],"392 cm²","Total surface area = 2(lb + bh + hl) = 2(12 × 8 + 8 × 5 + 5 × 12) = 2(96 + 40 + 60) = 2 × 196 = 392 cm².",chk=(2 * (96 + 40 + 60), 392))
    h = math.sqrt(10 ** 2 - 6 ** 2); assert h == 8
    M(QR,t,"Medium","A right circular cone has a base radius of 6 cm and a slant height of 10 cm. What is its volume?",["96π cm³","120π cm³","288π cm³","360π cm³"],"96π cm³","Height h = √(10² − 6²) = √64 = 8 cm. Volume = (1/3)πr²h = (1/3) × π × 36 × 8 = 96π cm³.",chk=(36 * 8 / 3, 96))
    M(QR,t,"Easy","A rectangle is 12 cm long and 5 cm wide. What is the length of its diagonal?",["13 cm","17 cm","12.5 cm","√119 cm"],"13 cm","Diagonal = √(12² + 5²) = √(144 + 25) = √169 = 13 cm.",chk=(math.hypot(12, 5), 13))
    # ======== QR: Statistics (+4)
    t = "Statistics"
    M(QR,t,"Easy","What is the mean of 4, 8, 12, 16 and 20?",["12","10","14","60"],"12","Sum = 4 + 8 + 12 + 16 + 20 = 60. Mean = 60/5 = 12.",chk=(sum([4, 8, 12, 16, 20]) / 5, 12))
    dd = [15, 7, 22, 9, 31, 12]
    M(QR,t,"Easy","What is the range of the data 15, 7, 22, 9, 31, 12?",["24","22","31","16"],"24","Range = largest − smallest = 31 − 7 = 24.",chk=(max(dd) - min(dd), 24))
    xv = 5 * 9 - (6 + 8 + 10 + 12); assert xv == 9
    M(QR,t,"Medium","The mean of 6, 8, x, 10 and 12 is 9. What is x?",["9","8","10","7"],"9","The sum must be 5 × 9 = 45. 6 + 8 + 10 + 12 = 36, so x = 45 − 36 = 9.",chk=(xv, 9))
    vals = [2, 4, 6, 8, 10]; mu = sum(vals) / 5; var = sum((v - mu) ** 2 for v in vals) / 5; assert var == 8
    M(QR,t,"Hard","What is the variance of 2, 4, 6, 8 and 10? (Divide by the number of observations.)",["8","10","4","2√2"],"8","Mean = 30/5 = 6. Squared deviations: 16, 4, 0, 4, 16, total 40. Variance = 40/5 = 8.",chk=(var, 8))
    # ======== LR: Assertion & Reason (+2)
    t = "Assertion & Reason"
    M(LR,t,"Medium","Assertion (A): The Sun appears reddish at sunrise and sunset.<br>Reason (R): At these times sunlight travels a longer path through the atmosphere, so more of the blue light is scattered away before it reaches us.",AR,AR[0],"Both statements are true, and the longer path that removes blue light by scattering is exactly why the remaining light looks red. So R correctly explains A.",fixed=True)
    M(LR,t,"Medium","Assertion (A): A person standing in a lift that is accelerating upward feels heavier than usual.<br>Reason (R): The mass of the person increases when the lift accelerates upward.",AR,AR[2],"A is true: the floor must push up with more than the person's weight to accelerate them, so they feel heavier. R is false: mass does not change; only the normal force (apparent weight) increases.",fixed=True)
    # ======== LR: Statements & Conclusions (+3)
    t = "Statements & Conclusions"
    M(LR,t,"Easy","Statement: No student who scored below 40% in the final exam was promoted. Rohan was promoted.<br>Conclusions: I. Rohan scored at least 40% in the final exam. II. Rohan scored above 90% in the final exam.",FX,FX[0],"If Rohan had scored below 40% he would not have been promoted, so he scored at least 40%: I follows. Nothing tells us how far above 40% he scored, so II does not follow.",fixed=True)
    M(LR,t,"Medium","Statement: The municipal corporation has decided to fine anyone found throwing waste on the streets ₹500.<br>Conclusions: I. The corporation wants the streets to be kept clean. II. From now on, nobody will throw waste on the streets.",FX,FX[0],"A fine for littering shows that the corporation wants clean streets, so I follows. A fine discourages littering but cannot guarantee that nobody will ever do it, so II does not follow.",fixed=True)
    M(LR,t,"Medium","Statement: All trains to Jaipur have been cancelled today because of track repairs. Amit needed to travel to Jaipur today by train.<br>Conclusions: I. Amit could not travel to Jaipur by train today. II. Track repairs on the Jaipur route are carried out every day.",FX,FX[0],"Since every train to Jaipur is cancelled today, Amit could not go by train: I follows. The statement is about today only, so II does not follow.",fixed=True)
    # ======== LR: Data Sufficiency (+3)
    t = "Data Sufficiency"
    rv = sp.solve([x - y - 4, x + y - 30], [x, y]); assert rv == {x: 17, y: 13}
    M(LR,t,"Easy","Question: What is Ravi's age?<br>Statement I: Ravi is 4 years older than Sita.<br>Statement II: The sum of the ages of Ravi and Sita is 30 years.",DS,DS[2],"I alone gives only the difference of the ages, and II alone gives only their sum. Together: R − S = 4 and R + S = 30, so R = 17. Both statements are needed.",fixed=True)
    n1 = [n for n in range(-50, 51) if n * n == 49 and n > 0]; n2 = [n for n in range(-50, 51) if 3 * n - 5 == 16]; assert n1 == [7] and n2 == [7]
    M(LR,t,"Medium","Question: What is the value of the integer n?<br>Statement I: n² = 49 and n is positive.<br>Statement II: 3n − 5 = 16.",DS,DS[3],"I: n² = 49 gives n = 7 or −7, and n positive leaves n = 7. II: 3n = 21, so n = 7. Each statement alone gives the value.",fixed=True)
    M(LR,t,"Medium","Question: How many students are there in the class?<br>Statement I: Riya is 12th from the top and 18th from the bottom of the class list.<br>Statement II: The class has 5 more boys than girls.",DS,DS[0],"I gives the total: 12 + 18 − 1 = 29 students. II gives only the difference between boys and girls, not the total. So I alone is sufficient, but II alone is not.",fixed=True,chk=(12 + 18 - 1, 29))
    # ======== LR: Statements & Assumptions (+4)
    t = "Statements & Assumptions"
    M(LR,t,"Easy","Statement: \"Please carry an umbrella; the weather office has forecast heavy rain this evening,\" a mother tells her son.<br>Assumptions: I. The weather forecast is likely to be reliable. II. An umbrella can protect a person from rain.",SA,SA[2],"The advice only makes sense if the mother trusts the forecast (I) and believes an umbrella will help in rain (II). Both are implicit.",fixed=True)
    M(LR,t,"Medium","Statement: The government has decided to set up 100 new public libraries in rural areas.<br>Assumptions: I. People in rural areas would use the libraries. II. There are no public libraries in urban areas.",SA,SA[0],"Building libraries assumes that people will use them, so I is implicit. The decision is about rural areas and says nothing about urban libraries, so II is not implicit.",fixed=True)
    M(LR,t,"Easy","Statement: \"Use our toothpaste for stronger teeth,\" says an advertisement.<br>Assumptions: I. People want stronger teeth. II. No other toothpaste can make teeth stronger.",SA,SA[0],"An advertisement promising stronger teeth assumes that people want them, so I is implicit. It does not need to assume that every other toothpaste fails, so II is not implicit.",fixed=True)
    M(LR,t,"Medium","Statement: A company has announced a 10% bonus for employees who join its new training programme.<br>Assumptions: I. Some employees may be motivated by a bonus to join the programme. II. The training programme is compulsory for all employees.",SA,SA[0],"Offering a bonus to those who join assumes that a bonus can motivate some employees, so I is implicit. If the programme were compulsory there would be no need for an incentive, so II is not implicit.",fixed=True)
    # ======== LR: Venn Diagrams (+4)
    t = "Venn Diagrams"
    M(LR,t,"Easy","In a class of 50 students, every student studies Hindi or English or both. 28 study Hindi and 30 study English. How many study both?",["8","12","22","2"],"8","n(H ∪ E) = 50. Both = 28 + 30 − 50 = 8.",chk=(28 + 30 - 50, 8))
    un = 60 + 45 + 40 - 20 - 15 - 18 + 8; assert un == 100
    M(LR,t,"Medium","Of 120 people surveyed, 60 read newspaper A, 45 read B and 40 read C. 20 read both A and B, 15 read both B and C, 18 read both A and C, and 8 read all three. How many read none of the three?",["20","28","12","32"],"20","At least one = 60 + 45 + 40 − 20 − 15 − 18 + 8 = 100. None = 120 − 100 = 20.",chk=(120 - un, 20))
    M(LR,t,"Easy","In a club of 70 members, 30 play chess, 25 play carrom and 20 play both. How many play exactly one of the two games?",["15","35","55","45"],"15","Only chess = 30 − 20 = 10 and only carrom = 25 − 20 = 5. Exactly one = 10 + 5 = 15.",chk=((30 - 20) + (25 - 20), 15))
    mins = min(b for b in range(0, 121) if 150 + 120 - b <= 200); assert mins == 70
    M(LR,t,"Medium","Of 200 people, 150 own a smartphone and 120 own a laptop. What is the least possible number of people who own both?",["70","30","120","50"],"70","At most 200 people can own at least one. Both = 150 + 120 − (number with at least one) ≥ 270 − 200 = 70, and 70 is reached when everyone owns at least one.",chk=(mins, 70))
    # ======== GMA: Analogies (+4)
    t = "Analogies"
    M(GMA,t,"Easy","Doctor : Hospital :: Teacher : ?",["School","Book","Student","Lesson"],"School","A doctor works in a hospital; a teacher works in a school.")
    M(GMA,t,"Easy","3 : 27 :: 5 : ?",["125","25","15","75"],"125","27 = 3³, so the second term is the cube of the first. 5³ = 125.",chk=(5 ** 3, 125))
    sh = lambda w: "".join(chr(ord(c) + 1) for c in w); assert sh("ACE") == "BDF" and sh("GIK") == "HJL"
    M(GMA,t,"Medium","ACE : BDF :: GIK : ?",["HJL","HIJ","IKM","FHJ"],"HJL","Each letter of ACE moves one place forward to give BDF. Doing the same to GIK gives HJL.")
    M(GMA,t,"Medium","Bird : Flock :: Fish : ?",["School","Herd","Pack","Swarm"],"School","A group of birds is a flock; a group of fish is a school. A herd is of cattle, a pack of wolves and a swarm of insects.")
    # ======== GMA: Mathematical Operations (+5)
    t = "Mathematical Operations"
    def sub(expr, m): return "".join(m.get(c, c) for c in expr)
    e1 = sub("18 × 6 − 3 + 4 ÷ 2", {"×": "+", "+": "-", "−": "/", "÷": "*"}); v1 = eval(e1); assert v1 == 12
    M(GMA,t,"Medium","If × means +, + means −, − means ÷ and ÷ means ×, what is the value of 18 × 6 − 3 + 4 ÷ 2?",["12","16","8","20"],"12","Replacing the signs gives 18 + 6 ÷ 3 − 4 × 2. Division and multiplication first: 18 + 2 − 8 = 12.",chk=(v1, 12))
    e2 = sub("20 P 15 S 3 Q 4 R 2", {"P": "+", "Q": "-", "R": "*", "S": "/"}); v2 = eval(e2); assert v2 == 17
    M(GMA,t,"Easy","If P means +, Q means −, R means × and S means ÷, what is the value of 20 P 15 S 3 Q 4 R 2?",["17","25","13","21"],"17","The expression is 20 + 15 ÷ 3 − 4 × 2 = 20 + 5 − 8 = 17.",chk=(v2, 17))
    star = lambda a, b: a * a - b; assert star(5, star(3, 4)) == 20
    M(GMA,t,"Medium","If a ★ b = a² − b, what is the value of 5 ★ (3 ★ 4)?",["20","21","5","16"],"20","3 ★ 4 = 9 − 4 = 5. Then 5 ★ 5 = 25 − 5 = 20.",chk=(star(5, star(3, 4)), 20))
    hs = [v for v in range(-20, 21) if 2 * v + 3 * 4 == 20]; assert hs == [4]
    M(GMA,t,"Easy","If a # b = 2a + 3b, and x # 4 = 20, what is x?",["4","8","2","6"],"4","x # 4 = 2x + 12 = 20, so 2x = 8 and x = 4.",chk=(hs[0], 4))
    base = "12 ÷ 4 + 3 × 6 − 2"; py = {"+": "+", "×": "*", "−": "-", "÷": "/"}
    def swap_ok(a, b):
        e = "".join(b if c == a else a if c == b else c for c in base); return abs(eval(sub(e, py)) - 13) < 1e-9
    cand = {"+ and ×": ("+", "×"), "÷ and −": ("÷", "−"), "+ and ÷": ("+", "÷"), "× and −": ("×", "−")}
    good = [k for k, (a, b) in cand.items() if swap_ok(a, b)]; assert good == ["+ and ×"], good
    allgood = [(a, b) for a, b in itertools.combinations("+×−÷", 2) if swap_ok(a, b)]; assert allgood == [("+", "×")], allgood
    M(GMA,t,"Hard","Which two signs must be interchanged to make the equation 12 ÷ 4 + 3 × 6 − 2 = 13 correct?",list(cand),"+ and ×","Interchanging + and × gives 12 ÷ 4 × 3 + 6 − 2 = 3 × 3 + 6 − 2 = 9 + 6 − 2 = 13, which is correct. The other swaps give: ÷ and − → 12 − 4 + 3 × 6 ÷ 2 = 17; + and ÷ → 12 + 4 ÷ 3 × 6 − 2 = 18; × and − → 12 ÷ 4 + 3 − 6 × 2 = −6.")
    # ======== GK: Indian Polity (+1)
    M(GK,"Indian Polity","Easy","Who appoints the Chief Justice of India?",["The President of India","The Prime Minister","The Parliament","The Union Law Minister"],"The President of India","Under Article 124 of the Constitution, the judges of the Supreme Court, including the Chief Justice of India, are appointed by the President.")
    # ======== GK: Geography (+3)
    M(GK,"Geography","Easy","Which is the largest state of India by area?",["Rajasthan","Madhya Pradesh","Maharashtra","Uttar Pradesh"],"Rajasthan","Rajasthan, at about 3.42 lakh km², is the largest state by area; Madhya Pradesh is second.")
    M(GK,"Geography","Easy","The Western Ghats are also known as the:",["Sahyadri","Aravalli","Vindhya","Satpura"],"Sahyadri","The Western Ghats are called the Sahyadri. The Aravalli, Vindhya and Satpura are separate ranges in north-western and central India.")
    M(GK,"Geography","Medium","Which is the southernmost point of mainland India?",["Kanyakumari","Indira Point","Rameswaram","Thiruvananthapuram"],"Kanyakumari","Kanyakumari (Cape Comorin) is the southern tip of the mainland. Indira Point, in the Great Nicobar island, is the southernmost point of India as a whole, but it is not on the mainland.")
    # ======== GK: History (+3)
    M(GK,"History","Easy","The Jallianwala Bagh massacre of 1919 took place in which city?",["Amritsar","Lahore","Lucknow","Meerut"],"Amritsar","On 13 April 1919, troops under General Dyer fired on a crowd at Jallianwala Bagh in Amritsar, Punjab.")
    M(GK,"History","Easy","Who founded the Maurya Empire?",["Chandragupta Maurya","Ashoka","Bindusara","Bimbisara"],"Chandragupta Maurya","Chandragupta Maurya founded the empire around 321 BCE with the help of Chanakya. Bindusara was his son and Ashoka his grandson; Bimbisara was an earlier ruler of Magadha.")
    M(GK,"History","Medium","In which year was the Quit India Movement launched?",["1942","1930","1920","1947"],"1942","The Quit India Movement was launched by the Indian National Congress on 8 August 1942 in Bombay.")
    # ======== GK: General Science (+4)
    M(GK,"General Science","Easy","Which gas do green plants take in from the air for photosynthesis?",["Carbon dioxide","Oxygen","Nitrogen","Hydrogen"],"Carbon dioxide","In photosynthesis plants use carbon dioxide and water, with sunlight, to make glucose, and release oxygen.")
    M(GK,"General Science","Easy","What is the chemical formula of common salt?",["NaCl","KCl","NaOH","CaCO₃"],"NaCl","Common salt is sodium chloride, NaCl. KCl is potassium chloride, NaOH is sodium hydroxide and CaCO₃ is calcium carbonate.")
    M(GK,"General Science","Easy","Which part of a cell is known as its 'powerhouse'?",["Mitochondria","Nucleus","Ribosome","Cell wall"],"Mitochondria","Mitochondria carry out cellular respiration and release most of the cell's energy (as ATP), hence the name 'powerhouse'.")
    M(GK,"General Science","Medium","What is the approximate speed of light in a vacuum?",["3 × 10⁸ m/s","3 × 10⁶ m/s","3 × 10⁵ m/s","3 × 10¹⁰ m/s"],"3 × 10⁸ m/s","Light travels about 3 × 10⁸ metres per second in a vacuum (more precisely 299,792,458 m/s).")
    # ======== GK: Environment (+4)
    M(GK,"Environment","Easy","The ozone layer is found mainly in which layer of the atmosphere?",["Stratosphere","Troposphere","Mesosphere","Thermosphere"],"Stratosphere","Most of the atmosphere's ozone lies in the stratosphere, roughly 15 to 35 km above the Earth, where it absorbs harmful ultraviolet rays.")
    M(GK,"Environment","Medium","In which year was Project Tiger launched in India?",["1973","1972","1985","1992"],"1973","Project Tiger was launched on 1 April 1973 to protect the tiger and its habitat. (The Wildlife Protection Act was passed in 1972.)")
    M(GK,"Environment","Easy","Which of the following is a non-renewable resource?",["Coal","Solar energy","Wind energy","Tidal energy"],"Coal","Coal is a fossil fuel formed over millions of years and cannot be replaced on a human timescale. Solar, wind and tidal energy are renewable.")
    M(GK,"Environment","Medium","Which greenhouse gas is released in the largest quantity by burning fossil fuels?",["Carbon dioxide","Methane","Nitrous oxide","Ozone"],"Carbon dioxide","Burning coal, oil and gas releases carbon dioxide in far larger amounts than any other greenhouse gas; methane comes mainly from agriculture, wetlands and gas leaks.")
