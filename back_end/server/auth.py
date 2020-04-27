from flask import Blueprint, jsonify, request
from .main import app
import sys
sys.path.insert(0,'..')
from database.database import db_connect
from datetime import datetime, timedelta
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token, jwt_refresh_token_required
)

auth = Blueprint('auth', __name__)

app.config['JWT_SECRET_KEY'] = 'dsafn87987345 3Q#$GRWE#$()_)*%@&#()nvdkJS*#@QW$%&BHDFSudsfkj'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
jwt = JWTManager(app)

@app.route('/auth', methods=['POST'])
def login():
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