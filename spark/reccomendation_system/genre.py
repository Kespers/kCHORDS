import requests
import os
import spacy
from fuzzywuzzy import process
from requests.auth import HTTPBasicAuth
from collections import Counter
import pandas as pd
from .utils import get_spotify_token

def extract_person_from_video_data(video_data):
    nlp = spacy.load('en_core_web_sm')
    text_to_search = video_data['title'] + " " + video_data['description'] + " " + " ".join(video_data['tags'])
    doc = nlp(text_to_search)

    person_entities = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

    return person_entities if person_entities else None


def get_most_similar_genre(genres, dataset_genres):
    most_similar_genre = None
    highest_similarity = 0

    for genre in genres:
        best_match = process.extractOne(genre, dataset_genres)
        if best_match:
            similarity_score = best_match[1]
            if similarity_score > highest_similarity:
                highest_similarity = similarity_score
                most_similar_genre = best_match[0]

    return most_similar_genre

def get_artist_genre(artist_name, access_token, dataset_genres):

    search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(search_url, headers=headers)

    genres = []
    if response.status_code == 200:
        results = response.json()
        if results['artists']['items']:
            genres = results['artists']['items'][0].get('genres', [])

    if genres:
        return get_most_similar_genre(genres, dataset_genres)
    return None



def get_genre_df(video_data, dataset_genres):
    def get_genre(video_data):
        access_token = get_spotify_token()

        genres = []
        possible_artists = extract_person_from_video_data(video_data)

        for person in possible_artists:
            genre = get_artist_genre(person, access_token, dataset_genres)
            if genre:
                genres.append(genre)

        genre_counts = Counter(genres)
        return genre_counts.most_common(1)[0][0] if genre_counts else None

    df = pd.DataFrame({'genre': [get_genre(video_data)]})
    
    # encoding
    for genre in dataset_genres:
        df[f'genre_{genre}'] = df['genre'].apply(lambda g: 1 if g == genre else 0)

    df.drop('genre', axis=1, inplace=True)

    return df