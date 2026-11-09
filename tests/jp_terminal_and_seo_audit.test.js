'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const INDEX_PATH = path.join(ROOT, 'index.html');
const SITEMAP_PATH = path.join(ROOT, 'sitemap.xml');
const JP_DIR = path.join(ROOT, 'jp');
const WORKFLOW_PATH = path.join(ROOT, '.github', 'workflows', 'getbreakai_jp_autopilot.yml');

test('STEP 1: 100% Native Japanese Localization & USD/JPY Dual Sizer in index.html', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');
  assert.match(html, /<html lang="ja"/);
  assert.match(html, /Noto\+Sans\+JP/);
  assert.ok(html.includes('ウォール街の英語'));
  assert.ok(html.includes('新NISA・米国株スイング投資家のためのATR損切り＆適正株数ターミナル'));
  assert.ok(html.includes('🔰 3ステップで完了：米国株機関投資家シグナル＆ATRリスク管理ガイド'));
  assert.ok(html.includes('🟢 AI日本語アクションプラン・適正株数＆損切りライン'));
  assert.ok(html.includes('🔴 エントリー禁止 / 会計リスク・ダークプール機関売り警告 (DO NOT BUY / AVOID)'));
  assert.ok(html.includes('📤 X(Twitter)で銘柄シグナルを共有'));
  assert.ok(html.includes('USD_JPY_RATE = 150.0'));
});

test('STEP 5: Japanese Securities (SBI/Kabutan/Buffett-Code) High-Trust Fintech UI/UX', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');
  assert.ok(html.includes('data-jp-theme="light"'), 'Default theme must be High-Trust Japanese Financial Light/Navy');
  assert.ok(html.includes('id="btnToggleJpTheme"'), 'Must include 1-click Dark/Light theme switcher');
  assert.ok(html.includes('SBI証券・楽天証券・マネックス対応'), 'Must include Japanese brokerage compatibility badge');
  assert.ok(html.includes('id="gbQuickMatrixTable"'), 'Must include Kabutan-style at-a-glance quick matrix table');
  assert.ok(html.includes('setJpAccountPreset('), 'Must include 1-tap Japanese Yen capital preset buttons (100万円~1,200万円 新NISA枠)');
  assert.ok(html.includes('setJpFxRate('), 'Must include 1-tap USD/JPY exchange rate preset buttons (145円~160円)');
  assert.ok(html.includes('id="gbVisualRangeBar"'), 'Must include visual price range thermometer bar');
  assert.ok(html.includes('id="jp-faq"'), 'Must include Japanese buyer Q&A section');
  assert.ok(html.includes('class="jp-mobile-bottom-nav"'), 'Must include smartphone one-handed sticky bottom navigation bar');
});

test('STEP 2: Japanese 3x Checkout Conversion Boosters & Store #296100 Live Checkout Links', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');
  assert.ok(!html.includes('kidsfit.lemonsqueezy.com'), 'Must not contain kidsfit.lemonsqueezy.com');
  assert.ok(html.includes('https://truthofmarket.lemonsqueezy.com/checkout/buy/bad98d00-7175-41f6-9d58-eeb2471d0da4'));
  assert.ok(html.includes('https://truthofmarket.lemonsqueezy.com/checkout/buy/00c9f6e1-c8be-42a4-b5a5-e05af1a41ed9'));
  assert.ok(html.includes('約4,400円・税込'));
  assert.ok(html.includes('👑 一番人気・買い切り'));
  assert.ok(html.includes('約30,000円・追加費用なしの買い切り'));
  assert.ok(html.includes('🔒 Stripe / Lemon Squeezy 安全決済（🍎 Apple Pay・Google Pay・JCB・Visa・Master・PayPal 対応 / いつでも1クリックで解約可能）'));
  assert.ok(html.includes('🔑 決済完了後、メールで届くライセンスキー（XXXX-XXXX-...）を入力すると即座にVIP全機能が解放されます。'));
  assert.ok(html.includes('Checkout.Success'));
  assert.ok(html.includes('特定商取引法に基づく表記'));
  assert.ok(html.includes('利用規約'));
  assert.ok(html.includes('プライバシーポリシー'));
  assert.ok(html.includes('返金ポリシー'));
  assert.ok(html.includes('1つのProライセンスキーで'));
});

test('STEP 3: 6 Technical Defect Fixes (VIP Paywall Lock, Live Sync, Abacus Beacon, OG/JSON-LD, Deep-Link)', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');
  assert.ok(html.includes('https://api.lemonsqueezy.com/v1/licenses/validate'));
  assert.ok(html.includes('🔒 [VIP限定] Proライセンスキー認証後にPine Script v5全文およびTradingViewウォッチリストをコピーできます'));
  assert.ok(html.includes('gba_getbreakai'));
  assert.ok(html.includes('paid_click_'));
  assert.ok(html.includes('hreflang="ja"'));
  assert.ok(fs.existsSync(path.join(ROOT, 'og-preview.png')));
  assert.ok(fs.statSync(path.join(ROOT, 'og-preview.png')).size > 30000);
  assert.ok(fs.existsSync(path.join(ROOT, 'scripts', 'sync_getbreakai_live_data.py')));
  assert.ok(fs.existsSync(path.join(ROOT, 'data', 'live_market_snapshot.json')));
});

test('STEP 4.1: 30 Japanese Static SEO Research Pages (/jp/*.html) >= 2,500 chars + Sitemap', () => {
  const files = fs.readdirSync(JP_DIR).filter(f => f.endsWith('.html') && f !== 'index.html');
  assert.equal(files.length, 30, 'Must have exactly 30 Japanese SEO research pages');
  const requiredSlugs = [
    'nvda-sec-gamma-atr-analysis.html',
    'pltr-insider-buying-analysis.html',
    'tsla-gamma-wall-swing-trade.html',
    'soxl-smh-semiconductor-timing.html',
    'smci-accounting-risk-warning.html',
    'shin-nisa-us-stock-atr-risk-management.html'
  ];
  for (const slug of requiredSlugs) {
    assert.ok(files.includes(slug), `Missing required SEO slug: ${slug}`);
  }
  for (const f of files) {
    const content = fs.readFileSync(path.join(JP_DIR, f), 'utf8');
    const textOnly = content.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<[^>]+>/g, '').trim();
    assert.ok(textOnly.length >= 2500, `${f} visible text length (${textOnly.length}) must be >= 2500 chars`);
    assert.ok(content.includes('FAQPage'), `${f} must include FAQPage JSON-LD`);
    assert.ok(content.includes('recalcMiniWidget'), `${f} must include interactive Mini ATR calculator widget`);
  }
  const sitemap = fs.readFileSync(SITEMAP_PATH, 'utf8');
  assert.ok(sitemap.includes('https://getbreakai.com/jp/nvda-sec-gamma-atr-analysis.html'));
});

test('STEP 4.2 & 4.3: Japanese Shorts (.mp4), Summary Cards (.png), 10 X Posts & GitHub Actions Autopilot Workflow', () => {
  assert.ok(fs.existsSync(WORKFLOW_PATH), 'getbreakai_jp_autopilot.yml must exist');
  const outboxBase = path.join(ROOT, 'marketing_outbox_jp');
  const dateFolders = fs.readdirSync(outboxBase).filter(d => /^\d{4}-\d{2}-\d{2}$/.test(d)).sort();
  assert.ok(dateFolders.length >= 1, 'Must have at least 1 dated folder in marketing_outbox_jp');
  const latestDir = path.join(outboxBase, dateFolders[dateFolders.length - 1]);
  for (const mp4 of ['jp_shorts_01_NVDA_gamma_atr.mp4', 'jp_shorts_02_PLTR_sec8k_atr.mp4', 'jp_shorts_03_TSLA_gex_atr.mp4']) {
    const p = path.join(latestDir, mp4);
    assert.ok(fs.existsSync(p), `Missing Japanese Shorts MP4: ${mp4}`);
    assert.ok(fs.statSync(p).size > 50000, `${mp4} must be a valid non-empty MP4 file`);
  }
  for (const png of ['card_01_NVDA_signal.png', 'card_02_PLTR_signal.png', 'card_03_TSLA_signal.png']) {
    assert.ok(fs.existsSync(path.join(latestDir, png)), `Missing Japanese X Summary Card: ${png}`);
  }
  const xPosts = JSON.parse(fs.readFileSync(path.join(latestDir, 'x_posts_10.json'), 'utf8'));
  assert.equal(xPosts.length, 10, 'Must have 10 Japanese X posts');
  assert.ok(fs.existsSync(path.join(latestDir, 'note_com_article_jp.md')));
});
