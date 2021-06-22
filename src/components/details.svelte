<script>
	import store from '$store';
	const details = store.state.details;
	const checking = store.state.checking;
	import { SyncLoader } from 'svelte-loading-spinners';
	import MediaDetails from '$components/media_details.svelte';
	import VideoInfo from '$components/video_info.svelte';
	const downloading = store.state.downloading;
	const formData = store.state.formData;
	const downloaded = store.state.downloaded;
	const pending = store.state.pending;

	let media_type = 'video';

	$: media_type = $formData['media type'] || 'video';

	let info = media_type;
	// $: console.log('pe', info, media_type);
	// $: console.log('pending', $pending);
	// $: console.log('downloading', $downloading);
	$: infos = [
		[1, media_type],
		[2, 'pending', $pending.length],
		[3, 'downloaded', $downloaded.length]
	];
</script>

<div class="pl-1 mx-auto bg-white rounded-xl shadow-md overflow-hidden fluid" style="width:500px">
	{#if $details && !$checking}
		<h3 class="capitalize tracking-wide text-lg text-center text-indigo-500 font-bold my-2">
			details
		</h3>
		<div class="flex justify-between px-1 md:px-5 border-b border-indigo-300">
			{#each infos as [id, name, num] (id)}
				<div>
					<button
						on:click={() => {
							info = name;
						}}
						class="capitalize hover:text-indigo-400 focus:outline-none"
						class:active={name === info}>{name}{num !== undefined ? `(${num})` : ''}</button
					>
				</div>
			{/each}
		</div>

		<div class="">
			<div class="md:flex p-2">
				<div class:hidden={info !== 'playlist' && info !== 'video'}>
					<!-- we do want MediaDetails to rerender everytime -->
					<MediaDetails />
				</div>

				{#if info !== 'playlist' && info !== 'video'}
					{#key info}
						<VideoInfo {info} />
					{/key}
				{/if}
			</div>
		</div>
	{:else if $checking === 'true'}
		<SyncLoader />
	{:else}
		<div class="capitalize p-3 text-indigo-700 font-simibold">
			Nothing to see here yet. try inputing some youtube video or playlist link or id
		</div>
	{/if}
</div>

<style lang="postcss">
	.active {
		@apply font-semibold text-indigo-700;
	}
</style>
