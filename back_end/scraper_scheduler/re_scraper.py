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
from notify_scraper.notify_scraper.spiders.domoplius import DomopliusSpider
from notify_scraper.notify_scraper.spiders.skelbiu import SkelbiuSpider
from notify_scraper.notify_scraper import settings
from scrapy.settings import Settings
import requests
from database.re_queries import get_all_re_queries, get_query_re_ads
from config import SECRET, SERVER_PORT, SERVER_NAME, SCRAPE_INTERVAL, SPIDER_CONFIG

items = []
config = SPIDER_CONFIG
config['ITEM_PIPELINES'] = {'scraper_scheduler.re_scraper.ItemCollector': 100}


class ItemCollector():
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        items.append(item)


class ReScraperScheduler():
    
    def __init__(self):
        self.re_queries = {}
        self.new_query_added = False
        self.cv = threading.Condition()
        self.current_query = None
        self.full_queries = {}

        re_query_list = get_all_re_queries()

        for query in re_query_list:
            self.re_queries[query["id"]] = query

        current_timestamp = time.time()
        for (query_id, query) in self.re_queries.items():
            # scrape after interval, or now if it doesnt exist
            if query["scrape_interval"] is None:
                query["scrape_interval"] = SCRAPE_INTERVAL
            if query["last_scraped"] is not None:
                query["next_scrape"] = query["last_scraped"] + query["scrape_interval"]
            elif query["last_scraped"] is None:
                query["next_scrape"] = current_timestamp # set to now


        # self.updater_thread = threading.Thread(target=self.run)
        # self.updater_thread.start()
        self.scraper_thread = threading.Thread(target=self.re_scraper_loop)
        self.scraper_thread.start()
        

    def scrape(self, q: Queue):
        """Runs the scrapers on self.current_query. MUST invoke in separate process with Process()"""
        print("SCRAPING RE QUERY NR: " + str(self.current_query["id"]))
        print("SUBPROCCESS PID:")
        print(os.getpid())
        print('__name__:')
        print(__name__)
        sett = Settings(config)
        # print("SETTINGS:")
        # print(vars(sett))
        # exit(0)
        process = CrawlerProcess(sett)
        if "sites" in self.current_query and self.current_query["sites"] is not None and "skelbiu" in self.current_query["sites"]:
            process.crawl(SkelbiuSpider, re_query_id=self.current_query["id"])
        if "sites" in self.current_query and self.current_query["sites"] is not None and "domo" in self.current_query["sites"]:
            process.crawl(DomopliusSpider, re_query_id=self.current_query["id"])
        process.start()

        print("TIME ON Q.PUT()")
        print(time.time())
        q.put(items)
        
    
    def re_scraper_loop(self):
        while True:
            lowest = math.inf
            self.current_query = None
            for (query_id, query) in self.re_queries.items():
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
                            print("Sleep got interrupted: new re query added or deleted.")
                        else:
                            print("Sleep ended, continue scraping")
                    else:
                        if self.cv.wait(time_to_wait):
                            print("Sleep got interrupted: new re query added or deleted.")
                        else:
                            print("Sleep ended, continue scraping")
            else:
                print("NO NEED TO WAIT")
            
            if self.current_query is None or time.time() < self.current_query["next_scrape"]:
                continue

            # print("SCRAPER TURNED OFF")
            # time.sleep(99999999)
            # get old ads
            old_ads = get_query_re_ads(self.current_query["id"])
            # SCRAPE HERE, more threads? maybe with proxy
            q = Queue()
            self.current_query["currently_scraping"] = True
            with db_connect().cursor() as cursor:
                cursor.execute("UPDATE re_queries SET currently_scraping=1 WHERE id=%s", self.current_query["id"])
                cursor.connection.commit()
                cursor.connection.close()
            
            requests.post(f'{SERVER_NAME}:{SERVER_PORT}/started_scraping_re_query/{self.current_query["user_id"]}/{self.current_query["id"]}', json={'secret':SECRET}, verify=False)
            p = Process(target=self.scrape, args=(q,)) 
            p.start()
            scraped_ads = q.get(True)
            p.join()

            self.current_query["currently_scraping"] = False
            with db_connect().cursor() as cursor:
                cursor.execute("UPDATE re_queries SET currently_scraping=0 WHERE id=%s", self.current_query["id"])
                cursor.connection.commit()
                cursor.connection.close()
            requests.post(f'{SERVER_NAME}:{SERVER_PORT}/done_scraping_re_query/{self.current_query["user_id"]}/{self.current_query["id"]}', json={'secret':SECRET}, verify=False)
            print("JOINED")
            print("TIME after Q.get()")
            print(time.time())
            print("SCRAPED ITEMS:")
            # get new ads
            # check differences and notify
            ttt = time.time()
            #TODO notif = Notifier(old_cars, scraped_cars, self.full_queries[self.current_query["id"]])
            print("NOTIFIER TOOK TIME:")
            print(time.time() - ttt)
            # update last scraped
            self.current_query["last_scraped"] = int(time.time())
            with db_connect().cursor() as cursor:
                cursor.execute("UPDATE re_queries SET last_scraped=%(last_scraped)s, was_scraped=1 WHERE id=%(id)s", self.current_query)
                cursor.connection.commit()
                cursor.connection.close()

            self.current_query["next_scrape"] = time.time() + self.current_query["scrape_interval"] if "scrape_interval" in self.current_query and \
                self.current_query["scrape_interval"] is not None else time.time() + SCRAPE_INTERVAL


    

    def update_queries(self, query):
        """Adds or updates new query by query["id"] key"""

        with self.cv:
            next_scrape = query["scrape_interval"] + time.time() if "scrape_interval" in query and \
                query["scrape_interval"] is not None else time.time()
            query["next_scrape"] = next_scrape
            self.re_queries[query["id"]] = query
            self.cv.notify()

    def delete_query(self, query_id):
        with self.cv:
            self.re_queries.pop(query_id, None) # TODO implement current query scraping cancellation
            self.cv.notify()

    def start_scraping(self, query_id):
        with self.cv:
            if query_id in self.re_queries:
                self.re_queries[query_id]["next_scrape"] = time.time() #now
                self.cv.notify()
                return True
            return False
