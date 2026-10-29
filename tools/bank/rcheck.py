"""Brute-force checkers for Bank/SSC reasoning items (inequalities, syllogisms, family trees, arrangements)."""
import itertools, re

# ---------- inequalities ----------
_OPS = {'>': lambda a, b: a > b, '<': lambda a, b: a < b, '≥': lambda a, b: a >= b, '≤': lambda a, b: a <= b, '=': lambda a, b: a == b}
def _parse(chain):
    toks = re.findall(r'[A-Z]|[><≥≤=]', chain); out = []
    for i in range(1, len(toks), 2): out.append((toks[i - 1], toks[i], toks[i + 1]))
    return out
def ineq(statements, c1, c2, vals=range(5)):
    """Return 'Only I', 'Only II', 'Either', 'Neither' or 'Both' by enumerating every integer model."""
    cons = [c for ch in statements.split(',') for c in _parse(ch)]
    vs = sorted({x for c in cons for x in (c[0], c[2])} | set(re.findall(r'[A-Z]', c1 + c2)))
    t1 = t2 = True; either = True; n = 0
    for combo in itertools.product(vals, repeat=len(vs)):
        m = dict(zip(vs, combo))
        if not all(_OPS[o](m[a], m[b]) for a, o, b in cons): continue
        n += 1
        a1 = all(_OPS[o](m[a], m[b]) for a, o, b in _parse(c1)); a2 = all(_OPS[o](m[a], m[b]) for a, o, b in _parse(c2))
        t1 &= a1; t2 &= a2; either &= (a1 != a2)
    assert n > 0
    if t1 and t2: return 'Both'
    if t1: return 'Only I'
    if t2: return 'Only II'
    same = sorted(re.findall(r'[A-Z]', c1)) == sorted(re.findall(r'[A-Z]', c2))
    return 'Either' if (either and same) else 'Neither'

# ---------- syllogisms (Venn-region models; every named class non-empty) ----------
def _models(names):
    n = len(names); regions = [r for r in itertools.product([0, 1], repeat=n) if any(r)]
    for mask in itertools.product([0, 1], repeat=len(regions)):
        live = [r for r, k in zip(regions, mask) if k]
        if all(any(r[i] for r in live) for i in range(n)): yield live
def _holds(live, names, st):
    kind, x, y = st; i, j = names.index(x), names.index(y)
    if kind == 'all': return all(r[j] for r in live if r[i])
    if kind == 'no': return not any(r[i] and r[j] for r in live)
    if kind == 'some': return any(r[i] and r[j] for r in live)
    if kind == 'somenot': return any(r[i] and not r[j] for r in live)
    raise ValueError(kind)
def syllo(names, statements, conclusions):
    """conclusions: list of (mode, stmt) with mode 'def' (definitely true) or 'pos' (a possibility).
    Returns per-conclusion truth list and an 'either' flag for the first two conclusions."""
    ms = [m for m in _models(names) if all(_holds(m, names, s) for s in statements)]
    assert ms
    res = []
    for mode, st in conclusions:
        res.append(all(_holds(m, names, st) for m in ms) if mode == 'def' else any(_holds(m, names, st) for m in ms))
    either = (not res[0] and not res[1] and all(_holds(m, names, conclusions[0][1]) != _holds(m, names, conclusions[1][1]) for m in ms))
    return res, either
def verdict(res, either):
    if either: return 'Either'
    return {(True, True): 'Both', (True, False): 'Only I', (False, True): 'Only II', (False, False): 'Neither'}[tuple(res[:2])]

# ---------- family trees ----------
class Fam:
    def __init__(self): self.g = {}; self.par = {}; self.sp = {}
    def p(self, name, g): self.g[name] = g; self.par.setdefault(name, set()); return self
    def child(self, parent, c): self.par[c].add(parent); return self
    def marry(self, a, b): self.sp[a] = b; self.sp[b] = a; return self
    def parents(self, x): return self.par.get(x, set())
    def children(self, x): return {c for c, ps in self.par.items() if x in ps}
    def sibs(self, x): return {y for y in self.g if y != x and self.parents(x) & self.parents(y)}
    def rel(self, a, b):
        """What a is to b."""
        m = self.g[a] == 'M'; T = lambda mt, ft: mt if m else ft
        if self.sp.get(b) == a: return T('Husband', 'Wife')
        if a in self.parents(b): return T('Father', 'Mother')
        if b in self.parents(a): return T('Son', 'Daughter')
        if a in self.sibs(b): return T('Brother', 'Sister')
        gp = {g for p in self.parents(b) for g in self.parents(p)}
        if a in gp: return T('Grandfather', 'Grandmother')
        if a in {g for x in gp for g in self.parents(x)}: return T('Great-grandfather', 'Great-grandmother')
        gc = {g for c in self.children(b) for g in self.children(c)}
        if a in gc: return T('Grandson', 'Granddaughter')
        if a in {self.sp.get(g) for g in gc}: return T('Grandson-in-law', 'Granddaughter-in-law')
        ps_sibs = {s for p in self.parents(b) for s in self.sibs(p)}
        if a in ps_sibs or a in {self.sp.get(s) for s in ps_sibs}: return T('Uncle', 'Aunt')
        if a in {c for s in self.sibs(b) for c in self.children(s)}: return T('Nephew', 'Niece')
        if a in {c for s in ps_sibs for c in self.children(s)}: return 'Cousin'
        sb = self.sp.get(b)
        if sb and a in self.parents(sb): return T('Father-in-law', 'Mother-in-law')
        if (sb and a in self.sibs(sb)) or a in {self.sp.get(s) for s in self.sibs(b)}: return T('Brother-in-law', 'Sister-in-law')
        if a in {self.sp.get(c) for c in self.children(b)}: return T('Son-in-law', 'Daughter-in-law')
        return None
