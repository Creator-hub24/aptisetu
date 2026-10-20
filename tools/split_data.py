# Splits the generated banks into per-section files so a page loads only what it needs,
# and writes data/stats.json (all counts shown on the site). Run automatically at the end
# of build_questions.py; never edit the generated files by hand.
import os, json
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
def load(n): return json.load(open(os.path.join(D, n)))
def dump(obj, *parts):
    p = os.path.join(D, *parts); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, "w"), ensure_ascii=False, separators=(",", ":"))
def main():
    gen, cat, cuet = load("questions.json"), load("cat.json"), load("cuet.json")
    st = {"stat": {}, "topic": {}, "catTopic": {}, "cuetTopic": {}, "cuetPart": {}}
    S = st["stat"]
    for k, s in gen.items():
        dump(s, "general", k + ".json"); S[k] = len(s["questions"])
        for q in s["questions"]: st["topic"][q["topic"]] = st["topic"].get(q["topic"], 0) + 1
    S["general"] = sum(len(s["questions"]) for s in gen.values())
    for name, bank in (("cat", cat), ("cuet", cuet)):
        for k, s in bank["sections"].items():
            used = {q["set"] for q in s["questions"] if q.get("set")}
            dump({"name": s["name"], "questions": s["questions"], "sets": {i: bank["sets"][i] for i in used}}, name, k + ".json")
            S[f"{name}-{k}"] = len(s["questions"])
    cq = [(k, q) for k, s in cat["sections"].items() for q in s["questions"]]
    S["cat"] = len(cq); S["cat-tita"] = sum(q["type"] == "tita" for _, q in cq); S["cat-mcq"] = sum(q["type"] == "mcq" for _, q in cq)
    S["cat-topics"] = len({(k, q["topic"]) for k, q in cq})
    S["cat-sets"] = sum(1 for s in cat["sets"].values() if s["kind"] == "dilr"); S["cat-passages"] = sum(1 for s in cat["sets"].values() if s["kind"] == "passage")
    for k, q in cq: key = k + "|" + q["topic"]; st["catTopic"][key] = st["catTopic"].get(key, 0) + 1
    uq = [(k, q) for k, s in cuet["sections"].items() for q in s["questions"]]
    shared = [1 for _, q in uq if q.get("source") == "general"]
    S["cuet"] = len(uq); S["cuet-shared"] = len(shared); S["cuet-original"] = len(uq) - len(shared)
    for k, q in uq:
        a = f"{k}|{q['part']}"; b = f"{a}|{q['topic']}"
        st["cuetPart"][a] = st["cuetPart"].get(a, 0) + 1; st["cuetTopic"][b] = st["cuetTopic"].get(b, 0) + 1
    S["questions"] = S["general"] + S["cat"] + S["cuet-original"]
    S["topics"] = len({(k, q["topic"]) for k, s in gen.items() for q in s["questions"]}) + S["cat-topics"] + len(st["cuetTopic"])
    dump(st, "stats.json")
    print("split ok:", {k: S[k] for k in ("general", "cat", "cuet", "questions", "topics")})
if __name__ == "__main__": main()
