import scrapy
import sys
from urllib.parse import urlencode
from scrape_utils import *
sys.path.insert(0,"..")
from database.database import db_connect
from .ads import CarAd, AutopliusAd

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
            yield scrapy.Request("https://autoplius.lt/skelbimai/audi-a4-2-0-l-sedanas-2001-benzinas-10635435.html", callback=self.parse_ad, 
                headers={"user-agent": 
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
        
    def parse_ad(self, response):
        car_ad = AutopliusAd(response)
        car_ad.parse()
        car_ad.prepare_data()
        car_ad.insert_auto_ad()