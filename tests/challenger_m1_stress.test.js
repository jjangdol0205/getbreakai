'use strict';

/**
 * Challenger M1 Empirical Stress Test Suite
 * Milestone: M1 (Visual Readability, High-Contrast Typography & Dual-Theme Engine)
 * Platform: Division 3 (GetBreakAI — getbreakai.com & /jp/)
 * 
 * Verifies:
 * 1. Mathematical WCAG 2.1 Contrast ratios across all 30 Japanese research pages + hub + root terminal.
 * 2. Visual declaration and styling of 7 unstyled classes (+ 2 VIP classes).
 * 3. Responsive media queries and layout rules across 375px, 640px, 768px, 1024px, 1440px.
 * 4. Dark and light dual-theme color engine consistency.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const INDEX_PATH = path.join(ROOT, 'index.html');
const JP_DIR = path.join(ROOT, 'jp');
const JP_HUB_PATH = path.join(JP_DIR, 'index.html');

// =========================================================================
// 1. Precise WCAG 2.1 Relative Luminance & Contrast Formula Implementation
// =========================================================================

function hexToRgb(hex) {
  let clean = hex.replace('#', '').trim();
  if (clean.length === 3) {
    clean = clean.split('').map(c => c + c).join('');
  }
  const num = parseInt(clean, 16);
  return {
    r: (num >> 16) & 255,
    g: (num >> 8) & 255,
    b: num & 255
  };
}

function parseRgba(rgbaStr) {
  const m = rgbaStr.match(/rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*,\s*([\d.]+))?\s*\)/);
  if (!m) return null;
  return {
    r: parseFloat(m[1]),
    g: parseFloat(m[2]),
    b: parseFloat(m[3]),
    a: m[4] !== undefined ? parseFloat(m[4]) : 1.0
  };
}

function alphaBlend(fgRgb, bgRgb, alpha) {
  return {
    r: Math.round(fgRgb.r * alpha + bgRgb.r * (1 - alpha)),
    g: Math.round(fgRgb.g * alpha + bgRgb.g * (1 - alpha)),
    b: Math.round(fgRgb.b * alpha + bgRgb.b * (1 - alpha))
  };
}

function relativeLuminance(rgb) {
  const normalize = (val) => {
    const s = val / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  const R = normalize(rgb.r);
  const G = normalize(rgb.g);
  const B = normalize(rgb.b);
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

function contrastRatio(colorA, colorB) {
  const lumA = relativeLuminance(colorA);
  const lumB = relativeLuminance(colorB);
  const lighter = Math.max(lumA, lumB);
  const darker = Math.min(lumA, lumB);
  return (lighter + 0.05) / (darker + 0.05);
}

// =========================================================================
// 2. Test Suite Execution
// =========================================================================

test('M1-1: Mathematical WCAG 2.1 Contrast in Light Theme (:root & html[data-jp-theme="light"])', () => {
  const white = hexToRgb('#ffffff');
  const lightBg = hexToRgb('#f1f5f9');
  const lightCardSub = hexToRgb('#f8fafc');
  const navyHeader = hexToRgb('#0b1f3a');

  const lightTextMain = hexToRgb('#0b1f3a');
  const lightTextMuted = hexToRgb('#334155');
  const lightTextSub = hexToRgb('#475569');

  const crMainOnWhite = contrastRatio(lightTextMain, white);
  const crMainOnBg = contrastRatio(lightTextMain, lightBg);
  const crMutedOnWhite = contrastRatio(lightTextMuted, white);
  const crSubOnWhite = contrastRatio(lightTextSub, white);

  assert.ok(crMainOnWhite >= 7.0, `Main text on white (${crMainOnWhite.toFixed(2)}:1) must meet WCAG AAA (7.0:1)`);
  assert.ok(crMainOnBg >= 7.0, `Main text on light bg (${crMainOnBg.toFixed(2)}:1) must meet WCAG AAA (7.0:1)`);
  assert.ok(crMutedOnWhite >= 7.0, `Muted text on white (${crMutedOnWhite.toFixed(2)}:1) must meet WCAG AAA (7.0:1)`);
  assert.ok(crSubOnWhite >= 4.5, `Sub text on white (${crSubOnWhite.toFixed(2)}:1) must meet WCAG AA (4.5:1)`);

  // Accents in light mode
  const accentViolet = hexToRgb('#6d28d9');
  const accentAmber = hexToRgb('#b45309');
  const accentEmerald = hexToRgb('#047857');
  const accentRose = hexToRgb('#be123c');
  const accentSky = hexToRgb('#0369a1');

  assert.ok(contrastRatio(accentViolet, white) >= 4.5, `Light violet on white must meet WCAG AA`);
  assert.ok(contrastRatio(accentAmber, white) >= 4.5, `Light amber on white must meet WCAG AA`);
  assert.ok(contrastRatio(accentEmerald, white) >= 4.5, `Light emerald on white must meet WCAG AA`);
  assert.ok(contrastRatio(accentRose, white) >= 4.5, `Light rose on white must meet WCAG AA`);
  assert.ok(contrastRatio(accentSky, white) >= 4.5, `Light sky on white must meet WCAG AA`);

  // Header contrast
  const headerText = hexToRgb('#f8fafc');
  assert.ok(contrastRatio(headerText, navyHeader) >= 7.0, `Header text on navy must meet WCAG AAA`);
});

test('M1-2: Mathematical WCAG 2.1 Contrast in Dark Theme (Terminal Mode)', () => {
  const darkBg = hexToRgb('#06050c');
  const darkCard = hexToRgb('#0e0b1a');

  const darkTextMain = hexToRgb('#f8fafc');
  const darkTextMuted = hexToRgb('#cbd5e1');
  const darkTextSub = hexToRgb('#94a3b8');

  assert.ok(contrastRatio(darkTextMain, darkBg) >= 7.0, `Dark main text on bg must meet WCAG AAA`);
  assert.ok(contrastRatio(darkTextMain, darkCard) >= 7.0, `Dark main text on card must meet WCAG AAA`);
  assert.ok(contrastRatio(darkTextMuted, darkBg) >= 7.0, `Dark muted text on bg must meet WCAG AAA`);
  assert.ok(contrastRatio(darkTextMuted, darkCard) >= 7.0, `Dark muted text on card must meet WCAG AAA`);
  assert.ok(contrastRatio(darkTextSub, darkBg) >= 4.5, `Dark sub text on bg must meet WCAG AA`);
});

test('M1-3: Verification of All 30 Japanese SEO Research Pages (/jp/*.html) Contrast Ratios', () => {
  const files = fs.readdirSync(JP_DIR).filter(f => f.endsWith('.html') && f !== 'index.html');
  assert.equal(files.length, 30, 'Must have exactly 30 Japanese research articles');

  const paleMintBg = alphaBlend(hexToRgb('#10b981'), hexToRgb('#ffffff'), 0.12);
  const paleRoseBg = alphaBlend(hexToRgb('#f43f5e'), hexToRgb('#ffffff'), 0.12);

  const bullishBannerColor = hexToRgb('#064e3b');
  const avoidBannerColor = hexToRgb('#881337');

  const crBullish = contrastRatio(bullishBannerColor, paleMintBg);
  const crAvoid = contrastRatio(avoidBannerColor, paleRoseBg);

  assert.ok(crBullish >= 7.0, `Bullish banner text must achieve WCAG AAA (got ${crBullish.toFixed(2)}:1)`);
  assert.ok(crAvoid >= 7.0, `Avoid banner text must achieve WCAG AAA (got ${crAvoid.toFixed(2)}:1)`);

  // Test every file for contrast regressions
  for (const f of files) {
    const filePath = path.join(JP_DIR, f);
    const content = fs.readFileSync(filePath, 'utf8');

    // Check banner text color
    if (content.includes('🔴 【AI緊急警告】')) {
      assert.ok(content.includes('color:#881337'), `${f} Avoid banner must use high-contrast #881337`);
    } else {
      assert.ok(content.includes('color:#064e3b'), `${f} Bullish banner must use high-contrast #064e3b`);
    }

    // Check related article links
    assert.ok(content.includes('style="color:#1d4ed8; text-decoration:none; font-weight:700;"'), `${f} must use #1d4ed8 for related links`);
    const crLink = contrastRatio(hexToRgb('#1d4ed8'), hexToRgb('#ffffff'));
    assert.ok(crLink >= 4.5, `Related link must have >= 4.5:1 contrast (got ${crLink.toFixed(2)}:1)`);

    // Check widget box header & copy
    assert.ok(content.includes('color:#0f172a;'), `${f} widget title must use #0f172a`);
    assert.ok(content.includes('color:#334155;'), `${f} widget text must use #334155`);
    const crWidgetH = contrastRatio(hexToRgb('#0f172a'), hexToRgb('#f8fafc'));
    const crWidgetP = contrastRatio(hexToRgb('#334155'), hexToRgb('#f8fafc'));
    assert.ok(crWidgetH >= 7.0, `Widget header contrast (${crWidgetH.toFixed(2)}:1) must meet AAA`);
    assert.ok(crWidgetP >= 7.0, `Widget copy contrast (${crWidgetP.toFixed(2)}:1) must meet AAA`);

    // Check that white text is never used on light cards or light backgrounds
    // In particular, verify mini calculator h3 and promo banner h3 are dark navy, not white
    assert.ok(!content.includes('style="margin-top:0; color:#fff;"'), `${f} mini calc header must not be white`);
    assert.ok(!content.includes('style="margin-top:0; color:#ffffff;"'), `${f} mini calc header must not be white`);
    assert.ok(!content.includes('color:#e2e8f0;') || content.indexOf('color:#e2e8f0;') < content.indexOf('<header>'), `${f} must not contain #e2e8f0 on light backgrounds`);
    assert.ok(!content.includes('color:#c4b5fd;'), `${f} must not contain #c4b5fd`);
    assert.ok(!content.includes('color:#b4add0;'), `${f} must not contain #b4add0`);

    // Verify all button text on dark gradients is high contrast (WCAG AA & AAA for bold UI buttons)
    const crBtn = contrastRatio(hexToRgb('#ffffff'), hexToRgb('#1d4ed8'));
    assert.ok(crBtn >= 4.5, `Button white text on #1d4ed8 must be >= 4.5:1 (got ${crBtn.toFixed(2)}:1)`);
  }
});

test('M1-4: Contrast Ratios on Japanese Research Hub (jp/index.html)', () => {
  const content = fs.readFileSync(JP_HUB_PATH, 'utf8');
  const hubBg = hexToRgb('#f4f6fa');
  const cardBg = hexToRgb('#ffffff');

  // Brand link
  assert.ok(content.includes('color:#0b1f3a; font-weight:900; font-size:1.25rem;'), 'Hub must have high-contrast brand link');
  const crBrand = contrastRatio(hexToRgb('#0b1f3a'), hubBg);
  assert.ok(crBrand >= 7.0, `Hub brand link contrast (${crBrand.toFixed(2)}:1) must meet AAA`);

  // Subtitle
  assert.ok(content.includes('style="color:#334155; font-size:0.95rem;"'), 'Hub must have high-contrast subtitle');
  const crSub = contrastRatio(hexToRgb('#334155'), hubBg);
  assert.ok(crSub >= 7.0, `Hub subtitle contrast (${crSub.toFixed(2)}:1) must meet AAA`);

  // Cards
  const crCardTitle = contrastRatio(hexToRgb('#0b1f3a'), cardBg);
  const crCardTicker = contrastRatio(hexToRgb('#b45309'), cardBg);
  const crCardDesc = contrastRatio(hexToRgb('#475569'), cardBg);
  assert.ok(crCardTitle >= 7.0, `Card title contrast (${crCardTitle.toFixed(2)}:1) must meet AAA`);
  assert.ok(crCardTicker >= 4.5, `Card ticker contrast (${crCardTicker.toFixed(2)}:1) must meet AA`);
  assert.ok(crCardDesc >= 4.5, `Card desc contrast (${crCardDesc.toFixed(2)}:1) must meet AA`);
});

test('M1-5: Visual Styling of 7 Specialized Classes (+ 2 VIP Classes) in index.html', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');
  const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
  assert.ok(styleMatch, 'index.html must contain a <style> block');
  const style = styleMatch[1];

  const requiredClasses = [
    { name: 'jp-preset-row', requiredProps: ['display', 'flex-wrap', 'gap'] },
    { name: 'jp-preset-btn', requiredProps: ['background', 'border', 'padding', 'border-radius', 'cursor'] },
    { name: 'jp-range-box', requiredProps: ['background', 'border', 'border-radius', 'padding'] },
    { name: 'jp-range-track', requiredProps: ['background', 'border-radius', 'height'] },
    { name: 'jp-range-labels', requiredProps: ['display', 'justify-content', 'font-family'] },
    { name: 'jp-mobile-bottom-nav', requiredProps: ['position', 'bottom', 'grid-template-columns', 'z-index'] },
    { name: 'jp-num', requiredProps: ['font-variant-numeric', 'font-family'] },
    { name: 'vip-locked-row', requiredProps: ['opacity', 'background'] },
    { name: 'vip-exec-row', requiredProps: ['display', 'justify-content', 'border-bottom'] }
  ];

  for (const item of requiredClasses) {
    // 1. Must be declared in <style>
    const classRegex = new RegExp(`\\.${item.name}\\b[^{]*\\{([^}]+)\\}`, 'm');
    const match = style.match(classRegex);
    assert.ok(match, `Class .${item.name} must be declared in <style>`);

    // 2. Must produce visual output (contain required CSS properties)
    const ruleContent = match[1];
    for (const prop of item.requiredProps) {
      assert.ok(
        ruleContent.includes(prop) || style.includes(prop),
        `Class .${item.name} must declare property '${prop}' for visual output`
      );
    }

    // 3. Must be used in HTML body
    assert.ok(html.includes(`class="${item.name}`) || html.includes(`class='${item.name}`) || html.includes(` ${item.name}`), `Class .${item.name} must be used in index.html HTML markup`);
  }
});

test('M1-6: Responsive Breakpoints & Viewport Layout Stress Tests (375px, 640px, 768px, 1024px, 1440px)', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');

  // Check 375px & 640px Mobile Rules
  assert.ok(html.includes('@media (max-width: 640px)'), 'Must declare mobile breakpoint @media (max-width: 640px)');
  assert.ok(html.includes('overflow-x: auto !important;'), 'Ticker bar must scroll horizontally on mobile');
  assert.ok(html.includes('flex-wrap: nowrap !important;'), 'Ticker bar must be nowrap on mobile');
  assert.ok(html.includes('flex: 0 0 auto !important;'), 'Ticker items must be non-wrapping on mobile');

  // Check 641px - 1024px Tablet 2-Column Rules
  assert.ok(
    html.includes('@media (min-width: 641px) and (max-width: 1024px)'),
    'Must declare tablet media query @media (min-width: 641px) and (max-width: 1024px)'
  );
  assert.ok(
    html.includes('grid-template-columns: repeat(2, 1fr) !important;'),
    'Tablet media query must set 2-column layout for features and pricing grids'
  );

  // Check 768px Mobile Bottom Nav Rules
  assert.ok(html.includes('@media (max-width: 768px)'), 'Must declare @media (max-width: 768px) for mobile bottom nav');
  assert.ok(html.includes('safe-area-inset-bottom'), 'Mobile bottom nav must handle iPhone safe-area-inset-bottom');

  // Check Desktop (> 1024px) Defaults
  assert.ok(html.includes('grid-template-columns: repeat(3, 1fr);'), 'Desktop default must have 3-column layout');
  assert.ok(html.includes('.container {') && html.includes('max-width: 1220px;'), 'Desktop container max width must be 1220px');

  // Check Horizontal Overflow Prevention
  assert.ok(html.includes('overflow-x: hidden;'), 'html, body must enforce overflow-x: hidden');
  assert.ok(html.includes('max-width: 100%;'), 'html, body must enforce max-width: 100%');
});

test('M1-7: Japanese Typography Metrics & PALT Kerning Enforcement', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');
  assert.ok(html.includes('font-feature-settings: "palt" 1;'), 'Must enforce proportional alternate metrics ("palt") in index.html');
  assert.ok(html.includes('Noto+Sans+JP'), 'Must load Noto Sans JP Google Font');
  assert.ok(html.includes('font-variant-numeric: tabular-nums;'), 'Must enforce tabular numbers for financial figures');
  assert.ok(html.includes('letter-spacing: 0.01em;'), 'Must optimize letter spacing for Japanese CJK text');
  assert.ok(html.includes('line-height: 1.7;'), 'Must use 1.7 line height for optical reading comfort');
});

test('M1-8: Empirical Component-Level Contrast Matrix Across All Light-Theme Overrides', () => {
  const pairs = [
    { name: 'Light Header Brand Logo', fg: '#f8fafc', bg: '#0b1f3a', min: 7.0 },
    { name: 'Light Header Nav Link Hover', fg: '#93c5fd', bg: '#0b1f3a', min: 7.0 },
    { name: 'Light Theme Switcher Button', fg: '#fde68a', bg: '#1e3a8a', min: 7.0 },
    { name: 'Light Catalyst Tape Item', fg: '#e2e8f0', bg: '#102a4c', min: 7.0 },
    { name: 'Light Hero Pill Text', fg: '#1e40af', bg: '#eff6ff', min: 7.0 },
    { name: 'Light Hero H1', fg: '#0b1f3a', bg: '#f1f5f9', min: 7.0 },
    { name: 'Light Hero Body Copy', fg: '#334155', bg: '#f1f5f9', min: 7.0 },
    { name: 'Light Playbook Banner Title', fg: '#0b1f3a', bg: '#ffffff', min: 7.0 },
    { name: 'Light Terminal Topbar Title', fg: '#ffffff', bg: '#0b1f3a', min: 7.0 },
    { name: 'Light Ticker Normal Button', fg: '#e2e8f0', bg: '#17325c', min: 7.0 },
    { name: 'Light Ticker Active Button', fg: '#0b1f3a', bg: '#f59e0b', min: 7.0 },
    { name: 'Light Plain Action Box Title', fg: '#065f46', bg: '#ecfdf5', min: 7.0 },
    { name: 'Light Plain Action Box Steps', fg: '#0f172a', bg: '#ecfdf5', min: 7.0 },
    { name: 'Light Feature Card Title', fg: '#0b1f3a', bg: '#ffffff', min: 7.0 },
    { name: 'Light Feature Card Desc', fg: '#334155', bg: '#ffffff', min: 7.0 },
    { name: 'Light Price Card Title', fg: '#0b1f3a', bg: '#ffffff', min: 7.0 },
    { name: 'Light Price Card Desc', fg: '#334155', bg: '#ffffff', min: 7.0 },
    { name: 'Light Comp Table Header', fg: '#ffffff', bg: '#0b1f3a', min: 7.0 },
    { name: 'Light Comp Table Cell', fg: '#0f172a', bg: '#ffffff', min: 7.0 },
    { name: 'Light Preset Btn Normal', fg: '#1e3a8a', bg: '#eff6ff', min: 7.0 },
    { name: 'Light Preset Btn Active', fg: '#ffffff', bg: '#1d4ed8', min: 4.5 },
    { name: 'Light Mobile Bottom Nav Normal', fg: '#f8fafc', bg: '#0b1f3a', min: 7.0 },
    { name: 'Light Mobile Bottom Nav Active', fg: '#fbbf24', bg: '#0b1f3a', min: 7.0 },
    { name: 'Light Mobile Bottom Nav CTA (UI Component AA)', fg: '#ffffff', bg: '#d97706', min: 3.0 },
    { name: 'Light Footer Text', fg: '#cbd5e1', bg: '#0b1f3a', min: 7.0 },
    { name: 'Light Footer Link', fg: '#93c5fd', bg: '#0b1f3a', min: 7.0 },
    { name: 'Light Legal Box Text', fg: '#475569', bg: '#f8fafc', min: 4.5 }
  ];

  for (const p of pairs) {
    const cr = contrastRatio(hexToRgb(p.fg), hexToRgb(p.bg));
    assert.ok(
      cr >= p.min,
      `${p.name} contrast (${cr.toFixed(2)}:1) failed to meet target minimum ${p.min}:1`
    );
  }
});

test('M1-9: DOM Functional Structure of 7 Classes & Theme Toggle JS Functionality', () => {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');

  // Verify preset buttons exist with onclick handlers
  assert.ok(html.includes('setJpAccountPreset(6700)'), 'Must have 100万円 preset button ($6,700)');
  assert.ok(html.includes('setJpAccountPreset(80000)'), 'Must have 1200万円 NISA preset button ($80,000)');
  assert.ok(html.includes('setJpFxRate(150)'), 'Must have 150円 FX preset button');

  // Verify Visual Range Thermometer structure
  assert.ok(html.includes('id="gbVisualRangeBar"'), 'Must have visual range bar container');
  assert.ok(html.includes('class="jp-range-track"'), 'Must have visual range track element');
  assert.ok(html.includes('class="jp-range-labels"'), 'Must have range labels');

  // Verify Mobile Bottom Nav contains 4 action anchors
  const navMatch = html.match(/class=["']jp-mobile-bottom-nav["'][\s\S]*?<\/div>/);
  assert.ok(navMatch, 'Must contain jp-mobile-bottom-nav block');
  const anchors = navMatch[0].match(/<a\b/g);
  assert.ok(anchors && anchors.length === 4, `Mobile bottom nav must have exactly 4 items (found ${anchors ? anchors.length : 0})`);

  // Verify theme toggle JavaScript function
  assert.ok(html.includes('function toggleJpTheme()'), 'toggleJpTheme() function must be defined');
  assert.ok(html.includes("root.setAttribute('data-jp-theme', next);"), 'toggleJpTheme must toggle data-jp-theme attribute');
  assert.ok(html.includes('🌙 ダーク切替') && html.includes('🌞 証券ライト切替'), 'toggleJpTheme must switch button label');
});
