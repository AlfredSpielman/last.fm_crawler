from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

user = 'takieo'
lastfm = f'https://www.last.fm/user/{user}/library'

uClient = uReq(lastfm)
library_html = uClient.read()
uClient.close()

# bs4.BeautifulSoup /with whole website
library_soup = soup(library_html, 'html.parser')

# bs4.element.ResultSet /with all containers
library_page = library_soup.findAll('tr', {'class': 'chartlist-row'})

dict_months = {
    'Jan':1,
    'Feb':2,
    'Mar':3,
    'Apr':4,
    'May':5,
    'Jun':6,
    'Jul':7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12}

def DatestampParser(datestamp):
    
    datestamp_list = datestamp.split(' ')
    
    day = int(datestamp_list[1])
    month = dict_months[str(datestamp_list[2])]
    year = int(datestamp_list[3][:4])  
    #hour
    #minute

data = []

for container in library_page:
    Artist_full = str(container.findAll('td', {'class': 'chartlist-name'}))
    Artist_short = Artist_full[(Artist_full.find('title=') + 6):(len(Artist_full)-11)]
    Artist = Artist_short[Artist_short.find('>')+1:]
    
    Track_full = str(container.findAll('td', {'class': 'chartlist-artist'}))
    Track_short = Track_full[(Track_full.find('title=')+6):(len(Track_full)-11)]
    Track = Track_short[Track_short.find('>')+1:]
    
    Timestamp_full= str(container)[str(container).find('timestamp')+54:len(str(container))-13]
    Timestamp_short = Timestamp_full[:Timestamp_full.find('>')-1]
    Timestamp = DatestampParser(Timestamp_short)

    data.append([Artist, Track, Timestamp])
