
import logging
import os

import inspect
import typing
from starlette.types import Receive, Scope, Send
from starlette.background import BackgroundTask
from starlette.concurrency import iterate_in_threadpool, run_until_first_complete
from urllib.error import HTTPError
from pytube import request, extract
from urllib.parse import quote

from pytube import Stream as _Stream
from backend.socket import Socket

from functools import lru_cache
from backend import config
from typing import Optional


class YouTubeVideoFile:
    is_stream = False

    def __init__(self, filepath: str,
                 filename: str = None,
                 media_type: str = None,):
        self.filepath: str = filepath
        self.filename: str = filename+'.mp4'
        self.media_type: str = media_type


class YoutubeVideoStream:
    '''
    This is mimic the YouTube Video Stream Object
    '''
    is_stream = True

    def __init__(self, filename, media_type, url=None, size=None):
        self.filename: str = filename+'.mp4'
        self.media_type: str = media_type
        self.url: str = url
        self.filesize: int = size

    def __call__(self, *args, **kwargs):
        try:
            for chunk in request.stream(self.url):
                yield chunk
        except HTTPError as e:
            if e.code != 404:
                raise
            # Some adaptive streams need to be requested with sequence numbers
            for chunk in request.seq_stream(self.url):
                yield chunk

    @property
    def content_disposition(self) -> str:
        content_disposition_filename = quote(self.filename)
        if content_disposition_filename != self.filename:
            content_disposition = "attachment; filename*=utf-8''{}".format(
                content_disposition_filename
            )
        else:
            content_disposition = 'attachment; filename="{}"'.format(
                self.filename)
        return content_disposition

    @property
    def headers(self):
        return {'Content-Length': f'{self.filesize}',
                'Content-Disposition': self.content_disposition}


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
