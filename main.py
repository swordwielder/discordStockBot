from asyncio.tasks import sleep
import os
import json, discord, asyncio, logging
from dotenv import load_dotenv
import time
import datetime
from expiringdict import ExpiringDict
from weathercall import weatherdata
#from cryptoscrape import displayCrypto
import requests
import re
import random
import string
from aws_scrape import getAWS
from crypto import getCryptoData
from stock import getStockData
from content_detection.imagesave import imageSaver
from  content_detection.s3upload import s3upload
from liquipediascrape import getGameEvents
from joke import get_joke
from speechToEval import recognize_speech_from_mic, calculate
from tts import repeat, speak
from scotch import totalwinelink
from Generate_Games import gambit
from listcrypto import getTopCrypto
from listcrypto import getCryptoPrice
from poshedge import searchPosHedge



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
CRYPTO_NOMICS_TOKEN = os.getenv('CRYPTO_NOMICS_API_KEY')

def discordlogger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    print(logger)



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        members = '\n - '.join([member.name for member in guild.members])
        print('\nTOTAL NUMBER OF USERS IS IN THIS DISCORD\n')
        print(len(guild.members))
        print(guild.name, guild.id)
        print(f'Guild Members:\n - {members}')
        

async def update_stats():
    await client.wait_until_ready()
    # global messages, joined
    channelID=813816622988918815
    # secondID = 797625408433553441
    # print('is this working??')
    # guildID = 797625407960514612
    print(813816622988918815)
    current=0
    while not client.is_closed():
        hedge = searchPosHedge(current)
        if type(hedge) == float:
            current = hedge
            channel = client.get_channel(channelID)
            await channel.send(f'@everyone {hedge}% hedge available https://gambitdataanalytics.web.app/')
        time.sleep(2.5)
        # print('this is a test')
        
        
        

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, StockBot has been waiting for you!'
    )

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if '!recognize' in message.content:
        # use regex to parse the url from the command
        url = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
        imageSaver(url)
        from content_detection.imagedetect import imganalyze
        imganalyze(f'{os.getcwd()}/content_detection/imagebank')
        rando_img_name =''.join(random.choice(string.ascii_lowercase) for i in range(10))
        s3upload(rando_img_name)
        embed = discord.Embed(title="Analysis Photo", description='Object Name with Percentage of Confidence',color=0x00ff00)
        embed.set_image(url=f'https://discordimage.s3.amazonaws.com/{rando_img_name}.jpg')
        await message.channel.send(embed=embed)

    if '!test' in message.content:
        await message.channel.send('@everyone new gambit backdoor hedge available!')

    if '!math' in message.content:
        channel = message.channel
        equation = message.content.replace(' ','')[5:]
        instructions = (
        "\nThe answer for " + equation + ":\n"
        )
        await channel.send(instructions)

        await channel.send(eval(equation))
        # await channel.send(calculate())


    if '!repeat' in message.content:
        channel = message.channel
        await channel.send('Please say the message you want the bot to repeat!')
        await channel.send(repeat())

    if '!games' in message.content:
        esport = message.content.split(' ')[1]
        try:
            matchups= getGameEvents(esport)
        except Exception:
            await message.channel.send('Please Input Valid Argument see !help for details')

        embed = discord.Embed(title=f'Current {esport} Schedule', description='Scores and Upcoming Game events')
        for matchup in matchups:
            embed.add_field(name="Team 1", value=f'```{matchup["team_left"]}```', inline=True)
            embed.add_field(name=f"({matchup['time']})", value=f'```{matchup["status"]}```', inline=True)
            embed.add_field(name="Team 2", value=f'```{matchup["team_right"]}```', inline=True)

        await message.channel.send(embed=embed)

    if '!gambit' in message.content:
        gambitGames = gambit()
        # embed = discord.Embed(title="Games today", description='Here are the Games today on Gambit', color=0x00ff00)
        # await message.channel.send(embed=embed)
        for i in gambitGames:
            await message.channel.send(i)
        # await message.channel.send(embed=embed)

    if '!joke' in message.content:
        joke=get_joke()
        await message.channel.send(f'If you insist {str(message.author)[:-5]}... :smirk: \n{joke}  \n\n give me a 👍 or 👎 to let me know how I did')

        def check(reaction, user):
            if reaction.emoji=='👍':
                return user == message.author and str(reaction.emoji) == '👍'
            else:
                return user == message.author and str(reaction.emoji) == '👎'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send('👎')
        else:
            if reaction.emoji== '👍':
                await message.channel.send(':stuck_out_tongue_closed_eyes: That was a good one, That was a good one.  I\'ll keep it up')
            elif reaction.emoji== '👎':
                await message.channel.send(':weary: I got this next time! ')

    if '!wine' in message.content:
        
        channel = message.channel
        scotch = message.content[5:]
        
        result = totalwinelink(scotch)
        if result:
            embed = discord.Embed(title="TotalWine", description='Here are the TotalWine result:', color=0x00ff00)
            embed.add_field(name="```Name```", value=result[0], inline=False)
            embed.add_field(name="```Quantity```", value=result[1], inline=False)
            embed.add_field(name="```Rating```", value=result[2], inline=False)
            embed.add_field(name="```Reviews```", value=result[3], inline=False)
            embed.add_field(name="```Price```", value=result[4], inline=False)
            # embed.add_field(name="```Name```", value=result[5], inline=False)
            # embed.add_field(name="```Quantity```", value=result[6], inline=False)
            # embed.add_field(name="```Rating```", value=result[7], inline=False)
            # embed.add_field(name="```Reviews```", value=result[8], inline=False)
            # embed.add_field(name="```Price```", value=result[9], inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('No Result Found!')

    if '!awsloft' in message.content:
        channel = message.channel
        upcoming_schedule = getAWS()
        if (upcoming_schedule):
            print(upcoming_schedule)
            first= upcoming_schedule[0][0].split('|')[0]
            last=upcoming_schedule[len(upcoming_schedule)-1][0].split('|')[0]
            if len(first)>1 and len(last):
                embed = discord.Embed(title="Upcoming AWS Schedule", description=f'{first}-{last} | [Link](<https://aws.amazon.com/start-ups/loft/ny-loft/>)')
                count=1
                spacer='----------------------------------------------------------------------------'
                embed.add_field(name=f'{spacer}\nWeek #{count}', value=f'**{spacer}---**', inline=False)
                for event in upcoming_schedule:
                    date=event[0]
                    title=event[1].split(':')[0]
                    link=event[2]
                    linktag=f' | [Event](<{link}>)'
                    if link == '':
                        linktag=''
                    embed.add_field(name=f'{date}', value=f'{title}{linktag}', inline=True)
                    if ('Friday' in date.split('|')[1] and count<4):
                        count+=1
                        embed.add_field(name=f'{spacer}\nWeek #{count}', value=f'**{spacer}---**', inline=False)
                await message.channel.send(embed=embed)
        else:
            await channel.send('No Schedule found!')
        

    if '$findstock' in message.content:
        # Remove whitespaces from input for exception handling
        ticker = message.content.replace(' ','')[10:]
        if len(api_limit) < 5:
            try:
                stockinfo = getStockData(ticker, api_limit)
                symbol, price, volume, \
                change, percent_change, \
                high, low= stockinfo['01. symbol'], stockinfo['05. price'],stockinfo['06. volume'], \
                           stockinfo['09. change'], stockinfo['10. change percent'], \
                           stockinfo['03. high'], stockinfo['04. low']

                colorformat = 0xBF270C
                diff='-'
                if float(change) > 0:
                    colorformat= 0x00ff00
                    diff='+'
                embed = discord.Embed(title="Stock", description=symbol, color=colorformat)

                embed.add_field(name="Price", value=f'${price}', inline=True)
                embed.add_field(name="Volume", value=volume, inline=True)
                embed.add_field(name="High", value=high, inline=True)
                embed.add_field(name="Low", value=low, inline=True)

                embed.add_field(name="Price Change", value=f'```diff\n{diff}${change}\n```', inline=True)
                embed.add_field(name="% Change", value=f'```diff\n{diff}{percent_change}\n```', inline=True)
                await message.channel.send(embed=embed)

            except KeyError:
                await message.channel.send('Invalid Stock Ticker. Ex: $FINDSTOCK AAPL')
        else:
            print(api_limit,'Failed')
            await message.channel.send('Too Many Calls Please Wait')

    if '$findcrypto' in message.content:
        cryptosymbol = message.content.replace(' ', '')[11:]
        symbol = cryptosymbol.upper()
        try:
            info = f'https://api.nomics.com/v1/prices?key={CRYPTO_NOMICS_TOKEN}&format=json'
            response = requests.get(info)
            
            data = response.text
            json_data = json.loads(data)
            
            
            price = (str('$'+next(item['price'] for item in json_data if item["currency"] == symbol)))
            # print(symbol)
            # print('the price is;')
            # print(price)
            # return price
            # cryptoprice = getCryptoPrice(symbol)
            # name = cryptoinfo['name']
            # rank = cryptoinfo['rank']
            # Pulls logo from online source with PNG because SVG is not compatible
            # icon = f'https://coincodex.com/en/resources/images/admin/coins/{name}.png'

            # time = cryptoinfo['price_date']

            # alter decimal based on price
            # decimalcount=2
            # if float(cryptoinfo['price']) < 1:
            #     decimalcount = 6

            # price = round(float(cryptoinfo['price']), decimalcount)
            # price_change = round(float(cryptoinfo['1d']['price_change']),decimalcount)
            # percent_change = round(float(cryptoinfo['1d']['price_change_pct'])*100,2)
            await message.channel.send(price)
            # embed = discord.Embed(title="Rank Coin Symbol", description=f'#({symbol})', color=0x00ff00)
            # embed.set_thumbnail(url=icon)
            # embed.add_field(name="Date", value=time, inline=True)
            # embed.add_field(name="Price", value=cryptoprice, inline=True)
            # embed.add_field(name="Change (24 Hr)", value=f'${price_change}', inline=True)
            # embed.add_field(name="% Change (24 Hr)", value=f'{percent_change}%', inline=True)
            # await message.channel.send(embed=embed)
        except:
            await message.channel.send('You have entered an invalid ticker')

    #Lists the crypto currencies
    if '!listcrypto' in message.content:
        # loop = message.content.replace(' ', '')[11:]
        
        info = getTopCrypto()
        
        # response = requests.get(info)
        # print('reponse')
        # print(response)
        # data = response.text
        # json_data = json.loads(data)
        # count = 1
        #embed = discord.Embed(title="Crypto Currency List", color=0x00ff00)
        #await message.channel.send(embed=embed)
        await message.channel.send('Top Crypto Currency List')
        for i in info:
            await message.channel.send(i)
        # new=3
        # activate=True
        # if loop:
        #     if loop.isnumeric():
        #         new = int(loop)
        #     else:
        #         activate=False
        # if activate:
        #     #await message.channel.send('Symbol')
        #     for currency in json_data:
        #         #print(currency['currency'], currency['name'])
        #         #embed.add_field(name="Symbol", value=f'{currency["currency"]}', inline=True)
        #         #embed.add_field(name="Name", value=f'{currency["name"]}', inline=False)
        #         await message.channel.send(str(count)+". " + f'{currency["currency"]}\t{currency["name"]}')

        #         if count == new:
        #             break
        #         count += 1

    #Lists all the commands for the bot
    if message.content == '!help':
        embed = discord.Embed(title="Help Menu", description='Here are a list of Commands and their uses', color=0x00ff00)
        embed.add_field(name="```$findcrypto [Symbol]```", value='This will return daily information for the coin')
        embed.add_field(name="```$findstock [Symbol]```", value='This will return daily information for the stock')
        embed.add_field(name="```!listcrypto```", value='Lists the top 3 Crypto Currencies ', inline=False)
        embed.add_field(name="```!joke```", value='Tells a joke', inline=False)
        embed.add_field(name="```!weather```", value='Tells the 5 days forecast of NYC', inline=False)
        embed.add_field(name="```!listcrypto```", value='Lists the top 3 Crypto Currencies ', inline=False)
        
        embed.add_field(name="```!games [game]```", value='Lists the upcoming matches (starcraft2,overwatch,pubg,dota2,etc.) ', inline=False)
        embed.add_field(name="```!awsloft```", value='Lists the schedule for AWS loft located in lower Manhattan ', inline=False)
        embed.add_field(name="```!recognize [Image Url]```", value='Uses Machine Learning to Detect Objects in Image', inline=False)
        # embed.add_field(name="```!repeat```", value='Say something for the bot to repeat!', inline=False)
        embed.add_field(name="```!math```", value='Calculates basic math equations ex: !math 2+2*2', inline=False)
        embed.add_field(name="```!wine [name]```", value='scrapes the total wine website data for stats on a wine', inline=False)
        embed.add_field(name="```!help```", value='A manual for all of the bot functions ', inline=False)
        embed.add_field(name="```Invite the bot```", value='https://discord.com/api/oauth2/authorize?client_id=623200683964891136&permissions=271973456&scope=bot', inline=False)
        embed.add_field(name="```note from devs```", value='currently making a better discord checkout: https://anychatio.herokuapp.com/ for early access, for questions and concerns, email anychatio@gmail.com', inline=False)
        await message.channel.send(embed=embed)

    if message.content=='!weather':
        weather = weatherdata()
        # for each in weather:
        #     print(each)
        embed = discord.Embed(title="Weather", description='Current 5 day forecast', color=0x00ff00)
        embed.add_field(name="Current:", value=str(weather[0])[11:], inline=True)
        embed.add_field(name="Temperature:", value=str(weather[1])+"°F", inline=True)
        embed.add_field(name="Summary:", value=str(weather[2]), inline=True)
        i=6
        spacer = '----------------------------------------------------------------------------'
        while i < len(weather):
            embed.add_field(name=f"\n{spacer}\nDate:", value=str(weather[i-3]), inline=False)
            embed.add_field(name=f"\n{spacer}\nHigh:", value=str(weather[i-1])+"°F", inline=True)
            embed.add_field(name="Low:", value=str(weather[i])+"°F", inline=True)
            embed.add_field(name="Summary:", value=str(weather[i - 2]), inline=True)
            i+=4
            if i>=24:
                break
        await message.channel.send(embed=embed)

api_limit = ExpiringDict(max_len=100, max_age_seconds=60)

async def degen():
    await client.wait_until_ready()
    # global messages, joined
    # channelID=813816622988918815
    secondID = 797625408433553441
    # print('is this working??')
    # guildID = 797625407960514612
    print(813816622988918815)
    current=0
    while not client.is_closed():
        # hedge = searchPosHedge(current)
        # if type(hedge) == float:
        #     current = hedge
        channel = client.get_channel(secondID)
        await channel.send('grinder is the biggest degen in existence.')
        time.sleep(5.5)
        # print('this is a test')


# bot = client.Bot(command_prefix="$")
# client.loop.create_task(degen())
# @bot.command()
# async def info():
# client.loop.create_task(update_stats())


if __name__ == '__main__':
    client.run(TOKEN)
