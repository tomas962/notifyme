from flask import Blueprint, jsonify
import sys
sys.path.insert(0,'..')
from database.database import db_connect
from database.car_query import get_car_queries_by_user_id
query_api = Blueprint('car_queries', __name__)

@query_api.route("/users/<int:user_id>/queries")
def user_query_list(user_id): #TODO filter by user id and car query id
    car_queries = get_car_queries_by_user_id(user_id)
    return jsonify(car_queries)