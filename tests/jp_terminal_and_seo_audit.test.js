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

test('STEP 2: Polar.sh Native PAYMENT_CONFIG, STORE_LIVE_READY:false, VIP Waitlist Modal & Legal Pages', () => {
  for (const [label, fp] of [['index.html', INDEX_PATH], ['jp/index.html', JP_INDEX_PATH]]) {
    const html = fs.readFileSync(fp, 'utf8');
    assert.ok(html.includes('window.PAYMENT_CONFIG'), `${label} must define window.PAYMENT_CONFIG`);
    assert.ok(html.includes("PROVIDER: 'polar_sh'"), `${label} must set PROVIDER: 'polar_sh'`);
    assert.ok(html.includes("DIVISION: 'GBA'"), `${label} must set DIVISION: 'GBA'`);
    assert.ok(html.includes("STORE_SLOT: 'FINANCE_STORE_SLOT'"), `${label} must define FINANCE_STORE_SLOT`);
    assert.ok(html.includes('STORE_LIVE_READY: false'), `${label} must default STORE_LIVE_READY: false`);
    assert.ok(html.includes('POLAR_CHECKOUT_URLS'), `${label} must define POLAR_CHECKOUT_URLS`);
    assert.ok(html.includes('POLAR_GBA_MONTHLY_URL'), `${label} must define POLAR_GBA_MONTHLY_URL`);
    assert.ok(html.includes('POLAR_GBA_ANNUAL_URL'), `${label} must define POLAR_GBA_ANNUAL_URL`);
    assert.ok(html.includes('Polar.sh (Merchant of Record · Global Card / Apple Pay / Google Pay)'), `${label} must display unified Polar.sh MoR label`);
    assert.ok(!/lemonsqueezy|lemon\s*squeezy|296100|d5e7e761|667aa482/i.test(html), `${label} must have 0 Lemon Squeezy or legacy Store #296100 references`);
    assert.ok(html.includes('月額 $29 / 約4,400円（税込）'));
    assert.ok(html.includes('年額 $199（約30,000円・税込）'));
    assert.ok(html.includes('随時更新・新NISA老後取り崩し実践PDFガイド＋3つの財布シミュレーター同梱'));
    assert.ok(html.includes('14日間返金保証'));
    assert.ok(html.includes('VIP創設メンバー先行案内＆早期20%割引クーポン予約（1秒メール登録）'));
    assert.ok(html.includes("segment: 'vip_waitlist'"));
    assert.ok(html.includes("payment') === 'success'"));
    assert.ok(html.includes('Checkout.Success'));
    assert.ok(html.includes('mailto:beable9489@gmail.com'));
    assert.ok(html.includes('read_complete'));
    assert.ok(html.includes('このマニュアルをメールで受け取る（無料倶楽部登録）'));
    assert.ok(html.includes('Instagram|FBAN|FBAV|KAKAOTALK|Line'));
  }

  for (const rel of [
    'terms.html', 'privacy.html', 'refund.html', 'contact.html',
    'jp/terms.html', 'jp/privacy.html', 'jp/refund.html', 'jp/contact.html',
    'dist/terms.html', 'dist/privacy.html', 'dist/refund.html', 'dist/contact.html',
    'dist/jp/terms.html', 'dist/jp/privacy.html', 'dist/jp/refund.html', 'dist/jp/contact.html'
  ]) {
    const fullPath = path.join(ROOT, rel);
    assert.ok(fs.existsSync(fullPath), `Required legal page must exist: ${rel}`);
    const lhtml = fs.readFileSync(fullPath, 'utf8');
    assert.ok(lhtml.includes('Polar.sh (Merchant of Record · Global Card / Apple Pay / Google Pay)'), `${rel} must display Polar.sh MoR label`);
    assert.ok(!/lemonsqueezy|lemon\s*squeezy|296100|d5e7e761|667aa482/i.test(lhtml), `${rel} must have 0 Lemon Squeezy references`);
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
    assert.ok(!/lemonsqueezy|lemon\s*squeezy|296100|d5e7e761|667aa482/i.test(content), `${f} must have 0 Lemon Squeezy references`);
    assert.ok(content.includes('window.PAYMENT_CONFIG') && content.includes("PROVIDER: 'polar_sh'"), `${f} must include Polar.sh window.PAYMENT_CONFIG`);
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
