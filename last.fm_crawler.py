from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd
from StringParsers import DateParser, TimeParser

user = 'takieo'
lastfm = f'https://www.last.fm/user/{user}/library'

uClient = uReq(lastfm)
library_html = uClient.read()
uClient.close()

# bs4.BeautifulSoup /with whole website
library_soup = soup(library_html, 'html.parser')

# number of pages in library
all_pages = library_soup.findAll('li', {'class':'pagination-page'})[::-1][0].get_text().strip('\n')

data = []

for page in range(1, int(all_pages)+1):

    lastfm = f'https://www.last.fm/user/{user}/library?page={page}'

    uClient = uReq(lastfm)
    library_html = uClient.read()
    uClient.close()

    library_soup = soup(library_html, 'html.parser')
    library_page = library_soup.findAll('tr', {'class': 'chartlist-row'})

    for container in library_page:

        Track = container.findAll('td', {'class': 'chartlist-name'})[0].get_text().strip('\n')
        Artist = container.findAll('td', {'class': 'chartlist-artist'})[0].get_text().strip('\n')
        
        Timestamp = container.findAll('td', {'class': 'chartlist-timestamp chartlist-timestamp--lang-en'})[0].find('span')['title']
        
        Date = DateParser(Timestamp)
        Time = TimeParser(Timestamp)

        data.append([Artist, Track, Date, Time])

df = pd.DataFrame(data, columns = ['Artist', 'Track', 'Date', 'Time'])

df.to_csv(f'lastfm_{user}.csv', index=False, encoding='utf-8')
