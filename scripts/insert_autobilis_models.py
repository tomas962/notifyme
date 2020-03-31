import sys
sys.path.insert(0,'..')
from database.database import connection
import json

data = json.load(open("autobilis_models_parsed.json", "r"))
total = 0
inserted = 0

with connection.cursor() as cursor:
    for models in data:
        if len(models) > 0:
            cursor.execute('SELECT * FROM `makes` WHERE `autobilis_make_id`=%s', (models[0]['parent_id']))
            make = cursor.fetchone()
            for model in models:
                if model['title'] != '-kiti-':
                    total += 1
                    before = inserted
                    inserted += cursor.execute('UPDATE `models` SET `autobilis_model_id`=%s WHERE `make_id`=%s AND `model_name`=%s', (model['id'], make['id'], model['title']))
                    if before == inserted:
                        inserted += cursor.execute('INSERT INTO `models`(`model_name`, `make_id`, `autobilis_model_id`) VALUES (%s,%s,%s)', (model['title'], make['id'], model['id']))



print(f"total: {total}")
print(f"inserted: {inserted}")
# connection.commit()

connection.close()