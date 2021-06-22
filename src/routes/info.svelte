<script context="module">
	import { browser, dev } from '$app/env';

	// we don't need any JS on this page, though we'll load
	// it in dev so that we get hot module replacement...
	export const hydrate = dev;

	// ...but if the client-side router is already loaded
	// (i.e. we came here from elsewhere in the app), use it
	export const router = browser;

	// since there's no dynamic data here, we can prerender
	// it so that it gets served as a static asset in prod
	export const prerender = true;
</script>

<div class="px-50 flex flex-col gap-7 text-3xl">
	<p class="text-7xl font-semibold my-10 text-indigo-600">Welcome to the info page</p>
	<p class="leading-tight">
		For the download to start faster use 360p or 720p. For the others it will have to download the
		video and the audio seperately and later merge it before you will see the download.
	</p>
	<p>
		But that is not a big problem on the server because the network is pretty fast there, you
		wouldn't even notice
	</p>
	<p>
		check out the
		<a class="text-blue-500 underline" href="https://github.com/Anyass3/youtube-dl"
			>source code
		</a>on my github
	</p>
</div>
