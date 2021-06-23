<script>
	import { fade } from 'svelte/transition';
	import store from '$store';
	import { debounce } from '$lib/utils';
	import Select from '$components/select.svelte';
	import ProgressBar from '$components/progress-bar.svelte';
	import { SyncLoader } from 'svelte-loading-spinners';

	const isAvailable = store.state.isAvailable; //bool

	const checking = store.state.checking; // bool
	const downloading = store.state.downloading; // bool
	const url = store.state.url;
	const showDownlaoder = store.state.showDownlaoder; // false,btn,loader

	const error = store.state.error; // string
	const media_types = store.state.media_types; //[?video,?playlist]
	const formData = store.state.formData; //[?video,?playlist]

	let startedTyping = false;
	// $: console.log($media_types);
	$: media_type = $formData['media type'];
	function check(..._) {
		const _url = $url.trim();
		if (startedTyping) {
			if (!_url) {
				store.dispatch('setError', "input shouldn't be empty");
			} else {
				debounce(() => store.dispatch('checkAvailability'))();
			}
		}
	}
	$: check(media_type, $url); // this so that 'check' can run everytime media_type changes
</script>

<div
	class="max-w-md md:min-w-sm mx-auto bg-white p-3 mb-1 rounded-xl shadow-md overflow-hidden md:max-w-2xl"
>
	<label class="capitalize text-indigo-600 text-lg" for="#video">Video|Playlist url|id</label>
	<input
		bind:value={$url}
		on:input|once={() => (startedTyping = true)}
		placeholder="url,id,playlist-id"
		class="w-full border p-2 border-indigo-500 rounded-md focus:border-indigo-700"
	/>
	{#if $checking}
		<SyncLoader size="60" color="#FF3E00" unit="px" duration="1s" />
	{:else if $error}
		<p in:fade out:fade class="bg-red-300 text-red-800">{$error}</p>
	{:else if $isAvailable}
		<div in:fade out:fade class="">
			{#if $media_types.length === 2}
				<Select name="media type" options={$media_types} />
			{/if}
			<Select name="resolution" options={['1080p', '720p', '480p', '360p', '144p']} />
		</div>
		<!-- <div in:fade out:fade class="my-2">
        <input
          class="p-2 border-indigo-300 checked:border-indigo-700"
          id="save-server"
          type="checkbox"
        />
        <label class="capitalize text-indigo-900" for="save-server">save in server</label>
      </div> -->
		{#if $showDownlaoder === 'btn'}
			<input
				in:fade
				out:fade
				type="submit"
				on:click={() => store.dispatch('postForm')}
				value={$downloading.length === 0 ? 'Download' : 'Add to Pending'}
				class="border-2 p-1 font-semibold rounded-md text-indigo-500 border-indigo-500 hover:border-gray-500"
			/>
		{:else if $showDownlaoder === 'loader'}
			<SyncLoader size="60" color="#FF3E00" unit="px" duration="1s" />
		{/if}
	{:else}
		<input
			in:fade
			out:fade
			on:click={() => {
				if (!startedTyping) startedTyping = true;
				check();
			}}
			type="submit"
			value="check"
			class="border-2 p-1 mt-2 font-semibold rounded-md text-indigo-500 border-indigo-500 hover:border-gray-500"
		/>
	{/if}
	<ProgressBar />
</div>

<style>
	p {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell,
			'Open Sans', 'Helvetica Neue', sans-serif;
	}
</style>
