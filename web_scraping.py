from bs4 import BeautifulSoup
import requests
import re

def stock_scrap():
    url = 'https://finance.yahoo.com/most-active/'
    webpage = requests.get(url)  

    soup = BeautifulSoup(webpage.content, 'html.parser')
    stock_name = soup.find_all('a', attrs={'data-test': 'quoteLink'})
    stock_list = []
    for stock in stock_name:
        scrapped = stock.get('href')
        cap_scrapped = re.search(r'[A-Z]+', scrapped)
        stock_list.append(cap_scrapped[0])

    return stock_list