import requests
import json

makes = []
with open("autobilis_makes.txt") as f:
    for line in f:
        tmp = line.split(',')
        if len(tmp) != 2:
            exit(1)
        tmp1 = {"make_id": tmp[0], "make": tmp[1].strip()}
        makes.append(tmp1)

#response = requests.get("https://en.autogidas.lt/ajax/category/models?category_id=01&make=Audi")

all_models = []
cookies = {
    "__cfduid": "dcbec87ee37dbd70ce4c1fbd027c11d551584725831",
    "searchCookieId": "eyJpdiI6Inc0bFlFa3pQdmZRTFVRcHhnQ0VMekE9PSIsInZhbHVlIjoicVhCMjlQNzdYdXpJVWw5eFRjNWh0MWRsTENJMHRSNGdsaUZoRlVqZ1IxOVlQV29EcVwvaEhObnE1ZmsxMytRYUUiLCJtYWMiOiIxZTc1YTcwNGFlZmIxYzFlNWU5M2QwN2QzODBmZGQ2YTVjMDQ2ZTcxNDU0NWVlYjVkOTQzNjA2OTY0ODkyOTAzIn0%3D",
    "XSRF-TOKEN": "eyJpdiI6InREa3BreElIaVIrckhcLzJRdVg5cmp3PT0iLCJ2YWx1ZSI6IkFjRDdzOVZMQW00OHRoZlZ2cnNUTUd3NmxGSWlnWjVpVGJ2U3lKbmdyXC8wcUhZM296bmNRenhnS1c2QlwvaVk3XC9LNHExN1FCZytyaGdWS1p4N3BVRUV3PT0iLCJtYWMiOiI4NTk2MTkwYjMxMDIwYWNmMDEwMGU0NGExM2ViZDk3MWEzNGM3MjRjZWIwYzllYTVmOWEwOWY1MDg2YTEyMTlmIn0%3D",
    "laravel_session": "eyJpdiI6Ik5oRHF5TjFpKzFNVWM1dGErMERlakE9PSIsInZhbHVlIjoiQWdNWDNwQmUwVEsyWGdNSTk1SExMUkVleFhvYzV6bDYrXC90UUtGNzExWlNobXlXOTJrQnUxc2w0RGR4YlY2Y2YxZWRyTkF6TzBUY0EyejhidG16T1RRPT0iLCJtYWMiOiI5M2EwYmYwOGQ0MmYzODZjZDNjZWMwMTI4NTU5MjlmY2Y3MWM0YmYyMDg1OWVkYzE0ZjM5MDA3ZDAwNWIyNWE1In0%3D"
}

for make in makes:
    response = requests.post(f"https://www.autobilis.lt/type", json={
                             "recursion": "true", "typeId": "2", "id": make['make_id']}, headers={"x-requested-with": "XMLHttpRequest"})

    res_json = response.text
    all_models.append(res_json)

json.dump(all_models, open("autobilis_models.json", 'w'))
