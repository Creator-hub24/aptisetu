"""Duplicate check for a new practice pack against every CAT item already in the bank (data/cat.json) and within itself.
Compares normalised text (tags, punctuation and case removed). For items that belong to a passage or data set, the
passage/set text is compared separately. Reports exact duplicates, near-duplicates (token similarity >= 0.85) and
numbers-changed variants (identical once every number is masked). Exit code 1 if an exact or near duplicate is found.
Run: python3 tools/cat/dedup_check.py practice-z1"""
import json, re, sys, difflib, os
pack = sys.argv[1] if len(sys.argv) > 1 else "practice-z1"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
cat = json.load(open(os.path.join(ROOT, "data", "cat.json")))
def norm(s): return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", re.sub(r"<[^>]+>", " ", s.lower()))).strip()
def mask(s): return re.sub(r"\d+", "#", s)
def sim(a, b):
    ta, tb = a.split(), b.split()
    if not ta or not tb: return 0.0
    j = len(set(ta) & set(tb)) / len(set(ta) | set(tb))
    if j < 0.4: return j
    return difflib.SequenceMatcher(None, ta, tb, autojunk=False).ratio()
old, new = [], []
for sec, s in cat["sections"].items():
    for q in s["questions"]:
        (new if q.get("pack") == pack else old).append((sec, q))
def key(q):   # question text + options (set questions are compared as text + their options; the set itself separately)
    return norm(q["question"] + " " + " ".join(map(str, q.get("options", []))))
bad, variants, checked = [], [], 0
pool = old + []
for i, (sec, q) in enumerate(new):
    k = key(q); checked += 1
    for sec2, o in pool + new[:i]:
        if sec2 != sec: continue
        if q.get("set") and o.get("set") and q["set"] != o["set"]:
            continue   # generic stems inside different data sets/passages ("Who is in seat 3?") are not duplicates; sets compared below
        k2 = key(o)
        if k == k2: bad.append(("EXACT", q["id"], o["id"])); continue
        r = sim(k, k2)
        if mask(k) == mask(k2): variants.append((q["id"], o["id"]))
        elif r >= 0.85: bad.append((f"NEAR {r:.2f}", q["id"], o["id"]))
newsets = {q["set"] for _, q in new if q.get("set")}
oldsets = {k: v for k, v in cat["sets"].items() if k not in newsets}
for sid in sorted(newsets):
    h = norm(cat["sets"][sid]["html"])
    for oid, o in list(oldsets.items()) + [(x, cat["sets"][x]) for x in sorted(newsets) if x < sid]:
        r = sim(h, norm(o["html"]))
        if r >= 0.85: bad.append((f"SET NEAR {r:.2f}", sid, oid))
print(f"{pack}: {checked} new items and {len(newsets)} new passages/data sets checked against {len(old)} existing CAT items and {len(oldsets)} existing sets")
print("numbers-changed variants:", len(variants), variants[:20])
print("exact/near duplicates:", len(bad))
for b in bad: print("  ", *b)
sys.exit(1 if bad else 0)
