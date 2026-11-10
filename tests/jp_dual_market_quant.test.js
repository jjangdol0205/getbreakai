'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const INDEX_PATH = path.join(ROOT, 'index.html');
const SNAPSHOT_PATH = path.join(ROOT, 'data', 'live_market_snapshot.json');

test('Dual Market 1: Japanese Indices & TSE Prime Equities in live_market_snapshot.json', () => {
  assert.ok(fs.existsSync(SNAPSHOT_PATH), 'live_market_snapshot.json must exist');
  const data = JSON.parse(fs.readFileSync(SNAPSHOT_PATH, 'utf8'));

  // Validate Indices
  assert.ok(data.indices, 'data.indices must be defined');
  assert.ok(data.indices['^N225'], 'Nikkei 225 (^N225) must exist');
  assert.equal(data.indices['^N225'].symbol, '^N225');
  assert.ok(data.indices['^N225'].price > 30000, 'Nikkei 225 price must be realistic');
  assert.ok(data.indices['^N225'].donchian_20d_high > 0, 'Nikkei 225 must have Donchian high');
  assert.ok(data.indices['^N225'].wilder_rsi > 0, 'Nikkei 225 must have Wilder RSI');
  assert.ok(data.indices['^N225'].atr_14d > 0, 'Nikkei 225 must have ATR');

  assert.ok(data.indices['^TOPX'], 'TOPIX (^TOPX) must exist');
  assert.equal(data.indices['^TOPX'].symbol, '^TOPX');
  assert.ok(data.indices['^TOPX'].price > 2000, 'TOPIX price must be realistic');

  // Validate Flagship TSE Prime Equities
  const expectedTseTickers = ['8035.T', '6857.T', '9984.T', '7203.T', '6758.T'];
  for (const sym of expectedTseTickers) {
    assert.ok(data.tickers[sym], `TSE Flagship ${sym} must exist in data.tickers`);
    const item = data.tickers[sym];
    assert.equal(item.currency, 'JPY', `${sym} currency must be JPY`);
    assert.equal(item.market, 'TSE_PRIME', `${sym} market must be TSE_PRIME`);
    assert.ok(item.entry > 1000, `${sym} entry price must be realistic`);
    assert.ok(item.atr > 0, `${sym} ATR must be positive`);
    assert.ok(item.donchian_20d_high > 0, `${sym} Donchian high must be positive`);
    assert.ok(item.wilder_rsi > 0 && item.wilder_rsi <= 100, `${sym} Wilder RSI must be bounded`);
    assert.ok(item.pw_rsi > 0, `${sym} PW-RSI must be positive`);
    assert.ok(item.stop_loss > 0, `${sym} stop loss must be positive`);
    assert.ok(item.target_25r > item.entry, `${sym} 2.5R target must be greater than entry`);
    assert.ok(item.catalyst_rating.length > 5, `${sym} must have catalyst rating`);
  }
});

test('Dual Market 2: Market Tape and Hero Header Japanese Regime Badges in index.html', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');

  // Tape must contain Nikkei, TOPIX, and TSE Prime
  assert.ok(html.includes('^N225 日経平均'), 'Market tape must include Nikkei 225');
  assert.ok(html.includes('8035 東京エレクトロン'), 'Market tape must include Tokyo Electron');
  assert.ok(html.includes('^TOPX 東証指数'), 'Market tape must include TOPIX');
  assert.ok(html.includes('6857 アドバンテスト'), 'Market tape must include Advantest');

  // Hero header must contain Nikkei and TOPIX regime badges
  assert.ok(html.includes('🇯🇵 日経平均 (^N225)'), 'Hero header must include Nikkei 225 regime badge');
  assert.ok(html.includes('🇯🇵 東証株価指数 (^TOPX)'), 'Hero header must include TOPIX regime badge');
  assert.ok(html.includes('日米デュアルクオンツ'), 'Hero header must highlight dual quant');
});

test('Dual Market 3: Quick Matrix Dual-Market Filtering & TSE Prime Equities', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');

  // Quick Matrix Market switch buttons
  assert.ok(html.includes('id="btnMatrixFilterAll"'), 'Quick Matrix must have All Markets button');
  assert.ok(html.includes('id="btnMatrixFilterTse"'), 'Quick Matrix must have TSE Prime button');
  assert.ok(html.includes('id="btnMatrixFilterUs"'), 'Quick Matrix must have US Tech button');
  assert.ok(html.includes('filterMatrixMarket('), 'Must define filterMatrixMarket function call');

  // Table rows for TSE Prime
  assert.ok(html.includes('data-market="tse"'), 'Must have rows tagged data-market="tse"');
  assert.ok(html.includes('data-market="us"'), 'Must have rows tagged data-market="us"');
  assert.ok(html.includes('8035 東京エレクトロン'), 'Quick Matrix must include Tokyo Electron row');
  assert.ok(html.includes('6857 アドバンテスト'), 'Quick Matrix must include Advantest row');
  assert.ok(html.includes('9984 ソフトバンクG'), 'Quick Matrix must include SoftBank row');
  assert.ok(html.includes('7203 トヨタ自動車'), 'Quick Matrix must include Toyota row');
  assert.ok(html.includes('6758 ソニーグループ'), 'Quick Matrix must include Sony row');
});

test('Dual Market 4: Radar Terminal Market Switch & Yen ATR Calculator Support', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');

  // Radar market switcher
  assert.ok(html.includes('id="btnRadarMarketTse"'), 'Radar must have TSE market switch button');
  assert.ok(html.includes('id="btnRadarMarketUs"'), 'Radar must have US market switch button');
  assert.ok(html.includes('switchRadarMarket('), 'Must define switchRadarMarket function');

  // TSE ticker buttons
  assert.ok(html.includes('data-ticker="8035"'), 'Radar must have ticker button for 8035');
  assert.ok(html.includes('data-ticker="6857"'), 'Radar must have ticker button for 6857');
  assert.ok(html.includes('data-ticker="9984"'), 'Radar must have ticker button for 9984');
  assert.ok(html.includes('data-ticker="7203"'), 'Radar must have ticker button for 7203');
  assert.ok(html.includes('data-ticker="6758"'), 'Radar must have ticker button for 6758');

  // CATALYST_DATA contains Yen stocks
  assert.ok(html.includes('"8035":'), 'CATALYST_DATA must contain 8035');
  assert.ok(html.includes('"currency": "JPY"'), 'CATALYST_DATA must support currency JPY');
});

test('Dual Market 5: In-Depth Quantitative Trading Methodology & Shin-NISA Tax Optimization', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');

  // Methodology Section
  assert.ok(html.includes('id="quant-methodology"'), 'Must include #quant-methodology section');
  assert.ok(html.includes('ドンチアン・チャネル20日新高値ブレイクアウト規則'), 'Must detail Donchian 20-day high breakout rules');
  assert.ok(html.includes('出来高拡大フィルター（1.5倍必須）'), 'Must detail 1.5x volume expansion requirement');
  assert.ok(html.includes('LOW_VOLUME_TRAP'), 'Must explain LOW_VOLUME_TRAP suppression');
  assert.ok(html.includes('INSTITUTIONAL_IGNITION'), 'Must explain PW-RSI >= 90 institutional ignition');

  // Asymmetric Risk-Reward
  assert.ok(html.includes('非対称リスクリワード'), 'Must explain asymmetric risk-reward mechanics');
  assert.ok(html.includes('厳格な-9.0%ハードストップ'), 'Must detail -9% strict hard stop-loss threshold');
  assert.ok(html.includes('2.0x ATR動的損切り'), 'Must detail dynamic 2.0x ATR volatility stop');

  // Shin-NISA Growth Quota Tax Optimization
  assert.ok(html.includes('年間240万円'), 'Must detail annual 2.4M JPY growth quota');
  assert.ok(html.includes('生涯1,200万円'), 'Must detail lifetime 12M JPY growth quota');
  assert.ok(html.includes('新NISA 成長投資枠 vs 特定口座'), 'Must include tax comparison table');
  assert.ok(html.includes('損益通算・繰越控除不可'), 'Must warn about NISA tax loss offset limitation');
});
