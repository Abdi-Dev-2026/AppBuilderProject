const CACHE_NAME = "app-cache-v1";

const urlsToCache = [
  "/",
  "/login/",
  "/dashboard/",
  "/static/css/style.css", // Hubi in magaca file-kaaga CSS uu kan yahay
  "/static/js/app.js",     // Haddii aadan lahayn app.js, waad ka saari kartaa khadkan
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
          console.log("Faylasha waa la keydiyay (Caching)!");
          return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Haddii faylka uu ku jiro Cache, soo celi, haddii kale internet-ka ka doon
        return response || fetch(event.request);
      })
  );
});