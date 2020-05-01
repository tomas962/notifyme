from flask import Flask, request, Response, jsonify
import sys
from database.database import connection, db_connect
app = Flask(__name__)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token, jwt_refresh_token_required
)
from datetime import datetime, timedelta
app.config['JWT_SECRET_KEY'] = 'dsafn87987345 3Q#$GRWE#$()_)*%@&#()nvdkJS*#@QW$%&BHDFSudsfkj'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
jwt = JWTManager(app)


import os
print(os.getpid())
from .cars import cars_api
from .car_queries import query_api
app.register_blueprint(cars_api)
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


@app.route('/auth', methods=['POST'])
def login_auth():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"error": "Missing email parameter"}), 400
    if not password:
        return jsonify({"error": "Missing password parameter"}), 400

    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email=%s", email)
        user = cursor.fetchone()
        print(user)
        if user is None:
            cursor.connection.close()
            return jsonify({"error": "Bad email or password"}), 401

        if user["password"] == password:
            access_token = create_access_token(identity={"user_id":user["id"], "group":user["user_group"], "email":user["email"]})
            refresh_token = create_refresh_token(identity={"user_id":user["id"], "group":user["user_group"], "email":user["email"]})
            cursor.connection.close()
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({"error": "Bad email or password"}), 401
    
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)  

