from flask import Blueprint, jsonify, request, Response
from database.database import db_connect
from database.car_query import get_car_queries_by_user_id, insert_car_query, update_car_query
query_api = Blueprint('car_queries', __name__)
from .car_scraper import car_scraper

@query_api.route("/users/<int:user_id>/queries")
def user_query_list(user_id): #TODO filter by user id and car query id
    car_queries = get_car_queries_by_user_id(user_id)
    return jsonify(car_queries)

@query_api.route("/users/<int:user_id>/queries", methods=["POST"])
def post_car_query(user_id):
    json = request.get_json()
    query_values = {}

    # car_queries
    query_values["price_from"] = json["price_from"] if "price_from" in json else None
    query_values["price_to"] = json["price_to"] if "price_to" in json else None
    query_values["year_from"] = json["year_from"] if "year_from" in json else None
    query_values["search_term"] = json["search_term"] if "search_term" in json else None
    query_values["year_to"] = json["year_to"] if "year_to" in json else None
    query_values["power_from"] = json["power_from"] if "power_from" in json else None
    query_values["power_to"] = json["power_to"] if "power_to" in json else None
    query_values["city_id"] = json["city_id"] if "city_id" in json else None
    query_values["user_id"] = user_id
    query_values["was_scraped"] = 0

    # query_fuel
    query_values["fuel_id"] = json["fuel_id"] if "fuel_id" in json else None

    # query_body_style
    query_values["body_style_id"] = json["body_style_id"] if "body_style_id" in json else None

    # query_make_model
    query_values["make_id"] = json["make_id"] if "make_id" in json else None
    query_values["model_id"] = json["model_id"] if "model_id" in json else None

    query_values["sites"] = ",".join(json["sites"]) if "sites" in json else None

    with db_connect().cursor() as cursor:
        insert_car_query(cursor, query_values)
        cursor.connection.commit()
        cursor.connection.close()

    car_scraper.update_queries(query_values)
    return Response(status=200)

@query_api.route("/users/<int:user_id>/queries/<int:query_id>", methods=["PUT"])
def put_car_query(user_id, query_id):
    json = request.get_json()
    query_values = {}
    
    # car_queries
    query_values["price_from"] = json["price_from"] if "price_from" in json else None
    query_values["price_to"] = json["price_to"] if "price_to" in json else None
    query_values["year_from"] = json["year_from"] if "year_from" in json else None
    query_values["search_term"] = json["search_term"] if "search_term" in json else None
    query_values["year_to"] = json["year_to"] if "year_to" in json else None
    query_values["power_from"] = json["power_from"] if "power_from" in json else None
    query_values["power_to"] = json["power_to"] if "power_to" in json else None
    query_values["city_id"] = json["city_id"] if "city_id" in json else None
    query_values["user_id"] = user_id
    query_values["id"] = query_id
    query_values["was_scraped"] = 0

    # query_fuel
    query_values["fuel_id"] = json["fuel_id"] if "fuel_id" in json else None

    # query_body_style
    query_values["body_style_id"] = json["body_style_id"] if "body_style_id" in json else None

    # query_make_model
    query_values["make_id"] = json["make_id"] if "make_id" in json else None
    query_values["model_id"] = json["model_id"] if "model_id" in json else None

    query_values["sites"] = ",".join(json["sites"]) if "sites" in json else None

    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM car_queries WHERE user_id=%(user_id)s AND id=%(id)s", query_values)
        if cursor.fetchone(): #update existing
            update_car_query(cursor, query_values)
            cursor.connection.commit()
            cursor.connection.close()
            car_scraper.update_queries(query_values)
            return Response(status=200)

        else: #insert new
            new_query_id = insert_car_query(cursor, query_values)
            cursor.connection.commit()
            cursor.connection.close()
            car_scraper.update_queries(query_values)
            return Response(status=201, headers={'Content-Location':f'/users/{user_id}/queries/{new_query_id}'})
