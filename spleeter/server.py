from flask import Flask, request
import os
from hdfs import InsecureClient
import subprocess
from utils import *

app = Flask(__name__)

@app.route('/')
def root():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <meta
            http-equiv="refresh"
            content="0; url=https://youtu.be/O5yw9s34UE4?si=5sjDIvKDC3_QMi5k"
            />
            <title>Redirect</title>
        </head>
        <body></body>
        </html>
    '''

@app.route('/separate', methods=['POST'])
def separate():
    song_data = {
        "song_path": request.form['song_path'],
        "id": request.form['id']
    }

    print(f"Request for the song: {song_data['song_path']}")
    input_path, local_path = save_song(song_data)

    print("\tDividing tracks", flush=True)
    divide_tracks(input_path, local_path)
    
    print("\tUploading on hdfs server", flush=True)
    hdfs_tracks_path = upload_hdfs(song_data, local_path)

    print("\tRemoving local song", flush=True)
    remove_local_song(song_data["id"])

    return hdfs_tracks_path

if __name__ == "__main__":
    app.run(debug=True)