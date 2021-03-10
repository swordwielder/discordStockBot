import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime


def searchPosHedge(current):
    url = 'https://gambitdataanalytics.web.app/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')  #'html.parser'
    divs = soup.findAll("td")
    a = str(divs[5])
    # print(type(a))
    comparison = float((a[4:9]))
    tds=[]
    print(datetime.now())
    print('the comparison value')
    print(comparison)
    print('current before comparison')
    print(current)
    time.sleep(3.5)
    if current != comparison:
        print('the current value before assignment')
        print(current)
        current = comparison
        print('current value after assignment')
        print(current)
        print( 'the hedge is different')
        return current
    # for div in divs:
        # rows = div.findAll('tr')
        # print(div)
        # for row in rows :
        #     tds.append(row.findAll('td'))
    # print(tds)
    # xpath = '/html/body/table/tbody/tr/td[6]'
    
    # print('Is this working')
    # time.sleep(5.0)
    # print('this is sleeping for 2.5')
    a=[]
    a.append(current)
    a.append('the hedge found is the same as the current hedge')
    # print()
    return a

# while True:
#     print(searchPosHedge(current))
#     time.sleep(3.5)