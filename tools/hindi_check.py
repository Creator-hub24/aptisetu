"""Check data/hi/general-solutions.json against the English Bank/SSC solutions.
Every question must have a Hindi solution, it must contain Devanagari, and the numbers in it
(digits, decimals, comma groups, superscript powers) must be exactly the same multiset as in the English solution."""
import json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')
nums = lambda s: sorted(re.findall(r'\d+(?:[.,]\d+)*', re.sub(r'<[^>]+>', '', s).translate(SUP)))
hi = json.load(open(os.path.join(ROOT, 'data/hi/general-solutions.json'), encoding='utf8'))
bad, n = [], 0
for sec in ('quant', 'reasoning', 'dilr'):
    for q in json.load(open(os.path.join(ROOT, f'data/general/{sec}.json'), encoding='utf8'))['questions']:
        n += 1; h = hi.get(q['id'])
        if not h: bad.append(f"{q['id']}: no Hindi solution"); continue
        if not re.search('[\u0900-\u097F]', h) and re.search(r'\b[a-z]{3,}\b', q['solution']): bad.append(f"{q['id']}: no Devanagari")
        if nums(q['solution']) != nums(h): bad.append(f"{q['id']}: numbers differ {nums(q['solution'])} vs {nums(h)}")
extra = set(hi) - {q['id'] for s in ('quant','reasoning','dilr') for q in json.load(open(os.path.join(ROOT, f'data/general/{s}.json')))['questions']}
if extra: bad.append(f"unknown ids: {sorted(extra)}")
print("\n".join(bad) if bad else f"hindi checks ok ({n} solutions, numbers identical)")
sys.exit(1 if bad else 0)
