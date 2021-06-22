<script>
	import 'tailwindcss/tailwind.css';
	import '../app.scss';
	import store from '$store';
	import Prompt from '$components/prompt.svelte';

	import Nav from '$components/nav.svelte';
	import { dev, browser } from '$app/env';

	const base_url = store.state.base_url;
	if (!dev && browser) {
		(async () => {
			if ('serviceWorker' in navigator) {
				const { Workbox, messageSW } = await import('workbox-window');
				const sw_url = base_url + 'service-worker.js';
				const wb = new Workbox(sw_url);
				let registration;

				const showSkipWaitingPrompt = (event) => {
					store.dispatch('showPrompt', {
						message:
							'New version of webapp is alredy downloaded. Can we activate it now and restart the app?',
						acceptText: 'yes sure',
						dismissText: 'no later',
						onaccept: () => {
							// fires when the waiting service worker becomes active
							wb.addEventListener('controlling', (event) => {
								window.location.reload();
							});

							// since the user accepted the prompt we should skip_waiting
							if (registration?.waiting) {
								messageSW(registration.waiting, { type: 'SKIP_WAITING' });
							}
						}
					});
				};

				// fires when service worker has installed but is waiting to activate.
				wb.addEventListener('waiting', showSkipWaitingPrompt);
				//   @ts-ignore
				wb.addEventListener('externalwaiting', showSkipWaitingPrompt);

				wb.register().then((r) => (registration = r));
			}
		})();
	}
</script>

<Prompt />
<div class="max-w-xlg min-h-screen mx-auto p-4 bg-gray-200 shadow-md">
	<Nav />
	<slot />
</div>
