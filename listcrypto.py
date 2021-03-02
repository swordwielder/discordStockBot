import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()


def getTopCrypto():

    CRYPTO_NOMICS_TOKEN = os.getenv('CRYPTO_NOMICS_API_KEY')

    info = f'https://api.nomics.com/v1/prices?key={CRYPTO_NOMICS_TOKEN}&format=json'
    # print('info')
    # print(info)
    response = requests.get(info)
    # print('reponse')
    # print(response)
    data = response.text
    json_data = json.loads(data)
    topCrypto=[]
    # btc=next(item['price'][:-6] for item in json_data if item["currency"] == "BTC")
    # print(btc)
    topCrypto.append(str('BTC price: $'+next(item['price'][:-6] for item in json_data if item["currency"] == "BTC")))
    topCrypto.append(str('ETH price: $'+next(item['price'][:-6] for item in json_data if item["currency"] == "ETH")))
    topCrypto.append(str('LTC price: $'+next(item['price'][:-6] for item in json_data if item["currency"] == "LTC")))
    # print('BTC price: $'+next(item['price'][:-6] for item in json_data if item["currency"] == "BTC"))
    # print('ETH price: $'+next(item['price'][:-6] for item in json_data if item["currency"] == "ETH"))
    # print('LTC price: $'+next(item['price'][:-6] for item in json_data if item["currency"] == "LTC"))
    return topCrypto

    # print(json_data.value('BTC'))
    # count = 1
def getCryptoPrice(symbol):
    info = f'https://api.nomics.com/v1/prices?key={CRYPTO_NOMICS_TOKEN}&format=json'
    response = requests.get(info)
    
    data = response.text
    json_data = json.loads(data)
    
    
    price = (str('$'+next(item['price'][:-6] for item in json_data if item["currency"] == symbol)))
    print(symbol)
    print('the price is;')
    print(price)
    return price