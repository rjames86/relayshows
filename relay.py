from bs4 import BeautifulSoup as Soup
import requests

from feeds import FeedInfos, get_show_episode_durations

BASE_URL = 'https://www.relay.fm'


def get_feed_urls(urls):
    return [url + '/feed' for url in urls]


def get_all_shows(soup):
    hrefs = [a['href'] for h3 in soup.find_all(
        'h3', {'class': 'broadcast__name'}) for a in h3.find_all('a', href=True)]
    return [BASE_URL + href for href in hrefs]


def get_data():
    content = requests.get('https://www.relay.fm/shows').content

    soup = Soup(content, features="html.parser")
    shows = get_all_shows(soup)
    return get_feed_urls(shows)
