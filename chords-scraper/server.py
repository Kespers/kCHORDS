from flask import Flask, jsonify, request
from scraper import scrape

app = Flask(__name__)

cache = {}

@app.route('/scrape', methods=['GET'])
def scrapeByLink():
    link = request.args.get('link')

    if not link:
        return jsonify({"error": "Missing link parameter"}), 400

    if link in cache:
        return jsonify(cache[link])
    
    result = scrape(link)
    cache[link] = result
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
