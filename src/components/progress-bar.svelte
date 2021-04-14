<script>
	import { BarLoader } from 'svelte-loading-spinners';
	import store from '$store';
	const downloading = store.state.downloading;
	const videosInfo = store.state.videosInfo;

	// $: console.log('downloading', $downloading);
	// $: console.log('videosInfo', $videosInfo);
</script>

{#each $downloading as { videoId, cancel, percentage, id } (id)}
	<div class="relative p-1 border-2 border-indigo-300 rounded-lg mt-3">
		<div class="flex mb-2 items-center justify-between">
			<div>
				<span
					class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-indigo-600 bg-indigo-100"
				>
					{$videosInfo[videoId].title}
				</span>
			</div>
			<div class="text-right">
				<span class="text-xs font-semibold inline-block text-indigo-600">
					{percentage?.toFixed?.(1)}%
				</span>
			</div>
		</div>
		{#if percentage}
			<div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-indigo-100">
				<div
					style="width:{percentage}%"
					class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500"
				/>
			</div>
		{:else}
			<div id="loader"><BarLoader color="#6366f1" size="100" /><span>starting download</span></div>
		{/if}
		<button
			on:click={() => {
				cancel();
				store.commit('rmCancelled', videoId);
			}}
			class="text-red-600 bg-red-200 p-1 rounded-lg active:ring focus:outline-none active:outline-none ring-red-400"
			>cancel</button
		>
	</div>
{/each}

<style>
	:global(div#loader > div) {
		width: 100% !important;
	}
</style>
