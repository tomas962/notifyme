from flask import Blueprint, jsonify, request, Response
from ..database.database import db_connect
from ..database.car_query import get_car_queries_by_user_id, insert_car_query
from .main import car_scraper
query_api = Blueprint('car_queries', __name__)

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
    query_values["query_id"] = query_id

    # query_fuel
    query_values["fuel_id"] = json["fuel_id"] if "fuel_id" in json else None

    # query_body_style
    query_values["body_style_id"] = json["body_style_id"] if "body_style_id" in json else None

    # query_make_model
    query_values["make_id"] = json["make_id"] if "make_id" in json else None
    query_values["model_id"] = json["model_id"] if "model_id" in json else None

    query_values["sites"] = ",".join(json["sites"]) if "sites" in json else None

    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM car_queries WHERE user_id=%(user_id)s AND id=%(query_id)s", query_values)
        if cursor.fetchone(): #update existing
            cursor.execute("""UPDATE `car_queries` SET price_from=%(price_from)s, price_to=%(price_to)s, 
                year_from=%(year_from)s, search_term=%(search_term)s, 
                year_to=%(year_to)s, power_from=%(power_from)s, power_to=%(power_to)s, 
                user_id=%(user_id)s, sites=%(sites)s, city_id=%(city_id)s WHERE id=%(query_id)s AND user_id=%(user_id)s""", query_values)
        
            if query_values["fuel_id"] is not None:
                cursor.execute("SELECT * FROM query_fuel WHERE query_id=%(query_id)s", query_values)
                if cursor.fetchone():
                    cursor.execute("""UPDATE `query_fuel` SET fuel_id=%(fuel_id)s WHERE query_id=%(query_id)s""", query_values)
                else:
                    cursor.execute("""INSERT INTO `query_fuel`(`query_id`, `fuel_id`) 
                        VALUES (%(query_id)s, %(fuel_id)s)""", query_values)

            if query_values["body_style_id"] is not None:
                cursor.execute("SELECT * FROM query_body_style WHERE query_id=%(query_id)s", query_values)
                if cursor.fetchone():
                    cursor.execute("""UPDATE `query_body_style` SET
                        body_style_id=%(body_style_id)s WHERE query_id=%(query_id)s""", query_values)
                else:
                    cursor.execute("""INSERT INTO `query_body_style`(`query_id`, `body_style_id`) 
                        VALUES (%(query_id)s, %(body_style_id)s)""", query_values)
        
            if query_values["make_id"] is not None:
                cursor.execute("SELECT * FROM query_make_model WHERE query_id=%(query_id)s", query_values)
                if cursor.fetchone():
                    cursor.execute("""UPDATE `query_make_model` SET
                        make_id=%(make_id)s, model_id=%(model_id)s WHERE query_id=%(query_id)s""", query_values)
                else:
                    cursor.execute("""INSERT INTO `query_make_model`(`query_id`, `make_id`, `model_id`) 
                        VALUES (%(query_id)s, %(make_id)s, %(model_id)s)""", query_values)
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
