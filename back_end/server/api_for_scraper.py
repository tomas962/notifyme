from flask import Blueprint, jsonify, request, Response
from config import SECRET
from .socketio_api import auth_users, socketio
import time
scraper_api = Blueprint('scraper_api', __name__)
#TODO one user connected with multiple devices
@scraper_api.route("/done_scraping_car_query/<int:user_id>/<int:query_id>", methods=['POST'])
def done_scraping_car_query(user_id, query_id):
    json = request.get_json()
    if json["secret"] != SECRET:
        return "", 404
    print(f"DONE SCRAPING {query_id}")
    if user_id in auth_users and auth_users[user_id]['expires'] > time.time():
        print("emitting to socket car_query_ended")
        print("socket_id:")
        print(auth_users[user_id]['sid'])
        socketio.emit('car_query_ended', {'user_id':user_id, 'query_id':query_id}, room=auth_users[user_id]['sid'])
    return "", 200

@scraper_api.route("/started_scraping_car_query/<int:user_id>/<int:query_id>", methods=['POST'])
def started_scraping_car_query(user_id, query_id):
    json = request.get_json()
    if json["secret"] != SECRET:
        return "", 404
    print(f"STARTED SCRAPING {query_id}")
    if user_id in auth_users and auth_users[user_id]['expires'] > time.time():
        print("emitting to socket car_query_started")
        print("socket_id:")
        print(auth_users[user_id]['sid'])
        socketio.emit('car_query_started', {'user_id':user_id, 'query_id':query_id}, room=auth_users[user_id]['sid'])
    return "", 200



# RE QUERIES ###################
@scraper_api.route("/done_scraping_re_query/<int:user_id>/<int:query_id>", methods=['POST'])
def done_scraping_re_query(user_id, query_id):
    json = request.get_json()
    if json["secret"] != SECRET:
        return "", 404
    print(f"DONE SCRAPING RE {query_id}")
    if user_id in auth_users and auth_users[user_id]['expires'] > time.time():
        print("emitting to socket re_query_ended")
        print("socket_id:")
        print(auth_users[user_id]['sid'])
        socketio.emit('re_query_ended', {'user_id':user_id, 'query_id':query_id}, room=auth_users[user_id]['sid'])
    return "", 200


@scraper_api.route("/started_scraping_re_query/<int:user_id>/<int:query_id>", methods=['POST'])
def started_scraping_re_query(user_id, query_id):
    json = request.get_json()
    if json["secret"] != SECRET:
        return "", 404
    print(f"STARTED SCRAPING RE {query_id}")
    if user_id in auth_users and auth_users[user_id]['expires'] > time.time():
        print("emitting to socket re_query_started")
        print("socket_id:")
        print(auth_users[user_id]['sid'])
        socketio.emit('re_query_started', {'user_id':user_id, 'query_id':query_id}, room=auth_users[user_id]['sid'])
    return "", 200