from bs4 import BeautifulSoup
import json
import pandas as pd
from scrapy.crawler import CrawlerProcess
from spiders.pvp_web_scraping import ProceduraSpider
import os
import sys
import datetime

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
    

inputs = pd.read_excel('input/input.xlsx')
inputs.columns = [col.lower() for col in inputs.columns]


# pd.DataFrame(parsed_data).to_excel('scraped_data.xlsx', index=False) #saves the output normally, without column widht adjusted
def dicToExcel(dict_list):
    with pd.ExcelWriter('scraped_data.xlsx', engine='xlsxwriter') as writer:
        for dictionary in dict_list:
            sheet_name = list(dictionary.keys())[0]
            df = pd.DataFrame(dictionary[sheet_name])
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Get the worksheet object
            worksheet = writer.sheets[sheet_name]

            # Auto-adjust column widths based on content length
            for i, col in enumerate(df.columns):
                column_len = max(df[col].astype(str).map(len).max(), len(col))
                worksheet.set_column(i, i, column_len + 2)




with open('tribunale_data.json', 'r') as file:
    loaded_dict = json.load(file)

failed=False
process = CrawlerProcess()
for index, row in inputs.iterrows():  
    # Check year
    try:
        anno = int(row['anno'] )
        if len(str(anno)) != 4:
            failed=True
            raise ValueError("L'anno deve avere 4 numeri.")
    except ValueError:
        failed=True
        raise ValueError("L'anno deve essere un numero intero (sono consentiti solo numeri).")
        
    # Check procedura
    try:
        procedura = int(row['procedura'])
    except ValueError:
        failed=True
        raise ValueError("Il numero di procedura deve essere un numero intero (sono consentiti solo numeri).")
        
    # Check tribunale
    tribunale = row['tribunale']
    n_tribunale = loaded_dict.get(tribunale.lower())
    if tribunale is None:
        failed=True
        raise ValueError("Il tribunale non corrisponde a uno esistente.")
        
    if failed==True:
        sys.exit(1)

    if(not os.path.exists(f'output/{n_tribunale}_{procedura}_{anno}.html')):
        process.crawl(ProceduraSpider, n_tribunale, procedura, anno)
process.start()

''' 
dictionaries = []
for file in f'output/{today}':
    parser = ReadHTMLParser(n_tribunale, procedura, anno)
    parsed_data = parser.parse()
    dictionaries.append({f'{tribunale}_{procedura}_{anno}': parsed_data})  # Append as a dictionary
    
dicToExcel(dictionaries)
'''
dictionaries = []
directory_path = f'output/{today}'
for file in os.listdir(directory_path):
        # Construct the full path to the file
        file_path = os.path.join(directory_path, file)

        # Assuming n_tribunale, procedura, and anno are defined elsewhere
        parser = ReadHTMLParser(n_tribunale, procedura, anno)
        parsed_data = parser.parse(file_path)
        dictionaries.append({f'{tribunale}_{procedura}_{anno}': parsed_data})  # Append as a dictionary

scraped_data_df = pd.DataFrame(dictionaries)
scraped_data_df = scraped_data_df.transpose().reset_index()
scraped_data_df.columns = ['Key', 'Parsed_Data']

dicToExcel(scraped_data_df)