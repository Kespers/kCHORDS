from .video_data import get_video_data
from .genre import get_genre_df
from .song_stats import get_song_stats
import pandas as pd
import asyncio

def get_song_df(video_id, request_id, hdfs_mp3_file_path, dataset_genres):
  print("Gettin song data...")
  video_data = get_video_data(video_id)

  print("VIDEODATA: ", video_data)
  print("Gettin genre mbare...")
  genre_df = get_genre_df(video_data, dataset_genres)

  print("Extracting song stats...")
  song_stat_df = get_song_stats(request_id, hdfs_mp3_file_path, video_data)

  print("Returnin datafreim...")
  return pd.concat([song_stat_df, genre_df], axis=1)
  #return pd.concat([pd.DataFrame([video_data])], axis=1)