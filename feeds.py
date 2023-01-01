import feedparser

EPISODE_EXCLUDE_LIST = ['B-Sides', 'Departures']


class FeedInfo:
    def __init__(self, name, episode, episode_title, seconds):
        self.name = name
        self.episode = episode
        self.episode_title = episode_title
        self.seconds = seconds

    @classmethod
    def parse(cls, name, xml):
        if xml.get('itunes_title'):
            title = xml.itunes_title
        else:
            title = xml.title

        if xml.get('itunes_episode'):
            episode_number = xml.itunes_episode
        else:
            episode_number = None

        return cls(
            name,
            episode_number,
            title,
            cls.get_duration(xml.itunes_duration)
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

    @staticmethod
    def get_duration(duration):
        if duration.isnumeric():
            return int(duration)
        else:
            return FeedInfo.get_seconds_from_string(duration)

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%d:%02d:%02d" % (hour, minutes, seconds)

    @staticmethod
    def get_seconds_from_string(time_str):
        """Get seconds from time."""
        time_parts = time_str.split(':')
        if len(time_parts) == 3:
            h, m, s = time_parts
        else:
            h = 0
            m, s = time_parts
        return int(h) * 3600 + int(m) * 60 + int(s)

    def format(self):
        return "{} - {}".format(self.name, str(self))

    def __repr__(self):
        return 'FeedInfo<name=%s, episode=%s, duration=%s>' % (self.name, self.episode, self.duration)

    def __str__(self):
        to_return = ""
        if self.episode is not None:
            to_return += "Episode {} ".format(self.episode)
        to_return += "%s (%s)" % (self.episode_title, self.duration)

        return to_return


class FeedInfos(list):
    def title(self):
        return self[0].name

    def sorted(self):
        return sorted(self, key=lambda s: s[0].name)

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
    if title in EPISODE_EXCLUDE_LIST:
        return None

    if len(feed.entries) == 0:
        return None

    for episode in feed.entries:
        feed_infos.append(FeedInfo.parse(title, episode))

    return feed_infos
