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
        cursor.execute("""SELECT *, makes.make as make_name, models.model_name as model_name,
            body_styles.name as body_type_name, fuel_types.fuel_name as fuel_name
            FROM car_ads 
            JOIN makes ON car_ads.make=makes.id
            JOIN models ON car_ads.model=models.id
            JOIN body_styles ON car_ads.body_type=body_styles.id
            JOIN fuel_types ON car_ads.fuel_type=fuel_types.id""")
        car_ads = cursor.fetchall()
    conn.close()
    return jsonify(car_ads)