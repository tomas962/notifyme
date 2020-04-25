from flask import Flask, request, Response, jsonify
import sys
sys.path.insert(0,'..')
from database.database import connection
app = Flask(__name__)

from .cars import cars_api
from .auth import auth
from .car_queries import query_api
app.register_blueprint(cars_api)
app.register_blueprint(auth)
app.register_blueprint(query_api)

from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token, jwt_refresh_token_required
)


app.debug = True
CORS(app, support_credentials=True)

@app.route("/")
def hello():
    result = 'empty'
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `makes` where `id`=%s"
        cursor.execute(sql, ("6"))
        result = cursor.fetchall()
    return jsonify(result)

@app.route("/cars", methods=["POST"])
def add_car():
    return Response(200)

@app.route("/car_queries", methods=["POST"])
def post_car_query():
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

    # query_fuel
    query_values["fuel_id"] = json["fuel_id"] if "fuel_id" in json else None

    # query_body_style
    query_values["body_style_id"] = json["body_style_id"] if "body_style_id" in json else None

    # query_make_model
    query_values["make_id"] = json["make_id"] if "make_id" in json else None
    query_values["model_id"] = json["model_id"] if "model_id" in json else None


    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO `car_queries`(`price_from`, `price_to`, 
            `year_from`, `search_term`, `year_to`, `power_from`, `power_to`) 
            VALUES (%(price_from)s, %(price_to)s, %(year_from)s, %(search_term)s, 
            %(year_to)s, %(power_from)s, %(power_to)s)""", query_values)
        
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

    connection.commit()
    return Response(200)