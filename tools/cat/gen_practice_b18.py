"""Writes tools/cat/packs/practice-b18.qa.json from the verified generator b18_qa.py.
Run: /workspace/.venv-edu/bin/python tools/cat/gen_practice_b18.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b18_qa
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b18_qa.build(B)
qs = []
for i, q in enumerate(B.qs["qa"], 1):
    q = dict(q); q["id"] = f"B18Q-{i:02d}"; qs.append(q)
json.dump({"name": "practice-b18 — QA", "sets": {}, "questions": qs}, open(os.path.join(D, "practice-b18.qa.json"), "w"), ensure_ascii=False, indent=1)
print("qa", len(qs), "items")
