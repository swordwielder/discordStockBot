import requests
import os
import json
import datetime
import time
from datetime import timedelta
import dateutil.parser
from bs4 import BeautifulSoup
from datetime import datetime
import threading

# For sports, if you want to add another category, all you need to is add the link to the list
alllinks = ["https://sports.intertops.eu/en/Bets/Basketball/NCAAB-Lines/1068",
"https://sports.intertops.eu/en/Bets/Basketball/NBA-Lines/1070", "https://sports.intertops.eu/en/Bets/American-Football/NFL-Lines/1018",
"https://sports.intertops.eu/en/Bets/Ice-Hockey/NHL-Lines/1064", "https://sports.intertops.eu/en/Bets/Baseball/MLB-Spring-Training/1114"]

#Initialize some indices of the list so we can modify based on specification later on
allrequests = ['hehexd'] * len(alllinks)
allBSoup = []

def doTheThing(number):
	global alllinks
	global allrequests
	global allBSoup
	
	thisLink = alllinks[number]
	allrequests[number] = requests.get(thisLink)	#Specify List Index instead of append()
	print('Request #' + str(number))				#Each thread will work on a different element of the list avoiding race condition
	allBSoup.append(BeautifulSoup(allrequests[number].content,'lxml'))
	print('Soup #' + str(number))

def doThisFirst():
	global resp
	global json_resp
	
	resp = requests.get('https://api.gambitprofit.com/gambit-plays?_sort=PlayDate:DESC')
	json_resp = json.loads(resp.content)
	
if __name__ == "__main__":
	start = time.time()
	
	requestnumber = 1
	soupnumber = 1
	linkSize = len(alllinks)
	threads = []
	
	sourceFile = open('raw.txt', 'w')
	
	firstThread = threading.Thread(target=doThisFirst)
	firstThread.start()
	
	for x in range(linkSize):
		thread = threading.Thread(target=doTheThing, args=(x,))
		threads.append(thread)
		thread.start()
	
	for thread in threads:
		thread.join()
	
	firstThread.join()
	
	# Fetch all the games available on Gambit
	gambitGames = []
	for play in json_resp:
		if play['PlayDate'] > datetime.now().isoformat()[:-3]+'Z':
			d = dateutil.parser.parse(play['PlayDate'])
			gambitGames.append(play['Team1']['Name'])
			gambitGames.append(play['Team2']['Name'])

	for i in allBSoup:
		links = i.find_all('a', class_="seeall cl-e")
		for link in links:
			# print(link)
			# Search to see if the game is on Gambit before adding it to the txt
			if link.b.div.string in gambitGames:
				fullLink = link.b.div.string + "; " + "https://sports.intertops.eu" + link.attrs['href']
				print(fullLink, file = sourceFile)

	sourceFile.close()

	# Remove the dupes
	lines_seen = set() # holds lines already seen
	gamesList = []
	for line in open('raw.txt', "r"):
		if line not in lines_seen: # not a duplicate
			gamesList.append(line)
			lines_seen.add(line)

	os.remove('raw.txt')
	
	for game in gamesList:
		print(game)

	end = time.time()
	print(str(end - start) + ' seconds to finish!')