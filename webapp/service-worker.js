const cacheVersion = 'v2'; // Update the cache version

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(`my-cache-${cacheVersion}`).then((cache) => { // Use cache version in the cache name
            return cache.addAll([
                '/',
                '/templates/static/styles.css',
                '/templates/static/app.js',
                // Add other assets to cache as needed
            ]);
        })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        // Clear old caches not matching the current cache version
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== `my-cache-${cacheVersion}`) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        // Try to match the request in the cache
        caches.match(event.request).then((response) => {
            return response || fetch(event.request); // Return cached response or fetch from the network
        })
    );
});