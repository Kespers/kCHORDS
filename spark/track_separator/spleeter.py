import requests

def separate_track(mp3_path):
    response = requests.post("http://localhost:5000/separate", json={"mp3_path": mp3_path})
    
    tracks = None
    if response.status_code == 200:
        return response.json().get("tracks", tracks)
    else:
        return tracks