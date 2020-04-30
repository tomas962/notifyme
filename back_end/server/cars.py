from flask import Blueprint, jsonify
from ..database.database import db_connect
from ..database.car import get_cars_by_query_id
cars_api = Blueprint('cars', __name__)

@cars_api.route("/cars")
def car_list():
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

@cars_api.route("/queries/<int:query_id>/cars")
def query_car_list(query_id):
    car_ads = get_cars_by_query_id(query_id)
    return jsonify(car_ads)

@cars_api.route("/makes")
def get_makes():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM makes")
        makes = cursor.fetchall()
        cursor.connection.close()
        return jsonify(makes)

@cars_api.route("/makes/<int:make_id>/models")
def get_models(make_id):
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM models WHERE make_id=%s", make_id)
        models = cursor.fetchall()
        cursor.connection.close()
        return jsonify(models)

@cars_api.route("/body_styles")
def get_body_styles():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM body_styles")
        body_styles = cursor.fetchall()
        cursor.connection.close()
        return jsonify(body_styles)

@cars_api.route("/fuel_types")
def get_fuel_types():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM fuel_types")
        fuel_types = cursor.fetchall()
        cursor.connection.close()
        return jsonify(fuel_types)

@cars_api.route("/cities")
def get_cities():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM cities")
        cities = cursor.fetchall()
        cursor.connection.close()
        return jsonify(cities)