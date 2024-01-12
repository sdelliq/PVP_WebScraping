from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import sys
import datetime

from scrapy.crawler import CrawlerProcess
from spiders.pvp_web_scraping import ProceduraSpider
from HTML_scraper import ReadHTMLParser
from functions import dicToExcel

today= datetime.date.today().strftime("%d_%m_%Y")
    
inputs = pd.read_excel('input/input.xlsx')
inputs.columns = [col.lower() for col in inputs.columns]

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

    if(not os.path.exists(f'output/{today}/{n_tribunale}_{procedura}_{anno}.html')):
        process.crawl(ProceduraSpider, n_tribunale, procedura, anno)

process.start()


dictionaries = pd.DataFrame()
directory_path = f'output/{today}'
for file in os.listdir(directory_path):
    n_tribunale, procedura, anno = map(int, file.rstrip('.html').split('_'))
    n_tribunale = f'{n_tribunale:010d}' #I put back the 0s it might have taken from the start in the conversion
    tribunale = list(loaded_dict.keys()) [list(loaded_dict.values()).index(n_tribunale)]

    # Assuming n_tribunale, procedura, and anno are defined elsewhere
    parser = ReadHTMLParser(n_tribunale, procedura, anno)
    parsed_data = parser.parse()
    
    parsed_data=pd.DataFrame(parsed_data)
    parsed_data['id'] = f'{tribunale}_{procedura}_{anno}'
    dictionaries = pd.concat([dictionaries, parsed_data])

dicToExcel(dictionaries)
