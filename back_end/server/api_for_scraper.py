from flask import Blueprint, jsonify, request, Response
scraper_api = Blueprint('car_queries', __name__)

@scraper_api.route("/done_scraping_car_query/<int:query_id>")
def done_scraping_car_query(query_id):
    print(f"DONE SCRAPING {query_id}")
    return "", 200

@scraper_api.route("/started_scraping_car_query/<int:query_id>")
def started_scraping_car_query(query_id):
    print(f"STARTED SCRAPING {query_id}")
    return "", 200