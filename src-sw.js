import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute, NavigationRoute } from 'workbox-routing';

precacheAndRoute(self.__WB_MANIFEST);

const FALLBACK_PAGE = 'webapp/templates/offline.html';

const navigationRoute = new NavigationRoute(({ event }) => {
  return (async () => {
    try {
      return await fetch(event.request);
    } catch (error) {
      const cache = await caches.open('workbox-precache');
      return cache.match(FALLBACK_PAGE);
    }
  })();
});

registerRoute(navigationRoute);