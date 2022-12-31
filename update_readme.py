from urllib.parse import quote
import re


def update_readme(all_episodes):
    TEMPLATE = """# Relay Shows

This shows the normal distribution for each show on the network

## Table of Contents:"""

    for show in all_episodes.sorted():
        url = re.sub(r'[^A-Za-z ]', '', show.title()).replace(' ', '-')

        TEMPLATE += "\n- [{0}](#{1})  ".format(show.title(), url)

    for show in all_episodes.sorted():
        TEMPLATE += "\n\n## {}\n\n".format(show.title())
        TEMPLATE += "**Longest episode:** {}  \n".format(
            show.get_longest_episode())
        TEMPLATE += "**Shortest episode:** {}  \n\n".format(
            show.get_shortest_episode())
        TEMPLATE += "![](images/{}.png)".format(quote(show.title()))

    with open('README.md', 'w') as f:
        f.write(TEMPLATE)
