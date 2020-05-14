from flask import Blueprint, jsonify, request, Response
re_query_api = Blueprint('re_queries', __name__)
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from .jwt_validations import validate_resource
from database.re_queries import (get_re_cities, get_re_categories, get_re_types, get_re_house_types,
    insert_re_query, get_user_re_queries, get_re_query, delete_re_query, get_query_re_ads, 
    get_re_ad, update_re_query)
from database.database import db_connect
import server.scraper_interface as scraper_interface

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
    new_query_id = insert_re_query(query)
    values["id"] = new_query_id
    scraper_interface.update_re_query(query)
    return "", 200

@re_query_api.route('/users/<int:user_id>/re_queries/<int:query_id>', methods=['PUT'])
@jwt_required
def put_query(user_id, query_id):
    jwt = get_jwt_identity()
    query = get_re_query(query_id)
    if query is None:
        if res := validate_resource(user_id) != True:
            return res
    elif query["user_id"] != jwt["user_id"]:
        if jwt["group"] != "admin":
            return jsonify({"error":"You can only access your own resources."}), 403
    
    values = request.get_json()
    values["user_id"] = user_id
    values["id"] = query_id
    values["sites"] = ",".join(values["sites"])


    if query: #PUT
        update_re_query(values)
        scraper_interface.update_re_query(values)
        return Response(status=200)
    else:
        new_query_id = insert_re_query(values)
        values["id"] = new_query_id
        scraper_interface.update_re_query(values)
        return Response(status=201, headers={'Content-Location':f'/users/{user_id}/re_queries/{new_query_id}'})
    return "", 200


@re_query_api.route('/users/<int:user_id>/re_queries', methods=['GET'])
@jwt_required
def get_queries(user_id):
    if res := validate_resource(user_id) != True:
        return res
    
    queries = get_user_re_queries(user_id)
    return jsonify(queries)

@re_query_api.route("/users/<int:user_id>/re_queries/<int:query_id>", methods=["DELETE"])
@jwt_required
def del_re_query(user_id, query_id):
    jwt = get_jwt_identity()
    query = get_re_query(query_id)
    if query is None:
        return Response(status=404)
    if query["user_id"] != jwt["user_id"]:
        if jwt["group"] != "admin":
            return jsonify({"error":"You can only access your own resources."}), 403

    if delete_re_query(user_id, query_id):
        scraper_interface.delete_re_query(user_id, query_id)
        return Response(status=200)

@re_query_api.route("/users/<int:user_id>/re_queries/<int:query_id>/re_ads", methods=["GET"])
@jwt_required
def re_ad_list(user_id, query_id):
    if res := validate_resource(user_id) != True:
        return res

    with db_connect().cursor() as cursor:
        cursor.execute("SELECT id FROM re_queries WHERE user_id=%s AND id=%s", (user_id, query_id))
        if not cursor.fetchone():
            return "", 404
    
    ads = get_query_re_ads(query_id)
    return jsonify(ads)

@re_query_api.route("/users/<int:user_id>/re_queries/<int:query_id>/re_ads/<int:re_ad_id>", methods=["GET"])
@jwt_required
def re_ad(user_id, query_id, re_ad_id):
    if res := validate_resource(user_id) != True:
        return res

    with db_connect().cursor() as cursor:
        cursor.execute("SELECT id FROM re_queries WHERE user_id=%s AND id=%s", (user_id, query_id))
        if not cursor.fetchone():
            return "", 404

    re_ad = get_re_ad(re_ad_id)
    if re_ad:
        return jsonify(re_ad)
    else:
        return "", 404

@re_query_api.route("/users/<int:user_id>/re_queries/<int:query_id>/start", methods=['POST'])
@jwt_required
def start_scraping_car_query(user_id, query_id):
    user = get_jwt_identity()
    if user["group"] != "admin":
        return jsonify({"error":"Only admin can access this endpoint"}), 403

    status_code = scraper_interface.start_re_query(user_id, query_id)
    return "", status_code
