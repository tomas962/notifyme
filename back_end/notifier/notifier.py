


class Notifier():
    def __init__(self, old_cars, scraped_cars, query):
        self.query: dict = query
        self.old_cars = {}
        self.new_cars = {}
        for car in old_cars:
            self.old_cars[car["id"]] = car

        for car in scraped_cars:
            self.new_cars[car["id"]] = car
        

        print("OLD CARS KEYS:")
        for k, v in self.old_cars.items():
            for ke, va in v.items():
                print(ke)
            break

        print("NEW CARS KEYS:")
        for k, v in self.new_cars.items():
            for ke, va in v.items():
                print(ke)
                
            break