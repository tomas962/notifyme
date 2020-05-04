import threading
from database.database import db_connect
import time
import math
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from multiprocessing import Queue
from scrapy import cmdline
import os
from notify_scraper.notify_scraper.spiders.autobilis import AutobilisSpider
from notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider
from notify_scraper.notify_scraper.spiders.autoplius import AutopliusSpider
SCRAPE_INTERVAL = 600
from notify_scraper.notify_scraper import settings
from scrapy.settings import Settings
from notifier.notifier import Notifier 
from database.car import get_cars_by_query_id
from database.car_query import get_all_car_queries, get_car_query

items = []
class ItemCollector():
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        items.append(item)


class ScraperScheduler():
    
    def __init__(self):
        self.car_queries = {}
        self.new_query_added = False
        self.added_query_id = None
        self.cv = threading.Condition()
        self.current_query = None
        self.full_queries = {}

        full_queries = get_all_car_queries()
        queries = [x["car_query"] for x in full_queries]
        for query in full_queries:
            self.full_queries[query["car_query"]["id"]] = query

        for query in queries:
            self.car_queries[query["id"]] = query

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
        self.scraper_thread = threading.Thread(target=self.car_scraper_loop)
        self.scraper_thread.start()
        

    def scrape(self, q: Queue):
        """Runs the scrapers on self.current_query. MUST invoke in separate process with Process()"""
        print("SCRAPING QUERY NR: " + str(self.current_query["id"]))
        print("SUBPROCCESS PID:")
        print(os.getpid())
        print('__name__:')
        print(__name__)
        sett = Settings({
            'COOKIES_ENABLED': settings.COOKIES_ENABLED, 
            'DOWNLOAD_DELAY': settings.DOWNLOAD_DELAY,
            'ITEM_PIPELINES': {'scraper_scheduler.scraper.ItemCollector': 100}
        })
        # print("SETTINGS:")
        # print(vars(sett))
        # exit(0)
        process = CrawlerProcess(sett)
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autobilis" in self.current_query["sites"]:
            process.crawl(AutobilisSpider, car_query_id=self.current_query["id"])
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autogidas" in self.current_query["sites"]:
            process.crawl(AutogidasSpider, car_query_id=self.current_query["id"])
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autoplius" in self.current_query["sites"]:
            process.crawl(AutopliusSpider, car_query_id=self.current_query["id"])
        process.start()

        print("TIME ON Q.PUT()")
        print(time.time())
        q.put(items)
        
    
    def car_scraper_loop(self):
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
                    if time_to_wait == math.inf:
                        if self.cv.wait():
                            print("Sleep got interrupted: new query added.")
                        else:
                            print("Sleep ended, continue scraping")
                    else:
                        if self.cv.wait(time_to_wait):
                            print("Sleep got interrupted: new query added.")
                        else:
                            print("Sleep ended, continue scraping")
            else:
                print("NO NEED TO WAIT")
            
            if self.current_query is None or time.time() < self.current_query["next_scrape"]:
                continue

            # print("SCRAPER TURNED OFF")
            # time.sleep(99999999)
            # get old cars
            old_cars = get_cars_by_query_id(self.current_query["id"])
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
            # get new cars
            # check differences and notify
            ttt = time.time()
            notif = Notifier(old_cars, scraped_cars, self.full_queries[self.current_query["id"]])
            print("NOTIFIER TOOK TIME:")
            print(time.time() - ttt)
            # update last scraped
            self.current_query["last_scraped"] = int(time.time())
            with db_connect().cursor() as cursor:
                cursor.execute("UPDATE car_queries SET last_scraped=%(last_scraped)s, was_scraped=1 WHERE id=%(id)s", self.current_query)
                cursor.connection.commit()
                cursor.connection.close()

            self.current_query["next_scrape"] = time.time() + self.current_query["scrape_interval"] if "scrape_interval" in self.current_query and \
                self.current_query["scrape_interval"] is not None else time.time() + SCRAPE_INTERVAL


    

    def update_queries(self, query):
        """Adds or updates new query by query["id"] key"""

        with self.cv:
            next_scrape = query["scrape_interval"] + time.time() if "scrape_interval" in query and \
                query["scrape_interval"] is not None else time.time()
            full_query = get_car_query(query["id"])
            self.full_queries[query["id"]] = full_query
            full_query["car_query"]["next_scrape"] = next_scrape
            self.car_queries[query["id"]] = full_query["car_query"]
            self.cv.notify()

