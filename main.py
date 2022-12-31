from relay import get_data
from chart import chart_show

data = get_data()

for show in data:
    chart_show(show)
