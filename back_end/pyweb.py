
from pywebpush import webpush
import json
import database.database as db

with db.db_connect().cursor() as cursor:
    cursor.execute("SELECT * FROM push_notification_auth WHERE user_id=1")
    auth = cursor.fetchone()
    auth_json = auth["auth_json"]

webpush(json.loads(auth_json), 
         data=json.dumps({"title":"My title", "body":"My blooolody", "href":"/register"}), 
         vapid_private_key='./vapid_private.pem', vapid_claims={"sub":"mailto:cctomass@gmail.com"}, verbose=True)
