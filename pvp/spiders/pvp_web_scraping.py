#pvp - portale delle vendite pubbliche https://pvp.giustizia.it/pvp/

import scrapy
import os


class ProceduraSpider(scrapy.Spider):
    name="view"

    #Take parameters and handle possible errors
    def __init__(self, tribunale='', procedura='', anno='', *args, **kwargs):
        super(ProceduraSpider, self).__init__(*args, **kwargs)
        self.anno = anno
        self.procedura = procedura
        self.tribunale = tribunale

        ''' 
        # Check year
        try:
            self.anno = int(anno)
            if len(str(self.anno)) != 4:
                raise ValueError("L'anno deve avere 4 numeri.")
        except ValueError:
            raise ValueError("L'anno deve essere un numero intero (sono consentiti solo numeri).")

        # Check procedura
        try:
            self.procedura = int(procedura)
        except ValueError:
            raise ValueError("Il numero di procedura deve essere numerico.")

        # Check tribunale
        self.tribunale = tribunale
        if self.tribunale is None:
            raise ValueError("Il tribunale non corrisponde a uno esistente.")
        '''
    #get URL ready    
    def start_requests(self):
        url = f"https://pvp.giustizia.it/pvp/it/risultati_ricerca.page?tipo_bene=immobili&geo=raggio&indirizzo=&raggio=25&lat=&lng=&tribunale={self.tribunale}&procedura={self.procedura}&anno={self.anno}&prezzo_da=&prezzo_a=&idInserzione=&ricerca_libera="
        yield scrapy.Request(url, self.parse)
    

    def parse(self, response):
        # Check if the 'output' directory exists, create it if not
        output_directory = 'output'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Save the HTML content to a file
        file_name = f"{self.tribunale}_{self.procedura}_{self.anno}.html"
        file_path = os.path.join(output_directory, file_name)

        with open(file_path, 'wb') as f:
            f.write(response.body)

        self.log(f"Saved HTML content to {file_path}")
    