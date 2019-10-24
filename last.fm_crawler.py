from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

user = 'takieo'
lastfm = f'https://www.last.fm/user/{user}/library'

uClient = uReq(lastfm)
library_html = uClient.read()
uClient.close()

# bs4.BeautifulSoup /with whole website
library_soup = soup(library_html, 'html.parser')

# number of pages in library
library_pages = library_soup.findAll('li', {'class':'pagination-page'})
all_pages_long = str(library_pages[::-1][0])
all_pages_short = all_pages_long[all_pages_long.find('page=')+5:]
all_pages = all_pages_short[:all_pages_short.find('"')]

dict_months = {'Jan':'01', 'Feb':'02', 'Mar':'03',
               'Apr':'04', 'May':'05', 'Jun':'06',
               'Jul':'07', 'Aug':'08', 'Sep':'09',
               'Oct':'10', 'Nov':'11', 'Dec':'12'}

def DateParser(datestamp):
    
    datestamp_list = datestamp.split(' ')
    
    day = int(datestamp_list[1])
    month = dict_months[str(datestamp_list[2])]
    year = int(datestamp_list[3][:4])  
    
    day = '0' + str(day) if day<10 else str(day)

    return f'{year}-{month}-{day}'

def TimeParser(datestamp):

    datestamp_list = datestamp.split(' ')
    time_long = str(datestamp_list[4])[:-2].split(":")
    
    hour = int(time_long[0])
    minute = str(time_long[1])
    
    if str(datestamp_list[4])[-2:] == 'pm': hour += 12
    hour = '0' + str(hour) if hour<10 else str(hour)

    return f'{hour}:{minute}'

data = []

for page in range(1, int(all_pages)+1):

    lastfm = f'https://www.last.fm/user/{user}/library?page={page}'

    uClient = uReq(lastfm)
    library_html = uClient.read()
    uClient.close()

    # bs4.BeautifulSoup /with whole website
    library_soup = soup(library_html, 'html.parser')

    # bs4.element.ResultSet /with all containers
    library_page = library_soup.findAll('tr', {'class': 'chartlist-row'})

    for container in library_page:

        Track_full = str(container.findAll('td', {'class': 'chartlist-name'}))
        Track_short = Track_full[(Track_full.find('title=') + 6):(len(Track_full)-11)]
        Track = Track_short[Track_short.find('>')+1:].replace('&amp;', '&')
    
        Artist_full = str(container.findAll('td', {'class': 'chartlist-artist'}))
        Artist_short = Artist_full[(Artist_full.find('title=')+6):(len(Artist_full)-11)]
        Artist = Artist_short[Artist_short.find('>')+1:].replace('&amp;', '&')

        Timestamp_full= str(container)[str(container).find('timestamp')+54:len(str(container))-13]
        Timestamp_short = Timestamp_full[:Timestamp_full.find('>')-1]
        Date = DateParser(Timestamp_short)
        Time = TimeParser(Timestamp_short)

        data.append([Artist, Track, Date, Time])

df = pd.DataFrame(data, columns = ['Artist', 'Track', 'Date', 'Time'])

df.to_csv(f'lastfm_{user}.csv', index=False, encoding='utf-8')
