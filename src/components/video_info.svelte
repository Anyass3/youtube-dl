<script>
	import store from '$store';
	export let info;
	const info_value = store.state[info];
	const videosInfo = store.state.videosInfo;
	// $: console.log('videosInfo', $videosInfo);
</script>

{#if $info_value.length === 0}
	<div class="relative p-1 bg-indigo-200 rounded-sm mt-3 w-full">
		No video {info}
	</div>
{:else}
	<div class="w-full mt-3">
		{#each $info_value as { videoId, id } (id)}
			<div class="relative p-1 my-1 bg-indigo-100 rounded-sm">
				<div class="flex justify-between">
					<span
						class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-indigo-500"
					>
						{$videosInfo[videoId]?.title || videoId}
					</span>
					{#if info === 'pending'}
						<button
							class="text-red-600 font-bold text-2xl p-1 bg-red-200 rounded-md"
							on:click={() => store.commit('rmPending', videoId)}>x</button
						>
					{/if}
				</div>
			</div>
		{/each}
	</div>
{/if}
