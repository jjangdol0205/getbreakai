/**
 * Dream Company OWASP 2025 Edge Security & Paywall Guard Middleware
 * Blocks direct public access to paid vault PDFs, retired GAS configs, dotfiles, lockfiles, and retired legacy APIs.
 */
const BLOCKED_EXACT = new Set([
  '/hq-mailing-endpoint.json',
  '/jp/hq-mailing-endpoint.json',
  '/assets/downloads/kfg_cdc_growth_guide.pdf',
  '/assets/downloads/tom_master_workbook_2000_2025_14p.pdf',
  '/jp/downloads/gba_jp_nisa_workbook_full.pdf',
  '/assets/downloads/kfk_tier1_masterbook.pdf',
  '/assets/downloads/kfk_tier2_fullpackage.pdf',
  '/samples/kidsfit_master_guide_17p.pdf',
  '/package.json',
  '/package-lock.json',
  '/pnpm-lock.yaml',
  '/yarn.lock',
  '/docker-compose.yml',
  '/.env',
  '/.npmrc',
  '/.yarnrc.yml',
]);

const BLOCKED_PREFIXES = [
  '/.git',
  '/api/lemonsqueezy',
  '/api/cloud-sync',
  '/api/auth/',
  '/products/',
];

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const p = url.pathname.toLowerCase();

  const isBlockedDotfile = p.startsWith('/.') && !p.startsWith('/.well-known/');
  const isBlockedPrefix = BLOCKED_PREFIXES.some((pre) => p === pre || p.startsWith(pre));
  if (BLOCKED_EXACT.has(p) || isBlockedDotfile || isBlockedPrefix) {
    return new Response('410 Gone', {
      status: 410,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-Robots-Tag': 'noindex, nofollow',
      },
    });
  }

  return context.next();
}
