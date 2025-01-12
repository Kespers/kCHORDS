import yt_dlp
from hdfs import InsecureClient
import os


def upload_hdfs(raw_download_path, request_id):
    # hdfs_base_path = os.getenv("HDFS_SONG_PATH")
    hdfs_tracks_path = f"/kCHORDS/Music/{request_id}"
    try:
        # server = os.getenv("HDFS_SERVER")
        # user = os.getenv("HDFS_USER")
        print("Connecting to hdfs")
        client = InsecureClient('http://namenode:9870', user='root')
    except Exception as e:
        raise e
        # return {'error': 'HDFS connection error'}

    if not client.status(hdfs_tracks_path, strict=False):
        client.makedirs(hdfs_tracks_path)

    try:
        client.upload(hdfs_tracks_path, raw_download_path, overwrite=True)
        print(f"\tUPLOADED {raw_download_path} in {hdfs_tracks_path}", flush=True)
    except Exception as e:
        raise e
    
    return hdfs_tracks_path


def download_mp3(link, request_id):
    output_path = f'./track_separator/songs/{request_id}/raw_song.mp3'
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'outtmpl': output_path,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            song_name = info_dict['title']

            hdfs_path = upload_hdfs(output_path, request_id)

            os.system(f"rm -rf songs/{request_id}")

            return hdfs_path
    except Exception as e:
        raise e
