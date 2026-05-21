const CACHE_NAME = "appbuilder-cache-v1";

// Feylasha aasaasiga ah ee loo baahan yahay si uu app-ku u furmo offline-ka
const urlsToCache = [
  "/",
  "/login/",
  "/dashboard/",
  "/static/manifest.json",
  "/static/icon.png"
];

// 1. Marka Service Worker-ka la rakibayo
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log("Feylasha aasaasiga ah waa la keydiyay!");
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// 2. Marka la hawlgalinayo (Tirtir cache-yadii hore haddii nidaamku isbeddelo)
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log("La tirtiray cache-gii hore:", cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 3. Maareynta dalabyada (Fetch Events) - Istiraatiijiyad Offline Adag
self.addEventListener("fetch", event => {
  // Kaliya soo qabo dalabyada GET (iska dhaaf POST/PUT)
  if (event.request.method !== "GET") return;

  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        // Haddii internet jiro, ka keen internet-ka oo nuqul cusub geli Cache-ga (Dynamic Caching)
        if (networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // Haddii internet-ku go'an yahay, si toos ah uga soo jookh Cache-ga
        return caches.match(event.request).then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // Haddii bogga la rabno uusan haba yaraatee cache-ga ku jirin (sida qof offline ah oo app cusub riixay)
          // Waxaad halkan u samayn kartaa bog gaar ah oo la yiraahdo /offline/ hadhow
        });
      })
  );
});