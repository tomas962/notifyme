import scrapy
import sys
from urllib.parse import urlencode
from scrape_utils import *
sys.path.insert(0,"..")
from database.database import db_connect
from .ads import CarAd, AutopliusAd
from database.car_query import get_car_query

def form_autop_query(params):
    new_params = {}
    if "make_model" in params and params["make_model"] is not None and "autoplius_make_id" in params["make_model"]:
        new_params["make_id_list"] = params["make_model"]["autoplius_make_id"] or ""
    if "make_model" in params and params["make_model"] and "autoplius_model_id" in params["make_model"]:
        new_params[f"make_id[{new_params['make_id_list']}]"] = params["make_model"]["autoplius_model_id"] or ""

    if "car_query" in params and params["car_query"] is not None:
        if "price_from" in params["car_query"]:
            new_params["sell_price_from"] = params["car_query"]["price_from"] if params["car_query"]["price_from"] is not None else ""
        if "price_to" in params["car_query"]:
            new_params["sell_price_to"] = params["car_query"]["price_to"] if params["car_query"]["price_to"] is not None else ""

        if "year_from" in params["car_query"]:
            new_params["make_date_from"] = params["car_query"]["year_from"] if params["car_query"]["year_from"] is not None else ""
        if "year_to" in params["car_query"]:
            new_params["make_date_to"] = params["car_query"]["year_to"] if params["car_query"]["year_to"] is not None else ""
        if "search_term" in params["car_query"] and params["car_query"]["search_term"] is not None:
            new_params["qt"] = params["car_query"]["search_term"] if params["car_query"]["search_term"] is not None else ""

    if "body_style" in params and params["body_style"] is not None and "autoplius_id" in params["body_style"]:
        new_params["body_type_id"] = params["body_style"]["autoplius_id"] if params["body_style"]["autoplius_id"] is not None else ""
        
    if "fuel_type" in params and params["fuel_type"] is not None and "autoplius_fuel_id" in params["fuel_type"]:
        new_params["fuel_id"] = params["fuel_type"]["autoplius_fuel_id"] if params["fuel_type"]["autoplius_fuel_id"] is not None else ""
    
    return new_params
    
class AutopliusSpider(scrapy.Spider):
    name = "autoplius"
    
    def __init__(self, car_query_id=None, **kwargs):
        self.car_query_id = car_query_id
        super().__init__(**kwargs)  

    def start_requests(self):
        self.i = 0

        if self.car_query_id is None:
            return
        car_query = get_car_query(int(self.car_query_id))
        assert car_query is not None, "Car query not found!"
        urls = ["https://autoplius.lt/skelbimai/naudoti-automobiliai?" + urlencode(form_autop_query(car_query))]

        
        for url in urls:
            rq = scrapy.Request(url=url, callback=self.parse, headers={"user-agent": 
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
            yield rq

    def parse(self, response):
        hrefs = response.css('a.announcement-item::attr(href)').getall()
        
        for href in hrefs:
            next_page = response.urljoin(href)
            yield scrapy.Request(href, callback=self.parse_ad, 
                headers={"user-agent": 
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
        
    def parse_ad(self, response):
        car_ad = AutopliusAd(response, self.car_query_id)
        car_ad.parse()
        car_ad.prepare_data()
        car_ad.insert_auto_ad()