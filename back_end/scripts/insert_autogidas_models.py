import sys
sys.path.insert(0,'..')
from database.database import connection
import json

data = json.load(open("autogidas_models.json", "r"))
rows_affected = 0

for models in data:
    with connection.cursor() as cursor:
        cursor.execute('SELECT id FROM `makes` WHERE `make`=%s', (models['make']))
        make_id = cursor.fetchone()
        if make_id is None:
            print(f"error: {models['make']} ID not found")
        for model in models['data']:
            rows_affected += cursor.execute('INSERT INTO `models`(`model_name`, `make_id`) VALUES (%s, %s)', (model['value'], make_id['id']))

print("rows affected: " + str(rows_affected))

connection.commit()