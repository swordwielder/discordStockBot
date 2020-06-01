import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import warnings
import selenium as se
import lxml
from lxml import html
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import time


def sams():
    options = Options()
    options.headless = True
    
    browser = webdriver.Chrome(ChromeDriverManager().install())
    # browser=webdriver.Chrome()
    browser.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){"+
                                        "var position = {\"coords\" : {\"latitude\": \"33.735021\",\"longitude\": \"-112.181337\"}};"+
                                        "success(position);}")
    
    url = "https://www.samsclub.com/s/johnnie%20walker"
    browser.get(url) #navigate to the page
    time.sleep(3)
    innerHTML = browser.execute_script("return document.body.innerHTML")

    return innerHTML

def bevmolink():
    # driver.findElement(locator).isEnabled()
    # driver.findElement(locator).isDisplayed()
    # driver.manage().timeouts().implicitlyWait(number_of_seconds, TimeUnit.SECONDS)

    browser = webdriver.Chrome(ChromeDriverManager().install())
    #browser = webdriver.Chrome(ChromeDriverManager().install())
    locator = 'fp-item-sale-price'
    browser.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){"+
                                        "var position = {\"coords\" : {\"latitude\": \"33.735021\",\"longitude\": \"-112.181337\"}};"+
                                        "success(position);}")

    # print(driver.execute_script("var positionStr=\"\";"+
    #                                 "window.navigator.geolocation.getCurrentPosition(function(pos){positionStr=pos.coords.latitude+\":\"+pos.coords.longitude});"+
    #                                 "return positionStr;"))
    
    url = "https://www.bevmo.com/shop#!/?q=scotch"
    browser.get(url) #navigate to the page
    time.sleep(3)
    innerHTML = browser.execute_script("return document.body.innerHTML")

    # locator = 'fp-item-sale-price'
    return innerHTML

def totalwinelink(search):
    q = '%20'.join(search.split())
    display = Display(visible=0, size=(800, 800))  
    display.start()
    #chrome_options = Options()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    
    browser = webdriver.Chrome()
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    #browser = webdriver.Chrome()
    browser.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){"+
                                        "var position = {\"coords\" : {\"latitude\": \"33.735021\",\"longitude\": \"-112.181337\"}};"+
                                        "success(position);}")
    
    url = "https://www.totalwine.com/search/all?text="+ q
    browser.get(url) #navigate to the page
    time.sleep(1)
    innerHTML = browser.find_elements_by_class_name("grid__1eZnNfL-")
    # innerHTML = browser.get_attribute("innerHTML")
    toreturn = []
    for element in innerHTML:
        b = element.text.split('\n')
        
        for i in range(len(b)):
            print (b[i])

            # toreturn.append(b[i])
            if b[i] != '90' and b[i] !='Pick Up In Stock' and b[i] != 'Delivery Unavailable' and b[i] != 'Add to Cart':
                toreturn.append(b[i])
            if len(toreturn)>=5:
                break
    return toreturn


# warnings.filterwarnings('ignore')


# bevmoUrl = 'https://www.bevmo.com/shop#!/?q=scotch&filter=include_out_of_stock'
# totalWineUrl = 'https://www.totalwine.com/search/all?text=johnnie%20walker%20black'  
# samsClubUrl = 'https://www.samsclub.com/s/johnnie%20walker%20black'

# bevmo = requests.get(bevmoUrl)
# totalWine = requests.get(totalWineUrl)

# bevmoSoup = BeautifulSoup(bevmo.text, 'html.parser')
# twineSoup = BeautifulSoup(totalWine.content,'html.parser')

# bevmoContent = bevmoSoup.find_all('div', class_='fp-result-list-content')
# totalWineContent = twineSoup.find_all('div' , class_='grid__1eZnNfL-')

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}




def search(q,choice):
    s = requests.Session()
    q = '%20'.join(q.split())
    url = ''
    #.PhantomJS()
    # browser = webdriver.Firefox(desired_capabilities={'firefox.page.settings.resourceTimeout': '3000'})
    # soup = BeautifulSoup(html, 'lxml')

    # chrome_options = se.webdriver.ChromeOptions()
    # print('chrome options:')
    # print(chrome_options)
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    #'chromedriver',
    if choice == 'bevmo':
        url = 'https://www.bevmo.com/shop#!/?q='+ q +'&filter=include_out_of_stock'
    elif choice =='totalwine':
        url = 'https://www.totalwine.com/search/all?text=' + q
    else:
        url = 'https://www.samsclub.com/s/' + q
        new = 'sc-infinite-loader sc-product-cards analytics'
    print('The url is:')
    print(url)
    # req = driver.get(url)
    # print('request for driver is:')
    # print(req)
    
    # r = s.get(url, headers=headers)
    # browser.get(url)
    # html = browser.page_source
    # print('HTML for browser page source:')
    # print(html)
    

    # soup = BeautifulSoup(r.text , "html.parser")
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    print('soup is:')
    # print(soup.prettify())
    output = []
    # print(soup)
    
    res = soup.findAll("div", {"class": 'sc-product-cards-wrapper'})

    # for result in soup.findAll("div", {"class": 'fp-item-container'}):
    #     print(result)
    
    output.append(res)
    
    print('SKIP')
    return output

# print('\nTotal Wine')
# print(totalWineContent)

# print(bevmoContent)
# for i in bevmoContent:
# print('\nBevmo')
# result = search('johnnie walker black','sams')
# print(result)

# a = totalwinelink('highland bird blended')

# print(a)