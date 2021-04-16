const sveltePreprocess = require('svelte-preprocess');
const { resolve } = require('path');
const staticAdapter = require('@sveltejs/adapter-static');
const pkg = require('./package.json');
const { default: WindiCSS } = require('vite-plugin-windicss');
const svelteWindiCssPreprocess = require('svelte-windicss-preprocess');

const { axios: _, ...noExternalDeps } = pkg.dependencies;

/** @type {import('@sveltejs/kit').Config} */
module.exports = {
	// Consult https://github.com/sveltejs/svelte-preprocess
	// for more information about preprocessors
	preprocess: [
		svelteWindiCssPreprocess.preprocess({
			// config: 'tailwind.config.js', // windi config file path (optional)
			compile: false, // false: interpretation mode; true: compilation mode
			prefix: 'windi-', // set compilation mode style prefix
			globalPreflight: true, // set preflight style is global or scoped
			globalUtility: true // set utility style is global or scoped
		}),
		sveltePreprocess()
	],
	kit: {
		// By default, `npm run build` will create a standard Node app.
		// You can create optimized builds for different platforms by
		// specifying a different adapter
		adapter: staticAdapter(),

		// hydrate the <div id="svelte"> element in src/app.html
		target: '#svelte',
		ssr: false,

		vite: {
			plugins: [
				WindiCSS(),
				{
					name: 'custom-config-plugin',
					enforce: 'post',

					//  we want to transform the $service-worker which is imported by our service-worker file
					// this so we can customize it to include hashes so it can work well with workbox-precaching
					// which will make our service-worker auto updatable
					transform(code, id) {
						if (id.endsWith('.svelte/build/runtime/service-worker.js')) {
							// to generate randon string hash
							const hash = () => Math.floor(2147483648 * Math.random()).toString(36);

							// this site should work 100% offline after first load

							// add index.html in order for it to be cached too
							code = code.replace(/files[\ ]*\=[\ ]*\[/, `files = [\n"/",`);

							// construct regular expressons
							const reBuild = /export[\ ]*const[\ ]*build[\ ]*\=[\ ]*(?<code>\[[^\[\]]*\])/;
							const reFiles = /export[\ ]*const[\ ]*files[\ ]*\=[\ ]*(?<code>\[[^\[\]]*\])/;

							// extract build files
							// const build = JSON.parse(code.match(reBuild)?.groups?.code || []);
							const build = JSON.parse(code.match(reBuild).groups.code);
							// extract static files/assets
							//const files = JSON.parse(code.match(reFiles)?.groups?.code || []);
							const files = JSON.parse(code.match(reFiles).groups.code);

							code = code.replace(
								reBuild,
								'export const build = ' +
									JSON.stringify(
										build.reduce((obj, file) => [...obj, { url: file, revision: hash() }], [])
									)
							);

							code = code.replace(
								reFiles,
								'export const files = ' +
									JSON.stringify(
										files.reduce((obj, file) => [...obj, { url: file, revision: hash() }], [])
									)
							);
							return { code };
						}
					}
				}
			],

			resolve: {
				alias: {
					$store: resolve('src/store'),
					$components: resolve('src/components')
				}
			},
			ssr: {
				noExternal: Object.keys(noExternalDeps || {}),
				external: ['axios']
			}
		}
	}
};
