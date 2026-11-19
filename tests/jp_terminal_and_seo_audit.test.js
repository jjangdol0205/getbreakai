'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const INDEX_PATH = path.join(ROOT, 'index.html');
const JP_INDEX_PATH = path.join(ROOT, 'jp', 'index.html');
const SITEMAP_PATH = path.join(ROOT, 'sitemap.xml');
const JP_DIR = path.join(ROOT, 'jp');
const DIST_DIR = path.join(ROOT, 'dist');
const WORKFLOW_PATH = path.join(ROOT, '.github', 'workflows', 'getbreakai_jp_autopilot.yml');

const MANDATORY_DISCLAIMER = '免責事項：当サイトは公開市場データの可視化および数学的シミュレーションツール（教育・情報提供目的）であり、金融商品取引法上の投資助言・代理業や個別銘柄の売買推奨を行うものではありません。';
const FSA_HYBRID_PHRASE = '『新NISA成長投資枠（米国半導体 SMH × 米国ヘルスケア XLV 現物1倍 2本柱）＋ 安全資産クッション（個人向け国債 変動10年 ／ 特定口座 SGOV）』';
const UNIFIED_PRODUCT_DEF = '教育目的の市場データニュースレター ＋ 2000–2025年 過去統計ワークブック（投資助言・個別推奨は一切行わない独立系リサーチ出版）';

test('STEP 1: Unified Root /index.html & /jp/index.html Shin-NISA Educational Research Edition', () => {
  for (const [label, fp] of [['index.html', INDEX_PATH], ['jp/index.html', JP_INDEX_PATH]]) {
    const html = fs.readFileSync(fp, 'utf8');
    assert.match(html, /<html lang="ja" data-jp-theme="light">/);
    assert.ok(!/[가-힣ㄱ-ㅎㅏ-ㅣ]/.test(html), `${label} must have 0 Hangul`);
    assert.ok(!/telegram|t\.me|semifeargreedbot|テレグラム/i.test(html), `${label} must have 0 Telegram references`);
    assert.ok(html.includes('id="gba-retirement-architect-jp"'), `${label} must preserve #gba-retirement-architect-jp`);
    assert.ok(html.includes('id="gbaMorningClubJp"'), `${label} must preserve #gbaMorningClubJp`);
    assert.ok(html.includes('id="gba-jp-passwordless-signup"'), `${label} must preserve #gba-jp-passwordless-signup`);
    assert.ok(html.includes('id="gba-jp-club-email"'), `${label} must include #gba-jp-club-email`);
    assert.ok(!html.includes('gbaJpPwlessEmail'), `${label} must not reference non-existent #gbaJpPwlessEmail`);
    assert.ok(html.includes('id="gbaFreeStarterManualJp"'), `${label} must preserve #gbaFreeStarterManualJp`);
    assert.ok(html.includes(FSA_HYBRID_PHRASE), `${label} must display FSA Shin-NISA Hybrid phrase`);
    assert.ok(html.includes(MANDATORY_DISCLAIMER), `${label} must display mandatory FIEA disclaimer`);
    assert.ok(html.includes(UNIFIED_PRODUCT_DEF), `${label} must display unified non-advisory product definition`);
    assert.ok(!/['"]\/\?unlock=1#vip-vault/.test(html), `${label} must never point to old root /?unlock=1#vip-vault`);
    assert.ok(html.includes('/jp/?unlock=1#vip-vault'), `${label} must route unlock to /jp/?unlock=1#vip-vault`);
  }
});

test('STEP 2: Whop Native PAYMENT_CONFIG, @whop/checkout Embed Modal + Direct Fallback & Legal Pages', () => {
  for (const [label, fp] of [['index.html', INDEX_PATH], ['jp/index.html', JP_INDEX_PATH]]) {
    const html = fs.readFileSync(fp, 'utf8');
    assert.ok(html.includes('window.PAYMENT_CONFIG'), `${label} must define window.PAYMENT_CONFIG`);
    assert.ok(html.includes("PROVIDER: 'whop'"), `${label} must set PROVIDER: 'whop'`);
    assert.ok(html.includes("DIVISION: 'GBA'"), `${label} must set DIVISION: 'GBA'`);
    assert.ok(html.includes("STORE_SLOT: 'FINANCE_STORE_SLOT'"), `${label} must define FINANCE_STORE_SLOT`);
    assert.ok(html.includes('STORE_LIVE_READY: true'), `${label} must set STORE_LIVE_READY: true`);
    assert.ok(html.includes('plan_UtG9mA9L5pZIS') && html.includes('https://whop.com/checkout/plan_UtG9mA9L5pZIS'), `${label} must include live Whop monthly plan`);
    assert.ok(html.includes('plan_ahYIXbLDE0CsQ') && html.includes('https://whop.com/checkout/plan_ahYIXbLDE0CsQ'), `${label} must include live Whop annual plan`);
    assert.ok(html.includes('https://js.whop.com/static/checkout/loader.js'), `${label} must load Whop checkout loader.js`);
    assert.ok(html.includes('id="gbaWhopCheckoutModal"'), `${label} must include Whop Embedded Checkout Modal`);
    assert.ok(html.includes('data-whop-direct-tab="1"'), `${label} must include 1-tap Open in New Tab direct checkout button`);
    assert.ok(!/lemonsqueezy|lemon\s*squeezy|polar\.sh|buy\.polar\.sh|polar_cl_|recommended_weight|売買シグナル|推奨配分|CSVエクスポート|チャートスクリプト/i.test(html), `${label} must have 0 forbidden payment or advisory terms`);
    assert.ok(html.includes('月額リサーチパス（¥4,400/月）'));
    assert.ok(html.includes('年間リサーチパス（¥29,800/年）'));
    assert.ok(html.includes('14日間返金'));
    assert.ok(html.includes("payment') === 'success'"));
    assert.ok(html.includes('mailto:beable9489@gmail.com'));
    assert.ok(html.includes('read_complete'));
  }

  for (const rel of [
    'terms.html', 'privacy.html', 'refund.html', 'tokushoho.html', 'contact.html',
    'jp/terms.html', 'jp/privacy.html', 'jp/refund.html', 'jp/tokushoho.html', 'jp/contact.html',
    'dist/terms.html', 'dist/privacy.html', 'dist/refund.html', 'dist/tokushoho.html', 'dist/contact.html',
    'dist/jp/terms.html', 'dist/jp/privacy.html', 'dist/jp/refund.html', 'dist/jp/tokushoho.html', 'dist/jp/contact.html'
  ]) {
    const fullPath = path.join(ROOT, rel);
    assert.ok(fs.existsSync(fullPath), `Required legal page must exist: ${rel}`);
    const lhtml = fs.readFileSync(fullPath, 'utf8');
    assert.ok(lhtml.includes('Whop.com'), `${rel} must display Whop.com billing label`);
    assert.ok(lhtml.includes(UNIFIED_PRODUCT_DEF), `${rel} must display unified non-advisory product definition`);
    assert.ok(!/lemonsqueezy|polar\.sh|buy\.polar\.sh|polar_cl_|売買シグナル|推奨配分/i.test(lhtml), `${rel} must have 0 forbidden references`);
  }
});

test('STEP 3: 30 Japanese Static SEO Research Pages (/jp/*.html) + Canonical Sitemap (0 Redirects)', () => {
  const excluded = new Set([
    'index.html', 'confirmation.html', 'daily-nisa-quant-report.html', 'nisa-quiet-barbell-essay.html',
    'terms.html', 'privacy.html', 'refund.html', 'tokushoho.html', 'contact.html'
  ]);
  const files = fs.readdirSync(JP_DIR).filter(f =>
    f.endsWith('.html') && !excluded.has(f) && !/^google[a-z0-9]+\.html$/i.test(f)
  );
  assert.equal(files.length, 30, 'Must have exactly 30 Japanese SEO research pages');

  for (const f of files) {
    const content = fs.readFileSync(path.join(JP_DIR, f), 'utf8');
    const textOnly = content.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<[^>]+>/g, '').trim();
    assert.ok(textOnly.length >= 2500, `${f} visible text length (${textOnly.length}) must be >= 2500 chars`);
    assert.ok(!/[가-힣ㄱ-ㅎㅏ-ㅣ]/.test(content), `${f} must have 0 Hangul`);
    assert.ok(!/telegram|t\.me|semifeargreedbot|テレグラム/i.test(content), `${f} must have 0 Telegram`);
    assert.ok(!/lemonsqueezy|polar\.sh|buy\.polar\.sh|polar_cl_|recommended_weight|売買シグナル|推奨配分|CSVエクスポート|チャートスクリプト/i.test(content), `${f} must have 0 forbidden payment/advisory strings`);
    assert.ok(content.includes('window.PAYMENT_CONFIG') && content.includes("PROVIDER: 'whop'"), `${f} must include Whop window.PAYMENT_CONFIG`);
    assert.ok(content.includes('/hq_member_crm_client.js'), `${f} must load hq_member_crm_client.js`);
    assert.ok(content.includes('月額リサーチパス（¥4,400/月）'), `${f} must display JPY monthly research pass`);
    assert.ok(content.includes(MANDATORY_DISCLAIMER), `${f} must display mandatory FIEA disclaimer`);
    assert.ok(content.includes(FSA_HYBRID_PHRASE), `${f} must include FSA Shin-NISA Hybrid guidance`);
    assert.ok(content.includes('read_complete'), `${f} must include read_complete beacon`);
    assert.ok(content.includes('FAQPage'), `${f} must include FAQPage JSON-LD`);
  }

  const hubHtml = fs.readFileSync(JP_INDEX_PATH, 'utf8');
  assert.ok(!hubHtml.includes('soxl-smh-semiconductor-timing.html'), 'Hub must de-feature SOXL 3x leveraged article');

  const sitemap = fs.readFileSync(SITEMAP_PATH, 'utf8');
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/</loc>'));
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/</loc>'));
  assert.ok(!sitemap.includes('index.html</loc>'), 'sitemap.xml must never contain /index.html redirect URLs');
  assert.ok(!sitemap.includes('soxl-smh-semiconductor-timing.html'), 'sitemap.xml must exclude noindex SOXL warning page');
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/terms.html</loc>'));
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/privacy.html</loc>'));
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/refund.html</loc>'));
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/tokushoho.html</loc>'));
  assert.ok(fs.existsSync(WORKFLOW_PATH), 'getbreakai_jp_autopilot.yml must exist');
  assert.ok(fs.existsSync(path.join(JP_DIR, 'feed.xml')));
  assert.ok(fs.existsSync(path.join(JP_DIR, 'x-feed.xml')));
});

test('STEP 4: Phase 2-A & 2-B Conversion Architecture (Above-the-Fold CTA, Live Temp Badge, Zero Email Wall, 0 Emojis)', () => {
  const emojiRegex = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u;
  for (const [label, fp] of [
    ['index.html', INDEX_PATH],
    ['jp/index.html', JP_INDEX_PATH],
    ['dist/index.html', path.join(DIST_DIR, 'index.html')],
    ['dist/jp/index.html', path.join(DIST_DIR, 'jp', 'index.html')]
  ]) {
    const html = fs.readFileSync(fp, 'utf8');
    assert.ok(!emojiRegex.test(html), `${label} must have strictly 0 emojis in main page UI & modals`);
    assert.ok(html.includes('html { font-size: 18px; }'), `${label} must set root font size to 18px`);
    assert.ok(html.includes('Shippori Mincho') && html.includes('#FBFBF9'), `${label} must use Shippori Mincho & #FBFBF9 paper palette`);

    // Screen 0: Above-the-Fold Instant Start CTA + Live Market Temperature Badge + 2000-2025 Table
    assert.ok(html.includes('新NISA・資産リサーチ研究室（教育目的）'), `${label} must display Educational Research Lab eyebrow`);
    assert.ok(html.includes('騒がしい銘柄探しを手放し、二つの柱で老後資産を守り抜くために。'), `${label} must display Founding headline`);
    assert.ok(html.includes('id="gbaLiveTempBadgeJp"') && html.includes('最新データ基準日：') && html.includes('市場温度指数：'), `${label} must display live semi_overview.json temperature badge`);
    assert.ok(html.includes('過去25年の統計バランスを確認する（無料・4問）'), `${label} must include above-the-fold primary CTA`);
    assert.ok(html.indexOf('id="btnStartPwStepUpJp"') < html.indexOf('<div class="pw-manifesto">'), `${label} primary CTA must appear ABOVE the long founding manifesto`);
    assert.ok(html.includes('~7.9%') && html.includes('-50.9%') && html.includes('~11.4%') && html.includes('-27.8%') && html.includes('0.41x'), `${label} must include 2000-2025 SMH × XLV simulation table`);

    // Screen 2: Zero Email Wall before Free Baseline Summary
    assert.ok(!html.includes('pwEmailGateLockedJp'), `${label} must NOT block free baseline summary behind an email wall`);
    assert.ok(html.includes('id="pwFreeBaselineSummaryJp"'), `${label} must immediately reveal free historical baseline summary`);
    assert.ok(html.includes('この統計要約を保存し、朝刊リサーチノートを受け取る（無料）'), `${label} must render 1-line passwordless save box below summary`);
    assert.ok(html.includes('月額リサーチパス（¥4,400/月）') && html.includes('年間リサーチパス（¥29,800/年）'), `${label} must display 2-tier Whop Research Pass cards`);
  }
});
