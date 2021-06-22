<script>
	import { page } from '$app/stores';
	import store from '$store';
	const base_url = store.state.base_url;
</script>

<div class=" flex justify-end">
	{#if $page.path === '/info'}
		<a href={`${base_url}`} class="capitalize left active hover:text-indigo-400 text-md pr-3"
			>home</a
		>
	{:else if $page.path === '/'}
		<a href={`${base_url}info`} class="capitalize left active hover:text-indigo-400 text-md pr-3"
			>info</a
		>
	{/if}
</div>

<style lang="postcss">
	.active {
		@apply border-indigo-400 border-b-8 text-indigo-700;
	}
</style>
