"""Bank/SSC batch B6 (29 Oct 2026): +85 Quantitative Aptitude items (every topic to 20), IBPS/SBI PO and SSC CGL level.
Every answer is computed in this file (exact arithmetic or brute force) before the item is added."""
import math, itertools
from fractions import Fraction as F
from math import comb, factorial as fact

def build(A):
    s = "quant"
    # ================= Algebra (+10) =================
    t = "Algebra"
    sol = [(x, y) for x in range(-20, 21) for y in range(-20, 21) if 2*x + 3*y == 12 and 3*x - y == 7]; assert sol == [(3, 2)]
    A(s,t,"Easy","If 2x + 3y = 12 and 3x − y = 7, what is the value of x + y?",["5","4","6","7"],"5",
      "From the second equation, y = 3x − 7. Substituting in the first: 2x + 9x − 21 = 12, so 11x = 33 and x = 3. Then y = 9 − 7 = 2, and x + y = 5.",
      "दूसरे समीकरण से y = 3x − 7. पहले समीकरण में रखने पर: 2x + 9x − 21 = 12, इसलिए 11x = 33 और x = 3. तब y = 9 − 7 = 2, और x + y = 5.")
    d = 3; v = d**3 + 3*d; assert v == 36
    A(s,t,"Medium","If x − 1/x = 3, what is the value of x³ − 1/x³?",["36","27","30","33"],"36",
      "Use (x − 1/x)³ = x³ − 1/x³ − 3(x − 1/x). So x³ − 1/x³ = 3³ + 3 × 3 = 27 + 9 = 36.",
      "(x − 1/x)³ = x³ − 1/x³ − 3(x − 1/x) का प्रयोग करें। इसलिए x³ − 1/x³ = 3³ + 3 × 3 = 27 + 9 = 36.", chk=(v, 36))
    v = F(12**2 - 50, 2); assert v == 47
    A(s,t,"Medium","If a + b + c = 12 and a² + b² + c² = 50, what is the value of ab + bc + ca?",["47","94","45","62"],"47",
      "(a + b + c)² = a² + b² + c² + 2(ab + bc + ca). So 144 = 50 + 2(ab + bc + ca), giving ab + bc + ca = 94/2 = 47.",
      "(a + b + c)² = a² + b² + c² + 2(ab + bc + ca). इसलिए 144 = 50 + 2(ab + bc + ca), अतः ab + bc + ca = 94/2 = 47.", chk=(v, 47))
    xv = 2 + math.sqrt(3); assert abs(xv**2 + xv**-2 - 14) < 1e-9
    A(s,t,"Hard","If x = 2 + √3, what is the value of x² + 1/x²?",["14","16","12","4√3"],"14",
      "1/x = 1/(2 + √3) = (2 − √3)/(4 − 3) = 2 − √3. So x + 1/x = 4, and x² + 1/x² = (x + 1/x)² − 2 = 16 − 2 = 14.",
      "1/x = 1/(2 + √3) = (2 − √3)/(4 − 3) = 2 − √3. इसलिए x + 1/x = 4, और x² + 1/x² = (x + 1/x)² − 2 = 16 − 2 = 14.", chk=(xv**2 + xv**-2, 14))
    assert all(r*r + 2*r - 15 == 0 for r in (3, -5))
    A(s,t,"Easy","Which quadratic equation has roots 3 and −5?",["x² + 2x − 15 = 0","x² − 2x − 15 = 0","x² + 8x + 15 = 0","x² − 8x − 15 = 0"],"x² + 2x − 15 = 0",
      "Sum of roots = 3 + (−5) = −2 and product = 3 × (−5) = −15. The equation is x² − (sum)x + product = 0, i.e. x² + 2x − 15 = 0.",
      "मूलों का योग = 3 + (−5) = −2 और गुणनफल = 3 × (−5) = −15. समीकरण x² − (योग)x + गुणनफल = 0 होता है, अर्थात x² + 2x − 15 = 0.")
    a, b, c = 13, -7, -6; v = a**3 + b**3 + c**3; assert v == 3*a*b*c == 1638
    A(s,t,"Hard","If a = 13, b = −7 and c = −6, what is the value of a³ + b³ + c³?",["1638","−1638","546","2756"],"1638",
      "Here a + b + c = 13 − 7 − 6 = 0, and whenever a + b + c = 0, a³ + b³ + c³ = 3abc. So the value is 3 × 13 × (−7) × (−6) = 1638. (Directly: 2197 − 343 − 216 = 1638.)",
      "यहाँ a + b + c = 13 − 7 − 6 = 0, और जब भी a + b + c = 0 हो, a³ + b³ + c³ = 3abc होता है। इसलिए मान = 3 × 13 × (−7) × (−6) = 1638. (सीधे: 2197 − 343 − 216 = 1638.)", chk=(v, 1638))
    ks = [k for k in range(-50, 51) if k != 0 and 144 - 36*k == 0]; assert ks == [4]
    A(s,t,"Medium","For what value of k does the equation kx² − 12x + 9 = 0 have two equal roots?",["4","3","−4","6"],"4",
      "Equal roots need the discriminant to be zero: (−12)² − 4 × k × 9 = 0, i.e. 144 − 36k = 0, so k = 4.",
      "समान मूलों के लिए विविक्तकर शून्य होना चाहिए: (−12)² − 4 × k × 9 = 0, अर्थात 144 − 36k = 0, इसलिए k = 4.")
    sol = [(p, n) for p in range(1, 100) for n in range(1, 100) if 3*p + 2*n == 110 and 2*p + 3*n == 115]; assert sol == [(20, 25)]
    A(s,t,"Easy","3 pens and 2 notebooks cost ₹110, while 2 pens and 3 notebooks cost ₹115. What is the cost of one pen and one notebook together?",["₹45","₹40","₹50","₹55"],"₹45",
      "Adding the two equations: 5 pens + 5 notebooks = ₹225, so 1 pen + 1 notebook = ₹45. (Separately, a pen costs ₹20 and a notebook ₹25.)",
      "दोनों समीकरण जोड़ने पर: 5 पेन + 5 नोटबुक = ₹225, इसलिए 1 पेन + 1 नोटबुक = ₹45. (अलग-अलग, पेन ₹20 और नोटबुक ₹25 की है।)", chk=(sum(sol[0]), 45))
    xs = [x for x in range(-10, 11) if 4**x == 8**(x - 1)] if True else []; assert xs == [3]
    A(s,t,"Medium","If 4ˣ = 8⁽ˣ⁻¹⁾, what is the value of x?",["3","2","4","−3"],"3",
      "Write both sides as powers of 2: 4ˣ = 2²ˣ and 8⁽ˣ⁻¹⁾ = 2³ˣ⁻³. So 2x = 3x − 3, giving x = 3.",
      "दोनों पक्षों को 2 की घात में लिखें: 4ˣ = 2²ˣ और 8⁽ˣ⁻¹⁾ = 2³ˣ⁻³. इसलिए 2x = 3x − 3, अतः x = 3.")
    r = (6 + math.sqrt(32)) / 2; v = r**4 + r**-4; assert abs(v - 1154) < 1e-6
    A(s,t,"Hard","If x² − 6x + 1 = 0, what is the value of x⁴ + 1/x⁴?",["1154","1156","34","1150"],"1154",
      "Divide x² − 6x + 1 = 0 by x: x + 1/x = 6. Then x² + 1/x² = 6² − 2 = 34, and x⁴ + 1/x⁴ = 34² − 2 = 1156 − 2 = 1154.",
      "x² − 6x + 1 = 0 को x से भाग देने पर: x + 1/x = 6. तब x² + 1/x² = 6² − 2 = 34, और x⁴ + 1/x⁴ = 34² − 2 = 1156 − 2 = 1154.", chk=(v, 1154))
    # ================= Averages & Alligation (+7) =================
    t = "Averages & Alligation"
    v = 6*49 + 6*52 - 11*50; assert v == 56
    A(s,t,"Medium","The average of 11 results is 50. The average of the first six results is 49 and that of the last six is 52. What is the sixth result?",["56","50","52","58"],"56",
      "The sixth result is counted in both groups of six. So it equals (sum of first six) + (sum of last six) − (sum of all eleven) = 6 × 49 + 6 × 52 − 11 × 50 = 294 + 312 − 550 = 56.",
      "छठा परिणाम छह-छह के दोनों समूहों में गिना गया है। इसलिए यह (पहले छह का योग) + (अंतिम छह का योग) − (सभी ग्यारह का योग) = 6 × 49 + 6 × 52 − 11 × 50 = 294 + 312 − 550 = 56 है।", chk=(v, 56))
    m = 40.0
    for _ in range(2): m -= m * 8 / 40
    assert abs(m - 25.6) < 1e-9
    A(s,t,"Hard","A vessel contains 40 litres of pure milk. 8 litres are taken out and replaced with water, and the process is repeated once more. How much milk is now in the vessel?",["25.6 litres","24 litres","26.4 litres","28.8 litres"],"25.6 litres",
      "Each replacement keeps (40 − 8)/40 = 4/5 of the milk. After two operations, milk = 40 × (4/5)² = 40 × 16/25 = 25.6 litres.",
      "हर बार बदलने पर दूध का (40 − 8)/40 = 4/5 भाग बचता है। दो बार के बाद दूध = 40 × (4/5)² = 40 × 16/25 = 25.6 लीटर।", chk=(m, 25.6))
    v = F(5*30 - 6 - 4*6, 4); assert v == 30
    A(s,t,"Medium","The average age of a family of 5 members is 30 years. The youngest member is 6 years old. What was the average age of the family just before the youngest member was born?",["30 years","24 years","28.5 years","36 years"],"30 years",
      "Total age now = 5 × 30 = 150 years. The other four members total 150 − 6 = 144 years now; 6 years ago they totalled 144 − 4 × 6 = 120 years. Average then = 120/4 = 30 years.",
      "अभी कुल आयु = 5 × 30 = 150 वर्ष। बाकी चार सदस्यों की आयु अभी 150 − 6 = 144 वर्ष है; 6 वर्ष पहले यह 144 − 4 × 6 = 120 वर्ष थी। तब औसत = 120/4 = 30 वर्ष।", chk=(v, 30))
    v = F(sum(range(1, 30, 2)), 15); assert v == 15
    A(s,t,"Easy","What is the average of the first 15 odd natural numbers?",["15","16","14","30"],"15",
      "The sum of the first n odd numbers is n², so the sum of the first 15 is 225. Average = 225/15 = 15.",
      "पहली n विषम संख्याओं का योग n² होता है, इसलिए पहली 15 का योग 225 है। औसत = 225/15 = 15.", chk=(v, 15))
    v = 21*42 - 20*40; assert v == 82
    A(s,t,"Medium","A batsman has an average of 40 runs after 20 innings. How many runs must he score in his 21st innings to raise his average to 42?",["82","62","84","80"],"82",
      "Runs so far = 20 × 40 = 800. To average 42 after 21 innings he needs 21 × 42 = 882 runs. So he must score 882 − 800 = 82.",
      "अब तक के रन = 20 × 40 = 800. 21 पारियों के बाद 42 औसत के लिए 21 × 42 = 882 रन चाहिए। इसलिए उसे 882 − 800 = 82 रन बनाने होंगे।", chk=(v, 82))
    cp = F(66) / F(132, 100); r_ = (60 - cp) / (cp - 0); assert cp == 50 and r_ == F(1, 5)
    A(s,t,"Hard","Milk costs a milkman ₹60 per litre. In what ratio must he mix water with milk so that by selling the mixture at ₹66 per litre he makes a profit of 32%?",["1 : 5","1 : 4","1 : 6","2 : 5"],"1 : 5",
      "Cost price of the mixture = 66/1.32 = ₹50 per litre. Water costs nothing, so by alligation water : milk = (60 − 50) : (50 − 0) = 10 : 50 = 1 : 5.",
      "मिश्रण का क्रय मूल्य = 66/1.32 = ₹50 प्रति लीटर। पानी मुफ़्त है, इसलिए मिश्रण नियम से पानी : दूध = (60 − 50) : (50 − 0) = 10 : 50 = 1 : 5.", chk=(r_, 0.2))
    g = F(2, 5) + F(3, 10); cu = F(3, 5) + F(7, 10); assert g / cu == F(7, 13)
    A(s,t,"Medium","Two alloys contain gold and copper in the ratios 2 : 3 and 3 : 7 respectively. Equal weights of the two alloys are melted together. What is the ratio of gold to copper in the new alloy?",["7 : 13","5 : 10","1 : 2","6 : 11"],"7 : 13",
      "Take 1 kg of each. Gold = 2/5 + 3/10 = 7/10 kg; copper = 3/5 + 7/10 = 13/10 kg. Ratio = 7 : 13.",
      "दोनों का 1 किग्रा लें। सोना = 2/5 + 3/10 = 7/10 किग्रा; ताँबा = 3/5 + 7/10 = 13/10 किग्रा। अनुपात = 7 : 13.", chk=(g / cu, 7/13))
    # ================= Geometry & Mensuration (+8) =================
    t = "Geometry & Mensuration"
    A(s,t,"Easy","The diagonals of a rhombus are 16 cm and 12 cm. What is its area?",["96 cm²","192 cm²","48 cm²","100 cm²"],"96 cm²",
      "Area of a rhombus = (product of diagonals)/2 = 16 × 12 / 2 = 96 cm².",
      "समचतुर्भुज का क्षेत्रफल = (विकर्णों का गुणनफल)/2 = 16 × 12 / 2 = 96 cm².", chk=(16*12/2, 96))
    v = F(1, 3) * F(22, 7) * 49 * 12; assert v == 616
    A(s,t,"Medium","What is the volume of a right circular cone of base radius 7 cm and height 12 cm? (Take π = 22/7)",["616 cm³","1848 cm³","308 cm³","924 cm³"],"616 cm³",
      "Volume = (1/3)πr²h = (1/3) × (22/7) × 49 × 12 = 616 cm³.",
      "आयतन = (1/3)πr²h = (1/3) × (22/7) × 49 × 12 = 616 cm³.", chk=(v, 616))
    side = 11; per = 4*side; rr = F(per) / (2*F(22, 7)); ar = F(22, 7) * rr**2; assert rr == 7 and ar == 154
    A(s,t,"Medium","A wire bent into a square encloses an area of 121 cm². The same wire is bent into a circle. What is the area of the circle? (Take π = 22/7)",["154 cm²","121 cm²","176 cm²","144 cm²"],"154 cm²",
      "Side of the square = √121 = 11 cm, so the wire is 4 × 11 = 44 cm long. As a circle, 2πr = 44 gives r = 7 cm. Area = (22/7) × 7² = 154 cm².",
      "वर्ग की भुजा = √121 = 11 cm, इसलिए तार 4 × 11 = 44 cm लंबा है। वृत्त में 2πr = 44 से r = 7 cm. क्षेत्रफल = (22/7) × 7² = 154 cm².", chk=(ar, 154))
    n_ = F(2, 3) * 9**3 / (F(4, 3) * F(3, 2)**3); assert n_ == 108
    A(s,t,"Medium","A solid metal hemisphere of radius 9 cm is melted and recast into small solid spheres, each of radius 1.5 cm. How many spheres are obtained?",["108","216","54","72"],"108",
      "Number of spheres = volume of hemisphere / volume of one sphere = (2/3)π × 9³ ÷ [(4/3)π × 1.5³] = 486π ÷ 4.5π = 108.",
      "गोलों की संख्या = अर्धगोले का आयतन / एक गोले का आयतन = (2/3)π × 9³ ÷ [(4/3)π × 1.5³] = 486π ÷ 4.5π = 108.", chk=(n_, 108))
    ns = [n for n in range(3, 50) if (n - 2) * 180 == 1440]; assert ns == [10]
    A(s,t,"Easy","The sum of the interior angles of a polygon is 1440°. How many sides does it have?",["10","8","12","9"],"10",
      "Sum of interior angles = (n − 2) × 180°. So (n − 2) × 180 = 1440, n − 2 = 8 and n = 10.",
      "अंतः कोणों का योग = (n − 2) × 180°. इसलिए (n − 2) × 180 = 1440, n − 2 = 8 और n = 10.")
    v = math.sqrt(12**2 + 9**2 + 8**2); assert v == 17
    A(s,t,"Medium","What is the length of the longest rod that can be placed in a room 12 m long, 9 m wide and 8 m high?",["17 m","15 m","19 m","29 m"],"17 m",
      "The longest rod lies along the room's diagonal: √(12² + 9² + 8²) = √(144 + 81 + 64) = √289 = 17 m.",
      "सबसे लंबी छड़ कमरे के विकर्ण पर आएगी: √(12² + 9² + 8²) = √(144 + 81 + 64) = √289 = 17 m.", chk=(v, 17))
    v = math.sqrt(13**2 - (8 - 3)**2); assert v == 12
    A(s,t,"Hard","Two circles of radii 8 cm and 3 cm have their centres 13 cm apart. What is the length of a direct common tangent to the two circles?",["12 cm","√120 cm","5 cm","11 cm"],"12 cm",
      "Length of a direct common tangent = √(d² − (r₁ − r₂)²) = √(13² − 5²) = √(169 − 25) = √144 = 12 cm.",
      "उभयनिष्ठ अनुस्पर्श रेखा (direct common tangent) की लंबाई = √(d² − (r₁ − r₂)²) = √(13² − 5²) = √(169 − 25) = √144 = 12 cm.", chk=(v, 12))
    v = (30 + 4) * (20 + 4) - 30 * 20; assert v == 216
    A(s,t,"Medium","A path 2 m wide runs all round the outside of a rectangular garden 30 m long and 20 m wide. What is the area of the path?",["216 m²","200 m²","208 m²","232 m²"],"216 m²",
      "With the path, the outer rectangle is (30 + 4) m by (20 + 4) m = 34 m by 24 m, area 816 m². Area of path = 816 − 600 = 216 m².",
      "पथ सहित बाहरी आयत (30 + 4) m × (20 + 4) m = 34 m × 24 m है, क्षेत्रफल 816 m². पथ का क्षेत्रफल = 816 − 600 = 216 m².", chk=(v, 216))
    # ================= Number System (+9) =================
    t = "Number System"
    opts = ["5,918", "4,825", "6,173", "7,341"]; div = [o for o in opts if int(o.replace(",", "")) % 11 == 0]; assert div == ["5,918"]
    A(s,t,"Easy","Which of the following numbers is divisible by 11?",opts,"5,918",
      "A number is divisible by 11 when the difference between the sums of its alternate digits is a multiple of 11. For 5918: (5 + 1) − (9 + 8) = −11, a multiple of 11. For 4825, 6173 and 7341 the differences are −7, 9 and 7. (5918 = 11 × 538.)",
      "कोई संख्या 11 से विभाज्य होती है जब उसके एकांतर अंकों के योगों का अंतर 11 का गुणज हो। 5918 के लिए: (5 + 1) − (9 + 8) = −11, जो 11 का गुणज है। 4825, 6173 और 7341 के लिए अंतर −7, 9 और 7 हैं। (5918 = 11 × 538.)")
    alt = lambda n: sum(int(c) for c in str(n)[0::2]) - sum(int(c) for c in str(n)[1::2])
    assert 5918 == 11 * 538 and [alt(n) for n in (5918, 4825, 6173, 7341)] == [-11, -7, 9, 7]
    from math import gcd as _g
    hs = [h for h in range(1, 200) if (3*h*5*h)//_g(3*h, 5*h) == 225]; assert hs == [15]
    A(s,t,"Easy","Two numbers are in the ratio 3 : 5 and their LCM is 225. What is their HCF?",["15","45","9","25"],"15",
      "Let the numbers be 3h and 5h, where h is the HCF (3 and 5 are co-prime). Their LCM = 15h = 225, so h = 15.",
      "माना संख्याएँ 3h और 5h हैं, जहाँ h HCF है (3 और 5 सहअभाज्य हैं)। उनका LCM = 15h = 225, इसलिए h = 15.", chk=(hs[0], 15))
    v = sum(1 for n in range(1, 301) if (n % 3 == 0) != (n % 5 == 0)); assert v == 120
    A(s,t,"Hard","How many integers from 1 to 300 are divisible by 3 or by 5, but not by both?",["120","140","160","100"],"120",
      "Multiples of 3: 100. Multiples of 5: 60. Multiples of both (i.e. of 15): 20. Divisible by exactly one = 100 + 60 − 2 × 20 = 120.",
      "3 के गुणज: 100. 5 के गुणज: 60. दोनों के (यानी 15 के) गुणज: 20. ठीक एक से विभाज्य = 100 + 60 − 2 × 20 = 120.", chk=(v, 120))
    v = (-1056) % 23; assert v == 2
    A(s,t,"Easy","What is the least number that must be added to 1,056 to make it exactly divisible by 23?",["2","21","3","4"],"2",
      "1,056 = 23 × 45 + 21, so the remainder is 21. Adding 23 − 21 = 2 gives 1,058 = 23 × 46.",
      "1,056 = 23 × 45 + 21, इसलिए शेषफल 21 है। 23 − 21 = 2 जोड़ने पर 1,058 = 23 × 46 मिलता है।", chk=(v, 2))
    v = sum(1 for d in range(1, 541) if 540 % d == 0 and d % 2 == 0); assert v == 16
    A(s,t,"Medium","How many even factors does 540 have?",["16","24","8","12"],"16",
      "540 = 2² × 3³ × 5. An even factor must contain 2¹ or 2², so there are 2 choices for the power of 2, 4 for the power of 3 and 2 for the power of 5: 2 × 4 × 2 = 16.",
      "540 = 2² × 3³ × 5. सम गुणनखंड में 2¹ या 2² होना चाहिए, इसलिए 2 की घात के 2 विकल्प, 3 की घात के 4 और 5 की घात के 2 विकल्प हैं: 2 × 4 × 2 = 16.", chk=(v, 16))
    v = max(n for n in range(1000, 10000) if n % 12 == 0 and n % 15 == 0 and n % 18 == 0); assert v == 9900
    A(s,t,"Medium","What is the largest four-digit number that is exactly divisible by each of 12, 15 and 18?",["9900","9720","9990","9960"],"9900",
      "LCM of 12, 15 and 18 = 180. 9,999 = 180 × 55 + 99, so the largest multiple of 180 with four digits is 9,999 − 99 = 9,900.",
      "12, 15 और 18 का LCM = 180. 9,999 = 180 × 55 + 99, इसलिए 180 का सबसे बड़ा चार अंकों वाला गुणज 9,999 − 99 = 9,900 है।", chk=(v, 9900))
    v = (pow(3, 65, 10) * pow(6, 59, 10) * pow(7, 71, 10)) % 10; assert v == 4
    A(s,t,"Hard","What is the unit digit of 3⁶⁵ × 6⁵⁹ × 7⁷¹?",["4","8","2","6"],"4",
      "Unit digits of powers of 3 and of 7 repeat every 4. 65 = 4 × 16 + 1, so 3⁶⁵ ends in 3. Every power of 6 ends in 6. 71 = 4 × 17 + 3, so 7⁷¹ ends like 7³ = 343, in 3. The product ends like 3 × 6 × 3 = 54, so the unit digit is 4.",
      "3 और 7 की घातों के इकाई अंक हर 4 पर दोहराते हैं। 65 = 4 × 16 + 1, इसलिए 3⁶⁵ का इकाई अंक 3 है। 6 की हर घात का इकाई अंक 6 है। 71 = 4 × 17 + 3, इसलिए 7⁷¹ का इकाई अंक 7³ = 343 जैसा, यानी 3 है। गुणनफल का इकाई अंक 3 × 6 × 3 = 54 जैसा, यानी 4 है।", chk=(v, 4))
    v = F(36, 99); assert v == F(4, 11)
    A(s,t,"Easy","Which fraction is equal to the recurring decimal 0.363636…?",["4/11","9/25","36/100","3/8"],"4/11",
      "For a two-digit repeating block, 0.3636… = 36/99. Dividing numerator and denominator by 9 gives 4/11.",
      "दो अंकों के आवर्ती खंड के लिए 0.3636… = 36/99. अंश और हर को 9 से भाग देने पर 4/11 मिलता है।", chk=(v, 4/11))
    rs = {n % 12 for n in range(19, 5000, 36)}; assert rs == {7}
    A(s,t,"Medium","A number leaves a remainder of 19 when divided by 36. What remainder does it leave when divided by 12?",["7","19","5","Cannot be determined"],"7",
      "The number is 36k + 19 for some whole number k. Since 36 is a multiple of 12, the remainder on division by 12 is the remainder of 19, which is 7.",
      "संख्या किसी पूर्ण संख्या k के लिए 36k + 19 है। 36, 12 का गुणज है, इसलिए 12 से भाग देने पर शेषफल 19 का शेषफल यानी 7 होगा।")
    # ================= Percentages (+4) =================
    t = "Percentages"
    v = 0.6*30 + 0.4*40; assert abs(v - 34) < 1e-9
    A(s,t,"Medium","In a school, 60% of the students are boys. If 30% of the boys and 40% of the girls take part in sports, what percentage of all the students take part in sports?",["34%","35%","36%","70%"],"34%",
      "Take 100 students: 60 boys and 40 girls. Boys in sports = 30% of 60 = 18; girls = 40% of 40 = 16. Total 34 out of 100, i.e. 34%.",
      "100 छात्र लें: 60 लड़के और 40 लड़कियाँ। खेल में लड़के = 60 का 30% = 18; लड़कियाँ = 40 का 40% = 16. कुल 100 में से 34, यानी 34%.", chk=(v, 34))
    e0 = 100 - 20; e1 = 125 - 20 * 1.5; v = (e1 - e0) / e0 * 100; assert abs(v - 18.75) < 1e-9
    A(s,t,"Hard","A man saves 20% of his income. His income increases by 25% and his savings increase by 50%. By what percentage does his expenditure increase?",["18.75%","20%","15%","25%"],"18.75%",
      "Take income = 100: savings 20, expenditure 80. New income = 125 and new savings = 30, so new expenditure = 95. Increase = 15 on 80, which is 18.75%.",
      "आय = 100 लें: बचत 20, खर्च 80. नई आय = 125 और नई बचत = 30, इसलिए नया खर्च = 95. वृद्धि = 80 पर 15, यानी 18.75%.", chk=(v, 18.75))
    v = F(20 * 400, 250); assert v == 32
    A(s,t,"Easy","If x% of 250 is equal to 20% of 400, what is x?",["32","30","25","40"],"32",
      "20% of 400 = 80. x% of 250 = 80 gives x = 80 × 100 / 250 = 32.",
      "400 का 20% = 80. 250 का x% = 80 से x = 80 × 100 / 250 = 32.", chk=(v, 32))
    Nv = (2000 / (0.55 - 0.45) + 500) / 0.8; assert abs(Nv - 25625) < 1e-6
    A(s,t,"Hard","In an election between two candidates, 20% of the voters on the list did not vote and 500 of the votes cast were invalid. The winner got 55% of the valid votes and won by 2,000 votes. How many voters were on the list?",["25,625","25,000","26,250","24,375"],"25,625",
      "The margin is 55% − 45% = 10% of the valid votes, so valid votes = 2,000 / 0.1 = 20,000. Votes cast = 20,000 + 500 = 20,500, which is 80% of the list. List = 20,500 / 0.8 = 25,625.",
      "अंतर वैध मतों का 55% − 45% = 10% है, इसलिए वैध मत = 2,000 / 0.1 = 20,000. डाले गए मत = 20,000 + 500 = 20,500, जो सूची का 80% है। सूची = 20,500 / 0.8 = 25,625.", chk=(Nv, 25625))
    # ================= Permutations & Combinations (+8) =================
    t = "Permutations & Combinations"
    w = "ARTICLE"; cnt = len({p for p in itertools.permutations(w) if all(p[i] in "AIE" for i in (1, 3, 5))}); assert cnt == 144
    A(s,t,"Medium","In how many ways can the letters of the word ARTICLE be arranged so that the vowels occupy only the even positions?",["144","72","288","576"],"144",
      "ARTICLE has 7 letters, with 3 vowels (A, I, E) and 4 consonants. There are exactly 3 even positions (2nd, 4th and 6th), so the vowels fill them in 3! = 6 ways and the consonants fill the other 4 places in 4! = 24 ways. Total = 6 × 24 = 144.",
      "ARTICLE में 7 अक्षर हैं, जिनमें 3 स्वर (A, I, E) और 4 व्यंजन हैं। सम स्थान ठीक 3 हैं (2वाँ, 4था और 6वाँ), इसलिए स्वर उन्हें 3! = 6 तरीकों से और व्यंजन बाकी 4 स्थान 4! = 24 तरीकों से भरते हैं। कुल = 6 × 24 = 144.", chk=(cnt, 144))
    v = comb(6, 2) * comb(5, 2); assert v == 150
    A(s,t,"Easy","A team of 4 is to be selected from 6 boys and 5 girls so that it has exactly 2 boys and 2 girls. In how many ways can this be done?",["150","330","60","120"],"150",
      "Choose 2 of the 6 boys in C(6, 2) = 15 ways and 2 of the 5 girls in C(5, 2) = 10 ways. Total = 15 × 10 = 150.",
      "6 लड़कों में से 2 को C(6, 2) = 15 तरीकों से और 5 लड़कियों में से 2 को C(5, 2) = 10 तरीकों से चुनें। कुल = 15 × 10 = 150.", chk=(v, 150))
    # circular: fix person 0 at seat 0, arrange the other 6 in seats 1..6; persons 1 and 2 must not be adjacent on a circle of 7
    cnt = 0
    for p in itertools.permutations(range(1, 7)):
        seat = {0: 0}; seat.update({q: i + 1 for i, q in enumerate(p)})
        if (seat[1] - seat[2]) % 7 not in (1, 6): cnt += 1
    assert cnt == 480 == fact(6) - 2 * fact(5)
    A(s,t,"Hard","In how many ways can 7 people sit around a round table if two particular people must not sit next to each other?",["480","720","240","600"],"480",
      "Without any condition, 7 people can sit round a table in (7 − 1)! = 720 ways. If the two sit together, treat them as one unit: (6 − 1)! = 120 arrangements, times 2 for their order = 240. So the arrangements with them apart = 720 − 240 = 480.",
      "बिना शर्त 7 लोग गोल मेज़ पर (7 − 1)! = 720 तरीकों से बैठ सकते हैं। यदि दोनों साथ बैठें तो उन्हें एक इकाई मानें: (6 − 1)! = 120 व्यवस्थाएँ, उनके क्रम के लिए 2 से गुणा = 240. इसलिए अलग बैठने के तरीके = 720 − 240 = 480.", chk=(cnt, 480))
    v = comb(10, 3) - comb(4, 3); assert v == 116
    A(s,t,"Medium","Ten points are marked in a plane, and no three of them are in a straight line except four of them, which all lie on one line. How many triangles can be formed with vertices among these points?",["116","120","112","110"],"116",
      "Any 3 of the 10 points would form a triangle, C(10, 3) = 120 choices, except the triples taken from the 4 collinear points, which give no triangle: C(4, 3) = 4. Triangles = 120 − 4 = 116.",
      "10 बिंदुओं में से कोई भी 3 बिंदु त्रिभुज बनाते, C(10, 3) = 120 विकल्प, सिवाय 4 संरेख बिंदुओं से लिए गए त्रिकों के, जो त्रिभुज नहीं बनाते: C(4, 3) = 4. त्रिभुज = 120 − 4 = 116.", chk=(v, 116))
    v = sum(1 for n in range(1000, 10000) if n % 2 == 0 and len(set(str(n))) == 4); assert v == 2296
    A(s,t,"Hard","How many four-digit even numbers have all four digits different?",["2296","2520","2016","4536"],"2296",
      "Split on the last digit. If it is 0: the other three places can be filled in 9 × 8 × 7 = 504 ways. If it is 2, 4, 6 or 8 (4 choices): the first digit can be anything except 0 and the last digit (8 choices), then 8 and 7 choices remain, giving 4 × 8 × 8 × 7 = 1792. Total = 504 + 1792 = 2296.",
      "अंतिम अंक के आधार पर बाँटें। यदि वह 0 है: बाकी तीन स्थान 9 × 8 × 7 = 504 तरीकों से भरे जा सकते हैं। यदि वह 2, 4, 6 या 8 है (4 विकल्प): पहला अंक 0 और अंतिम अंक के सिवा कुछ भी (8 विकल्प), फिर 8 और 7 विकल्प बचते हैं, कुल 4 × 8 × 8 × 7 = 1792. कुल = 504 + 1792 = 2296.", chk=(v, 2296))
    v = comb(12, 2); assert v == 66
    A(s,t,"Easy","At a meeting, each of 12 people shakes hands once with every other person. How many handshakes take place?",["66","132","144","72"],"66",
      "Each handshake is a pair of people, so the number of handshakes = C(12, 2) = 12 × 11 / 2 = 66.",
      "हर हाथ मिलाना दो लोगों की एक जोड़ी है, इसलिए हाथ मिलाने की संख्या = C(12, 2) = 12 × 11 / 2 = 66.", chk=(v, 66))
    v = 3**5; assert v == 243 == len(list(itertools.product(range(3), repeat=5)))
    A(s,t,"Medium","In how many ways can 5 different books be given to 3 students if a student may receive any number of books, including none?",["243","125","60","15"],"243",
      "Each of the 5 books can go to any of the 3 students independently, so the number of ways = 3 × 3 × 3 × 3 × 3 = 3⁵ = 243.",
      "5 किताबों में से हर किताब 3 छात्रों में से किसी को भी स्वतंत्र रूप से दी जा सकती है, इसलिए तरीके = 3 × 3 × 3 × 3 × 3 = 3⁵ = 243.", chk=(v, 243))
    v = fact(11) // (fact(4) * fact(4) * fact(2)); assert v == 34650
    A(s,t,"Medium","In how many different ways can the letters of the word MISSISSIPPI be arranged?",["34650","39916800","69300","17325"],"34650",
      "MISSISSIPPI has 11 letters: M once, I four times, S four times and P twice. Arrangements = 11! / (4! × 4! × 2!) = 39916800 / 1152 = 34650.",
      "MISSISSIPPI में 11 अक्षर हैं: M एक बार, I चार बार, S चार बार और P दो बार। व्यवस्थाएँ = 11! / (4! × 4! × 2!) = 39916800 / 1152 = 34650.", chk=(v, 34650))
    # ================= Probability (+9) =================
    t = "Probability"
    v = F(comb(13, 2), comb(52, 2)); assert v == F(1, 17)
    A(s,t,"Medium","Two cards are drawn at random, without replacement, from a well-shuffled pack of 52 cards. What is the probability that both are hearts?",["1/17","1/16","1/4","13/102"],"1/17",
      "Ways to pick 2 hearts = C(13, 2) = 78; ways to pick any 2 cards = C(52, 2) = 1326. Probability = 78/1326 = 1/17.",
      "2 पान (hearts) चुनने के तरीके = C(13, 2) = 78; कोई भी 2 पत्ते चुनने के तरीके = C(52, 2) = 1326. प्रायिकता = 78/1326 = 1/17.", chk=(v, 1/17))
    v = F(2, 6); assert v == F(1, 3)
    A(s,t,"Easy","A fair die is thrown once. What is the probability of getting a number greater than 4?",["1/3","1/2","2/3","1/6"],"1/3",
      "Only 5 and 6 are greater than 4: 2 favourable outcomes out of 6. Probability = 2/6 = 1/3.",
      "केवल 5 और 6 ही 4 से बड़े हैं: 6 में से 2 अनुकूल परिणाम। प्रायिकता = 2/6 = 1/3.", chk=(v, 1/3))
    v = F(2, 7)
    A(s,t,"Medium","What is the probability that a leap year, chosen at random, has 53 Sundays?",["2/7","1/7","3/7","1/2"],"2/7",
      "A leap year has 366 days = 52 weeks and 2 extra days. The 2 extra days are one of 7 equally likely pairs (Sunday–Monday, Monday–Tuesday, …, Saturday–Sunday), and 2 of these pairs contain a Sunday. Probability = 2/7.",
      "लीप वर्ष में 366 दिन = 52 सप्ताह और 2 अतिरिक्त दिन होते हैं। ये 2 अतिरिक्त दिन 7 समान संभावित जोड़ियों (रविवार–सोमवार, सोमवार–मंगलवार, …, शनिवार–रविवार) में से एक हैं, और इनमें से 2 जोड़ियों में रविवार है। प्रायिकता = 2/7.")
    days = ["Su","Mo","Tu","We","Th","Fr","Sa"]; assert sum(1 for i in range(7) if "Su" in (days[i], days[(i+1) % 7])) == 2
    v = 1 - F(2, 3) * F(3, 4); assert v == F(1, 2)
    A(s,t,"Medium","The probabilities that A and B can solve a problem are 1/3 and 1/4 respectively. If both try it independently, what is the probability that the problem gets solved?",["1/2","7/12","1/12","5/12"],"1/2",
      "The problem stays unsolved only if both fail: (1 − 1/3)(1 − 1/4) = (2/3)(3/4) = 1/2. So the probability that it is solved = 1 − 1/2 = 1/2.",
      "समस्या तभी अनसुलझी रहेगी जब दोनों असफल हों: (1 − 1/3)(1 − 1/4) = (2/3)(3/4) = 1/2. इसलिए हल होने की प्रायिकता = 1 − 1/2 = 1/2.", chk=(v, 0.5))
    v = F(sum(1 for r in itertools.product(range(6), repeat=3) if len(set(r)) == 1), 216); assert v == F(1, 36)
    A(s,t,"Medium","Three fair dice are thrown together. What is the probability that all three show the same number?",["1/36","1/216","1/6","1/18"],"1/36",
      "There are 6³ = 216 equally likely outcomes, and 6 of them show the same number on all three dice (1-1-1 up to 6-6-6). Probability = 6/216 = 1/36.",
      "कुल 6³ = 216 समान संभावित परिणाम हैं, और उनमें से 6 में तीनों पासों पर एक ही संख्या है (1-1-1 से 6-6-6 तक)। प्रायिकता = 6/216 = 1/36.", chk=(v, 1/36))
    v = F(4 * 5 * 6, comb(15, 3)); assert v == F(24, 91)
    A(s,t,"Hard","A bag contains 4 red, 5 green and 6 blue balls. Three balls are drawn at random. What is the probability that they are of three different colours?",["24/91","4/15","12/91","8/65"],"24/91",
      "Ways to draw one ball of each colour = 4 × 5 × 6 = 120. Ways to draw any 3 of the 15 balls = C(15, 3) = 455. Probability = 120/455 = 24/91.",
      "हर रंग की एक गेंद निकालने के तरीके = 4 × 5 × 6 = 120. 15 गेंदों में से कोई 3 निकालने के तरीके = C(15, 3) = 455. प्रायिकता = 120/455 = 24/91.", chk=(v, 24/91))
    perms = list(itertools.permutations("PRIDE")); fav = sum(1 for p in perms if abs(p.index("I") - p.index("E")) == 1); v = F(fav, len(perms)); assert v == F(2, 5)
    A(s,t,"Hard","The letters of the word PRIDE are arranged at random. What is the probability that the two vowels come together?",["2/5","1/5","3/5","1/10"],"2/5",
      "Total arrangements = 5! = 120. With I and E together, treat them as one unit: 4! = 24 arrangements, times 2 for their order = 48. Probability = 48/120 = 2/5.",
      "कुल व्यवस्थाएँ = 5! = 120. I और E साथ हों तो उन्हें एक इकाई मानें: 4! = 24 व्यवस्थाएँ, उनके क्रम के लिए 2 से गुणा = 48. प्रायिकता = 48/120 = 2/5.", chk=(v, 0.4))
    v = F(sum(1 for r in itertools.product("HT", repeat=2) if r.count("H") <= 1), 4); assert v == F(3, 4)
    A(s,t,"Easy","Two fair coins are tossed together. What is the probability of getting at most one head?",["3/4","1/2","1/4","2/3"],"3/4",
      "The four equally likely outcomes are HH, HT, TH and TT. All except HH have at most one head, so the probability = 3/4.",
      "चार समान संभावित परिणाम HH, HT, TH और TT हैं। HH को छोड़कर सभी में अधिक-से-अधिक एक चित है, इसलिए प्रायिकता = 3/4.", chk=(v, 0.75))
    v = F(sum(1 for n in range(1, 51) if n % 4 == 0 or n % 6 == 0), 50); assert v == F(8, 25)
    A(s,t,"Medium","A number is chosen at random from 1 to 50. What is the probability that it is divisible by 4 or by 6?",["8/25","2/5","1/3","9/25"],"8/25",
      "Multiples of 4: 12. Multiples of 6: 8. Multiples of both, i.e. of 12: 4. Favourable = 12 + 8 − 4 = 16, so the probability = 16/50 = 8/25.",
      "4 के गुणज: 12. 6 के गुणज: 8. दोनों के, यानी 12 के गुणज: 4. अनुकूल = 12 + 8 − 4 = 16, इसलिए प्रायिकता = 16/50 = 8/25.", chk=(v, 0.32))
    # ================= Profit & Loss (+4) =================
    t = "Profit & Loss"
    v = F(11, 33 - 11) * 100; assert v == 50
    A(s,t,"Hard","By selling 33 metres of cloth, a shopkeeper gains the selling price of 11 metres. What is his gain percentage?",["50%","33⅓%","25%","66⅔%"],"50%",
      "Selling price of 33 m − cost price of 33 m = selling price of 11 m, so the cost price of 33 m = selling price of 22 m. Gain on the cost of 22 m is the price of 11 m: 11/22 × 100 = 50%.",
      "33 मीटर का विक्रय मूल्य − 33 मीटर का क्रय मूल्य = 11 मीटर का विक्रय मूल्य, इसलिए 33 मीटर का क्रय मूल्य = 22 मीटर का विक्रय मूल्य। 22 मीटर की लागत पर लाभ 11 मीटर का मूल्य है: 11/22 × 100 = 50%.", chk=(v, 50))
    v = F(20 - 16, 16) * 100; assert v == 25
    A(s,t,"Medium","The cost price of 20 articles equals the selling price of 16 articles. What is the profit percentage?",["25%","20%","16%","4%"],"25%",
      "Let each article cost ₹1, so 20 articles cost ₹20, which is what 16 articles sell for. Profit on 16 articles = 20 − 16 = 4 on a cost of 16, i.e. 4/16 × 100 = 25%.",
      "माना हर वस्तु का मूल्य ₹1 है, तो 20 वस्तुओं का मूल्य ₹20 है, जो 16 वस्तुओं का विक्रय मूल्य है। 16 वस्तुओं पर लाभ = 20 − 16 = 4, लागत 16 पर, यानी 4/16 × 100 = 25%.", chk=(v, 25))
    cp = F(90) / F(15, 100); assert cp == 600
    A(s,t,"Medium","A shopkeeper sells an article at a loss of 10%. Had he sold it for ₹90 more, he would have gained 5%. What is the cost price?",["₹600","₹900","₹450","₹750"],"₹600",
      "The difference between a 5% gain and a 10% loss is 15% of the cost price, and this equals ₹90. Cost price = 90 / 0.15 = ₹600.",
      "5% लाभ और 10% हानि का अंतर क्रय मूल्य का 15% है, और यह ₹90 के बराबर है। क्रय मूल्य = 90 / 0.15 = ₹600.", chk=(cp, 600))
    g = F(110, 90) - 1; assert g == F(2, 9)
    A(s,t,"Hard","A dealer cheats by 10% while buying and also by 10% while selling, using false weights. What is his overall gain percentage?",["22 2/9%","20%","21%","11 1/9%"],"22 2/9%",
      "While buying he takes 1100 g but pays for 1000 g; while selling he gives 900 g but charges for 1000 g. So 1100 g, bought for the price of 1000 g, sells for the price of 1100/900 × 1000 g. Gain = 1100/900 − 1 = 2/9 = 22 2/9%.",
      "खरीदते समय वह 1000 g का मूल्य देकर 1100 g लेता है; बेचते समय 1000 g का मूल्य लेकर 900 g देता है। इसलिए 1000 g के मूल्य में खरीदा गया 1100 g, 1100/900 × 1000 g के मूल्य पर बिकता है। लाभ = 1100/900 − 1 = 2/9 = 22 2/9%.", chk=(g, 2/9))
    # ================= Ratio & Proportion (+9) =================
    t = "Ratio & Proportion"
    v = F(9 * 12, 4); assert v == 27
    A(s,t,"Easy","What is the fourth proportional to 4, 9 and 12?",["27","24","36","16"],"27",
      "If x is the fourth proportional, 4 : 9 = 12 : x, so 4x = 9 × 12 = 108 and x = 27.",
      "यदि x चतुर्थानुपाती है, तो 4 : 9 = 12 : x, इसलिए 4x = 9 × 12 = 108 और x = 27.", chk=(v, 27))
    k = F(128, 5 * 1 + 2 * 3 + 1 * 5); assert k == 8 and 3 * k == 24
    A(s,t,"Medium","A purse contains ₹5, ₹2 and ₹1 coins in the ratio 1 : 3 : 5 by number. If the total value is ₹128, how many ₹2 coins are there?",["24","8","40","32"],"24",
      "Let the numbers be k, 3k and 5k. Value = 5k + 2 × 3k + 1 × 5k = 16k = 128, so k = 8. Number of ₹2 coins = 3 × 8 = 24.",
      "माना संख्याएँ k, 3k और 5k हैं। मूल्य = 5k + 2 × 3k + 1 × 5k = 16k = 128, इसलिए k = 8. ₹2 के सिक्के = 3 × 8 = 24.", chk=(3 * k, 24))
    ks = [k for k in range(1, 50) if 6 * (3*k + 10) == 5 * (4*k + 10)]; assert ks == [5]
    A(s,t,"Medium","The present ages of A and B are in the ratio 3 : 4. Ten years from now, the ratio will be 5 : 6. What is B's present age?",["20 years","15 years","25 years","30 years"],"20 years",
      "Let the ages be 3k and 4k. Then (3k + 10)/(4k + 10) = 5/6, so 18k + 60 = 20k + 50 and k = 5. B's present age = 4 × 5 = 20 years.",
      "माना आयु 3k और 4k है। तब (3k + 10)/(4k + 10) = 5/6, इसलिए 18k + 60 = 20k + 50 और k = 5. B की वर्तमान आयु = 4 × 5 = 20 वर्ष।", chk=(4 * ks[0], 20))
    a_ = 20000 * 12; b_ = 30000 * 8; sh = F(18000 * a_, a_ + b_); assert sh == 9000
    A(s,t,"Medium","A invests ₹20,000 for 12 months and B invests ₹30,000 for 8 months in a business. Out of a total profit of ₹18,000, what is A's share?",["₹9,000","₹7,200","₹10,800","₹6,000"],"₹9,000",
      "Profit is shared in the ratio of capital × time: A = 20,000 × 12 = 2,40,000 and B = 30,000 × 8 = 2,40,000. The ratio is 1 : 1, so A gets half of ₹18,000 = ₹9,000.",
      "लाभ पूँजी × समय के अनुपात में बँटता है: A = 20,000 × 12 = 2,40,000 और B = 30,000 × 8 = 2,40,000. अनुपात 1 : 1 है, इसलिए A को ₹18,000 का आधा = ₹9,000 मिलता है।", chk=(sh, 9000))
    ks = [k for k in range(1, 20000) if 5 * (3*k + 4000) == 4 * (4*k + 4000)]; assert ks == [4000]
    A(s,t,"Medium","The salaries of A and B are in the ratio 3 : 4. If each gets an increment of ₹4,000, the ratio becomes 4 : 5. What is A's present salary?",["₹12,000","₹16,000","₹9,000","₹15,000"],"₹12,000",
      "Let the salaries be 3k and 4k. Then (3k + 4,000)/(4k + 4,000) = 4/5, so 15k + 20,000 = 16k + 16,000 and k = 4,000. A's salary = 3 × 4,000 = ₹12,000.",
      "माना वेतन 3k और 4k हैं। तब (3k + 4,000)/(4k + 4,000) = 4/5, इसलिए 15k + 20,000 = 16k + 16,000 और k = 4,000. A का वेतन = 3 × 4,000 = ₹12,000.", chk=(3 * ks[0], 12000))
    v = F(36 * 36, 16); assert v == 81
    A(s,t,"Easy","What is the third proportional to 16 and 36?",["81","56","64","72"],"81",
      "If x is the third proportional, 16 : 36 = 36 : x, so x = 36 × 36 / 16 = 1296/16 = 81.",
      "यदि x तृतीयानुपाती है, तो 16 : 36 = 36 : x, इसलिए x = 36 × 36 / 16 = 1296/16 = 81.", chk=(v, 81))
    k = F(2 * 14, 21); c = 14 - 6 * k; assert c == 6
    A(s,t,"Hard","If (a + b) : (b + c) : (c + a) = 6 : 7 : 8 and a + b + c = 14, what is the value of c?",["6","7","8","4"],"6",
      "Let a + b = 6k, b + c = 7k and c + a = 8k. Adding, 2(a + b + c) = 21k, so 28 = 21k and k = 4/3. Then a + b = 8 and c = 14 − 8 = 6.",
      "माना a + b = 6k, b + c = 7k और c + a = 8k. जोड़ने पर 2(a + b + c) = 21k, इसलिए 28 = 21k और k = 4/3. तब a + b = 8 और c = 14 − 8 = 6.", chk=(c, 6))
    sol = [(x, y) for x in range(1, 5000) for y in [2*x - 1000] if y > 0 and 5*x - 3*y == 2000]; assert sol == [(1000, 1000)]
    A(s,t,"Medium","The incomes of A and B are in the ratio 5 : 4 and their expenditures are in the ratio 3 : 2. If each of them saves ₹2,000, what is A's income?",["₹5,000","₹4,000","₹6,000","₹10,000"],"₹5,000",
      "Let incomes be 5x and 4x and expenditures 3y and 2y. Then 5x − 3y = 2,000 and 4x − 2y = 2,000. From the second, y = 2x − 1,000; substituting, 5x − 6x + 3,000 = 2,000, so x = 1,000. A's income = 5 × 1,000 = ₹5,000.",
      "माना आय 5x और 4x तथा व्यय 3y और 2y हैं। तब 5x − 3y = 2,000 और 4x − 2y = 2,000. दूसरे से y = 2x − 1,000; रखने पर 5x − 6x + 3,000 = 2,000, इसलिए x = 1,000. A की आय = 5 × 1,000 = ₹5,000.", chk=(5 * sol[0][0], 5000))
    m = F(3240, 2 + 3 + 4); assert m == 360 and 2 * m == F(2, 3) * 3 * m and 3 * m == F(3, 4) * 4 * m
    A(s,t,"Medium","₹3,240 is divided among A, B and C so that A gets 2/3 of B's share and B gets 3/4 of C's share. What is A's share?",["₹720","₹1,080","₹1,440","₹960"],"₹720",
      "Let C = 4m. Then B = 3/4 × 4m = 3m and A = 2/3 × 3m = 2m, so A : B : C = 2 : 3 : 4. A's share = 2/9 × 3,240 = ₹720.",
      "माना C = 4m. तब B = 3/4 × 4m = 3m और A = 2/3 × 3m = 2m, इसलिए A : B : C = 2 : 3 : 4. A का भाग = 2/9 × 3,240 = ₹720.", chk=(2 * m, 720))
    # ================= Simple & Compound Interest (+6) =================
    t = "Simple & Compound Interest"
    v = 16000 * 1.05**3 - 16000; assert abs(v - 2522) < 1e-6
    A(s,t,"Medium","What is the compound interest on ₹16,000 for 1½ years at 10% per annum, compounded half-yearly?",["₹2,522","₹2,400","₹2,480","₹2,560"],"₹2,522",
      "Half-yearly compounding at 10% a year means 5% per half-year for 3 half-years. Amount = 16,000 × 1.05³ = 16,000 × 1.157625 = ₹18,522. CI = 18,522 − 16,000 = ₹2,522.",
      "10% वार्षिक की अर्धवार्षिक चक्रवृद्धि का अर्थ है 3 छमाहियों के लिए 5% प्रति छमाही। मिश्रधन = 16,000 × 1.05³ = 16,000 × 1.157625 = ₹18,522. चक्रवृद्धि ब्याज = 18,522 − 16,000 = ₹2,522.", chk=(v, 2522))
    r_ = F(6655, 6050) - 1; P = F(6050) / (1 + r_)**2; assert r_ == F(1, 10) and P == 5000
    A(s,t,"Hard","A sum of money at compound interest amounts to ₹6,050 in 2 years and to ₹6,655 in 3 years. What is the sum?",["₹5,000","₹5,500","₹4,500","₹4,800"],"₹5,000",
      "Interest earned in the third year = 6,655 − 6,050 = ₹605, which is the interest on ₹6,050 for one year: 605/6,050 = 10%. Then the principal = 6,050 / 1.1² = 6,050 / 1.21 = ₹5,000.",
      "तीसरे वर्ष का ब्याज = 6,655 − 6,050 = ₹605, जो ₹6,050 पर एक वर्ष का ब्याज है: 605/6,050 = 10%. तब मूलधन = 6,050 / 1.1² = 6,050 / 1.21 = ₹5,000.", chk=(P, 5000))
    v = F(5200 - 4000, 4000 * 6) * 100; assert v == 5
    A(s,t,"Easy","In how many years will ₹4,000 amount to ₹5,200 at 6% per annum simple interest?",["5 years","4 years","6 years","3 years"],"5 years",
      "Interest needed = 5,200 − 4,000 = ₹1,200. Interest per year = 6% of 4,000 = ₹240. Time = 1,200 / 240 = 5 years.",
      "आवश्यक ब्याज = 5,200 − 4,000 = ₹1,200. प्रति वर्ष ब्याज = 4,000 का 6% = ₹240. समय = 1,200 / 240 = 5 वर्ष।", chk=(v, 5))
    v = 5000 * 1.1**3 - 5000 - 5000 * 0.1 * 3; assert abs(v - 155) < 1e-6
    A(s,t,"Medium","What is the difference between the compound interest and the simple interest on ₹5,000 for 3 years at 10% per annum?",["₹155","₹150","₹50","₹165"],"₹155",
      "SI = 5,000 × 10 × 3 / 100 = ₹1,500. Amount at CI = 5,000 × 1.1³ = ₹6,655, so CI = ₹1,655. Difference = 1,655 − 1,500 = ₹155.",
      "साधारण ब्याज = 5,000 × 10 × 3 / 100 = ₹1,500. चक्रवृद्धि मिश्रधन = 5,000 × 1.1³ = ₹6,655, इसलिए चक्रवृद्धि ब्याज = ₹1,655. अंतर = 1,655 − 1,500 = ₹155.", chk=(v, 155))
    sol = [a for a in range(1, 10800) if a * 8 * 3 == (10800 - a) * 6 * 5]; assert sol == [6000]
    A(s,t,"Medium","₹10,800 is split into two parts so that the simple interest on the first part at 8% per annum for 3 years equals the simple interest on the second part at 6% per annum for 5 years. What is the first part?",["₹6,000","₹4,800","₹5,400","₹6,400"],"₹6,000",
      "Interest on the first part = a × 8 × 3 / 100 = 24a/100; on the second = b × 6 × 5 / 100 = 30b/100. Equal interests give 24a = 30b, so a : b = 5 : 4. First part = 5/9 × 10,800 = ₹6,000.",
      "पहले भाग पर ब्याज = a × 8 × 3 / 100 = 24a/100; दूसरे पर = b × 6 × 5 / 100 = 30b/100. ब्याज बराबर होने से 24a = 30b, इसलिए a : b = 5 : 4. पहला भाग = 5/9 × 10,800 = ₹6,000.", chk=(sol[0], 6000))
    rs = [r for r in range(1, 50) if 2500 * (100 + r)**2 == 3025 * 100**2]; assert rs == [10]
    A(s,t,"Easy","At what rate of compound interest per annum will ₹2,500 amount to ₹3,025 in 2 years?",["10%","11%","12%","10.5%"],"10%",
      "(1 + r/100)² = 3,025 / 2,500 = 1.21 = 1.1², so 1 + r/100 = 1.1 and r = 10%.",
      "(1 + r/100)² = 3,025 / 2,500 = 1.21 = 1.1², इसलिए 1 + r/100 = 1.1 और r = 10%.")
    # ================= Time & Work (+7) =================
    t = "Time & Work"
    v = 1 / (F(1, 18) / F(5, 2)); assert v == 45
    A(s,t,"Medium","A is 50% more efficient than B, and together they finish a piece of work in 18 days. In how many days can B alone finish it?",["45 days","30 days","36 days","27 days"],"45 days",
      "If B does 2 units a day, A does 3 units, so B does 2/5 of the combined daily work. Together they do 1/18 of the job a day, so B alone does 2/5 × 1/18 = 1/45. B alone takes 45 days.",
      "यदि B प्रतिदिन 2 इकाई करता है, तो A 3 इकाई करता है, इसलिए B संयुक्त दैनिक काम का 2/5 करता है। साथ में वे प्रतिदिन काम का 1/18 करते हैं, इसलिए B अकेले 2/5 × 1/18 = 1/45 करता है। B अकेले 45 दिन लेगा।", chk=(v, 45))
    v = 1 / ((F(1, 10) + F(1, 15) + F(1, 12)) / 2 - F(1, 10)); assert v == 40
    A(s,t,"Medium","A and B together can do a job in 10 days, B and C in 15 days, and A and C in 12 days. In how many days can C alone do it?",["40 days","24 days","30 days","60 days"],"40 days",
      "Adding the three rates: 2(A + B + C) = 1/10 + 1/15 + 1/12 = (6 + 4 + 5)/60 = 15/60 = 1/4, so A + B + C = 1/8. C = 1/8 − 1/10 = 1/40, so C alone takes 40 days.",
      "तीनों दरें जोड़ने पर: 2(A + B + C) = 1/10 + 1/15 + 1/12 = (6 + 4 + 5)/60 = 15/60 = 1/4, इसलिए A + B + C = 1/8. C = 1/8 − 1/10 = 1/40, इसलिए C अकेले 40 दिन लेगा।", chk=(v, 40))
    done, d = F(0), F(0)
    while True:
        r = F(1, 18) if int(d) % 2 == 0 else F(1, 12)
        if done + r >= 1: d += (1 - done) / r; break
        done += r; d += 1
    assert d == F(29, 2)
    A(s,t,"Hard","A can do a piece of work in 12 days and B in 18 days. They work on alternate days, B starting on the first day. In how many days will the work be finished?",["14½ days","15 days","14 days","15½ days"],"14½ days",
      "Take the work as 36 units: A does 3 units a day and B 2 units. Each two-day cycle (B then A) completes 5 units, so 7 cycles = 14 days complete 35 units. On day 15 it is B's turn; the last 1 unit takes B half a day. Total = 14½ days.",
      "काम को 36 इकाई मानें: A प्रतिदिन 3 इकाई और B 2 इकाई करता है। हर दो दिन का चक्र (पहले B फिर A) 5 इकाई पूरी करता है, इसलिए 7 चक्र = 14 दिन में 35 इकाई पूरी होती हैं। दिन 15 को B की बारी है; अंतिम 1 इकाई में B को आधा दिन लगता है। कुल = 14½ दिन।", chk=(d, F(29, 2)))
    m = F(15, 10); v = F(15 * 12) / (6 * m + 11); assert v == 9
    A(s,t,"Medium","10 men or 15 women can finish a job in 12 days. In how many days will 6 men and 11 women finish it?",["9 days","10 days","8 days","12 days"],"9 days",
      "10 men do as much as 15 women, so 1 man = 1.5 women. 6 men + 11 women = 9 + 11 = 20 women. The job needs 15 × 12 = 180 woman-days, so 20 women take 180/20 = 9 days.",
      "10 पुरुष 15 महिलाओं के बराबर काम करते हैं, इसलिए 1 पुरुष = 1.5 महिला। 6 पुरुष + 11 महिलाएँ = 9 + 11 = 20 महिलाएँ। काम में 15 × 12 = 180 महिला-दिन लगते हैं, इसलिए 20 महिलाएँ 180/20 = 9 दिन लेंगी।", chk=(v, 9))
    v = 1 / (F(1, 10) - F(1, 12)); assert v == 60
    A(s,t,"Medium","A pipe can fill a tank in 10 hours, but because of a leak at the bottom it takes 12 hours to fill. In how many hours can the leak alone empty the full tank?",["60 hours","22 hours","30 hours","120 hours"],"60 hours",
      "Rate of the leak = 1/10 − 1/12 = (6 − 5)/60 = 1/60 of the tank per hour. So the leak empties the full tank in 60 hours.",
      "रिसाव की दर = 1/10 − 1/12 = (6 − 5)/60 = टंकी का 1/60 प्रति घंटा। इसलिए रिसाव भरी टंकी को 60 घंटे में खाली करेगा।", chk=(v, 60))
    v = 5 * 4; assert v == 20
    A(s,t,"Easy","A completes one-fourth of a piece of work in 5 days. How many days will he take to finish the whole work?",["20 days","15 days","25 days","10 days"],"20 days",
      "One-fourth takes 5 days, so the whole work (four quarters) takes 4 × 5 = 20 days.",
      "एक-चौथाई काम में 5 दिन लगते हैं, इसलिए पूरे काम (चार चौथाई) में 4 × 5 = 20 दिन लगेंगे।", chk=(v, 20))
    c = 1 - 3 * F(1, 6) - 3 * F(1, 9); pay = 1800 * c; assert c == F(1, 6) and pay == 300
    A(s,t,"Hard","A alone can do a job in 6 days and B alone in 9 days. They take it on for ₹1,800 and, with the help of C, finish it in 3 days. How much should C be paid?",["₹300","₹600","₹450","₹200"],"₹300",
      "In 3 days A does 3/6 = 1/2 of the job and B does 3/9 = 1/3. C did the rest: 1 − 1/2 − 1/3 = 1/6. Payment is in proportion to the work done, so C gets 1/6 × 1,800 = ₹300.",
      "3 दिनों में A काम का 3/6 = 1/2 और B 3/9 = 1/3 करता है। बाकी C ने किया: 1 − 1/2 − 1/3 = 1/6. भुगतान किए गए काम के अनुपात में होता है, इसलिए C को 1/6 × 1,800 = ₹300 मिलेंगे।", chk=(pay, 300))
    # ================= Time, Speed & Distance (+4) =================
    t = "Time, Speed & Distance"
    tt = F(200, 1000) / (12 - 10); v = 10 * tt; assert v == 1
    A(s,t,"Medium","A thief is spotted by a policeman from a distance of 200 m, and both start running at the same moment. The thief runs at 10 km/h and the policeman at 12 km/h. How far will the thief have run when he is caught?",["1 km","1.2 km","800 m","600 m"],"1 km",
      "The policeman gains 12 − 10 = 2 km/h on the thief. To close the gap of 200 m = 0.2 km he needs 0.2/2 = 0.1 hour. In that time the thief runs 10 × 0.1 = 1 km.",
      "सिपाही चोर पर 12 − 10 = 2 km/h की बढ़त लेता है। 200 m = 0.2 km का अंतर पाटने में उसे 0.2/2 = 0.1 घंटा लगेगा। इतने समय में चोर 10 × 0.1 = 1 km दौड़ेगा।", chk=(v, 1))
    tt = F(450, 70 + 80); assert tt == 3
    A(s,t,"Easy","Two stations are 450 km apart. At 8 a.m. one train leaves each station and they travel towards each other at 70 km/h and 80 km/h. At what time do they meet?",["11 a.m.","10:30 a.m.","11:30 a.m.","12 noon"],"11 a.m.",
      "They approach each other at 70 + 80 = 150 km/h, so they meet after 450/150 = 3 hours, at 8 a.m. + 3 hours = 11 a.m.",
      "वे एक-दूसरे की ओर 70 + 80 = 150 km/h से बढ़ते हैं, इसलिए 450/150 = 3 घंटे बाद, यानी 8 a.m. + 3 घंटे = 11 a.m. पर मिलते हैं।", chk=(tt, 3))
    dd = F(15, 60) / (F(1, 4) - F(1, 5)); assert dd == 5
    A(s,t,"Medium","Walking at 4 km/h, a man reaches his office 10 minutes late. Walking at 5 km/h, he reaches 5 minutes early. How far is his office?",["5 km","4 km","6 km","7.5 km"],"5 km",
      "The two times differ by 10 + 5 = 15 minutes = 1/4 hour. So d/4 − d/5 = 1/4, i.e. d/20 = 1/4, giving d = 5 km.",
      "दोनों समयों में 10 + 5 = 15 मिनट = 1/4 घंटे का अंतर है। इसलिए d/4 − d/5 = 1/4, अर्थात d/20 = 1/4, अतः d = 5 km.", chk=(dd, 5))
    sol = [(u, w) for u in range(1, 30) for w in range(u + 1, 40) if F(24, u) + F(28, w) == 6 and F(30, u) + F(21, w) == F(13, 2)]; assert sol == [(6, 14)]
    A(s,t,"Hard","A boat goes 24 km upstream and 28 km downstream in 6 hours. It goes 30 km upstream and 21 km downstream in 6.5 hours. What is the speed of the boat in still water?",["10 km/h","4 km/h","14 km/h","6 km/h"],"10 km/h",
      "Let the upstream speed be u and the downstream speed d. Then 24/u + 28/d = 6 and 30/u + 21/d = 6.5. Solving these two linear equations in 1/u and 1/d gives u = 6 km/h and d = 14 km/h. (Check: 4 + 2 = 6 and 5 + 1.5 = 6.5.) Speed in still water = (6 + 14)/2 = 10 km/h.",
      "माना धारा के विरुद्ध चाल u और धारा के साथ चाल d है। तब 24/u + 28/d = 6 और 30/u + 21/d = 6.5. 1/u और 1/d में इन दो रैखिक समीकरणों को हल करने पर u = 6 km/h और d = 14 km/h. (जाँच: 4 + 2 = 6 और 5 + 1.5 = 6.5.) शांत जल में चाल = (6 + 14)/2 = 10 km/h.", chk=((6 + 14) / 2, 10))
