import scrapy
import sys
from urllib.parse import urlencode
from scrape_utils import *
sys.path.insert(0,"..")
from database.database import db_connect

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
        with open("body.html", 'w') as f:
            f.write(response.url)
            print(response.headers)
            f.write(response.text)
        
        params = {}
        params["autop_id"] = response.url.split(".")[-2].split("-")[-1]
        addons = ""

        for row in response.css("div.feature-row"):
            addons += row.css("div.feature-label::text").get().strip() + ": "
            for feature in row.css("span.feature-item::text"):
                addons += feature.get().strip() + ", "
            addons = addons[:-2] + "\n"
        
        params["features"] = addons
        comment = response.css("div.announcement-description::text").get()
        params["comments"] = comment.strip() if comment is not None else None

        for param in response.css('div.parameter-row'):
            value = param.css('div.parameter-value::text').get()
            if value is None:
                continue
            key = db_translations[param.css('div.parameter-label::text').get().strip()]
            if key is None:
                continue
            params[key] = value.strip()
        
        location = response.css('div.owner-location::text').get()
        params["location"] = location.strip() if location is not None else None

        price_row = response.css('div.parameter-row-price')
        params["price"] = price_row.css('div.price::text').get().strip()

        params["make"] = response.css('body > div.body-wrapper > div.page-wrapper > div.content-container > div:nth-child(2) > div > ol > li:nth-child(3) > a::text').get().strip()
        params["model"] = response.css('body > div.body-wrapper > div.page-wrapper > div.content-container > div:nth-child(2) > div > ol > li:nth-child(4) > a::text').get().strip()
        values = prepare_data(params)
        print(values)
        insert_auto_ad(values)
