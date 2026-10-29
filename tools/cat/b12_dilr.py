"""Practice pack b12, DILR (original sets, added 29 Oct 2026). Every set is solved here by brute force over all
possibilities; the build stops unless exactly one possibility fits the clues, and every answer is read from it."""
import itertools

def ul(items): return "<ul class='clues'>" + "".join(f"<li>{c}</li>" for c in items) + "</ul>"
def tbl(head, rows): return ("<table class='data'><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>"
                             + "".join("<tr>" + "".join((f"<td class='miss'>?</td>" if c == "?" else f"<td>{c}</td>") for c in r) + "</tr>" for r in rows) + "</table>")

def build(B):
    s = "dilr"
    def fns(sid): return (lambda *a, **k: B.tita(s, *a, set_id=sid, **k)), (lambda *a, **k: B.mcq(s, *a, set_id=sid, **k))

    # ---------- Set 1: knockout bracket (Tournaments) ----------
    P = "ABCDEFGH"
    def play(res):
        sets = {p: 0 for p in P}; three = [0]
        def m(a, b, r):
            first, t = r; w, l = (a, b) if first else (b, a); sets[w] += 2; sets[l] += 1 if t else 0; three[0] += t; return (w, l, t)
        qf = [m(a, b, res[i]) for i, (a, b) in enumerate([("A", "B"), ("C", "D"), ("E", "F"), ("G", "H")])]
        s1 = m(qf[0][0], qf[1][0], res[4]); s2 = m(qf[2][0], qf[3][0], res[5]); f = m(s1[0], s2[0], res[6])
        return dict(sets=sets, three=three[0], qf=qf, sf=[s1, s2], f=f)
    sols = []
    for res in itertools.product(itertools.product([1, 0], [0, 1]), repeat=7):
        g = play(res); st = g["sets"]
        if (st["C"] == 0 and st["D"] == 5 and st["B"] == st["F"] == st["G"] == 1 and st["A"] == 3 and g["three"] == 5 and st["H"] < st["A"]):
            sols.append(g)
    assert len(sols) == 1, len(sols); g = sols[0]; st = g["sets"]
    assert [m[:2] for m in g["qf"]] == [("A", "B"), ("D", "C"), ("E", "F"), ("H", "G")] and g["sf"][0][:2] == ("D", "A") and g["sf"][1][:2] == ("E", "H") and g["f"][:2] == ("E", "D")
    B.add_set("b12-knockout", "dilr", "Knockout badminton (Medium)",
        "<b>Knockout badminton</b><p>Eight players, A to H, played a knockout badminton tournament. In the quarter-finals A played B, C played D, E played F and G played H. "
        "The winner of A–B met the winner of C–D in one semi-final, the winner of E–F met the winner of G–H in the other, and the two semi-final winners met in the final. "
        "Every match was the best of three games: the first player to win two games won the match, so each match ended 2–0 or 2–1. There were no walkovers.</p>"
        + ul(["C did not win a single game in the tournament.", "D won 5 games in all.", "B, F and G won exactly one game each.",
              "A won 3 games in all.", "Exactly five matches went to three games.", "H won fewer games than A."]))
    exp = ("C won no game, so C lost 2–0 to D. B, F and G each won exactly one game, so each lost their quarter-final 2–1 (a winner of a match has at least 2 games): A beat B 2–1, E beat F 2–1 and H beat G 2–1. "
           "D has 2 games from the quarter-final and 5 in all. Had D lost the semi-final, D would have at most 2 + 1 = 3; had D won both the semi-final and the final, D would have at least 2 + 2 + 2 = 6. So D won the semi-final and lost the final 2–1, giving 2 + 2 + 1 = 5. "
           "D's semi-final opponent was A, who has 2 games from beating B and 3 in all, so A lost that semi-final 2–1. "
           "H has 2 games from the quarter-final and fewer than A's 3, so H won no game in the other semi-final: E beat H 2–0, and E then beat D 2–1 in the final. "
           "Check: the three-game matches are A–B, E–F, G–H, D–A and the final — exactly five ✓. Games won: A 3, B 1, C 0, D 5, E 6, F 1, G 1, H 2. A computer check of all 4⁷ possible results finds only this one.")
    T, M = fns("b12-knockout")
    M("Tournaments", "Medium", "Who won the tournament?", ["D", "E", "H", "A"], g["f"][0], exp + " The champion is E.")
    T("Tournaments", "Medium", "How many games did E win in the tournament?", st["E"], exp + f" E won 2 + 2 + 2 = {st['E']} games.")
    tot = sum(st.values()); assert tot == 19
    T("Tournaments", "Medium", "How many games were played in the whole tournament?", tot, exp + f" Every game has exactly one winner, so the games played equal the games won: 3 + 1 + 0 + 5 + 6 + 1 + 1 + 2 = {tot}.")
    hb = [m[1] for m in g["qf"] + g["sf"] + [g["f"]] if m[0] == "H"]; assert hb == ["G"]
    M("Tournaments", "Medium", "Which player(s) did H defeat in the tournament?", ["G only", "G and E", "F only", "H did not win a match"], "G only", exp + " H beat G in the quarter-final and then lost 2–0 to E.")

    # ---------- Set 2: water network (Networks & routes) ----------
    sols = [(x, p, q) for x in range(0, 1201) for p in range(0, 101) for q in range(0, 101)
            if (1200 - x) * (100 - q) == 200 * 100 and q == 60 and (x * (100 - p) + (1200 - x) * q) == 720 * 100]
    assert sols == [(700, 40, 60)], sols; x, p, q = sols[0]
    AC, AD, BD, BE = x * p // 100, x * (100 - p) // 100, (1200 - x) * q // 100, (1200 - x) * (100 - q) // 100
    assert (AC, AD, BD, BE) == (280, 420, 300, 200)
    B.add_set("b12-pipes", "dilr", "Water pipeline network (Easy)",
        "<b>Water pipeline network</b><p>Water enters a network at junction S at 1,200 litres per minute and flows only along the pipes listed below, in the direction shown. "
        "At a junction, all the water that comes in leaves through its outgoing pipes; nothing is stored or lost. The water ends up in three tanks, C, D and E.</p>"
        + tbl(["Pipe", "From", "To"], [["1", "S", "A"], ["2", "S", "B"], ["3", "A", "Tank C"], ["4", "A", "Tank D"], ["5", "B", "Tank D"], ["6", "B", "Tank E"]])
        + ul(["Tank E receives 200 litres per minute.", "Junction B sends 60% of the water it receives to tank D.", "Tank D receives 720 litres per minute."]))
    exp = ("Junction B sends 60% to D, so the other 40% goes to E: 40% of B's inflow = 200, so B receives 500 litres/min and sends 300 to D. "
           "Then S sends 1,200 − 500 = 700 to A. Tank D gets 720, of which 300 comes from B, so pipe A→D carries 420 and pipe A→C carries 700 − 420 = 280. "
           "Flows (litres/min): S→A 700, S→B 500, A→C 280, A→D 420, B→D 300, B→E 200.")
    T, M = fns("b12-pipes")
    T("Networks & routes", "Easy", "What percentage of the water reaching junction A goes to tank C?", p, exp + f" 280/700 = {p}%.")
    M("Networks & routes", "Easy", "How many litres per minute does tank C receive?", ["240", "280", "300", "420"], str(AC), exp)
    M("Networks & routes", "Easy", "What fraction of the water entering at S ends up in tank D?", ["1/2", "3/5", "7/12", "2/3"], "3/5", exp + " 720/1,200 = 3/5.", chk=(720 / 1200, 3 / 5))
    nd = AD + (1200 - x); assert nd == 920
    T("Networks & routes", "Easy", "If junction B were changed to send all its water to tank D, with everything else unchanged, how many litres per minute would tank D receive?", nd, exp + f" D would get 420 from A plus all 500 from B = {nd}.")

    # ---------- Set 3: three clubs (Distribution) ----------
    sols = []
    for g_ in range(61):
        for d in range(61):
            for e in range(61):
                for f in range(61):
                    a, b, c = 22 - d - e - g_, 22 - d - f - g_, 25 - e - f - g_
                    if min(a, b, c) < 0: continue
                    h = 60 - (a + b + c + d + e + f + g_)
                    if h >= 0 and d + e + f == 15 and h == 12 and c == a + 2 and e == 4: sols.append((a, b, c, d, e, f, g_, h))
    assert sols == [(10, 8, 12, 5, 4, 6, 3, 12)], sols; a, b, c, d, e, f, g_, h = sols[0]
    B.add_set("b12-clubs", "dilr", "Three clubs (Medium)",
        "<b>Three clubs</b><p>A class of 60 students has three clubs: Music, Drama and Sports. A student may join any number of the clubs, including none.</p>"
        + ul(["Music has 22 members, Drama has 22 and Sports has 25.", "Exactly 15 students belong to exactly two clubs.", "12 students belong to no club.",
              "The number of students who are only in Sports is 2 more than the number who are only in Music.",
              "Exactly 4 students are in Music and Sports but not in Drama."]))
    exp = ("48 students are in at least one club. Adding the three club sizes counts students in one club once, in two clubs twice and in all three thrice: 22 + 22 + 25 = 69 = (only one) + 2 × 15 + 3 × (all three). "
           "Also (only one) + 15 + (all three) = 48. Subtracting, 69 − 48 = 15 + 2 × (all three), so 3 students are in all three clubs and 30 are in exactly one. "
           "Let Music-and-Drama-only = d and Drama-and-Sports-only = f, with Music-and-Sports-only = 4, so d + f = 11. Only Music = 22 − d − 4 − 3 = 15 − d and only Sports = 25 − 4 − f − 3 = 18 − f. "
           "The clue 'only Sports = only Music + 2' gives 18 − f = 17 − d, so f = d + 1; with d + f = 11, d = 5 and f = 6. "
           "So: only Music 10, only Drama 8, only Sports 12, Music & Drama only 5, Music & Sports only 4, Drama & Sports only 6, all three 3, none 12.")
    T, M = fns("b12-clubs")
    T("Distribution", "Medium", "How many students belong to all three clubs?", g_, exp)
    T("Distribution", "Medium", "How many students belong to exactly one club?", a + b + c, exp + f" 10 + 8 + 12 = {a + b + c}.")
    M("Distribution", "Medium", "How many students are in Drama and Sports but not in Music?", ["4", "5", "6", "9"], str(f), exp)
    md = a + b + d + e + f + g_; assert md == 36
    M("Distribution", "Medium", "How many students belong to Music or Drama (or both)?", ["30", "36", "39", "44"], str(md), exp + f" Everyone except the 12 in no club and the 12 only in Sports: 60 − 24 = {md}.")

    # ---------- Set 4: interview schedule (Scheduling) ----------
    C_ = "PQRSTU"; SL = ["Monday morning", "Monday afternoon", "Tuesday morning", "Tuesday afternoon", "Wednesday morning", "Wednesday afternoon"]
    sols = []
    for perm in itertools.permutations(range(6)):
        sl = dict(zip(C_, perm)); day = lambda z: sl[z] // 2; am = lambda z: sl[z] % 2 == 0
        for iv in set(itertools.permutations("XXYYZZ")):
            I = lambda z: iv[sl[z]]
            if (all(iv[2 * k] != iv[2 * k + 1] for k in range(3)) and iv[0] == "X" and (not am("R")) and I("R") == "Y"
                    and day("S") == day("T") and I("T") == "Z" and day("P") < day("Q") and I("P") == I("Q") and sl["U"] == 4
                    and "Z" not in iv[0:2] and am("S")):
                sols.append((sl, iv))
    assert len(sols) == 1, len(sols); sl, iv = sols[0]
    order = sorted(sl, key=sl.get); assert order == list("PRSTUQ") and iv == ("X", "Y", "Y", "Z", "Z", "X")
    B.add_set("b12-interviews", "dilr", "Interview schedule (Medium)",
        "<b>Interview schedule</b><p>Six candidates, P, Q, R, S, T and U, are interviewed one at a time over three days, Monday to Wednesday, with one interview each morning and one each afternoon. "
        "Three interviewers, X, Y and Z, each conduct exactly two of the six interviews, and no interviewer conducts two interviews on the same day.</p>"
        + ul(["X conducts the Monday-morning interview.", "R is interviewed in an afternoon, by Y.", "S and T are interviewed on the same day; T is interviewed by Z, and S in the morning.",
              "P is interviewed on an earlier day than Q, and both are interviewed by the same interviewer.", "U is interviewed on Wednesday morning.", "Z does not conduct any interview on Monday."]))
    exp = ("Z has two interviews on different days and none on Monday, so Z does one on Tuesday and one on Wednesday. "
           "S and T share a day with S in the morning; Wednesday morning is U's, so S and T are on Monday or Tuesday. T is Z's, and Z does not work Monday, so S and T are on Tuesday: S on Tuesday morning and T (with Z) on Tuesday afternoon. "
           "R is in an afternoon with Y; Tuesday afternoon is T's, so R is on Monday afternoon or Wednesday afternoon. P and Q take the other two slots on different days with P earlier. "
           "If R were on Wednesday afternoon, P and Q would be Monday morning and Monday afternoon — the same day — impossible. So R is on Monday afternoon (Y), P on Monday morning (X, by the first clue) and Q on Wednesday afternoon, also with X. "
           "Then Monday has X and Y, Wednesday has Z (with U, morning) and X (Q, afternoon), and Tuesday has Y (S, morning) and Z (T, afternoon). Final: Mon — P (X), R (Y); Tue — S (Y), T (Z); Wed — U (Z), Q (X).")
    T, M = fns("b12-interviews")
    M("Scheduling", "Medium", "Who is interviewed on Monday afternoon?", ["P", "R", "S", "Q"], order[1], exp)
    M("Scheduling", "Medium", "Who interviews U?", ["X", "Y", "Z", "Cannot be determined"], I_u := iv[sl["U"]], exp + " U's Wednesday-morning interview is taken by Z.", fixed=True)
    assert I_u == "Z"
    M("Scheduling", "Medium", "Who interviews S?", ["X", "Y", "Z", "Cannot be determined"], iv[sl["S"]], exp, fixed=True)
    xm = sum(1 for k in range(6) if iv[k] == "X" and k % 2 == 0); assert xm == 1
    T("Scheduling", "Medium", "How many of X's interviews are in the morning?", xm, exp + " X does Monday morning (P) and Wednesday afternoon (Q), so 1.")

    # ---------- Set 5: counting-out game (Games with rules) ----------
    N = ["Anu", "Bala", "Chetan", "Dev", "Esha", "Farah", "Gopal"]
    def run(m):
        c = list(range(7)); i = 0; out = []
        while c: i = (i + m - 1) % len(c); out.append(N[c.pop(i)])
        return out
    ok = [m for m in range(2, 10) if (lambda o: o.index("Gopal") >= 3 and o.index("Anu") < o.index("Dev") and o[0] != "Anu")(run(m))]
    assert ok == [3], ok; o = run(3); assert o == ["Chetan", "Farah", "Bala", "Gopal", "Esha", "Anu", "Dev"]
    B.add_set("b12-countout", "dilr", "Counting-out game (Medium)",
        "<b>Counting-out game</b><p>Seven children — Anu, Bala, Chetan, Dev, Esha, Farah and Gopal — stand in a circle in that order, clockwise (Gopal is next to Anu). "
        "They choose a whole number <i>m</i> from 2 to 9. Starting with Anu as 1, they count clockwise round the circle, and the child who is counted <i>m</i> leaves. "
        "Counting starts again at 1 from the next child still in the circle, and so on, until one child is left.</p>"
        + ul(["Anu was not the first child to leave.", "Gopal was not among the first three children to leave.", "Dev was still in the circle when Anu left."]))
    tab = "; ".join(f"m = {m}: " + ", ".join(run(m)) for m in range(2, 10))
    exp = ("Play the game for each m (leaving order, last name = the child left in the circle): " + tab + ". "
           "Anu leaves first only for m = 8. Gopal is among the first three for m = 6 (third) and m = 7 (first). Dev has already left when Anu leaves for m = 2, 4, 5 and 9. Only m = 3 satisfies all three clues. "
           "With m = 3 the children leave in the order Chetan, Farah, Bala, Gopal, Esha, Anu, and Dev is left.")
    T, M = fns("b12-countout")
    T("Games with rules", "Medium", "What is the value of m?", 3, exp)
    M("Games with rules", "Medium", "Which child is left at the end?", ["Gopal", "Dev", "Anu", "Esha"], o[-1], exp)
    M("Games with rules", "Medium", "Who was the fourth child to leave?", ["Bala", "Esha", "Gopal", "Farah"], o[3], exp)
    o4 = run(4); assert o4[-1] == "Bala"
    M("Games with rules", "Hard", "If the children had used a number one larger than m, with everything else the same, who would have been left at the end?", ["Bala", "Chetan", "Dev", "Gopal"], o4[-1], exp + " With 4 the order is " + ", ".join(o4) + ", so Bala is left.")

    # ---------- Set 6: the thief and the joker (Logic puzzles) ----------
    Ps = "ABCDE"
    st6 = {"A": lambda t, j: (t != "A", j != "C"), "B": lambda t, j: (t == "C", j != "B"), "C": lambda t, j: (t in "DE", j != "A"),
           "D": lambda t, j: (t != "D", j == "E"), "E": lambda t, j: (t != "B", j != "D")}
    sols = [(t, j) for t, j in itertools.permutations(Ps, 2)
            if all((not any(st6[p](t, j))) if p in (t, j) else all(st6[p](t, j)) for p in Ps)]
    assert sols == [("D", "B")], sols; t, j = sols[0]
    B.add_set("b12-thief", "dilr", "The thief and the joker (Medium)",
        "<b>The thief and the joker</b><p>Five people, A, B, C, D and E, are questioned about a theft. Exactly one of them is the thief and exactly one other is a joker. "
        "The thief and the joker both make two false statements; each of the other three makes two true statements.</p>"
        + ul(["A: “I am not the thief.” “C is not the joker.”", "B: “C is the thief.” “I am not the joker.”", "C: “The thief is D or E.” “A is not the joker.”",
              "D: “I am not the thief.” “E is the joker.”", "E: “B is not the thief.” “D is not the joker.”"]))
    exp = ("Exactly two people (the thief and the joker) lie. Suppose D tells the truth: then E is the joker, so E's statements are false and B is the thief. "
           "But then C, who is neither, must be truthful, and C says the thief is D or E — a contradiction. So D lies. If D were the joker, D's 'I am not the thief' would be false, making D the thief as well — impossible. "
           "So D is the thief. Then B's 'C is the thief' is false, so B is the other liar, the joker; B's 'I am not the joker' is indeed false ✓. "
           "Check the truth-tellers A, C, E: A is not the thief ✓, C is not the joker ✓; the thief is D ✓, A is not the joker ✓; B is not the thief ✓, D is not the joker ✓. "
           "D's 'E is the joker' is false ✓. Checking all 20 thief–joker pairs confirms D is the thief and B the joker, and nothing else works.")
    T, M = fns("b12-thief")
    M("Logic puzzles", "Medium", "Who is the thief?", ["B", "C", "D", "E"], t, exp)
    M("Logic puzzles", "Medium", "Who is the joker?", ["A", "B", "C", "E"], j, exp)
    ntrue = sum(sum(st6[p](t, j)) for p in Ps); assert ntrue == 6
    T("Logic puzzles", "Medium", "How many of the ten statements are true?", ntrue, exp + " The three truth-tellers make 2 true statements each: 6.")
    cand = {"A: “C is not the joker.”": st6["A"](t, j)[1], "C: “A is not the joker.”": st6["C"](t, j)[1], "E: “D is not the joker.”": st6["E"](t, j)[1], "D: “E is the joker.”": st6["D"](t, j)[1]}
    assert [k for k, v in cand.items() if not v] == ["D: “E is the joker.”"]
    M("Logic puzzles", "Medium", "Which one of the following statements is false?", list(cand), "D: “E is the joker.”", exp)

    # ---------- Set 7: quarterly sales with missing data (Tables with missing data) ----------
    sols = []
    for K2, L3, M1, M4, N2 in itertools.product(range(41), repeat=5):
        if 12 + 10 + M1 + 14 != 44: continue
        Tb = [[12, K2, 18, K2], [10, 14, L3, 13], [M1, 9, 16, M4], [14, N2, 12, 20]]
        q_ = [sum(r[i] for r in Tb) for i in range(4)]
        if q_[1] == 48 and q_[2] == 57 and sum(Tb[1]) == sum(Tb[2]) and sum(map(sum, Tb)) == 212: sols.append(Tb)
    assert sols == [[[12, 15, 18, 15], [10, 14, 11, 13], [8, 9, 16, 15], [14, 10, 12, 20]]], sols; Tb = sols[0]
    B.add_set("b12-quarters", "dilr", "Quarterly sales (Medium)",
        "<b>Quarterly sales</b><p>The table shows a company's sales (in hundreds of units) of four products, K, L, M and N, in the four quarters of a year. Some entries are missing.</p>"
        + tbl(["Product", "Q1", "Q2", "Q3", "Q4"], [["K", "12", "?", "18", "?"], ["L", "10", "14", "?", "13"], ["M", "?", "9", "16", "?"], ["N", "14", "?", "12", "20"]])
        + ul(["Total sales of the four products were 44 in Q1, 48 in Q2 and 57 in Q3.", "K's sales in Q2 and Q4 were equal.",
              "L and M had equal total sales for the year.", "Total sales for the year (all products, all quarters) were 212."]))
    exp = ("Q1: 12 + 10 + M1 + 14 = 44, so M's Q1 = 8. Q3: 18 + L3 + 16 + 12 = 57, so L's Q3 = 11, and L's year = 10 + 14 + 11 + 13 = 48. "
           "M's year is also 48 = 8 + 9 + 16 + M4, so M's Q4 = 15. Q4 total = 212 − 44 − 48 − 57 = 63 = K4 + 13 + 15 + 20, so K's Q4 = 15 and therefore K's Q2 = 15. "
           "Q2: 15 + 14 + 9 + N2 = 48, so N's Q2 = 10. Full table — K: 12, 15, 18, 15 (60); L: 10, 14, 11, 13 (48); M: 8, 9, 16, 15 (48); N: 14, 10, 12, 20 (56).")
    T, M = fns("b12-quarters")
    T("Tables with missing data", "Medium", "What were N's sales in Q2 (in hundreds of units)?", Tb[3][1], exp)
    tots = {k: sum(r) for k, r in zip("KLMN", Tb)}; best = max(tots, key=tots.get); assert best == "K" and list(tots.values()).count(60) == 1
    M("Tables with missing data", "Medium", "Which product had the highest total sales for the year?", ["K", "L", "M", "N"], best, exp, fixed=True)
    mq = max(range(4), key=lambda i: Tb[2][i]); assert mq == 2 and Tb[2].count(16) == 1
    M("Tables with missing data", "Medium", "In which quarter were M's sales the highest?", ["Q1", "Q2", "Q3", "Q4"], "Q3", exp + " M: 8, 9, 16, 15.", fixed=True)
    q4 = sum(r[3] for r in Tb); assert q4 == 63 and abs(q4 / 212 * 100 - 29.7) < 0.05
    M("Tables with missing data", "Medium", "Approximately what percentage of the year's total sales came in Q4?", ["About 25%", "About 27%", "About 30%", "About 33%"], "About 30%", exp + " Q4 = 63, and 63/212 ≈ 29.7%, about 30%.", fixed=True)

    # ---------- Set 8: preferential voting (Rankings & scoring) ----------
    def irv(ballots):
        alive = set("PQRS"); log = []
        while True:
            cnt = {c_: 0 for c_ in sorted(alive)}
            for od, n in ballots: cnt[next(c_ for c_ in od if c_ in alive)] += n
            log.append(dict(cnt)); tot_ = sum(cnt.values())
            w = [c_ for c_ in cnt if cnt[c_] * 2 > tot_]
            if w: return w[0], log
            lo = min(cnt.values()); L_ = [c_ for c_ in cnt if cnt[c_] == lo]; assert len(L_) == 1; alive.remove(L_[0])
    base = lambda x: [("PQRS", 30), ("QRPS", 25), ("RQPS", 20), ("SRQP", 18), ("SPQR", x), ("QPRS", 27 - x)]
    ok = [x for x in range(28) if sum(n for od, n in base(x) if od[0] == "S") == sum(n for od, n in base(x) if od[0] == "Q") + 2]
    assert ok == [18], ok
    win, log = irv(base(18)); assert win == "Q" and log == [{"P": 30, "Q": 34, "R": 20, "S": 36}, {"P": 30, "Q": 54, "S": 36}, {"Q": 84, "S": 36}]
    alt = [("PQRS", 30), ("QRPS", 25), ("RSQP", 20), ("SRQP", 18), ("SPQR", 18), ("QPRS", 9)]
    win2, log2 = irv(alt); assert win2 == "Q" and log2[-1] == {"Q": 64, "S": 56}
    B.add_set("b12-vote", "dilr", "Preferential vote (Hard)",
        "<b>Preferential vote</b><p>120 members elect a president from four candidates, P, Q, R and S. Each member ranks all four candidates. The table shows how many members chose each ranking (first preference on the left); two counts, x and y, are missing.</p>"
        + tbl(["Ranking", "Members"], [["P &gt; Q &gt; R &gt; S", "30"], ["Q &gt; R &gt; P &gt; S", "25"], ["R &gt; Q &gt; P &gt; S", "20"], ["S &gt; R &gt; Q &gt; P", "18"], ["S &gt; P &gt; Q &gt; R", "x"], ["Q &gt; P &gt; R &gt; S", "y"]])
        + "<p>Counting: each ballot counts for the highest-ranked candidate still in the race. If a candidate has more than half the ballots, that candidate wins. Otherwise the candidate with the fewest ballots is eliminated and the ballots are counted again.</p>"
        + ul(["In the first count, S had exactly 2 more ballots than Q."]))
    exp = ("x + y = 120 − 93 = 27. First count: P 30, Q 25 + y, R 20, S 18 + x. Q has 25 + y = 52 − x, so S = Q + 2 gives 18 + x = 54 − x, x = 18 and y = 9. "
           "Count 1: P 30, Q 34, R 20, S 36 — no majority (61 needed); R is eliminated and R's 20 ballots (R > Q > P > S) go to Q. "
           "Count 2: P 30, Q 54, S 36 — no majority; P is eliminated and P's 30 ballots (P > Q > R > S) go to Q. Count 3: Q 84, S 36, so Q wins.")
    T, M = fns("b12-vote")
    T("Rankings & scoring", "Medium", "What is the value of x?", 18, exp)
    M("Rankings & scoring", "Medium", "Which candidate was eliminated first?", ["P", "Q", "R", "S"], "R", exp, fixed=True)
    T("Rankings & scoring", "Hard", "How many ballots did the winner have in the final count?", log[-1]["Q"], exp)
    T("Rankings & scoring", "Hard", "Suppose the 20 members who ranked R > Q > P > S had instead ranked R > S > Q > P, and every other ballot stayed the same. How many ballots would S have in the final count?", log2[-1]["S"],
      exp + " With the change, count 1 is the same and R is eliminated, but R's 20 ballots now go to S: P 30, Q 34, S 56. P is eliminated and P's ballots go to Q: Q 64, S 56. Q still wins, and S has 56.")

    # ---------- Set 9: two facing rows (Arrangements) ----------
    Nm = ["Amit", "Bhavna", "Charu", "Deepak", "Ela", "Firoz"]
    SEATS = [(r, c_) for r in (1, 2) for c_ in (1, 2, 3)]
    rt = lambda p_: (p_[0], p_[1] - 1) if p_[0] == 1 else (p_[0], p_[1] + 1)   # row 1 faces south, row 2 faces north
    lt = lambda p_: (p_[0], p_[1] + 1) if p_[0] == 1 else (p_[0], p_[1] - 1)
    opp = lambda p_: (3 - p_[0], p_[1])
    sols = []
    for perm in itertools.permutations(SEATS):
        z = dict(zip(Nm, perm)); A_ = z["Amit"]
        if (A_[1] != 2 and z["Ela"] == opp(A_) and z["Bhavna"] != opp(z["Firoz"]) and z["Charu"][1] == 2 and z["Deepak"][0] != A_[0]
                and rt(A_) == z["Firoz"] and A_[0] == 1): sols.append(z)
    assert len(sols) == 1; z = sols[0]; at = {v: k for k, v in z.items()}
    assert z == {"Amit": (1, 3), "Bhavna": (1, 1), "Charu": (2, 2), "Deepak": (2, 1), "Ela": (2, 3), "Firoz": (1, 2)}
    B.add_set("b12-rows", "dilr", "Two facing rows (Easy)",
        "<b>Two facing rows</b><p>Six friends — Amit, Bhavna, Charu, Deepak, Ela and Firoz — sit in two rows of three seats. The north row faces south and the south row faces north, so each person directly faces one person in the other row.</p>"
        + ul(["Amit sits in the north row, in an end seat, and faces Ela.", "Firoz sits immediately to Amit's right.", "Charu sits in the middle seat of a row.",
              "Deepak does not sit in the same row as Amit.", "Bhavna does not face Firoz."]))
    exp = ("Firoz is immediately to Amit's right, in the same row, and Amit is at an end, so Firoz is in the north row's middle seat. Charu must then take the middle seat of the south row, facing Firoz. "
           "Deepak is in the south row, so the north row's remaining end seat goes to Bhavna. Ela faces Amit, so Deepak takes the other south end seat, facing Bhavna. "
           "Directions: the north row faces south, so a north-row person's right is towards the west. With Firoz on Amit's right, Amit is at the east end: north row (west to east) Bhavna, Firoz, Amit; south row (west to east) Deepak, Charu, Ela.")
    T, M = fns("b12-rows")
    M("Arrangements", "Easy", "Who faces Firoz?", ["Deepak", "Charu", "Ela", "Bhavna"], at[opp(z["Firoz"])], exp)
    M("Arrangements", "Easy", "Who faces Bhavna?", ["Deepak", "Charu", "Ela", "Amit"], at[opp(z["Bhavna"])], exp)
    assert at[lt(z["Charu"])] == "Deepak"
    M("Arrangements", "Easy", "Who sits immediately to Charu's left?", ["Deepak", "Ela", "Firoz", "No one"], "Deepak", exp + " Charu faces north, so Charu's left is towards the west, where Deepak sits.")
    ops = {"Ela sits immediately to Charu's right": at.get(rt(z["Charu"])) == "Ela", "Bhavna sits immediately to Firoz's left": at.get(lt(z["Firoz"])) == "Bhavna",
           "Deepak faces Amit": at[opp(z["Amit"])] == "Deepak", "Firoz sits at an end of a row": z["Firoz"][1] != 2}
    assert [k for k, v in ops.items() if v] == ["Ela sits immediately to Charu's right"], ops
    M("Arrangements", "Easy", "Which one of the following is true?", list(ops), "Ela sits immediately to Charu's right",
      exp + " Charu faces north, so her right is east, where Ela sits. Firoz faces south, so his left is east, where Amit (not Bhavna) sits; Ela, not Deepak, faces Amit; and Firoz is in a middle seat.")
