from flask import Blueprint, jsonify, request, Response
message_api = Blueprint('messages', __name__)
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from .jwt_validations import validate_resource
from database.messages import get_all_user_messages

@message_api.route('/users/<int:user_id>/messages', methods=['GET'])
@jwt_required
def get_user_messages(user_id):
    print("messages route")
    if (res := validate_resource(user_id)) != True:
        return res

    messages = get_all_user_messages(user_id)
    return jsonify(messages)