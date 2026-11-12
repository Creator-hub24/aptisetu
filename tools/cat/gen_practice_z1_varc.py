"""Writes tools/cat/packs/practice-z1.varc.json from b22_varc.py (original passages and verbal items).
Run: python3 tools/cat/gen_practice_z1_varc.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b22_varc
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b22_varc.build(B)
qs = []
for i, q in enumerate(B.qs["varc"], 1):
    q = dict(q); q["id"] = f"Z1V-{i:02d}"; qs.append(q)
json.dump({"name": "practice-z1 — VARC", "sets": B.sets, "questions": qs}, open(os.path.join(D, "practice-z1.varc.json"), "w"), ensure_ascii=False, indent=1)
print("varc", len(qs), "items,", len(B.sets), "passages")
