import requests
import os

from requests.auth import HTTPBasicAuth

def get_youtube_link_from_spotify_id(spotify_id):
    spotify_token = get_spotify_token()
    try:
        spotify_url = f"https://api.spotify.com/v1/tracks/{spotify_id}"
        spotify_headers = {
            "Authorization": f"Bearer {spotify_token}"
        }
        spotify_response = requests.get(spotify_url, headers=spotify_headers)
        
        if spotify_response.status_code != 200:
            return f"Errore Spotify: {spotify_response.status_code} - {spotify_response.json()}"
        
        spotify_data = spotify_response.json()
        song_name = spotify_data['name']
        artist_name = spotify_data['artists'][0]['name']
        query = f"{song_name} {artist_name}"


        youtube_api_key = os.getenv('GOOGLE_TOKEN')
        youtube_url = "https://www.googleapis.com/youtube/v3/search"
        youtube_params = {
            "part": "snippet",
            "q": query,
            "key": youtube_api_key,
            "type": "video",
            "maxResults": 1
        }
        youtube_response = requests.get(youtube_url, params=youtube_params)
        
        if youtube_response.status_code != 200:
            return f"Errore YouTube: {youtube_response.status_code} - {youtube_response.json()}"
        
        youtube_data = youtube_response.json()
        if "items" in youtube_data and len(youtube_data["items"]) > 0:
            video_id = youtube_data["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return "Nessun video trovato su YouTube."
    
    except Exception as e:
        return f"Errore: {str(e)}"
    

def get_spotify_token():
  CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
  CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

  spotify_base_url = "https://accounts.spotify.com/api/token"

  response = requests.post(
      spotify_base_url,
      data={'grant_type': 'client_credentials'},
      auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
  )

  if response.status_code == 200:
      return response.json()['access_token']