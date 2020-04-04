#!/usr/bin/env python3
# import scrapy
import sys
sys.path.insert(0, "..")
# from scrapy.crawler import CrawlerProcess
# from notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider
from database.database import connection
from urllib.parse import urlencode

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
    if "make_model" in params and "make" in params["make_model"]:
        new_params[f'f_1[0]'] = params["make_model"]["make"]
    if "make_model" in params and "model_name" in params["make_model"]:
        new_params[f'f_model_14[0]'] = params["make_model"]["model_name"]

    if "price_from" in params["car_query"]:
        new_params['f_215'] = params["car_query"]["price_from"]
    if "price_to" in params["car_query"]:
        new_params['f_216'] = params["car_query"]["price_to"]

    if "year_from" in params["car_query"]:
        new_params['f_41'] = params["car_query"]["year_from"]
    if "year_to" in params["car_query"]:
        new_params['f_42'] = params["car_query"]["year_to"]

    if "body_style" in params and "name" in params["body_style"]:
        new_params[f'f_3[0]'] = params["body_style"]["name"]
        
    if "fuel_type" in params and "fuel_name" in params["fuel_type"]:
        new_params[f'f_2[0]'] = params["fuel_type"]["fuel_name"]
    
    if "search_term" in params["car_query"] and params["car_query"]["search_term"] is not None:
        new_params['f_376'] = params["car_query"]["search_term"]
    
    return new_params

def get_car_query(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM car_queries WHERE id=%s", id)
        car_query = cursor.fetchone()
        
        cursor.execute("""SELECT fuel_types.* FROM query_fuel 
            INNER JOIN fuel_types 
            ON query_fuel.fuel_id=fuel_types.id
            WHERE query_fuel.query_id=%s""", id)
        fuel_type = cursor.fetchone()
        
        cursor.execute("""SELECT body_styles.* FROM `car_queries` 
            INNER JOIN query_body_style ON car_queries.id=query_body_style.query_id
            INNER JOIN body_styles ON query_body_style.body_style_id=body_styles.id
            WHERE car_queries.id=%s""", id)
        body_style = cursor.fetchone()

        cursor.execute("""SELECT makes.*, models.* FROM query_make_model 
            INNER JOIN makes 
            ON query_make_model.make_id=makes.id
            INNER JOIN models
            ON query_make_model.model_id=models.id
            WHERE query_make_model.query_id=%s""", id)
        make_model = cursor.fetchone()

        return {
            "car_query":car_query,
            "fuel_type":fuel_type,
            "body_style":body_style,
            "make_model":make_model
        }


if __name__ == "__main__":
    car_query = get_car_query(3)
    query_params = form_autog_query(car_query)
    print(urlencode(query_params))
    # process = CrawlerProcess()
    # process.crawl(AutogidasSpider)
    # process.start() # the script will block here until all crawling jobs are finished
    # pass