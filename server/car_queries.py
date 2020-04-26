from flask import Blueprint, jsonify, request, Response
import sys
sys.path.insert(0,'..')
from database.database import db_connect
from database.car_query import get_car_queries_by_user_id
query_api = Blueprint('car_queries', __name__)

@query_api.route("/users/<int:user_id>/queries")
def user_query_list(user_id): #TODO filter by user id and car query id
    car_queries = get_car_queries_by_user_id(user_id)
    return jsonify(car_queries)

@query_api.route("/users/<int:user_id>/queries", methods=["POST"])
def post_car_query(user_id):
    json = request.get_json()
    query_values = {}

    print("PRINTING JSON:")
    print(json)
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

    # query_fuel
    query_values["fuel_id"] = json["fuel_id"] if "fuel_id" in json else None

    # query_body_style
    query_values["body_style_id"] = json["body_style_id"] if "body_style_id" in json else None

    # query_make_model
    query_values["make_id"] = json["make_id"] if "make_id" in json else None
    query_values["model_id"] = json["model_id"] if "model_id" in json else None

    query_values["sites"] = ",".join(json["sites"]) if "sites" in json else None

    with db_connect().cursor() as cursor:
        cursor.execute("""INSERT INTO `car_queries`(`price_from`, `price_to`, 
            `year_from`, `search_term`, `year_to`, `power_from`, `power_to`, user_id, sites, city_id) 
            VALUES (%(price_from)s, %(price_to)s, %(year_from)s, %(search_term)s, 
            %(year_to)s, %(power_from)s, %(power_to)s, %(user_id)s, %(sites)s, %(city_id)s)""", query_values)
        
        query_values["query_id"] = cursor.lastrowid

        if query_values["fuel_id"] is not None:
            cursor.execute("""INSERT INTO `query_fuel`(`query_id`, `fuel_id`) 
                VALUES (%(query_id)s, %(fuel_id)s)""", query_values)

        if query_values["body_style_id"] is not None:
            cursor.execute("""INSERT INTO `query_body_style`(`query_id`, `body_style_id`) 
                VALUES (%(query_id)s, %(body_style_id)s)""", query_values)
        
        if query_values["make_id"] is not None:
            cursor.execute("""INSERT INTO `query_make_model`(`query_id`, `make_id`, `model_id`) 
                VALUES (%(query_id)s, %(make_id)s, %(model_id)s)""", query_values)
        cursor.connection.commit()
        cursor.connection.close()

    print(query_values)
    return Response(status=200)