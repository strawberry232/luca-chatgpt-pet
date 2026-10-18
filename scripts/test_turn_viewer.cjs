// Run after build_interactive_preview.py. Requires Playwright and a Chromium browser.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true,
    ...(process.env.PLAYWRIGHT_EXECUTABLE ? { executablePath: process.env.PLAYWRIGHT_EXECUTABLE } : {}) });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(pathToFileURL(path.resolve('build/luca-preview.html')).href);
    await page.waitForFunction(() => window.LucaPreview?.getState().loaded && LucaPreview.getState().continuousReady);
    const rect = await page.locator('#pet').boundingBox();
    const center = { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
    async function point(degrees) {
      const radians = degrees * Math.PI / 180;
      await page.mouse.move(center.x + Math.sin(radians) * 220, center.y - Math.cos(radians) * 220);
    }
    async function settle(degrees) {
      await point(degrees);
      await page.waitForFunction(degrees => {
        const state = LucaPreview.getState();
        return state.frame.index === Math.round(degrees / 22.5) % 16 && Math.abs(PetGaze.shortestDelta(state.gaze.angle, degrees)) < 0.1;
      }, degrees);
    }
    async function trace(from, to) {
      await settle(from);
      await page.evaluate(() => {
        window.turnSamples = [];
        window.turnRecording = true;
        function sample() {
          if (!window.turnRecording) return;
          window.turnSamples.push(LucaPreview.getState().frame.index);
          requestAnimationFrame(sample);
        }
        sample();
      });
      await point(to);
      await page.waitForFunction(degrees => {
        const state = LucaPreview.getState();
        return state.frame.index === Math.round(degrees / 22.5) % 16 && Math.abs(PetGaze.shortestDelta(state.gaze.angle, degrees)) < 0.1;
      }, to);
      const samples = await page.evaluate(() => { window.turnRecording = false; return window.turnSamples; });
      samples.push(Math.round(to / 22.5) % 16);
      const sequence = samples.filter((value, index) => index === 0 || value !== samples[index - 1]);
      for (let i = 1; i < sequence.length; i++) {
        const difference = (sequence[i] - sequence[i - 1] + 16) % 16;
        assert.ok(difference === 1 || difference === 15, `Skipped neighboring pose: ${sequence}`);
      }
      return sequence;
    }
    const quarterTurn = await trace(0, 90);
    assert.deepEqual(quarterTurn, [0, 1, 2, 3, 4]);
    const wrapForward = await trace(337.5, 22.5);
    assert.deepEqual(wrapForward, [15, 0, 1]);
    const wrapBackward = await trace(22.5, 337.5);
    assert.deepEqual(wrapBackward, [1, 0, 15]);
    const halfTurn = await trace(0, 180);
    assert.equal(halfTurn.length, 9);
    await settle(90);
    await page.mouse.move(center.x,center.y);
    await page.waitForTimeout(60);
    assert.equal(await page.evaluate(() => LucaPreview.getState().frame.index), 4, 'Crossing the center must hold the gaze, not reset to idle');
    await settle(0);
    const exactPixels = await page.locator('#pet').evaluate(canvas => canvas.toDataURL());
    await settle(6);
    assert.equal(await page.evaluate(() => LucaPreview.getState().frame.index), 0);
    const intermediatePixels = await page.locator('#pet').evaluate(canvas => canvas.toDataURL());
    assert.notEqual(exactPixels, intermediatePixels, 'Rendered pixels must change within one original direction sector');
    await settle(0);
    const jitter = [];
    for (let i = 0; i < 20; i++) {
      await point(i % 2 ? 10.8 : 11.8);
      await page.waitForTimeout(20);
      jitter.push(await page.evaluate(() => LucaPreview.getState().frame.index));
    }
    assert.ok(jitter.every(index => index === 0));
    const directions = [];
    for (let i = 0; i < 16; i++) {
      await settle(i * 22.5);
      const frame = await page.evaluate(() => LucaPreview.getState().frame);
      assert.equal(frame.row, 9 + Math.floor(i / 8));
      assert.equal(frame.column, i % 8);
      directions.push(i);
    }
    await page.locator('[data-mode="demo"]').click();
    await page.waitForFunction(() => LucaPreview.getState().frame.index === 12);
    await page.waitForFunction(() => LucaPreview.getState().frame.turning === true);
    await page.screenshot({ path: 'build/turning-viewer.png', fullPage: true });
    await page.locator('#language').click();
    assert.equal(await page.locator('[data-mode="demo"]').innerText(), 'Show turning demo');
    await page.locator('#language').click();
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.waitForFunction(() => LucaPreview.getState().frame.row === 0 && LucaPreview.getState().frame.column === 0);
    await page.locator('[data-mode="failed"]').click();
    await page.waitForFunction(() => LucaPreview.getState().frame.row === 5);
    await page.setViewportSize({ width: 390, height: 844 });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
    assert.deepEqual(errors, []);
    const report = { ok: true, scope: 'standalone viewer only', quarter_turn: quarterTurn,
      wrap_forward: wrapForward, wrap_backward: wrapBackward, half_turn: halfTurn,
      boundary_jitter_held: true, center_crossing_holds_gaze: true,
      continuous_pixels_within_sector: true, inbetween_frames: 128,
      directions, demo_mode: true, reduced_motion: true,
      bilingual_labels: true, narrow_layout: true, browser_errors: errors };
    await fs.writeFile('qa/turn-transition-browser-check.json', JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
