from database.database import db_connect

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

def get_car_queries_by_user_id(user_id):
    with db_connect().cursor() as cursor:
        cursor.execute("SELECT * FROM car_queries WHERE user_id=%s", user_id)
        car_queries = cursor.fetchall()
        
        if len(car_queries) == 0:
            return None
            

        result = []
        for c_query in car_queries:
            print(c_query["id"])

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

            cursor.execute("""SELECT makes.*, models.*, makes.id as make_id, models.id as model_id FROM query_make_model 
                INNER JOIN makes 
                ON query_make_model.make_id=makes.id
                INNER JOIN models
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