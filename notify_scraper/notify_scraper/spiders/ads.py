import sys
sys.path.insert(0, "..")
from scrape_utils import *
# from scrapy.crawler import CrawlerProcess
# from notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider
from database.database import connection, db_connect
from urllib.parse import urlencode

class CarAd():
    def __init__(self, response, query_id):
        self.response = response
        self.scraped_params = {}
        self.prepared_params = {}
        self.scraped_params["query_id"] = query_id

    def prepare_data(self):
        """
            Prepare data for insertion into database.  
            Add None where neccesary and convert to integers.
        """
        for k, v in db_translations.items():
            self.prepared_params[v] = self.scraped_params.get(v) # add None entries if doesn't exist

        self.prepared_params["price"] = int(self.prepared_params["price"].split("€")[0].replace(" ", "")) if self.prepared_params["price"] is not None else None
        self.prepared_params["export_price"] = int(self.prepared_params["export_price"].split("€")[0].replace(" ", "")) if self.prepared_params["export_price"] is not None else None
        self.prepared_params["year"] = self.prepared_params["year"].split(" ")[0] if self.prepared_params["year"] is not None else None
        self.prepared_params["weight"] = int(self.prepared_params["weight"].split(" ")[0]) if self.prepared_params["weight"] is not None else None
        self.prepared_params["ts_to"] = self.prepared_params["ts_to"] + "-01" if self.prepared_params["ts_to"] is not None else None


    def auto_foreign_keys(self, cursor):
        # convert values to ID's
        if self.prepared_params["make"] is not None:
            cursor.execute("SELECT * from makes WHERE make=%s", self.prepared_params["make"])
            make = cursor.fetchone()
            self.prepared_params["make"] = make["id"]
        if self.prepared_params["model"] is not None:
            cursor.execute("SELECT * from models WHERE make_id=%s AND model_name=%s", (self.prepared_params["make"], self.prepared_params["model"]))
            model = cursor.fetchone()
            self.prepared_params["model"] = model["id"]
        if self.prepared_params["fuel_type"] is not None:
            cursor.execute("SELECT * from fuel_types WHERE fuel_name=%s", self.prepared_params["fuel_type"])
            fuel = cursor.fetchone()
            self.prepared_params["fuel_type"] = fuel["id"]
        if self.prepared_params["body_type"] is not None:
            cursor.execute("SELECT * from body_styles WHERE name=%s", self.prepared_params["body_type"])
            body_t = cursor.fetchone()
            self.prepared_params["body_type"] = body_t["id"]

    def insert_auto_ad(self):
        if "autog_id" in self.prepared_params and self.prepared_params["autog_id"] is not None:
            self.prepared_params["key_column"] = "autog_id"
            self.prepared_params["key_value"] = self.prepared_params["autog_id"]
        elif "autop_id" in self.prepared_params and self.prepared_params["autop_id"] is not None:
            self.prepared_params["key_column"] = "autop_id"
            self.prepared_params["key_value"] = self.prepared_params["autop_id"]
        elif "autob_id" in self.prepared_params and self.prepared_params["autob_id"] is not None:
            self.prepared_params["key_column"] = "autob_id"
            self.prepared_params["key_value"] = self.prepared_params["autob_id"]

        with db_connect().cursor() as cursor:
            cursor.execute("SELECT * FROM car_ads WHERE "+self.prepared_params["key_column"]+"=%(key_value)s", self.prepared_params)
            ad_exists = cursor.fetchone()
            self.auto_foreign_keys(cursor)
            if ad_exists:
                cursor.execute(f"""UPDATE `car_ads` SET make=%(make)s, model=%(model)s, year=%(year)s, engine=%(engine)s,
                    fuel_type=%(fuel_type)s, body_type=%(body_type)s, 
                    color=%(color)s, gearbox=%(gearbox)s, driven_wheels=%(driven_wheels)s, damage=%(damage)s,
                    steering_column=%(steering_column)s,
                    door_count=%(door_count)s, cylinder_count=%(cylinder_count)s, gear_count=%(gear_count)s, 
                    seat_count=%(seat_count)s, ts_to=DATE(%(ts_to)s), weight=%(weight)s, 
                    wheels=%(wheels)s, fuel_urban=%(fuel_urban)s, fuel_overland=%(fuel_overland)s, 
                    fuel_overall=%(fuel_overall)s, features=%(features)s, comments=%(comments)s, 
                    """+self.prepared_params["key_column"]+f"""=%(key_value)s, price=%(price)s, export_price=%(export_price)s, vin_code=%(vin_code)s,
                    query_id=%(query_id)s 
                    WHERE {self.prepared_params["key_column"]}=%(key_value)s""", self.prepared_params)
                
            else:
                cursor.execute("""INSERT INTO `car_ads`(`make`, `model`, `year`, `engine`, `fuel_type`, 
                    `body_type`, `color`, `gearbox`, `driven_wheels`, `damage`, `steering_column`, `door_count`, 
                    `cylinder_count`, `gear_count`, `seat_count`, `ts_to`, `weight`, `wheels`, `fuel_urban`, 
                    `fuel_overland`, `fuel_overall`, `features`, `comments`, """+self.prepared_params["key_column"]+""", `price`,
                    `export_price`, `vin_code`, query_id) 
                    VALUES (%(make)s, %(model)s, %(year)s, %(engine)s, %(fuel_type)s, %(body_type)s, 
                    %(color)s, %(gearbox)s, %(driven_wheels)s, %(damage)s, %(steering_column)s,
                    %(door_count)s, %(cylinder_count)s, %(gear_count)s, %(seat_count)s, DATE(%(ts_to)s), %(weight)s, 
                    %(wheels)s, %(fuel_urban)s, %(fuel_overland)s, %(fuel_overall)s, %(features)s, %(comments)s, 
                    %(key_value)s, %(price)s, %(export_price)s, %(vin_code)s, %(query_id)s)""", self.prepared_params)
            cursor.connection.commit()
            cursor.connection.close()

    def parse(self):
        NotImplementedError("Child class must implement 'parse' method")

class AutogidasAd(CarAd):

    def parse(self):
        self.scraped_params["autog_id"] = self.response.url.split(".")[-2].split("-")[-1]
        addons = ""
        for addon in self.response.css('div.addon::text'):
            addons += addon.get().strip() + ", "
        addons = addons[:-2]
        self.scraped_params["features"] = addons
        comment = self.response.css('div.comments::text').get()
        self.scraped_params["comments"] = comment.strip() if comment is not None else None
        print(self.scraped_params)
        for param in self.response.css('div.param'):
            value = param.css('div.price::text').get() or param.css('div.right::text').get()
            self.scraped_params[db_translations[param.css('div.left::text').get().strip()]] = value.strip()
        
class AutopliusAd(CarAd):

    def parse(self):
        self.scraped_params["autop_id"] = self.response.url.split(".")[-2].split("-")[-1]
        addons = ""

        for row in self.response.css("div.feature-row"):
            addons += row.css("div.feature-label::text").get().strip() + ": "
            for feature in row.css("span.feature-item::text"):
                addons += feature.get().strip() + ", "
            addons = addons[:-2] + "\n"
        
        self.scraped_params["features"] = addons
        comment = self.response.css("div.announcement-description::text").get()
        self.scraped_params["comments"] = comment.strip() if comment is not None else None

        for param in self.response.css('div.parameter-row'):
            value = param.css('div.parameter-value::text').get()
            if value is None:
                continue
            key = db_translations[param.css('div.parameter-label::text').get().strip()]
            if key is None:
                continue
            self.scraped_params[key] = value.strip()
        
        location = self.response.css('div.owner-location::text').get()
        self.scraped_params["location"] = location.strip() if location is not None else None

        price_row = self.response.css('div.parameter-row-price')
        self.scraped_params["price"] = price_row.css('div.price::text').get().strip()

        self.scraped_params["make"] = self.response.css('body > div.body-wrapper > div.page-wrapper > div.content-container > div:nth-child(2) > div > ol > li:nth-child(3) > a::text').get().strip()
        self.scraped_params["model"] = self.response.css('body > div.body-wrapper > div.page-wrapper > div.content-container > div:nth-child(2) > div > ol > li:nth-child(4) > a::text').get().strip()


class AutobilisAd(CarAd):

    def db_driven_wheels(self):
        """
        Converts "driven_wheels" values to match ENUM database column 
        """
        if self.scraped_params.get("driven_wheels"):
            if "Priekiniai" in self.scraped_params["driven_wheels"]:
                self.scraped_params["driven_wheels"] = "Priekiniai varantys ratai"
            elif "Galiniai" in self.scraped_params["driven_wheels"]:
                self.scraped_params["driven_wheels"] = "Galiniai varantys ratai"
            elif "Visi" in self.scraped_params["driven_wheels"] or "visi" in self.scraped_params["driven_wheels"]:
                self.scraped_params["driven_wheels"] = "Visi varantys ratai"

    def parse(self):
        self.scraped_params["autob_id"] = self.response.url.split("/")[4]

        for row in self.response.css("div.row.car-info-r"):
            key = db_translations[row.css('div.col-sm-6.car-info-h > p::text').get().strip()]
            value = row.css('div.col-sm-6.car-info-c > p::text').get()
            self.scraped_params[key] = value.strip()

        self.scraped_params["engine"] = f'{self.scraped_params["engine_volume"]} L, {self.scraped_params["power"]}'
        
        self.scraped_params["features"] = ""
        feature_block = self.response.css('div.advert-price-MainInfo-features')
        for feature in feature_block.css('span::text'):
            self.scraped_params["features"] += feature.get().strip() + ", "
        self.scraped_params["features"] = self.scraped_params["features"][:-2]

        
        comment_block = self.response.css("div.advert-price-MainInfo-comments")
        if comment_block is not None:
            self.scraped_params["comments"] = comment_block.css('div.advert-price-MainInfo-text > span::text').get().strip()

        location = self.response.css('div.owner-location::text').get()
        self.scraped_params["location"] = self.scraped_params["country"] + ", " + self.scraped_params["city"]

        self.scraped_params["price"] = self.response.css('span.price-value::attr(data-price)').get().strip()

        self.scraped_params["fuel_overall"] = self.scraped_params.get("fuel_overall").split("l")[0] if self.scraped_params["fuel_overall"] else None
        self.db_driven_wheels()
