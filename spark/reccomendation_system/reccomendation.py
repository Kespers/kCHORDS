from .video_data import *
from .genre import get_genre_df
from .song_stats import get_song_stats
from .spotipy import *
import pandas as pd
import json
from confluent_kafka import Producer

def get_song_df(video_id, request_id, hdfs_mp3_file_path, artist_name, dataset_genres):
  print("[GET SONG DF]: Getting video data")
  video_data = get_video_by_id(video_id)
  print(f"{video_data}\n\n")

  print("[GET SONG DF]: Getting genre")
  genre_df = get_genre_df(video_data, artist_name, dataset_genres)
  print(f"{genre_df}\n\n")

  print("[GET SONG DF]: Getting song stats")
  song_stat_df = get_song_stats(request_id, hdfs_mp3_file_path, video_data)
  print(f"{song_stat_df}\n\n")

  return pd.concat([song_stat_df, genre_df], axis=1)


def extract_genre_from_df(df):
  genre_columns = [col for col in df.columns if col.startswith('genre_')]

  filtered_df = df[df[genre_columns].eq(1.0).any(axis=1)]

  if not filtered_df.empty:
      genre_column = filtered_df.iloc[0][genre_columns].idxmax()
      artist_genre = genre_column.replace('genre_', '')
  else:
      artist_genre = None

  return artist_genre

def get_recommendation(Yt_Id, song_stats, recommended_ids):
	recommends = []
	for id in recommended_ids:
		song_data = get_song_info(id, get_client())
		print("SONG DATA", song_data)
		print("\n\n\n")

		if song_data:
			recommends.append({
				"link": song_data['link'],
				"name": song_data['name'],
				"artists": song_data['artists'],
				"album": song_data['album']
			})
			
	song_stats_dic = song_stats.iloc[0].to_dict() 
	print("DICCC", song_stats_dic)
	return json.dumps({
		"Yt_Id": Yt_Id,
		"Recommends": recommends,
		"Song_Stats": {
			'danceability': song_stats_dic['danceability'],
			'energy': song_stats_dic['energy'],
			'loudness': song_stats_dic['loudness'],
			'speechiness': song_stats_dic['speechiness'],
			'acousticness': song_stats_dic['acousticness'],
			'instrumentalness': song_stats_dic['instrumentalness'],
			'liveness': song_stats_dic['liveness'],
			'valence': song_stats_dic['valence'],
			'tempo': song_stats_dic['tempo'],
			'popularity': song_stats_dic['popularity'],
		}
	})
    

def write_on_kafka(recomendations):
	conf = {
		'bootstrap.servers': 'kafkaServer:9092',
		'client.id': 'spark-recommendation'
	}

	producer = Producer(conf)

	def delivery_report(err, msg):
		if err is not None:
			print('Messaggio non inviato: {}'.format(err))
		else:
			print('Messaggio inviato a {}:{}'.format(msg.topic(), msg.partition()))


	producer.produce('recommendations', key=None, value=recomendations, callback=delivery_report)

	producer.flush()


   