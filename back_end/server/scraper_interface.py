import requests
from config import SCRAPER_PORT
import time

def update_car_query(query):
    print("QUERY BEFORE QUERY UPDATE:")
    print(query)
    print("TIME BEFORE QUERY UPDATE:")
    print(time.time())
    requests.post('http://127.0.0.1:'+str(SCRAPER_PORT)+'/queries', json=query)

def delete_car_query(user_id, query_id):
    print("TIME BEFORE QUERY DELETE:")
    print(time.time())
    requests.delete(f'http://127.0.0.1:{SCRAPER_PORT}/users/{user_id}/queries/{query_id}')

def start_query(user_id, query_id):
    res = requests.post(f'http://127.0.0.1:{SCRAPER_PORT}/users/{user_id}/queries/{query_id}/start')
    return res.status_code