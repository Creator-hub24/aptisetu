"""Shared helpers for the CAT bank. Every add() call validates the item."""
import math, re
from fractions import Fraction as F

def close(a, b): return abs(float(a) - float(b)) < 1e-9

class Bank:
    def __init__(self):
        self.qs = {"qa": [], "dilr": [], "varc": []}
        self.sets = {}      # id -> {kind, title, html}
    def _base(self, sec, topic, diff, text, solution, set_id):
        assert diff in ("Medium", "Hard"), diff
        assert solution and len(solution) > 20, text
        if set_id: assert set_id in self.sets, set_id
        q = dict(id=f"C{sec[0].upper()}{len(self.qs[sec])+1}", exam="cat", section=sec, topic=topic,
                 difficulty=diff, question=text, solution=solution)
        if set_id: q["set"] = set_id
        return q
    def add_set(self, sid, kind, title, html):
        assert sid not in self.sets
        self.sets[sid] = dict(kind=kind, title=title, html=html)
    def mcq(self, sec, topic, diff, text, options, correct, solution, set_id=None, chk=None, fixed=False):
        assert len(options) == 4 and len(set(options)) == 4, (text, options)
        assert options.count(correct) == 1, (text, correct)
        if chk is not None: assert close(*chk), (text, chk)
        q = self._base(sec, topic, diff, text, solution, set_id)
        q.update(type="mcq", options=options, answer=options.index(correct))
        if fixed: q["fixed"] = True
        self.qs[sec].append(q)
    def tita(self, sec, topic, diff, text, answer, solution, kind="number", set_id=None, chk=None):
        q = self._base(sec, topic, diff, text, solution, set_id)
        if kind == "number":
            assert isinstance(answer, (int, F)) or float(answer).is_integer(), answer
            if chk is not None: assert close(*chk) and close(answer, chk[1]), (text, answer, chk)
            ans = str(int(answer)) if float(answer).is_integer() else str(answer)
        elif kind == "sequence":
            assert re.fullmatch(r"\d+", answer) and sorted(answer) == [str(i) for i in range(1, len(answer)+1)], answer
            ans = answer
        elif kind == "digit":   # odd-sentence-out: a single sentence number
            assert re.fullmatch(r"[1-5]", answer); ans = answer; kind = "number"
        q.update(type="tita", kind=kind, answer=ans)
        self.qs[sec].append(q)
