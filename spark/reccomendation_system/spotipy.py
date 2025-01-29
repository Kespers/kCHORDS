import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_artist_genre(artist_name, dataset_genres, spotify):
    if not artist_name or artist_name.isspace():
        return []

    result = spotify.search(q=artist_name, type='artist', limit=1)

    genres = []
    if result['artists']['items']:
        genres = result['artists']['items'][0].get('genres', [])
    
    return genres

def get_song_info(song_id, spotify):
    try:
        track_info = spotify.track(song_id)
        
        song_data = {
            "name": track_info["name"],
            "artists": [artist["name"] for artist in track_info["artists"]],
            "album": track_info["album"]["name"],
            "link": track_info["external_urls"]["spotify"],
        }
        return song_data

    except Exception as e:
        print(f"Errore durante il recupero delle informazioni della canzone: {e}")
        return None

def get_client():
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)