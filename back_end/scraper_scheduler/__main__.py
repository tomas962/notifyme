from flask import Flask, request, Response, jsonify
app = Flask(__name__)
import time
from .scraper import ScraperScheduler
import socket

car_scraper_scheduler = ScraperScheduler()

@app.route("/query", methods=['POST'])
def add_query():
    query = request.get_json()
    print("NEW QUERY:")
    print(query)
    car_scraper_scheduler.update_queries(query)
    print("TIME AFTER UPDATE QUERY:")
    print(time.time())
    return jsonify(200)

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    print("WRITING")
    with open("config.py", "w") as f:
        f.write(f"SCRAPER_PORT={port}\n")
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False, )  
    