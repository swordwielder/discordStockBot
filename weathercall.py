from datetime import datetime, timedelta
import requests
import json
import os
import json, discord
from dotenv import load_dotenv


load_dotenv()
DARK_TOKEN=os.getenv('DARK_SKY_API')

def weatherdata():
    url = f'https://api.darksky.net/forecast/{DARK_TOKEN}/42.3601,-71.0589'
    response = requests.get(url)
    #print("response is ",response)
    data = response.text
    json_data = json.loads(data)
    #print(json_data)
    #dt_object = datetime.fromtimestamp(json_data['currently']['time'])

    #print("TIME IS: ", dt_object)
    embed = discord.Embed(title="Weather", description='7 day forecast', color=0x00ff00)
    # embed.set_thumbnail(url=json_data['currently']['icon'])
    # embed.add_field(name="Time:", value=datetime.fromtimestamp(f"{json_data['currently']['time']}"), inline=True)
    # embed.add_field(name="Current Temperature:", value=f"{json_data['currently']['temperature']}", inline=True)
    # embed.add_field(name="% Change (24 Hr)", value=f"{json_data['currently']['summary']}", inline=True)

    weather=[]
    weather.append(datetime.fromtimestamp(json_data['currently']['time']))
    weather.append(json_data['currently']['temperature'])
    weather.append(json_data['currently']['summary'])

    # adding and subtracting time using +-timedelta(days, minutes, seconds)
    for each in json_data['daily']['data']:
        weather.append((datetime.fromtimestamp(each['time'])).strftime('%m/%d/%Y'))
        weather.append(each['summary'])
        weather.append(each['temperatureHigh'])
        weather.append(each['temperatureLow'])
        # print("Date: ", (datetime.fromtimestamp(each['time'])).strftime('%m/%d/%Y'))
        # print("Summary ", each['summary'])
        # print("High ", each['temperatureHigh'])
        # print("Low ", each['temperatureLow'],"\n")

    return weather
    #print("time is " , datetime.fromtimestamp(json_data['daily']['data'][0]['time']))
    #print("time is " , datetime.fromtimestamp(json_data['daily']['data'][1]['time']))
    #print("time is " , datetime.fromtimestamp(json_data['daily']['data'][2]['time']))
    #print("time is " , datetime.fromtimestamp(json_data['daily']['data'][3]['time']))
    #print("type(dt_object) =", type(dt_object))




if __name__ == '__main__':
    weatherdata()