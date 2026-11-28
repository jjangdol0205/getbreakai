/**
 * Cloudflare Pages Function: Legacy /rss -> 301 redirect to /jp/rss.xml
 * Eliminates legacy GSC /rss 404/crawl error cleanly with zero open redirect.
 */
export async function onRequestGet() {
  return new Response(null, {
    status: 301,
    headers: {
      'Location': 'https://getbreakai.com/jp/rss.xml',
      'Cache-Control': 'public, max-age=3600',
      'X-Content-Type-Options': 'nosniff',
    },
  });
}
