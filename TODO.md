aggiungere a spark un timestamp richiesta
    come ora c'è un select che lo toglie

dashboard grafana
    dashboard richiesta
    dashboard totale richieste
    [capire come esportarla](https://stackoverflow.com/questions/63518460/grafana-import-dashboard-as-part-of-docker-compose)

pagina con input box per fare partire la pipeline

Scraper bugs:
    non legge i commenti
    togliere dal nome della canzone "Chords"
    togliere la virgola dagli interi

Scraper:
    - commenti buggati
    - buggato sulla versione pro delle tab
    - refactoring locator

---
Low priority:
    capire perché su hdfs non funzionano le variabili di ambiente per: server, user, hdfs_base_path

    capire come montare le cartelle di hdfs: c'era tutto il discorso di chmod

    perché tutte le cose che crea sono in root mode

    mettere var globale per python unbuffer [da testare]

    mettere nell'env il nome del file raw della song


Veri lou:
    fare caching di guitar tabs
    Mettere un nome ai container

--

# TODOS
## hdfs
1. capire come mettere di default una cartella e fare riferimento a quella per i volumi di hdfs
2. collegarsi ad un servizio esterno di storage???