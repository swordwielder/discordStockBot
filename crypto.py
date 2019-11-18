import requests, json, os
from dotenv import load_dotenv

load_dotenv()
CRYPTO_NOMICS_TOKEN = os.getenv('CRYPTO_NOMICS_API_KEY')
def getCryptoData(symbol):
    # coinapi=f'http://rest-sandbox.coinapi.io/v1/exchangerate/{symbol}/USD/?apikey={CRYPTO_TOKEN}'
    nomics=f'https://api.nomics.com/v1/currencies/ticker?key={CRYPTO_NOMICS_TOKEN}&ids={symbol}&interval=1d,30d&convert=USD&include-transparency=false'
    response = requests.get(nomics)
    data = response.text
    json_data = json.loads(data)
    return json_data[0]