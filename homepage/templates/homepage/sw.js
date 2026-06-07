const CACHE_NAME = "appbuilder-cache-v1";

const urlsToCache = [
  "/",
  "/login/",
  "/dashboard/",
  "/static/manifest.json",
  "/static/icon.png"
];

// Rakibaadda
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log("Feylasha aasaasiga ah waa la keydiyay!");
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// Hawlgallinta
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Maareynta dalabyada (Offline Strategy)
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        if (networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request).then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // Haddii boggu uusan ku jirin cache, halkan waxaad ugu talogali kartaa bog offline ah
        });
      })
  );
});