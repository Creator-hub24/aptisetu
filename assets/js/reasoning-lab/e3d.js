/* Reasoning Lab — tiny self-written 3D engine on <canvas> (orthographic, painter's algorithm, drag to rotate). */
(function (g) {
  'use strict';
  const RL = g.RL || (g.RL = {});
  const reduced = () => (g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches) || !!RL.motionOff;
  const live = new Set(); RL.redrawAll = () => live.forEach(s => { if (s.alive()) s.redraw(); else live.delete(s); });
  const css = n => getComputedStyle(RL.cssRoot || document.documentElement).getPropertyValue('--' + n).trim() || '#888';
  // ---- vector / matrix helpers (3x3 row-major arrays)
  const mul = (A, B) => { const C = new Array(9).fill(0); for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) for (let k = 0; k < 3; k++) C[i * 3 + j] += A[i * 3 + k] * B[k * 3 + j]; return C; };
  const ap = (M, v) => [M[0] * v[0] + M[1] * v[1] + M[2] * v[2], M[3] * v[0] + M[4] * v[1] + M[5] * v[2], M[6] * v[0] + M[7] * v[1] + M[8] * v[2]];
  const rx = a => { const c = Math.cos(a), s = Math.sin(a); return [1, 0, 0, 0, c, -s, 0, s, c]; };
  const ry = a => { const c = Math.cos(a), s = Math.sin(a); return [c, 0, s, 0, 1, 0, -s, 0, c]; };
  const rz = a => { const c = Math.cos(a), s = Math.sin(a); return [c, -s, 0, s, c, 0, 0, 0, 1]; };
  const I3 = [1, 0, 0, 0, 1, 0, 0, 0, 1];
  // rotation of angle a about an axis through point p with unit direction u (returns fn on points)
  function axisRot(p, u, a) { const c = Math.cos(a), s = Math.sin(a), [x, y, z] = u; const M = [c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s, y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s, z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)];
    return q => { const v = ap(M, [q[0] - p[0], q[1] - p[1], q[2] - p[2]]); return [v[0] + p[0], v[1] + p[1], v[2] + p[2]]; }; }
  RL.m3 = { mul, ap, rx, ry, rz, I3, axisRot };

  /* Scene: create(canvas, buildFn) — buildFn(t) returns {quads:[{p:[4 pts], fill, stroke, alpha, label, labelColor, lw}], lines:[{a,b,color,dash}], size}
     opts: {yaw, pitch, spin, anim:{dur, from}, onFrame} */
  function Scene(canvas, build, opts) {
    opts = opts || {}; const ctx = canvas.getContext('2d'); let yaw = opts.yaw !== undefined ? opts.yaw : -0.62, pitch = opts.pitch !== undefined ? opts.pitch : 0.5;
    let raf = 0, t0 = performance.now(), dragging = false, lx = 0, ly = 0, alive = true, userMoved = false;
    const dur = opts.dur || 0; const spin = !!opts.spin;
    function size() { const r = canvas.getBoundingClientRect(); const d = Math.min(2, g.devicePixelRatio || 1); const w = Math.max(160, Math.round((r.width || 320) * d)); if (canvas.width !== w || canvas.height !== w) { canvas.width = w; canvas.height = w; } return w; }
    function frame(now) {
      if (!alive) return; if (!canvas.isConnected) { alive = false; return; }
      const W = size(); const el = (now - t0) / 1000; const red = reduced();
      const t = dur && !red ? Math.min(1, el / dur) : 1;
      if (spin && !userMoved && !red) yaw = (opts.yaw !== undefined ? opts.yaw : -0.62) + Math.sin(el * 0.5) * 0.4;
      const S = build(t); const R = mul(rx(pitch), ry(yaw));
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, W);
      const sc = W / (S.size || 4), cx = W / 2, cy = W / 2;
      const P = v => { const q = ap(R, v); return [cx + q[0] * sc, cy - q[1] * sc, q[2]]; };
      const items = [];
      for (const q of S.quads) { const pp = q.p.map(P); const ax = pp[1][0] - pp[0][0], ay = pp[1][1] - pp[0][1], bx = pp[3][0] - pp[0][0], by = pp[3][1] - pp[0][1]; const cr = ax * by - ay * bx;
        if (!q.both && cr <= 0) continue; // back-face (screen y down: front faces are clockwise -> cr>0)
        const r0 = ap(R, q.p[0]), r1 = ap(R, q.p[1]), r3 = ap(R, q.p[3]); const e1 = [r1[0] - r0[0], r1[1] - r0[1], r1[2] - r0[2]], e2 = [r3[0] - r0[0], r3[1] - r0[1], r3[2] - r0[2]];
        const nx = e1[1] * e2[2] - e1[2] * e2[1], ny = e1[2] * e2[0] - e1[0] * e2[2], nz = e1[0] * e2[1] - e1[1] * e2[0], nl = Math.hypot(nx, ny, nz) || 1; const lam = Math.abs((nx * 0.3 - ny * 0.6 - nz * 0.74) / nl);
        items.push({ z: (pp[0][2] + pp[1][2] + pp[2][2] + pp[3][2]) / 4 + (q.bias || 0), pp, q, flip: cr < 0, shade: (1 - lam) * 0.24 }); }
      items.sort((a, b) => a.z - b.z);
      ctx.lineJoin = 'round';
      for (const { pp, q, flip, shade } of items) {
        ctx.globalAlpha = q.alpha === undefined ? 1 : q.alpha; ctx.beginPath(); ctx.moveTo(pp[0][0], pp[0][1]); for (let i = 1; i < 4; i++) ctx.lineTo(pp[i][0], pp[i][1]); ctx.closePath();
        if (q.fill) { ctx.fillStyle = flip && q.backFill ? q.backFill : q.fill; ctx.fill(); if (!q.flat && shade > 0.01) { ctx.fillStyle = `rgba(0,0,0,${shade.toFixed(3)})`; ctx.fill(); } }
        if (q.stroke) { ctx.strokeStyle = q.stroke; ctx.lineWidth = (q.lw || 1) * W / 400; ctx.stroke(); }
        if (q.label && !flip) { // affine map unit square -> quad (p0 top-left, p1 top-right, p3 bottom-left)
          ctx.save(); ctx.setTransform((pp[1][0] - pp[0][0]) / 100, (pp[1][1] - pp[0][1]) / 100, (pp[3][0] - pp[0][0]) / 100, (pp[3][1] - pp[0][1]) / 100, pp[0][0], pp[0][1]);
          ctx.fillStyle = q.labelColor || css('ink'); ctx.font = `800 ${q.labelSize || 52}px system-ui, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(q.label, 50, 54); ctx.restore(); }
      }
      ctx.globalAlpha = 1;
      for (const L of S.lines || []) { const a = P(L.a), b = P(L.b); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.strokeStyle = L.color; ctx.lineWidth = (L.lw || 1.5) * W / 400; ctx.setLineDash(L.dash ? [6 * W / 400, 5 * W / 400] : []); ctx.stroke(); ctx.setLineDash([]); }
      const moving = (dur && t < 1) || (spin && !userMoved && !red) || dragging;
      raf = moving ? requestAnimationFrame(frame) : 0;
    }
    const kick = () => { if (!raf && alive) raf = requestAnimationFrame(frame); };
    canvas.addEventListener('pointerdown', e => { dragging = true; userMoved = true; lx = e.clientX; ly = e.clientY; canvas.setPointerCapture(e.pointerId); kick(); });
    canvas.addEventListener('pointermove', e => { if (!dragging) return; yaw += (e.clientX - lx) * 0.01; pitch = Math.max(-1.5, Math.min(1.5, pitch + (e.clientY - ly) * 0.01)); lx = e.clientX; ly = e.clientY; kick(); });
    const up = () => { dragging = false; }; canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
    canvas.tabIndex = 0; canvas.addEventListener('keydown', e => { const k = e.key; if (!/^Arrow/.test(k)) return; e.preventDefault(); userMoved = true; if (k === 'ArrowLeft') yaw -= 0.15; if (k === 'ArrowRight') yaw += 0.15; if (k === 'ArrowUp') pitch = Math.max(-1.5, pitch - 0.15); if (k === 'ArrowDown') pitch = Math.min(1.5, pitch + 0.15); kick(); });
    if (g.ResizeObserver) new ResizeObserver(kick).observe(canvas);
    kick();
    const api = { redraw: () => { kick(); }, restart: () => { t0 = performance.now(); kick(); }, set: (y, p) => { yaw = y; pitch = p; userMoved = true; kick(); }, stop: () => { alive = false; }, alive: () => alive && canvas.isConnected };
    live.add(api); return api;
  }
  RL.Scene = Scene;

  // ---- face geometry of an axis-aligned box [x0,x1]x[y0,y1]x[z0,z1]; corners ordered TL, TR, BR, BL as seen from outside (text upright)
  function boxFaces(x0, x1, y0, y1, z0, z1) {
    return {
      top: [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]],
      bottom: [[x0, y0, z1], [x1, y0, z1], [x1, y0, z0], [x0, y0, z0]],
      front: [[x0, y1, z1], [x1, y1, z1], [x1, y0, z1], [x0, y0, z1]],
      back: [[x1, y1, z0], [x0, y1, z0], [x0, y0, z0], [x1, y0, z0]],
      left: [[x0, y1, z0], [x0, y1, z1], [x0, y0, z1], [x0, y0, z0]],
      right: [[x1, y1, z1], [x1, y1, z0], [x1, y0, z0], [x1, y0, z1]],
    };
  }
  RL.boxFaces = boxFaces;
  RL.css = css; RL.reduced = reduced;
})(typeof globalThis !== 'undefined' ? globalThis : this);
