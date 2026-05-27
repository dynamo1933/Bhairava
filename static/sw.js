// Service Worker for Daiva Anughara PWA
const CACHE_NAME = 'daiva-anughara-v1.0.0';
const STATIC_CACHE = 'daiva-anughara-static-v1.0.0';
const DYNAMIC_CACHE = 'daiva-anughara-dynamic-v1.0.0';

// Files to cache for offline use
const STATIC_FILES = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/countdown.js',
    '/static/js/search.js',
    '/static/images/favicon.ico',
    '/static/images/favicon-32x32.png',
    '/static/images/favicon-16x16.png',
    '/static/images/apple-touch-icon.png',
    '/static/images/android-chrome-192x192.png',
    '/static/images/android-chrome-512x512.png'
];

// Install event - cache static files
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('Caching static files');
                return cache.addAll(STATIC_FILES);
            })
            .then(() => {
                console.log('Static files cached successfully');
                return self.skipWaiting();
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip external requests
    if (url.origin !== self.location.origin) {
        return;
    }

    // Handle different types of requests
    if (request.destination === 'document') {
        // HTML pages - try cache first, then network
        event.respondWith(
            caches.match(request)
                .then((response) => {
                    if (response) {
                        return response;
                    }
                    return fetch(request)
                        .then((fetchResponse) => {
                            // Cache successful responses
                            if (fetchResponse && fetchResponse.status === 200) {
                                const responseClone = fetchResponse.clone();
                                caches.open(DYNAMIC_CACHE)
                                    .then((cache) => {
                                        cache.put(request, responseClone);
                                    });
                            }
                            return fetchResponse;
                        });
                })
        );
    } else if (request.destination === 'style' || request.destination === 'script') {
        // CSS and JS files - cache first strategy
        event.respondWith(
            caches.match(request)
                .then((response) => {
                    if (response) {
                        return response;
                    }
                    return fetch(request)
                        .then((fetchResponse) => {
                            if (fetchResponse && fetchResponse.status === 200) {
                                const responseClone = fetchResponse.clone();
                                caches.open(STATIC_CACHE)
                                    .then((cache) => {
                                        cache.put(request, responseClone);
                                    });
                            }
                            return fetchResponse;
                        });
                })
        );
    } else if (request.destination === 'image') {
        // Images - cache first strategy
        event.respondWith(
            caches.match(request)
                .then((response) => {
                    if (response) {
                        return response;
                    }
                    return fetch(request)
                        .then((fetchResponse) => {
                            if (fetchResponse && fetchResponse.status === 200) {
                                const responseClone = fetchResponse.clone();
                                caches.open(STATIC_CACHE)
                                    .then((cache) => {
                                        cache.put(request, responseClone);
                                    });
                            }
                            return fetchResponse;
                        });
                })
        );
    } else {
        // Other requests - network first strategy
        event.respondWith(
            fetch(request)
                .then((response) => {
                    if (response && response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(DYNAMIC_CACHE)
                            .then((cache) => {
                                cache.put(request, responseClone);
                            });
                    }
                    return response;
                })
                .catch(() => {
                    // Fallback to cache if network fails
                    return caches.match(request);
                })
        );
    }
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-sync') {
        event.waitUntil(
            // Handle background sync tasks
            console.log('Background sync triggered')
        );
    }
});

// Push notification handling
self.addEventListener('push', (event) => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body || 'New spiritual content available',
            icon: '/static/images/android-chrome-192x192.png',
            badge: '/static/images/favicon-32x32.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: 1
            },
            actions: [
                {
                    action: 'explore',
                    title: 'Explore',
                    icon: '/static/images/favicon-32x32.png'
                },
                {
                    action: 'close',
                    title: 'Close',
                    icon: '/static/images/favicon-32x32.png'
                }
            ]
        };

        event.waitUntil(
            self.registration.showNotification(data.title || 'Daiva Anughara', options)
        );
    }
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    } else if (event.action === 'close') {
        // Just close the notification
        return;
    } else {
        // Default action - open the app
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Message handling for communication with main thread
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
