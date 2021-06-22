<script context="module">
	export function load({ error, status }) {
		return {
			props: {
				error,
				status
			}
		};
	}
</script>

<script>
	export let status;
	export let error;
	const refreshPage = () => {
		window.location.reload();
	};
</script>

<div class="bg-red-200 flex justify-center flex-wrap items-center h-screen font-light">
	<div>
		<p class="text-red-900 text-9xl">Whoops!!!</p>
		<p class="text-red-900 text-5xl">Error Code: {status}</p>
		<p class="text-red-700 text-3xl">{error?.message}</p>
	</div>
	<button
		on:click={refreshPage}
		class="border-2 p-1 font-semibold shadow-lg rounded-md text-red-500 border-red-500 hover:bg-red-100 hover:border-red-400 hover:shadow-sm"
		>refresh page</button
	>
</div>
