import sys
sys.path.insert(0,'..')
from database.database import connection
import json

data = json.load(open("autobilis_models.json", "r"))
total = 0

formatted_data = []
for row in data:
    tmp = json.loads(row)
    print(tmp)
    if tmp is not None:
        formatted_data.append(tmp)
        total += 1


json.dump(formatted_data, open("tmp.json", 'w'))

print(f"total: {total}")
# connection.commit()