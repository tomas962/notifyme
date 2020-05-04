import requests
from config import SCRAPER_PORT
import time

def update_query(query):
    print("QUERY BEFORE QUERY UPDATE:")
    print(query)
    print("TIME BEFORE QUERY UPDATE:")
    print(time.time())
    requests.post('http://127.0.0.1:'+str(SCRAPER_PORT)+'/query', json=query)