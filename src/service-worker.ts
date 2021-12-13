import { build, files, timestamp } from '$service-worker';

// @ts-ignore
importScripts('/workbox-v6.4.2/workbox-sw.js');

workbox.setConfig({
	// debug: true,
	modulePathPrefix: '/workbox-v6.4.2'
});

workbox.loadModule('workbox-precaching');

workbox.precaching.precacheAndRoute([...build, ...files]);

// @ts-ignore-file
self.addEventListener('message', (event) => {
	if (event.data && event.data.type === 'SKIP_WAITING') {
		// @ts-ignore
		self.skipWaiting();
	}
});
