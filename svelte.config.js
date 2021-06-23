import preprocess from 'svelte-preprocess';
import { resolve } from 'path';
import adapterStatic from '@sveltejs/adapter-static';
import sw from 'kit-sw-workbox';
import fs from 'fs';

let VITE_SERVER_ENDPOINT;
if (fs.existsSync('.env')) {
	const env = fs.readFileSync('.env', 'utf-8');
	const envDict = env.split('\n').reduce((dict, e) => {
		const [key, value] = e.trim().split('=');
		return { ...dict, [key]: value.replace(/['"]/g, '') };
	}, {});
	VITE_SERVER_ENDPOINT = envDict.VITE_SERVER_ENDPOINT || 'http://127.0.0.1:8000';
	console.log(VITE_SERVER_ENDPOINT);
}

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
						target: VITE_SERVER_ENDPOINT,
						changeOrigin: true,
						rewrite: (path) => path.replace(/^\/_api/, '')
					}
				}
			}
		}
	}
};

export default config;
