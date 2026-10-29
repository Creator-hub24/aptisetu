"""Writes tools/cat/packs/practice-b21.qa.json from the verified generator b21_qa.py.
Run: /workspace/.venv-edu/bin/python tools/cat/gen_practice_b21.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b21_qa
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b21_qa.build(B)
qs = []
for i, q in enumerate(B.qs["qa"], 1):
    q = dict(q); q["id"] = f"B21Q-{i:02d}"; qs.append(q)
json.dump({"name": "practice-b21 — QA", "sets": {}, "questions": qs}, open(os.path.join(D, "practice-b21.qa.json"), "w"), ensure_ascii=False, indent=1)
print("qa", len(qs), "items")
