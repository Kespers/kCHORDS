import os
from hdfs import InsecureClient

def save_song(song_data):
    song_uid = f"{song_data.get('song_name')}{song_data.get('id')}"
    local_path = f"separated_tracks/{song_uid}"

    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    input_path = os.path.join(local_path, f"{song_data.get('song_name')}.mp3")
    song_data.get('song').save(input_path)

    return song_uid, input_path, local_path

def divide_tracks(input_path, local_path):
    os.system(f"spleeter separate -i {input_path} -p spleeter:5stems -o {local_path}")

def upload_hdfs(song_data, song_uid, local_path):
    # hdfs_base_path = os.getenv("HDFS_SONG_PATH")
    hdfs_tracks_path = f"/kCHORDS/Music/{song_uid}"
    try:
        # server = os.getenv("HDFS_SERVER")
        # user = os.getenv("HDFS_USER")
        client = InsecureClient('http://namenode:9870', user='root')
    except Exception as e:
        return {'error': 'HDFS connection error'}

    if not client.status(hdfs_tracks_path, strict=False):
        client.makedirs(hdfs_tracks_path)

    spleeter_path = os.path.join(local_path, song_data.get('song_name'))

    for root, _, files in os.walk(spleeter_path):
        for file in files:
            path = os.path.join(root, file)
            hdfs_file_path = os.path.join(hdfs_tracks_path, file)
            print(f"UPLOAD {path} in {hdfs_file_path}", flush=True)
            try:
                client.upload(hdfs_file_path, path, overwrite=True)
                print(f"\tUPLOADED {path} in {hdfs_file_path}", flush=True)
            except Exception as e:
                print(f"Errore durante l'upload di {path} in {hdfs_file_path}: {e}", flush=True)
    
    return hdfs_tracks_path

def remove_local_song(song_uid):
    os.system(f"rm -rf separated_tracks/{song_uid}")