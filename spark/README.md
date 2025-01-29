

### spark
topics:
```
docker compose up topics -d
```

start notebook
```
rm ./spark/notebook.log; rm -rf ./spark/logs; docker compose -f dev.docker-compose.yml up --build > ./spark/notebook.log 2>&1
```