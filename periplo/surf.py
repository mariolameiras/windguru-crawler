import os
from datetime import datetime
from itertools import chain

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import pprint
from core import hmm


def fetch_html(url):
    try:
        browser = webdriver.PhantomJS()
        browser.get(url)
        browser.implicitly_wait(30)
        browser.find_element_by_id('tabid_0_0_dates')
        html = browser.page_source
        return html
    except Exception as e:
        print(e)


def fetch_html_headless(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920x1080')
    driver = os.path.join(os.getcwd(), 'chromedriver')


    try:
        browser = webdriver.Chrome(chrome_options=options,
                                   executable_path=driver)
        browser.implicitly_wait(30)
        browser.get(url)
        browser.find_element_by_id('tabid_0_0_dates')
        html = browser.page_source
        return html
    except Exception as e:
        print(e)

def fetch_model(soup,table_id,model_id):
    tr_dates = soup('tr', {'id': table_id})
    hours = [td.contents for td in
             chain.from_iterable([x.find_all('td') for x in tr_dates])]
    tr = soup("tr", {'id': model_id})
    wave_period = [td.contents[0] for td in
                   chain.from_iterable([x.find_all('td') for x in tr])]
    #    dhoje = datetime.now().day
    #    forecast = filter(lambda x: int(x[0][2].strip('.')) == dhoje,
#    forecast = zip(hours, wave_period)
    
    model = dict(
        date=hours,
        period=wave_period
    )

#       for h, p in forecast:
#        print('{}: {}'.format(h[2].strip('.') + " - " + h[4], p))

    return model

def fetch_ipma(id_place):
    ipma_url = "https://www.ipma.pt/pt/maritima/costeira/index.jsp?idLocal="
    page = requests.get(ipma_url+id_place)
    soup = BeautifulSoup(page.content, 'html.parser')

    days = soup.select('ul.simpleTabsNavigation li a')
    # For each a split , first part
    tables = soup.select('table.tablelist')

    cols = [header.text for header in tables[0].findAll('th')]
    col_idx = cols.index('Periodoonda')
    col_values = [td[col_idx].string
                  for td in [tr.findAll('td')
                             for tr in tables[0].findAll('tr')]]

    print("done")
    #print(tab1)
#    a #tabber19_a_0
#    tabber19_div_0
#    table

#    print(print.prettify())


def main():
    print('Starting windGuru crawler...')


    url = "https://windguru.cz/103"
    wave_period = None
    hours = None

    html = fetch_html_headless(url)

    soup = BeautifulSoup(html, 'lxml')

    model = fetch_model(soup,'tabid_6_0_dates','tabid_6_0_PERPW')

    ipma = fetch_ipma("27")

    #pp = pprint.PrettyPrinter(indent=4)
    ##pp.pprint(model)



if __name__ == "__main__":
    main()
