# Per testare

avviare il server:
```
docker build -t chords-scraper .
docker run chords-scraper
```


richiedere lo scrape per un sito:
```
curl -X GET "http://172.17.0.2:6000/scrape?link=https://tabs.ultimate-guitar.com/tab/alessandro-mannarino/l-impero-chords-1760023"
```