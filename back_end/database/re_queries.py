from database.database import db_connect


def get_re_cities():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM `re_cities`")
        cities = cursor.fetchall()
        cursor.connection.close()
        return cities

def get_re_categories():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM `re_categories`")
        categories = cursor.fetchall()
        cursor.connection.close()
        return categories

def get_re_types():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM `re_types`")
        data = cursor.fetchall()
        cursor.connection.close()
        return data

def get_re_house_types():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM `re_house_type`")
        data = cursor.fetchall()
        cursor.connection.close()
        return data

def insert_re_query(re_query):
    with db_connect().cursor() as cursor:
        cursor.execute("""INSERT INTO `re_queries`(`city_id`, `house_type_id`, `type_id`, 
            `category_id`, `search_term`, `price_from`, `price_to`, `area_from`, `area_to`, 
            `rooms_from`, `rooms_to`, `year_from`, `year_to`, user_id, sites) 
            VALUES (%(city_id)s, %(house_type_id)s, %(type_id)s, %(category_id)s, %(search_term)s, %(price_from)s,
            %(price_to)s, %(area_from)s, %(area_to)s, %(rooms_from)s, %(rooms_to)s, %(year_from)s, %(year_to)s, %(user_id)s,
            %(sites)s)""", 
            re_query)
        cursor.connection.commit()
        cursor.connection.close()
        return cursor.lastrowid

def get_re_query(query_id):
    with db_connect().cursor() as cursor:
        cursor.execute("""SELECT  re_queries.id as id, `user_id`, `city_id`, `house_type_id`, `type_id`,
            `category_id`, `search_term`, `price_from`, `price_to`, `area_from`, `area_to`,
            `rooms_from`, `rooms_to`, `year_from`, `year_to`, `sites`, re_cities.city as city,
            re_cities.domo_id as domo_city_id, re_cities.skelbiu_id as skelbiu_city_id,
            re_house_type.name as house_type_name, re_house_type.skelbiu_id as skelbiu_house_type_id,
            re_house_type.domo_id as domo_house_type_id, re_types.name as type_name,
            re_types.skelbiu_id as skelbiu_type_id, re_types.domo_id as domo_type_id,
            re_categories.name as category_name, re_categories.domo_id as domo_category_id,
            re_categories.skelbiu_id as skelbiu_category_id 
            FROM `re_queries` 
            LEFT JOIN re_cities ON city_id=re_cities.id
            LEFT JOIN re_house_type ON house_type_id=re_house_type.id
            LEFT JOIN re_types ON type_id=re_types.id
            LEFT JOIN re_categories ON category_id=re_categories.id 
            WHERE re_queries.id=%s""", query_id)
        query = cursor.fetchone()
        cursor.connection.close()
        return query