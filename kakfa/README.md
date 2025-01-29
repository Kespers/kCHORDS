# Kafka
## ascolto coda kafka
vedere tutti i messaggi
```
docker exec -it kafkaServer bash -c "kafka-console-consumer.sh --topic recommendation --bootstrap-server kafkaServer:9092 --property print.key=true --from-beginning"

docker exec -it kafkaServer bash -c "kafka-console-consumer.sh --topic songRequests --bootstrap-server kafkaServer:9092 --property print.key=true --from-beginning"

docker exec -it kafkaServer bash -c "kafka-console-consumer.sh --topic songs --bootstrap-server kafkaServer:9092 --property print.key=true --from-beginning"
```