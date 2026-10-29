/* Independent 3D helpers for the test solvers: a die is a Map label -> outward unit normal [x,y,z].
   World axes: x = right, y = up, z = towards the viewer (front). Right-handed: y × z = x. */
const eq = (a, b) => a[0] === b[0] && a[1] === b[1] && a[2] === b[2];
const neg = a => [-a[0], -a[1], -a[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const UP = [0, 1, 0], FRONT = [0, 0, 1], RIGHT = [1, 0, 0];
const NORMALS = [[0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1], [-1, 0, 0], [1, 0, 0]];
// a view (top, front, right) is possible iff top ⟂ front and right = top × front
function hasView(die, [t, f, r]) { const a = die.get(t), b = die.get(f), c = die.get(r); if (!a || !b || !c) return false; return dot(a, b) === 0 && eq(cross(a, b), c); }
const opposite = (die, x) => { const n = neg(die.get(x)); for (const [k, v] of die) if (eq(v, n)) return k; };
// rotation that takes unit vector u onto unit vector v (u ⟂ v): 90° about axis u × v
function rot90(u, v) { const k = cross(u, v); return x => { const kx = cross(k, x), kd = dot(k, x); return [0, 1, 2].map(i => kx[i] + kd * k[i]).map(z => z + 0); }; } // Rodrigues with θ=90°: x' = k×x + k(k·x)
function orient(die, R) { const out = new Map(); for (const [k, v] of die) out.set(k, R(v)); return out; }
const faceAt = (die, n) => { for (const [k, v] of die) if (eq(v, n)) return k; };
// rolling moves (world): 'forward' = top goes to front, 'back' = top goes to back, 'right' = top goes to right, 'left' = top goes to left
const MOVE = { forward: rot90(UP, FRONT), back: rot90(UP, neg(FRONT)), right: rot90(UP, RIGHT), left: rot90(UP, neg(RIGHT)) };
// build a die from labels assigned to all 720 normal permutations
function* allDice(labels) { const P = perms(labels); for (const p of P) { const m = new Map(); p.forEach((l, i) => m.set(l, NORMALS[i])); yield m; } }
function perms(a) { if (a.length <= 1) return [a]; return a.flatMap((x, i) => perms(a.slice(0, i).concat(a.slice(i + 1))).map(r => [x].concat(r))); }
// die from a view list (top, front, right) of a fully known orientation + opposite function
function fromView([t, f, r], oppOf) { return new Map([[t, UP], [f, FRONT], [r, RIGHT], [oppOf(t), neg(UP)], [oppOf(f), neg(FRONT)], [oppOf(r), neg(RIGHT)]]); }
/* Fold a net (cells {r,c,label}) with the printed side OUTSIDE.
   The first cell is the TOP of a cube lying under the sheet; walking to a neighbour cell east (+c) means the
   sheet bends down over the cube's +x face, so we rotate the cube to bring that face to the top, etc.
   Returns {die, ok}: ok=false when two cells land on the same face or the walk is inconsistent around a loop. */
function foldNet(cells) {
  const at = new Map(cells.map((c, i) => [c.r + ',' + c.c, i])); const R = new Array(cells.length); // R[i]: function body->world as 3 column images
  const id = { x: [1, 0, 0], y: [0, 1, 0], z: [0, 0, 1] }; R[0] = id; const q = [0]; let ok = true;
  const apply = (M, f) => ({ x: f(M.x), y: f(M.y), z: f(M.z) });
  const step = { e: rot90(RIGHT, UP), w: rot90(neg(RIGHT), UP), s: rot90(FRONT, UP), n: rot90(neg(FRONT), UP) };
  const same = (A, B) => eq(A.x, B.x) && eq(A.y, B.y) && eq(A.z, B.z);
  while (q.length) { const i = q.shift(); const { r, c } = cells[i];
    for (const [d, dr, dc] of [['e', 0, 1], ['w', 0, -1], ['s', 1, 0], ['n', -1, 0]]) { const j = at.get((r + dr) + ',' + (c + dc)); if (j === undefined) continue; const M = apply(R[i], step[d]);
      if (R[j] === undefined) { R[j] = M; q.push(j); } else if (!same(R[j], M)) ok = false; } }
  if (R.some(x => x === undefined)) return { ok: false };
  // body normal of the face lying on top for cell i: world UP mapped back by R[i]^T
  const die = new Map(); const used = new Set();
  cells.forEach((cell, i) => { const M = R[i]; const b = [M.x[1], M.y[1], M.z[1]]; const k = b.join(); if (used.has(k)) ok = false; used.add(k); die.set(cell.label, b); });
  return { die, ok: ok && used.size === 6 && cells.length === 6 };
}
module.exports = { eq, neg, dot, cross, hasView, opposite, rot90, orient, faceAt, MOVE, allDice, perms, fromView, foldNet, UP, FRONT, RIGHT, NORMALS };
