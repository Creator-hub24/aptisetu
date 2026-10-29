"""Practice pack b2, DILR (original sets, added 29 Oct 2026). Each set is solved here by brute force over every
possible arrangement; the build stops unless exactly one arrangement fits the clues, and every answer is read from it."""
import itertools, collections
from fractions import Fraction as F

def ul(items): return "<ul class='clues'>" + "".join(f"<li>{c}</li>" for c in items) + "</ul>"

def build(B):
    s = "dilr"
    # ---------- Set 1: knights and knaves (Logic puzzles) ----------
    def kk(bclaim):
        def st(t):
            A, B_, C, D, E, F_ = t; k = sum(t)
            return [not B_, bclaim(k), (not D) or A, E == F_, A == D, (not C) or (not E)]
        return [t for t in itertools.product([True, False], repeat=6) if all(v == t[i] for i, v in enumerate(st(t)))]
    sol = kk(lambda k: k == 3); assert len(sol) == 1; t = sol[0]; P = "ABCDEF"
    knights = [P[i] for i in range(6) if t[i]]; assert knights == ["B", "C", "E"]
    alt = kk(lambda k: k == 4); assert len(alt) == 1; altk = [P[i] for i in range(6) if alt[0][i]]; assert altk == ["A", "C", "F"]
    B.add_set("b2-knights", "dilr", "Knights and knaves (Hard)",
        "<b>Knights and knaves</b><p>On an island every inhabitant is either a <i>knight</i>, who always tells the truth, or a <i>knave</i>, who always lies. Six inhabitants, A, B, C, D, E and F, make one statement each:</p>"
        + ul(["A: “B is a knave.”", "B: “Exactly three of us six are knights.”", "C: “D is a knave, or A is a knight.”",
              "D: “E and F are of the same type.”", "E: “A and D are of the same type.”", "F: “C is a knave, or E is a knave.”"])
        + "<p>(“X or Y” is true when at least one of X, Y is true.)</p>")
    exp = ("Split on B. If B is a knave, A's 'B is a knave' is true, so A is a knight, and C's statement is true (A is a knight), so C is a knight. If E were a knight, D would match A (a knight), D's 'E and F same type' would make F a knight, and F's 'C or E is a knave' would be false — impossible. So E is a knave, D differs from A (a knave), D's lie means F differs from E (F a knight), and F's 'E is a knave' is true ✓. That gives exactly three knights (A, C, F), which makes B's claim true — but B was assumed a knave. So B is a knight. "
           "Then A is a knave. If E were a knave, D would differ from A (a knight), so E and F match (F a knave), and F's lie would need both C and E to be knights — but E is a knave. So E is a knight, D is a knave (same as A), D's lie means F differs from E (F a knave), and F's lie means C and E are both knights; C's 'D is a knave or A is a knight' is true ✓. "
           "Result: B, C and E are knights; A, D and F are knaves (three knights, so B told the truth ✓). A computer check of all 64 possible assignments confirms this is the only consistent one.")
    T, M = (lambda *a, **k: B.tita(s, *a, set_id="b2-knights", **k)), (lambda *a, **k: B.mcq(s, *a, set_id="b2-knights", **k))
    T("Logic puzzles", "Medium", "How many of the six are knights?", len(knights), exp + " So there are 3 knights.")
    M("Logic puzzles", "Medium", "Which one of the following is a knight?", ["A", "D", "E", "F"], "E", exp + " Of the options, only E is a knight.")
    pairs = {"A and B": t[0] == t[1], "B and D": t[1] == t[3], "C and E": t[2] == t[4], "D and E": t[3] == t[4]}
    assert [k for k, v in pairs.items() if v] == ["C and E"]
    M("Logic puzzles", "Medium", "Which of the following pairs are of the same type?", list(pairs), "C and E", exp + " C and E are both knights; each of the other pairs has one knight and one knave.")
    M("Logic puzzles", "Hard", "Suppose B's statement were instead “Exactly four of us six are knights”, and all the other statements stayed the same. Who would then be the knights?",
      ["A, C and F only", "B, C and E only", "C only", "A and C only"], "A, C and F only",
      "First, B cannot be a knight: then A is a knave; if E is a knight, D is a knave (same as A), D's lie makes F a knave, and F's lie makes C and E knights — only B, C, E are knights, three not four; if E is a knave, D is a knight, D's truth makes F a knave like E, and F's lie needs E to be a knight — impossible. So B is a knave. Then A's 'B is a knave' is true, so A is a knight; C's statement is then true (A is a knight), so C is a knight. E says A and D are the same type: if E were a knight, D would be a knight, but D's 'E and F same type' would force F to be a knight too, and F's 'C or E is a knave' would be false — a contradiction. So E is a knave, D is a knave (different from A), and D's lie means E and F differ, so F is a knight; F's claim 'E is a knave' is indeed true. Knights: A, C, F — three, so B's 'four' is false, consistent. A full check of all 64 assignments gives only this one.")
    # ---------- Set 2: floors, pets and jobs (Logic puzzles) ----------
    N = ["Arjun", "Bina", "Chetan", "Divya", "Esha"]; PET = ["cat", "dog", "parrot", "fish", "rabbit"]; PRO = ["doctor", "lawyer", "teacher", "engineer", "pilot"]
    cl = [lambda f, p, r: f[r.index('pilot')] > f[p.index('dog')] and f[p.index('dog')] == f[r.index('teacher')] + 1,
          lambda f, p, r: f[0] + 1 == f[p.index('rabbit')],
          lambda f, p, r: f[r.index('doctor')] % 2 == 1 and p[r.index('doctor')] not in ('cat', 'dog'),
          lambda f, p, r: r[1] not in ('teacher', 'pilot') and f[1] % 2 == 0,
          lambda f, p, r: f[p.index('fish')] + 3 == f[p.index('dog')],
          lambda f, p, r: p[r.index('lawyer')] == 'cat',
          lambda f, p, r: f[3] < f[4] < f[1]]
    sols = [(f, p, r) for f in itertools.permutations(range(1, 6)) for p in itertools.permutations(PET) for r in itertools.permutations(PRO) if all(c(f, p, r) for c in cl)]
    assert len(sols) == 1, len(sols); f, p, r = sols[0]
    B.add_set("b2-floors", "dilr", "Floors, pets and jobs (Medium)",
        "<b>Floors, pets and jobs</b><p>Arjun, Bina, Chetan, Divya and Esha live on floors 1 to 5 of a building (floor 1 is the lowest), one person per floor. Each has a different pet — cat, dog, parrot, fish, rabbit — and a different job — doctor, lawyer, teacher, engineer, pilot.</p>"
        + ul(["The pilot lives above the dog owner, and the dog owner lives on the floor immediately above the teacher.",
              "Arjun lives on the floor immediately below the rabbit owner.",
              "The doctor lives on an odd-numbered floor and owns neither the cat nor the dog.",
              "Bina lives on an even-numbered floor and is neither the teacher nor the pilot.",
              "The fish owner lives exactly three floors below the dog owner.",
              "The lawyer owns the cat.",
              "Esha lives above Divya but below Bina."]))
    full = "; ".join(f"floor {fl}: {N[i]} ({p[i]}, {r[i]})" for fl in range(1, 6) for i in range(5) if f[i] == fl)
    exp = ("Fish is three floors below dog, so (fish, dog) is on floors (1, 4) or (2, 5). The dog owner is immediately above the teacher and below the pilot, so the dog cannot be on floor 5: fish on 1, dog on 4, teacher on 3 and pilot on 5. "
           "Bina is on an even floor above Esha, who is above Divya, so Bina is on floor 4 (the dog owner). Arjun is immediately below someone, so Arjun is not on 5: Chetan is on 5 and is the pilot. "
           "The doctor is on an odd floor other than 3 (teacher) and 5 (pilot), so on floor 1 with the fish. The lawyer owns the cat, so the lawyer is not on floor 1 (fish), 3 (teacher), 4 (dog) or 5 (pilot): the lawyer is on floor 2 with the cat. "
           "So the rabbit is not on floor 2 and Arjun cannot be on floor 1; Arjun is on floor 2 (lawyer, cat) with the rabbit on floor 3. Divya is below Esha, so Divya is on 1 and Esha on 3. "
           "Bina is the remaining engineer and Chetan has the remaining parrot. Final: " + full + ". (A computer check of every arrangement finds only this one.)")
    T, M = (lambda *a, **k: B.tita(s, *a, set_id="b2-floors", **k)), (lambda *a, **k: B.mcq(s, *a, set_id="b2-floors", **k))
    who3 = N[f.index(3)]; assert who3 == "Esha"
    M("Logic puzzles", "Medium", "Who lives on floor 3?", ["Arjun", "Esha", "Divya", "Chetan"], who3, exp)
    pp = p[r.index('pilot')]; assert pp == "parrot"
    M("Logic puzzles", "Medium", "Which pet does the pilot own?", ["Dog", "Cat", "Parrot", "Rabbit"], "Parrot", exp + " The pilot is Chetan, who owns the parrot.")
    above = sum(1 for i in range(5) if f[i] > f[r.index('lawyer')]); assert above == 3
    T("Logic puzzles", "Medium", "How many people live above the lawyer?", above, exp + f" The lawyer is {N[r.index('lawyer')]} on floor {f[r.index('lawyer')]}, so {above} people live above.")
    opts = {"The doctor owns the fish.": p[r.index('doctor')] == 'fish', "Bina is the lawyer.": r[1] == 'lawyer',
            "The rabbit owner lives on floor 4.": f[p.index('rabbit')] == 4, "Chetan owns the dog.": p[2] == 'dog'}
    assert [k for k, v in opts.items() if v] == ["The doctor owns the fish."]
    M("Logic puzzles", "Medium", "Which one of the following is true?", list(opts), "The doctor owns the fish.", exp)
    # ---------- Set 3: unique-number game (Games with rules) ----------
    def score(pk):
        c = collections.Counter(pk); return tuple(x if c[x] == 1 else 0 for x in pk)
    rounds = list(itertools.product(range(1, 5), repeat=4))
    R0 = [x for x in rounds if x[1] == 4 and len(set(x)) < 4]
    R1 = [x for x in rounds if max(collections.Counter(x).values()) == 3]
    R2 = [x for x in rounds if len(set(x)) < 4 and score(x)[0] > 0]
    sols = []
    for a in R0:
        for b in R1:
            for c in R2:
                tot = tuple(score(a)[i] + score(b)[i] + score(c)[i] for i in range(4))
                if tot == (4, 1, 5, 2) and len({a[2], b[2], c[2]}) == 3 and sum(a) + sum(b) + sum(c) == 33: sols.append((a, b, c))
    assert len(sols) == 1, len(sols); g = sols[0]; assert g == ((4, 4, 1, 2), (3, 3, 4, 3), (4, 1, 2, 2))
    B.add_set("b2-unique", "dilr", "The unique-number game (Hard)",
        "<b>The unique-number game</b><p>Four players, P, Q, R and S, play three rounds of a game. In each round every player secretly writes a whole number from 1 to 4; different players may write the same number. When the numbers are revealed, a player scores the number he wrote if nobody else wrote that number in that round; otherwise he scores 0 for the round.</p>"
        + ul(["In every round, at least two players wrote the same number.", "Q wrote 4 in round 1.",
              "In round 2, exactly three players wrote the same number.", "P scored in round 3.",
              "R wrote a different number in each round.",
              "At the end of the three rounds, the total scores were P 4, Q 1, R 5 and S 2.",
              "The twelve numbers written add up to 33."]))
    exp = ("Count scoring turns. R's 5 must come from two different numbers (1 + 4 or 2 + 3), so R scores in exactly two rounds; P, Q and S each score at least once. That is at least 5 scoring turns. A round with a repeated number has at most 2 scorers, and round 2 has exactly 1, so there are at most 2 + 1 + 2 = 5. Hence exactly 5: P scores once (4, in round 3), Q once (1), S once (2), R twice, and rounds 1 and 3 have two scorers each. "
           "Q wrote 4 in round 1 but scored only 1 overall, so Q did not score in round 1; P scored only in round 3. So the round-1 scorers are R and S, and Q's 4 was matched by P: round 1 is P 4, Q 4, S 2, R a with a = 1 or 3. "
           "If R scored again in round 3 (and Q in round 2), the totals of the numbers come out to 32 + 2b for a whole number b, never 33 — impossible. So Q scored 1 in round 3 and R scored alone in round 2 with 5 − a. If a = 3, R's numbers 3, 2 and his round-3 number (which must pair with S, avoiding 4 and 1) clash; so a = 1 and R wrote 4 in round 2. "
           "Round 2: P, Q, S wrote the same d; round 3: P 4, Q 1, R and S both c (c = 2 or 3). Sum: 11 + (3d + 4) + (5 + 2c) = 33 gives 3d + 2c = 13, so c = 2 and d = 3. "
           "Final: round 1 — P 4, Q 4, R 1, S 2; round 2 — P 3, Q 3, R 4, S 3; round 3 — P 4, Q 1, R 2, S 2. A computer check of all 4¹² possibilities confirms it is the only one.")
    T, M = (lambda *a, **k: B.tita(s, *a, set_id="b2-unique", **k)), (lambda *a, **k: B.mcq(s, *a, set_id="b2-unique", **k))
    M("Games with rules", "Hard", "What number did S write in round 2?", ["1", "2", "3", "4"], str(g[1][3]), exp)
    fours = sum(r_.count(4) for r_ in g); assert fours == 4
    T("Games with rules", "Hard", "In how many of the twelve writes was the number 4 written?", fours, exp + " The number 4 was written twice in round 1, once in round 2 and once in round 3: 4 times.")
    sc1 = [x for x, v in zip("PQRS", score(g[0])) if v > 0]; assert sc1 == ["R", "S"]
    M("Games with rules", "Hard", "Which players scored in round 1?", ["R and S only", "P and R only", "R only", "Q, R and S only"], "R and S only", exp)
    T("Games with rules", "Medium", "What was the sum of the four numbers written in round 3?", sum(g[2]), exp + f" Round 3: 4 + 1 + 2 + 2 = {sum(g[2])}.")
    # ---------- Set 4: the doubling game (Games with rules) ----------
    fin = (16, 32, 48, 64)
    def back(order):
        a = [F(x) for x in fin]
        for L in reversed(order):
            for i in range(4):
                if i != L: a[i] /= 2
            a[L] += sum(a[i] for i in range(4) if i != L)
        return a
    def fwd(init, order):
        a = list(init); h = [tuple(a)]
        for L in order:
            pay = sum(a[i] for i in range(4) if i != L)
            if a[L] < pay: return None
            for i in range(4):
                if i != L: a[i] *= 2
            a[L] -= pay; h.append(tuple(a))
        return h
    cands = []
    for o in itertools.permutations(range(4)):
        a = back(o)
        if not all(x.denominator == 1 and x >= 0 for x in a): continue
        a = [int(x) for x in a]; h = fwd(a, o)
        if h is None or h[-1] != fin: continue
        if a[1] > a[0] + a[2] + a[3] and a[2] == min(a) and a.count(min(a)) == 1 and o.index(3) < o.index(0): cands.append((o, a, h))
    assert len(cands) == 1, cands; o, a, h = cands[0]; assert o == (1, 3, 0, 2) and a == [21, 82, 13, 44]
    L = "ABCD"
    B.add_set("b2-doubling", "dilr", "The doubling game (Hard)",
        "<b>The doubling game</b><p>Four players, A, B, C and D, play four rounds of a game with coins. Each round has exactly one loser, and every player loses exactly one round. The loser of a round pays each of the other three players as many coins as that player holds at that moment, so each of the other three doubles their holding. The loser always has enough coins to pay. No other coins change hands.</p>"
        + ul(["After the four rounds, A, B, C and D hold 16, 32, 48 and 64 coins respectively.",
              "At the start, B held more coins than the other three put together.",
              "At the start, C held fewer coins than each of the others.",
              "D lost a round before A did."]))
    exp = ("The total, 160 coins, never changes. Work backwards from the end: in the round a player loses, every other player's holding is halved (undoing the doubling) and the loser gets back what he paid. "
           "Undoing the rounds for each of the 24 possible orders of losers shows that the round-1 loser always starts with 81 to 84 coins and everyone else with at most 44, so 'B held more than the other three together' means B lost round 1. "
           "Of the six orders with B first, only (B, D, A, C) and (B, A, D, C) leave C with the fewest coins at the start, and 'D before A' picks the first. Undoing the rounds for B, D, A, C gives starting holdings A 21, B 82, C 13, D 44. "
           "Forward check: after round 1 (B loses) 42, 4, 26, 88; after round 2 (D loses) 84, 8, 52, 16; after round 3 (A loses) 8, 16, 104, 32; after round 4 (C loses) 16, 32, 48, 64 ✓.")
    assert h == [(21, 82, 13, 44), (42, 4, 26, 88), (84, 8, 52, 16), (8, 16, 104, 32), (16, 32, 48, 64)]
    T, M = (lambda *a, **k: B.tita(s, *a, set_id="b2-doubling", **k)), (lambda *a, **k: B.mcq(s, *a, set_id="b2-doubling", **k))
    T("Games with rules", "Hard", "How many coins did A hold at the start?", a[0], exp)
    M("Games with rules", "Hard", "Who lost round 2?", ["A", "B", "C", "D"], L[o[1]], exp)
    T("Games with rules", "Hard", "How many coins did C hold at the end of round 2?", h[2][2], exp + f" C held {h[2][2]} coins after round 2.")
    mx = max(max(x) for x in h); assert mx == 104
    T("Games with rules", "Hard", "What is the largest number of coins held by any one player at any time (at the start or at the end of any round)?", mx, exp + f" The largest holding is C's {mx} coins after round 3.")

    # ---------- Set 5: sharing fruit (Distribution) ----------
    sols = []
    for xa, xb, xo, ya, yb, yo in itertools.product(range(7), repeat=6):
        za, zb, zo = 7 - xa - ya, 6 - xb - yb, 5 - xo - yo
        if min(za, zb, zo) < 0 or xa + xb + xo != 6 or ya + yb + yo != 6 or za + zb + zo != 6: continue
        if xo != 0 or not (ya > xa > za) or zo != zb: continue
        sols.append(((xa, xb, xo), (ya, yb, yo), (za, zb, zo)))
    assert sols == [((3, 3, 0), (4, 0, 2), (0, 3, 3))]; X_, Y_, Z_ = sols[0]
    B.add_set("b2-fruit", "dilr", "Sharing fruit (Easy)",
        "<b>Sharing fruit</b><p>Seven apples, six bananas and five oranges (18 fruits in all) are shared among three friends, X, Y and Z, so that each friend gets exactly six fruits. It is also known that:</p>"
        + ul(["X got no oranges.", "Y got more apples than X, and X got more apples than Z.", "Z got as many oranges as bananas."]))
    exp = ("Z's six fruits are apples plus equal numbers of oranges and bananas, so Z's apples = 6 − 2 × (Z's bananas), an even number. If Z had 2 or more apples, X would need at least 3 and Y at least 4, which is 9 or more apples, but there are only 7. "
           "So Z has 0 apples, 3 bananas and 3 oranges. X has no oranges, so the remaining 5 − 3 = 2 oranges are Y's. Y's other 4 fruits are apples and bananas, and X's 6 fruits are apples and bananas. "
           "X and Y share all 7 apples with Y having more: the splits (3, 4), (2, 5) and (1, 6) are possible in principle, but Y can hold at most 4 apples, so X has 3 apples and Y has 4. Then X has 6 − 3 = 3 bananas and Y has 0 bananas. "
           "Result: X 3 apples, 3 bananas, 0 oranges; Y 4 apples, 0 bananas, 2 oranges; Z 0 apples, 3 bananas, 3 oranges. A computer check of every possible split confirms this is the only one.")
    T, M = (lambda *a, **k: B.tita(s, *a, set_id="b2-fruit", **k)), (lambda *a, **k: B.mcq(s, *a, set_id="b2-fruit", **k))
    T("Distribution", "Easy", "How many bananas did X get?", X_[1], exp + " X got 3 bananas.")
    M("Distribution", "Easy", "Which friend got no bananas?", ["X", "Y", "Z", "None of them"], "Y", exp + " Only Y got no bananas.", fixed=True)
    M("Distribution", "Easy", "Which friend got the most oranges?", ["X", "Y", "Z", "Y and Z got the same number"], "Z", exp + " Z got 3 oranges, more than Y's 2 and X's 0.", fixed=True)
    allk = sum(all(v > 0 for v in f) for f in (X_, Y_, Z_)); assert allk == 0
    T("Distribution", "Medium", "How many of the three friends got at least one fruit of each of the three kinds?", allk, exp + " X has no oranges, Y has no bananas and Z has no apples, so none of them has all three kinds: the answer is 0.")
