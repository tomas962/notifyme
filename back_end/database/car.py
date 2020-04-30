from .database import db_connect

def get_cars_by_query_id(query_id):
    with db_connect().cursor() as cursor:
        cursor.execute("""SELECT *, makes.make as make_name, models.model_name as model_name,
            body_styles.name as body_type_name, fuel_types.fuel_name as fuel_name
            FROM car_ads 
            JOIN makes ON car_ads.make=makes.id
            JOIN models ON car_ads.model=models.id
            JOIN body_styles ON car_ads.body_type=body_styles.id
            JOIN fuel_types ON car_ads.fuel_type=fuel_types.id WHERE car_ads.query_id=%s""", query_id)
        car_ads = cursor.fetchall()
        cursor.connection.close()
        return car_ads
    