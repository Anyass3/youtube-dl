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
