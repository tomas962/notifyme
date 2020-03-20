import requests
import json

makes = []
with open("autogidas_makes.txt") as f:
    for line in f:
        makes.append(line.strip())

#response = requests.get("https://en.autogidas.lt/ajax/category/models?category_id=01&make=Audi")

all_models = []
for make in makes:
    response = requests.get("https://en.autogidas.lt/ajax/category/models?category_id=01&make=" + make)
    res_json = response.json()
    if res_json['success']:
        res_json['make'] = make
        all_models.append(res_json)
    else:
        with open("autogidas_model_collect.log", "a") as myfile:
            myfile.write("could't get make models: " + make + "\n")
    
json.dump( all_models, open( "autogidas_models.json", 'w' ) )