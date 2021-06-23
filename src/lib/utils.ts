/* eslint-disable no-extra-boolean-cast */
export const debounce = (fn: CallableFunction, delay = 500) => {
	let timeout;
	return (...args) => {
		if (!!timeout) clearTimeout(timeout);
		timeout = setTimeout(() => {
			fn(...args);
		}, delay);
	};
};

export const getHash = () => {
	return Math.floor(2147483648 * Math.random()).toString(36);
};
