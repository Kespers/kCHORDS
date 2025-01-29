# Ultimate Guitar Tab - Scraper
## Server Flask
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

## Scraper
### installazione
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

## Scaricamento Link Canzoni
### Dataset link
costruzione dataset dei link:
```
python get_links.py  > links.json
```

## Avvio Playwright UI
per testare i selettori avviare l'env ed eseguire:
```
python -m playwright codegen https://www.ultimate-guitar.com
```
---
## [bug fix dipendenze](https://github.com/microsoft/playwright/issues/2621#issuecomment-2083083392)