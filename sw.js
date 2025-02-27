const CACHE_NAME = 'v1';
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  './booking/01.jpg'
  // 如有其他資源，請加入此陣列中
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('快取開啟成功');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // 若找到快取資源則回傳，否則繼續進行網路請求
        return response || fetch(event.request);
      })
  );
});
