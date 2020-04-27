import sys
sys.path.insert(0,'..')
from database.database import connection
import json
deleted_rows = []
deleted = 0
duplicate = 0

first_match = False
second_match = False
dummy_id = -1
with connection.cursor() as cursor:
    cursor.execute('SELECT * FROM models')
    models = cursor.fetchall()
    for model in models:
        for othmodel in models:
            if model['id'] != othmodel['id'] and model['make_id'] == othmodel['make_id'] and model['model_name'] == othmodel['model_name']:
                print()
                print(model)
                print(othmodel)
                deleted += cursor.execute('DELETE from models where id=%s', (model['id']))
                deleted_rows.append(model)
                if model['id'] == 12928:
                    first_match = True
                if model['id'] == 8890:
                    second_match = True
                othmodel['id'] = dummy_id
                dummy_id -= 1
                
                duplicate += 1

print("DELETED ROWS: ")
print(deleted_rows)

print(f"duplicate: {duplicate}")
print(f"deleted: {deleted}")
print(f"{first_match}")
print(f"{second_match}")
# connection.commit()

connection.close()