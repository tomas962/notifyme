from flask import Blueprint, jsonify
import sys
sys.path.insert(0,'..')
from database.database import db_connect
cars_api = Blueprint('cars', __name__)

@cars_api.route("/cars")
def car_list(): #TODO filter by user id and car query id
    conn = db_connect()
    car_ads = None
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM car_ads")
        car_ads = cursor.fetchall()
    conn.close()
    return jsonify(car_ads)