import yt_dlp
from hdfs import InsecureClient
import os


def upload_hdfs(song_path, song_uid):
    # hdfs_base_path = os.getenv("HDFS_SONG_PATH")
    hdfs_tracks_path = f"/kCHORDS/Music/{song_uid}"
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
        client.upload(hdfs_tracks_path, song_path, overwrite=True)
        print(f"\tUPLOADED {song_path} in {hdfs_tracks_path}", flush=True)
    except Exception as e:
        raise e
        # print(f"Errore durante l'upload di {song_path} in {hdfs_tracks_path}: {e}", flush=True)
    
    return hdfs_tracks_path


def download_mp3(link, request_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'outtmpl': './track_separator/songs/%(title)s.mp3',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            song_name = info_dict['title']
            mp3_file = f'''{song_name}.mp3'''
            
            final_path = f"./track_separator/songs/{mp3_file}"
            
            # hdfs_path = upload_hdfs(final_path, f"{song_name}{request_id}")
            hdfs_path = ''
            return hdfs_path
    except Exception as e:
        raise e
        # print(f"Errore durante il download o la conversione: {e}")
