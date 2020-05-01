from database.car import mark_as_deleted_multiple_cars_by_id

class Notifier():
    def __init__(self, old_cars, scraped_cars, query):
        self.car_query: dict = query
        self.old_cars = {}
        self.new_cars = {}
        self.car_changes = {}
        print("SCRAPED CARS PASSED:")
        print(scraped_cars)
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

        if len(self.car_changes) != 0:
            msg = self.generate_message()
            print("MESSAGE TO SEND TO THE USER:")
            print(msg)

    def _diff(self, car_id, new_car, key):
        if self.old_cars[car_id][key] != new_car[key]:
            print(key+" CHANGED:")
            print(self.old_cars[car_id][key])
            print(new_car[key])
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
        print("CARS TO DELETE:")
        for car_id, car in self.old_cars.items():
            if car_id not in self.new_cars:
                cars_to_delete.append(car_id)
                print(car)
                print()

        print("NEW CARS")
        print(self.new_cars)
        return cars_to_delete
    

    def generate_message(self):
        lines = []
        lines.append(f"Įvyko pokyčiai jūsų pasirinktoje paieškoje ({self.car_query['make_model']['make']} {self.car_query['make_model']['model_name']}):")
        for car_id, change in self.car_changes.items():
            if change == True:
                lines.append(f"    Pridėtas naujas skelbimas: {self.new_cars[car_id]['make_name']} {self.new_cars[car_id]['model_name']}. /queries/{self.car_query['car_query']['id']}/cars/{car_id}")
                continue
            
            line = "    "
            if "price" in change:
                line += f"Pasikeitė kaina iš {self.old_cars[car_id]['price']}€ į {self.new_cars[car_id]['price']}€. "

            if "comments" in change:
                line += f"Pasikeitė aprašymas. "

            if line != "    ":
                line += f"({self.new_cars[car_id]['make_name']} {self.new_cars[car_id]['model_name']}. /queries/{self.car_query['car_query']['id']}/cars/{car_id})"
                lines.append(line)
        
        return "\n".join(lines)