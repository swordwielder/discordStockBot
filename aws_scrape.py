from bs4 import BeautifulSoup
import requests


def getAWS():
    url = 'https://aws.amazon.com/start-ups/loft/ny-loft/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    titlearray = soup.findAll(class_='a-link-section-expander accordion-toggle collapsed')
    contentarray = soup.findAll(class_='accordion-body')
    event_info = []
    for i in range(len(titlearray)):
        try:
            title = contentarray[i].find('a').text
            link = contentarray[i].find('a', href=True)['href']
        except Exception:
            link = ''
            title = 'CO-WORKING'
        date = titlearray[i].find('h3').text.split('-')[0]

        # print(date, title, link, sep='\t||\t')
        event_info.append([date, title, link])

    return event_info
