from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def validate_resource(user_id):
    jwt = get_jwt_identity()
    if jwt["user_id"] != user_id:
        if jwt["group"] != "admin":
            return jsonify({"error":"You can only access your own resources."}), 403
    return True