/* Loads the app's generator modules into Node (same files the browser uses). */
const path = require('path');
const ROOT = path.join(__dirname, '..', '..', 'assets', 'js', 'reasoning-lab');
const FILES = ['core.js', 'cube.js', 'dice.js', 'folding.js', 'mirror.js', 'figcount.js', 'blood.js', 'direction.js', 'syllogism.js', 'inequality.js', 'coding.js', 'series.js', 'ranking.js', 'seating.js', 'puzzles.js', 'dilr.js'];
FILES.forEach(f => require(path.join(ROOT, f)));
module.exports = { RL: globalThis.RL, FILES };
