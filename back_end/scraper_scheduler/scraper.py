import threading
from ..database.database import db_connect
import time
import math
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from scrapy import cmdline
import os
from ..notify_scraper.notify_scraper.spiders.autobilis import AutobilisSpider
from ..notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider
from ..notify_scraper.notify_scraper.spiders.autoplius import AutopliusSpider
SCRAPE_INTERVAL = 10

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


        self.updater_thread = threading.Thread(target=self.run)
        self.updater_thread.start()
        self.scraper_thred = threading.Thread(target=self.car_scraper)
        self.scraper_thred.start()
        

    def scrape(self):
        """Runs the scrapers on self.current_query. MUST invoke in separate process with Process()"""
        print("SCRAPING QUERY NR: " + str(self.current_query["query_id"]))
        print("SUBPROCCESS PID:")
        print(os.getpid())
        os.chdir("../notify_scraper")
        settings = get_project_settings()
        os.chdir("../server")
        process = CrawlerProcess(settings)
        print(os.getcwd())
        exit(0)
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autobilis" in self.current_query["sites"]:
            process.crawl(AutobilisSpider, car_query_id=self.current_query["query_id"])
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autogidas" in self.current_query["sites"]:
            process.crawl(AutogidasSpider, car_query_id=self.current_query["query_id"])
        if "sites" in self.current_query and self.current_query["sites"] is not None and "autoplius" in self.current_query["sites"]:
            process.crawl(AutopliusSpider, car_query_id=self.current_query["query_id"])
        process.start()
    
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
                time.sleep(time_to_wait)
            
            print("MY PID:")
            print(os.getpid())
            # SCRAPE HERE, more threads? maybe with proxy
            p = Process(target=self.scrape) #TODO SET DIR TO SCRAPY PROJECT
            p.start()
            p.join()
            print("JOINED")
            
            # update last scraped
            self.current_query["last_scraped"] = int(time.time())
            with db_connect().cursor() as cursor:
                cursor.execute("UPDATE car_queries SET last_scraped=%(last_scraped)s WHERE id=%(query_id)s", self.current_query)
                cursor.connection.commit()
                cursor.connection.close()

            self.current_query["next_scrape"] += self.current_query["scrape_interval"] if "scrape_interval" in self.current_query and \
                self.current_query["scrape_interval"] is not None else SCRAPE_INTERVAL



    def update_queries(self, query):
        """Adds or updates new query by query["query_id"] key"""

        with self.cv:
            query["next_scrape"] = query["scrape_interval"] + time.time() if "scrape_interval" in query and \
                query["scrape_interval"] is not None else time.time() + SCRAPE_INTERVAL
            self.car_queries[query["query_id"]] = query
            self.new_query_added = True
            self.added_query_id = query["query_id"]
            self.cv.notify()

    def run(self):
        while True:
            with self.cv:
                self.cv.wait_for(lambda: self.new_query_added)
                print("FROM RUN: NEW QUERY ADDED")
                print(self.car_queries[self.added_query_id])
                # for q, qe in self.car_queries.items():
                #     print(qe)
                self.new_query_added = False

                    
        