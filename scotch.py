import requests
from bs4 import BeautifulSoup
import json


bevmoUrl = 'https://www.bevmo.com/shop#!/?q=scotch'
totalWineUrl = 'https://www.totalwine.com/search/all?text=scotch'  

bevmo = requests.get(bevmoUrl)
totalWine = requests.get(totalWineUrl)

bevmoSoup = BeautifulSoup(bevmo.content, 'html.parser')
twineSoup = BeautifulSoup(totalWine.content,'html.parser')

bevmoContent = bevmoSoup.find_all('div', class_='fp-result-list-content')
totalWineContent = twineSoup.find_all('div' , class_='grid__1eZnNfL-')

print('\nTotal Wine')
for i in totalWineContent:
    print(i)

print('\nBevmo\n\n')
for i in bevmoContent:
    print(i)
print('\nend')
