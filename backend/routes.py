from fastapi.responses import FileResponse, StreamingResponse
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


@router.get("/playlist_urls/{playlist_id}")
async def playlist_urls(playlist_id: str):
    playlist = Playlist(
        "https://www.youtube.com/playlist?list=" + playlist_id)
    return playlist.video_urls


def delete_video(filepath):
    def _del(filepath):
        if filepath and os.path.exists(filepath):
            os.remove(filepath)

    return _del(filepath)


@router.get("/download/{videoId}")
async def stream_video(videoId: str, resolution: str = '360p'):
    video: YoutubeVideoStream = await load_video(videoId, res=resolution)
    if video.is_stream:
        return StreamingResponse(video(), media_type=video.media_type, headers=video.headers)
    return FileResponse(video.filepath, media_type=video.media_type, filename=video.filename, background=delete_video(video.filepath))
