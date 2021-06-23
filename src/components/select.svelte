<script>
	import store from '$store';
	import { createEventDispatcher } from 'svelte';
	const formData = store.state.formData;
	export let name;
	export let options = [];
	const dispatch = createEventDispatcher();
	// $: console.log($formData);
	const sendEvent = (detail) => {
		console.log('sendEvent', $formData);
		dispatch('change', { detail });
	};
</script>

<div class="my-4">
	<label class="capitalize text-indigo-900" for="#{name}">{name}</label>

	<!-- svelte-ignore a11y-no-onchange -->
	<select
		id={name}
		bind:value={$formData[name]}
		on:change={() => sendEvent($formData[name])}
		class="w-full border bg-gray-200 focus:bg-gray-100 rounded px-3 py-2 outline-none"
	>
		{#each options as option}
			<option class="py-1" value={option?.value || option}>{option?.key || option}</option>
		{/each}
	</select>
</div>
