import requests
import re
from bs4 import BeautifulSoup

pagini = ["https://www.emag.ro/brands/televizoare/brand/samsung/c?ref=search_category_2",
          "https://www.emag.ro/brands/telefoane-mobile/brand/samsung/c?ref=hp_menu_quick-nav_1_21&type=brand",
          "https://www.emag.ro/brands/casti-audio-telefoane/brand/samsung/c?ref=search_category_3",
          "https://www.emag.ro/brands/uscatoare-rufe/brand/samsung/c?ref=search_category_6",
          "https://www.emag.ro/brands/soundbar/brand/samsung/c?ref=search_category_7"
          ]

produse = []
 
titlu_produs = "card-v2-title"
thumb_produs = "card-v2-thumb"
pret_produs = "product-new-price"

for pagina in pagini:
    pagina_html = requests.get(pagina)
    soup_pagina = BeautifulSoup(pagina_html.content, 'html.parser')

    titluri = soup_pagina.find_all("a", class_=titlu_produs)
    thumburi = soup_pagina.find_all("a", class_=thumb_produs)
    preturi = soup_pagina.find_all("p", class_=pret_produs)
    
    titluri_format = [titlu.get_text() for titlu in titluri]
    imagini = [thumb.img.get('src') for thumb in thumburi]
    preturi = [pret.get_text() for pret in preturi if pret.get_text() != '']

    preturi_format = [pret[6:] if pret[:5] == "de la" else pret for pret in preturi]

    preturi_format = ["{},{} {}".format(pret.split()[0][:-2], pret.split()[0][-2:], pret.split()[1]) for pret in preturi_format]
    
    produse += zip(titluri_format, imagini, preturi_format)
    
    
    