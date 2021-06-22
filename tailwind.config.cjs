module.exports = {
	mode: 'jit',
	purge: [
		'./src/**/*.{html,js,svelte,ts}',
		'./src/**/**/*.{js,ts,svelte}',
		'./src/**/**/**/*.{js,ts,svelte}'
	],
	theme: {
		extend: {}
	},
	plugins: []
};
