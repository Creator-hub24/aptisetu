"""Shared helpers for the CUET (UG) bank. Every add() call validates the item."""
from fractions import Fraction as F

def close(a, b): return abs(float(a) - float(b)) < 1e-9

PREFIX = {"gat": "UG", "english": "UE", "maths": "UM"}

class UBank:
    def __init__(self):
        self.qs = {k: [] for k in PREFIX}
        self.sets = {}      # id -> {kind, title, html}
    def add_set(self, sid, kind, title, html):
        assert sid not in self.sets, sid
        self.sets[sid] = dict(kind=kind, title=title, html=html)
    def mcq(self, sec, part, topic, diff, text, options, correct, solution, set_id=None, chk=None, fixed=False):
        assert diff in ("Easy", "Medium", "Hard"), diff
        assert len(options) == 4 and len(set(map(str, options))) == 4, (text, options)
        options = [str(o) for o in options]; correct = str(correct)
        assert options.count(correct) == 1, (text, correct, options)
        assert solution and len(solution) > 15, text
        if chk is not None:
            if isinstance(chk, list):
                for c in chk: assert close(*c) if not isinstance(c[0], str) else c[0] == c[1], (text, c)
            else: assert (close(*chk) if not isinstance(chk[0], str) else chk[0] == chk[1]), (text, chk)
        if set_id: assert set_id in self.sets, set_id
        q = dict(id=f"{PREFIX[sec]}{len(self.qs[sec])+1}", exam="cuet", section=sec, part=part, topic=topic,
                 difficulty=diff, question=text, solution=solution, type="mcq", options=options, answer=options.index(correct))
        if set_id: q["set"] = set_id
        if fixed: q["fixed"] = True
        self.qs[sec].append(q)
        return q
