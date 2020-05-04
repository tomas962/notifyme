from .database import db_connect

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

        cursor.execute("""SELECT makes.*, makes.id as make_ID, models.* FROM query_make_model 
            LEFT JOIN makes 
            ON query_make_model.make_id=makes.id
            LEFT JOIN models
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

def get_all_car_queries():
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT car_queries.*, cities.city FROM `car_queries` LEFT JOIN cities on city_id=cities.id ")
        car_queries = cursor.fetchall()
        
        if len(car_queries) == 0:
            return []
            

        result = []
        for c_query in car_queries:
            cursor.execute("""SELECT fuel_types.* FROM query_fuel 
                INNER JOIN fuel_types 
                ON query_fuel.fuel_id=fuel_types.id
                """)
            fuel_type = cursor.fetchone()
            
            cursor.execute("""SELECT body_styles.* FROM `car_queries` 
                INNER JOIN query_body_style ON car_queries.id=query_body_style.query_id
                INNER JOIN body_styles ON query_body_style.body_style_id=body_styles.id
                """)
            body_style = cursor.fetchone()

            cursor.execute("""SELECT makes.make as make, models.model_name as model_name, makes.id as make_id, models.id as model_id FROM query_make_model 
                INNER JOIN makes 
                ON query_make_model.make_id=makes.id
                LEFT JOIN models
                ON query_make_model.model_id=models.id
                """)
            make_model = cursor.fetchone()
            result.append({
                "car_query":c_query,
                "fuel_type":fuel_type,
                "body_style":body_style,
                "make_model":make_model
            })
        cursor.connection.close()
        return result

def get_car_queries_by_user_id(user_id):
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT car_queries.*, cities.city FROM `car_queries` LEFT JOIN cities on city_id=cities.id WHERE user_id=%s", user_id)
        car_queries = cursor.fetchall()
        
        if len(car_queries) == 0:
            return []
            

        result = []
        for c_query in car_queries:
            cursor.execute("""SELECT fuel_types.* FROM query_fuel 
                INNER JOIN fuel_types 
                ON query_fuel.fuel_id=fuel_types.id
                WHERE query_fuel.query_id=%s""", (c_query["id"]))
            fuel_type = cursor.fetchone()
            
            cursor.execute("""SELECT body_styles.* FROM `car_queries` 
                INNER JOIN query_body_style ON car_queries.id=query_body_style.query_id
                INNER JOIN body_styles ON query_body_style.body_style_id=body_styles.id
                WHERE car_queries.id=%s""", (c_query["id"]))
            body_style = cursor.fetchone()

            cursor.execute("""SELECT makes.make as make, models.model_name as model_name, makes.id as make_id, models.id as model_id FROM query_make_model 
                INNER JOIN makes 
                ON query_make_model.make_id=makes.id
                LEFT JOIN models
                ON query_make_model.model_id=models.id
                WHERE query_make_model.query_id=%s""", (c_query["id"]))
            make_model = cursor.fetchone()
            result.append({
                "car_query":c_query,
                "fuel_type":fuel_type,
                "body_style":body_style,
                "make_model":make_model
            })
        cursor.connection.close()
        return result

def insert_car_query(cursor, query_values):
    cursor.execute("""INSERT INTO `car_queries`(`price_from`, `price_to`, 
            `year_from`, `search_term`, `year_to`, `power_from`, `power_to`, user_id, sites, city_id, was_scraped) 
            VALUES (%(price_from)s, %(price_to)s, %(year_from)s, %(search_term)s, 
            %(year_to)s, %(power_from)s, %(power_to)s, %(user_id)s, %(sites)s, %(city_id)s, %(was_scraped)s)""", query_values)
        
    query_values["id"] = cursor.lastrowid

    if query_values["fuel_id"] is not None:
        cursor.execute("""INSERT INTO `query_fuel`(`query_id`, `fuel_id`) 
            VALUES (%(id)s, %(fuel_id)s)""", query_values)

    if query_values["body_style_id"] is not None:
        cursor.execute("""INSERT INTO `query_body_style`(`query_id`, `body_style_id`) 
            VALUES (%(id)s, %(body_style_id)s)""", query_values)
    
    if query_values["make_id"] is not None:
        cursor.execute("""INSERT INTO `query_make_model`(`query_id`, `make_id`, `model_id`) 
            VALUES (%(id)s, %(make_id)s, %(model_id)s)""", query_values)
    return query_values["id"]

def update_car_query(cursor, query_values):
    cursor.execute("""UPDATE `car_queries` SET price_from=%(price_from)s, price_to=%(price_to)s, 
        year_from=%(year_from)s, search_term=%(search_term)s, 
        year_to=%(year_to)s, power_from=%(power_from)s, power_to=%(power_to)s, 
        user_id=%(user_id)s, sites=%(sites)s, city_id=%(city_id)s, was_scraped=%(was_scraped)s WHERE id=%(id)s AND user_id=%(user_id)s""", query_values)

    if query_values["fuel_id"] is not None:
        cursor.execute("SELECT * FROM query_fuel WHERE query_id=%(id)s", query_values)
        if cursor.fetchone():
            cursor.execute("""UPDATE `query_fuel` SET fuel_id=%(fuel_id)s WHERE query_id=%(id)s""", query_values)
        else:
            cursor.execute("""INSERT INTO `query_fuel`(`query_id`, `fuel_id`) 
                VALUES (%(id)s, %(fuel_id)s)""", query_values)

    if query_values["body_style_id"] is not None:
        cursor.execute("SELECT * FROM query_body_style WHERE query_id=%(id)s", query_values)
        if cursor.fetchone():
            cursor.execute("""UPDATE `query_body_style` SET
                body_style_id=%(body_style_id)s WHERE query_id=%(id)s""", query_values)
        else:
            cursor.execute("""INSERT INTO `query_body_style`(`query_id`, `body_style_id`) 
                VALUES (%(id)s, %(body_style_id)s)""", query_values)

    if query_values["make_id"] is not None:
        cursor.execute("SELECT * FROM query_make_model WHERE query_id=%(id)s", query_values)
        if cursor.fetchone():
            cursor.execute("""UPDATE `query_make_model` SET
                make_id=%(make_id)s, model_id=%(model_id)s WHERE query_id=%(id)s""", query_values)
        else:
            cursor.execute("""INSERT INTO `query_make_model`(`query_id`, `make_id`, `model_id`) 
                VALUES (%(id)s, %(make_id)s, %(model_id)s)""", query_values)

    cursor.execute("DELETE FROM query_car_fk WHERE query_id=%(id)s", query_values)

def delete_car_query(user_id, query_id):
    with db_connect().cursor() as cursor:
        cursor.execute("DELETE FROM car_queries WHERE id=%s AND user_id=%s", (query_id, user_id))
        cursor.connection.commit()
        cursor.connection.close()
        return True