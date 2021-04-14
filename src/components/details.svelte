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

<div class="pl-1 max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl">
	{#if $details && !$checking}
		<h3 class="capitalize tracking-wide text-lg text-center text-indigo-500 font-bold my-2">
			Info
		</h3>
		<div class="flex justify-between px-5 mb-2">
			{#each infos as [id, name, num] (id)}
				<button
					on:click={() => {
						info = name;
					}}
					class="capitalize hover:text-indigo-400"
					class:active={name === info}>{name}{num !== undefined ? `(${num})` : ''}</button
				>
			{/each}
		</div>

		<div class="">
			<div class="md:flex w-sm md:w-full md:min-w-md max-w-full">
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
		@apply border-indigo-400 text-semebold border-b-5 text-indigo-600;
	}
</style>
