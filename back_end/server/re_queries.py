from flask import Blueprint, jsonify, request, Response
re_query_api = Blueprint('re_queries', __name__)
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from .jwt_validations import validate_resource
from database.re_queries import (get_re_cities, get_re_categories, get_re_types, get_re_house_types,
    insert_re_query)

@re_query_api.route('/re_cities', methods=['GET'])
@jwt_required
def get_all_re_cities():
    cities = get_re_cities()
    return jsonify(cities)

@re_query_api.route('/re_categories', methods=['GET'])
@jwt_required
def get_all_re_categories():
    categories = get_re_categories()
    return jsonify(categories)

@re_query_api.route('/re_types', methods=['GET'])
@jwt_required
def get_all_re_types():
    re_types = get_re_types()
    return jsonify(re_types)

@re_query_api.route('/re_house_types', methods=['GET'])
@jwt_required
def get_all_house_re_types():
    re_house_types = get_re_house_types()
    return jsonify(re_house_types)


@re_query_api.route('/users/<int:user_id>/re_queries', methods=['POST'])
@jwt_required
def post_query(user_id):
    if res := validate_resource(user_id) != True:
        return res
    
    query = request.get_json()
    query["user_id"] = user_id
    query["sites"] = ",".join(query["sites"])
    print(query)
    insert_re_query(query)
    return "", 200