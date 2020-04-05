#!/usr/bin/env python3
# import scrapy
import sys
sys.path.insert(0, "..")
# from scrapy.crawler import CrawlerProcess
# from notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider
from database.database import connection, db_connect
from urllib.parse import urlencode

db_translations = {
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
    "VIN kodas":"vin_code"
}
# f_1[0]: BMW
# f_model_14[0]: Series 3
# f_215: 
# f_216: 4000
# f_41: 2002
# f_42: 2014
# f_3[1]: Sedanas
# f_3[2]: Hečbekas
# f_3[3]: Universalas
# f_2[1]: Dyzelinas
# f_2[2]: Benzinas
# f_376:
def form_autog_query(params):
    print(f"PARAMS: {params}")
    new_params = {}
    if "make_model" in params and params["make_model"] is not None and "make" in params["make_model"]:
        new_params[f'f_1[0]'] = params["make_model"]["make"] or ""
    if "make_model" in params and params["make_model"] and "model_name" in params["make_model"]:
        new_params[f'f_model_14[0]'] = params["make_model"]["model_name"] or ""

    if "price_from" in params["car_query"]:
        new_params['f_215'] = params["car_query"]["price_from"] if params["car_query"]["price_from"] is not None else ""
    if "price_to" in params["car_query"]:
        new_params['f_216'] = params["car_query"]["price_to"] if params["car_query"]["price_to"] is not None else ""

    if "year_from" in params["car_query"]:
        new_params['f_41'] = params["car_query"]["year_from"] if params["car_query"]["year_from"] is not None else ""
    if "year_to" in params["car_query"]:
        new_params['f_42'] = params["car_query"]["year_to"] if params["car_query"]["year_to"] is not None else ""

    if "body_style" in params and params["body_style"] is not None and "name" in params["body_style"]:
        new_params[f'f_3[0]'] = params["body_style"]["name"] if params["body_style"]["name"] is not None else ""
        
    if "fuel_type" in params and params["fuel_type"] is not None and "fuel_name" in params["fuel_type"]:
        new_params[f'f_2[0]'] = params["fuel_type"]["fuel_name"] if params["fuel_type"]["fuel_name"] is not None else ""
    
    if "search_term" in params["car_query"] and params["car_query"]["search_term"] is not None:
        new_params['f_376'] = params["car_query"]["search_term"] if params["car_query"]["search_term"] is not None else ""
    
    return new_params

def get_car_query(id):
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM car_queries WHERE id=%s", id)
        car_query = cursor.fetchone()
        
        cursor.execute("""SELECT fuel_types.* FROM query_fuel 
            INNER JOIN fuel_types 
            ON query_fuel.fuel_id=fuel_types.id
            WHERE query_fuel.query_id=%s""", id)
        fuel_type = cursor.fetchone()
        
        cursor.execute("""SELECT body_styles.* FROM `car_queries` 
            INNER JOIN query_body_style ON car_queries.id=query_body_style.query_id
            INNER JOIN body_styles ON query_body_style.body_style_id=body_styles.id
            WHERE car_queries.id=%s""", id)
        body_style = cursor.fetchone()

        cursor.execute("""SELECT makes.*, models.* FROM query_make_model 
            INNER JOIN makes 
            ON query_make_model.make_id=makes.id
            INNER JOIN models
            ON query_make_model.model_id=models.id
            WHERE query_make_model.query_id=%s""", id)
        make_model = cursor.fetchone()

        cursor.connection.close()
        return {
            "car_query":car_query,
            "fuel_type":fuel_type,
            "body_style":body_style,
            "make_model":make_model
        }


def prepare_data(params):
    """
        Prepare data for insertion into database.  
        Add None where neccesary and convert to integers.
    """
    for k, v in db_translations.items():
        params[v] = params.get(v) # add None entries if doesn't exist

    params["price"] = int(params["price"].split("€")[0].replace(" ", "")) if params["price"] is not None else None
    params["export_price"] = int(params["export_price"].split("€")[0].replace(" ", "")) if params["export_price"] is not None else None
    params["year"] = params["year"].split(" ")[0] if params["year"] is not None else None
    params["weight"] = int(params["weight"].split(" ")[0]) if params["weight"] is not None else None
    params["ts_to"] = params["ts_to"] + "-01" if params["ts_to"] is not None else None
    return params        

def autog_foreign_keys(values, cursor):
    # convert values to ID's
    if values["make"] is not None:
        cursor.execute("SELECT * from makes WHERE make=%s", values["make"])
        make = cursor.fetchone()
        values["make"] = make["id"]
    if values["model"] is not None:
        cursor.execute("SELECT * from models WHERE make_id=%s AND model_name=%s", (values["make"], values["model"]))
        model = cursor.fetchone()
        values["model"] = model["id"]
    if values["fuel_type"] is not None:
        cursor.execute("SELECT * from fuel_types WHERE fuel_name=%s", values["fuel_type"])
        fuel = cursor.fetchone()
        values["fuel_type"] = fuel["id"]
    if values["body_type"] is not None:
        cursor.execute("SELECT * from body_styles WHERE name=%s", values["body_type"])
        body_t = cursor.fetchone()
        values["body_type"] = body_t["id"]
    return values

def insert_autog_ad(values):
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM car_ads WHERE autog_id=%s", values["autog_id"])
        ad_exists = cursor.fetchone()
        values = autog_foreign_keys(values, cursor)
        if ad_exists:
            cursor.execute("""UPDATE `car_ads` SET make=%(make)s, model=%(model)s, year=%(year)s, engine=%(engine)s,
                fuel_type=%(fuel_type)s, body_type=%(body_type)s, 
                color=%(color)s, gearbox=%(gearbox)s, driven_wheels=%(driven_wheels)s, damage=%(damage)s,
                steering_column=%(steering_column)s,
                door_count=%(door_count)s, cylinder_count=%(cylinder_count)s, gear_count=%(gear_count)s, 
                seat_count=%(seat_count)s, ts_to=DATE(%(ts_to)s), weight=%(weight)s, 
                wheels=%(wheels)s, fuel_urban=%(fuel_urban)s, fuel_overland=%(fuel_overland)s, 
                fuel_overall=%(fuel_overall)s, features=%(features)s, comments=%(comments)s, 
                autog_id=%(autog_id)s, price=%(price)s, export_price=%(export_price)s, vin_code=%(vin_code)s
                WHERE autog_id=%(autog_id)s""", values)
            
        else:
            cursor.execute("""INSERT INTO `car_ads`(`make`, `model`, `year`, `engine`, `fuel_type`, 
                `body_type`, `color`, `gearbox`, `driven_wheels`, `damage`, `steering_column`, `door_count`, 
                `cylinder_count`, `gear_count`, `seat_count`, `ts_to`, `weight`, `wheels`, `fuel_urban`, 
                `fuel_overland`, `fuel_overall`, `features`, `comments`, `autog_id`, `price`, `export_price`, `vin_code`) 
                VALUES (%(make)s, %(model)s, %(year)s, %(engine)s, %(fuel_type)s, %(body_type)s, 
                %(color)s, %(gearbox)s, %(driven_wheels)s, %(damage)s, %(steering_column)s,
                %(door_count)s, %(cylinder_count)s, %(gear_count)s, %(seat_count)s, DATE(%(ts_to)s), %(weight)s, 
                %(wheels)s, %(fuel_urban)s, %(fuel_overland)s, %(fuel_overall)s, %(features)s, %(comments)s, 
                %(autog_id)s, %(price)s, %(export_price)s, %(vin_code)s)""", values)
        cursor.connection.commit()
        cursor.connection.close()

if __name__ == "__main__":
    params = {
            "price": "2 200 \u20ac",
            "make": "Audi",
            "model": "A4",
            "year": "2000/04 m.",
            "engine": "1.8 l. 92 kW (125 Ag)",
            "fuel_type": "Benzinas",
            "body_type": "Sedanas",
            "color": "M\u0117lyna",
            "gearbox": "Automatin\u0117",
            "mileage": "208000 km",
            "driven_wheels": "Priekiniai varantys ratai",
            "damage": "Be defekt\u0173",
            "steering_column": "Kair\u0117je",
            "door_count": "4/5",
            "wheels": "R15",
            "first_reg_country": "Vokietija",
            "fuel_urban": "11.0",
            "fuel_overland": "8.5",
            "fuel_overall": "10.0"
        }
    values = prepare_data(params)
    insert_ad(values) 
    # process = CrawlerProcess()
    # process.crawl(AutogidasSpider)
    # process.start() # the script will block here until all crawling jobs are finished
    # pass