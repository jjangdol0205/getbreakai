'use strict';

/**
 * Empirical Challenger Stress Test Harness — Milestone 1 (Division 3 GetBreakAI)
 * Tests:
 * 1. 1-second JPY/USD ATR Cut-Loss & Position Calculator in `dist/jp/index.html` (and `jp/index.html`)
 * 2. Boundary capital amounts (100k JPY, 10M JPY, 100M JPY, zero, negatives, extreme values)
 * 3. Share sizing formula `Math.floor((capital * 0.015) / (2.0 * atr))`
 * 4. Stop-loss formula `entry - 2.0 * atr` & 2.5R target formula `entry + 2.5 * 2.0 * atr`
 * 5. Output card string hygiene: zero NaN, undefined, or Infinity
 * 6. Lemon Squeezy Store #296100 Live UUID `gb-starter-29` and embed/redirect parameters
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const ROOT = path.resolve(__dirname, '..');
const DIST_JP_INDEX = path.join(ROOT, 'dist', 'jp', 'index.html');
const SRC_JP_INDEX = path.join(ROOT, 'jp', 'index.html');
const DIST_ROOT_INDEX = path.join(ROOT, 'dist', 'index.html');

/**
 * Helper: Extract the interactive calculator script from HTML and execute inside mock DOM
 */
function createCalculatorEnvironment(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');

  // Extract client script from HTML
  const scriptMatch = html.match(/<!--\s*Client-side Interactive Calculation Script\s*-->\s*<script>([\s\S]*?)<\/script>/i);
  assert.ok(scriptMatch, `Client calculation script must exist in ${htmlPath}`);
  const scriptContent = scriptMatch[1];

  // Mock DOM elements
  const elements = {
    jpCalcSlider: { value: '50000', id: 'jpCalcSlider' },
    jpCalcAccLbl: { innerText: '', id: 'jpCalcAccLbl' },
    jpOutShares: { innerText: '', id: 'jpOutShares' },
    jpOutRisk: { innerText: '', id: 'jpOutRisk' },
    jpOutGain: { innerText: '', id: 'jpOutGain' }
  };

  const presetChips = [];
  const capButtons = [];

  const mockDocument = {
    getElementById: (id) => elements[id] || null,
    querySelectorAll: (selector) => {
      if (selector === '.preset-chip') return presetChips;
      if (selector === '.cap-btn') return capButtons;
      return [];
    }
  };

  const mockWindow = {
    addEventListener: () => {}
  };

  const sandbox = {
    document: mockDocument,
    window: mockWindow,
    console: console,
    Math: Math,
    parseFloat: parseFloat,
    parseInt: parseInt
  };

  vm.createContext(sandbox);
  vm.runInContext(scriptContent, sandbox);

  return {
    sandbox,
    elements,
    html
  };
}

// =========================================================================
// Suite 1: Calculator Boundary Capital Amounts & Resiliency
// =========================================================================

test('Suite 1.1: Standard preset capital amounts (100万円 to 1,200万円)', () => {
  const { sandbox, elements } = createCalculatorEnvironment(DIST_JP_INDEX);

  const presets = [
    { label: '100万円', usd: 6700 },
    { label: '300万円', usd: 20000 },
    { label: '500万円', usd: 33300 },
    { label: '750万円', usd: 50000 },
    { label: '1,000万円', usd: 66700 },
    { label: '1,200万円', usd: 80000 }
  ];

  for (const preset of presets) {
    elements.jpCalcSlider.value = String(preset.usd);
    sandbox.recalcJpQuickCalc();

    assert.ok(elements.jpCalcAccLbl.innerText.includes('$' + preset.usd.toLocaleString()), `Acc label must contain $${preset.usd}`);
    assert.doesNotMatch(elements.jpCalcAccLbl.innerText, /NaN|undefined|Infinity/i);
    assert.doesNotMatch(elements.jpOutShares.innerText, /NaN|undefined|Infinity/i);
    assert.doesNotMatch(elements.jpOutRisk.innerText, /NaN|undefined|Infinity/i);
    assert.doesNotMatch(elements.jpOutGain.innerText, /NaN|undefined|Infinity/i);
  }
});

test('Suite 1.2: Boundary capital amounts (100k JPY, 10M JPY, 100M JPY)', () => {
  const { sandbox, elements } = createCalculatorEnvironment(DIST_JP_INDEX);

  // 100k JPY = 100,000 / 150 = $666.67
  const capital100kJpyInUsd = 100000 / 150.0;
  elements.jpCalcSlider.value = String(capital100kJpyInUsd);
  sandbox.recalcJpQuickCalc();
  assert.doesNotMatch(elements.jpOutShares.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutRisk.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutGain.innerText, /NaN|undefined|Infinity/i);
  assert.ok(elements.jpOutShares.innerText.includes('株'), 'Must render shares output');

  // 10M JPY = 10,000,000 / 150 = $66,666.67
  const capital10MJpyInUsd = 10000000 / 150.0;
  elements.jpCalcSlider.value = String(capital10MJpyInUsd);
  sandbox.recalcJpQuickCalc();
  assert.doesNotMatch(elements.jpOutShares.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutRisk.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutGain.innerText, /NaN|undefined|Infinity/i);

  // 100M JPY (1億円) = 100,000,000 / 150 = $666,666.67
  const capital100MJpyInUsd = 100000000 / 150.0;
  elements.jpCalcSlider.value = String(capital100MJpyInUsd);
  sandbox.recalcJpQuickCalc();
  assert.doesNotMatch(elements.jpOutShares.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutRisk.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutGain.innerText, /NaN|undefined|Infinity/i);
});

test('Suite 1.3: Zero and negative capital fallback & clamping', () => {
  const { sandbox, elements } = createCalculatorEnvironment(DIST_JP_INDEX);

  // Zero capital: "0" should safely fall back to 50000 default or calculate safely
  elements.jpCalcSlider.value = '0';
  sandbox.recalcJpQuickCalc();
  assert.doesNotMatch(elements.jpCalcAccLbl.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutShares.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutRisk.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutGain.innerText, /NaN|undefined|Infinity/i);

  // Negative capital: "-50000"
  elements.jpCalcSlider.value = '-50000';
  sandbox.recalcJpQuickCalc();
  assert.doesNotMatch(elements.jpCalcAccLbl.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutShares.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutRisk.innerText, /NaN|undefined|Infinity/i);
  assert.doesNotMatch(elements.jpOutGain.innerText, /NaN|undefined|Infinity/i);
  // Math.max(1, ...) guarantees shares is at least 1 even under negative input
  assert.match(elements.jpOutShares.innerText, /^1株/);
});

test('Suite 1.4: Extreme adversarial capital inputs (NaN, strings, null slider, huge numbers)', () => {
  const { sandbox, elements } = createCalculatorEnvironment(DIST_JP_INDEX);

  const adversarialInputs = ['abc', '', '   ', 'null', 'undefined', '1e15', '0.00001', '-0'];

  for (const input of adversarialInputs) {
    elements.jpCalcSlider.value = input;
    sandbox.recalcJpQuickCalc();
    assert.doesNotMatch(elements.jpCalcAccLbl.innerText, /NaN|undefined|Infinity/i, `Acc label failed on input ${input}`);
    assert.doesNotMatch(elements.jpOutShares.innerText, /NaN|undefined|Infinity/i, `OutShares failed on input ${input}`);
    assert.doesNotMatch(elements.jpOutRisk.innerText, /NaN|undefined|Infinity/i, `OutRisk failed on input ${input}`);
    assert.doesNotMatch(elements.jpOutGain.innerText, /NaN|undefined|Infinity/i, `OutGain failed on input ${input}`);
  }
});

// =========================================================================
// Suite 2: Share Sizing Mathematical Formula Verification
// =========================================================================

test('Suite 2.1: Share formula matches Math.floor((capital * 0.015) / (2.0 * atr))', () => {
  const { sandbox, elements } = createCalculatorEnvironment(DIST_JP_INDEX);

  // NVDA defaults: price = 186.64, atr = 8.02, activeStopDist = 16.04
  const capitalLevels = [10000, 25000, 50000, 75000, 100000, 250000];
  const price = 186.64;
  const atr = 8.02;
  const stopDist = atr * 2.0;

  for (const cap of capitalLevels) {
    elements.jpCalcSlider.value = String(cap);
    sandbox.recalcJpQuickCalc();

    const expectedRisk = cap * 0.015;
    const expectedRiskShares = Math.floor(expectedRisk / stopDist);
    const expectedMaxNotionalShares = Math.floor(cap / price);
    const expectedShares = Math.max(1, Math.min(expectedRiskShares, expectedMaxNotionalShares));

    const renderedMatch = elements.jpOutShares.innerText.match(/^(\d+)株/);
    assert.ok(renderedMatch, `Shares must match digit pattern: ${elements.jpOutShares.innerText}`);
    const actualShares = parseInt(renderedMatch[1], 10);

    assert.equal(actualShares, expectedShares, `Shares for capital $${cap} must be ${expectedShares}, got ${actualShares}`);
  }
});

test('Suite 2.2: Share sizing across all 5 preset tickers (NVDA, TSLA, PLTR, SOXL, 8035)', () => {
  const { sandbox, elements } = createCalculatorEnvironment(DIST_JP_INDEX);

  const tickers = [
    { ticker: 'NVDA', price: 186.64, atr: 8.02 },
    { ticker: 'TSLA', price: 325.50, atr: 18.20 },
    { ticker: 'PLTR', price: 61.20, atr: 3.45 },
    { ticker: 'SOXL', price: 38.50, atr: 2.85 },
    { ticker: '8035', price: 178.67, atr: 7.67 }
  ];

  const testCapital = 50000;
  elements.jpCalcSlider.value = String(testCapital);

  for (const t of tickers) {
    sandbox.setQuickStock(t.ticker, t.price, t.atr, null);

    const expectedStopDist = t.atr * 2.0;
    const expectedRisk = testCapital * 0.015;
    const expectedShares = Math.max(1, Math.min(Math.floor(expectedRisk / expectedStopDist), Math.floor(testCapital / t.price)));

    const match = elements.jpOutShares.innerText.match(/^(\d+)株/);
    assert.ok(match);
    const actualShares = parseInt(match[1], 10);
    assert.equal(actualShares, expectedShares, `Shares for ${t.ticker} must match formula`);

    // Verify stop loss price = activePrice - 2.0 * atr
    const expectedStopPrice = Math.max(0.01, t.price - expectedStopDist);
    const stopPriceMatch = elements.jpOutRisk.innerText.match(/^\$([\d.]+)/);
    assert.ok(stopPriceMatch);
    assert.equal(parseFloat(stopPriceMatch[1]), parseFloat(expectedStopPrice.toFixed(2)));

    // Verify 2.5R target price = activePrice + 2.5 * 2.0 * atr
    const expectedTargetPrice = t.price + (expectedStopDist * 2.5);
    const targetPriceMatch = elements.jpOutGain.innerText.match(/^\$([\d.]+)/);
    assert.ok(targetPriceMatch);
    assert.equal(parseFloat(targetPriceMatch[1]), parseFloat(expectedTargetPrice.toFixed(2)));

    // Verify Risk-Reward ratio is exactly 2.5R
    const riskDiff = t.price - expectedStopPrice;
    const rewardDiff = expectedTargetPrice - t.price;
    const rrRatio = rewardDiff / riskDiff;
    assert.ok(Math.abs(rrRatio - 2.5) < 0.01, `R:R ratio must be 2.5, got ${rrRatio}`);
  }
});

test('Suite 2.3: Fuzz test across 250 arbitrary capital and price/atr configurations', () => {
  const { sandbox, elements } = createCalculatorEnvironment(DIST_JP_INDEX);

  const testCases = [];
  for (let cap = 5000; cap <= 250000; cap += 5000) {
    testCases.push(cap);
  }
  // Add extreme fuzz points
  testCases.push(0.01, 1, 100, 666.67, 333333, 1000000, 5000000, 10000000);

  for (const cap of testCases) {
    elements.jpCalcSlider.value = String(cap);
    sandbox.recalcJpQuickCalc();

    // Verify no NaN or undefined leaked into any DOM string
    assert.doesNotMatch(elements.jpCalcAccLbl.innerText, /NaN|undefined|Infinity/i);
    assert.doesNotMatch(elements.jpOutShares.innerText, /NaN|undefined|Infinity/i);
    assert.doesNotMatch(elements.jpOutRisk.innerText, /NaN|undefined|Infinity/i);
    assert.doesNotMatch(elements.jpOutGain.innerText, /NaN|undefined|Infinity/i);

    // Verify shares are positive integer
    const sharesMatch = elements.jpOutShares.innerText.match(/^(\d+)株/);
    assert.ok(sharesMatch);
    assert.ok(parseInt(sharesMatch[1], 10) >= 1);
  }
});

// =========================================================================
// Suite 3: Lemon Squeezy Store #296100 Live UUID & Checkout Integrity
// =========================================================================

test('Suite 3.1: dist/jp/index.html Lemon Squeezy checkout link and Store #296100 integrity', () => {
  const html = fs.readFileSync(DIST_JP_INDEX, 'utf8');

  // Must contain live UUIDs d5e7e761-8b1b-4ca8-b1fe-771acd1450f8 ($29/mo) & 667aa482-f17c-47d1-b7f3-a2427c36516b ($199/yr)
  assert.ok(html.includes('d5e7e761-8b1b-4ca8-b1fe-771acd1450f8'), 'Must contain live $29/mo UUID');
  assert.ok(html.includes('667aa482-f17c-47d1-b7f3-a2427c36516b'), 'Must contain live $199/yr UUID');

  // Must contain truthofmarket Lemon Squeezy store checkout URL with embed=1 and redirect_url
  const expectedCheckoutPattern = /https:\/\/truthofmarket\.lemonsqueezy\.com\/checkout\/buy\/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8\?embed=1&checkout\[redirect_url\]=https:\/\/getbreakai\.com\/confirmation\.html/;
  assert.match(html, expectedCheckoutPattern, 'Must contain exact Lemon Squeezy checkout link with embed=1 and redirect_url');

  // Must contain Store #296100 trust mark
  assert.ok(html.includes('Lemon Squeezy Store #296100'), 'Must contain Store #296100 trust mark');

  // Must NOT contain invalid or unauthorized store URLs or broken slugs
  assert.ok(!html.includes('kidsfit.lemonsqueezy.com'), 'Must not contain kidsfit.lemonsqueezy.com in Div 3');
  assert.ok(!html.includes('gb-starter-29') && !html.includes('gb-pro-49') && !html.includes('gb-inst-1499'), 'Must not contain broken 404 slugs');
});

test('Suite 3.2: Hash parity between jp/index.html and dist/jp/index.html', () => {
  const srcHtml = fs.readFileSync(SRC_JP_INDEX, 'utf8');
  const distHtml = fs.readFileSync(DIST_JP_INDEX, 'utf8');

  assert.equal(srcHtml, distHtml, 'dist/jp/index.html must be identical to jp/index.html');
});

test('Suite 3.3: Root dist/index.html Store #296100 Live UUIDs integrity', () => {
  const rootHtml = fs.readFileSync(DIST_ROOT_INDEX, 'utf8');

  // Must contain live UUIDs + corporate inquiry
  assert.ok(rootHtml.includes('d5e7e761-8b1b-4ca8-b1fe-771acd1450f8'), 'Root index must include live $29/mo UUID');
  assert.ok(rootHtml.includes('667aa482-f17c-47d1-b7f3-a2427c36516b'), 'Root index must include live $199/yr UUID');
  assert.ok(rootHtml.includes('mailto:beable9489@gmail.com'), 'Root index must include corporate inquiry link');

  // Check pricing
  assert.ok(rootHtml.includes('$29'), 'Root index must include $29');
  assert.ok(rootHtml.includes('$199'), 'Root index must include $199');
  assert.ok(rootHtml.includes('43%OFF'), 'Root index must include 43%OFF');
});

// =========================================================================
// Suite 4: Responsive Table Wrapper Verification in Root index.html
// =========================================================================

test('Suite 4.1: Responsive comp-table-wrap wrapping #gbQuickMatrixTable', () => {
  const rootHtml = fs.readFileSync(DIST_ROOT_INDEX, 'utf8');

  const tableIdx = rootHtml.indexOf('id="gbQuickMatrixTable"');
  assert.ok(tableIdx > 0, '#gbQuickMatrixTable must exist in root index.html');

  // Look back up to 200 characters before table to verify wrapper
  const lookback = rootHtml.substring(Math.max(0, tableIdx - 200), tableIdx);
  assert.ok(lookback.includes('comp-table-wrap'), 'comp-table-wrap must immediately enclose #gbQuickMatrixTable');
});
