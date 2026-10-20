"""Assigns CAT practice sets deterministically (no randomness). Run from build_questions.py.

Rules
- Level of a single question = its difficulty (Easy / Medium / Hard).
- A passage (VARC) or data set (DILR) takes the majority level of its questions; a tie goes to the harder level.
  Groups are never split.
- A practice set has exactly 10 questions. Set numbers: Easy 1-5, Medium 6-10, Hard 11-15.
- QA and VARC: groups are packed in bank order; a group that does not fit the current set waits for the next one.
  A set is "ready" only when it reaches exactly 10 questions; leftovers stay out of the set system.
- DILR: a set is exactly 2 data sets of 5 questions; data sets with 4 questions do not qualify.
Each question gets "level"; questions in a ready set also get "practiceSet" (int).
Writes data/cat/sets.json: the ready sets per section and level.
"""
import json, os
LEVELS = ("Easy", "Medium", "Hard"); START = {"Easy": 1, "Medium": 6, "Hard": 11}; PER_LEVEL = 5; SIZE = 10
RANK = {l: i for i, l in enumerate(LEVELS)}

def group_level(qs):
    c = {l: sum(q["difficulty"] == l for q in qs) for l in LEVELS}
    top = max(c.values())
    return max((l for l in LEVELS if c[l] == top), key=RANK.get)   # tie -> harder

def groups(questions):
    out, idx = [], {}
    for q in questions:
        k = q.get("set") or q["id"]
        if k not in idx: idx[k] = len(out); out.append([])
        out[idx[k]].append(q)
    return out

def pack(gs):
    """Pack groups (bank order) into sets of exactly SIZE; returns (ready_sets, leftover_groups)."""
    rest, ready = list(gs), []
    while rest and len(ready) < PER_LEVEL:
        cur, keep = [], []
        for g in rest:
            (cur if len(cur) + len(g) <= SIZE and sum(map(len, cur)) + len(g) <= SIZE else keep).append(g)
        if sum(map(len, cur)) != SIZE: break
        ready.append(cur); rest = keep
    return ready, rest

def assign(cat_out, path):
    report = {}
    for sec, s in cat_out["sections"].items():
        gs = groups(s["questions"]); rep = report[sec] = {}
        for g in gs:
            lv = group_level(g)
            for q in g: q["level"] = lv; q.pop("practiceSet", None)
        excluded = []
        for lv in LEVELS:
            pool = [g for g in gs if g[0]["level"] == lv]
            if sec == "dilr":
                excluded += [g[0]["set"] for g in pool if len(g) != 5]
                pool = [g for g in pool if len(g) == 5]
            ready, left = pack(pool)
            sets = []
            for i, st in enumerate(ready):
                n = START[lv] + i
                for g in st:
                    for q in g: q["practiceSet"] = n
                sets.append({"set": n, "ids": [q["id"] for g in st for q in g],
                             "groups": [g[0]["set"] for g in st if g[0].get("set")]})
            rep[lv] = {"ready": sets, "leftoverQuestions": sum(map(len, left))}
        if sec == "dilr": rep["excludedDataSets"] = excluded
    out = {"size": SIZE, "levels": {l: [START[l], START[l] + PER_LEVEL - 1] for l in LEVELS},
           "timers": {"qa": 20, "varc": 20, "dilr": 25}, "sections": report}
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
    for sec, rep in report.items():
        print("SETS", sec, {lv: [x["set"] for x in rep[lv]["ready"]] for lv in LEVELS},
              "leftover", {lv: rep[lv]["leftoverQuestions"] for lv in LEVELS}, rep.get("excludedDataSets", ""))
    return out
