import sys
sys.path.insert(0,'..')
from database.database import connection

lines = []
with open("autoplius_makes.txt") as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines] 


for line in lines:
    words = line.split(',')
    make_id = words[0]
    make  = words[1]
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM `makes` WHERE `make`=%s', (make) )
        if len(cursor.fetchall()) == 0:
            cursor.execute('INSERT INTO `makes`(`make`, `autoplius_make_id`) VALUES (%s,%s)', (make, make_id))

connection.commit()
connection.close()