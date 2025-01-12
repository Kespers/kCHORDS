# kCHORDS

## Testing
### kafka
Invia messaggio kafka
```
docker exec -it kafkaServer bash -c "kafka-console-producer.sh --broker-list kafkaServer:9092 --topic songRequests" --from-beginning
```

incolla:
```
{"Id": 1,"Yt_Link": "https://www.youtube.com/watch?v=R4x4ysqc_qM","UgChords_Link": "https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956925","Request_Date": "2025-01-01 00:00:00"}
```

#### ascolto coda kafka
vedere tutti i messaggi
```
docker exec -it kafkaServer bash -c "kafka-console-consumer.sh --topic songRequests --bootstrap-server kafkaServer:9092 --property print.key=true --from-beginning"

docker exec -it kafkaServer bash -c "kafka-console-consumer.sh --topic songs --bootstrap-server kafkaServer:9092 --property print.key=true --from-beginning"
```

### spark
topics:
```
docker compose up topics -d
```

start notebook
```
rm ./spark/notebook.log; rm -rf ./spark/logs; docker compose -f dev.docker-compose.yml up --build > ./spark/notebook.log 2>&1
```

