/* Independent ranking solver: arithmetic re-derivations and brute-force permutations of comparison clues. */
const ordN = s => +String(s).replace(/\D/g, '');
const ord = n => n + (n % 100 >= 11 && n % 100 <= 13 ? 'th' : ['th', 'st', 'nd', 'rd'][n % 10] || 'th');
function perms(a) { if (a.length <= 1) return [a]; return a.flatMap((x, i) => perms(a.slice(0, i).concat(a.slice(i + 1))).map(r => [x].concat(r))); }
function compare(p) { const q = p.question; const names = q.match(/\(([^)]+)\)/)[1].split(', ');
  const ADJ = { taller: 'shorter', older: 'younger', heavier: 'lighter', richer: 'poorer' }; const SUP = { taller: 'tallest', older: 'oldest', heavier: 'heaviest', richer: 'richest' }, SUPLO = { taller: 'shortest', older: 'youngest', heavier: 'lightest', richer: 'poorest' };
  const hi = Object.keys(ADJ).find(a => q.includes(' ' + a + ' ') || q.includes(SUP[a]) || q.includes(ADJ[a]) || q.includes(SUPLO[a])); const lo = ADJ[hi];
  const tests = []; // each test: order (index 0 = most) => bool
  const r = (o, x) => o.indexOf(x);
  for (const c of p.clues) { let m;
    if ((m = c.match(new RegExp(`^(\\w+) is ${hi} than (\\w+) but ${lo} than (\\w+)\\.$`)))) { const [, a, b, d] = m; tests.push(o => r(o, a) < r(o, b) && r(o, d) < r(o, a)); }
    else if ((m = c.match(new RegExp(`^(\\w+) is ${hi} than (\\w+)\\.$`)))) { const [, a, b] = m; tests.push(o => r(o, a) < r(o, b)); }
    else if ((m = c.match(new RegExp(`^(\\w+) is ${lo} than (\\w+)\\.$`)))) { const [, a, b] = m; tests.push(o => r(o, a) > r(o, b)); }
    else if ((m = c.match(new RegExp(`^(\\w+) is the ${SUP[hi]}\\.$`)))) { const a = m[1]; tests.push(o => r(o, a) === 0); }
    else if ((m = c.match(new RegExp(`^(\\w+) is the ${SUPLO[hi]}\\.$`)))) { const a = m[1]; tests.push(o => r(o, a) === o.length - 1); }
    else if ((m = c.match(new RegExp(`^(\\w+) is not the ${SUP[hi]}\\.$`)))) { const a = m[1]; tests.push(o => r(o, a) !== 0); }
    else if ((m = c.match(new RegExp(`^(\\w+) is not the ${SUPLO[hi]}\\.$`)))) { const a = m[1]; tests.push(o => r(o, a) !== o.length - 1); }
    else throw new Error('clue? ' + c); }
  const S = perms(names).filter(o => tests.every(t => t(o))); if (!S.length) throw new Error('no order');
  let m; const outs = new Set();
  if ((m = q.match(new RegExp(`Who is the (?:(\\d+)\\w\\w )?${SUP[hi]}\\?`)))) { const k = m[1] ? +m[1] - 1 : 0; S.forEach(o => outs.add(o[k])); }
  else if ((m = q.match(new RegExp(`How many friends are ${hi} than (\\w+)\\?`)))) S.forEach(o => outs.add(String(r(o, m[1]))));
  else throw new Error('ask?');
  if (outs.size !== 1) throw new Error('answer not unique'); return [...outs][0]; }
module.exports = {
  'rank-e1': p => { const m = p.question.match(/stands (\d+)\w\w; counting from the \w+, \w+ stands (\d+)\w\w/); return String(+m[1] + +m[2] - 1); },
  'rank-e2': p => { const m = p.question.match(/row of (\d+) \w+, \w+ is (\d+)\w\w from the left/); return ord(+m[1] - +m[2] + 1); },
  'rank-m1': p => { const m = p.question.match(/row of (\d+) \w+, \w+ is (\d+)\w\w from the left and \w+ is (\d+)\w\w from the right/); const N = +m[1], a = +m[2], b = N - +m[3] + 1;
    if (a === b) throw new Error('same'); return String(Math.abs(a - b) - 1); },
  'rank-m2': p => { const m = p.question.match(/(\w+) is (\d+)\w\w from the left and (\w+) is (\d+)\w\w from the right\. When they swap places, \1 becomes (\d+)\w\w from the left/);
    // brute N: B's position from left = N - bR + 1 must equal the new position of A
    const sols = []; for (let N = 2; N < 300; N++) { const bL = N - +m[4] + 1; if (bL === +m[5] && +m[2] <= N && bL >= 1 && bL !== +m[2]) sols.push(N); } if (sols.length !== 1) throw new Error('N'); return String(sols[0]); },
  'rank-h1': p => { const m = p.question.match(/(\w+) is (\d+)\w\w from the front and (\w+) is (\d+)\w\w from the back\. Exactly (\d+) people/); const f = +m[2], b = +m[4], k = +m[5];
    for (let N = 2; N < 300; N++) { const pb = N - b + 1; if (pb < 1 || f > N) continue; if (pb !== f && Math.abs(pb - f) - 1 === k) return String(N); } },
  'rank-h2': p => { const m = p.question.match(/(\w+) is (\d+)\w\w from the top and (\d+)\w\w from the bottom in a class\. (\d+) students ranked below \1(?: and (\d+) ranked above \1)? leave the class(?:, and (\d+) new students? joins?,(?: all)? ranked below \1)?\. (.+)$/);
    if (!m) throw new Error('parse'); const t = +m[2], bm = +m[3], below = +m[4], above = +(m[5] || 0), join = +(m[6] || 0);
    // simulate a list
    const L = []; for (let i = 1; i <= t + bm - 1; i++) L.push(i < t ? 'A' : i === t ? 'X' : 'B'); let nb = 0, na = 0;
    const M = L.filter(x => (x === 'B' && nb++ < below) || (x === 'A' && na++ < above) ? false : true); for (let i = 0; i < join; i++) M.push('J');
    const ix = M.indexOf('X'); if (/rank from the top/.test(m[7])) return ord(ix + 1); if (/rank from the bottom/.test(m[7])) return ord(M.length - ix); return String(M.length); },
  'rank-e3': compare, 'rank-m3': compare, 'rank-h3': compare,
};
