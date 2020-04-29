import scrapy
from urllib.parse import urlencode
from ....database.database import connection, db_connect
from .ads import CarAd, AutogidasAd
from ....database.car_query import get_car_query

# f_1[0]: BMW
# f_model_14[0]: Series 3
# f_215: 
# f_216: 4000
# f_41: 2002
# f_42: 2014
# f_3[1]: Sedanas
# f_3[2]: Hečbekas
# f_3[3]: Universalas
# f_2[1]: Dyzelinas
# f_2[2]: Benzinas
# f_376:
def form_autog_query(params):
    new_params = {}
    if "make_model" in params and params["make_model"] is not None and "make" in params["make_model"]:
        new_params[f'f_1[0]'] = params["make_model"]["make"] or ""
    if "make_model" in params and params["make_model"] and "model_name" in params["make_model"]:
        new_params[f'f_model_14[0]'] = params["make_model"]["model_name"] or ""

    if "car_query" in params and params["car_query"] is not None:
        if "price_from" in params["car_query"]:
            new_params['f_215'] = params["car_query"]["price_from"] if params["car_query"]["price_from"] is not None else ""
        if "price_to" in params["car_query"]:
            new_params['f_216'] = params["car_query"]["price_to"] if params["car_query"]["price_to"] is not None else ""

        if "year_from" in params["car_query"]:
            new_params['f_41'] = params["car_query"]["year_from"] if params["car_query"]["year_from"] is not None else ""
        if "year_to" in params["car_query"]:
            new_params['f_42'] = params["car_query"]["year_to"] if params["car_query"]["year_to"] is not None else ""
        if "search_term" in params["car_query"] and params["car_query"]["search_term"] is not None:
            new_params['f_376'] = params["car_query"]["search_term"] if params["car_query"]["search_term"] is not None else ""

    if "body_style" in params and params["body_style"] is not None and "name" in params["body_style"]:
        new_params[f'f_3[0]'] = params["body_style"]["name"] if params["body_style"]["name"] is not None else ""
        
    if "fuel_type" in params and params["fuel_type"] is not None and "fuel_name" in params["fuel_type"]:
        new_params[f'f_2[0]'] = params["fuel_type"]["fuel_name"] if params["fuel_type"]["fuel_name"] is not None else ""
    
    return new_params
class AutogidasSpider(scrapy.Spider):
    name = "autogidas"

    def __init__(self, car_query_id=None, **kwargs):
        self.car_query_id = car_query_id
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        self.i = 0

        if self.car_query_id is None:
            raise ValueError("No car_query_id passed to spider")
            return
        car_query = get_car_query(int(self.car_query_id))
        
        urls = ["https://autogidas.lt/skelbimai/automobiliai/?" + urlencode(form_autog_query(car_query))]

        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css('a.item-link::attr(href)').getall()

        for href in hrefs:
            next_page = response.urljoin(href)
            yield scrapy.Request(next_page, callback=self.parse_ad)
        
    def parse_ad(self, response):
       
        car_ad = AutogidasAd(response, self.car_query_id)

        car_ad.parse()
        car_ad.prepare_data()
        car_ad.insert_auto_ad()
