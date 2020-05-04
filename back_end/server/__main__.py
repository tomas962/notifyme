from flask import Flask, request, Response, jsonify
import sys
import bcrypt
from database.database import connection, db_connect
app = Flask(__name__)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token, jwt_refresh_token_required, fresh_jwt_required
)
from datetime import datetime, timedelta
app.config['JWT_SECRET_KEY'] = 'dsafn87987345 3Q#$GRWE#$()_)*%@&#()nvdkJS*#@QW$%&BHDFSudsfkj'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
jwt = JWTManager(app)


import os
print(os.getpid())
from .cars import cars_api
from .car_queries import query_api
app.register_blueprint(cars_api)
app.register_blueprint(query_api)

from flask_cors import CORS
app.debug = True
CORS(app, support_credentials=True)

# @app.after_request
# def after_request_h(response: Response):
#     print(request)
#     print(response.headers)
#     return response

@app.route("/")
@fresh_jwt_required
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

        
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user["password"], 'utf-8')):
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


@app.route('/register', methods=['POST'])
def register_user():
    userjson = request.get_json()
    if "email" not in userjson or userjson["email"] is None:
        return jsonify({"error":"email error"}), 400

    em = userjson["email"].split('@')
    if " " in userjson["email"] or len(em) <= 1 or em[0] == userjson["email"] or len(em[1]) == 0:
        return jsonify({"error":"Invalid email. Email can not contain spaces and must contain one '@'."}), 400
        

    if "password" not in userjson or \
    "confirm_password" not in userjson or \
    userjson["password"] is None or \
    userjson["confirm_password"] is None or \
    userjson["password"] != userjson["confirm_password"] or \
    len(userjson["password"]) == 0:
        return jsonify({"error":"password error"}), 400

    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email=%s", userjson["email"])
        if cursor.fetchone():
            cursor.connection.close()
            return jsonify({"error":"Account with this email already registered."}), 409

        hashed_pw = bcrypt.hashpw(bytes(userjson["password"], 'utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO `users`(`email`, `password`, `user_group`) VALUES (%s, %s, %s)", (userjson["email"], hashed_pw, 'regular'))
        cursor.connection.commit()
        cursor.connection.close()
        return Response(status=200)

print("__name__")
print(__name__)
if __name__ == "__main__":
    print("RAN ONCE")
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)  

