import axios from 'axios';
import { v4 } from 'uuid';
import { browser } from '$app/env';

//@ts-ignore
const VITE_SERVER_ENDPOINT: string = import.meta.env.VITE_SERVER_ENDPOINT;

export const getSocketId = () => {
	if (!browser) return;
	let id = window.localStorage.getItem('youtube_downloader_uuid');
	if (!id) {
		id = v4();
		window.localStorage.setItem('youtube_downloader_uuid', id);
	}
	return id;
};

export const axiosFetch = async (instance, path: string, ...args) => {
	try {
		const res = await instance(path, ...args);
		return { status: res?.status, ok: true, headers: res?.headers, data: res?.data };
	} catch (error) {
		return {
			status: error.response?.status,
			ok: false,
			headers: error.response?.headers,
			data: error.response?.data
		};
	}
};

export const axiosInstance = axios.create({
	baseURL: VITE_SERVER_ENDPOINT
});
export const api = {
	get: (path: string, ...args) => axiosFetch(axiosInstance.get, path, ...args),
	post: (path: string, ...args) => axiosFetch(axiosInstance.post, path, ...args)
};
if (browser) window['api'] = api;

// this can be used to cancel a download
api['CancelToken'] = () => axios.CancelToken.source();
