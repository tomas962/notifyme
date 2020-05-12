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