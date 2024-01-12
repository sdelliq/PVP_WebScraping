import datetime
from bs4 import BeautifulSoup

today= datetime.date.today().strftime("%d_%m_%Y")

class ReadHTMLParser:
    def __init__(self, tribunale, procedura, anno):
        self.file_name = f"{tribunale}_{procedura}_{anno}.html"

    def read_html(self):
        with open(f'output/{today}/{self.file_name}', 'r', encoding='utf-8') as file:
            html_content = file.read()
        return html_content
  
    def parse(self):
        html_content = self.read_html()
        soup = BeautifulSoup(html_content, 'html.parser')

        details_list = []
        for lotto in soup.find_all(class_='col-md-6 col-lg-4 col-sm-6 col-xs-12 tile-dettaglio'):
            address = lotto.find('div', class_='anagrafica-risultato').get_text().strip()
            nLotto = lotto.find(class_='black').get_text()

            data_vendita = lotto.find(class_='margin-top-15').find(class_='font-green').get_text()

            offerta_elements = lotto.find_all(class_='inline font-blue')
            offerta_minima = offerta_elements[0].get_text() 
            rialzo_minimo = offerta_elements[1].get_text()
            n_procedura = lotto.find(class_='font-black inline').get_text()
            prezzo_base = lotto.find(class_='margin-bottom-15').find(class_='font-blue font18').get_text()
            
            if nLotto and "Lotto nr." in nLotto:
                nLotto = nLotto.replace("\n                ", "")

            details_dict = {
                'Address': address,
                'Lotto': nLotto.strip() if nLotto else '',
                'Data di vendita': data_vendita.strip() if data_vendita else '',
                'Offerta minima': offerta_minima.strip() if offerta_minima else '',
                'Rialzo minimo': rialzo_minimo.strip() if rialzo_minimo else '',
                'N° Procedura': n_procedura.strip() if n_procedura else '',
                "Prezzo base d'asta": prezzo_base.strip() if prezzo_base else ''
            }
            details_list.append(details_dict)

        return details_list