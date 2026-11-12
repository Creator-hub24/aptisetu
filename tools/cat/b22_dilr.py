"""Practice pack b22, DILR (original arrangement sets, added 12 Nov 2026).
Each data set comes from a hidden arrangement drawn with a fixed seed. Clues are added until a brute-force search of
every arrangement finds exactly one that fits; clues that are not needed are then removed (the search is re-run each
time) and every answer is read from the unique solution. The generator stops if any check fails.

Difficulty calibration (against the existing Easy pack ez-row* and the bank's Medium/Hard sets):
- Easy:   5 people, 1 attribute + position; direct clues allowed; about 6-8 clues, 5-7 deduction steps (~3 min/question).
- Medium: 6 people, 2 attributes + position; at most 2 direct facts, the rest relative; about 9-12 clues (~4-5 min/question).
- Hard:   6 people, 2-3 attributes + position; no direct facts about a named person's position; negative,
          'exactly k between', cross-attribute and either-or clues; about 11-15 clues, case analysis (~5-6 min/question).
"""
import itertools, random

from ortools.sat.python import cp_model

def pid(sol, r): return r[1] if r[0] == "n" else sol[r[1]].index(r[2])
def holds(spec, sol):
    """Plain-Python check of one clue on a complete arrangement (independent of the solver)."""
    P = lambda r: sol[0][pid(sol, r)]
    t = spec[0]
    if t == "rel": return P(spec[2]) - P(spec[1]) in spec[3]
    if t == "at": return P(spec[1]) == spec[2]
    if t == "notat": return P(spec[1]) != spec[2]
    if t == "in": return P(spec[1]) in spec[2]
    if t == "is": return pid(sol, spec[1]) == pid(sol, spec[2])
    if t == "isnot": return pid(sol, spec[1]) != pid(sol, spec[2])
    if t == "either": return (P(spec[1]) == spec[2]) != (P(spec[3]) == spec[4])
    raise ValueError(spec)

class _Unused:
    def __init__(self, V, n, k, limit):
        super().__init__(); self.V, self.n, self.k, self.limit, self.out = V, n, k, limit, []
    def on_solution_callback(self):
        self.out.append([tuple(self.Value(self.V[a][p]) for p in range(self.n)) for a in range(self.k + 1)])
        if len(self.out) >= self.limit: self.StopSearch()

def model(n, k, clues):
    m = cp_model.CpModel()
    V = [[m.NewIntVar(0, n - 1, f"v{a}_{p}") for p in range(n)] for a in range(k + 1)]
    I = [[m.NewIntVar(0, n - 1, f"i{a}_{v}") for v in range(n)] for a in range(k + 1)]
    for a in range(k + 1): m.AddAllDifferent(V[a]); m.AddInverse(V[a], I[a])
    cache = {}
    def P(r):
        if r[0] == "n": return V[0][r[1]]
        if r not in cache:
            x = m.NewIntVar(0, n - 1, ""); m.AddElement(I[r[1]][r[2]], V[0], x); cache[r] = x
        return cache[r]
    def who(r): return r[1] if r[0] == "n" else I[r[1]][r[2]]
    for c in clues:
        sp = c["spec"]; t = sp[0]
        if t == "rel":
            d = m.NewIntVar(-(n - 1), n - 1, ""); m.Add(d == P(sp[2]) - P(sp[1]))
            m.AddLinearExpressionInDomain(d, cp_model.Domain.FromValues(sorted(sp[3])))
        elif t == "at": m.Add(P(sp[1]) == sp[2])
        elif t == "notat": m.Add(P(sp[1]) != sp[2])
        elif t == "in": m.AddLinearExpressionInDomain(P(sp[1]), cp_model.Domain.FromValues(sorted(sp[2])))
        elif t in ("is", "isnot"):
            x, y = who(sp[1]), who(sp[2])
            if isinstance(x, int) and isinstance(y, int): (m.Add(0 == 0) if (x == y) == (t == "is") else m.Add(0 == 1))
            else:
                if isinstance(x, int): x, y = y, x
                m.Add(x == y) if t == "is" else m.Add(x != y)
        elif t == "either":
            b1, b2 = m.NewBoolVar(""), m.NewBoolVar("")
            m.Add(P(sp[1]) == sp[2]).OnlyEnforceIf(b1); m.Add(P(sp[1]) != sp[2]).OnlyEnforceIf(b1.Not())
            m.Add(P(sp[3]) == sp[4]).OnlyEnforceIf(b2); m.Add(P(sp[3]) != sp[4]).OnlyEnforceIf(b2.Not())
            m.Add(b1 + b2 == 1)
    return m, V

def solve(n, k, clues, limit=2):
    """Find up to `limit` different arrangements that fit the clues, with the OR-tools CP-SAT solver: solve, then forbid
    the arrangement just found and solve again, until the model is proved infeasible or `limit` is reached.
    (The puzzle is accepted only if this returns exactly one arrangement AND every single fact of it is separately proved
    forced by `fixed` below; every clue is also re-checked in plain Python with `holds`.)"""
    m, V = model(n, k, clues); out = []
    while len(out) < limit:
        s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.cp_model_presolve = False
        st = s.Solve(m)
        if st == cp_model.INFEASIBLE: break
        assert st in (cp_model.FEASIBLE, cp_model.OPTIMAL), st
        sol = [tuple(s.Value(V[a][p]) for p in range(n)) for a in range(k + 1)]
        assert all(holds(c["spec"], sol) for c in clues)
        out.append(sol)
        bs = []
        for a in range(k + 1):
            for p in range(n):
                b = m.NewBoolVar(""); m.Add(V[a][p] != sol[a][p]).OnlyEnforceIf(b); bs.append(b)
        m.AddBoolOr(bs)
    return out

def levels(spec):
    refs = [x for x in spec[1:] if isinstance(x, tuple)]
    lv = {r[1] for r in refs if r[0] == "a"}
    if spec[0] not in ("is", "isnot"): lv.add(0)
    return max(lv) if lv else 0

def brute(n, k, clues, limit=2):
    """Independent plain-Python check (no solver): every position permutation, then every permutation of each
    attribute in turn; a clue is tested as soon as all the attributes it mentions are assigned."""
    by = [[] for _ in range(k + 1)]
    for c in clues: by[levels(c["spec"])].append(c["spec"])
    perms = list(itertools.permutations(range(n))); sol = [None] * (k + 1); out = []
    def rec(a):
        if a > k: out.append([tuple(x) for x in sol]); return len(out) >= limit
        for pm in perms:
            sol[a] = pm
            if all(holds(sp, sol) for sp in by[a]) and rec(a + 1): return True
        sol[a] = None; return False
    rec(0); return out

def fixed(n, k, clues, sol):
    """Facts (person, attribute, value) of `sol` that are forced by `clues`: for each one the solver proves that no
    arrangement fitting the clues gives that person a different value (a fresh model per fact)."""
    out = []
    for a in range(k + 1):
        for p in range(n):
            m, V = model(n, k, clues); m.Add(V[a][p] != sol[a][p])
            s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.cp_model_presolve = False
            st = s.Solve(m); assert st in (cp_model.INFEASIBLE, cp_model.FEASIBLE, cp_model.OPTIMAL), st
            if st == cp_model.INFEASIBLE: out.append((p, a, sol[a][p]))
    return out

def cap(s): return s[0].upper() + s[1:]

class Gen:
    def __init__(self, seed, names, attrs, lay, level, circular=False):
        self.rng = random.Random(seed); self.names = names; self.attrs = attrs; self.lay = lay
        self.level = level; self.circ = circular; self.n = len(names); self.k = len(attrs)
        self.sol = [tuple(self.rng.sample(range(self.n), self.n)) for _ in range(self.k + 1)]
    # refs: ("n", p) or ("a", a, v)
    def txt(self, r): return self.names[r[1]] if r[0] == "n" else self.attrs[r[1] - 1]["who"].format(self.attrs[r[1] - 1]["vals"][r[2]])
    def rand_ref(self, allow_attr=True):
        if allow_attr and self.k and self.rng.random() < 0.45:
            a = self.rng.randint(1, self.k); return ("a", a, self.rng.randrange(self.n))
        return ("n", self.rng.randrange(self.n))
    def clue(self, kind, spec, text): return {"kind": kind, "spec": spec, "text": cap(text)}
    def candidates(self):
        L, s0, n, out = self.lay, self.sol, self.n, []
        P = lambda r: s0[0][pid(s0, r)]
        allv = set(range(-(n - 1), n))
        def rel(kind, r1, r2, S, text): out.append(self.clue(kind, ("rel", r1, r2, frozenset(S)), text))
        for _ in range(400):
            r1, r2 = self.rand_ref(), self.rand_ref()
            if r1 == r2: continue
            diff_kind = not (r1[0] == "n" and r2[0] == "n") and not (r1[0] == r2[0] == "a" and r1[1] == r2[1])
            if pid(s0, r1) == pid(s0, r2):
                if diff_kind: out.append(self.clue("is", ("is", r1, r2), self.same_text(r1, r2, True)))
                continue
            t1, t2 = self.txt(r1), self.txt(r2); d = P(r2) - P(r1)
            if self.circ:
                dm = d % n
                if dm == 1: rel("imm", r1, r2, {1, 1 - n}, L["imm"](t1, t2))
                if dm == 2: rel("two", r1, r2, {2, 2 - n}, L["two"](t1, t2))
                if dm == n // 2: rel("opp", r1, r2, {n // 2, -(n // 2)}, L["opp"](t1, t2))
                nb = {1, -1, n - 1, 1 - n}
                if dm in (1, n - 1): rel("next", r1, r2, nb, L["next"](t1, t2))
                else: rel("notnext", r1, r2, allv - nb - {0}, L["notnext"](t1, t2))
            else:
                if d == 1: rel("imm", r1, r2, {1}, L["imm"](t1, t2))
                if d > 0: rel("before", r1, r2, set(range(1, n)), L["before"](t1, t2))
                g = abs(d) - 1
                if g >= 1: rel("gap", r1, r2, {g + 1, -(g + 1)}, L["gap"](t1, t2, g))
                if g == 0: rel("next", r1, r2, {1, -1}, L["next"](t1, t2))
                else: rel("notnext", r1, r2, allv - {1, -1, 0}, L["notnext"](t1, t2))
            if diff_kind: out.append(self.clue("isnot", ("isnot", r1, r2), self.same_text(r1, r2, False)))
        for _ in range(60):
            r = self.rand_ref(); p = P(r)
            out.append(self.clue("at", ("at", r, p), L["at"](self.txt(r), p)))
            q = self.rng.choice([x for x in range(n) if x != p])
            out.append(self.clue("notat", ("notat", r, q), L["notat"](self.txt(r), q)))
            if not self.circ and p in (0, n - 1): out.append(self.clue("end", ("in", r, frozenset({0, n - 1})), L["end"](self.txt(r))))
            if self.level == "Hard":
                r2 = self.rand_ref(); q2 = self.rng.randrange(n)
                if P(r2) != q2 and pid(s0, r2) != pid(s0, r):
                    out.append(self.clue("either", ("either", r, p, r2, q2), L["either"](self.txt(r), p, self.txt(r2), q2)))
        seen, uniq = set(), []
        for c in out:
            assert holds(c["spec"], s0), c["text"]
            if c["text"] not in seen: seen.add(c["text"]); uniq.append(c)
        return uniq
    def ok_kind(self, c):
        named_at = c["kind"] in ("at", "end") and c["text"].split()[0] in self.names
        if self.level == "Hard": return c["kind"] not in ("at", "is") or (c["kind"] == "is" and self.rng.random() < 0.35)
        if self.level == "Medium": return not named_at or self.rng.random() < 0.3
        return True
    def make(self):
        pool = [c for c in self.candidates() if self.ok_kind(c)]
        self.rng.shuffle(pool)
        strong = {"Easy": ("at", "is", "imm", "next"), "Medium": ("imm", "gap", "two", "opp", "is"),
                  "Hard": ("gap", "two", "opp", "imm", "either", "is")}[self.level]
        weak = ("notat", "isnot", "notnext")
        def rr(cs):   # round-robin over clue kinds, so no kind dominates
            by = {}
            for c in cs: by.setdefault(c["kind"], []).append(c)
            ks = sorted(by); self.rng.shuffle(ks); out = []
            while any(by.values()):
                for kk in ks:
                    if by[kk]: out.append(by[kk].pop(0))
            return out
        pool = (rr([c for c in pool if c["kind"] in strong]) + rr([c for c in pool if c["kind"] not in strong and c["kind"] not in weak])
                + rr([c for c in pool if c["kind"] in weak])[:4])
        if self.level != "Easy":   # mix strong and medium clues
            s_, m_ = [c for c in pool if c["kind"] in strong], [c for c in pool if c["kind"] not in strong]
            pool = [x for pair in itertools.zip_longest(s_, s_[len(s_):], m_) for x in pair if x is not None]
        chosen = []
        for c in pool:
            chosen.append(c)
            if len(solve(self.n, self.k, chosen, 2)) == 1: break
        else: return None
        for c in list(chosen):   # minimise
            t = [x for x in chosen if x is not c]
            if len(solve(self.n, self.k, t, 2)) == 1: chosen = t
        res = solve(self.n, self.k, chosen, 2); assert len(res) == 1 and res[0] == [tuple(x) for x in self.sol]
        assert all(holds(c["spec"], self.sol) for c in chosen)
        self.clues = chosen; return chosen
    # ---------- solution narrative
    def facts(self, s):
        out = []
        for p in range(self.n):
            out.append((p, 0, s[0][p]))
            for a in range(1, self.k + 1): out.append((p, a, s[a][p]))
        return out
    def fact_text(self, f):
        p, a, v = f
        return self.lay["fixpos"](self.names[p], v) if a == 0 else f"{self.names[p]}: {self.attrs[a-1]['vals'][v]}"
    def narrative(self):
        order = sorted(self.clues, key=lambda c: ["at", "is", "imm", "opp", "two", "gap", "either", "end", "next", "before", "notat", "isnot", "notnext"].index(c["kind"]))
        steps, known, used = [], set(), []
        for i, c in enumerate(order, 1):
            used.append(c)
            new = [f for f in sorted(fixed(self.n, self.k, used, self.sol), key=lambda f: (f[1], f[0])) if f not in known]; known |= set(new)
            steps.append(f"Step {i}: “{c['text'].rstrip('.')}.” " + ("Now fixed: " + "; ".join(self.fact_text(f) for f in new) + "." if new else
                         "Note it; it rules out some placements but fixes nothing on its own yet."))
        assert len(known) == self.n * (self.k + 1)
        bf = brute(self.n, self.k, self.clues, 2); assert bf == [[tuple(x) for x in self.sol]], "brute-force check failed"
        return " ".join(steps) + " Every possible arrangement was checked by computer and exactly one fits all the clues: " + self.table_text() + "."
    def table_text(self):
        rows = []
        for pos in range(self.n):
            p = self.sol[0].index(pos)
            extra = ", ".join(self.attrs[a - 1]["vals"][self.sol[a][p]] for a in range(1, self.k + 1))
            rows.append(f"{self.lay['pos'](pos)}: {self.names[p]}" + (f" ({extra})" if extra else ""))
        return "; ".join(rows)

    def same_text(self, r1, r2, yes):
        if r1[0] == "a" and r2[0] == "n": r1, r2 = r2, r1
        if r1[0] == "n":
            at = self.attrs[r2[1] - 1]
            return at["has" if yes else "hasnot"].format(self.names[r1[1]], at["vals"][r2[2]])
        return f"{self.txt(r1)} is {'also' if yes else 'not'} {self.txt(r2)}."

# ---------------- layouts ----------------
def linear(noun, left, right, before_w, front=None):
    """Positions numbered 1..n from the left (or bottom)."""
    return {
        "pos": lambda i: f"{noun} {i+1}",
        "fixpos": lambda nm, i: f"{nm} in {noun} {i+1}",
        "at": lambda a, p: f"{a} is in {noun} {p+1}.",
        "notat": lambda a, p: f"{a} is not in {noun} {p+1}.",
        "imm": lambda a, b: f"{a} is immediately {left} {b}.",
        "before": lambda a, b: f"{a} is somewhere {before_w} {b}.",
        "gap": lambda a, b, g: f"There {'is exactly one' if g == 1 else 'are exactly ' + str(g)} {'person' if g == 1 else 'people'} between {a} and {b}.",
        "next": lambda a, b: f"{a} and {b} are next to each other.",
        "notnext": lambda a, b: f"{a} and {b} are not next to each other.",
        "end": lambda a: f"{a} is at one of the two ends.",
        "either": lambda a, p, b, q: f"Either {a} is in {noun} {p+1} or {b} is in {noun} {q+1}, but not both.",
        "whoat": lambda i: f"Who is in {noun} {i+1}?",
        "posq": lambda r: f"In which {noun} is {r}? (Enter the {noun} number.)",
        "rel": f"immediately {right}", "relf": lambda p, n: p + 1 if p + 1 < n else None,
        "numeric": True, "linear": True,
    }

def floors():
    return {
        "pos": lambda i: f"floor {i+1}",
        "fixpos": lambda nm, i: f"{nm} on floor {i+1}",
        "at": lambda a, p: f"{a} lives on floor {p+1}.",
        "notat": lambda a, p: f"{a} does not live on floor {p+1}.",
        "imm": lambda a, b: f"{a} lives on the floor immediately below {b}.",
        "before": lambda a, b: f"{a} lives on some floor below {b}.",
        "gap": lambda a, b, g: f"There {'is exactly one floor' if g == 1 else 'are exactly ' + str(g) + ' floors'} between the floors of {a} and {b}.",
        "next": lambda a, b: f"{a} and {b} live on adjacent floors.",
        "notnext": lambda a, b: f"{a} and {b} do not live on adjacent floors.",
        "end": lambda a: f"{a} lives on either the top floor or the bottom floor.",
        "either": lambda a, p, b, q: f"Either {a} lives on floor {p+1} or {b} lives on floor {q+1}, but not both.",
        "whoat": lambda i: f"Who lives on floor {i+1}?",
        "posq": lambda r: f"On which floor does {r} live? (Enter the floor number.)",
        "rel": "on the floor immediately above", "relf": lambda p, n: p + 1 if p + 1 < n else None,
        "numeric": True, "linear": True,
    }

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
def days():
    return {
        "pos": lambda i: DAYS[i],
        "fixpos": lambda nm, i: f"{nm} on {DAYS[i]}",
        "at": lambda a, p: f"{a} is scheduled on {DAYS[p]}.",
        "notat": lambda a, p: f"{a} is not scheduled on {DAYS[p]}.",
        "imm": lambda a, b: f"{a} is scheduled on the day immediately before {b}.",
        "before": lambda a, b: f"{a} is scheduled on some day before {b}.",
        "gap": lambda a, b, g: f"There {'is exactly one day' if g == 1 else 'are exactly ' + str(g) + ' days'} between the days of {a} and {b}.",
        "next": lambda a, b: f"{a} and {b} are scheduled on consecutive days.",
        "notnext": lambda a, b: f"{a} and {b} are not scheduled on consecutive days.",
        "end": lambda a: f"{a} is scheduled on either the first or the last day.",
        "either": lambda a, p, b, q: f"Either {a} is scheduled on {DAYS[p]} or {b} is scheduled on {DAYS[q]}, but not both.",
        "whoat": lambda i: f"Who is scheduled on {DAYS[i]}?",
        "posq": None,
        "rel": "on the day immediately after", "relf": lambda p, n: p + 1 if p + 1 < n else None,
        "numeric": False, "linear": True,
    }

def circle():
    return {
        "pos": lambda i: f"seat {i+1}",
        "fixpos": lambda nm, i: f"{nm} in seat {i+1}",
        "at": lambda a, p: f"{a} sits in seat {p+1}.",
        "notat": lambda a, p: f"{a} does not sit in seat {p+1}.",
        "imm": lambda a, b: f"{b} sits to the immediate left of {a}.",
        "two": lambda a, b: f"{b} sits second to the left of {a}.",
        "opp": lambda a, b: f"{a} sits directly opposite {b}.",
        "next": lambda a, b: f"{a} sits next to {b}.",
        "notnext": lambda a, b: f"{a} does not sit next to {b}.",
        "either": lambda a, p, b, q: f"Either {a} sits in seat {p+1} or {b} sits in seat {q+1}, but not both.",
        "whoat": lambda i: f"Who sits in seat {i+1}?",
        "posq": lambda r: f"In which seat does {r} sit? (Enter the seat number.)",
        "rel": "to the immediate right of", "relf": lambda p, n: (p - 1) % n,
        "numeric": True, "linear": False,
    }

def attr(label, who, has, hasnot, q, vals): return {"label": label, "who": who, "has": has, "hasnot": hasnot, "q": q, "vals": vals}

# ---------------- questions ----------------
def questions(g, sid, level, B, topic="Arrangements"):
    rng, n, s, L = g.rng, g.n, g.sol, g.lay
    exp = g.narrative()
    clue_txt = " ".join(c["text"] for c in g.clues)
    T = lambda *a, **k: B.tita("dilr", *a, set_id=sid, **k)
    M = lambda *a, **k: B.mcq("dilr", *a, set_id=sid, **k)
    pos_of = lambda p: s[0][p]; at = lambda i: s[0].index(i)
    nm = g.names
    def others(correct, pool):
        o = [x for x in pool if x != correct]; rng.shuffle(o); return o[:3] + [correct]
    made = []
    def q_whoat():
        cands = [i for i in range(n) if L["at"](nm[at(i)], i).rstrip(".") not in clue_txt]
        i = rng.choice(cands); c = nm[at(i)]
        M(topic, level, L["whoat"](i), others(c, nm), c, exp + f" Reading off: {L['pos'](i)} has {c}.")
    def q_attr():
        a = rng.randint(1, g.k); at_ = g.attrs[a - 1]
        cands = [p for p in range(n) if at_["has"].format(nm[p], at_["vals"][s[a][p]]).rstrip(".") not in clue_txt]
        p = rng.choice(cands); c = at_["vals"][s[a][p]]
        M(topic, level, at_["q"].format(nm[p]), others(c, at_["vals"]), c, exp + f" Reading off: {nm[p]} — {c}.")
    def q_cross():
        a, b = rng.sample(range(1, g.k + 1), 2); A, Bt = g.attrs[a - 1], g.attrs[b - 1]
        v = rng.randrange(n); p = s[a].index(v); c = Bt["vals"][s[b][p]]
        M(topic, level, f"What is the {Bt['label']} of {A['who'].format(A['vals'][v])}?", others(c, Bt["vals"]), c,
          exp + f" {cap(A['who'].format(A['vals'][v]))} is {nm[p]}, whose {Bt['label']} is {c}.")
    def q_between():
        pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if abs(pos_of(x) - pos_of(y)) >= 2]
        x, y = rng.choice(pairs)
        if g.k and rng.random() < 0.6:
            a = rng.randint(1, g.k); rx = g.attrs[a - 1]["who"].format(g.attrs[a - 1]["vals"][s[a][x]])
        else: rx = nm[x]
        ans = abs(pos_of(x) - pos_of(y)) - 1
        T(topic, level, f"How many people are between {rx} and {nm[y]}?", ans, exp + f" {cap(rx)} ({nm[x]}) is in {L['pos'](pos_of(x))} and {nm[y]} in {L['pos'](pos_of(y))}, so {ans} {'person is' if ans == 1 else 'people are'} between them.")
    def q_posnum():
        if g.k and rng.random() < 0.7:
            a = rng.randint(1, g.k); v = rng.randrange(n); p = s[a].index(v); r = g.attrs[a - 1]["who"].format(g.attrs[a - 1]["vals"][v])
        else: p = rng.randrange(n); r = nm[p]
        T(topic, level, L["posq"](r), pos_of(p) + 1, exp + f" {cap(r)} is {nm[p]}, in {L['pos'](pos_of(p))}.")
    def q_count():   # days layout / generic: how many scheduled after someone
        p = rng.choice([p for p in range(n) if 0 < pos_of(p) < n - 1]); ans = n - 1 - pos_of(p)
        T(topic, level, f"How many of the {n} are scheduled on days after {nm[p]}'s day?", ans, exp + f" {nm[p]} is on {L['pos'](pos_of(p))}, and {ans} people come after.")
    def q_true():
        def st(kind, x, y=None, a=None):
            if kind == "next":
                tv = abs(pos_of(x) - pos_of(y)) == 1 if L["linear"] else (pos_of(x) - pos_of(y)) % n in (1, n - 1)
                return L["next"](nm[x], nm[y]), tv
            if kind == "at": return L["at"](nm[x], y), pos_of(x) == y
            if kind == "has": at_ = g.attrs[a - 1]; return at_["has"].format(nm[x], at_["vals"][y]), s[a][x] == y
        tr, fa, tries = [], [], 0
        while (not tr or len(fa) < 3) and tries < 500:
            tries += 1; kind = rng.choice(["next", "at"] + (["has"] * 2 if g.k else []))
            x = rng.randrange(n)
            if kind == "next": t, v = st(kind, x, rng.choice([y for y in range(n) if y != x]))
            elif kind == "at": t, v = st(kind, x, rng.randrange(n))
            else: a = rng.randint(1, g.k); t, v = st(kind, x, rng.randrange(n), a)
            if t.rstrip(".") in clue_txt or t in tr or t in fa: continue
            (tr if v else fa).append(t)
        c = tr[0]; opts = fa[:3] + [c]
        M(topic, level, "Which of the following statements is true?", [o.rstrip(".") for o in opts], c.rstrip("."),
          exp + f" Checking each option against this arrangement, only “{c.rstrip('.')}” holds.")
    def q_chain():
        cands = [p for p in range(n) if L["relf"](pos_of(p), n) is not None]
        p = rng.choice(cands); q = at(L["relf"](pos_of(p), n))
        if g.k and rng.random() < 0.6:
            a = rng.randint(1, g.k); A = g.attrs[a - 1]; c = A["vals"][s[a][q]]
            text = f"What is the {A['label']} of the person {L['rel']} {nm[p]}?"; opts = others(c, A["vals"])
        else:
            c = nm[q]; text = f"Who is {L['rel']} {nm[p]}?"; opts = others(c, [x for x in nm if x != nm[p]])
        M(topic, level, text, opts, c, exp + f" {nm[p]} is in {L['pos'](pos_of(p))}; the person {L['rel']} is {nm[q]}" + (f", whose {A['label']} is {c}." if c != nm[q] else "."))
    tita1 = q_posnum if L["posq"] else q_count
    tita2 = q_between if L["linear"] else q_posnum
    if level == "Easy": plan = [q_whoat, q_attr, tita2, q_true, q_chain]
    elif level == "Medium": plan = [q_attr, q_cross, tita1, q_true, q_chain]
    else: plan = [q_cross, tita2, q_true, q_chain, tita1] if L["linear"] else [q_cross, q_posnum, q_true, q_chain, q_attr]
    for f in plan: f()

# ---------------- themes ----------------
A = attr
COL = lambda vals: A("colour", "the person with the {} umbrella", "{0}'s umbrella is {1}.", "{0}'s umbrella is not {1}.", "What is the colour of {0}'s umbrella?", vals)
THEMES = [
 # (level, intro, names, layout, attrs, title)
 ("Easy", "Five colleagues, {N}, hang their coats on five hooks numbered 1 to 5 from left to right, one coat per hook. Each of them carries an umbrella of a different colour: {V0}.",
  ["Kabir", "Lata", "Mohan", "Nisha", "Om"], linear("hook", "to the left of", "to the right of", "to the left of"),
  [COL(["green", "yellow", "purple", "orange", "brown"])], "Coat hooks"),
 ("Easy", "Five neighbours, {N}, live in a five-storey building, one on each floor; floor 1 is the lowest and floor 5 the highest. Each keeps a different pet: {V0}.",
  ["Pallavi", "Qadir", "Rekha", "Sunil", "Tanvi"], floors(),
  [A("pet", "the {} owner", "{0} keeps the {1}.", "{0} does not keep the {1}.", "Which pet does {0} keep?", ["parrot", "rabbit", "cat", "tortoise", "goldfish"])], "Five floors"),
 ("Easy", "Five speakers, {N}, give one talk each at a club, one per day from Monday to Friday. Each talk is on a different subject: {V0}.",
  ["Uday", "Vani", "Waseem", "Yamini", "Zubin"], days(),
  [A("subject", "the {} speaker", "{0} speaks on {1}.", "{0} does not speak on {1}.", "On which subject does {0} speak?", ["birds", "coins", "stamps", "trains", "kites"])], "Talk week"),
 ("Easy", "Five runners, {N}, start a race from five lanes numbered 1 to 5 from left to right. Each wears a different bib number: {V0}.",
  ["Aditi", "Bhavesh", "Charu", "Dhruv", "Elina"], linear("lane", "to the left of", "to the right of", "to the left of"),
  [A("bib", "the runner wearing bib {}", "{0} wears bib {1}.", "{0} does not wear bib {1}.", "Which bib number does {0} wear?", ["11", "22", "33", "44", "55"])], "Starting lanes"),
 ("Easy", "Five cousins, {N}, sit on five chairs in a straight row, numbered 1 to 5 from left to right, all facing the stage. Each has ordered a different drink: {V0}.",
  ["Farah", "Girish", "Hema", "Imran", "Jyoti"], linear("chair", "to the left of", "to the right of", "to the left of"),
  [A("drink", "the person who ordered {}", "{0} ordered {1}.", "{0} did not order {1}.", "Which drink did {0} order?", ["lassi", "coffee", "lemonade", "buttermilk", "cocoa"])], "Front row"),
 ("Easy", "Five interns, {N}, each present a report on a different day from Monday to Friday. Each report is on a different city: {V0}.",
  ["Keshav", "Leela", "Manav", "Naina", "Ojas"], days(),
  [A("city", "the intern reporting on {}", "{0} reports on {1}.", "{0} does not report on {1}.", "Which city does {0} report on?", ["Indore", "Mysuru", "Shillong", "Udaipur", "Varanasi"])], "Report days"),
 # ---- Medium: 6 people, 2 attributes
 ("Medium", "Six friends, {N}, sit around a circular table in seats numbered 1 to 6 clockwise, all facing the centre (so the person on someone's immediate left is in the next seat clockwise). Each supports a different football club, {V0}, and each drinks a different beverage, {V1}.",
  ["Arjun", "Bela", "Chaitanya", "Divya", "Eshan", "Fiza"], circle(),
  [A("club", "the {} supporter", "{0} supports {1}.", "{0} does not support {1}.", "Which club does {0} support?", ["Rovers", "United", "City", "Athletic", "Wanderers", "Rangers"]),
   A("drink", "the person drinking {}", "{0} drinks {1}.", "{0} does not drink {1}.", "What does {0} drink?", ["tea", "coffee", "juice", "milk", "soda", "water"])], "Round table"),
 ("Medium", "Six tenants, {N}, live in a six-storey building, one per floor (floor 1 is the lowest). Each owns a different vehicle, {V0}, and each works in a different field, {V1}.",
  ["Gauri", "Harish", "Ira", "Jatin", "Kamala", "Lokesh"], floors(),
  [A("vehicle", "the {} owner", "{0} owns the {1}.", "{0} does not own the {1}.", "Which vehicle does {0} own?", ["scooter", "sedan", "bicycle", "jeep", "van", "motorbike"]),
   A("profession", "the {}", "{0} is the {1}.", "{0} is not the {1}.", "What is {0}'s profession?", ["nurse", "chef", "pilot", "lawyer", "painter", "teacher"])], "Six storeys"),
 ("Medium", "Six students, {N}, stand in a row of six spots numbered 1 to 6 from left to right for a photograph. Each holds a different musical instrument, {V0}, and each is from a different state, {V1}.",
  ["Manish", "Neha", "Omkar", "Preeti", "Rahul", "Sanya"], linear("spot", "to the left of", "to the right of", "to the left of"),
  [A("instrument", "the {} player", "{0} plays the {1}.", "{0} does not play the {1}.", "Which instrument does {0} play?", ["flute", "sitar", "tabla", "violin", "veena", "drums"]),
   A("state", "the student from {}", "{0} is from {1}.", "{0} is not from {1}.", "Which state is {0} from?", ["Assam", "Bihar", "Goa", "Kerala", "Punjab", "Odisha"])], "Band photo"),
 ("Medium", "Six chefs, {N}, each cook the staff lunch on one day from Monday to Saturday. Each makes a different main dish, {V0}, and each uses a different spice as the highlight, {V1}.",
  ["Tara", "Umesh", "Vidya", "Wahid", "Yash", "Zoya"], days(),
  [A("dish", "the chef who makes {}", "{0} makes {1}.", "{0} does not make {1}.", "Which dish does {0} make?", ["pulao", "khichdi", "biryani", "dal", "kadhi", "rajma"]),
   A("spice", "the chef who uses {}", "{0} uses {1}.", "{0} does not use {1}.", "Which spice does {0} use?", ["saffron", "clove", "cardamom", "fennel", "nutmeg", "mustard"])], "Lunch rota"),
 ("Medium", "Six players, {N}, sit around a circular card table in seats numbered 1 to 6 clockwise, all facing the centre (the person on someone's immediate left is in the next seat clockwise). Each wears a cap of a different colour, {V0}, and each prefers a different card game, {V1}.",
  ["Anand", "Bindu", "Chirayu", "Devika", "Ehsaan", "Falguni"], circle(),
  [A("cap", "the player in the {} cap", "{0} wears the {1} cap.", "{0} does not wear the {1} cap.", "What colour is {0}'s cap?", ["red", "blue", "green", "white", "black", "pink"]),
   A("game", "the {} fan", "{0} prefers {1}.", "{0} does not prefer {1}.", "Which game does {0} prefer?", ["rummy", "bridge", "poker", "hearts", "solitaire", "snap"])], "Card table"),
 ("Medium", "Six shops in a market lane are numbered 1 to 6 from west to east (shop 1 is the westernmost). They are run by {N}, one each. Each shop sells a different product, {V0}, and each closes for its weekly holiday on a different day, {V1}.",
  ["Gopal", "Hina", "Ishaan", "Jaya", "Karan", "Lavanya"], linear("shop", "to the west of", "to the east of", "to the west of"),
  [A("product", "the {} seller", "{0} sells {1}.", "{0} does not sell {1}.", "What does {0} sell?", ["shoes", "toys", "books", "spices", "lamps", "clocks"]),
   A("holiday", "the shopkeeper who closes on {}", "{0} closes on {1}.", "{0} does not close on {1}.", "On which day does {0}'s shop close?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"])], "Market lane"),
 ("Medium", "Six officers, {N}, occupy six cabins numbered 1 to 6 in a straight corridor (cabin 1 at the left end). Each handles a different department, {V0}, and each has joined in a different year, {V1}.",
  ["Mehul", "Nandini", "Ojasvi", "Pranav", "Ritika", "Sahil"], linear("cabin", "to the left of", "to the right of", "to the left of"),
  [A("department", "the officer handling {}", "{0} handles {1}.", "{0} does not handle {1}.", "Which department does {0} handle?", ["audit", "sales", "legal", "payroll", "design", "support"]),
   A("year", "the officer who joined in {}", "{0} joined in {1}.", "{0} did not join in {1}.", "In which year did {0} join?", ["2015", "2016", "2018", "2019", "2021", "2023"])], "Office corridor"),
 ("Medium", "Six residents, {N}, live on floors 1 to 6 of a tower, one per floor (floor 1 is the lowest). Each reads a different newspaper, {V0}, and each has a different hobby, {V1}.",
  ["Tanmay", "Urmila", "Varun", "Wamiqa", "Yuvraj", "Zeenat"], floors(),
  [A("newspaper", "the {} reader", "{0} reads the {1}.", "{0} does not read the {1}.", "Which newspaper does {0} read?", ["Herald", "Courier", "Tribune", "Gazette", "Chronicle", "Bulletin"]),
   A("hobby", "the person who enjoys {}", "{0} enjoys {1}.", "{0} does not enjoy {1}.", "What is {0}'s hobby?", ["chess", "pottery", "cycling", "baking", "gardening", "origami"])], "Tower residents"),
 ("Medium", "Six speakers, {N}, sit around a round discussion table in seats numbered 1 to 6 clockwise, facing the centre (the person on someone's immediate left is in the next seat clockwise). Each represents a different city, {V0}, and each speaks on a different theme, {V1}.",
  ["Abhay", "Bhumika", "Chetna", "Dinesh", "Elakshi", "Firoz"], circle(),
  [A("city", "the delegate from {}", "{0} represents {1}.", "{0} does not represent {1}.", "Which city does {0} represent?", ["Agartala", "Bhopal", "Cuttack", "Dehradun", "Erode", "Gaya"]),
   A("theme", "the speaker on {}", "{0} speaks on {1}.", "{0} does not speak on {1}.", "Which theme does {0} speak on?", ["water", "energy", "health", "housing", "transport", "waste"])], "Round-table panel"),
]
HARD = [
 ("Six engineers, {N}, sit in a row of six desks numbered 1 to 6 from left to right. Each uses a different laptop brand, {V0}; each codes mainly in a different language, {V1}; and each started on a different weekday, {V2}.",
  ["Aakash", "Bhoomi", "Chandan", "Deepika", "Eklavya", "Gargi"], linear("desk", "to the left of", "to the right of", "to the left of"),
  [A("laptop", "the {} user", "{0} uses the {1} laptop.", "{0} does not use the {1} laptop.", "Which laptop brand does {0} use?", ["Arco", "Brisk", "Corvo", "Delta", "Echo", "Fable"]),
   A("language", "the person who codes in {}", "{0} codes in {1}.", "{0} does not code in {1}.", "Which language does {0} code in?", ["Python", "Java", "Go", "Rust", "Kotlin", "Swift"]),
   A("start day", "the person who started on {}", "{0} started on {1}.", "{0} did not start on {1}.", "On which day did {0} start?", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])], "Desk row"),
 ("Six families, {N}, live on floors 1 to 6 of a building, one family per floor (floor 1 is the lowest). Each family owns a different car colour, {V0}, and each has a different number of members, {V1}.",
  ["the Bhatts", "the Chawlas", "the Dases", "the Gills", "the Iyers", "the Joshis"], floors(),
  [A("car colour", "the family with the {} car", "{0} own the {1} car.", "{0} do not own the {1} car.", "What colour is the car of {0}?", ["silver", "maroon", "beige", "navy", "olive", "teal"]),
   A("size", "the family of {}", "{0} are a family of {1}.", "{0} are not a family of {1}.", "How many members do {0} have?", ["two", "three", "four", "five", "six", "seven"])], "Family floors"),
 ("Six friends, {N}, sit around a circular table in seats numbered 1 to 6 clockwise, all facing the centre (the person on someone's immediate left is in the next seat clockwise). Each ordered a different dessert, {V0}; each paid by a different method, {V1}; and each arrived by a different mode, {V2}.",
  ["Kunal", "Lalita", "Mitali", "Nakul", "Parth", "Ruchi"], circle(),
  [A("dessert", "the person who ordered {}", "{0} ordered {1}.", "{0} did not order {1}.", "Which dessert did {0} order?", ["kulfi", "halwa", "rasmalai", "jalebi", "brownie", "sorbet"]),
   A("payment", "the person who paid by {}", "{0} paid by {1}.", "{0} did not pay by {1}.", "How did {0} pay?", ["cash", "card", "UPI", "voucher", "cheque", "wallet"]),
   A("transport", "the person who came by {}", "{0} came by {1}.", "{0} did not come by {1}.", "How did {0} come?", ["metro", "bus", "auto", "taxi", "bike", "foot"])], "Dessert table"),
 ("Six lectures by {N} are held on six consecutive days, Monday to Saturday, one per day. Each lecture is in a different hall, {V0}, and each covers a different topic, {V1}.",
  ["Prof. Sen", "Prof. Rao", "Prof. Pillai", "Prof. Mehta", "Prof. Khan", "Prof. Bose"], days(),
  [A("hall", "the lecture in {}", "{0} lectures in {1}.", "{0} does not lecture in {1}.", "In which hall does {0} lecture?", ["Hall A", "Hall B", "Hall C", "Hall D", "Hall E", "Hall F"]),
   A("topic", "the lecturer on {}", "{0} lectures on {1}.", "{0} does not lecture on {1}.", "On which topic does {0} lecture?", ["comets", "fungi", "glaciers", "monsoons", "volcanoes", "tides"])], "Lecture week"),
 ("Six cyclists, {N}, finished a race in positions 1 to 6 with no ties (position 1 is the winner, and someone 'ahead of' another finished in a smaller position number). Each rode a bicycle of a different colour, {V0}; each represented a different club, {V1}; and each is a different age, {V2}.",
  ["Ajay", "Bhavna", "Chirag", "Dolly", "Ehsan", "Farida"], linear("position", "ahead of", "behind", "ahead of"),
  [A("bike colour", "the rider on the {} bike", "{0} rode the {1} bike.", "{0} did not ride the {1} bike.", "What colour was {0}'s bike?", ["red", "blue", "green", "yellow", "white", "black"]),
   A("club", "the {} club rider", "{0} rode for {1}.", "{0} did not ride for {1}.", "Which club did {0} ride for?", ["Falcons", "Hawks", "Kites", "Eagles", "Swifts", "Herons"]),
   A("age", "the {}-year-old", "{0} is {1}.", "{0} is not {1}.", "How old is {0}?", ["19", "21", "23", "25", "27", "29"])], "Race result"),
 ("Six singers, {N}, perform one after another in slots 1 to 6 at a concert (slot 1 is first). Each sings in a different language, {V0}, and each is accompanied by a different instrument, {V1}.",
  ["Gulzar", "Harpreet", "Indu", "Jagan", "Komal", "Lakshmi"], linear("slot", "before", "after", "before"),
  [A("language", "the {} singer", "{0} sings in {1}.", "{0} does not sing in {1}.", "In which language does {0} sing?", ["Tamil", "Bangla", "Marathi", "Telugu", "Kannada", "Urdu"]),
   A("instrument", "the singer accompanied by the {}", "{0} is accompanied by the {1}.", "{0} is not accompanied by the {1}.", "Which instrument accompanies {0}?", ["harmonium", "sarod", "santoor", "mridangam", "shehnai", "guitar"])], "Concert order"),
 ("Six analysts, {N}, sit around a hexagonal table in seats numbered 1 to 6 clockwise, all facing the centre (the person on someone's immediate left is in the next seat clockwise). Each covers a different sector, {V0}, and each has a different rating, {V1}.",
  ["Mahesh", "Nirmala", "Oindrila", "Prakash", "Rohini", "Sameer"], circle(),
  [A("sector", "the {} analyst", "{0} covers {1}.", "{0} does not cover {1}.", "Which sector does {0} cover?", ["banking", "cement", "pharma", "steel", "telecom", "textiles"]),
   A("rating", "the analyst rated {}", "{0} is rated {1}.", "{0} is not rated {1}.", "What is {0}'s rating?", ["A1", "A2", "B1", "B2", "C1", "C2"])], "Hexagonal table"),
 ("Six tenants, {N}, occupy floors 1 to 6 of a building (floor 1 is the lowest). Each has a different profession, {V0}; each has a different favourite fruit, {V1}; and each owns a different pet, {V2}.",
  ["Tushar", "Uma", "Vikram", "Wasima", "Yogesh", "Zara"], floors(),
  [A("profession", "the {}", "{0} is the {1}.", "{0} is not the {1}.", "What is {0}'s profession?", ["architect", "dentist", "editor", "farmer", "jeweller", "potter"]),
   A("fruit", "the person who likes {}", "{0} likes {1}.", "{0} does not like {1}.", "Which fruit does {0} like?", ["mango", "guava", "papaya", "litchi", "plum", "fig"]),
   A("pet", "the {} owner", "{0} owns the {1}.", "{0} does not own the {1}.", "Which pet does {0} own?", ["dog", "cat", "parrot", "hamster", "turtle", "rabbit"])], "Three-way floors"),
 ("Six interviews of candidates {N} take place on six consecutive days, Monday to Saturday, one per day. Each candidate applies for a different role, {V0}, and each comes from a different city, {V1}.",
  ["Aarav", "Barkha", "Cyrus", "Damini", "Eshwar", "Fatima"], days(),
  [A("role", "the candidate for {}", "{0} applies for {1}.", "{0} does not apply for {1}.", "Which role does {0} apply for?", ["analyst", "designer", "tester", "manager", "writer", "trainer"]),
   A("city", "the candidate from {}", "{0} comes from {1}.", "{0} does not come from {1}.", "Which city does {0} come from?", ["Nagpur", "Surat", "Ranchi", "Kochi", "Jammu", "Patna"])], "Interview week"),
 ("Six guests, {N}, sit around a round dinner table in seats numbered 1 to 6 clockwise, all facing the centre (the person on someone's immediate left is in the next seat clockwise). Each is a different profession, {V0}; each wears a different colour, {V1}; and each brought a different gift, {V2}.",
  ["Ganesh", "Hansa", "Inder", "Jharna", "Kiran", "Lubna"], circle(),
  [A("profession", "the {}", "{0} is the {1}.", "{0} is not the {1}.", "What is {0}'s profession?", ["doctor", "banker", "poet", "actor", "coach", "judge"]),
   A("colour", "the guest in {}", "{0} wears {1}.", "{0} does not wear {1}.", "What colour does {0} wear?", ["red", "blue", "gold", "grey", "mauve", "cream"]),
   A("gift", "the guest who brought {}", "{0} brought {1}.", "{0} did not bring {1}.", "Which gift did {0} bring?", ["flowers", "sweets", "a book", "a plant", "wine glasses", "a candle"])], "Dinner circle"),
 ("Six stalls in a row at a fair are numbered 1 to 6 from left to right and are run by {N}, one each. Each stall sells a different craft, {V0}; each was booked on a different date, {V1}; and each stallholder comes from a different district, {V2}.",
  ["Madhav", "Nupur", "Oshin", "Pankaj", "Radhika", "Shaurya"], linear("stall", "to the left of", "to the right of", "to the left of"),
  [A("craft", "the {} seller", "{0} sells {1}.", "{0} does not sell {1}.", "Which craft does {0} sell?", ["baskets", "bangles", "carpets", "dolls", "masks", "puppets"]),
   A("booking date", "the stall booked on the {}", "{0} booked on the {1}.", "{0} did not book on the {1}.", "On which date did {0} book?", ["1st", "3rd", "5th", "8th", "13th", "21st"]),
   A("district", "the stallholder from {}", "{0} comes from {1}.", "{0} does not come from {1}.", "Which district does {0} come from?", ["Kutch", "Bastar", "Kangra", "Madhubani", "Nalanda", "Sivasagar"])], "Craft fair"),
]

def intro(t, names, attrs):
    d = {"N": ", ".join(names[:-1]) + " and " + names[-1]}
    for i, a in enumerate(attrs): d[f"V{i}"] = ", ".join(a["vals"][:-1]) + " and " + a["vals"][-1]
    return t.format(**d)

def build(B, seeds=None, only=None):
    items = [(lv, t, nm, lay, at, ti) for lv, t, nm, lay, at, ti in THEMES] + [("Hard", t, nm, lay, at, ti) for t, nm, lay, at, ti in HARD]
    for i, (lv, t, nm, lay, at, ti) in enumerate(items):
        if only is not None and i not in only: continue
        seed = (seeds or {}).get(i, 2200 + i)
        while True:
            g = Gen(seed, nm, at, lay, lv, circular=not lay["linear"])
            ch = g.make()
            nclue = len(ch) if ch else 0
            lo, hi = {"Easy": (5, 9), "Medium": (8, 13), "Hard": (10, 17 if len(at) < 3 else 19)}[lv]
            if ch and lo <= nclue <= hi: break
            seed += 1000
            assert seed < 2200 + i + 1000 * 60, ('no puzzle in range', i)
        rng = random.Random(seed); clues = list(g.clues); rng.shuffle(clues); g.clues = clues
        sid = f"z1-d{i+1:02d}"
        B.add_set(sid, "dilr", f"{ti} ({lv})", f"<b>{ti}</b><p>{intro(t, nm, at)}</p><p>The following is known:</p><ul class='clues'>"
                  + "".join(f"<li>{c['text']}</li>" for c in clues) + "</ul>")
        questions(g, sid, lv, B)
        print(i, lv, ti, "seed", seed, "clues", nclue, flush=True)
