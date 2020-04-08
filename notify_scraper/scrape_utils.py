#!/usr/bin/env python3
# import scrapy
import sys
sys.path.insert(0, "..")
# from scrapy.crawler import CrawlerProcess
# from notify_scraper.notify_scraper.spiders.autogidas import AutogidasSpider
from database.database import connection, db_connect
from urllib.parse import urlencode

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

    # autoplius
    "Pagaminimo data":"year",
    "Rida":"mileage",
    "Varantieji ratai":"driven_wheels",
    "Klimato valdymas":"?0",
    "Ratlankių skersmuo":"wheels",
    "Tech. apžiūra iki":"ts_to",
    "Nuosava masė, kg":"weight",
    "Kuro bako talpa": "?1",
    "Paslaugos pavadinimas": "?2",
    "Paslaugos tipas":"?3",
    "Kėbulo numeris (VIN)":"vin_code",
    "Nauja / naudota":"?4",
    
    # empty for db columns
    "?0":"autog_id",
    "?1":"autop_id",
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
    new_params = {}
    if "make_model" in params and params["make_model"] is not None and "make" in params["make_model"]:
        new_params[f'f_1[0]'] = params["make_model"]["make"] or ""
    if "make_model" in params and params["make_model"] and "model_name" in params["make_model"]:
        new_params[f'f_model_14[0]'] = params["make_model"]["model_name"] or ""

    if "car_query" in params and params["car_query"] is not None:
        if "price_from" in params["car_query"]:
            new_params['f_215'] = params["car_query"]["price_from"] if params["car_query"]["price_from"] is not None else ""
        if "price_to" in params["car_query"]:
            new_params['f_216'] = params["car_query"]["price_to"] if params["car_query"]["price_to"] is not None else ""

        if "year_from" in params["car_query"]:
            new_params['f_41'] = params["car_query"]["year_from"] if params["car_query"]["year_from"] is not None else ""
        if "year_to" in params["car_query"]:
            new_params['f_42'] = params["car_query"]["year_to"] if params["car_query"]["year_to"] is not None else ""
        if "search_term" in params["car_query"] and params["car_query"]["search_term"] is not None:
            new_params['f_376'] = params["car_query"]["search_term"] if params["car_query"]["search_term"] is not None else ""

    if "body_style" in params and params["body_style"] is not None and "name" in params["body_style"]:
        new_params[f'f_3[0]'] = params["body_style"]["name"] if params["body_style"]["name"] is not None else ""
        
    if "fuel_type" in params and params["fuel_type"] is not None and "fuel_name" in params["fuel_type"]:
        new_params[f'f_2[0]'] = params["fuel_type"]["fuel_name"] if params["fuel_type"]["fuel_name"] is not None else ""
    
    
    
    return new_params

def form_autop_query(params):
    new_params = {}
    if "make_model" in params and params["make_model"] is not None and "autoplius_make_id" in params["make_model"]:
        new_params["make_id_list"] = params["make_model"]["autoplius_make_id"] or ""
    if "make_model" in params and params["make_model"] and "autoplius_model_id" in params["make_model"]:
        new_params[f"make_id[{new_params['make_id_list']}]"] = params["make_model"]["autoplius_model_id"] or ""

    if "car_query" in params and params["car_query"] is not None:
        if "price_from" in params["car_query"]:
            new_params["sell_price_from"] = params["car_query"]["price_from"] if params["car_query"]["price_from"] is not None else ""
        if "price_to" in params["car_query"]:
            new_params["sell_price_to"] = params["car_query"]["price_to"] if params["car_query"]["price_to"] is not None else ""

        if "year_from" in params["car_query"]:
            new_params["make_date_from"] = params["car_query"]["year_from"] if params["car_query"]["year_from"] is not None else ""
        if "year_to" in params["car_query"]:
            new_params["make_date_to"] = params["car_query"]["year_to"] if params["car_query"]["year_to"] is not None else ""
        if "search_term" in params["car_query"] and params["car_query"]["search_term"] is not None:
            new_params["qt"] = params["car_query"]["search_term"] if params["car_query"]["search_term"] is not None else ""

    if "body_style" in params and params["body_style"] is not None and "autoplius_id" in params["body_style"]:
        new_params["body_type_id"] = params["body_style"]["autoplius_id"] if params["body_style"]["autoplius_id"] is not None else ""
        
    if "fuel_type" in params and params["fuel_type"] is not None and "autoplius_fuel_id" in params["fuel_type"]:
        new_params["fuel_id"] = params["fuel_type"]["autoplius_fuel_id"] if params["fuel_type"]["autoplius_fuel_id"] is not None else ""
    
    
    
    return new_params

def get_car_query(id):
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM car_queries WHERE id=%s", id)
        car_query = cursor.fetchone()
        
        if car_query is None:
            return None

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