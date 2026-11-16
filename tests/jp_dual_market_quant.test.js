'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const INDEX_PATH = path.join(ROOT, 'index.html');
const JP_INDEX_PATH = path.join(ROOT, 'jp', 'index.html');
const SNAPSHOT_PATH = path.join(ROOT, 'data', 'live_market_snapshot.json');

test('Dual Market 1: Japanese Indices & TSE Prime Equities in live_market_snapshot.json', () => {
  assert.ok(fs.existsSync(SNAPSHOT_PATH), 'live_market_snapshot.json must exist');
  const data = JSON.parse(fs.readFileSync(SNAPSHOT_PATH, 'utf8'));
  assert.ok(data.indices['^N225'], 'Nikkei 225 (^N225) must exist');
  assert.ok(data.indices['^TOPX'], 'TOPIX (^TOPX) must exist');

  const expectedTseTickers = ['8035.T', '6857.T', '9984.T', '7203.T', '6758.T'];
  for (const sym of expectedTseTickers) {
    assert.ok(data.tickers[sym], `TSE Flagship ${sym} must exist in data.tickers`);
    assert.equal(data.tickers[sym].currency, 'JPY');
    assert.equal(data.tickers[sym].market, 'TSE_PRIME');
  }
});

test('Dual Market 2: FSA Shin-NISA Eligible Core (1489/VYM/HDV/Orkan/S&P500) + Tokutei Hybrid (SGOV/JEPI)', () => {
  for (const fp of [INDEX_PATH, JP_INDEX_PATH]) {
    const html = fs.readFileSync(fp, 'utf8');
    assert.ok(html.includes('1489'), 'Must include 1489 Nikkei High Dividend 50 ETF');
    assert.ok(html.includes('VYM'), 'Must include VYM US High Dividend ETF');
    assert.ok(html.includes('HDV'), 'Must include HDV ETF');
    assert.ok(html.includes('オルカン'), 'Must include All-Country index');
    assert.ok(html.includes('S&amp;P500') || html.includes('S&P500'), 'Must include S&P500');
    assert.ok(html.includes('新NISA 適格（四半期配当 VYM・HDV・1489・オルカン・S&P500 時間差組み合わせ）＋ 特定口座（毎月分配 SGOV・JEPI）ハイブリッド設計'));
    assert.ok(html.includes("setJpHubTaxMode('nisa')") && html.includes("setJpHubTaxMode('tokutei')"));
  }
});
