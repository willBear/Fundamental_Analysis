###########################
# Created on May 6th 2020
# @ Author: WillBear
###########################



import requests
from bs4 import BeautifulSoup

def find_stock_price():
    url = 'https://finance.yahoo.com/quote/FB?p=FB'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    # print(soup)
    # The price is pulled from
    price = soup.find_all('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text

    print(price)

def find_analyst_target(symbol):
    url = 'https://finance.yahoo.com/quote/'+symbol+'?p=' + symbol
    response = requests.get(url)

    # Call the response and convert it into a lxml format
    soup = BeautifulSoup(response.text,'lxml')
    # print(soup)
    data_table = soup.find_all('table', {'class':'W(100%) M(0) Bdcl(c)'})
    print(data_table)

    target_price = data_table[0].find('td', {'class':'Ta(end) Fw(600) Lh(14px)','data-test':'ONE_YEAR_TARGET_PRICE-value'})
    print(target_price)
    print(target_price.text)



find_analyst_target('WMT')