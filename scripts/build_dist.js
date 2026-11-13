#!/usr/bin/env node
/**
 * GetBreakAI (3사업부) — Static Site Distribution Builder (./dist)
 * Ensures Render Static Site (Publish Directory: ./dist) always has
 * 100% synchronized HTML, JP deep research pages, assets, and SEO files.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const DIST_DIR = path.join(ROOT_DIR, 'dist');

const ROOT_FILES = [
  'index.html',
  'confirmation.html',
  'contact.html',
  'terms.html',
  'privacy.html',
  'refund.html',
  'CNAME',
  'favicon.svg',
  'og-preview.png',
  'robots.txt',
  'sitemap.xml',
  'llms.txt',
  'gba2026indexnowkey88429104.txt',
  'flow_24_prompts_studio.html',
  'yt_ig_setup_studio.html'
];

const DIRS_TO_COPY = [
  'jp',
  'assets',
  'data',
  'static_api'
];

function copyRecursiveSync(src, dest) {
  if (!fs.existsSync(src)) return;
  const baseName = path.basename(src);
  if (/telegraph_account|secret|token|^\.env/i.test(baseName)) return;
  const stats = fs.statSync(src);
  if (stats.isDirectory()) {
    if (baseName === 'fonts') return; // Local video renderer fonts only; keep ./dist lean
    fs.mkdirSync(dest, { recursive: true });
    for (const entry of fs.readdirSync(src)) {
      copyRecursiveSync(path.join(src, entry), path.join(dest, entry));
    }
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

function buildDist() {
  fs.mkdirSync(DIST_DIR, { recursive: true });
  const leakedAcct = path.join(DIST_DIR, 'data', 'jp_telegraph_account.json');
  if (fs.existsSync(leakedAcct)) {
    try { fs.unlinkSync(leakedAcct); } catch (_) {}
  }

  let copiedFiles = 0;
  for (const fileName of ROOT_FILES) {
    const srcPath = path.join(ROOT_DIR, fileName);
    if (fs.existsSync(srcPath)) {
      fs.copyFileSync(srcPath, path.join(DIST_DIR, fileName));
      copiedFiles++;
    }
  }

  for (const dirName of DIRS_TO_COPY) {
    const srcDir = path.join(ROOT_DIR, dirName);
    const destDir = path.join(DIST_DIR, dirName);
    if (fs.existsSync(srcDir)) {
      copyRecursiveSync(srcDir, destDir);
    }
  }

  // Synchronize Shorts Manifests & Kits
  const studioDir = path.join(ROOT_DIR, 'flow_shorts_studio');
  const distStudio = path.join(DIST_DIR, 'flow_shorts_studio');
  const distData = path.join(DIST_DIR, 'data');
  const manifestSrc = path.join(studioDir, 'mastered_24_shorts_manifest.json');
  if (fs.existsSync(manifestSrc)) {
    fs.mkdirSync(distStudio, { recursive: true });
    fs.mkdirSync(distData, { recursive: true });
    fs.copyFileSync(manifestSrc, path.join(DIST_DIR, 'mastered_24_shorts_manifest.json'));
    fs.copyFileSync(manifestSrc, path.join(distStudio, 'mastered_24_shorts_manifest.json'));
    fs.copyFileSync(manifestSrc, path.join(distData, 'mastered_24_shorts_manifest.json'));
  }
  const kitSrc = path.join(studioDir, 'UPLOAD_COPY_PASTE_KIT_24EP.md');
  if (fs.existsSync(kitSrc)) {
    fs.mkdirSync(distStudio, { recursive: true });
    fs.copyFileSync(kitSrc, path.join(distStudio, 'UPLOAD_COPY_PASTE_KIT_24EP.md'));
  }

  // Synchronize V4 Cinema-Quant Japanese Viral Shorts Manifest & Upload Kit
  const v4ManifestSrc = path.join(studioDir, 'viral_jp_v4', 'viral_jp_v4_manifest.json');
  const v4KitSrc = path.join(studioDir, 'viral_jp_v4', 'VIRAL_UPLOAD_KIT_JP_12EP.md');
  if (fs.existsSync(v4ManifestSrc)) {
    fs.mkdirSync(distStudio, { recursive: true });
    fs.mkdirSync(distData, { recursive: true });
    fs.copyFileSync(v4ManifestSrc, path.join(distStudio, 'viral_jp_v4_manifest.json'));
    fs.copyFileSync(v4ManifestSrc, path.join(distData, 'viral_jp_v4_manifest.json'));
  }
  if (fs.existsSync(v4KitSrc)) {
    fs.mkdirSync(distStudio, { recursive: true });
    fs.copyFileSync(v4KitSrc, path.join(distStudio, 'VIRAL_UPLOAD_KIT_JP_12EP.md'));
  }

  console.log(`[GetBreakAI Build] Synchronized ${copiedFiles} root files + [${DIRS_TO_COPY.join(', ')}] + shorts manifests into ./dist`);
}

buildDist();
