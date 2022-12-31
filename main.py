from relay import get_data
from chart import chart_show
from update_readme import update_readme

data = get_data()

for show in data:
    chart_show(show)

update_readme(data)
