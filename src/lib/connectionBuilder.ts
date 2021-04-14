import axios from 'axios';
import { v4 } from 'uuid';
import { browser } from '$app/env';

// @ts-ignore
const VITE_SERVER_ENDPOINT: string = import.meta.env.VITE_SERVER_ENPOINT;

// @ts-ignore
const VITE_WEBSOCKET_ENDPOINT: string = import.meta.env.VITE_WEBSOCKET_ENDPOINT;

export const serverEndpoint = VITE_SERVER_ENDPOINT || 'http://127.0.0.1:8000';

export const getSocketId = () => {
	if (!browser) return;
	let id = window.localStorage.getItem('youtube_downloader_uuid');
	if (!id) {
		id = v4();
		window.localStorage.setItem('youtube_downloader_uuid', id);
	}
	return id;
};

// @ts-ignore
const match = serverEndpoint.match(/(^http(?<ssl>s)?\:\/\/)?(?<path>.+)/);
const ssl = browser ? window.location.protocol.includes('s') : null;
const path = match.groups.path;
export const getWebsoket = () => {
	let ws_endpoint = VITE_WEBSOCKET_ENDPOINT;
	if (!ws_endpoint) {
		if (ssl) ws_endpoint = `wss://${path}/ws`;
		else ws_endpoint = `ws://${path}/ws`;
	}
	return new WebSocket(ws_endpoint);
};
// console.log(serverEndpoint, VITE_SERVER_ENDPOINT, VITE_WEBSOCKET_ENDPOINT);
export const api = axios.create({
	// @ts-ignore
	baseURL: serverEndpoint
});

// this can be used to cancel a download
api['CancelToken'] = () => axios.CancelToken.source();
