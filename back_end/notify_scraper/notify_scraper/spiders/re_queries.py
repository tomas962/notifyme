class SkelbiuReQuery():

    def __init__(self, query):
        self.old_params = {}
        self.new_params = {}
        self.old_params = query

    def generate(self):
        self.new_params["category_id"] = self.old_params.get("skelbiu_category_id") or ""
        self.new_params["cities"] = self.old_params.get("skelbiu_city_id") or ""
        self.new_params["building_type"] = self.old_params.get("skelbiu_house_type_id") or ""
        self.new_params["building"] = self.old_params.get("skelbiu_type_id") or ""
        self.new_params["keywords"] = self.old_params.get("search_term") or ""
        self.new_params["cost_min"] = self.old_params.get("price_from") or ""
        self.new_params["cost_max"] = self.old_params.get("price_to") or ""
        self.new_params["space_min"] = self.old_params.get("area_from") or ""
        self.new_params["space_max"] = self.old_params.get("area_to") or ""
        self.new_params["rooms_min"] = self.old_params.get("rooms_from") or ""
        self.new_params["rooms_max"] = self.old_params.get("rooms_to") or ""
        self.new_params["year_min"] = self.old_params.get("year_from") or ""
        self.new_params["year_max"] = self.old_params.get("year_to") or ""
        return self.new_params


class DomoReQuery():
    def __init__(self, query):
        self.old_params = {}
        self.new_params = {}
        self.old_params = query
        self.query_prefix = ""
        self.gen_prefix()

    def gen_prefix(self):
        if self.old_params.get("domo_category_id") == 1:
            self.query_prefix = "butai"
        elif self.old_params.get("domo_category_id") == 7:
            self.query_prefix = "namai-kotedzai-sodai"
        elif self.old_params.get("domo_category_id") == 5:
            self.query_prefix = "sklypai"


    def generate(self):
        self.new_params["category_search"] = self.old_params.get("domo_category_id") or ""
        self.new_params["address_1"] = self.old_params.get("domo_city_id") or ""
        
        if self.old_params.get("domo_house_type_id") is not None:
            self.new_params[f"building_type_id[{self.old_params.get('domo_house_type_id')}]"] = self.old_params.get("domo_house_type_id") or ""
        
        self.new_params["construction_type_id"] = self.old_params.get("domo_type_id") or ""
        self.new_params["qt"] = self.old_params.get("search_term") or ""
        self.new_params["sell_price_from"] = self.old_params.get("price_from") or ""
        self.new_params["sell_price_to"] = self.old_params.get("price_to") or ""
            
        if self.query_prefix == "butai":
            self.new_params["flat_size_from"] = self.old_params.get("area_from") or ""
            self.new_params["flat_size_to"] = self.old_params.get("area_to") or ""
            self.new_params["flat_rooms_from"] = self.old_params.get("rooms_from") or ""
            self.new_params["flat_rooms_to"] = self.old_params.get("rooms_to") or ""
            
        
        if self.query_prefix == "namai-kotedzai-sodai":
            self.new_params["building_size_from"] = self.old_params.get("area_from") or ""
            self.new_params["building_size_to"] = self.old_params.get("area_to") or ""
            self.new_params["building_rooms_from"] = self.old_params.get("rooms_from") or ""
            self.new_params["building_rooms_to"] = self.old_params.get("rooms_to") or ""


        if self.query_prefix == "sklypai":
            self.new_params["site_size_from"] = self.old_params.get("area_from") or ""
            self.new_params["site_size_to"] = self.old_params.get("area_to") or ""

        self.new_params["building_build_date_from"] = self.old_params.get("year_from") or ""
        self.new_params["building_build_date_to"] = self.old_params.get("year_to") or ""

        self.new_params["action_type"] = "1"

        return self.new_params


