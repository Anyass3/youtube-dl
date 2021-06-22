import preprocess from 'svelte-preprocess';
import { resolve } from 'path';
import adapterStatic from '@sveltejs/adapter-static';
import sw from 'kit-sw-workbox';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://github.com/sveltejs/svelte-preprocess
	// for more information about preprocessors
	preprocess: [
		preprocess({
			postcss: true
		})
	],

	kit: {
		// By default, `npm run build` will create a standard Node app.
		// You can create optimized builds for different platforms by
		// specifying a different adapter
		adapter: adapterStatic(),

		// hydrate the <div id="svelte"> element in src/app.html
		target: '#svelte',
		ssr: false,
		// amp: true,

		vite: {
			plugins: [sw({ routes: ['/', '/info'] })],
			resolve: {
				alias: {
					$store: resolve('src/store'),
					$components: resolve('src/components')
				}
			},
			server: {
				proxy: {
					'/_api': {
						target: 'http://127.0.0.1:8000',
						changeOrigin: true,
						rewrite: (path) => path.replace(/^\/_api/, '')
					}
				}
			}
		}
	}
};

export default config;
