/* Self-Unregistering Kill-Switch Service Worker (2026-11-28)
 * Purges all legacy caches and unregisters itself so browsers always load fresh Cloudflare Pages builds.
 */
self.addEventListener('install', function () {
  self.skipWaiting();
});
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) { return Promise.all(keys.map(function (k) { return caches.delete(k); })); })
      .then(function () { return self.registration.unregister(); })
      .then(function () { return self.clients.matchAll({ type: 'window' }); })
      .then(function (clients) {
        clients.forEach(function (client) {
          try { client.navigate(client.url); } catch (_e) {}
        });
      })
  );
});
