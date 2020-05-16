from flask import Flask, request, Response, jsonify
import sys
import bcrypt
import pymysql
from database.database import connection, db_connect
from .init_apps import app, socketio
import server.socketio_api
import server.messages
import server.re_queries
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token, jwt_refresh_token_required, fresh_jwt_required,
    decode_token
)
from datetime import datetime, timedelta
from .jwt_validations import validate_resource
app.config['JWT_SECRET_KEY'] = 'dsafn87987345 3Q#$GRWE#$()_)*%@&#()nvdkJS*#@QW$%&BHDFSudsfkj'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
#app.config['SECRET_KEY'] = 'secret!'

jwt = JWTManager(app)

print("after socketio")

import os
print(os.getpid())
from .cars import cars_api
from .car_queries import query_api
from .api_for_scraper import scraper_api 
from .messages import message_api 
app.register_blueprint(cars_api)
app.register_blueprint(query_api)
app.register_blueprint(scraper_api)
app.register_blueprint(message_api)
app.register_blueprint(server.re_queries.re_query_api)

from flask_cors import CORS
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
            #return jsonify(access_token=access_token, refresh_token=refresh_token), 200
            return jsonify(access_token=access_token), 200

    return jsonify({"error": "Bad email or password"}), 401
    
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    return "", 404
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

@app.route('/changepw', methods=['POST'])
@jwt_required
def change_password():
    json = request.get_json()

    if not json or "old_password" not in json or "new_password" not in json or "confirm_password" not in json \
        or json["old_password"] == "" or json["new_password"] == "" or json["confirm_password"] == "":
        return jsonify({"error":"Incorrect request json"}),400

    if json["new_password"] != json["confirm_password"]:
        return jsonify({'error':'Passwords do not match.'}), 400

    user_ident = get_jwt_identity()
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", user_ident["user_id"])
        user = cursor.fetchone()
        if user is None:
            cursor.connection.close()
            return Response(status=404)
        
        if not bcrypt.checkpw(bytes(json["old_password"], 'utf-8'), bytes(user["password"], 'utf-8')):
            cursor.connection.close()
            return jsonify({'error':'Incorrect password'}), 403

        pw_hash = bcrypt.hashpw(bytes(json["new_password"], 'utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (pw_hash, user_ident["user_id"]))
        cursor.connection.commit()
        cursor.connection.close()
        return "", 200

@app.route('/users/<int:user_id>/settings', methods=['GET'])
@jwt_required
def user_settings(user_id):
    if res := validate_resource(user_id) != True:
        return res

    with db_connect().cursor() as cursor:
        cursor.execute("SELECT email_notifications FROM users WHERE id=%s", user_id)
        settings = cursor.fetchone()
        return jsonify(settings)

@app.route('/users/<int:user_id>/settings', methods=['POST'])
@jwt_required
def update_user_settings(user_id):
    if res := validate_resource(user_id) != True:
        return res

    settings = request.get_json()

    if not settings or "email_notifications" not in settings:
        return "", 403

    with db_connect().cursor() as cursor:
        cursor.execute("UPDATE users SET email_notifications=%s WHERE id=%s", (settings["email_notifications"], user_id))
        cursor.connection.commit()
        cursor.connection.close()
        return "", 200

@app.route('/users/<int:user_id>/push_auth', methods=['POST'])
@jwt_required
def push_auth_post(user_id):
    if res := validate_resource(user_id) != True:
        return res
    
    data = request.get_json()
    with db_connect().cursor() as cursor:
        try:
            cursor.execute("INSERT INTO `push_notification_auth`(`user_id`, `auth_json`) VALUES (%s, %s)", (user_id, data["auth_json"]))
        except pymysql.IntegrityError as err:
            print("This push auth token already exists")
            print(err)
        cursor.connection.commit()
        cursor.connection.close()
        return "", 200

print("__name__")
print(__name__)
if __name__ == "__main__":
    print("RAN ONCE")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)  