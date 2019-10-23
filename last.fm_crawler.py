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
library_page = library_soup.findAll("tr", {'class': 'chartlist-row'})


library_page.findAll("td", {'class': 'chartlist-artist'})
