import requests

def separate_track(hdfs_path, request_id):
    request_data = {
        "song_path": hdfs_path,
        "id": request_id
    }
    response = requests.post("http://spleeter:5000/separate", data=request_data)
    
    tracks = None
    if response.status_code == 200:
        return response.text
    else:
        return tracks