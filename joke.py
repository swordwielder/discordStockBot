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
    print('The header')
    print(headers)
    response = request('GET', url, headers=headers)
    
    try:
        json_data = json.loads(response.text)
    
        return json_data['content'] 
    except:
        return 'Something happened to the joke Database! :scream:'

