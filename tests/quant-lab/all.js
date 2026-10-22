// Node entry: load the Quant Lab generators that ship in assets/js/quant-lab/.
const D = '../../assets/js/quant-lab/';
const Q = require(D + 'core.js'); require(D + 'arithmetic.js'); require(D + 'algebra.js'); require(D + 'geometry.js'); require(D + 'modern.js'); module.exports = Q;
