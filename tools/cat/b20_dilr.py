"""Practice pack b20, DILR (original sets, added 30 Oct 2026): Logic puzzles, Games with rules, Scheduling.
Every set is solved here by brute force; the build stops unless exactly one possibility fits the clues,
and every answer is read from the computed solution."""
import itertools

def ul(items): return "<ul class='clues'>" + "".join(f"<li>{c}</li>" for c in items) + "</ul>"
def tbl(head, rows): return ("<table class='data'><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>"
                             + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table>")

def build(B):
    s = "dilr"
    def fns(sid): return (lambda *a, **k: B.tita(s, *a, set_id=sid, **k)), (lambda *a, **k: B.mcq(s, *a, set_id=sid, **k))

    # ---------- Set 1: true/false answer key (Logic puzzles) ----------
    sheets = {"Asha": "TTFTF", "Bharat": "TFFTT", "Chitra": "FTTTF", "Dev": "FFTFT", "Esha": "TTTFF"}
    def score(k, a): return sum(x == y for x, y in zip(k, a))
    sols = []
    for key in itertools.product("TF", repeat=5):
        k = "".join(key); sc = {n: score(k, a) for n, a in sheets.items()}
        if (sc["Asha"] == sc["Chitra"] == sc["Esha"] and sc["Asha"] > sc["Bharat"]
                and all(sc["Dev"] < v for n, v in sc.items() if n != "Dev")):
            sols.append((k, sc))
    assert len(sols) == 1, sols; key, sc = sols[0]
    assert key == "TTTTF" and sc == {"Asha": 4, "Bharat": 2, "Chitra": 4, "Dev": 1, "Esha": 4}
    B.add_set("b20-anskey", "dilr", "The missing answer key (Medium)",
        "<b>The missing answer key</b><p>A quiz had five true/false questions, Q1 to Q5. Five students answered every question; their answers are shown below (T = true, F = false). "
        "Each correct answer earned 1 mark and there was no negative marking. The answer key has been lost.</p>"
        + tbl(["Student", "Q1", "Q2", "Q3", "Q4", "Q5"], [[n] + list(a) for n, a in sheets.items()])
        + ul(["Asha, Chitra and Esha got the same score.", "Each of Asha, Chitra and Esha scored more than Bharat.", "Dev scored less than every other student."]))
    exp = ("Asha and Chitra differ only on Q1 and Q3, so equal scores mean the key matches Asha on exactly one of them: the key has the same value for Q1 and Q3. "
           "Asha and Esha differ only on Q3 and Q4, so in the same way the key has the same value for Q3 and Q4. Hence Q1 = Q3 = Q4 in the key. "
           "Let x (0, 1 or 2) be the number of the questions Q2, Q5 on which the key matches Asha's answers (T, F). "
           "If Q1 = Q3 = Q4 = F: Asha = 1 + x and Dev = 2 + (2 − x) = 4 − x (Dev's Q2, Q5 answers are the opposite of Asha's). Dev below Asha needs x = 2, but then Bharat = 1 + 0 = 1 is below Dev's 2, "
           "so Dev is not the lowest — this case fails. "
           "If Q1 = Q3 = Q4 = T: Asha = 2 + x, Chitra = 2 + x, Esha = 2 + x, Bharat = 2 + (2 − x) = 4 − x and Dev = 1 + (2 − x) = 3 − x. "
           "Asha > Bharat needs 2 + x > 4 − x, so x = 2: Q2 = T and Q5 = F. "
           "Key: T, T, T, T, F. Scores: Asha 4, Bharat 2, Chitra 4, Dev 1, Esha 4, and Dev is lowest ✓. A computer check of all 32 possible keys finds only this one.")
    T, M = fns("b20-anskey")
    nt = key.count("T"); assert nt == 4
    M("Logic puzzles", "Medium", "How many of the five questions have the answer 'true'?", ["2", "3", "4", "5"], str(nt), exp + f" The key has {nt} trues.")
    T("Logic puzzles", "Medium", "What was Bharat's score?", sc["Bharat"], exp + f" Bharat matches the key on Q1 and Q4 only, so his score is {sc['Bharat']}.")
    tot = sum(sc.values()); neg = 2 * tot - (25 - tot); assert (tot, neg) == (15, 20)
    T("Logic puzzles", "Medium", "If the quiz had instead given +2 for a correct answer and −1 for a wrong answer, what would the five students' marks add up to?", neg,
      exp + f" Together they gave 4 + 2 + 4 + 1 + 4 = {tot} correct and 25 − {tot} = 10 wrong answers, so the total is 2 × {tot} − 10 = {neg}.")
    per = [sum(a[i] == key[i] for a in sheets.values()) for i in range(5)]; nq = sum(p == 3 for p in per); assert per == [3] * 5 and nq == 5
    M("Logic puzzles", "Medium", "For how many of the five questions did exactly three of the five students give the correct answer?", ["2", "3", "4", "5"], str(nq),
      exp + " Reading each column against the key T, T, T, T, F, every question was answered correctly by exactly three students, so the answer is 5.")

    # ---------- Set 2: siblings' ages (Logic puzzles) ----------
    sols = [(a, b, c, d, e) for a, b, c, d, e in itertools.product(range(1, 31), repeat=5)
            if len({a, b, c, d, e}) == 5 and a + b + c + d + e == 50 and a == c + 4 and b == 2 * d and e == a + 3 and d > c
            and b == max(a, b, c, d, e) and b - min(a, b, c, d, e) == 8]
    assert sols == [(10, 14, 6, 7, 13)], sols; a, b, c, d, e = sols[0]
    B.add_set("b20-siblings", "dilr", "Five siblings (Easy)",
        "<b>Five siblings</b><p>Anil, Babita, Chirag, Dimple and Ekta are siblings. Their ages are whole numbers of years, and no two of them are the same age.</p>"
        + ul(["Their ages add up to 50 years.", "Anil is 4 years older than Chirag.", "Babita is twice as old as Dimple.", "Ekta is 3 years older than Anil.",
              "Dimple is older than Chirag.", "Babita is the eldest, and she is 8 years older than the youngest sibling."]))
    exp = ("Let Chirag be c and Dimple d. Then Anil = c + 4, Ekta = c + 7 and Babita = 2d, so the total is 3c + 3d + 11 = 50, giving c + d = 13 with d > c. "
           "The youngest is Chirag (Anil and Ekta are older than Chirag, and so are Dimple and Babita), so 2d − c = 8. With c + d = 13 this gives 3d = 21: d = 7, c = 6. "
           "Ages: Anil 10, Babita 14, Chirag 6, Dimple 7, Ekta 13 (total 50 ✓, Babita eldest ✓).")
    T, M = fns("b20-siblings")
    T("Logic puzzles", "Easy", "How old is Dimple (in years)?", d, exp)
    order = sorted(zip((a, b, c, d, e), ["Anil", "Babita", "Chirag", "Dimple", "Ekta"]), reverse=True); assert order[1][1] == "Ekta"
    M("Logic puzzles", "Easy", "Who is the second eldest of the five?", ["Anil", "Ekta", "Dimple", "Chirag"], "Ekta", exp + " In order of age: Babita 14, Ekta 13, Anil 10, Dimple 7, Chirag 6.")
    old = sum(x > a for x in (b, c, d, e)); assert old == 2
    M("Logic puzzles", "Easy", "How many of the siblings are older than Anil?", ["1", "2", "3", "4"], str(old), exp + " Only Babita (14) and Ekta (13) are older than Anil (10).")
    yrs = [t for t in range(0, 50) if (c + t) + (d + t) == b + t]; assert yrs == [1]
    T("Logic puzzles", "Easy", "After how many years will the combined age of Chirag and Dimple equal Babita's age at that time?", yrs[0],
      exp + " After t years: (6 + t) + (7 + t) = 14 + t, so 13 + 2t = 14 + t and t = 1.")

    # ---------- Set 3: parcels weighed in pairs (Logic puzzles) ----------
    pair_list = [11, 13, 16, 17, 20, 20, 22, 23, 25, 29]
    sols = [w for w in itertools.combinations(range(1, 41), 5) if sorted(x + y for x, y in itertools.combinations(w, 2)) == pair_list]
    assert sols == [(4, 7, 9, 13, 16)], sols; P_, Q_, R_, S_, T_ = sols[0]
    B.add_set("b20-parcels", "dilr", "Parcels weighed in pairs (Medium)",
        "<b>Parcels weighed in pairs</b><p>Five parcels P, Q, R, S and T have different weights, each a whole number of kilograms, with P &lt; Q &lt; R &lt; S &lt; T. "
        "Every one of the ten possible pairs of parcels was put on a scale together, and the ten readings were written down without noting which pair gave which reading. "
        "The readings, in kg, in increasing order were:</p><p><b>11, 13, 16, 17, 20, 20, 22, 23, 25, 29</b></p>")
    exp = ("Each parcel appears in 4 of the 10 pairs, so the readings add up to 4 × (total weight): 196 = 4 × total, total = 49 kg. "
           "The two lightest readings must be P + Q = 11 and P + R = 13; the two heaviest must be S + T = 29 and R + T = 25. "
           "Then R = 49 − (P + Q) − (S + T) = 49 − 11 − 29 = 9, so P = 13 − 9 = 4, Q = 7, T = 25 − 9 = 16 and S = 13. "
           "Check: the ten sums of 4, 7, 9, 13, 16 are exactly 11, 13, 16, 17, 20, 20, 22, 23, 25, 29 ✓ (a computer search over all sets of five weights up to 40 kg finds no other).")
    T, M = fns("b20-parcels")
    T("Logic puzzles", "Medium", "What is the total weight (in kg) of all five parcels?", P_ + Q_ + R_ + S_ + T_, exp)
    T("Logic puzzles", "Medium", "What is the weight (in kg) of parcel R?", R_, exp)
    M("Logic puzzles", "Medium", "What is the weight of parcel T?", ["13 kg", "15 kg", "16 kg", "18 kg"], f"{T_} kg", exp, fixed=False)
    pairs20 = sorted(n1 + "–" + n2 for (n1, x), (n2, y) in itertools.combinations(zip("PQRST", sols[0]), 2) if x + y == 20); assert pairs20 == ["P–T", "Q–S"]
    M("Logic puzzles", "Medium", "Which two pairs gave the reading of 20 kg?", ["P–T and Q–S", "P–S and Q–T", "Q–S and R–S", "P–T and R–S"], "P–T and Q–S",
      exp + " 4 + 16 = 20 (P–T) and 7 + 13 = 20 (Q–S).")

    # ---------- Set 4: rock-paper-scissors (Games with rules) ----------
    beats = {("R", "S"), ("P", "R"), ("S", "P")}
    hands = "RPS"; cells = [(x, y) for x in hands for y in hands if x != y]
    sols = []
    for vals in itertools.product(range(10), repeat=6):
        n = dict(zip(cells, vals))
        if sum(vals) != 9: continue
        rv = [sum(n[(x, y)] for y in hands if y != x) for x in hands]
        sm = [sum(n[(x, y)] for x in hands if x != y) for y in hands]
        if rv != [4, 3, 2] or sm != [2, 3, 4]: continue
        rw = sum(v for k, v in n.items() if k in beats)
        if 9 - rw > rw and rw >= 2: sols.append((n, rw))
    assert len(sols) == 1, sols; n, rw = sols[0]
    assert n == {("R", "P"): 2, ("R", "S"): 2, ("P", "R"): 1, ("P", "S"): 2, ("S", "R"): 1, ("S", "P"): 1} and rw == 4
    B.add_set("b20-rps", "dilr", "Rock, paper, scissors (Hard)",
        "<b>Rock, paper, scissors</b><p>Ravi and Sima played 9 rounds of rock–paper–scissors. In each round both show one hand at the same time: rock beats scissors, scissors beats paper and paper beats rock; "
        "the same hand on both sides is a draw.</p>"
        + ul(["None of the 9 rounds was a draw.", "Ravi showed rock 4 times, paper 3 times and scissors 2 times.", "Sima showed rock 2 times, paper 3 times and scissors 4 times.",
              "Sima won more rounds than Ravi.", "Ravi won at least two rounds."]))
    exp = ("Write RP for 'Ravi rock, Sima paper' and so on; with no draws there are six kinds of round. Let RP = x. "
           "Ravi's rocks: RP + RS = 4, so RS = 4 − x. Sima's paper: RP + SP = 3, so SP = 3 − x. Ravi's scissors: SR + SP = 2, so SR = x − 1. "
           "Sima's rock: PR + SR = 2, so PR = 3 − x. Ravi's paper: PR + PS = 3, so PS = x. (Sima's scissors: RS + PS = 4 ✓.) So 1 ≤ x ≤ 3. "
           "Ravi wins with RS, PR and SP: (4 − x) + (3 − x) + (3 − x) = 10 − 3x; Sima wins the other 3x − 1. "
           "x = 1 gives Ravi 7 wins (Sima does not win more); x = 3 gives Ravi only 1 win; so x = 2. "
           "Rounds: RP 2, RS 2, PR 1, PS 2, SR 1, SP 1. Ravi won 4 rounds and Sima 5.")
    T, M = fns("b20-rps")
    T("Games with rules", "Hard", "How many rounds did Ravi win?", rw, exp)
    T("Games with rules", "Hard", "In how many rounds did Ravi's rock lose to Sima's paper?", n[("R", "P")], exp + f" RP = x = {n[('R', 'P')]}.")
    M("Games with rules", "Hard", "In how many rounds did Ravi show paper and win?", ["0", "1", "2", "3"], str(n[("P", "R")]), exp + f" Ravi's paper wins against rock: PR = {n[('P', 'R')]}.")
    alt = set()
    for vals in itertools.product(range(10), repeat=6):
        m = dict(zip(cells, vals))
        if sum(vals) != 9: continue
        if [sum(m[(x, y)] for y in hands if y != x) for x in hands] != [4, 3, 2] or [sum(m[(x, y)] for x in hands if x != y) for y in hands] != [2, 3, 4]: continue
        r = sum(v for k, v in m.items() if k in beats)
        if 9 - r > r: alt.add(r)
    assert alt == {1, 4}
    M("Games with rules", "Hard", "If the last condition (Ravi won at least two rounds) were dropped, how many different values would be possible for the number of rounds Ravi won?",
      ["1", "2", "3", "4"], str(len(alt)), exp + " Without that condition both x = 2 and x = 3 are allowed, giving Ravi 4 or 1 wins — two possible values.")

    # ---------- Set 5: pebble passing (Games with rules) ----------
    names = "ABCD"; st = [11, 7, 4, 2]; hist = [tuple(st)]; giver = [None]
    for r in range(1, 101):
        g = max(range(4), key=lambda i: (st[i], -i)); giver.append(names[g])
        for i in range(4):
            if i != g: st[i] += 1
        st[g] -= 3; hist.append(tuple(st))
    assert hist[1:5] == [(8, 8, 5, 3), (5, 9, 6, 4), (6, 6, 7, 5), (7, 7, 4, 6)] and hist[5:7] == [(4, 8, 5, 7), (5, 5, 6, 8)]
    assert all(hist[r] == hist[r - 4] for r in range(7, 101))
    B.add_set("b20-pebbles", "dilr", "Passing pebbles (Medium)",
        "<b>Passing pebbles</b><p>Four children, A, B, C and D, start a game with 11, 7, 4 and 2 pebbles respectively. The game is played in rounds. "
        "In each round, the child holding the most pebbles gives one pebble to each of the other three children. If two or more children are tied for the most, "
        "the one who comes first in alphabetical order gives.</p>")
    exp = ("Holdings (A, B, C, D) after each round: start (11, 7, 4, 2); round 1, A gives: (8, 8, 5, 3); round 2, A gives (tie with B, A first): (5, 9, 6, 4); "
           "round 3, B gives: (6, 6, 7, 5); round 4, C gives: (7, 7, 4, 6); round 5, A gives: (4, 8, 5, 7); round 6, B gives: (5, 5, 6, 8); round 7, D gives: (6, 6, 7, 5) — the same as after round 3. "
           "So from round 3 on the holdings repeat every 4 rounds, with givers C, A, B, D in rounds 4, 5, 6, 7, then 8, 9, 10, 11, and so on.")
    T, M = fns("b20-pebbles")
    M("Games with rules", "Medium", "Who gives pebbles in round 3?", ["A", "B", "C", "D"], giver[3], exp)
    T("Games with rules", "Medium", "How many pebbles does D hold after round 50?", hist[50][3],
      exp + f" After round r (r ≥ 3) the holdings depend on r mod 4: 50 leaves remainder 2, the same as round 6, so D holds {hist[50][3]}.")
    na = giver[1:21].count("A"); assert na == 6
    T("Games with rules", "Medium", "In how many of the first 20 rounds is A the child who gives?", na,
      exp + f" A gives in rounds 1, 2, 5, 9, 13 and 17 — {na} times.")
    mn = min(min(h) for h in hist[1:]); assert mn == 3
    M("Games with rules", "Medium", "Over the first 100 rounds, what is the smallest number of pebbles held by any child at the end of a round?", ["2", "3", "4", "5"], str(mn),
      exp + " D has 3 after round 1; after that every state in the cycle has at least 4 in each hand (round 2's smallest is 4 too). So the minimum is 3.")

    # ---------- Set 6: sealed-bid auction (Games with rules) ----------
    bids = {"W": [40, 30, 35, 20, 50], "X": [35, 45, 10, 40, 30], "Y": [30, 40, 45, 30, 25], "Z": [45, 20, 30, 45, 40]}
    def sim(bids, first_price=False, capped=True):
        tok = {p: 100 for p in "WXYZ"}; log = []
        for L in range(5):
            eff = {p: (min(bids[p][L], tok[p]) if capped else bids[p][L]) for p in "WXYZ"}
            order = sorted("WXYZ", key=lambda p: (-eff[p], -tok[p], p))
            assert eff[order[0]] > eff[order[1]]   # no tie for the top bid in any variant asked
            w = order[0]; price = eff[w] if first_price else eff[order[1]]
            tok[w] -= price; log.append((L + 1, w, price))
        return tok, log
    tok, log = sim(bids)
    assert log == [(1, "Z", 40), (2, "X", 40), (3, "Y", 35), (4, "Z", 40), (5, "W", 30)] and tok == {"W": 70, "X": 60, "Y": 65, "Z": 20}
    B.add_set("b20-auction", "dilr", "Sealed-bid auction (Medium)",
        "<b>Sealed-bid auction</b><p>Four collectors, W, X, Y and Z, each start with 100 tokens. Five lots are auctioned one after another, Lot 1 to Lot 5. "
        "Before the auction each collector wrote down a planned bid for every lot (table below). The rules are:</p>"
        + ul(["For each lot, a collector's actual bid is the planned bid, or the tokens he has left at that moment if that is smaller.",
              "The highest actual bid wins the lot, but the winner pays the <i>second-highest</i> actual bid for that lot.",
              "If two collectors tie for the highest bid, the one with more tokens left wins (this never happens below)."])
        + tbl(["Collector", "Lot 1", "Lot 2", "Lot 3", "Lot 4", "Lot 5"], [[p] + v for p, v in bids.items()]))
    exp = ("Lot 1: Z bids 45 (highest), second-highest is W's 40 — Z pays 40 and has 60 left. Lot 2: X 45 wins and pays Y's 40 (X left 60). "
           "Lot 3: Y 45 wins and pays W's 35 (Y left 65). Lot 4: Z 45 (Z still has 60) wins and pays X's 40 — Z has 20 left. "
           "Lot 5: Z's planned 40 is cut to 20 tokens; W 50 wins and pays the second-highest actual bid, X's 30 (W left 70). "
           "Final tokens: W 70, X 60, Y 65, Z 20.")
    T, M = fns("b20-auction")
    T("Games with rules", "Medium", "How many tokens does Z have left at the end of the auction?", tok["Z"], exp)
    lo = min(log, key=lambda t: t[2]); assert lo[0] == 5 and sorted(t[2] for t in log) == [30, 35, 40, 40, 40]
    M("Games with rules", "Medium", "Which lot was sold for the lowest price?", ["Lot 1", "Lot 3", "Lot 4", "Lot 5"], f"Lot {lo[0]}",
      exp + " Prices: 40, 40, 35, 40, 30 — Lot 5 at 30 is the lowest.")
    tok2, _ = sim(bids, capped=False); assert tok2["W"] == 60
    T("Games with rules", "Medium", "If bids were never cut down to the tokens a collector has left (everything else unchanged), how many tokens would W have at the end?", tok2["W"],
      exp + " Only Lot 5 changes: Z's bid stays 40, so W still wins with 50 but pays 40 instead of 30, ending with 100 − 40 = 60.")
    tok3, log3 = sim(bids, first_price=True); assert log3 == [(1, "Z", 45), (2, "X", 45), (3, "Y", 45), (4, "Z", 45), (5, "W", 50)] and tok3["Z"] == 10
    M("Games with rules", "Medium", "If instead the winner of each lot paid his own actual bid (everything else unchanged), how many tokens would Z have at the end?",
      ["0", "10", "15", "20"], str(tok3["Z"]),
      exp + " With pay-your-bid: Z wins Lot 1 for 45 (55 left), X wins Lot 2 for 45, Y wins Lot 3 for 45, Z wins Lot 4 for 45 (10 left), and W wins Lot 5 for 50 (Z's bid is cut to 10). Z ends with 10.")

    # ---------- Set 7: project tasks (Scheduling) ----------
    TK = {"A": (3, ""), "B": (4, ""), "C": (2, "A"), "D": (5, "AB"), "E": (3, "C"), "F": (4, "DE"), "G": (2, "B"), "H": (5, "G")}
    ef = {}
    for t in "ABCDEFGH": ef[t] = max([ef[p] for p in TK[t][1]], default=0) + TK[t][0]
    proj = max(ef.values()); lf = {}
    for t in sorted(TK, key=lambda t: -ef[t]):
        lf[t] = min([lf[x] - TK[x][0] for x in TK if t in TK[x][1]], default=proj)
    slack = {t: lf[t] - ef[t] for t in TK}
    assert proj == 13 and slack == {"A": 1, "B": 0, "C": 1, "D": 0, "E": 1, "F": 0, "G": 2, "H": 2}
    def best(k):   # exact minimum finish with k workers, no splitting of tasks (starts only at time 0 or at finishes: left-shift argument)
        from functools import lru_cache
        @lru_cache(None)
        def dfs(done, running, t):
            if len(done) == 8: return t
            res = 10 ** 9; busy = {x for _, x in running}
            avail = [x for x in TK if x not in done and x not in busy and all(p in done for p in TK[x][1])]
            for m in range(min(k - len(running), len(avail)), -1, -1):
                for sub in itertools.combinations(avail, m):
                    nr = tuple(sorted(running + tuple((t + TK[x][0], x) for x in sub)))
                    if not nr: continue
                    f = nr[0][0]
                    res = min(res, dfs(done | frozenset(x for ff, x in nr if ff == f), tuple(r for r in nr if r[0] != f), f))
            return res
        return dfs(frozenset(), (), 0)
    b1, b2, b3 = best(1), best(2), best(3); assert (b1, b2, b3) == (28, 14, 13)
    kmin = min(k for k in (1, 2, 3, 4) if best(k) == proj); assert kmin == 3
    B.add_set("b20-project", "dilr", "Workshop renovation (Hard)",
        "<b>Workshop renovation</b><p>A renovation has eight tasks, A to H. The table gives each task's duration in days and the tasks that must be fully finished before it can start. "
        "A task, once started, is done by one worker without a break; a worker does one task at a time; any worker can do any task.</p>"
        + tbl(["Task", "Duration (days)", "Must follow"], [[t, d, ", ".join(p) if p else "—"] for t, (d, p) in TK.items()]))
    exp = ("With enough workers, every task starts as soon as its predecessors finish. Finish days: A 3, B 4, C 5, D 9 (after A and B), E 8, F 13 (after D at 9 and E at 8), G 6, H 11. "
           "So the project needs 13 days, along the chain B → D → F (4 + 5 + 4). Working backwards from day 13, the latest finishes are A 4, B 4, C 6, D 9, E 9, F 13, G 8, H 13, "
           "so the slacks are A 1, B 0, C 1, D 0, E 1, F 0, G 2, H 2.")
    T, M = fns("b20-project")
    T("Scheduling", "Medium", "With as many workers as needed, what is the minimum number of days to finish the whole renovation?", proj, exp)
    M("Scheduling", "Hard", "With as many workers as needed and the renovation finishing in the minimum time, which tasks can each be delayed by 2 days without delaying the finish?",
      ["G and H only", "A, C and E only", "C, E and G only", "G only"], "G and H only", exp + " Only G and H have a slack of 2 days.")
    T("Scheduling", "Hard", "If only two workers are available, what is the minimum number of days needed?", b2,
      exp + " The tasks total 3 + 4 + 2 + 5 + 3 + 4 + 2 + 5 = 28 worker-days, so two workers need at least 14 days. 14 is achievable: worker 1 does A (0–3), C (3–5), D (5–10), F (10–14); "
      "worker 2 does B (0–4), G (4–6), E (6–9), H (9–14). Every task starts after its predecessors finish, so the answer is 14.")
    M("Scheduling", "Hard", "What is the smallest number of workers with which the renovation can still be finished in the minimum possible time found with unlimited workers?",
      ["2", "3", "4", "5"], str(kmin), exp + " Two workers need at least 28/2 = 14 days, so 13 days needs at least 3. With three it works: start every task as early as possible — "
      "at most three tasks (C, D and G, during day 4 to 5) are ever in progress together, so 3 workers suffice.")
    # confirm the claim about the early-start schedule's peak load
    es = {t: ef[t] - TK[t][0] for t in TK}
    assert max(sum(es[t] <= x < ef[t] for t in TK) for x in range(13)) == 3

    # ---------- Set 8: exam timetable (Scheduling) ----------
    papers = {"A": "Accounts", "B": "Biology", "C": "Chemistry", "D": "Drawing", "E": "Economics", "F": "French"}
    sols = []
    for days in itertools.permutations(range(1, 9), 6):
        dd = dict(zip("ABCDEF", days)); free = sorted(set(range(1, 9)) - set(days))
        if 1 in free or 8 in free or free[1] - free[0] == 1: continue
        if not (dd["B"] < dd["C"] and dd["C"] - dd["B"] > 1): continue
        if dd["E"] - dd["A"] != 3 or any(dd["A"] < x < dd["E"] for x in free): continue
        if dd["F"] - 1 not in free or dd["B"] % 2 or dd["C"] < dd["F"]: continue
        sols.append((dd, free))
    assert len(sols) == 1, sols; dd, free = sols[0]
    assert dd == {"A": 1, "B": 2, "C": 8, "D": 3, "E": 4, "F": 6} and free == [5, 7]
    B.add_set("b20-exams", "dilr", "Exam timetable (Medium)",
        "<b>Exam timetable</b><p>Six papers — Accounts, Biology, Chemistry, Drawing, Economics and French — are to be held over eight days, Day 1 to Day 8, at most one paper a day. "
        "So exactly two days have no paper (free days).</p>"
        + ul(["There is a paper on Day 1 and on Day 8, and the two free days are not next to each other.",
              "Biology is held before Chemistry, and they are not on consecutive days.",
              "Economics is held exactly three days after Accounts, and there is no free day between them.",
              "French is held on the day just after a free day.",
              "Biology is held on an even-numbered day.",
              "Chemistry is held after French."]))
    exp = ("Accounts and Economics are 3 days apart with no free day between, so Accounts, two other papers and Economics fill four consecutive days. "
           "French follows a free day and Chemistry comes after French, so Chemistry is not on Day 1–3 and French is not on Day 1. "
           "Trying the placements (the computer checks all 20,160 ways): the only timetable that fits is Day 1 Accounts, Day 2 Biology, Day 3 Drawing, Day 4 Economics, Day 5 free, "
           "Day 6 French, Day 7 free, Day 8 Chemistry. Check: free days 5 and 7 not adjacent ✓; Biology (2) before Chemistry (8), not consecutive ✓; Economics 4 = Accounts 1 + 3 with Days 2–3 busy ✓; "
           "French on 6 after free Day 5 ✓; Biology on an even day ✓; Chemistry after French ✓.")
    T, M = fns("b20-exams")
    M("Scheduling", "Medium", "Which paper is held on Day 3?", ["Biology", "Drawing", "Economics", "French"], "Drawing", exp)
    T("Scheduling", "Medium", "On which day is French held?", dd["F"], exp)
    M("Scheduling", "Medium", "Which are the two free days?", ["Days 4 and 6", "Days 5 and 7", "Days 3 and 5", "Days 2 and 7"], "Days 5 and 7", exp)
    between = sum(dd["B"] < v < dd["C"] for v in dd.values()); assert between == 3
    M("Scheduling", "Medium", "How many papers are held after Biology but before Chemistry?", ["2", "3", "4", "5"], str(between),
      exp + " Drawing (3), Economics (4) and French (6) lie between Biology (2) and Chemistry (8): 3 papers.")
