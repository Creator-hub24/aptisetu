/* Independent dice solver using outward normals and real 3D rotations (tests/lib/geo.js). */
const G = require('../lib/geo');
const parseView = s => { const m = s.match(/top (\w+), front (\w+), right (\w+)/); return [m[1], m[2], m[3]]; };
const viewsIn = q => [...q.matchAll(/top (\w+), front (\w+), right (\w+)/g)].map(m => [m[1], m[2], m[3]]);
const MV = { 'tips forward (towards you)': 'forward', 'tips backward (away from you)': 'back', 'tips to the right': 'right', 'tips to the left': 'left', 'towards you': 'forward', away: 'back', right: 'right', left: 'left' };
const roll = (die, moves) => moves.reduce((d, m) => G.orient(d, G.MOVE[m]), die);
const labelsOf = vs => [...new Set(vs.flat())];
function consistentDice(labels, vs) { const out = []; for (const d of G.allDice(labels)) if (vs.every(v => G.hasView(d, v))) out.push(d); return out; }
const unique = (arr, what) => { const s = new Set(arr); if (s.size !== 1) throw new Error(what + ' not determined: ' + [...s]); return arr[0]; };
const labelUniverse = p => p.options.map(o => o.label).concat(viewsIn(p.question).flat());
function sixLabels(p) { const s = new Set(viewsIn(p.question).flat()); p.options.forEach(o => { if (/^\w+$/.test(o.label)) s.add(o.label); }); return [...s]; }
const pad = l => { l = [...new Set(l)]; while (l.length < 6) l.push('?' + l.length); if (l.length > 6) throw new Error('labels ' + l); return l; };
const STD_OPP = x => String(7 - +x);
module.exports = {
  'dice-e1': p => { const v = viewsIn(p.question)[0]; const d = G.fromView(v, STD_OPP); if (!G.hasView(d, v)) throw new Error('bad'); return String(v.reduce((s, x) => s + (7 - +x), 0)); },
  'dice-e2': p => { const vs = viewsIn(p.question), x = p.question.match(/opposite (\w+)\?/)[1]; const labs = pad(sixLabels(p).concat([x])); const r = unique(consistentDice(labs, vs).map(d => G.opposite(d, x)), 'opposite'); if (r[0] === '?') throw new Error('placeholder'); return r; },
  'dice-e3': p => { const v = viewsIn(p.question)[0]; const mv = p.question.match(/\. It (.+)\. Which/)[1].split(', then ').map(s => MV[s]); const d = roll(G.fromView(v, STD_OPP), mv); return G.faceAt(d, G.UP); },
  'dice-m1': p => module.exports['dice-e2'](p),
  'dice-m2': p => { const q = p.question.split('Which')[0]; const vs = viewsIn(q); const labs = pad(labelsOf(vs.concat(p.options.map(o => parseView(o.label)))));
    const C = consistentDice(labs, vs); if (!C.length) throw new Error('no die'); return o => { const v = parseView(o.label); const r = C.map(d => G.hasView(d, v)); if (new Set(r).size !== 1) throw new Error('view undetermined'); return !r[0]; }; },
  'dice-m3': p => { const q = p.question; const pairs = [...q.match(/opposite pairs (.+?)\. It starts/)[1].matchAll(/(\w+)–(\w+)/g)].map(m => [m[1], m[2]]);
    const oppOf = x => { const pr = pairs.find(pp => pp.includes(x)); return pr[0] === x ? pr[1] : pr[0]; }; const v = parseView(q.match(/starts showing (top \w+, front \w+, right \w+)/)[1]);
    const mv = q.match(/right \w+, then (.+)\. Which/)[1].split(', then ').map(s => MV[s]); return G.faceAt(roll(G.fromView(v, oppOf), mv), G.UP); },
  'dice-h1': p => { const q = p.question; const vs = viewsIn(q.split('If the die')[0]); const m = q.match(/with (\w+) on top and (\w+) at the front/); const labs = labelsOf(vs.concat([[m[1], m[2]]]).concat(p.options.map(o => [o.label])));
    if (labs.length !== 6) throw new Error('labels ' + labs);
    return unique(consistentDice(labs, vs).map(d => { const r = G.cross(d.get(m[1]), d.get(m[2])); if (G.dot(d.get(m[1]), d.get(m[2])) !== 0) throw new Error('not adjacent'); return G.faceAt(d, r); }), 'right'); },
  'dice-h2': p => { const { die, ok } = G.foldNet(p.viz.cells); if (!ok) throw new Error('not a net'); return o => G.hasView(die, parseView(o.label)); },
  'dice-h3': p => { const q = p.question; const { die, ok } = G.foldNet(p.viz.cells); if (!ok) throw new Error('net'); const v = parseView(q.match(/starts with (top \w+, front \w+, right \w+)/)[1]); if (!G.hasView(die, v)) throw new Error('start view impossible');
    const oppOf = x => G.opposite(die, x); const mv = q.match(/rolled: (.+)\. Which/)[1].split(', ').map(s => MV[s]); const ask = q.match(/at the (top|bottom) at the end/)[1];
    return G.faceAt(roll(G.fromView(v, oppOf), mv), ask === 'top' ? G.UP : G.neg(G.UP)); },
};
