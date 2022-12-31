from feeds import FeedInfos, get_show_episode_durations
from relay import get_data
from chart import chart_show
from update_readme import update_readme


class PodcastNetwork:
    def __init__(self, name, feeds):
        self.name = name
        self.feeds = feeds
        self._show_durations = None

    def add_feeds(self, feeds):
        self.feeds.extend(feeds)

    def add_feed(self, feed):
        self.add_feeds([feed])

    @property
    def show_durations(self):
        if self._show_durations is None:
            all_episodes = FeedInfos()
            for feed_url in self.feeds:
                show_info = get_show_episode_durations(feed_url)
                if show_info is not None:
                    all_episodes.append(show_info)

            self._show_durations = all_episodes
        return self._show_durations


all_networks = [
    PodcastNetwork('Relay.fm', get_data()),
    PodcastNetwork('ATP', ['https://cdn.atp.fm/rss/public']),
]

for network in all_networks:
    for show in network.show_durations:
        chart_show(show)

update_readme(all_networks)
