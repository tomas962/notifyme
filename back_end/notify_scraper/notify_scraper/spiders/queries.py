

class AutopliusQuery():


    def __init__(self, query):
        self.params: dict = query

    def check_params(self):

        if "make_model" in self.params and self.params["make_model"] is not None:
            if self.params["make_model"]["autoplius_make_id"] is None: 
                for key, value in self.params["make_model"].items():
                    if "_make_" in key:
                        if value is not None and self.params["make_model"]["make_ID"] != 1:
                            print("NOT SCRAPING AUTOPLIUS: MAKE ID NOT FOUND")
                            return False # don't scrape
            if self.params["make_model"]["autoplius_model_id"] is None: 
                #only scrape if all other model_id's are also None to prevent scraping random models when 
                for key, value in self.params["make_model"].items():
                    if "model_" in key:
                        if value is not None:
                            print("RETURNING FALSE")
                            return False # don't scrape
                        
        print("RETURNING TRUE")
        return True # scrape


    def generate(self):
        if not self.check_params():
            return None
        new_params = {}
        if "make_model" in self.params and self.params["make_model"] is not None and "autoplius_make_id" in self.params["make_model"]:
            new_params["make_id_list"] = self.params["make_model"]["autoplius_make_id"] or ""
        if "make_model" in self.params and self.params["make_model"] and "autoplius_model_id" in self.params["make_model"]:
            new_params[f"make_id[{new_params['make_id_list']}]"] = self.params["make_model"]["autoplius_model_id"] or ""

        if "car_query" in self.params and self.params["car_query"] is not None:
            if "price_from" in self.params["car_query"]:
                new_params["sell_price_from"] = self.params["car_query"]["price_from"] if self.params["car_query"]["price_from"] is not None else ""
            if "price_to" in self.params["car_query"]:
                new_params["sell_price_to"] = self.params["car_query"]["price_to"] if self.params["car_query"]["price_to"] is not None else ""

            if "year_from" in self.params["car_query"]:
                new_params["make_date_from"] = self.params["car_query"]["year_from"] if self.params["car_query"]["year_from"] is not None else ""
            if "year_to" in self.params["car_query"]:
                new_params["make_date_to"] = self.params["car_query"]["year_to"] if self.params["car_query"]["year_to"] is not None else ""
            if "search_term" in self.params["car_query"] and self.params["car_query"]["search_term"] is not None:
                new_params["qt"] = self.params["car_query"]["search_term"] if self.params["car_query"]["search_term"] is not None else ""
            if "power_from" in self.params["car_query"] and self.params["car_query"]["power_from"] is not None:
                new_params["power_from"] = self.params["car_query"]["power_from"]
            if "power_to" in self.params["car_query"] and self.params["car_query"]["power_to"] is not None:
                new_params["power_to"] = self.params["car_query"]["power_to"]
            if "autop_city_id" in self.params["car_query"] and self.params["car_query"]["autop_city_id"] is not None:
                new_params["fk_place_cities_id"] = self.params["car_query"]["autop_city_id"]
            

        if "body_style" in self.params and self.params["body_style"] is not None and "autoplius_id" in self.params["body_style"]:
            new_params["body_type_id"] = self.params["body_style"]["autoplius_id"] if self.params["body_style"]["autoplius_id"] is not None else ""
            
        if "fuel_type" in self.params and self.params["fuel_type"] is not None and "autoplius_fuel_id" in self.params["fuel_type"]:
            new_params["fuel_id"] = self.params["fuel_type"]["autoplius_fuel_id"] if self.params["fuel_type"]["autoplius_fuel_id"] is not None else ""
        
        return new_params

class AutogidasQuery():
    def __init__(self, query):
        self.params: dict = query

    def check_params(self):
        return True # scrape always, because if model doesn't exist it won't find any cars

    def generate(self):
        if not self.check_params():
            return None
        new_params = {}
        
        if "make_model" in self.params and self.params["make_model"] is not None and "make" in self.params["make_model"] and \
         self.params["make_model"]["make"] != "Visos markės":
            new_params[f'f_1[0]'] = self.params["make_model"]["make"] or ""
            if "make_model" in self.params and self.params["make_model"] and "model_name" in self.params["make_model"]:
                new_params[f'f_model_14[0]'] = self.params["make_model"]["model_name"] or ""

        if "car_query" in self.params and self.params["car_query"] is not None:
            if "price_from" in self.params["car_query"]:
                new_params['f_215'] = self.params["car_query"]["price_from"] if self.params["car_query"]["price_from"] is not None else ""
            if "price_to" in self.params["car_query"]:
                new_params['f_216'] = self.params["car_query"]["price_to"] if self.params["car_query"]["price_to"] is not None else ""

            if "year_from" in self.params["car_query"]:
                new_params['f_41'] = self.params["car_query"]["year_from"] if self.params["car_query"]["year_from"] is not None else ""
            if "year_to" in self.params["car_query"]:
                new_params['f_42'] = self.params["car_query"]["year_to"] if self.params["car_query"]["year_to"] is not None else ""
            if "search_term" in self.params["car_query"] and self.params["car_query"]["search_term"] is not None:
                new_params['f_376'] = self.params["car_query"]["search_term"] if self.params["car_query"]["search_term"] is not None else ""
            if "power_from" in self.params["car_query"] and self.params["car_query"]["power_from"] is not None:
                new_params["f_63"] = self.params["car_query"]["power_from"]
            if "power_to" in self.params["car_query"] and self.params["car_query"]["power_to"] is not None:
                new_params["f_64"] = self.params["car_query"]["power_to"]
            if "city" in self.params["car_query"] and self.params["car_query"]["city"] is not None:
                new_params["f_13"] = self.params["car_query"]["city"]

        if "body_style" in self.params and self.params["body_style"] is not None and "name" in self.params["body_style"]:
            new_params[f'f_3[0]'] = self.params["body_style"]["name"] if self.params["body_style"]["name"] is not None else ""
            
        if "fuel_type" in self.params and self.params["fuel_type"] is not None and "fuel_name" in self.params["fuel_type"]:
            new_params[f'f_2[0]'] = self.params["fuel_type"]["fuel_name"] if self.params["fuel_type"]["fuel_name"] is not None else ""
        
        
        return new_params

class AutobilisQuery():
    def __init__(self, query):
        self.params: dict = query
    def check_params(self):
        if "make_model" in self.params and self.params["make_model"] is not None:
            if self.params["make_model"]["autobilis_make_id"] is None: 
                for key, value in self.params["make_model"].items():
                    if "_make_" in key:
                        if value is not None and self.params["make_model"]["make_ID"] != 1:
                            print("NOT SCRAPING AUTOBILIS: MAKE ID NOT FOUND")
                            return False # don't scrape
            if self.params["make_model"]["autobilis_model_id"] is None: 
                #only scrape if all other model_id's are also None to prevent scraping random models when 
                for key, value in self.params["make_model"].items():
                    if "model_" in key:
                        if value is not None:
                            print("RETURNING FALSE")
                            return False # don't scrape
                        
        print("RETURNING TRUE")
        return True # scrape


    def generate(self):
        if not self.check_params():
            return None
        new_params = {}
        if "make_model" in self.params and self.params["make_model"] is not None and "autobilis_make_id" in self.params["make_model"]:
            new_params["make_id[]"] = self.params["make_model"]["autobilis_make_id"] or ""
        if "make_model" in self.params and self.params["make_model"] and "autobilis_model_id" in self.params["make_model"]:
            new_params[f"model_id[]"] = self.params["make_model"]["autobilis_model_id"] or ""

        if "car_query" in self.params and self.params["car_query"] is not None:
            if "price_from" in self.params["car_query"]:
                new_params["price_from"] = self.params["car_query"]["price_from"] if self.params["car_query"]["price_from"] is not None else ""
            if "price_to" in self.params["car_query"]:
                new_params["price_to"] = self.params["car_query"]["price_to"] if self.params["car_query"]["price_to"] is not None else ""

            if "year_from" in self.params["car_query"]:
                new_params["year_from"] = self.params["car_query"]["year_from"] if self.params["car_query"]["year_from"] is not None else ""
            if "year_to" in self.params["car_query"]:
                new_params["year_to"] = self.params["car_query"]["year_to"] if self.params["car_query"]["year_to"] is not None else ""
            if "search_term" in self.params["car_query"] and self.params["car_query"]["search_term"] is not None:
                new_params["qt"] = self.params["car_query"]["search_term"] if self.params["car_query"]["search_term"] is not None else ""
            if "power_from" in self.params["car_query"] and self.params["car_query"]["power_from"] is not None:
                new_params["engine_power_from"] = self.params["car_query"]["power_from"]
            if "power_to" in self.params["car_query"] and self.params["car_query"]["power_to"] is not None:
                new_params["engine_power_to"] = self.params["car_query"]["power_to"]
            if "autob_city_id" in self.params["car_query"] and self.params["car_query"]["autob_city_id"] is not None:
                new_params["city"] = self.params["car_query"]["autob_city_id"]

        if "body_style" in self.params and self.params["body_style"] is not None and "autobilis_id" in self.params["body_style"]:
            new_params["body_type"] = self.params["body_style"]["autobilis_id"] if self.params["body_style"]["autobilis_id"] is not None else ""
            
        if "fuel_type" in self.params and self.params["fuel_type"] is not None and "autobilis_fuel_id" in self.params["fuel_type"]:
            new_params["fuel_type"] = self.params["fuel_type"]["autobilis_fuel_id"] if self.params["fuel_type"]["autobilis_fuel_id"] is not None else ""
        
        if "power_from" in self.params and self.params["power_from"] is not None:
            new_params["engine_power_from"] = self.params["power_from"]

        if "power_to" in self.params and self.params["power_to"] is not None:
            new_params["engine_power_to"] = self.params["power_to"]


        return new_params