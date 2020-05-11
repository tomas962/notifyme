from flask import Blueprint, jsonify, request, Response
re_query_api = Blueprint('re_queries', __name__)
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from .jwt_validations import validate_resource
from database.re_queries import get_re_cities, get_re_categories, get_re_types

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