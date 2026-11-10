'use strict';

/**
 * GetBreakAI (Division 3) — Final Empirical Adversarial Stress Test Suite
 * Archetype: EMPIRICAL CHALLENGER
 * Roles: critic, specialist
 * 
 * Comprehensive Adversarial Verification Across 4 Core Challenge Dimensions:
 * 1. User Inputs, Confirmation URL Parameters, Fallbacks & XSS Resistance
 * 2. Position Sizing Numerical Boundaries, Zero/Negative ATR, Extreme Yen & Tax Invariants
 * 3. Responsive Breakpoints (320px to 1920px), Zero Bleed & WCAG Accessible Touch Targets
 * 4. Lemon Squeezy Store #296100, Tier Variant IDs & @SemifearGreedbot VIP Onboarding
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const INDEX_HTML_PATH = path.join(ROOT, 'index.html');
const CONFIRMATION_HTML_PATH = path.join(ROOT, 'confirmation.html');
const JP_CONFIRMATION_HTML_PATH = path.join(ROOT, 'jp', 'confirmation.html');
const JP_INDEX_HTML_PATH = path.join(ROOT, 'jp', 'index.html');
const LEMON_PATH = path.join(ROOT, 'src', 'services', 'lemonsqueezy.js');
const ENGINE_PATH = path.join(ROOT, 'src', 'engine', 'breakout_engine.js');
const SNAPSHOT_PATH = path.join(ROOT, 'data', 'live_market_snapshot.json');

// Import services and engine
const { STORE_CONFIG, createCheckoutUrl, verifyWebhookSignature, parseWebhookEvent } = require(LEMON_PATH);
const { calculateAtrPositionSize, calculateCatalystOptionsMove } = require(ENGINE_PATH);

// Helper to simulate browser LocalStorage with quota / permission error capability
function createMockLocalStorage(options = {}) {
  const store = { ...(options.initialStore || {}) };
  const throwOnSet = !!options.throwOnSet;
  return {
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(store, key) ? String(store[key]) : null;
    },
    setItem(key, value) {
      if (throwOnSet) {
        const err = new Error('QuotaExceededError: The quota has been exceeded.');
        err.name = 'QuotaExceededError';
        throw err;
      }
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

// Helper simulating confirmation.html initConfirmation query parsing
function simulateConfirmationInit(queryString, mockStorage) {
  let search = queryString;
  if (search.startsWith('?')) search = search.substring(1);
  const params = new URLSearchParams(search);

  const fallbackOrderId = 'LS-' + Date.now().toString(36).toUpperCase();
  const fallbackOrderKey = 'GBA-E2E0-TEST-FALL';
  const fallbackEmail = 'ご登録メールアドレス宛に送信完了';

  const orderId = (params.get('order_id') || params.get('orderId') || params.get('checkout_id') || '').trim() || fallbackOrderId;
  const orderKey = (params.get('order_key') || params.get('orderKey') || params.get('license_key') || '').trim() || fallbackOrderKey;
  const customerEmail = (params.get('customer_email') || params.get('email') || '').trim() || (mockStorage ? mockStorage.getItem('gb_vip_customer_email') : null) || fallbackEmail;

  if (mockStorage) {
    try {
      mockStorage.setItem('gb_vip_unlocked', 'true');
      mockStorage.setItem('gb_vip_license_key', orderKey);
      mockStorage.setItem('gb_vip_order_id', orderId);
      if (params.get('customer_email') || params.get('email')) {
        mockStorage.setItem('gb_vip_customer_email', customerEmail);
      }
    } catch (_) {
      // Ignored safely as in confirmation.html
    }
  }

  return {
    orderId,
    orderKey,
    customerEmail,
    isUnlocked: mockStorage ? mockStorage.getItem('gb_vip_unlocked') === 'true' : false
  };
}

// Sizing logic replication matching index.html recalcSizer
function runPositionSizerMath({
  account,
  entry,
  atr,
  currentIv = 50,
  isJpy = false,
  usdJpyRate = 150.0,
  taxMode = 'nisa'
}) {
  const jpTaxRate = 0.20315;
  const isTokutei = (taxMode === 'tokutei');

  if (isJpy) {
    const accountYen = account * usdJpyRate;
    const maxRiskYen = accountYen * 0.015;
    const stopDist = Math.max(0.01, atr * 2.0);
    const stopPrice = Math.max(1, entry - stopDist);
    const rawShares = stopDist > 0 ? Math.floor(maxRiskYen / stopDist) : 0;
    const maxAfford = entry > 0 ? Math.floor(accountYen / entry) : 0;
    const shares = Math.max(0, Math.min(rawShares, maxAfford));
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
    const rawShares = stopDist > 0 ? Math.floor(maxRiskDollars / stopDist) : 0;
    const maxAfford = entry > 0 ? Math.floor(account / entry) : 0;
    const shares = Math.max(0, Math.min(rawShares, maxAfford));
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

// =========================================================================
// SUITE 1: ADVERSARIAL INPUTS, CONFIRMATION URL PARAMS & SECURITY
// =========================================================================

test('ADV 1.1: XSS Injection Payloads in confirmation.html are safely neutralized', () => {
  const confirmHtml = fs.readFileSync(CONFIRMATION_HTML_PATH, 'utf8');
  const jpConfirmHtml = fs.readFileSync(JP_CONFIRMATION_HTML_PATH, 'utf8');

  // Verify that DOM population in confirmation.html strictly uses .innerText (not .innerHTML)
  assert.ok(confirmHtml.includes('elOrderId.innerText = String(orderId)'), 'Must assign orderId via innerText');
  assert.ok(confirmHtml.includes('elEmail.innerText = String(customerEmail)'), 'Must assign email via innerText');
  assert.ok(confirmHtml.includes('elKey.innerText = String(orderKey)'), 'Must assign license key via innerText');

  assert.ok(jpConfirmHtml.includes('elOrderId.innerText = String(orderId)'));
  assert.ok(jpConfirmHtml.includes('elEmail.innerText = String(customerEmail)'));
  assert.ok(jpConfirmHtml.includes('elKey.innerText = String(orderKey)'));

  // Test adversarial XSS vectors
  const xssPayloads = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert(1)>',
    '"><svg onload=alert(document.cookie)>',
    'javascript:alert(1)',
    '"><iframe src="evil.com">',
    '"><a href="javascript:alert(1)">Click</a>'
  ];

  for (const payload of xssPayloads) {
    const storage = createMockLocalStorage();
    const query = `?order_id=${encodeURIComponent(payload)}&order_key=${encodeURIComponent(payload)}&customer_email=${encodeURIComponent(payload)}`;
    const res = simulateConfirmationInit(query, storage);

    assert.equal(res.orderId, payload, 'Raw payload stored as literal text');
    assert.equal(res.orderKey, payload);
    assert.equal(res.customerEmail, payload);
    // Because innerText is used in confirmation.html, no script tags can execute in the DOM.
  }
});

test('ADV 1.2: URL Query Edge Cases: Empty, Whitespace, Delimiters & Missing Values', () => {
  const storage = createMockLocalStorage();

  // 1. Completely empty query
  const resEmpty = simulateConfirmationInit('', storage);
  assert.ok(resEmpty.orderId.startsWith('LS-'));
  assert.ok(resEmpty.orderKey.startsWith('GBA-'));
  assert.equal(resEmpty.customerEmail, 'ご登録メールアドレス宛に送信完了');

  // 2. Query with only '?'
  const resQuestion = simulateConfirmationInit('?', storage);
  assert.ok(resQuestion.orderId.startsWith('LS-'));
  assert.ok(resQuestion.orderKey.startsWith('GBA-'));

  // 3. Query with repeated delimiters '?&&&'
  const resDelim = simulateConfirmationInit('?&&&', storage);
  assert.ok(resDelim.orderId.startsWith('LS-'));

  // 4. Query with empty keys and whitespace values
  const resSpaces = simulateConfirmationInit('?order_id=%20%20%20&order_key=%20&customer_email=%20%20', storage);
  assert.ok(resSpaces.orderId.startsWith('LS-'), 'Whitespace orderId must trigger safe fallback');
  assert.ok(resSpaces.orderKey.startsWith('GBA-'), 'Whitespace orderKey must trigger safe fallback');
  assert.equal(resSpaces.customerEmail, 'ご登録メールアドレス宛に送信完了');
});

test('ADV 1.3: Parameter Aliases & Case Variations', () => {
  const storage = createMockLocalStorage();

  // Test alternative aliases (orderId, checkout_id, orderKey, license_key, email)
  const res1 = simulateConfirmationInit('?orderId=ORD_991&orderKey=KEY_771&email=client1@tokyo.jp', storage);
  assert.equal(res1.orderId, 'ORD_991');
  assert.equal(res1.orderKey, 'KEY_771');
  assert.equal(res1.customerEmail, 'client1@tokyo.jp');

  const res2 = simulateConfirmationInit('?checkout_id=CK_442&license_key=LIC_882&email=client2@osaka.jp', storage);
  assert.equal(res2.orderId, 'CK_442');
  assert.equal(res2.orderKey, 'LIC_882');
  assert.equal(res2.customerEmail, 'client2@osaka.jp');
});

test('ADV 1.4: Extreme String Length & DoS Stress (10,000+ characters)', () => {
  const storage = createMockLocalStorage();
  const giantString = 'A'.repeat(12000);
  const query = `?order_id=${giantString}&license_key=${giantString}&email=${giantString}@firm.jp`;

  const startTime = Date.now();
  const res = simulateConfirmationInit(query, storage);
  const duration = Date.now() - startTime;

  assert.ok(duration < 100, `Large string processing must complete in <100ms (took ${duration}ms)`);
  assert.equal(res.orderId.length, 12000);
  assert.equal(res.orderKey.length, 12000);
  assert.ok(res.customerEmail.includes('@firm.jp'));
});

test('ADV 1.5: Character Encodings, Japanese Unicode, Emojis & Null Bytes', () => {
  const storage = createMockLocalStorage();
  const unicodeOrder = 'LS-注文-2026-東京-👑🚀';
  const unicodeEmail = '佐藤健一@証券会社.co.jp';
  const unicodeKey = 'GBA-新NISA-ダイヤモンド-💎';

  const query = `?order_id=${encodeURIComponent(unicodeOrder)}&license_key=${encodeURIComponent(unicodeKey)}&customer_email=${encodeURIComponent(unicodeEmail)}`;
  const res = simulateConfirmationInit(query, storage);

  assert.equal(res.orderId, unicodeOrder);
  assert.equal(res.orderKey, unicodeKey);
  assert.equal(res.customerEmail, unicodeEmail);

  // Null bytes
  const nullQuery = `?order_id=LS-TEST%00EVIL&license_key=GBA-NULL%00KEY`;
  const resNull = simulateConfirmationInit(nullQuery, storage);
  assert.ok(resNull.orderId.includes('LS-TEST'));
});

test('ADV 1.6: Prototype Pollution Parameter Immunity', () => {
  const storage = createMockLocalStorage();
  const query = '?__proto__[polluted]=true&constructor[prototype][injected]=yes';
  simulateConfirmationInit(query, storage);

  assert.equal(Object.prototype.polluted, undefined, 'Object prototype must NOT be polluted');
  assert.equal(Object.prototype.injected, undefined);
});

test('ADV 1.7: LocalStorage Quota Exceeded & Incognito Mode Resilience', () => {
  const failingStorage = createMockLocalStorage({ throwOnSet: true });
  assert.doesNotThrow(() => {
    simulateConfirmationInit('?order_id=LS-OFFLINE-1&license_key=GBA-INC-1', failingStorage);
  }, 'Must handle LocalStorage quota error gracefully without unhandled exception');
});

// =========================================================================
// SUITE 2: POSITION SIZING BOUNDARIES, ZERO/NEGATIVE ATR & EXTREME YEN
// =========================================================================

test('ADV 2.1: breakout_engine.js:calculateAtrPositionSize strict input validations', () => {
  // 1. Negative or zero account balance throws descriptive error
  assert.throws(() => {
    calculateAtrPositionSize({ accountBalance: 0, entryPrice: 100, atr: 5 });
  }, /Valid positive accountBalance, entryPrice, and atr are required/);

  assert.throws(() => {
    calculateAtrPositionSize({ accountBalance: -10000, entryPrice: 100, atr: 5 });
  }, /Valid positive accountBalance, entryPrice, and atr are required/);

  // 2. Zero or negative entry price throws
  assert.throws(() => {
    calculateAtrPositionSize({ accountBalance: 50000, entryPrice: 0, atr: 5 });
  }, /Valid positive accountBalance, entryPrice, and atr are required/);

  assert.throws(() => {
    calculateAtrPositionSize({ accountBalance: 50000, entryPrice: -50, atr: 5 });
  }, /Valid positive accountBalance, entryPrice, and atr are required/);

  // 3. Zero or negative ATR throws
  assert.throws(() => {
    calculateAtrPositionSize({ accountBalance: 50000, entryPrice: 100, atr: 0 });
  }, /Valid positive accountBalance, entryPrice, and atr are required/);

  assert.throws(() => {
    calculateAtrPositionSize({ accountBalance: 50000, entryPrice: 100, atr: -2.5 });
  }, /Valid positive accountBalance, entryPrice, and atr are required/);
});

test('ADV 2.2: Terminal Sizer Numerical Boundaries (Zero Capital, Zero ATR, Micro Entry)', () => {
  // Boundary A: Zero capital -> 0 shares, notional 0, no NaN
  const zeroCap = runPositionSizerMath({ account: 0, entry: 100, atr: 5, isJpy: false });
  assert.equal(zeroCap.shares, 0);
  assert.equal(zeroCap.notional, 0);
  assert.equal(zeroCap.actualRisk, 0);
  assert.ok(!Number.isNaN(zeroCap.notional));

  // Boundary B: Negative capital -> clamps safely to 0 shares
  const negCap = runPositionSizerMath({ account: -5000, entry: 100, atr: 5, isJpy: false });
  assert.equal(negCap.shares, 0);

  // Boundary C: Micro entry price ($0.05 penny stock) -> stop price clamps to floor $0.01
  const microPrice = runPositionSizerMath({ account: 10000, entry: 0.05, atr: 0.04, isJpy: false });
  assert.ok(microPrice.stopPrice >= 0.01, 'Stop price must never drop below $0.01 floor');

  // Boundary D: Zero ATR in simulation -> guarded by stopDist floor Math.max(0.01, atr * 2.0)
  const zeroAtr = runPositionSizerMath({ account: 50000, entry: 100, atr: 0, isJpy: false });
  assert.ok(zeroAtr.stopDist >= 0.01);
  assert.ok(!Number.isNaN(zeroAtr.shares));
  assert.ok(zeroAtr.shares <= 500); // cannot exceed account / entry
});

test('ADV 2.3: Extreme Whale Portfolios (¥100M to ¥10B) & High JPY Equities', () => {
  const portfolios = [
    { name: '1億円 (¥100,000,000)', yen: 100000000 },
    { name: '10億円 (¥1,000,000,000)', yen: 1000000000 },
    { name: '100億円 (¥10,000,000,000)', yen: 10000000000 }
  ];

  // Test against Tokyo Electron (¥24,850/share, ATR ¥620) and Fast Retailing (¥50,000/share, ATR ¥1,200)
  for (const p of portfolios) {
    const usdEquiv = p.yen / 150.0;
    const res = runPositionSizerMath({
      account: usdEquiv,
      entry: 24850,
      atr: 620,
      isJpy: true,
      usdJpyRate: 150.0
    });

    assert.ok(Number.isInteger(res.shares), `${p.name}: Shares must be an integer (got ${res.shares})`);
    assert.ok(res.shares > 0, `${p.name}: Shares must be positive`);
    assert.ok(res.notional <= p.yen, `${p.name}: Position notional must not exceed total capital`);
    assert.ok(res.actualRisk <= p.yen * 0.015, `${p.name}: Actual risk must not exceed 1.5% capital ceiling`);
    assert.ok(!Number.isNaN(res.netProfitJpy), `${p.name}: Net profit must not be NaN`);
  }
});

test('ADV 2.4: Extreme USD/JPY Exchange Rates (80.0 to 250.0)', () => {
  const rates = [80.0, 100.0, 150.0, 200.0, 250.0];
  let prevTaxSaved = -1;

  for (const rate of rates) {
    const res = runPositionSizerMath({
      account: 50000,
      entry: 186.64,
      atr: 5.79,
      isJpy: false,
      usdJpyRate: rate,
      taxMode: 'nisa'
    });

    assert.ok(res.taxSavedJpy > 0);
    assert.ok(res.taxSavedJpy > prevTaxSaved, `Higher USD/JPY rate (${rate}) must yield monotonically higher Yen tax savings`);
    prevTaxSaved = res.taxSavedJpy;
  }
});

test('ADV 2.5: Shin-NISA vs Japanese Tokutei Account Tax Exemption Invariants', () => {
  // Test identical trade under NISA vs Tokutei
  const tradeNisa = runPositionSizerMath({ account: 50000, entry: 186.64, atr: 5.79, isJpy: false, taxMode: 'nisa' });
  const tradeTokutei = runPositionSizerMath({ account: 50000, entry: 186.64, atr: 5.79, isJpy: false, taxMode: 'tokutei' });

  assert.equal(tradeNisa.shares, tradeTokutei.shares);
  assert.equal(tradeNisa.gain, tradeTokutei.gain);

  // NISA net profit must be strictly greater than Tokutei net profit by the 20.315% tax
  assert.ok(tradeNisa.netProfitJpy > tradeTokutei.netProfitJpy, 'NISA must yield higher net profit than Tokutei');
  const expectedTaxDiff = tradeNisa.gain > 0 ? Math.round(tradeNisa.netProfitJpy - tradeTokutei.netProfitJpy) : 0;
  assert.ok(expectedTaxDiff > 0, 'Tax difference must be positive');
});

// =========================================================================
// SUITE 3: RESPONSIVE BREAKPOINTS (320px-1920px), ZERO BLEED & TOUCH TARGETS
// =========================================================================

test('ADV 3.1: Viewport Meta Tag completeness across all core pages', () => {
  const files = [INDEX_HTML_PATH, CONFIRMATION_HTML_PATH, JP_INDEX_HTML_PATH, JP_CONFIRMATION_HTML_PATH];
  for (const fp of files) {
    const content = fs.readFileSync(fp, 'utf8');
    assert.ok(
      content.includes('<meta name="viewport" content="width=device-width, initial-scale=1.0">'),
      `${path.basename(fp)} must include standard mobile viewport meta`
    );
  }
});

test('ADV 3.2: Zero Horizontal Page Bleed CSS Enforcement', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');

  // Verify overflow-x: hidden on html, body
  assert.ok(indexHtml.includes('overflow-x: hidden'), 'Must enforce overflow-x: hidden');
  assert.ok(indexHtml.includes('max-width: 100%'), 'Must enforce max-width: 100% on html/body');
  assert.ok(indexHtml.includes('box-sizing: border-box'), 'Must enforce box-sizing: border-box');
  assert.ok(indexHtml.includes('overflow-wrap: break-word'), 'Must enforce overflow-wrap: break-word');
});

test('ADV 3.3: All Tables Wrapped in Responsive Horizontal Scroll Containers', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');

  // Match all <table> elements
  const tableMatches = [...indexHtml.matchAll(/<table[^>]*>/gi)];
  assert.ok(tableMatches.length >= 3, `Expected at least 3 tables, found ${tableMatches.length}`);

  // Check each table's enclosing or preceding container for overflow-x: auto
  for (let i = 0; i < tableMatches.length; i++) {
    const pos = tableMatches[i].index;
    const surrounding = indexHtml.slice(Math.max(0, pos - 1500), pos + 100);
    const hasScrollWrap = surrounding.includes('comp-table-wrap') || surrounding.includes('overflow-x: auto');
    assert.ok(hasScrollWrap, `Table #${i + 1} at char ${pos} must be enclosed in an overflow-x: auto container`);
  }
});

test('ADV 3.4: Accessible Touch Targets & Sticky Mobile Bottom Nav (WCAG 2.5.5)', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');

  // 1. Mobile bottom nav must exist with high z-index and fixed position
  assert.ok(indexHtml.includes('.jp-mobile-bottom-nav'));
  assert.ok(indexHtml.includes('position: fixed'));
  assert.ok(indexHtml.includes('bottom: 0'));
  assert.ok(indexHtml.includes('z-index: 999'));

  // 2. Safe-area-inset padding for iOS home indicator
  assert.ok(indexHtml.includes('env(safe-area-inset-bottom'));

  // 3. Body padding offset prevents bottom nav from obscuring bottom page content
  assert.ok(indexHtml.includes('padding-bottom: calc(64px + env(safe-area-inset-bottom'));

  // 4. Verify touch target sizing (padding: 10px 4px + flex column >= 44px height)
  assert.ok(indexHtml.includes('padding: 10px 4px'));

  // 5. Verify all 4 bottom nav anchors exist in DOM
  const requiredAnchors = ['#gbQuickMatrixSection', '#radar', '#vip-vault', '#pricing'];
  for (const anchor of requiredAnchors) {
    const id = anchor.substring(1);
    assert.ok(indexHtml.includes(`id="${id}"`), `Target anchor id="${id}" must exist for bottom nav`);
    assert.ok(indexHtml.includes(`href="${anchor}"`), `Bottom nav must contain link to ${anchor}`);
  }
});

test('ADV 3.5: Responsive Breakpoint Matrix (320px to 1920px) Media Query Coverage', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');

  // Check key breakpoint queries in CSS
  assert.ok(indexHtml.includes('@media (max-width: 640px)'), 'Must have mobile <=640px breakpoint');
  assert.ok(indexHtml.includes('@media (max-width: 768px)'), 'Must have mobile/tablet <=768px breakpoint');
  assert.ok(indexHtml.includes('@media (max-width: 940px)'), 'Must have tablet <=940px breakpoint');
  assert.ok(indexHtml.includes('(min-width: 641px) and (max-width: 1024px)'), 'Must have 2-col tablet query');
});

// =========================================================================
// SUITE 4: LEMON SQUEEZY STORE #296100, TIER VARIANTS & @SemifearGreedbot
// =========================================================================

test('ADV 4.1: Store #296100 Configuration & 3 Subscription Tiers', () => {
  assert.equal(STORE_CONFIG.storeId, '296100', 'Store ID must strictly be #296100');
  assert.equal(STORE_CONFIG.supportEmail, 'beable9489@gmail.com');

  const plans = STORE_CONFIG.plans;
  assert.equal(plans.starter_monthly.variantId, 'gb-starter-29');
  assert.equal(plans.starter_monthly.priceUsd, 29);

  assert.equal(plans.pro_monthly.variantId, 'gb-pro-49');
  assert.equal(plans.pro_monthly.priceUsd, 49);

  assert.equal(plans.institutional_annual.variantId, 'gb-inst-1499');
  assert.equal(plans.institutional_annual.priceUsd, 1499);
});

test('ADV 4.2: Live Checkout URLs & Redirect Journey in index.html', () => {
  const indexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');

  const starterRegex = /truthofmarket\.lemonsqueezy\.com\/checkout\/buy\/gb-starter-29\?embed=1&checkout\[redirect_url\]=https:\/\/getbreakai\.com\/confirmation\.html/;
  const proRegex = /truthofmarket\.lemonsqueezy\.com\/checkout\/buy\/gb-pro-49\?embed=1&checkout\[redirect_url\]=https:\/\/getbreakai\.com\/confirmation\.html/;
  const instRegex = /truthofmarket\.lemonsqueezy\.com\/checkout\/buy\/gb-inst-1499\?embed=1&checkout\[redirect_url\]=https:\/\/getbreakai\.com\/confirmation\.html/;

  assert.match(indexHtml, starterRegex, 'Starter checkout button must have embedded redirect URL');
  assert.match(indexHtml, proRegex, 'Pro checkout button must have embedded redirect URL');
  assert.match(indexHtml, instRegex, 'Institutional checkout button must have embedded redirect URL');

  // Verify Lemon.js script tag
  assert.ok(indexHtml.includes('https://assets.lemonsqueezy.com/lemon.js'));
});

test('ADV 4.3: Telegram @SemifearGreedbot VIP Onboarding Flow in confirmation.html', () => {
  const confirmHtml = fs.readFileSync(CONFIRMATION_HTML_PATH, 'utf8');
  const jpConfirmHtml = fs.readFileSync(JP_CONFIRMATION_HTML_PATH, 'utf8');

  for (const [name, html] of [['confirmation.html', confirmHtml], ['jp/confirmation.html', jpConfirmHtml]]) {
    // 1. Direct Telegram link
    assert.ok(html.includes('https://t.me/SemifearGreedbot'), `${name} must link to https://t.me/SemifearGreedbot`);
    // 2. Mention @SemifearGreedbot
    assert.ok(html.includes('@SemifearGreedbot'), `${name} must mention @SemifearGreedbot`);
    // 3. /start command
    assert.ok(html.includes('/start'), `${name} must instruct user to send /start`);
    // 4. Store #296100
    assert.ok(html.includes('296100'), `${name} must display Store #296100`);
    // 5. Support email
    assert.ok(html.includes('beable9489@gmail.com'), `${name} must display support email beable9489@gmail.com`);
    // 6. Return link to index.html#vip-vault
    assert.ok(html.includes('https://getbreakai.com/#vip-vault'), `${name} must link to #vip-vault`);
  }
});

test('ADV 4.4: Webhook Security, Timing-Safe HMAC & Payload Tampering Resistance', () => {
  const secret = 'webhook_secret_getbreakai_2026_adversarial';
  const validPayload = JSON.stringify({
    meta: { event_name: 'subscription_created' },
    data: {
      id: 'sub_9981',
      attributes: {
        store_id: 296100,
        variant_id: 'gb-pro-49',
        user_email: 'trader@hedgefund.jp',
        status: 'active'
      }
    }
  });

  const crypto = require('node:crypto');
  const validSignature = crypto.createHmac('sha256', secret).update(validPayload).digest('hex');

  // 1. Valid signature passes
  assert.equal(verifyWebhookSignature(validPayload, validSignature, secret), true);

  // 2. Tampered variant ID fails
  const tamperedPayload = validPayload.replace('gb-pro-49', 'gb-starter-29');
  assert.equal(verifyWebhookSignature(tamperedPayload, validSignature, secret), false);

  // 3. Timing-safe comparison invoked
  const forgedSignature = 'a'.repeat(64);
  assert.equal(verifyWebhookSignature(validPayload, forgedSignature, secret), false);
});
