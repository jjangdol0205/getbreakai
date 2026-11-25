/**
 * Cloudflare Pages Function: /go/[slug] (GBA — https://getbreakai.com)
 * 1) Immediate 302 redirect (0ms blocking latency) to fixed same-origin destination with clean internal GA4 UTM.
 * 2) Non-blocking async telemetry via context.waitUntil -> https://api.truthofmarket.com/api/track-go
 * Security: Strict same-origin allowlist (zero open redirect).
 */
const SITE_KEY = "GBA";
const SLUG_MAP = {
  "yt": "https://getbreakai.com/jp/?utm_source=youtube&utm_medium=video&utm_campaign=go_yt",
  "yt-fg": "https://getbreakai.com/jp/smh-fear-greed?utm_source=youtube&utm_medium=video&utm_campaign=go_yt_fg",
  "yt-sample": "https://getbreakai.com/jp/downloads/gba_jp_sample_2p.pdf",
  "yt-guides": "https://getbreakai.com/jp/guides/?utm_source=youtube&utm_medium=video&utm_campaign=go_yt_guides",
  "ig": "https://getbreakai.com/jp/?utm_source=instagram&utm_medium=social&utm_campaign=go_ig",
  "share": "https://getbreakai.com/jp/?utm_source=share_card&utm_medium=referral&utm_campaign=go_share"
};
const DEFAULT_PREFIX = "https://getbreakai.com/jp/?utm_source=go_link&utm_medium=referral&utm_campaign=";

export async function onRequestGet(context) {
  const raw = String((context.params && context.params.slug) || 'yt').toLowerCase().trim();
  const slug = /^[a-z0-9_-]{1,32}$/.test(raw) ? raw : 'yt';
  const dest = Object.prototype.hasOwnProperty.call(SLUG_MAP, slug)
    ? SLUG_MAP[slug]
    : (DEFAULT_PREFIX + encodeURIComponent(slug));

  const ref = String(context.request.headers.get('referer') || '').slice(0, 240);
  const ua = String(context.request.headers.get('user-agent') || '').slice(0, 140);

  if (typeof context.waitUntil === 'function') {
    context.waitUntil(
      fetch('https://api.truthofmarket.com/api/track-go', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          site: SITE_KEY,
          slug: slug,
          ref: ref,
          ua: ua,
          ts: new Date().toISOString()
        })
      }).catch(() => {})
    );
  }

  return new Response(null, {
    status: 302,
    headers: {
      'Location': dest,
      'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
      'X-Robots-Tag': 'noindex, nofollow',
      'X-Content-Type-Options': 'nosniff'
    }
  });
}
