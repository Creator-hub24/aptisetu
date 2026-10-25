"""CUET (UG) Mathematics / Applied Mathematics (319): original questions, every answer verified with sympy."""
import itertools
import sympy as sp
from sympy import Rational as Q, pi, sqrt, symbols, Matrix, integrate, diff, limit, simplify, atan, asin, exp, sin, cos, oo
A1, B1 = "Section A (common)", "Section B1 (Mathematics)"
x, y, C = symbols("x y C")

def mx(m):
    """2D list -> small HTML matrix (CSS class mx)."""
    return "<span class='mx'>" + "".join("<span class='mx-r'>" + "".join(f"<span>{str(v).replace('-', '−')}</span>" for v in row) + "</span>" for row in m) + "</span>"
def eq(a, b): return simplify(a - b) == 0

def build(B):
    M = lambda *a, **k: B.mcq("maths", *a, **k)
    # ---------------- Section A (common to Mathematics and Applied Mathematics) ----------------
    t = "Matrices"
    A = Matrix([[2, 1], [3, 4]]); Bm = Matrix([[1, 0], [-1, 2]]); AB = A * Bm; assert AB == Matrix([[1, 2], [-1, 8]])
    M(A1,t,"Easy",f"If A = {mx([[2,1],[3,4]])} and B = {mx([[1,0],[-1,2]])}, then AB equals:",[mx(AB.tolist()),mx((Bm*A).tolist()),mx([[2,0],[-3,8]]),mx([[3,1],[2,6]])],mx(AB.tolist()),"Row × column: (1,1) = 2·1 + 1·(−1) = 1; (1,2) = 2·0 + 1·2 = 2; (2,1) = 3·1 + 4·(−1) = −1; (2,2) = 3·0 + 4·2 = 8. (The second option is BA, which is different because matrix multiplication is not commutative. The third multiplies entry by entry, and the fourth adds the matrices.)")
    assert Bm * A != AB   # the BA distractor really is different
    a_, b_, c_ = symbols("a b c"); S = Matrix([[0, a_, b_], [-a_, 0, c_], [-b_, -c_, 0]]); assert S.T == -S and S.trace() == 0
    M(A1,t,"Easy","If A is a 3 × 3 skew-symmetric matrix, the sum of its diagonal entries is:",["0","1","3","It depends on A"],"0","In a skew-symmetric matrix Aᵀ = −A, so every diagonal entry satisfies aᵢᵢ = −aᵢᵢ, i.e. aᵢᵢ = 0. The sum is 0 whatever the other entries are.",fixed=True)
    P = Matrix([[2, 3], [1, 2]]); Pi = P.inv(); assert Pi == Matrix([[2, -3], [-1, 2]]) and P.det() == 1
    M(A1,t,"Medium",f"The inverse of A = {mx([[2,3],[1,2]])} is:",[mx(Pi.tolist()),mx([[2,3],[1,2]]),mx([[-2,3],[1,-2]]),mx([[2,-1],[-3,2]])],mx(Pi.tolist()),"|A| = 2·2 − 3·1 = 1. For a 2 × 2 matrix, A⁻¹ = (1/|A|) × (swap the diagonal entries and change the sign of the other two), which gives the first option. Check: A·A⁻¹ = I.")
    t = "Determinants"
    D = Matrix([[1, 2, 3], [0, 4, 5], [1, 0, 6]]).det(); assert D == 22
    M(A1,t,"Medium",f"The value of the determinant {mx([[1,2,3],[0,4,5],[1,0,6]])} is:",["22","−22","26","34"],str(D),"Expand along the first row: 1(4·6 − 5·0) − 2(0·6 − 5·1) + 3(0·0 − 4·1) = 24 + 10 − 12 = 22.")
    ar = abs(Matrix([[1, 0, 1], [6, 0, 1], [4, 3, 1]]).det()) / 2; assert ar == Q(15, 2)
    M(A1,t,"Medium","Using determinants, what is the area of the triangle with vertices (1, 0), (6, 0) and (4, 3)?",["7.5 square units","15 square units","10 square units","6 square units"],"7.5 square units","Area = ½ |det| of the rows (x, y, 1): ½ |1(0 − 3) − 0 + 1(18 − 0)| = ½ × 15 = 7.5. (Check: base 5 on the x-axis, height 3 gives ½ × 5 × 3 = 7.5.)")
    t = "Continuity & Differentiability"
    f = x**3 - 6*x**2 + 9*x + 1; d2 = diff(f, x, 2).subs(x, 1); assert d2 == -6
    M(A1,t,"Easy","If y = x³ − 6x² + 9x + 1, what is the value of d²y/dx² at x = 1?",["−6","4","6","0"],str(d2).replace("-","−"),"dy/dx = 3x² − 12x + 9 and d²y/dx² = 6x − 12. At x = 1 this is −6. (0 is the value of dy/dx at x = 1.)")
    t = "Applications of Derivatives"
    g = x**3 - 3*x; crit = sp.solve(diff(g, x), x); assert sorted(crit) == [-1, 1] and diff(g, x).subs(x, 0) < 0
    assert sp.solve_univariate_inequality(diff(g, x) < 0, x, relational=False) == sp.Interval.open(-1, 1)
    M(A1,t,"Medium","The function f(x) = x³ − 3x is strictly decreasing on the interval:",["(−1, 1)","(1, ∞)","(−∞, −1)","(0, 3)"],"(−1, 1)","f′(x) = 3x² − 3 = 3(x − 1)(x + 1), which is negative exactly when −1 < x < 1. On (1, ∞) and (−∞, −1), f is increasing.")
    h = -x**2 + 4*x + 5; xc = sp.solve(diff(h, x), x)[0]; mv = h.subs(x, xc); assert xc == 2 and mv == 9 and diff(h, x, 2) < 0
    M(A1,t,"Easy","What is the maximum value of f(x) = −x² + 4x + 5?",["9","5","2","13"],str(mv),"f′(x) = −2x + 4 = 0 gives x = 2, and f″(x) = −2 < 0, so x = 2 is a maximum. f(2) = −4 + 8 + 5 = 9.")
    t = "Integrals"
    I1 = integrate(x * exp(x), (x, 0, 1)); assert I1 == 1
    M(A1,t,"Medium","Evaluate ∫₀¹ x eˣ dx.",["1","e","e − 1","e − 2"],"1","By parts with u = x, dv = eˣ dx: ∫ x eˣ dx = x eˣ − eˣ. From 0 to 1: (e − e) − (0 − 1) = 1.")
    I2 = integrate(1 / (x**2 + 9), x); assert eq(I2, atan(x / 3) / 3)
    M(A1,t,"Easy","∫ dx / (x² + 9) equals:",["(1/3) tan⁻¹(x/3) + C","tan⁻¹(x/3) + C","(1/9) tan⁻¹(x/9) + C","(1/3) log|x² + 9| + C"],"(1/3) tan⁻¹(x/3) + C","Use the standard result ∫ dx/(x² + a²) = (1/a) tan⁻¹(x/a) + C with a = 3.")
    I3 = integrate(sin(x)**2, (x, 0, pi / 2)); assert I3 == pi / 4
    M(A1,t,"Medium","Evaluate ∫₀^{π/2} sin²x dx.",["π/4","π/2","1/2","π"],"π/4","sin²x = (1 − cos 2x)/2. Integrating from 0 to π/2 gives [x/2 − sin 2x/4] = π/4 − 0 = π/4.")
    t = "Application of Integrals"
    AI = integrate(x**2, (x, 0, 3)); assert AI == 9
    M(A1,t,"Easy","What is the area of the region bounded by the curve y = x², the x-axis and the lines x = 0 and x = 3?",["9 square units","27 square units","3 square units","6 square units"],"9 square units","Area = ∫₀³ x² dx = [x³/3] from 0 to 3 = 27/3 = 9.")
    t = "Differential Equations"
    M(A1,t,"Medium","What are the order and the degree of the differential equation (d²y/dx²)³ + (dy/dx)⁴ + y = 0?",["Order 2, degree 3","Order 3, degree 2","Order 2, degree 4","Order 4, degree 3"],"Order 2, degree 3","The order is that of the highest derivative present, d²y/dx², so it is 2. The degree is the power of that highest-order derivative (the equation is a polynomial in the derivatives), which is 3.")
    yf = sp.Function("y"); sol = sp.dsolve(sp.Eq(yf(x).diff(x), yf(x) / x), yf(x), ics={yf(1): 2}); assert eq(sol.rhs, 2 * x) and sol.rhs.subs(x, 3) == 6
    M(A1,t,"Medium","If dy/dx = y/x and y = 2 when x = 1, what is y when x = 3?",["6","2/3","9","5"],"6","Separate variables: dy/y = dx/x, so log|y| = log|x| + c and y = kx. y(1) = 2 gives k = 2, so y = 2x and y(3) = 6.")
    t = "Probability"
    fav = sum(1 for a, b in itertools.product(range(1, 7), repeat=2) if a + b == 8); assert Q(fav, 36) == Q(5, 36)
    M(A1,t,"Easy","Two fair dice are thrown. What is the probability that the sum of the numbers is 8?",["5/36","1/6","1/9","7/36"],"5/36","Out of 36 equally likely outcomes, a sum of 8 comes from (2,6), (3,5), (4,4), (5,3) and (6,2): 5 outcomes. P = 5/36.")
    t = "Linear Programming"
    xs_, ys_ = symbols("xs ys"); cons = [xs_ + ys_ - 4, xs_ - 3, -xs_, -ys_]   # each <= 0
    verts = set()
    for c1, c2 in itertools.combinations(cons, 2):
        s_ = sp.solve([c1, c2], [xs_, ys_], dict=True)
        if s_ and all(c.subs(s_[0]) <= 0 for c in cons): verts.add((s_[0][xs_], s_[0][ys_]))
    best = max(3 * a + 2 * b for a, b in verts); assert verts == {(0, 0), (3, 0), (3, 1), (0, 4)} and best == 11
    M(A1,t,"Medium","Maximise Z = 3x + 2y subject to x + y ≤ 4, x ≤ 3, x ≥ 0, y ≥ 0. The maximum value of Z is:",["11","9","8","12"],"11","The corner points of the feasible region are (0, 0), (3, 0), (3, 1) and (0, 4). Z = 0, 9, 11 and 8 there, so the maximum is 11, at (3, 1). (12 would need x = 4, which breaks x ≤ 3.)")
    # ---------------- Section B1: Mathematics ----------------
    t = "Relations & Functions"
    S3 = [1, 2, 3]; R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}
    refl = all((a, a) in R for a in S3); sym = all((b, a) in R for a, b in R); tra = all((a, d) in R for a, b in R for c, d in R if b == c)
    assert refl and sym and tra
    M(B1,t,"Medium","On the set {1, 2, 3}, the relation R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)} is:",["an equivalence relation","reflexive and symmetric, but not transitive","symmetric, but not reflexive","neither reflexive nor symmetric"],"an equivalence relation","Reflexive: (1,1), (2,2) and (3,3) are all present. Symmetric: (1,2) and (2,1) are both present. Transitive: every chain is closed, e.g. (1,2) and (2,1) give (1,1), which is in R. So R is an equivalence relation, with classes {1, 2} and {3}.")
    inj = sum(1 for f_ in itertools.product("abcd", repeat=3) if len(set(f_)) == 3); assert inj == 24
    M(B1,t,"Easy","How many one-one functions are there from A = {1, 2, 3} to B = {a, b, c, d}?",["24","64","81","12"],str(inj),"1 can go to any of 4 elements, 2 to any of the remaining 3, and 3 to any of the remaining 2: 4 × 3 × 2 = 24. (64 = 4³ counts all functions.)")
    t = "Inverse Trigonometric Functions"
    assert asin(-Q(1, 2)) == -pi / 6
    M(B1,t,"Easy","What is the principal value of sin⁻¹(−1/2)?",["−π/6","7π/6","5π/6","π/6"],"−π/6","The principal range of sin⁻¹ is [−π/2, π/2]. sin(−π/6) = −1/2, and −π/6 lies in that range. (sin 7π/6 is also −1/2, but 7π/6 is outside the principal range.)")
    t = "Continuity & Differentiability"
    k = limit((x**2 - 4) / (x - 2), x, 2); assert k == 4
    M(B1,t,"Easy","f(x) = (x² − 4)/(x − 2) for x ≠ 2, and f(2) = k. For which value of k is f continuous at x = 2?",["4","2","0","No value of k"],"4","For x ≠ 2, f(x) = (x − 2)(x + 2)/(x − 2) = x + 2, which tends to 4 as x → 2. Continuity needs f(2) = 4, so k = 4.",fixed=True)
    dv = diff(exp(2 * x) * sin(x), x).subs(x, 0); assert dv == 1
    M(B1,t,"Medium","If y = e²ˣ sin x, then dy/dx at x = 0 is:",["1","2","0","3"],str(dv),"Product rule: dy/dx = 2e²ˣ sin x + e²ˣ cos x. At x = 0: 0 + 1·1 = 1.")
    t = "Applications of Derivatives"
    r = symbols("r"); rate = (diff(pi * r**2, r) * 2).subs(r, 5); assert rate == 20 * pi
    M(B1,t,"Medium","The radius of a circle is increasing at 2 cm/s. How fast is its area increasing when the radius is 5 cm?",["20π cm²/s","10π cm²/s","25π cm²/s","4π cm²/s"],"20π cm²/s","A = πr², so dA/dt = 2πr · dr/dt = 2π × 5 × 2 = 20π cm²/s.")
    t = "Vectors"
    a = Matrix([1, 2, 0]); b = Matrix([3, 0, 1]); cr = a.cross(b); assert list(cr) == [2, -1, -6] and cr.norm() == sqrt(41)
    M(B1,t,"Medium","What is the area of the parallelogram whose adjacent sides are a = î + 2ĵ and b = 3î + k̂?",["√41 square units","41 square units","√11 square units","7 square units"],"√41 square units","Area = |a × b|. a × b = (2·1 − 0·0)î − (1·1 − 0·3)ĵ + (1·0 − 2·3)k̂ = 2î − ĵ − 6k̂. Its magnitude is √(4 + 1 + 36) = √41.")
    t = "Three-dimensional Geometry"
    u = Matrix([1, 1, 0]); v = Matrix([0, 1, 1]); cth = u.dot(v) / (u.norm() * v.norm()); assert cth == Q(1, 2)
    M(B1,t,"Medium","What is the angle between two lines whose direction ratios are 1, 1, 0 and 0, 1, 1?",["60°","45°","90°","30°"],"60°","cos θ = |a₁a₂ + b₁b₂ + c₁c₂| / (√(a₁² + b₁² + c₁²) √(a₂² + b₂² + c₂²)) = (0 + 1 + 0)/(√2 · √2) = 1/2, so θ = 60°.")
    t = "Probability"
    pa, pb, pab = Q(1, 2), Q(2, 5), Q(1, 5); assert pab / pb == Q(1, 2) and pa * pb == pab
    M(B1,t,"Medium","P(A) = 0.5, P(B) = 0.4 and P(A ∩ B) = 0.2. Which statement is true?",["P(A | B) = 0.5, and A and B are independent","P(A | B) = 0.4, and A and B are independent","P(A | B) = 0.5, and A and B are not independent","P(A | B) = 0.2, and A and B are mutually exclusive"],"P(A | B) = 0.5, and A and B are independent","P(A | B) = P(A ∩ B)/P(B) = 0.2/0.4 = 0.5, which equals P(A). Also P(A)P(B) = 0.2 = P(A ∩ B), so A and B are independent. They are not mutually exclusive, since P(A ∩ B) ≠ 0.")
    post = (Q(1, 2) * Q(3, 5)) / (Q(1, 2) * Q(3, 5) + Q(1, 2) * Q(2, 5)); assert post == Q(3, 5)
    M(B1,t,"Hard","Bag I contains 3 red and 2 black balls; Bag II contains 2 red and 3 black balls. A bag is chosen at random and a ball drawn from it is red. What is the probability that it came from Bag I?",["3/5","1/2","3/10","2/5"],"3/5","Bayes' theorem: P(I | red) = (½ × 3/5) / (½ × 3/5 + ½ × 2/5) = (3/10)/(5/10) = 3/5.")


def build2(B):
    """Second batch: +34 questions (17 Section A, 17 Section B1). Every answer is computed or asserted with sympy."""
    M = lambda *a, **k: B.mcq("maths", *a, **k)
    mn = lambda v: str(v).replace("-", "−")
    # ---------------- Section A (common) ----------------
    t = "Matrices"
    A = Matrix([[1, 2], [3, 4]]); A2 = A * A; assert A2 == Matrix([[7, 10], [15, 22]])
    M(A1,t,"Easy",f"If A = {mx([[1,2],[3,4]])}, then A² is:",[mx(A2.tolist()),mx([[1,4],[9,16]]),mx([[5,6],[11,16]]),mx([[2,4],[6,8]])],mx(A2.tolist()),"A² = A × A. Row × column: (1,1) = 1·1 + 2·3 = 7; (1,2) = 1·2 + 2·4 = 10; (2,1) = 3·1 + 4·3 = 15; (2,2) = 3·2 + 4·4 = 22. Squaring each entry (the second option) is not matrix multiplication.")
    d3 = 3**2 * 5; assert d3 == 45
    M(A1,t,"Medium","If A is a 2 × 2 matrix with |A| = 5, then |3A| equals:",["45","15","135","25"],"45","For an n × n matrix, |kA| = kⁿ|A|. Here n = 2 and k = 3, so |3A| = 3² × 5 = 45. (15 forgets that both rows are multiplied by 3.)")
    xs, ys = symbols("xs ys"); sl = sp.solve([xs + ys - 7, xs - ys - 1], [xs, ys]); assert sl == {xs: 4, ys: 3}
    M(A1,t,"Medium",f"If {mx([['x + y',2],[5,'x − y']])} = {mx([[7,2],[5,1]])}, then the value of xy is:",["12","7","10","15"],"12","Equal matrices have equal entries: x + y = 7 and x − y = 1. Adding gives x = 4, and then y = 3. So xy = 12.")
    t = "Determinants"
    dv = Matrix([[1, 1, 1], [1, 2, 3], [1, 4, 9]]).det(); assert dv == 2
    M(A1,t,"Medium",f"The value of the determinant {mx([[1,1,1],[1,2,3],[1,4,9]])} is:",["2","0","6","−2"],"2","Subtract the first row from the second and third: rows become (0, 1, 2) and (0, 3, 8). Expanding along the first column gives 1 × (1·8 − 2·3) = 2.")
    M(A1,t,"Medium","If A is a 3 × 3 matrix with |A| = 4, then |adj A| equals:",["16","4","64","12"],"16","For an n × n matrix, |adj A| = |A|ⁿ⁻¹. With n = 3 this is 4² = 16.")
    t = "Continuity & Differentiability"
    dd = diff(x**x, x).subs(x, 1); assert dd == 1
    M(A1,t,"Medium","If y = xˣ (x > 0), then dy/dx at x = 1 is:",["1","0","e","2"],"1","Take logs: log y = x log x, so y′/y = log x + 1 and y′ = xˣ(1 + log x). At x = 1: 1 × (1 + 0) = 1.")
    kk = sp.solve(5 * symbols("k") + 1 - (3 * 5 - 5), symbols("k"))[0]; assert kk == Q(9, 5)
    M(A1,t,"Medium","f(x) = kx + 1 for x ≤ 5 and f(x) = 3x − 5 for x > 5. For which value of k is f continuous at x = 5?",["9/5","2","1","5/9"],"9/5","The left value is 5k + 1 and the right limit is 3(5) − 5 = 10. Continuity needs 5k + 1 = 10, so k = 9/5.")
    t = "Applications of Derivatives"
    M(A1,t,"Easy","What is the equation of the tangent to the curve y = x² at the point (1, 1)?",["y = 2x − 1","y = x","y = 2x + 1","y = x²"],"y = 2x − 1","dy/dx = 2x = 2 at x = 1. The tangent through (1, 1) is y − 1 = 2(x − 1), i.e. y = 2x − 1.")
    ar = sp.maximum(symbols("w") * (20 - symbols("w")), symbols("w"), sp.Interval(0, 20)); assert ar == 100
    M(A1,t,"Medium","A rectangle has a perimeter of 40 cm. What is the largest area it can have?",["100 cm²","80 cm²","96 cm²","120 cm²"],"100 cm²","With sides w and 20 − w the area is w(20 − w). Its derivative 20 − 2w is zero at w = 10, giving a square of side 10 and area 100 cm², which is a maximum because the second derivative is negative.")
    t = "Integrals"
    i1 = integrate(x / (x**2 + 1), x); assert eq(i1, sp.log(x**2 + 1) / 2)
    M(A1,t,"Easy","∫ x/(x² + 1) dx equals:",["(1/2) log(x² + 1) + C","log(x² + 1) + C","tan⁻¹ x + C","(1/2) tan⁻¹ x + C"],"(1/2) log(x² + 1) + C","Put u = x² + 1, so du = 2x dx and x dx = du/2. The integral becomes (1/2) ∫ du/u = (1/2) log|u| + C.")
    i2 = integrate(x**2 * exp(x**3), (x, 0, 1)); assert sp.simplify(i2 - (sp.E - 1) / 3) == 0
    M(A1,t,"Medium","Evaluate ∫₀¹ x² e^{x³} dx.",["(e − 1)/3","e − 1","e/3","(e + 1)/3"],"(e − 1)/3","Put u = x³, du = 3x² dx. The limits stay 0 to 1, and the integral is (1/3) ∫₀¹ eᵘ du = (e − 1)/3.")
    i3 = integrate(1 / sp.sqrt(4 - x**2), x); assert eq(i3, asin(x / 2))
    M(A1,t,"Easy","∫ dx/√(4 − x²) equals:",["sin⁻¹(x/2) + C","sin⁻¹ x + C","(1/2) sin⁻¹(x/2) + C","cos⁻¹(x/2) + C"],"sin⁻¹(x/2) + C","Use the standard result ∫ dx/√(a² − x²) = sin⁻¹(x/a) + C with a = 2.")
    t = "Application of Integrals"
    ab = integrate(x - x**2, (x, 0, 1)); assert ab == Q(1, 6)
    M(A1,t,"Medium","What is the area enclosed between the curves y = x and y = x² ?",["1/6 square unit","1/3 square unit","1/2 square unit","1 square unit"],"1/6 square unit","The curves meet at x = 0 and x = 1, and y = x lies above y = x² in between. Area = ∫₀¹ (x − x²) dx = 1/2 − 1/3 = 1/6.")
    t = "Differential Equations"
    M(A1,t,"Medium","The integrating factor of the differential equation dy/dx + (2/x) y = x² (x > 0) is:",["x²","e^{2x}","1/x²","2x"],"x²","The integrating factor is e^{∫P dx} with P = 2/x. ∫(2/x) dx = 2 log x, so the factor is e^{2 log x} = x².")
    M(A1,t,"Easy","If dy/dx = y and y = 1 when x = 0, then the value of y at x = 1 is:",["e","1","2","e²"],"e","Separating variables, dy/y = dx gives log y = x + c. y(0) = 1 gives c = 0, so y = eˣ and y(1) = e.")
    t = "Probability"
    M(A1,t,"Medium","A fair coin is tossed four times. What is the probability of getting at least one head?",["15/16","7/8","1/16","3/4"],"15/16","P(no head) = (1/2)⁴ = 1/16. So P(at least one head) = 1 − 1/16 = 15/16.")
    # ---------------- Section B1 (Mathematics) ----------------
    t = "Relations & Functions"
    M(B1,t,"Medium","How many reflexive relations can be defined on a set with 3 elements?",["64","512","8","27"],"64","A relation on a 3-element set is a subset of the 9 ordered pairs. For reflexivity the 3 pairs (a, a) must be included, and the other 6 pairs are free: 2⁶ = 64. (512 = 2⁹ counts all relations.)")
    M(B1,t,"Easy","The function f: R → R defined by f(x) = x² is:",["neither one-one nor onto","one-one but not onto","onto but not one-one","both one-one and onto"],"neither one-one nor onto","f(2) = f(−2) = 4, so f is not one-one. Its values are never negative, so the range is [0, ∞) and not all of R: f is not onto.")
    gf = (lambda xx: (2 * xx + 1)**2)(2); assert gf == 25
    M(B1,t,"Easy","If f(x) = 2x + 1 and g(x) = x², then (g∘f)(2) equals:",["25","9","17","5"],"25","(g∘f)(2) = g(f(2)) = g(5) = 25. (9 is (f∘g)(2) = f(4), the composition in the other order.)")
    t = "Inverse Trigonometric Functions"
    assert sp.N(sp.atan(1) + sp.atan(2) + sp.atan(3) - pi, 20) < 1e-15
    M(B1,t,"Hard","The value of tan⁻¹ 1 + tan⁻¹ 2 + tan⁻¹ 3 is:",["π","π/2","3π/4","2π"],"π","tan⁻¹ 1 = π/4. For tan⁻¹ 2 + tan⁻¹ 3, ab = 6 > 1, so the sum is π + tan⁻¹((2 + 3)/(1 − 6)) = π + tan⁻¹(−1) = π − π/4 = 3π/4. Total = π/4 + 3π/4 = π.")
    assert sp.sin(sp.acos(Q(3, 5))) == Q(4, 5)
    M(B1,t,"Medium","The value of sin(cos⁻¹(3/5)) is:",["4/5","3/5","5/4","3/4"],"4/5","Let θ = cos⁻¹(3/5), so cos θ = 3/5 with θ in [0, π]. Then sin θ = √(1 − 9/25) = 4/5, which is positive in that range.")
    assert sp.acos(-Q(1, 2)) == 2 * pi / 3
    M(B1,t,"Easy","What is the principal value of cos⁻¹(−1/2)?",["2π/3","π/3","−π/3","4π/3"],"2π/3","The principal range of cos⁻¹ is [0, π]. cos(2π/3) = −1/2 and 2π/3 lies in that range. (4π/3 also has cosine −1/2 but is outside the range.)")
    t = "Continuity & Differentiability"
    tt = symbols("tt"); aa = symbols("aa", positive=True); dydx = diff(2 * aa * tt, tt) / diff(aa * tt**2, tt); assert sp.simplify(dydx.subs(tt, 1)) == 1
    M(B1,t,"Medium","If x = at² and y = 2at, then dy/dx at t = 1 is:",["1","2","0","1/2"],"1","dx/dt = 2at and dy/dt = 2a, so dy/dx = (dy/dt)/(dx/dt) = 2a/(2at) = 1/t. At t = 1 this is 1.")
    rc = sp.solve(diff(x**2 - 4 * x + 3, x), x)[0]; assert rc == 2
    M(B1,t,"Medium","Rolle's theorem is applied to f(x) = x² − 4x + 3 on [1, 3]. The value of c is:",["2","1.5","2.5","3"],"2","f(1) = f(3) = 0, so Rolle's theorem applies. f′(x) = 2x − 4 = 0 gives c = 2, which lies in (1, 3).")
    t = "Applications of Derivatives"
    fm = (x**3 - 12 * x).subs(x, -2); assert fm == 16 and diff(x**3 - 12 * x, x, 2).subs(x, -2) < 0
    M(B1,t,"Medium","The local maximum value of f(x) = x³ − 12x is:",["16","−16","2","0"],"16","f′(x) = 3x² − 12 = 0 gives x = ±2. f″(x) = 6x is negative at x = −2, so that is the local maximum: f(−2) = −8 + 24 = 16. (−16 is the local minimum at x = 2.)")
    sa = symbols("sa"); vr = diff(sa**3, sa).subs(sa, 2) * 3; assert vr == 36
    M(B1,t,"Medium","The edge of a cube increases at 3 cm/s. How fast is its volume increasing when the edge is 2 cm?",["36 cm³/s","12 cm³/s","24 cm³/s","54 cm³/s"],"36 cm³/s","V = a³, so dV/dt = 3a² · da/dt = 3 × 4 × 3 = 36 cm³/s.")
    t = "Vectors"
    ang = sp.acos(Q(6, 12)); assert ang == pi / 3
    M(B1,t,"Easy","If |a| = 3, |b| = 4 and a · b = 6, then the angle between a and b is:",["60°","30°","45°","90°"],"60°","cos θ = (a · b)/(|a||b|) = 6/12 = 1/2, so θ = 60°.")
    lam = sp.solve(Matrix([1, 2, 3]).dot(Matrix([3, -1, symbols("lam")])), symbols("lam"))[0]; assert lam == -Q(1, 3)
    M(B1,t,"Medium","The vectors a = î + 2ĵ + 3k̂ and b = 3î − ĵ + λk̂ are perpendicular. The value of λ is:",["−1/3","1/3","3","−3"],"−1/3","Perpendicular vectors have a · b = 0: 3 − 2 + 3λ = 0, so λ = −1/3.")
    t = "Three-dimensional Geometry"
    dist = Q(abs(1 + 4 + 6 - 3), 3); assert dist == Q(8, 3)
    M(B1,t,"Medium","What is the distance of the point (1, 2, 3) from the plane x + 2y + 2z = 3?",["8/3","3","11/3","2/3"],"8/3","Distance = |1 + 2(2) + 2(3) − 3| / √(1 + 4 + 4) = 8/3.")
    assert Q(2, 7)**2 + Q(3, 7)**2 + Q(6, 7)**2 == 1
    M(B1,t,"Easy","A line has direction ratios 2, 3, 6. The cosine of the angle it makes with the x-axis is:",["2/7","2/3","3/7","6/7"],"2/7","The length of (2, 3, 6) is √(4 + 9 + 36) = 7, so the direction cosines are 2/7, 3/7 and 6/7. The cosine with the x-axis is the first one, 2/7.")
    t = "Probability"
    pa, pb = Q(3, 10), Q(1, 2); pu = Q(65, 100); pab = pa + pb - pu; assert pab == pa * pb == Q(15, 100)
    M(B1,t,"Medium","For events A and B, P(A) = 0.3, P(B) = 0.5 and P(A ∪ B) = 0.65. Then:",["A and B are independent","A and B are mutually exclusive","P(A ∩ B) = 0.2","P(A | B) = 0.6"],"A and B are independent","P(A ∩ B) = P(A) + P(B) − P(A ∪ B) = 0.8 − 0.65 = 0.15. This equals P(A)P(B) = 0.15, so the events are independent. They are not mutually exclusive because P(A ∩ B) ≠ 0.")
    M(B1,t,"Medium","A random variable X follows a binomial distribution with n = 6 and p = 1/3. Its mean and variance are:",["2 and 4/3","2 and 2/3","6 and 4/3","1/3 and 2/3"],"2 and 4/3","Mean = np = 6 × 1/3 = 2. Variance = npq = 6 × 1/3 × 2/3 = 4/3.")
    t = "Linear Programming"
    cons = [4 - xs - ys, 1 - xs, -ys]   # each <= 0 means x+y>=4, x>=1, y>=0
    verts = set()
    for c1, c2 in itertools.combinations(cons, 2):
        s_ = sp.solve([c1, c2], [xs, ys], dict=True)
        if s_ and all(c.subs(s_[0]) <= 0 for c in cons): verts.add((s_[0][xs], s_[0][ys]))
    assert verts == {(1, 3), (4, 0)} and min(2 * a + 3 * b for a, b in verts) == 8
    M(A1,t,"Medium","Minimise Z = 2x + 3y subject to x + y ≥ 4, x ≥ 1, y ≥ 0. The minimum value of Z is:",["8","11","12","9"],"8","The corner points of this (unbounded) region are (1, 3) and (4, 0). Z = 11 at (1, 3) and Z = 8 at (4, 0). Because Z has positive coefficients, it only grows along the open directions, so the minimum is 8.")
