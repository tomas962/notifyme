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
        print(re_query)
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

def update_re_query(re_query):
    with db_connect().cursor() as cursor:
        cursor.execute("""UPDATE `re_queries` SET `city_id`=%(city_id)s, `house_type_id`=%(house_type_id)s, 
            `type_id`=%(type_id)s, `category_id`=%(category_id)s, `search_term`=%(search_term)s,
            `price_from`=%(price_from)s, `price_to`=%(price_to)s, `area_from`=%(area_from)s, 
            `area_to`=%(area_to)s, `rooms_from`=%(rooms_from)s, `rooms_to`=%(rooms_to)s, `year_from`=%(year_from)s, 
            `year_to`=%(year_to)s, user_id=%(user_id)s, sites=%(sites)s, was_scraped=0 WHERE id=%(id)s""", 
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
            re_categories.skelbiu_id as skelbiu_category_id, scrape_interval, last_scraped, was_scraped, 
            currently_scraping
            FROM `re_queries` 
            LEFT JOIN re_cities ON city_id=re_cities.id
            LEFT JOIN re_house_type ON house_type_id=re_house_type.id
            LEFT JOIN re_types ON type_id=re_types.id
            LEFT JOIN re_categories ON category_id=re_categories.id 
            WHERE re_queries.id=%s""", query_id)
        query = cursor.fetchone()
        cursor.connection.close()
        return query

def get_user_re_queries(user_id):
    with db_connect().cursor() as cursor:
        cursor.execute("""SELECT  re_queries.id as id, `user_id`, `city_id`, `house_type_id`, `type_id`,
            `category_id`, `search_term`, `price_from`, `price_to`, `area_from`, `area_to`,
            `rooms_from`, `rooms_to`, `year_from`, `year_to`, `sites`, re_cities.city as city,
            re_cities.domo_id as domo_city_id, re_cities.skelbiu_id as skelbiu_city_id,
            re_house_type.name as house_type_name, re_house_type.skelbiu_id as skelbiu_house_type_id,
            re_house_type.domo_id as domo_house_type_id, re_types.name as type_name,
            re_types.skelbiu_id as skelbiu_type_id, re_types.domo_id as domo_type_id,
            re_categories.name as category_name, re_categories.domo_id as domo_category_id,
            re_categories.skelbiu_id as skelbiu_category_id, scrape_interval, last_scraped, was_scraped, 
            currently_scraping
            FROM `re_queries` 
            LEFT JOIN re_cities ON city_id=re_cities.id
            LEFT JOIN re_house_type ON house_type_id=re_house_type.id
            LEFT JOIN re_types ON type_id=re_types.id
            LEFT JOIN re_categories ON category_id=re_categories.id 
            WHERE re_queries.user_id=%s""", user_id)
        queries = cursor.fetchall()
        cursor.connection.close()
        return queries

def delete_re_query(user_id, query_id):
    with db_connect().cursor() as cursor:
        cursor.execute("DELETE FROM re_queries WHERE id=%s AND user_id=%s", (query_id, user_id))
        cursor.connection.commit()
        cursor.connection.close()
        return True


def get_query_re_ads(query_id):
    with db_connect().cursor() as cursor:
        cursor.execute("""SELECT re_ads.*, re_cities.city AS city  FROM `re_ads` 
            JOIN re_query_ad_fk ON re_query_ad_fk.re_ad_id=re_ads.id
            JOIN re_cities ON re_cities.id=re_ads.city_id
            WHERE re_query_ad_fk.query_id=%s AND re_ads.deleted=0
            """, query_id)
        re_ads = cursor.fetchall()

        for ad in re_ads:
            cursor.execute("SELECT * FROM re_ad_pictures WHERE re_ad_id=%s", ad["id"])
            ad["pictures"] = [x["picture_href"] for x in cursor.fetchall()]

        cursor.connection.close()
        return re_ads

def get_re_ad(re_ad_id):
    with db_connect().cursor() as cursor:
        cursor.execute("""SELECT re_ads.*, re_cities.city AS city  FROM `re_ads` 
            JOIN re_cities ON re_cities.id=re_ads.city_id
            WHERE re_ads.id=%s AND re_ads.deleted=0
            """, re_ad_id)
        re_ad = cursor.fetchone()

        cursor.execute("SELECT * FROM re_ad_pictures WHERE re_ad_id=%s", re_ad["id"])
        re_ad["pictures"] = [x["picture_href"] for x in cursor.fetchall()]

        cursor.connection.close()
        return re_ad

def get_all_re_queries():
    with db_connect().cursor() as cursor:
        cursor.execute("""SELECT  re_queries.id as id, `user_id`, `city_id`, `house_type_id`, `type_id`,
            `category_id`, `search_term`, `price_from`, `price_to`, `area_from`, `area_to`,
            `rooms_from`, `rooms_to`, `year_from`, `year_to`, `sites`, re_cities.city as city,
            re_cities.domo_id as domo_city_id, re_cities.skelbiu_id as skelbiu_city_id,
            re_house_type.name as house_type_name, re_house_type.skelbiu_id as skelbiu_house_type_id,
            re_house_type.domo_id as domo_house_type_id, re_types.name as type_name,
            re_types.skelbiu_id as skelbiu_type_id, re_types.domo_id as domo_type_id,
            re_categories.name as category_name, re_categories.domo_id as domo_category_id,
            re_categories.skelbiu_id as skelbiu_category_id, scrape_interval, last_scraped, was_scraped, 
            currently_scraping
            FROM `re_queries` 
            LEFT JOIN re_cities ON city_id=re_cities.id
            LEFT JOIN re_house_type ON house_type_id=re_house_type.id
            LEFT JOIN re_types ON type_id=re_types.id
            LEFT JOIN re_categories ON category_id=re_categories.id 
            """, )
        queries = cursor.fetchall()
        cursor.connection.close()
        return queries


def mark_re_ads_as_deleted(ad_ids: list):
    with db_connect().cursor() as cursor:
        cursor.executemany("UPDATE `re_ads` SET deleted=1 WHERE re_ads.id=%s", ad_ids)
        cursor.connection.commit()
        cursor.connection.close()