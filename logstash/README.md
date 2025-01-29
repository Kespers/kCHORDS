# Cheffa?
prende dalla coda "songs" e crea un indice "songs" per ora...poi si vedrà

# Testing
entrare nel container di kafka

vedere offset:
```
kafka-consumer-groups.sh --bootstrap-server kafkaServer:9092 --group logstash --describe
```

eliminare offset di kafka
```
kafka-consumer-groups.sh --bootstrap-server kafkaServer:9092 \
    --group logstash \
    --topic songs \
    --reset-offsets --to-earliest --execute
```