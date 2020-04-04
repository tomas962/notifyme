import scrapy
import sys
from urllib.parse import urlencode
from scrape_utils import *
sys.path.insert(0,"..")
from database.database import connection

class AutogidasSpider(scrapy.Spider):
    name = "autogidas"

    def start_requests(self):
        self.i = 0
        car_query = get_car_query(3)
        urls = ["https://www.autogidas.lt/skelbimai/automobiliai/?" + urlencode(form_autog_query(car_query))]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        print("XPATH: ")
        hrefs = response.css('a.item-link::attr(href)').getall()

        for href in hrefs:
            next_page = response.urljoin(href)
            yield scrapy.Request(next_page, callback=self.parse_add)
        
    def parse_add(self, response):
        filename = 'autogidas-%s.html' % self.i
        self.i += 1
        
        for param in response.css('div.param'):
            yield {
                "name": param.css('div.left::text').get(),
                "value": param.css('div.right::text').get()
            }
            
