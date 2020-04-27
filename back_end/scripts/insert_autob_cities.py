import sys
sys.path.insert(0,'..')
from database.database import db_connect
from pymysql.cursors import DictCursor

count = 0
affected = 0
with open("autob_cities_v2.txt", "r") as f:
    lines = f.readlines()
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor: DictCursor
        for line in lines:
            words = line.split(" ", 1)
            
            prev = affected
            affected += cursor.execute("UPDATE `cities` SET `autob_id`=%s WHERE city=%s", (words[0].strip(), words[1].strip()))
            if prev == affected:
                print("couldn't find this city: " + words[1].strip())
            count += 1

    print("total rows:")
    print(count)
    print("affected rows:")
    print(affected)
    conn.commit()
    conn.close()