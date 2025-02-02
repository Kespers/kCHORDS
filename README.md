# kCHORDS

Tired of juggling multiple windows just to play along with a song?

With kCHORDS, simply provide:
- link of the [chords](https://www.ultimate-guitar.com/)
- link of the [song](https://www.youtube.com/) you want to play

kCHORDS will automatically separates the audio into distinct tracks—vocals (bass, piano, drums, and other instruments) and presents everything in a single, seamless interface.

But that’s not all! featuring a content-based recommendation system that suggests songs based on the characteristics of the one you just played.

Stop wasting time setting up...find your place in the
sound 🎸🥁🎹

# Running commands
0. To run the project you will need youtube and spotify API TOKENS:

Create a `.env` file with your tokens
```
GOOGLE_TOKEN={YOUR_TOKEN}
SPOTIFY_CLIENT_ID={YOUR_TOKEN}
SPOTIFY_CLIENT_SECRET={YOUR_TOKEN}
SCRAPER_URL=http://chords_scraper:6000/scrape
```


1. Start the project
```
docker compose up --build
```
2. Follow the [Grafana README](./grafana/README.md) to setup the dashboard

3. Open `web-page/index.html` to access the web interface, where you’ll be guided on how to proceed with the pipeline.

# Architecture
![alt text](pipeline.jpg)

It is made by the following containers:
- **Fluentd**: receives the YouTube & Ultimate Guitar links, adds a timestamp and unique ID, and sends them to Kafka.
- **Kafka**: Uses topics to queue data for Spark processing.
- **Spark**: Orchestrates data extraction, audio separation, and storage.
- **Hdfs**: Stores both the raw audio and processed stems for further analysis.
- **Spleeter**: Separate the audio file into 5 stems
- **Chords_Scraper**: Scrapes and structures guitar tabs from Ultimate Guitar Tabs
- **Logstash**: Ingests processed song data from Kafka topic "songs" into Elasticsearch.
- **Elasticsearch**: Stores and indexes song metadata, extracted tabs, and separated audio tracks.
- **Grafana**: Visualizes everything in an interactive dashboard.
