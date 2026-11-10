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
  'data'
];

function copyRecursiveSync(src, dest) {
  if (!fs.existsSync(src)) return;
  const stats = fs.statSync(src);
  if (stats.isDirectory()) {
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

  console.log(`[GetBreakAI Build] Synchronized ${copiedFiles} root files + [${DIRS_TO_COPY.join(', ')}] + shorts manifests into ./dist`);
}

buildDist();
