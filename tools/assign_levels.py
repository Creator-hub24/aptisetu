"""Assigns CAT practice sets deterministically (no randomness). Run from build_questions.py.

Rules
- Level of a single question = its difficulty (Easy / Medium / Hard).
- A passage (VARC) or data set (DILR) takes the majority level of its questions; a tie goes to the harder level.
  Groups are never split.
- A practice set has exactly 10 questions. The number of set slots per level is set per section in SLOTS;
  set numbers run consecutively Easy, then Medium, then Hard (e.g. Quant: Easy 1-5, Medium 6-13, Hard 14-18).
- QA and VARC: groups are packed in bank order; a group that does not fit the current set waits for the next one.
  A set is "ready" only when it reaches exactly 10 questions; leftovers stay out of the set system (practice only).
- MIX_AFTER: questions added after the given id are packed in topic round-robin order (so each new set mixes
  topics) with NEAR_DUPLICATES last, so the earlier sets keep their exact content.
- DILR: a set is exactly 2 data sets of 5 questions; data sets with 4 questions do not qualify.
Each question gets "level"; questions in a ready set also get "practiceSet" (int).
Writes data/cat/sets.json: per section, the level ranges, the total slot count and the ready sets.
"""
import json, os
LEVELS = ("Easy", "Medium", "Hard"); SIZE = 10
RANK = {l: i for i, l in enumerate(LEVELS)}
SLOTS = {"qa": {"Easy": 5, "Medium": 8, "Hard": 5},
         "varc": {"Easy": 5, "Medium": 5, "Hard": 5},
         "dilr": {"Easy": 5, "Medium": 5, "Hard": 5}}
MIX_AFTER = {"qa": 120}            # CQ121 onwards (user's Medium sets M1/M2 extras)
NEAR_DUPLICATES = {"CQ124", "CQ129", "CQ135", "CQ142", "CQ155"}   # close to an existing question: placed last

def num(qid): return int("".join(c for c in qid if c.isdigit()))

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

def mixed(gs):
    """Topic round-robin (topics in order of first appearance), near-duplicates at the end. Deterministic."""
    near = [g for g in gs if g[0]["id"] in NEAR_DUPLICATES]; rest = [g for g in gs if g[0]["id"] not in NEAR_DUPLICATES]
    by, order = {}, []
    for g in rest:
        t = g[0]["topic"]
        if t not in by: by[t] = []; order.append(t)
        by[t].append(g)
    out = []
    while any(by.values()):
        for t in order:
            if by[t]: out.append(by[t].pop(0))
    return out + near

def pack(gs, limit):
    """Pack groups (in the given order) into sets of exactly SIZE; returns (ready_sets, leftover_groups)."""
    rest, ready = list(gs), []
    while rest and len(ready) < limit:
        cur, keep = [], []
        for g in rest:
            (cur if sum(map(len, cur)) + len(g) <= SIZE else keep).append(g)
        if sum(map(len, cur)) != SIZE: break
        ready.append(cur); rest = keep
    return ready, rest

FILL = {"varc", "dilr"}   # fill every empty slot (see fill())
# Former relative-easy fill of VARC/DILR sets 1-5, replaced by genuine Easy packs (practice-easy). Held in reserve
# (never re-used by fill()), so the filled Medium/Hard sets 6-15 keep exactly the same content.
RESERVE = {k: set(v) for k, v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cat", "level_reserve.json"))).items()
           if not k.startswith("_")}

def hardness(g): return sum(RANK[q["difficulty"]] for q in g) / len(g)

def fill(sec, questions, rep, start, slots):
    """VARC/DILR have almost no Easy-tagged content, so slots left empty by the difficulty rules above are filled
    by RELATIVE difficulty: unused non-mock groups (bank, practice-* and *-sectional packs; never mock-* packs)
    sorted easiest first (stable, bank order), packed into the empty slots in order Easy -> Medium -> Hard.
    Sets made earlier keep their exact content. DILR: 2 data sets (4 or 5 questions each), VARC: exactly 10."""
    used = {i for lv in LEVELS for st in rep[lv]["ready"] for i in st["ids"]}
    free = [g for g in groups([q for q in questions if not (q.get("pack") or "").startswith("mock-")])
            if not any(q["id"] in used or q["id"] in RESERVE.get(sec, ()) for q in g)]
    if sec == "dilr": free = [g for g in free if len(g) in (4, 5)]
    free.sort(key=hardness)
    for lv in LEVELS:
        have = {x["set"] for x in rep[lv]["ready"]}
        for n in range(start[lv], start[lv] + slots[lv]):
            if n in have or not free: continue
            if sec == "dilr":
                if len(free) < 2: break
                st = [free.pop(0), free.pop(0)]
            else:
                got, rest = pack(free, 1)
                if not got: break
                st, free = got[0], rest
            for g in st:
                for q in g: q["practiceSet"] = n
            rep[lv]["ready"].append({"set": n, "ids": [q["id"] for g in st for q in g],
                                     "groups": [g[0]["set"] for g in st if g[0].get("set")], "filled": True})
        rep[lv]["ready"].sort(key=lambda x: x["set"])

def assign(cat_out, path):
    report = {}
    for sec, s in cat_out["sections"].items():
        for q in s["questions"]:
            if q.get("pack"): q["level"] = q["difficulty"]; q.pop("practiceSet", None)   # fixed packs: own level
        # mock/sectional packs never enter levelled sets; practice-* packs fill the remaining slots (after the
        # original bank in bank order, so earlier sets keep their exact content)
        gs = groups([q for q in s["questions"] if not q.get("pack") or q["pack"].startswith("practice-")]); rep = report[sec] = {}
        slots = SLOTS[sec]; start, n0 = {}, 1
        for lv in LEVELS: start[lv] = n0; n0 += slots[lv]
        for g in gs:
            lv = group_level(g)
            for q in g: q["level"] = lv; q.pop("practiceSet", None)
        excluded = []
        for lv in LEVELS:
            pool = [g for g in gs if g[0]["level"] == lv]
            if sec == "dilr":
                excluded += [g[0]["set"] for g in pool if len(g) != 5]
                pool = [g for g in pool if len(g) == 5]
            cut = MIX_AFTER.get(sec)
            old = [g for g in pool if cut is None or num(g[0]["id"]) <= cut]
            new = [g for g in pool if cut is not None and num(g[0]["id"]) > cut]
            ready, left = pack(old, slots[lv])
            if new:
                more, left2 = pack(left + mixed(new), slots[lv] - len(ready))
                ready += more; left = left2
            sets = []
            for i, st in enumerate(ready):
                n = start[lv] + i
                for g in st:
                    for q in g: q["practiceSet"] = n
                sets.append({"set": n, "ids": [q["id"] for g in st for q in g],
                             "groups": [g[0]["set"] for g in st if g[0].get("set")]})
            rep[lv] = {"range": [start[lv], start[lv] + slots[lv] - 1], "ready": sets,
                       "leftoverQuestions": sum(map(len, left)), "leftoverIds": [q["id"] for g in left for q in g]}
        if sec in FILL: fill(sec, s["questions"], rep, start, slots)
        rep["count"] = n0 - 1
        if sec == "dilr": rep["excludedDataSets"] = excluded
        if sec in RESERVE: rep["reserveIds"] = sorted(RESERVE[sec])
    out = {"size": SIZE, "levels": list(LEVELS), "timers": {"qa": 20, "varc": 20, "dilr": 25}, "sections": report}
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
    for sec, rep in report.items():
        print("SETS", sec, rep["count"], {lv: [x["set"] for x in rep[lv]["ready"]] for lv in LEVELS},
              "leftover", {lv: rep[lv]["leftoverQuestions"] for lv in LEVELS}, rep.get("excludedDataSets", ""))
    return out
