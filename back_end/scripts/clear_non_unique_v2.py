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
    cursor.execute('SELECT COUNT(*) AS `Rows`, `model_name` FROM `models` GROUP BY `model_name` ORDER BY `model_name`')
    models = cursor.fetchall()
    for model in models:
        if model['Rows'] > 1 and len(model['model_name']) >= 1:
            duplicate += 1
            cursor.execute('SELECT * FROM models WHERE model_name=%s', (model['model_name']))
            dup_models = cursor.fetchall()
            curr_model = dup_models[0]
            for dup_model in dup_models[1:]:
                if curr_model['autoplius_model_id'] == dup_model['autoplius_model_id'] and curr_model['make_id'] == dup_model['make_id']:
                    print(dup_model)
                    deleted += cursor.execute('DELETE FROM models WHERE id=%s', (dup_model['id']))
                    break

print("DELETED ROWS: ")
print(deleted_rows)

print(f"duplicate: {duplicate}")
print(f"deleted: {deleted}")
print(f"{first_match}")
print(f"{second_match}")
# connection.commit()

connection.close()