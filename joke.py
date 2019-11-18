from requests import request
from dotenv import load_dotenv
import json
import os

load_dotenv()
def get_joke():
    url = 'https://joke3.p.rapidapi.com/v1/joke'
    headers = {
        'x-rapidapi-key': os.getenv('XRAPID_KEY')
        }

    response = request('GET', url, headers=headers)
    json_data = json.loads(response.text)
    return json_data['content']

