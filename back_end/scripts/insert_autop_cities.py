import sys
sys.path.insert(0,'..')
from database.database import db_connect

with open("autop_cities_v2.txt", "r") as f:
    lines = f.readlines()
    conn = db_connect()
    with conn.cursor() as cursor:
        for line in lines:
            words = line.split("\\", 1)
            
            words[1] = words[1].encode('utf-8')
            words[1] = words[1].decode('unicode-escape')
            print(words[0] + " " + words[1])
            cursor.execute("INSERT INTO `cities`(`city`, `autop_id`) VALUES (%s, %s)", (words[1].strip(), words[0].strip()))
    conn.commit()
    conn.close()