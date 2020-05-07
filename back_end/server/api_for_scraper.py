from flask import Blueprint, jsonify, request, Response
from config import SECRET
scraper_api = Blueprint('scraper_api', __name__)

@scraper_api.route("/done_scraping_car_query/<int:query_id>", methods=['POST'])
def done_scraping_car_query(query_id):
    json = request.get_json()
    if json["secret"] != SECRET:
        return "", 404
    print(f"DONE SCRAPING {query_id}")
    return "", 200

@scraper_api.route("/started_scraping_car_query/<int:query_id>", methods=['POST'])
def started_scraping_car_query(query_id):
    json = request.get_json()
    if json["secret"] != SECRET:
        return "", 404
    print(f"STARTED SCRAPING {query_id}")
    return "", 200