import time
import os
from backend.utils import YouTube, Settings
from backend.store import store
from backend.socket import Socket

from backend import config
import secrets


def get_code(): return secrets.token_hex()


class CustomYoutubeVideoStream:
    '''
    This is mimic the YouTube Video Stream Object
    '''

    def __init__(self, default_filename, path, mime_type):
        self.default_filename = default_filename
        self.path = path
        self.mime_type = mime_type

    def start_streaming(self, *args, **kwargs):
        return open(self.path, mode='rb')

    @property
    def filesize(self):
        return os.stat(self.path).st_size


downloads = {}


def on_progress(*args):
    # print('args', args[-1])
    pass


def on_complete(*args):
    print('args', args)


async def download_video(youtube_video_stream_filtered_ext, youtube_obj, save_path, ext, res) -> CustomYoutubeVideoStream:
    '''
    This returns the Youtube video object if the requested is progressive
    else returns CustomYoutubeVideoStream object
    but first it downloads both audio and video seperately and
    later combines them as one video which is then 
    constructed with CustomYoutubeVideoStream instance p
    '''

    print(ext, res)
    vid = youtube_video_stream_filtered_ext.filter(
        res=res).filter(progressive=True).first()
    # print(f'This is vid: {vid}')
    if vid:
        print('there is vid')
        # filename = get_code()
        return vid
    else:
        vid = youtube_video_stream_filtered_ext.filter(res=res).first()
        aud = youtube_obj.streams.filter(type='audio').filter(file_extension=ext).filter(
            progressive=False).first()

        print('vid,aud', vid)
        filename = get_code()

        aud_path = aud.download(save_path, filename=filename+'-a')
        vid_path = vid.download(save_path, filename=filename+'-v')

        # vid_path = os.path.join(save_path, filename+'-v.'+ext)
        # aud_path = os.path.join(save_path, filename+'-a.'+ext)

        file_path = os.path.join(save_path, filename+'.'+ext)

        print('filename', file_path, aud_path)
        command = f"ffmpeg -i {vid_path} -i {aud_path} -c copy {file_path}"
        os.system(command)
        os.remove(vid_path)
        os.remove(aud_path)
        return CustomYoutubeVideoStream(vid.title, file_path, vid.mime_type)


async def load_video(videoId, socket_id, ext='mp4', res='720p'):
    # print('starting download')
    url = f'https://youtu.be/{videoId}'
    # downloads = store.downloads
    # if store.downloads.__contains__(url):
    #     print('store.downloads', store.downloads)

    t1 = time.perf_counter()
    typ = 'video'
    save_path = config.Path
    print('save_path', save_path)
    # this is just to help me check if a youtube_video_stream_filtered_ext is downloaded or not
    downloaded = False
    youtube_obj = YouTube(url, on_progress_callback=on_progress,
                          on_complete_callback=on_complete)
    # youtube_obj.socket_id = 'socket_id'
    title = youtube_obj.title

    async def on_start():
        'sends this info to browser client in order to start showing downloads on_progress'
        await Socket(socket_id).emit('download_start', {'videoId': videoId, 'filename': title})
        print('\ndownload_start\n')

    # await on_start()
    # await Socket(socket_id).on('download_start', on_start)
    # await Socket(socket_id).emit('download_start', {'videoId': videoId, 'filename': title})
    youtube_video_stream = youtube_obj.streams.filter(type=typ)
    youtube_video_stream_filtered_ext = youtube_video_stream.filter(
        file_extension=ext)
    if not youtube_video_stream_filtered_ext.first():
        ext = 'mp4'
        youtube_video_stream_filtered_ext = youtube_video_stream.filter(
            file_extension=ext)
    try:
        return await download_video(youtube_video_stream_filtered_ext, youtube_obj, save_path, ext, res)
        downloaded = True
    except Exception as e:
        'The resolution which was provided could not be downloaded'
        'It is going to try other resolutions starting from the best posible quality'
        print(e)
        resolutions = ['1080p', '720p', '480p', '360p', '144p']
        if res in resolutions:
            'removes the current failed resolutions'
            resolutions.remove(res)
        for rs in resolutions:
            try:
                return await download_video(youtube_video_stream_filtered_ext, youtube_obj, save_path, ext, res)
                downloaded = True
                break
            except:
                continue
    if not downloaded:
        assert(f'Sorry could not download Youtube Video with id => {videoId} ')
    t2 = time.perf_counter()
    print(f'\nIt took {t2 - t1 } secs to complete')
