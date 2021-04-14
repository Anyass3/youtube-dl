<script context="module">
	/**
	 * @type {import('@sveltejs/kit').Load}
	 */
	export async function load({ page, fetch, session, context }) {
		// const url= serverEndpoint+'/info'
		let res = {};

		try {
			res = await store.state.api('/info');

			if (res.statusText == 'OK') {
				return {
					props: {
						app_info: await res.data
					}
				};
			}
		} catch (error) {
			return {
				status: res.status,
				error: new Error(
					'Could not load server_endpoint/info. Server is probably down or not responding'
				)
			};
		}
	}
</script>

<script>
	import Details from '$components/details.svelte';

	import store from '$store';
	// router.mode.hash(); // enables hash navigation method
	import Form from '$components/form.svelte';
	store.dispatch('startSocket');

	export let app_info;
	store.dispatch('setApp_info', app_info).then((r) => console.log('app_info is set'));
	// console.log(store.state.api['CancelToken']());
</script>

<main class="">
	<h4 class="uppercase tracking-wide text-lg text-center text-indigo-500 font-semibold">
		Simple Youtube downloader
	</h4>
	<div>
		<div class="gap-1 flex flex-wrap md:flex-nowrap justify-around">
			<Form />
			<Details />
		</div>
	</div>
</main>

<!-- <Route path="/room/:roomId">
  <Room />
</Route> -->
<style>
	:global(iframe) {
		max-width: 100%;
	}
</style>
