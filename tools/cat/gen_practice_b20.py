"""Writes tools/cat/packs/practice-b20.dilr.json from the verified generator b20_dilr.py.
Run: /workspace/.venv-edu/bin/python tools/cat/gen_practice_b20.py"""
import json, os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b20_dilr
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b20_dilr.build(B)
pos = iter([2, 0, 3, 1] * 20)
qs = []
for i, q in enumerate(B.qs["dilr"], 1):
    q = dict(q); q["id"] = f"B20D-{i:02d}"
    if q["type"] == "mcq" and not q.get("fixed"):   # balance the position of the correct option (deterministic)
        o = list(q["options"]); c = q["answer"]; t = next(pos); o[c], o[t] = o[t], o[c]
        corr = o[t]
        if all(re.fullmatch(r"\d+(\.\d+)?(/\d+)?", v) for v in o): o.sort(key=F)   # purely numeric options are listed in increasing order
        q["options"], q["answer"] = o, o.index(corr)
    qs.append(q)
json.dump({"name": "practice-b20 — DILR", "sets": B.sets, "questions": qs}, open(os.path.join(D, "practice-b20.dilr.json"), "w"), ensure_ascii=False, indent=1)
print("dilr", len(qs), "items,", len(B.sets), "sets")
