import requests
import json

makes = []
with open("autoplius_makes.txt") as f:
    for line in f:
        tmp = line.split(',')
        if len(tmp) != 2:
            exit(1)
        tmp1 = {"make_id": tmp[0], "make": tmp[1].strip()}
        makes.append(tmp1)

#response = requests.get("https://en.autogidas.lt/ajax/category/models?category_id=01&make=Audi")

all_models = []
for make in makes:
    response = requests.get(f"https://en.autoplius.lt/api/vehicle/models?make_id={make['make_id']}&category_id=2")
    res_json = response.json()
    all_models.append(res_json)
    
json.dump( all_models, open( "autoplius_models.json", 'w' ) )