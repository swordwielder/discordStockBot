import requests, json, os
from time import time
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
STOCK_TOKEN = os.getenv('STOCK_API_KEY')
def getStockData(ticker,TTLcache):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&interval=5min&apikey={STOCK_TOKEN}'
    response = requests.get(url)
    data = response.text
    json_data = json.loads(data)
    ts = time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    TTLcache[st]=1
    print(TTLcache, len(TTLcache), 'Succeeded')
    return json_data['Global Quote']