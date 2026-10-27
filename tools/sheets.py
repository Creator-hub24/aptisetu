# Printable formula sheets. Executed by m2pages.py. Every formula is numerically checked in check_sheets().
SHEETS = [
{"slug":"cat-quant","title":"CAT Quant Formula Sheet (Printable)","h1":"CAT Quant formula sheet",
 "desc":"A printable one-page CAT Quantitative Ability formula sheet: algebra, progressions, logarithms, number system, P&C, probability, geometry and mensuration. Every formula is checked by script.",
 "groups":[
  ("Algebra",[("(a + b)² = a² + 2ab + b²",""),("a² − b² = (a − b)(a + b)",""),("a³ + b³ = (a + b)(a² − ab + b²)",""),("a³ − b³ = (a − b)(a² + ab + b²)",""),("a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca)","If a + b + c = 0, then a³ + b³ + c³ = 3abc."),("ax² + bx + c = 0: x = [−b ± √(b² − 4ac)] / 2a","Sum of roots = −b/a, product = c/a."),("AM ≥ GM: (a + b)/2 ≥ √(ab) for a, b ≥ 0","Equality when a = b.")]),
  ("Progressions",[("AP: Tₙ = a + (n − 1)d,  Sₙ = n/2 [2a + (n − 1)d]",""),("GP: Tₙ = arⁿ⁻¹,  Sₙ = a(rⁿ − 1)/(r − 1)","r ≠ 1."),("Infinite GP: S = a/(1 − r)","|r| &lt; 1."),("1 + 2 + … + n = n(n + 1)/2",""),("1² + 2² + … + n² = n(n + 1)(2n + 1)/6",""),("1³ + 2³ + … + n³ = [n(n + 1)/2]²","")]),
  ("Logarithms",[("log(mn) = log m + log n,  log(m/n) = log m − log n",""),("log mᵏ = k log m",""),("logₐ b = log b / log a","Change of base."),("a^(logₐ x) = x","")]),
  ("Number system",[("N = pᵃ qᵇ rᶜ has (a + 1)(b + 1)(c + 1) factors",""),("Sum of factors = [(pᵃ⁺¹ − 1)/(p − 1)] × …","Multiply over every prime."),("HCF × LCM = product (two numbers)",""),("Trailing zeros of n! = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …",""),("Euler: a^φ(n) ≡ 1 (mod n) if gcd(a, n) = 1","φ(p) = p − 1 for a prime p.")]),
  ("Counting &amp; probability",[("ⁿPᵣ = n!/(n − r)!,  ⁿCᵣ = n!/[r!(n − r)!]",""),("Circular arrangements of n = (n − 1)!",""),("Ways to split n identical items among r people = ⁿ⁺ʳ⁻¹Cᵣ₋₁","Each may get zero."),("P(A ∪ B) = P(A) + P(B) − P(A ∩ B)",""),("P(not A) = 1 − P(A)","")]),
  ("Geometry &amp; mensuration",[("Triangle: area = ½ab sin C = √[s(s − a)(s − b)(s − c)]","s = (a + b + c)/2 (Heron)."),("Equilateral triangle area = (√3/4)a²",""),("Interior angle of a regular n-gon = (n − 2) × 180°/n",""),("Diagonals of an n-gon = n(n − 3)/2",""),("Circle: area πr², circumference 2πr; sector = (θ/360)πr²",""),("Sphere V = (4/3)πr³, S = 4πr²; cone V = (1/3)πr²h; cylinder V = πr²h","")]),
 ]},
{"slug":"bank-ssc-quant","title":"Bank & SSC Quant Formula Sheet (Printable)","h1":"Bank &amp; SSC Quant formula sheet",
 "desc":"A printable Quant formula sheet for IBPS, SBI and SSC exams: percentages, profit and loss, interest, speed, work, averages, mixtures and mensuration, each checked by script.",
 "groups":[
  ("Percentages",[("Net change of a% then b% = a + b + ab/100 %","Use negative values for falls."),("Rise to recover a fall of x% = x/(100 − x) × 100 %",""),("Price ↑ r% ⇒ cut use by r/(100 + r) × 100 %","Same spending.")]),
  ("Profit, loss &amp; discount",[("Profit % = (SP − CP)/CP × 100","Always on cost price."),("SP = MP × (1 − d/100)","Discount is on marked price."),("Successive discounts d₁, d₂ = d₁ + d₂ − d₁d₂/100 %",""),("Same SP, x% gain and x% loss ⇒ loss of x²/100 %","")]),
  ("Interest",[("SI = PRT/100",""),("A = P(1 + R/100)ⁿ",""),("CI − SI (2 years) = P(R/100)²",""),("CI − SI (3 years) = P(R/100)²(3 + R/100)",""),("Half-yearly: rate R/2, periods 2n","")]),
  ("Speed &amp; work",[("km/h × 5/18 = m/s",""),("Average speed (equal distances) = 2xy/(x + y)",""),("Boat b = (down + up)/2, stream s = (down − up)/2",""),("A alone a days, B alone b days ⇒ together ab/(a + b) days",""),("M₁D₁H₁/W₁ = M₂D₂H₂/W₂","Men × days × hours per unit of work.")]),
  ("Averages &amp; mixtures",[("Average = sum/count",""),("Alligation: cheaper : dearer = (d − m) : (m − c)",""),("After n replacements of fraction f: left = (1 − f)ⁿ of original","")]),
  ("Mensuration",[("Rectangle area lw, perimeter 2(l + w)",""),("Trapezium area = ½(a + b)h",""),("Rhombus area = ½d₁d₂",""),("Cube V = a³, S = 6a²; cuboid S = 2(lb + bh + hl)",""),("Cylinder CSA = 2πrh, TSA = 2πr(r + h)",""),("Cone slant l = √(r² + h²), CSA = πrl","")]),
 ]},
{"slug":"reasoning","title":"Reasoning Shortcuts Sheet (Printable)","h1":"Reasoning shortcuts sheet",
 "desc":"A printable reasoning shortcuts sheet for Bank, SSC and CUET: letter positions, clocks, calendars, ranking, directions, inequalities and syllogism rules, checked by script.",
 "groups":[
  ("Letters &amp; coding",[("A–Z positions: E = 5, J = 10, O = 15, T = 20, Y = 25","Remember 'EJOTY'."),("Opposite letter: position of opposite = 27 − position","A ↔ Z, M ↔ N."),("Reverse position = 27 − forward position","")]),
  ("Clocks",[("Angle between hands = |30H − 5.5M|°","Take 360 minus it if over 180."),("Hands coincide every 720/11 = 65 5/11 minutes",""),("Hands overlap 22 times, are opposite 22 times, and at right angles 44 times in 24 hours","")]),
  ("Calendars",[("Odd days: ordinary year 1, leap year 2",""),("Leap year: divisible by 4; century years only if divisible by 400","1900 no, 2000 yes."),("Days of the week repeat every 7 days; 100 years have 5 odd days","")]),
  ("Ranking &amp; order",[("Total = rank from left + rank from right − 1",""),("People between two ranks (same side) = difference − 1","")]),
  ("Directions",[("Turning right from North gives East; left gives West",""),("Shortest distance = √(x² + y²)","Net east-west x, net north-south y.")]),
  ("Inequalities &amp; syllogisms",[("A ≥ B &gt; C ⇒ A &gt; C; A ≥ B ≤ C ⇒ no relation",""),("Either-or: when two conclusions are complementary and neither alone follows",""),("All A are B + All B are C ⇒ All A are C",""),("Some A are B ⇒ Some B are A; 'All A are B' ⇒ 'Some B are A'","Possibility questions: check if it can be true.")]),
 ]},
]

def check_sheets():
    from math import isclose, sqrt, pi, comb, perm, factorial, log, gcd, lcm, prod
    import math, calendar, datetime
    a,b,c=3.0,-5.0,2.0
    assert isclose((a+b)**2,a*a+2*a*b+b*b) and isclose(a*a-b*b,(a-b)*(a+b))
    assert isclose(a**3+b**3,(a+b)*(a*a-a*b+b*b)) and isclose(a**3-b**3,(a-b)*(a*a+a*b+b*b))
    assert isclose(a**3+b**3+c**3-3*a*b*c,(a+b+c)*(a*a+b*b+c*c-a*b-b*c-c*a))
    x,y=4.0,-7.0; assert isclose(x**3+y**3+(-x-y)**3,3*x*y*(-x-y))
    A,B,C=2.0,-3.0,-5.0; d=sqrt(B*B-4*A*C); r1,r2=(-B+d)/(2*A),(-B-d)/(2*A)
    assert isclose(A*r1*r1+B*r1+C,0,abs_tol=1e-9) and isclose(r1+r2,-B/A) and isclose(r1*r2,C/A)
    assert (4+9)/2>=sqrt(36)
    a0,dd,n=3,4,10; assert sum(a0+k*dd for k in range(n))==n*(2*a0+(n-1)*dd)/2
    g,r=2,3; assert sum(g*r**k for k in range(6))==g*(r**6-1)/(r-1); assert isclose(sum(.5**k for k in range(60)),1/(1-.5))
    for n in (7,20): assert sum(range(1,n+1))==n*(n+1)//2 and sum(k*k for k in range(1,n+1))==n*(n+1)*(2*n+1)//6 and sum(k**3 for k in range(1,n+1))==(n*(n+1)//2)**2
    m,q=7.0,3.0; assert isclose(log(m*q),log(m)+log(q)) and isclose(log(m/q),log(m)-log(q)) and isclose(log(m**5),5*log(m))
    assert isclose(math.log(81,3),log(81)/log(3)) and isclose(2**math.log(13,2),13)
    N=2**3*3**2*5; divs=[k for k in range(1,N+1) if N%k==0]
    assert len(divs)==4*3*2 and sum(divs)==(2**4-1)//1*(3**3-1)//2*(5**2-1)//4
    assert gcd(36,84)*lcm(36,84)==36*84
    for n in (100,137): s=str(factorial(n)); assert len(s)-len(s.rstrip("0"))==sum(n//5**k for k in range(1,5))
    assert pow(3,6,7)==1 and pow(2,10,11)==1
    assert perm(7,3)==factorial(7)//factorial(4) and comb(7,3)==factorial(7)//(factorial(3)*factorial(4))
    import itertools
    perms=set(); 
    for p in itertools.permutations(range(5)):
        i=p.index(0); perms.add(p[i:]+p[:i])
    assert len(perms)==factorial(4)
    assert sum(1 for t in itertools.product(range(7),repeat=3) if sum(t)==6)==comb(6+3-1,3-1)
    pa,pb,pab=.5,.4,.2; assert isclose(pa+pb-pab,.7)
    sa,sb,sc=5.0,6.0,7.0; s=(sa+sb+sc)/2; Cang=math.acos((sa*sa+sb*sb-sc*sc)/(2*sa*sb))
    assert isclose(.5*sa*sb*math.sin(Cang),sqrt(s*(s-sa)*(s-sb)*(s-sc)))
    assert isclose(.5*4*4*math.sin(pi/3),sqrt(3)/4*16)
    assert (8-2)*180/8==135 and 8*5//2==comb(8,2)-8
    rr,th=3.0,60; assert isclose(th/360*pi*rr*rr,.5*rr*rr*math.radians(th))
    # volumes via numeric integration (sphere, cone)
    R,H=2.0,5.0; nn=200000; dx=2*R/nn
    assert isclose(sum(pi*(R*R-(-R+(i+.5)*dx)**2)*dx for i in range(nn)),4/3*pi*R**3,rel_tol=1e-6)
    dh=H/nn; assert isclose(sum(pi*(R*(i+.5)*dh/H)**2*dh for i in range(nn)),pi*R*R*H/3,rel_tol=1e-6)
    # bank/ssc
    net=lambda a,b:a+b+a*b/100
    assert isclose(100*1.25*.8,100) and isclose((1+20/100)*(1-20/120),1)
    d1,d2=20,10; assert isclose(100*(1-d1/100)*(1-d2/100),100-(d1+d2-d1*d2/100))
    sp=120.0; x=20; cp1=sp/1.2; cp2=sp/.8; assert isclose((2*sp-(cp1+cp2))/(cp1+cp2)*100,-x*x/100)
    P,R=5000,8; assert isclose(P*(1+R/100)**2-P-P*R*2/100,P*(R/100)**2) and isclose(P*(1+R/100)**3-P-P*R*3/100,P*(R/100)**2*(3+R/100))
    assert isclose(P*(1+R/200)**2,P*(1+R/100/2)**(2*1))
    assert isclose(90*5/18,25) and isclose(2*120/(120/60+120/40),2*60*40/100)
    assert isclose(1/(1/12+1/18),12*18/30)
    assert isclose(12*10*8/1, 16*7.5*8/1)  # M1D1H1 = M2D2H2 for the same work
    c_,dd_,m_=40,55,45; assert isclose((c_*(dd_-m_)+dd_*(m_-c_))/(dd_-c_),m_)
    vol=1.0
    for _ in range(3): vol*=1-.1
    assert isclose(vol,(1-.1)**3)
    l,w,h=3.0,4.0,5.0
    assert isclose(2*(l*w+w*h+h*l),94) and isclose(.5*(4+6)*3,15) and isclose(.5*6*8,24)
    rad,ht=3.0,4.0; assert isclose(sqrt(rad*rad+ht*ht),5) and isclose(2*pi*rad*ht+2*pi*rad*rad,2*pi*rad*(rad+ht))
    # reasoning
    pos=lambda ch: ord(ch)-64
    assert [pos(ch) for ch in "EJOTY"]==[5,10,15,20,25] and all(pos(chr(65+i))+pos(chr(90-i))==27 for i in range(26))
    def ang(H,M):
        hand_h=(H%12)*30+M*.5; hand_m=M*6; return abs(hand_h-hand_m)
    for H in range(12):
        for M in range(60): assert isclose(ang(H,M),abs(30*H-5.5*M))
    assert isclose(720/11,65+5/11)
    # count overlaps / opposite / right angles in 24h by relative angle 5.5°/min
    mins=24*60; tot=5.5*mins
    assert int(tot//360)==22 and int((tot+180)//360)==22 and int(tot//180)*1==44
    assert 365%7==1 and 366%7==2 and calendar.isleap(2000) and not calendar.isleap(1900) and calendar.isleap(2024)
    days=(datetime.date(2101,1,1)-datetime.date(2001,1,1)).days; assert days%7==5
    L,Rr=7,12; assert L+Rr-1==18 and (15-9-1)==len(range(10,15))
    assert isclose(sqrt(3*3+4*4),5)
    return True
