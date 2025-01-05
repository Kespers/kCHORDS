from flask import Flask, jsonify, request
from scraper import scrape

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrapeByLink():
    # Ottieni il link dalla query string
    link = request.args.get('link')

    if not link:
        return jsonify({"error": "Missing link parameter"}), 400

    # Esegui lo scraping con il link fornito
    result = scrape(link)
    
    return jsonify(scraped_data=result)

if __name__ == '__main__':
    app.run(debug=True)