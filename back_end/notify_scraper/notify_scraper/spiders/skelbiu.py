import scrapy
from urllib.parse import urlencode
import sys
from database.re_queries import get_re_query
from .re_queries import SkelbiuReQuery
from.re_ads import SkelbiuAd

class SkelbiuSpider(scrapy.Spider):
    name = "skelbiu"
    
    def __init__(self, re_query_id=None, **kwargs):
        self.re_query_id = re_query_id
        super().__init__(**kwargs)  

    def start_requests(self):
        self.i = 0

        if self.re_query_id is None:
            raise ValueError("No re_query_id passed to spider")
            return
        query_from_db = get_re_query(int(self.re_query_id))
        if query_from_db is None: # don't scrape
            print("WARNING: Skelbiu: Not scraping (query not found):")
            print(query_from_db)
            return None
        qr = SkelbiuReQuery(query_from_db)
        re_query = qr.generate()
        if re_query is None: # don't scrape
            print("WARNING: Skelbiu: Not scraping:")
            print(query_from_db)
            return None
        assert re_query is not None, "RE query not found!"

        urls = ["https://skelbiu.lt/skelbimai/?" + urlencode(re_query)]

        print("STARTED CRAWLING SKELBIU")
        for url in urls:
            rq = scrapy.Request(url=url, callback=self.parse, headers={"user-agent": 
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
            yield rq

    def parse(self, response):
        hrefs = response.css('div.itemReview > h3 > a::attr(href)').getall()
        # with open("tmp.html", "w") as f:
        #     f.write(response.text)
        # hrefs = ["https://www.skelbiu.lt/skelbimai/parduodamas-vieno-auksto-privatus-namas-isskirtineje-miesto-48001317.html"]
        for href in hrefs:
            next_page = response.urljoin(href)
            yield scrapy.Request(next_page, callback=self.parse_ad, 
                headers={"user-agent": 
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
        
    def parse_ad(self, response):
        ad = SkelbiuAd(response, self.re_query_id)
        ad.parse()
        ad.prepare_data()
        yield ad.insert_ad()