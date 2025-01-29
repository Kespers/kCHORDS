import pandas as pd
from .hdfs import get_song_audio_file, remove_local_song
from essentia.standard import MusicExtractor


def get_popularity_score(video_info):
    view_count = int(video_info['view_count'])
    like_count = int(video_info['like_count'])
    comment_count = int(video_info['comment_count'])

    max_view_count = 100000  
    max_like_count = 1000    
    max_comment_count = 100 

    
    normalized_view_count = view_count / max_view_count
    normalized_like_count = like_count / max_like_count
    normalized_comment_count = comment_count / max_comment_count

    
    normalized_view_count = min(normalized_view_count, 1)
    normalized_like_count = min(normalized_like_count, 1)
    normalized_comment_count = min(normalized_comment_count, 1)

    
    weight_view_count = 0.2
    weight_like_count = 0.3
    weight_comment_count = 0.25

    
    popularity_score = (
        weight_view_count * normalized_view_count +
        weight_like_count * normalized_like_count +
        weight_comment_count * normalized_comment_count
    )

    
    return round(popularity_score, 2)

def get_song_stats(request_id, song_path, video_data):
    music_extractor = MusicExtractor(
        lowlevelStats=['mean', 'stdev'],
        rhythmStats=['mean', 'stdev'],
        tonalStats=['mean', 'stdev']
    )

    print("downloadin rawMP3 from hdfs...")
    audio_file = get_song_audio_file(request_id, song_path)

    print("AUDIO PATH: ", audio_file)
    

    print(f"Extracting metadatass [{audio_file}]...")
    features, _ = music_extractor(audio_file)
    
    stats = {
        "danceability": features["rhythm.danceability"], #0 to 3 
        "energy": features["lowlevel.spectral_energy.mean"],
        "loudness": features["lowlevel.average_loudness"], # 0 to 1
        "speechiness": features["lowlevel.spectral_entropy.mean"],
        "acousticness": features["lowlevel.melbands_flatness_db.mean"],
        "instrumentalness": features["lowlevel.pitch_salience.mean"],
        "liveness": features["lowlevel.spectral_flux.mean"],
        "valence": features["tonal.chords_strength.mean"],
        "tempo": features["rhythm.bpm"],
        "popularity": get_popularity_score(video_data)
    }

    remove_local_song(request_id)
    
    return pd.DataFrame([stats])