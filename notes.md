arriva richiesta
c'è un song_dataset_df
    dataset canzoni su cui fare similarity + colonna: "track_id"

c'è un song_dataset_similarity_df
    sarebbe "song_dataset_df" - track_id
    serve per fare similarity


c'è un canzoni_vector_df
    conterrà le stats della canzone richiesta
    serve per fare la similarity search con il dataset
    verrà popolato dei vettori calcolati (df_canzone) sulle canzoni che arrivano

calcolo df_canzone
    avrò un df con le stesse colonne del dataset "song_dataset_similarity_df"
    appendo df_canzone a canzoni_vector_df

similarity
    cosine_similarity tra "canzoni_vector_df" e "song_dataset_similarity_df"
        restituisce n righe di similarity scores
    queste n righe le metto nella colonna "similarity_scores" in un df che copio da song_dataset_df
    ordino in ordine descendente
    prendo i track id dei primi 5
        devo restituire un oggetto {
            yt_link: get_youtube_link_from_spotify_id()
            ug_chords: scraper/get_chords_link()
        }