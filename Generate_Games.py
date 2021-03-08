import requests
import os
import json
import datetime
from datetime import timedelta
import dateutil.parser
from bs4 import BeautifulSoup
from datetime import datetime




def gambit():
	alllinks = ["https://sports.intertops.eu/en/Bets/Basketball/NCAAB-Lines/1068",
	"https://sports.intertops.eu/en/Bets/Basketball/NBA-Lines/1070", "https://sports.intertops.eu/en/Bets/American-Football/NFL-Lines/1018",
	"https://sports.intertops.eu/en/Bets/Ice-Hockey/NHL-Lines/1064", "https://sports.intertops.eu/en/Bets/Baseball/MLB-Spring-Training/1114", 
	"https://sports.intertops.eu/en/Bets/Esports/40", 
	"https://sports.intertops.eu/en/Bets/Tennis/26" , "https://sports.intertops.eu/en/Bets/Baseball/4"]
	resp = requests.get('https://api.gambitprofit.com/gambit-plays?_sort=PlayDate:DESC')

	json_resp = json.loads(resp.content)
	sourceFile = open('raw.txt', 'w')

	allrequests=[]
	for i in alllinks:
		allrequests.append(requests.get(i))

	allBSoup=[]
	for i in allrequests:
		allBSoup.append(BeautifulSoup(i.content,'lxml'))
		
	sourceFile = open('raw.txt', 'w')

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
			# Search to see if the game is on Gambit before adding it to the txt
			if link.b.div.string in gambitGames:
				fullLink = link.b.div.string + "; " + "https://sports.intertops.eu" + link.attrs['href']
				print(fullLink, file = sourceFile)


	sourceFile.close()

	# Remove the dupes
	lines_seen = set() # holds lines already seen
	allgambitgames = []
	outfile = open('List_of_Games.txt', "w")
	for line in open('raw.txt', "r"):
		if line not in lines_seen: # not a duplicate
			
			outfile.write(line)
			allgambitgames.append(line)
			lines_seen.add(line)


	outfile.close()
	return allgambitgames

# os.remove("raw.txt")

