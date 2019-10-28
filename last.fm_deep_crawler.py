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

for page in range(1, 5):#int(all_pages)+1):

    lastfm = f'https://www.last.fm/user/{user}/library?page={page}'

    uClient = uReq(lastfm)
    library_html = uClient.read()
    uClient.close()

    library_soup = soup(library_html, 'html.parser')
    library_page = library_soup.findAll('tr', {'class': 'chartlist-row'})

    for container in library_page:

        # LIBRARY PART
        Track = container.findAll('td', {'class': 'chartlist-name'})[0].get_text().strip('\n')
        Artist = container.findAll('td', {'class': 'chartlist-artist'})[0].get_text().strip('\n')

        Timestamp = container.findAll('td', {'class': 'chartlist-timestamp chartlist-timestamp--lang-en'})[0].find('span')['title']

        Date = DateParser(Timestamp)
        Time = TimeParser(Timestamp)

        # TRACK DETAILS PART
        href = container.find_all('a', {'class':''})[0].get('href')
        v = f'https://www.last.fm{href}'

        uClient = uReq(track_html)
        track_html_open = uClient.read()
        uClient.close()

        track_soup = soup(track_html_open, 'html.parser')

        tag_list = track_soup.find_all('ul', {'class':'tags-list tags-list--global'})[0].find_all('li', {'class':'tag'})
        Tags = []
        for i, value in enumerate(tag_list):
            Tags.append(value.get_text())

        Length = track_soup.find_all('dd', {'class':'catalogue-metadata-description'})[0].get_text().strip('\n').strip(' ').strip('\n')
        Album = track_soup.find_all('h4', {'class':'source-album-name'})[0].get_text()

        # APPEND LIST
        data.append([Artist, Track, Date, Time, Tags, Length, Album])

df = pd.DataFrame(data, columns = ['Artist', 'Track', 'Date', 'Time', 'Tags', 'Length', 'Album'])

column_order = ['Artist', 'Album', 'Track', 'Length', 'Tags', 'Date', 'Time']

df.to_csv(f'lastfm_deep_{user}.csv',
          columns = column_order,
          index=False,
          encoding='utf-8')
