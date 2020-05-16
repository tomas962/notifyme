# from scrapy.crawler import CrawlerProcess
# from notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider
import os
import sys
sys.path.insert(0,'..')
from database.database import connection, db_connect
from urllib.parse import urlencode
from typing import Dict, Union
from scrapy.http import Response 
import pymysql
import json

db_translations = {
    #autogidas
    "Make":"make",
    "Model":"model",
    "Year":"year",
    "Engine":"engine",
    "Fuel Type":"fuel_type",
    "Body Type":"body_type",
    "Color":"color",
    "Gearbox":"gearbox",
    "Driven wheels":"driven_wheels",
    "Damage":"damage",
    "Steering column":"steering_column",
    "Doors":"door_count",
    "Number of cylinders":"cylinder_count",
    "Number of gears":"gear_count",
    "Number of Seats":"seat_count",
    "TS to":"ts_to",
    "Weight, kg":"weight",
    "Wheels":"wheels",
    "Urban":"fuel_urban",
    "Overland":"fuel_overland",
    "Overall":"fuel_overall",
    "Features":"features",
    "Comments":"comments",
    "Price":"price",
    "Export price":"export_price",
    "Mileage":"mileage",
    "First registration country":"first_reg_country",
    "Euro standard":"euro_standard",

    "Markė":"make",
    "Modelis":"model",
    "Metai":"year",
    "Variklis":"engine",
    "Kuro tipas":"fuel_type",
    "Kėbulo tipas":"body_type",
    "Spalva":"color",
    "Pavarų dėžė":"gearbox",
    "Varomieji ratai":"driven_wheels",
    "Defektai":"damage",
    "Vairo padėtis":"steering_column",
    "Durų skaičius":"door_count",
    "Cilindrų skaičius":"cylinder_count",
    "Pavarų skaičius":"gear_count",
    "Sėdimų vietų skaičius":"seat_count",
    "TA iki":"ts_to",
    "Svoris, kg":"weight",
    "Ratlankiai":"wheels",
    "Mieste":"fuel_urban",
    "Užmiestyje":"fuel_overland",
    "Mišrus":"fuel_overall",
    "Ypatybės":"features",
    "Komentarai":"comments",
    "Kaina":"price",
    "Kaina eksportui":"export_price",
    "Rida, km":"mileage",
    "Pirmosios registracijos šalis":"first_reg_country",
    "Euro standartas":"euro_standard",
    "CO2 emisija, g/km":"co2_emmision",
    "#1":"autog_id", # for setting to None,
    "VIN kodas":"vin_code",
    "Telefonas":"phone",
    "Pardavėjas": "?",

    # autoplius
    "Pagaminimo data":"year",
    "Rida":"mileage",
    "Varantieji ratai":"driven_wheels",
    "Klimato valdymas":"climate_control",
    "Ratlankių skersmuo":"wheels",
    "Tech. apžiūra iki":"ts_to",
    "Nuosava masė, kg":"weight",
    "Kuro bako talpa": "?1",
    "Paslaugos pavadinimas": "?2",
    "Paslaugos tipas":"?3",
    "Kėbulo numeris (VIN)":"vin_code",
    "Nauja / naudota":"?4",
    "Vidutinės":"fuel_overall",
    "Eksportui":"export_price",
    "":"?", # ikraunamas elektr
    "Elektra nuvažiuojamas atstumas":"el_range",

    #autobilis
    "Mėnuo":"?5",
    "Darbinis tūris, l.":"engine_volume",
    "Šalis":"country",
    "Miestas":"city",
    "Galia, kW":"power",
    "Transmisija":"driven_wheels",
    "Būklė":"damage",
    "TA galiojimo laikas":"ts_to",
    "Skelbimo data":"date_added",
    "Kuro sąnaudos":"fuel_overall",
    "Pirma registracijos šalis":"first_reg_country",
    "VIN numeris":"vin_code",
    "Klimato kontrolė":"climate_control",
    "Tipas":"?6", # https://www.autobilis.lt/advert/443210/bmw-120-2008
    "CO₂ emisija, g/km": "co2_emmision",
    
    # empty for db columns
    "?0":"autog_id",
    "?1":"autop_id",
    "?2":"autob_id",
    "?3":"query_id",
    "?4":"href",
    "?5":"picture_href",
    "?6":"location",
    
}

class CarAd():
    scraped_params: Dict[str, Union[str, int, float]]
    def __init__(self, response, query_id):
        self.response: Response = response
        self.scraped_params = {}
        self.prepared_params = {}
        self.scraped_params["query_id"] = query_id

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
        self.prepared_params["ts_to"] = self.prepared_params["ts_to"] + "-01-01" if self.prepared_params["ts_to"] is not None else None


    def auto_foreign_keys(self, cursor):
        # convert values to ID's
        if self.prepared_params["make"] is not None:
            cursor.execute("SELECT * from makes WHERE make=%s", self.prepared_params["make"])
            make = cursor.fetchone()
            self.prepared_params["make_name"] = self.prepared_params["make"]
            self.prepared_params["make"] = make["id"]
        if self.prepared_params["model"] is not None:
            #TODO fix not matching model names
            cursor.execute("SELECT * from models WHERE make_id=%s AND model_name=%s", (self.prepared_params["make"], self.prepared_params["model"]))
            model = cursor.fetchone()
            self.prepared_params["model_name"] = self.prepared_params["model"]
            self.prepared_params["model"] = model["id"]
        if self.prepared_params["fuel_type"] is not None:
            cursor.execute("SELECT * from fuel_types WHERE fuel_name=%s", self.prepared_params["fuel_type"].replace(" ", ""))
            fuel = cursor.fetchone()
            self.prepared_params["fuel_type_name"] = self.prepared_params["fuel_type"]
            self.prepared_params["fuel_type"] = fuel["id"]
        if self.prepared_params["body_type"] is not None:
            cursor.execute("SELECT * from body_styles WHERE name=%s", self.prepared_params["body_type"])
            body_t = cursor.fetchone()
            self.prepared_params["body_type_name"] = self.prepared_params["body_type"]
            self.prepared_params["body_type"] = body_t["id"]

    def extract_relevant_attributes(self):
        """Extracts only relevant attributes, to return for later data processing."""
        car = {}
        car["make"] = self.prepared_params["make"]
        car["model"] = self.prepared_params["model"]
        car["year"] = self.prepared_params["year"]
        car["engine"] = self.prepared_params["engine"]
        car["fuel_type"] = self.prepared_params["fuel_type"]
        car["body_type"] = self.prepared_params["body_type"]
        car["color"] = self.prepared_params["color"]
        car["gearbox"] = self.prepared_params["gearbox"]
        car["driven_wheels"] = self.prepared_params["driven_wheels"]
        car["damage"] = self.prepared_params["damage"]
        car["steering_column"] = self.prepared_params["steering_column"]
        car["door_count"] = self.prepared_params["door_count"]
        car["cylinder_count"] = self.prepared_params["cylinder_count"]
        car["ts_to"] = self.prepared_params["ts_to"]
        car["weight"] = self.prepared_params["weight"]
        car["wheels"] = self.prepared_params["wheels"]
        car["fuel_urban"] = self.prepared_params["fuel_urban"]
        car["fuel_overland"] = self.prepared_params["fuel_overland"]
        car["fuel_overall"] = self.prepared_params["fuel_overall"]
        car["features"] = self.prepared_params["features"]
        car["comments"] = self.prepared_params["comments"]
        car["key_value"] = self.prepared_params["key_value"]
        car["price"] = self.prepared_params["price"]
        car["autog_id"] = self.prepared_params["autog_id"]
        car["autob_id"] = self.prepared_params["autob_id"]
        car["autop_id"] = self.prepared_params["autop_id"]
        car["export_price"] = self.prepared_params["export_price"]
        car["vin_code"] = self.prepared_params["vin_code"]
        car["query_id"] = self.prepared_params["query_id"]
        car["href"] = self.prepared_params["href"]
        car["picture_href"] = self.prepared_params["picture_href"]
        car["mileage"] = self.prepared_params["mileage"]
        car["location"] = self.prepared_params["location"]
        car["id"] = self.prepared_params["id"]
        car["make_name"] = self.prepared_params["make_name"]
        car["model_name"] = self.prepared_params["model_name"]
        car["body_type_name"] = self.prepared_params["body_type_name"]
        car["fuel_type_name"] = self.prepared_params["fuel_type_name"]
        return car

    def insert_auto_ad(self):
        """Inserts car ad into database and returns inserted car ad"""
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
                    href=%(href)s, mileage=%(mileage)s, location=%(location)s, when_scraped=unix_timestamp(),
                    phone=%(phone)s, deleted=0, first_reg_country=%(first_reg_country)s, el_range=%(el_range)s
                    WHERE {self.prepared_params["key_column"]}=%(key_value)s""", self.prepared_params)
                self.prepared_params["id"] = ad_exists["id"]
                try:
                    cursor.execute("INSERT INTO query_car_fk (query_id, car_id) VALUES (%(query_id)s, %(id)s)", self.prepared_params)
                except pymysql.IntegrityError as err:
                    print("Car ad already existed: ")
                    print(err)
                
                try:
                    cursor.executemany("INSERT INTO `car_pictures`(`car_id`, `picture_href`) VALUES (%s, %s)",
                        [(self.prepared_params["id"], p_href) for p_href in self.prepared_params["picture_href"]])
                except pymysql.IntegrityError as err:
                    print("Picture already exists: ")
                    print(err)
            else:
                cursor.execute("""INSERT INTO `car_ads`(`make`, `model`, `year`, `engine`, `fuel_type`, 
                    `body_type`, `color`, `gearbox`, `driven_wheels`, `damage`, `steering_column`, `door_count`, 
                    `cylinder_count`, `gear_count`, `seat_count`, `ts_to`, `weight`, `wheels`, `fuel_urban`, 
                    `fuel_overland`, `fuel_overall`, `features`, `comments`, """+self.prepared_params["key_column"]+""", `price`,
                    `export_price`, `vin_code`, href, mileage, location, when_scraped, phone, deleted, first_reg_country, el_range) 
                    VALUES (%(make)s, %(model)s, %(year)s, %(engine)s, %(fuel_type)s, %(body_type)s, 
                    %(color)s, %(gearbox)s, %(driven_wheels)s, %(damage)s, %(steering_column)s,
                    %(door_count)s, %(cylinder_count)s, %(gear_count)s, %(seat_count)s, DATE(%(ts_to)s), %(weight)s, 
                    %(wheels)s, %(fuel_urban)s, %(fuel_overland)s, %(fuel_overall)s, %(features)s, %(comments)s, 
                    %(key_value)s, %(price)s, %(export_price)s, %(vin_code)s, %(href)s, 
                    %(mileage)s, %(location)s, unix_timestamp(), %(phone)s, 0, %(first_reg_country)s, %(el_range)s)""", self.prepared_params)
                self.prepared_params["id"] = cursor.lastrowid

                cursor.execute("INSERT INTO query_car_fk (query_id, car_id) VALUES (%(query_id)s, %(id)s)", self.prepared_params)

                cursor.executemany("INSERT INTO `car_pictures`(`car_id`, `picture_href`) VALUES (%s, %s)",
                    [(self.prepared_params["id"], p_href) for p_href in self.prepared_params["picture_href"]])
            cursor.connection.commit()
            cursor.connection.close()
        
        car = self.extract_relevant_attributes()
        return car

    def parse(self):
        NotImplementedError("Child class must implement 'parse' method")

class AutogidasAd(CarAd):

    def prepare_data(self):
        super().prepare_data()
        self.prepared_params["mileage"] = self.prepared_params["mileage"].split(" ")[0] if self.prepared_params["mileage"] is not None else None

    def scrape_imgs(self):
        self.scraped_params["picture_href"] = []
        js: str = self.response.css("body > script:nth-child(13)::text").get()
        if js is not None:
            for line in js.splitlines():
                if "gallery.addImage" in line:
                    self.scraped_params["picture_href"].append(line.split("'")[1])

    def parse(self):
        self.scraped_params["autog_id"] = self.response.url.split(".")[-2].split("-")[-1]
        addons = ""
        for addon in self.response.css('div.addon::text'):
            addons += addon.get().strip() + ", "
        addons = addons[:-2]
        self.scraped_params["features"] = addons
        comment = self.response.css('div.comments::text').getall()
        if comment:
            self.scraped_params["comments"] = "\n".join(comment)
        for param in self.response.css('div.param'):
            value = param.css('div.price::text').get() or param.css('div.right::text').get()
            self.scraped_params[db_translations[param.css('div.left::text').get().strip()]] = value.strip()

        img = self.response.css("img.show::attr(src)").get()
        self.scraped_params["picture_href"] = img.strip() if img is not None else None
        self.scraped_params["href"] = self.response.url

        location = self.response.css("div.seller-ico.seller-btn.seller-location::text").get()
        if location:
            words = location.split(",")
            country = words[1].strip()
            city = words[0].strip()
            self.scraped_params["location"] = country + ", " + city

        self.scraped_params["phone"] = self.response.css("div.seller-info > div.seller-ico.seller-phones.btn-action::text").get()
        self.scraped_params["phone"] = self.scraped_params["phone"].strip() if self.scraped_params["phone"] is not None else None

        self.scrape_imgs()

class AutopliusAd(CarAd):

    def prepare_data(self):
        super().prepare_data()

        self.prepared_params["fuel_urban"] = self.prepared_params["fuel_urban"].replace(',','.') if self.prepared_params["fuel_urban"] is not None else None
        self.prepared_params["fuel_overland"] = self.prepared_params["fuel_overland"].replace(',','.') if self.prepared_params["fuel_overland"] is not None else None
        self.prepared_params["fuel_overall"] = self.prepared_params["fuel_overall"].replace(',','.') if self.prepared_params["fuel_overall"] is not None else None
        if self.prepared_params["mileage"] is not None:
            self.prepared_params["mileage"] = self.prepared_params["mileage"].replace(" ", "").replace("km", "")
        if self.prepared_params["el_range"] is not None:
            self.prepared_params["el_range"] = self.prepared_params["el_range"].replace(" ", "").replace("km", "")
        

    def scrape_body_type(self):
        btype = self.response.css(".page-title > h1::text").get()
        if btype:
            if "(coupe)" in btype:
                self.scraped_params["body_type"] = "Coupe"
            elif "komercinis" in btype:
                self.scraped_params["body_type"] = "Komercinis auto(su būda)"
            elif "keleiviniai" in btype:
                self.scraped_params["body_type"] = "Keleivinis mikroautobusas"
            else:
                self.scraped_params["body_type"] = self.response.css(".page-title > h1::text").get().split(", ")[-1].capitalize()

    def scrape_imgs(self):
        self.scraped_params["picture_href"] = []
        js_code: str = self.response.css('body > div.body-wrapper > div.page-wrapper > div.content-container > div.row.native-baner-theme > div.col-7 > script:nth-child(4)::text').get()
        if js_code:
            pic_json = js_code.split("mediaGalleryItems")[1].strip(" =;\n\t")
            pic_list = json.loads(pic_json)
            for p in pic_list:
                self.scraped_params["picture_href"].append(p["url"])
       

    def parse(self):
        self.scraped_params["autop_id"] = self.response.url.split(".")[-2].split("-")[-1]
        addons = ""

        for row in self.response.css("div.feature-row"):
            addons += row.css("div.feature-label::text").get().strip() + ": "
            for feature in row.css("span.feature-item::text"):
                addons += feature.get().strip() + ", "
            addons = addons[:-2] + "\n"
        
        self.scraped_params["features"] = addons
        comment = self.response.css("div.announcement-description::text").getall()
        if comment:
            self.scraped_params["comments"] = "\n".join(comment)

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

        self.scraped_params["href"] = self.response.url

        self.db_driven_wheels()

        self.scrape_body_type()

   
        if "steering_column" in self.scraped_params and self.scraped_params["steering_column"] is not None:
            if "Dešinėje" in self.scraped_params["steering_column"]:
                self.scraped_params["steering_column"] = "Dešinėje"

        self.scraped_params["phone"] = self.response.css("div.announcement-owner-contacts-main.js-owner-contacts > div.contacts-column.owner-contacts > ul > li > div::text").get()
        self.scraped_params["phone"] = self.scraped_params["phone"].strip() if self.scraped_params["phone"] is not None else None

        self.scrape_imgs()

class AutobilisAd(CarAd):

    def prepare_data(self):
        super().prepare_data()

        if self.prepared_params["mileage"] is not None:
            self.prepared_params["mileage"] = self.prepared_params["mileage"].replace(" ", "").replace("km", "")

    def convert_body_type(self):
        if self.scraped_params.get("body_type"):
            if "Kupė" in self.scraped_params["body_type"]:
                self.scraped_params["body_type"] = "Coupe"
            elif "Komercinis" in self.scraped_params["body_type"]:
                self.scraped_params["body_type"] = "Komercinis auto(su būda)"
            elif "Kabrioletas" in self.scraped_params["body_type"]:
                self.scraped_params["body_type"] = "Kabrioletas"

    def gen_location(self):
        location = self.response.css('div.owner-location::text').get()
        if self.scraped_params.get("country") and self.scraped_params.get("city"):
            self.scraped_params["location"] = self.scraped_params["country"] + ", " + self.scraped_params["city"]
        elif self.scraped_params.get("country"):
            self.scraped_params["location"] = self.scraped_params["country"]
        elif self.scraped_params.get("city"):
            self.scraped_params["location"] = self.scraped_params["city"]

    def gen_engine(self):
        if "engine_volume" in self.scraped_params and "power" in self.scraped_params:
            self.scraped_params["engine"] = f'{self.scraped_params["engine_volume"]} L, {self.scraped_params["power"]}'
        elif "engine_volume" in self.scraped_params:
            self.scraped_params["engine"] = f'{self.scraped_params["engine_volume"]} L'
        elif "power" in self.scraped_params:
            self.scraped_params["engine"] = f'{self.scraped_params["power"]}'

    def scrape_imgs(self):
        self.scraped_params["picture_href"] = []
        pic: str = self.response.css("div.single-item-wrapper div img::attr(src)").get()
        if pic is not None:
            self.scraped_params["picture_href"].append(pic.replace("big", "large", 1))
        for attr in self.response.css("div.single-item-wrapper div img::attr(data-lazy)"):
            pic = attr.get()
            if pic is not None:
                self.scraped_params["picture_href"].append(pic.replace("big", "large", 1))
    def parse(self):
        self.scraped_params["autob_id"] = self.response.url.split("/")[4]

        for row in self.response.css("div.row.car-info-r"):
            key = db_translations[row.css('div.col-sm-6.car-info-h > p::text').get().strip()]
            value = row.css('div.col-sm-6.car-info-c > p::text').get()
            self.scraped_params[key] = value.strip() if value is not None else None

        self.gen_engine()
        
        self.scraped_params["features"] = ""
        feature_block = self.response.css('div.advert-price-MainInfo-features')
        for feature in feature_block.css('span::text'):
            self.scraped_params["features"] += feature.get().strip() + ", "
        self.scraped_params["features"] = self.scraped_params["features"][:-2]

        
        comment_block = self.response.css("div.advert-price-MainInfo-comments")
        if comment_block is not None:
            comment = comment_block.css('div.advert-price-MainInfo-text > span::text').getall()
            if comment:
                self.scraped_params["comments"] = "\n".join(comment)

        self.gen_location()

        self.scraped_params["price"] = self.response.css('span.price-value::attr(data-price)').get().strip()

        self.scraped_params["fuel_overall"] = self.scraped_params.get("fuel_overall").split("l")[0] if "fuel_overall" in self.scraped_params and\
            self.scraped_params["fuel_overall"] else None
        self.db_driven_wheels()

        self.scraped_params["href"] = self.response.url

        self.scraped_params["picture_href"] = self.response.css("div.single-item-wrapper > div  img::attr(src)").get()
        self.scraped_params["picture_href"] = self.scraped_params["picture_href"].strip() if self.scraped_params["picture_href"] is not None else None
        
        self.convert_body_type()

        for row in self.response.css("div.clearfix"):
            vals = row.css("div::text").getall()
            if 0 in vals and vals[0] is not None and vals[0].strip() == "Telefonas":
                self.scraped_params["phone"] = vals[1].strip() if 1 in vals and vals[1] is not None else None
                
        self.scrape_imgs()