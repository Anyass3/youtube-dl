import StoreX from 'stores-x';
import { api } from '$lib/connectionBuilder';
import { dev } from '$app/env';
import { timedelta, initPrompt, hash } from './utils';

export default StoreX([
	{
		noStore: ['api', 'app_info', 'tempDetails', 'base_url'],
		state: {
			api, // axios instance
			ws: null, // websocket instance
			formData: { 'media type': '' }, // {videoId,'media type',resolution}
			//
			media_types: [], // ['video','playlist']
			//
			url: dev
				? 'https://www.youtube.com/watch?v=gYJ03GyrSrM&list=PLXTOW_XMsIDQ3nkny1ErmqlpSUhcLaItg&index=1'
				: '', // string
			// @ts-ignore
			base_url: import.meta.env.BASE_URL.replace('_app/', ''),
			//
			isAvailable: false, // bool
			checking: false, // bool
			showDownlaoder: 'btn', // false|'btn'|'loader'
			//
			app_info: {}, // some info from server
			details: null, // video or playlist details object {}
			tempDetails: new Map(), // temp video or playlist details Map {}
			videosInfo: {}, // {videoId:{videoId,title,}}
			//
			prompt: initPrompt(), // prompt to used when new bundle of app is avialable (service workers)
			//
			pending: [], // [{ ...state.formData.get(), videoId, id: hash() },]
			tempPending: [], // [{ videoId, title },]
			downloading: [], // [{ videoId, id: hash() },]
			downloaded: [], // [{ videoId, id: hash(), cancel: CancelToken.source().cancel },]
			//
			error: undefined // string|undefined
		},
		mutations: {
			updatePromptValues(state, options = {}) {
				state.prompt.update((value) => {
					for (let option in options) {
						value[option] = options[option];
						return value;
					}
				});
			},
			onDownloadStart(state, { videoId, cancel }) {
				state.pending.update((videos) => {
					// console.log('videos', videos);
					return videos.filter((video) => video.videoId !== videoId);
				});

				state.downloading.update((videos) => {
					videos.push({ videoId, cancel, id: hash() });
					return videos;
				});
			},
			onDownloadEnd(state, videoId) {
				state.downloading.update((videos) => {
					return videos.filter((video) => video.videoId !== videoId);
				});

				state.downloaded.update((videos) => {
					videos.push({ videoId, id: hash() });
					return videos;
				});

				state.videosInfo.update((value) => {
					const { videoId, ...videosinfo } = value;
					return videosinfo;
				});
			},
			setContentLen(state, { videoId, content_len }) {
				state.videosInfo.update((value) => {
					// console.log('content-len', videoId, content_len);
					value[videoId]['content_len'] = content_len;
					return value;
				});
			},
			setProgress(state, videoId) {
				let video;
				return ({ loaded, total }) => {
					state.downloading.update((value) => {
						let index;
						video = value.find((video, idx) => {
							video.videoId === videoId;
							index = idx;
							return video;
						});
						if (video) {
							const percentage = (loaded / total) * 100;
							video['percentage'] = percentage;
							value[index][videoId] = video;
							// console.log(percentage, value);
						}
						return value;
					});
					return video;
				};
			},
			setMedia_types(state, { videoId, playlistId }) {
				const media_types =
					videoId && playlistId
						? ['video', 'playlist']
						: videoId
						? 'video'
						: playlistId
						? 'playlist'
						: [];
				state.media_types.set(media_types);
			},
			addToPending(state) {
				const videos: Array<any> = state.tempPending.get();
				state.pending.update((value) => {
					for (let videoId of videos) value.push({ ...state.formData.get(), videoId, id: hash() });
					return value;
				});
			},
			rmPending(state, videoId) {
				state.pending.update((videos) => {
					return videos.filter((video) => video.videoId !== videoId);
				});
			},
			setTempPending(state, videos: Array<any>) {
				const value = [];
				for (let { videoId } of videos) value.push(videoId);
				state.tempPending.set(value);
			},
			setVideoInfos(state, videos: Array<any>) {
				state.videosInfo.update((value) => {
					for (let { videoId, title } of videos) {
						// const id = hash();
						value[videoId] = { videoId, title };
					}
					return value;
				});
			}
		},
		actions: {
			async showPrompt({ commit }, options) {
				options = initPrompt({ ...options, visible: true });
				commit('setPrompt', options);
			},
			async hidePrompt({ commit }) {
				const options = initPrompt({ visible: false });
				commit('setPrompt', options);
			},
			async get_info({ dispatch }) {
				const resp = await api.get('/info');
				dispatch('setApp_info', resp.data);
			},
			async checkAvailability({ state, commit, dispatch, g }) {
				const url = state.url.get().trim();

				dispatch('setShowDownlaoder', 'btn');
				let title; // might be needed in addToPending below
				let id;

				const { playlistId, videoId } = await g('filteredUrl', url);
				if (playlistId || videoId) {
					if (videoId && playlistId) {
						commit('setMedia_types', { videoId, playlistId });
						id = state.formData.get()['media type'] === 'playlist' ? playlistId : videoId;
					} else {
						id = videoId || playlistId;
						commit('setMedia_types', { videoId, playlistId });
					}
					// console.log(id, videoId, playlistId);
					dispatch('setError');
					dispatch('setChecking', true);
					const temp = state.tempDetails.get(id);
					// console.log(state.tempDetails, temp);
					if (temp) {
						dispatch('setDetails', temp);
						title = temp.title;
						// dispatch('setIsAvailable', true);
					} else {
						const resp = await dispatch('fetchMediaDetails', id);
						if (state.isAvailable.get()) {
							dispatch('setDetails', resp);
							// dispatch('setIsAvailable', true);
							state.tempDetails.set(id, resp);
							title = resp.title;
						}
						// else dispatch('setIsAvailable', false);
					}
					if (id.length > 11) {
						const url = '/playlist_items/' + playlistId;
						const tempVideos = state.tempDetails.get(url);
						if (tempVideos) {
							commit('setVideoInfos', tempVideos);
							commit('setTempPending', tempVideos);
						} else {
							const resp = await api.get(url);
							if (resp.ok) {
								state.tempDetails.set(url, resp.data);
								commit('setVideoInfos', resp.data);
								commit('setTempPending', resp.data);
							} else {
								dispatch('setChecking', false);
								dispatch('setError', "Sorry can't get playlist_urls. Try again later!");
							}
						}
					} else {
						commit('setVideoInfos', [{ videoId, title }]);
						commit('setTempPending', [{ videoId, title }]);
					}
				} else {
					// dispatch('setIsAvailable', false);
					dispatch('setError', 'Invalid videoId or playlistId or URL');
				}
				dispatch('setChecking', false);
			},
			async listeners({ state }) {
				window.addEventListener('beforeunload', (event) => {
					if (state.pending.get().length > 0 || state.downloading.get().length > 0)
						event.returnValue = true;
					// console.log(event);
				});
				// window.addEventListener('close', (event) => {
				// 		event.returnValue = true;
				// 	// console.log(event);
				// });
			},
			downloadIterator({ g, dispatch }) {
				let iterationCount = 0;
				const Iterator = {
					next: function () {
						const generator = g('genPending').next();
						const done = generator?.done;
						const video = generator?.value;
						// window['gn'] = generator;
						if (!done && video.videoId) {
							dispatch('download', video);
							iterationCount++;
							// console.log('starting download of =>', videoId);
						}
						return { value: video, done, total: iterationCount };
					}
				};
				return Iterator;
			},
			async rmCancelled({ state, dispatch }, videoId) {
				state.downloading.update((videos) => {
					return videos.filter((video) => video.videoId !== videoId);
				});
				state.showDownlaoder.set('btn');
				const downloadIterator = await dispatch('downloadIterator');
				downloadIterator.next();
				console.log('download_error', 'download cancelled by user');
			},

			async postForm({ state, commit, g, dispatch }) {
				commit('addToPending');
				if (state.downloading.get().length === 0) {
					dispatch('setShowDownlaoder', 'loader');
					const downloadIterator = await dispatch('downloadIterator');
					downloadIterator.next();
				} else dispatch('setShowDownlaoder', false);
			},
			async download({ state, commit, dispatch }, { videoId = '', resolution = '360p' } = {}) {
				const cancelToken = api['CancelToken']();

				//start download
				dispatch('setShowDownlaoder', false);
				commit('onDownloadStart', { videoId, cancel: cancelToken.cancel });
				console.log('starting', { videoId, cancel: cancelToken.cancel });
				const url = `/download/${videoId}?resolution=${resolution}`;
				const blob_resp = await api.get(url, {
					responseType: 'blob',
					onDownloadProgress: commit('setProgress', videoId),
					cancelToken: cancelToken.token
				});

				const blob = blob_resp.data;
				console.log('blob', blob, state.videosInfo.get(), blob_resp);

				const link = document.createElement('a');
				link.href = window.URL.createObjectURL(new Blob([blob], { type: blob.type }));

				const fileName = `${state.videosInfo.get()?.[videoId]?.title || videoId}-${resolution}.mp4`;
				link.download = fileName;
				// link.target = '_blank';
				// console.log(link.href);
				document.body.appendChild(link);
				link.click();
				link.remove();
				commit('onDownloadEnd', videoId);
				const downloadIterator = await dispatch('downloadIterator');
				downloadIterator.next();
				console.log('downloaded', videoId);
			},
			async fetchMediaDetails({ dispatch }, id) {
				// this will fetch a youtube playlist or video detials
				// this could be done in js directly but it might exposed api_key
				const url = '/detials/' + id;
				let attrs = [];
				if (id.length > 11)
					// if it is greater than 11 it is playlist
					attrs = ['title', 'channelId', 'channelTitle', 'description', 'publishedAt'];
				else attrs = ['channelTitle', 'title', 'channelId', 'publishedAt', 'description'];
				const resp = (await api.get(url))?.data?.items?.[0];
				// console.log(resp);
				if (resp) {
					const data: any = {
						player: resp.player.embedHtml
							.replace(/src="http[^s]/, 'src="https:')
							.replace(/src='http[^s]/, "src='https:")
					};
					data['aspectRatio'] =
						parseInt(data.player.match(/width=["'](?<width>[0-9]+)["']/).groups.width) /
						parseInt(data.player.match(/height=["'](?<height>[0-9]+)["']/).groups.height);

					for (let i of attrs) data[i] = resp?.snippet[i];

					data['published'] = timedelta(data['publishedAt']);
					const { publishedAt, ...toShow } = data;

					dispatch('setIsAvailable', !!resp);
					// console.log('resp.player', data.player);
					return toShow;
				} else dispatch('setError', 'fetch error or Invalid videoId or playlistId or URL');
			}
		},
		getters: {
			async filteredUrl(_, url) {
				const playlistId = (
					url.match(/(?:list=(?<id>[\w-]{34}))/) || url.match(/(?<id>^PL[\w-]{32}$)/)
				)?.groups?.id;
				const videoId = (url.match(/(?:v=|\/)(?<id>[\w-]{11})/) || url.match(/(?<id>^[\w-]{11}$)/))
					?.groups?.id;
				return { playlistId, videoId };
			},
			genPending: function* (state) {
				yield* state.pending.get();
			}
		}
	}
]);
