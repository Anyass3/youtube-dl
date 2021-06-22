
import logging
import os

import inspect
import typing
from fastapi.responses import StreamingResponse as _StreamingResponse
from starlette.types import Receive, Scope, Send
from starlette.background import BackgroundTask
from starlette.concurrency import iterate_in_threadpool, run_until_first_complete
from urllib.error import HTTPError
from pytube import request, extract

from pytube import YouTube as _YouTube
from pytube import Stream as _Stream
from backend.socket import Socket

from functools import lru_cache
from backend import config
from typing import Optional


logger = logging.getLogger(__name__)


class StreamingResponse(_StreamingResponse):

    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
        socket_id: str = None,
        content_len: int = None,
        video_id: str = None,
        filename: str = None,
        filepath: str = None

    ) -> None:
        if inspect.isasyncgen(content):
            self.body_iterator = content
        else:
            self.body_iterator = iterate_in_threadpool(content)
        self.status_code = status_code
        self.media_type = self.media_type if media_type is None else media_type
        self.background = background
        self.init_headers(headers)
        self.video_id = video_id
        self.filepath = filepath
        self.content_len = content_len
        self.socket = Socket
        self.socket_id = socket_id

    async def listen_for_disconnect(self, receive: Receive) -> None:
        while True:
            message = await receive()
            print('\nlisten_for_disconnect', message, '\n')
            if message["type"] == "http.disconnect":
                # [os.remove(path)
                #  for path in self.socket.downloads if os.path.exists(path)]
                if self.filepath and os.path.exists(self.filepath):
                    os.remove(self.filepath)
                break

    async def on_content_len(self):
        await self.socket(self.socket_id).emit('content_len', {
            'videoId': self.video_id, 'content_len': self.content_len})

    async def stream_response(self, send: Send) -> None:
        bytes_loaded = 0
        await self.on_content_len()
        await self.socket(self.socket_id).on('content_len', self.on_content_len)
        # print('self.content_len', self.content_len)
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )
        async for chunk in self.body_iterator:
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)

            await send({"type": "http.response.body", "body": chunk, "more_body": True})

            bytes_loaded += len(chunk)

            # await self.socket(self.socket_id).emit(
            #     'progress', {'videoId': self.video_id, 'size': bytes_loaded})

        await send({"type": "http.response.body", "body": b"", "more_body": False})
        # await self.socket(self.socket_id).emit(
        #     'downloaded', {'videoId': self.video_id})
        if self.filepath and os.path.exists(self.filepath):
            os.remove(self.filepath)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        print('\nin __call__\n')
        await run_until_first_complete(
            (self.stream_response, {"send": send}),
            (self.listen_for_disconnect, {"receive": receive}),
        )

        if self.background is not None:
            await self.background()


class Stream(_Stream):
    path = None

    def signal_stream(
        self,
        output_path: Optional[str] = None,
        filename: Optional[str] = None,
        video_id: Optional[str] = None,
    ) -> str:

        bytes_remaining = self.filesize
        logger.debug(
            "downloading (%s total bytes) file to %s",
            self.filesize,
        )
        bytes_loaded = 0

        try:
            for chunk in request.stream(self.url):
                # reduce the (bytes) remainder by the length of the chunk.
                bytes_loaded += len(chunk)
                # send to the on_progress callback.

                if self._monostate.on_progress:
                    self._monostate.on_progress(
                        self, video_id, chunk, bytes_loaded, self.filesize)
        except HTTPError as e:
            if e.code != 404:
                raise
            # Some adaptive streams need to be requested with sequence numbers
            for chunk in request.seq_stream(self.url):
                # reduce the (bytes) remainder by the length of the chunk.
                bytes_loaded += len(chunk)
                # send to the on_progress callback.

                if self._monostate.on_progress:
                    self._monostate.on_progress(
                        self, video_id, chunk, bytes_loaded, self.filesize)
        on_complete = self._monostate.on_complete
        if on_complete:
            logger.debug("calling on_complete callback %s", on_complete)
            on_complete(self, self.filesize)
        return video_id

    async def start_streaming(self, video_id: Optional[str] = None) -> str:
        # print('socket_id=self.socket_id', self.socket_id)
        try:
            for chunk in request.stream(self.url):

                # print('w chuck', len(chunk))
                # socket.emit('on_progress', {'videoId': video_id, 'size': len(
                #     chunk), 'total': self.filesize})
                yield chunk
        except HTTPError as e:
            if e.code != 404:
                raise
            # Some adaptive streams need to be requested with sequence numbers
            for chunk in request.seq_stream(self.url):
                # socket.emit('on_complete', {'videoId': video_id, 'size': len(
                #     chunk), 'total': self.filesize})
                yield chunk


class YouTube(_YouTube):
    # socket_id = 'hello'
    @property
    def fmt_streams(self):
        """Returns a list of streams if they have been initialized.

        If the streams have not been initialized, finds all relevant
        streams and initializes them.
        """
        self.check_availability()
        if self._fmt_streams:
            return self._fmt_streams

        self._fmt_streams = []
        # https://github.com/pytube/pytube/issues/165
        stream_maps = ["url_encoded_fmt_stream_map"]
        if "adaptive_fmts" in self.player_config_args:
            stream_maps.append("adaptive_fmts")

        # unscramble the progressive and adaptive stream manifests.
        for fmt in stream_maps:
            if not self.age_restricted and fmt in self.vid_info:
                extract.apply_descrambler(self.vid_info, fmt)
            extract.apply_descrambler(self.player_config_args, fmt)

            extract.apply_signature(self.player_config_args, fmt, self.js)

            # build instances of :class:`Stream <Stream>`
            # Initialize stream objects
            stream_manifest = self.player_config_args[fmt]
            for stream in stream_manifest:
                video = Stream(
                    stream=stream,
                    player_config_args=self.player_config_args,
                    monostate=self.stream_monostate,
                )
                self._fmt_streams.append(video)

        self.stream_monostate.title = self.title
        self.stream_monostate.duration = self.length

        return self._fmt_streams


@ lru_cache()
def Settings():
    return config.Settings()


# def clean_filter(_dict, expected: list, deep=False):
#     new_dict = {i: _dict[i] for i in _dict if i in expected}
#     if not deep:
#         return new_dict
#     return {i: new_dict[i] for i in new_dict if new_dict[i]}


# class Get():
#     def get(self, *args, **kwargs): pass


# async def getMetaProps(html, props=[]):
#     return {prop: (html.find('meta', attrs={'property': f'og:{prop}'}) or Get()).get('content') for prop in props}


# async def getPlaylistVideos(urls):
#     responses = (BeautifulSoup(requests.get(url).text) for url in urls)
#     return [{'title': html.title.text, 'url': html.find('meta', attrs={'property': f'og:url'}).get('content')} for html in responses]
