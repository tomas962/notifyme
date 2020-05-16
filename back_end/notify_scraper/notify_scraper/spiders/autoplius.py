import scrapy
from urllib.parse import urlencode
import sys
sys.path.insert(0,'..')
from database.database import db_connect
from .ads import CarAd, AutopliusAd
from database.car_query import get_car_query
from .queries import AutopliusQuery

    
class AutopliusSpider(scrapy.Spider):
    name = "autoplius"
    
    def __init__(self, car_query_id=None, **kwargs):
        self.car_query_id = car_query_id
        super().__init__(**kwargs)  

    def start_requests(self):
        self.i = 0

        if self.car_query_id is None:
            raise ValueError("No car_query_id passed to spider")
            return
        query_from_db = get_car_query(int(self.car_query_id))
        car_query = AutopliusQuery(query_from_db).generate()
        if car_query is None: # don't scrape
            print("WARNING: Autoplius: Not scraping, because model_id doesn't exist for selected model:")
            print(query_from_db)
            return None
        assert car_query is not None, "Car query not found!"

        urls = ["https://autoplius.lt/skelbimai/naudoti-automobiliai?" + urlencode(car_query)]

        print("STARTED CRAWLING AUTOPLIUS")
        for url in urls:
            rq = scrapy.Request(url=url, callback=self.parse, headers={"user-agent": 
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
            yield rq

    def parse(self, response):
        hrefs = response.css('a.announcement-item::attr(href)').getall()
        
        for href in hrefs:
            next_page = response.urljoin(href)
            yield scrapy.Request(next_page, callback=self.parse_ad, 
                headers={"user-agent": 
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
        
    def parse_ad(self, response):
        car_ad = AutopliusAd(response, self.car_query_id)
        car_ad.parse()
        car_ad.prepare_data()
        yield car_ad.insert_auto_ad()