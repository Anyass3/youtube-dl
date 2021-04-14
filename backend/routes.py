from fastapi.responses import FileResponse
import time
import httpx
import json
from pydantic import BaseModel
from typing import Optional, Dict
from fastapi import FastAPI, Path, Query, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from fastapi import APIRouter, Depends, HTTPException
from backend.download import YouTube, load_video
from backend.store import store
from backend.socket import Socket
from urllib.parse import quote
from backend.utils import *
from backend import config

from pytube import Playlist
router = APIRouter()


@router.get('/info')
async def get_info():
    settings = Settings()
    return {
        "app_name": settings.app_name
    }


@router.get('/detials/{id}')
async def video_detials(id: str):
    settings = Settings()
    if(len(id) == 11):
        url = f'https://youtube.googleapis.com/youtube/v3/videos?part=player&part=snippet&id={id}&key={settings.api_key}'
    else:
        url = f'https://youtube.googleapis.com/youtube/v3/playlists?part=snippet&part=player&id={id}&key={settings.api_key}'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return json.loads(resp.content)


@router.get('/playlist_items/{playlist_id}')
async def playlist_items(playlist_id: str):
    items = []
    settings = Settings()
    url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={settings.api_key}'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp = json.loads(resp.content)
        # import pdb
        # pdb.set_trace()
        items += resp['items']
        while True:
            try:
                _url = f"{url}&pageToken={resp['nextPageToken']}"
            except Exception as e:
                assert (e)
                break
            else:
                resp = await client.get(_url)
                resp = json.loads(resp.content)
                items += resp['items']
        items = [{'videoId': i['snippet']['resourceId']['videoId'], 'title': i['snippet']['title']}
                 for i in items]
        return items


@router.post("/connect_socket_route/{id}")
async def push_to_connected_websockets(id: str):
    pass
    # socket = Socket(id)

    # async def playlist_urls(playlist_id):
    #     try:
    #         playlist = Playlist(
    #             "https://www.youtube.com/playlist?list=" + playlist_id)
    #     except Exception as e:
    #         await socket.emit('playlist_urls', 'error')
    #         assert (e)
    #     else:
    #         await socket.emit('playlist_urls', playlist.video_urls)

    # await socket.on('playlist_urls', playlist_urls)


@router.get("/playlist_urls/{playlist_id}")
async def playlist_urls(playlist_id: str):
    playlist = Playlist(
        "https://www.youtube.com/playlist?list=" + playlist_id)
    return playlist.video_urls


class Params(BaseModel):
    id: Optional[str]
    urls: Optional[str]
    extension: str
    resolution: str


@router.get("/download/{socket_id}/{videoId}")
async def stream_video(socket_id: str, videoId: str, extension: str = "mp4", resolution: str = '360p'):
    video = await load_video(videoId, socket_id, ext=extension, res=resolution)
    filename = video.default_filename+'.mp4'
    content_disposition_filename = quote(filename)
    if content_disposition_filename != filename:
        content_disposition = "attachment; filename*=utf-8''{}".format(
            content_disposition_filename
        )
    else:
        content_disposition = 'attachment; filename="{}"'.format(
            filename)
    headers = {'Content-Length': f'{video.filesize}',
               'Content-Disposition': content_disposition}
    return StreamingResponse(video.start_streaming(videoId), media_type=video.mime_type, headers=headers, content_len=video.filesize, socket_id=socket_id, filename=filename, video_id=videoId, filepath=video.path)
