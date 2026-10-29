"""Writes tools/cat/packs/practice-b2.{qa,dilr}.json from the verified generators b2_qa.py and b2_dilr.py.
Run: /workspace/.venv-edu/bin/python tools/cat/gen_practice_b2.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Bank
import b2_qa, b2_dilr
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
B = Bank(); b2_qa.build(B); b2_dilr.build(B)
pre = {"qa": "B2Q", "dilr": "B2D", "varc": "B2V"}
for sec in ("qa", "dilr"):
    qs = []
    for i, q in enumerate(B.qs[sec], 1):
        q = dict(q); q["id"] = f"{pre[sec]}-{i:02d}"; qs.append(q)
    sets = {k: v for k, v in B.sets.items() if any(q.get("set") == k for q in qs)}
    json.dump({"name": f"practice-b2 — {sec.upper()}", "sets": sets, "questions": qs}, open(os.path.join(D, f"practice-b2.{sec}.json"), "w"), ensure_ascii=False, indent=1)
    print(sec, len(qs), "items,", len(sets), "sets")
