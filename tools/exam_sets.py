"""Practice sets for CUET (UG), Bank and SSC, built ONLY from questions already in the banks (no new questions).
Run by tools/build_pages.py (deterministic, no randomness); writes data/sets/{cuet,bank,ssc}.json.
CAT sets are separate (tools/assign_levels.py -> data/cat/sets.json) and are not touched here.

Rules (same idea as the CAT sets)
- Level of a question = its existing difficulty tag. A passage / data set is never split and takes the majority
  level of its questions (a tie goes to the harder level).
- A set has exactly SIZE questions; a level gets as many complete sets as its pool allows (up to its slots).
  Empty slots are shown as "Coming soon". Groups are packed in topic round-robin order so each set mixes topics.
- Each question is in at most one set ACROSS ALL EXAMS:
  * CUET General Aptitude uses only questions written for CUET (source != "general"). The GAT items reused from
    the Bank/SSC bank (source "general") stay in the random GAT sectional and topic practice only.
  * Bank and SSC share the general bank, so it is split between them: Bank-only topics (e.g. seating, puzzles,
    inequalities, P&C, probability), SSC-only topics (e.g. geometry, algebra, odd one out, series, clocks), and the
    rest is shared out level by level so that the two exams get the most complete sets (evenly when it is a tie).
Marking and timers come from the official notices (see SOURCES); they are written into the JSON for the site.
"""
import json, os
LEVELS = ("Easy", "Medium", "Hard"); RANK = {l: i for i, l in enumerate(LEVELS)}
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

SOURCES = {
    "cuet": "NTA CUET (UG) 2026 Information Bulletin, 2.3 and 12.1: 50 compulsory questions per paper in 60 minutes; +5 correct, -1 wrong, 0 unanswered (https://cuet.nta.nic.in/information-bulletin/)",
    "bank": "IBPS CRP PO/MT-XVI notification (2026), Preliminary exam: Quantitative Aptitude 35 questions and Reasoning Ability 35 questions, 20 minutes each (separately timed); one fourth of the marks of a question deducted for a wrong answer (https://www.ibps.in/)",
    "ssc": "SSC CGL 2026 notice, para 13.8: Tier-I 25 questions per section, 2 marks each, sectional timer of 15 minutes, 0.50 marks deducted per wrong answer; SSC CHSL 2025 notice, para 13.7: 25 questions / 50 marks per part, 0.50 negative (https://ssc.gov.in/)",
}
# exam -> label, marking [correct, wrong], sections
EXAMS = {
    "cuet": {"label": "CUET (UG)", "marks": [5, -1], "sections": {
        # Half a paper at the official pace (50 questions in 60 minutes = 72 s per question)
        "gat": {"name": "General Aptitude Test", "src": "cuet/gat", "size": 25, "timer": 30, "order": "part"},
        "english": {"name": "English", "src": "cuet/english", "size": 25, "timer": 30, "order": "topic"},
        "maths": {"name": "Mathematics", "src": "cuet/maths", "size": 25, "timer": 30, "order": "topic"}}},
    "bank": {"label": "Bank", "marks": [1, -0.25], "sections": {
        # A prelims sectional: 35 questions in 20 minutes
        "quant": {"name": "Quantitative Aptitude", "src": "general/quant", "size": 35, "timer": 20, "order": "topic"},
        "reasoning": {"name": "Reasoning Ability", "src": "general/reasoning", "size": 35, "timer": 20, "order": "topic"},
        # DI is part of the prelims Quant section; a DI set is 2 whole data sets at the same pace (20 min / 35 questions)
        "di": {"name": "Data Interpretation", "src": "general/dilr", "size": 10, "timer": 6, "order": "topic"}}},
    "ssc": {"label": "SSC", "marks": [2, -0.5], "sections": {
        # One Tier-I section: 25 questions with a 15-minute sectional timer
        "maths": {"name": "Quantitative Aptitude", "src": "general/quant", "size": 25, "timer": 15, "order": "topic"},
        "reasoning": {"name": "General Intelligence & Reasoning", "src": "general/reasoning", "size": 25, "timer": 15, "order": "topic"}}},
}
SLOTS = 3            # minimum slots per level (a level with more complete sets gets more slots)
BANK_ONLY = {"quant": {"Permutations & Combinations", "Probability"},
             "reasoning": {"Seating Arrangement", "Puzzles", "Inequalities"}}
SSC_ONLY = {"quant": {"Geometry & Mensuration", "Algebra"},
            "reasoning": {"Odd One Out", "Number & Letter Series", "Clocks & Calendars", "Alphabet Test"}}
DI_TOPICS = {"Tables", "Bar Charts", "Pie Charts", "Line Graphs", "Caselets"}
PAIR = {"quant": ("quant", "maths"), "reasoning": ("reasoning", "reasoning")}   # general file -> (bank sec, ssc sec)

def load(src): return json.load(open(os.path.join(ROOT, "data", src + ".json")))["questions"]
def groups(qs):
    out, idx = [], {}
    for q in qs:
        k = q.get("set") or q["id"]
        if k not in idx: idx[k] = len(out); out.append([])
        out[idx[k]].append(q)
    return out
def glevel(g):
    c = {l: sum(q["difficulty"] == l for q in g) for l in LEVELS}; top = max(c.values())
    return max((l for l in LEVELS if c[l] == top), key=RANK.get)
def rr(gs, key):
    """Round-robin over key (in order of first appearance), bank order inside each key. Deterministic."""
    by, order = {}, []
    for g in gs:
        k = key(g[0])
        if k not in by: by[k] = []; order.append(k)
        by[k].append(g)
    out = []
    while any(by.values()):
        for k in order:
            if by[k]: out.append(by[k].pop(0))
    return out
def pack(gs, size):
    """Sets of exactly `size` questions from whole groups, earliest groups first (small exact subset search)."""
    rest, ready = list(gs), []
    while True:
        pick = []
        def dfs(i, tot):
            if tot == size: return True
            for j in range(i, len(rest)):
                n = len(rest[j])
                if tot + n <= size:
                    pick.append(j)
                    if dfs(j + 1, tot + n): return True
                    pick.pop()
                    if n == 1: return False   # singles: if the earliest single does not complete it, later ones won't either
            return False
        if sum(map(len, rest)) < size or not dfs(0, 0): break
        ready.append([rest[j] for j in pick]); rest = [g for j, g in enumerate(rest) if j not in set(pick)]
    return ready, rest
def interleave(items, k):
    """Choose k of the items, spread evenly through the list (Bresenham). Returns (chosen, others)."""
    s = len(items); a, b = [], []
    for i, x in enumerate(items):
        (a if (i + 1) * k // s > i * k // s else b).append(x)
    return a, b

def split_general(fname, qs):
    """Split one general file between Bank and SSC, per level. Returns {bank_sec: {L: [groups]}, ssc_sec: {...}}."""
    bsec, ssec = PAIR[fname]; bsz = EXAMS["bank"]["sections"][bsec]["size"]; ssz = EXAMS["ssc"]["sections"][ssec]["size"]
    out = {"bank": {}, "ssc": {}}
    for L in LEVELS:
        lv = [q for q in qs if q["difficulty"] == L]
        b = [q for q in lv if q["topic"] in BANK_ONLY[fname]]; s = [q for q in lv if q["topic"] in SSC_ONLY[fname]]
        sh = rr([[q] for q in lv if q["topic"] not in BANK_ONLY[fname] | SSC_ONLY[fname]], lambda q: q["topic"])
        best = max(range(len(sh) + 1), key=lambda k: ((len(b) + k) // bsz + (len(s) + len(sh) - k) // ssz, -abs(2 * k - len(sh))))
        tb, ts = interleave(sh, best)
        out["bank"][L] = rr([[q] for q in b], lambda q: q["topic"]) + tb
        out["ssc"][L] = rr([[q] for q in s], lambda q: q["topic"]) + ts
        out["bank"][L] = rr(out["bank"][L], lambda q: q["topic"]); out["ssc"][L] = rr(out["ssc"][L], lambda q: q["topic"])
    return out

def build(write=True):
    pools = {e: {} for e in EXAMS}   # exam -> sec -> level -> [groups] (already in packing order)
    for sec, cfg in EXAMS["cuet"]["sections"].items():
        qs = [q for q in load(cfg["src"]) if q.get("source") != "general" and not q.get("pack")]
        gs = groups(qs); key = (lambda q: q["part"]) if cfg["order"] == "part" else (lambda q: q["topic"])
        pools["cuet"][sec] = {L: rr([g for g in gs if glevel(g) == L], key) for L in LEVELS}
    for fname in ("quant", "reasoning"):
        sp = split_general(fname, load("general/" + fname))
        pools["bank"][PAIR[fname][0]] = sp["bank"]; pools["ssc"][PAIR[fname][1]] = sp["ssc"]
    di = [g for g in groups(load("general/dilr")) if g[0]["topic"] in DI_TOPICS]
    pools["bank"]["di"] = {L: rr([g for g in di if glevel(g) == L], lambda q: q["topic"]) for L in LEVELS}
    out, seen = {}, {}
    for exam, ecfg in EXAMS.items():
        secs = {}
        for sec, cfg in ecfg["sections"].items():
            rep, n0 = {"name": cfg["name"], "src": "data/" + cfg["src"] + ".json", "size": cfg["size"], "timer": cfg["timer"]}, 1
            for L in LEVELS:
                ready, left = pack(pools[exam][sec][L], cfg["size"])
                slots = max(SLOTS, len(ready)); sets = []
                for i, st in enumerate(ready):
                    # inside a set, questions of one paper part / topic sit together (as in the real papers), in bank order
                    po = {}; [po.setdefault((g[0].get("part") or ""), len(po)) for g in pools[exam][sec][L] for _ in [0]]
                    to = {}; [to.setdefault(g[0]["topic"], len(to)) for g in pools[exam][sec][L]]
                    st = sorted(st, key=lambda g: (po[g[0].get("part") or ""], to[g[0]["topic"]]))
                    ids = [q["id"] for g in st for q in g]
                    assert len(ids) == cfg["size"] == len(set(ids)), (exam, sec, L, i)
                    for qid in ids:   # at most one set across all exams (general items are keyed by file)
                        k = (cfg["src"].split("/")[0] == "general" and cfg["src"] or exam + sec, qid)
                        assert k not in seen, ("question in two sets", k, seen.get(k)); seen[k] = (exam, sec, n0 + i)
                    sets.append({"set": n0 + i, "ids": ids})
                rep[L] = {"range": [n0, n0 + slots - 1], "ready": sets, "leftoverQuestions": sum(map(len, left))}
                n0 += slots
            rep["count"] = n0 - 1
            secs[sec] = rep
        out[exam] = {"exam": exam, "label": ecfg["label"], "levels": list(LEVELS),
                     "marks": {"correct": ecfg["marks"][0], "wrong": ecfg["marks"][1], "blank": 0},
                     "source": SOURCES[exam], "sections": secs}
        if write:
            json.dump(out[exam], open(os.path.join(ROOT, "data", "sets", exam + ".json"), "w"), ensure_ascii=False, indent=1)
    # GAT reused items must never be in a GAT set; the general originals may be in a Bank/SSC set (one place only)
    return out

if __name__ == "__main__":
    for exam, d in build().items():
        for sec, r in d["sections"].items():
            print(exam, sec, {L: [x["set"] for x in r[L]["ready"]] for L in LEVELS}, "slots", r["count"],
                  "leftover", {L: r[L]["leftoverQuestions"] for L in LEVELS})
