/**
 * Adversarial Quantitative Engine & Security Stress Test Suite
 * File: getbreakai/tests/adversarial_breakout_stress.test.js
 * 
 * Disciplines Tested:
 * 1. SMA calculation boundaries, negative periods, zero period, and rolling window precision
 * 2. Wilder RSI edge conditions (monotonic trends, zero delta flatlines, gap spikes, array bounds)
 * 3. Donchian Channel lookback constraints, duplicate highs, negative price highs
 * 4. Price-Weighted RSI (PW-RSI) volume factors, zero volume, negative volume, extreme volume caps
 * 5. Institutional Asymmetric Risk Profile (-9% stop, +18% 2x TP, +15% breakeven trigger, +1% trailing stop)
 * 6. Signal evaluation boundary transitions (exact 1.5x volume, exact 90.0 PW-RSI, exact breakout price)
 * 7. Position lifecycle state machine (hard stop breach, take-profit breach, simultaneous gap bar, breakeven latching)
 * 8. Robustness under NaN, Infinity, negative prices, null/undefined inputs
 */

'use strict';

const assert = require('assert');
const crypto = require('crypto');
const {
  calculateSMA,
  calculateRSI,
  calculateDonchianHigh,
  calculatePwRsi,
  calculateRiskProfile,
  evaluateBreakoutSignal,
  updatePositionStatus
} = require('../src/engine/breakout_engine');

const {
  STORE_CONFIG,
  createCheckoutUrl,
  verifyWebhookSignature,
  parseWebhookEvent
} = require('../src/services/lemonsqueezy');

let totalTests = 0;
let passedTests = 0;
const findings = [];

function challenge(name, fn) {
  totalTests++;
  try {
    fn();
    console.log(`  ✓ [PASS] ${name}`);
    passedTests++;
  } catch (err) {
    console.error(`  ✗ [FAIL] ${name}`);
    console.error(`     Error: ${err.message}`);
    findings.push({ name, error: err.message, stack: err.stack });
  }
}

console.log('========================================================================');
console.log('   EMPIRICAL ADVERSARIAL STRESS TEST SUITE — GETBREAKAI & LEMON SQUEEZY ');
console.log('========================================================================\n');

// -----------------------------------------------------------------------------
// Category 1: SMA Boundaries & Rolling Window Resilience
// -----------------------------------------------------------------------------
console.log('[Category 1: Moving Average Engine Stress Tests]');

challenge('SMA.1: Empty price array returns empty array without throwing', () => {
  const result = calculateSMA([], 20);
  assert.deepStrictEqual(result, []);
});

challenge('SMA.2: Array length shorter than period produces all nulls', () => {
  const prices = [10, 20, 30];
  const result = calculateSMA(prices, 5);
  assert.deepStrictEqual(result, [null, null, null]);
});

challenge('SMA.3: Period = 1 returns prices identical to input array', () => {
  const prices = [10.5, 20.25, 30.75];
  const result = calculateSMA(prices, 1);
  assert.deepStrictEqual(result, [10.5, 20.25, 30.75]);
});

challenge('SMA.4: High-volume stress (100,000 bars) executes with O(N) rolling sum stability', () => {
  const count = 100000;
  const prices = new Array(count).fill(100.0);
  const start = Date.now();
  const sma20 = calculateSMA(prices, 20);
  const elapsed = Date.now() - start;

  assert.strictEqual(sma20.length, count);
  assert.strictEqual(sma20[18], null);
  assert.strictEqual(sma20[19], 100.0);
  assert.strictEqual(sma20[count - 1], 100.0);
  assert(elapsed < 2000, `Execution took ${elapsed}ms, expected < 2000ms`);
});

// -----------------------------------------------------------------------------
// Category 2: Wilder RSI Edge Cases & Smoothing Convergence
// -----------------------------------------------------------------------------
console.log('\n[Category 2: Wilder RSI & PW-RSI Stress Tests]');

challenge('RSI.1: Array shorter than period + 1 returns safe default 50.0 array', () => {
  const closes = [100, 101, 102];
  const result = calculateRSI(closes, 14);
  assert.strictEqual(result.length, 3);
  assert.deepStrictEqual(result, [50.0, 50.0, 50.0]);
});

challenge('RSI.2: Monotonically rising series converges to exactly 100.0', () => {
  const rising = [];
  for (let i = 0; i < 30; i++) rising.push(100 + i * 2);
  const rsi = calculateRSI(rising, 14);
  assert.strictEqual(rsi[rsi.length - 1], 100.0);
});

challenge('RSI.3: Monotonically falling series converges to exactly 0.0', () => {
  const falling = [];
  for (let i = 0; i < 30; i++) falling.push(200 - i * 2);
  const rsi = calculateRSI(falling, 14);
  assert.strictEqual(rsi[rsi.length - 1], 0.0);
});

challenge('RSI.4: Flat price series (zero gain & zero loss) does not crash or return NaN', () => {
  const flat = new Array(30).fill(100.0);
  const rsi = calculateRSI(flat, 14);
  const lastVal = rsi[rsi.length - 1];
  assert(!isNaN(lastVal), 'RSI on flat series must not be NaN');
  assert(lastVal >= 0 && lastVal <= 100, `RSI must be between 0 and 100, got ${lastVal}`);
});

challenge('RSI.5: Extreme price gap (10x overnight gap) maintains [0, 100] bound without overflow', () => {
  const gapSeries = new Array(20).fill(10.0);
  gapSeries.push(10000.0); // 1000x gap
  const rsi = calculateRSI(gapSeries, 14);
  const lastVal = rsi[rsi.length - 1];
  assert(lastVal <= 100.0 && lastVal >= 0.0, `Expected bounded RSI, got ${lastVal}`);
});

challenge('PW-RSI.1: Zero current volume evaluates to exactly 0.0 PW-RSI', () => {
  const pw = calculatePwRsi(70.0, 0, 1000000);
  assert.strictEqual(pw, 0.0);
});

challenge('PW-RSI.2: Zero or negative moving average volume safely falls back to unadjusted RSI', () => {
  assert.strictEqual(calculatePwRsi(65.0, 500000, 0), 65.0);
  assert.strictEqual(calculatePwRsi(65.0, 500000, -100), 65.0);
  assert.strictEqual(calculatePwRsi(65.0, 500000, null), 65.0);
});

challenge('PW-RSI.3: Extreme volume spike (100x average) is capped strictly at 3.0x multiplier', () => {
  const pw = calculatePwRsi(50.0, 100000000, 1000000); // 100x volume
  assert.strictEqual(pw, 150.0); // 50.0 * 3.0 = 150.0
});

// -----------------------------------------------------------------------------
// Category 3: Donchian Channel Lookback & Extreme Highs
// -----------------------------------------------------------------------------
console.log('\n[Category 3: Donchian Channel Boundary Tests]');

challenge('Donchian.1: Lookback period equals array length sets initial values to null', () => {
  const bars = Array.from({ length: 20 }, (_, i) => ({ high: 100 + i }));
  const highs = calculateDonchianHigh(bars, 20);
  assert.strictEqual(highs[19], null);
});

challenge('Donchian.2: Current bar high is excluded from prior N-bar highest high calculation', () => {
  const bars = Array.from({ length: 25 }, () => ({ high: 100 }));
  bars[24].high = 999; // huge breakout on current bar
  const highs = calculateDonchianHigh(bars, 20);
  // Donchian high at index 24 should look at bars 4..23, which all had high = 100
  assert.strictEqual(highs[24], 100);
});

challenge('Donchian.3: All negative prices handle correctly without falling to -Infinity', () => {
  const bars = Array.from({ length: 25 }, (_, i) => ({ high: -100 + i }));
  const highs = calculateDonchianHigh(bars, 20);
  assert.strictEqual(highs[20], -81); // max of bars 0..19 (-100 + 19 = -81)
});

// -----------------------------------------------------------------------------
// Category 4: Asymmetric Risk Engine (-9% Stop & +18% TP Boundaries)
// -----------------------------------------------------------------------------
console.log('\n[Category 4: Asymmetric Risk Profile Mathematical Integrity]');

challenge('Risk.1: Zero or negative entry price throws descriptive Error', () => {
  assert.throws(() => calculateRiskProfile(0), /Valid positive entry price is required/);
  assert.throws(() => calculateRiskProfile(-100), /Valid positive entry price is required/);
  assert.throws(() => calculateRiskProfile(null), /Valid positive entry price is required/);
  assert.throws(() => calculateRiskProfile('100'), /Valid positive entry price is required/);
});

challenge('Risk.2: Exactly 2:1 Reward-to-Risk ratio maintained across broad price ranges', () => {
  const testPrices = [1.00, 10.50, 45.67, 100.00, 345.89, 2500.00];
  for (const p of testPrices) {
    const risk = calculateRiskProfile(p, 9.0, 2.0);
    const expectedStop = Number((p * 0.91).toFixed(2));
    const expectedRiskAmount = Number((p - expectedStop).toFixed(2));
    const expectedTP = Number((p + expectedRiskAmount * 2.0).toFixed(2));

    assert.strictEqual(risk.stopLoss, expectedStop, `Stop mismatch at ${p}`);
    assert.strictEqual(risk.takeProfit, expectedTP, `TP mismatch at ${p}`);
    assert.strictEqual(risk.rewardToRiskRatio, 2.0);
    assert.strictEqual(risk.breakevenTrigger, Number((p * 1.15).toFixed(2)));
    assert.strictEqual(risk.trailingBreakevenStop, Number((p * 1.01).toFixed(2)));
  }
});

challenge('Risk.3: Boundary test: high decimal fraction precision (cents rounding)', () => {
  const entryPrice = 99.99;
  const risk = calculateRiskProfile(entryPrice);
  assert.strictEqual(risk.entryPrice, 99.99);
  assert.strictEqual(risk.stopLoss, 90.99); // 99.99 * 0.91 = 90.9909 -> 90.99
  assert.strictEqual(risk.riskAmount, 9.00); // 99.99 - 90.99 = 9.00
  assert.strictEqual(risk.takeProfit, 117.99); // 99.99 + 2 * 9.00 = 117.99
});

// -----------------------------------------------------------------------------
// Category 5: Breakout Evaluation Signal Precision & Edge Cases
// -----------------------------------------------------------------------------
console.log('\n[Category 5: Signal Evaluation Threshold Boundaries]');

challenge('Signal.1: Exact boundary close == donchianHigh results in NEUTRAL (no breakout yet)', () => {
  const eval1 = evaluateBreakoutSignal({
    close: 100.00,
    high: 101.00,
    volume: 2000000,
    donchianHigh: 100.00, // equal to close
    sma60: 90.00,
    sma20Vol: 1000000,
    rsi: 65.00
  });
  assert.strictEqual(eval1.signal, 'NEUTRAL');
  assert.strictEqual(eval1.isActionable, false);
});

challenge('Signal.2: Breakout with 1 cent above donchianHigh triggers breakout evaluation', () => {
  const eval2 = evaluateBreakoutSignal({
    close: 100.01,
    high: 101.00,
    volume: 2000000,
    donchianHigh: 100.00,
    sma60: 90.00,
    sma20Vol: 1000000, // 2.0x volume factor
    rsi: 65.00         // PW-RSI = 130.0 >= 90.0
  });
  assert.strictEqual(eval2.signal, 'INSTITUTIONAL_IGNITION');
  assert.strictEqual(eval2.isActionable, true);
});

challenge('Signal.3: Volume factor boundary at 1.49x is trapped vs 1.50x is accepted', () => {
  // 1.49x volume factor
  const trapped = evaluateBreakoutSignal({
    close: 105.00,
    high: 106.00,
    volume: 1490000,
    donchianHigh: 100.00,
    sma60: 90.00,
    sma20Vol: 1000000,
    rsi: 65.00
  });
  assert.strictEqual(trapped.signal, 'LOW_VOLUME_TRAP');
  assert.strictEqual(trapped.isActionable, false);

  // 1.50x volume factor
  const accepted = evaluateBreakoutSignal({
    close: 105.00,
    high: 106.00,
    volume: 1500000,
    donchianHigh: 100.00,
    sma60: 90.00,
    sma20Vol: 1000000,
    rsi: 65.00
  });
  assert(accepted.isActionable, 'Volume factor 1.50x must be actionable');
});

challenge('Signal.4: PW-RSI boundary: 89.99 is STANDARD_BREAKOUT vs 90.00 is INSTITUTIONAL_IGNITION', () => {
  // PW-RSI = 59.99 * 1.5 = 89.985 -> 89.99
  const standard = evaluateBreakoutSignal({
    close: 105.00,
    high: 106.00,
    volume: 1500000,
    donchianHigh: 100.00,
    sma60: 90.00,
    sma20Vol: 1000000,
    rsi: 59.99
  });
  assert.strictEqual(standard.signal, 'STANDARD_BREAKOUT');

  // PW-RSI = 60.00 * 1.5 = 90.00
  const ignition = evaluateBreakoutSignal({
    close: 105.00,
    high: 106.00,
    volume: 1500000,
    donchianHigh: 100.00,
    sma60: 90.00,
    sma20Vol: 1000000,
    rsi: 60.00
  });
  assert.strictEqual(ignition.signal, 'INSTITUTIONAL_IGNITION');
});

challenge('Signal.5: Zero volume bar produces LOW_VOLUME_TRAP during breakout price action', () => {
  const zeroVol = evaluateBreakoutSignal({
    close: 105.00,
    high: 106.00,
    volume: 0,
    donchianHigh: 100.00,
    sma60: 90.00,
    sma20Vol: 1000000,
    rsi: 60.00
  });
  assert.strictEqual(zeroVol.signal, 'LOW_VOLUME_TRAP');
  assert.strictEqual(zeroVol.isActionable, false);
});

// -----------------------------------------------------------------------------
// Category 6: Position State Machine & Conflict Resolution
// -----------------------------------------------------------------------------
console.log('\n[Category 6: Position Lifecycle & Gap Bar Resolution]');

challenge('Position.1: Simultaneous gap bar breaching BOTH stop-loss and take-profit defaults to STOP_LOSS', () => {
  const risk = calculateRiskProfile(100.00); // Stop 91.00, TP 118.00
  const position = {
    entryPrice: 100.00,
    currentStopLoss: risk.stopLoss,
    takeProfit: risk.takeProfit,
    riskProfile: risk,
    status: 'ACTIVE',
    isBreakevenArmed: false
  };

  // Ultra-wide volatility bar (low: 80.00 <= 91.00, high: 130.00 >= 118.00)
  const wideBar = { high: 130.00, low: 80.00, close: 125.00 };
  const updated = updatePositionStatus(position, wideBar);

  // Must trigger hard stop-loss first as per risk-averse institutional mandate
  assert.strictEqual(updated.status, 'CLOSED_STOP_LOSS');
  assert.strictEqual(updated.exitPrice, 91.00);
  assert.strictEqual(updated.pnlPercent, -9.00);
});

challenge('Position.2: Closed positions are immutable and terminal', () => {
  const closedPosition = {
    entryPrice: 100.00,
    currentStopLoss: 91.00,
    takeProfit: 118.00,
    status: 'CLOSED_STOP_LOSS',
    exitPrice: 91.00,
    pnlPercent: -9.00
  };

  const nextBar = { high: 150.00, low: 140.00, close: 145.00 };
  const updated = updatePositionStatus(closedPosition, nextBar);

  assert.strictEqual(updated.status, 'CLOSED_STOP_LOSS');
  assert.strictEqual(updated.exitPrice, 91.00);
  assert.strictEqual(updated.pnlPercent, -9.00);
});

challenge('Position.3: Breakeven arming latches and preserves trailing stop on subsequent dip', () => {
  const risk = calculateRiskProfile(100.00); // Stop 91.00, TP 118.00, Breakeven Trigger 115.00, Trailing Stop 101.00
  let position = {
    entryPrice: 100.00,
    currentStopLoss: risk.stopLoss,
    takeProfit: risk.takeProfit,
    riskProfile: risk,
    status: 'ACTIVE',
    isBreakevenArmed: false
  };

  // Bar 1: Reaches 115.50 (+15.5%) -> arms breakeven
  position = updatePositionStatus(position, { high: 115.50, low: 108.00, close: 114.00 });
  assert.strictEqual(position.isBreakevenArmed, true);
  assert.strictEqual(position.currentStopLoss, 101.00);

  // Bar 2: Price dips to 100.50 (breaches original 91 stop, but hits the new 101 stop)
  position = updatePositionStatus(position, { high: 105.00, low: 100.50, close: 102.00 });
  assert.strictEqual(position.status, 'CLOSED_STOP_LOSS');
  assert.strictEqual(position.exitPrice, 101.00);
  assert.strictEqual(position.pnlPercent, 1.00, 'Protected net +1.0% profit on trailing stop exit');
});

// -----------------------------------------------------------------------------
// Category 7: Lemon Squeezy Store Config & Security Invariants
// -----------------------------------------------------------------------------
console.log('\n[Category 7: Lemon Squeezy Enterprise Security & Configuration]');

challenge('Lemon.1: Store ID matches Live Store #296100 exactly', () => {
  assert.strictEqual(STORE_CONFIG.storeId, '296100');
});

challenge('Lemon.2: Support email is strictly beable9489@gmail.com', () => {
  assert.strictEqual(STORE_CONFIG.supportEmail, 'beable9489@gmail.com');
});

challenge('Lemon.3: Webhook HMAC rejects replay attacks with mismatched payload content', () => {
  const secret = 'super_secure_webhook_key_2026';
  const payload1 = JSON.stringify({ event: 'order_created', id: 'ord_1', total: 1000 });
  const payload2 = JSON.stringify({ event: 'order_created', id: 'ord_2', total: 1000 });

  const hmac1 = crypto.createHmac('sha256', secret).update(payload1).digest('hex');
  assert.strictEqual(verifyWebhookSignature(payload1, hmac1, secret), true);
  assert.strictEqual(verifyWebhookSignature(payload2, hmac1, secret), false);
});

challenge('Lemon.4: Null bytes or malformed characters in signature header handled safely', () => {
  const secret = 'webhook_key';
  const payload = '{"test":true}';
  assert.strictEqual(verifyWebhookSignature(payload, '\0'.repeat(64), secret), false);
  assert.strictEqual(verifyWebhookSignature(payload, 'undefined', secret), false);
  assert.strictEqual(verifyWebhookSignature(payload, 'NaN', secret), false);
});

challenge('Lemon.5: Checkout URL generation strictly URL-encodes user email and parameters', () => {
  const url = createCheckoutUrl('starter_monthly', {
    userEmail: 'attacker+inject@evil.com?param=hacked#hash',
    userId: 'usr_<script>alert(1)</script>'
  });

  assert(!url.includes('<script>'), 'XSS vectors must be URL encoded');
  assert(url.includes('attacker%2Binject%40evil.com'), 'Email characters must be URL encoded');
});

// -----------------------------------------------------------------------------
// Summary & Verdict
// -----------------------------------------------------------------------------
console.log('\n========================================================================');
console.log(`Adversarial Stress Test Results: ${passedTests} / ${totalTests} Passed`);
console.log(`Failures/Findings: ${findings.length}`);
console.log('========================================================================\n');

if (findings.length > 0) {
  console.error('Critical findings encountered during empirical challenge:');
  findings.forEach(f => console.error(` - [${f.name}]: ${f.error}`));
  process.exit(1);
} else {
  console.log('Engine successfully passed all adversarial quantitative & security stress tests!');
}
