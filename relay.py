from bs4 import BeautifulSoup as Soup
import requests
import feedparser
import csv

BASE_URL = 'https://www.relay.fm'

EXCLUDE_LIST = ['B-Sides', 'Departures']


class FeedInfo:
    def __init__(self, name, episode, seconds):
        self.name = name
        self.episode = episode
        self.seconds = seconds

    @classmethod
    def parse(cls, name, xml):
        return cls(
            name,
            xml.itunes_episode,
            int(xml.itunes_duration)
        )

    @property
    def duration(self):
        return self.convert(self.seconds)

    def asdict(self):
        return dict(
            name=self.name,
            episode=self.episode,
            seconds=self.seconds
        )

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def __repr__(self):
        return 'FeedInfo<name=%s, episode=%s, duration=%s>' % (self.name, self.episode, self.duration)

    def __str__(self):
        return "%s - %s (%s)" % (self.name, self.episode, self.duration)


class FeedInfos(list):
    def title(self):
        return self[0].name

    def get_longest_episode(self):
        return max(self.flatten(), key=lambda s: s.duration)

    def get_shortest_episode(self):
        return min(self.flatten(), key=lambda s: s.duration)

    def flatten(self):
        if isinstance(self[0], FeedInfos):
            return [val for sublist in self for val in sublist]
        return self


def get_show_episode_durations(feed_url):
    feed_infos = FeedInfos()
    feed = feedparser.parse(feed_url)
    title = feed.channel.title
    if title in EXCLUDE_LIST:
        return None
    for episode in feed.entries:
        feed_infos.append(FeedInfo.parse(title, episode))
    return feed_infos


def get_feed_urls(urls):
    return [url + '/feed' for url in urls]


def get_all_shows(soup):
    hrefs = [a['href'] for h3 in soup.find_all(
        'h3', {'class': 'broadcast__name'}) for a in h3.find_all('a', href=True)]
    return [BASE_URL + href for href in hrefs]


def output_as_csv(shows):
    with open('/Users/rjames/Desktop/shows.csv', 'w') as csvfile:
        fieldnames = ['name', 'episode', 'seconds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for episode in shows.flatten():
            writer.writerow(episode.asdict())


def get_data():
    content = requests.get('https://www.relay.fm/shows').content

    soup = Soup(content, features="html.parser")
    shows = get_all_shows(soup)
    feed_urls = get_feed_urls(shows)

    all_episodes = FeedInfos()
    for feed_url in feed_urls:
        show_info = get_show_episode_durations(feed_url)
        if show_info is not None:
            all_episodes.append(show_info)

    print(all_episodes.get_longest_episode(),
          all_episodes.get_shortest_episode())

    for show in all_episodes:
        print(show.get_longest_episode(),
              show.get_shortest_episode())

    return all_episodes
