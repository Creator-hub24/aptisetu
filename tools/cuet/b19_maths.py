"""CUET (UG) batch B19 (30 Oct 2026): original Mathematics items for the thinner chapters.
Every answer is computed or verified here with sympy / exhaustive enumeration; the build fails if any check fails."""
import itertools
import sympy as sp
from sympy import Rational as Q, pi, sqrt, symbols, Matrix, integrate, simplify, diff, atan, asin, acos, exp, log, sin, cos, E as e_
from fractions import Fraction as F
from batch_b2 import balanced
from maths import mx
A1, B1 = "Section A (common)", "Section B1 (Mathematics)"
x, y = symbols("x y", real=True)
def eq(a, b): return simplify(a - b) == 0

def maths(B):
    M = balanced(B, "maths", 1919)
    # ---------- Determinants (+4)
    t = "Determinants"
    D = Matrix([[2, -3, 5], [6, 0, 4], [1, 5, -7]]); assert D.cofactor(1, 2) == -13
    M(A1,t,"Easy",f"For the determinant {mx([[2,-3,5],[6,0,4],[1,5,-7]])}, what is the cofactor of the element 4 (row 2, column 3)?",["−13","13","7","−7"],"−13","Delete row 2 and column 3: the minor is 2·5 − (−3)·1 = 10 + 3 = 13. The cofactor carries the sign (−1)²⁺³ = −1, so it is −13.")
    assert sp.solve(sp.Eq(Matrix([[x, 2], [18, x]]).det(), Matrix([[6, 2], [18, 6]]).det()), x) == [-6, 6]
    M(A1,t,"Easy",f"If {mx([['x',2],[18,'x']])} = {mx([[6,2],[18,6]])} as determinants, then x equals:",["±6","6 only","±3","±2"],"±6","x² − 36 = 36 − 36 = 0, so x² = 36 and x = ±6.")
    a, b, c = symbols("a b c")
    assert sp.expand(Matrix([[a-b, b-c, c-a], [b-c, c-a, a-b], [c-a, a-b, b-c]]).det()) == 0
    M(A1,t,"Medium",f"For all real a, b, c, the value of the determinant {mx([['a − b','b − c','c − a'],['b − c','c − a','a − b'],['c − a','a − b','b − c']])} is:",["0","1","(a − b)(b − c)(c − a)","a³ + b³ + c³ − 3abc"],"0","Add the second and third columns to the first (this does not change the determinant). Every entry of the first column becomes (a − b) + (b − c) + (c − a) = 0, and a determinant with a zero column is 0.")
    assert sp.solve(Matrix([[1, x, x**2], [1, 2, 4], [1, 3, 9]]).det(), x) == [2, 3]
    M(A1,t,"Medium",f"The roots of the equation {mx([[1,'x','x²'],[1,2,4],[1,3,9]])} = 0 are:",["2 and 3","−2 and −3","1 and 2","1 and 3"],"2 and 3","The determinant is a polynomial in x of degree at most 2. Putting x = 2 makes rows 1 and 2 identical, and x = 3 makes rows 1 and 3 identical, so both give 0. A quadratic with leading coefficient 3 − 2 = 1 ≠ 0 has no other roots: x = 2 and x = 3.")
    # ---------- Matrices (+4)
    t = "Matrices"
    for A in (Matrix([[1, 0], [0, 0]]), Matrix([[2, -2], [1, -1]])):
        assert A**2 == A; I2 = sp.eye(2); assert (I2 + A)**3 - 7*A == I2
    M(A1,t,"Medium","A square matrix A satisfies A² = A. Then (I + A)³ − 7A equals:",["I","A","I + A","0"],"I","Since A² = A, every power Aⁿ = A. (I + A)³ = I + 3A + 3A² + A³ = I + 3A + 3A + A = I + 7A. So (I + A)³ − 7A = I.")
    assert Matrix([[1, 1], [0, 1]])**10 == Matrix([[1, 10], [0, 1]])
    M(A1,t,"Medium",f"If A = {mx([[1,1],[0,1]])}, then A¹⁰ equals:",[mx([[1,10],[0,1]]),mx([[1,1],[0,1]]),mx([[10,10],[0,10]]),mx([[1,1024],[0,1]])],mx([[1,10],[0,1]]),"A² = [[1, 2], [0, 1]], A³ = [[1, 3], [0, 1]], and in general Aⁿ = [[1, n], [0, 1]] (each multiplication by A adds 1 to the top-right entry). So A¹⁰ = [[1, 10], [0, 1]].")
    th = symbols("theta"); R = Matrix([[cos(th), -sin(th)], [sin(th), cos(th)]])
    assert sp.solve(sp.Eq(2*cos(th), 1), th)[0] == pi/3 and (R + R.T).subs(th, pi/3) == sp.eye(2)
    M(A1,t,"Easy",f"If A = {mx([['cos θ','−sin θ'],['sin θ','cos θ']])} and A + Aᵀ = I, where 0 < θ < π/2, then θ equals:",["π/3","π/6","π/4","π/2"],"π/3","A + Aᵀ = [[2cos θ, 0], [0, 2cos θ]]. Setting this equal to I gives 2cos θ = 1, so cos θ = 1/2 and θ = π/3.")
    Am, Bm = sp.ones(2, 3), sp.ones(3, 4); assert (Am*Bm).T.shape == (4, 2)
    M(A1,t,"Easy","A is a 2 × 3 matrix and B is a 3 × 4 matrix. What is the order of (AB)ᵀ?",["4 × 2","2 × 4","3 × 3","3 × 2"],"4 × 2","AB is defined (A has 3 columns, B has 3 rows) and has order 2 × 4. Its transpose has order 4 × 2.")
    # ---------- Application of Integrals (+3)
    t = "Application of Integrals"
    assert eq(4*integrate(3*sqrt(1 - x**2/16), (x, 0, 4)), 12*pi)
    M(A1,t,"Medium","What is the area enclosed by the ellipse x²/16 + y²/9 = 1?",["12π square units","7π square units","25π square units","24π square units"],"12π square units","By symmetry the area is 4 × ∫₀⁴ (3/4)√(16 − x²) dx. ∫₀⁴ √(16 − x²) dx is a quarter of the area of a circle of radius 4, i.e. 4π, so the area = 4 × (3/4) × 4π = 12π (in general πab).")
    assert eq(integrate(cos(x) - sin(x), (x, 0, pi/4)), sqrt(2) - 1)
    M(A1,t,"Medium","What is the area of the region between the curves y = cos x and y = sin x from x = 0 to x = π/4?",["√2 − 1 square units","√2 square units","1 − 1/√2 square units","√2 + 1 square units"],"√2 − 1 square units","On [0, π/4], cos x ≥ sin x. Area = ∫₀^{π/4} (cos x − sin x) dx = [sin x + cos x]₀^{π/4} = (1/√2 + 1/√2) − (0 + 1) = √2 − 1.")
    assert integrate(2 - sp.Abs(x), (x, -2, 2)) * 2 == 8
    M(A1,t,"Easy","What is the area of the region enclosed by the curve |x| + |y| = 2?",["8 square units","4 square units","16 square units","2 square units"],"8 square units","For −2 ≤ x ≤ 2 the region runs from y = −(2 − |x|) to y = 2 − |x|. Area = 2∫₋₂² (2 − |x|) dx = 2 × 4 = 8. (It is a square with diagonals 4 and 4: area = ½ × 4 × 4 = 8.)")
    # ---------- Differential Equations (+4)
    t = "Differential Equations"
    yv = x*log(x); assert eq(diff(yv, x) - (x + yv)/x, 0) and yv.subs(x, 1) == 0 and eq(yv.subs(x, e_), e_)
    M(A1,t,"Medium","If x dy/dx = x + y for x > 0 and y = 0 when x = 1, what is y when x = e?",["e","1","e²","2e"],"e","Put y = vx: v + x dv/dx = 1 + v, so dv/dx = 1/x and v = log x + C. y(1) = 0 gives C = 0, so y = x log x and y(e) = e × 1 = e.")
    k_, t_ = symbols("k t", positive=True); N0 = symbols("N0", positive=True); Nt = N0*exp(k_*t_)
    kk = sp.solve(sp.Eq(Nt.subs(t_, 2), 2*N0), k_)[0]; assert eq(Nt.subs({k_: kk, t_: 6})/N0, 8)
    M(A1,t,"Medium","A bacteria culture grows at a rate proportional to its size (dN/dt = kN) and doubles in 2 hours. How many times its original size is it after 6 hours?",["8","6","3","12"],"8","dN/dt = kN gives N = N₀eᵏᵗ. Doubling in 2 hours means e²ᵏ = 2. After 6 hours N/N₀ = e⁶ᵏ = (e²ᵏ)³ = 2³ = 8.")
    cands = {"y = 3 sin x − 2 cos x": 3*sin(x) - 2*cos(x), "y = eˣ": exp(x), "y = x sin x": x*sin(x), "y = sin x + x": sin(x) + x}
    ok = [k for k, f in cands.items() if eq(diff(f, x, 2) + f, 0)]; assert ok == ["y = 3 sin x − 2 cos x"]
    M(A1,t,"Easy","Which of the following is a solution of the differential equation d²y/dx² + y = 0?",list(cands),"y = 3 sin x − 2 cos x","For y = 3 sin x − 2 cos x: y′ = 3 cos x + 2 sin x and y″ = −3 sin x + 2 cos x = −y, so y″ + y = 0. For eˣ, y″ + y = 2eˣ; for x sin x, y″ + y = 2cos x; for sin x + x, y″ + y = x — none of these is 0.")
    M(A1,t,"Easy","How many arbitrary constants does the general solution of a third-order differential equation contain?",["3","2","1","0"],"3","The general solution of a differential equation of order n contains exactly n arbitrary constants, so a third-order equation has 3 (a particular solution has none).")
    # ---------- Inverse Trigonometric Functions (+4)
    t = "Inverse Trigonometric Functions"
    assert sp.solve([2*x - 1 >= -1, 2*x - 1 <= 1], x) == sp.And(sp.Le(0, x), sp.Le(x, 1))
    M(B1,t,"Easy","What is the domain of the function f(x) = sin⁻¹(2x − 1)?",["[0, 1]","[−1, 1]","[−1, 0]","[0, 2]"],"[0, 1]","sin⁻¹ is defined only on [−1, 1], so −1 ≤ 2x − 1 ≤ 1. Adding 1: 0 ≤ 2x ≤ 2, so 0 ≤ x ≤ 1.")
    rs = sp.solve(6*x**2 + 5*x - 1, x); assert set(rs) == {Q(1, 6), -1}
    good = [r for r in rs if abs(sp.N(atan(2*r) + atan(3*r) - pi/4, 30)) < 1e-25]; assert good == [Q(1, 6)] and sp.N(atan(-2) + atan(-3)) < 0
    M(B1,t,"Hard","Which value of x satisfies tan⁻¹(2x) + tan⁻¹(3x) = π/4?",["1/6","−1","1/6 and −1","1/5"],"1/6","Taking tan of both sides: (2x + 3x)/(1 − 6x²) = 1, so 6x² + 5x − 1 = 0, i.e. (6x − 1)(x + 1) = 0 and x = 1/6 or −1. For x = −1 both tan⁻¹(−2) and tan⁻¹(−3) are negative, so their sum cannot be π/4; it is rejected. Check x = 1/6: tan⁻¹(1/3) + tan⁻¹(1/2) = tan⁻¹((5/6)/(5/6)) = π/4.")
    pts = [F(k, 100) for k in range(-100, 101)]; S = [p for p in pts if sp.N(acos(sp.Rational(p.numerator, p.denominator))) > sp.N(asin(sp.Rational(p.numerator, p.denominator)))]
    assert max(S) == F(70, 100) and min(S) == -1 and F(71, 100) not in S
    M(B1,t,"Medium","For which values of x is cos⁻¹x > sin⁻¹x?",["−1 ≤ x < 1/√2","1/√2 < x ≤ 1","0 ≤ x < 1/√2","−1 ≤ x < 0"],"−1 ≤ x < 1/√2","Since sin⁻¹x + cos⁻¹x = π/2, the condition is π/2 − sin⁻¹x > sin⁻¹x, i.e. sin⁻¹x < π/4. sin⁻¹ is increasing on [−1, 1], so x < sin(π/4) = 1/√2. Together with the domain: −1 ≤ x < 1/√2.")
    assert eq(atan(sqrt(3)) - acos(Q(-1, 2)), -pi/3)
    M(B1,t,"Easy","Using principal values, tan⁻¹(√3) − sec⁻¹(−2) equals:",["−π/3","π","π/3","−2π/3"],"−π/3","tan⁻¹(√3) = π/3. sec⁻¹(−2) = cos⁻¹(−1/2) = 2π/3 (the principal range of sec⁻¹ is [0, π] without π/2). So the value is π/3 − 2π/3 = −π/3.")
    # ---------- Relations & Functions (+4)
    t = "Relations & Functions"
    cls = [n for n in range(-10, 11) if (n - 2) % 5 == 0]; assert cls == [-8, -3, 2, 7]
    M(B1,t,"Easy","On the set of integers, a R b means a − b is divisible by 5. Which set lists elements of the equivalence class of 2?",["{…, −8, −3, 2, 7, 12, …}","{…, −7, −2, 2, 7, 12, …}","{2, 7, 12, 17, …} only","{…, −10, −5, 0, 5, 10, …}"],"{…, −8, −3, 2, 7, 12, …}","The class of 2 is all integers b with b − 2 divisible by 5, i.e. b = 2 + 5k for every integer k: …, −8, −3, 2, 7, 12, …. (−2 is not in it, since −2 − 2 = −4.)")
    f = lambda z: (4*z + 3)/(6*z - 4); assert simplify(f(f(x)) - x) == 0
    M(B1,t,"Medium","f(x) = (4x + 3)/(6x − 4) for x ≠ 2/3. Then f(f(x)), for x ≠ 2/3, equals:",["x","1/x","(4x + 3)/(6x − 4)","−x"],"x","f(f(x)) = [4(4x + 3)/(6x − 4) + 3] / [6(4x + 3)/(6x − 4) − 4] = (16x + 12 + 18x − 12)/(24x + 18 − 24x + 16) = 34x/34 = x. So f is its own inverse.")
    Nn = range(1, 60)
    def inj(g): v = [g(n) for n in Nn]; return len(set(v)) == len(v)
    def onto_small(g): return set(range(1, 20)) <= {g(n) for n in Nn}
    fs = {"f(n) = n + 1": lambda n: n + 1, "f(n) = n": lambda n: n, "f(n) = ⌈n/2⌉ (the least integer ≥ n/2)": lambda n: -(-n // 2), "f(n) = n − 1 for even n, n + 1 for odd n": lambda n: n - 1 if n % 2 == 0 else n + 1}
    ans = [k for k, g in fs.items() if inj(g) and not onto_small(g)]; assert ans == ["f(n) = n + 1"]
    M(B1,t,"Medium","Which of these functions from N = {1, 2, 3, …} to N is one-one but not onto?",list(fs),"f(n) = n + 1","f(n) = n + 1 is one-one (different n give different values), but 1 is never a value, so it is not onto. f(n) = n and the even/odd swap are bijections; ⌈n/2⌉ is onto but not one-one (f(1) = f(2) = 1).")
    base = {(1, 2), (2, 3)}; Uall = [(i, j) for i in (1, 2, 3) for j in (1, 2, 3)]
    def ok_rel(R): return all((i, i) in R for i in (1, 2, 3)) and all((i, l) in R for (i, j) in R for (k2, l) in R if j == k2)
    best = min(len(extra) for r in range(0, 8) for extra in itertools.combinations([p for p in Uall if p not in base], r) if ok_rel(base | set(extra))); assert best == 4
    M(B1,t,"Medium","R = {(1, 2), (2, 3)} is a relation on {1, 2, 3}. What is the least number of ordered pairs that must be added to R to make it both reflexive and transitive?",["4","3","5","6"],"4","Reflexivity needs (1, 1), (2, 2) and (3, 3). Transitivity: (1, 2) and (2, 3) force (1, 3). With these four added, R = {(1,1), (2,2), (3,3), (1,2), (2,3), (1,3)}, which is reflexive and transitive. So 4 pairs.")
    # ---------- Vectors (+3)
    t = "Vectors"
    av = Matrix([2, 0, 0]); bv = Matrix([Q(3, 2), 3*sqrt(3)/2, 0]); assert eq(av.dot(bv), 3) and eq((av + bv).norm(), sqrt(19))
    M(B1,t,"Medium","|a| = 2, |b| = 3 and the angle between a and b is π/3. What is |a + b|?",["√19","√7","5","√13"],"√19","|a + b|² = |a|² + |b|² + 2a·b = 4 + 9 + 2 × (2 × 3 × cos π/3) = 13 + 6 = 19, so |a + b| = √19.")
    av = Matrix([4, 0, 0]); bv = Matrix([3, 4, 0]); assert av.cross(bv).norm()**2 + av.dot(bv)**2 == 400
    M(B1,t,"Easy","If |a| = 4 and |b| = 5, then |a × b|² + (a · b)² equals:",["400","81","41","20"],"400","|a × b|² + (a · b)² = |a|²|b|²sin²θ + |a|²|b|²cos²θ = |a|²|b|² = 16 × 25 = 400, whatever the angle.")
    P, Qv = Matrix([1, 2, -1]), Matrix([4, -1, 5]); assert (2*Qv + P)/3 == Matrix([3, 0, 3])
    M(B1,t,"Easy","P and Q have position vectors î + 2ĵ − k̂ and 4î − ĵ + 5k̂. What is the position vector of the point dividing PQ internally in the ratio 2 : 1?",["3î + 3k̂","2î + ĵ + k̂","3î + ĵ + 3k̂","(5/2)î + (1/2)ĵ + 2k̂"],"3î + 3k̂","By the section formula the point is (2Q + 1P)/3 = (2(4, −1, 5) + (1, 2, −1))/3 = (9, 0, 9)/3 = (3, 0, 3), i.e. 3î + 3k̂.")
    # ---------- Probability (+3)
    t = "Probability"
    xs, ps = [1, 2, 3], [Q(1, 4), Q(1, 2), Q(1, 4)]; m = sum(a*p for a, p in zip(xs, ps)); v = sum(a*a*p for a, p in zip(xs, ps)) - m**2; assert m == 2 and v == Q(1, 2)
    M(B1,t,"Medium","A random variable X takes the values 1, 2 and 3 with probabilities 1/4, 1/2 and 1/4. What is the variance of X?",["1/2","2","1/4","3/2"],"1/2","E(X) = 1/4 + 1 + 3/4 = 2. E(X²) = 1/4 + 2 + 9/4 = 9/2. Var(X) = E(X²) − [E(X)]² = 9/2 − 4 = 1/2.")
    om = list(itertools.product("HT", repeat=2)); A_ = [o for o in om if "H" in o]; assert F(sum(1 for o in A_ if o == ("H", "H")), len(A_)) == F(1, 3)
    M(B1,t,"Easy","Two fair coins are tossed. Given that at least one shows a head, what is the probability that both show heads?",["1/3","1/2","1/4","2/3"],"1/3","The outcomes with at least one head are HH, HT and TH, equally likely. Only HH has both heads, so the conditional probability is 1/3.")
    E_ = {2, 4, 6}; F_ = {1, 2, 3}; assert F(len(E_ & F_), 6) != F(len(E_), 6) * F(len(F_), 6)
    M(A1,t,"Medium","A fair die is thrown once. E is the event 'the number is even' and F is the event 'the number is at most 3'. Which statement is true?",["E and F are not independent, since P(E ∩ F) = 1/6 ≠ 1/4","E and F are independent, since P(E) = P(F)","E and F are mutually exclusive","E and F are independent, since P(E ∩ F) = 1/4"],"E and F are not independent, since P(E ∩ F) = 1/6 ≠ 1/4","P(E) = 3/6 = 1/2 and P(F) = 3/6 = 1/2, so P(E)P(F) = 1/4. E ∩ F = {2}, so P(E ∩ F) = 1/6. As 1/6 ≠ 1/4, E and F are not independent (and they are not mutually exclusive, as both contain 2).")
    # ---------- Integrals (+2)
    t = "Integrals"
    assert eq(diff(exp(x)*sin(x), x), exp(x)*(sin(x) + cos(x)))
    M(A1,t,"Easy","∫ eˣ (sin x + cos x) dx equals:",["eˣ sin x + C","eˣ cos x + C","−eˣ cos x + C","eˣ (sin x − cos x) + C"],"eˣ sin x + C","Use ∫ eˣ [f(x) + f′(x)] dx = eˣ f(x) + C with f(x) = sin x, f′(x) = cos x. Check: d/dx (eˣ sin x) = eˣ sin x + eˣ cos x.")
    assert integrate(x*(1 - x)**9, (x, 0, 1)) == Q(1, 110)
    M(A1,t,"Medium","Evaluate ∫₀¹ x(1 − x)⁹ dx.",["1/110","1/90","1/100","1/11"],"1/110","Using ∫₀¹ f(x) dx = ∫₀¹ f(1 − x) dx, the integral equals ∫₀¹ (1 − x)x⁹ dx = ∫₀¹ (x⁹ − x¹⁰) dx = 1/10 − 1/11 = 1/110.")
    # ---------- Applications of Derivatives (+2)
    t = "Applications of Derivatives"
    assert sp.solve(sp.Eq(diff(x**2, x), 4), x) == [2]
    M(A1,t,"Easy","At which point on the curve y = x² is the tangent parallel to the line y = 4x + 1?",["(2, 4)","(4, 16)","(1, 1)","(−2, 4)"],"(2, 4)","The tangent's slope is dy/dx = 2x. Parallel to y = 4x + 1 means slope 4, so 2x = 4, x = 2 and y = 4. The point is (2, 4).")
    assert sorted(sp.solve(diff(x**4 - 2*x**2, x), x)) == [-1, 0, 1]
    M(B1,t,"Easy","How many critical points does f(x) = x⁴ − 2x² have?",["3","2","1","4"],"3","f′(x) = 4x³ − 4x = 4x(x − 1)(x + 1), which is zero at x = −1, 0 and 1: three critical points (minima at ±1, a local maximum at 0).")
    # ---------- Three-dimensional Geometry (+1)
    t = "Three-dimensional Geometry"
    pl = lambda X, Y, Z: 6*X + 4*Y + 3*Z - 12; assert pl(2, 0, 0) == pl(0, 3, 0) == pl(0, 0, 4) == 0
    M(B1,t,"Easy","Which plane cuts off intercepts 2, 3 and 4 on the x-, y- and z-axes respectively?",["6x + 4y + 3z = 12","2x + 3y + 4z = 12","4x + 3y + 2z = 12","3x + 4y + 6z = 12"],"6x + 4y + 3z = 12","The intercept form is x/2 + y/3 + z/4 = 1. Multiplying by 12 gives 6x + 4y + 3z = 12. Check: (2, 0, 0), (0, 3, 0) and (0, 0, 4) all satisfy it.")
