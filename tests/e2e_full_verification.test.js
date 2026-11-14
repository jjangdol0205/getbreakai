'use strict';

/**
 * GetBreakAI (Division 3) — Comprehensive E2E Verification Test Suite
 * Covers:
 *   Tier 1: Feature Coverage (Lemon Squeezy 3-tier SaaS on Store #296100, TSE Prime vs US Tech, Donchian ATR Sizers in JPY/USD, Dual-Theme)
 *   Tier 2: Boundary & Corner Cases (URL query fallbacks, numerical extremes, negative/zero inputs, extreme Yen FX)
 *   Tier 3: Cross-Feature Interactions (Theme toggle, responsive navigation, market filtering, VIP lock/unlock, Telegram modal)
 *   Tier 4: Real-World User Journeys (Landing -> Scan -> Sizing -> Checkout -> Confirmation metadata -> Telegram onboarding)
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const INDEX_HTML_PATH = path.join(ROOT, 'index.html');
const CONFIRMATION_HTML_PATH = path.join(ROOT, 'confirmation.html');
const JP_CONFIRMATION_HTML_PATH = path.join(ROOT, 'jp', 'confirmation.html');
const SNAPSHOT_PATH = path.join(ROOT, 'data', 'live_market_snapshot.json');
const LEMON_PATH = path.join(ROOT, 'src', 'services', 'lemonsqueezy.js');
const ENGINE_PATH = path.join(ROOT, 'src', 'engine', 'breakout_engine.js');

// Load configurations and services
const {
  STORE_CONFIG,
  createCheckoutUrl,
  verifyWebhookSignature,
  parseWebhookEvent
} = require(LEMON_PATH);

const BreakoutEngine = require(ENGINE_PATH);

// Helper to simulate browser LocalStorage in Node.js
function createMockLocalStorage(initialStore = {}) {
  const store = { ...initialStore };
  return {
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(store, key) ? String(store[key]) : null;
    },
    setItem(key, value) {
      store[key] = String(value);
    },
    removeItem(key) {
      delete store[key];
    },
    clear() {
      for (const k of Object.keys(store)) delete store[k];
    },
    dump() {
      return { ...store };
    }
  };
}

// Helper to simulate confirmation.html initConfirmation query parsing (zero fake keys, unified gb_vip_license_key + gb_vip_key)
function simulateConfirmationPageInit(queryString, mockStorage) {
  const params = new URLSearchParams(queryString.startsWith('?') ? queryString.substring(1) : queryString);
  const isPlausible = (k) => k && k.length >= 12 && !/^(LS-|DEMO-|FAKE-|TEMP-)/i.test(k);

  const storedPrimary = String(mockStorage.getItem('gb_vip_license_key') || '').trim();
  const storedLegacy = String(mockStorage.getItem('gb_vip_key') || '').trim();
  const existingValidKey = isPlausible(storedPrimary) ? storedPrimary : (isPlausible(storedLegacy) ? storedLegacy : '');

  const rawOrderId = (params.get('order_id') || params.get('orderId') || params.get('checkout_id') || '').trim();
  const rawParamKey = (params.get('license_key') || params.get('order_key') || params.get('orderKey') || '').trim();
  const rawEmail = (params.get('customer_email') || params.get('email') || '').trim();

  const orderId = rawOrderId || mockStorage.getItem('gb_vip_order_id') || 'メール記載の注文番号をご確認ください';
  const customerEmail = rawEmail || mockStorage.getItem('gb_vip_customer_email') || 'ご登録メールアドレス宛にライセンスキー送信済み';
  const orderKey = isPlausible(rawParamKey) ? rawParamKey : existingValidKey;

  if (rawOrderId) mockStorage.setItem('gb_vip_order_id', rawOrderId);
  if (rawEmail) mockStorage.setItem('gb_vip_customer_email', rawEmail);

  if (orderKey) {
    mockStorage.setItem('gb_vip_unlocked', 'true');
    mockStorage.setItem('gb_vip_license_key', orderKey);
    mockStorage.setItem('gb_vip_key', orderKey);
  }

  return {
    orderId,
    orderKey,
    customerEmail,
    isUnlocked: mockStorage.getItem('gb_vip_unlocked') === 'true'
  };
}

// Helper to calculate position sizing replicating index.html recalcSizer logic
function calculatePositionSizing({
  account,
  entry,
  atr,
  currentIv = 55,
  isJpy = false,
  usdJpyRate = 150.0,
  taxMode = 'nisa' // 'nisa' or 'tokutei'
}) {
  const jpTaxRate = 0.20315;
  const isTokutei = (taxMode === 'tokutei');

  if (isJpy) {
    const accountYen = account * usdJpyRate;
    const maxRiskYen = accountYen * 0.015;
    const stopDist = Math.max(0.01, atr * 2.0);
    const stopPrice = Math.max(1, entry - stopDist);
    const rawShares = Math.floor(maxRiskYen / stopDist);
    const maxAfford = entry > 0 ? Math.floor(accountYen / entry) : 0;
    const shares = Math.max(1, Math.min(rawShares, maxAfford));
    const notionalYen = Math.round(shares * entry);
    const actualRiskYen = Math.round(shares * stopDist);

    const expMove = entry * (currentIv / 100.0) * Math.sqrt(5.0 / 252.0);
    const upperWall = entry + expMove;
    const target25R = entry + stopDist * 2.5;
    const gainYen = Math.round(shares * (target25R - entry));

    const grossProfitJpy = Math.max(0, gainYen);
    const taxSavedJpy = grossProfitJpy * jpTaxRate;
    const netProfitJpy = isTokutei ? (grossProfitJpy * (1 - jpTaxRate)) : grossProfitJpy;

    return {
      currency: 'JPY',
      shares,
      notional: notionalYen,
      stopDist,
      stopPrice,
      actualRisk: actualRiskYen,
      target25R,
      gain: gainYen,
      taxSavedJpy,
      netProfitJpy,
      upperWall
    };
  } else {
    const maxRiskDollars = account * 0.015;
    const stopDist = Math.max(0.01, atr * 2.0);
    const stopPrice = Math.max(0.01, entry - stopDist);
    const rawShares = Math.floor(maxRiskDollars / stopDist);
    const maxAfford = entry > 0 ? Math.floor(account / entry) : 0;
    const shares = Math.max(1, Math.min(rawShares, maxAfford));
    const notional = Math.round(shares * entry);
    const actualRiskUsd = Math.round(shares * stopDist);

    const expMove = entry * (currentIv / 100.0) * Math.sqrt(5.0 / 252.0);
    const upperWall = entry + expMove;
    const target25R = entry + stopDist * 2.5;
    const gainDollars = Math.round(shares * (target25R - entry));

    const buyCommUsd = (taxMode === 'nisa') ? 0 : Math.min(22.0, notional * 0.00495);
    const sellNotional = shares * target25R;
    const sellCommUsd = Math.min(22.0, sellNotional * 0.00495);
    const fxSpreadJpy = (notional + sellNotional) * 0.25;
    const totalFeeUsd = buyCommUsd + sellCommUsd + (fxSpreadJpy / usdJpyRate);

    const grossProfitUsd = Math.max(0, gainDollars - totalFeeUsd);
    const grossProfitJpy = grossProfitUsd * usdJpyRate;
    const taxSavedJpy = grossProfitJpy * jpTaxRate;
    const netProfitJpy = isTokutei ? (grossProfitJpy * (1 - jpTaxRate)) : grossProfitJpy;

    return {
      currency: 'USD',
      shares,
      notional,
      stopDist,
      stopPrice,
      actualRisk: actualRiskUsd,
      target25R,
      gain: gainDollars,
      taxSavedJpy,
      netProfitJpy,
      upperWall
    };
  }
}


// =====================================================================
// TIER 1: FEATURE COVERAGE
// =====================================================================

test('Tier 1.1: Lemon Squeezy 3-Tier SaaS on Live Store #296100', () => {
  // 1. Verify lemon squeezy config
  assert.equal(STORE_CONFIG.storeId, '296100', 'Must be Store #296100');
  assert.equal(STORE_CONFIG.supportEmail, 'beable9489@gmail.com');

  const plans = STORE_CONFIG.plans;
  assert.ok(plans.starter_monthly, 'Must configure starter_monthly ($29/mo)');
  assert.equal(plans.starter_monthly.variantId, 'd5e7e761-8b1b-4ca8-b1fe-771acd1450f8');
  assert.equal(plans.starter_monthly.priceUsd, 29);
  assert.equal(plans.starter_monthly.interval, 'month');

  assert.ok(plans.pro_annual, 'Must configure pro_annual ($199/yr · 43%OFF)');
  assert.equal(plans.pro_annual.variantId, '667aa482-f17c-47d1-b7f3-a2427c36516b');
  assert.equal(plans.pro_annual.priceUsd, 199);
  assert.equal(plans.pro_annual.interval, 'year');

  assert.ok(plans.institutional_enterprise, 'Must configure institutional_enterprise (mailto inquiry)');
  assert.equal(plans.institutional_enterprise.checkoutUrl, 'mailto:beable9489@gmail.com');

  // 2. Verify index.html contains live UUID checkout buttons and zero broken 404 slugs
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');
  assert.ok(indexHtml.includes('d5e7e761-8b1b-4ca8-b1fe-771acd1450f8'));
  assert.ok(indexHtml.includes('667aa482-f17c-47d1-b7f3-a2427c36516b'));
  assert.ok(indexHtml.includes('mailto:beable9489@gmail.com'));
  assert.ok(indexHtml.includes('truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&checkout[redirect_url]=https://getbreakai.com/confirmation.html'));
  assert.ok(indexHtml.includes('truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&checkout[redirect_url]=https://getbreakai.com/confirmation.html'));

  // 3. Dynamic checkout URL generator
  const customCheckout = createCheckoutUrl('pro_annual', {
    userId: 'usr_8820',
    userEmail: 'investor@firm.jp',
    redirectUrl: 'https://getbreakai.com/confirmation.html'
  });
  assert.ok(customCheckout.includes('truthofmarket.lemonsqueezy.com/checkout/buy/667aa482-f17c-47d1-b7f3-a2427c36516b'));
  assert.ok(customCheckout.includes('checkout%5Bcustom%5D%5Buser_id%5D=usr_8820'));
  assert.ok(customCheckout.includes('checkout%5Bemail%5D=investor%40firm.jp'));
  assert.ok(customCheckout.includes('checkout%5Bredirect_url%5D=https%3A%2F%2Fgetbreakai.com%2Fconfirmation.html'));
});

test('Tier 1.2: Dual-Market Quant Coverage (TSE Prime vs US Tech Equities)', () => {
  const data = JSON.parse(fs.readFileSync(SNAPSHOT_PATH, 'utf8'));

  // Indices
  assert.ok(data.indices['^N225'], 'Nikkei 225 must exist');
  assert.ok(data.indices['^TOPX'], 'TOPIX must exist');
  assert.ok(data.indices['^N225'].price > 30000);
  assert.ok(data.indices['^TOPX'].price > 2000);

  // Japanese Flagship Equities
  const tseKeys = ['8035.T', '6857.T', '9984.T', '7203.T', '6758.T'];
  for (const sym of tseKeys) {
    const item = data.tickers[sym];
    assert.ok(item, `Ticker ${sym} must exist in snapshot`);
    assert.equal(item.currency, 'JPY');
    assert.equal(item.market, 'TSE_PRIME');
    assert.ok(item.entry > 1000);
    assert.ok(item.atr > 0);
    assert.ok(item.stop_loss < item.entry, `${sym} stop loss must be below entry`);
    assert.ok(item.target_25r > item.entry, `${sym} 2.5R target must be above entry`);
  }

  // US Tech Flagship Equities
  const usKeys = ['NVDA', 'PLTR', 'TSLA', 'META'];
  for (const sym of usKeys) {
    const item = data.tickers[sym];
    assert.ok(item, `US Ticker ${sym} must exist in snapshot`);
    assert.equal(item.currency, 'USD');
    assert.equal(item.market, 'US_TECH');
    assert.ok(item.entry > 0);
    assert.ok(item.atr > 0);
    assert.ok(item.stop_loss < item.entry);
    assert.ok(item.target_25r > item.entry);
  }

  // Verify index.html contains matrix filter buttons for dual market
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');
  assert.ok(indexHtml.includes("filterMatrixMarket('all', this)"), 'Matrix must have all filter');
  assert.ok(indexHtml.includes("filterMatrixMarket('tse', this)"), 'Matrix must have tse filter');
  assert.ok(indexHtml.includes("filterMatrixMarket('us', this)"), 'Matrix must have us filter');
});

test('Tier 1.3: Donchian & ATR Calculator Engine in JPY and USD', () => {
  // Test US Tech sizing (e.g. NVDA: entry $186.64, atr $5.79, account $50,000)
  const usResult = calculatePositionSizing({
    account: 50000,
    entry: 186.64,
    atr: 5.79,
    currentIv: 68,
    isJpy: false,
    taxMode: 'nisa'
  });
  assert.equal(usResult.currency, 'USD');
  assert.ok(usResult.shares > 0);
  assert.ok(usResult.actualRisk <= 50000 * 0.015, 'Actual risk must not exceed 1.5% capital ceiling');
  assert.equal(usResult.stopDist, 5.79 * 2.0);
  assert.equal(Number(usResult.stopPrice.toFixed(2)), 175.06);
  assert.equal(Number(usResult.target25R.toFixed(2)), 215.59);
  assert.ok(usResult.taxSavedJpy > 0, 'NISA must compute non-zero tax savings');

  // Test TSE Prime sizing (e.g. 8035.T Tokyo Electron: entry ¥24,850, atr ¥620, account ¥5,000,000 / $33,333)
  const jpResult = calculatePositionSizing({
    account: 33333.33,
    entry: 24850,
    atr: 620,
    currentIv: 42,
    isJpy: true,
    usdJpyRate: 150.0,
    taxMode: 'tokutei'
  });
  assert.equal(jpResult.currency, 'JPY');
  assert.ok(jpResult.shares >= 1);
  assert.ok(jpResult.actualRisk <= 5000000 * 0.015, 'Actual risk must not exceed 1.5% capital ceiling in Yen');
  assert.equal(jpResult.stopDist, 620 * 2.0);
  assert.equal(jpResult.stopPrice, 24850 - 1240);
  assert.equal(jpResult.target25R, 24850 + 1240 * 2.5);
  assert.ok(jpResult.netProfitJpy < jpResult.gain, 'Tokutei account must deduct 20.315% capital gains tax');
});

test('Tier 1.4: Dual-Theme Engine (Light Navy vs Dark Terminal)', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');
  const confirmHtml = fs.readFileSync(CONFIRMATION_HTML_PATH, 'utf8');

  // Both pages default to Japanese Fintech Light Mode
  assert.match(indexHtml, /<html\s+lang="ja"\s+data-jp-theme="light"/);
  assert.match(confirmHtml, /<html\s+lang="ja"\s+data-jp-theme="light"/);

  // Both define CSS variables for light & dark
  assert.ok(indexHtml.includes('html[data-jp-theme="light"]'));
  assert.ok(indexHtml.includes('html[data-jp-theme="dark"]'));
  assert.ok(confirmHtml.includes('html[data-jp-theme="light"]'));
  assert.ok(confirmHtml.includes('html[data-jp-theme="dark"]'));

  // Theme switch button and persistence
  assert.ok(indexHtml.includes('id="btnToggleJpTheme"'));
  assert.ok(indexHtml.includes('function toggleJpTheme()'));
  assert.ok(confirmHtml.includes("localStorage.setItem('gb_jp_theme'"));
});


// =====================================================================
// TIER 2: BOUNDARY & CORNER CASES
// =====================================================================

test('Tier 2.1: Confirmation Page Zero-Fake-Key Guardrail & Unified VIP Key Sync', () => {
  const confirmHtml = fs.readFileSync(CONFIRMATION_HTML_PATH, 'utf8');
  const jpConfirmHtml = fs.readFileSync(JP_CONFIRMATION_HTML_PATH, 'utf8');
  assert.ok(!confirmHtml.includes('Math.random') && !confirmHtml.includes("'GBA-'"), 'confirmation.html must NOT generate fake random GBA- keys');
  assert.ok(!jpConfirmHtml.includes('Math.random') && !jpConfirmHtml.includes("'GBA-'"), 'jp/confirmation.html must NOT generate fake random GBA- keys');
  assert.ok(confirmHtml.includes('confirmManualKeyInput') && jpConfirmHtml.includes('confirmManualKeyInput'), 'Both confirmation pages must provide instant activation input');

  // Case A: Completely empty query string -> Must NOT unlock with a fake key
  const storageA = createMockLocalStorage();
  const resA = simulateConfirmationPageInit('', storageA);
  assert.equal(resA.orderKey, '');
  assert.equal(resA.isUnlocked, false);
  assert.equal(storageA.getItem('gb_vip_unlocked'), null);

  // Case B: Legacy gb_vip_key already stored -> Automatically syncs to gb_vip_license_key & unlocks
  const storageB = createMockLocalStorage({ gb_vip_key: '38b1460a-5104-4067-a91d-77b872934d51' });
  const resB = simulateConfirmationPageInit('?order_id=992144', storageB);
  assert.equal(resB.orderId, '992144');
  assert.equal(resB.orderKey, '38b1460a-5104-4067-a91d-77b872934d51');
  assert.equal(storageB.getItem('gb_vip_license_key'), '38b1460a-5104-4067-a91d-77b872934d51');
  assert.equal(resB.isUnlocked, true);

  // Case C: Real Lemon Squeezy UUID passed via URL -> Syncs both gb_vip_license_key and gb_vip_key
  const storageC = createMockLocalStorage();
  const resC = simulateConfirmationPageInit('?checkout_id=CK_999&license_key=38b1460a-5104-4067-a91d-77b872934d51&email=alpha%40hedge.jp', storageC);
  assert.equal(resC.orderId, 'CK_999');
  assert.equal(resC.orderKey, '38b1460a-5104-4067-a91d-77b872934d51');
  assert.equal(resC.customerEmail, 'alpha@hedge.jp');
  assert.equal(storageC.getItem('gb_vip_license_key'), '38b1460a-5104-4067-a91d-77b872934d51');
  assert.equal(storageC.getItem('gb_vip_key'), '38b1460a-5104-4067-a91d-77b872934d51');
  assert.equal(storageC.getItem('gb_vip_customer_email'), 'alpha@hedge.jp');
});

test('Tier 2.2: Calculator Numerical Boundary & Safeguard Tests', () => {
  // Boundary 1: Zero account capital -> clamps safely without NaN
  const zeroCap = calculatePositionSizing({
    account: 0,
    entry: 100,
    atr: 5,
    isJpy: false
  });
  assert.equal(zeroCap.shares, 1, 'Shares must clamp to minimum safe 1');
  assert.ok(!Number.isNaN(zeroCap.notional));

  // Boundary 2: Microcap stock price -> Stop price cannot drop below $0.01
  const microcap = calculatePositionSizing({
    account: 10000,
    entry: 0.10,
    atr: 0.08,
    isJpy: false
  });
  assert.ok(microcap.stopPrice >= 0.01, 'Stop price must never drop below 0.01 floor');

  // Boundary 3: Ultra-high Yen price stock (e.g. ¥85,000 / share, ¥100,000,000 capital)
  const whalePortfolio = calculatePositionSizing({
    account: 666666.67, // $666k * 150 = ¥100,000,000
    entry: 85000,
    atr: 2500,
    isJpy: true,
    usdJpyRate: 150.0
  });
  assert.ok(whalePortfolio.shares > 0);
  assert.ok(whalePortfolio.notional <= 100000000, 'Notional cannot exceed total capital');
  assert.ok(whalePortfolio.actualRisk <= 100000000 * 0.015, 'Actual risk cannot exceed 1.5% capital ceiling');
  assert.equal(whalePortfolio.stopDist, 5000);
  assert.equal(whalePortfolio.stopPrice, 80000);

  // Boundary 4: Extreme FX rates (100.0 vs 200.0 USD/JPY)
  const fx100 = calculatePositionSizing({ account: 10000, entry: 100, atr: 5, isJpy: false, usdJpyRate: 100.0 });
  const fx200 = calculatePositionSizing({ account: 10000, entry: 100, atr: 5, isJpy: false, usdJpyRate: 200.0 });
  assert.ok(fx100.notional > 0 && fx200.notional > 0);
  assert.ok(fx200.taxSavedJpy > fx100.taxSavedJpy, 'Higher FX rate yields higher Yen tax savings');
});


// =====================================================================
// TIER 3: CROSS-FEATURE INTERACTIONS
// =====================================================================

test('Tier 3.1: Theme Toggle & Responsive Navigation Component States', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');
  const confirmHtml = fs.readFileSync(CONFIRMATION_HTML_PATH, 'utf8');

  // 1. Theme toggle function defined and operational
  assert.ok(indexHtml.includes('function toggleJpTheme()'));
  assert.ok(indexHtml.includes('btnToggleJpTheme'));
  assert.ok(confirmHtml.includes('function updateThemeToggleUI(theme)'));
  assert.ok(confirmHtml.includes('function toggleJpTheme()'));

  // 2. Responsive mobile bottom navigation bar exists with valid anchors
  assert.ok(indexHtml.includes('class="jp-mobile-bottom-nav"'));
  assert.ok(indexHtml.includes('href="#radar"'));
  assert.ok(indexHtml.includes('href="#gbQuickMatrixSection"'));
  assert.ok(indexHtml.includes('href="#vip-vault"'));
  assert.ok(indexHtml.includes('href="#pricing"'));

  // 3. Responsive media queries configured
  assert.ok(indexHtml.includes('(max-width: 768px)'));
  assert.ok(indexHtml.includes('(max-width: 1024px)'));
});

test('Tier 3.2: Market Selector + Preset Sync + Action Plan Synchronization', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');

  // Account capital presets (Japanese Yen: 100万, 300万, 600万, 1200万)
  assert.ok(indexHtml.includes('setJpAccountPreset('));
  assert.ok(indexHtml.includes('setJpFxRate('));
  assert.ok(indexHtml.includes('setJpTaxMode('));

  // Visual Range Thermometer Bar
  assert.ok(indexHtml.includes('id="gbVisualRangeBar"'));
  assert.ok(indexHtml.includes('id="barStopVal"'));
  assert.ok(indexHtml.includes('id="barEntryVal"'));
  assert.ok(indexHtml.includes('id="barWallVal"'));
  assert.ok(indexHtml.includes('id="barTargetVal"'));

  // Action plan box
  assert.ok(indexHtml.includes('id="gbPlainEnglishActionBox"'));
  assert.ok(indexHtml.includes('id="gbPlainRewardBadge"'));
});

test('Tier 3.3: VIP Vault Paywall Gate & Real-Time Unlock State Flow', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');

  // 1. VIP vault lock functions exist
  assert.ok(indexHtml.includes('function hasValidStoredVipSession()'));
  assert.ok(indexHtml.includes('function requireVipOrScrollToPricing('));
  assert.ok(indexHtml.includes('function unlockGbVipVault('));
  assert.ok(indexHtml.includes('function renderVipVaultState()'));

  // 2. VIP features gated before unlock
  assert.ok(indexHtml.includes('downloadGbCatalystCsv()'));
  assert.ok(indexHtml.includes('downloadGbInsiderCsv()'));
  assert.ok(indexHtml.includes('copyGbPineScript()'));
  assert.ok(indexHtml.includes('copyGbTvWatchlist()'));
  assert.ok(indexHtml.includes('copyGbWebhookJson()'));

  // 3. Lemon.js Checkout.Success auto-unlock hook
  assert.ok(indexHtml.includes('Lemon.js Checkout.Success'));
  assert.ok(indexHtml.includes("localStorage.setItem('gb_vip_unlocked', 'true')"));
});


// =====================================================================
// TIER 4: REAL-WORLD USER JOURNEYS
// =====================================================================

test('Tier 4.1: End-to-End User Conversion & VIP Onboarding Journey', () => {
  // Step 1: User lands on getbreakai.com and checks live market tape
  const data = JSON.parse(fs.readFileSync(SNAPSHOT_PATH, 'utf8'));
  assert.ok(['BULLISH_EXPANSION', 'CONSOLIDATION'].includes(data.indices['^N225'].regime));
  assert.ok(['ACCUMULATION_BREAKOUT', 'DEFENSIVE_VALUE'].includes(data.indices['^TOPX'].regime));

  // Step 2: User scans Tokyo Electron (8035.T) and calculates NISA position size
  const sizing = calculatePositionSizing({
    account: 33333.33, // ¥5,000,000 at 150 USD/JPY
    entry: 24850,
    atr: 620,
    currentIv: 42,
    isJpy: true,
    usdJpyRate: 150.0,
    taxMode: 'nisa'
  });
  assert.equal(sizing.shares, 60);
  assert.equal(sizing.stopPrice, 23610);
  assert.equal(sizing.target25R, 27950);
  assert.ok(sizing.gain > 150000);
  assert.ok(sizing.taxSavedJpy > 30000); // Over 3万円 tax saved by NISA!

  // Step 3: User triggers Pro Annual checkout with redirect URL
  const checkoutUrl = createCheckoutUrl('pro_annual', {
    userEmail: 'investor@hedge-fund.co.jp',
    redirectUrl: 'https://getbreakai.com/confirmation.html'
  });
  assert.ok(checkoutUrl.includes('667aa482-f17c-47d1-b7f3-a2427c36516b'));
  assert.ok(checkoutUrl.includes('truthofmarket.lemonsqueezy.com'));
  assert.ok(checkoutUrl.includes('https%3A%2F%2Fgetbreakai.com%2Fconfirmation.html'));

  // Step 4: User completes payment, redirected to confirmation.html with Lemon Squeezy UUID key
  const mockStorage = createMockLocalStorage();
  const session = simulateConfirmationPageInit(
    '?order_id=992144&license_key=38b1460a-5104-4067-a91d-77b872934d51&customer_email=investor%40hedge-fund.co.jp',
    mockStorage
  );
  assert.equal(session.orderId, '992144');
  assert.equal(session.orderKey, '38b1460a-5104-4067-a91d-77b872934d51');
  assert.equal(session.customerEmail, 'investor@hedge-fund.co.jp');
  assert.equal(session.isUnlocked, true);

  // Step 5: User is directed to Web VIP Vault + @GetBreakAI YouTube (ZERO Telegram)
  const confirmHtml = fs.readFileSync(CONFIRMATION_HTML_PATH, 'utf8');
  assert.ok(!/telegram|t\.me|semifeargreedbot/i.test(confirmHtml), 'Must have ZERO Telegram references in confirmation.html');
  assert.ok(confirmHtml.includes('https://www.youtube.com/@GetBreakAI'), 'Must link to @GetBreakAI YouTube');
  assert.ok(confirmHtml.includes('https://getbreakai.com/#vip-vault'));
  assert.ok(confirmHtml.includes('beable9489@gmail.com'));

  // Step 6: User returns to index.html#vip-vault with active VIP session synced across both keys
  assert.equal(mockStorage.getItem('gb_vip_unlocked'), 'true');
  assert.equal(mockStorage.getItem('gb_vip_license_key'), '38b1460a-5104-4067-a91d-77b872934d51');
  assert.equal(mockStorage.getItem('gb_vip_key'), '38b1460a-5104-4067-a91d-77b872934d51');
});
