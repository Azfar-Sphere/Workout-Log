import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute, NavigationRoute } from 'workbox-routing';

precacheAndRoute([{"revision":"3412d89984e53cb0f92a8a504bef0cd9","url":"main.py"},{"revision":"9ea998eeaf8cea3c52d8c4742b9d94c2","url":"manifest.json"},{"revision":"91f2dce1125c6ef7f876d2c8e335c1c7","url":"README.md"},{"revision":"fc17be497b27d6e45b075f89952d82bb","url":"webapp/__init__.py"},{"revision":"cc6745becfbc078abf29e183eb30685c","url":"webapp/__pycache__/__init__.cpython-310.pyc"},{"revision":"8b37e44b56c6f7ed8287d432f3bff176","url":"webapp/__pycache__/app.cpython-310.pyc"},{"revision":"bf3b574cdc69ef94d7e0c129b20006e9","url":"webapp/__pycache__/auth.cpython-310.pyc"},{"revision":"c815e51a694d8ded3c118697b90c49a3","url":"webapp/__pycache__/pwa_routes.cpython-310.pyc"},{"revision":"d0c0552ce17f450da58508ff10eb88f1","url":"webapp/__pycache__/routes.cpython-310.pyc"},{"revision":"08eacf9c75aa58d91f2c40a360bebfb8","url":"webapp/__pycache__/tables.cpython-310.pyc"},{"revision":"c8faa45badd28bed59a221a0cc4f6eb7","url":"webapp/auth.py"},{"revision":"784d483f9eb7747a9e82fce7ae4c88e0","url":"webapp/data.db"},{"revision":"644451755fb029b2da91e03d555137e9","url":"webapp/pwa_routes.py"},{"revision":"34f324d81aa3b54f1eb0903ad500f22b","url":"webapp/routes.py"},{"revision":"a96497da8418346e2beebc58b70affde","url":"webapp/tables.py"},{"revision":"ab8bf0dbf69a1f75cbf1db3e671554d2","url":"webapp/templates/error.html"},{"revision":"818e9378d9577227b1a09999bd294562","url":"webapp/templates/index.html"},{"revision":"ce54e44c2e20bdfdf733045690352420","url":"webapp/templates/layout.html"},{"revision":"8b9ee492740e5d58e2f4902007f29c4b","url":"webapp/templates/login.html"},{"revision":"9f1d2206eb11e2c4687258ed84fc5090","url":"webapp/templates/offline.html"},{"revision":"3b0b816d520c766c78a0df87fde3ae5a","url":"webapp/templates/register.html"},{"revision":"d41d8cd98f00b204e9800998ecf8427e","url":"webapp/templates/static/app.js"},{"revision":"72ee8587ee8133729a059ee0af51da59","url":"webapp/templates/static/icon.png"},{"revision":"0c625c7fc4434c43721b4f1ba088eb2b","url":"webapp/templates/static/manifest-icon-192.maskable.png"},{"revision":"8e4e32f25ddc2ffa814d9846814227cb","url":"webapp/templates/static/manifest-icon-512.maskable.png"},{"revision":"d41d8cd98f00b204e9800998ecf8427e","url":"webapp/templates/static/styles.css"},{"revision":"d4fc1ad7ca02c8228e983b22606382e4","url":"webapp/templates/static/workout.js"},{"revision":"fac2dfe7cd51179b4f9cfdbafe07f7d4","url":"webapp/templates/workout.html"},{"revision":"58cb8a550903930086c74d75c51cfeb0","url":"workbox-8ecedfd2.js"},{"revision":"d1def1a460ff6e7aacc168ace68dc38e","url":"workbox-config.js"}]);

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