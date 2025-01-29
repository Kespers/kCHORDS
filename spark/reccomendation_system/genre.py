import requests
import os
import spacy
from fuzzywuzzy import process
from requests.auth import HTTPBasicAuth
from collections import Counter
import pandas as pd
from .spotipy import *

def extract_person_from_video_data(video_data):
    nlp = spacy.load('en_core_web_sm')
    text_to_search = video_data['title'] + " " + video_data['description'] + " " + " ".join(video_data['tags'])
    doc = nlp(text_to_search)

    person_entities = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

    return person_entities if person_entities else None


def dataset_mapping(genres, dataset_genres):
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

def get_genre_df(video_data, artist_name, dataset_genres):
    genres = []
    possible_artists = [artist_name]

    if not possible_artists:
        possible_artists = extract_person_from_video_data(video_data)
    
    for person in possible_artists:
        raw_genre = get_artist_genre(person, dataset_genres, get_client())
        genre = dataset_mapping(raw_genre, dataset_genres)

        if genre:
            genres.append(genre)

    genre_counts = Counter(genres)
    artist_genre = genre_counts.most_common(1)[0][0] if genre_counts else None

    df = pd.DataFrame({'genre': [artist_genre]})
    
    # encoding
    for genre in dataset_genres:
        df[f'genre_{genre}'] = df['genre'].apply(lambda g: 1 if g == genre else 0)

    df.drop('genre', axis=1, inplace=True)

    return df