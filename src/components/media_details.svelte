<script>
	import store from '$store';
	const details = store.state.details;
	import { onMount } from 'svelte';
	import { browser } from '$app/env';
	const setHeight = () => {
		// respect aspectRatio
		if (browser) {
			const ifm = document.querySelector('iframe');
			ifm.height = `${ifm.clientWidth / $details.aspectRatio}`;
		}
	};
	onMount(() => setHeight());
</script>

<svelte:window on:resize={setHeight} />

<div class="bg-center w-full">
	<div class="flex justify-center ">
		<div class="border-indigo-500 rounded-lg p-1 border bg-indigo-100">
			{@html $details?.player}
		</div>
	</div>
	<div class="px-2 py-8">
		<div class="tracking-wide text-sm font-semibold">
			{#each Object.keys($details) as item}
				{#if item !== 'player' && item !== 'aspectRatio'}
					<p>
						{item}: <span class="text-gray-600">{$details?.[item]}</span>
					</p>
				{/if}
			{/each}
		</div>
	</div>
</div>
