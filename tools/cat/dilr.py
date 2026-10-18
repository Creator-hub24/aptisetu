"""CAT DILR sets: original puzzles. Each set is solved by brute force here and must have exactly one solution;
answers are read off that solution."""
import itertools

def ul(items): return "<ul class='clues'>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def build(B):
    s = "dilr"
    M = lambda *a, **k: B.mcq(s, *a, **k)
    T = lambda *a, **k: B.tita(s, *a, **k)

    # ===== Set 1: seminar scheduling =====
    P = "ABCDEF"; sols = []
    for order in itertools.permutations(P):
        d = {p: i for i, p in enumerate(order)}
        if d["B"] != 3 or d["E"] != d["C"] + 1 or d["A"] not in (0, 5) or not d["F"] > d["D"] or abs(d["D"] - d["B"]) == 1: continue
        for subj in set(itertools.permutations("EEHHPP")):
            sb = {p: subj[d[p]] for p in P}
            if sb["B"] != "H" or sb["A"] != "P" or sb["C"] == "H" or sb["E"] != "E" or sb["F"] != "P": continue
            if not any(subj[i] == subj[i+1] == "E" for i in range(5)) or any(subj[i] == subj[i+1] == "P" for i in range(5)): continue
            sols.append((order, subj))
    assert len(sols) == 1, sols
    order, subj = sols[0]; day = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    d = {p: i for i, p in enumerate(order)}; full = {"E": "Economics", "H": "History", "P": "Physics"}
    B.add_set("cd-seminar", "dilr", "Seminar week", "<b>Seminar week</b><p>Six professors, A to F, each give one talk at a seminar running Monday to Saturday, one talk per day. Two talks are on Economics, two on History and two on Physics.</p>" + ul([
        "B speaks on Thursday, on History.", "C speaks on the day immediately before E.", "A speaks on either Monday or Saturday, on Physics.",
        "F speaks on some day after D, and D does not speak on a day adjacent to B's.", "The two Economics talks are on consecutive days, but no two Physics talks are.",
        "C's talk is not on History. E speaks on Economics and F on Physics."]))
    sid = "cd-seminar"; t = "Scheduling"
    expl = ("B is on Thursday, so the C–E pair is Mon–Tue, Tue–Wed or Fri–Sat, and D can't be on Wed or Fri. "
            "If A is on Saturday: C–E on Mon–Tue leaves Wed and Fri for D and F (D can't take either). C–E on Tue–Wed gives D Mon, F Fri, but then A (Sat) and F (Fri) are consecutive Physics talks. "
            "So A is on Monday. C–E on Tue–Wed leaves Fri and Sat, with D forced to Sat and F after D, which is impossible. So C–E = Fri–Sat, D = Tue, F = Wed. "
            "Subjects: A, F Physics (Mon, Wed are not consecutive ✓). E (Sat) is Economics and the other Economics must be adjacent, so C (Fri). D (Tue) is History, as is B. "
            f"Final: " + ", ".join(f"{day[i][:3]} {order[i]} ({full[subj[i]]})" for i in range(6)) + ". ")
    M(t,"Medium","Who speaks on Wednesday?",["C","D","E","F"],order[2], expl, set_id=sid)
    M(t,"Medium","What is the subject of D's talk?",["Economics","History","Physics","Cannot be determined"],full[subj[d["D"]]], expl + "D speaks on Tuesday. The Physics talks are Mon and Wed and the Economics pair is Fri–Sat, so Tuesday is History.", set_id=sid, fixed=True)
    T(t,"Medium","How many talks take place strictly between A's talk and C's talk?", abs(d["C"]-d["A"])-1, expl + "A is on Monday and C on Friday, with Tue, Wed and Thu in between: 3 talks.", set_id=sid)
    M(t,"Hard","On which day is the second Physics talk of the week?",["Tuesday","Wednesday","Friday","Saturday"],day[[i for i in range(6) if subj[i]=="P"][1]], expl + "The Physics talks are A (Mon) and F (Wed).", set_id=sid)
    pairs = [("D","B"),("A","C"),("F","E"),("D","F")]
    M(t,"Medium","Which pair of professors speak on the same subject?",[f"{x} and {y}" for x,y in pairs],[f"{x} and {y}" for x,y in pairs if subj[d[x]]==subj[d[y]]][0], expl + "D and B both speak on History. A/C = Physics/Economics, F/E = Physics/Economics, D/F = History/Physics.", set_id=sid)
    assert sum(1 for x,y in pairs if subj[d[x]]==subj[d[y]]) == 1

    # ===== Set 2: football round robin =====
    TM = "ABCDE"; pr = list(itertools.combinations(TM, 2)); sols = []
    for res in itertools.product("WDL", repeat=10):
        pts = {x: 0 for x in TM}; r = {}
        for (x, y), o in zip(pr, res):
            r[(x, y)] = o; r[(y, x)] = {"W": "L", "L": "W", "D": "D"}[o]
            if o == "W": pts[x] += 3
            elif o == "L": pts[y] += 3
            else: pts[x] += 1; pts[y] += 1
        if [pts[x] for x in TM] != [10, 7, 6, 4, 1]: continue
        if any(r[("A", y)] == "L" for y in TM if y != "A"): continue
        if r[("B", "C")] != "W": continue
        if r[("E", "A")] != "D": continue    # E's only point came against A (E has 1 point, so the rest are losses)
        sols.append(r)
    assert len(sols) == 1, len(sols); r = sols[0]
    B.add_set("cd-league", "dilr", "Five-team league", "<b>Five-team league</b><p>Five teams A, B, C, D and E played a league in which every team played every other team exactly once. A win earned 3 points, a draw 1 point and a loss 0.</p><table class='data'><tr><th>Team</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th></tr><tr><td>Final points</td><td>10</td><td>7</td><td>6</td><td>4</td><td>1</td></tr></table>" + ul(["A did not lose any match.", "B beat C.", "E's only point came from its match against A."]))
    sid = "cd-league"; t = "Tournaments"
    draws = sum(1 for (x, y) in pr if r[(x, y)] == "D")
    grid = "A: W v B, W v C, W v D, D v E. B: W v C, D v D, W v E. C: W v D, W v E. D: W v E."
    base = "Each team plays 4 matches. A has 10 points and is unbeaten, so 3 wins + 1 draw, and the draw must be against E (E's only point). E lost the rest. B has 7 = 2W + 1D: B beat C and E (and lost to A), so B drew with D. C has 6: lost to A and B, so C beat D and E. D has 4: draw with B, win over E. "
    T(t,"Medium","How many matches in the league ended in a draw?", draws, base + f"The draws were A–E and B–D, so {draws}.", set_id=sid)
    M(t,"Medium","What was the result of the match between B and D?",["B won","D won","Draw","Cannot be determined"],"Draw", base, set_id=sid, fixed=True)
    M(t,"Medium","How many matches did C win?",["1","2","3","0"],str(sum(1 for y in TM if y!="C" and r[("C",y)]=="W")), base + "C beat D and E.", set_id=sid)
    M(t,"Hard","Which team(s) did D beat?",["Only C","Only E","C and E","None"],"Only E", base, set_id=sid, fixed=True)
    assert [y for y in TM if y!="D" and r[("D",y)]=="W"] == ["E"]
    b2 = sum(2 if r[("B",y)]=="W" else 1 if r[("B",y)]=="D" else 0 for y in TM if y!="B")
    T(t,"Hard","If a win had been worth 2 points instead of 3 (draws still 1), how many points would B have finished with?", b2, base + "B: 2 wins and 1 draw ⇒ 2 × 2 + 1 = 5.", set_id=sid)

    # ===== Set 3: table with missing data =====
    F1 = 40; S2 = 20; H1 = 20; H3 = 30; C2 = 30; rowF = 150; rowS = 100; rowC = 130; jan = 150; feb = 140; grand = 470
    vals = range(10, 100, 10); sols = []
    for F2 in vals:
        F3 = rowF - F1 - F2
        for S1 in vals:
            S3 = rowS - S1 - S2
            for C1 in vals:
                C3 = rowC - C1 - C2
                for H2 in vals:
                    cells = [F2, F3, S1, S3, H2, C1, C3]
                    if not all(10 <= v <= 90 and v % 10 == 0 for v in cells): continue
                    if F1 + S1 + H1 + C1 != jan or F2 + S2 + H2 + C2 != feb: continue
                    if rowF + rowS + (H1 + H2 + H3) + rowC != grand: continue
                    if C1 != 2 * S1: continue
                    sols.append(dict(F=[F1,F2,F3], S=[S1,S2,S3], H=[H1,H2,H3], C=[C1,C2,C3]))
    assert len(sols) == 1, sols; tb = sols[0]
    def cell(v, show): return f"<td>{v}</td>" if show else "<td class='miss'>?</td>"
    shown = dict(F=[1,0,0], S=[0,1,0], H=[1,0,1], C=[0,1,0]); names = dict(F="Fiction", S="Science", H="History", C="Comics")
    rows = "".join(f"<tr><td>{names[k]}</td>" + "".join(cell(tb[k][i], shown[k][i]) for i in range(3)) + f"<td>{sum(tb[k]) if k!='H' else '?'}</td></tr>" for k in "FSHC")
    B.add_set("cd-books", "dilr", "Bookshop sales", "<b>Bookshop sales (units)</b><p>A bookshop's sales of four genres over three months are shown. Some entries are missing.</p><table class='data'><tr><th>Genre</th><th>Jan</th><th>Feb</th><th>Mar</th><th>Total</th></tr>" + rows + f"<tr><th>Total</th><th>{jan}</th><th>{feb}</th><th class='miss'>?</th><th>{grand}</th></tr></table>" + ul(["Every entry in the table is a multiple of 10 between 10 and 90.", "In January, Comics sold exactly twice as many units as Science."]))
    sid = "cd-books"; t = "Tables with missing data"
    mar = sum(tb[k][2] for k in "FSHC")
    base = "History total = 470 − 150 − 100 − 130 = 90 ⇒ History Feb = 40. Feb column: Fiction Feb = 140 − 20 − 40 − 30 = 50 ⇒ Fiction Mar = 60. January: Science + Comics = 150 − 40 − 20 = 90 with Comics = 2 × Science ⇒ Science Jan = 30, Comics Jan = 60. Then Science Mar = 50 and Comics Mar = 40. "
    T(t,"Medium","How many units of Fiction were sold in March?", tb["F"][2], base, set_id=sid)
    T(t,"Medium","What were the total sales (all genres) in March?", mar, base + f"March = 60 + 50 + 30 + 40 = {mar}.", set_id=sid)
    tot = {k: sum(v) for k, v in tb.items()}; top = max(tot, key=tot.get); assert sorted(tot.values())[-1] != sorted(tot.values())[-2]
    M(t,"Medium","Which genre had the highest total sales over the three months?",["Fiction","Science","History","Comics"],names[top], base + "Totals: Fiction 150, Science 100, History 90, Comics 130.", set_id=sid)
    sm = max(range(3), key=lambda i: tb["S"][i])
    M(t,"Medium","In which month were Science sales the highest?",["January","February","March","Equal in two months"],["January","February","March"][sm], base + "Science: 30, 20, 50.", set_id=sid, fixed=True)
    ch = (tb["C"][2]-tb["C"][1])/tb["C"][1]*100
    M(t,"Hard","By what percentage did Comics sales change from February to March?",["25% increase","33.33% increase","25% decrease","40% increase"],"33.33% increase", base + "Comics: 30 → 40, an increase of 10/30 = 33.33%.", set_id=sid, chk=(round(ch,2),33.33))

    # ===== Set 4: coin game =====
    def win_moves(n, moves, misere=False):
        lose = {}
        for k in range(0, 60):
            if k == 0: lose[k] = not misere   # normal: player to move at 0 has lost; misère: the previous player took the last coin and lost
            else: lose[k] = all(not lose[k - m] for m in moves if m <= k)
        return [m for m in moves if m <= n and lose[n - m]], lose
    B.add_set("cd-coins", "dilr", "Coin game", "<b>Coin game</b><p>Asha and Bilal play a game with a pile of coins. They take turns, Asha first. On each turn a player must remove <b>1, 2 or 4</b> coins (never more than the pile holds). Under the standard rule, the player who takes the <b>last</b> coin wins. Both players always play perfectly.</p>")
    sid = "cd-coins"; t = "Games with rules"
    wm, lose = win_moves(20, (1, 2, 4)); assert wm == [2]
    assert [k for k in range(1, 40) if lose[k]] == list(range(3, 40, 3))
    base = "Work backwards: a pile is 'losing' for the player to move if every move leads to a winning pile. 0 is losing. 1, 2 and 4 can reach 0, so they're winning. 3 → 2 or 1 only, so it's losing. In general, the losing piles are exactly the multiples of 3, because 1, 2 and 4 are never multiples of 3. "
    M(t,"Medium","With 20 coins, how many coins must Asha remove on her first turn to be sure of winning?",["1","2","4","She cannot force a win"],"2", base + "20 − 2 = 18 is a multiple of 3. Taking 1 (19) or 4 (16) leaves a winning pile for Bilal.", set_id=sid, fixed=True)
    cnt = sum(1 for k in range(1, 31) if lose[k])
    T(t,"Medium","For how many starting pile sizes from 1 to 30 (inclusive) can Bilal force a win?", cnt, base + "Bilal wins exactly when the start is a multiple of 3: 3, 6, …, 30, which is 10 sizes.", set_id=sid)
    T(t,"Hard","Under the standard rule, what is the smallest starting pile larger than 20 with which Bilal can force a win?", next(k for k in range(21, 60) if lose[k]), base + "The next multiple of 3 after 20 is 21.", set_id=sid)
    wm2, lose2 = win_moves(23, (1, 2, 3, 4)); assert wm2 == [3] and [k for k in range(1, 30) if lose2[k]] == [5, 10, 15, 20, 25]
    M(t,"Hard","Suppose players may remove 1, 2, 3 or 4 coins (last coin still wins). With 23 coins, how many should Asha remove first to be sure of winning?",["1","2","3","4"],"3", "With moves 1–4, the losing piles are multiples of 5 (any move from 5k can be answered to return to 5(k − 1)). Asha should leave 20, so she takes 3.", set_id=sid)
    wm3, lose3 = win_moves(10, (1, 2, 4), misere=True); assert wm3 == []
    msol = [k for k in range(1, 16) if lose3[k]]; assert msol == [1, 4, 7, 10, 13]
    M(t,"Hard","Now suppose the rule is reversed: the player who takes the last coin LOSES (moves are still 1, 2 or 4). With 10 coins, how many should Asha remove first to be sure of winning?",["1","2","4","She cannot force a win"],"She cannot force a win", "Now a pile of 1 is losing for the player to move, because they must take the last coin. Working upward: 2, 3 → can leave 1, so winning. 4 → leaves 3, 2 or 0, and 0 means you just took the last coin and lost, so 4 is losing. The losing piles are 1, 4, 7, 10, 13, … (one more than a multiple of 3). 10 is losing: from 10, Asha can leave 9, 8 or 6, and each lets Bilal move back to 7. So she cannot force a win.", set_id=sid, fixed=True)

    # ===== Set 5: chocolates =====
    sols = [c for c in itertools.product(range(1, 25), repeat=5) if sum(c) == 24 and len(set(c)) == 5 and c[1] == 2*c[2] and c[3] == c[4]+1 and c[0] == c[1]+c[4] and c[0] == max(c) and c[2] > c[3]]
    assert len(sols) == 1, sols; Pq, Qq, Rq, Sq, Tq = sols[0]
    B.add_set("cd-choc", "dilr", "Sharing chocolates", "<b>Sharing chocolates</b><p>24 chocolates were shared among five friends P, Q, R, S and T. Each got at least one, and no two got the same number.</p>" + ul(["Q got twice as many as R.", "S got exactly one more than T.", "P got as many as Q and T together, and P got the most.", "R got more than S."]))
    sid = "cd-choc"; t = "Distribution"
    base = "Let T = t, so S = t + 1. Let R = r, so Q = 2r and P = 2r + t. Total: (2r + t) + 2r + r + (t + 1) + t = 5r + 3t + 1 = 24 ⇒ 5r + 3t = 23. Options: (r, t) = (4, 1) or (1, 6). R > S rules out (1, 6) (R = 1 < S = 7). So P = 9, Q = 8, R = 4, S = 2, T = 1. "
    T(t,"Medium","How many chocolates did Q get?", Qq, base, set_id=sid)
    M(t,"Medium","Who got the fewest chocolates?",["P","R","S","T"],"T", base, set_id=sid)
    T(t,"Medium","How many more chocolates did P get than S?", Pq - Sq, base + "9 − 2 = 7.", set_id=sid)
    opts = {"Q and R": Qq+Rq, "P and S": Pq+Sq, "P and T": Pq+Tq, "R and S": Rq+Sq}; assert list(opts.values()).count(12) == 1
    M(t,"Hard","Which two friends together got exactly half of all the chocolates?",list(opts),[k for k, v in opts.items() if v == 12][0], base + "Q + R = 8 + 4 = 12. The other pairs: P + S = 11, P + T = 10, R + S = 6.", set_id=sid)

    # ===== Set 6: code breaking =====
    def fb(code, g):
        pos = sum(a == b for a, b in zip(code, g)); com = len(set(code) & set(g)); return pos, com - pos
    code = "7392"; guesses = ["7148", "2054", "9361", "3520", "8697", "1052"]
    clues = [(g, fb(code, g)) for g in guesses]
    cand = [c for c in map("".join, itertools.permutations("0123456789", 4)) if c[0] != "0" and all(fb(c, g) == f for g, f in clues)]
    assert cand == [code], cand
    def desc(f):
        a, b = f; parts = []
        if a: parts.append(f"{a} correct digit{'s' if a > 1 else ''} in the correct place")
        if b: parts.append(f"{b} correct digit{'s' if b > 1 else ''} in the wrong place")
        return "; ".join(parts) if parts else "no correct digits"
    B.add_set("cd-code", "dilr", "Locker code", "<b>Locker code</b><p>A locker opens with a 4-digit code. All four digits are different and the first digit is not 0. Six guesses were tried, and each was given the feedback shown.</p><table class='data'><tr><th>Guess</th><th>Feedback</th></tr>" + "".join(f"<tr><td style='font-family:monospace;font-size:1rem'>{g}</td><td style='text-align:left'>{desc(f)}</td></tr>" for g, f in clues) + "</table>")
    sid = "cd-code"; t = "Logic puzzles"
    base = ("(1) 2054 says exactly one of 2, 0, 5, 4 is in the code. 3520 says two of 3, 5, 2, 0 are, so 3 is in the code plus exactly one of 5, 2, 0, and 4 is out. "
            "(2) 9361 needs two of 9, 3, 6, 1, so one of 9, 6, 1 (call it y). 8697 needs two of 8, 6, 9, 7. If y = 1, there's no room for two of those, so y is 9 or 6 and the 4th digit (z) is 8 or 7. "
            "(3) 7148: exactly one digit, in place, so z sits where 7148 has it (7 → 1st place, 8 → 4th place). 1 is out. "
            "(4) 1052: one digit in place, so the digit x from {5, 2, 0} is where 1052 has it: 0 → 2nd, 5 → 3rd, 2 → 4th. But 2054 says x is misplaced there: 0 would be 2nd and 5 would be 3rd in both guesses, a contradiction. So x = 2 in 4th place, which forces z = 7 in 1st place. "
            "(5) The code is 7 _ _ 2 with 3 and y in the middle. 9361 needs exactly one in place: 7362 gives two in place and 7632 gives none, so y = 9. 7932 gives none in place, but 7392 gives 3 in place and 9 misplaced ✓. 8697 then gives 9 in place and 7 misplaced ✓. Code = 7392 (a computer check of all 4,536 possible codes confirms it's the only one). ")
    T(t,"Hard","What is the code? (Enter all four digits.)", int(code), base, set_id=sid)
    T(t,"Medium","What is the sum of the digits of the code?", sum(map(int, code)), base + "7 + 3 + 9 + 2 = 21.", set_id=sid)
    M(t,"Medium","Which digit is in the second position of the code?",["3","9","5","1"],code[1], base, set_id=sid)
    T(t,"Medium","What is the product of the first and last digits of the code?", int(code[0])*int(code[-1]), base + "7 × 2 = 14.", set_id=sid)

    # ===== Set 7: houses =====
    N = ["Kiran","Leela","Manav","Nisha"]; PE = ["cat","dog","parrot","fish"]; CO = ["red","blue","white","black"]; sols = []
    for n in itertools.permutations(N):
        for p in itertools.permutations(PE):
            for c in itertools.permutations(CO):
                h = {x: i for i, x in enumerate(n)}; hp = {x: i for i, x in enumerate(p)}; hc = {x: i for i, x in enumerate(c)}
                if hp["parrot"] != h["Leela"] or hc["red"] != hp["dog"] + 1: continue
                if h["Kiran"] not in (0, 3) or h["Nisha"] not in (0, 3): continue
                if hc["black"] != h["Manav"] or hp["fish"] != 0 or hc["white"] != 3: continue
                if hp["cat"] == h["Manav"] or hp["fish"] != h["Kiran"]: continue
                sols.append((n, p, c))
    assert len(sols) == 1, sols; n, p, c = sols[0]
    B.add_set("cd-houses", "dilr", "Four houses", "<b>Four houses</b><p>Kiran, Leela, Manav and Nisha live in four houses numbered 1 to 4 in a row. Each owns a different pet (cat, dog, parrot, fish) and drives a different coloured car (red, blue, white, black).</p>" + ul(["Kiran and Nisha live in the two end houses.", "Leela owns the parrot. Kiran owns the fish.", "The fish lives in house 1, and the white car belongs to house 4.", "Manav drives the black car and does not own the cat.", "The red car belongs to the house immediately to the right of (one number higher than) the dog's house."]))
    sid = "cd-houses"; t = "Arrangements"
    base = "Kiran owns the fish, which is in house 1, so Kiran = 1 and Nisha = 4 (white car). Leela and Manav are in houses 2 and 3. The dog isn't Kiran's, Leela's (parrot) or in house 4 (red must be to its right), so the dog is Manav's. Red is to the right of the dog and can't be house 4 (white), so Manav = 2 and red = 3 = Leela. Kiran drives blue and Nisha owns the cat. "
    M(t,"Medium","Who owns the cat?",["Kiran","Leela","Manav","Nisha"],n[p.index("cat")], base, set_id=sid)
    M(t,"Medium","What colour is Leela's car?",["Red","Blue","White","Black"],c[n.index("Leela")].capitalize(), base, set_id=sid)
    M(t,"Medium","Who lives in house 2?",["Kiran","Leela","Manav","Nisha"],n[1], base, set_id=sid)
    M(t,"Hard","Which pet lives in the house with the blue car?",["Cat","Dog","Parrot","Fish"],p[c.index("blue")].capitalize(), base, set_id=sid)

    # ===== Set 8: quiz rounds =====
    Cn = "WXYZ"; sols = []
    for r1 in itertools.permutations(Cn):
        for r2 in itertools.permutations(Cn):
            for r3 in itertools.permutations(Cn):
                pts = {x: 0 for x in Cn}
                for rr in (r1, r2, r3):
                    for i, x in enumerate(rr): pts[x] += 4 - i
                if sorted(pts.values(), reverse=True) != [10, 8, 7, 5] or pts["Y"] != 10: continue
                if r1[0] != "X" or r3[3] != "X" or r1[3] != "Z" or r2.index("Z") > r2.index("W"): continue
                if len({r1[0], r2[0], r3[0]}) != 3 or not pts["W"] > pts["Z"]: continue
                sols.append((r1, r2, r3, pts))
    assert len(sols) == 1, sols; r1, r2, r3, pts = sols[0]
    B.add_set("cd-quiz", "dilr", "Three-round quiz", "<b>Three-round quiz</b><p>Four contestants W, X, Y and Z played three rounds. In each round the contestants were ranked 1st to 4th (no ties) and earned 4, 3, 2 and 1 points respectively. The final totals were 10, 8, 7 and 5 points, in some order.</p>" + ul(["Y had the highest total.", "X won Round 1 but came last in Round 3.", "Z came last in Round 1, and finished ahead of W in Round 2.", "Each round had a different winner.", "W's total was higher than Z's."]))
    sid = "cd-quiz"; t = "Rankings & scoring"
    base = ("R1 winner is X and Z is last. Each round has a different winner, so Y wins exactly one of R2/R3. Y = 10 = 4 + 3 + 3, so Y is 2nd in the other two rounds, giving R1: X, Y, W, Z. "
            "X = 4 + (R2 points) + 1 must be 8, 7 or 5, so X is 2nd (X = 8) or 3rd (X = 7) in R2. "
            "Case Y wins R3: R2's winner is Z (Z must be ahead of W) and Y is 2nd, so X is 3rd (X = 7) and W 4th. Then W and Z must total 8 and 5. Z = 1 + 4 + (2 or 3) ≥ 7, so Z = 8 and W = 5, contradicting W > Z. "
            "So Y wins R2. If R2 = Y, Z, X, W, then X = 7, and R3 (won by W or Z) makes either W = 7 (a repeat of X's 7) or W < Z. So R2 = Y, X, Z, W and X = 8. "
            "R3 = winner, Y, other, X. Z winning gives Z = 7 > W = 5 ✗, so W wins. "
            f"Final: R1 {' > '.join(r1)}; R2 {' > '.join(r2)}; R3 {' > '.join(r3)}. Totals W {pts['W']}, X {pts['X']}, Y {pts['Y']}, Z {pts['Z']}. ")
    M(t,"Medium","Who won Round 3?",["W","X","Y","Z"],r3[0], base, set_id=sid)
    T(t,"Medium","What was Z's final total?", pts["Z"], base, set_id=sid)
    M(t,"Hard","Who came second in Round 2?",["W","X","Y","Z"],r2[1], base, set_id=sid)
    T(t,"Hard","In how many rounds did Y finish second?", sum(1 for rr in (r1, r2, r3) if rr[1] == "Y"), base + "Y was 2nd in Rounds 1 and 3.", set_id=sid)
