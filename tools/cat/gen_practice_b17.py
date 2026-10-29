"""Writes tools/cat/packs/practice-b17.qa.json from the verified generator b17_qa.py.
Run: /workspace/.venv-edu/bin/python tools/cat/gen_practice_b17.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b17_qa
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b17_qa.build(B)
qs = []
for i, q in enumerate(B.qs["qa"], 1):
    q = dict(q); q["id"] = f"B17Q-{i:02d}"; qs.append(q)
json.dump({"name": "practice-b17 — QA", "sets": {}, "questions": qs}, open(os.path.join(D, "practice-b17.qa.json"), "w"), ensure_ascii=False, indent=1)
print("qa", len(qs), "items")
