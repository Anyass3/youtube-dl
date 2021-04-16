## Get started

This is youtube video/playlist downloader

### made with

> backend: python fast-api
> frontend: svelte-kit

#### to play with it you will need a YOUTUBE_API_KEY

clone repo and
Install the dependencies...

```bash
cd youtube-dl
npm install
```

create python virtual environment and install requiremennts

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

run backend

```
API_KEY=YOUR_YOUTUBE_API_KEY uvicorn backend:app --reload
```

start frontend

```bash
npm run dev
```

Navigate to [localhost:3000](http://localhost:3000). You should see your app running.

## backend requirement

ffmpeg is needed when downloading resolutions other than 360p or 720p

because the video and audio have to be first downloaded seperately and later merge together using ffmpeg

## Building and running in production mode

- frontend

you might want to create a /.env file in root of this project

In it write

> VITE_SERVER_ENPOINT=http(s)://your_server_endpoint

To create an optimised version of the app:

```bash
npm run build
```

You can run the newly built app with `npm start`.

- backend

you might want to a .env file in /backend/

In it write

> API_KEY=your_youtube_api_key

you can use gunicorn as a manager for uvicorn

```bash
source env/bin/activate
pip install gunicorn
```

now run backend with gunicorn

```bash
gunicorn backend:app -w 4 -k uvicorn.workers.UvicornWorker
```

# features

- frontend works offline after first load thanks to svelte-kit service-worker feature and [workbox](https://developers.google.com/web/tools/workbox/)
- frontend is installable
- auto-updatable after every build thanks to my custom-config-plugin in [svelte.config.cjs](https://github.com/Anyass3/youtube-dl/blob/main/svelte.config.cjs#L37)
- downloads a youtube video
- downloads a youtube playlist

preview

![preview](https://github.com/Anyass3/youtube-dl/blob/main/screenshot.png)

# youtube-dl
