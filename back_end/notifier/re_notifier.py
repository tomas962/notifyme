from database.re_queries import mark_re_ads_as_deleted, get_re_query
from database.user import get_user
from database.messages import insert_message
import yagmail
import threading
import pywebpush
import json
import database.database as db
from config import SERVER_NAME

class ReNotifier():
    def __init__(self, old_ads, scraped_ads, query):
        self.re_query: dict = query
        self.old_ads = {}
        self.new_ads = {}
        self.ad_changes = {}
        for ad in old_ads:
            self.old_ads[ad["id"]] = ad

        for ad in scraped_ads:
            self.new_ads[ad["id"]] = ad

        self.compare_re_ads()
        ads_to_delete = self.deleted_re_ads()
        print("ads_to_ mark as deleted:")
        print(ads_to_delete)
        
        mark_re_ads_as_deleted(ads_to_delete)

        print("RE_AD_CHANGES:")
        print(self.ad_changes)

        self.re_query = get_re_query(self.re_query["id"])
        if self.re_query["was_scraped"] and len(self.ad_changes) != 0:
            msg = self.generate_message()
            self.msg_id = insert_message(self.re_query["user_id"], "Pasikeitė paieškos rezultatai", msg)
            print("MESSAGE TO SEND TO THE USER:")
            print(msg)
            threading.Thread(target=self.send_email, args=(msg,)).start()
            threading.Thread(target=self.send_push_notifications, args=(msg,)).start()
        else:
            print("NO RE AD CHANGES OR RE QUERY IS NEW")

    def _diff(self, ad_id, new_ad, key):
        if str(self.old_ads[ad_id][key]) != str(new_ad[key]):
            if ad_id not in self.ad_changes:
                self.ad_changes[ad_id] = {}
            self.ad_changes[ad_id][key] = True

    def compare_re_ads(self):
        """compares old and new ads"""
        for ad_id, ad in self.new_ads.items():
            if self.ad_is_new(ad_id):
                continue
            self._diff(ad_id, ad, "price")
            self._diff(ad_id, ad, "description")
    
    def ad_is_new(self, ad_id):
        if ad_id not in self.old_ads:
            self.ad_changes[ad_id] = True
            return True
        else:
            return False

    def deleted_re_ads(self):
        ads_to_delete = []
        for ad_id, ad in self.old_ads.items():
            if ad_id not in self.new_ads:
                ads_to_delete.append(ad_id)

        return ads_to_delete
    

    def generate_message(self):
        lines = []
        lines.append(f"Įvyko pokyčiai jūsų pasirinktoje paieškoje ({self.re_query['category_name'] or 'Visos kategorijos'} {self.re_query['city'] or 'Visi miestai'}):\n")
        for ad_id, change in self.ad_changes.items():
            if change == True:
                lines.append(f"\tPridėtas naujas skelbimas: {self.new_ads[ad_id]['title']} | {self.new_ads[ad_id]['city']}. {SERVER_NAME}/users/{self.re_query['user_id']}/re_queries/{self.re_query['id']}/re_ads/{ad_id}")
                continue
            
            line = "\t"
            if "price" in change:
                line += f"Pasikeitė kaina iš {self.old_ads[ad_id]['price']}€ į {self.new_ads[ad_id]['price']}€. "

            if "comments" in change:
                line += f"Pasikeitė aprašymas. "

            if line != "\t":
                line += f"({self.new_ads[ad_id]['title']} | {self.new_ads[ad_id]['city']}. {SERVER_NAME}/users/{self.re_query['user_id']}/re_queries/{self.re_query['id']}/re_ads/{ad_id})"
                lines.append(line)
        
        return "\n".join(lines)

    def send_email(self, msg):
        user = get_user(self.re_query["user_id"])
        if user is None:
            print(__name__ + " re_notifier.py error: USER NOT FOUND")
            return
        
        if not user["email_notifications"]:
            print("email notifications disabled for this user:")
            print(user)
            return
        
        print(f"SENDING EMAIL TO {user['email']}")
        print(f"EMAIL CONTENT:")
        print(msg)
        yag = yagmail.SMTP("skelbimupranesejas")
        yag.send(to=user["email"], subject="Naujas/pasikeitęs skelbimas", contents=msg)

    def send_push_notifications(self, msg):
        with db.db_connect().cursor() as cursor:
            cursor.execute("SELECT * FROM push_notification_auth WHERE user_id=%s", (self.re_query["user_id"]))
            auth_list = cursor.fetchall()
            for auth in auth_list:
                print("SENDING PUSH NOTIFICATION")
                auth_json = auth["auth_json"]

                try:
                    pywebpush.webpush(json.loads(auth_json), 
                        data=json.dumps({"title":"Pasikeitė paieškos rezultatai", "body":f"{self.re_query['category_name'] or 'Visos kategorijos'}, {self.re_query['city']}", "href":f"/users/{self.re_query['user_id']}/messages"}), 
                        vapid_private_key='./vapid_private.pem', vapid_claims={"sub":"mailto:cctomass@gmail.com"})
                except pywebpush.WebPushException as err:
                    print("Web push failed:")
                    print(err)
                    if "expired" in err.message:
                        cursor.execute("DELETE FROM `push_notification_auth` WHERE id=%s", auth["id"])
            
            cursor.connection.commit()
            cursor.connection.close()