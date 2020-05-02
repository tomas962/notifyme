from .database import db_connect

def get_cars_by_query_id(query_id):
    with db_connect().cursor() as cursor:
        cursor.execute("""SELECT *, makes.make as make_name, models.model_name as model_name,
            body_styles.name as body_type_name, fuel_types.fuel_name as fuel_name FROM `query_car_fk` 
            JOIN car_ads ON query_car_fk.car_id=car_ads.id
            LEFT JOIN makes ON car_ads.make=makes.id
            LEFT JOIN models ON car_ads.model=models.id
            LEFT JOIN body_styles ON car_ads.body_type=body_styles.id
            LEFT JOIN fuel_types ON car_ads.fuel_type=fuel_types.id
            WHERE query_car_fk.query_id=%s AND car_ads.deleted=0""", query_id)
        car_ads = cursor.fetchall()
        cursor.connection.close()
        return car_ads
    
def mark_as_deleted_multiple_cars_by_id(car_ids: list):
    with db_connect().cursor() as cursor:
        cursor.executemany("UPDATE `car_ads` SET deleted=1 WHERE car_ads.id=%s", car_ids)
        cursor.connection.commit()
        cursor.connection.close()

def get_car_by_id(car_id):
    with db_connect().cursor() as cursor:
        cursor.execute("""SELECT *, makes.make as make_name, models.model_name as model_name,
            body_styles.name as body_type_name, fuel_types.fuel_name as fuel_name FROM `car_ads`
            LEFT JOIN makes ON car_ads.make=makes.id
            LEFT JOIN models ON car_ads.model=models.id
            LEFT JOIN body_styles ON car_ads.body_type=body_styles.id
            LEFT JOIN fuel_types ON car_ads.fuel_type=fuel_types.id
            WHERE car_ads.id=%s AND car_ads.deleted=0""", car_id)
        car_ad = cursor.fetchone()
        cursor.connection.close()
        return car_ad