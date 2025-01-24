import os
from hdfs import InsecureClient
from pathlib import Path

def connect_hdfs():
    try:
        # server = os.getenv("HDFS_SERVER")
        # user = os.getenv("HDFS_USER")
        return InsecureClient('http://namenode:9870', user='root')
    except Exception as e:
        return {'error': 'HDFS connection error'}

def save_song(song_data):
    # togli id
    local_path = f"separated_tracks/{song_data['id']}"

    # Path(local_path).mkdir(parents=True, exist_ok=True)
    os.makedirs(local_path, exist_ok=True)
    input_path = f"{local_path}/{song_data['id']}/raw_song.mp3"

    client = connect_hdfs()
    client.download(song_data["song_path"], local_path, overwrite=True)

    return input_path, local_path

def divide_tracks(input_path, local_path):
    os.system(f"spleeter separate -i {input_path} -p spleeter:5stems -o {local_path}")

def upload_hdfs(song_data, local_path):
    # spleeter  | Errore durante l'upload di separated_tracks/1/raw_song/piano.wav in /kCHORDS/Music/1/raw_song.mp3/piano.wav: /kCHORDS/Music/1/raw_song.mp3 (is not a directory)
    
    hdfs_tracks_path = f"/kCHORDS/Music/{song_data['id']}/separated_tracks"

    client = connect_hdfs()
    if not client.status(hdfs_tracks_path, strict=False):
        client.makedirs(hdfs_tracks_path)

    spleeter_path = os.path.join(local_path, "raw_song")

    for root, _, files in os.walk(spleeter_path):
        for file in files:
            path = os.path.join(root, file)
            hdfs_file_path = os.path.join(hdfs_tracks_path, file)
            print(f"UPLOAD {path.split('/')[-1]} in {hdfs_file_path.split('/')[-1]}", flush=True)
            try:
                client.upload(hdfs_file_path, path, overwrite=True)
                print(f"\tSUCCESS", flush=True)
            except Exception as e:
                print(f"Errore durante l'upload di {path} in {hdfs_file_path}: {e}", flush=True)
    
    return hdfs_tracks_path

def remove_local_song(song_id):
     os.system(f"rm -rf separated_tracks/{song_id}")