<script>
	import store from '$store';
	const formData = store.state.formData;
	export let name;
	export let options = [];
	// $: console.log($formData);
</script>

<div class="my-4">
	<label class="capitalize text-indigo-900" for="#{name}">{name}</label>

	<select
		id={name}
		bind:value={$formData[name]}
		class="w-full border bg-gray-200 focus:bg-gray-100 rounded px-3 py-2 outline-none"
	>
		{#each options as option}
			<option class="py-1" value={option?.value || option}>{option?.key || option}</option>
		{/each}
	</select>
</div>
