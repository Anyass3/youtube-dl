<script>
	import Details from '$components/details.svelte';
	import Form from '$components/form.svelte';
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
