/**
 * Dream Company OWASP 2025 Edge Security, Paywall Guard & Fail-Open CRO Slot SSR Middleware (GBA — Division 3)
 * - Blocks direct public access to paid vault PDFs, retired GAS configs, dotfiles, lockfiles, and retired legacy APIs.
 * - For GET /, /index.html, /jp, /jp/, /jp/index.html only: applies Sanctuary-safe text-only (html:false) Edge HTMLRewriter slots from R2.
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
  '/flow_24_prompts_studio',
  '/flow_24_prompts_studio.html',
  '/yt_ig_setup_studio',
  '/yt_ig_setup_studio.html',
  '/data/jp_telegraph_account.json',
  '/data/shorts-state.json',
  '/assets/youtube/youtube_insta_channel_config.json',
  '/static_api/stocks_free.json',
]);

const BLOCKED_PREFIXES = [
  '/.git',
  '/api/lemonsqueezy',
  '/api/cloud-sync',
  '/api/auth/',
  '/products/',
];

const CRO_TARGET_PATHS = new Set(['/', '/index.html', '/jp', '/jp/', '/jp/index.html']);
const R2_CRO_BASE = 'https://pub-c1592ad8d860431c9bf3d4dd12c228ef.r2.dev/cro';
const ALLOWED_DENSITY = new Set(['cro-pad-compact', 'cro-pad-airy']);
const GBA_FORBIDDEN_RE = /(?:<|>|javascript:|on(?:click|error|load|submit|input)\s*=|[\uAC00-\uD7A3]|t\.me|telegram|\u30c6\u30ec\u30b0\u30e9\u30e0|\u30af\u30aa\u30f3\u30c4|\u30aa\u30eb\u30ab\u30f3|1489|\bvym\b|\bclinical\b|\b1:1\b|1\u5bfe1|lemonsqueezy|beable9489|trycloudflare\.com)/i;
const SLOT_SELECTORS_GBA = [
  ['hero_h1', 'h1.pw-serif-h1'],
  ['cta_primary', '#btnStartPwStepUpJp'],
  ['gate_cta', '#gba-jp-club-submit'],
];

async function fetchCroSlotConfig(div, previewId, bypassCache) {
  const ctrl = new AbortController();
  const timeoutMs = (previewId || bypassCache) ? 2500 : 1200;
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const targetUrl = previewId
      ? `${R2_CRO_BASE}/${div}_staging_${previewId}.json?nc=${Date.now()}`
      : (bypassCache
          ? `${R2_CRO_BASE}/${div}_active.json?nc=${Date.now()}`
          : `${R2_CRO_BASE}/${div}_active.json`);
    const opts = {
      signal: ctrl.signal,
      headers: { Accept: 'application/json' },
    };
    if (previewId || bypassCache) {
      opts.cf = { cacheTtl: 0 };
    } else {
      opts.cf = { cacheTtl: 30, cacheEverything: true };
    }
    const r = await fetch(targetUrl, opts);
    if (!r || !r.ok) return null;
    const j = await r.json();
    if (!j || typeof j !== 'object') return null;
    return j;
  } catch (_) {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

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

  const resp = await context.next();

  // Fail-Open Edge CRO Slot SSR — strictly GET /, /index.html, /jp, /jp/, /jp/index.html returning 200 text/html only
  if (context.request.method !== 'GET' || !CRO_TARGET_PATHS.has(p)) {
    return resp;
  }
  const ct = String(resp.headers.get('Content-Type') || '').toLowerCase();
  if (resp.status !== 200 || !ct.includes('text/html')) {
    return resp;
  }

  const rawPreview = String(url.searchParams.get('cro_preview') || '').trim();
  const previewId = /^[A-Za-z0-9_\-]{4,64}$/.test(rawPreview) ? rawPreview : '';
  const bypassCache = Boolean(
    previewId ||
    url.searchParams.has('nocache') ||
    String(context.request.headers.get('Cache-Control') || '').toLowerCase().includes('no-cache')
  );

  const cfg = await fetchCroSlotConfig('GBA', previewId, bypassCache);
  if (!cfg) return resp;

  const slots = (cfg.slots && typeof cfg.slots === 'object') ? cfg.slots : {};
  const density = ALLOWED_DENSITY.has(String(cfg.density || '')) ? String(cfg.density) : '';
  const expId = String(cfg.active_exp_id || '').replace(/[^A-Za-z0-9_,\-]/g, '').slice(0, 100);
  const hasAnySlot = SLOT_SELECTORS_GBA.some(([k]) => typeof slots[k] === 'string' && slots[k].trim().length >= 3);

  if (!hasAnySlot && !density) {
    return resp;
  }

  try {
    let rewriter = new HTMLRewriter();
    if (expId) {
      rewriter = rewriter.on('head', {
        element(el) {
          el.append(`<meta name="dc-cro-exp" content="${expId}">`, { html: true });
        },
      });
    }
    if (density) {
      rewriter = rewriter.on('body', {
        element(el) {
          el.setAttribute('data-cro-density', density);
        },
      });
    }
    for (const [slotKey, selector] of SLOT_SELECTORS_GBA) {
      const val = typeof slots[slotKey] === 'string' ? slots[slotKey].trim() : '';
      if (val && val.length <= 220 && !GBA_FORBIDDEN_RE.test(val)) {
        rewriter = rewriter.on(selector, {
          element(el) {
            el.setInnerContent(val, { html: false });
          },
        });
      }
    }
    const transformed = rewriter.transform(resp);
    const outHeaders = new Headers(transformed.headers);
    if (expId) outHeaders.set('X-DC-CRO-Exp', expId);
    if (previewId) outHeaders.set('Cache-Control', 'no-store, max-age=0');
    return new Response(transformed.body, {
      status: transformed.status,
      statusText: transformed.statusText,
      headers: outHeaders,
    });
  } catch (_) {
    return resp;
  }
}
