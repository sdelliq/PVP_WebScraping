#pvp - portale delle vendite pubbliche https://pvp.giustizia.it/pvp/

import scrapy
import os
import random
import datetime

today= datetime.date.today().strftime("%d_%m_%Y")
class ProceduraSpider(scrapy.Spider):
    name="view"

    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': random.uniform(1, 5),
        'DOWNLOAD_TIMEOUT': 15, #: The maximum time (in seconds) that Scrapy will wait for a response before considering a request as failed.
        'CONCURRENT_REQUESTS': 1, #The maximum number of concurrent requests that Scrapy should process.
    }
    
    #Take parameters and handle possible errors
    def __init__(self, tribunale='', procedura='', anno='', *args, **kwargs):
        super(ProceduraSpider, self).__init__(*args, **kwargs)
        self.anno = anno
        self.procedura = procedura
        self.tribunale = tribunale

    #get URL ready    
    def start_requests(self):
        url = f"https://pvp.giustizia.it/pvp/it/risultati_ricerca.page?tipo_bene=immobili&geo=raggio&indirizzo=&raggio=25&lat=&lng=&tribunale={self.tribunale}&procedura={self.procedura}&anno={self.anno}&prezzo_da=&prezzo_a=&idInserzione=&ricerca_libera="
        yield scrapy.Request(url, self.parse)
    

    def parse(self, response):
        # Check if the 'output' directory exists, create it if not
        output_directory = os.path.join('output', today)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Save the HTML content to a file
        file_name = f"{self.tribunale}_{self.procedura}_{self.anno}.html"
        file_path = os.path.join(output_directory, file_name)

        with open(file_path, 'wb') as f:
            f.write(response.body)

        self.log(f"Saved HTML content to {file_path}")
    