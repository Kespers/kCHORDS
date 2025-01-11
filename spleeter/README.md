# Testing
Per test il file si trova in questa cartella ma poi arriva tramite post

dalla root fai partire il server:
```
docker compose up spleeter --build
```

invia richiesta
```
curl -X POST http://localhost:5000/separate \
  -F "mp3_path=@spleeter/quanti_anni_hai.mp3" \
  -F "song_name=quanti_anni_hai" \
  -F "id=1"
```

