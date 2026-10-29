"""Writes tools/cat/packs/practice-b16.varc.json from the verified generator b16_varc.py (six original RC passages + VA items).
Run: /workspace/.venv-edu/bin/python tools/cat/gen_practice_b16.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b16_varc
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b16_varc.build(B)
qs = []
for i, q in enumerate(B.qs["varc"], 1):
    q = dict(q); q["id"] = f"B16V-{i:02d}"; qs.append(q)
sets = {k: v for k, v in B.sets.items() if any(q.get("set") == k for q in qs)}
json.dump({"name": "practice-b16 — VARC", "sets": sets, "questions": qs}, open(os.path.join(D, "practice-b16.varc.json"), "w"), ensure_ascii=False, indent=1)
print("varc", len(qs), "items,", len(sets), "sets")
