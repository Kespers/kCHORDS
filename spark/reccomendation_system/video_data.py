import os
import requests

def get_video_data(query: str = None, video_id: str = None):
    YT_KEY = os.getenv('GOOGLE_TOKEN')

    if not YT_KEY:
        raise ValueError("Google API key is missing. Please set 'GOOGLE_TOKEN' in the environment variables.")

    base_url = 'https://www.googleapis.com/youtube/v3'

    if video_id:
        url = f'{base_url}/videos'
        params = {
            'key': YT_KEY,
            'id': video_id,
            'part': 'snippet,statistics,contentDetails',
        }
    elif query:
        url = f'{base_url}/search'
        params = {
            'key': YT_KEY,
            'q': query,
            'part': 'snippet',
            'type': 'video',
            'maxResults': 1
        }
    else:
        raise ValueError("Devi fornire un video_id o una query!")

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if video_id:
            if 'items' in data and len(data['items']) > 0:
                video_info = data['items'][0]
                return {
                    'video_id': video_id,
                    'title': video_info['snippet']['title'],
                    'description': video_info['snippet']['description'],
                    'tags': video_info['snippet'].get('tags', []),
                    'view_count': video_info['statistics']['viewCount'],
                    'like_count': video_info['statistics'].get('likeCount', 'N/A'),
                    'comment_count': video_info['statistics'].get('commentCount', 'N/A'),
                    'duration': video_info['contentDetails']['duration']
                }
        elif query:
            if 'items' in data and len(data['items']) > 0:
                first_video = data['items'][0]
                video_id = first_video['id']['videoId']
                return {
                    'video_id': video_id,
                    'title': first_video['snippet']['title'],
                    'description': first_video['snippet']['description'],
                    'channel_title': first_video['snippet']['channelTitle'],
                    'video_link': f'https://www.youtube.com/watch?v={video_id}'
                }
    else:
        print(f"Errore durante la richiesta: {response.status_code}")
    return None

def get_video_by_id(video_id):
    return get_video_data(video_id=video_id)

def get_video_by_name(query):
    return get_video_data(query=query)