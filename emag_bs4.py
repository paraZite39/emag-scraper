import requests
import re
from bs4 import BeautifulSoup
import csv

tags = ["fotografie", 
        "informatica", 
        "televizor", 
        "telefon", 
        "laptop", 
        "pc", 
        "accesorii pc", 
        "telefon", 
        "accesorii smartphone",
        "pictura",
        "sneakers",
        "tuxedo",]

emag_pages = ["https://www.emag.ro/laptopuri/",
              "https://www.emag.ro/label/Accesorii-Laptop/",
              "https://www.emag.ro/label/telefoane-mobile-accesorii/Accesorii-telefoane/",
              "https://www.emag.ro/telefoane-mobile/",
              "https://www.emag.ro/tablete/",
              "https://www.emag.ro/smartwatch/",
              "https://www.emag.ro/bratari-fitness/",
              "https://www.emag.ro/desktop-pc/",
              "https://www.emag.ro/monitoare-lcd-led/",
              "https://www.emag.ro/mouse/",
              "https://www.emag.ro/tastaturi/",
              "https://www.emag.ro/hard_disk-uri_externe/",
              "https://www.emag.ro/casti-pc/",
              "https://www.emag.ro/tablete-grafice/",
              "https://www.emag.ro/memorii-usb/",
              "https://www.emag.ro/televizoare/",
              "https://www.emag.ro/audio-hi-fi/",
              "https://www.emag.ro/home-cinema-blu-ray/",
              ]

products = []

def emag_search(url_list):
    product_title_class = "card-v2-title"
    product_thumb_class = "card-v2-thumb"
    product_price_class = "product-new-price"
    
    subpages_number_id = "listing-paginator"
    
    products = []

    for url in url_list:
        page_html = requests.get(url)
        soup = BeautifulSoup(page_html.content, 'html.parser')
        
        num_of_pages = int(soup.find(id=subpages_number_id).span.get_text().split()[-1])
        print(num_of_pages)
        
        for page_number in range(1, min(5, num_of_pages + 1)):
            subpage_url = "{}p{}/c".format(url, page_number)
            print("page is " + url + ", subpage is " + subpage_url)
            subpage_html = requests.get(subpage_url)
            subpage_soup = BeautifulSoup(subpage_html.content, 'html.parser')
            
            titles = subpage_soup.find_all("a", class_=product_title_class)
            formatted_titles = [title.get_text() for title in titles]
            
            thumbs = subpage_soup.find_all("a", class_=product_thumb_class)
            thumb_images = [thumb.img.get('src') for thumb in thumbs]
            
            prices = subpage_soup.find_all("p", class_=product_price_class)
            prices = [price.get_text() for price in prices if price.get_text() != '']
            prices = [price[6:] if price[:5] == 'de la' else price for price in prices]
            formatted_prices = ["{},{} {}".format(price.split()[0][:-2], price.split()[0][-2:], price.split()[1]) for price in prices]
  
            products += zip(formatted_titles, thumb_images, formatted_prices)
            
            with(open('emag_products_lap_2.csv', 'w', encoding='utf-8', newline='')) as csv_file:
                writer = csv.writer(csv_file)
                for product in products:
                    writer.writerow(product)
    
    return products
    
    
    