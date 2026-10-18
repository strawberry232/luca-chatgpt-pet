(function (root) {
  'use strict';
  function frameForPointer(rect, point, spriteVersionNumber = 2, deadzone = 1) {
    if (spriteVersionNumber !== 2 || !point) return null;
    const dx = point.x - (rect.left + rect.width / 2);
    const dy = point.y - (rect.top + rect.height / 2);
    if (Math.hypot(dx, dy) <= deadzone) return null;
    const degrees = (Math.atan2(dx, -dy) * 180 / Math.PI + 360) % 360;
    const index = Math.round(degrees / 22.5) % 16;
    return { index, row: 9 + Math.floor(index / 8), column: index % 8, degrees: index * 22.5 };
  }
  const api = { frameForPointer };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.PetGaze = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
