#!/usr/bin/env python3
import scrapy
from scrapy.crawler import CrawlerProcess
from notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider


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
def convert_query_params(params, site):
    """
    params = {
        makes: list[str],
        models: list[str],
        price_from: int,
        price_to: int,
        year_from: int,
        year_to: int,
        body_types: list[str],
        fuel_types: list[str],
        search_term: str
    }
    """

    new_params = {}
    if site == "autogidas.lt":
        if "makes" in params:
            for i, make in enumerate(params["makes"]):
                new_params[f'f_1[{i}]'] = make
        if "models" in params:
            for i, model in enumerate(params["models"]):
                new_params[f'f_model_14[{i}]'] = model
        if "price_from" in params:
            new_params['f_215'] = params["price_from"]
        if "price_to" in params:
            new_params['f_216'] = params["price_to"]
        if "year_from" in params:
            new_params['f_41'] = params["year_from"]
        if "year_to" in params:
            new_params['f_42'] = params["year_to"]
        if "body_types" in params:
            for i, body_type in enumerate(params["body_types"]):
                new_params[f'f_3[{i}]'] = body_type
        if "fuel_types" in params:
            for i, fuel_type in enumerate(params["fuel_types"]):
                new_params[f'f_2[{i}]'] = fuel_type
        if "search_term" in params:
            new_params['f_376'] = params["search_term"]
    
    return new_params



if __name__ == "__main__":
    print("test")
    
    process = CrawlerProcess()
    process.crawl(AutogidasSpider)
    process.start() # the script will block here until all crawling jobs are finished
    pass