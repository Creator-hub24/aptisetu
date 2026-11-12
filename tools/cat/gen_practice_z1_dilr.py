"""Writes tools/cat/packs/practice-z1.dilr.json from the verified generator b22_dilr.py (needs ortools:
python3 -m venv .venv-qb && .venv-qb/bin/pip install ortools). The pack name sorts after every existing practice pack,
so the levelled sets that already exist keep their exact content.
Run: .venv-qb/bin/python tools/cat/gen_practice_z1_dilr.py"""
import json, os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b22_dilr
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b22_dilr.build(B)
pos = iter([2, 0, 3, 1] * 60)
qs = []
for i, q in enumerate(B.qs["dilr"], 1):
    q = dict(q); q["id"] = f"Z1D-{i:03d}"
    if q["type"] == "mcq":   # balance the position of the correct option (deterministic)
        o = list(q["options"]); c = q["answer"]; t = next(pos); o[c], o[t] = o[t], o[c]; corr = o[t]
        if all(re.fullmatch(r"\d+", v) for v in o): o.sort(key=int)
        q["options"], q["answer"] = o, o.index(corr)
    qs.append(q)
json.dump({"name": "practice-z1 — DILR", "sets": B.sets, "questions": qs}, open(os.path.join(D, "practice-z1.dilr.json"), "w"), ensure_ascii=False, indent=1)
print("dilr", len(qs), "items,", len(B.sets), "sets")
