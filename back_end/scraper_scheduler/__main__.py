from flask import Flask, request, Response, jsonify
app = Flask(__name__)
import time
from .scraper import CarScraperScheduler
from.re_scraper import ReScraperScheduler
import socket

# car_scraper_scheduler = CarScraperScheduler()
re_scraper_scheduler = ReScraperScheduler()

@app.route("/queries", methods=['POST'])
def add_query():
    query = request.get_json()
    print("NEW QUERY:")
    print(query)
    car_scraper_scheduler.update_queries(query)
    print("TIME AFTER UPDATE QUERY:")
    print(time.time())
    return jsonify(200)


@app.route("/users/<int:user_id>/queries/<int:query_id>", methods=['DELETE'])
def delete_query(user_id, query_id):
    query = request.get_json()
    print("DELETING QUERY:")
    print(query)
    car_scraper_scheduler.delete_query(query_id)
    print("TIME AFTER DELETE QUERY:")
    print(time.time())
    return Response(status=200)

@app.route("/users/<int:user_id>/queries/<int:query_id>/start", methods=['POST'])
def start_scraping_car_query(user_id, query_id):
    print(f"Got request to start scraping {query_id}")
    if car_scraper_scheduler.start_scraping(query_id):
        return "", 200
    else:
        return "", 404


@app.route("/users/<int:user_id>/re_queries/<int:query_id>", methods=['DELETE'])
def delete_re_query(user_id, query_id):
    query = request.get_json()
    print("DELETING RE QUERY:")
    print(query)
    re_scraper_scheduler.delete_query(query_id)
    print("TIME AFTER DELETE RE QUERY:")
    print(time.time())
    return Response(status=200)

@app.route("/re_queries", methods=['POST'])
def add_re_query():
    query = request.get_json()
    print("NEW RE QUERY:")
    print(query)
    re_scraper_scheduler.update_queries(query)
    print("TIME AFTER UPDATE QUERY:")
    print(time.time())
    return jsonify(200)

@app.route("/users/<int:user_id>/re_queries/<int:query_id>/start", methods=['POST'])
def start_scraping_re_query(user_id, query_id):
    print(f"Got request to start scraping re query: {query_id}")
    if re_scraper_scheduler.start_scraping(query_id):
        return "", 200
    else:
        return "", 404

if __name__ == "__main__":
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind(('localhost', 0))
    port = 40375 #sock.getsockname()[1]
    # sock.close()
    # print("WRITING")
    # with open("config.py", "w") as f:
    #     f.write(f"SCRAPER_PORT={port}\n")
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False, )  
    