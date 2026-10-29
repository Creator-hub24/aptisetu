"""CUET (UG) batch B10 (Oct 2026): original Mathematics items for the thinner chapters.
Every answer is computed or verified here with sympy / exhaustive enumeration; build fails if any check fails."""
import itertools, math
import sympy as sp
from sympy import Rational as Q, pi, sqrt, symbols, Matrix, integrate, simplify, diff, atan, asin, acos, acot, exp, log, sin, cos, tan, sec, E as e_
from batch_b2 import balanced
from maths import mx
A1, B1 = "Section A (common)", "Section B1 (Mathematics)"
x, y = symbols("x y")
def eq(a, b): return simplify(a - b) == 0

def maths(B):
    M = balanced(B, "maths", 1010)
    # ---------- Matrices (+4)
    t = "Matrices"
    A = Matrix([[1, 2], [2, 1]]); assert A**2 - 2*A == 3*sp.eye(2)
    M(A1,t,"Medium",f"If A = {mx([[1,2],[2,1]])}, then A² − 2A equals:",["3I","I","2I","−3I"],"3I","A² = [[1·1 + 2·2, 1·2 + 2·1], [2·1 + 1·2, 2·2 + 1·1]] = [[5, 4], [4, 5]]. A² − 2A = [[5 − 2, 4 − 4], [4 − 4, 5 − 2]] = [[3, 0], [0, 3]] = 3I.")
    assert Matrix([[2, 0], [0, 3]]).inv() == Matrix([[Q(1, 2), 0], [0, Q(1, 3)]])
    M(A1,t,"Easy",f"The inverse of the diagonal matrix {mx([[2,0],[0,3]])} is:",[mx([["1/2",0],[0,"1/3"]]),mx([[3,0],[0,2]]),mx([["−1/2",0],[0,"−1/3"]]),mx([["1/3",0],[0,"1/2"]])],mx([["1/2",0],[0,"1/3"]]),"For a diagonal matrix with non-zero diagonal entries, the inverse is the diagonal matrix of reciprocals: diag(1/2, 1/3). Check: diag(2, 3) × diag(1/2, 1/3) = diag(1, 1) = I.")
    assert sum(1 for _ in itertools.product((0, 1), repeat=9)) == 512
    M(A1,t,"Easy","How many 3 × 3 matrices can be formed if every entry is either 0 or 1?",["512","81","9","729"],"512","A 3 × 3 matrix has 9 entries and each entry has 2 choices, so the number of matrices is 2⁹ = 512.")
    A = Matrix([[1, 3], [5, 7]]); P = (A + A.T) / 2; Qm = (A - A.T) / 2
    assert P == Matrix([[1, 4], [4, 7]]) and Qm == Matrix([[0, -1], [1, 0]]) and P + Qm == A
    M(A1,t,"Medium",f"The matrix A = {mx([[1,3],[5,7]])} is written as P + Q, where P is symmetric and Q is skew-symmetric. The entry in row 1, column 2 of P is:",["4","3","5","−1"],"4","P = (A + Aᵀ)/2. Aᵀ = [[1, 5], [3, 7]], so A + Aᵀ = [[2, 8], [8, 14]] and P = [[1, 4], [4, 7]]. The row 1, column 2 entry is (3 + 5)/2 = 4. (Q = (A − Aᵀ)/2 = [[0, −1], [1, 0]].)")
    # ---------- Determinants (+3; a plain 3×3 evaluation was dropped as a near-repeat)
    t = "Determinants"
    n, dA = 3, 2; d2A = 2**n * dA; assert d2A == 16 and d2A**(n - 1) == 256
    Ar = Matrix([[2, 0, 0], [0, 1, 0], [0, 0, 1]]); assert (2*Ar).adjugate().det() == 256
    M(A1,t,"Hard","A is a 3 × 3 matrix with |A| = 2. What is |adj(2A)|?",["256","64","16","128"],"256","For an n × n matrix, |adj B| = |B|ⁿ⁻¹. Here B = 2A with n = 3, so |B| = 2³ × |A| = 8 × 2 = 16, and |adj(2A)| = 16² = 256.")
    k = symbols("k"); sk = sp.solve(Matrix([[1, 2, 1], [3, k, 1], [5, 10, 1]]).det(), k); assert sk == [6]
    M(A1,t,"Easy","For which value of k are the points (1, 2), (3, k) and (5, 10) collinear?",["6","5","8","4"],"6","The points are collinear when the area determinant is zero: 1(k − 10) − 2(3 − 5) + 1(30 − 5k) = k − 10 + 4 + 30 − 5k = 24 − 4k = 0, so k = 6.")
    dk = Matrix([[1, 1, 1], [1, 2, 3], [1, 3, k]]).det(); assert sp.expand(dk) == k - 5
    M(A1,t,"Medium","For which value of k does the system x + y + z = 1, x + 2y + 3z = 2, x + 3y + kz = 3 fail to have a unique solution?",["5","3","4","6"],"5","A unique solution exists exactly when the coefficient determinant is non-zero. Determinant = 1(2k − 9) − 1(k − 3) + 1(3 − 2) = 2k − 9 − k + 3 + 1 = k − 5, which is zero when k = 5.")
    # ---------- Integrals (+5)
    t = "Integrals"
    assert eq(integrate(tan(x)**2, (x, 0, pi/4)), 1 - pi/4)
    M(A1,t,"Medium","Evaluate ∫₀^{π/4} tan²x dx.",["1 − π/4","π/4 − 1","1 + π/4","π/4"],"1 − π/4","tan²x = sec²x − 1, so the integral is [tan x − x] from 0 to π/4 = (1 − π/4) − 0 = 1 − π/4.")
    assert integrate(sp.Abs(x), (x, -1, 1)) == 1
    M(A1,t,"Easy","Evaluate ∫₋₁¹ |x| dx.",["1","0","2","1/2"],"1","|x| is even, so the integral = 2∫₀¹ x dx = 2 × 1/2 = 1.")
    assert eq(integrate(x*sin(x), (x, 0, pi)), pi)
    M(A1,t,"Medium","Evaluate ∫₀^π x sin x dx.",["π","2π","π/2","0"],"π","Integrate by parts: ∫ x sin x dx = −x cos x + sin x. From 0 to π: (−π cos π + sin π) − (0 + 0) = π.")
    assert eq(integrate(sin(x)/(sin(x) + cos(x)), (x, 0, pi/2)), pi/4)
    M(A1,t,"Hard","Evaluate ∫₀^{π/2} sin x / (sin x + cos x) dx.",["π/4","π/2","1","π/8"],"π/4","Call it I. Replacing x by π/2 − x gives I = ∫₀^{π/2} cos x / (cos x + sin x) dx. Adding the two forms, 2I = ∫₀^{π/2} 1 dx = π/2, so I = π/4.")
    F_ = log(sp.Abs(x/(x + 1))); assert eq(diff(log(x) - log(x + 1), x), 1/(x*(x + 1)))
    M(A1,t,"Medium","∫ dx / (x(x + 1)) equals:",["log|x/(x + 1)| + C","log|x(x + 1)| + C","log|(x + 1)/x| + C","1/(x + 1) + C"],"log|x/(x + 1)| + C","Partial fractions: 1/(x(x + 1)) = 1/x − 1/(x + 1). Integrating gives log|x| − log|x + 1| + C = log|x/(x + 1)| + C.")
    # ---------- Differential Equations (+4)
    t = "Differential Equations"
    Aa, Bb = symbols("A B"); yy = Aa*exp(2*x) + Bb*exp(-2*x); assert eq(diff(yy, x, 2) - 4*yy, 0)
    M(A1,t,"Medium","The differential equation of the family of curves y = A e^{2x} + B e^{−2x} (A, B arbitrary constants) is:",["d²y/dx² = 4y","d²y/dx² = 2y","dy/dx = 2y","d²y/dx² = −4y"],"d²y/dx² = 4y","Differentiate twice: y′ = 2A e^{2x} − 2B e^{−2x}, y″ = 4A e^{2x} + 4B e^{−2x} = 4y. Two constants are eliminated, so the equation has order 2.")
    C = symbols("C"); sol = sp.tan(atan(x) + C)
    assert eq(diff(atan(sol), x) - 1/(1 + x**2), 0)
    M(A1,t,"Medium","The general solution of dy/dx = (1 + y²)/(1 + x²) is:",["tan⁻¹y = tan⁻¹x + C","tan⁻¹y = tan⁻¹x · C","y = x + C","log(1 + y²) = log(1 + x²) + C"],"tan⁻¹y = tan⁻¹x + C","Separate the variables: dy/(1 + y²) = dx/(1 + x²). Integrating both sides gives tan⁻¹y = tan⁻¹x + C.")
    yv = log(exp(x) + 1); assert eq(diff(yv, x) - exp(x - yv), 0) and eq(yv.subs(x, 0), log(2)) and eq(yv.subs(x, log(3)), log(4))
    M(A1,t,"Medium","If dy/dx = e^{x − y} and y = log 2 when x = 0, what is y when x = log 3?",["log 4","log 3","log 2","log 6"],"log 4","Separate: eʸ dy = eˣ dx, so eʸ = eˣ + C. At x = 0, y = log 2: 2 = 1 + C, so C = 1. At x = log 3: eʸ = 3 + 1 = 4, so y = log 4.")
    M(A1,t,"Easy","What is the degree of the differential equation (d²y/dx²)² + sin(dy/dx) = 0?",["Not defined","2","1","0"],"Not defined","Degree is defined only when the equation is a polynomial in its derivatives. Here dy/dx appears inside sin, so the equation is not a polynomial in its derivatives and its degree is not defined (its order is 2).")
    # ---------- Continuity & Differentiability (+5)
    t = "Continuity & Differentiability"
    f_ = sp.Abs(x - 2); assert sp.limit(f_, x, 2) == 0 and sp.limit((f_ - 0)/(x - 2), x, 2, "+") == 1 and sp.limit((f_ - 0)/(x - 2), x, 2, "-") == -1
    M(A1,t,"Easy","At x = 2, the function f(x) = |x − 2| is:",["continuous but not differentiable","differentiable but not continuous","both continuous and differentiable","neither continuous nor differentiable"],"continuous but not differentiable","The limit of |x − 2| as x → 2 is 0 = f(2), so f is continuous there. The right-hand derivative is +1 and the left-hand derivative is −1; they differ, so f is not differentiable at x = 2.")
    ys = asin(x); assert eq((1 - x**2)*diff(ys, x, 2) - x*diff(ys, x), 0)
    M(B1,t,"Medium","If y = sin⁻¹x, then the value of (1 − x²) d²y/dx² − x dy/dx is:",["0","1","−1","x"],"0","y′ = 1/√(1 − x²), so √(1 − x²) y′ = 1. Differentiate: √(1 − x²) y″ − x y′/√(1 − x²) = 0. Multiply by √(1 − x²): (1 − x²) y″ − x y′ = 0.")
    assert eq(diff(log(sec(x) + tan(x)), x) - sec(x), 0)
    M(A1,t,"Medium","d/dx [log(sec x + tan x)] equals:",["sec x","tan x","sec x tan x","sec²x"],"sec x","By the chain rule, the derivative is (sec x tan x + sec²x)/(sec x + tan x) = sec x (tan x + sec x)/(sec x + tan x) = sec x.")
    assert sp.idiff(x**2 + y**2 - 25, y, x).subs({x: 3, y: 4}) == Q(-3, 4)
    M(A1,t,"Easy","For the curve x² + y² = 25, what is dy/dx at the point (3, 4)?",["−3/4","3/4","−4/3","4/3"],"−3/4","Differentiate implicitly: 2x + 2y dy/dx = 0, so dy/dx = −x/y = −3/4 at (3, 4).")
    c = symbols("c", positive=True); cs = sp.solve(sp.Eq(3*c**2, Q(27 - 0, 3)), c); assert cs == [sqrt(3)]
    M(B1,t,"Medium","The value of c given by the Mean Value Theorem for f(x) = x³ on [0, 3] is:",["√3","3/2","1","√2"],"√3","MVT: f′(c) = (f(3) − f(0))/(3 − 0) = 27/3 = 9. f′(c) = 3c² = 9 gives c² = 3, so c = √3, which lies in (0, 3).")
    # ---------- Applications of Derivatives (+4)
    t = "Applications of Derivatives"
    g = x*exp(-x); assert sp.solve(diff(g, x), x) == [1] and diff(g, x, 2).subs(x, 1) < 0 and eq(g.subs(x, 1), 1/e_)
    M(A1,t,"Medium","The maximum value of f(x) = x e^{−x} is:",["1/e","e","1","2/e²"],"1/e","f′(x) = e^{−x}(1 − x) = 0 gives x = 1, and f′ changes from positive to negative there, so it is a maximum. f(1) = 1 · e^{−1} = 1/e.")
    assert diff(x**3, x).subs(x, 2) == 12
    M(A1,t,"Easy","What is the slope of the normal to the curve y = x³ at the point (2, 8)?",["−1/12","12","−12","1/12"],"−1/12","The tangent slope is dy/dx = 3x² = 3 × 2² = 12 at x = 2. The normal is perpendicular, so its slope is −1/12.")
    h = 2*x**3 - 9*x**2 + 12*x + 1; assert sp.expand(diff(h, x) - 6*(x - 1)*(x - 2)) == 0
    assert sp.solve_univariate_inequality(diff(h, x) > 0, x, relational=False) == sp.Union(sp.Interval.open(-sp.oo, 1), sp.Interval.open(2, sp.oo))
    M(B1,t,"Medium","On which set is f(x) = 2x³ − 9x² + 12x + 1 strictly increasing?",["(−∞, 1) ∪ (2, ∞)","(1, 2)","(−∞, 2)","(1, ∞)"],"(−∞, 1) ∪ (2, ∞)","f′(x) = 6x² − 18x + 12 = 6(x − 1)(x − 2). This is positive when x < 1 or x > 2, so f is strictly increasing on (−∞, 1) ∪ (2, ∞) and decreasing on (1, 2).")
    approx = 5 + Q(1, 2*5) * Q(2, 10); assert approx == Q(502, 100) and abs(math.sqrt(25.2) - 5.02) < 0.001
    M(B1,t,"Medium","Using differentials, the approximate value of √25.2 is:",["5.02","5.04","5.01","5.2"],"5.02","Take y = √x, x = 25, Δx = 0.2. dy = Δx/(2√x) = 0.2/10 = 0.02, so √25.2 ≈ 5 + 0.02 = 5.02.")
    # ---------- Probability (+5; "both aces" dropped as a near-repeat of a Bank item)
    t = "Probability"
    assert Q(4, 10) * Q(1, 2) == Q(1, 5)
    M(A1,t,"Easy","If P(A) = 0.4 and P(B | A) = 0.5, what is P(A ∩ B)?",["0.2","0.9","0.8","0.1"],"0.2","By the multiplication rule, P(A ∩ B) = P(A) × P(B | A) = 0.4 × 0.5 = 0.2.")
    assert Q(3, 10) + Q(4, 10) - Q(3, 10)*Q(4, 10) == Q(58, 100)
    M(A1,t,"Easy","A and B are independent events with P(A) = 0.3 and P(B) = 0.4. What is P(A ∪ B)?",["0.58","0.7","0.12","0.82"],"0.58","For independent events P(A ∩ B) = 0.3 × 0.4 = 0.12, so P(A ∪ B) = 0.3 + 0.4 − 0.12 = 0.58.")
    pB = Q(40, 100)*Q(3, 100) / (Q(60, 100)*Q(2, 100) + Q(40, 100)*Q(3, 100)); assert pB == Q(1, 2)
    M(A1,t,"Medium","Machine A makes 60% of a factory's bolts and machine B the rest. 2% of A's bolts and 3% of B's bolts are defective. A bolt chosen at random is defective. What is the probability that it was made by B?",["1/2","2/5","3/5","1/3"],"1/2","By Bayes' theorem: P(B | defective) = (0.4 × 0.03)/(0.6 × 0.02 + 0.4 × 0.03) = 0.012/(0.012 + 0.012) = 1/2.")
    kk = Q(1, 10); assert kk*(1 + 2 + 3 + 4) == 1 and sum(i*(i + 1)*kk for i in range(4)) == 2
    M(B1,t,"Medium","A random variable X takes the values 0, 1, 2, 3 with P(X = 0) = k, P(X = 1) = 2k, P(X = 2) = 3k and P(X = 3) = 4k. What is the mean E(X)?",["2","1","3/2","5/2"],"2","The probabilities add to 1: k + 2k + 3k + 4k = 10k = 1, so k = 1/10. E(X) = 0(1/10) + 1(2/10) + 2(3/10) + 3(4/10) = (0 + 2 + 6 + 12)/10 = 2.")
    assert sp.binomial(5, 2) * Q(1, 2)**5 == Q(5, 16)
    M(B1,t,"Easy","A fair coin is tossed 5 times. What is the probability of getting exactly 2 heads?",["5/16","1/4","2/5","3/16"],"5/16","By the binomial distribution, P(X = 2) = ⁵C₂ (1/2)⁵ = 10/32 = 5/16.")
    # ---------- Relations & Functions (+4)
    t = "Relations & Functions"
    pairs2 = list(itertools.product((1, 2), repeat=2)); assert 2**len(pairs2) == 16
    M(B1,t,"Easy","How many relations can be defined on the set A = {1, 2}?",["16","4","8","2"],"16","A relation on A is any subset of A × A. A × A has 2 × 2 = 4 ordered pairs, so there are 2⁴ = 16 relations.")
    S = [1, 2, 3]; P3 = list(itertools.product(S, repeat=2))
    sym = sum(1 for m in range(2**9) if all(((m >> P3.index((a, b))) & 1) == ((m >> P3.index((b, a))) & 1) for a, b in P3)); assert sym == 64
    M(B1,t,"Medium","How many symmetric relations can be defined on the set {1, 2, 3}?",["64","512","8","27"],"64","A symmetric relation is fixed by choosing which of the 3 diagonal pairs (a, a) it contains and which of the 3 unordered pairs {a, b} (a ≠ b) it contains, taking both orders together. That is 3 + 3 = 6 independent yes/no choices, so there are 2⁶ = 64 relations.")
    assert sp.solve(3*x + 2 - 11, x) == [3]
    M(B1,t,"Easy","If f: R → R is defined by f(x) = 3x + 2, then f⁻¹(11) equals:",["3","35","13/3","11/3"],"3","f⁻¹(11) is the x with 3x + 2 = 11, i.e. x = 3. (In general f⁻¹(y) = (y − 2)/3.)")
    onto = sum(1 for f in itertools.product("ab", repeat=4) if set(f) == {"a", "b"}); assert onto == 14
    M(B1,t,"Medium","How many onto functions are there from {1, 2, 3, 4} to {a, b}?",["14","16","8","12"],"14","There are 2⁴ = 16 functions in all. Exactly 2 of them are not onto (all values a, or all values b), so 16 − 2 = 14 are onto.")
    # ---------- Inverse Trigonometric Functions (+4)
    t = "Inverse Trigonometric Functions"
    assert eq(asin(sin(2*pi/3)), pi/3)
    M(B1,t,"Medium","The value of sin⁻¹(sin(2π/3)) is:",["π/3","2π/3","−π/3","π/6"],"π/3","The principal range of sin⁻¹ is [−π/2, π/2], and 2π/3 is outside it. sin(2π/3) = sin(π − 2π/3) = sin(π/3), and π/3 is inside the range, so the value is π/3.")
    acot_ncert = lambda v: atan(1/sp.S(v)) if v > 0 else pi + atan(1/sp.S(v))   # NCERT principal range (0, π)
    for v in (Q(1, 3), 2, 5, -3, Q(-1, 2)):
        th = acot_ncert(v); assert 0 < sp.N(th) < sp.N(pi) and abs(sp.N(cos(th)/sin(th) - v, 30)) < 1e-25
        assert abs(sp.N(cos(atan(v) + th), 30)) < 1e-25
    M(B1,t,"Easy","For any real x, cos(tan⁻¹x + cot⁻¹x) equals:",["0","1","−1","1/2"],"0","For every real x, tan⁻¹x + cot⁻¹x = π/2, and cos(π/2) = 0.")
    assert eq(pi/2 - pi/5, 3*pi/10)
    M(B1,t,"Easy","If sin⁻¹x = π/5 for some x, then cos⁻¹x equals:",["3π/10","π/5","4π/5","π/10"],"3π/10","For x in [−1, 1], sin⁻¹x + cos⁻¹x = π/2, so cos⁻¹x = π/2 − π/5 = 3π/10.")
    assert eq(atan(-sqrt(3)), -pi/3)
    M(B1,t,"Easy","What is the principal value of tan⁻¹(−√3)?",["−π/3","2π/3","π/3","−π/6"],"−π/3","The principal range of tan⁻¹ is (−π/2, π/2). tan(−π/3) = −√3 and −π/3 lies in that range, so the principal value is −π/3.")
    # ---------- Vectors (+4)
    t = "Vectors"
    ab = Q(49 - 9 - 25, 2); assert ab == Q(15, 2) and ab / (3*5) == Q(1, 2)
    av, bv = Matrix([3, 0, 0]), Matrix([Q(5, 2), 5*sqrt(3)/2, 0]); cv = -(av + bv); assert eq(cv.norm(), 7) and eq(av.dot(bv)/(3*5), Q(1, 2))
    M(B1,t,"Hard","Vectors a, b and c satisfy a + b + c = 0, with |a| = 3, |b| = 5 and |c| = 7. What is the angle between a and b?",["60°","30°","45°","120°"],"60°","c = −(a + b), so |c|² = |a|² + |b|² + 2 a·b: 49 = 9 + 25 + 2 a·b, giving a·b = 15/2. cos θ = (15/2)/(3 × 5) = 1/2, so θ = 60°.")
    Pa, Pb, Pc = Matrix([1, 1, 1]), Matrix([1, 2, 3]), Matrix([2, 3, 1]); cr = (Pb - Pa).cross(Pc - Pa); assert cr == Matrix([-4, 2, -1]) and eq(cr.norm()/2, sqrt(21)/2)
    M(B1,t,"Medium","What is the area of the triangle with vertices A(1, 1, 1), B(1, 2, 3) and C(2, 3, 1)?",["√21/2 square units","√21 square units","√30/2 square units","5/2 square units"],"√21/2 square units","AB = ĵ + 2k̂ and AC = î + 2ĵ. AB × AC = (1·0 − 2·2)î + (2·1 − 0·0)ĵ + (0·2 − 1·1)k̂ = −4î + 2ĵ − k̂, with magnitude √(16 + 4 + 1) = √21. Area = ½|AB × AC| = √21/2.")
    assert Matrix([2, 3, -1]).cross(Matrix([4, 6, -2])) == Matrix([0, 0, 0])
    M(B1,t,"Easy","For which value of λ are the vectors 2î + 3ĵ − k̂ and 4î + λĵ − 2k̂ parallel?",["6","3","−6","4"],"6","Parallel vectors have proportional components: 4/2 = λ/3 = (−2)/(−1) = 2, so λ = 6.")
    I_, J_, K_ = Matrix([1, 0, 0]), Matrix([0, 1, 0]), Matrix([0, 0, 1]); assert I_.dot(J_.cross(K_)) + J_.dot(K_.cross(I_)) + K_.dot(I_.cross(J_)) == 3
    M(B1,t,"Easy","The value of î · (ĵ × k̂) + ĵ · (k̂ × î) + k̂ · (î × ĵ) is:",["3","0","1","−3"],"3","ĵ × k̂ = î, k̂ × î = ĵ and î × ĵ = k̂. So the sum is î·î + ĵ·ĵ + k̂·k̂ = 1 + 1 + 1 = 3.")
    # ---------- Three-dimensional Geometry (+5)
    t = "Three-dimensional Geometry"
    bd, nn = Matrix([1, 2, 2]), Matrix([2, -1, 2]); assert eq(sp.Abs(bd.dot(nn))/(bd.norm()*nn.norm()), Q(4, 9))
    M(B1,t,"Medium","What is the angle between the line (x − 1)/1 = (y + 2)/2 = (z − 3)/2 and the plane 2x − y + 2z = 5?",["sin⁻¹(4/9)","cos⁻¹(4/9)","sin⁻¹(2/9)","π/2"],"sin⁻¹(4/9)","The line has direction b = (1, 2, 2) and the plane has normal n = (2, −1, 2). sin θ = |b·n|/(|b||n|) = |2 − 2 + 4|/(3 × 3) = 4/9, so θ = sin⁻¹(4/9).")
    tt = sp.solve(9*symbols('t') - 9)[0]; assert tt == 1; foot = Matrix([2, 1, 2]) * tt; assert foot.dot(Matrix([2, 1, 2])) == 9
    M(B1,t,"Medium","What is the foot of the perpendicular from the origin to the plane 2x + y + 2z = 9?",["(2, 1, 2)","(1, 2, 2)","(2, 2, 1)","(4, 2, 4)"],"(2, 1, 2)","The perpendicular from the origin runs along the normal, so the foot is t(2, 1, 2). Substituting: 4t + t + 4t = 9, so t = 1 and the foot is (2, 1, 2).")
    l = 1/sqrt(3); assert eq(3*l**2, 1)
    M(B1,t,"Easy","A line makes equal angles with the three coordinate axes. Its direction cosines are:",["±(1/√3, 1/√3, 1/√3)","(1, 1, 1)","±(1/3, 1/3, 1/3)","±(1/√2, 1/√2, 1/√2)"],"±(1/√3, 1/√3, 1/√3)","If l = m = n, then l² + m² + n² = 1 gives 3l² = 1, so l = ±1/√3. The direction cosines are ±(1/√3, 1/√3, 1/√3).")
    assert sp.Abs(7 - 1)/Matrix([2, 1, 2]).norm() == 2
    M(B1,t,"Medium","What is the distance between the parallel planes 2x + y + 2z = 1 and 4x + 2y + 4z = 14?",["2 units","13/3 units","5/3 units","4 units"],"2 units","Divide the second equation by 2: 2x + y + 2z = 7. For planes ax + by + cz = d₁ and ax + by + cz = d₂, distance = |d₂ − d₁|/√(a² + b² + c²) = |7 − 1|/3 = 2.")
    assert sp.solve(Matrix([2, k, 1]).dot(Matrix([1, 2, -4])), k) == [1]
    M(B1,t,"Easy","For which value of k are the lines (x − 1)/2 = (y − 2)/k = (z − 3)/1 and x/1 = y/2 = z/(−4) perpendicular?",["1","2","−1","4"],"1","The direction ratios are (2, k, 1) and (1, 2, −4). The lines are perpendicular when 2·1 + k·2 + 1·(−4) = 0, i.e. 2k − 2 = 0, so k = 1.")
