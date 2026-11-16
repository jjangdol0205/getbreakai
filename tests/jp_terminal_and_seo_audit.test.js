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
const FSA_HYBRID_PHRASE = '『新NISA 適格（四半期配当 VYM・HDV・1489・オルカン・S&P500 時間差組み合わせ）＋ 特定口座（毎月分配 SGOV・JEPI）ハイブリッド設計』';

test('STEP 1: Unified Root /index.html & /jp/index.html 50-70s Shin-NISA Hybrid Cashflow Edition', () => {
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
    assert.ok(!/['"]\/\?unlock=1#vip-vault/.test(html), `${label} must never point to old root /?unlock=1#vip-vault`);
    assert.ok(html.includes('/jp/?unlock=1#vip-vault'), `${label} must route VIP unlock to /jp/?unlock=1#vip-vault`);
  }
});

test('STEP 2: PAYMENT_CONFIG, STORE_LIVE_READY:false, VIP Waitlist Modal & 6 Legal Pages', () => {
  const html = fs.readFileSync(JP_INDEX_PATH, 'utf8');
  assert.ok(html.includes('window.PAYMENT_CONFIG'), 'Must define window.PAYMENT_CONFIG');
  assert.ok(html.includes('STORE_LIVE_READY: false'), 'Must default STORE_LIVE_READY: false');
  assert.ok(html.includes('FINANCE_STORE_SLOT'), 'Must define FINANCE_STORE_SLOT');
  assert.ok(html.includes('PEDIATRIC_STORE_SLOT'), 'Must define PEDIATRIC_STORE_SLOT');
  assert.ok(html.includes('d5e7e761-8b1b-4ca8-b1fe-771acd1450f8?embed=1&locale=ja'));
  assert.ok(html.includes('667aa482-f17c-47d1-b7f3-a2427c36516b?embed=1&locale=ja'));
  assert.ok(html.includes('c1cd7f12-3479-49e8-ab71-59c98135d599'));
  assert.ok(html.includes('c562946d-ef68-4c2f-a802-df9da0179895'));
  assert.ok(html.includes('月額 $29 / 約4,400円（税込）'));
  assert.ok(html.includes('年額 $199（約30,000円・税込）'));
  assert.ok(html.includes('VIP創設メンバー先行案内＆早期20%割引クーポン予約（1秒メール登録）'));
  assert.ok(html.includes("segment: 'vip_waitlist'"));
  assert.ok(html.includes('Checkout.Success'));
  assert.ok(html.includes('mailto:beable9489@gmail.com'));
  assert.ok(html.includes('read_complete'));
  assert.ok(html.includes('このマニュアルをメールで受け取る（無料倶楽部登録）'));
  assert.ok(html.includes('Instagram|FBAN|FBAV|KAKAOTALK'));

  for (const rel of [
    'terms.html', 'privacy.html', 'refund.html',
    'jp/terms.html', 'jp/privacy.html', 'jp/refund.html',
    'dist/terms.html', 'dist/privacy.html', 'dist/refund.html',
    'dist/jp/terms.html', 'dist/jp/privacy.html', 'dist/jp/refund.html'
  ]) {
    assert.ok(fs.existsSync(path.join(ROOT, rel)), `Required legal page must exist: ${rel}`);
  }
});

test('STEP 3: 30 Japanese Static SEO Research Pages (/jp/*.html) + Canonical Sitemap (0 Redirects)', () => {
  const excluded = new Set([
    'index.html', 'confirmation.html', 'daily-nisa-quant-report.html',
    'terms.html', 'privacy.html', 'refund.html', 'contact.html'
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
    assert.ok(!/機関投資家機関投資家|機関需給\s*Squeeze|SEC\s*Form\s*公式業績発表/.test(content), `${f} must have 0 machine-replaced typos`);
    assert.ok(content.includes('window.PAYMENT_CONFIG'), `${f} must include window.PAYMENT_CONFIG`);
    assert.ok(content.includes('/hq_member_crm_client.js'), `${f} must load hq_member_crm_client.js`);
    assert.ok(content.includes('月額 $29 / 約4,400円（税込）'), `${f} must display JPY monthly price`);
    assert.ok(content.includes(MANDATORY_DISCLAIMER), `${f} must display mandatory FIEA disclaimer`);
    assert.ok(content.includes(FSA_HYBRID_PHRASE), `${f} must include FSA Shin-NISA Hybrid guidance`);
    assert.ok(content.includes('read_complete'), `${f} must include read_complete beacon`);
    assert.ok(content.includes('FAQPage'), `${f} must include FAQPage JSON-LD`);
    assert.ok(content.includes('recalcMiniWidget'), `${f} must include interactive Mini calculator`);
  }

  const hubHtml = fs.readFileSync(JP_INDEX_PATH, 'utf8');
  assert.ok(!hubHtml.includes('soxl-smh-semiconductor-timing.html'), 'Hub must de-feature SOXL 3x leveraged article');

  const sitemap = fs.readFileSync(SITEMAP_PATH, 'utf8');
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/</loc>'));
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/</loc>'));
  assert.ok(!sitemap.includes('index.html</loc>'), 'sitemap.xml must never contain /index.html redirect URLs');
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/terms.html</loc>'));
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/privacy.html</loc>'));
  assert.ok(sitemap.includes('<loc>https://getbreakai.com/jp/refund.html</loc>'));
  assert.ok(fs.existsSync(WORKFLOW_PATH), 'getbreakai_jp_autopilot.yml must exist');
  assert.ok(fs.existsSync(path.join(JP_DIR, 'feed.xml')));
  assert.ok(fs.existsSync(path.join(JP_DIR, 'x-feed.xml')));
});
