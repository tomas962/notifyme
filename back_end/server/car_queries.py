from flask import Blueprint, jsonify, request, Response
from database.database import db_connect
from database.car_query import (get_car_queries_by_user_id, insert_car_query, update_car_query,
    delete_car_query, get_car_query, get_car_queries_state)
query_api = Blueprint('car_queries', __name__)
import server.scraper_interface as scraper_interface
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from .jwt_validations import validate_resource

@query_api.route("/users/<int:user_id>/queries")
@jwt_required
def user_query_list(user_id):
    car_queries = get_car_queries_by_user_id(user_id)
    return jsonify(car_queries)

@query_api.route("/users/<int:user_id>/queries", methods=["POST"])
@jwt_required
def post_car_query(user_id):
    if res := validate_resource(user_id) != True:
        return res
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

    scraper_interface.update_car_query(query_values)
    return Response(status=200)

@query_api.route("/users/<int:user_id>/queries/<int:query_id>", methods=["PUT"])
@jwt_required
def put_car_query(user_id, query_id):
    jwt = get_jwt_identity()
    query = get_car_query(query_id)
    if query is None:
        if res := validate_resource(user_id) != True:
            return res
    elif query["car_query"]["user_id"] != jwt["user_id"]:
        if jwt["group"] != "admin":
            return jsonify({"error":"You can only access your own resources."}), 403
    
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
            scraper_interface.update_car_query(query_values)
            return Response(status=200)

        else: #insert new
            new_query_id = insert_car_query(cursor, query_values)
            cursor.connection.commit()
            cursor.connection.close()
            scraper_interface.update_car_query(query_values)
            return Response(status=201, headers={'Content-Location':f'/users/{user_id}/queries/{new_query_id}'})


@query_api.route("/users/<int:user_id>/queries/<int:query_id>", methods=["DELETE"])
@jwt_required
def del_query(user_id, query_id):
    jwt = get_jwt_identity()
    query = get_car_query(query_id)
    if query is None:
        return Response(status=404)
    if query["car_query"]["user_id"] != jwt["user_id"]:
        if jwt["group"] != "admin":
            return jsonify({"error":"You can only access your own resources."}), 403

    if delete_car_query(user_id, query_id):
        scraper_interface.delete_car_query(user_id, query_id)
        return Response(status=200)

@query_api.route("/users/<int:user_id>/queries/state")
@jwt_required
def user_car_queries_state(user_id):
    if res := validate_resource(user_id) != True:
        return res
    car_queries = get_car_queries_state(user_id)
    return jsonify(car_queries)