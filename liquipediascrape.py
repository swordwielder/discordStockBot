from bs4 import BeautifulSoup
import requests

def dateformat(utc):
    justtime=utc.split('- ')[1].split(' ')
    est_time= int(justtime[0].split(':')[0])-4
    if est_time < 0:
        est_time+=24
    finaltime=':'.join([str(est_time),justtime[0].split(':')[1]])
    return finaltime+' EST'

def getGameEvents(esport):
    url = f'https://liquipedia.net/{esport}'
    home= 'https://liquipedia.net'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    upcoming_matches = soup.find_all(class_='table table-striped infobox_matches_content')
    upcoming=False
    count=0
    matchups = []
    for match in upcoming_matches:
        status = match.find(class_='versus').text.strip('\n')

        # handing hidden pages found in csgo
        if 'vs' in status:
            upcoming =True
        if upcoming == True and 'vs' not in status:
            break

        if 'vs' not in status:
            time = 'Live!'
        else:
            time = dateformat(match.find(class_='match-countdown').text)

        team_left = match.find(class_='team-left').find('span').text
        team_right = match.find(class_='team-right').find('span').text
        if esport == 'starcraft2':
            team_left_icon= home + match.findAll('img')[1]['src']
            team_right_icon = home + match.findAll('img')[2]['src']
        else:
            team_left_icon = home + match.findAll('img')[0]['src']
            team_right_icon = home + match.findAll('img')[1]['src']
        matchups.append({'time':time,
                         'team_left':team_left,
                         'team_left_icon':team_left_icon,
                         'status':status,
                         'team_right_icon':team_right_icon,
                         'team_right':team_right})
        print([time],[team_left ,team_left_icon ],[team_right, team_right_icon], sep =status)

    return matchups
