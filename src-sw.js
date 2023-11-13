import { precacheAndRoute, matchPrecache } from 'workbox-precaching';

// Precache your assets
precacheAndRoute(self.__WB_MANIFEST);

// Implement the fetch event to serve from cache first
self.addEventListener('fetch', (event) => {
  // Respond with cached content if available
  const cachedResponse = matchPrecache(event.request);
  event.respondWith(
    cachedResponse || fetch(event.request).catch(() => {
      // Fallback to an offline page if the request can't be fulfilled
      return caches.match('webapp/templates/offline.html');
    })
  );
});




