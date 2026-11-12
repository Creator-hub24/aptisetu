"""Writes tools/cat/packs/practice-z1.qa.json from the verified generator b22_qa.py.
Run: /workspace/.venv-edu/bin/python tools/cat/gen_practice_z1_qa.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b22_qa
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b22_qa.build(B)
qs = []
for i, q in enumerate(B.qs["qa"], 1):
    q = dict(q); q["id"] = f"Z1Q-{i:02d}"; qs.append(q)
json.dump({"name": "practice-z1 — QA", "sets": {}, "questions": qs}, open(os.path.join(D, "practice-z1.qa.json"), "w"), ensure_ascii=False, indent=1)
print("qa", len(qs), "items")
