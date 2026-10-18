"""Formula & rules sheets, grouped by topic. Each topic: (icon, name, [(formula, short explanation), ...]).
Running this file numerically spot-checks the formulas (python3 tools/formulas.py)."""
FORMULAS = {
"quant": [
 ("📈","Percentages",[
  ("Net change = a + b + ab/100 %","Two successive changes of a% and b%. Use a negative value for a decrease."),
  ("% change = (New − Old) / Old × 100",""),
  ("Rise needed after x% fall = x / (100 − x) × 100 %","To get back to the original value."),
  ("Price ↑ r% ⇒ cut use by r / (100 + r) × 100 %","Keeps spending unchanged."),
 ]),
 ("💰","Profit &amp; Loss",[
  ("Profit % = (SP − CP) / CP × 100","Profit and loss % are always on cost price."),
  ("SP = CP × (100 + P%) / 100","For a loss, use (100 − L%)."),
  ("SP = MP × (1 − d/100)","Discount is always on the marked price."),
  ("False-weight gain % = (True − False) / False × 100","E.g. 900 g for 1 kg: 100/900 = 11 1/9%."),
 ]),
 ("🏦","Simple &amp; Compound Interest",[
  ("SI = P × R × T / 100",""),
  ("A = P (1 + R/100)ⁿ,  CI = A − P","Compounded annually for n years."),
  ("CI − SI (2 years) = P (R/100)²",""),
 ]),
 ("⚖️","Ratio &amp; Proportion",[
  ("a : b = c : d  ⇔  a × d = b × c","Cross-multiplication."),
  ("Mean proportional of a and b = √(ab)",""),
  ("Partnership: profit share ∝ capital × time",""),
 ]),
 ("⚗️","Averages &amp; Alligation",[
  ("Average = Sum / Count",""),
  ("Average of 1, 2, …, n = (n + 1) / 2",""),
  ("Cheaper : Dearer = (d − m) : (m − c)","c = cheaper price, d = dearer price, m = mixture price."),
 ]),
 ("🛠️","Time &amp; Work",[
  ("Together = ab / (a + b) days","When A takes a days and B takes b days."),
  ("M₁ × D₁ = M₂ × D₂","For the same job: men × days stays constant."),
  ("Net rate = 1/a − 1/b","A fill pipe (a hours) and an empty pipe (b hours) open together."),
 ]),
 ("🚆","Time, Speed &amp; Distance",[
  ("Speed = Distance / Time",""),
  ("km/h → m/s: × 5/18     m/s → km/h: × 18/5",""),
  ("Average speed = 2xy / (x + y)","Two equal distances at speeds x and y."),
  ("Crossing time = (L₁ + L₂) / relative speed","Add the speeds for opposite directions and subtract for the same direction. For a pole, L₂ = 0."),
  ("Downstream = b + s,  Upstream = b − s","b = boat speed in still water, s = stream speed."),
 ]),
 ("🔢","Number System",[
  ("Zeros at end of n! = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …",""),
  ("N = pᵃ·qᵇ·rᶜ ⇒ factors = (a+1)(b+1)(c+1)","From the prime factorisation of N."),
  ("HCF(a, b) × LCM(a, b) = a × b","For two numbers only."),
  ("Unit digits of 2, 3, 7, 8 repeat every 4 powers","Use the power mod 4 (0 means the 4th). 4 and 9 repeat every 2 powers. 0, 1, 5, 6 never change."),
 ]),
 ("✖️","Algebra",[
  ("(a ± b)² = a² ± 2ab + b²",""),
  ("a² − b² = (a + b)(a − b)",""),
  ("a³ + b³ = (a + b)³ − 3ab(a + b)",""),
  ("x² + 1/x² = (x + 1/x)² − 2",""),
  ("ax² + bx + c = 0: sum of roots = −b/a, product = c/a",""),
 ]),
 ("📐","Geometry &amp; Mensuration",[
  ("Circle: Area = πr², Circumference = 2πr",""),
  ("Right triangle: circumradius = hypotenuse / 2",""),
  ("Equilateral triangle: Area = (√3 / 4) a²",""),
  ("Regular n-gon: interior angle = (n − 2) × 180° / n",""),
  ("Diagonals of an n-gon = n(n − 3) / 2",""),
  ("Cube: Surface area = 6a², Volume = a³",""),
 ]),
 ("🔀","Permutations &amp; Combinations",[
  ("nPr = n! / (n − r)!","Order matters (arrangements)."),
  ("nCr = n! / (r! (n − r)!)","Order doesn't matter (selections)."),
  ("Arrangements with repeats = n! / (p! q! …)","p, q, … = how many times each letter repeats."),
  ("At least one = Total − None",""),
 ]),
 ("🎲","Probability",[
  ("P(E) = favourable / total outcomes","When all outcomes are equally likely."),
  ("P(not E) = 1 − P(E)",""),
  ("P(A or B) = P(A) + P(B) − P(A and B)",""),
  ("Independent events: P(A and B) = P(A) × P(B)",""),
 ]),
],
"reasoning": [
 ("🔗","Syllogisms",[
  ("All A are B ⇒ Some B are A","Conversion. It does not give 'All B are A'."),
  ("Some A are B ⇒ Some B are A",""),
  ("No A is B ⇒ No B is A",""),
  ("All A are B + No B is C ⇒ No A is C",""),
  ("'Some' + 'No' on the same two terms ⇒ Either I or II","Use this only when neither conclusion follows on its own."),
 ]),
 ("🔤","Coding &amp; Alphabet",[
  ("A = 1, B = 2, … , Z = 26",""),
  ("k-th from the right = (27 − k)-th from the left",""),
  ("E J O T Y = 5, 10, 15, 20, 25","Anchors for finding letter positions quickly."),
  ("Mirror letters: A↔Z, B↔Y, … (positions add to 27)",""),
 ]),
 ("🕐","Clocks &amp; Calendars",[
  ("Angle = |30H − 5.5M|°","If the result is over 180°, subtract it from 360° to get the smaller angle."),
  ("Hands together at (60H / 11) min past H","Between H and H + 1 o'clock. E.g. H = 4 gives 21 9/11 min."),
  ("Hands coincide 11 times in 12 hours","Once every 65 5/11 minutes."),
  ("Odd days: normal year = 1, leap year = 2",""),
  ("Leap year: divisible by 4 (century years: by 400)",""),
 ]),
 ("🧭","Direction Sense",[
  ("Right turns: N → E → S → W → N","Left turns go the other way."),
  ("Distance = √(x² + y²)","x = net east–west, y = net north–south."),
  ("Morning shadow → west,  evening shadow → east","The sun rises in the east and sets in the west."),
 ]),
 ("🏆","Ranking &amp; Order",[
  ("Total = L + R − 1","L = position from the left (or top), R = position from the right (or bottom)."),
  ("From right = Total − L + 1",""),
 ]),
 ("⚖️","Inequalities",[
  ("A > B ≥ C ⇒ A > C","Signs pointing the same way chain together."),
  ("A ≥ B ≥ C ⇒ A ≥ C",""),
  ("A > B < C ⇒ A, C cannot be compared","Opposite signs break the chain."),
 ]),
 ("📶","Series",[
  ("Check: differences → ratios → squares/cubes → n(n + 1) → ×2 ± 1","A good order to test patterns."),
  ("Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29 …",""),
 ]),
 ("👪","Blood Relations",[
  ("+ male,  − female,  = couple,  | next generation","Symbols for drawing a family tree."),
  ("Read chains from the end","E.g. 'my father's father's only son' = my father."),
 ]),
],
"dilr": [
 ("📈","Growth &amp; Share",[
  ("Growth % = (New − Old) / Old × 100",""),
  ("Share % = Part / Total × 100",""),
  ("% more (A over B) = (A − B) / B × 100","Divide by the value you are comparing against."),
  ("CAGR = (End / Start)^(1/n) − 1","Average yearly growth over n years."),
 ]),
 ("🥧","Pie Charts",[
  ("Central angle = % × 3.6°","1% = 3.6°, 25% = 90°, 10% = 36°."),
  ("Value = % × Total / 100",""),
 ]),
 ("➗","Averages &amp; Ratios",[
  ("Average = Sum / Count",""),
  ("A : B in lowest terms = (A ÷ HCF) : (B ÷ HCF)","E.g. 240 : 180 = 4 : 3."),
 ]),
 ("⭕","Venn Diagrams",[
  ("n(A ∪ B) = n(A) + n(B) − n(A ∩ B)",""),
  ("n(A ∪ B ∪ C) = ΣA − Σ(pairs) + n(A ∩ B ∩ C)","Here 'pairs' includes those in all three."),
  ("Only A = A − (A∩B) − (A∩C) + (A∩B∩C)",""),
  ("Exactly two = Σ(pairs) − 3 × n(A ∩ B ∩ C)",""),
  ("None = Total − n(at least one)",""),
 ]),
 ("🏅","Games &amp; Tournaments",[
  ("Round robin (n teams) = nC2 = n(n − 1) / 2 matches","Each pair of teams plays once."),
  ("Knock-out (n teams) = n − 1 matches","Each match eliminates one team."),
  ("Total points = points per match × matches","E.g. 2 per win with no draws: 2 × matches."),
 ]),
 ("🗺️","Network &amp; Routes",[
  ("Shortest route = min(sum of road lengths over all paths)","List the candidate paths and add up each one."),
  ("If a road closes, re-check only paths that used it",""),
 ]),
],
}

if __name__ == "__main__":
    from math import comb, factorial, isclose, sqrt, pi
    a,b=20,-20; assert isclose((1+a/100)*(1+b/100)-1, (a+b+a*b/100)/100)
    x=20; assert isclose((1-x/100)*(1+x/(100-x)),1)
    r=25; assert isclose((1+r/100)*(1-r/(100+r)),1)
    P,R=8000,5; assert isclose(P*(1+R/100)**2-P-P*R*2/100, P*(R/100)**2)
    c,d,m=40,55,45; assert isclose((c*(d-m)+d*(m-c))/((d-m)+(m-c)), m)
    A,B=12,18; assert isclose(1/(1/A+1/B), A*B/(A+B))
    assert isclose(2*60*40/(60+40), 2*120/(120/60+120/40))
    import math
    for n in (50, 100, 137):
        s=str(math.factorial(n)); assert len(s)-len(s.rstrip("0"))==sum(n//5**k for k in range(1,6))
    assert sum(1 for k in range(1,361) if 360%k==0)==(3+1)*(2+1)*(1+1)
    assert math.gcd(36,84)*math.lcm(36,84)==36*84
    assert [pow(7,k,10) for k in range(1,9)]==[7,9,3,1,7,9,3,1] and [pow(4,k,10) for k in (1,2,3)]==[4,6,4]
    p,q=2.0,5.0; assert isclose(p**3+q**3,(p+q)**3-3*p*q*(p+q)); xx=2.0; assert isclose(xx**2+1/xx**2,(xx+1/xx)**2-2)
    assert (6-2)*180/6==120 and 10*7//2==comb(10,2)-10
    assert factorial(5)//(factorial(2)*factorial(2))==30
    assert isclose(60*4/11,21+9/11) and isclose(720/11,65+5/11)
    assert ord("E")-64==5 and ord("Y")-64==25 and (ord("A")-64)+(ord("Z")-64)==27
    assert comb(6,2)==6*5//2
    # 3-set check with the site's sports data
    C,F,H,cf,fh,ch,all3=50,40,30,15,10,12,5
    assert C+F+H-cf-fh-ch+all3==88 and C-cf-ch+all3==28 and (cf+fh+ch)-3*all3==22
    print("formula checks ok")
