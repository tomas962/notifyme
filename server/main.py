from flask import Flask, request, Response, jsonify
import sys
sys.path.insert(0,'..')
from database.database import connection

app = Flask(__name__)



@app.route("/")
def hello():
    result = 'empty'
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `makes` where `car_id`=%s"
        cursor.execute(sql, ("6"))
        result = cursor.fetchall()
    return jsonify(result)

@app.route("/cars", methods=["POST"])
def add_car():
    return Response(200)
