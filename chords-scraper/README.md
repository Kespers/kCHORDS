# Ultimate Guitar Tabs Scraper
scrapes the following info from [ultimate guitar tabs](https://www.ultimate-guitar.com):
```json
{
  "added_favorites": {
    "artist": {
      "name": "",
      "profile_link": ""
    },
    "author": {
      "profile_link": "",
      "username": ""
    },
    "capo_position": "",
    "chords": "",
    "comments": [
      {
        "author": "",
        "message": "",
        "date": "",
        "upvote": ""
      }
    ],
    "difficulty": "",
    "key": "",
    "more_versions": [
      {
        "link": "",
        "name": "",
        "stars": ""
      }
    ],
    "name": "",
    "related_tabs": [
      {
        "link": "",
        "name": "",
        "stars": ""
      }
    ],
    "stars": "",
    "tuning": "",
    "url": "",
    "views": ""
  }
}

```

# 1 Debug
## 1.1 Server Flask
avviare il server:
```
docker build -t chords-scraper .
docker run chords-scraper

```
richiedere lo scrape per un sito:

se avviato con docker:
```
curl -X GET "http://172.17.0.2:6000/scrape?link=https://tabs.ultimate-guitar.com/tab/alessandro-mannarino/apriti-cielo-chords-1936739"
```

se avviato con compose:
```
curl -X GET "http://localhost:6000/scrape?link=https://tabs.ultimate-guitar.com/tab/alessandro-mannarino/l-impero-chords-1760023"
```

## 1.2 Scraper
### 1.2.1 installazione
```
python -m venv venv
cd venv
source bin/activate
pip install playwright
playwright install
```

```
python tester.py > test.json
```

## 1.2.2 Scaricamento Link Canzoni
### 1.2.2.1 Dataset link
costruzione dataset dei link:
```
python get_links.py  > links.json
```

## 1.2.3 Avvio Playwright UI
per testare i selettori avviare l'env ed eseguire:
```
python -m playwright codegen https://www.ultimate-guitar.com
```


## 1.2.4 [bug fix gnome dipendenze](https://github.com/microsoft/playwright/issues/2621#issuecomment-2083083392)