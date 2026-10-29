"""Writes tools/cat/packs/practice-b9.qa.json from the verified generator b9_qa.py.
Run: /workspace/.venv-edu/bin/python tools/cat/gen_practice_b9.py"""
import json, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b9_qa
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b9_qa.build(B)
# Dropped after dedupe review against the whole bank: exact repeats (19, 29, 35) and
# same-template items that differ only in numbers (7, 9, 15, 16, 18, 20, 23, 24, 27, 28, 31, 33, 37, 38).
DROP = {7, 9, 15, 16, 18, 19, 20, 23, 24, 27, 28, 29, 31, 33, 35, 37, 38}
pos = iter([2, 0, 3, 1] * 20)
qs = []
kept = [q for i, q in enumerate(B.qs["qa"], 1) if i not in DROP]
for i, q in enumerate(kept, 1):
    q = dict(q); q["id"] = f"B9Q-{i:02d}"
    if q["type"] == "mcq":   # balance the position of the correct option (deterministic)
        o = list(q["options"]); c = q["answer"]; t = next(pos); o[c], o[t] = o[t], o[c]; q["options"], q["answer"] = o, t
    qs.append(q)
json.dump({"name": "practice-b9 — QA", "sets": {}, "questions": qs}, open(os.path.join(D, "practice-b9.qa.json"), "w"), ensure_ascii=False, indent=1)
print("qa", len(qs), "items")
