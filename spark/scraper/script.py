import requests
import os

def scrape_chords(chords_link):
    url = os.getenv("SCRAPER_URL", "http://chords_scraper:6000/scrape")
    
    try:
        response = requests.get(f'''{url}?link={chords_link}''')
    except Exception as e:
        raise e
    
    return response.text