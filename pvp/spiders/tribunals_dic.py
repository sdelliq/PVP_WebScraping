import scrapy
import json

#This class gets all tribunals and their ID, saves them as dictionary, and saves it as a json file.
class TribunaleSpider(scrapy.Spider):
    name = "tribunale"
    start_urls = [
        "https://pvp.giustizia.it/pvp/"
    ]

    def parse(self, response):
        tribunale_dict = {}
        
        for tribunale_option in response.css('select#IDTribunale2 option'):
            option_value = tribunale_option.attrib['value']
            option_text = tribunale_option.css('::text').get().strip().lower()
            
            tribunale_dict[option_text] = option_value
        
        with open('tribunale_data.json', 'w') as file:
            json.dump(tribunale_dict, file)

        # Return the scraped data
        return tribunale_dict