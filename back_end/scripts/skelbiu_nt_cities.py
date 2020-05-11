import scrapy
import scrapy.responsetypes
import os

class Spider(scrapy.Spider):
    name = "spider"
    start_urls = ["file://"+os.getcwd()+"/scripts/domoplius_nt_cities.html"]

    def parse(self, response: scrapy.responsetypes.Response):
        
        city_ids = response.css(".dropDownLabel::attr(data-id)").getall()
        city_names = response.css(".dropDownLabel::text").getall()
        city_names = [x.strip() for x in city_names]
        print(city_ids)
        print(city_names)
        print(len(city_ids))
        print(len(city_names))
        with open("./scripts/skelbiu_nt_cities.txt", "w") as f:
            lines = []
            for i in range(len(city_ids)):
                lines.append(f"{city_names[i]},{city_ids[i]}\n")
            lines.sort()
            f.writelines(lines)