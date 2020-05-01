import scrapy
from urllib.parse import urlencode
import sys
sys.path.insert(0,'..')
from database.database import connection, db_connect
from .ads import CarAd, AutogidasAd
from database.car_query import get_car_query
from .queries import AutogidasQuery
# from .queries import Query
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
        query_from_db = get_car_query(int(self.car_query_id))
        car_query = AutogidasQuery(query_from_db).generate()
        if car_query is None: # don't scrape
            print("WARNING: Autogidas: Not scraping, because model_id doesn't exist for selected model:")
            print(query_from_db)
            return None
        assert car_query is not None, "Car query not found!"
        
        urls = ["https://autogidas.lt/skelbimai/automobiliai/?" + urlencode(car_query)]

        print("GENERATED AUTOGIDAS QUERY:")
        print(urls)
        print("STARTED CRAWLING AUTOGIDAS")
        
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
        yield car_ad.insert_auto_ad()
