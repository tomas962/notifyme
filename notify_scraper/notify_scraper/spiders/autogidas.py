import scrapy
import sys
from urllib.parse import urlencode
from scrape_utils import *
sys.path.insert(0,"..")
from database.database import connection, db_connect
from .ads import CarAd, AutogidasAd

class AutogidasSpider(scrapy.Spider):
    name = "autogidas"

    def __init__(self, car_query_id=None, **kwargs):
        self.car_query_id = car_query_id
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        self.i = 0

        if self.car_query_id is None:
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

        car_ad = AutogidasAd(response)

        car_ad.parse()
        car_ad.prepare_data()
        car_ad.insert_auto_ad()
