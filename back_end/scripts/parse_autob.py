import json

data = json.load(open("autobilis_models.json"))

parsed = []
for row in data:
    tmp = json.loads(row)
    parsed.append(tmp)
    
json.dump(parsed, open("autobilis_parsed_models.json", 'w'))