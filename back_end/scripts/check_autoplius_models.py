import sys
sys.path.insert(0,'..')
from database.database import connection
import json

data = json.load(open("autoplius_models.json", "r"))
total = 0
inserted = 0
rows_affected = 0

for models in data:
    with connection.cursor() as cursor:
        for model in models:
            if model['title'] == "-kita-":
                continue
            
            total += 1
            cursor.execute('SELECT * FROM `models` WHERE `autoplius_model_id`=%s', (model['id']))
            make = cursor.fetchone()
            if make is not None:
                inserted += 1
            else:
                print(f"not inserted: {model['id']}, {model['title']}")

            
            # if before == inserted:
            #     inserted += cursor.execute('INSERT INTO `models`(`model_name`, `make_id`, `autoplius_model_id`) VALUES (%s,%s,%s)', (model['title'], make['id'], model['id']))
            # for model in models['data']:
            #     rows_affected += cursor.execute('INSERT INTO `models`(`model_name`, `make_id`) VALUES (%s, %s)', (model['value'], make_id['id']))


print(f"total: {total}")
print(f"inserted: {inserted}")
# connection.commit()