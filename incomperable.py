from bs4 import BeautifulSoup as Soup
import requests

from feeds import FeedInfos, get_show_episode_durations

BASE_URL = 'https://www.theincomparable.com'
FEED_BASE_URL = 'https://feeds.theincomparable.com'


def get_feed_urls(urls):
    return [FEED_BASE_URL + url for url in urls]


def get_all_shows(soup):

    active_hrefs = [a['href'] for a in soup.find_all('a', {'class': 'podcast-img'}, href=True)]
    retired_hrefs = [a['href'] for div in soup.find_all(
        'div', {'class': 'podcast-info'}) for a in div.find_all('a', href=True)]
    return [href for href in active_hrefs + retired_hrefs]


def get_data():
    content = requests.get('https://www.theincomparable.com/shows').content

    soup = Soup(content, features="html.parser")
    shows = get_all_shows(soup)
    return get_feed_urls(shows)
