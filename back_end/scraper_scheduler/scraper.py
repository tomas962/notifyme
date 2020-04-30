import threading
from ..database.database import db_connect
import time
import math
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from multiprocessing import Queue
from scrapy import cmdline
import os
from ..notify_scraper.notify_scraper.spiders.autobilis import AutobilisSpider
from ..notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider
from ..notify_scraper.notify_scraper.spiders.autoplius import AutopliusSpider
SCRAPE_INTERVAL = 600
from ..notify_scraper.notify_scraper import settings
from scrapy.settings import Settings
from database.car import get_cars_by_query_id
from notifier.notifier import Notifier 

items = []
class ItemCollector():
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        items.append(item)


class Scraper():
    
    def __init__(self):
        self.car_queries = {}
        self.new_query_added = False
        self.added_query_id = None
        self.cv = threading.Condition()
        self.current_query = None

        with db_connect().cursor() as cursor:
            cursor.execute("SELECT * FROM car_queries")
            queries = cursor.fetchall()
            
            for query in queries:
                query["query_id"] = query["id"]
                self.car_queries[query["id"]] = query
            cursor.connection.close()

        current_timestamp = time.time()
        for (query_id, query) in self.car_queries.items():
            # scrape after interval, or now if it doesnt exist
            if query["scrape_interval"] is None:
                query["scrape_interval"] = SCRAPE_INTERVAL
            if query["last_scraped"] is not None:
                query["next_scrape"] = query["last_scraped"] + query["scrape_interval"]
            elif query["last_scraped"] is None:
                query["next_scrape"] = current_timestamp # set to now


        # self.updater_thread = threading.Thread(target=self.run)
        # self.updater_thread.start()
        self.scraper_thread = threading.Thread(target=self.car_scraper)
        self.scraper_thread.start()
        

    def scrape(self, q: Queue):
        """Runs the scrapers on self.current_query. MUST invoke in separate process with Process()"""
        print("SCRAPING QUERY NR: " + str(self.current_query["query_id"]))
        print("SUBPROCCESS PID:")
        print(os.getpid())
        print('__name__:')
        print(__name__)
        sett = Settings({
            'COOKIES_ENABLED': settings.COOKIES_ENABLED, 
            'DOWNLOAD_DELAY': settings.DOWNLOAD_DELAY,
            'ITEM_PIPELINES': {'back_end.scraper_scheduler.scraper.ItemCollector': 100}
        })
        # print("SETTINGS:")
        # print(vars(sett))
        # exit(0)
        process = CrawlerProcess(sett)
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autobilis" in self.current_query["sites"]:
            process.crawl(AutobilisSpider, car_query_id=self.current_query["query_id"])
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autogidas" in self.current_query["sites"]:
            process.crawl(AutogidasSpider, car_query_id=self.current_query["query_id"])
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autoplius" in self.current_query["sites"]:
            process.crawl(AutopliusSpider, car_query_id=self.current_query["query_id"])
        process.start()

        print("TIME ON Q.PUT()")
        print(time.time())
        q.put(items)
    
    def car_scraper(self):
        while True:
            lowest = math.inf
            self.current_query = None
            for (query_id, query) in self.car_queries.items():
                if query["next_scrape"] < lowest:
                    lowest = query["next_scrape"]
                    self.current_query = query
            
            current_timestamp = time.time()
            time_to_wait = lowest - current_timestamp
            if time_to_wait > 0:
                print("SLEEPING TIME:")
                print(time_to_wait)
                # time.sleep(time_to_wait)
                with self.cv:
                    if self.cv.wait(time_to_wait):
                        print("Sleep got interrupted: new query added.")
                    else:
                        print("Sleep ended, continue scraping")
            else:
                print("NO NEED TO WAIT")
            
            if time.time() < self.current_query["next_scrape"]:
                continue

            # get old cars
            old_cars = get_cars_by_query_id(self.current_query["query_id"])
            # SCRAPE HERE, more threads? maybe with proxy
            q = Queue()
            
            p = Process(target=self.scrape, args=(q,)) 
            p.start()
            scraped_cars = q.get(True)
            
            p.join()
            print("JOINED")
            print("TIME after Q.get()")
            print(time.time())
            print("SCRAPED ITEMS:")
            print(scraped_cars)
            # get new cars
            # check differences and notify
            notif = Notifier(old_cars, scraped_cars, self.current_query)
            # update last scraped
            self.current_query["last_scraped"] = int(time.time())
            with db_connect().cursor() as cursor:
                cursor.execute("UPDATE car_queries SET last_scraped=%(last_scraped)s WHERE id=%(query_id)s", self.current_query)
                cursor.connection.commit()
                cursor.connection.close()

            self.current_query["next_scrape"] = time.time() + self.current_query["scrape_interval"] if "scrape_interval" in self.current_query and \
                self.current_query["scrape_interval"] is not None else time.time() + SCRAPE_INTERVAL



    def update_queries(self, query):
        """Adds or updates new query by query["query_id"] key"""

        with self.cv:
            query["next_scrape"] = query["scrape_interval"] + time.time() if "scrape_interval" in query and \
                query["scrape_interval"] is not None else time.time()
            self.car_queries[query["query_id"]] = query
            self.added_query_id = query["query_id"]
            self.cv.notify()

    # def run(self):
    #     while True:
    #         with self.cv:
    #             self.cv.wait_for(lambda: self.new_query_added)
    #             print("FROM RUN: NEW QUERY ADDED")
    #             print(self.car_queries[self.added_query_id])
    #             # for q, qe in self.car_queries.items():
    #             #     print(qe)
    #             self.new_query_added = False

                    