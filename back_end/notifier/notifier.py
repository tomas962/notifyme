from database.car import mark_as_deleted_multiple_cars_by_id
from database.user import get_user
import yagmail
import threading

class Notifier():
    def __init__(self, old_cars, scraped_cars, query):
        self.car_query: dict = query
        self.old_cars = {}
        self.new_cars = {}
        self.car_changes = {}
        for car in old_cars:
            self.old_cars[car["id"]] = car

        for car in scraped_cars:
            self.new_cars[car["id"]] = car

        self.compare_car_ads()
        cars_to_delete = self.deleted_car_ads()
        print("cars_to_ mark as deleted:")
        print(cars_to_delete)
        
        mark_as_deleted_multiple_cars_by_id(cars_to_delete)

        print("CAR_CHANGES:")
        print(self.car_changes)

        if self.car_query["car_query"]["was_scraped"] and len(self.car_changes) != 0:
            msg = self.generate_message()
            print("MESSAGE TO SEND TO THE USER:")
            print(msg)
            threading.Thread(target=self.send_email, args=(msg,)).start()
        else:
            print("NO CAR CHANGES OR CAR QUERY IS NEW")

    def _diff(self, car_id, new_car, key):
        if self.old_cars[car_id][key] != new_car[key]:
            if car_id not in self.car_changes:
                self.car_changes[car_id] = {}
            self.car_changes[car_id][key] = True

    def compare_car_ads(self):
        """compares old and new cars"""
        for car_id, car in self.new_cars.items():
            if self.car_ad_is_new(car_id):
                continue
            self._diff(car_id, car, "price")
            self._diff(car_id, car, "comments")
    
    def car_ad_is_new(self, car_id):
        if car_id not in self.old_cars:
            self.car_changes[car_id] = True
            return True
        else:
            return False

    def deleted_car_ads(self):
        cars_to_delete = []
        for car_id, car in self.old_cars.items():
            if car_id not in self.new_cars:
                cars_to_delete.append(car_id)

        return cars_to_delete
    

    def generate_message(self):
        lines = []
        lines.append(f"Įvyko pokyčiai jūsų pasirinktoje paieškoje ({self.car_query['make_model']['make']} {self.car_query['make_model']['model_name']}):")
        for car_id, change in self.car_changes.items():
            if change == True:
                lines.append(f"\tPridėtas naujas skelbimas: {self.new_cars[car_id]['make_name']} {self.new_cars[car_id]['model_name']}. http://192.168.100.7:8080/queries/{self.car_query['car_query']['id']}/cars/{car_id}")
                continue
            
            line = "\t"
            if "price" in change:
                line += f"Pasikeitė kaina iš {self.old_cars[car_id]['price']}€ į {self.new_cars[car_id]['price']}€. "

            if "comments" in change:
                line += f"Pasikeitė aprašymas. "

            if line != "\t":
                line += f"({self.new_cars[car_id]['make_name']} {self.new_cars[car_id]['model_name']}. http://192.168.100.7:8080/queries/{self.car_query['car_query']['id']}/cars/{car_id})"
                lines.append(line)
        
        return "\n".join(lines)

    def send_email(self, msg):
        user = get_user(self.car_query["car_query"]["user_id"])
        if user is None:
            print(__name__ + " notifier.py error: USER NOT FOUND")
            return
        
        print(f"SENDING EMAIL TO {user['email']}")
        print(f"EMAIL CONTENT:")
        print(msg)
        yag = yagmail.SMTP("skelbimupranesejas")
        yag.send(to=user["email"], subject="Naujas/pasikeitęs skelbimas", contents=msg)
