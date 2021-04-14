// @ts-ignore
import { build, files, timestamp } from '$service-worker';

import { precacheAndRoute } from 'workbox-precaching';

// // @ts-ignore
precacheAndRoute([...build, ...files]);

self.addEventListener('message', (event) => {
	if (event.data && event.data.type === 'SKIP_WAITING') {
		// @ts-ignore
		self.skipWaiting();
	}
});
