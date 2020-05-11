from database.database import db_connect

re_cities = {}
with db_connect().cursor() as cursor:

    with open("./scripts/skelbiu_nt_cities_ready.txt", "r") as f, open("./scripts/domoplius_nt_cities_ready.txt", "r") as f2:
        sk_lines = f.readlines()
        domo_lines = f2.readlines()
        print(sk_lines)
        print(domo_lines)
        for i in range(len(sk_lines)):
            sk_words = sk_lines[i].split(',')
            domo_words = domo_lines[i].split(',')
            re_cities[sk_words[0].strip()] = {'skelbiu_id':sk_words[1].strip()}
            re_cities[domo_words[0].strip()]['domo_id'] = domo_words[1].strip()

        for i, val in re_cities.items():
            print(i)
            print(val)

            cursor.execute("INSERT INTO `re_cities`(`city`, `domo_id`, `skelbiu_id`) VALUES (%s, %s, %s)", (i, val['domo_id'], val['skelbiu_id']))
        cursor.connection.commit()
        cursor.connection.close()