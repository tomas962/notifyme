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
    "Klimato valdymas":"climate_control",
    "Ratlankių skersmuo":"wheels",
    "Tech. apžiūra iki":"ts_to",
    "Nuosava masė, kg":"weight",
    "Kuro bako talpa": "?1",
    "Paslaugos pavadinimas": "?2",
    "Paslaugos tipas":"?3",
    "Kėbulo numeris (VIN)":"vin_code",
    "Nauja / naudota":"?4",

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

    
    # empty for db columns
    "?0":"autog_id",
    "?1":"autop_id",
    "?2":"autob_id",
}


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