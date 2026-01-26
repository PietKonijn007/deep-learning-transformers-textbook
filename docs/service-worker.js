// Deep Learning Textbook Service Worker
const CACHE_NAME = 'dl-textbook-v1';

// Files to cache for offline access
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/css/style.css',
  '/js/main.js',
  '/manifest.json',
  '/chapters/preface.html',
  '/chapters/notation.html',
  '/chapters/chapter01_linear_algebra.html',
  '/chapters/chapter02_calculus_optimization.html',
  '/chapters/chapter03_probability_information.html',
  '/chapters/chapter04_feedforward_networks.html',
  '/chapters/chapter05_convolutional_networks.html',
  '/chapters/chapter06_recurrent_networks.html',
  '/chapters/chapter07_attention_fundamentals.html',
  '/chapters/chapter08_self_attention.html',
  '/chapters/chapter09_attention_variants.html',
  '/chapters/chapter10_transformer_model.html',
  '/chapters/chapter11_training_transformers.html',
  '/chapters/chapter12_computational_analysis.html',
  '/chapters/chapter13_bert.html',
  '/chapters/chapter14_gpt.html',
  '/chapters/chapter15_t5_bart.html',
  '/chapters/chapter16_efficient_transformers.html',
  '/chapters/chapter17_vision_transformers.html',
  '/chapters/chapter18_multimodal_transformers.html',
  '/chapters/chapter19_long_context.html',
  '/chapters/chapter20_pretraining_strategies.html',
  '/chapters/chapter21_pytorch_implementation.html',
  '/chapters/chapter22_hardware_optimization.html',
  '/chapters/chapter23_best_practices.html'
];

// External resources to cache
const EXTERNAL_ASSETS = [
  'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(name => name !== CACHE_NAME)
            .map(name => caches.delete(name))
        );
      })
      .then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          // Return cached version
          return cachedResponse;
        }

        // Not in cache, fetch from network
        return fetch(event.request)
          .then(response => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            // Cache the fetched resource
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch(() => {
            // Network failed, return offline page if available
            if (event.request.destination === 'document') {
              return caches.match('/index.html');
            }
          });
      })
  );
});
