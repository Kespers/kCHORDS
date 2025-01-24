# kCHORDS

## Testing
### kafka
Invia messaggio kafka
```
docker exec -it kafkaServer bash -c "kafka-console-producer.sh --broker-list kafkaServer:9092 --topic songRequests" --from-beginning
```

incolla:
```
{"Yt_Id": "1", "Request_Date": "2025-01-13 15:33:00","Yt_Link": "https://youtu.be/X6G6UpDgGxk?si=mMHNX5rBNIg-rzOh","UgChords_Link": "https://tabs.ultimate-guitar.com/tab/alessandro-mannarino/apriti-cielo-chords-1936739"}

{"Id": 3,"Yt_Link": "https://youtu.be/mr_ZKg7aiD4?si=4ujDIOGBArKQstQe","UgChords_Link": "https://tabs.ultimate-guitar.com/tab/alessandro-mannarino/deija-chords-1760024","Request_Date": "2025-01-13 15:33:00"}
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

