import scrapy 
import json

class ProceduraSpider(scrapy.Spider):
    name="view"
    
    #bulk call - excel input 
    #first get the HTML and then do the parse (different classes)
    #output an excel 
    

    def __init__(self, tribunale='', procedura='', anno='', *args, **kwargs):
        super(ProceduraSpider, self).__init__(*args, **kwargs)

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
        with open('tribunale_data.json', 'r') as file:
            loaded_dict = json.load(file)

        self.tribunale = loaded_dict.get(tribunale.lower())
        if self.tribunale is None:
            raise ValueError("Il tribunale non corrisponde a uno esistente.")
        
        
    def start_requests(self):
        url = f"https://pvp.giustizia.it/pvp/it/risultati_ricerca.page?tipo_bene=immobili&geo=raggio&indirizzo=&raggio=25&lat=&lng=&tribunale={self.tribunale}&procedura={self.procedura}&anno={self.anno}&prezzo_da=&prezzo_a=&idInserzione=&ricerca_libera="
        yield scrapy.Request(url, self.parse)
    
    ''' 
    def parse(self, response):
        for lotto in response.css('.col-md-6.col-lg-4.col-sm-6.col-xs-12.tile-dettaglio'):
            address = lotto.xpath('.//div[@class="anagrafica-risultato"]/text()').extract()
            nLotto = lotto.css('span.black::text').get()
            data_vendita = lotto.css('.margin-top-15 span.font-green::text').get()
            offerta_minima = lotto.css('span:contains("Offerta minima") span.font-blue::text').get()
            rialzo_minimo = lotto.css('span:contains("Rialzo minimo") span.font-blue::text').get()
            n_procedura = lotto.css('span:contains("N° Procedura") span.font-black::text').get()
            prezzo_base = lotto.css('span:contains("Prezzo base d\'asta") span.font-blue::text').get()
            
            if nLotto and "Lotto nr." in nLotto:
                nLotto = nLotto.replace("\r\n                ", "")
            
            details_dict = {
                'Address': ' '.join(address).strip() if address else '',
                'Lotto': nLotto.strip() if nLotto else '',
                
                'Data di vendita': data_vendita.strip() if data_vendita else '',
                'Offerta minima': offerta_minima.strip() if offerta_minima else '',
                'Rialzo minimo': rialzo_minimo.strip() if rialzo_minimo else '',
                'N° Procedura': n_procedura.strip() if n_procedura else '',
                "Prezzo base d'asta": prezzo_base.strip() if prezzo_base else ''
            }
            yield details_dict  # Yield each item individually
'''