from scrapy.responsetypes import Response
from database.database import db_connect
import re
import pymysql

re_db_mappings = {
    # skelbiu.lt
    "Gyvenvietė":"village",
    "Gatvė":"street",
    "Plotas, m²":"area",
    "Įrengimas":"installation",
    "Aukštas":"floor",
    "Metai":"year",
    "Šildymas":"heating",
    "Ypatybės":"features",
    "Mikrorajonas":"neighborhood",
    "Namo numeris":"house_number",
    "Kamb. sk":"room_count",
    "Tipas":"house_type",
    "Aukštų skaičius":"floor_count",
    "Energetinė klasė":"energy_class",
    "Sklypo plotas, a":"site_area",
    "Kamb. sk.":"room_count",
    "Pastato tipas":"type",

    # domoplius
    "Kaina":"price",
    "1 kv. m kaina":"price_per_area",
    "Bendras pastato plotas":"area",
    "Kambarių skaičius":"room_count",
    "Statybos metai":"year",
    "Sklypo plotas":"site_area",
    "Namo būklė":"installation",
    "Namo tipas":"type",
    "Rekonstrukcijos metai":"year_reconstructed",
    "Energinio naudingumo klasė":"energy_class",
    "Vandentiekis":"water",
    "Kanalizacija":"sewage",
    "Dujos":"gas",
    "Buto plotas (kv. m)":"area",
    "Būklė":"installation",
    "Plotas, a":"site_area",

    "?":"city",
    "?1":"city_id",
    "?2":"href",
    "?3":"skelbiu_id",
    "?4":"domo_id",
    "?5":"title",
    "?6":"house_type",
    "?7":"description",
    "?8":"price",
    "?9":"price_per_area",
    "?10":"phone",
    "?11":"href",
    "?12":"query_id",
    "?13":"pictures",


    "Naudingas plotas (kv. m)": "?",
    "Žemės paskirtis":"?",
    "Garažo plotas (kv. m)":"?",
    "Rūsio plotas (kv. m)":"?",
    "Pamatai":"?",
    "Langai":"?",
    "Stogas":"?",
    "Stogo danga":"?",
    "Perdanga": "?",
    "Išorės apdaila": "?",
    "Paskirtis": "?",
    "1 aro kaina": "?",
    "1 hektaro kaina": "?",
    "Matavimų tipas": "?",
}

class ReAd():

    def __init__(self, response: Response, query_id):
        self.query_id = query_id
        self.response = response
        self.scraped_params = {}
        self.prepared_data = {}
        self.scraped_params["query_id"] = query_id

    def extract_relevant_attributes(self):
        """Extracts only relevant attributes, to return for later data processing."""
        ad = {}
        ad["id"] = self.prepared_data["id"]
        ad["city_id"] = self.prepared_data["city_id"]
        ad["city"] = self.prepared_data["city"]
        ad["title"] = self.prepared_data["title"]
        ad["village"] = self.prepared_data["village"]
        ad["installation"] = self.prepared_data["installation"]
        ad["type"] = self.prepared_data["type"]
        ad["house_type"] = self.prepared_data["house_type"]
        ad["year"] = self.prepared_data["year"]
        ad["site_area"] = self.prepared_data["site_area"]
        ad["heating"] = self.prepared_data["heating"]
        ad["area"] = self.prepared_data["area"]
        ad["street"] = self.prepared_data["street"]
        ad["description"] = self.prepared_data["description"]
        ad["floor"] = self.prepared_data["floor"]
        ad["neighborhood"] = self.prepared_data["neighborhood"]
        ad["energy_class"] = self.prepared_data["energy_class"]
        ad["floor_count"] = self.prepared_data["floor_count"]
        ad["features"] = self.prepared_data["features"]
        ad["price"] = self.prepared_data["price"]
        ad["price_per_area"] = self.prepared_data["price_per_area"]
        ad["phone"] = self.prepared_data["phone"]
        ad["skelbiu_id"] = self.prepared_data["skelbiu_id"]
        ad["domo_id"] = self.prepared_data["domo_id"]
        ad["href"] = self.prepared_data["href"]
        ad["room_count"] = self.prepared_data["room_count"]
        ad["year_reconstructed"] = self.prepared_data["year_reconstructed"]
        ad["water"] = self.prepared_data["water"]
        ad["sewage"] = self.prepared_data["sewage"]
        ad["gas"] = self.prepared_data["gas"]
        ad["pictures"] = self.prepared_data["pictures"]
        ad["query_id"] = self.prepared_data["query_id"]
        return ad

    def prepare_data(self):
        for title, db_col in re_db_mappings.items():
            self.prepared_data[db_col] = self.scraped_params.get(db_col)


    def _foreign_keys(self):
        with db_connect().cursor() as cursor:
            cursor.execute("""SELECT id FROM re_cities WHERE city=%(city)s""", self.prepared_data)
            ct = cursor.fetchone()
            self.prepared_data["city_id"] = ct.get("id")
            cursor.connection.close()

    def _site(self):
        if self.prepared_data.get("skelbiu_id"):
            self.prepared_data["key_column"] = "skelbiu_id"
            self.prepared_data["key_value"] = self.prepared_data.get("skelbiu_id")
        elif self.prepared_data.get("domo_id"):
            self.prepared_data["key_column"] = "domo_id"
            self.prepared_data["key_value"] = self.prepared_data.get("domo_id")

    def insert_ad(self):
        self._site()
        self._foreign_keys()
        with db_connect().cursor() as cursor:
            cursor.execute(f"SELECT id FROM re_ads WHERE {self.prepared_data['key_column']}=%(key_value)s", self.prepared_data)
            ad_in_db = cursor.fetchone()

            if ad_in_db:
                self.prepared_data["id"] = ad_in_db["id"]
                cursor.execute(f"""UPDATE re_ads SET `city_id`=%(city_id)s, `title`=%(title)s, 
                    `village`=%(village)s, `installation`=%(installation)s, `type`=%(type)s, 
                    `house_type`=%(house_type)s, `year`=%(year)s, `site_area`=%(site_area)s, 
                    `heating`=%(heating)s, `area`=%(area)s, `street`=%(street)s, 
                    `description`=%(description)s, `floor`=%(floor)s, `neighborhood`=%(neighborhood)s, 
                    `energy_class`=%(energy_class)s, `floor_count`=%(floor_count)s, `features`=%(features)s, 
                    `price`=%(price)s, `price_per_area`=%(price_per_area)s, `phone`=%(phone)s, 
                    {self.prepared_data['key_column']}=%(key_value)s, `room_count`=%(room_count)s, 
                    href=%(href)s, when_scraped=unix_timestamp(), year_reconstructed=%(year_reconstructed)s, 
                    water=%(water)s, sewage=%(sewage)s, gas=%(gas)s
                    WHERE id=%(id)s""", self.prepared_data)
                
                try:
                    cursor.execute("INSERT INTO re_query_ad_fk (query_id, re_ad_id) VALUES (%(query_id)s, %(id)s)", self.prepared_data)
                except pymysql.IntegrityError as err:
                    print("RE ad already existed: ")
                    print(err)
                
                try:
                    cursor.executemany("INSERT INTO `re_ad_pictures`(`re_ad_id`, `picture_href`) VALUES (%s, %s)",
                        [(self.prepared_data["id"], p_href) for p_href in self.prepared_data["pictures"]])
                except pymysql.IntegrityError as err:
                    print("Picture already exists: ")
                    print(err)
            else:
                cursor.execute(f"""INSERT INTO `re_ads`(`city_id`, `title`, `village`, `installation`, 
                    `type`, `house_type`, `year`, `site_area`, `heating`, `area`, `street`, `description`, 
                    `floor`, `neighborhood`, `energy_class`, `floor_count`, `features`, `price`, `price_per_area`, 
                    `phone`, {self.prepared_data['key_column']}, `room_count`, href, when_scraped, year_reconstructed, 
                    water, sewage, gas) 
                    VALUES (%(city_id)s, %(title)s, %(village)s, %(installation)s, %(type)s, %(house_type)s, %(year)s, 
                    %(site_area)s, %(heating)s, %(area)s, %(street)s, %(description)s, %(floor)s, %(neighborhood)s, 
                    %(energy_class)s, %(floor_count)s, %(features)s, %(price)s, %(price_per_area)s, %(phone)s, 
                    %(key_value)s, %(room_count)s, %(href)s, unix_timestamp(), %(year_reconstructed)s, %(water)s, 
                    %(sewage)s, %(gas)s)""", self.prepared_data)
                self.prepared_data["id"] = cursor.lastrowid

                cursor.execute("INSERT INTO re_query_ad_fk (query_id, re_ad_id) VALUES (%(query_id)s, %(id)s)", self.prepared_data)

                cursor.executemany("INSERT INTO `re_ad_pictures`(`re_ad_id`, `picture_href`) VALUES (%s, %s)",
                        [(self.prepared_data["id"], p_href) for p_href in self.prepared_data["pictures"]])

            cursor.connection.commit()
            cursor.connection.close()
            return self.extract_relevant_attributes()
        
class SkelbiuAd(ReAd):

    def parse(self):
        for row in self.response.css(".detail"):
            title = row.css(".title::text").get()
            title = title.strip(" :") if title else None
            data = row.css(".value::text").get()
            data = data.strip() if data else None
            if title and data:
                self.scraped_params[re_db_mappings[title]] = data
        

        title = self.response.css("div.left-block > h1::text").get()
        self.scraped_params["title"] = title.strip() if title else None

        city = self.response.css("div.left-block > p::text").getall()
        if len(city) > 0:
            city = "".join(city)
            self.scraped_params["city"] = city.strip() if city else None

        price = self.response.css("div.right-block > p.price::text").get()
        self.scraped_params["price"] = price.strip(" €").replace(" ", "") if price else None

        price_area = self.response.css("div.right-block > p.price-for-unit::text").get()
        price_area = price_area.strip() if price_area else None
        if price_area:
            if price_area[len(price_area)-1] == "m":
                price_area += "²"
            self.scraped_params["price_per_area"] = price_area

        description = self.response.css("div.item-description > div::text").getall()
        if len(description) > 0:
            description = [x.strip() for x in description]
            if description[len(description)-1] == "Rodyti daugiau":
                description.pop(len(description)-1)
            description = "\n".join(description)
            self.scraped_params["description"] = description.strip() if description else None

        self.scraped_params["href"] = self.response.url

        self.scraped_params["skelbiu_id"] = self.response.url.split('-').pop().split('.')[0]
        
        phone = self.response.css("div.phone-button > div.primary::text").get()
        self.scraped_params["phone"] = phone.strip() if phone else None

        features = self.response.css(".values > .value::text").getall()
        if features:
            features = [x.strip() for x in features]
            self.scraped_params["features"] = "|".join(features)

        pictures = []
        for script in self.response.css("body > script::text").getall():
            s = script.strip()
            if s.startswith("var adId"):
                for line in s.splitlines():
                    if "full_size_src" in line:
                        pictures.append(line.split("'")[1])
                break
        
        self.scraped_params["pictures"] = pictures

class DomoAd(ReAd):

    def parse(self):
        print("parse called")
        for row in self.response.css(".view-group tr"):
            title = row.css("th::text").get()
            title = title.strip("\n\t :") if title else None
            value = row.css("td > strong::text").get()
            value = value.strip() if value else None
            if value and title:
                self.scraped_params[re_db_mappings[title]] = value

        if "price" in self.scraped_params:
            self.scraped_params["price"] = self.scraped_params["price"].strip(" €").replace(" ","")


        idx = -1
        for row in self.response.css("div.medium.info-block > div"):
            idx -= 1
            if idx >= 0:
                if idx == 0:
                    descr = row.css("::text").getall()
                    self.scraped_params["description"] = "".join(descr)
                    break
            else:
                text = row.css("::text").getall()
                text = "".join(text).strip()
                if text.startswith("Komentarai"):
                    idx = 2

        feature_list = []
        for ft in self.response.css("li.fr::text").getall():
            feature_list.append(ft.strip())
        for ft in self.response.css("li.fl::text").getall():
            feature_list.append(ft.strip())

        self.scraped_params["features"] = "|".join(feature_list)

        title = self.response.css(".fl.title-view::text").get()
        self.scraped_params["title"] = title.strip() if title else None

        self.scraped_params["href"] = self.response.url
        self.scraped_params["domo_id"] = self.response.url.split("-").pop().split(".")[0]

        city = self.response.css("div.breadcrumb > div:nth-child(1) > a > span::text").get()
        self.scraped_params["city"] = city.replace("sav.", "").strip()
        

        pictures = []
        for pic in self.response.css(".small-thumbs img::attr(src)").getall():
            pictures.append(pic.replace("_small", "_big"))
        self.scraped_params["pictures"] = pictures