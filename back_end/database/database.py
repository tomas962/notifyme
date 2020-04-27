import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='phpmyadmin',
                             password='kompas88',
                             db='notify',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def db_connect():
    return pymysql.connect(host='localhost',
                             user='phpmyadmin',
                             password='kompas88',
                             db='notify',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         pass
#         # Create a new record
#         # sql = "SELECT FROM `users` (`email`, `password`) VALUES (%s, %s)"
#         # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT * FROM `makes` where `car_id`=%s"
#         cursor.execute(sql, ("6"))
#         result = cursor.fetchall()
#         print(result)
# finally:
#     connection.close()