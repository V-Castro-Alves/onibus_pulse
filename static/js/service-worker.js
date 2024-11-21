self.addEventListener('install', function(event) {
    console.log('Service Worker installed');
    self.skipWaiting(); // Ensures the new service worker activates immediately
});

self.addEventListener('activate', function(event) {
    console.log('Service Worker activated');
});

self.addEventListener('push', function(event) {
    var options = {
        body: event.data ? event.data.text() : 'No data available.',
        icon: '/static/icon.png',  // Set a notification icon
        badge: '/static/badge.png',  // Set a notification badge (optional)
    };
    
    event.waitUntil(
        self.registration.showNotification('Bus Notification', options)
    );
});
