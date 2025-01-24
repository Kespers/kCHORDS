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
    local_path = f"reccomendation_system/separated_tracks/{song_data['id']}"

    # Path(local_path).mkdir(parents=True, exist_ok=True)
    os.makedirs(local_path, exist_ok=True)
    input_path = f"{local_path}/{song_data['id']}/raw_song.mp3"

    client = connect_hdfs()
    client.download(song_data["song_path"], local_path, overwrite=True)

    return input_path, local_path

def convert_to_optimal_codec(song_path):
    # hdfs non tornava un codec che piaceva alla libreria
    output_path = song_path.split("raw_song.mp3")[0]
    os.system(f"ffmpeg -i ./{song_path} -acodec libmp3lame {output_path}/output_file.mp3")

    return f"{output_path}/output_file.mp3"

def get_song_audio_file(request_id, song_path):
    input_path, _ = save_song({
        "song_path": song_path,
        "id": request_id
    })

    return convert_to_optimal_codec(song_path)


def remove_local_song(song_id):
     os.system(f"rm -rf separated_tracks/{song_id}")