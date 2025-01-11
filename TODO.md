Verificare se lo scraping funziona con la nuova ui del sito.
Fare il gitignore

Su spark:
    fare udf scaricamento audio:
        rimuove audio in locale
    
    udf che chiama server spleeter:

    udf che chiama scraping

    join

    buttare sulla coda kafka

Scraper bugs:
    non legge i commenti
    togliere dal nome della canzone "Chords"
    togliere la virgola dagli interi

Scraper:
    - buggato sulla versione pro delle tab
    - refactoring locator

---
Low priority:
    capire perché su hdfs non funzionano le variabili di ambiente per: server, user, hdfs_base_path

    capire come montare le cartelle di hdfs: c'era tutto il discorso di chmod

    perché tutte le cose che crea sono in root mode

    mettere var globale per python unbuffer

Veri lou:
    fare caching di guitar tabs

--

Testin stuff:
## kafka tests
ascolto coda kafka

```
docker exec -it kafkaServer kafka-console-consumer.sh --topic song_requests --bootstrap-server http://kafkaServer:9092 --property print.key=true
```

```
docker exec -it kafkaServer kafka-console-consumer.sh --topic songs --bootstrap-server http://kafkaServer:9092 --property print.key=true
```

## spark tests
inviare su kafka:
```
{"Id": 1,"Yt_Link": "https://www.youtube.com/watch?v=R4x4ysqc_qM","UgChords_Link": "https://tabs.ultimate-guitar.com/tab/alessandro-mannarino/me-so-mbriacato-chords-1516487","Request_Date": "2025-01-01 00:00:00"}
```


# TODOS
## hdfs
1. capire come mettere di default una cartella e fare riferimento a quella per i volumi di hdfs
2. collegarsi ad un servizio esterno di storage???