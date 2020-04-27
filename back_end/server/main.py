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

# @app.after_request
# def after_request_h(response: Response):
#     print(request)
#     print(response.headers)
#     return response

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

