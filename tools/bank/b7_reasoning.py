"""Bank/SSC batch B7: Reasoning, +95 items (every topic raised toward 20). Each answer is recomputed here:
alphabet/coding by string rules, clocks by formula and datetime, directions by coordinates, inequalities and syllogisms by
enumerating every model (rcheck), family trees by an explicit tree, puzzles/seating/ranking by brute-force permutations
with a unique-solution assert. Hindi solutions carry the same numbers."""
import itertools, datetime, calendar, string
from fractions import Fraction as F
import rcheck as RC
AL = string.ascii_uppercase
pos = lambda c: AL.index(c) + 1

def build(A):
    s = "reasoning"
    SY, SYE = A.fixed_sets
    V = {'Only I': 'Only I follows', 'Only II': 'Only II follows', 'Both': 'Both I and II follow', 'Neither': 'Neither follows', 'Either': 'Either I or II follows'}
    # ================= Alphabet Test (+9) =================
    t = "Alphabet Test"
    v = AL[(27 - 6) - 9 - 1]; assert v == "L"
    A(s,t,"Easy","Which letter is the 9th to the left of the 6th letter from the right end of the English alphabet?",["L","M","K","N"],"L",
      "The 6th letter from the right is the (27 − 6) = 21st letter from the left, U. 9 places to its left is the 21 − 9 = 12th letter, L.",
      "दाएँ से 6वाँ अक्षर बाएँ से (27 − 6) = 21वाँ अक्षर U है। उसके 9 स्थान बाएँ 21 − 9 = 12वाँ अक्षर L है।", chk=(v, "L"))
    seq = AL[:13][::-1] + AL[13:]; v = seq[9 - 1 + 4]; assert seq[8] == "E" and v == "A"
    A(s,t,"Medium","If the first half of the English alphabet (A to M) is written in reverse order and the second half is left unchanged, which letter will be the 4th to the right of the 9th letter from the left?",["A","D","Q","R"],"A",
      "The new sequence starts M L K J I H G F E D C B A N O P … The 9th letter from the left is E, and the 4th letter to its right is the 13th letter of the sequence, A.",
      "नया क्रम M L K J I H G F E D C B A N O P … से शुरू होता है। बाएँ से 9वाँ अक्षर E है, और उसके 4 स्थान दाएँ क्रम का 13वाँ अक्षर A है।", chk=(v, "A"))
    v = AL[(5 + 23) // 2 - 1]; assert (27 - 4) == 23 and v == "N"
    A(s,t,"Easy","Which letter lies exactly midway between the 5th letter from the left and the 4th letter from the right of the English alphabet?",["N","M","O","L"],"N",
      "The 5th letter from the left is E (position 5) and the 4th from the right is W (position 27 − 4 = 23). The midpoint is position (5 + 23)/2 = 14, which is N.",
      "बाएँ से 5वाँ अक्षर E (स्थान 5) और दाएँ से 4था अक्षर W (स्थान 27 − 4 = 23) है। मध्य स्थान (5 + 23)/2 = 14 है, जो N है।", chk=(v, "N"))
    rem = AL[0::2]; v = rem[-7]; assert len(rem) == 13 and v == "M"
    A(s,t,"Medium","If every alternate letter of the English alphabet, starting with B, is removed, which letter will be the 7th from the right end of the remaining sequence?",["M","K","O","N"],"M",
      "Removing B, D, F, …, Z leaves A, C, E, …, Y — 13 letters. Counting from the right: Y, W, U, S, Q, O, M. The 7th is M.",
      "B, D, F, …, Z हटाने पर A, C, E, …, Y — 13 अक्षर बचते हैं। दाएँ से गिनने पर: Y, W, U, S, Q, O, M. 7वाँ M है।", chk=(v, "M"))
    w = "FORMULATE"; v = sorted(w, reverse=True)[2]; assert "".join(sorted(w, reverse=True)) == "UTROMLFEA" and v == "R"
    A(s,t,"Medium","If the letters of the word FORMULATE are arranged in reverse alphabetical order (Z to A), which letter will be 3rd from the left?",["R","O","T","M"],"R",
      "In reverse alphabetical order the letters are U T R O M L F E A. The 3rd from the left is R.",
      "उल्टे वर्णानुक्रम में अक्षर U T R O M L F E A हैं। बाएँ से 3रा अक्षर R है।", chk=(v, "R"))
    w = "FIGHTER"; pr = [(w[i], w[j]) for i in range(len(w)) for j in range(i + 1, len(w)) if abs(pos(w[i]) - pos(w[j])) == j - i]
    assert sorted(pr) == [('G', 'H'), ('I', 'E'), ('T', 'R')]
    A(s,t,"Hard","How many pairs of letters are there in the word FIGHTER that have as many letters between them in the word as in the English alphabet (counting in either direction)?",["3","2","4","1"],"3",
      "Check every pair against its alphabet gap. G–H are adjacent both in the word and in the alphabet. I (2nd) and E (6th) are 4 places apart in the word, and I(9) and E(5) are 4 apart in the alphabet. T (5th) and R (7th) are 2 places apart in the word, and T(20) and R(18) are 2 apart in the alphabet. No other pair matches, so there are 3 pairs.",
      "हर जोड़ी को उसके वर्णमाला अंतर से मिलाएँ। G–H शब्द और वर्णमाला दोनों में पास-पास हैं। I (2रा) और E (6ठा) शब्द में 4 स्थान दूर हैं, और I(9) व E(5) वर्णमाला में भी 4 दूर हैं। T (5वाँ) और R (7वाँ) शब्द में 2 स्थान दूर हैं, और T(20) व R(18) वर्णमाला में भी 2 दूर हैं। कोई और जोड़ी मेल नहीं खाती, इसलिए 3 जोड़ियाँ हैं।", chk=(len(pr), 3))
    v = sum(1 for c in AL[4:23] if c in "AEIOU"); assert AL[3] == "D" and AL[-3] == "X" and v == 4
    A(s,t,"Medium","How many vowels are there in the English alphabet strictly between the 4th letter from the left and the 3rd letter from the right?",["4","5","3","6"],"4",
      "The 4th letter from the left is D and the 3rd from the right is X. The letters strictly between them run from E to W, which contain the vowels E, I, O and U — 4 vowels.",
      "बाएँ से 4था अक्षर D और दाएँ से 3रा अक्षर X है। इनके बीच के अक्षर E से W तक हैं, जिनमें स्वर E, I, O और U हैं — 4 स्वर।", chk=(v, 4))
    rv = AL[::-1]; v = rv[rv.index("T") + 7]; assert v == "M"
    A(s,t,"Easy","If the English alphabet is written in reverse order (Z to A), which letter will be the 7th to the right of T?",["M","A","G","N"],"M",
      "In the reversed alphabet, moving right from T gives S, R, Q, P, O, N, M. The 7th letter is M.",
      "उल्टी वर्णमाला में T से दाएँ चलने पर S, R, Q, P, O, N, M मिलते हैं। 7वाँ अक्षर M है।", chk=(v, "M"))
    w = "PLANET"; v = sum(1 for a, b in zip(w, sorted(w)) if a == b); assert v == 2
    A(s,t,"Medium","If the letters of the word PLANET are arranged in alphabetical order, how many letters will remain in the same position as in the original word?",["2","1","0","3"],"2",
      "Alphabetical order gives A E L N P T. Comparing with P L A N E T position by position, only N (4th) and T (6th) stay in place: 2 letters.",
      "वर्णानुक्रम में A E L N P T मिलता है। P L A N E T से स्थान-दर-स्थान मिलाने पर केवल N (4था) और T (6ठा) अपनी जगह रहते हैं: 2 अक्षर।", chk=(v, 2))
    # ================= Blood Relations (+8) =================
    t = "Blood Relations"
    def fam_check(build_tree, a, b, unknown, want):
        outs = set()
        for gs in itertools.product("MF", repeat=len(unknown)):
            f = build_tree(dict(zip(unknown, gs))); outs.add(f.rel(a, b))
        assert outs == {want}, outs
        return want
    def t1(g):
        f = RC.Fam(); [f.p(n, x) for n, x in (("GF", "M"), ("Arjun", "M"), ("Girl", "F"))]
        f.child("GF", "Arjun"); f.child("Arjun", "Girl"); return f
    v = fam_check(t1, "Girl", "Arjun", [], "Daughter")
    A(s,t,"Easy","Pointing to a girl, Arjun says, \"She is the only daughter of my father's only son.\" How is the girl related to Arjun?",["Daughter","Sister","Niece","Cousin"],"Daughter",
      "Arjun is a man, so his father's only son is Arjun himself. The girl is the only daughter of Arjun, i.e. his daughter.",
      "अर्जुन पुरुष है, इसलिए उसके पिता का इकलौता पुत्र स्वयं अर्जुन है। लड़की अर्जुन की इकलौती पुत्री है, यानी उसकी बेटी।", chk=(v, "Daughter"))
    def t2(g):
        f = RC.Fam(); [f.p(n, x) for n, x in (("A", "F"), ("B", "F"), ("C", g["C"]), ("D", "M"), ("E", "F"))]
        f.child("A", "B"); f.child("A", "C"); f.child("C", "D"); f.marry("D", "E"); return f
    v = fam_check(t2, "E", "A", ["C"], "Granddaughter-in-law")
    A(s,t,"Medium","A is the mother of B. B is the sister of C. D is the son of C. E is the wife of D. How is E related to A?",["Granddaughter-in-law","Daughter-in-law","Granddaughter","Niece"],"Granddaughter-in-law",
      "B and C are A's children, so D (C's son) is A's grandson. E is the wife of A's grandson, so E is A's granddaughter-in-law.",
      "B और C, A की संतान हैं, इसलिए D (C का पुत्र) A का पोता/नाती है। E, A के पोते की पत्नी है, इसलिए E, A की पोतबहू (granddaughter-in-law) है।", chk=(v, "Granddaughter-in-law"))
    def t3(g):
        f = RC.Fam(); [f.p(n, x) for n, x in (("A", "M"), ("B", "M"), ("C", "F"), ("D", "F"), ("E", g["E"]))]
        for c in "BCD": f.child("A", c)
        f.child("D", "E"); return f
    v = fam_check(t3, "A", "E", ["E"], "Grandfather")
    A(s,t,"Medium","In a code, P × Q means P is the father of Q; P + Q means P is the brother of Q; P − Q means P is the sister of Q; P ÷ Q means P is the mother of Q. If A × B + C − D ÷ E, how is A related to E?",["Grandfather","Father","Uncle","Great-grandfather"],"Grandfather",
      "A × B: A is B's father. B + C and C − D: B, C and D are siblings, so A is also D's father. D ÷ E: D is E's mother. So A is the father of E's mother — E's grandfather.",
      "A × B: A, B का पिता है। B + C और C − D: B, C और D भाई-बहन हैं, इसलिए A, D का भी पिता है। D ÷ E: D, E की माता है। अतः A, E की माता का पिता — E का नाना (Grandfather) है।", chk=(v, "Grandfather"))
    def t4(g):
        f = RC.Fam(); [f.p(n, x) for n, x in (("P", "M"), ("R", "F"), ("S", "M"), ("T", "F"), ("U", "F"), ("Q", "M"))]
        f.marry("P", "R"); f.child("P", "S"); f.child("R", "S"); f.child("P", "T"); f.child("R", "T"); f.marry("S", "U"); f.child("S", "Q"); f.child("U", "Q"); return f
    v = fam_check(t4, "T", "Q", [], "Aunt"); assert t4({}).rel("U", "R") == "Daughter-in-law"
    A(s,t,"Medium","A family has six members P, Q, R, S, T and U, with two married couples. R is the wife of P. S is the only son of P and R. T is the sister of S and is unmarried. U is the daughter-in-law of R. Q is the son of U. How is T related to Q?",["Aunt","Mother","Sister","Grandmother"],"Aunt",
      "S is the only son of P and R, so U (R's daughter-in-law) is S's wife, and the two couples are P–R and S–U. Q, the son of U, is therefore S's son. T is S's sister, so T is Q's father's sister — Q's aunt.",
      "S, P और R का इकलौता पुत्र है, इसलिए U (R की पुत्रवधू) S की पत्नी है, और दोनों दंपती P–R और S–U हैं। U का पुत्र Q इसलिए S का पुत्र है। T, S की बहन है, अतः T, Q के पिता की बहन — Q की बुआ (Aunt) है।", chk=(v, "Aunt"))
    def t5(g):
        f = RC.Fam(); [f.p(n, x) for n, x in (("Fa", "M"), ("Neha", "F"), ("Man", "M"))]
        f.child("Fa", "Neha"); f.marry("Neha", "Man"); return f
    v = fam_check(t5, "Man", "Neha", [], "Husband")
    A(s,t,"Easy","Introducing a man, Neha says, \"His wife is the only daughter of my father.\" How is the man related to Neha?",["Husband","Brother","Brother-in-law","Father-in-law"],"Husband",
      "Neha is a woman, so the only daughter of her father is Neha herself. The man's wife is Neha, so he is her husband.",
      "नेहा महिला है, इसलिए उसके पिता की इकलौती पुत्री स्वयं नेहा है। उस पुरुष की पत्नी नेहा है, इसलिए वह उसका पति है।", chk=(v, "Husband"))
    def t6(g):
        f = RC.Fam(); [f.p(n, x) for n, x in (("A", "M"), ("B", "M"), ("C", g["C"]), ("D", "M"), ("E", "F"))]
        f.child("C", "A"); f.child("C", "B"); f.child("D", "C"); f.child("D", "E"); return f
    v = fam_check(t6, "A", "E", ["C"], "Nephew")
    A(s,t,"Medium","A is the brother of B. B is the son of C. D is the father of C. E is the daughter of D. How is A related to E?",["Nephew","Son","Brother","Cousin"],"Nephew",
      "A and B are C's children. C and E are both D's children, so E is C's sister. A is the son of E's sibling, so A is E's nephew.",
      "A और B, C की संतान हैं। C और E दोनों D की संतान हैं, इसलिए E, C की बहन है। A, E के भाई/बहन का पुत्र है, इसलिए A, E का भतीजा/भांजा (Nephew) है।", chk=(v, "Nephew"))
    def t7(g):
        f = RC.Fam(); [f.p(n, x) for n, x in (("P", "F"), ("Q", "F"), ("R", "M"), ("S", "M"), ("T", g["T"]))]
        f.marry("Q", "R")
        for c in "PST": f.child("Q", c); f.child("R", c)
        return f
    v = fam_check(t7, "P", "T", ["T"], "Sister")
    A(s,t,"Medium","In a code, A @ B means A is the daughter of B; A $ B means A is the wife of B; A # B means A is the father of B; A & B means A is the brother of B. If P @ Q $ R # S & T, how is P related to T?",["Sister","Daughter","Mother","Cannot be determined"],"Sister",
      "P @ Q: P is Q's daughter. Q $ R: Q is R's wife, so P is also R's daughter. R # S and S & T: S and T are R's children. P is a female child of the same parents as T, so P is T's sister (whatever T's gender).",
      "P @ Q: P, Q की बेटी है। Q $ R: Q, R की पत्नी है, इसलिए P, R की भी बेटी है। R # S और S & T: S और T, R की संतान हैं। P, T के ही माता-पिता की बेटी है, इसलिए P, T की बहन है (T का लिंग कुछ भी हो)।", chk=(v, "Sister"))
    def t8(g):
        f = RC.Fam(); [f.p(n, x) for n, x in (("Fa", "M"), ("Mo", "F"), ("Kunal", "M"), ("W", "F"), ("Son", "M"))]
        f.marry("Fa", "Mo"); f.child("Fa", "Kunal"); f.child("Mo", "Kunal"); f.marry("Kunal", "W"); f.child("Kunal", "Son"); f.child("W", "Son"); return f
    v = fam_check(t8, "W", "Kunal", [], "Wife")
    A(s,t,"Hard","Pointing to a woman, Kunal says, \"She is the mother of the only grandson of my mother's husband.\" Kunal has no brothers or sisters. How is the woman related to Kunal?",["Wife","Sister","Mother","Sister-in-law"],"Wife",
      "Kunal's mother's husband is Kunal's father. As Kunal has no siblings, any grandson of his father must be Kunal's son. The mother of Kunal's son is Kunal's wife.",
      "कुणाल की माता का पति कुणाल का पिता है। कुणाल का कोई भाई-बहन नहीं है, इसलिए उसके पिता का कोई भी पोता कुणाल का ही पुत्र होगा। कुणाल के पुत्र की माता कुणाल की पत्नी है।", chk=(v, "Wife"))
    # ================= Clocks & Calendars (+7) =================
    t = "Clocks & Calendars"
    ang = lambda h, m: min(abs(30 * h - 5.5 * m), 360 - abs(30 * h - 5.5 * m))
    v = ang(8, 25); assert v == 102.5
    A(s,t,"Medium","What is the smaller angle between the hour hand and the minute hand of a clock at 8:25?",["102.5°","107.5°","97.5°","112.5°"],"102.5°",
      "Angle = |30H − 5.5M| = |30 × 8 − 5.5 × 25| = |240 − 137.5| = 102.5°.",
      "कोण = |30H − 5.5M| = |30 × 8 − 5.5 × 25| = |240 − 137.5| = 102.5°.", chk=(v, 102.5))
    ts = [F(720 * k, 11) for k in range(0, 12)]; v = sum(1 for x in ts if 180 < x < 540); assert v == 6 and [int(x) for x in ts if 180 < x < 540][0] == 196
    A(s,t,"Hard","How many times do the hour hand and the minute hand of a clock coincide between 3 p.m. and 9 p.m.?",["6","5","7","4"],"6",
      "The hands coincide every 720/11 = 65 5/11 minutes, i.e. at 720k/11 minutes after 12 o'clock (k = 0, 1, 2, …). Between 3 p.m. (180 minutes) and 9 p.m. (540 minutes) this needs 180 < 720k/11 < 540, i.e. 2.75 < k < 8.25, so k = 3, 4, 5, 6, 7, 8: 6 times (about 3:16, 4:22, 5:27, 6:33, 7:38 and 8:44). The 9 o'clock coincidence comes only at about 9:49.",
      "सुइयाँ हर 720/11 = 65 5/11 मिनट पर मिलती हैं, यानी 12 बजे के 720k/11 मिनट बाद (k = 0, 1, 2, …)। 3 p.m. (180 मिनट) और 9 p.m. (540 मिनट) के बीच 180 < 720k/11 < 540 चाहिए, यानी 2.75 < k < 8.25, इसलिए k = 3, 4, 5, 6, 7, 8: 6 बार (लगभग 3:16, 4:22, 5:27, 6:33, 7:38 और 8:44)। 9 बजे वाला मिलन लगभग 9:49 पर ही होता है।", chk=(v, 6))
    m = F(180 + 60, 1) / F(11, 2); assert m == F(480, 11) and m == 43 + F(7, 11)
    A(s,t,"Hard","At what time between 2 o'clock and 3 o'clock will the hour hand and the minute hand of a clock point in exactly opposite directions?",["43 7/11 minutes past 2","43 minutes past 2","45 5/11 minutes past 2","40 10/11 minutes past 2"],"43 7/11 minutes past 2",
      "At 2:00 the minute hand is 60° behind the hour hand. It gains 5.5° per minute and must get 180° ahead, a total gain of 60 + 180 = 240°. Time = 240/5.5 = 480/11 = 43 7/11 minutes past 2.",
      "2:00 बजे मिनट की सुई घंटे की सुई से 60° पीछे है। यह प्रति मिनट 5.5° आगे बढ़ती है और इसे 180° आगे जाना है, कुल 60 + 180 = 240°. समय = 240/5.5 = 480/11 = 2 बजकर 43 7/11 मिनट।", chk=(m, F(480, 11)))
    real = F(720 * 60, 56); assert real == 771 + F(3, 7) and divmod(771, 60) == (12, 51)
    A(s,t,"Hard","A clock loses 4 minutes every hour. It is set right at 8 a.m. What is the correct time when this clock shows 8 p.m. the same day?",["8:51 3/7 p.m.","8:48 p.m.","8:52 p.m.","7:12 p.m."],"8:51 3/7 p.m.",
      "In 60 minutes of correct time the clock shows only 56 minutes. When it shows 12 hours = 720 minutes, the correct time elapsed is 720 × 60/56 = 771 3/7 minutes = 12 hours 51 3/7 minutes. So the correct time is 8:51 3/7 p.m.",
      "सही समय के 60 मिनट में घड़ी केवल 56 मिनट दिखाती है। जब यह 12 घंटे = 720 मिनट दिखाती है, तो वास्तविक बीता समय 720 × 60/56 = 771 3/7 मिनट = 12 घंटे 51 3/7 मिनट है। इसलिए सही समय रात 8:51 3/7 p.m. है।", chk=(real, 771 + F(3, 7)))
    v = datetime.date(1950, 1, 26).strftime("%A"); assert v == "Thursday" and (0 + 1 + (12 * 2 + 37) + 26) % 7 == 4
    A(s,t,"Medium","On which day of the week did 26 January 1950 fall?",["Thursday","Wednesday","Friday","Sunday"],"Thursday",
      "Odd days up to 31 December 1949: 1600 years give 0, the next 300 years give 1, and 49 years (12 leap + 37 ordinary) give 12 × 2 + 37 = 61, i.e. 5. Total so far 0 + 1 + 5 = 6. Add 26 days of January: 6 + 26 = 32, and 32 leaves remainder 4 on division by 7. Day 4 (counting Sunday as 0) is Thursday.",
      "31 दिसंबर 1949 तक विषम दिन: 1600 वर्ष से 0, अगले 300 वर्ष से 1, और 49 वर्ष (12 लीप + 37 साधारण) से 12 × 2 + 37 = 61, यानी 5. अब तक कुल 0 + 1 + 5 = 6. जनवरी के 26 दिन जोड़ें: 6 + 26 = 32, और 32 को 7 से भाग देने पर शेष 4. दिन 4 (रविवार को 0 मानकर) गुरुवार है।", chk=(v, "Thursday"))
    assert datetime.date(2027, 3, 3).strftime("%A") == "Wednesday"; v = datetime.date(2028, 3, 3).strftime("%A"); assert v == "Friday"
    A(s,t,"Medium","3 March 2027 is a Wednesday. What day of the week will 3 March 2028 be?",["Friday","Thursday","Saturday","Wednesday"],"Friday",
      "The period from 3 March 2027 to 3 March 2028 includes 29 February 2028 (2028 is a leap year), so it has 366 days = 52 weeks + 2 days. 2 days after Wednesday is Friday.",
      "3 मार्च 2027 से 3 मार्च 2028 की अवधि में 29 फरवरी 2028 आता है (2028 लीप वर्ष है), इसलिए इसमें 366 दिन = 52 सप्ताह + 2 दिन हैं। बुधवार के 2 दिन बाद शुक्रवार है।", chk=(v, "Friday"))
    sig = lambda y: (datetime.date(y, 1, 1).weekday(), calendar.isleap(y))
    good = [y for y in (2037, 2032, 2034, 2036) if sig(y) == sig(2026)]; assert good == [2037]
    A(s,t,"Hard","The calendar of 2026 will be repeated exactly (same days on the same dates) in which of these years?",["2037","2032","2034","2036"],"2037",
      "2026 is an ordinary year. Counting odd days from 2026: 2026 (1), 2027 (1), 2028 (2), 2029 (1), 2030 (1), 2031 (1), 2032 (2), 2033 (1), 2034 (1), 2035 (1), 2036 (2) — a total of 14, a multiple of 7. So 2037 starts on the same day as 2026, and it is also an ordinary year, so its calendar is identical. (2032 and 2036 are leap years, and 2034 starts on a different day.)",
      "2026 साधारण वर्ष है। 2026 से विषम दिन गिनें: 2026 (1), 2027 (1), 2028 (2), 2029 (1), 2030 (1), 2031 (1), 2032 (2), 2033 (1), 2034 (1), 2035 (1), 2036 (2) — कुल 14, जो 7 का गुणज है। इसलिए 2037 उसी दिन से शुरू होता है जिससे 2026, और यह भी साधारण वर्ष है, अतः इसका कैलेंडर बिल्कुल समान है। (2032 और 2036 लीप वर्ष हैं, और 2034 अलग दिन से शुरू होता है।)", chk=(good[0], 2037))
    od = [2 if calendar.isleap(y) else 1 for y in range(2026, 2037)]; assert sum(od) == 14
    # ================= Coding-Decoding (+7) =================
    t = "Coding-Decoding"
    sh = lambda c, k: AL[(AL.index(c) + k) % 26]
    enc = lambda w: "".join(sh(c, 1) for c in w[::-1]); assert enc("MOTHER") == "SFIUPN"; v = enc("FATHER"); assert v == "SFIUBG"
    A(s,t,"Medium","In a certain code, MOTHER is written as SFIUPN. How is FATHER written in that code?",["SFIUBG","SFIUGB","GBUIFS","RDHTAF"],"SFIUBG",
      "The word is reversed and each letter is then moved one place forward: MOTHER → REHTOM → SFIUPN. Similarly FATHER → REHTAF → SFIUBG.",
      "शब्द को उल्टा करके हर अक्षर को एक स्थान आगे बढ़ाया गया है: MOTHER → REHTOM → SFIUPN. इसी प्रकार FATHER → REHTAF → SFIUBG.", chk=(v, "SFIUBG"))
    rp = lambda w: "-".join(str(27 - pos(c)) for c in w); assert rp("ROAD") == "9-12-26-23"; v = rp("LANE"); assert v == "15-26-13-22"
    A(s,t,"Medium","In a certain code, ROAD is written as 9-12-26-23. How is LANE written in that code?",["15-26-13-22","12-1-14-5","15-26-14-22","14-26-13-22"],"15-26-13-22",
      "Each letter is replaced by its position counted from the end of the alphabet (Z = 1, …, A = 26): R = 9, O = 12, A = 26, D = 23. So L = 15, A = 26, N = 13, E = 22, giving 15-26-13-22.",
      "हर अक्षर को वर्णमाला के अंत से गिनी गई स्थिति से बदला गया है (Z = 1, …, A = 26): R = 9, O = 12, A = 26, D = 23. इसलिए L = 15, A = 26, N = 13, E = 22, यानी 15-26-13-22.", chk=(v, "15-26-13-22"))
    S1, S2, S3 = ({"come", "and", "go"}, {"pa", "ri", "sa"}), ({"go", "and", "run"}, {"ri", "na", "pa"}), ({"run", "fast", "now"}, {"ta", "na", "ke"})
    v = (S1[1] - S2[1]); assert S1[0] - S2[0] == {"come"} and v == {"sa"}
    A(s,t,"Medium","In a certain code language, 'come and go' is written as 'pa ri sa', 'go and run' as 'ri na pa', and 'run fast now' as 'ta na ke'. What is the code for 'come'?",["sa","pa","ri","na"],"sa",
      "'and go' is common to the first two sentences, and 'pa ri' is common to their codes, so 'and' and 'go' are coded as 'pa' and 'ri' in some order. The remaining word of the first sentence, 'come', must be 'sa'.",
      "पहले दोनों वाक्यों में 'and go' उभयनिष्ठ है, और उनके कोड में 'pa ri' उभयनिष्ठ है, इसलिए 'and' और 'go' का कोड किसी क्रम में 'pa' और 'ri' है। पहले वाक्य का बचा हुआ शब्द 'come' इसलिए 'sa' होगा।", chk=("".join(v), "sa"))
    mp = dict(zip("PAINT", "74128")); mp2 = dict(zip("EXCEL", "93596")); assert all(mp2[k] == d for k, d in zip("EXCEL", "93596"))
    mp.update(mp2); v = "".join(mp[c] for c in "ACCEPT"); assert v == "455978"
    A(s,t,"Medium","If PAINT is coded as 74128 and EXCEL as 93596, how is ACCEPT coded?",["455978","455987","545978","454978"],"455978",
      "Each letter has a fixed digit: P = 7, A = 4, I = 1, N = 2, T = 8 and E = 9, X = 3, C = 5, L = 6 (E = 9 is consistent at both ends of EXCEL). So A C C E P T = 4 5 5 9 7 8 = 455978.",
      "हर अक्षर का एक निश्चित अंक है: P = 7, A = 4, I = 1, N = 2, T = 8 तथा E = 9, X = 3, C = 5, L = 6 (EXCEL के दोनों सिरों पर E = 9 समान है)। इसलिए A C C E P T = 4 5 5 9 7 8 = 455978.", chk=(v, "455978"))
    alt = lambda w: "".join(sh(c, 1 if i % 2 == 0 else -1) for i, c in enumerate(w)); assert alt("PLANET") == "QKBMFS"; v = alt("CORNER"); assert v == "DNSMFQ"
    A(s,t,"Medium","In a certain code, PLANET is written as QKBMFS. How is CORNER written in that code?",["DNSMFQ","DPSOFS","BNQMDQ","DNSMFS"],"DNSMFQ",
      "Letters in odd positions move one step forward and letters in even positions move one step back: P+1 = Q, L−1 = K, A+1 = B, N−1 = M, E+1 = F, T−1 = S. So C+1 = D, O−1 = N, R+1 = S, N−1 = M, E+1 = F, R−1 = Q: DNSMFQ.",
      "विषम स्थानों के अक्षर एक कदम आगे और सम स्थानों के अक्षर एक कदम पीछे जाते हैं: P+1 = Q, L−1 = K, A+1 = B, N−1 = M, E+1 = F, T−1 = S. इसलिए C+1 = D, O−1 = N, R+1 = S, N−1 = M, E+1 = F, R−1 = Q: DNSMFQ.", chk=(v, "DNSMFQ"))
    pr_ = lambda w: __import__("math").prod(pos(c) for c in w); assert pr_("BAD") == 8 and pr_("CAB") == 6; v = pr_("DEED"); assert v == 400
    A(s,t,"Medium","In a certain code, BAD = 8 and CAB = 6. Following the same rule, what is the code for DEED?",["400","18","200","320"],"400",
      "The code is the product of the alphabet positions: BAD = 2 × 1 × 4 = 8 and CAB = 3 × 1 × 2 = 6. So DEED = 4 × 5 × 5 × 4 = 400.",
      "कोड अक्षरों की वर्णमाला स्थितियों का गुणनफल है: BAD = 2 × 1 × 4 = 8 और CAB = 3 × 1 × 2 = 6. इसलिए DEED = 4 × 5 × 5 × 4 = 400.", chk=(v, 400))
    inc = lambda w: "".join(sh(c, i + 1) for i, c in enumerate(w)); assert inc("ROSE") == "SQVI"; v = inc("LILY"); assert v == "MKOC"
    A(s,t,"Hard","In a certain code, ROSE is written as SQVI. How is LILY written in that code?",["MKOC","MKOD","MJOC","NKOC"],"MKOC",
      "The letters move forward by 1, 2, 3 and 4 places in turn: R+1 = S, O+2 = Q, S+3 = V, E+4 = I. So L+1 = M, I+2 = K, L+3 = O and Y+4 = C (counting past Z back to A, B, C): MKOC.",
      "अक्षर क्रमशः 1, 2, 3 और 4 स्थान आगे बढ़ते हैं: R+1 = S, O+2 = Q, S+3 = V, E+4 = I. इसलिए L+1 = M, I+2 = K, L+3 = O और Y+4 = C (Z के बाद फिर A, B, C गिनते हुए): MKOC.", chk=(v, "MKOC"))
    # ================= Direction Sense (+8) =================
    t = "Direction Sense"
    import math
    def walk(steps, start="N"):
        D = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}; order = "NESW"; d = start; x = y = 0
        for turn, k in steps:
            if turn == "R": d = order[(order.index(d) + 1) % 4]
            elif turn == "L": d = order[(order.index(d) - 1) % 4]
            elif turn in D: d = turn
            x += D[d][0] * k; y += D[d][1] * k
        return x, y
    x, y = walk([("E", 6), ("L", 8), ("L", 12)]); assert (x, y) == (-6, 8) and math.hypot(x, y) == 10
    A(s,t,"Medium","Kiran walks 6 km east, turns left and walks 8 km, then turns left again and walks 12 km. How far and in which direction is she from her starting point?",["10 km North-West","10 km North-East","14 km North-West","10 km South-West"],"10 km North-West",
      "Take the start as (0, 0). After 6 km east she is at (6, 0); turning left she faces north and reaches (6, 8); turning left again she faces west and reaches (6 − 12, 8) = (−6, 8). Distance = √(6² + 8²) = 10 km, towards the north-west.",
      "आरंभ को (0, 0) मानें। 6 km पूर्व के बाद वह (6, 0) पर है; बाएँ मुड़कर वह उत्तर की ओर (6, 8) पहुँचती है; फिर बाएँ मुड़कर पश्चिम की ओर (6 − 12, 8) = (−6, 8) पहुँचती है। दूरी = √(6² + 8²) = 10 km, उत्तर-पश्चिम दिशा में।", chk=(math.hypot(x, y), 10))
    b = (90 + 45 - 180 + 90) % 360; assert b == 45
    A(s,t,"Medium","A man is facing east. He turns 45° clockwise, then 180° anticlockwise, and then 90° clockwise. Which direction is he facing now?",["North-East","South-West","North-West","South-East"],"North-East",
      "Measure bearings clockwise from north: east = 90°. After the turns: 90 + 45 = 135°, then 135 − 180 = −45° (i.e. 315°), then 315 + 90 = 405° = 45°, which is north-east.",
      "उत्तर से दक्षिणावर्त कोण मापें: पूर्व = 90°. मुड़ने के बाद: 90 + 45 = 135°, फिर 135 − 180 = −45° (यानी 315°), फिर 315 + 90 = 405° = 45°, जो उत्तर-पूर्व है।", chk=(b, 45))
    d = math.hypot(9, 12); assert d == 15
    A(s,t,"Medium","Point A is 9 m west of point B. Point C is 12 m south of point B. How far is C from A, and in which direction is C with respect to A?",["15 m, South-East","15 m, South-West","21 m, South-East","15 m, North-East"],"15 m, South-East",
      "Take B = (0, 0): A = (−9, 0) and C = (0, −12). From A, C is 9 m to the east and 12 m to the south, so AC = √(9² + 12²) = 15 m and C is to the south-east of A.",
      "B = (0, 0) लें: A = (−9, 0) और C = (0, −12). A से C, 9 m पूर्व और 12 m दक्षिण में है, इसलिए AC = √(9² + 12²) = 15 m और C, A के दक्षिण-पूर्व में है।", chk=(d, 15))
    A(s,t,"Easy","At 4 p.m. on a sunny day, Rina stands facing her own shadow. Which direction is she facing?",["East","West","North","South"],"East",
      "In the afternoon the sun is in the west, so shadows fall towards the east. Facing her shadow, Rina faces east.",
      "दोपहर बाद सूर्य पश्चिम में होता है, इसलिए छाया पूर्व की ओर पड़ती है। अपनी छाया की ओर मुँह करके रीना पूर्व की ओर देख रही है।", chk=("East", "East"))
    x, y = walk([("N", 4), ("R", 6), ("R", 9), ("L", 6), ("L", 5)]); assert (x, y) == (12, 0)
    A(s,t,"Hard","Rahul leaves his house and walks 4 km north. He turns right and walks 6 km, turns right and walks 9 km, turns left and walks 6 km, and finally turns left and walks 5 km. How far and in which direction is he from his house?",["12 km East","12 km West","13 km North-East","6 km East"],"12 km East",
      "Take the house as (0, 0). North 4 → (0, 4); right (east) 6 → (6, 4); right (south) 9 → (6, −5); left (east) 6 → (12, −5); left (north) 5 → (12, 0). He is 12 km due east of his house.",
      "घर को (0, 0) लें। उत्तर 4 → (0, 4); दाएँ (पूर्व) 6 → (6, 4); दाएँ (दक्षिण) 9 → (6, −5); बाएँ (पूर्व) 6 → (12, −5); बाएँ (उत्तर) 5 → (12, 0). वह घर से ठीक 12 km पूर्व में है।", chk=((x, y), (12, 0)))
    d = math.hypot(3 - (-3), 7 - (-1)); assert d == 10
    A(s,t,"Medium","P and Q start from the same point. P walks 7 km north and then 3 km east. Q walks 3 km west and then 1 km south. What is the straight-line distance between P and Q now?",["10 km","14 km","8 km","12 km"],"10 km",
      "With the start at (0, 0), P is at (3, 7) and Q at (−3, −1). The horizontal gap is 3 + 3 = 6 km and the vertical gap 7 + 1 = 8 km, so PQ = √(6² + 8²) = 10 km.",
      "आरंभ (0, 0) पर, P (3, 7) पर और Q (−3, −1) पर है। क्षैतिज अंतर 3 + 3 = 6 km और ऊर्ध्वाधर अंतर 7 + 1 = 8 km है, इसलिए PQ = √(6² + 8²) = 10 km.", chk=(d, 10))
    b = (45 + 1.5 * 30) % 360; assert b == 90
    A(s,t,"Medium","A wall clock is fixed so that its 12 points towards the north-east. In which direction will the hour hand point at 1:30?",["East","North","South-East","North-East"],"East",
      "At 1:30 the hour hand is 1.5 × 30 = 45° clockwise from the 12. The 12 points north-east (45° from north), so the hour hand points at 45 + 45 = 90° from north, which is east.",
      "1:30 बजे घंटे की सुई 12 से 1.5 × 30 = 45° दक्षिणावर्त होती है। 12 उत्तर-पूर्व (उत्तर से 45°) की ओर है, इसलिए घंटे की सुई उत्तर से 45 + 45 = 90° पर, यानी पूर्व की ओर होगी।", chk=(b, 90))
    Pp = (0, 0); Qp = (0, 10); Rp = (6, 10); Sp = (6, 8); Tp = (0, 8); assert (Sp[0] - 6, Sp[1]) == Tp
    A(s,t,"Medium","Village Q is 10 km north of village P. Village R is 6 km east of Q. Village S is 2 km south of R, and village T is 6 km west of S. Where is T with respect to P?",["8 km North","10 km North","8 km North-East","6 km North"],"8 km North",
      "Take P = (0, 0). Then Q = (0, 10), R = (6, 10), S = (6, 8) and T = (0, 8). T is 8 km due north of P.",
      "P = (0, 0) लें। तब Q = (0, 10), R = (6, 10), S = (6, 8) और T = (0, 8). T, P से ठीक 8 km उत्तर में है।", chk=(Tp, (0, 8)))
    # ================= Inequalities (+9) =================
    t = "Inequalities"
    def IQ(diff, st, c1, c2, want, sol, hi, shown=None, text=None):
        v = RC.ineq(st, c1, c2); assert v == want, (st, v)
        opts = SYE if want == "Either" else SY; assert V[want] in opts
        q = text or f"Statements: {(shown or st).replace('<', '&lt;')}<br>Conclusions: I. {c1.replace('<', '&lt;')} II. {c2.replace('<', '&lt;')}"
        A(s, t, diff, q, opts, V[want], sol, hi, chk=(v, want))
    IQ("Medium", "M > N ≥ O = P, Q < O", "M > P", "Q < N", "Both",
       "Combining: M > N ≥ O = P gives M > P, so I follows. Q < O = P and O ≤ N gives Q < N, so II follows. Both follow.",
       "जोड़ने पर: M > N ≥ O = P से M > P, इसलिए I सही है। Q < O और O ≤ N से Q < N, इसलिए II सही है। दोनों सही हैं।")
    IQ("Medium", "A ≥ B = C, D ≤ C", "A ≥ D", "D > B", "Only I",
       "A ≥ B = C ≥ D gives A ≥ D, so I follows. Since D ≤ C = B, D can never be greater than B, so II does not follow. Only I follows.",
       "A ≥ B = C ≥ D से A ≥ D, इसलिए I सही है। चूँकि D ≤ C = B, D कभी B से बड़ा नहीं हो सकता, इसलिए II सही नहीं है। केवल I सही है।")
    IQ("Hard", "R ≥ S > T, U ≥ S", "R > U", "U ≥ T", "Only II",
       "R and U are both at least S, but nothing links R with U directly, so I does not follow. U ≥ S > T gives U > T, which makes U ≥ T true, so II follows. Only II follows.",
       "R और U दोनों S से कम नहीं हैं, पर R और U का सीधा संबंध नहीं है, इसलिए I सही नहीं है। U ≥ S > T से U > T, जिससे U ≥ T सत्य है, इसलिए II सही है। केवल II सही है।")
    IQ("Medium", "K ≤ L = M, M ≥ N", "K < M", "K = M", "Either",
       "K ≤ L = M gives K ≤ M. Neither K < M nor K = M is certain on its own, but one of them must be true and they cover every case of K ≤ M. So either I or II follows.",
       "K ≤ L = M से K ≤ M. अकेले न K < M निश्चित है न K = M, पर इनमें से एक अवश्य सत्य है और ये K ≤ M की सभी स्थितियाँ समेटते हैं। इसलिए या तो I या II सही है।")
    IQ("Hard", "W > X, X < Y, Y ≥ Z", "W > Z", "Y > W", "Neither", 
       "W and Y are both greater than X but are not compared with each other, and Z is linked only through Y. So neither W > Z nor Y > W can be established. Neither follows.",
       "W और Y दोनों X से बड़े हैं पर आपस में तुलना नहीं है, और Z केवल Y के माध्यम से जुड़ा है। इसलिए न W > Z सिद्ध होता है न Y > W. कोई सही नहीं है।", shown="W > X < Y ≥ Z")
    IQ("Hard", "P < Q ≥ R = S, T ≥ S", "T > R", "T = R", "Either",
       "T ≥ S = R gives T ≥ R. Neither T > R nor T = R is certain, but together they cover every possibility, so either I or II follows.",
       "T ≥ S = R से T ≥ R. न T > R निश्चित है न T = R, पर दोनों मिलकर हर संभावना समेटते हैं, इसलिए या तो I या II सही है।")
    v = RC.ineq("A ≥ B, B = C, C > D", "A > D", "B ≥ D"); assert v == "Both"
    A(s,t,"Hard","In a certain code, 'P # Q' means P is not smaller than Q; 'P @ Q' means P is neither greater nor smaller than Q; 'P % Q' means P is greater than Q; and 'P &amp; Q' means P is smaller than Q.<br>Statements: A # B, B @ C, C % D<br>Conclusions: I. A % D II. B # D",SY,V["Both"],
      "Decoding: A ≥ B, B = C, C > D, i.e. A ≥ B = C > D. So A > D, which is A % D (I follows), and B > D, which makes 'B is not smaller than D' (B # D) true (II follows). Both follow.",
      "कोड खोलने पर: A ≥ B, B = C, C > D, यानी A ≥ B = C > D. इसलिए A > D, जो A % D है (I सही), और B > D, जिससे 'B, D से छोटा नहीं है' (B # D) सत्य है (II सही)। दोनों सही हैं।", chk=(v, "Both"))
    IQ("Medium", "X ≤ Y < Z, W > Z", "W > X", "Y ≥ W", "Only I",
       "W > Z > Y ≥ X gives W > X, so I follows. The same chain gives W > Y, so Y ≥ W is false. Only I follows.",
       "W > Z > Y ≥ X से W > X, इसलिए I सही है। इसी श्रृंखला से W > Y, इसलिए Y ≥ W असत्य है। केवल I सही है।")
    IQ("Hard", "J > K ≥ L, M ≤ L, N > M", "N > K", "J > M", "Only II",
       "N is greater than M only; it is not compared with K, so I does not follow. J > K ≥ L ≥ M gives J > M, so II follows. Only II follows.",
       "N केवल M से बड़ा है; इसकी K से तुलना नहीं है, इसलिए I सही नहीं है। J > K ≥ L ≥ M से J > M, इसलिए II सही है। केवल II सही है।")
    # ================= Number & Letter Series (+4) =================
    t = "Number & Letter Series"
    sq = [4]; [sq.append(sq[-1] * 3 - 2) for _ in range(5)]; assert sq == [4, 10, 28, 82, 244, 730]
    A(s,t,"Medium","Find the next term: 4, 10, 28, 82, 244, ?",["730","732","728","488"],"730",
      "Each term is 3 times the previous term minus 2: 4 × 3 − 2 = 10, 10 × 3 − 2 = 28, 28 × 3 − 2 = 82, 82 × 3 − 2 = 244, so the next is 244 × 3 − 2 = 730.",
      "हर पद पिछले पद का 3 गुना घटा 2 है: 4 × 3 − 2 = 10, 10 × 3 − 2 = 28, 28 × 3 − 2 = 82, 82 × 3 − 2 = 244, इसलिए अगला 244 × 3 − 2 = 730.", chk=(sq[-1], 730))
    given = [2, 5, 11, 23, 47, 96, 191]; right = [2]; [right.append(right[-1] * 2 + 1) for _ in range(6)]
    bad = [g for g, r in zip(given, right) if g != r]; assert bad == [96]
    A(s,t,"Hard","Find the wrong number in the series: 2, 5, 11, 23, 47, 96, 191",["96","47","191","23"],"96",
      "Each term should be 2 × (previous) + 1: 2, 5, 11, 23, 47, 95, 191. The term 96 should be 95 (and 2 × 95 + 1 = 191 confirms it), so 96 is wrong.",
      "हर पद 2 × (पिछला) + 1 होना चाहिए: 2, 5, 11, 23, 47, 95, 191. पद 96 के स्थान पर 95 होना चाहिए (और 2 × 95 + 1 = 191 इसकी पुष्टि करता है), इसलिए 96 गलत है।", chk=(bad[0], 96))
    grp = ["".join(AL[i + 2 * k] for k in range(3)) for i in range(1, 20, 6)]; assert grp[:4] == ["BDF", "HJL", "NPR", "TVX"]
    A(s,t,"Medium","Find the next term: BDF, HJL, NPR, ?",["TVX","TUV","SUW","UWY"],"TVX",
      "The letters run B, D, F, H, J, L, N, P, R, … skipping one letter each time, taken three at a time. The next group is T, V, X.",
      "अक्षर B, D, F, H, J, L, N, P, R, … हर बार एक अक्षर छोड़ते हुए तीन-तीन के समूह में चलते हैं। अगला समूह T, V, X है।", chk=(grp[3], "TVX"))
    sq = [n ** n for n in range(1, 6)]; assert sq == [1, 4, 27, 256, 3125]
    A(s,t,"Medium","Find the next term: 1, 4, 27, 256, ?",["3125","1024","625","3025"],"3125",
      "The terms are 1¹, 2², 3³, 4⁴, so the next term is 5⁵ = 3125.",
      "पद 1¹, 2², 3³, 4⁴ हैं, इसलिए अगला पद 5⁵ = 3125 है।", chk=(sq[-1], 3125))
    # ================= Odd One Out (+10) =================
    t = "Odd One Out"
    def odd(items, prop, want):
        out = [x for x in items if not prop(x)]; assert out == [want], out; return want
    isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))
    v = odd([13, 17, 19, 27, 29], isprime, 27)
    A(s,t,"Easy","Find the odd one out: 13, 17, 19, 27, 29",["27","17","19","29"],"27",
      "13, 17, 19 and 29 are prime numbers. 27 = 3 × 9 is not prime, so it is the odd one out.",
      "13, 17, 19 और 29 अभाज्य संख्याएँ हैं। 27 = 3 × 9 अभाज्य नहीं है, इसलिए यह भिन्न है।", chk=(v, 27))
    v = odd([216, 343, 512, 720, 1000], lambda n: round(n ** (1 / 3)) ** 3 == n, 720)
    A(s,t,"Medium","Find the odd one out: 216, 343, 512, 720, 1000",["720","343","512","1000"],"720",
      "216 = 6³, 343 = 7³, 512 = 8³ and 1000 = 10³ are perfect cubes. 720 is not a perfect cube (9³ = 729).",
      "216 = 6³, 343 = 7³, 512 = 8³ और 1000 = 10³ पूर्ण घन हैं। 720 पूर्ण घन नहीं है (9³ = 729)।", chk=(v, 720))
    v = odd(["Lion", "Tiger", "Leopard", "Wolf", "Cheetah"], lambda a: a != "Wolf", "Wolf")
    A(s,t,"Easy","Find the odd one out: Lion, Tiger, Leopard, Wolf, Cheetah",["Wolf","Tiger","Leopard","Cheetah"],"Wolf",
      "Lion, tiger, leopard and cheetah are all big cats (cat family). The wolf belongs to the dog family, so it is the odd one out.",
      "शेर, बाघ, तेंदुआ और चीता सभी बड़ी बिल्लियाँ (बिल्ली कुल) हैं। भेड़िया कुत्ता कुल का है, इसलिए यह भिन्न है।", chk=(v, "Wolf"))
    v = odd(["BCD", "FGH", "JKM", "PQR"], lambda w: all(pos(w[i + 1]) - pos(w[i]) == 1 for i in range(2)), "JKM")
    A(s,t,"Medium","Find the odd one out: BCD, FGH, JKM, PQR",["JKM","BCD","FGH","PQR"],"JKM",
      "BCD, FGH and PQR are three consecutive letters of the alphabet. In JKM, L is skipped between K and M, so JKM is the odd one out.",
      "BCD, FGH और PQR वर्णमाला के लगातार तीन अक्षर हैं। JKM में K और M के बीच L छूटा है, इसलिए JKM भिन्न है।", chk=(v, "JKM"))
    v = odd([35, 48, 63, 80, 100], lambda n: round((n + 1) ** 0.5) ** 2 == n + 1, 100)
    A(s,t,"Medium","Find the odd one out: 35, 48, 63, 80, 100",["100","48","63","80"],"100",
      "35 = 6² − 1, 48 = 7² − 1, 63 = 8² − 1 and 80 = 9² − 1. The pattern continues with 10² − 1 = 99, so 100 does not fit.",
      "35 = 6² − 1, 48 = 7² − 1, 63 = 8² − 1 और 80 = 9² − 1. यह क्रम 10² − 1 = 99 पर जाता है, इसलिए 100 मेल नहीं खाता।", chk=(v, 100))
    v = odd([(3, 27), (4, 64), (5, 125), (6, 216), (7, 350)], lambda p: p[0] ** 3 == p[1], (7, 350))
    A(s,t,"Medium","Find the odd pair: 3 : 27, 4 : 64, 5 : 125, 6 : 216, 7 : 350",["7 : 350","4 : 64","5 : 125","6 : 216"],"7 : 350",
      "In each pair the second number is the cube of the first: 3³ = 27, 4³ = 64, 5³ = 125, 6³ = 216. But 7³ = 343, not 350, so 7 : 350 is the odd pair.",
      "हर जोड़ी में दूसरी संख्या पहली का घन है: 3³ = 27, 4³ = 64, 5³ = 125, 6³ = 216. पर 7³ = 343 है, 350 नहीं, इसलिए 7 : 350 भिन्न जोड़ी है।", chk=(v, (7, 350)))
    v = odd(["Rupee", "Dollar", "Yen", "Euro", "Kilogram"], lambda w: w != "Kilogram", "Kilogram")
    A(s,t,"Easy","Find the odd one out: Rupee, Dollar, Yen, Euro, Kilogram",["Kilogram","Dollar","Yen","Euro"],"Kilogram",
      "Rupee, dollar, yen and euro are currencies. Kilogram is a unit of mass, so it is the odd one out.",
      "रुपया, डॉलर, येन और यूरो मुद्राएँ हैं। किलोग्राम द्रव्यमान की इकाई है, इसलिए यह भिन्न है।", chk=(v, "Kilogram"))
    v = odd(["ACE", "IKM", "OQS", "UWY", "EGJ"], lambda w: pos(w[1]) - pos(w[0]) == 2 and pos(w[2]) - pos(w[1]) == 2, "EGJ")
    A(s,t,"Medium","Find the odd one out: ACE, IKM, OQS, UWY, EGJ",["EGJ","IKM","OQS","UWY"],"EGJ",
      "In ACE, IKM, OQS and UWY each letter is 2 places after the previous one (A+2 = C, C+2 = E). In EGJ, G+2 would be I, not J, so EGJ is the odd one out.",
      "ACE, IKM, OQS और UWY में हर अक्षर पिछले से 2 स्थान आगे है (A+2 = C, C+2 = E)। EGJ में G+2 = I होना चाहिए, J नहीं, इसलिए EGJ भिन्न है।", chk=(v, "EGJ"))
    v = odd([121, 242, 363, 484, 595], lambda n: n % 121 == 0, 595)
    A(s,t,"Hard","Find the odd one out: 121, 242, 363, 484, 595",["595","242","363","484"],"595",
      "121, 242, 363 and 484 are 121 × 1, 121 × 2, 121 × 3 and 121 × 4. The next multiple would be 121 × 5 = 605; 595 is not a multiple of 121 (or even of 11), so it is the odd one out.",
      "121, 242, 363 और 484 क्रमशः 121 × 1, 121 × 2, 121 × 3 और 121 × 4 हैं। अगला गुणज 121 × 5 = 605 होता; 595, 121 का (और 11 का भी) गुणज नहीं है, इसलिए यह भिन्न है।", chk=(v, 595))
    v = odd([123, 234, 345, 456, 568], lambda n: [int(c) for c in str(n)] == [int(str(n)[0]) + k for k in range(3)], 568)
    A(s,t,"Easy","Find the odd one out: 123, 234, 345, 456, 568",["568","234","345","456"],"568",
      "123, 234, 345 and 456 are made of three consecutive digits in increasing order. In 568 the digit 7 is skipped, so it is the odd one out.",
      "123, 234, 345 और 456 बढ़ते क्रम में तीन लगातार अंकों से बनी हैं। 568 में अंक 7 छूटा है, इसलिए यह भिन्न है।", chk=(v, 568))
    # ================= Seating Arrangement (+8) =================
    def uniq(cands, cond):
        sol = [c for c in cands if cond(c)]; assert len(sol) == 1, sol; return sol[0]
    t = "Seating Arrangement"
    def lin_ok(p):
        i = {c: k for k, c in enumerate(p)}
        return i['D'] == 2 and abs(i['D'] - i['G']) == 3 and i['A'] == i['G'] + 1 and i['B'] in (0, 6) and abs(i['C'] - i['B']) == 1 and i['E'] < i['F']
    row = "".join(uniq(itertools.permutations("ABCDEFG"), lin_ok)); assert row == "BCDEFGA"
    lin = ("Seven friends A, B, C, D, E, F and G sit in a row facing north. D sits third from the left end. Exactly two persons sit between D and G. "
           "A sits immediately to the right of G. B sits at one of the ends, and C sits next to B. E sits somewhere to the left of F.")
    lsol = "Working through the clues gives the unique row (left to right): B C D E F G A. "
    lhi = "सुरागों से एकमात्र पंक्ति (बाएँ से दाएँ) बनती है: B C D E F G A. "
    A(s,t,"Medium",lin + "<br>Who sits at the right end of the row?",["A","G","B","F"],"A",
      lsol + "D is 3rd from the left; G, with two persons between, is 6th; A, immediately right of G, is 7th. B must be at the left end (the right end is taken) and C 2nd. E before F fills places 4 and 5. A is at the right end.",
      lhi + "D बाएँ से 3रा है; G, बीच में दो व्यक्तियों के साथ, 6ठा है; A, G के ठीक दाएँ, 7वाँ है। B बाएँ सिरे पर होगा (दायाँ सिरा भरा है) और C 2रा। E, F से पहले, स्थान 4 और 5 भरते हैं। दाएँ सिरे पर A है।", chk=(row[-1], "A"))
    A(s,t,"Medium",lin + "<br>Who sits exactly between D and F?",["E","C","G","B"],"E",
      lsol + "D is 3rd and F is 5th, so the person between them, 4th from the left, is E.",
      lhi + "D 3रा और F 5वाँ है, इसलिए उनके बीच बाएँ से 4था व्यक्ति E है।", chk=(row[3], "E"))
    A(s,t,"Medium",lin + "<br>How many persons sit between C and G?",["3","2","4","1"],"3",
      lsol + "C is 2nd and G is 6th from the left, so D, E and F — 3 persons — sit between them.",
      lhi + "C बाएँ से 2रा और G 6ठा है, इसलिए उनके बीच D, E और F — 3 व्यक्ति — बैठे हैं।", chk=(row.index('G') - row.index('C') - 1, 3))
    A(s,t,"Medium",lin + "<br>Who sits second to the right of E?",["G","F","A","D"],"G",
      lsol + "E is 4th from the left; two places to the right (facing north, right is towards the right end) is the 6th seat, G.",
      lhi + "E बाएँ से 4था है; दो स्थान दाएँ (उत्तर की ओर मुख होने पर दायाँ यानी दाएँ सिरे की ओर) 6ठा स्थान G है।", chk=(row[row.index('E') + 2], "G"))
    def circ_ok(p):
        seat = ("P",) + p; i = {c: k for k, c in enumerate(seat)}
        R = lambda x, k: seat[(i[x] - k) % 8]; L = lambda x, k: seat[(i[x] + k) % 8]
        return R('P', 4) == 'S' and R('P', 2) == 'U' and R('S', 1) == 'T' and L('T', 2) == 'Q' and L('P', 1) == 'V' and 'W' not in (R('P', 1), L('P', 1))
    cs = ("P",) + uniq(itertools.permutations("VWTSQUR"), circ_ok); assert "".join(cs) == "PVWTSQUR"
    ci = {c: k for k, c in enumerate(cs)}; opp = lambda x: cs[(ci[x] + 4) % 8]
    circ = ("Eight persons P, Q, R, S, T, U, V and W sit around a circular table facing the centre. S sits opposite P. U sits second to the right of P. "
            "T sits immediately to the right of S. Q sits second to the left of T. V sits immediately to the left of P. W is not an immediate neighbour of P.")
    csol = "Facing the centre, 'right' is anticlockwise. Placing P first, the clues give the unique clockwise order P, V, W, T, S, Q, U, R. "
    chi = "केंद्र की ओर मुख होने पर 'दायाँ' वामावर्त है। P को पहले रखने पर सुरागों से एकमात्र दक्षिणावर्त क्रम P, V, W, T, S, Q, U, R बनता है। "
    A(s,t,"Hard",circ + "<br>Who sits opposite V?",["Q","U","T","R"],"Q",
      csol + "S is opposite P, U two seats anticlockwise of P, T next to S anticlockwise, Q two seats clockwise of T, V next to P clockwise; W cannot be next to P, so W takes the seat after V and R the seat before P. Opposite V is Q.",
      chi + "S, P के सामने है, U, P से दो स्थान वामावर्त, T, S के बगल में वामावर्त, Q, T से दो स्थान दक्षिणावर्त, V, P के बगल में दक्षिणावर्त; W, P के बगल में नहीं हो सकता, इसलिए W, V के बाद और R, P से पहले वाले स्थान पर है। V के सामने Q है।", chk=(opp('V'), "Q"))
    A(s,t,"Hard",circ + "<br>Who sits immediately to the right of W?",["V","T","R","S"],"V",
      csol + "Immediate right means the next seat anticlockwise. Anticlockwise from W comes V.",
      chi + "ठीक दाएँ का अर्थ अगला वामावर्त स्थान है। W से वामावर्त अगला V है।", chk=(cs[(ci['W'] - 1) % 8], "V"))
    A(s,t,"Hard",circ + "<br>Who sits third to the left of S?",["R","U","W","V"],"R",
      csol + "Left means clockwise. Going clockwise from S: Q (1st), U (2nd), R (3rd).",
      chi + "बायाँ यानी दक्षिणावर्त। S से दक्षिणावर्त: Q (1ला), U (2रा), R (3रा)।", chk=(cs[(ci['S'] + 3) % 8], "R"))
    A(s,t,"Hard",circ + "<br>Who sits opposite R?",["T","W","S","Q"],"T",
      csol + "R and T are four seats apart, so T sits opposite R.",
      chi + "R और T के बीच चार स्थान का अंतर है, इसलिए R के सामने T है।", chk=(opp('R'), "T"))
    # ================= Puzzles (+10) =================
    t = "Puzzles"
    def p1_ok(p):
        f = {c: k + 1 for k, c in enumerate(p)}
        return f['K'] % 2 == 1 and f['K'] > 4 and abs(f['K'] - f['N']) == 3 and f['L'] == f['N'] - 1 and f['O'] < f['M'] < f['J'] and f['P'] == f['J'] + 1 and f['P'] % 2 == 0
    fl = "".join(uniq(itertools.permutations("JKLMNOP"), p1_ok)); assert fl == "OMLNJPK"; fo = {c: k + 1 for k, c in enumerate(fl)}
    p1 = ("Seven persons J, K, L, M, N, O and P live on different floors of a 7-storey building (ground floor = floor 1, top floor = floor 7). "
          "K lives on an odd-numbered floor above floor 4. Exactly two persons live between K and N. L lives immediately below N. "
          "O lives below M, and M lives below J. P lives immediately above J, on an even-numbered floor.")
    p1s = "Brute-force over all orders leaves one arrangement (floor 1 to 7): O, M, L, N, J, P, K. "
    p1h = "सभी क्रमों की जाँच के बाद एक ही व्यवस्था बचती है (मंज़िल 1 से 7): O, M, L, N, J, P, K. "
    A(s,t,"Hard",p1 + "<br>Who lives on floor 5?",["J","N","P","M"],"J",
      p1s + "If K were on floor 5, N would be on floor 2 and L on floor 1, leaving no room for O < M < J with P immediately above J on an even floor. So K is on floor 7, N on 4, L on 3; P must be on 6 with J on 5, and O, M take floors 1 and 2. Floor 5 is J.",
      p1h + "यदि K मंज़िल 5 पर हो तो N मंज़िल 2 पर और L मंज़िल 1 पर होगा, तब O < M < J तथा J के ठीक ऊपर सम मंज़िल पर P के लिए जगह नहीं बचती। इसलिए K मंज़िल 7 पर, N 4 पर, L 3 पर; P मंज़िल 6 पर और J 5 पर, तथा O, M मंज़िल 1 और 2 पर। मंज़िल 5 पर J है।", chk=(fl[4], "J"))
    A(s,t,"Hard",p1 + "<br>How many persons live between M and K?",["4","3","5","2"],"4",
      p1s + "M is on floor 2 and K on floor 7, so L, N, J and P — 4 persons — live between them.",
      p1h + "M मंज़िल 2 पर और K मंज़िल 7 पर है, इसलिए बीच में L, N, J और P — 4 व्यक्ति — रहते हैं।", chk=(fo['K'] - fo['M'] - 1, 4))
    A(s,t,"Hard",p1 + "<br>Who lives immediately above L?",["N","M","J","O"],"N",
      p1s + "L is on floor 3, and floor 4 belongs to N.",
      p1h + "L मंज़िल 3 पर है, और मंज़िल 4 पर N है।", chk=(fl[fo['L']], "N"))
    A(s,t,"Hard",p1 + "<br>On which floor does O live?",["1","2","3","4"],"1",
      p1s + "O, below M, takes floor 1.",
      p1h + "O, M के नीचे, मंज़िल 1 पर है।", chk=(fo['O'], 1))
    def p2_ok(p):
        d = {c: k for k, c in enumerate(p)}
        return d['W'] == 2 and abs(d['W'] - d['Y']) == 2 and d['Y'] != 0 and d['U'] == d['X'] + 1 and d['Z'] < d['V']
    wk = "".join(uniq(itertools.permutations("UVWXYZ"), p2_ok)); assert wk == "XUWZYV"; days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    p2 = ("Six lectures U, V, W, X, Y and Z are held on six consecutive days from Monday to Saturday, one per day. W is held on Wednesday. "
          "Exactly one lecture is held between W and Y. Y is not held on Monday. U is held on the day immediately after X. Z is held on some day before V.")
    p2s = "The arrangement is unique: Monday X, Tuesday U, Wednesday W, Thursday Z, Friday Y, Saturday V. "
    p2h = "व्यवस्था एकमात्र है: सोमवार X, मंगलवार U, बुधवार W, गुरुवार Z, शुक्रवार Y, शनिवार V. "
    A(s,t,"Medium",p2 + "<br>Which lecture is held on Thursday?",["Z","Y","V","U"],"Z",
      p2s + "Y is two days from Wednesday and not on Monday, so Y is on Friday. X–U must be consecutive among Monday, Tuesday, Thursday and Saturday, so X is Monday and U Tuesday. Z before V leaves Z on Thursday and V on Saturday.",
      p2h + "Y बुधवार से दो दिन दूर है और सोमवार को नहीं, इसलिए Y शुक्रवार को है। X–U सोमवार, मंगलवार, गुरुवार और शनिवार में लगातार होने चाहिए, इसलिए X सोमवार और U मंगलवार। Z, V से पहले होने के कारण Z गुरुवार और V शनिवार।", chk=(wk[3], "Z"))
    A(s,t,"Medium",p2 + "<br>How many lectures are held between U and Y?",["2","1","3","0"],"2",
      p2s + "U is on Tuesday and Y on Friday, so W and Z — 2 lectures — fall between them.",
      p2h + "U मंगलवार और Y शुक्रवार को है, इसलिए बीच में W और Z — 2 व्याख्यान — हैं।", chk=(wk.index('Y') - wk.index('U') - 1, 2))
    A(s,t,"Medium",p2 + "<br>On which day is V held?",["Saturday","Thursday","Friday","Tuesday"],"Saturday",
      p2s + "V is the last lecture, on Saturday.",
      p2h + "V अंतिम व्याख्यान है, शनिवार को।", chk=(days[wk.index('V')], "Saturday"))
    def p3_ok(p):
        r = {c: k for k, c in enumerate(p)}
        return r['C'] == 3 and r['E'] < r['A'] < r['C'] and r['F'] > r['D'] and r['B'] != 5 and r['E'] != 0 and r['D'] < r['B']
    ht = "".join(uniq(itertools.permutations("ABCDEF"), p3_ok)); assert ht == "DEACBF"
    p3 = ("Six friends A, B, C, D, E and F have different heights. C is taller than only two of them. E is taller than A, and A is taller than C. "
          "F is shorter than D. B is not the shortest. E is not the tallest. D is taller than B.")
    p3s = "The unique order from tallest to shortest is D, E, A, C, B, F. "
    p3h = "लंबे से छोटे का एकमात्र क्रम D, E, A, C, B, F है। "
    A(s,t,"Medium",p3 + "<br>Who is the tallest?",["D","E","A","B"],"D",
      p3s + "C is 4th tallest, so B and F are the two below C. E and A are above C; D is taller than both B and F, so D cannot be among the two below C, and D, E, A fill the top three; E is not the tallest and A is below E, so D is tallest, then E, then A. B is not the shortest, so B is 5th and F 6th.",
      p3h + "C 4था सबसे लंबा है, इसलिए B और F, C से नीचे के दो हैं। E और A, C से ऊपर हैं; D, B और F दोनों से लंबा है, इसलिए D, C से नीचे के दो में नहीं हो सकता, और D, E, A ऊपर के तीन स्थान भरते हैं; E सबसे लंबा नहीं है और A, E से नीचे है, इसलिए D सबसे लंबा, फिर E, फिर A. B सबसे छोटा नहीं है, इसलिए B 5वाँ और F 6ठा।", chk=(ht[0], "D"))
    A(s,t,"Medium",p3 + "<br>Who is the second shortest?",["B","C","F","A"],"B",
      p3s + "From the shortest: F, then B. B is second shortest.",
      p3h + "सबसे छोटे से: F, फिर B. दूसरा सबसे छोटा B है।", chk=(ht[-2], "B"))
    A(s,t,"Medium",p3 + "<br>How many friends are taller than A?",["2","1","3","4"],"2",
      p3s + "Only D and E are taller than A: 2 friends.",
      p3h + "केवल D और E, A से लंबे हैं: 2 मित्र।", chk=(ht.index('A'), 2))
    # ================= Ranking & Order (+10) =================
    t = "Ranking & Order"
    v = 45 - 17 + 1; assert v == 29
    A(s,t,"Easy","In a row of 45 children, Neha is 17th from the right end. What is her position from the left end?",["29th","28th","30th","27th"],"29th",
      "Position from left = total − position from right + 1 = 45 − 17 + 1 = 29th.",
      "बाएँ से स्थान = कुल − दाएँ से स्थान + 1 = 45 − 17 + 1 = 29वाँ।", chk=(v, 29))
    ok = [N for N in range(5, 40) if N - 8 + 1 >= 1 and abs(5 - (N - 8 + 1)) - 1 == 3]
    v = min(ok); assert v == 8 and sorted(ok) == [8, 16]
    A(s,t,"Hard","In a queue, Amit is 5th from the front and Bina is 8th from the back. Exactly 3 persons stand between Amit and Bina. What is the minimum possible number of persons in the queue?",["8","16","9","15"],"8",
      "Bina's position from the front is N − 8 + 1 = N − 7. With 3 persons between them, the two positions differ by 4: either N − 7 = 9 (Bina behind Amit), giving N = 16, or N − 7 = 1 (Bina ahead of Amit), giving N = 8. The minimum is 8: Bina 1st, three persons, then Amit 5th, and three more behind him.",
      "आगे से बीना का स्थान N − 8 + 1 = N − 7 है। बीच में 3 व्यक्ति होने से दोनों स्थानों में 4 का अंतर है: या तो N − 7 = 9 (बीना अमित के पीछे), जिससे N = 16, या N − 7 = 1 (बीना अमित के आगे), जिससे N = 8. न्यूनतम 8 है: बीना 1ली, तीन व्यक्ति, फिर अमित 5वाँ, और उसके पीछे तीन और।", chk=(v, 8))
    v = (7 + 26 - 1) + 5 + 3; assert v == 40
    A(s,t,"Medium","Among the students who passed an exam, Ravi ranked 7th from the top and 26th from the bottom. If 5 students failed and 3 were absent, how many students are in the class?",["40","32","37","38"],"40",
      "Students who passed = 7 + 26 − 1 = 32. Adding 5 who failed and 3 who were absent: 32 + 5 + 3 = 40.",
      "उत्तीर्ण छात्र = 7 + 26 − 1 = 32. 5 अनुत्तीर्ण और 3 अनुपस्थित जोड़ने पर: 32 + 5 + 3 = 40.", chk=(v, 40))
    v = 40 - (9 + 6) + 1; assert v == 26
    A(s,t,"Medium","In a class of 40 students, Sita ranks 9th from the top. Mira is 6 ranks below Sita. What is Mira's rank from the bottom?",["26th","25th","31st","27th"],"26th",
      "Mira's rank from the top = 9 + 6 = 15th. From the bottom: 40 − 15 + 1 = 26th.",
      "ऊपर से मीरा की रैंक = 9 + 6 = 15वीं। नीचे से: 40 − 15 + 1 = 26वीं।", chk=(v, 26))
    sc = uniq(itertools.permutations("PQRST"), lambda o: o.index('Q') < o.index('S') and o.index('P') < o.index('Q') and o.index('T') < o.index('P') and o.index('R') < o.index('T'))
    assert "".join(sc) == "RTPQS"
    A(s,t,"Medium","In a test, Q scored more than S but less than P. T scored less than R but more than P. Who scored the second lowest?",["Q","P","S","T"],"Q",
      "S < Q < P and P < T < R combine into R > T > P > Q > S. The lowest is S, so the second lowest is Q.",
      "S < Q < P और P < T < R मिलकर R > T > P > Q > S देते हैं। सबसे कम S है, इसलिए दूसरा सबसे कम Q है।", chk=(sc[-2], "Q"))
    v = 50 - 25 + 1; assert v == 26
    A(s,t,"Easy","In a row of 50 students, Bharat is 25th from the left end. What is his position from the right end?",["26th","25th","24th","27th"],"26th",
      "Position from right = 50 − 25 + 1 = 26th.",
      "दाएँ से स्थान = 50 − 25 + 1 = 26वाँ।", chk=(v, 26))
    v = 20 + 20 - 1; assert v == 39
    A(s,t,"Easy","Arjun is 20th from the top and also 20th from the bottom in a class ranking. How many students are in the class?",["39","40","41","38"],"39",
      "Total = 20 + 20 − 1 = 39 (Arjun is counted in both positions).",
      "कुल = 20 + 20 − 1 = 39 (अर्जुन दोनों स्थितियों में गिना गया है)।", chk=(v, 39))
    def w_ok(o):
        i = {c: k for k, c in enumerate(o)}  # heaviest first
        return i['U'] == 5 and i['Q'] == 4 and i['S'] < i['Q'] and i['P'] < i['S'] and i['R'] < i['P'] and i['R'] != 0
    wt = uniq(itertools.permutations("PQRSTU"), w_ok); assert "".join(wt) == "TRPSQU"
    A(s,t,"Hard","Six boxes P, Q, R, S, T and U have different weights. Q is heavier than U only. S is heavier than Q but lighter than P. R is heavier than P but is not the heaviest. Which box is the third heaviest?",["P","R","S","T"],"P",
      "Q heavier than U only means U is lightest and Q 5th. Then S > Q, P > S and R > P give R > P > S above Q. R is not the heaviest, so T is. Order: T, R, P, S, Q, U. The third heaviest is P.",
      "Q केवल U से भारी है, यानी U सबसे हल्का और Q 5वाँ। फिर S > Q, P > S और R > P से Q के ऊपर R > P > S. R सबसे भारी नहीं है, इसलिए T सबसे भारी है। क्रम: T, R, P, S, Q, U. तीसरा सबसे भारी P है।", chk=(wt[2], "P"))
    v = 35 - (10 + 4) + 1; assert v == 22
    A(s,t,"Medium","Mohan is 10th from the left end in a row of 35 boys. If he shifts 4 places to the right, what will be his position from the right end?",["22nd","21st","26th","23rd"],"22nd",
      "After the shift he is 10 + 4 = 14th from the left, so from the right he is 35 − 14 + 1 = 22nd.",
      "खिसकने के बाद वह बाएँ से 10 + 4 = 14वाँ है, इसलिए दाएँ से 35 − 14 + 1 = 22वाँ।", chk=(v, 22))
    N = 18 + 12 - 1; v = N - 7 + 1; assert N == 29 and v == 23
    A(s,t,"Hard","In a row, X is 7th from the left and Y is 12th from the right. When X and Y interchange their positions, X becomes 18th from the left. What is Y's new position from the right?",["23rd","22nd","24th","19th"],"23rd",
      "After the swap X is in Y's old seat, which is 18th from the left and 12th from the right, so the row has 18 + 12 − 1 = 29 persons. Y now sits in X's old seat, 7th from the left, which is 29 − 7 + 1 = 23rd from the right.",
      "अदला-बदली के बाद X, Y की पुरानी जगह पर है, जो बाएँ से 18वीं और दाएँ से 12वीं है, इसलिए पंक्ति में 18 + 12 − 1 = 29 व्यक्ति हैं। Y अब X की पुरानी जगह, बाएँ से 7वीं पर है, जो दाएँ से 29 − 7 + 1 = 23वीं है।", chk=(v, 23))
    # ================= Syllogisms (+5) =================
    t = "Syllogisms"
    def SG(diff, names, sts, cons, want, stext, ctext, sol, hi):
        res, eit = RC.syllo(names, sts, cons); v = RC.verdict(res, eit); assert v == want, (stext, v)
        A(s, t, diff, f"Statements: {stext}<br>Conclusions: I. {ctext[0]} II. {ctext[1]}", SYE if want == "Either" else SY, V[want], sol, hi, chk=(v, want))
    SG("Medium", ["key", "lock", "door", "window"], [("all", "key", "lock"), ("some", "lock", "door"), ("no", "door", "window")],
       [("def", ("somenot", "lock", "window")), ("def", ("some", "key", "window"))], "Only I",
       "All keys are locks. Some locks are doors. No door is a window.", ["Some locks are not windows.", "Some keys are windows."],
       "The locks that are doors cannot be windows, because no door is a window, so some locks are not windows: I follows. Keys are not linked to windows by any statement, so II is not certain. Only I follows.",
       "जो ताले दरवाज़े हैं वे खिड़कियाँ नहीं हो सकते, क्योंकि कोई दरवाज़ा खिड़की नहीं है, इसलिए कुछ ताले खिड़कियाँ नहीं हैं: I सही है। चाबियों का खिड़कियों से कोई कथन संबंध नहीं बनाता, इसलिए II निश्चित नहीं है। केवल I सही है।")
    SG("Medium", ["river", "lake", "pond", "well"], [("some", "river", "lake"), ("all", "lake", "pond"), ("no", "pond", "well")],
       [("def", ("somenot", "river", "well")), ("def", ("some", "lake", "well"))], "Only I",
       "Some rivers are lakes. All lakes are ponds. No pond is a well.", ["Some rivers are not wells.", "Some lakes are wells."],
       "The rivers that are lakes are also ponds, and no pond is a well, so those rivers are not wells: I follows. Every lake is a pond and no pond is a well, so no lake is a well: II is false. Only I follows.",
       "जो नदियाँ झीलें हैं वे तालाब भी हैं, और कोई तालाब कुआँ नहीं है, इसलिए वे नदियाँ कुएँ नहीं हैं: I सही है। हर झील तालाब है और कोई तालाब कुआँ नहीं, इसलिए कोई झील कुआँ नहीं: II असत्य है। केवल I सही है।")
    SG("Medium", ["pen", "marker", "crayon"], [("some", "pen", "marker"), ("somenot", "marker", "crayon"), ("all", "crayon", "pen")],
       [("def", ("some", "marker", "crayon")), ("def", ("some", "pen", "crayon"))], "Only II",
       "Some pens are markers. Some markers are not crayons. All crayons are pens.", ["Some markers are crayons.", "Some pens are crayons."],
       "Nothing forces any marker to be a crayon (the markers may lie wholly outside crayons), so I does not follow. Crayons exist and every crayon is a pen, so some pens are crayons: II follows. Only II follows.",
       "कोई कथन किसी मार्कर को क्रेयॉन होने पर बाध्य नहीं करता (मार्कर पूरी तरह क्रेयॉन से बाहर हो सकते हैं), इसलिए I सही नहीं है। क्रेयॉन मौजूद हैं और हर क्रेयॉन पेन है, इसलिए कुछ पेन क्रेयॉन हैं: II सही है। केवल II सही है।")
    SG("Hard", ["bird", "eagle", "hunter"], [("some", "bird", "eagle"), ("somenot", "bird", "eagle"), ("all", "eagle", "hunter")],
       [("def", ("some", "bird", "hunter")), ("def", ("all", "bird", "hunter"))], "Only I",
       "Only a few birds are eagles. All eagles are hunters.", ["Some birds are hunters.", "All birds are hunters."],
       "'Only a few birds are eagles' means some birds are eagles and some birds are not. The birds that are eagles are hunters, so some birds are hunters: I follows. The birds that are not eagles may or may not be hunters, so II is not certain. Only I follows.",
       "'केवल कुछ पक्षी चील हैं' का अर्थ है कुछ पक्षी चील हैं और कुछ नहीं। जो पक्षी चील हैं वे शिकारी हैं, इसलिए कुछ पक्षी शिकारी हैं: I सही है। जो पक्षी चील नहीं हैं वे शिकारी हो भी सकते हैं और नहीं भी, इसलिए II निश्चित नहीं है। केवल I सही है।")
    SG("Hard", ["fan", "cooler", "heater", "light"], [("all", "fan", "cooler"), ("some", "cooler", "heater"), ("no", "heater", "light")],
       [("pos", ("some", "fan", "heater")), ("pos", ("all", "light", "fan"))], "Both",
       "All fans are coolers. Some coolers are heaters. No heater is a light.", ["Some fans being heaters is a possibility.", "All lights being fans is a possibility."],
       "Fans and heaters can overlap inside coolers, so I is possible. Lights only have to stay away from heaters; they can all sit inside the part of fans that is not heaters, so II is also possible. Both follow.",
       "पंखे और हीटर कूलर के अंदर ओवरलैप कर सकते हैं, इसलिए I संभव है। लाइटों को केवल हीटरों से अलग रहना है; वे सभी पंखों के उस भाग में हो सकती हैं जो हीटर नहीं है, इसलिए II भी संभव है। दोनों सही हैं।")
