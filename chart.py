import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def x_formatter(tick_val, tick_pos):
    return convert(tick_val)


def chart_show(show):

    # Generate some data for this
    # demonstration.
    data = [episode.seconds for episode in show]

    # Fit a normal distribution to
    # the data:
    # mean and standard deviation
    mu, std = norm.fit(data)

    fig, ax = plt.subplots()
    formatter = FuncFormatter(x_formatter)
    ax.xaxis.set_major_formatter(formatter)

    # Plot the histogram.
    plt.hist(data, bins=25, density=True, alpha=0.6, color='b')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)

    ax.plot(x, p, 'k', linewidth=2)
    title = "{}. Mean {} Average {}".format(
        show.title(), convert(mu), convert(std))
    ax.set_title(title)

    fig.savefig('images/' + show.title() + '.png')
