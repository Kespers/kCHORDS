# Testing
Per test il file si trova in questa cartella ma poi arriva tramite post

dalla root fai partire il server:
```
docker compose up spleeter --build
```

invia richiesta
```bash
curl -X POST http://spleeter:5000/separate \
  -F "song_path=/kCHORDS/Music/1" \
  -F "id=1"
```

