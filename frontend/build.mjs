import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.join(__dirname, "dist");
const assetsDir = path.join(distDir, "assets");
const publicDir = path.join(__dirname, "public");

fs.mkdirSync(assetsDir, { recursive: true });

const moduleOrder = [
  "src/locales/i18n.js",
  "src/services/api.js",
  "src/components/PositionDoctor.js",
  "src/components/Header.js",
  "src/components/Hero.js",
  "src/components/ProofCard.js",
  "src/components/StockTable.js",
  "src/components/ProVault.js",
  "src/components/Pricing.js",
  "src/components/Modals.js",
  "src/components/SemiFearGreedView.js",
  "src/main.js",
];

function stripImportsAndExports(code) {
  return code
    .replace(/^\s*import\s+[\s\S]*?from\s+["'][^"']+["'];?\s*$/gm, "")
    .replace(/^\s*import\s+["'][^"']+["'];?\s*$/gm, "")
    .replace(/^\s*export\s+(async\s+function|function|const|let|var)\s+/gm, "$1 ");
}

const bundledJs = moduleOrder
  .map((relPath) => {
    const absPath = path.join(__dirname, relPath);
    const raw = fs.readFileSync(absPath, "utf8");
    return `// --- ${relPath} ---\n${stripImportsAndExports(raw)}`;
  })
  .join("\n\n");

const jsFileName = "index-BIziPp23.js";
const cssFileName = "index-CaOpdap3.css";

fs.writeFileSync(path.join(assetsDir, jsFileName), bundledJs, "utf8");

const cssRaw = fs.readFileSync(path.join(__dirname, "src/styles/theme.css"), "utf8");
fs.writeFileSync(path.join(assetsDir, cssFileName), cssRaw, "utf8");

const indexHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <script>window.__DEFAULT_VIEW__ = 'rightside';</script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>RightSideAlpha × SemiFearGreed | 72 US Equity PW-RSI Turnaround Terminal & Semiconductor Fear & Greed Index</title>
  <meta name="description" content="Real-time CNN-Edition Semiconductor Fear & Greed Index (0-100), $SMH/$XLV 70:30 & 80:20 Contrarian Barbell Rebalancing Engine, and 72 US Equity Post-Washout Right-Side Ignition (PW-RSI) Terminal." />
  <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&family=Noto+Sans+JP:wght@400;600;700&family=Noto+Sans+KR:wght@400;600;700&display=swap" rel="stylesheet" />
  <script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
  <script type="module" crossorigin src="./assets/${jsFileName}"></script>
  <link rel="stylesheet" crossorigin href="./assets/${cssFileName}" />
</head>
<body>
  <div id="app"></div>
</body>
</html>
`;

fs.writeFileSync(path.join(distDir, "index.html"), indexHtml, "utf8");

if (fs.existsSync(publicDir)) {
  fs.cpSync(publicDir, distDir, { recursive: true });
}

console.log(`Built frontend/dist successfully (${jsFileName}, ${cssFileName})`);
