# %% [markdown]
# # Setup

# %%
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, TimestampType, StringType, ArrayType, DoubleType, FloatType
from pyspark.sql.functions import from_json, col, udf, row_number, lit
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import col
from pyspark.ml.linalg import Vectors
from pyspark.sql import functions as F
from pyspark.sql.functions import col
from pyspark.sql import functions as F
from pyspark.ml.linalg import Vectors
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from track_separator.download_mp3 import download_mp3
from track_separator.spleeter import separate_track
from scraper.script import scrape_chords
from reccomendation_system.reccomendation import *

# %%
# senza check
spark = SparkSession.builder \
	.appName("kCHORDS") \
	.getOrCreate()


spark.sparkContext.setLogLevel("INFO")

# %%
df_song_requests_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafkaServer:9092") \
    .option("subscribe", "songRequests") \
    .load()

# %%

SONG_REQUEST_SCHEMA = StructType([
    StructField("Yt_Id", StringType(), True),
    StructField("Yt_Link", StringType(), True),
    StructField("UgChords_Link", StringType(), True),
    StructField("Request_Date", TimestampType(), True),
])

# %%
def print_df(df):
	query = df.writeStream \
	.outputMode("append") \
	.format("console") \
	.start()

	query.awaitTermination()

# query.awaitTermination()

# %% [markdown]
# # Lettura da topic Input

# %%
df_song_requests = df_song_requests_raw \
	.selectExpr("CAST(value AS STRING)") \
	.select(from_json(col("value"), SONG_REQUEST_SCHEMA).alias("data")) \
	.select("data.*")

# %% [markdown]
# # Scraping accordi

# %%
@udf(returnType=StringType())
def scrape_chords_udf(chords_link):
	return scrape_chords(chords_link)

df_chords_raw = df_song_requests.withColumn("scraped_data_raw", scrape_chords_udf(col("UgChords_Link")))
# query = df_chords_raw \
# 	.writeStream \
# 	.outputMode("append") \
# 	.format("json") \
# 	.option("path", "./logs") \
# 	.option("checkpointLocation", "./logs/checkpoint/raw") \
# 	.start()

# query.awaitTermination()

# %%
ArtistType = StructType([
	StructField('name', StringType(), True),
	StructField('profile_link', StringType(), True),
])

AuthorType = StructType([
	StructField('profile_link', StringType(), True),
	StructField('username', StringType(), True),
])

CommentsType = 	ArrayType(StructType([
        StructField('author', StringType(), True),
		StructField('message', StringType(), True),
		StructField('date', TimestampType(), True),
		StructField('upvote', IntegerType(), True)
]))

tab_schema = ArrayType(StructType([
	StructField('link', StringType(), True),
	StructField('name', StringType(), True),
	StructField('stars', IntegerType(), True),
]))
MoreVersionType = tab_schema
RelatedTabsType = tab_schema

CHORDS_SCHEMA = StructType(
    [
        StructField('added_favorites', IntegerType(), True),
        StructField('artist', ArtistType, True),
        StructField('author', AuthorType, True),
        StructField('capo_position', StringType(), True),
        StructField('chords', StringType(), True),
        StructField('comments', CommentsType, True),
        StructField('difficulty', StringType(), True),
        StructField('key', StringType(), True),
        StructField('more_versions', MoreVersionType, True),
        StructField('name', StringType(), True),
        StructField('related_tabs', RelatedTabsType, True),
        StructField('stars', IntegerType(), True),
        StructField('tuning', StringType(), True),
        StructField('url', StringType(), True),
        StructField('views', IntegerType(), True),
    ]
)

df_chords = df_chords_raw \
    .select("*", from_json(col("scraped_data_raw"), CHORDS_SCHEMA).alias("scraped_data"))

df_chords.printSchema()


# print_df(df_chords)

# query = df_chords \
# 	.writeStream \
# 	.outputMode("append") \
# 	.format("json") \
# 	.option("path", "./logs") \
# 	.option("checkpointLocation", "./logs/checkpoint") \
# 	.start()

# query.awaitTermination()

# %% [markdown]
# # Estrazione audio tracks

# %%
@udf(returnType=StringType())
def download_mp3_udf(yt_link, request_id):
	return download_mp3(yt_link, request_id)


df_audio = df_song_requests.withColumn("Hdfs_Song_Path", download_mp3_udf(col("Yt_Link"), col("Yt_Id")))
df_audio.printSchema()

# %%
@udf(returnType=StringType())
def separate_track_udf(hdfs_song_path, request_id):
	return separate_track(hdfs_song_path, request_id)


df_separated_tracks = df_audio.withColumn("Hdfs_Tracks_Path", separate_track_udf(col("Hdfs_Song_Path"), col("Yt_Id")))

df_separated_tracks \
	.printSchema()

# %% [markdown]
# # Sistema di Raccomandazione

# %%
RECCOMENDATION_DATASET_SCHEMA = StructType([
    StructField("index", IntegerType(), True),
    StructField("track_id", StringType(), True),
    StructField("popularity", DoubleType(), True),
    StructField("danceability", DoubleType(), True),
    StructField("energy", DoubleType(), True),
    StructField("loudness", DoubleType(), True),
    StructField("speechiness", DoubleType(), True),
    StructField("acousticness", DoubleType(), True),
    StructField("instrumentalness", DoubleType(), True),
    StructField("liveness", DoubleType(), True),
    StructField("valence", DoubleType(), True),
    StructField("tempo", DoubleType(), True),
] + [
    StructField(f"genre_{genre}", DoubleType(), True)
    for genre in [
		'acoustic', 'alt-rock', 'alternative', 'ambient', 'blues', 'classical', 'country', 'dance', 
		'disco', 'electro', 'electronic', 'folk', 'funk', 'gospel', 'hip-hop', 'house', 'indie', 'jazz', 
		'latin', 'metal', 'pop', 'rock', 'soul', 'synth-pop', 'techno', 'trance'
    ]
])

song_dataset = spark \
    .read \
    .option("mode", "PERMISSIVE") \
    .schema(RECCOMENDATION_DATASET_SCHEMA) \
    .option("delimiter", "\t") \
    .option("header", "true") \
    .csv("reccomendation_system/SONG_DATASET.csv")

song_dataset.show()

# %%
columns_to_drop = ['index', 'track_id']
song_dataset_cosine_sim = song_dataset.drop(*columns_to_drop)

song_dataset_cosine_sim.show()

# %%
dataset_columns = song_dataset_cosine_sim.columns
print(dataset_columns)

# %%
genres = [genre.replace('genre_','') for genre in song_dataset.columns if "genre_" in genre]
genres

# %%
columns = ['Yt_Id', 'Hdfs_Song_Path', col('scraped_data.artist.name').alias('artist_name')]
df_reccomendation = df_audio \
    .join(df_chords, on=["Yt_Id"], how="inner") \
    .select(*columns)

df_reccomendation.printSchema()

# %%
def reccomend_songs(batch_df, batch_id):
    for row in batch_df.collect():
        video_id = row['Yt_Id']
        request_id = row['Yt_Id']
        hdfs_mp3_file_path = row['Hdfs_Song_Path']
        artist_name = row['artist_name']

        song_df = get_song_df(video_id, request_id, hdfs_mp3_file_path, artist_name, genres)

        x = song_dataset_cosine_sim.toPandas()
        y = song_df
        similarity_scores = cosine_similarity(x, y)

        feat_vec = song_dataset.toPandas()
        feat_vec['similarity_score'] = similarity_scores

        artist_genre = extract_genre_from_df(song_df)
        print("Genre: ", artist_genre)
        top_similarities_ids = feat_vec\
            .loc[feat_vec[f'genre_{artist_genre}'] == 1] \
            .sort_values(by='similarity_score', ascending=False) \
            .drop_duplicates(subset='track_id') \
            .head(5) \
            ['track_id']

        print("TOPPPPSIM: ", top_similarities_ids)
        print("\n\n\n")

        song_stats = song_df.loc[:, ~song_df.columns.str.startswith('genre_')]

        recomendations = get_recommendation(request_id, song_stats, top_similarities_ids)
        write_on_kafka(recomendations)

df_recommended_songs = df_reccomendation \
	.writeStream \
	.foreachBatch(reccomend_songs)\
	.start()

# %%
SONG_STATS_SCHEMA = StructType([
    StructField('danceability', DoubleType(), True),
    StructField('energy', DoubleType(), True),
    StructField('loudness', DoubleType(), True),
    StructField('speechiness', DoubleType(), True),
    StructField('acousticness', DoubleType(), True),
    StructField('instrumentalness', DoubleType(), True),
    StructField('liveness', DoubleType(), True),
    StructField('valence', DoubleType(), True),
    StructField('tempo', DoubleType(), True),
    StructField('popularity', DoubleType(), True),
])

RECOMMENDED_SONGS_SCHEMA = ArrayType(StructType([
        StructField('yt_link', StringType(), True),
		StructField('name', StringType(), True),
		StructField('artists', ArrayType(StringType()), True),
		StructField('album', StringType(), True)
]))

RECOMMENDATION_SCHEMA = StructType([
    StructField("Yt_Id", StringType(), True),
    StructField('Song_Stats', SONG_STATS_SCHEMA, True),
    StructField('Recommends', RECOMMENDED_SONGS_SCHEMA, True),
])

# %%
df_recommendation_response_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafkaServer:9092") \
    .option("subscribe", "recommendations") \
    .option("startingOffsets", "earliest") \
    .load()

df_recommendation_response = df_recommendation_response_raw \
	.selectExpr("CAST(value AS STRING)") \
	.select(from_json(col("value"), RECOMMENDATION_SCHEMA).alias("data")) \
	.select("data.*")

df_recommendation_response.printSchema()

# %% [markdown]
# # Join: Chords - Track Separator - Reccomendation System

# %%
df_merged = df_chords \
    .join(df_separated_tracks, on=["Yt_Id"], how="inner") \
    .join(df_recommendation_response, on=["Yt_Id"], how="inner") \
    .drop('scraped_data_raw')
df_merged.printSchema()

# %% [markdown]
# # Scrittura nel topic di output

# %%
df_merged \
	.selectExpr('cast(Yt_Id as string) as key', 'to_json(struct(*)) as value') \
	.writeStream \
    .outputMode("append") \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafkaServer:9092") \
    .option("checkpointLocation", "/tmp") \
    .option("topic", "songs") \
    .start() \
    .awaitTermination()


