import time
import os
from backend.utils import Settings, YouTubeVideoFile, YoutubeVideoStream
from backend.store import store
from backend.socket import Socket
from pytube import YouTube

from backend import config
import secrets


def get_code(): return secrets.token_hex()


downloads = {}


async def download_video(youtube_video_stream, youtube_obj, save_path, ext) -> YoutubeVideoStream:
    '''
    This returns the Youtube video object if the requested is progressive
    else returns CustomYoutubeVideoStream object
    but first it downloads both audio and video seperately and
    later combines them as one video which is then 
    constructed with CustomYoutubeVideoStream instance p
    '''
    vid = youtube_video_stream.filter(progressive=True).first()
    # print(f'This is vid: {vid}')
    if vid:
        print('video is progressive')
        return YoutubeVideoStream(vid.title, vid.mime_type, url=vid.url, size=vid.filesize)
    else:
        print('video is NOT progressive')
        vid = youtube_video_stream.first()
        aud = youtube_obj.streams.filter(type='audio').filter(file_extension=ext).filter(
            progressive=False).first() or youtube_obj.streams.filter(type='audio').filter(
            progressive=False).first()

        filename = get_code()

        aud_path = aud.download(save_path, filename=filename+'-a')
        vid_path = vid.download(save_path, filename=filename+'-v')

        file_path = os.path.join(save_path, filename+'.'+ext)

        print('filename', file_path, aud_path)
        command = f"ffmpeg -i {vid_path} -i {aud_path} -c copy {file_path}"
        os.system(command)
        os.remove(vid_path)
        os.remove(aud_path)
        return YouTubeVideoFile(file_path, vid.title, vid.mime_type)


async def load_video(videoId, res='720p', typ='video'):
    print('loading... video')
    url = f'https://youtu.be/{videoId}'
    ext = "mp4"
    save_path = config.Path

    print('save_path', save_path)

    youtube_obj = YouTube(url)
    youtube_video_stream = youtube_obj.streams.filter(type=typ)
    youtube_video_stream = youtube_video_stream.filter(
        file_extension=ext).filter(res=res)
    try:
        return await download_video(youtube_video_stream, youtube_obj, save_path, ext)
    except Exception as e:
        'The resolution which was provided could not be downloaded'
        print(e)
