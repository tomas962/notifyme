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