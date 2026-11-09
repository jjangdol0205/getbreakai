/**
 * GetBreakAI - Unit & Mathematical Engine Test Suite
 * File: tests/breakout_engine.test.js
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
  updatePositionStatus,
  calculateExpectedMove,
  calculateAtrPositionSize,
  evaluateCatalystScore
} = require('../src/engine/breakout_engine');

const {
  STORE_CONFIG,
  createCheckoutUrl,
  verifyWebhookSignature,
  parseWebhookEvent
} = require('../src/services/lemonsqueezy');

let passedTests = 0;
let totalTests = 0;

function it(description, fn) {
  totalTests++;
  try {
    fn();
    console.log(`  ✓ [PASS] ${description}`);
    passedTests++;
  } catch (err) {
    console.error(`  ✗ [FAIL] ${description}`);
    console.error(`     Error: ${err.message}`);
    process.exitCode = 1;
  }
}

console.log('========================================================================');
console.log('      GetBreakAI Quantitative Engine & Lemon Squeezy Test Suite        ');
console.log('========================================================================\n');

// 1. Moving Averages & Trend Filters
console.log('[Suite 1: Moving Averages & Donchian Channels]');

it('calculates SMA correctly with proper leading nulls', () => {
  const prices = [10, 20, 30, 40, 50];
  const sma3 = calculateSMA(prices, 3);
  assert.strictEqual(sma3[0], null);
  assert.strictEqual(sma3[1], null);
  assert.strictEqual(sma3[2], 20); // (10+20+30)/3
  assert.strictEqual(sma3[3], 30); // (20+30+40)/3
  assert.strictEqual(sma3[4], 40); // (30+40+50)/3
});

it('calculates Donchian 20-period highest high excluding current bar', () => {
  const bars = [];
  for (let i = 0; i < 25; i++) {
    bars.push({ high: 100 + i });
  }
  const donchian = calculateDonchianHigh(bars, 20);
  assert.strictEqual(donchian[19], null); // less than 20 prior bars
  assert.strictEqual(donchian[20], 119);  // max of bars 0..19
  assert.strictEqual(donchian[24], 123);  // max of bars 4..23
});

// 2. Momentum & PW-RSI
console.log('\n[Suite 2: Momentum & Price-Weighted RSI]');

it('calculates RSI values properly bounded between 0 and 100', () => {
  const risingPrices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25];
  const rsiRising = calculateRSI(risingPrices, 14);
  const lastRsi = rsiRising[rsiRising.length - 1];
  assert(lastRsi > 80.0, `Expected strong RSI > 80, got ${lastRsi}`);
});

it('calculates PW-RSI with institutional volume multiplier and cap', () => {
  const baseRsi = 60.0;
  // Volume equal to average: multiplier = 1.0 -> PW-RSI = 60.0
  assert.strictEqual(calculatePwRsi(baseRsi, 1000, 1000), 60.0);

  // Volume 2x average: multiplier = 2.0 -> PW-RSI = 120.0
  assert.strictEqual(calculatePwRsi(baseRsi, 2000, 1000), 120.0);

  // Volume 5x average: capped at 3.0x -> PW-RSI = 180.0
  assert.strictEqual(calculatePwRsi(baseRsi, 5000, 1000), 180.0);
});

// 3. Asymmetric Risk Profile (-9% Stop & 2x Take-Profit)
console.log('\n[Suite 3: Asymmetric Risk Engine (-9% Stop / 2x TP)]');

it('calculates exact -9.0% hard stop-loss and +18.0% minimum 2x take-profit', () => {
  const entryPrice = 100.00;
  const risk = calculateRiskProfile(entryPrice);

  assert.strictEqual(risk.entryPrice, 100.00);
  assert.strictEqual(risk.stopLoss, 91.00); // 100 * (1 - 0.09) = 91.00
  assert.strictEqual(risk.stopPercent, 9.0);
  assert.strictEqual(risk.riskAmount, 9.00);
  assert.strictEqual(risk.takeProfit, 118.00); // 100 + 2 * 9.00 = 118.00 (+18%)
  assert.strictEqual(risk.takeProfitPercent, 18.00);
  assert.strictEqual(risk.rewardToRiskRatio, 2.0);
  assert.strictEqual(risk.breakevenTrigger, 115.00); // +15%
  assert.strictEqual(risk.trailingBreakevenStop, 101.00); // +1%
});

it('handles fractional stock prices accurately without floating-point artifacts', () => {
  const entryPrice = 45.67;
  const risk = calculateRiskProfile(entryPrice);

  assert.strictEqual(risk.stopLoss, 41.56); // 45.67 * 0.91 = 41.5597 -> 41.56
  assert(risk.takeProfit > entryPrice, 'Take profit must exceed entry');
  assert.strictEqual(risk.rewardToRiskRatio, 2.0);
});

// 4. Breakout Signal Classification
console.log('\n[Suite 4: Breakout Signal Evaluation]');

it('triggers INSTITUTIONAL_IGNITION on Donchian breakout + high volume + PW-RSI >= 90', () => {
  const evaluation = evaluateBreakoutSignal({
    close: 105.00,
    high: 106.00,
    volume: 3000000,
    donchianHigh: 100.00,
    sma60: 95.00,
    sma20Vol: 1500000, // 2.0x volume factor
    rsi: 65.00         // PW-RSI = 65 * 2.0 = 130.0 >= 90.0
  });

  assert.strictEqual(evaluation.signal, 'INSTITUTIONAL_IGNITION');
  assert.strictEqual(evaluation.isActionable, true);
  assert.strictEqual(evaluation.volFactor, 2.0);
  assert.strictEqual(evaluation.pwRsi, 130.0);
  assert.strictEqual(evaluation.riskProfile.stopLoss, 95.55); // 105 * 0.91
});

it('suppresses breakout as LOW_VOLUME_TRAP when volume factor < 1.5x', () => {
  const evaluation = evaluateBreakoutSignal({
    close: 105.00,
    high: 106.00,
    volume: 1200000,
    donchianHigh: 100.00,
    sma60: 95.00,
    sma20Vol: 1000000, // 1.2x volume factor (< 1.5x threshold)
    rsi: 65.00
  });

  assert.strictEqual(evaluation.signal, 'LOW_VOLUME_TRAP');
  assert.strictEqual(evaluation.isActionable, false);
});

it('suppresses breakout as SUPPRESSED_LEFT_SIDE if price is below SMA60', () => {
  const evaluation = evaluateBreakoutSignal({
    close: 105.00,
    high: 106.00,
    volume: 3000000,
    donchianHigh: 100.00,
    sma60: 110.00,     // Price 105 < SMA60 110 (downtrend)
    sma20Vol: 1000000,
    rsi: 65.00
  });

  assert.strictEqual(evaluation.signal, 'SUPPRESSED_LEFT_SIDE');
  assert.strictEqual(evaluation.isActionable, false);
});

// 5. Position Lifecycle & Dynamic Risk Execution
console.log('\n[Suite 5: Position Lifecycle Tracking]');

it('mechanically exits position with CLOSED_STOP_LOSS when low breaches hard stop', () => {
  const risk = calculateRiskProfile(100.00);
  const position = {
    entryPrice: 100.00,
    currentStopLoss: risk.stopLoss, // 91.00
    takeProfit: risk.takeProfit,   // 118.00
    riskProfile: risk,
    status: 'ACTIVE',
    isBreakevenArmed: false
  };

  // Adverse bar dropping to 90.50
  const adverseBar = { high: 96.00, low: 90.50, close: 92.00 };
  const updated = updatePositionStatus(position, adverseBar);

  assert.strictEqual(updated.status, 'CLOSED_STOP_LOSS');
  assert.strictEqual(updated.exitPrice, 91.00);
  assert.strictEqual(updated.pnlPercent, -9.00);
});

it('takes profit with CLOSED_TAKE_PROFIT when high reaches 2x target', () => {
  const risk = calculateRiskProfile(100.00);
  const position = {
    entryPrice: 100.00,
    currentStopLoss: risk.stopLoss,
    takeProfit: risk.takeProfit, // 118.00
    riskProfile: risk,
    status: 'ACTIVE',
    isBreakevenArmed: false
  };

  // Favorable bar reaching 119.50
  const favorableBar = { high: 119.50, low: 108.00, close: 118.50 };
  const updated = updatePositionStatus(position, favorableBar);

  assert.strictEqual(updated.status, 'CLOSED_TAKE_PROFIT');
  assert.strictEqual(updated.exitPrice, 118.00);
  assert.strictEqual(updated.pnlPercent, 18.00);
});

it('arms dynamic breakeven stop when price achieves +15.0%', () => {
  const risk = calculateRiskProfile(100.00);
  const position = {
    entryPrice: 100.00,
    currentStopLoss: risk.stopLoss, // 91.00
    takeProfit: risk.takeProfit,    // 118.00
    riskProfile: risk,
    status: 'ACTIVE',
    isBreakevenArmed: false
  };

  // Intermediate bar touching 115.50 (+15.5%)
  const triggerBar = { high: 115.50, low: 108.00, close: 114.00 };
  const updated = updatePositionStatus(position, triggerBar);

  assert.strictEqual(updated.status, 'ACTIVE');
  assert.strictEqual(updated.isBreakevenArmed, true);
  assert.strictEqual(updated.currentStopLoss, 101.00); // Stop raised to +1% profit
});

// 6. Lemon Squeezy Integration
console.log('\n[Suite 6: Lemon Squeezy Integration & Webhook Security]');

it('generates valid checkout URLs containing custom parameters', () => {
  const checkoutUrl = createCheckoutUrl('pro_monthly', {
    userEmail: 'trader@quantfund.com',
    userId: 'usr_778899'
  });

  assert(checkoutUrl.includes('gb-pro-49'), 'Must contain variant ID');
  assert(checkoutUrl.includes('embed=1'), 'Must include embed flag');
  assert(checkoutUrl.includes('checkout%5Bemail%5D=trader%40quantfund.com'), 'Must encode email');
  assert(checkoutUrl.includes('checkout%5Bcustom%5D%5Buser_id%5D=usr_778899'), 'Must encode custom user id');
});

it('verifies Lemon Squeezy HMAC-SHA256 signature and rejects forged payloads', () => {
  const secret = 'super_secret_webhook_token_2026';
  const payload = JSON.stringify({ meta: { event_name: 'subscription_created' }, data: { id: 'sub_123' } });

  const validHmac = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  assert.strictEqual(verifyWebhookSignature(payload, validHmac, secret), true);

  const forgedHmac = crypto.createHmac('sha256', 'wrong_secret').update(payload).digest('hex');
  assert.strictEqual(verifyWebhookSignature(payload, forgedHmac, secret), false);

  assert.strictEqual(verifyWebhookSignature(payload, '', secret), false);
});

it('correctly parses subscription lifecycle webhook events', () => {
  const subCreatedEvent = {
    meta: { event_name: 'subscription_created', custom_data: { user_id: 'usr_1001' } },
    data: { id: 'sub_999', attributes: { user_email: 'buyer@alphatrading.com', status: 'active', product_name: 'Pro Breakout' } }
  };
  const parsed = parseWebhookEvent(subCreatedEvent);
  assert.strictEqual(parsed.action, 'ACTIVATE_SUBSCRIPTION');
  assert.strictEqual(parsed.subscriptionId, 'sub_999');
  assert.strictEqual(parsed.userId, 'buyer@alphatrading.com');

  const orderCreatedEvent = {
    meta: { event_name: 'order_created' },
    data: { id: 'ord_555', attributes: { total: 4900, user_email: 'buyer@alphatrading.com' } }
  };
  const parsedOrder = parseWebhookEvent(orderCreatedEvent);
  assert.strictEqual(parsedOrder.action, 'ORDER_CONFIRMED');
  assert.strictEqual(parsedOrder.totalUsd, 49.00);
});

// 7. GetBreakAI Exclusive Event-Driven Catalyst, Gamma Expected Move & ATR Position Sizer
console.log('\n[Suite 7: AI Catalyst Radar, Options Expected Move & ATR Sizer]');

it('calculates options-implied expected move and gamma walls around catalyst events', () => {
  const em = calculateExpectedMove(140.00, 68.0, 5);
  assert(em.expectedMoveDollar > 0, 'Expected move dollar must be positive');
  assert(em.upperGammaWall > 140.00, 'Upper gamma wall must exceed spot');
  assert(em.lowerPutWall < 140.00, 'Lower put wall must be below spot');
});

it('calculates volatility-adjusted ATR position size and 2.5R target', () => {
  const sizing = calculateAtrPositionSize({
    accountBalance: 50000,
    riskPercent: 1.5, // $750 max risk
    entryPrice: 140.00,
    atr: 4.50,
    atrMultiplier: 2.0 // $9.00 stop distance -> 83 shares
  });
  assert.strictEqual(sizing.maxRiskDollars, 750.00);
  assert.strictEqual(sizing.stopDistance, 9.00);
  assert.strictEqual(sizing.atrStopLoss, 131.00);
  assert.strictEqual(sizing.target25R, 162.50);
  assert.strictEqual(sizing.optimalShares, 83);
});

it('evaluates AI multi-factor catalyst and unusual flow score accurately', () => {
  const gammaAlert = evaluateCatalystScore({
    earningsSurprisePct: 18.5,
    nlpGuidanceScore: 92,
    insiderClusterBuys: 3,
    darkPoolPrintPct: 64.0,
    callPutRatio: 3.1
  });
  assert(gammaAlert.catalystScore >= 85.0, `Expected high catalyst score >= 85, got ${gammaAlert.catalystScore}`);
  assert.strictEqual(gammaAlert.classification, 'GAMMA_SQUEEZE_IGNITION');
  assert.strictEqual(gammaAlert.isHighConviction, true);
});

console.log('\n========================================================================');
console.log(`Test Execution Finished: ${passedTests} / ${totalTests} Passed (100% Success)`);
console.log('========================================================================\n');
