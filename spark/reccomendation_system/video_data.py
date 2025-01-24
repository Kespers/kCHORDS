import os
import requests

def get_video_data(video_id):
    
    YT_KEY = os.getenv('GOOGLE_TOKEN')

    url = f'https://www.googleapis.com/youtube/v3/videos'

    
    params = {
        'key': YT_KEY,
        'id': video_id,
        'part': 'snippet,statistics,contentDetails,recordingDetails,status,topicDetails',  
    }
        
    response = requests.get(url, params=params)

    
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            video_info = data['items'][0]
            return {
                'title': video_info['snippet']['title'],
                'description': video_info['snippet']['description'],
                'tags': video_info['snippet'].get('tags', []),
                'view_count': video_info['statistics']['viewCount'],
                'like_count': video_info['statistics']['likeCount'],
                'comment_count': video_info['statistics']['commentCount'],
                'duration': video_info['contentDetails']['duration']
            }
    return None
