from urllib.parse import quote
import re
from datetime import datetime
import os


def create_network_page(network):
    TEMPLATE = "# {}".format(network.name)
    TEMPLATE += "\n\n## Table of Contents:"
    
    for show in network.show_durations.sorted():
        url = re.sub(r'[^A-Za-z ]', '', show.title()).replace(' ', '-')
        TEMPLATE += "\n- [{0}](#{1})  ".format(show.title(), url)

    TEMPLATE += "\n\n**Network's longest episode:** {}".format(
        network.show_durations.get_longest_episode().format())
    TEMPLATE += "\n\n**Network's shortest episode:** {}".format(
        network.show_durations.get_shortest_episode().format())

    for show in network.show_durations.sorted():
        TEMPLATE += "\n\n### {}\n\n".format(show.title())
        TEMPLATE += "**Longest episode:** {}  \n".format(
            show.get_longest_episode())
        TEMPLATE += "**Shortest episode:** {}  \n\n".format(
            show.get_shortest_episode())
        TEMPLATE += "![](../images/{}.png)".format(quote(show.title()))

    with open('networks/{}.md'.format(network.name.upper()), 'w') as f:
        f.write(TEMPLATE)
    


def update_readme(all_networks):
    if not os.path.exists('networks'):
        os.mkdir('networks')

    now = datetime.now()
    TEMPLATE = """# Podcast Network Stats

*Last updated on:* {now}

This displays the normal distribution for each show on the network. Data will be updated daily at midnight.

Visit each individual network's pages for show stats:  """.format(now=now.strftime("%Y-%m-%d %H:%M"))

    for network in all_networks:
        TEMPLATE += "\n\n- [{}](networks/{}.md)".format(network.name, network.name.upper())
        create_network_page(network)

    # TEMPLATE += "\n\n## Table of Contents:"
    # for network in all_networks:
    #     network_url = url = re.sub(
    #         r'[^A-Za-z ]', '', network.name).replace(' ', '-')
    #     TEMPLATE += "\n- [{0}](#{1})  ".format(network.name, network_url)

    #     for show in network.show_durations.sorted():
    #         url = re.sub(r'[^A-Za-z ]', '', show.title()).replace(' ', '-')
    #         TEMPLATE += "\n\t- [{0}](#{1})  ".format(show.title(), url)

    # for network in all_networks:
    #     TEMPLATE += "\n\n## {}  ".format(network.name)

    #     TEMPLATE += "\n\n**Network's longest episode:** {}".format(
    #         network.show_durations.get_longest_episode().format())
    #     TEMPLATE += "\n\n**Network's shortest episode:** {}".format(
    #         network.show_durations.get_shortest_episode().format())

    #     for show in network.show_durations.sorted():
    #         TEMPLATE += "\n\n### {}\n\n".format(show.title())
    #         TEMPLATE += "**Longest episode:** {}  \n".format(
    #             show.get_longest_episode())
    #         TEMPLATE += "**Shortest episode:** {}  \n\n".format(
    #             show.get_shortest_episode())
    #         TEMPLATE += "![](images/{}.png)".format(quote(show.title()))

    with open('README.md', 'w') as f:
        f.write(TEMPLATE)
