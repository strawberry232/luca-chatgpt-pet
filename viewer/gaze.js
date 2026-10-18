(function (root) {
  'use strict';
  function frameForPointer(rect, point, spriteVersionNumber = 2, deadzone = 1) {
    if (spriteVersionNumber !== 2 || !point) return null;
    const dx = point.x - (rect.left + rect.width / 2);
    const dy = point.y - (rect.top + rect.height / 2);
    if (Math.hypot(dx, dy) <= deadzone) return null;
    const degrees = (Math.atan2(dx, -dy) * 180 / Math.PI + 360) % 360;
    const index = Math.round(degrees / 22.5) % 16;
    return { ...frameForIndex(index), targetDegrees: degrees };
  }
  function frameForIndex(index) {
    index = ((index % 16) + 16) % 16;
    return { index, row: 9 + Math.floor(index / 8), column: index % 8, degrees: index * 22.5 };
  }
  function shortestDelta(from, to) {
    return ((to - from + 540) % 360 + 360) % 360 - 180;
  }
  function normalize(degrees) { return ((degrees % 360) + 360) % 360; }
  function createGazeController({ maxSpeed = 540, acceleration = 3200, hysteresis = 3 } = {}) {
    let angle = null, velocity = 0, index = 0, lastTime = null, targetAngle = null;
    function reset() { angle = null; velocity = 0; lastTime = null; targetAngle = null; }
    function update(target, now) {
      if (!target) { reset(); return null; }
      targetAngle = normalize(target.targetDegrees ?? target.degrees);
      if (angle === null) {
        angle = targetAngle; index = target.index; lastTime = now;
        return { ...frameForIndex(index), turning: false };
      }
      // Capping elapsed time keeps a background-tab pause from skipping poses.
      const dt = Math.max(0, Math.min(50, now - lastTime)) / 1000;
      lastTime = now;
      const delta = shortestDelta(angle, targetAngle);
      if (velocity * delta < 0) velocity = 0;
      const desired = Math.sign(delta) * Math.min(maxSpeed, Math.sqrt(2 * acceleration * Math.abs(delta)));
      const change = Math.max(-acceleration * dt, Math.min(acceleration * dt, desired - velocity));
      velocity += change;
      const step = velocity * dt;
      if (Math.abs(step) >= Math.abs(delta)) { angle = targetAngle; velocity = 0; }
      else angle = normalize(angle + step);
      // Hold a small band around sector boundaries to prevent pointer chatter.
      // Emit at most one neighboring pose per display frame, including wraparound.
      const offset = shortestDelta(index * 22.5, angle);
      if (offset > 11.25 + hysteresis) index = (index + 1) % 16;
      else if (offset < -11.25 - hysteresis) index = (index + 15) % 16;
      return { ...frameForIndex(index), turning: Math.abs(shortestDelta(angle, targetAngle)) > 2 };
    }
    return { update, reset, getState: () => ({ angle, velocity, index, targetAngle }) };
  }
  const api = { frameForPointer, frameForIndex, shortestDelta, createGazeController };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.PetGaze = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
