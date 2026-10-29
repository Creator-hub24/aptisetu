"""Helpers for Bank/SSC batches written after Oct 2026. Each batch module calls add() for every item: the correct option
is swapped to a balanced, deterministic position (standard answer sets and 'Cannot/None/Neither...' sets keep their order),
the item goes through build_questions.Q() (4 distinct options, exactly one correct, chk recomputed), and the Hindi solution
must carry exactly the same numbers as the English one (the same rule tools/hindi_check.py enforces)."""
import re, random, numbers
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')
def nums(s): return sorted(re.findall(r'\d+(?:[.,]\d+)*', re.sub(r'<[^>]+>', '', s).translate(SUP)))

class Adder:
    def __init__(self, Q, OUT, SY, SYE, seed):
        self.Q, self.OUT, self.fixed_sets = Q, OUT, (SY, SYE)
        pos = [t for _ in range(80) for t in range(4)]; random.Random(seed).shuffle(pos); self.pos = iter(pos)
        self.hi = {}
    def __call__(self, sec, topic, diff, text, options, correct, solution, hi, chk=None, data=None, set_id=None):
        options = [str(o) for o in options]; correct = str(correct)
        assert options.count(correct) == 1, (text, correct, options)
        if options not in self.fixed_sets and not any(o.startswith(("Cannot", "No ", "None", "Neither")) for o in options) and options != ["None", "One", "Two", "Three"]:
            t = next(self.pos); c = options.index(correct); options[c], options[t] = options[t], options[c]
        assert re.search('[\u0900-\u097F]', hi), hi
        assert nums(solution) == nums(hi), (text[:60], nums(solution), nums(hi))
        if chk is not None and not all(isinstance(x, numbers.Real) for x in chk):
            assert chk[0] == chk[1], (text[:60], chk); chk = None  # non-numeric answer (letter/word/tuple): exact match checked here
        self.Q(sec, topic, diff, text, options, correct, solution, data=data, set_id=set_id, chk=chk)
        qid = self.OUT[sec][-1]["id"]; assert qid not in self.hi; self.hi[qid] = hi
        return qid
