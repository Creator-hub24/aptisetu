"""Fixed CAT packs: full mocks, sectionals and practice sets, stored as JSON in tools/cat/packs/<pack>.<section>.json.
Each item is appended to the bank with a "pack" field. Packed items keep their own ids and difficulty tags. They
are left out of the random sectionals and the levelled practice sets, so existing content is unchanged.
Items whose pack starts with "practice-" also appear in topic practice. Every item is re-validated here.
The answers were generated and verified upstream: QA by an independent check per item, DILR sets by
brute-force solving, and VARC by a blind second read."""
import json, os, re, glob
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packs")
PACKS = []   # (pack, section) in load order

def words(html): return len(re.sub(r"<[^>]+>", " ", html).split())

def build(CB):
    seen = {q["id"] for v in CB.qs.values() for q in v}
    for f in sorted(glob.glob(os.path.join(D, "*.json"))):
        pack, sec = os.path.basename(f)[:-5].rsplit(".", 1)
        d = json.load(open(f)); PACKS.append((pack, sec))
        for sid, s in d["sets"].items():
            assert s["kind"] in ("passage", "dilr"), sid
            if s["kind"] == "passage": assert 400 <= words(s["html"]) <= 620, (sid, words(s["html"]))
            CB.add_set(sid, s["kind"], s["title"], s["html"])
        for q in d["questions"]:
            assert q["id"] not in seen, q["id"]; seen.add(q["id"])
            assert q["section"] == sec and q["exam"] == "cat" and q["difficulty"] in ("Easy", "Medium", "Hard"), q["id"]
            assert len(q["solution"]) > 20 and q["question"], q["id"]
            if q.get("set"): assert q["set"] in d["sets"], q["id"]
            if q["type"] == "mcq":
                assert len(q["options"]) == 4 and len(set(map(str, q["options"]))) == 4 and 0 <= q["answer"] < 4, q["id"]
            else:
                assert q["type"] == "tita" and q["kind"] in ("number", "sequence"), q["id"]
                if q["kind"] == "sequence":
                    assert sorted(q["answer"]) == [str(i) for i in range(1, len(q["answer"]) + 1)], q["id"]
                else: float(q["answer"])
            q = {k: v for k, v in q.items() if k not in ("level", "practiceSet")}
            q["pack"] = pack; CB.qs[sec].append(q)
